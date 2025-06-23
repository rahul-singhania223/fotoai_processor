import torch
import requests
from io import BytesIO
from PIL import Image
from torchvision import transforms

from models.BiRefNet.models.birefnet import BiRefNet
from lib.utils import upload_to_supabase

birefnet = BiRefNet.from_pretrained('ZhengPeng7/BiRefNet')


class BiRefNetModel:
    def __init__(self):
        self.birefnet = BiRefNet.from_pretrained('ZhengPeng7/BiRefNet')
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
            return {"status": "FAILED", "error_code": "INVALID_PARAMETERS"}

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
            preds = birefnet(input_images)[-1].sigmoid().cpu()
        pred = preds[0].squeeze()
        pred_pil = transforms.ToPILImage()(pred)
        mask = pred_pil.resize(image.size)
        image.putalpha(mask)

        return {"status": "SUCCESS", "result_image": image}
    
    def process(self, image_url):
        extract_response = self.extract_object(image_url)
        if extract_response["status"] == "FAILED":
            return extract_response
        
        image = extract_response['result_image']

        # upload to storage
        with BytesIO() as buffer:
            image.save(buffer, format="PNG")
            image_buffer = buffer.getvalue()

        upload_res = upload_to_supabase(image_buffer)

        print("PROCESS_COMPLETED")

        return upload_res
