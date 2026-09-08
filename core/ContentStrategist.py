import random

class ContentStrategist:
    # Styles focused on historical reconstruction and photographic realism
    STYLES = [
        "Historical documentary reconstruction, cinematic realism, 8k resolution, authentic costumes",
        "National Geographic photography style, ultra-realistic, historical accuracy, natural lighting",
        "Photorealistic cinematic shot, high-end historical drama, 35mm lens, highly detailed"
    ]
    # Emotions focused on educational outreach, intrigue, and drama
    EMOTIONS = ["Intriguing and educational", "Shocking historical truth", "Fascinating and dramatic", "Interested and passionate"]
    PERSPECTIVES = [
        "Educational TikToker explaining a mind-blowing real historical event",
        "Documentary narrator uncovering hidden facts from history"
    ]

    @staticmethod
    def get_random_config():
        return {
            "num_scenes": random.randint(8, 15),
            "style": random.choice(ContentStrategist.STYLES),
            "emotion": random.choice(ContentStrategist.EMOTIONS),
            "pov": random.choice(ContentStrategist.PERSPECTIVES),
            "seed": random.randint(0, 999999)
        }