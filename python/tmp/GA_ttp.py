import itertools

def tsp_solver(distance_matrix):
    num_cities = len(distance_matrix)
    cities = list(range(num_cities))
    shortest_distance = float('inf')
    best_path = None

    for path in itertools.permutations(cities):
        total_distance = 0
        for i in range(num_cities):
            city1 = path[i]
            city2 = path[(i + 1) % num_cities]
            total_distance += distance_matrix[city1][city2]

        if total_distance < shortest_distance:
            shortest_distance = total_distance
            best_path = path

    return best_path, shortest_distance

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
best_path, shortest_distance = tsp_solver(distance_matrix)

print("Best TSP Path:", best_path)
print("Shortest Distance:", shortest_distance)
