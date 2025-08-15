"""
MeshProbe Viewer - Refactored Sample Structure
This is a demonstration of how the code could be restructured for better maintainability
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from scipy.interpolate import RegularGridInterpolator
import tkinter as tk
from tkinter import filedialog, messagebox
from dataclasses import dataclass
from typing import Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MeshData:
    """Container for mesh probe data"""
    data: np.ndarray
    rows: int
    cols: int
    
    @property
    def shape(self) -> Tuple[int, int]:
        return (self.rows, self.cols)
    
    @property
    def statistics(self) -> dict:
        return {
            'min': np.min(self.data),
            'max': np.max(self.data),
            'mean': np.mean(self.data),
            'std': np.std(self.data),
            'range': np.max(self.data) - np.min(self.data)
        }


class DataLoader:
    """Handles loading of different data formats"""
    
    @staticmethod
    def load_custom_format(filepath: str) -> MeshData:
        """Load data in custom format (rows, cols in header)"""
        try:
            with open(filepath, 'r') as file:
                num_rows = int(file.readline().strip())
                num_cols = int(file.readline().strip())
            
            data = np.genfromtxt(filepath, skip_header=2)
            data = data.reshape(num_rows, num_cols)
            
            return MeshData(data=data, rows=num_rows, cols=num_cols)
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise
    
    @staticmethod
    def load_csv_format(filepath: str) -> MeshData:
        """Load standard CSV format"""
        # Implementation for CSV loading
        pass


class MeshProbeViewer:
    """Main application class for viewing mesh probe data"""
    
    def __init__(self):
        self.mesh_data: Optional[MeshData] = None
        self.fig = None
        self.ax = None
        self.interpolator = None
        self.interp_method = 'nearest'
        self.mesh_density = 10
        self.z_scale = 1.0
        
    def load_data(self, filepath: Optional[str] = None) -> bool:
        """Load mesh data from file"""
        if not filepath:
            filepath = self._select_file()
            if not filepath:
                return False
        
        try:
            self.mesh_data = DataLoader.load_custom_format(filepath)
            logger.info(f"Loaded data: {self.mesh_data.shape}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            return False
    
    def _select_file(self) -> Optional[str]:
        """Open file dialog to select data file"""
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(
            title="Select Mesh Probe Data File",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        root.destroy()
        return filepath if filepath else None
    
    def setup_plot(self):
        """Initialize the plot window and widgets"""
        if not self.mesh_data:
            raise ValueError("No data loaded")
        
        # Setup matplotlib
        plt.rcParams.update({'font.size': 12})
        
        # Create figure
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Setup interpolator
        self._setup_interpolator()
        
        # Create initial plot
        self._update_plot()
        
        # Add widgets
        self._add_widgets()
        
        # Add title and labels
        self._setup_labels()
        
        # Maximize window
        self._maximize_window()
    
    def _setup_interpolator(self):
        """Setup the interpolation grid"""
        x = np.linspace(0, self.mesh_data.cols, self.mesh_data.cols)
        y = np.linspace(0, self.mesh_data.rows, self.mesh_data.rows)
        
        self.interpolator = RegularGridInterpolator(
            (x, y),
            self.mesh_data.data.T,
            method=self.interp_method,
            bounds_error=False
        )
    
    def _update_plot(self):
        """Update the 3D surface plot"""
        self.ax.clear()
        
        # Generate interpolated grid
        xx, yy = np.meshgrid(
            np.linspace(0, self.mesh_data.cols, int(self.mesh_data.cols * self.mesh_density)),
            np.linspace(0, self.mesh_data.rows, int(self.mesh_data.rows * self.mesh_density)),
            indexing='xy'
        )
        
        # Plot surface
        surf = self.ax.plot_surface(
            xx, yy, 
            self.interpolator((xx, yy)), 
            cmap='plasma',
            alpha=0.9
        )
        
        # Set limits and aspect
        self.ax.set_xlim(0, self.mesh_data.cols)
        self.ax.set_ylim(0, self.mesh_data.rows)
        self.ax.set_zlim(self.mesh_data.statistics['min'], self.mesh_data.statistics['max'])
        self.ax.set_box_aspect([self.mesh_data.cols, self.mesh_data.rows, self.z_scale])
        
        # Labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        plt.draw()
    
    def _add_widgets(self):
        """Add interactive widgets"""
        # Z-scale slider
        scale_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        scale_mean = (self.mesh_data.cols + self.mesh_data.rows) / 4
        self.scale_slider = Slider(
            scale_ax, 'Z Scale', 
            scale_mean / 2, scale_mean * 2, 
            valinit=scale_mean
        )
        self.scale_slider.on_changed(self._on_scale_change)
        
        # Mesh density slider
        density_ax = plt.axes([0.1, 0.02, 0.8, 0.03])
        self.density_slider = Slider(
            density_ax, 'Mesh Density',
            1, 30, valinit=10
        )
        self.density_slider.on_changed(self._on_density_change)
        
        # Interpolation method selector
        method_ax = plt.axes([0.05, 0.15, 0.12, 0.05])
        self.method_selector = RadioButtons(
            method_ax,
            ('nearest', 'linear')
        )
        self.method_selector.on_clicked(self._on_method_change)
    
    def _on_scale_change(self, val):
        """Handle Z-scale slider change"""
        self.z_scale = val
        self.ax.set_box_aspect([self.mesh_data.cols, self.mesh_data.rows, self.z_scale])
        plt.draw()
    
    def _on_density_change(self, val):
        """Handle mesh density slider change"""
        self.mesh_density = int(val)
        self._update_plot()
    
    def _on_method_change(self, label):
        """Handle interpolation method change"""
        self.interp_method = label
        self._setup_interpolator()
        self._update_plot()
    
    def _setup_labels(self):
        """Add title and information labels"""
        # Title
        self.fig.text(
            0.5, 0.95, 
            'Table Flatness Probe Mesh Interpreter',
            fontsize=20, ha='center'
        )
        
        # Statistics
        stats = self.mesh_data.statistics
        info_text = f"""
Data Shape: {self.mesh_data.cols} x {self.mesh_data.rows}
Z Range: {stats['min']:.4f} to {stats['max']:.4f}
Z Mean: {stats['mean']:.4f} ± {stats['std']:.4f}
Total Range: {stats['range']:.4f}
        """
        self.fig.text(0.05, 0.5, info_text, fontsize=10, verticalalignment='top')
    
    def _maximize_window(self):
        """Maximize the plot window"""
        try:
            mng = plt.get_current_fig_manager()
            mng.window.state('zoomed')
            mng.set_window_title('MeshProbe Viewer')
        except:
            pass  # Not all backends support this
    
    def show(self):
        """Display the plot"""
        plt.show()
    
    def export_plot(self, filename: str, dpi: int = 300):
        """Export the current plot to file"""
        self.fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        logger.info(f"Plot saved to {filename}")
    
    def export_statistics(self, filename: str):
        """Export data statistics to file"""
        stats = self.mesh_data.statistics
        with open(filename, 'w') as f:
            f.write("Mesh Probe Data Statistics\n")
            f.write("=" * 30 + "\n")
            f.write(f"Data Shape: {self.mesh_data.cols} x {self.mesh_data.rows}\n")
            for key, value in stats.items():
                f.write(f"{key.capitalize()}: {value:.6f}\n")
        logger.info(f"Statistics saved to {filename}")


def main():
    """Main entry point"""
    viewer = MeshProbeViewer()
    
    if viewer.load_data():
        viewer.setup_plot()
        viewer.show()


if __name__ == "__main__":
    main()
