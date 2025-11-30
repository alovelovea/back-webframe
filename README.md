# 🚀 프로젝트 실행 방법

** 반드시 Django 서버(백엔드)를 먼저 실행한 후, React(프론트엔드)를 실행하세요!**

---

## 1. 백엔드 실행 (필수)

### 1-1. 가상환경 생성 및 활성화 (최상위 디렉토리에서 실행)

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

### 1-2. 필요한 패키지 설치
통합 스크립트를 실행하면 모든 CSV 데이터가 DB에 자동으로 로드됩니다.

```bash
pip install -r requirements.txt
```

### 1-3. 데이터베이스 초기 설정 

```bash
python manage.py makemigrations
python manage.py migrate
```

### 1-4. CSV 기반 전체 데이터 자동 로드

```bash
python apis/scripts/load_all_data.py
```

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
