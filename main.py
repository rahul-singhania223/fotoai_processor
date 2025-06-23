from models.BiRefNet.main import BiRefNetModel
import runpod

processor_dict = {
    "REMOVE_BG": BiRefNetModel()
}

def process_image(input):
    job_input = input['input']
    image_url = job_input['image_url']
    process_type = job_input['process_type']
    agent = processor_dict[process_type]
    output = agent.process(image_url=image_url)
    return output


def main():
    runpod.serverless.start({ "handler": process_image })

    
if __name__ == "__main__":
    main()


