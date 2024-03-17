
def vertex_cover_fitness(vertices_genome, connections):
    vertices = get_chosen_vertices(vertices_genome)
    obstacles_pent = 0
    for connection in connections:
        if connection[0] not in vertices and connection[1] not in vertices:
            obstacles_pent += len(vertices_genome)
    return vertices_genome, sum(vertices_genome) + obstacles_pent


def is_vertex_cover(vertices, connections):
    for connection in connections:
        if connection[0] not in vertices and connection[1] not in vertices:
            return False
    return True


def get_chosen_vertices(vertices_genome):
    result = set()
    for i in range(len(vertices_genome)):
        if vertices_genome[i] == 1:
            result.add(i + 1)
    return result


def get_best(particles_locations, connections):
    vertices_num = len(particles_locations[0])
    best = [0] * vertices_num
    best_score = vertices_num
    for particle in particles_locations:
        vertices = get_chosen_vertices(particle)
        if is_vertex_cover(vertices, connections) and best_score < len(vertices):
            best = particle
            best_score = len(vertices)
    return best, best_score


def get_valid_or_ones(particles_locations, connections):
    vertices_num = len(particles_locations[0])
    all_vertices = [1] * vertices_num

    return_array = []

    for particle in particles_locations:
        vertices = get_chosen_vertices(particle)
        if is_vertex_cover(vertices, connections):
            return_array.append(particle)
        else:
            return_array.append(all_vertices)
    return return_array
