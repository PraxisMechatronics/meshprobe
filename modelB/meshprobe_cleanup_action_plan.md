# MeshProbe Repository Cleanup Action Plan

## Overview
The MeshProbe repository is a tool for analyzing CNC table flatness data from probe measurements. It visualizes 3D geometric tolerancing data but suffers from code duplication, inconsistent organization, and lack of documentation.

## Current State Analysis

### File Inventory
1. **Main Visualization Scripts (3 versions with duplicated functionality):**
   - `read_mesh.py` - Basic version with file dialog, 3D plotting, and slider
   - `read_mesh3.py` - Enhanced version with more controls (interpolation methods, visibility toggles)
   - `read_mesh_np.py` - Most complete version with better UI and maximized window support

2. **Data Generation/Testing Scripts:**
   - `dummydata.py` - Generates random test data in specific format
   - `fake_data.py` - Incomplete CSV data generator
   - `dummyreader.py` - Simple reader for the dummy data format
   - `random_data.txt` - Generated test data file
   - `test.csv` - Sample CSV data

3. **Experimental/Test Scripts:**
   - `interpolation.py` - Standalone interpolation example
   - `plottest.py` - Basic 3D plotting test
   - `tests.py` - Matplotlib table display test (unrelated to main functionality)

4. **G-Code:**
   - `meshprobe.nc` - The actual CNC macro for probe measurements

## Key Issues Identified

1. **Code Duplication:** Three versions of essentially the same visualization tool
2. **No Clear Entry Point:** Unclear which script users should run
3. **Missing Documentation:** Minimal README, no usage instructions
4. **No Requirements File:** Dependencies not documented
5. **Inconsistent Data Format:** CSV vs custom text format handling
6. **No Error Handling:** Scripts crash if file selection is cancelled
7. **Hardcoded Values:** Window manager specific code, fixed data assumptions
8. **No Modularity:** Everything in single scripts, no reusable components

## Recommended Actions

### 1. Immediate Cleanup (Delete Redundant Files)
```bash
# Delete redundant/experimental files
rm interpolation.py  # Just a scipy example
rm plottest.py      # Basic matplotlib test
rm tests.py         # Unrelated table display
rm fake_data.py     # Incomplete and unused
rm read_mesh.py     # Superseded by read_mesh_np.py
rm read_mesh3.py    # Superseded by read_mesh_np.py
```

### 2. Reorganize Project Structure
```
meshprobe/
├── README.md              # Enhanced documentation
├── requirements.txt       # Dependencies
├── meshprobe.py          # Main entry point (renamed from read_mesh_np.py)
├── gcode/
│   └── meshprobe.nc      # CNC macro
├── utils/
│   ├── __init__.py
│   ├── data_reader.py    # Extract data reading logic
│   └── visualization.py  # Extract plotting utilities
├── tests/
│   ├── __init__.py
│   ├── generate_test_data.py  # Renamed from dummydata.py
│   └── test_data/
│       ├── sample.csv
│       └── sample.txt
└── examples/
    └── example_usage.py
```

### 3. Code Improvements

#### A. Create a Proper Main Script (`meshprobe.py`)
- Add proper argument parsing for command-line usage
- Add error handling for file operations
- Make window maximization cross-platform
- Add option to load file from command line

#### B. Extract Reusable Components
- **Data Reader Module:** Handle both CSV and custom text formats
- **Visualization Module:** 3D plotting utilities
- **Interpolation Utilities:** Configurable interpolation methods

#### C. Add Configuration Support
- Allow users to save/load visualization preferences
- Support for different color maps
- Configurable default interpolation settings

### 4. Documentation Improvements

#### A. Enhanced README.md
```markdown
# MeshProbe - CNC Table Flatness Analysis Tool

## Overview
Visualize and analyze CNC table flatness measurements from probe data.

## Features
- 3D surface visualization with interpolation
- Multiple interpolation methods (nearest, linear)
- Adjustable Z-axis scaling
- Interactive mesh density control
- Statistical analysis display

## Installation
pip install -r requirements.txt

## Usage
python meshprobe.py [datafile]

## Data Format
...
```

#### B. Add Requirements File
```
numpy>=1.20.0
matplotlib>=3.3.0
scipy>=1.7.0
```

### 5. Major Improvements to Implement

#### A. Enhanced Data Handling
- Support multiple data formats (CSV, text, possibly direct CNC output)
- Add data validation and error messages
- Support for different probe grid patterns

#### B. Analysis Features
- Add flatness tolerance visualization (show areas out of spec)
- Export analysis reports (PDF/HTML)
- Compare multiple measurements
- Calculate standard flatness metrics (peak-to-valley, RMS, etc.)

#### C. User Interface Improvements
- Add file menu for recent files
- Save/export visualizations
- Add measurement annotations
- Implement proper zoom/pan controls

#### D. Performance Optimization
- Lazy loading for large datasets
- Caching for interpolated surfaces
- Option to downsample for performance

### 6. Advanced Features (Future)
- Real-time data streaming from CNC
- Database storage for historical measurements
- Web-based visualization option
- Integration with CAD/CAM software
- Machine learning for predictive maintenance

## Implementation Priority

1. **Phase 1 (Immediate):**
   - Clean up redundant files
   - Create requirements.txt
   - Fix error handling in main script
   - Update README

2. **Phase 2 (Short-term):**
   - Reorganize into proper package structure
   - Extract reusable modules
   - Add command-line interface
   - Improve documentation

3. **Phase 3 (Medium-term):**
   - Add analysis features
   - Implement data format flexibility
   - Create test suite
   - Add configuration support

4. **Phase 4 (Long-term):**
   - Web interface
   - Database integration
   - Advanced analytics
   - Machine learning features

## Quick Start Commands
```bash
# Clean up repository
git rm interpolation.py plottest.py tests.py fake_data.py read_mesh.py read_mesh3.py

# Rename main file
git mv read_mesh_np.py meshprobe.py

# Create new structure
mkdir -p gcode utils tests/test_data examples
git mv meshprobe.nc gcode/
git mv dummydata.py tests/generate_test_data.py
git mv test.csv tests/test_data/sample.csv
git mv random_data.txt tests/test_data/sample.txt
```

This plan provides a clear path from the current messy state to a well-organized, maintainable tool that can grow with your needs.
