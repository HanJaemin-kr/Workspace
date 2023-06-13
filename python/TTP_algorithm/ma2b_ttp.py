import random

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
            new_weight = self.calculate_weight(new_solution)

            if new_fitness > best_fitness and new_weight <= self.knapsack_capacity:
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

    def calculate_weight(self, solution):
        total_weight = 0
        for i in range(len(solution)):
            if solution[i] == 1:
                total_weight += self.item_weights[i]
        return total_weight

    def ma2b_algorithm(self, num_iterations=1000):
        best_fitness = float('-inf')
        best_tsp_solution = None
        best_kp_solution = None

        for _ in range(num_iterations):
            tsp_solution = self.tsp_solver()
            kp_solution = self.kp_solver()

            tsp_fitness = self.calculate_distance(tsp_solution)
            kp_fitness = self.calculate_fitness(kp_solution)
            total_fitness = kp_fitness / tsp_fitness

            if total_fitness > best_fitness:
                best_fitness = total_fitness
                best_tsp_solution = tsp_solution
                best_kp_solution = kp_solution

        return best_tsp_solution, best_kp_solution, best_fitness

distance_matrix = [
    [0, 2, 5, 9, 10, 3, 7, 4],
    [2, 0, 4, 8, 9, 7, 6, 5],
    [5, 4, 0, 6, 7, 2, 3, 1],
    [9, 8, 6, 0, 3, 4, 9, 2],
    [10, 9, 7, 3, 0, 6, 5, 3],
    [3, 7, 2, 4, 6, 0, 8, 6],
    [7, 6, 3, 9, 5, 8, 0, 7],
    [4, 5, 1, 2, 3, 6, 7, 0]
]
item_values = [4, 6, 8, 2, 5, 3, 7, 9]
item_weights = [1, 2, 3, 2, 1, 4, 5, 3]
knapsack_capacity = 6


ma2b = MA2B(distance_matrix, item_values, item_weights, knapsack_capacity)
tsp_solution, kp_solution, total_fitness = ma2b.ma2b_algorithm()

