from models.RealESRGAN.main import RealESRGANModel
from models.BiRefNet.main import BiRefNetModel
from models.Zero_DCE.main import DCENetModel
from models.Platform.main import PlatformModel

import runpod

def remove_bg(image_url, settings=None):
    model = BiRefNetModel()
    return model.process(image_url=image_url)

def upscale_2x(image_url, settings=None):
    model = RealESRGANModel(scale=2)
    return model.process(image_url=image_url)

def upscale_4x(image_url, settings=None):
    model = RealESRGANModel(scale=4)
    return model.process(image_url=image_url)

def light_fix(image_url, settings=None):
    model = DCENetModel()
    return model.process(image_url=image_url, settings=settings)

def platform(image_url, settings=None):
    model = PlatformModel()
    return model.process(image_url=image_url, settings=settings)


agent_dict = {
    "REMOVE_BG": remove_bg,
    "UPSCALE_2X": upscale_2x,
    "UPSCALE_4X": upscale_4x,
    "LIGHT_FIX": light_fix,
    "PLATFORM": platform
}

process_with_settings = ['LIGHT_FIX', 'PLATFORM']

def process_image(event):    
    job_input = event.get('input', {})
    image_url = job_input.get('image_url')
    process_type = job_input.get('process_type')

    if not image_url or not process_type:
        raise ValueError("Missing image_url or process_type in input")
    
    if process_type not in agent_dict:
        raise ValueError(f"Unknown process_type: {process_type}")

    agent = agent_dict[process_type]
    settings = None

    # process with settings
    if process_type in process_with_settings:
        settings = job_input.get('settings', {}) 

    output = agent(image_url, settings=settings)
    return output


def main():
    runpod.serverless.start({ "handler": process_image })

    
if __name__ == "__main__":
    main()
