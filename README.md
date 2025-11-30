
# 🚀 프로젝트 실행 방법

** 반드시 Django 서버(백엔드)를 먼저 실행한 후, React(프론트엔드)를 실행하세요!**

---

## 1. 백엔드 실행 (필수)

### 1-1. 가상환경 생성 및 활성화 (최상위 디렉토리에서 실행)

> venv 이름으로 새로운 가상환경을 생성합니다.

```bash
python -m venv venv
.\venv\Scripts\activate
```
---

### 1-2. 필요한 패키지 설치

> requirements.txt에 기재된 Django, DRF, CORS, LangChain 등
프로젝트 실행에 필요한 모든 라이브러리를 자동으로 설치합니다.

```bash
pip install -r requirements.txt
```

### 1-3. 데이터베이스 초기 설정 

---

> makemigrations: models.py 변경사항을 기반으로 마이그레이션 파일 생성합니다.
> migrate: 실제 SQLite(DB)에 테이블을 생성합니다.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 1-4. CSV 기반 전체 데이터 자동 로드
---
> 통합 스크립트를 실행하면 모든 CSV 데이터가 DB에 자동으로 로드됩니다.
> Ingredient.csv, allergy.csv, Fridge.csv... 등 내가 작성해 놓은 csv파일을 기반으로 알맞은 model에 저장됩니다.

```bash
python apis/scripts/load_all_data.py
```

#### ✔ 데이터 로드 상세 설명

load_all_data.py 스크립트는 아래 순서대로 CSV 데이터를 DB에 삽입합니다:

1. **Allergy**  
   - 알러지 (ex 갑각류)

2. **Ingredient**  
   - 재료 (ex 새우)

3. **Person**  
   - 사용자 (ex 민재)

4. **PersonAllergy**  
   - 사용자와 알러지의 관계 매핑 (ex 민재는 갑각류알러지)

5. **AllergyIngredient**  
   - 재료와 알러지 매핑 (ex 새우는 갑각류)

6. **Recipe**  
   - 레시피 (ex 알리올리오)

7. **RecipeIngredient**  
   - 각 레시피가 필요로 하는 재료와 양을 매핑 (ex 알리올리오는 새우를 3개 사용)

8. **Fridge**  
   - 사용자와 재료 관계 매핑 (ex 민재는 냉장고에 새우가 3개 있음)

9. **Like**  
   - 사용자와 레시피 좋아요 관계 매핑 (ex 민재는 알리올리오를 좋아요 표시함)

10. **Shopping**  
   - 쇼핑 (ex 민재가 새우를 3개 삼)
---
### 1-5. 서버 실행

```bash
python manage.py runserver
```
---

## 2. React 실행

### 2-1. client 폴더로 이동 후 실행

```bash
npm install
npm start
```
---

# 🛠 실행 환경(Environment)

본 프로젝트는 **Django(백엔드)** + **React(프론트엔드)**로 구성된 풀스택 웹 애플리케이션입니다.  
아래 환경에서 정상적으로 동작하도록 구성되어 있으며, 동일한 환경을 갖추는 것을 권장합니다.

---

### 1. 공통 실행 환경

| 항목 | 요구 버전 |
|------|-----------|
| **Python** | 3.10 이상 권장 |
| **Node.js** | 18.x 이상 |
| **npm** | 9.x 이상 |
| **Git** | 최신 버전 |
| **OS** | Windows 10+, macOS, Linux 모두 지원 |

---

### 2. 백엔드 (Django) 실행 환경

Django API 서버는 다음 구성에서 실행됩니다:

- **Django 5.x**
- **Django REST Framework**
- **CORS Headers**
- **SQLite3 (기본 DB)**
- **LangChain / OpenAI 연동 사용 가능**
- **Python venv 가상환경 기반 실행**

####  Python 패키지 의존성
아래 모든 패키지는 `requirements.txt`에서 자동 설치됩니다.

- django  
- djangorestframework  
- django-cors-headers  
- langchain  
- pillow  
- etc...

---

### 3. 프론트엔드 (React) 실행 환경

React는 다음 라이브러리들을 기반으로 실행됩니다:

- **React 18**
- **React Router**
- **Axios**
- **CSS / Tailwind(optional)**
- **Radix UI(optional)**

####  Node 패키지 의존성
`npm install` 실행 시 자동 설치됩니다.

- react  
- react-dom  
- react-router-dom  
- axios  
- 기타 component/UI 패키지  

---

### 📁 프로젝트 구조

```
폴더
├─ apis/ # Django 앱 
│ ├─ models/ # DB 모델 정의
│ ├─ views/ # API View 함수
│ ├─ scripts/ # CSV 자동 로드 스크립트
│ ├─ urls.py # 앱 URL 매핑
│ └─ ...
│
├─ client/ # React 프론트엔드
│ ├─ src/ # React 컴포넌트/페이지/상태관리 등
│ ├─ public/ # 정적 리소스
│ └─ ...
│
├─ project_fridge/ # Django 프로젝트 루트 
│ ├─ init.py
│ ├─ settings.py # Django 전체 설정 파일
│ ├─ urls.py # 전체 URL 라우팅 엔트리
│ ├─ wsgi.py # WSGI 서버 설정
│ └─ asgi.py # ASGI 서버 설정
│
├─ README.md 
├─ manage.py # Django 실행 파일
├─ ...
```
