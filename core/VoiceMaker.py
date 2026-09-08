import edge_tts
import asyncio

class VoiceMaker:

    VOICE = "es-MX-JorgeNeural"

    @staticmethod
    async def generate_voice(text, output_path):
        communicate = edge_tts.Communicate(
            text,
            VoiceMaker.VOICE,
            rate="-5%",   # 5% slower: adds dramatic weight to narration
            pitch="-4Hz"  # Slightly deeper pitch: removes default AI assistant sharpness
        )
        await communicate.save(output_path)

    @staticmethod
    def create_audio(text, output_path):
        print(f"Generating audio at {output_path}")
        asyncio.run(VoiceMaker.generate_voice(text, output_path))


# test
"""
if __name__ == "__main__":
    print("Starting VoiceMaker test...")
    test_text = "Érase una vez, un pueblo fantasma en las oscuras calles de Alnarrín, un pueblo pequeño a las afueras de Moscú"
    output_path = "test_voice.mp3"
    VoiceMaker.create_audio(test_text, output_path)
    print(f" Check your project directory. You should see a file named {output_path}")
"""