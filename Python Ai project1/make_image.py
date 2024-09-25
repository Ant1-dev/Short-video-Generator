from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

def make_from_data(data):
    image_order = 0
    for element in data:
        if element["type"] != "image":
            continue
        image_order += 1
        image_file_name = f"image_{image_order}.webp"
        makeImage(element["description"], os.path.join("images", image_file_name))

def makeImage(description, outfile):
    response = client.images.generate(
    model="dall-e-3",
    prompt=description,
    size="1024x1024",
    quality="standard",
    response_format="b64_json",
    n=1
)
    images_b64 = response.data[0].b64_json
    
    with open (outfile, "wb") as f:
        f.write(base64.b64decode(images_b64))



