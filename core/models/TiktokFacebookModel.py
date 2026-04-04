from core.models.BaseModel import BaseModel

class TiktokFacebookModel(BaseModel):

    def generate_content(self, topic, workflow_data):
        """
        Specific class to develop short content for TikTok or Facebook
        """
        print(f"🎬 [TiktokModel] Procesando tema: {topic}")

        #IDs from my ComfyUI schema
        ID_PROMPT = "2"
        ID_LATENT = "5"
        workflow_path = "workflows/workflow_flux_api.json"

        #Building of main prompt
        full_prompt = (
            f"A cinematic, high-quality 9:16 vertical shot of {topic}, "
            f"medieval dark fantasy style, moody lighting, highly detailed, 8k."
        )


        print(f"🚀 [TiktokModel] Enviando orden a Flux vía Bridge...")

        return self.bridge.generate_image(
            workflow_data,
            full_prompt,
            ID_PROMPT,
            ID_LATENT
        )