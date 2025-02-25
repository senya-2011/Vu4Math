def create_matrix():
    size = int(input("Размер матрицы: ").strip())
    if 0 < size <= 20:
        print("Введите строки матрицы:")
        matrix = []
        for i in range(size):
            row = list(map(float, input().strip().split()))
            if len(row) != size + 1:
                print("Неверное кол-во элементов строки в матрице!")
                return None
            matrix.append(row)
        return matrix
    else:
        print("Неверный размер матрицы!")
        return None
