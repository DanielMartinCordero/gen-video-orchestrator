import subprocess
import time
import requests
class ComfyLauncher:
   BAT_PATH = r"C:\Users\Dani34M04B\Desktop\ComfyUI.bat"
   URL = "http://127.0.0.1:8188"

   @staticmethod
   def launch():
      resultado = False
      print("Arrancando ComfyUI...")
      subprocess.Popen([ComfyLauncher.BAT_PATH], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
      timeout = 60
      start_time = time.time()

      while (time.time() - start_time < timeout) and (not resultado):
         time.sleep(2)
         print("Esperando a que el servidor responda...")
         try:
            response = requests.get(ComfyLauncher.URL)
            if(response.status_code == 200):
               print("ComfyUI esta listo")
               resultado = True
         except:
            pass
      return resultado
