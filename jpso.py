import random
from copy import deepcopy

from fitness import get_best, get_valid_or_ones, get_chosen_vertices


def init_swarm(swarm_size, vertices_num):
    return [[random.choice([0, 1]) for _ in range(vertices_num)] for _ in range(swarm_size)]


def count_vertices(position):
    return sum(position)


def zero_out_row_and_column(matrix, index):
    # Zero out the specified row
    for i in range(len(matrix[index])):
        matrix[index][i] = 0

    # Zero out the specified column
    for i in range(len(matrix)):
        matrix[i][index] = 0


def find_vertices_to_correct_cover(combined_particle_pos, adjacency_matrix):
    vertices_to_cover = get_chosen_vertices(combined_particle_pos)
    for vertex_index in vertices_to_cover:
        zero_out_row_and_column(adjacency_matrix, vertex_index)

    return make_position_valid_solution(combined_particle_pos, adjacency_matrix)


def make_position_valid_solution(combined_particle_pos, adjacency_matrix):
    max_amount_of_not_covered_edges = 0
    index_of_max_uncovered = 0

    for i in range(len(adjacency_matrix)):
        not_covered_edges = sum(adjacency_matrix[i])
        if not_covered_edges > max_amount_of_not_covered_edges:
            max_amount_of_not_covered_edges = not_covered_edges
            index_of_max_uncovered = i

    if max_amount_of_not_covered_edges == 0:
        return combined_particle_pos
    else:
        combined_particle_pos[index_of_max_uncovered] = 1
        zero_out_row_and_column(adjacency_matrix, index_of_max_uncovered)
        return make_position_valid_solution(combined_particle_pos, adjacency_matrix)


def combine(particle_pos, selected, adjacency_matrix):
    A = deepcopy(adjacency_matrix)
    combined_particle_pos = deepcopy(particle_pos)

    # get vertices indexes when get random some of them to combine
    vertices_index = get_chosen_vertices(particle_pos)
    how_much_to_combine = random.randint(0, len(vertices_index))

    selected_vertices_index = get_chosen_vertices(selected)

    for _ in range(how_much_to_combine):
        combine_selector = random.uniform(0, 1)
        if combine_selector <= 0.5:
            index = random.choice(vertices_index)
            combined_particle_pos[index] = 0
        elif selected_vertices_index:
            index = random.choice(selected_vertices_index)
            combined_particle_pos[index] = 1

    return find_vertices_to_correct_cover(combined_particle_pos, A)


def jpso_vertex_cover(graph_data, swarm_size, iterations):
    (num_vertices, adjacency_matrix, connections) = graph_data
    vertices_num = len(adjacency_matrix[0])
    swarm_pos = init_swarm(swarm_size, vertices_num)
    swarm_local_best = get_valid_or_ones(swarm_pos, connections)
    (global_best_pos, g_best_score) = get_best(swarm_pos, connections)

    global_best_val_timeline = []
    for _ in range(iterations):
        neighbour_pos = None
        for i in range(vertices_num):
            if i == 0:
                neighbour_pos = [1] * vertices_num

            particle_pos = swarm_pos[i]

            combine_select_rand = random.uniform(0, 1)

            if combine_select_rand <= 0.25:
                selected = particle_pos
            elif combine_select_rand <= 0.5:
                selected = swarm_local_best[i]
            elif combine_select_rand <= 0.75:
                selected = neighbour_pos
            else:
                selected = global_best_pos

            particle_pos = combine(particle_pos, selected, adjacency_matrix)
            solution_quality = count_vertices(particle_pos)

            if count_vertices(swarm_local_best[i]) > solution_quality:
                swarm_local_best[i] = particle_pos
            if count_vertices(neighbour_pos) > solution_quality:
                neighbour_pos = particle_pos
            if g_best_score > solution_quality:
                global_best_pos = particle_pos
                g_best_score = count_vertices(global_best_pos)

            swarm_pos[i] = particle_pos
        global_best_val_timeline.append(g_best_score)
        # print(g_best_score)
        # print(global_best_pos)

    return global_best_pos, global_best_val_timeline
