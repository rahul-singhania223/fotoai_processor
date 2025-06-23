from models.BiRefNet.main import BiRefNetModel


if __name__ == "__main__":
    processor = BiRefNetModel()

    processor.process("image_url")