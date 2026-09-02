import os
from google import genai
from gtts import gTTS

# 1. Gemini API를 이용해 쇼츠 대본 생성
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="유튜브 쇼츠용 30초 대본을 한 줄씩 3~4문장으로 짧고 강렬하게 작성해줘. 주제: 2026년 청년들이 꼭 알아야 할 돈 모으기 꿀팁. 다른 부가 설명 없이 대본 텍스트만 출력해줘.",
)

script_text = response.text.strip()
print(f"생성된 대본:\n{script_text}")

# 2. 대본을 음성(TTS) 파일로 변환
tts = gTTS(text=script_text, lang='ko')
audio_path = "output_short.mp3"
tts.save(audio_path)

print(f"오디오 음성 파일 생성 완료: {audio_path}")
