import os
import google.generativeai as genai
from datetime import datetime

# 1. Gemini API 키 설정
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

genai.configure(api_key=api_key)

# 2. 모델 선택
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 고단가 수익형(금융·부동산·IT) 블로그 프롬프트 설정
prompt = """
당신은 전문 금융, 부동산 및 IT 테크 블로거입니다. 
구글 검색 엔진 최적화(SEO)에 최적화되어 있으며, 독자에게 실질적인 도움이 되고 신뢰성 있는 정보를 담은 블로그 포스팅 초안을 작성해주세요.

[주제 선정 가이드라인]
- 최신 부동산 제도/청약 정보, 실생활에 유용한 금융 상식(금리, 대출, 예적금 트렌드), 정부 지원 정책, 또는 고단가 IT/테크 트렌드 중 하나를 선택하세요.

[포스팅 작성 규칙]
1. 제목은 검색 유입이 높고 클릭을 유도할 수 있는 키워드 중심으로 작성해주세요.
2. 마크다운 형식(#, ##, -, 테이블 등)을 활용해 가독성을 극대화해주세요.
3. 뇌피셜이 아닌 객관적이고 유용한 정보 위주로 구성하며, 광고 단가(CPC)가 높고 검색 수요가 꾸준한 내용으로 채워주세요.
4. 마지막에는 블로그 하단에 넣기 좋은 '핵심 요약 및 추천 태그(Labels)'를 5개 이상 적어주세요.
5. 전체 언어는 신뢰감 주는 한국어로 작성해주세요.
"""

# 4. Gemini에 요청하여 블로그 글 생성
response = model.generate_content(prompt)
post_content = response.text

# 5. posts 폴더 생성 및 마크다운 파일 저장
os.makedirs("posts", exist_ok=True)

date_str = datetime.now().strftime("%Y-%m-%d-%H%M%S")
file_name = f"posts/post-{date_str}.md"

with open(file_name, "w", encoding="utf-8") as f:
    f.write(post_content)

print(f"블로그 초안 생성 완료: {file_name}")
