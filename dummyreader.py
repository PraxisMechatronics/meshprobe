import numpy as np

# Define the file path
file_path = "random_data.txt"

# Read the first two lines to get the number of rows and columns
with open(file_path, "r") as file:
    num_rows = int(file.readline().strip())
    num_cols = int(file.readline().strip())

# Read data from text file using np.genfromtxt
data = np.genfromtxt(file_path, skip_header=2)

# Reshape the data array based on the number of rows and columns
data = data.reshape(num_rows, num_cols)

# Print the data
print(data)
