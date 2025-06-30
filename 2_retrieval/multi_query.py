from langchain_community.document_loaders import CSVLoader
from langchain.embeddings import OllamaEmbeddings  
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.llms import Ollama

# Step 1. Embedding & LLM 세팅
embedding_model = OllamaEmbeddings(model="nomic-embed-text")
llm = Ollama(model="llama3.1:8b", temperature=0.7)

# Step 2. CSV 로드 및 청크 분할
loader = CSVLoader(file_path="pokemon_data.csv")
raw_documents = loader.load()
documents = CharacterTextSplitter(chunk_size=200, chunk_overlap=0).split_documents(raw_documents)

# Step 3. Chroma 벡터 DB 구축 및 저장
db = Chroma.from_documents(documents, embedding_model, persist_directory="./pokemon_db")
db.persist()

# Step 4. 저장된 DB 다시 불러오기
db_conn = Chroma(persist_directory="./pokemon_db", embedding_function=embedding_model)

# Step 5. MultiQueryRetriever 생성
retriever = MultiQueryRetriever.from_llm(
    retriever=db_conn.as_retriever(),
    llm=llm
)

# Step 6. 단일 쿼리를 여러 표현으로 파생하여 검색
query = "What is the best defending pokemon?"
docs = retriever.invoke(query)

# Step 7. 결과 출력
print(f"\n🔍 Original Query: {query}")
for i, doc in enumerate(docs):
    print(f"\n📄 Result {i + 1}:\n{doc.page_content}")

"""
🔍 Original Query: What is the best defending pokemon?

📄 Result 1:
id: 917
name: tarountula
base_experience: 42
height: 3
weight: 40
types: bug
abilities: insomnia, stakeout
moves: headbutt, tackle, body-slam, take-down, counter
stats: hp=35, attack=41, defense=45, special-attack=29, special-defense=40, speed=20

📄 Result 2:
id: 795
name: pheromosa
base_experience: 257
height: 18
weight: 250
types: bug, fighting
abilities: beast-boost
moves: stomp, double-kick, jump-kick, leer, ice-beam
stats: hp=71, attack=137, defense=37, special-attack=137, special-defense=37, speed=151

📄 Result 3:
id: 106
name: hitmonlee
base_experience: 159
height: 15
weight: 498
types: fighting
abilities: limber, reckless, unburden
moves: mega-punch, swords-dance, double-kick, mega-kick, jump-kick
stats: hp=50, attack=120, defense=53, special-attack=35, special-defense=110, speed=87

📄 Result 4:
id: 214
name: heracross
base_experience: 175
height: 15
weight: 540
types: bug, fighting
abilities: swarm, guts, moxie
moves: swords-dance, cut, headbutt, horn-attack, fury-attack
stats: hp=80, attack=125, defense=75, special-attack=40, special-defense=95, speed=85
"""