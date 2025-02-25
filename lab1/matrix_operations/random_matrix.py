import random

def generate_random_list(size):
    return [random.randint(1, size + 1) for _ in range(size + 1)]

def create_random_matrix(size):
    if 0 < size <= 20:
        matrix = []
        for i in range(size):
            row = list(map(float, generate_random_list(size)))
            if len(row) != size + 1:
                print("Неверное кол-во элементов строки в матрице!")
                return None
            matrix.append(row)
        return matrix
    else:
        print("Неверный размер матрицы!")
        return None