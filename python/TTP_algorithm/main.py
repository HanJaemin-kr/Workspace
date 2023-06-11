#from matls_ttp import MATLS
from ma2b_ttp import MA2B
from coGA_ttp import CoGA
from s5_ttp import S5
from bruteforce_ttp import BRUTE
import numpy as np
import numpy as np
from itertools import permutations

def calculate_distance(path, distance_matrix):
    total_distance = 0
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        total_distance += distance_matrix[start][end]
    return total_distance

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

# TTP problem example
distance_matrix = [
 [0, 2, 5, 9],
 [2, 0, 4, 8],
 [5, 4, 0, 6],
 [9, 8, 6, 0],]
item_values = [4, 6, 8, 2]
item_weights = [1, 2, 3, 2]
knapsack_capacity = 4

# co-EA
population_size = 10
elite_size = 0.2
num_generations = 30

num_agents = 50


# Co-evolution Algorithm
coga = CoGA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size, num_generations)
best_individual, ttp_fitness = coga.solve_ttp_problem()

print("\n=======Co-evolution Algorithm=======")
print("Best Individual (TSP Genome):", best_individual['tsp_genome'])
print("Best Individual (KP Genome):", best_individual['kp_genome'])

print("\nSelected Knapsack Weights:", sum([item_weights[i] for i in range(len(best_individual['kp_genome'])) if best_individual['kp_genome'][i] == 1]))
print("Total Item Value:", sum([item_values[i] for i in range(len(best_individual['kp_genome'])) if best_individual['kp_genome'][i] == 1]))
print("Distance:", ttp_fitness)
print(" == > Total Fitness:", ttp_fitness)

# brute-force Algorithm
brute = BRUTE(distance_matrix, item_values, item_weights, knapsack_capacity)
best_tsp_genome, best_kp_genome, best_fitness = brute.solve_ttp_brute_force()

print("\n=======Brute-force Algorithm=======")
print("TSP Solution:", best_tsp_genome)
print("KP Solution:", best_kp_genome)

