# UnstructuredHTMLLoader를 사용하여 HTML 파일 로드
from langchain_community.document_loaders import UnstructuredHTMLLoader

# sample.html 파일을 로드하기 위한 UnstructuredHTMLLoader 인스턴스 생성
loader = UnstructuredHTMLLoader(file_path="sample.html")
# HTML 파일의 데이터를 로드
data = loader.load()
# 로드된 데이터 출력 
print(data)
"""
[Document(metadata={'source': 'sample.html'}, page_content='Hello, LangChain!')]
"""

# BeautifulSoup 기반의 BSHTMLLoader를 사용하여 HTML 파일 로드
from langchain_community.document_loaders import BSHTMLLoader
# sample.html 파일을 로드하기 위한 BSHTMLLoader 인스턴스 생성
loader = BSHTMLLoader(file_path='sample.html')
# HTML 파일의 데이터를 로드
data = loader.load()
# 로드된 데이터 출력
print(data)
# 첫 번째 문서의 실제 내용만 출력
print(data[0].page_content)

"""
[Document(metadata={'source': 'sample.html', 'title': ''}, page_content='\n\nHello, LangChain!\n\n')]
Hello, LangChain!
"""