import random
import copy
import math

# TSP solver using 2-OPT hill climber
def tsp_solver(distance_matrix):
    num_cities = len(distance_matrix)
    tsp_solution = list(range(num_cities))
    improved = True

    while improved:
        improved = False
        for i in range(1, num_cities - 2):
            for j in range(i + 1, num_cities):
                if j - i == 1:
                    continue
                new_solution = tsp_solution[:]
                new_solution[i:j] = tsp_solution[j - 1:i - 1:-1]
                new_distance = calculate_distance(new_solution, distance_matrix)
                if new_distance < calculate_distance(tsp_solution, distance_matrix):
                    tsp_solution = new_solution
                    improved = True

    return tsp_solution


# KP solver using Simulated Annealing
def kp_solver(item_values, item_weights, knapsack_capacity):
    num_items = len(item_values)
    current_solution = [random.randint(0, 1) for _ in range(num_items)]
    current_fitness = calculate_fitness(current_solution, item_values, item_weights, knapsack_capacity)

    best_solution = current_solution[:]
    best_fitness = current_fitness

    temperature = 100.0
    cooling_rate = 0.01

    while temperature > 0.1:
        new_solution = current_solution[:]
        random_index = random.randint(0, num_items - 1)
        new_solution[random_index] = 1 - new_solution[random_index]  # Bit-flip

        new_fitness = calculate_fitness(new_solution, item_values, item_weights, knapsack_capacity)

        if accept_solution(current_fitness, new_fitness, temperature):
            current_solution = new_solution[:]
            current_fitness = new_fitness

        if new_fitness > best_fitness:
            best_solution = new_solution[:]
            best_fitness = new_fitness

        temperature *= 1 - cooling_rate

    return best_solution


# Helper functions for fitness calculation and acceptance probability
def calculate_distance(solution, distance_matrix):
    distance = 0
    num_cities = len(solution)
    for i in range(num_cities):
        city1 = solution[i]
        city2 = solution[(i + 1) % num_cities]
        distance += distance_matrix[city1][city2]
    return distance


def calculate_fitness(solution, item_values, item_weights, knapsack_capacity):
    fitness = 0
    total_weight = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            fitness += item_values[i]
            total_weight += item_weights[i]
            if total_weight > knapsack_capacity:
                return 0
    return fitness


def accept_solution(current_fitness, new_fitness, temperature):
    if new_fitness > current_fitness:
        return True
    else:
        acceptance_probability = math.exp((new_fitness - current_fitness) / temperature)
        return random.random() < acceptance_probability


# CS2SA algorithm
def cs2sa_algorithm(distance_matrix, item_values, item_weights, knapsack_capacity):
    num_cities = len(distance_matrix)
    num_items = len(item_values)
    tsp_solution = tsp_solver(distance_matrix)
    kp_solution = kp_solver(item_values, item_weights, knapsack_capacity)

    best_tsp_solution = tsp_solution[:]
    best_kp_solution = kp_solution[:]
    best_fitness = calculate_fitness(best_kp_solution, item_values, item_weights, knapsack_capacity)

    iterations = 100

    for _ in range(iterations):
        tsp_solution = tsp_solver(distance_matrix)
        kp_solution = kp_solver(item_values, item_weights, knapsack_capacity)

        tsp_fitness = calculate_distance(tsp_solution, distance_matrix)
        kp_fitness = calculate_fitness(kp_solution, item_values, item_weights, knapsack_capacity)

        if tsp_fitness + kp_fitness > best_fitness:
            best_tsp_solution = tsp_solution[:]
            best_kp_solution = kp_solution[:]
            best_fitness = tsp_fitness + kp_fitness

    return best_tsp_solution, best_kp_solution, best_fitness


# Example usage
distance_matrix = [
    [0, 2, 9, 10],
    [2, 0, 6, 4],
    [9, 6, 0, 8],
    [10, 4, 8, 0]
]
item_values = [2, 4, 6, 8]
item_weights = [1, 2, 3, 4]
knapsack_capacity = 7

best_tsp_solution, best_kp_solution, best_fitness = cs2sa_algorithm(distance_matrix, item_values, item_weights,
                                                                   knapsack_capacity)

print("Best TSP Solution:", best_tsp_solution)
print("Best KP Solution:", best_kp_solution)
print("Total Fitness:", best_fitness)
