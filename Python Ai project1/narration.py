from elevenlabs.client import ElevenLabs 
from elevenlabs import save, Voice
import os
elevenlabs_client = ElevenLabs( api_key=os.getenv("ELEVEN_API_KEY"))

#Function to parse/ split up text obtained from openai's text
def parse(narration):
    output = [] #creating an empty list to put completed parsed narrated text
    lines = narration.split("\n") #seperating the the narration into a list 
    
    # Initialize variables
    current_background = None
    
    for line in lines:
        line = line.strip()  # Clean up leading and trailing whitespace

        if line.startswith('**Narrator:**'):
            # Extract text following '**Narrator:**'
            text = line.replace('**Narrator:**', '').strip()
            if current_background:
                output.append({
                    "type": "image",
                    "description": current_background,
                })
                current_background = None
            output.append({
                "type": "text",
                "content": text,
            })
        elif line.startswith('**Background image:**'):
            # Extract text following 'background image: '
            current_background = line.replace('**background image:**', '').strip()

    # Append the last background image if any
    if current_background:
        output.append({
            "type": "image",
            "description": current_background,
        })

    return output

def create(data, output_file):
    narration = "" #Inialize narriation
    for  element in data:
        if element["type"] != "text": #If current iteration is not text continue to next iteration
            continue
        narration += element["content"] + "\n\n" # Else add that element value to the narration string
    
    audio = elevenlabs_client.generate(
        text=narration,
        voice= Voice(
            voice_id='onwK4e9ZLuTAKqWW03F9'
        ),
        model= "eleven_monolingual_v1"
    )
    save(audio, output_file)
    