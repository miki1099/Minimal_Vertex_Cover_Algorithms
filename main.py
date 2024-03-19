import sys
from abc_algo import abc_vertex_cover
from adjacency_matrix_creator import create_adjacency_matrix
from fitness import get_chosen_vertices, is_vertex_cover
from genetic_khuri import genetic_khuri
from genetic_with_2_approx import genetic_approx
from jpso import jpso_vertex_cover


sys.setrecursionlimit(3000)
data = create_adjacency_matrix('DIMACS benchmarks/C125-9.mtx')

# (global_best_pos_jpso, global_best_pos_timeline_jpso) = jpso_vertex_cover(data, 10, 20)

(global_best_pos_abc, global_best_pos_timeline_abc) = abc_vertex_cover(data, 50, 100)

(global_best_pos_gen_khuri, global_best_pos_timeline_gen_khuri) = genetic_khuri(data, 50, 100)

(global_best_pos_gen_approx, global_best_pos_timeline_gen_approx) = genetic_approx(data, 50, 100)

print(global_best_pos_abc)
print(sum(global_best_pos_abc))
vertices = get_chosen_vertices(global_best_pos_abc)
print(is_vertex_cover(vertices, data[2]))
print(global_best_pos_timeline_abc)

print(global_best_pos_gen_khuri)
print(sum(global_best_pos_gen_khuri))
vertices = get_chosen_vertices(global_best_pos_gen_khuri)
print(is_vertex_cover(vertices, data[2]))
print(global_best_pos_timeline_gen_khuri)

print(global_best_pos_gen_approx)
print(sum(global_best_pos_gen_approx))
vertices = get_chosen_vertices(global_best_pos_gen_approx)
print(is_vertex_cover(vertices, data[2]))
print(global_best_pos_timeline_gen_approx)
