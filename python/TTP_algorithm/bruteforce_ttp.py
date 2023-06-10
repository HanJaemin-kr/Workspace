import itertools


# Brute-force 알고리즘을 사용하여 TTP 문제를 해결하는 함수
def solve_ttp_brute_force(distance_matrix, item_values, item_weights, knapsack_capacity):
    num_cities = len(distance_matrix)
    num_items = len(item_values)

    best_tsp_genome = None
    best_kp_genome = None
    best_fitness = 0

    # 모든 가능한 TSP 경로와 KP 아이템 조합에 대해 해를 생성하고 평가
    for tsp_genome in itertools.permutations(range(num_cities)):
        for kp_genome in itertools.product([0, 1], repeat=num_items):
            tsp_fitness = evaluate_tsp(list(tsp_genome), distance_matrix)
            kp_fitness = evaluate_kp(list(kp_genome), item_values, item_weights, knapsack_capacity)
            ttp_fitness = tsp_fitness + kp_fitness

            # 현재 해가 더 우수한 경우 최적해 갱신
            if ttp_fitness > best_fitness:
                best_tsp_genome = list(tsp_genome)
                best_kp_genome = list(kp_genome)
                best_fitness = ttp_fitness

    return best_tsp_genome, best_kp_genome, best_fitness


# TSP 문제의 적합도를 계산하는 함수
def evaluate_tsp(genome, distance_matrix):
    tsp_fitness = 0
    num_cities = len(genome)
    for i in range(num_cities):
        city1 = genome[i]
        city2 = genome[(i + 1) % num_cities]
        tsp_fitness += distance_matrix[city1][city2]
    return tsp_fitness


# KP 문제의 적합도를 계산하는 함수
def evaluate_kp(genome, item_values, item_weights, knapsack_capacity):
    kp_fitness = 0
    total_weight = 0
    for i in range(len(genome)):
        if genome[i] == 1:
            kp_fitness += item_values[i]
            total_weight += item_weights[i]
            if total_weight > knapsack_capacity:
                return 0
    return kp_fitness


# TTP 문제에 대한 예시 실행
distance_matrix = [
    [0, 10, 15, 20, 25],
    [10, 0, 25, 35, 40],
    [15, 25, 0, 30, 50],
    [20, 35, 30, 0, 60],
    [25, 40, 50, 60, 0]
]

item_values = [2, 4, 6, 8, 10, 12]
item_weights = [1, 2, 3, 4, 5, 6]
knapsack_capacity = 12

best_tsp_genome, best_kp_genome, best_fitness = solve_ttp_brute_force(distance_matrix, item_values, item_weights,
                                                                      knapsack_capacity)

print("Brute-force Algorithm")
print("TSP Solution:", best_tsp_genome)
print("KP Solution:", best_kp_genome)
print("Total Fitness:", best_fitness)
