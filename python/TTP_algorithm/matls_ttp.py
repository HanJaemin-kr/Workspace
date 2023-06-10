import random
import numpy as np

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

    def evaluate_fitness(self, distance_matrix, item_values, item_weights, knapsack_capacity):
        tsp_fitness = self.evaluate_tsp(distance_matrix)
        kp_fitness = self.evaluate_kp(item_values, item_weights, knapsack_capacity)
        self.fitness = tsp_fitness + kp_fitness

    def evaluate_tsp(self, distance_matrix):
        tsp_fitness = 0
        num_cities = len(self.tsp_genome)
        for i in range(num_cities):
            city1 = self.tsp_genome[i]
            city2 = self.tsp_genome[(i + 1) % num_cities]
            tsp_fitness += distance_matrix[city1][city2]
        return tsp_fitness

    def evaluate_kp(self, item_values, item_weights, knapsack_capacity):
        kp_fitness = 0
        total_weight = 0
        for i in range(len(self.kp_genome)):
            if self.kp_genome[i] == 1:
                kp_fitness += item_values[i]
                total_weight += item_weights[i]
                if total_weight > knapsack_capacity:
                    return 0
        return kp_fitness


class MATLS:
    def __init__(self, distance_matrix, item_values, item_weights, knapsack_capacity, num_agents, num_generations):
        self.distance_matrix = distance_matrix
        self.item_values = item_values
        self.item_weights = item_weights
        self.knapsack_capacity = knapsack_capacity
        self.num_agents = num_agents
        self.num_generations = num_generations
        self.agents = []

    def initialize_agents(self, num_cities, num_items):
        self.agents = [Agent(num_cities, num_items) for _ in range(self.num_agents)]

    def evaluate_agents_fitness(self):
        for agent in self.agents:
            agent.evaluate_fitness(self.distance_matrix, self.item_values, self.item_weights, self.knapsack_capacity)

    def run(self):
        num_cities = len(self.distance_matrix)
        num_items = len(self.item_values)
        self.initialize_agents(num_cities, num_items)
        self.evaluate_agents_fitness()

        for _ in range(self.num_generations):
            new_agents = []
            for _ in range(self.num_agents):
                parent1, parent2 = self.select_parents()
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_agents.append(child)

            self.agents += new_agents
            self.evaluate_agents_fitness()
            self.agents = self.select_elite_agents()

    def select_parents(self):
        parents = random.choices(self.agents, k=2)
        return parents

    def crossover(self, parent1, parent2):
        child = Agent(len(parent1.tsp_genome), len(parent1.kp_genome))

        tsp_crossover_point = random.randint(1, len(parent1.tsp_genome) - 1)
        kp_crossover_point = random.randint(1, len(parent1.kp_genome) - 1)

        child.tsp_genome = parent1.tsp_genome[:tsp_crossover_point] + parent2.tsp_genome[tsp_crossover_point:]
        child.kp_genome = parent1.kp_genome[:kp_crossover_point] + parent2.kp_genome[kp_crossover_point:]

        return child

    def mutate(self, agent):
        tsp_genome = agent.tsp_genome
        kp_genome = agent.kp_genome

        tsp_mutation_point = random.randint(0, len(tsp_genome) - 1)
        tsp_genome[tsp_mutation_point] = random.choice(tsp_genome)

        kp_mutation_point = random.randint(0, len(kp_genome) - 1)
        kp_genome[kp_mutation_point] = 1 - kp_genome[kp_mutation_point]

    def select_elite_agents(self):
        sorted_agents = sorted(self.agents, key=lambda x: x.fitness, reverse=True)
        elite_agents = sorted_agents[:self.num_agents]
        return elite_agents

    def get_best_solution(self):
        best_agent = max(self.agents, key=lambda x: x.fitness)
        return best_agent

"""
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

matls = MATLS(distance_matrix, item_values, item_weights, knapsack_capacity, num_agents, num_generations)
matls.run()

best_agent = matls.get_best_solution()
best_fitness = best_agent.fitness

print("Best Individual (TSP Genome):", best_agent.tsp_genome)
print("Best Individual (KP Genome):", best_agent.kp_genome)
print("Total Fitness:", best_fitness)
"""
