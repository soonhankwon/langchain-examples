from typing import List  # 타입 힌팅을 위한 List 타입
from langchain_community.llms import Ollama  # 일반 텍스트 생성을 위한 Ollama 모델
from langchain.schema import BaseOutputParser  # 출력 파서의 기본 클래스
from langchain.prompts import ChatPromptTemplate  # 채팅 프롬프트 템플릿

# Ollama 모델들을 초기화
llm = Ollama(model="llama3.1:8b", temperature=0.7)  # 일반 텍스트 생성 모델