print("\nSelected Knapsack Weights:", sum([item_weights[i] for i in range(len(best_kp_genome)) if best_kp_genome[i] == 1]))
print("Total Item Value:", sum([item_values[i] for i in range(len(best_kp_genome)) if best_kp_genome[i] == 1]))
print("Distance:", best_fitness)
print(" == > Total Fitness:", best_fitness)
"""
print('///////////')
print('가방 용령 =',knapsack_capacity)
print('///////////')
# MATLS Algorithm
#matls = MATLS(distance_matrix, item_values, item_weights, knapsack_capacity, num_agents, num_generations)
#matls.run()

#best_agent = matls.get_best_solution()
#best_fitness = best_agent.fitness

#print("=======MATLS Algorithm=======")
#print("Best Individual (TSP Genome):", best_agent.tsp_genome)
#print("Best Individual (KP Genome):", best_agent.kp_genome)
#print("Total Fitness:", best_fitness)
#print("Selected Knapsack Weights:", sum([item_weights[i] for i in range(len(best_agent.kp_genome)) if best_agent.kp_genome[i] == 1]))
#print("Total Item Value:", sum([item_values[i] for i in range(len(best_agent.kp_genome)) if best_agent.kp_genome[i] == 1]))
#print("Distance:", best_fitness)

# MA2B Algorithm
ma2b = MA2B(distance_matrix, item_values, item_weights, knapsack_capacity)
tsp_solution, kp_solution, total_fitness = ma2b.ma2b_algorithm()

print("\n=======MA2B Algorithm=======")
print("TSP Solution:", tsp_solution)
#print("KP Solution:", kp_solution)
#print("Total Fitness:", total_fitness)
print("Selected Knapsack Weights:", sum([item_weights[i] for i in range(len(kp_solution)) if kp_solution[i] == 1]))
print("Total Item Value:", sum([item_values[i] for i in range(len(kp_solution)) if kp_solution[i] == 1]))
print("Distance:", total_fitness)

# s5 Algorithm
s5 = S5(distance_matrix, item_values, item_weights, knapsack_capacity)
best_tsp_solution, best_kp_solution, best_fitness = s5.s5_algorithm(num_agents=50, num_generations=100)

print("\n=======S5 Algorithm=======")
print("Best TSP Solution:", best_tsp_solution)
#print("Best KP Solution:", best_kp_solution)
#print("Total Fitness:", best_fitness)
print("Selected Knapsack Weights:", sum([item_weights[i] for i in range(len(best_kp_solution)) if best_kp_solution[i] == 1]))
print("Total Item Value:", sum([item_values[i] for i in range(len(best_kp_solution)) if best_kp_solution[i] == 1]))
print("Distance:", best_fitness)

# Co-evolution Algorithm
coga = CoGA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size, num_generations)
best_individual, ttp_fitness = coga.solve_ttp_problem()

print("\n=======Co-evolution Algorithm=======")
print("Best Individual (TSP Genome):", best_individual['tsp_genome'])
#print("Best Individual (KP Genome):", best_individual['kp_genome'])
#print("Total Fitness:", ttp_fitness)
print("Selected Knapsack Weights:", sum([item_weights[i] for i in range(len(best_individual['kp_genome'])) if best_individual['kp_genome'][i] == 1]))
print("Total Item Value:", sum([item_values[i] for i in range(len(best_individual['kp_genome'])) if best_individual['kp_genome'][i] == 1]))
print("Distance:", ttp_fitness)

# Brute-force Algorithm
brute = BRUTE(distance_matrix, item_values, item_weights, knapsack_capacity)
best_tsp_genome, best_kp_genome, best_fitness = brute.solve_ttp_brute_force()

print("\n=======Brute-force Algorithm=======")
print("TSP Solution:", best_tsp_genome)
#print("KP Solution:", best_kp_genome)
#print("Total Fitness:", best_fitness)
print("Selected Knapsack Weights:", sum([item_weights[i] for i in range(len(best_kp_genome)) if best_kp_genome[i] == 1]))
print("Total Item Value:", sum([item_values[i] for i in range(len(best_kp_genome)) if best_kp_genome[i] == 1]))
print("Distance:", best_fitness)

print("\n\n\n\n")

# MA2B Algorithm
ma2b_path = [0, 1, 2, 3]
ma2b_distance = calculate_distance(ma2b_path, distance_matrix)
print("MA2B Algorithm")
print("TSP Solution:", ma2b_path)
print("Distance:", ma2b_distance)

# S5 Algorithm
s5_path = [1, 2, 0, 3]
s5_distance = calculate_distance(s5_path, distance_matrix)
print("\nS5 Algorithm")
print("Best TSP Solution:", s5_path)
print("Distance:", s5_distance)

# Co-evolution Algorithm
coevolution_path = [1, 3, 2, 0]
coevolution_distance = calculate_distance(coevolution_path, distance_matrix)
print("\nCo-evolution Algorithm")
print("Best Individual (TSP Genome):", coevolution_path)
print("Distance:", coevolution_distance)

# Brute-force Algorithm
brute_force_path, brute_force_distance = calculate_brute_force(distance_matrix)
print("\nBrute-force Algorithm")
print("TSP Solution:", brute_force_path)
print("Distance:", brute_force_distance)

#/usr/local/bin/python3.9 /Users/hanjaemin/Desktop/Workspace/python/TTP_algorithm/test.py
#Best tour: (0, 1, 3, 2)
#Max profit: 14\\



TSP 피트니스는 총 이동 거리를 최소화하는 측면에서 개인의 TSP 게놈(도시 순서)이 얼마나 잘 수행되는지를 측정합니다. 
KP 적합도는 개인의 KP 게놈(항목 선택)이 배낭 용량을 초과하지 않으면서 선택된 항목의 총 가치를 최대화하는 측면에서 얼마나 잘 수행되는지를 평가합니다.

따라서 "최선의 솔루션" 또는 "최적의 솔루션"에 대한 판단은 모집단에서 개인이 달성한 가장 높은 전체 적합성을 기반으로 합니다. 
코드는 적합도가 가장 높은 개인을 최상의 솔루션으로 선택하여 TSP 및 KP 적합도 측면에서 모두 최고를 수행했음을 나타냅니다.
"""