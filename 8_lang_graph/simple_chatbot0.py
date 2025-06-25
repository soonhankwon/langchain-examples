from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)
llm = Ollama(model="llama3.1:8b", temperature=0.8)

def chatbot(state: State):
    # 힙합 스타일의 프롬프트 템플릿 생성
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a 2000s hip-hop rapper. Always respond in hip-hop style with slang, attitude and rhythm. Use emojis and hip-hop expressions."),
        ("human", "{input}")
    ])
    # 사용자 메시지 가져오기
    user_message = state["messages"][-1]
    # 프롬프트 실행
    response = chat_prompt | llm
    result = response.invoke({"input": user_message})
    
    return {"messages": [{"role": "assistant", "content": result}]}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
                print("Kendrick Lamar: ", value["messages"][-1]["content"])

while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Peace out, homie! Stay fresh! 🎤")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("You: " + user_input)
        stream_graph_updates(user_input)
        break
