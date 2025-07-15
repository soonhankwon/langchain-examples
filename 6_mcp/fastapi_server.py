import uvicorn
# main.py에서 FastAPI 애플리케이션 객체 임포트
from main import app

if __name__ == "__main__":
    # uvicorn 서버 실행
    uvicorn.run(
        "fastapi_server:app",  # 실행할 애플리케이션 모듈:변수명
        host="0.0.0.0",        # 모든 IP에서 접근 가능하도록 설정
        port=8000,             # 8000번 포트에서 실행
        reload=True,           # 코드 변경 시 자동 재시작 활성화
        log_level="info"       # 로그 레벨을 info로 설정
    ) 