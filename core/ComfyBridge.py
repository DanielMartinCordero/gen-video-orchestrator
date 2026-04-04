import requests
import json
import time

class ComfyBridge:
    def __init__(self, server_url="http://127.0.0.1:8188"):
        self.server_url = server_url

    def generate_image(self, workflow_data, prompt_text, id_prompt, id_latent):
        actual_workflow = json.loads(json.dumps(workflow_data))
        actual_workflow[id_prompt]["inputs"]["text"] = prompt_text
        actual_workflow[id_latent]["inputs"]["width"] = 512
        actual_workflow[id_latent]["inputs"]["height"] = 912

        payload = {
            "prompt": actual_workflow,
            "client_id": "creator_ai_orchestrator"
        }

        try:
            response = requests.post(f"{self.server_url}/prompt", json=payload)
            response.raise_for_status()
            # return prompt ID to find it later
            return response.json().get('prompt_id')
        except Exception as e:
            print(f"❌ [ComfyBridge] Error al conectar: {e}")
            return None

    def wait_for_image(self, prompt_id):
        """
        Polling: Ask server each 2 seconds if the image is already done
        """
        print(f"⏳ [ComfyBridge] Esperando a que la GPU termine (ID: {prompt_id})...")

        while True:
            try:
                # Check sever history for the specific prompt ID
                response = requests.get(f"{self.server_url}/history/{prompt_id}")
                history = response.json()

                # If the prompt is in the history, it means that the image is already done
                if prompt_id in history:
                    print("✅ [ComfyBridge] ¡Generación completada!")
                    # Extraemos el nombre del archivo del primer nodo que generó imágenes
                    outputs = history[prompt_id]['outputs']
                    for node_id in outputs:
                        if 'images' in outputs[node_id]:
                            return outputs[node_id]['images'][0]['filename']

                # If the process hasnt ended yet, wait 2 seconds before pulling again
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ [ComfyBridge] Consultando estado... ({e})")
                time.sleep(2)