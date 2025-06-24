# 프롬프트 템플릿과 파일 로딩을 위한 클래스들을 임포트
from langchain.prompts import load_prompt, PromptTemplate

# 프롬프트 템플릿 문자열 정의 - {adjective}와 {content}는 나중에 채워질 변수
template = "Tell me a {adjective} joke about {content}."

# PromptTemplate 객체 생성
# - template: 위에서 정의한 템플릿 문자열
# - input_variables: 템플릿에서 사용될 변수들의 리스트
prompt = PromptTemplate(template=template, input_variables=["adjective", "content"])

# 생성된 프롬프트 템플릿을 JSON 파일로 저장: 이렇게 저장된 템플릿은 나중에 재사용 가능
prompt.save("simple_prompt.json")

# 저장된 JSON 파일에서 프롬프트 템플릿을 다시 로드
prompt = load_prompt("simple_prompt.json")

# 로드된 프롬프트에 실제 값을 넣어 포맷팅
# - adjective에 "funny", content에 "chickens"를 대입하여 최종 프롬프트 생성
print(prompt.format(adjective="funny", content="chickens"))

"""
{
    "name": null,
    "input_variables": [
        "adjective",
        "content"
    ],
    "optional_variables": [],
    "output_parser": null,
    "partial_variables": {},
    "metadata": null,
    "tags": null,
    "template": "Tell me a {adjective} joke about {content}.",
    "template_format": "f-string",
    "validate_template": false,
    "_type": "prompt"
}
"""