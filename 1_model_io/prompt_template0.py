# Langchain 라이브러리에서 필요한 모듈들을 가져옵니다
from langchain_community.llms import Ollama  # 일반 텍스트 생성을 위한 Ollama 모델
from langchain.prompts import ChatPromptTemplate  # 채팅 프롬프트 템플릿 정의
from langchain.prompts import PromptTemplate  # 프롬프트 템플릿 정의

# 일반 텍스트 생성을 위한 Ollama 모델을 초기화합니다
# temperature가 0.7로 설정되어 적당한 창의성을 가진 응답을 생성합니다
llm = Ollama(model="llama3.1:8b", temperature=0.7)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a 1990's East Side {musician_type}."),
    ("human", "{input}"),
])

chain = chat_prompt | llm

system_prompt = PromptTemplate.from_template("You are a 1990's East Side {musician_type}.")
human_prompt = PromptTemplate.from_template("Make a verse of {music_type} lyrics with dope punchlines")
system_resp = system_prompt.format(musician_type="hip-hop rapper")
human_resp = human_prompt.format(music_type="hip-hop")

response = chain.invoke({"musician_type": system_resp, "input": human_resp})

print(response)

"""
Yo, what's good fam? Here's a hot one:

"Listen up, y'all, I'm on the mic tonight
Got my Adidas shell-toes, and my Kangol tight
East Side representin', where the streets is cold
But my rhymes so hot, they'll leave you feelin' old

I'm rockin' my flyest fits, from FUBU to Polo
 Ain't nobody touchin' me, I'm the king of the block though
Got my eyes on the prize, and it's shinin' bright
Leavin' all the haters in the dust, day and night"

Word?
"""
