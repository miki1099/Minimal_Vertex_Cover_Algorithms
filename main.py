from abc_algo import abc_vertex_cover
from adjacency_matrix_creator import create_adjacency_matrix
from jpso import jpso_vertex_cover

data = create_adjacency_matrix('DIMACS benchmarks/C125-9.mtx')

(global_best_pos_jpso, global_best_pos_timeline_jpso) = jpso_vertex_cover(data, 100, 200)

(global_best_pos_abc, global_best_pos_timeline_abc) = abc_vertex_cover(data, 100, 200)

# print(global_best_pos_jpso)