#TripoSR: Image-to-3D Model Pipeline
TripoSR is a Python-based pipeline that bridges 2D image generation and 3D model extraction. Using OpenAI's DALL·E API to generate images from text prompts and a custom TripoSR pipeline to convert those images into 3D meshes, this project provides an interactive way to transform creative ideas into tangible 3D models.

Features
Image Generation:
Generate images from textual prompts via OpenAI's DALL·E API.

3D Model Conversion:
Convert generated images into 3D meshes using the TripoSR pipeline (run through a subprocess).

Interactive Interface:
Leverage Gradio to quickly prototype and interact with the pipeline through a web interface.

Download Capabilities:
Easily download generated images and 3D models.

Getting Started
Prerequisites
Python 3.8+

Install required Python packages:
pip install -r requirements.txt
Ensure you have packages like openai, gradio, requests, Pillow, python-dotenv, among others.
Set up your environment by creating a .env file with your OpenAI API key:
OPENAI_API_KEY=your-api-key-here


Running the Application
Generate and Convert:
Run the main application:
python app.py


This will launch a local Gradio interface where you can:

Input a text prompt to generate an image.
Convert the image into a 3D mesh by invoking the TripoSR pipeline.
3D Model Pipeline:
The 3D conversion is handled by run.py, which:

Processes the input image.
Uses various modules within the tsr directory for background removal, mesh extraction (using marching cubes), and texture baking.
Repository Structure
app.py:
Main entry point with Gradio interface for image generation and 3D conversion.

run.py:
Handles the 3D model extraction and rendering pipeline.

tsr/
Contains the core modules for 3D processing:

system.py: Loads and configures the TripoSR model.
models/: Contains isosurface extraction using marching cubes.
bake_texture.py: Implements texture baking for the mesh.
utils.py: Utility functions for background removal, image resizing, and video saving.
.env:
Environment file to securely store the OpenAI API key.

License
This project is open-source and available under the MIT License.
