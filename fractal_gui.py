import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import math
from typing import List, Tuple
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon
import colorsys

class FractalGenerator:
    def __init__(self):
        self.canvas = None
        self.figure = None
        
    def midpoint(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> Tuple[float, float]:
        """Calculate midpoint between two points."""
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    
    def draw_triangle(self, points: List[Tuple[float, float]], color: str, ax, depth: int, max_depth: int):
        """Draw a filled triangle with gradient shading."""
        # Create gradient effect based on depth
        alpha = 0.9 - (depth / max_depth) * 0.3
        
        # Fix polygon color warning by using facecolor instead of color
        triangle = Polygon(points, facecolor=color, alpha=alpha, edgecolor='black', linewidth=0.5)
        ax.add_patch(triangle)
    
    def sierpinski_triangle(self, points: List[Tuple[float, float]], depth: int, ax, palette: List[str], max_depth: int = 7):
        """Generate Sierpinski triangle fractal with gradient colors."""
        # Create gradient color based on depth
        color = self.create_gradient_color(palette, depth, max_depth)
        self.draw_triangle(points, color, ax, depth, max_depth)
        
        if depth > 0:
            p0, p1, p2 = points
            self.sierpinski_triangle([p0, self.midpoint(p0, p1), self.midpoint(p0, p2)], depth - 1, ax, palette, max_depth)
            self.sierpinski_triangle([p1, self.midpoint(p1, p0), self.midpoint(p1, p2)], depth - 1, ax, palette, max_depth)
            self.sierpinski_triangle([p2, self.midpoint(p2, p0), self.midpoint(p2, p1)], depth - 1, ax, palette, max_depth)
    
    def koch_curve(self, start: Tuple[float, float], end: Tuple[float, float], depth: int, ax, color: str, max_depth: int = 7):
        """Generate Koch curve fractal with gradient line width."""
        if depth == 0:
            # Gradient line width based on depth
            linewidth = 3 - (max_depth - depth) * 0.2
            linewidth = max(0.5, linewidth)
            ax.plot([start[0], end[0]], [start[1], end[1]], color=color, linewidth=linewidth, alpha=0.9)
        else:
            # Calculate the four points of the Koch curve
            p1 = start
            p2 = ((2*start[0] + end[0])/3, (2*start[1] + end[1])/3)
            
            # Calculate the peak point - corrected angle calculation
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            length = math.sqrt(dx*dx + dy*dy) / 3
            angle = math.atan2(dy, dx)
            
            # The peak should be at 60 degrees from the line
            p3 = (p2[0] + length * math.cos(angle + math.pi/3), 
                  p2[1] + length * math.sin(angle + math.pi/3))
            
            p4 = ((start[0] + 2*end[0])/3, (start[1] + 2*end[1])/3)
            p5 = end
            
            # Recursively draw the four segments
            self.koch_curve(p1, p2, depth - 1, ax, color, max_depth)
            self.koch_curve(p2, p3, depth - 1, ax, color, max_depth)
            self.koch_curve(p3, p4, depth - 1, ax, color, max_depth)
            self.koch_curve(p4, p5, depth - 1, ax, color, max_depth)
    
    def koch_snowflake(self, center: Tuple[float, float], size: float, depth: int, ax, palette: List[str]):
        """Generate Koch snowflake fractal with gradient colors."""
        # Alternative approach: Start with equilateral triangle
        # Calculate the three vertices of the initial triangle
        height = size * math.sqrt(3) / 2
        
        # Vertices of equilateral triangle
        v1 = (center[0], center[1] + 2*height/3)
        v2 = (center[0] - size/2, center[1] - height/3)
        v3 = (center[0] + size/2, center[1] - height/3)
        
        color = self.create_gradient_color(palette, depth, 7)
        
        # Draw the three sides of the triangle using Koch curves
        # Try alternative approach for better snowflake formation
        if depth == 0:
            # Base case: draw simple triangle
            triangle = plt.Polygon([v1, v2, v3], fill=False, edgecolor=color, linewidth=2, alpha=0.9)
            ax.add_patch(triangle)
        else:
            # Recursive case: apply Koch curve transformation to each side
            # Use the proper Koch curve implementation
            self.koch_curve_proper(v1, v2, depth, ax, color, 7)
            self.koch_curve_proper(v2, v3, depth, ax, color, 7)
            self.koch_curve_proper(v3, v1, depth, ax, color, 7)
    
    def koch_curve_proper(self, start: Tuple[float, float], end: Tuple[float, float], depth: int, ax, color: str, max_depth: int = 7):
        """Proper Koch curve implementation following the mathematical definition."""
        if depth == 0:
            # Base case: draw a straight line
            linewidth = 3 - (max_depth - depth) * 0.2
            linewidth = max(0.5, linewidth)
            ax.plot([start[0], end[0]], [start[1], end[1]], color=color, linewidth=linewidth, alpha=0.9)
        else:
            # Divide the line segment into three equal parts
            p1 = start
            p2 = ((2*start[0] + end[0])/3, (2*start[1] + end[1])/3)
            p4 = ((start[0] + 2*end[0])/3, (start[1] + 2*end[1])/3)
            p5 = end
            
            # Calculate the outward bend (equilateral triangle peak)
            # Vector from p2 to p4
            dx = p4[0] - p2[0]
            dy = p4[1] - p2[1]
            segment_length = math.sqrt(dx*dx + dy*dy)
            
            if segment_length > 0:
                # Unit vector along the line segment
                ux = dx / segment_length
                uy = dy / segment_length
                
                # Perpendicular vector (rotated 90 degrees counterclockwise)
                px = -uy
                py = ux
                
                # The peak forms an equilateral triangle, so the height is segment_length * sqrt(3)/2
                height = segment_length * math.sqrt(3) / 2
                
                # The peak point is at the midpoint of p2-p4 plus the height in perpendicular direction
                p3 = (p2[0] + (p4[0] - p2[0])/2 + px * height,
                      p2[1] + (p4[1] - p2[1])/2 + py * height)
            else:
                p3 = p2
            
            # Recursively draw the four segments
            self.koch_curve_proper(p1, p2, depth - 1, ax, color, max_depth)
            self.koch_curve_proper(p2, p3, depth - 1, ax, color, max_depth)
            self.koch_curve_proper(p3, p4, depth - 1, ax, color, max_depth)
            self.koch_curve_proper(p4, p5, depth - 1, ax, color, max_depth)
    
    def cantor_set_proper(self, intervals: List[Tuple[float, float]], depth: int, ax, color: str, y_pos: float, max_depth: int = 7):
        """Proper Cantor set implementation following the mathematical definition."""
        if depth == 0:
            # Base case: draw all remaining intervals
            linewidth = 4 - (max_depth - depth) * 0.3
            linewidth = max(1, linewidth)
            alpha = 1.0 - (max_depth - depth) * 0.1
            
            for start, end in intervals:
                ax.plot([start, end], [y_pos, y_pos], color=color, linewidth=linewidth, alpha=alpha)
        else:
            # Apply Cantor set construction: delete middle third from each interval
            new_intervals = []
            
            for start, end in intervals:
                length = end - start
                # Create two new intervals: [start, start + length/3] and [start + 2*length/3, end]
                new_intervals.append((start, start + length/3))
                new_intervals.append((start + 2*length/3, end))
            
            # Recursively apply to the new intervals
            self.cantor_set_proper(new_intervals, depth - 1, ax, color, y_pos - 10, max_depth)
            
            # Also draw the current level
            linewidth = 4 - (max_depth - depth) * 0.3
            linewidth = max(1, linewidth)
            alpha = 1.0 - (max_depth - depth) * 0.1
            
            for start, end in intervals:
                ax.plot([start, end], [y_pos, y_pos], color=color, linewidth=linewidth, alpha=alpha)
    
    def cantor_set(self, start: Tuple[float, float], length: float, depth: int, ax, color: str, y_pos: float, max_depth: int = 7):
        """Wrapper for Cantor set that converts to proper format."""
        # Start with the interval [0, 1] and scale it
        initial_intervals = [(start[0], start[0] + length)]
        self.cantor_set_proper(initial_intervals, depth, ax, color, y_pos, max_depth)
    
    def create_gradient_color(self, palette: List[str], depth: int, max_depth: int) -> str:
        """Create gradient color based on depth."""
        if max_depth == 0:
            return palette[0]
        
        # Normalize depth to 0-1 range
        normalized_depth = depth / max_depth
        
        # Convert palette colors to HSV for smooth interpolation
        colors_hsv = []
        for color in palette:
            # Convert hex to RGB to HSV
            hex_color = color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            hsv = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
            colors_hsv.append(hsv)
        
        # Interpolate between colors based on depth
        color_index = normalized_depth * (len(colors_hsv) - 1)
        lower_idx = int(color_index)
        upper_idx = min(lower_idx + 1, len(colors_hsv) - 1)
        
        if lower_idx == upper_idx:
            selected_hsv = colors_hsv[lower_idx]
        else:
            t = color_index - lower_idx
            selected_hsv = (
                colors_hsv[lower_idx][0] + t * (colors_hsv[upper_idx][0] - colors_hsv[lower_idx][0]),
                colors_hsv[lower_idx][1] + t * (colors_hsv[upper_idx][1] - colors_hsv[lower_idx][1]),
                colors_hsv[lower_idx][2] + t * (colors_hsv[upper_idx][2] - colors_hsv[lower_idx][2])
            )
        
        # Convert back to hex
        rgb = colorsys.hsv_to_rgb(selected_hsv[0], selected_hsv[1], selected_hsv[2])
        hex_color = '#' + ''.join(f'{int(c*255):02x}' for c in rgb)
        return hex_color
    
    def mandelbrot_set(self, ax, max_iter: int):
        """Generate Mandelbrot set fractal with enhanced visualization."""
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
        
        # Create custom colormap with better colors
        colors = ['#000428', '#004e92', '#009ffd', '#2a2a72', '#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3']
        n_bins = 256
        cmap = LinearSegmentedColormap.from_list('mandelbrot', colors, N=n_bins)
        
        # Plot the result with enhanced colormap
        im = ax.imshow(iterations, extent=[x_min, x_max, y_min, y_max], 
                      cmap=cmap, origin='lower', aspect='equal')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Iterations', rotation=270, labelpad=15)
        
        # Add grid for better visualization
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Real', fontsize=12)
        ax.set_ylabel('Imaginary', fontsize=12)
        ax.set_title('Mandelbrot Set', fontsize=14, pad=20)

class FractalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fractal Generator")
        self.root.geometry("1000x800")
        
        # Configure grey theme
        self.setup_theme()
        
        self.fractal_generator = FractalGenerator()
        self.current_fractal = "Sierpinski Triangle"
        self.depth = 3
        self.color_scheme = "Vibrant"
        
        self.setup_ui()
        self.update_fractal()
    
    def setup_ui(self):
        # Main frame with grey background
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
        
        # Depth slider (limited to 7)
        self.depth_label = ttk.Label(control_frame, text=f"Depth: {self.depth}")
        self.depth_label.pack(anchor=tk.W)
        self.depth_var = tk.IntVar(value=self.depth)
        depth_scale = ttk.Scale(control_frame, from_=0, to=7, variable=self.depth_var, 
                              orient=tk.HORIZONTAL, command=self.on_depth_change)
        depth_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Add update delay to prevent too frequent updates during slider movement
        self.update_job = None
        
        # Color scheme selection
        ttk.Label(control_frame, text="Color Scheme:").pack(anchor=tk.W)
        self.color_var = tk.StringVar(value=self.color_scheme)
        color_combo = ttk.Combobox(control_frame, textvariable=self.color_var,
                                 values=["Vibrant", "Ocean", "Sunset", "Forest", "Fire", "Pastel"],
                                 state="readonly")
        color_combo.pack(fill=tk.X, pady=(0, 10))
        color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        
        # Update button (now optional since slider auto-updates)
        update_btn = ttk.Button(control_frame, text="Refresh Fractal", command=self.update_fractal)
        update_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Save button
        save_btn = ttk.Button(control_frame, text="Save Image", command=self.save_image)
        save_btn.pack(fill=tk.X)
        
        # Plot frame
        plot_frame = ttk.Frame(main_frame)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure with grey theme
        self.figure = Figure(figsize=(8, 6), dpi=100, facecolor='#f0f0f0')
        self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_theme(self):
        """Setup the grey theme for the application."""
        self.root.configure(bg='#e0e0e0')
        
        # Configure matplotlib style
        plt.style.use('default')
        plt.rcParams['figure.facecolor'] = '#f0f0f0'
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['axes.edgecolor'] = '#666666'
        plt.rcParams['text.color'] = '#333333'
        plt.rcParams['axes.labelcolor'] = '#333333'
        plt.rcParams['xtick.color'] = '#666666'
        plt.rcParams['ytick.color'] = '#666666'
    
    def get_color_palette(self):
        """Get color palette based on selected scheme."""
        schemes = {
            "Vibrant": ["#e74c3c", "#f39c12", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6", "#e91e63"],
            "Ocean": ["#1abc9c", "#16a085", "#3498db", "#2980b9", "#34495e", "#2c3e50", "#95a5a6"],
            "Sunset": ["#ff7675", "#fd79a8", "#fdcb6e", "#e17055", "#d63031", "#74b9ff", "#0984e3"],
            "Forest": ["#00b894", "#00cec9", "#55a3ff", "#74b9ff", "#a29bfe", "#6c5ce7", "#fd79a8"],
            "Fire": ["#ff6b6b", "#ffa726", "#ffca28", "#66bb6a", "#42a5f5", "#ab47bc", "#ef5350"],
            "Pastel": ["#ff9ff3", "#54a0ff", "#5f27cd", "#00d2d3", "#ff9f43", "#10ac84", "#ee5a24"]
        }
        return schemes.get(self.color_scheme, schemes["Vibrant"])
    
    def on_fractal_change(self, event):
        self.current_fractal = self.fractal_var.get()
        self.update_fractal()
    
    def on_depth_change(self, value):
        self.depth = int(float(value))
        # Update the label directly
        self.depth_label.config(text=f"Depth: {self.depth}")
        
        # Cancel any pending update
        if self.update_job:
            self.root.after_cancel(self.update_job)
        
        # Schedule a new update after a short delay to prevent too frequent updates
        self.update_job = self.root.after(100, self.update_fractal)
    
    def on_color_change(self, event):
        self.color_scheme = self.color_var.get()
        self.update_fractal()
    
    def update_fractal(self):
        """Update the fractal display."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        palette = self.get_color_palette()
        
        try:
            if self.current_fractal == "Sierpinski Triangle":
                ax.set_aspect('equal')
                # Equilateral triangle coordinates
                size = 200
                points = [(-size, -size), (0, size), (size, -size)]
                self.fractal_generator.sierpinski_triangle(points, self.depth, ax, palette, 7)
                ax.set_xlim(-size*1.2, size*1.2)
                ax.set_ylim(-size*1.2, size*1.2)
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('X', fontsize=12)
                ax.set_ylabel('Y', fontsize=12)
                
            elif self.current_fractal == "Koch Snowflake":
                ax.set_aspect('equal')
                self.fractal_generator.koch_snowflake((0, 0), 300, self.depth, ax, palette)
                ax.set_xlim(-200, 200)
                ax.set_ylim(-200, 200)
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('X', fontsize=12)
                ax.set_ylabel('Y', fontsize=12)
                
            elif self.current_fractal == "Cantor Set":
                ax.set_aspect('equal')
                self.fractal_generator.cantor_set((-200, 0), 400, self.depth, ax, palette[0], 100, 7)
                ax.set_xlim(-250, 250)
                ax.set_ylim(-200, 150)
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('Position', fontsize=12)
                ax.set_ylabel('Level', fontsize=12)
                
            elif self.current_fractal == "Mandelbrot Set":
                # Enhanced Mandelbrot depth scaling
                max_iter = max(20, self.depth * 50 + 50)  # Better scaling: 20-400 iterations
                self.fractal_generator.mandelbrot_set(ax, max_iter)
                ax.set_aspect('equal')
            
            # Set title with proper spacing to avoid covering the image
            self.figure.suptitle(f"{self.current_fractal} (Depth: {self.depth})", 
                               fontsize=14, y=0.95, color='#333333')
            
            # Adjust layout to prevent title overlap
            self.figure.tight_layout(rect=[0, 0.03, 1, 0.93])
            
            # Force canvas update
            self.canvas.draw_idle()
            
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
