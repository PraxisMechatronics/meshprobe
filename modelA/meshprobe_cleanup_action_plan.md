# MeshProbe Repository Cleanup and Improvement Action Plan

## Executive Summary
The meshprobe repository contains a tool for visualizing CNC table flatness data. The codebase shows signs of rapid prototyping with multiple iterations and duplicated functionality. This action plan outlines steps to clean up, consolidate, and improve the codebase.

## Current State Analysis

### Repository Structure
- **Main functionality**: 3D surface plotting of probe mesh data from CNC machines
- **Multiple versions**: Three different `read_mesh` files with overlapping functionality
- **Test/dummy files**: Various data generation and testing scripts
- **Documentation**: Minimal (only a 2-line README)
- **Dependencies**: No requirements.txt or setup.py

### Key Files Overview

1. **Main Application Files** (duplicates with variations):
   - `read_mesh.py` - Basic version with file dialog, interpolation, and dual plot display
   - `read_mesh3.py` - Enhanced version with more widgets (radio buttons, better controls)
   - `read_mesh_np.py` - Most refined version with cleaner UI and better organization

2. **Test/Development Files**:
   - `plottest.py` - Simple matplotlib 3D plot test
   - `tests.py` - Table display test (unrelated to main functionality)
   - `interpolation.py` - Scipy interpolation example/test

3. **Data Generation Files**:
   - `dummydata.py` - Generates random test data in specific format
   - `fake_data.py` - Incomplete CSV data generator
   - `dummyreader.py` - Test reader for generated data

4. **Data Files**:
   - `random_data.txt` - Generated test data
   - `test.csv` - Sample CSV data
   - `meshprobe.nc` - G-code macro for CNC probing

## Action Plan

### Phase 1: Immediate Cleanup (Priority: High)

1. **Consolidate Main Application**
   - Keep `read_mesh_np.py` as the main application (most refined version)
   - Delete redundant versions:
     - `read_mesh.py`
     - `read_mesh3.py`
   - Rename `read_mesh_np.py` to `meshprobe_viewer.py`

2. **Remove Unnecessary Test Files**
   - Delete `plottest.py` (basic matplotlib test)
   - Delete `tests.py` (unrelated table display)
   - Delete `interpolation.py` (scipy example)

3. **Consolidate Data Generation**
   - Keep `dummydata.py` (rename to `generate_test_data.py`)
   - Delete `fake_data.py` (incomplete and redundant)
   - Delete `dummyreader.py` (functionality already in main app)

### Phase 2: Code Improvements (Priority: High)

1. **Refactor Main Application** (`meshprobe_viewer.py`):
   ```python
   # Suggested structure:
   - class MeshProbeViewer:
       - __init__()
       - load_data()
       - setup_ui()
       - create_plot()
       - update_callbacks()
   - Separate data loading logic
   - Add error handling
   - Add data validation
   ```

2. **Add Configuration Support**:
   - Create `config.py` for default values
   - Support command-line arguments
   - Allow saving/loading of view preferences

3. **Improve Data Format Support**:
   - Currently supports custom format (rows, cols header + data)
   - Add CSV import with automatic detection
   - Add data format validation

### Phase 3: Documentation and Setup (Priority: Medium)

1. **Create Proper Documentation**:
   - Expand README.md with:
     - Project description
     - Installation instructions
     - Usage examples
     - Data format specification
     - Screenshots
   
2. **Add Setup Files**:
   - Create `requirements.txt`:
     ```
     numpy>=1.20.0
     matplotlib>=3.3.0
     scipy>=1.7.0
     tkinter (note: usually comes with Python)
     ```
   - Create `setup.py` for proper package installation

3. **Add Example Data**:
   - Create `examples/` directory
   - Move test data files there
   - Add real-world example if available

### Phase 4: Feature Enhancements (Priority: Medium)

1. **Export Capabilities**:
   - Save plots as images (PNG, PDF)
   - Export interpolated data
   - Generate flatness reports (statistics, deviations)

2. **Enhanced Visualization**:
   - Add contour plot view
   - Add cross-section views
   - Add deviation heatmap
   - Support for multiple datasets comparison

3. **Analysis Features**:
   - Calculate flatness metrics (peak-to-valley, RMS)
   - Identify high/low spots
   - Generate tolerance compliance reports

4. **UI Improvements**:
   - Add menu bar with File, View, Analysis, Help menus
   - Add toolbar for common operations
   - Remember window state and preferences
   - Add data info panel (min, max, mean, std dev)

### Phase 5: Code Quality (Priority: Low)

1. **Add Type Hints**:
   - Use Python type hints throughout
   - Add docstrings to all functions/classes

2. **Add Tests**:
   - Create `tests/` directory
   - Add unit tests for data loading
   - Add integration tests for UI components

3. **Code Formatting**:
   - Apply Black formatter
   - Add pre-commit hooks
   - Follow PEP 8 guidelines

## File Deletion List

**Delete immediately:**
- `read_mesh.py` (replaced by read_mesh_np.py)
- `read_mesh3.py` (replaced by read_mesh_np.py)
- `plottest.py` (simple test, not needed)
- `tests.py` (unrelated functionality)
- `interpolation.py` (example code, not needed)
- `fake_data.py` (incomplete, redundant)
- `dummyreader.py` (functionality in main app)

**Keep and rename:**
- `read_mesh_np.py` → `meshprobe_viewer.py`
- `dummydata.py` → `generate_test_data.py`

**Keep as-is:**
- `meshprobe.nc` (G-code reference)
- `random_data.txt` (move to examples/)
- `test.csv` (move to examples/)

## Proposed New Structure

```
meshprobe/
├── meshprobe_viewer.py      # Main application
├── config.py                # Configuration defaults
├── utils.py                 # Helper functions
├── generate_test_data.py    # Test data generator
├── requirements.txt         # Python dependencies
├── setup.py                # Package setup
├── README.md               # Comprehensive documentation
├── LICENSE                 # Keep existing
├── .gitignore             # Keep existing
├── examples/              # Example data directory
│   ├── random_data.txt
│   ├── test.csv
│   └── sample_output.png
├── docs/                  # Additional documentation
│   ├── data_format.md
│   └── gcode_reference.md (move meshprobe.nc content here)
└── tests/                 # Unit tests
    ├── test_data_loading.py
    └── test_analysis.py
```

## Implementation Priority

1. **Week 1**: Phase 1 (Cleanup) + Start Phase 2 (Refactoring)
2. **Week 2**: Complete Phase 2 + Phase 3 (Documentation)
3. **Week 3**: Phase 4 (Feature Enhancements)
4. **Week 4**: Phase 5 (Code Quality)

## Major Improvement Opportunities

1. **Modular Architecture**: Current code is monolithic; break into modules
2. **Error Handling**: No error handling for file operations or data validation
3. **Performance**: Consider using vispy or plotly for large datasets
4. **Data Pipeline**: Create clear data flow from raw probe data to visualization
5. **Batch Processing**: Support processing multiple files
6. **Report Generation**: Automated PDF reports with plots and statistics
7. **Integration**: Consider plugin architecture for different CNC/probe formats

This action plan provides a clear path from the current prototype to a professional-grade tool while maintaining the existing functionality.
