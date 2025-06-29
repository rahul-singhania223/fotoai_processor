import torch
import requests
import base64
from io import BytesIO
from PIL import Image
from torchvision import transforms

from models.BiRefNet.models.birefnet import BiRefNet
from lib.utils import upload_to_supabase


class BiRefNetModel:
    def __init__(self):
        self.birefnet = BiRefNet.from_pretrained('ZhengPeng7/BiRefNet')
        torch.set_float32_matmul_precision(['high', 'highest'][0])
        self.birefnet.to('cuda')
        self.birefnet.eval()
        self.birefnet.half()

    def extract_object(self, image_url):        
        res = requests.get(image_url)

        # Data settings
        image_size = (1024, 1024)
        transform_image = transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        image = Image.open(BytesIO(res.content))
        input_images = transform_image(image).unsqueeze(0).to('cuda').half()

        # Prediction
        with torch.no_grad():
            preds = self.birefnet(input_images)[-1].sigmoid().cpu()
        pred = preds[0].squeeze()
        pred_pil = transforms.ToPILImage()(pred)
        mask = pred_pil.resize(image.size)

        image.putalpha(mask)

        return image
    
    def process(self, image_url, settings={}):
        image = self.extract_object(image_url)

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        image_buffer = buffer.getvalue()    

        upload_res = upload_to_supabase(image_buffer)
       
        return upload_res
