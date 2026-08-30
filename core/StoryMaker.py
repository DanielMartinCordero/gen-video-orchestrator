import os
import json

from google import genai
from dotenv import load_dotenv
from core.ContentStrategist import ContentStrategist

class StoryMaker:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ No se encontró GEMINI_API_KEY en el archivo .env")

        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'

    def generate_script(self, user_topic, config):
        print(f"🧠 [Storyteller] Orquestando guion para: {user_topic}")

        # PROMPT MAESTRO: Estructura profesional y técnica
        master_prompt = f"""
        ROLE: Expert Viral Content Creator & Dark Fantasy Scriptwriter.
        TASK: Generate a {config['num_scenes']}-scene narrative script based on the TOPIC: "{user_topic}".
        
        ATMOSPHERE AND TONE: {config['emotion']}
        VISUAL STYLE: {config['style']}
        NARRATIVE POV: {config['pov']}
        
        STORYTELLING RULES:
        1. HOOK: Scene 1 must present a high-stakes conflict or a mysterious visual.
        2. TENSION: Scenes 2 to the penultimate must escalate the dark atmosphere or historical drama.
        3. RESOLUTION: The final scene must provide a cinematic or philosophical closure.
        4. CONCISION: Narration text must be impactful, short (max 15 words per scene), and IN SPANISH.
        
        IMAGE GENERATION RULES (Visual Prompts):
        - Follow the VISUAL STYLE requested exactly.
        - Composition: Vertical 9:16, medium or close-up shots for TikTok.
        - Language: Visual prompts MUST be in English for maximum compatibility with Flux.

        OUTPUT FORMAT:
        You must return ONLY a JSON array of objects. No intro text, no markdown code blocks.
        JSON Structure:
        [
          {{
            "scene": 1,
            "narration": "Spanish text for the voiceover",
            "visual_prompt": "Highly detailed English prompt for the image generator"
          }}
        ]
        """
        print("El prompt general es: "+master_prompt)

        try:
            response = self.client.models.generate_content(
                model= self.model_name,
                contents=master_prompt
            )
            # Limpieza de seguridad por si la IA añade markdown (```json ...)
            raw_text = response.text.replace('```json', '').replace('```', '').strip()

            script = json.loads(raw_text)
            print(f"✅ [Storyteller] Guion generado con {len(script)} escenas.")
            return script
        except Exception as e:
            print(f"❌ [Storyteller] Error crítico en la generación o parseo: {e}")
            return None