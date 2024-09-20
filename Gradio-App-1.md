# Building an AI Text Generation App

## Part 1: Creating a Local App with OpenAI API

### Step 1: Set Up Your Environment


1. Open a terminal or command prompt
2. Create and navigate to your project directory:
   ```bash
   mkdir ai_text_app
   cd ai_text_app
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv gradio
   source gradio/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
   Or using conda/mamba to create env
   ```bash
   conda create -n gradio python=3.11
   conda activate gradio
   ```
4. Install required packages:
   ```bash
   pip install gradio openai python-dotenv
   ```

### Step 2: Set Up OpenAI API Key

1. Sign up for an OpenAI account at [openai.com](https://openai.com/)
2. Create a new API key in the API section
3. Create a `.env` file in your project directory and add your API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

### Step 3: Create the Local App

Create a file named `app_local.py` with the following code:

```python

import gradio as gr
import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set up  API key
api_key = os.getenv("OPENAI_API_KEY")
base_url="https://api.deepinfra.com/v1/openai" # deepinfra
# base_url = None # default to openAI
# base_url='http://localhost:11434/v1/' # 

# model="gpt-3.5-turbo"
model="gpt-3.5-turbo"

# Qwen2.5
model="Qwen/Qwen2.5-72B-Instruct"


# create client
from dotenv import load_dotenv
import os


client = OpenAI(
    base_url=base_url,
    api_key=api_key  # Required but ignored by Ollama
)

def generate_text(prompt, max_tokens=4000):

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create Gradio interface
iface = gr.Interface(
    fn=generate_text,
    inputs=[
        gr.Textbox(lines=3, placeholder="Enter your prompt here..."),
        gr.Slider(minimum=10, maximum=4000, value=500, step=8, label="Max Tokens")
    ],
    outputs="text",
    title="AI Text Generation with {model}",
    description="Generate text using {model}."
)

# Launch the app
if __name__ == "__main__":
    iface.launch()

```

**Code Explanation:**
- Loads the API key from the `.env` file using `python-dotenv`
- Defines a function to generate text using OpenAI/DeepInfra/Ollama's API
- Creates a Gradio interface with input for prompt and max tokens
- Launches the Gradio app when the script is run

### Step 4: Run the Local App

1. Ensure your virtual environment is activated
2. Run the app:
   ```bash
   python app_local.py
   ```
3. Open the provided URL in your web browser
