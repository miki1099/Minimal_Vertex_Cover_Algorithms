import random
import time
from copy import deepcopy

from fitness import get_best, get_chosen_vertices, mvc_approx

bee_neighbour_to_check = 10


def init_swarm(swarm_size, vertices_num, connections):
    swarm = [[random.choice([0, 1]) for _ in range(vertices_num)] for _ in range(swarm_size)]
    for i in range(len(swarm)):
        swarm[i] = find_vertices_to_correct_cover(swarm[i], connections)

    return swarm


def get_random_valid_pos(vertices_num, connections):
    new_pos = [random.choice([0, 1]) for _ in range(vertices_num)]
    return find_vertices_to_correct_cover(new_pos, connections)


def count_vertices(position):
    return sum(position)


def zero_out_row_and_column(matrix, index):
    # Zero out the specified row
    for i in range(len(matrix[index])):
        matrix[index][i] = 0

    # Zero out the specified column
    for i in range(len(matrix)):
        matrix[i][index] = 0


def find_vertices_to_correct_cover(combined_particle_pos, connections):
    return mvc_approx(combined_particle_pos, connections)


def fitness(position):
    num_of_vertices = position.count(1)
    return 1/(1 + num_of_vertices)


def invert_val_at_index(pos, index):
    pos_copy = deepcopy(pos)
    if pos[index] == 1:
        pos_copy[index] = 0
    else:
        pos_copy[index] = 1

    return pos_copy


def run_bee_through_neighbourhood(bee_pos, connections):
    neighbour_arr = []
    for i in range(bee_neighbour_to_check):
        random_index1 = random.randint(0, len(bee_pos) - 1)
        random_index2 = random.randint(0, len(bee_pos) - 1)
        random_index3 = random.randint(0, len(bee_pos) - 1)
        neighbour_arr1 =  invert_val_at_index(bee_pos, random_index1)
        neighbour_arr2 = invert_val_at_index(neighbour_arr1, random_index2)
        neighbour_arr3 = invert_val_at_index(neighbour_arr2, random_index3)
        neighbour_arr.append(neighbour_arr3)

    for i in range(len(neighbour_arr)):
        neighbour_arr[i] = find_vertices_to_correct_cover(neighbour_arr[i], connections)

    return neighbour_arr


def calculate_neighbour_fittness(bee_valid_neighbours):
    fitt_array = []
    for neighbour in bee_valid_neighbours:
        fitt_array.append(fitness(neighbour))

    return fitt_array


def get_new_place_from_neighbour(bee_valid_neighbours, bee_valid_neighbours_fit):
    fit_sum = sum(bee_valid_neighbours_fit)

    probabilistic_sum_buffer = 0
    neighbours_prob_array = []
    for neighbour_fitness in bee_valid_neighbours_fit:
        segment_prob = neighbour_fitness/fit_sum
        neighbours_prob_array.append(segment_prob + probabilistic_sum_buffer)
        probabilistic_sum_buffer += segment_prob

    random_val = random.uniform(0, 1)
    for i in range(len(bee_valid_neighbours_fit)):
        if neighbours_prob_array[i] > random_val:
            return bee_valid_neighbours[i]

    return bee_valid_neighbours[len(bee_valid_neighbours_fit)-1]


def combine_new_place(bee_pos, new_place_by_onlooker, connections):
    new_place = []
    for i in range(len(bee_pos)):
        if bee_pos[i] == new_place_by_onlooker[i]:
            new_place.append(bee_pos[i])
        else:
            new_place.append(random.randint(0, 1))

    return find_vertices_to_correct_cover(new_place, connections)


def abc_vertex_cover(graph_data, swarm_size, timeout):
    start_time = time.time()
    (num_vertices, adjacency_matrix, connections) = graph_data
    swarm_pos = init_swarm(swarm_size, num_vertices, connections)
    (global_best_pos, g_best_score) = get_best(swarm_pos, connections)

    global_best_val_timeline = []
    iter_times = []
    while time.time() - start_time <= timeout * 60:
        iter_start_time = time.time()
        for i in range(len(swarm_pos)):
            # employer bee region
            bee_pos = swarm_pos[i]

            bee_valid_neighbours = run_bee_through_neighbourhood(bee_pos, connections)
            bee_valid_neighbours_fit = calculate_neighbour_fittness(bee_valid_neighbours)
            # end employer bee region

            # onlooker bee region
            new_place_by_onlooker = get_new_place_from_neighbour(bee_valid_neighbours, bee_valid_neighbours_fit)
            combined_new_place = combine_new_place(bee_pos, new_place_by_onlooker, connections)
            # end onlooker bee region

            solution_quality = count_vertices(combined_new_place)

            if g_best_score > solution_quality:
                global_best_pos = combined_new_place
                g_best_score = solution_quality

            # scout bee region
            if bee_pos == combined_new_place:
                swarm_pos[i] = get_random_valid_pos(num_vertices, connections)
            else:
                swarm_pos[i] = combined_new_place
            # end scout bee region

        global_best_val_timeline.append(g_best_score)
        iter_times.append(time.time() - iter_start_time)
        # print(g_best_score)
        # print(global_best_pos)

    return global_best_pos, global_best_val_timeline, iter_times
