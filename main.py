import os
import google.generativeai as genai
from datetime import datetime

# 1. API 키 설정
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

genai.configure(api_key=api_key)

# 2. 에러 메시지가 지시한 최신 모델로 적용
model = genai.GenerativeModel('gemini-3.6-flash')

# 3. 고단가 수익형 블로그 프롬프트
prompt = """
당신은 전문 금융, 부동산 및 IT 테크 블로거입니다.
구글 검색 엔진 최적화(SEO)에 최적화되어 있으며, 독자에게 실질적인 도움이 되고 신뢰성 있는 정보를 담은 블로그 포스팅 초안을 작성해주세요.

[주제 선정 가이드라인]
- 최신 부동산 제도/청약 정보, 실생활에 유용한 금융 상식(금리, 대출, 예적금 트렌드), 정부 지원 정책, 또는 고단가 IT/테크 트렌드 중 하나를 선택하세요.

[글쓰기 스타일 — 반드시 지켜주세요]
- AI가 쓴 것처럼 보이는 서식은 쓰지 마세요. 긴 대시(---) 구분선, ①②③ 같은 원문자 번호는 절대 쓰지 마세요.
- 자연스러운 문단과 소제목(##) 위주로 글을 구성하세요.
- 중간중간 "제가 직접 알아보니까~", "실제로 해보니~" 같은 경험담 느낌의 문장을 자연스럽게 섞어주세요. 딱딱한 정보 나열이 아니라 사람이 직접 조사하고 쓴 것처럼 써주세요.
- 중요한 부분은 **볼드체**로 강조하고, 필요하면 번호 목록이나 체크리스트, 표를 적절히 활용해 가독성을 높이세요.
- 뇌피셜이 아닌 객관적이고 유용한 정보 위주로 구성하며, 광고 단가(CPC)가 높고 검색 수요가 꾸준한 내용으로 채우세요.
- 제목은 검색 유입이 높고 클릭을 유도할 수 있는 키워드 중심으로 작성하세요.

[하지 말아야 할 것]
- 글 맨 아래에 해시태그(#태그) 뭉치나 "추천 태그(Labels)" 목록을 넣지 마세요. 대신 자연스러운 마무리 문단으로 글을 끝내세요.

전체 언어는 신뢰감 주는 한국어로 작성해주세요.
"""

# 4. 블로그 글 생성
try:
    response = model.generate_content(prompt)
    post_content = response.text
except Exception as e:
    raise RuntimeError(f"Gemini API 호출 중 오류 발생: {e}")

# 5. posts 폴더 생성 및 마크다운 파일 저장
os.makedirs("posts", exist_ok=True)
date_str = datetime.now().strftime("%Y-%m-%d-%H%M%S")
file_name = f"posts/post-{date_str}.md"

with open(file_name, "w", encoding="utf-8") as f:
    f.write(post_content)

print(f"블로그 초안 생성 완료: {file_name}")
