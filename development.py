from models.BiRefNet.main import BiRefNet


birefnet = BiRefNet()

if __name__ == "__main__":
    birefnet.process("image_url")