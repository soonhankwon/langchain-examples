# Supabase User MCP Server

FastAPI와 Supabase를 사용하여 특정 유저 정보를 조회하는 MCP (Model Context Protocol) 서버입니다.

## 기능

- 특정 유저 정보 조회

## 설치

1. 의존성 설치:
```bash
pip install -e .
```

2. 환경 변수 설정:
```bash
cp env.example .env
```

`.env` 파일에 Supabase 연결 정보를 입력하세요:
```
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

## 사용법

### MCP 서버 실행
```bash
python main.py
```

### FastAPI 서버 실행 (개발용)
```bash
python fastapi_server.py
```

서버가 실행되면 `http://localhost:8000`에서 API 문서를 확인할 수 있습니다.

## API 엔드포인트

- `GET /users/{user_id}` - 특정 유저 조회 (user_id는 정수)

## MCP 도구

- `get_user_by_id` - 특정 ID의 유저 정보 가져오기 (user_id는 정수)

## 테스트

API 테스트를 실행하려면:
```bash
python test_api.py
```

테스트할 유저 ID(정수)를 입력하면 해당 유저의 정보를 조회합니다.
