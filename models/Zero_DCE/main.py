import torch
from torchvision import transforms
from PIL import Image
import os
import numpy as np
import requests
from io import BytesIO

from models.Zero_DCE.model import DCENet
from lib.utils import upload_to_supabase

class DCENetModel:
    def __init__(self):
        # Load model

        model_path = "models/Zero_DCE/weights/model200_dark_faces.pth"
        self.device = "cuda"

        self.model = DCENet()
        self.model.load_state_dict(torch.load(model_path, map_location=self.device, weights_only=False))
        self.model.to(self.device).eval()


    def process(self, image_url, settings={'alpha': 1.0}):
        alpha = settings['alpha']
        # load image
        res = requests.get(image_url)
        image = Image.open(BytesIO(res.content))
        transform = transforms.Compose([
            transforms.ToTensor(),  # Converts to [0,1]
        ])
        img_tensor = transform(image).unsqueeze(0).to(self.device)  # [1, 3, H, W]

        # forward pass
        with torch.no_grad():
            _, enhanced_image, _ = self.model(img_tensor, alpha=alpha)

        # upload result
        img = enhanced_image.squeeze(0).cpu().detach().numpy().transpose(1, 2, 0)  # [H, W, C]
        img = np.clip(img * 255.0, 0, 255).astype(np.uint8)
        image_buffer = Image.fromarray(img)

        upload_res = upload_to_supabase(image_buffer, "light_fix_output.jpeg", format='jpeg')

        return upload_res



