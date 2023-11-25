import numpy

from benchmarks_opener import open_and_get_data


def create_adjacency_matrix(file_dir):
    (num_vertices, connections) = open_and_get_data(file_dir)
    adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]
    for edge in connections:
        i = edge[0] - 1
        j = edge[1] - 1
        adjacency_matrix[i][j] = 1
        adjacency_matrix[j][i] = 1
    return num_vertices, adjacency_matrix, connections
