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

        model_path = "models/Zero_DCE/weights/Epoch99.pth"
        self.device = "cuda"

        self.model = DCENet().cuda()
        self.model.load_state_dict(torch.load(model_path))


    def process(self, image_url, settings={'alpha': 1.0}):
        os.environ['CUDA_VISIBLE_DEVICES']='0'
        alpha = settings['alpha']
        # load image
        res = requests.get(image_url)
        image = Image.open(BytesIO(res.content)).convert('RGB')
        image = (np.asarray(image)/255.0)
        image = torch.from_numpy(image).float()
        image = image.permute(2,0,1)
        image = image.cuda().unsqueeze(0)
       
        # forward pass
        with torch.no_grad():
            _, enhanced_image, _ = self.model(image, alpha=alpha)

        # upload result
        img = enhanced_image.squeeze(0).cpu().detach().numpy().transpose(1, 2, 0)  # [H, W, C]
        img = np.clip(img * 255.0, 0, 255).astype(np.uint8)
        image_buffer = Image.fromarray(img)

        upload_res = upload_to_supabase(image_buffer, "light_fix_output.jpeg", format='jpeg')

        return upload_res



