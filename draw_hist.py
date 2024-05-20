import numpy as np
import os
import matplotlib.pyplot as plt

def plot_arrays_from_directory(directory_path):
    # Initialize a dictionary to hold data for plotting
    data = {}

    # Iterate through each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.npy'):
            file_path = os.path.join(directory_path, filename)
            # Load the numpy array from the file
            array = np.load(file_path)
            # Use the filename without the extension as the label
            label = os.path.splitext(filename)[0]
            data[label] = array

    # Plot each array with its corresponding label
    plt.figure(figsize=(10, 6))
    for label, values in data.items():
        plt.plot(values, marker='o', label=label)

    # Adding title and labels
    plt.title('Graphlet Counts from .npy Files')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    plt.tight_layout()
    plt.show()

plot_arrays_from_directory("graph_arrays")