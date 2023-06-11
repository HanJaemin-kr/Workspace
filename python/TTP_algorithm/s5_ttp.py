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


class S5:
    def __init__(self, distance_matrix, item_values, item_weights, knapsack_capacity):
        self.distance_matrix = distance_matrix
        self.item_values = item_values
        self.item_weights = item_weights
        self.knapsack_capacity = knapsack_capacity

    def tsp_solver(self, num_cities):
        tsp_solution = list(range(num_cities))
        random.shuffle(tsp_solution)
        return tsp_solution

    def kp_solver(self, num_items):
        best_solution = [random.randint(0, 1) for _ in range(num_items)]
        best_fitness = self.calculate_fitness(best_solution)

        iterations = 100

        for _ in range(iterations):
            new_solution = best_solution[:]
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

    def s5_algorithm(self, num_agents, num_generations):
        agents = []
        for _ in range(num_agents):
            agent = Agent(len(self.distance_matrix), len(self.item_values))
            agents.append(agent)

        for _ in range(num_generations):
            for agent in agents:
                tsp_solution = self.tsp_solver(len(self.distance_matrix))
                kp_solution = self.kp_solver(len(self.item_values))

                tsp_fitness = self.calculate_distance(tsp_solution)
                kp_fitness = self.calculate_fitness(kp_solution)
                total_fitness = 0.2 * kp_fitness + 0.8 * tsp_fitness

                agent.tsp_genome = tsp_solution
                agent.kp_genome = kp_solution
                agent.fitness = total_fitness

            agents.sort(key=lambda x: x.fitness, reverse=True)

            # Elitism: Preserve top agents
            elite_agents = agents[:5]

            # Reproduction: Generate offspring
            offspring_agents = []
            for _ in range(num_agents - len(elite_agents)):
                parent1 = random.choice(agents)
                parent2 = random.choice(agents)

                tsp_offspring = parent1.tsp_genome[:]
                kp_offspring = parent2.kp_genome[:]

                offspring = Agent(len(self.distance_matrix), len(self.item_values))
                offspring.tsp_genome = tsp_offspring
                offspring.kp_genome = kp_offspring

                offspring_agents.append(offspring)

            agents = elite_agents + offspring_agents

        best_agent = agents[0]
        best_tsp_solution = best_agent.tsp_genome
        best_kp_solution = best_agent.kp_genome
        best_fitness = best_agent.fitness

        return best_tsp_solution, best_kp_solution, best_fitness