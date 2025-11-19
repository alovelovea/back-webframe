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
from apis.models import AllergyIngredient, Ingredient, Allergy

# ✅ 파일 경로 설정
CSV_PATH = 'apis/data/AllergyIngredient.csv'

# ✅ 기존 데이터 삭제
print("🧹 AllergyIngredient 데이터 전체 삭제 중...")
AllergyIngredient.objects.all().delete()
print("✅ 기존 데이터 삭제 완료!")

# ✅ CSV 읽어서 이름으로 매핑 후 삽입
with open(CSV_PATH, encoding='utf-8-sig') as file:  # ← BOM 제거
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        ingredient_name = row['ingredient_name'].strip()  # ← 공백 제거
        allergy_name = row['allergy_name'].strip()        # ← 공백 제거
        try:
            ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)
            allergy = Allergy.objects.get(allergy_name=allergy_name)
            AllergyIngredient.objects.create(ingredient=ingredient, allergy=allergy)
            count += 1
        except Ingredient.DoesNotExist:
            print(f"⚠️ 재료 '{ingredient_name}'를 찾을 수 없습니다.")
        except Allergy.DoesNotExist:
            print(f"⚠️ 알러지 '{allergy_name}'를 찾을 수 없습니다.")

print(f"✅ AllergyIngredient 데이터 {count}개 삽입 완료!")
