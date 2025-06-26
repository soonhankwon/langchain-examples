from langchain_community.document_loaders import CSVLoader

# Mobile Phone Pricing.csv 파일을 로드하기 위한 CSVLoader 인스턴스 생성
loader = CSVLoader(file_path="./Mobile Phone Pricing.csv")

# CSV 파일의 데이터를 로드
data = loader.load()

# 첫 번째 데이터의 내용 출력
print(data[0].page_content)

# 첫 번째 데이터의 메타데이터 출력 (파일 정보 등)
print(data[0].metadata)