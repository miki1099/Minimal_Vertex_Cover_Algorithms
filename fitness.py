def is_vertex_cover(vertices_genome, connections):
    vertices = convert_to_list(vertices_genome)
    obstacles = 0
    for connection in connections:
        if connection[0] not in vertices and connection[1] not in vertices:
            obstacles += 1
    return obstacles == 0, obstacles


def convert_to_list(vertices_genome):
    binary_string = str(vertices_genome)
    result = set()
    for i, bit in enumerate(binary_string):
        if bit == '1':
            result.add(i + 1)
    return result
