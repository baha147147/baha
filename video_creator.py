import os
import random
import moviepy.editor as mp
from datetime import datetime
from google.cloud import texttospeech
import tweepy

class VideoCreator:
    def __init__(self):
        # Initialize APIs (use environment variables)
        self.tts_client = texttospeech.TextToSpeechClient()
        self.twitter_api = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN')
        )

    def create_video(self):
        """Main function to create and upload video"""
        try:
            print("🔄 Starting video creation...")
            
            # 1. Get trending topic
            topic = self.get_trending_topic()
            print(f"🔥 Trending Topic: {topic}")
            
            # 2. Generate script
            script = f"Today's trending topic is {topic}. Let's discuss!"
            
            # 3. Create voiceover
            voiceover = self.generate_voiceover(script)
            
            # 4. Make video
            self.render_video(
                topic=topic,
                voiceover_path=voiceover,
                output_path="output.mp4"
            )
            
            print("✅ Video created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

    def get_trending_topic(self):
        """Get random trending topic from Twitter"""
        trends = self.twitter_api.get_place_trends(id=1)  # Worldwide trends
        return random.choice([t['name'] for t in trends[0]['trends'][:5]])

    def generate_voiceover(self, text):
        """Convert text to speech"""
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-D"
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = self.tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        with open("voiceover.mp3", "wb") as out:
            out.write(response.audio_content)
        return "voiceover.mp3"

    def render_video(self, topic, voiceover_path, output_path):
        """Combine images/audio into video"""
        # Create simple video with text overlay
        clip = mp.ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=10)
        text = mp.TextClip(
            topic,
            fontsize=70,
            color='white',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=2
        ).set_position('center').set_duration(10)
        
        audio = mp.AudioFileClip(voiceover_path)
        final = mp.CompositeVideoClip([clip, text]).set_audio(audio)
        final.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )

if __name__ == "__main__":
    creator = VideoCreator()
    creator.create_video()