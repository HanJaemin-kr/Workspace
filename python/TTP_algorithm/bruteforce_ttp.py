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
        print("\n==========================brute-force genetic Algorithm==========================")
        print("Best Individual (TSP Genome):", [x + 1 for x in best_tsp_solution])
        print("Best Individual (KP Genome):", best_kp_solution)
        weight = sum([self.item_weights[i] for i in range(len(best_kp_solution)) if best_kp_solution[i] == 1])
        print(" > Selected Knapsack Weights:", weight)
        selected_values = sum([self.item_values[i] for i in range(len(best_kp_solution)) if best_kp_solution[i] == 1])
        print(" > Total Item Value:", selected_values)

        print(" > Total Distance:", self.calculate_total_distance(best_tsp_solution))
        print("===> Fitness:", selected_values / weight)

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

# 예시 문제 데이터
# distance_matrix = [[0, 2, 5, 9, 10],
#                    [2, 0, 4, 8, 9],
#                    [5, 4, 0, 6, 7],
#                    [9, 8, 6, 0, 3],
#                    [10, 9, 7, 3, 0]]
# item_values = [4, 6, 8, 2, 5]
# item_weights = [1, 2, 3, 2, 1]
# knapsack_capacity = 6
#
# brute = BRUTE(distance_matrix, item_values, item_weights, knapsack_capacity)
# best_tsp_solution, best_kp_solution, best_fitness = brute.solve_ttp_brute_force()
#
# # 출력
# print("Best Individual (TSP Solution):", best_tsp_solution)
# print("Best Individual (KP Solution):", best_kp_solution)
# print("Total Fitness:", best_fitness)


# #노드 15개
# distance_matrix = [
#     [0, 2, 5, 9, 10, 3, 7, 4, 8, 6, 3, 9, 5, 7, 2],
#     [2, 0, 4, 8, 9, 7, 6, 5, 3, 1, 2, 4, 6, 8, 3],
#     [5, 4, 0, 6, 7, 2, 3, 1, 9, 2, 5, 4, 3, 7, 1],
#     [9, 8, 6, 0, 3, 4, 9, 2, 7, 3, 8, 1, 6, 2, 4],
#     [10, 9, 7, 3, 0, 6, 5, 3, 4, 8, 1, 7, 2, 5, 6],
#     [3, 7, 2, 4, 6, 0, 8, 6, 1, 5, 2, 9, 3, 4, 7],
#     [7, 6, 3, 9, 5, 8, 0, 7, 2, 4, 7, 3, 1, 8, 2],
#     [4, 5, 1, 2, 3, 6, 7, 0, 5, 9, 1, 2, 4, 5, 3],
#     [8, 3, 9, 7, 4, 1, 2, 5, 0, 7, 4, 5, 3, 2, 9],
#     [6, 1, 2, 3, 8, 5, 4, 9, 7, 0, 3, 6, 8, 9, 2],
#     [3, 2, 5, 8, 1, 2, 7, 1, 4, 3, 0, 7, 9, 4, 6],
#     [9, 4, 4, 1, 7, 9, 3, 2, 5, 6, 7, 0, 2, 1, 4],
#     [5, 6, 3, 6, 2, 3, 1, 4, 3, 8, 9, 2, 0, 5, 3],
#     [7, 8, 7, 2, 5, 4, 8, 5, 2, 9, 4, 1, 5, 0, 7],
#     [2, 3, 1, 4, 6, 7, 2, 3, 9, 2, 6, 4, 3, 7, 0]
# ]
# item_values = [4, 6, 8, 2, 5, 3, 7, 9, 1, 6, 3, 2, 5, 7, 2, 4, 6, 8, 1, 3]
# item_weights = [1, 2, 3, 2, 1, 4, 5, 3, 2, 1, 3, 2, 4, 2, 1, 3, 2, 1, 2, 3]
# knapsack_capacity = 9