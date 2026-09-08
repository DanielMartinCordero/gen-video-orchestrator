from core.models.BaseModel import BaseModel

class TiktokFacebookModel(BaseModel):

    def generate_content(self, prompt, workflow_data):
        """
        Specific class to develop short content for TikTok or Facebook
        """
        print(f" [TiktokModel] Processing theme: {prompt}")

        #IDs from my ComfyUI schema
        ID_PROMPT = "2"
        ID_LATENT = "5"

        print(f" [TiktokModel] Sending order to flux...")

        return self.bridge.generate_image(
            workflow_data,
            prompt,
            ID_PROMPT,
            ID_LATENT
        )