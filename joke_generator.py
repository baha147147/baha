import pyttsx3
import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont
import random
import datetime
import os

# مجلد الإخراج
os.makedirs("output_videos", exist_ok=True)

# تحميل النكت
with open("jokes.txt", "r", encoding="utf-8") as f:
    jokes = [line.strip() for line in f.readlines() if line.strip()]

# توليد نكتة عشوائية
joke = random.choice(jokes)

# تحويل النص إلى صوت
tts = pyttsx3.init()
audio_file = "audio.mp3"
tts.save_to_file(joke, audio_file)
tts.runAndWait()

# إنشاء صورة من النكتة
img = Image.new("RGB", (1280, 720), color=(20, 20, 20))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
w, h = draw.textsize(joke, font=font)
draw.text(((1280 - w) / 2, (720 - h) / 2), joke, font=font, fill=(255, 255, 0))
img_path = "image.jpg"
img.save(img_path)

# تركيب فيديو
clip = mp.ImageClip(img_path).set_duration(7)
audio = mp.AudioFileClip(audio_file)
video = clip.set_audio(audio)

# اسم الفيديو حسب الوقت
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"output_videos/joke_{timestamp}.mp4"
video.write_videofile(output_path, fps=24)

print(f"✅ Done: {output_path}")
