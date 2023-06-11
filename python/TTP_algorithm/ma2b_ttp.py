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


class MA2B:
    def __init__(self, distance_matrix, item_values, item_weights, knapsack_capacity):
        self.distance_matrix = distance_matrix
        self.item_values = item_values
        self.item_weights = item_weights
        self.knapsack_capacity = knapsack_capacity

    def tsp_solver(self):
        num_cities = len(self.distance_matrix)
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
                    new_distance = self.calculate_distance(new_solution)
                    if new_distance < self.calculate_distance(tsp_solution):
                        tsp_solution = new_solution
                        improved = True

        return tsp_solution

    def kp_solver(self):
        num_items = len(self.item_values)
        current_solution = [random.randint(0, 1) for _ in range(num_items)]
        current_fitness = self.calculate_fitness(current_solution)

        best_solution = current_solution[:]
        best_fitness = current_fitness

        iterations = 100

        for _ in range(iterations):
            new_solution = current_solution[:]
            random_index = random.randint(0, num_items - 1)
            new_solution[random_index] = 1 - new_solution[random_index]  # Bit-flip mutation

            new_fitness = self.calculate_fitness(new_solution)

            if new_fitness > best_fitness:
                best_solution = new_solution[:]
                best_fitness = new_fitness

        return best_solution

    def calculate_distance(self, solution):
        distance = 0
        num_cities = len(solution)
        for i in range(num_cities):
            city1 = solution[i]
            city2 = solution[(i + 1) % num_cities]
            distance += self.distance_matrix[city1][city2]
        return distance

    def calculate_fitness(self, solution):
        fitness = 0
        total_weight = 0
        for i in range(len(solution)):
            if solution[i] == 1:
                fitness += self.item_values[i]
                total_weight += self.item_weights[i]
                if total_weight > self.knapsack_capacity:
                    return 0
        return fitness

    def ma2b_algorithm(self):
        tsp_solution = self.tsp_solver()
        kp_solution = self.kp_solver()

        tsp_fitness = self.calculate_distance(tsp_solution)
        kp_fitness = self.calculate_fitness(kp_solution)
        total_fitness = tsp_fitness + kp_fitness
        print(tsp_solution, kp_solution, total_fitness)
        return tsp_solution, kp_solution, total_fitness
