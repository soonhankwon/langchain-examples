# 텍스트를 청크 단위로 분할하기 위한 RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# state_of_the_union.txt 파일을 읽어서 문자열로 저장
with open('./state_of_the_union.txt', 'r') as f:
    state_of_the_union = f.read()

# 텍스트 분할기 설정
# - chunk_size: 각 청크의 최대 크기(문자 수)
# - chunk_overlap: 청크 간 중복되는 문자 수
# - length_function: 텍스트 길이를 측정하는 함수
# - add_start_index: 각 청크의 시작 인덱스 포함 여부
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    add_start_index=True,
)

# 텍스트를 청크로 분할하여 Document 객체 리스트 생성
texts = text_splitter.create_documents([state_of_the_union])

# 첫 번째와 두 번째 청크 출력
print(texts[0].page_content)
"""
Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and
"""
print(texts[1].page_content)
"""
of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.
"""