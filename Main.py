import os
import json
import shutil

from core.ComfyBridge import ComfyBridge
from core.ComfyLauncher import ComfyLauncher
from core.models.TiktokFacebookModel import TiktokFacebookModel
from core.ContentStrategist import ContentStrategist
from core.StoryMaker import StoryMaker
from core.VoiceMaker import VoiceMaker

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
    config = ContentStrategist.get_random_config()
    maker = StoryMaker()

    tema = "Medieval life in Europe during diseases"
    script = maker.generate_script(tema, config)

    if not script:
        print("Something went wrong while generating the script.")
        return

    for scene_selected in script:
        # We take each data from its apart in our dictionary, created in StoryMaker
        # To avoid errors in Windows, we use zfill(2) to add a 0 ahead the number
        num_scene = str(scene_selected['scene']).zfill(2)
        prompt_voice = scene_selected['narration']
        prompt_image = scene_selected['visual_prompt']

        print(f"---Procesando escena número: {num_scene}---")

        # --- CREATE AUDIO ---
        audio_name = f"scene_{num_scene}.mp3"
        audio_path = os.path.join(LOCAL_OUTPUT_PATH, audio_name)

        print(f"🎙️ Grabando voz: '{prompt_voice}'")
        VoiceMaker.create_audio(prompt_voice, audio_path)

        # --- CREATE IMAGE ---
        prompt_id = app_engine.generate_content(prompt_image, workflow_data)

        if prompt_id:
            # The program waits until the file exists
            filename = bridge.wait_for_image(prompt_id)

            if filename:
                # Move file to our local carpet
                source_file = os.path.join(COMFY_OUTPUT_PATH, filename)
                image_name = f"scene_{num_scene}.png"
                destination_file = os.path.join(LOCAL_OUTPUT_PATH, image_name)

                if os.path.exists(source_file):
                    # We use shutil.move to avoid filling the disk with duplicates
                    shutil.copy2(source_file, destination_file)
                    print(f"✨ ¡Éxito! Imagen rescatada y guardada en: {destination_file}")
                else:
                    print(f"⚠️ El archivo {filename} se generó pero no se encuentra en la ruta origen.")
        else:
            print("❌ El Bridge no pudo iniciar la tarea.")

    print("---PRODUCCIÓN TERMINADA---")
if __name__ == "__main__":
    main()