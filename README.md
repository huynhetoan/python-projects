# Fractal Generator GUI

A beautiful GUI application for generating and exploring various mathematical fractals with interactive controls.

## Features

- **Multiple Fractal Types:**
  - Sierpinski Triangle
  - Koch Snowflake
  - Cantor Set
  - Mandelbrot Set

- **Interactive Controls:**
  - Depth slider (0-8 levels)
  - Multiple color schemes (Rainbow, Blues, Greens, Reds, Purples)
  - Real-time fractal updates

- **Additional Features:**
  - High-quality fractal visualization using matplotlib
  - Save fractals as high-resolution images
  - Responsive GUI built with tkinter

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python fractal_gui.py
```

## Usage

1. Select a fractal type from the dropdown menu
2. Adjust the depth using the slider (higher values create more detailed fractals)
3. Choose a color scheme
4. Click "Update Fractal" to generate the new fractal
5. Use "Save Image" to export your fractal as a PNG file

## Fractal Types

### Sierpinski Triangle
A classic fractal formed by recursively subdividing an equilateral triangle.

### Koch Snowflake
Based on the Koch curve, creating a snowflake-like pattern with infinite perimeter but finite area.

### Cantor Set
A fractal formed by repeatedly removing the middle third of line segments.

### Mandelbrot Set
One of the most famous fractals, showing the boundary between convergent and divergent complex numbers.

## Requirements

- Python 3.7+
- matplotlib
- numpy
- tkinter (usually included with Python)

## Notes

- Higher depth values will take longer to compute, especially for the Mandelbrot set
- The Mandelbrot set uses depth as a multiplier for maximum iterations
- All fractals are rendered with high quality and can be saved at 300 DPI