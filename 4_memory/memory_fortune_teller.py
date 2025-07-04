from langchain_community.chat_models import ChatOllama  # Chat model for conversational responses
from langchain.prompts import PromptTemplate  # Chat prompt template
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


# 메모리 객체 생성
memory = ConversationBufferMemory()

# 대화 체인 생성
chat_model = ChatOllama(model="llama3.1:8b", temperature=0.9)
conversation = ConversationChain(
    llm=chat_model, 
    memory=memory,
    prompt=PromptTemplate(
        input_variables=["history", "input"],
        template="""당신은 전문적인 사주상담가입니다. 사용자의 생년월일과 태어난 시간을 바탕으로 운세를 봐주세요.
        이전 대화 내용:
        {history}
        
        사용자: {input}
        사주상담가:"""
    )
)

# 대화 예시
while True:
    user_input = input("질문을 입력하세요 (종료하려면 'q' 입력): ")
    if user_input.lower() == 'q':
        break
        
    response = conversation.predict(input=user_input)
    print(f"사주상담가: {response}")
    print("\n" + "="*50 + "\n")

"""
사주상담가: 당신의 사주의 자세한 사항을 알려드리겠습니다.

**소양지:** 
서서공활이다. 

**팔갑지:** 
서서해방이다.

**수합지 :**
소화로 평안한 인물입니다.

**진사주:**
1년차 4월, 5월, 6월에 큰 사업을 많이 시작하고 있습니다. 새로운 지인과 만나는 기회가 많았습니다. 

2년차 11월, 12월에 이익이 쌓입니다. 

3년차 7월, 8월, 9월에 어려움을 겪어야 합니다.

4년차 3월, 4월에 새로운 가능성을 발견할 것입니다. 

5년차 10월, 11월에 큰 성공을 맛보게 됩니다. 

6년차 2월, 3월에 기복이 심해집니다. 

7년차 8월, 9월에 이익을 누리게 됩니다.

**지방:** 
서쪽, 북쪽입니다.

**형상 :**
소화로 평안한 인물입니다.

**별운:**
양우를 받았습니다.

**주문기:**
당신의 주생일인 xxxx년 1월 2일은 xx년에 해당합니다. 

**나타난 사주:**
서서공활, 서서해방이 나타났습니다. 

* * *

사주의 자세한 사항을 알려드렸습니다.

==================================================

질문을 입력하세요 (종료하려면 'q' 입력): 서서공활이랑 서서해방의 뜻은무엇인가요?    

서서공활: 다른 사람으로부터 도움을 받지 않고 자신의 힘으로 success하는 모습입니다.

서서해방: 자신만의 능력으로 어려움에서 해방되는 인물입니다. 

이 두 사주가 나타난 것을 볼 때, 사용자는 내적 능력을 믿고 자신이 문제를 해결 할 수 있는 인물이라고 할 수 있습니다.

==================================================

질문을 입력하세요 (종료하려면 'q' 입력): 저는 몇년도에 출생했다고 했죠?
사주상담가: xxxx년 1월 2일에 태어났습니다.

==================================================
"""
