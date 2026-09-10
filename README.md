# Autonomous AI Video Generation Pipeline

An end-to-end, fully automated pipeline in Python designed to generate vertical short-form video content (TikTok, YouTube Shorts, Instagram Reels) from scratch. The system autonomously handles scriptwriting, neural voice synthesis, local generative image rendering, and dynamic video editing.

---

## ⚡ Key Features

* **Autonomous Scriptwriting**: Powered by Google's `gemini-2.5-flash` via the official `google-genai` SDK, producing structured, multi-scene documentary scripts with retention-focused hooks.
* **Local Generative Imaging**: Integrates seamlessly with a local ComfyUI instance running the **Flux** diffusion model via API polling.
* **Subprocess Management**: Automatically boots the local ComfyUI portable environment on startup if it is not already running.
* **Neural Voice Synthesis**: Generates conversational voiceover tracks using `edge-tts` with custom cadence and pitch modulation.
* **Dynamic Video Assembly**: Uses `moviepy` to assemble scenes, apply progressive **Zoom-in** motion effects, and synchronize audio with visual assets.
* **Fault-Tolerant Execution**: Built-in exponential retry loops and exceptions, to mitigate API rate limits and network latency in image, audio or text generation.

---

## 🏗️ Architecture & Pipeline Flow

```text
       ┌──────────────────────┐
       │       Main.py        │  ◄── Strategy Selector (Random Seed / Topic)
       └──────────┬───────────┘
                  │
        [1] Topic & Framing
                  ▼
       ┌──────────────────────┐
       │   StoryMaker (LLM)   │  ──► Google Gemini 2.5 Flash API
       └──────────┬───────────┘
                  │  Outputs Scene JSON (Narrations + Flux Prompts from Google Gemini 2.5 Flash)
                  ├───────────────────────────────┐
                  ▼                               ▼
       ┌──────────────────────┐       ┌──────────────────────┐
       │  VoiceMaker (Audio)  │       │  ComfyBridge (Images)│
       └──────────┬───────────┘       └──────────┬───────────┘
                  │                               │
        edge-tts (.mp3)                 Local ComfyUI / Flux (.png)
                  │                               │
                  └───────────────┬───────────────┘
                                  ▼
                      ┌──────────────────────┐
                      │     VideoEditor      │  ──► Zoom-in FX and Concatenation
                      └──────────┬───────────┘
                                  ▼
                      ┌──────────────────────┐
                      │ final_video.mp4 (9:16)│
                      └──────────────────────┘
```

---

## 📁 Repository Structure

```text
├── core/
│   ├── models/
│   │   ├── BaseModel.py           # Abstract base class for model adapters
│   │   ├── TiktokFacebookModel.py # 9:16 vertical aspect ratio configuration
|   |   └── [Future models].py 
│   ├── ComfyBridge.py             # HTTP API connector and polling worker for ComfyUI
│   ├── ComfyLauncher.py           # Subprocess runner for automatic GPU initialization
│   ├── ContentStrategist.py       # Randomizer for narrative styles, tones, and seeds
│   ├── StoryMaker.py              # Gemini prompt orchestration and JSON extraction
│   ├── VideoEditor.py             # MoviePy renderer with Ken Burns dynamic motion
│   └── VoiceMaker.py              # Async TTS synthesizer (Edge-TTS)
├── workflows/
│   └── workflow_flux_api.json     # Exported ComfyUI Flux API schema
├── output/                        # Ignored directory for intermediate assets & final video
├── .gitignore                     # Git rules to exclude cache, environments, and media
├── Main.py                        # Pipeline entry point and orchestrator
├── README.md                      # Project documentation
└── requirements.txt               # Pinned Python package dependencies
```

---

## 🛠️ Prerequisites

* **OS**: Windows 10/11 (with CUDA-capable GPU).
* **Python**: `3.10.x` or higher.
* **Hardware**: Dedicated NVIDIA GPU with at least 8 GB VRAM (for running Flux locally).
* **Local Diffusion Engine**: ComfyUI portable installed locally.
* **Google Gemini API Key**: Obtainable from Google AI Studio.

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone <YOUR_REPOSITORY_URL>
cd AI-Generator
```

### 2. Set up a virtual environment
```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Update local system paths
Verify that the paths in `Main.py` and `core/ComfyLauncher.py` match your local ComfyUI installation:
```python
# core/ComfyLauncher.py
BAT_PATH = r"C:\path\to\your\ComfyUI_windows_portable\run_nvidia_gpu.bat"

# Main.py
COMFY_OUTPUT_PATH = r"C:\path\to\your\ComfyUI_windows_portable\ComfyUI\output"
```

---

## 💻 Usage

Run the main pipeline:

```bash
python Main.py
```

The system will:
1. Ping and initialize your local ComfyUI server.
2. Select a topic and generate a cohesive narrative script.
3. Concurrently synthesize voiceovers and queue image generation.
4. Apply Ken Burns camera movements and export the final video to `output/tiktok_documentary.mp4`.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
