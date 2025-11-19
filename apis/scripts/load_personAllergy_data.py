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
from apis.models import Person, Allergy, PersonAllergy

# ✅ CSV 파일 경로
CSV_PATH = 'apis/data/PersonAllergy.csv'

# ✅ 기존 데이터 전체 삭제
print("🧹 기존 PersonAllergy 데이터 삭제 중...")
PersonAllergy.objects.all().delete()
print("✅ 기존 데이터 삭제 완료!")

# ✅ CSV 읽어서 DB에 삽입
with open(CSV_PATH, encoding='utf-8') as file:
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        try:
            # 🔥 수정된 부분: user_id 컬럼으로 조회
            person = Person.objects.get(user_id=row['user_id'])
            allergy = Allergy.objects.get(allergy_name=row['allergy_name'])
            
            PersonAllergy.objects.create(
                person=person,
                allergy=allergy
            )
            count += 1
        except Person.DoesNotExist:
            print(f"⚠️ 사용자 '{row['user_id']}' 를 찾을 수 없습니다.")
        except Allergy.DoesNotExist:
            print(f"⚠️ 알러지 '{row['allergy_name']}' 를 찾을 수 없습니다.")
        except Exception as e:
            print(f"❌ 삽입 중 오류 발생: {e}")

print(f"✅ PersonAllergy 데이터 {count}개 삽입 완료!")
