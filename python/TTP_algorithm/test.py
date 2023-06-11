import numpy as np
from itertools import combinations

def calculate_score(path, values):
    score = 0
    for node in path:
        score += values[node]
    return score

def ttp_solver(distance_matrix, item_values, item_weights, knapsack_capacity):
    num_nodes = len(distance_matrix)
    best_score = 0
    best_path = []

    # Generate all possible paths
    all_paths = []
    for r in range(1, num_nodes+1):
        all_paths.extend(combinations(range(1, num_nodes), r))

    # Iterate over all paths
    for path in all_paths:
        path = (0,) + path + (0,)  # Add starting and ending node
        path_weight = 0
        path_score = calculate_score(path, item_values)

        # Check if the path violates the knapsack capacity
        for node in path[1:-1]:
            path_weight += item_weights[node-1]
        if path_weight <= knapsack_capacity and path_score > best_score:
            best_score = path_score
            best_path = path

    return best_path, best_score

# Example usage
distance_matrix = np.array([
    [0, 2, 9, 10],
    [2, 0, 6, 4],
    [9, 6, 0, 8],
    [10, 4, 8, 0]
])
item_values = [2, 4, 6, 8]
item_weights = [1, 2, 3, 4]
knapsack_capacity = 7

best_path, best_score = ttp_solver(distance_matrix, item_values, item_weights, knapsack_capacity)
print("Best Path:", best_path)
print("Best Score:", best_score)
