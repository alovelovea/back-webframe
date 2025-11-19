import os
import sys
import django
import csv

# ✅ Django 프로젝트 루트 등록
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ✅ Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_fridge.settings')
django.setup()

# ✅ 모델 불러오기
from apis.models import RecipeIngredient, Recipe, Ingredient

CSV_PATH = 'apis/data/RecipeIngredient.csv'

print("🧹 RecipeIngredient 데이터 전체 삭제 중...")
RecipeIngredient.objects.all().delete()
print("✅ 기존 데이터 삭제 완료!")

with open(CSV_PATH, encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        recipe_name = row['recipe_name'].strip()
        ingredient_name = row['ingredient_name'].strip()
        r_quantity = float(row['r_quantity'].strip())

        try:
            recipe = Recipe.objects.get(recipe_name=recipe_name)
            ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, r_quantity=r_quantity)
            count += 1
            print(f"🥣 {recipe_name} ← {ingredient_name} ({r_quantity}) 추가됨")
        except Recipe.DoesNotExist:
            print(f"⚠️ 레시피 '{recipe_name}'를 찾을 수 없습니다.")
        except Ingredient.DoesNotExist:
            print(f"⚠️ 재료 '{ingredient_name}'를 찾을 수 없습니다.")

print(f"🎯 RecipeIngredient 데이터 {count}개 삽입 완료!")
