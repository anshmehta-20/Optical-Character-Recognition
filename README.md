# Optical Character Recognition (OCR) Project

This project is a Python-based OCR pipeline with a simple Tkinter GUI for selecting an image and extracting text using Tesseract. It also includes a standalone, script-style file with the same preprocessing steps for experimentation.

## What This Does
- Provides a basic GUI to select an image and run OCR.
- Applies a sequence of image preprocessing steps (invert, grayscale, binarize, noise removal, erosion/dilation, deskew, border handling).
- Runs Tesseract OCR and prints or displays extracted text.

## Project Layout
- `Final Project/OCR_Python.py`
  - Main GUI application.
  - Wraps the preprocessing pipeline and OCR in a Tkinter interface.
- `Final Project/Final code.py`
  - Script-style version for experimentation and step-by-step output.
- `Final Project/*.png`
  - Sample images used for testing.

## Requirements
Python 3.x plus these packages:
- `opencv-python`
- `pytesseract`
- `Pillow`
- `matplotlib` (used for optional image display in the pipeline)
- `tkinter` (usually bundled with standard Python on Windows)

You also need the **Tesseract OCR engine** installed.

## Tesseract Setup
The code tries to locate Tesseract in this order:
1. A `tesseract.exe` next to the script file.
2. The environment variable `TESSERACT_CMD`.
3. A `tesseract` binary available on your system `PATH`.

If none are found, it raises:
`FileNotFoundError: Tesseract not found. Install it and add to PATH or set TESSERACT_CMD.`

## How To Run (GUI)
From the project root:

```bash
python "Final Project/OCR_Python.py"
```

In the GUI:
1. Click **Select Image** and choose a `.png`, `.jpg`, or `.bmp`.
2. Click **Perform OCR** to extract text.
3. OCR output appears in the text box.

## How To Run (Script Mode)
You can also run the processing script directly:

```bash
python "Final Project/Final code.py"
```

This script expects specific image paths and writes intermediate results to disk.

## Notes About File Paths
The current code writes intermediate files to hardcoded paths such as:
- `D:\Coding\Python\CSE100 Project\...` in `Final Project/OCR_Python.py`
- `C:\Python Programming\Optical Character Recognition\Final Project\...` in `Final Project/Final code.py`

If those folders do not exist on your machine, you should update the paths in the scripts to point to a valid output directory.

## Pipeline Summary (OCR_Python.py)
The main OCR function:
1. Loads the image with OpenCV.
2. Creates several transformed versions: inverted, grayscale, thresholded.
3. Removes noise with morphological operations.
4. Applies erosion/dilation to adjust font thickness.
5. Detects skew and deskews.
6. Removes borders and adds padding back if needed.
7. Runs Tesseract to extract text.

## Troubleshooting
- If you see `FileNotFoundError` for Tesseract:
  - Install Tesseract and add it to PATH, or set `TESSERACT_CMD`.
- If OCR outputs are empty:
  - Try a higher-quality or higher-contrast image.
  - Verify the image file path is correct.
- If the app crashes on save paths:
  - Update the hardcoded output directories to valid paths on your machine.
