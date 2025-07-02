from langchain_community.chat_models import ChatOllama  # Chat model for conversational responses
from langchain.prompts import ChatPromptTemplate  # Chat prompt template
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough

# llama 모델 초기화 - 온도 0.8로 설정하여 적당한 창의성 부여
chat_model = ChatOllama(model="llama3.1:8b", temperature=0.8)

# RunnablePassthrough()는 입력을 그대로 통과시킴
runnable = RunnableParallel(
    passed=RunnablePassthrough()
)

print(runnable.invoke({"num": 10}))
"""
{'passed': {'num': 10}}
"""

# 여러 Runnable을 병렬로 실행하는 예제
# passed: 입력을 그대로 통과
# extra: 입력값에 mult 키를 추가하여 num * 3 계산
# modified: num에 1을 더한 값 반환
runnable = RunnableParallel(
    passed=RunnablePassthrough(),
    extra=RunnablePassthrough.assign(mult=lambda x: x["num"] * 3),
    modified=lambda x: x["num"] + 1
)

print(runnable.invoke({"num": 1}))
"""
{'passed': {'num': 1}, 'extra': {'num': 1, 'mult': 3}, 'modified': 2}
"""

chat_model.temperature = 0
joke_chain = ChatPromptTemplate.from_template("Tell me a joke about {topic}") | chat_model
poem_chain = (
    ChatPromptTemplate.from_template("Write a poem about {topic}") | chat_model
)

# 동시에 prompt execution
map_chain = RunnableParallel(
    joke=joke_chain,
    poem=poem_chain,
)

result = map_chain.invoke({"topic": "bear"})
print("Joke:", result["joke"].content)
print("Poem:", result["poem"].content)
"""
Joke: Why did the bear go to the doctor?

Because it had a grizzly cough! (get it?)
Poem: In forest depths, a creature roams,
A symbol of strength, in gentle homes.
The bear, with fur so soft and bright,
Ambles through woods, with quiet might.

Its eyes, like pools, of calmest blue,
Reflect the world, with wisdom true.
It sniffs the air, with twitching nose,
Drinking in scents, from forest rose.

With paws, that pad, upon the ground,
The bear moves slow, without a sound.
A monarch of woods, in quiet reign,
It rules its kingdom, with gentle hand and brain.

In summer's heat, it seeks the shade,
And in winter's cold, its den is made.
A place to rest, where snows do lie,
Where it can dream, and watch the world go by.

The bear, a creature, wild and free,
A symbol of power, for you and me.
It roams the woods, with gentle pace,
A reminder of nature's peaceful space.
"""