import os
from google import genai
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip

# 1. Gemini API를 이용해 쇼츠 대본 생성 (안정적인 모델명 사용)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="유튜브 쇼츠용 30초 대본을 한 줄씩 3~4문장으로 짧고 강렬하게 작성해줘. 주제: 2026년 청년들이 꼭 알아야 할 돈 모으기 꿀팁. 다른 부가 설명 없이 대본 텍스트만 출력해줘.",
)

script_text = response.text.strip()
print(f"생성된 대본:\n{script_text}")

# 2. 대본을 음성(TTS) 파일로 변환
audio_path = "temp_voice.mp3"
tts = gTTS(text=script_text, lang='ko')
tts.save(audio_path)

# 3. MoviePy로 세로형 쇼츠 영상(mp4) 생성 (텍스트 충돌 에러 방지용 안정적 배경 합성)
audio_clip = AudioFileClip(audio_path)
duration = audio_clip.duration

# 세로형 쇼츠 비율(1080x1920) 배경 클립 생성
bg_clip = ColorClip(size=(1080, 1920), color=(15, 23, 42), duration=duration)

# 오디오 결합
video = bg_clip.set_audio(audio_clip)

# 4. 최종 MP4 영상 파일로 렌더링
output_video_path = "output_short.mp4"
video.write_videofile(
    output_video_path, 
    fps=24, 
    codec='libx264', 
    audio_codec='aac',
    logger=None # 로그 출력 간소화로 에러 예방
)

print(f"쇼츠 영상 생성 완료: {output_video_path}")
