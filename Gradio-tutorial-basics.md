# Gradio GUI Tutorial: Building Interactive Interfaces for Machine Learning and AI Models

## Introduction

Gradio is a Python library that allows you to quickly create customizable web interfaces for your machine learning models, functions, and APIs. This tutorial will guide you through the process of creating various Gradio interfaces, from simple to more complex examples.

## Prerequisites

Before we begin, make sure you have Python installed on your system. Then, install Gradio using pip:

```bash
pip install gradio
```

---

## Step 1: Creating a Basic Interface

Let's start with a simple example to help you understand the basics of Gradio.

```python
import gradio as gr

def greet(name):
    return "Hello, " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
```

This code creates a simple interface with a text input and output. When you run this script, it will open a local web server, typically at `http://localhost:7860`.

---


## Step 2: Understanding the Interface Components

The `gr.Interface` class is the core of Gradio. It takes three main arguments:

1. `fn`: The function to wrap with a UI
2. `inputs`: The input component(s)
3. `outputs`: The output component(s)

Gradio provides various components for inputs and outputs, such as text boxes, sliders, images, and more.

---


## Step 3: Adding Multiple Inputs

Let's create an interface with multiple inputs:

```python
import gradio as gr

def calculate_bmi(height, weight):
    bmi = weight / (height/100)**2
    return f"Your BMI is: {bmi:.2f}"

demo = gr.Interface(
    fn=calculate_bmi,
    inputs=[gr.Number(label="Height (cm)"), gr.Number(label="Weight (kg)")],
    outputs="text"
)
demo.launch()
```

This example demonstrates how to use multiple input components and label them.

---


## Step 4: Working with Images

Gradio can handle various data types, including images. Here's an example of an image classification interface:

```python

import gradio as gr
import base64
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4o-mini"
base_url = None

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

def describe_image(image, prompt):
    # Check if image is a string (file path) or a file object
    if isinstance(image, str):
        image_path = image
    else:
        image_path = image.name

    # Convert the image to base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Prepare the messages for the API call
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                },
            ],
        }
    ]

    # Call the OpenAI API
    response = client.chat.completions.create(
          model=model,
        messages=messages,
        max_tokens=300,
    )

    # Extract and return the response
    return response.choices[0].message.content

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown(f"# Image Analyzing App using {model}")
    
    with gr.Row():
        image_input = gr.Image(type="filepath", label="Upload an image")
        prompt_input = gr.Textbox(label="Enter your prompt", placeholder="Describe this image in detail")
    
    output = gr.Textbox(label="Image Description")
    
    submit_button = gr.Button("Analyze Image")
    submit_button.click(fn=describe_image, inputs=[image_input, prompt_input], outputs=output)

# Ensure the API key is loaded before launching the demo
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

demo.launch()
```
**Note:** alternative API: https://app.hyperbolic.xyz/models/qwen2-vl-7b-instruct

Let's explain the code step by step:

### 4.1. Import Required Libraries

```python
import gradio as gr
import base64
import os
from dotenv import load_dotenv
from openai import OpenAI
```

This section imports the necessary libraries:
- `gradio` for creating the user interface
- `base64` for encoding the image
- `os` and `dotenv` for handling environment variables
- `OpenAI` client for interacting with the OpenAI API

### 4.2. Set Up Environment and API Client

```python
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4o-mini"
base_url = None

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)
```

Here, we:
- Load environment variables from a .env file
- Get the OpenAI API key from the environment variables
- Set the model name and base URL (if needed)
- Initialize the OpenAI client

### 4.3. Define the Image Description Function

```python
def describe_image(image, prompt):
    # Function implementation...
```

This function takes an image and a prompt as input and returns a description. It:
- Checks if the image is a file path or file object
- Converts the image to base64 encoding
- Prepares the message for the OpenAI API
- Calls the API and returns the response

### 4.4. Create the Gradio Interface

```python
with gr.Blocks() as demo:
    gr.Markdown(f"# Image Analyzing App using {model}")
    
    with gr.Row():
        image_input = gr.Image(type="filepath", label="Upload an image")
        prompt_input = gr.Textbox(label="Enter your prompt", 
            placeholder="Describe this image in detail")
    
    output = gr.Textbox(label="Image Description")
    
    submit_button = gr.Button("Analyze Image")
    submit_button.click(fn=describe_image, inputs=[image_input, prompt_input], outputs=output)
```

