# TripoSR: Image-to-3D Model Pipeline

TripoSR is a Python-based pipeline that seamlessly connects 2D image generation with 3D model extraction. By leveraging OpenAI's DALL·E API for image generation and a custom TripoSR pipeline for 3D mesh conversion, this project offers an interactive way to bring creative ideas to life as 3D models.

## Features

- **Image Generation:** Generate high-quality images from text prompts using OpenAI's DALL·E API.
- **3D Model Conversion:** Transform generated images into 3D meshes via the TripoSR pipeline.
- **Interactive Interface:** Utilize Gradio for a user-friendly web interface to interact with the pipeline.
- **Download Support:** Easily download generated images and 3D models.

## Getting Started

### Prerequisites

- Python 3.8+
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
- Ensure required packages are installed, including `openai`, `gradio`, `requests`, `Pillow`, and `python-dotenv`.
- Set up your environment by creating a `.env` file and adding your OpenAI API key:
  ```sh
  OPENAI_API_KEY=your-api-key-here
  ```

### Running the Application

#### Generate and Convert

Start the application with:
```sh
python app.py
```
This launches a local Gradio interface where you can:
- Enter a text prompt to generate an image.
- Convert the generated image into a 3D mesh using the TripoSR pipeline.

#### 3D Model Pipeline

The 3D conversion is handled by `run.py`, which:
- Processes the input image.
- Uses modules within the `tsr` directory for background removal, mesh extraction (via marching cubes), and texture baking.

## Repository Structure

```
├── app.py          # Main entry point with Gradio interface
├── run.py          # Handles 3D model extraction and rendering
├── tsr/            # Core modules for 3D processing
│   ├── system.py   # Loads and configures the TripoSR model
│   ├── models/     # Contains isosurface extraction logic
│   ├── bake_texture.py  # Implements texture baking
│   ├── utils.py    # Utility functions for image processing
├── .env            # Environment file storing API keys
├── requirements.txt # List of required Python packages
```

## License

This project is open-source and available under the **MIT License**.

---
Feel free to contribute and enhance TripoSR!

