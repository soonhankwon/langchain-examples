from typing import List  # 타입 힌팅을 위한 List 타입
from langchain_community.llms import Ollama  # 일반 텍스트 생성을 위한 Ollama 모델
from langchain_community.chat_models import ChatOllama  # 대화형 응답을 위한 Ollama 채팅 모델
from langchain.schema import BaseOutputParser  # 출력 파서의 기본 클래스
from langchain.prompts import ChatPromptTemplate  # 채팅 프롬프트 템플릿

# Ollama 모델들을 초기화
llm = Ollama(model="llama3.1:8b", temperature=0.7)  # 일반 텍스트 생성 모델
chat_model = ChatOllama(model="llama3.1:8b", temperature=0.7)  # 채팅 모델

# 쉼표로 구분된 리스트를 파싱하는 커스텀 출력 파서를 정의
class CommaSeparatedListOutputParser(BaseOutputParser):
    def parse(self, text: str) -> List[str]:
        # 입력 텍스트를 쉼표로 분리하고 앞뒤 공백을 제거하여 리스트로 반환
        return text.strip().split(", ")
    
# 시스템 프롬프트 템플릿을 정의
template = """You are helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
ONLY return a comma seperated list, and noting more."""
# 사용자 입력을 위한 템플릿을 정의
human_template = "{text}"
# 채팅 프롬프트 템플릿을 생성
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

# LangChain Expression Language(LCEL)를 사용하여 체인을 구성
# 프롬프트 -> LLM -> 출력 파서 순서로 데이터가 흐름
chain = chat_prompt | llm | CommaSeparatedListOutputParser()
print(chain.invoke({"text" : "hip-hop genre"}))  # "hip-hop" 카테고리에 대한 5가지 항목을 생성
"""
['Gangsta Rap', 'Trap', 'Drill', 'Mafioso Rap', 'Conscious Hip-Hop']
"""