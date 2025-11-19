import os, sys, django, csv

# Django 환경
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_fridge.settings')
django.setup()

from apis.models import Person

CSV_PATH = 'apis/data/Person.csv'  # 파일명/경로 확인

def to_bool(s):
    return str(s).strip().lower() in ('true','1','y','yes','t')

def main():
    # 필요시 초기화 -> 주석 해제
    # Person.objects.all().delete()

    inserted = updated = 0
    with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            obj, created = Person.objects.update_or_create(
                user_id=row['user_id'].strip(),
                defaults={
                    'name': row.get('name','').strip(),
                    'password_2': (row.get('password_2') or '').strip(),
                    'address': row.get('address','').strip(),
                    'is_vegan': to_bool(row.get('is_vegan','')),
                }
            )
            inserted += int(created)
            updated  += int(not created)
    print(f"✅ Person 삽입 {inserted}건, 갱신 {updated}건 완료")

if __name__ == '__main__':
    main()
