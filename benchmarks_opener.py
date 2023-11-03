
def open_and_get_data(file_dir):

    with open(file_dir, 'r') as f:
        f.readline()
        vertices_number = f.readline().split()[0]
        lines = f.readlines()
        tuples_list = [(int(line.split()[0]), int(line.split()[1])) for line in lines]
        return int(vertices_number), tuples_list
