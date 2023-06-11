import random
import numpy as np

class Agent:
    def __init__(self, num_cities, num_items):
        self.tabu_list = []
        self.tsp_genome = self.generate_tsp_genome(num_cities)
        self.kp_genome = self.generate_kp_genome(num_items)
        self.fitness = None

    def run(self, distance_matrix, item_values, item_weights, knapsack_capacity):
        self._fitness(distance_matrix, item_values, item_weights, knapsack_capacity)

    def _fitness(self, distance_matrix, item_values, item_weights, knapsack_capacity):
        tsp_fitness = self._evaluate_tsp(distance_matrix)
        kp_fitness = self._evaluate_kp(item_values, item_weights, knapsack_capacity)
        self.fitness = tsp_fitness + kp_fitness

    def generate_tsp_genome(self, num_cities):
        genome = []
        for _ in range(num_cities):
            available_cities = [city for city in range(num_cities) if city not in self.tabu_list]
            if not available_cities:
                raise Exception("No available cities to select from.")
            selected_city = random.choice(available_cities)
            genome.append(selected_city)
            self.tabu_list.append(selected_city)
        return genome

    def generate_kp_genome(self, num_items):
        genome = []
        for _ in range(num_items):
            genome.append(random.randint(0, 1))
        return genome

    def _evaluate_tsp(self, distance_matrix):
        tsp_fitness = 0
        num_cities = len(self.tsp_genome)
        for i in range(num_cities):
            city1 = self.tsp_genome[i]
            city2 = self.tsp_genome[(i + 1) % num_cities]
            tsp_fitness += distance_matrix[city1][city2]
        return tsp_fitness

    def _evaluate_kp(self, item_values, item_weights, knapsack_capacity):
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
    def __init__(self, num_agents, num_generations):
        self.distance_matrix = None
        self.item_values = None
        self.item_weights = None
        self.knapsack_capacity = None
        self.num_agents = num_agents
        self.num_generations = num_generations
        self.agents = []
        self.tabu_list = []
        self.mutation_rate = 0.1
        self.elitism_rate = 0.1

    def initialize_agents(self, num_cities, num_items):
        if self.num_agents < 2:
            raise ValueError("Number of agents is less than 2.")
        self.agents = [Agent(num_cities, num_items) for _ in range(self.num_agents)]

    def evaluate_agents_fitness(self):
        for agent in self.agents:
            agent.run(self.distance_matrix, self.item_values, self.item_weights, self.knapsack_capacity)

    def select_parents(self):
        num_agents = len(self.agents)
        if num_agents < 2:
            return None, None
        participants = random.sample(self.agents, 2)
        participants = sorted(participants, key=lambda x: x.fitness, reverse=True)
        parent1 = participants[0]
        parent2 = participants[1]
        return parent1, parent2

    def crossover(self, parent1, parent2):
        if parent1 is None or parent2 is None:
            return None
        crossover_point = random.randint(0, len(parent1.tsp_genome))
        child = Agent(len(parent1.tsp_genome), len(parent1.kp_genome))
        child.tsp_genome = parent1.tsp_genome[:crossover_point] + parent2.tsp_genome[crossover_point:]
        child.kp_genome = parent1.kp_genome[:crossover_point] + parent2.kp_genome[crossover_point:]
        return child

    def mutate(self, agent):
        if agent is None:
            return
        num_cities = len(agent.tsp_genome)
        num_items = len(agent.kp_genome)

        for i in range(num_cities):
            if random.random() < self.mutation_rate:
                agent.tsp_genome[i] = random.choice([city for city in range(num_cities) if city != agent.tsp_genome[i]])

        for i in range(num_items):
            if random.random() < self.mutation_rate:
                agent.kp_genome[i] = 1 - agent.kp_genome[i]

    def select_elite_agents(self):
        num_elite_agents = int(self.elitism_rate * self.num_agents)
        elite_agents = sorted(self.agents, key=lambda x: x.fitness, reverse=True)[:num_elite_agents]
        return elite_agents


    def run(self, distance_matrix, item_values, item_weights, knapsack_capacity):
        num_cities = len(distance_matrix)
        num_items = len(item_values)

        self.distance_matrix = distance_matrix
        self.item_values = item_values
        self.item_weights = item_weights
        self.knapsack_capacity = knapsack_capacity

        self.initialize_agents(num_cities, num_items)

        for _ in range(self.num_generations):
            self.evaluate_agents_fitness()

            new_agents = []
            for _ in range(self.num_agents):
                parent1, parent2 = self.select_parents()
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_agents.append(child)

            self.agents += new_agents
            self.evaluate_agents_fitness()
            self.agents = self.select_elite_agents()

        self.evaluate_agents_fitness()

        # Get the best individual
        best_individual = max(self.agents, key=lambda x: x.fitness)
        tsp_genome = best_individual.tsp_genome
        kp_genome = best_individual.kp_genome
        total_fitness = best_individual.fitness

        # Print the best individual's TSP genome, KP genome, and total fitness
        print("Best Individual (TSP Genome):", tsp_genome)
        print("Best Individual (KP Genome):", kp_genome)
        print("Total Fitness:", total_fitness)

# Define the distance matrix, item values, item weights, and knapsack capacity

distance_matrix = np.array([[0, 2, 9, 10],
                            [1, 0, 6, 4],
                            [15, 7, 0, 8],
                            [6, 3, 12, 0]])

item_values = [10, 20, 30, 40]
item_weights = [5, 10, 15, 20]
knapsack_capacity = 30

# Create an instance of MATLS algorithm and run it
matls = MATLS(num_agents=10, num_generations=100)
matls.run(distance_matrix, item_values, item_weights, knapsack_capacity)

# Get the best individual
best_individual = max(matls.agents, key=lambda x: x.fitness)
tsp_genome = best_individual.tsp_genome
kp_genome = best_individual.kp_genome
total_fitness = best_individual.fitness

# Print the best individual's TSP genome, KP genome, and total fitness
print("Best Individual (TSP Genome):", tsp_genome)
print("Best Individual (KP Genome):", kp_genome)
print("Total Fitness:", total_fitness)
