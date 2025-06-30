from langchain_community.document_loaders import CSVLoader
from langchain.embeddings import OllamaEmbeddings  
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

# nomic-embed-text 모델을 사용하여 임베딩 모델을 초기화합니다
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

# CSV 파일에서 포켓몬 데이터를 로드합니다
loader = CSVLoader(file_path="pokemon_data.csv")
raw_documents = loader.load()

# 문서를 200자 크기의 청크로 분할합니다 (청크 간 중복 없음)
documents = CharacterTextSplitter(chunk_size=200, chunk_overlap=0).split_documents(raw_documents)

# Chroma 벡터 데이터베이스를 생성하고 문서를 저장합니다
db = Chroma.from_documents(documents, embedding_model, persist_directory="./pokemon_db")

# 데이터베이스를 디스크에 영구 저장합니다 (SQLite 형식)
db.persist()

# 저장된 데이터베이스에 다시 연결합니다
db_conn = Chroma(persist_directory="./pokemon_db", embedding_function=embedding_model)

# 공격력이 가장 높은 포켓몬을 찾는 쿼리를 실행합니다
query = "What is the best attacking pokemon?"
docs = db_conn.similarity_search(query)
print(docs[0].page_content)
"""
id: 106
name: hitmonlee
base_experience: 159
height: 15
weight: 498
types: fighting
abilities: limber, reckless, unburden
moves: mega-punch, swords-dance, double-kick, mega-kick, jump-kick
stats: hp=50, attack=120, defense=53, special-attack=35, special-defense=110, speed=87
"""

# 데이터베이스를 retriever로 변환하여 방어력이 가장 높은 포켓몬을 찾습니다
retriever = db.as_retriever()
result = retriever.invoke("What is the best defending pokemon?")
print(result[0].page_content)
"""
id: 795
name: pheromosa
base_experience: 257
height: 18
weight: 250
types: bug, fighting
abilities: beast-boost
moves: stomp, double-kick, jump-kick, leer, ice-beam
stats: hp=71, attack=137, defense=37, special-attack=137, special-defense=37, speed=151
"""