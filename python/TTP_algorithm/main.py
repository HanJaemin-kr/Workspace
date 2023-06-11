#from matls_ttp import MATLS
from ma2b_ttp import MA2B
from coGA_ttp import CoGA
from s5_ttp import S5
from bruteforce_ttp import BRUTE
import numpy as np
import numpy as np
from itertools import permutations
from GA_ttp import GA
import time

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

# ================ co-EA ================
population_size = 1000
elite_size = 0.2
num_generations = 50
num_agents = 1

# 타이머 1 시작
start_time = time.time()
brute = BRUTE(distance_matrix, item_values, item_weights, knapsack_capacity)
best_tsp_genome, best_kp_genome, best_fitness = brute.solve_ttp_brute_force()
end_time = time.time()
# 타이머 1 종료 후 출력
print("Brute Force Execution Time:", end_time - start_time, "seconds")

# 타이머 2 시작
start_time = time.time()
coga = CoGA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size, num_generations)
best_individual, ttp_fitness = coga.solve_ttp_problem()
end_time = time.time()
# 타이머 2 종료 후 출력
print("Co-EA Execution Time:", end_time - start_time, "seconds")

# 타이머 3 시작
start_time = time.time()
ga = GA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size, num_generations)
best_individual, ttp_fitness = ga.solve_ttp_problem()
end_time = time.time()
# 타이머 3 종료 후 출력
print("GA Execution Time:", end_time - start_time, "seconds")