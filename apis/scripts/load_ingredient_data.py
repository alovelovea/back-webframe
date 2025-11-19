import os
import sys
import django
import csv

# ✅ Django 프로젝트 루트 경로 등록
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ✅ Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_fridge.settings')
django.setup()

# ✅ 모델 불러오기
from apis.models import Ingredient

# ✅ 파일 경로 설정
CSV_PATH = 'apis/data/Ingredient.csv'
PHOTO_BASE_PATH = 'photo/INGREDIENT/'  # DB에 저장될 상대경로 (data/photo/INGREDIENT)
Ingredient.objects.all().delete()
# ✅ CSV 읽어서 DB에 삽입
with open(CSV_PATH, encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        Ingredient.objects.create(
            ingredient_name=row['ingredient_name'],
            ingredient_img=os.path.join(PHOTO_BASE_PATH, row['ingredient_img']).replace("\\", "/"),
            unit=row['unit'],
            ingredient_category=row['ingredient_category'],
            price=int(row['price']) if row['price'] else 0  # ✅ price 필드 추가
        )

print("✅ Ingredient 데이터 삽입 완료!")
