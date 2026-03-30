import requests # Librería externa para HTTP
import json     # Librería nativa (no necesita instalación)

class ComfyBridge:
    def __init__(self, server_url="http://127.0.0.1:8188"):

        self.server_url = server_url

    def generate_image(self, workflow_data, prompt_text, id_prompt, id_latent):
        """With the prompt, ask Comfy Ui to generate a picture or video"""

        # Clonamos el diccionario (Deep Copy) para evitar efectos secundarios
        actual_workflow = json.loads(json.dumps(workflow_data))

        # Inyectamos valores
        actual_workflow[id_prompt]["inputs"]["text"] = prompt_text
        actual_workflow[id_latent]["inputs"]["width"] = 512
        actual_workflow[id_latent]["inputs"]["height"] = 912

        payload = {
            "prompt": actual_workflow,
            "client_id": "creator_ai_orchestrator" # Corregido typo: orchestrator
        }

        try:
            # Usamos la variable correcta: self.server_url
            response = requests.post(f"{self.server_url}/prompt", json=payload)
            response.raise_for_status()

            # Devolvemos el ID de la tarea para poder rastrearla luego
            return response.json().get('prompt_id')

        except Exception as e:
            print(f"❌ [ComfyBridge] Error al conectar: {e}")
            return None