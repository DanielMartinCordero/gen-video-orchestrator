import subprocess
import time
import requests
import os # Necesario para manejar rutas

class ComfyLauncher:
   # Ruta al .bat real
   BAT_PATH = r"C:\IA_ComfyUI\ComfyUI_windows_portable\run_nvidia_gpu.bat"
   URL = "http://127.0.0.1:8188"

   @staticmethod
   def launch():
      resultado = False
      print("🚀 Intentando arrancar ComfyUI...")

      # 1. Obtenemos la carpeta donde vive el .bat
      # Esto es vital para que el .bat encuentre sus dependencias
      bat_directory = os.path.dirname(ComfyLauncher.BAT_PATH)

      try:
         # 2. Lanzamos indicando el 'cwd' (Current Working Directory)
         subprocess.Popen(
            ComfyLauncher.BAT_PATH,
            shell=True,
            cwd=bat_directory, # <--- LA CLAVE: "Sitúate en esta carpeta antes de lanzar"
            creationflags=subprocess.CREATE_NEW_CONSOLE
         )
      except Exception as e:
         print(f"❌ Error crítico al lanzar el proceso: {e}")
         return False

      timeout = 90 # Subimos a 90 por si tu PC está cargando modelos pesados
      start_time = time.time()

      while (time.time() - start_time < timeout) and (not resultado):
         time.sleep(3) # Damos un respiro más largo entre intentos
         print(f"⏳ Esperando servidor... ({int(time.time() - start_time)}s)")
         try:
            # Ponemos un timeout pequeño a la petición para no bloquearnos
            response = requests.get(ComfyLauncher.URL, timeout=5)
            if response.status_code == 200:
               print("✅ [ComfyLauncher] ComfyUI está listo.")
               resultado = True
         except:
            # Es normal que falle mientras arranca
            pass

      return resultado
