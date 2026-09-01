import os
import google.genai as genai


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

client = genai.Client(api_key=api_key)

def generate_blog_content():
    prompt = """
    블로그에 발행할 매력적이고 트렌디한 IT/테크 관련 주제를 정하고,
    그 주제에 대한 블로그 포스팅 초안을 작성해줘.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    print(response.text)

if __name__ == "__main__":
    generate_blog_content()
