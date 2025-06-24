# 필요한 라이브러리들을 임포트
from typing import List  # 타입 힌팅을 위한 List 타입
from langchain_community.llms import Ollama  # 일반 텍스트 생성을 위한 Ollama 모델
from langchain.prompts import PromptTemplate  # 프롬프트 템플릿 생성을 위한 클래스
from langchain.output_parsers import PydanticOutputParser  # Pydantic 모델 기반 출력 파서
from pydantic import BaseModel, Field  # Pydantic 모델 정의를 위한 클래스들

# Ollama LLM 모델 초기화 (temperature가 높을수록 더 창의적인 출력)
llm = Ollama(model="llama3.1:8b", temperature=0.7)

# 래퍼 정보를 담을 Pydantic 모델 클래스 정의
class Rapper(BaseModel):
    name: str = Field(description="The name of the rapper")  # 래퍼의 이름
    file_name: List[str] = Field(description="list of names of albums they featured in")  # 앨범 목록

# 사용자 쿼리 정의 - 무작위 래퍼의 앨범 목록 생성 요청
rapper_query = "Pick a random rapper and list their album names. Do not pick Kendrick Lamar every time."

# Pydantic 모델을 기반으로 출력 파서 생성
parser = PydanticOutputParser(pydantic_object=Rapper)

# 프롬프트 템플릿 생성
# - format_instructions: Pydantic 모델에 맞는 출력 형식 안내
# - query: 사용자 쿼리가 들어갈 부분
prompt = PromptTemplate(
    template=(
        "Answer the user query as a JSON object that matches the following example:\n"
        "{format_instructions}\n"
        "{query}\n"
    ),
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# 프롬프트에 쿼리를 포맷팅하여 입력 생성
_input = prompt.format(query=rapper_query)
# LLM에 입력을 전달하여 응답 받기
output = llm.invoke(_input)
# 응답을 Pydantic 모델 형식으로 파싱하여 출력
print(parser.parse(output))
"""
name='Kendrick Lamar' file_name=['Good Kid, M.A.A.D City', 'To Pimp a Butterfly', 'DAMN.', 'Section.80']
"""