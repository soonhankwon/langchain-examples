from langchain_community.document_loaders import WebBaseLoader  # 웹 페이지 로딩을 위한 로더
from langchain.embeddings import OllamaEmbeddings  # 텍스트 임베딩을 위한 모델
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 텍스트 분할을 위한 스플리터
from langchain_community.vectorstores import Chroma  # 벡터 데이터베이스
from langchain.retrievers.multi_query import MultiQueryRetriever  # 다중 쿼리 검색기
from langchain_community.llms import Ollama  # LLM 모델

# Step 1. 임베딩 모델과 LLM 모델을 초기화합니다
embedding_model = OllamaEmbeddings(model="nomic-embed-text")  # 텍스트 임베딩용 모델
llm = Ollama(model="llama3.1:8b", temperature=0.7)  # 텍스트 생성용 모델

# 위키피디아 페이지를 로드합니다
loader = WebBaseLoader(web_paths=["https://en.wikipedia.org/wiki/The_Feynman_Lectures_on_Physics"])
data = loader.load()

# 텍스트를 500자 크기의 청크로 분할합니다 (중복 없음)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = text_splitter.split_documents(data)

# 분할된 텍스트를 벡터 데이터베이스에 저장합니다
vectordb = Chroma.from_documents(documents=splits, embedding=embedding_model)

# 검색할 질문을 정의합니다
question = "What is the Feynman Lectures on Physics?"
# 다중 쿼리 검색기를 초기화합니다
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=vectordb.as_retriever(),
    llm=llm
)

# 요약을 위한 추가 라이브러리들을 임포트합니다
from langchain.chains import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

# 요약을 위한 프롬프트 템플릿을 정의합니다
summary_prompt = PromptTemplate.from_template(
    "Summarize what the Feynman Lectures on Physics are about from the following documents:\n\n{documents}"
)

# LLM 체인을 생성합니다
llm_chain = LLMChain(llm=llm, prompt=summary_prompt)

# 문서 요약을 위한 체인을 구성합니다
summarizer = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_variable_name="documents"
)

# 검색된 문서들을 요약합니다
docs = retriever_from_llm.invoke(question)  # 다중 쿼리로 관련 문서 검색
summary = summarizer.run(docs)  # 검색된 문서들을 요약

# 결과를 출력합니다
print("\n📝 Summary:", summary)
"""
📝 Summary: Here's a summary of what the Feynman Lectures on Physics are about:

**Overview**: The Feynman Lectures on Physics is a comprehensive textbook written by Richard Feynman, Robert B. Leighton, and Matthew Sands. It's based on lectures given by Feynman to undergraduate students at Caltech from 1961-1964.

**Content**: The book covers three volumes:

* Volume I: Mechanics, Radiation, and Heat (including relativistic effects)
* Volume II: Electromagnetism and Matter
* Volume III: Quantum Mechanics

The textbook includes chapters on the relationship between mathematics and physics, as well as the relationship of physics to other sciences.

**Purpose**: The lectures aim to provide a clear and intuitive understanding of fundamental concepts in physics, rather than just presenting mathematical formulas. Feynman's goal was to make complex ideas accessible to students without sacrificing scientific rigor.

**Teaching style**: The book is characterized by Feynman's unique teaching style, which emphasizes:

* Clear explanations of difficult concepts
* Use of simple analogies and examples
* Emphasis on understanding rather than memorization

**Impact**: The Feynman Lectures have had a significant impact on physics education, making complex ideas accessible to students and inspiring new generations of physicists.
"""