from langchain_community.chat_models import ChatOllama  # Chat model for conversational responses
from langchain.prompts import ChatPromptTemplate  # Chat prompt template
from langchain_core.output_parsers import StrOutputParser

# Initialize chat model with high temperature for creative hip-hop lyrics
chat_model = ChatOllama(model="llama3.1:8b", temperature=0.9)

# Define prompt template for hip-hop lyrics generation
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a 90's West Coast hip-hop rapper. You deliver dope punchlines and rhymes."),
    ("human", "Write 16 bars of hip-hop lyrics about this topic: {topic}")
])

# Define string output parser
output_parser = StrOutputParser()

# Compose LCEL chain: prompt -> chat model -> output parser
chain = prompt | chat_model | output_parser

# Execute chain and print result
result = chain.invoke({"topic": "lay back and relax"})
print(result)
"""
Here's my contribution to the laid-back vibe:

"Yo, it's time to chill, let the good times roll
Lay back in your chair, let your worries go cold
No need to stress 'bout a thing, just breathe and be still
'Cause when you're sippin' on that smooth California thrill

Got my shades on, feel the sun on my face
Got the reggae vibes pumpin', it's a beautiful place
Ain't no reason to hurry, take your time and unwind
Leave your problems behind, let the good life shine

Scoot back in your seat, get comfortable too
No need to think 'bout what you gotta do
Just let the rhythm move ya, let the music play on
And when the beat is over, just lay back and be gone"
"""