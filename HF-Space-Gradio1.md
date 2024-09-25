# Tutorial for Deploying a Gradio App on Hugging Face Spaces

### Step 1: Sign Up for Hugging Face

1. Go to [huggingface.co](https://huggingface.co/) and sign up

### Step 2: Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click "Create new Space"
2. Choose a name, e.g. "phi3.5-demo", select "Gradio" as the SDK, and set visibility

### Step 3: Prepare Your App for Deployment

Create a file named `app_huggingface.py`:

```python

import gradio as gr
from huggingface_hub import InferenceClient

client = InferenceClient("microsoft/Phi-3.5-mini-instruct")

# Predefined prompts
prompts = [
    "Tell me a joke about programming",
    "Write a short story about a time-traveling robot",
    "Explain quantum computing to a 5-year-old",
    "Create a recipe for the most unusual pizza",
    "Describe an alien civilization's first contact with Earth"
]

def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    if not message:
        return []
    
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    prompt = "\n".join([m["content"] for m in messages])
    response = ""

    try:
        for chunk in client.text_generation(
            prompt,
            max_new_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        ):
            if isinstance(chunk, str):
                response += chunk
            else:
                response += chunk.token.text if hasattr(chunk, 'token') else chunk.generated_text
            yield [(message, response)]
    except Exception as e:
        yield [(message, f"An error occurred: {str(e)}")]

def update_textbox(prompt):
    return gr.update(value=prompt)

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Type your message or select a prompt")
    with gr.Row():
        prompt_dropdown = gr.Dropdown(choices=[""] + prompts, label="Select a premade prompt", value="")
        submit = gr.Button("Submit")
    clear = gr.ClearButton([msg, chatbot])

    with gr.Accordion("Advanced options", open=False):
        system = gr.Textbox(value="You are a friendly Chatbot.", label="System message")
        max_tokens = gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens")
        temperature = gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature")
        top_p = gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p (nucleus sampling)")

    prompt_dropdown.change(update_textbox, inputs=[prompt_dropdown], outputs=[msg])

    submit.click(respond, [msg, chatbot, system, max_tokens, temperature, top_p], chatbot)
    msg.submit(respond, [msg, chatbot, system, max_tokens, temperature, top_p], chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch()
```

**Code Explanation:**
- Loads the Phi-3.5 model and tokenizer from Hugging Face
- Defines a function to generate text using the loaded model
- Creates a Gradio interface similar to the local app 
- access files at https://huggingface.co/spaces/<your_user_name>/<your_space_name>/tree/main

Create a `requirements.txt` file:

```
huggingface_hub==0.22.2
```

### Step 4: Upload Files to Hugging Face Space

1. In your Space, upload `app_huggingface.py` (rename to `app.py`)
2. Upload `requirements.txt`

### Step 5: Deploy Your App

1. Wait for the automatic build process to complete
2. Your app will be live at the provided Hugging Face Spaces URL https://huggingface.co/spaces/<your_user_name>/<your_space_name>/

