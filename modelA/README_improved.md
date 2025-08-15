# MeshProbe Viewer

A Python-based 3D visualization tool for analyzing CNC machine table flatness data collected via probe mesh routines.

![MeshProbe Viewer Screenshot](docs/images/screenshot.png)

## Overview

MeshProbe Viewer processes and visualizes geometric tolerance data from CNC machines, helping machinists and quality engineers assess table flatness and identify areas requiring adjustment. The tool supports interactive 3D visualization with adjustable interpolation methods and export capabilities.

## Features

- **Interactive 3D Visualization**: Real-time 3D surface plots with adjustable viewing angles
- **Multiple Interpolation Methods**: Nearest neighbor and linear interpolation with adjustable mesh density
- **Statistical Analysis**: Automatic calculation of min, max, mean, and standard deviation
- **Flexible Data Import**: Support for custom probe data formats
- **Export Capabilities**: Save plots and statistical reports
- **Customizable Display**: Adjustable Z-axis scaling for enhanced visualization

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Install from source
```bash
git clone https://github.com/yourusername/meshprobe.git
cd meshprobe
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python meshprobe_viewer.py
```
This will open a file dialog to select your probe data file.

### Command Line Usage
```bash
python meshprobe_viewer.py --file data.txt --method linear --density 20
```

### Data Format

The tool expects probe data in the following format:
```
<number_of_rows>
<number_of_columns>
<z_value_1>
<z_value_2>
...
<z_value_n>
```

Example:
```
3
4
0.0012
0.0008
-0.0003
0.0015
...
```

### Generating Test Data
```bash
python generate_test_data.py --rows 24 --cols 48 --output test_data.txt
```

## G-Code Macro

The included `meshprobe.nc` file contains a G-code macro for Haas machines that automates the probe mesh data collection process. Key parameters:

- `#1`: Probe tool offset number
- `#2`: X table dimension (inches)
- `#3`: Y table dimension (inches)
- `#4`: X probe grid cell size (inches)
- `#5`: Y probe grid cell size (inches)

## Interface Controls

- **Z Scale Slider**: Adjust vertical exaggeration for better visualization
- **Mesh Density Slider**: Control interpolation resolution (higher = smoother)
- **Interpolation Method**: Choose between nearest neighbor and linear interpolation
- **Mouse Controls**: Click and drag to rotate, scroll to zoom

## Examples

### Visualizing Table Flatness
```python
from meshprobe_viewer import MeshProbeViewer

viewer = MeshProbeViewer()
viewer.load_data('probe_data.txt')
viewer.setup_plot()
viewer.show()
```

### Exporting Results
```python
# Export high-resolution plot
viewer.export_plot('flatness_plot.png', dpi=300)

# Export statistical report
viewer.export_statistics('flatness_report.txt')
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
```bash
pip install -r requirements-dev.txt
```

### Running Tests
```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Developed for validating CNC machine table flatness
- Uses matplotlib for 3D visualization
- Interpolation powered by scipy

## Troubleshooting

### Common Issues

**ImportError for tkinter**: Install python3-tk package
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (if using Homebrew Python)
brew install python-tk
```

**Memory issues with large datasets**: Reduce mesh density or use data decimation

**Slow performance**: Try using nearest neighbor interpolation instead of linear

## Roadmap

- [ ] Add support for CSV and Excel data formats
- [ ] Implement cubic and quintic interpolation options
- [ ] Add contour plot visualization mode
- [ ] Create tolerance band overlay feature
- [ ] Add batch processing for multiple files
- [ ] Implement automated report generation with PDF export

## Contact

For questions or support, please open an issue on GitHub.
