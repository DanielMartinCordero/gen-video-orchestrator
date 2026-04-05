import os
import json
import shutil

from core.ComfyBridge import ComfyBridge
from core.ComfyLauncher import ComfyLauncher
from core.models.TiktokFacebookModel import TiktokFacebookModel


def main():
    # Turning on ComfyUI
    if not ComfyLauncher.launch():
        print("❌ El sistema no pudo arrancar ComfyUI. Abortando...")
        return

    # Harcoded paths
    COMFY_OUTPUT_PATH = r"C:\IA_ComfyUI\ComfyUI_windows_portable\ComfyUI\output"
    LOCAL_OUTPUT_PATH = "output"
    WORKFLOW_PATH = os.path.join("workflows", "workflow_flux_api.json")

    # Check if exits local folder
    if not os.path.exists(LOCAL_OUTPUT_PATH):
        os.makedirs(LOCAL_OUTPUT_PATH)

    # Load JSON to workflow_data
    try:
        with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
            workflow_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encuentra el archivo en {WORKFLOW_PATH}")
        return

    bridge = ComfyBridge()

    app_engine = TiktokFacebookModel(bridge)

    # Start image generation
    tema_prueba = "A dark fantasy knight, glowing blue eyes, rain, hyper-realistic, 8k"
    print(f"--- Iniciando Pipeline para: {tema_prueba} ---")

    prompt_id = app_engine.generate_content(tema_prueba, workflow_data)

    if prompt_id:
        # Python wait until the file exists
        filename = bridge.wait_for_image(prompt_id)

        if filename:
            # Move file to our local carpet
            source_file = os.path.join(COMFY_OUTPUT_PATH, filename)
            destination_file = os.path.join(LOCAL_OUTPUT_PATH, filename)

            if os.path.exists(source_file):
                # We use shutil.move to avoid filling the disk with duplicates
                shutil.move(source_file, destination_file)
                print(f"✨ ¡Éxito! Imagen rescatada y guardada en: {destination_file}")
            else:
                print(f"⚠️ El archivo {filename} se generó pero no se encuentra en la ruta origen.")
    else:
        print("❌ El Bridge no pudo iniciar la tarea.")

if __name__ == "__main__":
    main()