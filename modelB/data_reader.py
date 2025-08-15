"""
Data reader utilities for MeshProbe
Handles various probe data formats
"""

import numpy as np
from pathlib import Path
from typing import Tuple, Optional


class ProbeDataReader:
    """Reader for various probe data formats."""
    
    @staticmethod
    def read_file(file_path: str) -> np.ndarray:
        """
        Read probe data from file, automatically detecting format.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            numpy array of probe measurements
            
        Raises:
            ValueError: If file format is not recognized
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Try custom format first
        try:
            return ProbeDataReader.read_custom_format(file_path)
        except:
            pass
            
        # Try CSV format
        try:
            return ProbeDataReader.read_csv_format(file_path)
        except:
            pass
            
        # Try space-delimited format
        try:
            return ProbeDataReader.read_space_delimited(file_path)
        except:
            pass
            
        raise ValueError(f"Unable to parse file format: {file_path}")
    
    @staticmethod
    def read_custom_format(file_path: str) -> np.ndarray:
        """
        Read custom format with dimensions in header.
        
        Format:
        <num_rows>
        <num_cols>
        <data values...>
        """
        with open(file_path, 'r') as file:
            num_rows = int(file.readline().strip())
            num_cols = int(file.readline().strip())
            
        data = np.genfromtxt(file_path, skip_header=2)
        
        # Remove any NaN values that might be from empty lines
        data = data[~np.isnan(data)]
        
        if len(data) != num_rows * num_cols:
            raise ValueError(f"Data size mismatch. Expected {num_rows*num_cols}, got {len(data)}")
            
        return data.reshape(num_rows, num_cols)
    
    @staticmethod
    def read_csv_format(file_path: str) -> np.ndarray:
        """Read standard CSV format with optional header."""
        # Try with header first
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
        
        # Check if it's valid numeric data
        if np.any(np.isnan(data)):
            # Try without header
            data = np.genfromtxt(file_path, delimiter=',')
            
        if data.ndim != 2:
            raise ValueError("CSV data must be 2-dimensional")
            
        return data
    
    @staticmethod
    def read_space_delimited(file_path: str) -> np.ndarray:
        """Read space-delimited format."""
        data = np.loadtxt(file_path)
        
        if data.ndim != 2:
            raise ValueError("Data must be 2-dimensional")
            
        return data
    
    @staticmethod
    def validate_data(data: np.ndarray) -> Tuple[bool, Optional[str]]:
        """
        Validate probe data for common issues.
        
        Returns:
            (is_valid, error_message)
        """
        if data is None:
            return False, "Data is None"
            
        if data.size == 0:
            return False, "Data is empty"
            
        if np.any(np.isnan(data)):
            return False, "Data contains NaN values"
            
        if np.any(np.isinf(data)):
            return False, "Data contains infinite values"
            
        # Check for reasonable Z values (assuming measurements in inches)
        if np.abs(data).max() > 1.0:
            return False, "Data contains unreasonably large values (>1 inch)"
            
        if data.shape[0] < 2 or data.shape[1] < 2:
            return False, "Data grid too small (minimum 2x2)"
            
        return True, None
    
    @staticmethod
    def save_data(data: np.ndarray, file_path: str, format: str = 'custom') -> None:
        """
        Save probe data to file.
        
        Args:
            data: Probe measurement array
            file_path: Output file path
            format: 'custom', 'csv', or 'space'
        """
        if format == 'custom':
            with open(file_path, 'w') as f:
                f.write(f"{data.shape[0]}\n")
                f.write(f"{data.shape[1]}\n\n")
                for row in data:
                    for value in row:
                        f.write(f"{value:.6f}\n")
                    f.write("\n")
                    
        elif format == 'csv':
            np.savetxt(file_path, data, delimiter=',', fmt='%.6f')
            
        elif format == 'space':
            np.savetxt(file_path, data, fmt='%.6f')
            
        else:
            raise ValueError(f"Unknown format: {format}")


def demo_usage():
    """Demonstrate usage of the ProbeDataReader."""
    # Generate sample data
    sample_data = np.random.randn(5, 8) * 0.001
    
    # Save in different formats
    ProbeDataReader.save_data(sample_data, "demo_custom.txt", format='custom')
    ProbeDataReader.save_data(sample_data, "demo.csv", format='csv')
    
    # Read back
    data1 = ProbeDataReader.read_file("demo_custom.txt")
    data2 = ProbeDataReader.read_file("demo.csv")
    
    print(f"Custom format shape: {data1.shape}")
    print(f"CSV format shape: {data2.shape}")
    
    # Validate
    is_valid, msg = ProbeDataReader.validate_data(data1)
    print(f"Validation: {is_valid} {msg if msg else 'OK'}")


if __name__ == "__main__":
    demo_usage()