This section creates the Gradio interface:
- Uses `gr.Blocks()` for a flexible layout
- Adds a title with the model name
- Creates a row with an image upload component and a text input for the prompt
- Adds an output text box for the description
- Creates a submit button that triggers the `describe_image` function

### 4.5. Launch the App

```python
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

demo.launch()
```

Finally, we:
- Check if the API key is present
- Launch the Gradio demo

### Key Points to Note:

1. **Image Handling**: Gradio's `Image` component is set to `type="filepath"`, which means it will provide the file path of the uploaded image to our function.

2. **API Integration**: The app uses OpenAI's API to analyze the image. Make sure you have the necessary API key and permissions.

3. **Base64 Encoding**: The image is converted to base64 encoding to be sent as part of the API request.

4. **Flexible Prompts**: Users can enter custom prompts, allowing for versatile image analysis queries.

5. **Error Handling**: The app checks for the presence of an API key before launching, preventing runtime errors.

This image analysis app demonstrates how to combine Gradio's user interface capabilities with external API services to create powerful and interactive applications. It showcases handling file uploads, text inputs, and integrating with AI services for image analysis.


---


## Step 5: Creating Interactive Demos

Gradio's `gr.Blocks` allows for more flexible layouts and interactivity:

```python
import gradio as gr

def greet(name):
    return f"Hello, {name}!"

with gr.Blocks() as demo:
    gr.Markdown("# Greeting App")
    name_input = gr.Textbox(label="Name")
    output = gr.Textbox(label="Greeting")
    greet_btn = gr.Button("Greet")
    greet_btn.click(fn=greet, inputs=name_input, outputs=output)

demo.launch()
```

This example creates a more structured layout with a markdown header and a button to trigger the greeting function.

---


## Step 6: Adding Examples

You can provide example inputs to help users understand how to use your interface:

```python
import gradio as gr

def echo(text):
    return text

demo = gr.Interface(
    fn=echo,
    inputs="text",
    outputs="text",
    examples=[["Hello, World!"], ["Gradio is awesome!"], ["Machine learning is fun!"]]
)
demo.launch()
```

This adds an "Examples" section below the interface with pre-filled inputs.

**Your task:** Change image app in step 4, by adding examples. **Note**, examples are list of lists. The inner lists are arguements to the function. Since function `echo` takes only 1 arguement so the inner lists are list of single string. For the image app, the function takes 2 arguements, so the inner lists have 2 arguements:

```python
examples = [
    ["path/to/image1.png",  "Who is the person in the image?"],
    ["path/to/image2.jpg", "What is mathjax code for expression in this image?"]
]

```

---



## Step 7: Customizing the Interface

In this step, we'll transform a basic Gradio app into a more feature-rich and interactive application. We'll start with a simple greeting app and enhance it with various Gradio components and features.

### Starting Point

Here's the basic app we'll be working with:

```python
import gradio as gr

def greet(name):
    return f"Hello, {name}!"

with gr.Blocks() as demo:
    gr.Markdown("# Greeting App")
    name_input = gr.Textbox(label="Name")
    output = gr.Textbox(label="Greeting")
    greet_btn = gr.Button("Greet")
    greet_btn.click(fn=greet, inputs=name_input, outputs=output)

demo.launch()
```

### Enhancing the App

Let's walk through the process of enhancing this app:

### 7.1. Expand the Greeting Function

First, let's make our greeting function more versatile:

```python
def greet(name, intensity, is_shouting, color):
    greeting = f"Hello, {name}!"
    greeting = greeting * intensity
    if is_shouting:
        greeting = greeting.upper() + "!"
    return f"<p style='color: {color}; font-size: 24px;'>{greeting}</p>"
```

### 7.2. Add More Input Components

Next, we'll add more input options for users:

```python
with gr.Tab("Basic Greeting"):
    gr.Markdown("## Enter your name and customize your greeting")
    with gr.Row():
        name_input = gr.Textbox(label="Name")
        intensity = gr.Slider(minimum=1, maximum=5, step=1, label="Greeting Intensity", value=1)
    is_shouting = gr.Checkbox(label="Shout the greeting?")
```

