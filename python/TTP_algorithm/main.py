from python.TTP_algorithm.ma2b_ttp import MA2B
from coGA_ttp import CoGA
from cs2sa_ttp import CS2SA
from bruteforce_ttp import BRUTE

import random
import json
import time
import numpy as np

def create_tsp_graph_matrix(size):
    graph = np.random.randint(1, 10, size=(size, size))  # 임의의 그래프 매트릭스 생성
    np.fill_diagonal(graph, 0)  # 대각선 요소는 0으로 설정

    # 모든 노드 간의 거리를 동일하게 만듦
    for i in range(size):
        for j in range(size):
            if i != j:
                graph[i][j] = graph[j][i]

    return graph


def print_result(result):
    for i, round_data in enumerate(result):
        round_num = i + 1
        print(f"\n=== Round {round_num} ===")
        for algorithm_data in round_data[round_num]:
            algorithm_name = list(algorithm_data.keys())[0]
            algorithm_result = algorithm_data[algorithm_name]
            print(f"{algorithm_name}:")
            print(f"Value: {algorithm_result['value']}")
            print(f"Weight: {algorithm_result['weight']}")
            print(f"Distance: {algorithm_result['distance']}")
            print(f"Fitness: {algorithm_result['fitness']}")
            print(f"Time: {algorithm_result['time']}")
            print()

def calculate_total_distance(tsp_solution, distance_matrix):
    total_distance = 0
    num_cities = len(tsp_solution)
    for i in range(num_cities):
        city1 = tsp_solution[i] - 1  # Adjust index to match the distance matrix
        city2 = tsp_solution[(i + 1) % num_cities] - 1
        total_distance += distance_matrix[city1][city2]
    return total_distance

# 초기 문제 제시
distance_matrix = [
      [0, 2, 5],
      [2, 0, 4],
      [5, 4, 0]
    ]
item_values = [4, 6, 8]
item_weights = [1, 2, 3]
knapsack_capacity = 3

# ================ ga-param ================
population_size = 1000
elite_size = 0.2
num_generations = 10
num_agents = 1
# ================================================================

brute_tsp_ls, brute_kp_ls, brute_time_ls, brute_fitness_ls = [], [], [], []
coga_tsp_ls, coga_kp_ls, coga_time_ls, coga_fitness_ls = [], [], [], []
cs2sa_tsp_ls, cs2sa_kp_ls, cs2sa_time_ls, cs2sa_fitness_ls = [], [], [], []
ma2b_tsp_ls, ma2b_kp_ls, ma2b_time_ls, ma2b_fitness_ls = [], [], [], []


result = []


for i in range(1, 7):

    result.append({i: []})
    distance_matrix = list(create_tsp_graph_matrix(i+2))
    new_value = random.randint(1, 5)
    item_values.append(new_value)
    new_weight = random.randint(1, 3)
    item_weights.append(new_weight)
    knapsack_capacity += random.randint(0, 2)
    print(distance_matrix)
    print('capacity : ',knapsack_capacity)
    print(' value ==>',item_values)
    print(' weight ==>',item_weights)
    print('\n')


    #brute-force Algorithm
    start_time = time.time()
    brute = BRUTE(distance_matrix, item_values, item_weights, knapsack_capacity)
    best_tsp_genome, best_kp_genome, best_fitness = brute.solve_ttp_brute_force()
    end_time = time.time()
    best_kp_genome = list(best_kp_genome)
    total_value = sum([item_values[i] for i in range(len(best_kp_genome)) if best_kp_genome[i] == 1])
    total_weight = sum([item_weights[i] for i in range(len(best_kp_genome)) if best_kp_genome[i] == 1])
    result[i - 1][i].append( { 'brute' : {
            "value": total_value,
            "weight": total_weight,
            "distance": calculate_total_distance(list(best_tsp_genome), distance_matrix),
            "fitness" : best_fitness,
            "time": end_time - start_time
        }
    })

    # co-ga Algorithm
    start_time = time.time()
    coga = CoGA(distance_matrix, item_values, item_weights, knapsack_capacity, population_size, elite_size, num_generations)

    best_individual, ttp_fitness, value, distance, weight = coga.solve_ttp_problem()
    end_time = time.time()
    result[i - 1][i].append( { 'coga' : {
            "value": value,
            "weight": weight,
            "distance": distance,
            "fitness" : ttp_fitness,
            "time": end_time - start_time
        }
    })


    # cs2sa
    start_time = time.time()
    cs2sa = CS2SA()
    best_tsp_solution, best_kp_solution, best_fitness, total_distance, selected_values, selected_weights = cs2sa.cs2sa_algorithm(distance_matrix, item_values, item_weights, knapsack_capacity)
    end_time = time.time()

    result[i - 1][i].append( { 'cs2sa' : {
            "value": selected_values,
            "weight": selected_weights,
            "distance": calculate_total_distance(best_tsp_solution, distance_matrix),
            "fitness" : best_fitness,
            "time": end_time - start_time
        }
    })


    # MA2B Algorithm
    start_time = time.time()
    ma2b = MA2B(distance_matrix, item_values, item_weights, knapsack_capacity)
    tsp_solution, kp_solution, total_fitness = ma2b.ma2b_algorithm()
    end_time = time.time()

    total_value = sum([item_values[i] for i in range(len(kp_solution)) if kp_solution[i] == 1])
    total_weight = sum([item_weights[i] for i in range(len(kp_solution)) if kp_solution[i] == 1])

    result[i - 1][i].append({'ma2b': {
        "value": total_value,
        "weight": total_weight,
        "distance": calculate_total_distance(tsp_solution, distance_matrix),
        "fitness": total_fitness,
        "time": end_time - start_time
    }
    })


print(print_result(result))
# 결과를 저장할 파일 경로 및 파일명
file_path = "result_2.txt"

# result 변수를 JSON 형식으로 변환
result_json = json.dumps(result)

# JSON 형식의 결과를 파일에 저장
with open(file_path, "w") as file:
    file.write(result_json)

