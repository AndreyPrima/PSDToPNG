# PSD to Image Converter

A simple and efficient tool to convert PSD files to various image formats such as PNG, JPEG, BMP, and TIFF. This application provides a graphical user interface (GUI) built with PyQt5 and supports batch processing of PSD files.

## Features
- Convert PSD files to PNG, JPEG, BMP, and TIFF formats.
- Batch conversion of multiple PSD files.
- Option to select output quality for JPEG format.
- Option to enable error logging.
- Light and dark theme options for the GUI.

## Screenshots
![Light Theme]((https://imgur.com/a/pwbNJDE))

![Dark Theme]((https://imgur.com/a/bxhGq6i))

## Requirements
- Python 3.6+
- PyQt5
- Pillow

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AndreyPrima/PSDToPNG.git
   cd psd-to-image-converter
2. Install the required dependencies:
   ```bash
    pip install -r requirements.txt

3. Run the application:
   ```bash
   python converter.py

## Usage
1. Launch the application using the command mentioned above.
2. Select the input directory containing PSD files.
3. Select the output directory where the converted images will be saved.
4. Choose the desired output format (PNG, JPEG, BMP, or TIFF).
5. (Optional) Adjust the quality for JPEG output.
6. Click "Convert" to start the conversion process.
