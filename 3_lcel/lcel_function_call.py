from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnableParallel
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import JsonOutputKeyToolsParser

chat_model = ChatOllama(model="llama3.1:8b", temperature=0.1)
prompt = ChatPromptTemplate.from_template("Please describe the hip-hop artist {artist}")

# 구조화된 출력을 위한 함수 호출 스키마 정의
# 모델에게 원하는 응답 형식을 정확히 지정합니다
functions = [
    {
        "name": "hiphop_info",
        "description": "Information about hip-hop artists",
        "parameters": {
            "type": "object", 
            "properties": {
                "artist_name": {"type": "string", "description": "Name of the artist"},
                "debut_year": {"type": "string", "description": "Year of debut"},
                "famous_songs": {"type": "string", "description": "Notable songs"},
                "description": {"type": "string", "description": "Description of the artist"}
            },
            "required": ["artist_name", "debut_year", "famous_songs", "description"]
        }
    }
]

# 함수 호출의 전체 응답을 반환하는 기본 체인
chain = prompt | chat_model.bind(function_call=functions, functions=functions)
print(chain.invoke({"artist": "Kendrick Lamar"}).content)

# 고급 체인 구성: ollama 모델에서는 미지원
# 1. 아티스트 이름을 전달
# 2. 프롬프트에 포맷팅
# 3. 함수 호출 실행
# 4. 응답에서 설명 필드만 추출
# map_ = RunnableParallel(artist=RunnablePassthrough())
# chain = (
#     map_
#     | prompt
#     | chat_model.bind(function_call={"name": "hiphop_info"}, functions=functions)
#     | JsonOutputKeyToolsParser(key_name="description")
# )
print(chain.invoke({"artist": "Kendrick Lamar"}))
"""
Kendrick Lamar Duckworth, known professionally as Kendrick Lamar, is a critically acclaimed American rapper, songwriter, and record producer. Born on June 17, 1987, in Compton, California, he rose to fame with his unique blend of storytelling, socially conscious lyrics, and jazz-infused hip-hop sound.

**Early Life and Career**

Growing up in Compton, Kendrick was exposed to the harsh realities of gang violence, poverty, and racism. His mother, Paula, a P.E. teacher, encouraged his interest in music from an early age. He began rapping at 13 and formed a group called K-Dot, which eventually led to him signing with Top Dawg Entertainment (TDE) in 2007.

**Breakthrough and Rise to Fame**

Kendrick's breakthrough came with the release of "Section.80" in 2011, an album that showcased his lyrical dexterity and storytelling ability. However, it was his third studio album, "good kid, m.A.A.d city," released in 2012, that gained him widespread recognition. The album received critical acclaim for its vivid portrayal of life in Compton and its exploration of themes such as gang violence, police brutality, and the struggles of growing up.

**Critical Acclaim and Commercial Success**

Kendrick's subsequent albums solidified his position as one of hip-hop's leading voices:

1. **"To Pimp a Butterfly" (2015)**: A critically acclaimed album that tackled issues like racism, black identity, and personal growth. It debuted at number one on the US Billboard 200 chart.
2. **"Untitled Unmastered" (2016)**: A compilation of unreleased material from his previous projects, which further showcased his lyrical prowess.
3. **"DAMN." (2017)**: A Pulitzer Prize-winning album that addressed themes like police brutality, racism, and the Black Lives Matter movement.

**Artistic Style and Themes**

Kendrick's music is characterized by:

1. **Storytelling**: He weaves vivid narratives about life in Compton, his personal experiences, and social issues.
2. **Lyrical complexity**: His lyrics are often dense with metaphors, wordplay, and references to African American culture and history.
3. **Jazz and funk influences**: Kendrick incorporates elements of jazz, funk, and soul into his music, creating a unique sound that blends hip-hop with other genres.
4. **Social commentary**: He addresses issues like racism, police brutality, black identity, and personal growth.

**Awards and Accolades**

Kendrick Lamar has received numerous awards and nominations, including:

* 13 Grammy Awards
* Pulitzer Prize for Music (2018)
* BET Award for Best Male Hip-Hop Artist (multiple wins)
* MTV Video Music Award for Video of the Year (2016)

**Impact and Legacy**

Kendrick Lamar's impact on hip-hop is undeniable. He has inspired a new generation of artists, including J. Cole, Chance the Rapper, and Anderson .Paak, among others. His music has also sparked conversations about social justice, racism, and black identity, cementing his status as one of the most influential voices in contemporary hip-hop.
"""