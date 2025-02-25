import matrix_operations.create_matrix as create_matrix
import matrix_operations.diagonal_checker as diagonal_checker
import matrix_operations.epsilon as epsilon
import matrix_operations.read_matrix as read_matrix


def matrix_choice():
    print("1. Клавиатура\n2. Файл")
    choice = input("Выберите способ ввода: ").strip()
    if choice == "1":
        matrix = create_matrix.create_matrix()
    elif choice == "2":
        path = input("Имя файла: ").strip()
        matrix, eps = read_matrix.read_matrix(path)
        if eps is None:
            return
        check_matrix(matrix, eps)
    else:
        print("Неверный выбор")
        return

    if matrix is None:
        return
    if choice=="1":
        eps = epsilon.get_epsilon()
        if eps is None:
            return
        check_matrix(matrix, eps)

def check_matrix(matrix, eps):
    if not diagonal_checker.check(matrix):
        matrix = diagonal_checker.rearrangement_of_string(matrix)

        if matrix is None:
            return "диагональное преобладание невозможно"


        print("после перестановки:")
        for row in matrix:
            print(row)
    return solve_matrix(matrix, eps)


def solve_matrix(matrix, eps, max_iterations=1000):
    decimal_places = len(str(eps).split('.')[-1])
    size = len(matrix)
    x = [0.0] * size
    B = [row[-1] for row in matrix]
    iter_counter = 0

    while iter_counter < max_iterations:
        new_x = x.copy()
        norma = 0.0

        for i in range(size):
            sum_ = sum(matrix[i][j] * x[j] for j in range(size) if j != i)
            new_x[i] = (B[i] - sum_) / matrix[i][i]
            norma = max(norma, abs(new_x[i] - x[i]))

        x = new_x
        iter_counter += 1

        if norma < eps:
            break

    if iter_counter == max_iterations:
        return "Метод не сошёлся за максимальное число итераций!"

    result = f'Метод сошёлся за {iter_counter} итераций.\n'

    for i in range(size):
        result += f"x{i + 1} = {x[i]:.{decimal_places}f}\n"


    residuals = calculate_residuals(matrix, x, B)
    result += "Вектор невязки:\n"
    for i, res in enumerate(residuals):
        result += f"Δx{i + 1} = {res:.{decimal_places}f}\n"
    print(result)
    return result


def calculate_residuals(matrix, x, B):
    size = len(matrix)
    residuals = []
    for i in range(size):
        Ax_i = sum(matrix[i][j] * x[j] for j in range(size))
        residuals.append(Ax_i - B[i])
    return residuals