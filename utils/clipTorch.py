import torch
import clip
import cv2
import numpy as np
from PIL import Image
from typing import List

# CLIP model (shared vector space for text and images):
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14@336px", device=device)


class Embed:

    @staticmethod
    def image(image) -> List[float]:
        '''Embeds a single image into a 768-float normalized vector. Accepts a file path or a cv2 numpy array.'''

        try:
            if isinstance(image, str):
                image = Image.open(image)
            elif isinstance(image, np.ndarray):
                image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            image = preprocess(image).unsqueeze(0).to(device)

            with torch.no_grad():
                emb = model.encode_image(image)
                emb = emb / emb.norm(dim=-1, keepdim=True)
                return emb.squeeze().cpu().tolist()

        except Exception as e:
            print(f'Exception: Embed.image()\n{e}')

    @staticmethod
    def text(text: str) -> List[float]:
        '''Embeds a text string into a 768-float normalized vector. Accepts full sentences.'''

        try:
            tokens = clip.tokenize([text], truncate=True).to(device)

            with torch.no_grad():
                emb = model.encode_text(tokens)
                emb = emb / emb.norm(dim=-1, keepdim=True)
                return emb.squeeze().cpu().tolist()

        except Exception as e:
            print(f'Exception: Embed.text()\n{e}')

    @staticmethod
    def video(frames: list) -> List[float]:
        '''Embeds multiple keyframes and averages them into a single 768-float normalized vector.'''

        try:
            embeddings = [Embed.image(frame) for frame in frames]
            avg = torch.tensor(embeddings).mean(dim=0)
            avg = avg / avg.norm()
            return avg.tolist()

        except Exception as e:
            print(f'Exception: Embed.video()\n{e}')
