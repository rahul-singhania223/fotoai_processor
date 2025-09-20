import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BiRefNet.main import BiRefNetModel
from models.Real_ESRGAN.main import RealESRGANModel
from models.Zero_DCE.main import DCENetModel


processor_dict = {
    "REMOVE_BG": BiRefNetModel(),
    "UPSCALE_2X": RealESRGANModel(scale=2),
    "UPSCALE_4X": RealESRGANModel(scale=4),
    "LIGHT_FIX": DCENetModel()
}

process_with_settings = ['LIGHT_FIX']

def process_image(input):
    
    job_input = input['input']
    image_url = job_input['image_url']
    process_type = job_input['process_type']  

    agent = processor_dict[process_type]
    settings = {}

    # process with settings
    if process_type in process_with_settings:
        settings = job_input['settings']  

    output = agent.process(image_url=image_url, settings=settings)
    return output




