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

        for tsp_genome in itertools.permutations(range(num_cities)):
            for kp_genome in itertools.product([0, 1], repeat=num_items):
                tsp_fitness = self.evaluate_tsp(list(tsp_genome))
                kp_fitness = self.evaluate_kp(list(kp_genome))
                ttp_fitness = tsp_fitness + kp_fitness

                if ttp_fitness > best_fitness:
                    best_tsp_genome = list(tsp_genome)
                    best_kp_genome = list(kp_genome)
                    best_fitness = ttp_fitness

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