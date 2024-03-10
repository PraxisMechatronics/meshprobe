import matplotlib.pyplot as plt

data = [
    ["Name", "Age", "Gender"],
    ["John", 30, "Male"],
    ["Jane", 25, "Female"],
    ["Doe", 40, "Male"],
]

fig, ax = plt.subplots()

# Create the table and add it to the plot
table = ax.table(cellText=data, loc="center")

# Modify the table properties
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 1)  # Adjust the size of the table

# Remove axis
ax.axis("off")

plt.show()
