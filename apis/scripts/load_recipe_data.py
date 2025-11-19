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
from apis.models import Recipe

Recipe.objects.all().delete()
# ✅ 파일 경로 설정
CSV_PATH = 'apis/data/Recipe.csv'
PHOTO_BASE_PATH = 'photo/FOOD/'  # DB에 저장될 상대경로 (data/photo/INGREDIENT)
Recipe.objects.all().delete()
with open(CSV_PATH, encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        Recipe.objects.create(
            recipe_name=row['recipe_name'],
            description=row['description'],
            recipe_img=os.path.join(PHOTO_BASE_PATH, row['recipe_img']).replace("\\", "/"),
            recipe_category=row['recipe_category']
        )

print("✅ Recipe 데이터 삽입 완료!")
