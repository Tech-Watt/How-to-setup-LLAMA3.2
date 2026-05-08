# How to Setup Llama 3.2

This repository contains a simple Python command-line app that demonstrates how to use Llama 3.2 Vision through the Groq API. The app can analyze an image, generate an image through Eden AI, and read responses aloud with text-to-speech.

## Project Structure

| File | Description |
| --- | --- |
| `main.py` | Main CLI app for image analysis, image generation, and text-to-speech output. |
| `car.jpg` | Sample image that can be used for testing image analysis. |
| `requirements.txt` | Python dependency list. |

## Features

- Analyze local images with `llama-3.2-11b-vision-preview`
- Convert image files to base64 for vision model input
- Generate images from prompts through Eden AI
- Speak model responses using `pyttsx3`
- Simple terminal menu for choosing actions

## Requirements

- Python 3.8 or newer
- Groq API key
- Eden AI API key
- Internet connection

The current `requirements.txt` includes:

```text
python-dotenv
groq
```

The script also imports `requests` and `pyttsx3`, so install them as well:

```bash
pip install requests pyttsx3
```

## Getting Started

Clone the repository:

```bash
git clone https://github.com/Tech-Watt/How-to-setup-LLAMA3.2.git
cd How-to-setup-LLAMA3.2
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install requests pyttsx3
```

## API Key Setup

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
EDEN_API_KEY=your_eden_ai_api_key_here
```

The app loads both keys in `main.py`:

```python
key = os.getenv("GROQ_API_KEY")
eden = os.getenv("EDEN_API_KEY")
```

Keep your `.env` file private and do not commit API keys to GitHub.

## Running the App

Run:

```bash
python main.py
```

You will see a simple menu:

```text
1. Analyze Image
2. Generate Image
3. Exit
```

## Analyze an Image

Choose option `1`, then enter the path to an image file.

Example:

```text
car.jpg
```

The app reads the image, converts it to base64, and sends it to Groq using:

```python
model="llama-3.2-11b-vision-preview"
```

The response is printed in the terminal and read aloud using text-to-speech.

## Generate an Image

Choose option `2`, then enter an image prompt.

Example:

```text
A futuristic car driving through a neon city
```

The app sends the prompt to Eden AI's image generation endpoint and prints the generated image URL.

## How It Works

Image analysis flow:

1. Read a local image file.
2. Encode it as base64.
3. Send the image and a question to Llama 3.2 Vision through Groq.
4. Print the model response.
5. Read the response aloud.

Image generation flow:

1. Ask the user for a prompt.
2. Send the prompt to Eden AI.
3. Return the generated image URL.
4. Read a success message aloud.

## Customization

You can modify the project by:

- Changing the image analysis question
- Using a different Groq-supported model
- Changing the image generation provider in Eden AI
- Adjusting the generated image resolution
- Removing text-to-speech if you only want terminal output
- Building a Streamlit or Gradio interface around the same functions

## Notes

- `pyttsx3` may require system voice support depending on your operating system.
- The Eden AI image generation request currently uses the `openai` provider.
- API usage may require paid credits depending on your provider account.
- Add `requests` and `pyttsx3` to `requirements.txt` if you want a fully complete dependency file.

## Author

Created by [Tech Watt](https://github.com/Tech-Watt).
