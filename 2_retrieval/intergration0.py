from langchain_community.document_loaders import CSVLoader 
from langchain.prompts.chat import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama

template = """당신은 모바일 폰 데이터 분석 전문가입니다. 
주어진 모바일 폰 데이터셋에서 {analysis_task}에 대한 정보를 분석하고 답변해주세요.

데이터셋 컬럼 설명:
- battery_power: 배터리 파워 (mAh)
- blue: 블루투스 지원 (0=없음, 1=있음)
- clock_speed: CPU 클럭 속도 (GHz)
- dual_sim: 듀얼심 지원 (0=없음, 1=있음)
- fc: 프론트 카메라 (MP)
- four_g: 4G 지원 (0=없음, 1=있음)
- int_memory: 내부 메모리 (GB)
- mobile_wt: 모바일 무게 (g)
- n_cores: CPU 코어 수
- pc: 기본 카메라 (MP)
- px_height: 화면 높이 (픽셀)
- px_width: 화면 너비 (픽셀)
- ram: RAM 용량 (MB)
- sc_h: 화면 높이 (cm)
- sc_w: 화면 너비 (cm)
- talk_time: 통화 시간 (시간)
- three_g: 3G 지원 (0=없음, 1=있음)
- touch_screen: 터치스크린 (0=없음, 1=있음)
- wifi: WiFi 지원 (0=없음, 1=있음)
- price_range: 가격 범위 (0=저가, 1=중저가, 2=중고가, 3=고가)

데이터: `{data}`"""

human_template = "{question}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])

loader = CSVLoader(file_path="Mobile Phone Pricing.csv")
data = loader.load()

text_list = []
for record in data:
    text_list.append(record.page_content)

chat_prompt_output = chat_prompt.format_messages(
    analysis_task="배터리 파워가 가장 높은 모바일 폰과 그 사양",
    data=("\n".join(text_list[:20])),  # 처음 20개 레코드 사용
    question="이 데이터에서 배터리 파워가 가장 높은 모바일 폰의 배터리 용량과 RAM, 그리고 가격 범위는 무엇인가요?")

chat_model = ChatOllama(model="llama3.1:8b", temperature=0.7)
response = chat_model(chat_prompt_output)
"""
데이터를 분석한 결과, 배터리 파워가 가장 높은 모바일 폰은 다음과 같습니다.

* 배터리 파워: 1954 mAh
* RAM 용량: 3220 MB
* 가격 범위: 3 (고가)

이러한 특징을 가진 모바일 폰의 아이디는 없습니다. 하지만, 다음과 같은 데이터를 찾았습니다.

* battery_power: 1954
blue: 0
clock_speed: 0.5
dual_sim: 1
fc: 0
four_g: 0
int_memory: 24
m_dep: 0.8
mobile_wt: 187
n_cores: 4
pc: 0
px_height: 512
px_width: 1149
ram: 700
sc_h: 16
sc_w: 3
talk_time: 5
three_g: 1
touch_screen: 1
wifi: 1
price_range: 0
"""
print(response.content)