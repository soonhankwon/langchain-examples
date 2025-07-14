from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("다음 주제에 대해 설명해줘: {topic}")

chat_model = ChatOllama(model="llama3.1:8b", temperature=0.3)

# 프롬프트와 모델을 연결하여 체인 생성
chain = prompt | chat_model

from fastapi import FastAPI
from langserve import add_routes

# FastAPI 앱 생성
app = FastAPI(title="LangServe Example", description="LangServe Example")

# /explain 경로에 체인 라우트 추가
add_routes(
    app,
    chain,
    path="/explain"
)

# 메인 실행 코드
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)  # localhost:8001에서 서버 실행

"""
# API 호출 예시:
curl -X POST "http://localhost:8001/explain/invoke" \
     -H "Content-Type: application/json" \
     -d '{"input": {"topic": "인공지능"}}'
"""