import random
import numpy.random as npr

from fitness import mvc_approx

GENES = [0, 1]


def initialize_pop(pop_size, gene_size):
    population = list()

    for i in range(pop_size):
        temp = list()
        for j in range(gene_size):
            temp.append(random.choice(GENES))
        population.append(temp)

    return population


def crossover(gene_size, population, pop_size):
    offspring_cross = []
    for i in range(int(pop_size)):
        parent1 = select_one(population)
        parent2 = random.choice(population[:int(pop_size * 50)])

        p1 = parent1[0]
        p2 = parent2[0]

        crossover_points = sorted(random.sample(range(1, gene_size - 1), 2))
        child = p1[:crossover_points[0]] + p2[crossover_points[0]:crossover_points[1]] + p1[crossover_points[1]:]
        offspring_cross.extend([child])
    return offspring_cross


def mutate(offspring, mut_rate):
    mutated_offspring = []

    for arr in offspring:
        for i in range(len(arr)):
            if random.random() < mut_rate:
                arr[i] = abs(arr[i]-1)
        mutated_offspring.append(arr)
    return mutated_offspring


def select_one(population):
    total_inverse_fitness = sum(1 / chromo[1] for chromo in population)
    selection_probs = [(1 / chromo[1]) / total_inverse_fitness for chromo in population]
    return population[npr.choice(len(population), p=selection_probs)]


def replace(new_gen, population):
    for _ in range(len(population)):
        if population[_][1] > new_gen[_][1]:
            population[_] = new_gen[_][0], new_gen[_][1]
    return population


def make_genome_feasible_approx(population, connections):
    feasible_solutions = []
    for _ in range(len(population)):
        feasible_solutions.append(mvc_approx(population[_], connections))

    return feasible_solutions


def simple_fitness(vertices_genome):
    return vertices_genome, sum(vertices_genome)


def genetic_approx(graph_data, pop_size, iterations):
    (num_vertices, adjacency_matrix, connections) = graph_data
    gene_size = num_vertices
    mut_rate = 1/num_vertices
    initial_population = initialize_pop(pop_size, gene_size)
    initial_population = make_genome_feasible_approx(initial_population, connections)
    population = []
    g_best_fit = gene_size
    g_best_pos = [1] * gene_size
    global_best_val_timeline = [g_best_fit]

    for _ in range(len(initial_population)):
        population.append(simple_fitness(initial_population[_]))

    for _ in range(iterations):

        population = sorted(population, key=lambda x: x[1])
        crossovered = crossover(gene_size, population, pop_size)

        mutated = mutate(crossovered, mut_rate)
        mutated = make_genome_feasible_approx(mutated, connections)

        new_gen = []
        for _ in mutated:
            new_gen.append(simple_fitness(_))

        for individual in new_gen:
            if g_best_fit > individual[1]:
                g_best_fit = individual[1]
                g_best_pos = individual[0]

        global_best_val_timeline.append(g_best_fit)
        population = replace(new_gen, population)

    return g_best_pos, global_best_val_timeline
