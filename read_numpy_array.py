import numpy as np

# Convert to a numpy array
array = np.array([1418, 29265,   4071, 472715, 227708 ,213036,   6494,  36093 ,  7085])

# Save the numpy array to a file
np.save("graphlet_arrays/georgianFolk_graph.net.npy", array)
loaded_array = np.load("graphlet_arrays/georgianFolk_graph.net.npy")
print("Loaded Array:\n", loaded_array)