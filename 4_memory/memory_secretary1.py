from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain

chat_model = ChatOllama(model="llama3.1:8b", temperature=0.3)

# 메모리 객체 생성
memory = ConversationSummaryBufferMemory(llm=chat_model, max_token_limit=200)

conversation = ConversationChain(
    llm=chat_model, 
    memory=memory,
    prompt=PromptTemplate(
        input_variables=["history", "input"],
        template="""당신은 최고의 운전 보조 AI 어시스턴트입니다. 운전자의 안전하고 편안한 주행을 위해 필요한 정보를 제공하고 도와주세요.
        실시간 교통 정보, 최적 경로 안내, 주변 시설물(주유소, 주차장, 맛집 등) 검색, 차량 상태 점검, 운전 중 간단한 메모 작성 등을 도와줄 수 있습니다.
        항상 명확하고 간결한 음성 안내 스타일로 답변해주세요. 운전자의 안전을 최우선으로 생각하며, 주행에 방해되지 않도록 간결하게 소통하세요.
        
        이전 대화 내용:
        {history}
        
        사용자: {input}
        AI 어시스턴트: """
    )
)

# 시작 멘트
print("\n" + "="*50)
print("🤖 AI 운전비서입니다. 무엇을 도와드릴까요? 🤖")
print("="*50 + "\n")

# 대화 예시
while True:
    user_input = input("말씀해주세요 (종료하시려면 'q' 입력): ")
    if user_input.lower() == 'q':
        print("\n오늘도 좋은 하루 보내세요. 필요하실 때 언제든 불러주세요!\n")
        break
        
    response = conversation.predict(input=user_input)
    print(f"\nAI 운전비서: {response}\n")
    print("="*50 + "\n")

"""
==================================================
🤖 AI 운전비서입니다. 무엇을 도와드릴까요? 🤖
==================================================

말씀해주세요 (종료하시려면 'q' 입력): 분당에서 주차되는 플레이스 3곳만 추천해줘

AI 운전비서: 분당 지역의 주차장입니다.

1.  **분당역주차장**: 분당역 인근에 위치한 대형 주차장이며, 24시간 운영합니다.
2.  **성남시민운동장주차장**: 성남시민운동장 인근에 있는 주차장으로, 주말에는 무료 주차가 가능합니다.
3.  **분당고등학교주차장**: 분당고등학교 인근의 주차장이며, 주간에는 무료 주차가 가능합니다.

위 주차장들은 모두 분당 지역에서 쉽게 찾을 수 있으며, 주변 시설물로 가는 데 도움이 될 것입니다.

==================================================

말씀해주세요 (종료하시려면 'q' 입력): 분당역 주차장 운영시간은 몇시간이야?

AI 운전비서: 분당역 주차장은 24시간 운영합니다.

==================================================

말씀해주세요 (종료하시려면 'q' 입력): 분당고등학교주차장은 주간에는 주차비가 얼마야?

AI 운전비서: 분당고등학교 주차장은 주간에는 무료 주차입니다.

==================================================
"""