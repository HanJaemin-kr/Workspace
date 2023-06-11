#from matls_ttp import MATLS
from ma2b_ttp import MA2B
from coGA_ttp import CoGA
from s5_ttp import S5
from cs2sa_ttp import CS2SA
from bruteforce_ttp import BRUTE
from GA_ttp import GA
import numpy as np
import time
from itertools import permutations


def calculate_brute_force(distance_matrix):
    cities = list(range(len(distance_matrix)))
    min_distance = float('inf')
    best_path = None
    for perm in permutations(cities):
        distance = calculate_distance(perm, distance_matrix)
        if distance < min_distance:
            min_distance = distance
            best_path = perm
    return best_path, min_distance

def calculate_distance(path, distance_matrix):
    total_distance = 0
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        total_distance += distance_matrix[start][end]
    return total_distance


# TTP problem example
distance_matrix = [
    [0, 2, 5, 9, 10, 3, 7, 4],
    [2, 0, 4, 8, 9, 7, 6, 5],
    [5, 4, 0, 6, 7, 2, 3, 1],
    [9, 8, 6, 0, 3, 4, 9, 2],
    [10, 9, 7, 3, 0, 6, 5, 3],
    [3, 7, 2, 4, 6, 0, 8, 6],
    [7, 6, 3, 9, 5, 8, 0, 7],
    [4, 5, 1, 2, 3, 6, 7, 0]
]
item_values = [4, 6, 8, 2, 5, 3, 7, 9]
item_weights = [1, 2, 3, 2, 1, 4, 5, 3]
knapsack_capacity = 6
"""
distance_matrix = [
 [0, 2, 5, 9],
 [2, 0, 4, 8],
 [5, 4, 0, 6],
 [9, 8, 6, 0],]
item_values = [4, 6, 8, 2]
item_weights = [1, 2, 3, 2]
knapsack_capacity = 4
"""
# ================ ga-param ================
population_size = 1000
elite_size = 0.2
num_generations = 50
num_agents = 1
# ================================================================


# brute-force Algorithm
start_time = time.time()
brute = BRUTE(distance_matrix, item_values, item_weights, knapsack_capacity)
best_tsp_genome, best_kp_genome, best_fitness = brute.solve_ttp_brute_force()
end_time = time.time()

print("Brute Force Execution Time:", end_time - start_time, "seconds")

# co-ga Algorithm
start_time = time.time()
coga = CoGA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size, num_generations)
best_individual, ttp_fitness = coga.solve_ttp_problem()
end_time = time.time()

print("Co-EA Execution Time:", end_time - start_time, "seconds")

# ga Algorithm
start_time = time.time()
ga = GA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size, num_generations)
best_individual, ttp_fitness = ga.solve_ttp_problem()
end_time = time.time()

print("GA Execution Time:", end_time - start_time, "seconds")



start_time = time.time()
cs2sa = CS2SA()
best_tsp_solution, best_kp_solution, best_fitness = cs2sa.cs2sa_algorithm(distance_matrix, item_values, item_weights,
                                                                   knapsack_capacity)
end_time = time.time()
print("CS2SA Execution Time:", end_time - start_time, "seconds")




# MA2B Algorithm
start_time = time.time()
ma2b = MA2B(distance_matrix, item_values, item_weights, knapsack_capacity)
tsp_solution, kp_solution, total_fitness = ma2b.ma2b_algorithm()

print("\n\n\n=======MA2B Algorithm=======")
print("TSP Solution:", tsp_solution)
print("Selected Knapsack Weights:", sum([item_weights[i] for i in range(len(kp_solution)) if kp_solution[i] == 1]))
print("Total Item Value:", sum([item_values[i] for i in range(len(kp_solution)) if kp_solution[i] == 1]))
total_distance = 0
for i in range(len(tsp_solution)):
    city1 = tsp_solution[i] - 1
    city2 = tsp_solution[(i + 1) % len(tsp_solution)] - 1
    total_distance += distance_matrix[city1][city2]
print(" >2 Total Distance:", total_distance)
print("Total Fitness:", total_fitness)

end_time = time.time()
print("MA2B Execution Time:", end_time - start_time, "seconds")


# s5 Algorithm
start_time = time.time()
s5 = S5(distance_matrix, item_values, item_weights, knapsack_capacity)
best_tsp_solution, best_kp_solution, best_fitness = s5.s5_algorithm(num_agents=50, num_generations=100)

print("\n=======S5 Algorithm=======")
print("Best TSP Solution:", best_tsp_solution)
print("Selected Knapsack Weights:", sum([item_weights[i] for i in range(len(best_kp_solution)) if best_kp_solution[i] == 1]))
print("Total Item Value:", sum([item_values[i] for i in range(len(best_kp_solution)) if best_kp_solution[i] == 1]))
total_distance = 0
for i in range(len(best_tsp_solution)):
    city1 = best_tsp_solution[i] - 1
    city2 = best_tsp_solution[(i + 1) % len(best_tsp_solution)] - 1
    total_distance += distance_matrix[city1][city2]
print(" >2 Total Distance:", total_distance)
print("s5 Fitness:", best_fitness)

end_time = time.time()
print("s5 Execution Time:", end_time - start_time, "seconds")






