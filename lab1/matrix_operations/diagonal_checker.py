def check(matrix):
    size = len(matrix)
    for i in range(size):
        diagonal = abs(matrix[i][i])  # модуль диаг элемента
        row_sum = sum(abs(matrix[i][j]) for j in range(size) if j != i)  # сумма всех остальных

        if diagonal <= row_sum:
            return False  # любая строка не проходит => не диагональ

    return True


def rearrangement_of_string(matrix, step=0):
    size = len(matrix)

    if step >= size - 1:
        return matrix if check(matrix) else None  #достигли диагонального преобладания???

    for row in range(step, size):
        matrix[step], matrix[row] = matrix[row], matrix[step]

        for col in range(step, size):
            for r in range(size):
                matrix[r][step], matrix[r][col] = matrix[r][col], matrix[r][step]

            adjusted = rearrangement_of_string(matrix, step + 1)
            if adjusted is not None:
                return adjusted

            for r in range(size):
                matrix[r][step], matrix[r][col] = matrix[r][col], matrix[r][step]

        matrix[step], matrix[row] = matrix[row], matrix[step]

    return None

