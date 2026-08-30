import edge_tts
import asyncio

class VoiceMaker:

    VOICE = "es-MX-JorgeNeural"

    @staticmethod
    async def generate_voice(text, output_path):
        communicate = edge_tts.Communicate(text, VoiceMaker.VOICE)
        await communicate.save(output_path)

    @staticmethod
    def create_audio(text, output_path):
        print(f"Generando audio en {output_path}")
        asyncio.run(VoiceMaker.generate_voice(text, output_path))

if __name__ == "__main__":
    print("Iniciando test de VoiceMaker...")
    texto_prueba = "Érase una vez, un pueblo fantasma en las oscuras calles de Alnarrín, un pueblo pequeño a las afueras de Moscú"
    ruta_salida = "test_voz.mp3"
    VoiceMaker.create_audio(texto_prueba, ruta_salida)
    print(f"✅ Revisa la carpeta de tu proyecto. Deberías tener un archivo llamado {ruta_salida}")
