import os
from dotenv import load_dotenv
from groq import Groq
import base64
import pyttsx3
import requests

load_dotenv()
key = os.getenv("GROQ_API_KEY")
eden = os.getenv("EDEN_API_KEY")

eden_ai_key = f"Bearer {eden}"

def analyze_image(image_path):
    with open(image_path, 'rb') as image_file:
        byte_image = image_file.read()
        encoded_image = base64.b64encode(byte_image).decode('utf-8')

    client = Groq(api_key=key)
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
                            "url": f"data:image/jpeg;base64,{encoded_image}"
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

    return completion.choices[0].message.content

def generate_image(prompt):
    url = "https://api.edenai.run/v2/image/generation"
    payload = {
        "providers": "openai",
        "text": prompt,
        "resolution": "512x512",
        "num_images": 1
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {eden}" 
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        image_url = result['openai']['items'][0]['image_resource_url']
        return image_url
    else:
        return f"Error: {response.status_code} - {response.text}"

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("\n1. Analyze Image")
        print("2. Generate Image")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            image_path = input("Enter the path to the image: ")
            result = analyze_image(image_path)
            print(result)
            speak_text(result)
        elif choice == '2':
            prompt = input("Enter the prompt for image generation: ")
            image_url = generate_image(prompt)
            print(f"Generated image URL: {image_url}")
            speak_text(f"Image generated successfully. You can view it at {image_url}")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
