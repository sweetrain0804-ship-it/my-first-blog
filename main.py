import os
import google.generativeai as genai

# 1. GitHub Secrets에 등록한 API 키 불러오기
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

# 2. Gemini API 설정
genai.configure(api_key=api_key)

# 3. 사용할 Gemini 모델 선택 (최신 1.5 Flash 모델 활용)
model = genai.GenerativeModel ("gemini-2.5-flash")


def generate_blog_content():
  # 무한 글감 추천 및 블로그 본문 생성을 위한 프롬프트
  prompt = """
    블로그에 발행할 매력적이고 트렌디한 IT/테크 관련 주제 하나를 스스로 선정하고, 
    그 주제에 대한 블로그 포스팅 초안을 작성해줘.
    
    출력 형식:
    [주제] (여기에 주제 작성)
    [본문] (여기에 마크다운 형식의 알찬 본문 작성)
    """

  print("🤖 Gemini가 글감을 고민하고 블로그 글을 작성 중입니다...")
  response = model.generate_content(prompt)

  return response.text


if __name__ == "__main__":
  blog_post = generate_blog_content()
  print("\n--- 생성된 블로그 글 결과 ---\n")
  print(blog_post)