### 7.3. Implement Color Customization

Let's add a color picker for greeting customization:

```python
color_state = gr.State("#000000")

with gr.Tab("Greeting Customization"):
    gr.Markdown("## Customize the appearance of your greeting")
    color_picker = gr.ColorPicker(label="Choose greeting color", value="#000000")
    color_output = gr.Markdown("Current greeting color: #000000")
    
    color_picker.change(fn=change_greeting_color, inputs=color_picker, outputs=color_output)
    color_picker.change(lambda x: x, inputs=color_picker, outputs=color_state)
```

### Explanation of Color Picker Change Events

These two lines set up change events for the color picker:

```python
color_picker.change(fn=change_greeting_color, inputs=color_picker, outputs=color_output)
color_picker.change(lambda x: x, inputs=color_picker, outputs=color_state)
```

With color picker selecting new color, two update events are triggered. Let's break them down:

1. `color_picker.change(fn=change_greeting_color, inputs=color_picker, outputs=color_output)`
   - This line sets up an event that triggers when the color picker value changes.
   - It calls the `change_greeting_color` function, passing the new color as input.
   - The function's output is then used to update the `color_output` component, which displays the current color.

2. `color_picker.change(lambda x: x, inputs=color_picker, outputs=color_state)`
   - This line also triggers on color picker value changes.
   - It uses a lambda function `lambda x: x`, which simply returns its input unchanged.
   - The purpose is to update the `color_state` with the new color value.
   - `color_state` is a special Gradio component that maintains state across interactions.

By using these two change events, we ensure that:
- The displayed color information is always up to date.
- The current color is stored in the app's state, ready to be used when generating a new greeting.

This demonstrates how Gradio can handle multiple actions on a single event and how to use state management for persisting values across different parts of your app.

### 7.4. Organize with Tabs

We'll use tabs to organize different sections of our app:

```python
with gr.Blocks() as demo:
    gr.Markdown("# 🎉 Welcome to the Enhanced Greeting App!")
    
    with gr.Tab("Basic Greeting"):
        # Basic greeting components here
    
    with gr.Tab("Greeting Customization"):
        # Color customization components here
```

### 5. Add Instructions and About Section

Include helpful information for users:

```python
gr.Markdown("### How to use this app:")
gr.Markdown(
"""
1. Enter your name in the 'Name' field.
2. Adjust the 'Greeting Intensity' slider to repeat the greeting.
3. Check 'Shout the greeting?' if you want it in ALL CAPS.
4. Click the 'Greet' button to see your personalized greeting.
5. In the 'Greeting Customization' tab, you can choose a color for your greeting.
6. The color you choose will be applied to your greeting when you click 'Greet' again.
"""
)

with gr.Accordion("About this demo"):
    gr.Markdown(
    """
    This demo showcases several Gradio components and features:
    - Blocks layout with Tabs and Accordion
    - Various input types: Textbox, Slider, Checkbox, ColorPicker
    - Button interactions
    - Markdown and HTML for rich text formatting
    - Row layout for organizing components
    - State management for color persistence
    """
    )
```

### 7.6. Update Output to HTML

Change the output to HTML for styled text:

```python
output = gr.HTML(label="Greeting")
```

### 7.7. Connect Everything

Finally, connect all components:

```python
greet_btn.click(fn=greet, inputs=[name_input, intensity, is_shouting, color_state], outputs=output)
```

### 8. Run the Enhanced App

Your enhanced Gradio app is now ready to run! It features multiple inputs, color customization, tabbed interface, and informative sections.


---



## Step 8: Sharing Your Interface (on Huggingface space or gradio.app)

To share your Gradio interface publicly, you can use the `share` parameter:

```python
demo.launch(share=True)
```

This will generate a public URL that anyone can access to use your interface.

---


## Summary

This tutorial has covered the basics of creating Gradio interfaces, from simple text inputs to more complex layouts with images and customizations. Gradio provides an easy way to create interactive demos for your machine learning models or functions, making it simple to share and showcase your work.

Remember to explore the [Gradio documentation](https://www.gradio.app/docs/) for more advanced features and components to enhance your interfaces further[1].
