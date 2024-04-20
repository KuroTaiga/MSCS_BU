from PIL import Image, ImageSequence
import numpy as np
import io
import time

from tensorly.decomposition import tucker, tensor_train
from tensorly.tenalg import inner
from tensorly import norm
from tensorly.tt_matrix import tt_matrix_to_tensor
from tensorly.tt_tensor import tt_to_tensor

#number of frame we use for comparison
FRAME_COUNT = 900

# Function to load a GIF file into a tensor
def gif_to_tensor(file_path):
    with Image.open(file_path) as img:
        # Convert all frames to grayscale and stack them into a tensor
        frames = np.stack([np.array(frame.convert('L')) for frame in ImageSequence.Iterator(img)])
        return frames

# Load each GIF into a tensor
file_paths = ['./fastsmallball.gif', './slowbigball.gif','./different.gif']
tensors = [gif_to_tensor(path) for path in file_paths]

print("Shape of tensors:")
print(tensors[0].shape, tensors[1].shape, tensors[2].shape) # Display the shape of the tensors to confirm loading

from scipy.spatial.distance import cosine

# Function to calculate cosine similarity between two tensors
def calculate_cosine_similarity(tensor_a, tensor_b):
    # Flatten the tensors
    flattened_a = tensor_a.flatten()
    flattened_b = tensor_b.flatten()
    
    # Calculate the cosine similarity
    similarity = 1 - cosine(flattened_a, flattened_b)
    return similarity

# Normalize all tensors to have the same number of frames
# frame number can be changed to experiment with execution time effect with different tensor decomp
normalized_tensors = [np.mean(np.split(tensor, FRAME_COUNT, axis=0), axis=1) for tensor in tensors]

# Calculate similarity scores
start_time = time.time()

similarity_1_2 = calculate_cosine_similarity(normalized_tensors[0], normalized_tensors[1])
similarity_2_3 = calculate_cosine_similarity(normalized_tensors[1], normalized_tensors[2])
similarity_1_3 = calculate_cosine_similarity(normalized_tensors[0], normalized_tensors[2])

execution_time = time.time() - start_time

print("Fast and slow ball:",similarity_1_2)
print("Slow ball and rectangle:",similarity_2_3)
print("Fast ball and rectangle",similarity_1_3)
print("Runtime: ",execution_time)

# Function to decompose a tensor using Tensor Train, return the tt_matrix
def train_decompose(tensor, rank):
    tt_matrix = tensor_train(tensor,rank=rank)
    return tt_matrix.to_tensor()
# # A simple metric is the Frobenius norm of the difference between core tensors.
# def compare_tt(tt1, tt2):
#     core_diff = np.linalg.norm(tt1.core.data - tt2.core.data)
#     return core_diff

# Function to decompose a tensor using Tucker Decomposition and return the core tensor
def tucker_decompose(tensor, rank):
    core, _ = tucker(tensor, rank=rank)
    return core
# # Function to calculate cosine similarity between two decomposed tensors
# def calculate_tucker_decomposed_similarity(core_a, core_b):
#     # Normalize the cores to have a unit norm
#     core_a = core_a / norm(core_a)
#     core_b = core_b / norm(core_b)
#     # Compute inner product between two normalized cores as similarity
#     similarity = inner(core_a, core_b)
#     return similarity

print("TensorTrain:")
rank = [1, 3, 3, 1]
start_time = time.time()
tt_matrixs = [train_decompose(tensor, rank) for tensor in normalized_tensors]
decomposition_time = time.time() - start_time
start_time = time.time()
tt_similarity_1_2 = calculate_cosine_similarity(tt_matrixs[0],tt_matrixs[1])
tt_similarity_2_3 = calculate_cosine_similarity(tt_matrixs[1],tt_matrixs[2])
tt_similarity_1_3 = calculate_cosine_similarity(tt_matrixs[0],tt_matrixs[2])
comparison_time = time.time() - start_time
total_execution_time = decomposition_time+comparison_time

print("Fast and slow ball:",tt_similarity_1_2)
print("Slow ball and rectangle:",tt_similarity_2_3)
print("Fast ball and rectangle",tt_similarity_1_3)
print("Decomposition time:",decomposition_time)
print("Comparison time:",comparison_time)
print("Total Runtime: ",total_execution_time)

print("Tucker:")
# Define a rank for the Tucker Decomposition based on the smallest mode size (to ensure decomposition is possible)
rank = (20, 20, 20) 
# Apply Tucker Decomposition to each tensor to get the core tensors
start_decomposition_time = time.time()

core_tensors = [tucker_decompose(tensor, rank) for tensor in normalized_tensors]

decomposition_time = time.time() - start_decomposition_time

# Calculate similarity scores after decomposition
start_comparison_time = time.time()

decomposed_similarity_1_2 = calculate_cosine_similarity(core_tensors[0], core_tensors[1])
decomposed_similarity_2_3 = calculate_cosine_similarity(core_tensors[1], core_tensors[2])
decomposed_similarity_1_3 = calculate_cosine_similarity(core_tensors[0], core_tensors[2])

comparison_time = time.time() - start_comparison_time
total_execution_time = decomposition_time + comparison_time


print("Fast and slow ball:",decomposed_similarity_1_2)
print("Slow ball and rectangle:",decomposed_similarity_2_3)
print("Fast ball and rectangle",decomposed_similarity_1_3)
print("Decomposition time:",decomposition_time)
print("Comparison time:",comparison_time)
print("Total Runtime: ",total_execution_time)


