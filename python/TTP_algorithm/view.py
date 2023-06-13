import numpy as np
import matplotlib.pyplot as plt

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

# 매트릭스 크기 입력 받기
size = int(input("매트릭스 크기를 입력하세요: "))

# TSP 그래프 매트릭스 생성
tsp_graph = create_tsp_graph_matrix(size)

print("TSP 그래프 매트릭스:")
print(tsp_graph)




"""
# Data for brute force algorithm
brute_tsp_ls = [10, 20, 30, 40, 50]
brute_kp_ls = [15, 25, 35, 45, 55]
brute_time_ls = [0.5, 0.6, 0.7, 0.8, 0.9]
brute_fitness_ls = [0.3, 0.4, 0.5, 0.6, 0.7]

# Data for genetic algorithm (COGA)
coga_tsp_ls = [20, 30, 40, 50, 60]
coga_kp_ls = [25, 35, 45, 55, 65]
coga_time_ls = [0.6, 0.7, 0.8, 0.9, 1.0]
coga_fitness_ls = [0.4, 0.5, 0.6, 0.7, 0.8]

# Data for simulated annealing algorithm (CS2SA)
cs2sa_tsp_ls = [15, 25, 35, 45, 55]
cs2sa_kp_ls = [20, 30, 40, 50, 60]
cs2sa_time_ls = [0.7, 0.8, 0.9, 1.0, 1.1]
cs2sa_fitness_ls = [0.5, 0.6, 0.7, 0.8, 0.9]

# Data for multi-agent two-body algorithm (MA2B)
ma2b_tsp_ls = [25, 35, 45, 55, 65]
ma2b_kp_ls = [30, 40, 50, 60, 70]
ma2b_time_ls = [0.8, 0.9, 1.0, 1.1, 1.2]
ma2b_fitness_ls = [0.6, 0.7, 0.8, 0.9, 1.0]

# Plotting the data
x = [10, 20, 30, 40, 50]  # Assuming x-axis values

# Plotting TSP results
plt.figure(figsize=(10, 6))
plt.plot(x, brute_tsp_ls, marker='o', label='Brute Force')
plt.plot(x, coga_tsp_ls, marker='o', label='COGA')
plt.plot(x, cs2sa_tsp_ls, marker='o', label='CS2SA')
plt.plot(x, ma2b_tsp_ls, marker='o', label='MA2B')
plt.xlabel('Input Size')
plt.ylabel('TSP Result')
plt.title('TSP Results Comparison')
plt.legend()
plt.grid(True)
plt.show()

# Plotting Knapsack results
plt.figure(figsize=(10, 6))
plt.plot(x, brute_kp_ls, marker='o', label='Brute Force')
plt.plot(x, coga_kp_ls, marker='o', label='COGA')
plt.plot(x, cs2sa_kp_ls, marker='o', label='CS2SA')
plt.plot(x, ma2b_kp_ls, marker='o', label='MA2B')
plt.xlabel('Input Size')
plt.ylabel('Knapsack Result')
plt.title('Knapsack Results Comparison')
plt.legend()
plt.grid(True)
plt.show()

# Plotting Execution Time
plt.figure(figsize=(10, 6))
plt.plot(x, brute_time_ls, marker='o', label='Brute Force')
plt.plot(x, coga_time_ls, marker='o', label='COGA')
plt.plot(x, cs2sa_time_ls, marker='o', label='CS2SA')
plt.plot(x, ma2b_time_ls, marker='o', label='MA2B')
plt.xlabel('Input Size')
plt.ylabel('Execution Time (s)')
plt.title('Execution Time Comparison')
plt.legend()
plt.grid(True)
plt.show()

# Plotting Fitness
plt.figure(figsize=(10, 6))
plt.plot(x, brute_fitness_ls, marker='o', label='Brute Force')
plt.plot(x, coga_fitness_ls, marker='o', label='COGA')
plt.plot(x, cs2sa_fitness_ls, marker='o', label='CS2SA')
plt.plot(x, ma2b_fitness_ls, marker='o', label='MA2B')
plt.xlabel('Input Size')
plt.ylabel('Fitness')
plt.title('Fitness Comparison')
plt.legend()
plt.grid(True)
plt.show()
"""