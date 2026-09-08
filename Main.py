import os
import json
import random
import shutil

from core.ComfyBridge import ComfyBridge
from core.ComfyLauncher import ComfyLauncher
from core.models.TiktokFacebookModel import TiktokFacebookModel
from core.ContentStrategist import ContentStrategist
from core.StoryMaker import StoryMaker
from core.VoiceMaker import VoiceMaker
from core.VideoEditor import VideoEditor

def main():
    # Turning on ComfyUI

    if not ComfyLauncher.launch():
        print("System failed to launch ComfyUI. Stopping...")
        return

    # Harcoded paths
    COMFY_OUTPUT_PATH = r"C:\IA_ComfyUI\ComfyUI_windows_portable\ComfyUI\output"
    LOCAL_OUTPUT_PATH = "output"
    WORKFLOW_PATH = os.path.join("workflows", "workflow_flux_api.json")
    HISTORICAL_TOPICS = [
        # 1. Ancient medicine or extreme treatments
        "Bizarre, lethal, or extreme historical medical treatments and surgeries before modern anesthesia",
        # 2. Collective hysteria and psychological outbreaks
        "Historical mass psychogenic illnesses, unexplained collective hysterias, and bizarre social contagions",
        # 3. Extreme judicial methods and historical punishments
        "Brutal judicial punishments, bizarre historical trials (including animals or dead bodies), and legal ordeals",
        # 4. Psychological warfare tactics and medieval sieges
        "Extreme psychological warfare, horrifying siege tactics, and early biological strategies in ancient and medieval warfare",
        # 5. Pandemics, forgotten plagues, and lethal outbreaks
        "Devastating historical epidemics, forgotten plagues, and extreme quarantine methods across ancient civilizations",
        # 6. Extreme survival scenarios and historical famines
        "Catastrophic historical famines, harsh winters, and documented extreme survival scenarios in human history",
        # 7. Extreme conditions and unsanitary hygiene in ancient cities
        "The disturbing, toxic, and grotesque daily hygiene, living conditions, and sanitation hazards of pre-industrial cities",
        # 8. Extreme religious fanaticism and doomsday cults
        "Apocalyptic cults, flagellant movements, and extreme religious rituals driven by fear in historical crises",
        # 9. Bizarre urban accidents and historical disasters
        "Unusual, bizarre, and deadly historical accidents, fires, and structural catastrophes caused by human error or greed",
        # 10. Disappearances and failed historical expeditions
        "Disastrous historical expeditions, doomed voyages, and documented expeditions where whole groups vanished or starved"
    ]
    # Check if exists local folder
    if not os.path.exists(LOCAL_OUTPUT_PATH):
        os.makedirs(LOCAL_OUTPUT_PATH)

    # Load JSON to workflow_data
    try:
        with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
            workflow_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found at {WORKFLOW_PATH}")
        return

    bridge = ComfyBridge()
    app_engine = TiktokFacebookModel(bridge)
    config = ContentStrategist.get_random_config()
    maker = StoryMaker()

    theme = random.choice(HISTORICAL_TOPICS)
    script = maker.generate_script(theme, config)

    if not script:
        print("Something went wrong while generating the script.")
        return

    for scene_selected in script:
        # We take each data from its apart in our dictionary, created in StoryMaker
        # To avoid errors in Windows, we use zfill(2) to add a 0 ahead the number
        num_scene = str(scene_selected['scene']).zfill(2)
        prompt_voice = scene_selected['narration']
        prompt_image = scene_selected['visual_prompt']

        print(f"---Processing scene: {num_scene}---")

        # --- CREATE AUDIO ---
        audio_name = f"scene_{num_scene}.mp3"
        audio_path = os.path.join(LOCAL_OUTPUT_PATH, audio_name)

        print(f"🎙️ Recording voice: '{prompt_voice}'")
        VoiceMaker.create_audio(prompt_voice, audio_path)

        # --- CREATE IMAGE ---
        prompt_id = app_engine.generate_content(prompt_image, workflow_data)

        if prompt_id:
            # The program waits until the file exists
            filename = bridge.wait_for_image(prompt_id)

            if filename:
                # Move file to our local folder
                source_file = os.path.join(COMFY_OUTPUT_PATH, filename)
                image_name = f"scene_{num_scene}.png"
                destination_file = os.path.join(LOCAL_OUTPUT_PATH, image_name)

                if os.path.exists(source_file):
                    shutil.copy2(source_file, destination_file)
                    print(f" Image retrieved and saved to: {destination_file}")
                else:
                    print(f" File {filename} was generated but could not be found at source path.")
        else:
            print(" Bridge failed starting the task.")

    print("---- Images and audio successfully generated ----")


    VideoEditor.render_video(LOCAL_OUTPUT_PATH, "tiktok_documentary.mp4")
    print("---PRODUCTION COMPLETED---")
if __name__ == "__main__":
    main()