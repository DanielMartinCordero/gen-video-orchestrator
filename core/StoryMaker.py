import os
import json
import time

from google import genai
from dotenv import load_dotenv

class StoryMaker:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(" [StoryMaker] Error: GEMINI_API_KEY not found in .env file")

        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'

    def generate_script(self, user_topic, config):
        print(f" [StoryMaker] Orchestrating script for: {user_topic}")

        #  MASTER PROMPT: Documental Approach & TikTok Retention
        master_prompt = f"""
        ROLE: Expert Educational Content Creator & Historian for TikTok (like History Channel meets TikTok viral hooks).
        TASK: Generate a {config['num_scenes']}-scene script based on the TOPIC: "{user_topic}".
        
        ATMOSPHERE AND TONE: {config['emotion']}
        VISUAL STYLE: {config['style']}
        NARRATIVE POV: {config['pov']}
        
        STORYTELLING RULES (CRITICAL):
        1. HOOK: Scene 1 MUST start with a shocking, real historical hook (e.g., "¿Sabías que en...", "El dato más aterrador y real sobre...").
        2. FACTUAL & REAL: Do NOT invent fantasy stories, monsters, or magic. The script must explain in most real historical facts, and real human behavior related to the topic.
        3. PACE: Fast-paced, educational, and highly engaging. Designed to prevent scrolling.
        4. NARRATION: Max 30 words per scene, written in fluid, conversational SPANISH. 
        5. SPECIFIC EVENT SELECTION: The topic is broad. You MUST pick ONE specific, real, and documented historical event, individual, or practice within this category. Avoid the most cliché examples; prioritize obscure, shocking, and factual historical accounts.
        
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
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                response = self.client.models.generate_content(
                    model= self.model_name,
                    contents=master_prompt
                )
                print("Answer from Gemini: "+response.text)

                # Safety sanitization in case the model wraps output in markdown code blocks
                raw_text = response.text.replace('```json', '').replace('```', '').strip()

                script = json.loads(raw_text)
                print(f"[Storyteller] Script generated with {len(script)} scenes.")
                return script

            except Exception as e:
                if attempt < max_attempts -1:
                    print(f"Error sending the prompt (attempt {attempt + 1}/{max_attempts}), retrying in 10s...")
                    time.sleep(10)
                else:
                    print("Critical communication error, retries exhausted. ")
                    print(f"Error: {e}")
        return None