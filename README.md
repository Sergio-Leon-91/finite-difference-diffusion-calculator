# Finite Fourier Transform Drawing Calculator

This repository provides a small Tkinter-based app that lets you draw a 2D pattern and visualize its discrete Fourier transform.

## Features
- Canvas for freehand drawing using the left mouse button.
- Computes a centered 2D FFT (using `numpy.fft.fft2` + `fftshift`).
- Shows both the drawing and the log-magnitude spectrum side by side in a Matplotlib window.
- Buttons to clear the canvas or quit the app.

## Getting started
1. Install Python 3.11+ along with the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the app:
   ```bash
   python fft_drawing_app.py
   ```
3. Draw on the canvas with the left mouse button. Click **Compute FFT** to view the spectrum. Use **Clear Canvas** to start over.

## Requirements
- Tkinter (commonly included with Python installations)
- matplotlib
- numpy
- pillow
