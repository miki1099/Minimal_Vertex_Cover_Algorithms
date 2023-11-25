from adjacency_matrix_creator import create_adjacency_matrix
from jpso import jpso_vertex_cover

data = create_adjacency_matrix('DIMACS benchmarks/johnson8-4-4.mtx')

(global_best_pos, global_best_pos_timeline) = jpso_vertex_cover(data, 100, 200)

print(global_best_pos)