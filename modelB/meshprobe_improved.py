#!/usr/bin/env python3
"""
MeshProbe - CNC Table Flatness Analysis Tool
Visualize and analyze CNC table flatness measurements from probe data.
"""

import sys
import argparse
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import RegularGridInterpolator
from matplotlib.widgets import Slider, RadioButtons


class MeshProbeAnalyzer:
    """Main class for analyzing and visualizing probe mesh data."""
    
    def __init__(self, data_file=None):
        self.data_file = data_file
        self.data = None
        self.interp = None
        self.fig = None
        self.ax = None
        
        # Default parameters
        self.interp_method = 'nearest'
        self.mesh_density = 10
        self.z_scale = None
        
    def load_data(self, file_path=None):
        """Load probe data from file."""
        if file_path is None:
            file_path = self._select_file()
            if not file_path:
                print("No file selected. Exiting.")
                sys.exit(0)
        
        try:
            # Try to read custom format (rows, cols in header)
            with open(file_path, 'r') as file:
                first_line = file.readline().strip()
                second_line = file.readline().strip()
                
                # Check if it's the custom format
                if first_line.isdigit() and second_line.isdigit():
                    num_rows = int(first_line)
                    num_cols = int(second_line)
                    self.data = np.genfromtxt(file_path, skip_header=2)
                    self.data = self.data.reshape(num_rows, num_cols)
                else:
                    # Try CSV format
                    file.seek(0)
                    self.data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
                    
            print(f"Loaded data shape: {self.data.shape}")
            print(f"Data range: [{np.min(self.data):.4f}, {np.max(self.data):.4f}]")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            sys.exit(1)
            
    def _select_file(self):
        """Open file dialog for data selection."""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select Probe Data File",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        root.destroy()
        return file_path
        
    def setup_interpolation(self):
        """Set up the interpolation grid."""
        # Generate grid for interpolation
        self.x = np.linspace(0, self.data.shape[1], self.data.shape[1])
        self.y = np.linspace(0, self.data.shape[0], self.data.shape[0])
        
        # Create interpolator
        self.interp = RegularGridInterpolator(
            (self.x, self.y),
            self.data.T,
            method=self.interp_method,
            bounds_error=False,
        )
        
        # Generate high-resolution mesh
        self._update_mesh()
        
    def _update_mesh(self):
        """Update the interpolated mesh based on current density."""
        self.xx, self.yy = np.meshgrid(
            np.linspace(0, self.data.shape[1], int(self.data.shape[1] * self.mesh_density)),
            np.linspace(0, self.data.shape[0], int(self.data.shape[0] * self.mesh_density)),
            indexing="xy",
        )
        
    def create_visualization(self):
        """Create the main visualization window."""
        # Set up matplotlib parameters
        mpl.rcParams.update({"font.size": 14})
        
        # Create figure
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection="3d")
        
        # Initial plot
        self._update_plot()
        
        # Add controls
        self._add_controls()
        
        # Add information panel
        self._add_info_panel()
        
        # Configure window
        self._configure_window()
        
    def _update_plot(self):
        """Update the 3D surface plot."""
        self.ax.clear()
        
        # Plot surface
        surf = self.ax.plot_surface(
            self.xx, self.yy, 
            self.interp((self.xx, self.yy)), 
            cmap=cm.plasma,
            alpha=0.9
        )
        
        # Set labels and limits
        self.ax.set_xlabel('X Position')
        self.ax.set_ylabel('Y Position')
        self.ax.set_zlabel('Z Height')
        
        self.ax.set_xlim(0, self.data.shape[1])
        self.ax.set_ylim(0, self.data.shape[0])
        self.ax.set_zlim(np.min(self.data), np.max(self.data))
        
        # Set aspect ratio
        if self.z_scale:
            self.ax.set_box_aspect([self.data.shape[1], self.data.shape[0], self.z_scale])
            
        # Add colorbar if not exists
        if not hasattr(self, 'colorbar'):
            self.colorbar = self.fig.colorbar(surf, ax=self.ax, shrink=0.5, aspect=10, pad=0.1)
            self.colorbar.set_label('Height (units)')
            
    def _add_controls(self):
        """Add interactive controls to the plot."""
        # Z-scale slider
        scale_mean = (self.data.shape[1] + self.data.shape[0]) / 4
        self.z_scale = scale_mean
        
        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        self.z_slider = Slider(
            slider_ax, 'Z Scale', 
            scale_mean / 2, scale_mean * 2, 
            valinit=scale_mean
        )
        self.z_slider.on_changed(self._update_z_scale)
        
        # Mesh density slider
        slider2_ax = plt.axes([0.1, 0.02, 0.8, 0.03])
        self.density_slider = Slider(
            slider2_ax, 'Mesh Density', 
            1, 30, 
            valinit=self.mesh_density,
            valstep=1
        )
        self.density_slider.on_changed(self._update_mesh_density)
        
        # Interpolation method selector
        radio_ax = plt.axes([0.02, 0.15, 0.15, 0.1])
        self.radio = RadioButtons(radio_ax, ('nearest', 'linear'))
        self.radio.on_clicked(self._update_interp_method)
        
    def _add_info_panel(self):
        """Add information panel with statistics."""
        info_text = f"""Data Statistics:
X size: {self.data.shape[1]} points
Y size: {self.data.shape[0]} points
Z max : {np.max(self.data):.4f}
Z min : {np.min(self.data):.4f}
Z mean: {np.mean(self.data):.4f}
Z std : {np.std(self.data):.4f}
Z P-V : {np.max(self.data) - np.min(self.data):.4f}"""
        
        self.fig.text(0.02, 0.5, info_text, fontsize=12, 
                     verticalalignment='center',
                     bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray"))
        
        # Title
        self.fig.suptitle('Table Flatness Probe Mesh Analysis', fontsize=20)
        
    def _configure_window(self):
        """Configure the matplotlib window."""
        mng = plt.get_current_fig_manager()
        
        # Try to maximize window (platform-specific)
        try:
            # For TkAgg backend
            if hasattr(mng, 'window'):
                if hasattr(mng.window, 'state'):
                    mng.window.state('zoomed')
                elif hasattr(mng.window, 'showMaximized'):
                    mng.window.showMaximized()
        except:
            pass
            
        # Set window title
        if hasattr(mng, 'set_window_title'):
            mng.set_window_title('MeshProbe - Table Flatness Analyzer')
            
    def _update_z_scale(self, val):
        """Update Z-axis scale."""
        self.z_scale = val
        self.ax.set_box_aspect([self.data.shape[1], self.data.shape[0], self.z_scale])
        plt.draw()
        
    def _update_mesh_density(self, val):
        """Update mesh density for interpolation."""
        self.mesh_density = int(val)
        self._update_mesh()
        self._update_plot()
        plt.draw()
        
    def _update_interp_method(self, label):
        """Update interpolation method."""
        self.interp_method = label
        
        # Recreate interpolator with new method
        self.interp = RegularGridInterpolator(
            (self.x, self.y),
            self.data.T,
            method=self.interp_method,
            bounds_error=False,
        )
        
        # Update plot
        self._update_plot()
        plt.draw()
        
    def show(self):
        """Display the visualization."""
        plt.show()
        
    def export_report(self, filename):
        """Export analysis report (future feature)."""
        # TODO: Implement PDF/HTML report generation
        pass


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Analyze CNC table flatness probe data'
    )
    parser.add_argument('datafile', nargs='?', help='Path to probe data file')
    parser.add_argument('--demo', action='store_true', 
                       help='Run with demo data')
    
    args = parser.parse_args()
    
    # Create analyzer instance
    analyzer = MeshProbeAnalyzer()
    
    # Load data
    if args.demo:
        # Generate demo data
        print("Generating demo data...")
        analyzer.data = np.random.randn(20, 30) * 0.001
    else:
        analyzer.load_data(args.datafile)
    
    # Set up and display
    analyzer.setup_interpolation()
    analyzer.create_visualization()
    analyzer.show()


if __name__ == '__main__':
    main()
