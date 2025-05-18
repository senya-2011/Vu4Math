# Построение матрицы конструкторов и решение нормальных уравнений
# X: матрица признаков, y: вектор наблюдений
def solve_normal_equations(design_matrix, y_vector):
    """
    Решает систему нормальных уравнений X^T X * coeffs = X^T y
    методом Гаусса. В случае сингулярности возбуждает исключение
    ValueError внутри solve_gauss.
    """
    # Формируем систему нормальных уравнений
    Xt = transpose_matrix(design_matrix)
    XtX = mat_mat_mul(Xt, design_matrix)
    XtY = mat_vec_mul(Xt, y_vector)
    # Решаем методом Гаусса (там уже есть проверка на вырожденность)
    return solve_gauss(XtX, XtY)


# Вспомогательная функция: транспонирование матрицы
def transpose_matrix(matrix):
    """Транспонирует матрицу"""
    return [list(row) for row in zip(*matrix)]


# Вспомогательная функция: умножение двух матриц
def mat_mat_mul(A, B):
    """Перемножает матрицы A и B"""
    rows_A, cols_A = len(A), len(A[0])
    cols_B = len(B[0])
    result = [[0.0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result


# Вспомогательная функция: умножение матрицы на вектор
def mat_vec_mul(A, v):
    """Перемножает матрицу A на вектор v"""
    rows, cols = len(A), len(A[0])
    result = [0.0] * rows
    for i in range(rows):
        for j in range(cols):
            result[i] += A[i][j] * v[j]
    return result

# Решение системы линейных уравнений Ax = b методом Гаусса
# с выбором главного элемента (прямой и обратный ход)
def solve_gauss(A, b, epsilon=1e-10):
    n = len(A)
    # Формируем расширенную матрицу
    M = [row[:] + [b_i] for row, b_i in zip(A, b)]
    # Прямой ход
    for i in range(n):
        # Поиск ведущего элемента
        max_row, max_val = i, abs(M[i][i])
        for r in range(i+1, n):
            if abs(M[r][i]) > max_val:
                max_row, max_val = r, abs(M[r][i])
        M[i], M[max_row] = M[max_row], M[i]
        pivot = M[i][i]
        for j in range(i, n+1): M[i][j] /= pivot
        for k in range(i+1, n):
            factor = M[k][i]
            for j in range(i, n+1):
                M[k][j] -= factor * M[i][j]
    # Обратный ход
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n]
        for j in range(i+1, n):
            x[i] -= M[i][j]*x[j]
        x[i] /= M[i][i]
    return x
