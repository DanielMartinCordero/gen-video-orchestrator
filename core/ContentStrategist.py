import random

class ContentStrategist:
    # Estilos enfocados en reconstrucción histórica y realismo fotográfico
    STYLES = [
        "Historical documentary reconstruction, cinematic realism, 8k resolution, authentic costumes",
        "National Geographic photography style, ultra-realistic, historical accuracy, natural lighting",
        "Photorealistic cinematic shot, high-end historical drama, 35mm lens, highly detailed"
    ]
    # Emociones enfocadas en la divulgación y la intriga
    EMOTIONS = ["Intriguing and educational", "Shocking historical truth", "Fascinating and dramatic"]
    PERSPECTIVES = [
        "Educational TikToker explaining a mind-blowing real historical event",
        "Documentary narrator uncovering hidden facts from history"
    ]

    @staticmethod
    def get_random_config():
        return {
            "num_scenes": 4, # Mantenemos 4 para que la prueba sea rápida
            "style": random.choice(ContentStrategist.STYLES),
            "emotion": random.choice(ContentStrategist.EMOTIONS),
            "pov": random.choice(ContentStrategist.PERSPECTIVES),
            "seed": random.randint(0, 999999)
        }