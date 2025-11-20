import os
import sys
import django
import csv
from datetime import datetime
from decimal import Decimal

# Django 프로젝트 루트 등록
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_fridge.settings')
django.setup()

# 모델 불러오기
from apis.models import Shopping, Person, Ingredient

CSV_PATH = 'apis/data/Shopping.csv'

print("🧹 Shopping 데이터 전체 삭제 중...")
Shopping.objects.all().delete()
print("✅ Shopping 기존 데이터 삭제 완료!")

with open(CSV_PATH, encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    count = 0

    for row in reader:

        user_id = row['user_id'].strip()
        ingredient_name = row['ingredient_name'].strip()

        # 🔥 quantity 안전 파싱
        quantity_raw = row['quantity'].strip().split()[0]
        quantity = Decimal(quantity_raw)

        # 🔥 purchased_date 안전 파싱
        date_raw = row['purchased_date'].strip().split()[0]
        purchased_date = datetime.strptime(date_raw, "%Y-%m-%d").date()

        try:
            person = Person.objects.get(user_id=user_id)
            ingredient = Ingredient.objects.get(ingredient_name=ingredient_name)

            shopping = Shopping.objects.create(
                person=person,
                ingredient=ingredient,
                quantity=quantity,
                purchased_date=purchased_date
            )

            count += 1
            print(f"🛒 쇼핑 추가됨 → {user_id} / {ingredient_name} / {quantity}개 / {purchased_date}")

        except Person.DoesNotExist:
            print(f"⚠ 사용자 '{user_id}' 없음")
        except Ingredient.DoesNotExist:
            print(f"⚠ 재료 '{ingredient_name}' 없음")

print(f"\n🎯 총 {count}개의 쇼핑 데이터 삽입 완료!")
