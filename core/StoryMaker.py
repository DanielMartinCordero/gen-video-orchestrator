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
        # PROMPT MAESTRO: Enfoque Documental y Retención TikTok
        master_prompt = f"""
        ROLE: Expert Educational Content Creator & Historian for TikTok (like History Channel meets TikTok viral hooks).
        TASK: Generate a {config['num_scenes']}-scene script based on the TOPIC: "{user_topic}".
        
        ATMOSPHERE AND TONE: {config['emotion']}
        VISUAL STYLE: {config['style']}
        NARRATIVE POV: {config['pov']}
        
        STORYTELLING RULES (CRITICAL):
        1. HOOK: Scene 1 MUST start with a shocking, real historical hook (e.g., "¿Sabías que en...", "El dato más aterrador y real sobre...").
        2. FACTUAL & REAL: Do NOT invent fantasy stories, monsters, or magic. The script must explain REAL historical facts, real dates, and real human behavior related to the topic.
        3. PACE: Fast-paced, educational, and highly engaging. Designed to prevent scrolling.
        4. NARRATION: 20-30 words per scene, written in fluid, conversational SPANISH. 
        
        IMAGE GENERATION RULES (Visual Prompts):
        - Style: Gritty historical realism, dark cinematic lighting, highly detailed.
        - TONE (CRITICAL): Raw, unsettling, and slightly macabre. Do NOT sanitize the past. Show the grim and harsh reality of the era (dirt, despair, eerie medical practices, plague signs).
        - Composition: Vertical 9:16, medium or close-up shots for TikTok. High contrast.
        - Language: Visual prompts MUST be in English.

        OUTPUT FORMAT:
        You must return ONLY a JSON array of objects. No intro text, no markdown code blocks.
        JSON Structure:
        [
          {{
            "scene": 1,
            "narration": "Spanish text for the voiceover...",
            "visual_prompt": "Highly detailed English prompt for the image generator..."
          }}
        ]
        """

        try:
            response = self.client.models.generate_content(
                model= self.model_name,
                contents=master_prompt
            )
            print("El prompt general es: "+response.text)

            # Limpieza de seguridad por si la IA añade markdown (```json ...)
            raw_text = response.text.replace('```json', '').replace('```', '').strip()

            script = json.loads(raw_text)
            print(f"✅ [Storyteller] Guion generado con {len(script)} escenas.")
            return script
        except Exception as e:
            print(f"❌ [Storyteller] Error crítico en la generación o parseo: {e}")
            return None