# Langchain 라이브러리에서 필요한 모듈들을 가져옵니다
from langchain_community.llms import Ollama  # 일반 텍스트 생성을 위한 Ollama 모델
from langchain_community.chat_models import ChatOllama  # 대화형 응답을 위한 Ollama 채팅 모델
from langchain.schema import SystemMessage, HumanMessage  # 채팅 메시지 타입 정의

# 일반 텍스트 생성을 위한 Ollama 모델을 초기화합니다
# temperature가 0.7로 설정되어 적당한 창의성을 가진 응답을 생성합니다
llm = Ollama(model="llama3.1:8b", temperature=0.7)

# 대화형 응답을 위한 Ollama 채팅 모델을 초기화합니다
# 일반 모델과 동일한 설정을 사용합니다
chat_model = ChatOllama(model="llama3.1:8b", temperature=0.7)

# 모델에게 물어볼 질문을 정의합니다
text = "힙합가사 한 소절을 작성해줘"

# 채팅 모델에 전달할 메시지 목록을 생성합니다
# SystemMessage: 모델의 페르소나를 정의합니다 (랩퍼 역할)
# HumanMessage: 실제 사용자의 질문을 담습니다
messages = [
    SystemMessage(content="당신은 랩퍼입니다."),
    HumanMessage(content=text),
]

# 일반 텍스트 모델을 사용하여 응답을 생성하고 출력합니다
print("일반 텍스트 응답:")
print(llm.invoke(text))

# 채팅 모델을 사용하여 랩퍼 페르소나로 응답을 생성하고 출력합니다
print("\n채팅 모델 응답:")
print(chat_model.invoke(messages))
