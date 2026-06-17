import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import base64
import pyttsx3
import requests
from PIL import Image
import io
import json

# Load environment variables
load_dotenv()

# Initialize session state for API keys and saved responses
if 'eden_ai_key' not in st.session_state:
    st.session_state.eden_ai_key = os.getenv("EDEN_AI_KEY", "")
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")
if 'saved_responses' not in st.session_state:
    # Load saved responses from file if it exists
    try:
        with open('saved_responses.json', 'r') as f:
            st.session_state.saved_responses = json.load(f)
    except FileNotFoundError:
        st.session_state.saved_responses = []

st.set_page_config(layout="wide", page_title="AI Assistant")

# Sidebar for API key input
st.sidebar.title("API Keys")
eden_ai_key = st.sidebar.text_input("Enter EDEN AI API Key", value=st.session_state.eden_ai_key, type="password")
groq_api_key = st.sidebar.text_input("Enter GROQ API Key", value=st.session_state.groq_api_key, type="password")

# Update session state with new API keys
st.session_state.eden_ai_key = eden_ai_key
st.session_state.groq_api_key = groq_api_key

def analyze_image(image_file):
    try:
        byte_image = image_file.getvalue()
        encoded_image = base64.b64encode(byte_image).decode('utf-8')

        client = Groq(api_key=st.session_state.groq_api_key)
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
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def generate_image(prompt):
    try:
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
            "authorization": f"Bearer {st.session_state.eden_ai_key}"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            image_url = result['openai']['items'][0]['image_resource_url']
            return image_url
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error generating image: {str(e)}"

def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.warning(f"Error speaking text: {str(e)}")

def save_responses():
    with open('saved_responses.json', 'w') as f:
        json.dump(st.session_state.saved_responses, f)

st.title("AI Assistant")

choice = st.radio("Choose an option:", ("Analyse Image", "Generate Image"))

if choice == "Analyze Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", width=400)
        with col2:
            if st.button("Analyze Image"):
                if not st.session_state.groq_api_key:
                    st.error("Please enter your GROQ API Key in the sidebar.")
                else:
                    with st.spinner("Analyzing image and generating voice response..."):
                        result = analyze_image(uploaded_file)
                        st.write("Analysis Result:")
                        st.write(result)
                        speak_text(result)
                    
                    if st.button("Save Response"):
                        st.session_state.saved_responses.append({
                            "type": "analysis",
                            "image": uploaded_file.name,
                            "result": result
                        })
                        save_responses()
                        st.success("Response saved!")

elif choice == "Generate Image":
    prompt = st.text_input("Enter the prompt for image generation:")
    if st.button("Generate Image"):
        if not st.session_state.eden_ai_key:
            st.error("Please enter your EDEN AI API Key in the sidebar.")
        else:
            with st.spinner("Generating image and voice response..."):
                image_url = generate_image(prompt)
                if image_url.startswith("http"):
                    st.image(image_url, caption="Generated Image", width=400)
                    speak_text("Image generated successfully.")
                    
                    if st.button("Save Response"):
                        st.session_state.saved_responses.append({
                            "type": "generation",
                            "prompt": prompt,
                            "image_url": image_url
                        })
                        save_responses()
                        st.success("Response saved!")
                else:
                    st.error(image_url)

# Display saved responses
st.sidebar.title("Saved Responses")
for i, response in enumerate(st.session_state.saved_responses):
    with st.sidebar.expander(f"Response {i+1}"):
        if response["type"] == "analysis":
            st.write(f"Image: {response['image']}")
            st.write(f"Analysis: {response['result']}")
        else:
            st.write(f"Prompt: {response['prompt']}")
            st.image(response['image_url'], width=200)

# Theme toggle
if st.sidebar.button("Toggle Theme"):
    if st.session_state.get("theme", "light") == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

# Apply theme
if st.session_state.get("theme", "dark") == "dark":
    st.markdown("""
    <style>
    body { color: white; background-color: #1E1E1E; }
    .stApp { background-color: #1E1E1E; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body { color: black; background-color: white; }
    .stApp { background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# Custom CSS for card layout
st.markdown("""
<style>
.stImage > img {
    max-width: 400px;
    max-height: 400px;
    object-fit: contain;
}
</style>
""", unsafe_allow_html=True)
