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
from apis.models import Like, Person, Recipe

# ✅ CSV 파일 경로
CSV_PATH = 'apis/data/Like.csv'

# ✅ 기존 데이터 전체 삭제
print("🧹 기존 Like 데이터 삭제 중...")
Like.objects.all().delete()
print("✅ 기존 데이터 삭제 완료!")

# ✅ CSV 읽어서 DB에 삽입
with open(CSV_PATH, encoding='utf-8') as file:
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        try:
            person = Person.objects.get(user_id=row['user_id'])
            recipe = Recipe.objects.get(recipe_name=row['recipe_name'])
            Like.objects.create(person=person, recipe=recipe)
            count += 1
        except Person.DoesNotExist:
            print(f"⚠️ 사용자 '{row['user_id']}' 를 찾을 수 없습니다.")
        except Recipe.DoesNotExist:
            print(f"⚠️ 레시피 '{row['recipe_name']}' 를 찾을 수 없습니다.")

print(f"✅ Like 데이터 {count}개 삽입 완료!")
