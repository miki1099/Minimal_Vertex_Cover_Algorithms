import sys
from abc_algo import abc_vertex_cover
from adjacency_matrix_creator import create_adjacency_matrix
from fitness import get_chosen_vertices, is_vertex_cover
from genetic_khuri import genetic_khuri
from jpso import jpso_vertex_cover


sys.setrecursionlimit(3000)
data = create_adjacency_matrix('DIMACS benchmarks/johnson8-2-4.mtx')

# (global_best_pos_jpso, global_best_pos_timeline_jpso) = jpso_vertex_cover(data, 10, 20)

# (global_best_pos_abc, global_best_pos_timeline_abc) = abc_vertex_cover(data, 10, 20)

(global_best_pos_gen_khuri, global_best_pos_timeline_gen_khuri) = genetic_khuri(data, 50, 2000)

print(global_best_pos_gen_khuri)
print(sum(global_best_pos_gen_khuri))
vertices = get_chosen_vertices(global_best_pos_gen_khuri)
print(is_vertex_cover(vertices, data[2]))
