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

    def generate_tsp_genome(self, num_cities):
        genome = list(range(num_cities))
        random.shuffle(genome)
        return genome

    def generate_kp_genome(self, num_items):
        genome = []
        for _ in range(num_items):
            genome.append(random.randint(0, 1))
        return genome

    def initialize_population(self, num_cities, num_items):
        population = []
        for _ in range(self.population_size):
            tsp_genome = self.generate_tsp_genome(num_cities)
            kp_genome = self.generate_kp_genome(num_items)
            individual = {'tsp_genome': tsp_genome, 'kp_genome': kp_genome}
            population.append(individual)
        return population

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

    def evaluate_population(self, population):
        fitness_scores = []
        for individual in population:
            tsp_genome = individual['tsp_genome']
            kp_genome = individual['kp_genome']

            tsp_fitness = self.evaluate_tsp(tsp_genome)
            kp_fitness = self.evaluate_kp(kp_genome)

            fitness_score = tsp_fitness + kp_fitness
            fitness_scores.append(fitness_score)

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

        tsp_crossover_point = random.randint(1, len(tsp_genome1) - 1)
        kp_crossover_point = random.randint(1, len(kp_genome1) - 1)

        tsp_child_genome = tsp_genome1[:tsp_crossover_point] + tsp_genome2[tsp_crossover_point:]
        kp_child_genome = kp_genome1[:kp_crossover_point] + kp_genome2[kp_crossover_point:]

        child = {'tsp_genome': tsp_child_genome, 'kp_genome': kp_child_genome}
        return child

    def mutate(self, child):
        tsp_genome = child['tsp_genome']
        kp_genome = child['kp_genome']

        tsp_mutation_point = random.randint(0, len(tsp_genome) - 1)
        tsp_genome[tsp_mutation_point] = random.choice(tsp_genome)

        kp_mutation_point = random.randint(0, len(kp_genome) - 1)
        kp_genome[kp_mutation_point] = 1 - kp_genome[kp_mutation_point]

    def evaluate_ttp(self, genome):
        tsp_fitness = 0
        num_cities = len(genome)
        for i in range(num_cities):
            city1 = genome[i] - 1
            city2 = genome[(i + 1) % num_cities] - 1
            tsp_fitness += self.distance_matrix[city1][city2]

        kp_fitness = 0
        total_weight = 0
        for i in range(len(genome)):
            if genome[i] == 1:
                kp_fitness += self.item_values[i]
                total_weight += self.item_weights[i]
                if total_weight > self.knapsack_capacity:
                    kp_fitness = 0
                    break

        ttp_fitness = tsp_fitness + kp_fitness
        return ttp_fitness

    def solve_ttp_problem(self):
        num_cities = len(self.distance_matrix)
        num_items = len(self.item_values)

        # 초기 개체 집단 생성
        population = self.initialize_population(num_cities, num_items)

        for _ in range(self.num_generations):
            # 개체 집단의 적합도 계산
            fitness_scores = self.evaluate_population(population)

            # 협력 과정 수행하여 새로운 개체 집단 생성
            new_population = []

            # 우수한 개체들을 그대로 유지
            elite_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k], reverse=True)[
                            :self.elite_size]
            for elite_index in elite_indices:
                new_population.append(population[elite_index])

            # 나머지 개체들을 생성
            while len(new_population) < len(population):
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)

            population = new_population

        # 최종 개체 집단에서 가장 우수한 개체 선택
        best_individual = max(population, key=lambda x: self.evaluate_population([x])[0])

        # Best Individual의 적합도 계산
        ttp_fitness = self.evaluate_ttp(best_individual['tsp_genome'])

        return best_individual, ttp_fitness

"""
# TTP 문제에 대한 예시 실행
distance_matrix = [
    [0, 2, 9, 10],
    [2, 0, 6, 4],
    [9, 6, 0, 8],
    [10, 4, 8, 0]
]
item_values = [2, 4, 6, 8]
item_weights = [1, 2, 3, 4]
knapsack_capacity = 7
population_size = 50
elite_size = 5
num_generations = 100

coga = CoGA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size,
            num_generations)
best_individual, ttp_fitness = coga.solve_ttp_problem()

print("Best Individual:", best_individual)
print("TTP Fitness:", ttp_fitness)
"""