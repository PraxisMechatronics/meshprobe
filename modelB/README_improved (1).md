# MeshProbe - CNC Table Flatness Analysis Tool

A Python-based visualization and analysis tool for CNC machine table flatness measurements obtained through probe mesh routines.

## Overview

MeshProbe helps machinists and quality engineers visualize and analyze the flatness of CNC machine tables by processing probe measurement data. The tool creates interactive 3D visualizations with various interpolation methods to identify high and low spots on the table surface.

## Features

- **Interactive 3D Visualization**: Rotate, zoom, and pan the surface plot
- **Multiple Interpolation Methods**: Choose between nearest-neighbor and linear interpolation
- **Adjustable Mesh Density**: Control the resolution of the interpolated surface
- **Z-Axis Scaling**: Exaggerate vertical features for better visibility
- **Statistical Analysis**: View key metrics including mean, standard deviation, and peak-to-valley
- **Multiple Data Formats**: Support for custom text format and CSV files
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install from Source
```bash
git clone https://github.com/yourusername/meshprobe.git
cd meshprobe
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python meshprobe.py
```
This will open a file dialog to select your probe data file.

### Command Line
```bash
python meshprobe.py path/to/your/data.txt
```

### Demo Mode
```bash
python meshprobe.py --demo
```
This runs the tool with randomly generated demo data.

## Data Format

MeshProbe supports two data formats:

### Custom Text Format
```
<number_of_rows>
<number_of_columns>

<z_value_1>
<z_value_2>
...
```

Example:
```
3
4

0.0010
0.0012
0.0008
0.0011
0.0009
0.0013
0.0007
0.0010
0.0011
0.0008
0.0012
0.0009
```

### CSV Format
Standard CSV with header row:
```csv
Company,Technician,Machine,SerialNumber,X_dim,Y_dim,Mode
0.0010,0.0012,0.0008,0.0011
0.0009,0.0013,0.0007,0.0010
0.0011,0.0008,0.0012,0.0009
```

## G-Code Macro

The included `meshprobe.nc` file contains a macro for Haas CNC machines that performs the probe routine:

### Required Macro Variables:
- `#1`: Probe tool offset number (e.g., 25)
- `#2`: X table dimension in inches
- `#3`: Y table dimension in inches
- `#4`: X probe grid cell size in inches
- `#5`: Y probe grid cell size in inches

### Optional Variables:
- `#7`: Work coordinate system (default: G54)
- `#8`: Starting Z plane
- `#9`: Protected Z height before probing
- `#10`: Z depth relative to G54 Z0
- `#11`: Retract after each point (0=No, 1=Yes)

## Understanding the Visualization

- **Color Map**: The plasma colormap shows height variations (purple=low, yellow=high)
- **Grid Lines**: Represent the actual probe points
- **Interpolated Surface**: Smooth surface estimated between probe points
- **Statistics Panel**: Shows key flatness metrics

### Important Metrics:
- **Z P-V (Peak-to-Valley)**: Total flatness variation
- **Z std**: Standard deviation indicates consistency
- **Z mean**: Average height (useful for leveling reference)

## Tips for Best Results

1. **Probe Grid Spacing**: Use 1-2 inch spacing for general checks, 0.5 inch for precision
2. **Table Preparation**: Clean the table thoroughly before probing
3. **Temperature**: Allow machine to reach thermal equilibrium
4. **Probe Calibration**: Verify probe repeatability before measurement

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with NumPy, Matplotlib, and SciPy
- Inspired by the need for better CNC quality control tools
