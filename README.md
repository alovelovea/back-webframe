# 🍀 Back-WebFrame (Django Backend)

이 저장소는 **Django 기반 백엔드 서버 프로젝트**입니다.  
냉장고 재료 관리, 레시피 추천, 알러지 기반 필터링 기능을 제공합니다.

아래 가이드를 따르면 저장소를 **클론한 후 바로 실행**할 수 있습니다.

---

## 🚀 1. 프로젝트 클론

```bash
git clone https://github.com/alovelovea/back-webframe.git
cd back-webframe
```

---

## 🚀 2. 가상환경 생성 및 활성화

### 🔹 Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 🔹 Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 🚀 3. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

> Django, DRF, CORS, LangChain 등 모든 의존성이 자동 설치됩니다.

---

## 🚀 4. 데이터베이스 초기 설정 (Migration)

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🚀 5. CSV 기반 전체 데이터 자동 로드

통합 스크립트를 실행하면 모든 CSV 데이터가 DB에 자동으로 로드됩니다.

```bash
python apis/scripts/load_all_data.py
```

### 📌 데이터 로드 순서

1. Allergy  
2. Ingredient  
3. Person  
4. PersonAllergy  
5. AllergyIngredient  
6. Recipe  
7. RecipeIngredient  
8. Fridge  
9. Like  
10. Shopping
---

## 🚀 6. 서버 실행

```bash
python manage.py runserver
```

서버 접속 주소:

👉 http://127.0.0.1:8000/

---

## 🔑 7. 관리자(Admin) 계정 생성 (선택) id, pw 설정 후 사용. 데이터베이스 보기 좋음
<img width="2559" height="1205" alt="image" src="https://github.com/user-attachments/assets/8842430f-c928-4b95-b201-1e0a14f24a79" />

```bash
python manage.py createsuperuser
```

관리자 페이지:

👉 http://127.0.0.1:8000/admin/

---

## 📁 프로젝트 구조

```
back-webframe/
├── apis/
│   ├── data/
│   ├── scripts/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── project_fridge/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── requirements.txt
├── manage.py
└── .gitignore
```

---

## 🔧 기술 스택

- Python 3.10  
- Django 5.x  
- Django REST Framework  
- django-cors-headers  
- LangChain + OpenAI  
- SQLite3  
- CSV 기반 데이터 자동 로드

---


