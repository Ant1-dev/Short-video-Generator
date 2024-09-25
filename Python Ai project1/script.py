from openai import OpenAI
import os
from dotenv import load_dotenv
import narration
import make_image
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

with open("source_material.txt") as f:
    source_material = f.read()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system",
         "content": """You create narration for short entertaining short videos like on tik tok
         in the format of:
         
         **Background image:** 5 word description of an environment
         
         \n 
         
         **Narrator:** text text text 
         
         \n
         
         **Background image:** 5 word description of an evironment
         and repeat a couple times
         STick to this formate"""



         },
        {
            "role": "user",
            "content": f"Create a narration based on the following source material:\n\n {source_material}"
        }
    ]
)
print(completion.choices[0].message.content)
data = narration.parse(completion.choices[0].message.content)
print("\n\n\n")
print(data)
#narration.create(data, "narration.mp3")
if not os.path.exists("images"):
    os.makedirs("images")
    
make_image.make_from_data(data)