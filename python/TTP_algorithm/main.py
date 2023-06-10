from matls_ttp import MATLS
from ma2b_ttp import MA2B
from coGA_ttp import CoGA
from s5_ttp import S5
import numpy as np

# TTP 문제에 대한 예시 실행
distance_matrix = np.array([
    [0, 2, 9, 10],
    [2, 0, 6, 4],
    [9, 6, 0, 8],
    [10, 4, 8, 0]
])

item_values = [2, 4, 6, 8]
item_weights = [1, 2, 3, 4]
knapsack_capacity = 7
num_agents = 50
num_generations = 100

population_size = 50
elite_size = 5





# MATLS Algorithm
matls = MATLS(distance_matrix, item_values, item_weights, knapsack_capacity, num_agents, num_generations)
matls.run()

best_agent = matls.get_best_solution()
best_fitness = best_agent.fitness

print("MATLS Algorithm")
print("Best Individual (TSP Genome):", best_agent.tsp_genome)
print("Best Individual (KP Genome):", best_agent.kp_genome)
print("Total Fitness:", best_fitness)

# MA2B Algorithm
ma2b = MA2B(distance_matrix, item_values, item_weights, knapsack_capacity)
tsp_solution, kp_solution, total_fitness = ma2b.ma2b_algorithm()

print("\nMA2B Algorithm")
print("TSP Solution:", tsp_solution)
print("KP Solution:", kp_solution)
print("Total Fitness:", total_fitness)


# s5 Algorithm
s5 = S5(distance_matrix, item_values, item_weights, knapsack_capacity)
best_tsp_solution, best_kp_solution, best_fitness = s5.s5_algorithm(num_agents=50, num_generations=100)

print("\nS5 Algorithm")
print("Best TSP Solution:", best_tsp_solution)
print("Best KP Solution:", best_kp_solution)
print("Total Fitness:", best_fitness)


# Co-evolution Algorithm
coga = CoGA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size, num_generations)
best_individual, ttp_fitness = coga.solve_ttp_problem()

print("\nCo-evolution Algorithm")
print("Best Individual (TSP Genome):", best_individual['tsp_genome'])
print("Best Individual (KP Genome):", best_individual['kp_genome'])
print("TTP Fitness:", ttp_fitness)
