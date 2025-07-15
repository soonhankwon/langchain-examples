import requests
import json
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

chat_model = ChatOllama(model="llama3.1:8b", temperature=0.3)
prompt = ChatPromptTemplate.from_template("""
다음 사용자 정보를 자연스러운 한국어로 설명해주세요:
{user_info}
""")

BASE_URL = "http://localhost:8000"

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
    
    # 테스트할 유저 ID를 입력하세요
    user_id = int(input("조회할 유저 ID를 입력하세요: "))
    
    # 특정 유저 조회
    test_get_user(user_id)
    
    print("테스트 완료!")

"""
조회할 유저 ID를 입력하세요: 1
=== 특정 유저 조회 결과 ===
사용자의 ID는 1이고, 닉네임은 '테스터'이며, 이메일 주소는 'tester@gmail.com'입니다.
"""