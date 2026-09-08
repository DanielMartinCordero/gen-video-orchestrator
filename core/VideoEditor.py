import os

from PIL import Image

# --- COMPATIBILITY PATCH FOR MOVIEPY ---
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

class VideoEditor:
    @staticmethod
    def zoom_effect(clip):
        zoom_ratio = 0.15
        """
        Zoom in effect: scales the image progressively throughout the clip duration.
        """
        w, h = clip.size

        # Mathematical function calculating scale per frame (t = current second, passed by MoviePy resize function)
        def resize_func(t):
            return 1 + (zoom_ratio * (t / clip.duration))

        # 1. Apply progressive scaling to the image
        zoomed_clip = clip.resize(resize_func)

        # 2. Center crop to keep resolution (w, h) constant
        final_clip = zoomed_clip.crop(x_center=w/2, y_center=h/2, width=w, height=h)
        return final_clip

    @staticmethod
    def render_video(local_folder, output_filename="video_final.mp4"):
        print("------ STARTING FINAL ASSEMBLY... ------")

        clips = []
        files = sorted(os.listdir(local_folder))
        images = []
        for image in files :
            if image.endswith(".png") and image.startswith("scene_"):
                images.append(image)

        if not images:
            print(" [VideoEditor] No scene images found in directory.")
            return False

        for img_name in images:
            base_name = img_name.split('.')[0]
            audio_name = f"{base_name}.mp3"

            img_path = os.path.join(local_folder, img_name)
            audio_path = os.path.join(local_folder, audio_name)

            if os.path.exists(audio_path):
                print(f"Assembling and applying zoom to: {base_name}")

                audio_clip = AudioFileClip(audio_path)
                video_clip = ImageClip(img_path).set_duration(audio_clip.duration)

                # Apply motion zoom effect
                video_clip = VideoEditor.zoom_effect(video_clip)

                video_clip = video_clip.set_audio(audio_clip)
                clips.append(video_clip)
            else:
                print(f" [VideoEditor] Missing audio file for {img_name}. Skipping...")

        if not clips:
            print("[VideoEditor] Could not assemble any clips. Aborting.")
            return False

        print("\n[VideoEditor] Rendering MP4 video (this may take a few minutes due to zoom processing)...")

        final_video = concatenate_videoclips(clips, method="compose")

        export_path = os.path.join(local_folder, output_filename)
        final_video.write_videofile(
            export_path,
            fps=30,
            codec="libx264",
            audio_codec="aac",
            logger= None
        )

        print(f" [VideoEditor] Video completed, saved in: {export_path}")
        return True
