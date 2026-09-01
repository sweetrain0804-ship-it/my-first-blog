import os
import datetime
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

genai.configure(api_key=api_key)

def generate_blog_content():
    prompt = """
    블로그(usunsee.blogspot.com)에 발행할 매력적이고 트렌디한 IT/테크 관련 주제로 
    모바일에서 읽기 좋은 블로그 포스팅 초안을 작성해줘. 
    마크다운 형식을 활용해서 깔끔하게 작성해줘.
    """
    model = genai.GenerativeModel('gemini-3.6-flash')
    response = model.generate_content(prompt)
    return response.text

def save_to_file(content):
    os.makedirs("posts", exist_ok=True)
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    file_path = f"posts/draft-{today}.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"초안 파일이 성공적으로 저장되었습니다: {file_path}")

if __name__ == "__main__":
    print("Gemini 블로그 콘텐츠 생성 시작...")
    content = generate_blog_content()
    save_to_file(content)
    print("콘텐츠 생성 및 저장 완료!")
