import random

from fitness import vertex_cover_fitness

GENES = [0, 1]


def initialize_pop(pop_size, gene_size):
    population = list()

    for i in range(pop_size):
        temp = list()
        for j in range(gene_size):
            temp.append(random.choice(GENES))
        population.append(temp)

    return population


def crossover(selected_chromo, gene_size, population, pop_size):
    offspring_cross = []
    for i in range(int(pop_size)):
        parent1 = random.choice(selected_chromo)
        parent2 = random.choice(population[:int(pop_size * 50)])

        p1 = parent1[0]
        p2 = parent2[0]

        crossover_point = random.randint(1, gene_size - 1)
        child = p1[:crossover_point] + p2[crossover_point:]
        offspring_cross.extend([child])
    return offspring_cross


def mutate(offspring, mut_rate):
    mutated_offspring = []

    for arr in offspring:
        for i in range(len(arr)):
            if random.random() < mut_rate:
                arr[i] = random.choice(GENES)
        mutated_offspring.append(arr)
    return mutated_offspring


def selection(population, pop_size):
    sorted_chromo_pop = sorted(population, key=lambda x: x[1])
    return sorted_chromo_pop[:int(0.5 * pop_size)]


def replace(new_gen, population):
    for _ in range(len(population)):
        if population[_][1] > new_gen[_][1]:
            population[_] = new_gen[_][0], new_gen[_][1]
    return population


def genetic_khuri(graph_data, pop_size, iterations):
    (num_vertices, adjacency_matrix, connections) = graph_data
    gene_size = num_vertices
    mut_rate = 1/num_vertices
    initial_population = initialize_pop(pop_size, gene_size)
    population = []
    g_best_fit = gene_size
    g_best_pos = [1] * gene_size
    global_best_val_timeline = [g_best_fit]

    for _ in range(len(initial_population)):
        population.append(vertex_cover_fitness(initial_population[_], connections))

    for _ in range(iterations):

        selected = selection(population, pop_size)

        population = sorted(population, key=lambda x: x[1])
        crossovered = crossover(selected, gene_size, population, pop_size)

        mutated = mutate(crossovered, mut_rate)

        new_gen = []
        for _ in mutated:
            new_gen.append(vertex_cover_fitness(_, connections))

        for individual in new_gen:
            if g_best_fit > individual[1]:
                g_best_fit = individual[1]
                g_best_pos = individual[0]

        global_best_val_timeline.append(g_best_fit)
        population = replace(new_gen, population)

    return g_best_pos, global_best_val_timeline
