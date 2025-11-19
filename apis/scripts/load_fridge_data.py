import os
import sys
import django
import csv
from datetime import datetime

# ✅ Django 프로젝트 루트 등록
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ✅ Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_fridge.settings')
django.setup()

# ✅ 모델 불러오기
from apis.models import Fridge, Ingredient, Person

CSV_PATH = 'apis/data/Fridge.csv'

print("🧹 Fridge 데이터 전체 삭제 중...")
Fridge.objects.all().delete()
print("✅ 기존 데이터 삭제 완료!")

with open(CSV_PATH, encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        user_id = row['user_id'].strip()
        ingredient_name = row['ingredient_name'].strip()
        f_quantity = float(row['f_quantity'].strip())
        exdate_str = row['exdate'].strip()
        exdate = datetime.strptime(exdate_str, "%Y-%m-%d").date()

        try:
            person = Person.objects.get(user_id=user_id)
            ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)
            Fridge.objects.create(
                person=person,
                ingredient=ingredient,
                f_quantity=f_quantity,
                exdate=exdate
            )
            count += 1
            print(f"🧊 {user_id} 냉장고 ← {ingredient_name} ({f_quantity}, {exdate}) 추가됨")
        except Person.DoesNotExist:
            print(f"⚠️ 사용자 '{user_id}'를 찾을 수 없습니다.")
        except Ingredient.DoesNotExist:
            print(f"⚠️ 재료 '{ingredient_name}'를 찾을 수 없습니다.")

print(f"🎯 Fridge 데이터 {count}개 삽입 완료!")
