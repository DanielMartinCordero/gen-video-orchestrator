import subprocess
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ComfyLauncher:
   BAT_PATH = os.getenv("COMFY_BAT_PATH")
   URL = os.getenv("COMFY_URL", "http://127.0.0.1:8188")

   @staticmethod
   def launch():
      result = False
      print("[ComfyLauncher] Trying to launch ComfyUI...")

      # 1. Get the directory that contains the .bat file
      bat_directory = os.path.dirname(ComfyLauncher.BAT_PATH)

      try:
         # 2. Launch specifying the 'cwd' (Current Working Directory)
         subprocess.Popen(
            ComfyLauncher.BAT_PATH,
            shell=True,
            cwd=bat_directory,
            creationflags=subprocess.CREATE_NEW_CONSOLE
         )
      except Exception as e:
         print(f"Critical error launching the process: {e}")
         return False

      timeout = 90 # 90 seconds to launch ComfyUI
      start_time = time.time()

      while (time.time() - start_time < timeout) and (not result):
         time.sleep(3) # Wait interval
         print(f"[ComfyLauncher] Waiting for server... ({int(time.time() - start_time)}s)")
         try:
            # Set a short request timeout to prevent blocking
            response = requests.get(ComfyLauncher.URL, timeout=5)
            if response.status_code == 200:
               print("[ComfyLauncher] ComfyUI is ready.")
               result = True
         except:
            # Connection errors are expected during startup
            pass

      return result
