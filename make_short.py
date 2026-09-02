import os
from google import genai
from gtts import gTTS
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, TextClip

# 1. Gemini API를 이용해 쇼츠 대본 생성
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="유튜브 쇼츠용 30초 대본을 한 줄씩 3~4문장으로 짧고 강렬하게 작성해줘. 주제: 2026년 청년들이 꼭 알아야 할 돈 모으기 꿀팁. 다른 부가 설명 없이 대본 텍스트만 출력해줘.",
)

script_text = response.text.strip()
print(f"생성된 대본:\n{script_text}")

# 2. 대본을 음성(TTS) 파일로 변환
audio_path = "temp_voice.mp3"
tts = gTTS(text=script_text, lang='ko')
tts.save(audio_path)

# 3. MoviePy로 세로형 쇼츠 영상(mp4) 생성
audio_clip = AudioFileClip(audio_path)
duration = audio_clip.duration

# 세로형 쇼츠 비율(1080x1920) 배경 클립
bg_clip = ColorClip(size=(1080, 1920), color=(15, 23, 42), duration=duration)

# 4. 자막 텍스트 클립 추가 (한글 폰트 지정 및 자동 줄바꿈 적용)
try:
    txt_clip = TextClip(
        script_text,
        fontsize=60,
        color='white',
        font='/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
        size=(900, None),
        method='caption'
    ).set_duration(duration).set_position('center')

    video = CompositeVideoClip([bg_clip, txt_clip]).set_audio(audio_clip)
except Exception as e:
    print(f"자막 생성 실패 이유: {repr(e)}")
    video = bg_clip.set_audio(audio_clip)

# 5. 최종 MP4 영상 파일로 저장
output_video_path = "output_short.mp4"
video.write_videofile(
    output_video_path,
    fps=24,
    codec='libx264',
    audio_codec='aac'
)

print(f"쇼츠 영상 및 자막 생성 완료: {output_video_path}")
