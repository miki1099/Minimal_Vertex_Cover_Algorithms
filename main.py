import math


import pyswarms.discrete as ps
import numpy as np
from fitness import is_vertex_cover
from benchmarks_opener import open_and_get_data

(num_vertices, connections) = open_and_get_data('DIMACS benchmarks/MANN-a9.mtx')

# all_possible_vertex = pow(2, num_vertices)/1000
#
# max_bound = [1] * num_vertices
# min_bound = [0] * num_vertices
#
# bounds = (min_bound, max_bound)

n_particles = 200

init_pos = np.random.randint(2, size=(n_particles, num_vertices))
init_pos[0] = [1] * num_vertices


def dimensions_values_to_genome(solution):
    solution_genome = ''
    for solution_dimension in solution:
        if solution_dimension < 0.5:
            solution_genome += '0'
        else:
            solution_genome += '1'
    return solution_genome


def mvc_fitness_function(solutions):
    fitness_arr = []
    for solution in solutions:
        vertex_genome = dimensions_values_to_genome(solution)
        solution_vertices_count = vertex_genome.count('1')
        is_valid_solutions = is_vertex_cover(vertex_genome, connections)
        if not is_valid_solutions[0]:
            fitness_arr.append(num_vertices + is_valid_solutions[1])
        else:
            fitness_arr.append(solution_vertices_count)
    return fitness_arr


options = {'c1': 2, 'c2': 2, 'w': 0.7, 'k': 1, 'p': 1}

optimizer = ps.BinaryPSO(n_particles=n_particles, dimensions=num_vertices, options=options, init_pos=init_pos)

best_cost, best_pos = optimizer.optimize(mvc_fitness_function, iters=2000)

print(f"Minimal vertex cover found by PSO: {best_cost}")
genome = dimensions_values_to_genome(best_pos)
print(f"Genome: {genome}")
