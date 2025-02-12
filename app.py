import gradio as gr
import openai
import requests
import os
import io
from PIL import Image
import subprocess
import uuid
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  # Loads variables from .env into the environment

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(prompt):
    """
    Generate an image using the OpenAI DALL·E API based on the provided prompt.
    The image is downloaded and saved as 'temp_image.png'.
    Returns the local file path.
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"  # Options: "256x256", "512x512", "1024x1024"
        )
        # Retrieve image URL from response
        image_url = response["data"][0]["url"]
        print("DALL·E API response URL:", image_url)
        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        image = Image.open(io.BytesIO(image_response.content))
        image_path = "temp_image.png"
        image.save(image_path)
        return image_path
    except Exception as e:
        print(f"Error generating image with DALL·E API: {e}")
        return f"Error: {e}"

def image_to_3d(image_path):
    """
    Convert the given image to a 3D model using the TripoSR pipeline.
    This function calls run.py as a subprocess.
    Returns the path to the generated 3D mesh file.
    """
    try:
        command = [
            "python",
            "run.py",
            image_path,             # Input image path
            "--output-dir", "output"  # Output directory for the 3D model
        ]
        # Assumes app.py and run.py are in the same folder
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=".")
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"TripoSR failed: {stderr.decode()}")
            return "Error: TripoSR failed. Check the console for details."
        print(stdout.decode())
        # For a single image, run.py saves the mesh as "mesh.obj" in folder "output/0/"
        return os.path.join("output", "0", "mesh.obj")
    except FileNotFoundError:
        return "Error: TripoSR script not found. Check the file path."
    except subprocess.CalledProcessError as e:
        print(f"TripoSR failed: {e.stderr.decode()}")
        return f"Error: TripoSR failed: {e.stderr.decode()}"

def download_image(image_path):
    """Return the provided image path for download."""
    return image_path

def update_download_button(state):
    """
    Update the download button's visibility.
    If state (the generated image path) is not None, show the button.
    """
    if state:
        return gr.update(visible=True)
    else:
        return gr.update(visible=False)

def generate_image_wrapper(prompt):
    """
    Wrapper for generate_image that returns the generated image path
    as both the image output and the state.
    """
    image_path = generate_image(prompt)
    if image_path and "Error" not in image_path:
        return image_path, image_path
    else:
        return image_path, None

def image_to_3d_wrapper(image_path):
    """
    Wrapper for image_to_3d that converts the image to 3D.
    """
    if image_path:
        return image_to_3d(image_path)
    else:
        return "Error: No image to convert."

def build_ui():
    with gr.Blocks() as demo:
        text_prompt = gr.Textbox(label="Enter Text Prompt")
        generate_button = gr.Button("Generate Image")
        image_output = gr.Image(label="Generated Image")
        convert_button = gr.Button("Convert to 3D Model")
        model_output = gr.Model3D(label="3D Model")
        download_button = gr.Button("Download Image", visible=False)
        state = gr.State(None)  # To store the generated image path

        # When the generate button is clicked, generate an image and update state
        generate_button.click(
            generate_image_wrapper,
            inputs=text_prompt,
            outputs=[image_output, state]
        )
        # When the state changes, update the download button's visibility
        state.change(
            update_download_button,
            inputs=state,
            outputs=download_button
        )
        # When the convert button is clicked, run the 3D conversion
        convert_button.click(
            image_to_3d_wrapper,
            inputs=state,
            outputs=model_output
        )
        # When the download button is clicked, trigger download
        download_button.click(
            download_image,
            inputs=state,
            outputs=None
        )
    return demo

if __name__ == "__main__":
    demo = build_ui()
    demo.launch(share=False)
