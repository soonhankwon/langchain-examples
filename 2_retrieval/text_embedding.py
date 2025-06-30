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