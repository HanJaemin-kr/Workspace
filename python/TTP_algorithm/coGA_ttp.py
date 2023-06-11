import random


class CoGA:
    def __init__(self, distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size,
                 num_generations):
        self.distance_matrix = distance_matrix
        self.item_values = item_values
        self.item_weights = item_weights
        self.knapsack_capacity = knapsack_capacity
        self.population_size = population_size
        self.elite_size = elite_size
        self.num_generations = num_generations

    def generate_genome(self, num_cities, num_items):
        tsp_genome = list(range(1, num_cities + 1))
        random.shuffle(tsp_genome)

        kp_genome = []
        for _ in range(num_items):
            kp_genome.append(random.randint(0, 1))

        return {'tsp_genome': tsp_genome, 'kp_genome': kp_genome}

    def initialize_population(self, num_cities, num_items):
        population = []
        for _ in range(self.population_size):
            individual = self.generate_genome(num_cities, num_items)
            population.append(individual)
        return population

    def evaluate_ttp(self, genome):
        tsp_genome = genome['tsp_genome']
        kp_genome = genome['kp_genome']

        tsp_fitness = 0
        num_cities = len(tsp_genome)
        for i in range(num_cities):
            city1 = tsp_genome[i]
            city2 = tsp_genome[(i + 1) % num_cities]
            tsp_fitness += self.distance_matrix[city1-1][city2-1]

        kp_fitness = 0
        total_weight = 0
        for i in range(len(kp_genome)):
            if kp_genome[i] == 1:
                kp_fitness += self.item_values[i]
                total_weight += self.item_weights[i]
                if total_weight > self.knapsack_capacity:
                    kp_fitness = 0
                    break

        ttp_fitness = tsp_fitness + kp_fitness
        return ttp_fitness

    def evaluate_population(self, population):
        fitness_scores = []
        for individual in population:
            fitness = self.evaluate_ttp(individual)
            fitness_scores.append(fitness)
        return fitness_scores

    def select_parents(self, population, fitness_scores):
        total_fitness = sum(fitness_scores)
        probabilities = [fitness / total_fitness for fitness in fitness_scores]
        parent1 = random.choices(population, probabilities)[0]
        parent2 = random.choices(population, probabilities)[0]
        return parent1, parent2

    def crossover(self, parent1, parent2):
        tsp_genome1 = parent1['tsp_genome']
        tsp_genome2 = parent2['tsp_genome']
        kp_genome1 = parent1['kp_genome']
        kp_genome2 = parent2['kp_genome']

        if len(tsp_genome1) <= 1 or len(tsp_genome2) <= 1:
            return parent1

        tsp_crossover_point = random.randint(1, len(tsp_genome1) - 1)
        kp_crossover_point = random.randint(1, len(kp_genome1) - 1)

        tsp_child_genome = tsp_genome1[:tsp_crossover_point] + tsp_genome2[tsp_crossover_point:]
        tsp_child_genome = self.remove_duplicates(tsp_child_genome)  # Remove duplicate cities

        kp_child_genome = kp_genome1[:kp_crossover_point] + kp_genome2[kp_crossover_point:]

        child = {'tsp_genome': tsp_child_genome, 'kp_genome': kp_child_genome}
        return child

    def remove_duplicates(self, tsp_genome):
        visited = set()
        unique_genome = []
        for city in tsp_genome:
            if city not in visited:
                unique_genome.append(city)
                visited.add(city)
        return unique_genome


    def mutate(self, child, mutation_rate):
        tsp_genome = child['tsp_genome']
        kp_genome = child['kp_genome']

        for i in range(len(tsp_genome)):
            if random.random() < mutation_rate:
                available_cities = [city for city in range(1, len(tsp_genome) + 1) if city != tsp_genome[i]]
                if available_cities:
                    tsp_genome[i] = random.choice(available_cities)

        for i in range(len(kp_genome)):
            if random.random() < mutation_rate:
                kp_genome[i] = random.randint(0, 1)

        return child

    def evolve_population(self, population, mutation_rate):
        fitness_scores = self.evaluate_population(population)
        elite_size = int(self.elite_size * self.population_size)
        new_population = population[:elite_size]

        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents(population, fitness_scores)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child, mutation_rate)
            new_population.append(child)

        return new_population

    def solve_ttp_problem(self, mutation_rate=0.01):
        num_cities = len(self.distance_matrix)
        num_items = len(self.item_values)

        population = self.initialize_population(num_cities, num_items)

        for _ in range(self.num_generations):
            population = self.evolve_population(population, mutation_rate)

        fitness_scores = self.evaluate_population(population)
        best_index = fitness_scores.index(max(fitness_scores))
        best_individual = population[best_index]
        ttp_fitness = fitness_scores[best_index]

        return best_individual, ttp_fitness

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

population_size = 1000
elite_size = 0.2
num_generations = 300

coga = CoGA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size, num_generations)
best_individual, ttp_fitness = coga.solve_ttp_problem()
print("\n=======Co-evolution Algorithm=======")
print("Best Individual (TSP Genome):", best_individual['tsp_genome'])
print("Best Individual (KP Genome):", best_individual['kp_genome'])
print("Total Fitness:", ttp_fitness)

print("\nSelected Knapsack Weights:", sum([item_weights[i] for i in range(len(best_individual['kp_genome'])) if best_individual['kp_genome'][i] == 1]))
print("Total Item Value:", sum([item_values[i] for i in range(len(best_individual['kp_genome'])) if best_individual['kp_genome'][i] == 1]))
print("Distance:", ttp_fitness)
"""