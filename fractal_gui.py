import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import math
from typing import List, Tuple

class FractalGenerator:
    def __init__(self):
        self.canvas = None
        self.figure = None
        
    def midpoint(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> Tuple[float, float]:
        """Calculate midpoint between two points."""
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    
    def draw_triangle(self, points: List[Tuple[float, float]], color: str, ax):
        """Draw a filled triangle."""
        triangle = plt.Polygon(points, color=color, alpha=0.8)
        ax.add_patch(triangle)
    
    def sierpinski_triangle(self, points: List[Tuple[float, float]], depth: int, ax, palette: List[str]):
        """Generate Sierpinski triangle fractal."""
        self.draw_triangle(points, palette[depth % len(palette)], ax)
        if depth > 0:
            p0, p1, p2 = points
            self.sierpinski_triangle([p0, self.midpoint(p0, p1), self.midpoint(p0, p2)], depth - 1, ax, palette)
            self.sierpinski_triangle([p1, self.midpoint(p1, p0), self.midpoint(p1, p2)], depth - 1, ax, palette)
            self.sierpinski_triangle([p2, self.midpoint(p2, p0), self.midpoint(p2, p1)], depth - 1, ax, palette)
    
    def koch_curve(self, start: Tuple[float, float], end: Tuple[float, float], depth: int, ax, color: str):
        """Generate Koch curve fractal."""
        if depth == 0:
            ax.plot([start[0], end[0]], [start[1], end[1]], color=color, linewidth=2)
        else:
            # Calculate the four points of the Koch curve
            p1 = start
            p2 = ((2*start[0] + end[0])/3, (2*start[1] + end[1])/3)
            
            # Calculate the peak point
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            angle = math.atan2(dy, dx)
            length = math.sqrt(dx*dx + dy*dy) / 3
            
            p3 = (start[0] + length * math.cos(angle - math.pi/3), 
                  start[1] + length * math.sin(angle - math.pi/3))
            
            p4 = ((start[0] + 2*end[0])/3, (start[1] + 2*end[1])/3)
            p5 = end
            
            # Recursively draw the four segments
            self.koch_curve(p1, p2, depth - 1, ax, color)
            self.koch_curve(p2, p3, depth - 1, ax, color)
            self.koch_curve(p3, p4, depth - 1, ax, color)
            self.koch_curve(p4, p5, depth - 1, ax, color)
    
    def koch_snowflake(self, center: Tuple[float, float], size: float, depth: int, ax, palette: List[str]):
        """Generate Koch snowflake fractal."""
        # Calculate triangle vertices
        height = size * math.sqrt(3) / 2
        p1 = (center[0], center[1] + height)
        p2 = (center[0] - size/2, center[1] - height/2)
        p3 = (center[0] + size/2, center[1] - height/2)
        
        color = palette[depth % len(palette)]
        self.koch_curve(p1, p2, depth, ax, color)
        self.koch_curve(p2, p3, depth, ax, color)
        self.koch_curve(p3, p1, depth, ax, color)
    
    def cantor_set(self, start: Tuple[float, float], length: float, depth: int, ax, color: str, y_pos: float):
        """Generate Cantor set fractal."""
        if depth == 0:
            ax.plot([start[0], start[0] + length], [y_pos, y_pos], color=color, linewidth=3)
        else:
            # Draw the middle third
            self.cantor_set(start, length/3, depth - 1, ax, color, y_pos)
            self.cantor_set((start[0] + 2*length/3, start[1]), length/3, depth - 1, ax, color, y_pos)
            
            # Draw the next level below
            self.cantor_set(start, length/3, depth - 1, ax, color, y_pos - 30)
            self.cantor_set((start[0] + 2*length/3, start[1]), length/3, depth - 1, ax, color, y_pos - 30)
    
    def mandelbrot_set(self, ax, max_iter: int):
        """Generate Mandelbrot set fractal."""
        # Define the region of interest
        x_min, x_max = -2.5, 1.5
        y_min, y_max = -2, 2
        
        # Create a grid of complex numbers
        width, height = 400, 400
        x = np.linspace(x_min, x_max, width)
        y = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        
        # Initialize the result array
        Z = np.zeros_like(C)
        iterations = np.zeros(C.shape, dtype=int)
        
        # Calculate the Mandelbrot set
        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            iterations += mask
        
        # Plot the result
        ax.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                 cmap='hot', origin='lower')
        ax.set_title('Mandelbrot Set')

class FractalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fractal Generator")
        self.root.geometry("1000x800")
        
        self.fractal_generator = FractalGenerator()
        self.current_fractal = "Sierpinski Triangle"
        self.depth = 3
        self.color_scheme = "Rainbow"
        
        self.setup_ui()
        self.update_fractal()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Fractal type selection
        ttk.Label(control_frame, text="Fractal Type:").pack(anchor=tk.W)
        self.fractal_var = tk.StringVar(value=self.current_fractal)
        fractal_combo = ttk.Combobox(control_frame, textvariable=self.fractal_var, 
                                   values=["Sierpinski Triangle", "Koch Snowflake", "Cantor Set", "Mandelbrot Set"],
                                   state="readonly")
        fractal_combo.pack(fill=tk.X, pady=(0, 10))
        fractal_combo.bind('<<ComboboxSelected>>', self.on_fractal_change)
        
        # Depth slider
        ttk.Label(control_frame, text=f"Depth: {self.depth}").pack(anchor=tk.W)
        self.depth_var = tk.IntVar(value=self.depth)
        depth_scale = ttk.Scale(control_frame, from_=0, to=8, variable=self.depth_var, 
                              orient=tk.HORIZONTAL, command=self.on_depth_change)
        depth_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Color scheme selection
        ttk.Label(control_frame, text="Color Scheme:").pack(anchor=tk.W)
        self.color_var = tk.StringVar(value=self.color_scheme)
        color_combo = ttk.Combobox(control_frame, textvariable=self.color_var,
                                 values=["Rainbow", "Blues", "Greens", "Reds", "Purples"],
                                 state="readonly")
        color_combo.pack(fill=tk.X, pady=(0, 10))
        color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        
        # Update button
        update_btn = ttk.Button(control_frame, text="Update Fractal", command=self.update_fractal)
        update_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Save button
        save_btn = ttk.Button(control_frame, text="Save Image", command=self.save_image)
        save_btn.pack(fill=tk.X)
        
        # Plot frame
        plot_frame = ttk.Frame(main_frame)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def get_color_palette(self):
        """Get color palette based on selected scheme."""
        schemes = {
            "Rainbow": ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#4b0082", "#9400d3"],
            "Blues": ["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c"],
            "Greens": ["#2ca02c", "#98df8a", "#d62728", "#ff9896", "#9467bd"],
            "Reds": ["#d62728", "#ff9896", "#9467bd", "#c5b0d5", "#8c564b"],
            "Purples": ["#9467bd", "#c5b0d5", "#8c564b", "#c49c94", "#e377c2"]
        }
        return schemes.get(self.color_scheme, schemes["Rainbow"])
    
    def on_fractal_change(self, event):
        self.current_fractal = self.fractal_var.get()
        self.update_fractal()
    
    def on_depth_change(self, value):
        self.depth = int(float(value))
        # Update the label
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ttk.Label) and grandchild.cget('text').startswith('Depth:'):
                                grandchild.config(text=f"Depth: {self.depth}")
                                break
    
    def on_color_change(self, event):
        self.color_scheme = self.color_var.get()
        self.update_fractal()
    
    def update_fractal(self):
        """Update the fractal display."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_aspect('equal')
        ax.axis('off')
        
        palette = self.get_color_palette()
        
        try:
            if self.current_fractal == "Sierpinski Triangle":
                # Equilateral triangle coordinates
                size = 200
                points = [(-size, -size), (0, size), (size, -size)]
                self.fractal_generator.sierpinski_triangle(points, self.depth, ax, palette)
                ax.set_xlim(-size*1.2, size*1.2)
                ax.set_ylim(-size*1.2, size*1.2)
                
            elif self.current_fractal == "Koch Snowflake":
                self.fractal_generator.koch_snowflake((0, 0), 300, self.depth, ax, palette)
                ax.set_xlim(-200, 200)
                ax.set_ylim(-200, 200)
                
            elif self.current_fractal == "Cantor Set":
                self.fractal_generator.cantor_set((-200, 0), 400, self.depth, ax, palette[0], 100)
                ax.set_xlim(-250, 250)
                ax.set_ylim(-200, 150)
                
            elif self.current_fractal == "Mandelbrot Set":
                # For Mandelbrot, use depth as max iterations
                max_iter = max(50, self.depth * 20)
                self.fractal_generator.mandelbrot_set(ax, max_iter)
            
            ax.set_title(f"{self.current_fractal} (Depth: {self.depth})")
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating fractal: {str(e)}")
    
    def save_image(self):
        """Save the current fractal as an image."""
        try:
            filename = f"{self.current_fractal.lower().replace(' ', '_')}_depth_{self.depth}.png"
            self.figure.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Success", f"Image saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving image: {str(e)}")

def main():
    root = tk.Tk()
    app = FractalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
