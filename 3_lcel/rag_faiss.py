# Ollama의 임베딩 기능을 사용하기 위한 임포트
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# nomic-embed-text 모델을 사용하여 임베딩 모델 초기화
embedding_model = OllamaEmbeddings(model="nomic-embed-text")
vector_store = FAISS.from_texts(
    [
        "NVIDIA는 AI 반도체 시장을 선도하고 있다",
        "NVIDIA의 GPU는 딥러닝과 머신러닝 분야에서 핵심적인 역할을 한다",
        "NVIDIA는 자율주행차 기술 개발을 위한 플랫폼도 제공하고 있다",
        "NVIDIA의 CUDA 기술은 병렬 컴퓨팅의 표준이 되었다",
        "NVIDIA는 데이터센터용 GPU 솔루션으로 높은 성장세를 보이고 있다",
        "NVIDIA의 GeForce RTX 시리즈는 게이밍 GPU 시장을 주도하고 있다",
        "NVIDIA는 메타버스 플랫폼 'Omniverse'를 개발하여 제공 중이다",
        "NVIDIA의 AI 추론 엔진은 챗GPT와 같은 대형 언어 모델 운영에 필수적이다",
        "NVIDIA는 엔터프라이즈 AI 솔루션 'DGX'를 통해 기업용 시장을 공략하고 있다",
        "NVIDIA의 반도체 설계 기술은 업계 최고 수준으로 평가받고 있다",
    ],
    embedding=embedding_model
)

# 벡터 저장소 저장 및 로드
vector_store.save_local("stock_faiss_index")
vector_store_new = FAISS.load_local("stock_faiss_index", embedding_model, allow_dangerous_deserialization=True)
retriever = vector_store_new.as_retriever(search_kwargs={"k": 10})

template = """
다음 문맥만을 기반으로 질문에 답변해주세요:

{context}

질문: {question}

다음 언어로 답변해주세요: {language}
"""

prompt = ChatPromptTemplate.from_template(template)
model = ChatOllama(model="llama3.1:8b", temperature=0.7)

chain = (
    {"context": retriever, "question": RunnablePassthrough(), "language": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# 디버깅: 검색된 컨텍스트 확인
question = "NVIDIA가 개발하고 있는 메타버스는 플랫폼은 무엇인가요?"
docs = retriever.get_relevant_documents(question)
print(chain.invoke({"question": question, "language": "한국어"}))
"""
NVIDIA가 개발하고 있는 메타버스의 플랫폼은 'Omniverse'입니다.
"""