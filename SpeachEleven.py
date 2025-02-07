import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
import base64
# Load environment variables
load_dotenv()

# Initialize the ElevenLabs client
client = ElevenLabs(
    api_key=os.getenv("ELEVEN_API_KEY")  # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

def audioGenerating(text):
    try:
        # Generate audio
        audio_generator = client.generate(
            text=text,
            voice="a1KZUXKFVFDOb33I1uqr",  #Adam, #Lily, #Alice
            model="eleven_multilingual_v2"
        )

        # Combine the generator's output into a bytes object
        audio_bytes = b"".join(audio_generator)

        # Save the generated audio to a file
        with open("sounds/output_audio.mp3", "wb") as file:
            file.write(audio_bytes)

        print("Audio saved as output_audio.mp3")
        
        #encodeed audio for send-to-Nodejs
        with open("./sounds/output_audio.mp3", "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')

        return encoded_audio, 200
    except BaseException as e:
        return e, 400