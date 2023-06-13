import numpy as np
import matplotlib.pyplot as plt

import random

distance_matrix = [[0, 2, 5, 9],
                   [2, 0, 4, 8],
                   [5, 4, 0, 6],
                   [9, 8, 6, 0]]
item_values = [4, 6, 8, 2]
item_weights = [1, 2, 3, 2]
knapsack_capacity = 4

for i in range(1, 6):
    print(f"=== Round {i} ===")

    for j in range(len(distance_matrix)):
        new_element = random.randint(1, 5)
        distance_matrix[j].append(new_element)
    new_row = [random.randint(1, 5) for _ in range(len(distance_matrix[0]) + 1)]
    distance_matrix.append(new_row)
    new_value = random.randint(1, 5)
    item_values.append(new_value)
    new_weight = random.randint(1, 3)
    item_weights.append(new_weight)
    knapsack_capacity += random.randint(1, 3)

"""
# Data for brute force algorithm
brute_tsp_ls = [10, 20, 30, 40, 50]
brute_kp_ls = [15, 25, 35, 45, 55]
brute_time_ls = [0.5, 0.6, 0.7, 0.8, 0.9]
brute_fitness_ls = [0.3, 0.4, 0.5, 0.6, 0.7]

# Data for genetic algorithm (COGA)
coga_tsp_ls = [20, 30, 40, 50, 60]
coga_kp_ls = [25, 35, 45, 55, 65]
coga_time_ls = [0.6, 0.7, 0.8, 0.9, 1.0]
coga_fitness_ls = [0.4, 0.5, 0.6, 0.7, 0.8]

# Data for simulated annealing algorithm (CS2SA)
cs2sa_tsp_ls = [15, 25, 35, 45, 55]
cs2sa_kp_ls = [20, 30, 40, 50, 60]
cs2sa_time_ls = [0.7, 0.8, 0.9, 1.0, 1.1]
cs2sa_fitness_ls = [0.5, 0.6, 0.7, 0.8, 0.9]

# Data for multi-agent two-body algorithm (MA2B)
ma2b_tsp_ls = [25, 35, 45, 55, 65]
ma2b_kp_ls = [30, 40, 50, 60, 70]
ma2b_time_ls = [0.8, 0.9, 1.0, 1.1, 1.2]
ma2b_fitness_ls = [0.6, 0.7, 0.8, 0.9, 1.0]

# Plotting the data
x = [10, 20, 30, 40, 50]  # Assuming x-axis values

# Plotting TSP results
plt.figure(figsize=(10, 6))
plt.plot(x, brute_tsp_ls, marker='o', label='Brute Force')
plt.plot(x, coga_tsp_ls, marker='o', label='COGA')
plt.plot(x, cs2sa_tsp_ls, marker='o', label='CS2SA')
plt.plot(x, ma2b_tsp_ls, marker='o', label='MA2B')
plt.xlabel('Input Size')
plt.ylabel('TSP Result')
plt.title('TSP Results Comparison')
plt.legend()
plt.grid(True)
plt.show()

# Plotting Knapsack results
plt.figure(figsize=(10, 6))
plt.plot(x, brute_kp_ls, marker='o', label='Brute Force')
plt.plot(x, coga_kp_ls, marker='o', label='COGA')
plt.plot(x, cs2sa_kp_ls, marker='o', label='CS2SA')
plt.plot(x, ma2b_kp_ls, marker='o', label='MA2B')
plt.xlabel('Input Size')
plt.ylabel('Knapsack Result')
plt.title('Knapsack Results Comparison')
plt.legend()
plt.grid(True)
plt.show()

# Plotting Execution Time
plt.figure(figsize=(10, 6))
plt.plot(x, brute_time_ls, marker='o', label='Brute Force')
plt.plot(x, coga_time_ls, marker='o', label='COGA')
plt.plot(x, cs2sa_time_ls, marker='o', label='CS2SA')
plt.plot(x, ma2b_time_ls, marker='o', label='MA2B')
plt.xlabel('Input Size')
plt.ylabel('Execution Time (s)')
plt.title('Execution Time Comparison')
plt.legend()
plt.grid(True)
plt.show()

# Plotting Fitness
plt.figure(figsize=(10, 6))
plt.plot(x, brute_fitness_ls, marker='o', label='Brute Force')
plt.plot(x, coga_fitness_ls, marker='o', label='COGA')
plt.plot(x, cs2sa_fitness_ls, marker='o', label='CS2SA')
plt.plot(x, ma2b_fitness_ls, marker='o', label='MA2B')
plt.xlabel('Input Size')
plt.ylabel('Fitness')
plt.title('Fitness Comparison')
plt.legend()
plt.grid(True)
plt.show()
"""