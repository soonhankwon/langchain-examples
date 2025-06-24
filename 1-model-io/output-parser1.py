from typing import List  # 타입 힌팅을 위한 List 타입
from langchain_community.llms import Ollama  # 일반 텍스트 생성을 위한 Ollama 모델
from langchain_community.chat_models import ChatOllama  # 대화형 응답을 위한 Ollama 채팅 모델
from langchain.prompts import ChatPromptTemplate  # 채팅 프롬프트 템플릿
from langchain.prompts import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser

# Ollama 모델들을 초기화
llm = Ollama(model="llama3.1:8b", temperature=0.7)  # 일반 텍스트 생성 모델

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()

# check what expect to LLM
prompt = PromptTemplate(
    template="List five {subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)

_input = prompt.format(subject="hip-hop genre")
output = llm.invoke(_input)
print(output_parser.parse(output))
"""
['Here are 5 hip-hop genres:', 'Trap', 'Drill', 'Gangsta Rap', 'Conscious Rap', 'Old School Hip Hop']
"""

