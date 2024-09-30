import os 
from dotenv import load_dotenv
from groq import Groq 
import base64


load_dotenv()
key = os.getenv('grok_key')


image_path = 'car.jpg'
with open(image_path,'rb') as image_file:
    byte_image = image_file.read()
    encoded_image = base64.b64encode(byte_image).decode('utf-8')



client = Groq(api_key = key )

completion = client.chat.completions.create(
    model="llama-3.2-11b-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is in the image?",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"  # Use Data URL format
                    }
                }
            ]
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

# Print the response message
print(completion.choices[0].message)