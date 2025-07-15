import requests
import json
import re
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

chat_model = ChatOllama(model="llama3.1:8b", temperature=0.3)
prompt = ChatPromptTemplate.from_template("""
다음 사용자 정보를 자연스러운 한국어로 설명해주세요:
{user_info}
""")

BASE_URL = "http://localhost:8000"

def extract_user_id(text):
    """텍스트에서 숫자 추출"""
    numbers = re.findall(r'\d+', text)
    return int(numbers[0]) if numbers else None

def test_get_user(user_id):
    """특정 유저 조회 테스트"""
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    
    if response.status_code == 200:
        user_data = response.json()
        chain = prompt | chat_model
        result = chain.invoke({"user_info": json.dumps(user_data, ensure_ascii=False)})
        
        print("=== 특정 유저 조회 결과 ===")
        print(result.content)
        print()
    else:
        print(f"오류가 발생했습니다. 상태 코드: {response.status_code}")
        print(f"응답: {response.text}")
        print()

if __name__ == "__main__":
    print("Supabase User API 테스트를 시작합니다...")
    print()
    
    # 자연어로 유저 ID 입력 받기
    user_input = input("찾고 싶은 유저를 입력하세요 (예: 1번 유저 찾아줘): ")
    user_id = extract_user_id(user_input)
    
    if user_id is not None:
        # 특정 유저 조회
        test_get_user(user_id)
    else:
        print("유효한 유저 ID를 찾을 수 없습니다. 숫자를 포함하여 입력해주세요.")
    
    print("테스트 완료!")

"""
Supabase User API 테스트를 시작합니다...

찾고 싶은 유저를 입력하세요 (예: 1번 유저 찾아줘): 1번 유저 
=== 특정 유저 조회 결과 ===
사용자의 아이디는 1이고, 닉네임은 '테스터'이며, 이메일 주소는 'test@gmail.com'입니다.

테스트 완료!
"""