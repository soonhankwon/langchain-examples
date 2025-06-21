# Langchain 라이브러리에서 필요한 모듈들을 가져옵니다
from langchain_community.llms import Ollama  # 일반 텍스트 생성을 위한 Ollama 모델
from langchain.prompts import ChatPromptTemplate  # 채팅 프롬프트 템플릿 정의

# 일반 텍스트 생성을 위한 Ollama 모델을 초기화합니다
# temperature가 0.7로 설정되어 적당한 창의성을 가진 응답을 생성합니다
llm = Ollama(model="llama3.1:8b", temperature=0.7)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a 1990's East Side Hip Hop rapper."),
    ("human", "{input}"),
])

chain = chat_prompt | llm

response = chain.invoke({"input": "Make a verse of hip-hop lyrics with dope punchlines"})
print(response)

"""
Ahh, let me get in the zone...

**Verse**

Yo, listen up, I'm on the mic, reppin' my block
East Side represent, where the streets is rock
I'm a product of the Ghetto, ain't no sugarcoatin'
My rhymes so tight, they'll leave you feelin' like you're gettin' drained

Got my eyes on the prize, tryna make that dough
But it's hard to grind when the system's got you in a chokehold, yo
I'm just a kid from the Bottoms, but I won't be held down
My rhymes is like a bullet, they'll leave you wearin' a frown

I'm on the mic, and I'm here to say
East Side Hip Hop, we run this game in every way
We ain't never stoppin', our movement's on the rise
So you better get ready, 'cause we're takin' over the skies!

Word.
"""
