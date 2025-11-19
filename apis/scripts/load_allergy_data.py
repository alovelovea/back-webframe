import os
import sys
import django
import csv

# ✅ 프로젝트 루트 경로 추가 (중요!)
# → C:\Users\alswo\Desktop\newproject 를 Python import 경로에 등록
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ✅ Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_fridge.settings')
django.setup()

# ✅ 모델 불러오기
from apis.models import Allergy
Allergy.objects.all().delete()
# ✅ CSV 파일 읽어서 삽입
with open('apis/data/Allergy.csv', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        Allergy.objects.create(
            allergy_name=row['allergy_name']
        )

print("✅ Allergy 데이터 삽입 완료!")
