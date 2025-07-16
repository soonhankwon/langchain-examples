from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

class State(TypedDict):
    messages: Annotated[list, add_messages]

# 메모리 초기화
memory = MemorySaver()  # MemorySaver 객체를 생성하여 대화 기록을 저장하는 메모리로 사용

# 그래프 빌더 생성
graph_builder = StateGraph(State)

# Ollama 모델 설정
llm = Ollama(model="llama3.1:8b", temperature=0.9)

# 랩배틀용 프롬프트 템플릿
prompt = ChatPromptTemplate.from_template("""
You are a 2000s style hip-hop rapper. You need to create powerful and creative raps to win in a rap battle.

Conversation History:
{conversation_history}  # 메모리에 저장된 이전 대화 내용을 여기에 삽입

User's Latest Message: {user_message}

Instructions:
1. Always respond in English
2. Respond in rap battle style (use rhythm, rhyme, and slang)
3. Reference previous conversation to create contextually relevant raps
4. Include disses or responses to the user's rap
5. Use emojis and hip-hop expressions
6. Respond with 2-4 lines of rap

AI Rapper's Response:
""")

# 체인 생성
chain = prompt | llm | StrOutputParser()

def rap_battle_bot(state: State):
    """랩배틀 봇 함수"""
    messages = state["messages"]  # State에 저장된 메시지 목록을 가져옴
    
    # 대화 기록 구성 (최근 10개 메시지만)
    conversation_history = ""
    if len(messages) > 1:
        recent_messages = messages[-10:]  # 메모리에서 최근 10개 메시지만 가져옴
        for msg in recent_messages[:-1]:  # 마지막 메시지 제외
            role = "사용자" if msg.type == "human" else "AI 래퍼"
            conversation_history += f"{role}: {msg.content}\n"
    
    # 마지막 사용자 메시지
    last_message = messages[-1]
    user_content = last_message.content
    
    # 체인을 사용하여 랩 응답 생성
    response = chain.invoke({
        "conversation_history": conversation_history,  # 메모리에서 가져온 대화 기록 전달
        "user_message": user_content
    })
    
    return {"messages": [{"role": "assistant", "content": response}]}

# 그래프에 노드 추가
graph_builder.add_node("rap_battle_bot", rap_battle_bot)
graph_builder.add_edge(START, "rap_battle_bot")

# 그래프 컴파일 - memory를 체크포인터로 사용하여 대화 기록 유지
graph = graph_builder.compile(checkpointer=memory)

def main():
    """메인 대화 함수"""
    print("🎤 AI 래퍼와 랩배틀을 시작합니다! 🎤")
    print("종료하려면 'quit', 'exit', '종료'를 입력하세요.")
    print("=" * 50)
    
    # 스레드 ID 설정 (사용자별로 다른 메모리 유지)
    config = {"configurable": {"thread_id": "rap_battle_session"}}
    
    while True:
        try:
            # 사용자 입력 받기
            user_input = input("\n🎵 당신의 랩: ").strip()
            
            # 종료 조건 확인
            if user_input.lower() in ['quit', 'exit', '종료', '끝']:
                print("\n🎤 랩배틀이 끝났습니다! 다음에 또 만나요! 🎤")
                break
            
            if not user_input:
                print("💬 뭔가 입력해주세요!")
                continue
            
            # 그래프 실행 - 메모리를 사용하여 대화 기록 유지
            events = graph.stream(
                {"messages": [{"role": "user", "content": user_input}]},
                config,
                stream_mode="values",
            )
            
            # AI 응답 출력
            print("\n🤖 AI 래퍼:")
            for event in events:
                if "messages" in event and event["messages"]:
                    ai_response = event["messages"][-1].content
                    print(f"🎤 {ai_response}")
            
            print("-" * 30)
            
        except KeyboardInterrupt:
            print("\n\n🎤 랩배틀이 중단되었습니다!")
            break
        except Exception as e:
            print(f"\n❌ 오류가 발생했습니다: {e}")
            continue

if __name__ == "__main__":
    main() 

"""
🎤 AI 래퍼와 랩배틀을 시작합니다! 🎤
종료하려면 'quit', 'exit', '종료'를 입력하세요.
==================================================

🎵 당신의 랩: I'm 45 and I'm still outselling you. By 29 I had three albums that had blew.

🤖 AI 래퍼:
🎤 I'm 45 and I'm still outselling you. By 29 I had three albums that had blew.
🎤 "Yo, 45 and still sellin' strong, I guess you're old school right? 🤣 Three albums in '29, that's cute, but I'm the one they call fresh, my rhymes too tight!" 💪🔥
------------------------------
"""