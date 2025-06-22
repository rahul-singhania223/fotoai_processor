from transformers import AutoModelForImageSegmentation
from torchvision import transforms
from PIL import Image
import torch
from lib.utils import upload_to_supabase

import requests
from io import BytesIO


class BiRefNet:
    def __init__(self):
        self.birefnet = AutoModelForImageSegmentation.from_pretrained('ZhengPeng7/BiRefNet', trust_remote_code=True)
        torch.set_float32_matmul_precision(['high', 'highest'][0])
        self.birefnet.to('cuda')
        self.birefnet.eval()
        self.birefnet.half()

    def extract_object(self, image_url):
        # download image
        try:
            res = requests.get(image_url)
            image = Image.open(BytesIO(res.content))
            image.verify()
        except Exception as downloadErr:
            print(f"Something is wrong with the URL: {str(downloadErr)}")
            return { "status": "FAILED", "message": "Invalid URL"}
        
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

        return {"status": "SUCCESS", "image": image}
    
    
    def process(self, image_url):
        extract_response = self.extract_object(image_url)

        if extract_response['status'] == 'FAILED':
            return extract_response
        
        image = extract_response['image']

        # upload
        with BytesIO() as buffer:
            image.save(buffer, format='PNG')
            result_image = buffer.getvalue()

        upload_res = upload_to_supabase(result_image)

        if upload_res['status'] == 'FAILED':
            return upload_res
        
        result_url = upload_to_supabase['result_url']

        return {"status": "SUCCESS", "result_url": result_url}
        




