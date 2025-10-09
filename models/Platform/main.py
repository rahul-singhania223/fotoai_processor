from models.RealESRGAN.main import RealESRGANModel
from models.BiRefNet.main import BiRefNetModel
from models.Zero_DCE.main import DCENetModel

from lib.utils import upload_to_supabase

from PIL import Image
import requests
from io import BytesIO

class PlatformModel:
    def __init__(self):
        self.birefnet_model = BiRefNetModel()
        self.realesrgan_model = RealESRGANModel(4)
        self.dce_model = DCENetModel()

    def process(self, image_url, settings={ 'dimension': 1024, 'format': 'png'}):     
        res = requests.get(image_url)
        image = Image.open(BytesIO(res.content))

        # extract object
        obj_img = self.birefnet_model.extract_object_from_image(image)

        # upspscale <= dimension
        obj_upscaled = self.realesrgan_model.process_from_image(obj_img)

        # light fix
        obj_light_fixed = self.dce_model.process_from_image(obj_upscaled, alpha=0.5)

        # fix dimension
        obj_fixed = obj_light_fixed.resize((settings['dimension'], settings['dimension']))

        # upload
        buffer = BytesIO()
        obj_fixed.save(buffer, format=format.upper())
        obj_buffer = buffer.getvalue()

        upload_res = upload_to_supabase(obj_buffer, format)

        return upload_res
        

        

