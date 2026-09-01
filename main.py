import os
from google import genai
from datetime import datetime

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

client = genai.Client(api_key=api_key)

prompt = """
당신은 전문 금융, 부동산 및 IT 테크 블로거입니다. 구글 검색 엔진 최적화(SEO)에 맞추어 독자에게 유용한 블로그 포스팅 초안을 작성해주세요. 
- 자연스러운 문단과 소제목(##) 사용
- 경험담 느낌의 친근한 문체 섞기
- 볼드체 활용 및 광고 단가(CPC)가 높은 정보 위주
- 해시태그 생략
전체 언어는 한국어로 작성해주세요.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

os.makedirs("posts", exist_ok=True)
file_name = f"posts/post-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.md"
with open(file_name, "w", encoding="utf-8") as f:
    f.write(response.text)
print(f"생성 완료: {file_name}")
