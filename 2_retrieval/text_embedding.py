# Ollama의 임베딩 기능을 사용하기 위한 임포트
from langchain.embeddings import OllamaEmbeddings

# nomic-embed-text 모델을 사용하여 임베딩 모델 초기화
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

# 여러 힙합 관련 문장들을 임베딩 벡터로 변환
# embed_documents 메서드는 문장 리스트를 받아서 임베딩 벡터 리스트를 반환
embeddings = embedding_model.embed_documents(
    [
        "Hip-hop is my whole life!",
        "Let me drop a beatbox real quick",
        "I'm a rapper who battles with rhymes",
        "When I grab the mic, endless flows",
        "Journey started in the underground",
        "Beats echoing through the streets",
        "Hip-hop is culture, it's a lifestyle",
        "Through rap I tell my story",
    ]
)

# 임베딩 결과 확인
print(len(embeddings))     # 입력한 문장의 개수만큼 임베딩이 생성됨 (8개)
print(len(embeddings[0]))  # 768
print(len(embeddings[1]))  # 768

from langchain_community.document_loaders.csv_loader import CSVLoader
loader = CSVLoader(file_path="pokemon_data.csv")
data = loader.load()

# 각 포켓몬 데이터의 내용(page_content)을 임베딩 벡터로 변환
embeddings = embedding_model.embed_documents([
    text.page_content for text in data
])

# 생성된 임베딩 벡터의 개수 출력 (포켓몬의 수와 동일)
print(len(embeddings))

# 쿼리 문장을 임베딩 벡터로 변환하여 포켓몬 데이터와 비교 가능하게 함
embedded_query = embedding_model.embed_query("What pokemon is the best attacker?")

# 생성된 쿼리 임베딩 벡터의 처음 5개 값을 출력하여 확인
print(embedded_query[:5])
"""
[0.7038830518722534, 1.7359747886657715, -4.408138275146484, 0.4778326451778412, 0.41343098878860474]
"""