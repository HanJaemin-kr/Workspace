import random


class GA:
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
        genome = {
            'tsp_genome': list(range(1, num_cities + 1)),
            'kp_genome': [random.randint(0, 1) for _ in range(num_items)]
        }
        return genome

    def initialize_population(self, num_cities, num_items):
        population = []
        for _ in range(self.population_size):
            individual = self.generate_genome(num_cities, num_items)
            population.append(individual)
        return population

    def evaluate_ttp(self, genome):
        tsp_genome = genome['tsp_genome']
        kp_genome = genome['kp_genome']

        tsp_fitness = self.calculate_tsp_fitness(tsp_genome)
        kp_fitness = self.calculate_kp_fitness(kp_genome)

        ttp_fitness = 0.2 * kp_fitness + 0.8 * tsp_fitness

        return ttp_fitness

    def calculate_tsp_fitness(self, tsp_genome):
        tsp_fitness = 0
        num_cities = len(tsp_genome)

        for i in range(num_cities):
            city1 = tsp_genome[i]
            city2 = tsp_genome[(i + 1) % num_cities]
            tsp_fitness += self.distance_matrix[city1 - 1][city2 - 1]

        return tsp_fitness

    def calculate_kp_fitness(self, kp_genome):
        kp_fitness = 0
        total_weight = 0

        for i in range(len(kp_genome)):
            if kp_genome[i] == 1:
                kp_fitness += self.item_values[i]
                total_weight += self.item_weights[i]
                if total_weight > self.knapsack_capacity:
                    kp_fitness = 0
                    break

        return kp_fitness

    def evaluate_population(self, population):
        fitness_scores = []
        for individual in population:
            fitness_scores.append(self.evaluate_ttp(individual))
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

        tsp_child_genome = self.partially_mapped_crossover(tsp_genome1, tsp_genome2)
        kp_child_genome = self.uniform_crossover(kp_genome1, kp_genome2)

        child = {
            'tsp_genome': tsp_child_genome,
            'kp_genome': kp_child_genome
        }

        return child

    def partially_mapped_crossover(self, genome1, genome2):
        tsp_child_genome = [-1] * len(genome1)

        start = random.randint(0, len(genome1) - 1)
        end = random.randint(start, len(genome1) - 1)

        tsp_child_genome[start: end + 1] = genome1[start: end + 1]

        for i in range(len(genome2)):
            if genome2[i] not in tsp_child_genome:
                for j in range(len(tsp_child_genome)):
                    if tsp_child_genome[j] == -1:
                        tsp_child_genome[j] = genome2[i]
                        break

        return tsp_child_genome

    def uniform_crossover(self, genome1, genome2):
        kp_child_genome = []
        for gene1, gene2 in zip(genome1, genome2):
            if random.random() < 0.5:
                kp_child_genome.append(gene1)
            else:
                kp_child_genome.append(gene2)
        return kp_child_genome

    def mutate(self, child, mutation_rate):
        tsp_genome = child['tsp_genome']
        kp_genome = child['kp_genome']

        for i in range(len(tsp_genome)):
            if random.random() < mutation_rate:
                tsp_genome[i] = random.choice(tsp_genome)

        for i in range(len(kp_genome)):
            if random.random() < mutation_rate:
                kp_genome[i] = 1 - kp_genome[i]

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


# 예시 문제 데이터
distance_matrix = [[0, 2, 5, 9, 10], [2, 0, 4, 8, 9], [5, 4, 0, 6, 7], [9, 8, 6, 0, 3], [10, 9, 7, 3, 0]]
item_values = [4, 6, 8, 2, 5]
item_weights = [1, 2, 3, 2, 1]
knapsack_capacity = 6

population_size = 100
elite_size = 0.2
num_generations = 100

ga = GA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size, num_generations)
best_individual, ttp_fitness = ga.solve_ttp_problem()

# 출력
print("\n=======Genetic Algorithm=======")
print("Best Individual (TSP Genome):", best_individual['tsp_genome'])
print("Best Individual (KP Genome):", best_individual['kp_genome'])
print("Total Distance:", ga.calculate_tsp_fitness(best_individual['tsp_genome']))
print("Total Item Value:", ga.calculate_kp_fitness(best_individual['kp_genome']))
print("Fitness:", ttp_fitness)
