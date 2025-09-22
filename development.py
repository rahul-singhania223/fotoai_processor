from models.RealESRGAN.main import RealESRGANModel

agent = RealESRGANModel(scale=2)

def proc(input):
    return agent.process(input)


if __name__ == '__main__':
    proc('https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg')