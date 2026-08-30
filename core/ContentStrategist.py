import random

class ContentStrategist:
    STYLES = ["Dark Fantasy, Cinematic lighting, 35mm lens",
              "Gothic Oil Painting, thick brushstrokes, moody dark tones",
              "Noir Film, high contrast, grainy texture, 1940s aesthetic",
              "Hyper-realistic Unreal Engine 5 render, volumetric fog",
              "Vintage 16mm film, muted colors, mystical atmosphere"]
    EMOTIONS = ["Terrifying", "Melancholic", "Epic & Heroic", "Mysterious", "Aggressive"]
    PERSPECTIVES = ["First-person: The character is talking to the viewer",
                    "Third-person: An omniscient narrator telling a legend",
                    "Found footage: Raw, shaky, and mysterious perspective"]

    @staticmethod
    def get_random_config():
        return {
            "num_scenes": random.randint(12, 15),
            "style": random.choice(ContentStrategist.STYLES),
            "emotion": random.choice(ContentStrategist.EMOTIONS),
            "pov": random.choice(ContentStrategist.PERSPECTIVES),
            "seed": random.randint(0, 999999) # Para Flux
        }