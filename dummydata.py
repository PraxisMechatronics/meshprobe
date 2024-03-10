import random

datarows = 24
datacols = 48


# Function to generate random data
def generate_random_data():
    return [
        (random.uniform(-1, 1) * 0.002) for _ in range(datacols)
    ]  # Generate 12 random values


# File path to save the text file
file_path = "random_data.txt"

# Generate random data and write to text file
with open(file_path, "w") as txtfile:
    txtfile.write(str(datarows) + "\n")
    txtfile.write(str(datacols) + "\n" + "\n")

    for _ in range(datarows):
        data_group = generate_random_data()
        for value in data_group:
            txtfile.write(f"{value:.4f}\n")
        txtfile.write("\n")  # Write an empty line after each group

print(f"Random data saved to {file_path}")
