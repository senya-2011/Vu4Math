def read_matrix(path):
    try:
        with open(path, 'r') as file:
            size = count_lines(path) - 1
            matrix = []
            for _ in range(size):
                row = list(map(float, file.readline().strip().split()))
                if len(row) != size + 1:
                    print("Неверное количество элементов в строке.")
                    return None
                matrix.append(row)
            eps = float(file.readline().strip())
            return matrix, eps
    except Exception as e:
        print(e)
        return None, None

def count_lines(path):
    with open(path, 'r') as file:
        return sum(1 for _ in file)

def read_matrix_from_file(file):
    size = count_lines_from_file(file) - 1
    matrix = []
    for _ in range(size):
        row = list(map(float, file.readline().strip().split()))
        if len(row) != size + 1:
            print("Неверное количество элементов в строке.")
            return None
        matrix.append(row)
    eps = float(file.readline().strip())
    return matrix, eps

def count_lines_from_file(file):
    return sum(1 for _ in file)