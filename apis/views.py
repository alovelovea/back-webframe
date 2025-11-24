from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage

from .models import (
    Person, Fridge, Ingredient, Like, Recipe,
    Allergy, PersonAllergy, RecipeIngredient
)

# REST API용 import
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

# GPT 관련 import
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os, base64, mimetypes, json


# ============================
# GPT 초기화
# ============================
llm_consistent = None
try:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        llm_consistent = ChatOpenAI(
            model='gpt-4o',
            temperature=0,
            max_tokens=1000,
            top_p=0.3,
            frequency_penalty=0.1,
        )
    else:
        print("⚠️ OPENAI_API_KEY 없음 → GPT 비활성화")
except Exception as e:
    print(f"⚠️ ChatOpenAI 초기화 실패: {e}")


# ============================
# GPT 이미지 분석
# ============================
def classify_query_view(request):
    uploaded_file = request.FILES.get("image")
    base64_image_data = None
    media_type = "image/jpeg"

    if uploaded_file:
        media_type = uploaded_file.content_type or "image/jpeg"
        base64_image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
    else:
        return JsonResponse({"detail": "이미지가 없습니다."}, status=400)

    image_data_uri = f"data:{media_type};base64,{base64_image_data}"

    system_prompt = """
    재료 분석 전문가 역할을 수행하세요.
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=[{"type": "image_url", "image_url": {"url": image_data_uri}}])
    ]

    response = llm_consistent.invoke(messages)
    return JsonResponse(response.content, safe=False)


# ============================
# 냉장고 관련
# ============================
def my_fridge(request):
    person = Person.objects.get(user_id='minjae01')
    fridge_items = Fridge.objects.filter(person=person)
    liked_recipes = Recipe.objects.filter(like__person=person)

    return render(request, "fridge_app/my_fridge.html", {
        'person': person,
        'fridge_items': fridge_items,
        'liked_recipes': liked_recipes
    })


def add_ingredient(request):
    if request.method == 'POST':
        user_id = 'minjae01'
        person = Person.objects.get(user_id=user_id)

        ingredient_name = request.POST["ingredient"]
        quantity = request.POST["quantity"]
        added_date = request.POST["added_date"]

        ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)

        Fridge.objects.create(
            person=person,
            ingredient=ingredient,
            f_quantity=quantity,
            added_date=added_date
        )
    return redirect("my_fridge")


def delete_ingredient(request, fridge_id):
    item = get_object_or_404(Fridge, pk=fridge_id)
    item.delete()
    return redirect("my_fridge")


def toggle_like(request, recipe_id):
    person = Person.objects.get(user_id='minjae01')
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    existing = Like.objects.filter(person=person, recipe=recipe)
    if existing.exists():
        existing.delete()
    else:
        Like.objects.create(person=person, recipe=recipe)

    return redirect("my_fridge")


# ============================
# 로그인
# ============================
@api_view(['POST'])
@csrf_exempt
def login_user(request):
    user_id = request.data.get('user_id')
    password_2 = request.data.get('password_2')

    try:
        person = Person.objects.get(user_id=user_id)
        if person.password_2 == password_2:
            return JsonResponse({
                "message": "로그인 성공",
                "user_id": person.user_id,
                "name": person.name,
                "address": person.address,
                "is_vegan": person.is_vegan
            })
        return JsonResponse({"error": "비밀번호가 틀렸습니다."}, status=401)

    except Person.DoesNotExist:
        return JsonResponse({"error": "존재하지 않는 사용자입니다."}, status=404)


# ============================
# 회원가입
# ============================
@api_view(['POST'])
@csrf_exempt
def signup_user(request):
    try:
        data = request.data
        user_id = data.get("user_id")
        name = data.get("name")
        password_2 = data.get("password_2")
        address = data.get("address")
        is_vegan = data.get("is_vegan", False)
        allergies = data.get("allergies", [])

        if Person.objects.filter(user_id=user_id).exists():
            return JsonResponse({"error": "이미 존재하는 아이디입니다."}, status=400)

        person = Person.objects.create(
            user_id=user_id, name=name,
            password_2=password_2,
            address=address, is_vegan=is_vegan
        )

        for allergy_name in allergies:
            allergy_obj, _ = Allergy.objects.get_or_create(allergy_name=allergy_name)
            PersonAllergy.objects.create(person=person, allergy=allergy_obj)

        return JsonResponse({"message": "회원가입 완료"}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ============================
# 냉장고 조회 API
# ============================
@api_view(['GET'])
def fridge_items_api(request):
    user_id = request.GET.get("user_id")
    person = Person.objects.get(user_id=user_id)

    fridge_items = Fridge.objects.filter(person=person).select_related("ingredient")

    data = [
        {
            "ingredient": f.ingredient.ingredient_name,
            "quantity": float(f.f_quantity),
            "unit": f.ingredient.unit,
            "added_date": f.added_date.strftime("%Y-%m-%d"),
            "expiry_date": f.expiry_date.strftime("%Y-%m-%d")
        }
        for f in fridge_items
    ]

    return JsonResponse({"items": data})


# ============================
# 레시피 리스트 API
# ============================
@api_view(['GET'])
def recipe_list_api(request):
    user_id = request.GET.get("user_id")
    person = Person.objects.get(user_id=user_id)

    recipes = Recipe.objects.all()
    liked_ids = Like.objects.filter(person=person).values_list("recipe_id", flat=True)

    data = []
    for r in recipes:
        ing_list = RecipeIngredient.objects.filter(recipe=r)
        ingredients = [
            f"{ri.ingredient.ingredient_name} {float(ri.r_quantity)}{ri.ingredient.unit}"
            for ri in ing_list
        ]

        data.append({
            "id": r.recipe_id,
            "name": r.recipe_name,
            "category": r.recipe_category,
            "image": r.recipe_img,
            "ingredients": ", ".join(ingredients),
            "favorite": r.recipe_id in liked_ids
        })

    return JsonResponse({"recipes": data})


# ===========================
# 🔥 1) 재료 목록 제공 API (프론트에서 선택 UI를 만들 때 사용)
# ===========================
@api_view(['GET'])
def ingredient_list(request):
    ingredients = Ingredient.objects.all()

    data = [
        {
            "name": ing.ingredient_name,
            "category": ing.ingredient_category
        }
        for ing in ingredients
    ]

    return JsonResponse({"ingredients": data}, status=200)



# ===========================
# 🔥 2) 레시피 저장 API
# ===========================
@api_view(['POST'])
@csrf_exempt
def add_recipe(request):
    try:
        # --- 기본 정보 ---
        name = request.POST.get("name")
        description = request.POST.get("description")
        category = request.POST.get("category")
        ingredients = json.loads(request.POST.get("ingredients", "[]"))
        image_file = request.FILES.get("image")

        # -------------------------
        # 1) Recipe 생성
        # -------------------------
        recipe = Recipe.objects.create(
            recipe_name=name,
            description=description,
            recipe_category=category
        )

        # -------------------------
        # 2) 이미지 파일 저장
        # -------------------------
        if image_file:
            save_path = default_storage.save(f"recipes/{image_file.name}", image_file)
            recipe.recipe_img = settings.MEDIA_URL + save_path
            recipe.save()

        # -------------------------
        # 3) RecipeIngredient 생성
        #    재료 이름만 넘어온다고 가정.
        #    수량은 기본 1로 저장.
        # -------------------------
        for ing_name in ingredients:
            ingredient = Ingredient.objects.get(ingredient_name=ing_name)

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                r_quantity=1  # 기본 1개로 저장
            )

        return JsonResponse({"message": "레시피 저장 완료", "recipe_id": recipe.recipe_id}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ============================
# 🔥 레시피 상세 조회 API (추가)
# ============================
@api_view(['GET'])
def recipe_detail_api(request, recipe_id):
    try:
        recipe = Recipe.objects.get(recipe_id=recipe_id)

        # 재료 목록 가져오기
        ing_list = RecipeIngredient.objects.filter(recipe=recipe)
        ingredients_list = [
            f"{ri.ingredient.ingredient_name} {float(ri.r_quantity)}{ri.ingredient.unit}"
            for ri in ing_list
        ]

        data = {
            "id": recipe.recipe_id,
            "name": recipe.recipe_name,
            "image": recipe.recipe_img,
            "category": recipe.recipe_category,
            "description": recipe.description or "",
            "ingredients_list": ingredients_list,
        }

        return JsonResponse(data, status=200)

    except Recipe.DoesNotExist:
        return JsonResponse({"error": "레시피를 찾을 수 없습니다."}, status=404)