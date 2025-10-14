# Fractal Generator GUI

A beautiful GUI application for generating and exploring various mathematical fractals with interactive controls.

## Technical Highlights

- Recursive fractal generation with depth-aware styling
- Gradient color interpolation using HSV blending
- Modular design with reusable geometry functions
- Matplotlib integration with high-DPI export
- Tkinter GUI with real-time updates and theme support

## Features

- **Multiple Fractal Types:**
  - Sierpinski Triangle
  - Koch Snowflake
  - Cantor Set
  - Mandelbrot Set

- **Interactive Controls:**
  - Depth slider (0–7 levels)
  - Multiple color schemes:
    - `Vibrant`: reds, yellows, greens, blues, purples
    - `Ocean`: teals, blues, deep sea tones
    - `Sunset`: warm pinks, oranges, and twilight blues
    - `Forest`: cool greens and woodland hues
    - `Fire`: intense reds, oranges, and purples
    - `Pastel`: soft, playful tones
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

### Example: Koch Snowflake at Depth 5
![Koch Snowflake Depth 5](koch_snowflake_depth5.png)

## Fractal Types

### Sierpinski Triangle
A classic fractal formed by recursively subdividing an equilateral triangle.

### Koch Snowflake
Based on the Koch curve, creating a snowflake-like pattern with infinite perimeter but finite area.


### Cantor Set
Visualizes the recursive removal of middle thirds. Each level is spaced vertically to reveal the fractal ladder structure. Points correspond to ternary numbers with no digit 1.

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