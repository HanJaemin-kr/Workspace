import itertools

class BRUTE:
    def __init__(self, distance_matrix, item_values, item_weights, knapsack_capacity):
        self.distance_matrix = distance_matrix
        self.item_values = item_values
        self.item_weights = item_weights
        self.knapsack_capacity = knapsack_capacity

    def calculate_total_distance(self, tsp_solution):
        total_distance = 0
        num_cities = len(tsp_solution)
        for i in range(num_cities):
            city1 = tsp_solution[i] - 1  # Adjust index to match the distance matrix
            city2 = tsp_solution[(i + 1) % num_cities] - 1
            total_distance += self.distance_matrix[city1][city2]
        return total_distance

    def solve_ttp_brute_force(self):
        num_cities = len(self.distance_matrix)
        num_items = len(self.item_values)

        best_tsp_solution = None
        best_kp_solution = None
        best_fitness = float('-inf')

        for tsp_solution in itertools.permutations(range(1, num_cities + 1), num_cities):
            for kp_solution in itertools.product([0, 1], repeat=num_items):
                tsp_fitness = self.calculate_total_distance(tsp_solution)
                kp_fitness = self.calculate_kp_fitness(kp_solution)
                ttp_fitness = kp_fitness / tsp_fitness

                if ttp_fitness > best_fitness:
                    best_tsp_solution = tsp_solution
                    best_kp_solution = kp_solution
                    best_fitness = ttp_fitness

        return best_tsp_solution, best_kp_solution, best_fitness

    def calculate_kp_fitness(self, kp_solution):
        total_weight = 0
        total_value = 0
        for i in range(len(kp_solution)):
            if kp_solution[i] == 1:
                total_weight += self.item_weights[i]
                total_value += self.item_values[i]
                if total_weight > self.knapsack_capacity:
                    return 0
        return total_value
