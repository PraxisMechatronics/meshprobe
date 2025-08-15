#!/bin/bash
# MeshProbe Repository Cleanup Script
# This script reorganizes the meshprobe repository structure

echo "MeshProbe Repository Cleanup"
echo "============================"

# Create new directory structure
echo "Creating new directory structure..."
mkdir -p gcode
mkdir -p utils
mkdir -p tests/test_data
mkdir -p examples

# Move files to appropriate locations
echo "Moving files..."

# Move G-code
mv meshprobe.nc gcode/ 2>/dev/null || echo "  - meshprobe.nc already moved or not found"

# Move test data
mv test.csv tests/test_data/sample.csv 2>/dev/null || echo "  - test.csv already moved or not found"
mv random_data.txt tests/test_data/sample.txt 2>/dev/null || echo "  - random_data.txt already moved or not found"

# Rename files
mv dummydata.py tests/generate_test_data.py 2>/dev/null || echo "  - dummydata.py already moved or not found"
mv read_mesh_np.py meshprobe.py 2>/dev/null || echo "  - read_mesh_np.py already moved or not found"

# Remove redundant files
echo "Removing redundant files..."
rm -f interpolation.py plottest.py tests.py fake_data.py read_mesh.py read_mesh3.py dummyreader.py

# Create __init__.py files for Python packages
touch utils/__init__.py
touch tests/__init__.py

# Copy improved files if they exist
if [ -f "/tmp/outputs/meshprobe_improved.py" ]; then
    echo "Copying improved meshprobe.py..."
    cp /tmp/outputs/meshprobe_improved.py meshprobe.py
fi

if [ -f "/tmp/outputs/requirements.txt" ]; then
    echo "Copying requirements.txt..."
    cp /tmp/outputs/requirements.txt requirements.txt
fi

if [ -f "/tmp/outputs/README_improved.md" ]; then
    echo "Copying improved README.md..."
    cp /tmp/outputs/README_improved.md README.md
fi

echo ""
echo "Cleanup complete! New structure:"
echo "================================"
tree -L 3 2>/dev/null || find . -type f -name "*.py" -o -name "*.nc" -o -name "*.txt" -o -name "*.md" | grep -v ".git" | sort

echo ""
echo "Next steps:"
echo "1. Review the changes"
echo "2. Test meshprobe.py to ensure it works"
echo "3. Commit the changes to git"
echo ""
echo "To test: python meshprobe.py --demo"
