import itertools
import random


class Agent:
    def __init__(self, num_cities, num_items):
        self.tsp_genome = self.generate_tsp_genome(num_cities)
        self.kp_genome = self.generate_kp_genome(num_items)
        self.fitness = None

    def generate_tsp_genome(self, num_cities):
        genome = list(range(num_cities))
        random.shuffle(genome)
        return genome

    def generate_kp_genome(self, num_items):
        genome = []
        for _ in range(num_items):
            genome.append(random.randint(0, 1))
        return genome


class BRUTE:
    def __init__(self, distance_matrix, item_values, item_weights, knapsack_capacity):
        self.distance_matrix = distance_matrix
        self.item_values = item_values
        self.item_weights = item_weights
        self.knapsack_capacity = knapsack_capacity

    def solve_ttp_brute_force(self):
        num_cities = len(self.distance_matrix)
        num_items = len(self.item_values)

        best_tsp_genome = None
        best_kp_genome = None
        best_fitness = float('-inf')

        for tsp_genome in itertools.permutations(range(num_cities), num_cities):
            for kp_genome in itertools.product([0, 1], repeat=num_items):
                tsp_fitness = self.evaluate_tsp(list(tsp_genome))
                kp_fitness = self.evaluate_kp(list(kp_genome))
                ttp_fitness = 0.2 * kp_fitness + 0.8 * tsp_fitness

                if ttp_fitness > best_fitness:
                    best_tsp_genome = list(tsp_genome)
                    best_kp_genome = list(kp_genome)
                    best_fitness = ttp_fitness

        print("\n==========================brute-force genetic Algorithm==========================")
        print("Best Individual (TSP Genome):", [x + 1 for x in best_tsp_genome])
        print("Best Individual (KP Genome):", best_kp_genome)
        print(" > Selected Knapsack Weights:", sum([self.item_weights[i] for i in range(len(best_kp_genome)) if best_kp_genome[i] == 1]))
        selected_values = sum([self.item_values[i] for i in range(len(best_kp_genome)) if best_kp_genome[i] == 1])
        print(" > Total Item Value:", selected_values)

        total_distance = 0
        for i in range(len(best_tsp_genome)):
            city1 = best_tsp_genome[i] - 1
            city2 = best_tsp_genome[(i + 1) % len(best_tsp_genome)] - 1
            total_distance += self.distance_matrix[city1][city2]
        print(" > Total Distance:", total_distance)
        print("===> Fitness:", best_fitness)

        return best_tsp_genome, best_kp_genome, best_fitness

    def evaluate_tsp(self, genome):
        tsp_fitness = 0
        num_cities = len(genome)
        for i in range(num_cities):
            city1 = genome[i]
            city2 = genome[(i + 1) % num_cities]
            tsp_fitness += self.distance_matrix[city1][city2]
        return tsp_fitness

    def evaluate_kp(self, genome):
        kp_fitness = 0
        total_weight = 0
        for i in range(len(genome)):
            if genome[i] == 1:
                kp_fitness += self.item_values[i]
                total_weight += self.item_weights[i]
                if total_weight > self.knapsack_capacity:
                    return 0
        return kp_fitness

"""
# 예시 문제 데이터
distance_matrix = [[0, 2, 5, 9, 10],
                   [2, 0, 4, 8, 9],
                   [5, 4, 0, 6, 7],
                   [9, 8, 6, 0, 3],
                   [10, 9, 7, 3, 0]]
item_values = [4, 6, 8, 2, 5]
item_weights = [1, 2, 3, 2, 1]
knapsack_capacity = 6

brute = BRUTE(distance_matrix, item_values, item_weights, knapsack_capacity)
best_tsp_genome, best_kp_genome, best_fitness = brute.solve_ttp_brute_force()

# 출력
print("\n=======brute-force Algorithm=======")
print("Best Individual (TSP Genome):", best_tsp_genome)
print("Best Individual (KP Genome):", best_kp_genome)
print("Total Fitness:", best_fitness)

selected_weights = sum([item_weights[i] for i in range(len(best_kp_genome)) if best_kp_genome[i] == 1])
selected_values = sum([item_values[i] for i in range(len(best_kp_genome)) if best_kp_genome[i] == 1])
print("\nSelected Knapsack Weights:", selected_weights)

total_distance = 0
for i in range(len(best_tsp_genome)):
    city1 = best_tsp_genome[i] - 1
    city2 = best_tsp_genome[(i + 1) % len(best_tsp_genome)] - 1
    total_distance += distance_matrix[city1][city2]
print("Total Distance:", total_distance)
print(" ===> Fitness:", best_fitness)
"""