from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# 메모리 객체 생성
memory = ConversationBufferMemory()

# 대화 체인 생성
chat_model = ChatOllama(model="llama3.1:8b", temperature=0.3)
conversation = ConversationChain(
    llm=chat_model, 
    memory=memory,
    prompt=PromptTemplate(
        input_variables=["history", "input"],
        template="""당신은 전문적이고 효율적인 AI 개인비서입니다. 사용자의 일정, 업무, 생활 전반을 관리하고 도와주세요.
        업무 일정 관리, 이메일 작성 보조, 정보 검색, 일상적인 조언 등 다양한 방면에서 도움을 제공해주세요.
        항상 정중하고 프로페셔널한 태도를 유지하세요.
        
        이전 대화 내용:
        {history}
        
        사용자: {input}
        비서: """
    )
)

# 시작 멘트
print("\n" + "="*50)
print("🤖 AI 비서입니다. 무엇을 도와드릴까요? 🤖")
print("="*50 + "\n")

# 대화 예시
while True:
    user_input = input("말씀해주세요 (종료하시려면 'q' 입력): ")
    if user_input.lower() == 'q':
        print("\n오늘도 좋은 하루 보내세요. 필요하실 때 언제든 불러주세요!\n")
        break
        
    response = conversation.predict(input=user_input)
    print(f"\n비서: {response}\n")
    print("="*50 + "\n")

"""
==================================================
🤖 AI 비서입니다. 무엇을 도와드릴까요? 🤖
==================================================

말씀해주세요 (종료하시려면 'q' 입력): 나 내일 12시에 중요한 미팅이 잡혀있어

비서: 내일 12시의 미팅에 대한 기록을 추가해 드리겠습니다. 또한, 미팅 준비를 위한 참고자료나 이메일 작성 도움도 받으실 수 있습니다. 혹시 미팅 준비가 필요한 사항이나 특이한 요구사항이 있으시면 알려주시기 바랍니다.

==================================================

말씀해주세요 (종료하시려면 'q' 입력): 내일 중요한 일이 있었나?

비서: 네, 내일은 중요한 미팅이 예정되어있었습니다. 그에 대한 기록을 확인해 보았습니다. 미팅 시간과 장소, 내용 등 모든 사항이 정상적으로 진행되었습니다. 혹시 미팅 후 추가적인 업무나 과제가 생긴 경우 알려주시면 감사하겠습니다.

==================================================

말씀해주세요 (종료하시려면 'q' 입력): 몇시에?

비서: 12시에 중요한 미팅이 예정되어있었습니다! 그에 대한 기록을 확인해 보았습니다. 미팅 시간과 장소, 내용 등 모든 사항이 정상적으로 진행되었습니다. 혹시 미팅 후 추가적인 업무나 과제가 생긴 경우 알려주시면 감사하겠습니다.

==================================================
"""
