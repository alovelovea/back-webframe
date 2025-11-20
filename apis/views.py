from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Person, Fridge, Ingredient, Like, Recipe, Allergy, PersonAllergy

# REST API용 import
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

# GPT 관련 import
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os, base64, mimetypes


# ------------------------------
# GPT 초기화
# ------------------------------
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
        print("⚠️ OPENAI_API_KEY가 설정되지 않아 ChatOpenAI를 비활성화합니다.")
except Exception as e:
    print(f"⚠️ ChatOpenAI 초기화 실패: {e}")


# ------------------------------
# GPT 이미지 분석 뷰
# ------------------------------
def classify_query_view(request):
    uploaded_file = request.FILES.get("image")
    base64_image_data = None
    media_type = "image/jpeg"

    if uploaded_file:
        try:
            media_type = uploaded_file.content_type or "image/jpeg"
            base64_image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
        except Exception:
            return JsonResponse({"detail": "failed to read uploaded file"}, status=400, safe=False)

    else:
        user_input = (request.POST.get("query") or request.GET.get("query") or "").strip()
        if not user_input:
            try:
                user_input = request.body.decode("utf-8").strip()
            except Exception:
                user_input = ""

        if not user_input:
            return JsonResponse({"detail": "empty query"}, status=400, safe=False)

        if user_input.lower().startswith(("http://", "https://")):
            return JsonResponse({"detail": "URL 입력은 지원하지 않습니다."}, status=400, safe=False)
        else:
            if not os.path.exists(user_input):
                return JsonResponse({"detail": f"file not found: {user_input}"}, status=400, safe=False)
            try:
                with open(user_input, "rb") as f:
                    base64_image_data = base64.b64encode(f.read()).decode("utf-8")
                media_type = mimetypes.guess_type(user_input)[0] or "image/jpeg"
            except Exception:
                return JsonResponse({"detail": "failed to read image path"}, status=400, safe=False)

    image_data_uri = f"data:{media_type};base64,{base64_image_data}"

    system_prompt = """
    [역할]
    당신은 냉장고 이미지 속 재료를 식별하고, 아래의 '재료 목록'과 '수량 판별 규칙'에 따라 각 항목의 정확한 수량을 판별하는 전문 분석가입니다.
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=[{"type": "image_url", "image_url": {"url": image_data_uri}}])
    ]

    response = llm_consistent.invoke(messages)
    food_list = response.content
    return JsonResponse(food_list, safe=False)


# ------------------------------
# 냉장고 관련 기능
# ------------------------------
def my_fridge(request):
    person = Person.objects.get(user_id='minjae01')  # 로그인 기능 적용 전까지는 고정 사용자
    fridge_items = Fridge.objects.filter(person=person)
    liked_recipes = Recipe.objects.filter(like__person=person)

    return render(request, 'fridge_app/my_fridge.html', {
        'person': person,
        'fridge_items': fridge_items,
        'liked_recipes': liked_recipes
    })


def add_ingredient(request):
    if request.method == 'POST':
        user_id = 'minjae01'  # 로그인 연동 시 변경
        ingredient_name = request.POST['ingredient']
        quantity = request.POST['quantity']
        added_date = request.POST['added_date']  # 🔥 exdate → added_date

        person = Person.objects.get(user_id=user_id)
        ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)

        Fridge.objects.create(
            person=person,
            ingredient=ingredient,
            f_quantity=quantity,
            added_date=added_date   # 🔥 expiry_date는 save()에서 자동 계산됨
        )
    return redirect('my_fridge')


def delete_ingredient(request, fridge_id):
    item = get_object_or_404(Fridge, pk=fridge_id)
    item.delete()
    return redirect('my_fridge')


def toggle_like(request, recipe_id):
    person = Person.objects.get(user_id='minjae01')
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    existing = Like.objects.filter(person=person, recipe=recipe)

    if existing.exists():
        existing.delete()
    else:
        Like.objects.create(person=person, recipe=recipe)
    return redirect('my_fridge')


# ------------------------------
# 로그인 API
# ------------------------------
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
            }, status=200)
        else:
            return JsonResponse({"error": "비밀번호가 일치하지 않습니다."}, status=401)

    except Person.DoesNotExist:
        return JsonResponse({"error": "존재하지 않는 사용자입니다."}, status=404)


# ------------------------------
# 회원가입 API
# ------------------------------
@api_view(['POST'])
@csrf_exempt
def signup_user(request):
    try:
        data = request.data
        name = data.get('name')
        address = data.get('address')
        user_id = data.get('user_id')
        password_2 = data.get('password_2')
        is_vegan = data.get('is_vegan', False)
        allergies = data.get('allergies', [])

        if Person.objects.filter(user_id=user_id).exists():
            return JsonResponse({"error": "이미 존재하는 아이디입니다."}, status=400)

        person = Person.objects.create(
            name=name,
            address=address,
            user_id=user_id,
            password_2=password_2,
            is_vegan=is_vegan
        )

        for allergy_name in allergies:
            allergy_obj, _ = Allergy.objects.get_or_create(allergy_name=allergy_name)
            PersonAllergy.objects.create(person=person, allergy=allergy_obj)

        return JsonResponse({
            "message": "회원가입 성공",
            "user_id": person.user_id,
            "name": person.name,
            "address": person.address,
            "is_vegan": person.is_vegan
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ------------------------------
# React용 냉장고 재료 조회 API
# ------------------------------
@api_view(['GET'])
@csrf_exempt
def fridge_items_api(request):
    user_id = request.GET.get('user_id')
    try:
        person = Person.objects.get(user_id=user_id)
        fridge_items = Fridge.objects.filter(person=person).select_related('ingredient')

        data = [
            {
                "ingredient": item.ingredient.ingredient_name,
                "quantity": float(item.f_quantity),
                "unit": item.ingredient.unit,
                "added_date": item.added_date.strftime("%Y-%m-%d"),
                "expiry_date": item.expiry_date.strftime("%Y-%m-%d")  # 🔥 변경 완료
            }
            for item in fridge_items
        ]
        return JsonResponse({"items": data}, status=200)

    except Person.DoesNotExist:
        return JsonResponse({"error": "존재하지 않는 사용자입니다."}, status=404)
