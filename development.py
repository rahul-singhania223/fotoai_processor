from models.BiRefNet.main import BiRefNetModel

agent = BiRefNetModel()

image_url = "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg"

def main():
    out = agent.process(image_url=image_url)
    print(out)


if __name__ == "__main__":
    main()