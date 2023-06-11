import random
import numpy as np

class PSO:
    def __init__(self, distance_matrix, item_values, item_weights, knapsack_capacity, num_particles, num_iterations,
                 inertia_weight, cognitive_weight, social_weight):
        self.distance_matrix = np.array(distance_matrix)
        self.item_values = item_values
        self.item_weights = item_weights
        self.knapsack_capacity = knapsack_capacity
        self.num_particles = num_particles
        self.num_iterations = num_iterations
        self.inertia_weight = inertia_weight
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight

        num_cities = len(distance_matrix)
        num_items = len(item_values)
        self.num_dimensions = num_cities + num_items

        self.positions = np.zeros((num_particles, self.num_dimensions))
        self.velocities = np.zeros((num_particles, self.num_dimensions))
        self.pbest_positions = np.zeros((num_particles, self.num_dimensions))
        self.pbest_fitness = np.full(num_particles, float('-inf'))
        self.gbest_position = np.zeros(self.num_dimensions)
        self.gbest_fitness = float('-inf')

        for i in range(num_particles):
            self.positions[i] = self.generate_particle_position(num_cities, num_items)
            self.velocities[i] = self.generate_particle_velocity()

    def generate_particle_position(self, num_cities, num_items):
        tsp_genome = list(range(num_cities))
        random.shuffle(tsp_genome)
        tsp_genome = np.array(tsp_genome) + 1

        kp_genome = [random.randint(0, 1) for _ in range(num_items)]
        kp_genome = np.array(kp_genome)

        return np.concatenate((tsp_genome, kp_genome))

    def generate_particle_velocity(self):
        return np.random.uniform(low=-1, high=1, size=self.num_dimensions)

    def evaluate_fitness(self, position):
        tsp_genome = position[:len(self.distance_matrix)]
        kp_genome = position[len(self.distance_matrix):]

        tsp_fitness = 0
        num_cities = len(tsp_genome)
        for i in range(num_cities):
            city1 = int(tsp_genome[i]) - 1
            city2 = int(tsp_genome[(i + 1) % num_cities]) - 1
            tsp_fitness += self.distance_matrix[city1][city2]

        kp_fitness = 0
        total_weight = 0
        for i in range(len(kp_genome)):
            if kp_genome[i] == 1:
                kp_fitness += self.item_values[i]
                total_weight += self.item_weights[i]
                if total_weight > self.knapsack_capacity:
                    kp_fitness = 0
                    break

        ttp_fitness = tsp_fitness + kp_fitness
        return ttp_fitness

    def update_particle(self, particle_index):
        position = self.positions[particle_index]
        velocity = self.velocities[particle_index]
        pbest_position = self.pbest_positions[particle_index]
        pbest_fitness = self.pbest_fitness[particle_index]

        new_velocity = (self.inertia_weight * velocity +
                        self.cognitive_weight * random.random() * (pbest_position - position) +
                        self.social_weight * random.random() * (self.gbest_position - position))

        new_position = position + new_velocity
        num_cities = len(self.distance_matrix)
        new_position = np.clip(new_position, 1, num_cities)

        # Round the city indices to the nearest integer
        new_position[:num_cities] = np.round(new_position[:num_cities])

        # Convert the city indices to integers
        new_position[:num_cities] = new_position[:num_cities].astype(int)

        ttp_fitness = self.evaluate_fitness(new_position)
        if ttp_fitness > pbest_fitness:
            self.pbest_positions[particle_index] = new_position
            self.pbest_fitness[particle_index] = ttp_fitness

        if ttp_fitness > self.gbest_fitness:
            self.gbest_position = new_position
            self.gbest_fitness = ttp_fitness

        self.positions[particle_index] = new_position
        self.velocities[particle_index] = new_velocity

    def solve_ttp_problem(self):
        num_particles = self.num_particles
        num_iterations = self.num_iterations

        for _ in range(num_iterations):
            for i in range(num_particles):
                self.update_particle(i)

        best_individual = self.gbest_position
        ttp_fitness = self.gbest_fitness

        return best_individual, ttp_fitness


# 예시 문제 데이터
distance_matrix = [[0, 2, 5, 9, 10],
                   [2, 0, 4, 8, 9],
                   [5, 4, 0, 6, 7],
                   [9, 8, 6, 0, 3],
                   [10, 9, 7, 3, 0]]
item_values = [4, 6, 8, 2, 5]
item_weights = [1, 2, 3, 2, 1]
knapsack_capacity = 6

num_particles = 100
num_iterations = 100
inertia_weight = 0.5
cognitive_weight = 1.5
social_weight = 1.5

pso = PSO(distance_matrix, item_values, item_weights, knapsack_capacity, num_particles, num_iterations,
          inertia_weight, cognitive_weight, social_weight)
best_individual, ttp_fitness = pso.solve_ttp_problem()



print("Best Individual:", best_individual)
print("TTP Fitness:", ttp_fitness)
