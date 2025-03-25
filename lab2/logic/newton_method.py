import logic.properties as properties
import logic.derivative_function as derivative_fun
import logic.jacobian_matrix as jacobian_matrix


def calculate(f, x, eps=properties.def_eps):
    df = derivative_fun.return_df(f)
    for i in range(properties.max_iter):
        f_x = f(x)
        df_x = df(x)
        if (df_x != 0):
            next_x = x - f_x / df_x
        else:
            return 0,0,0

        if abs(f_x) < eps:
            return f(x) ,x, i + 1
        elif abs(next_x - x) < eps:
            return f(x), next_x, i + 1

        x = next_x

    return f(x), x, properties.max_iter


def calculate_system(f, x0, y0, eps=properties.def_eps, max_iter=properties.max_iter):
    if(x0==0):
        x0 = 0.01
    errors = []
    for iteration in range(max_iter):
        f_x = [func(x0, y0) for func in f]
        J_x = jacobian_matrix.jacobian(f[0], f[1], x0, y0)

        delta = solve_linear_system(J_x, f_x)
        if (delta == "err"):
            return 0, 0, 0, [(0,0)], 0

        x1 = x0 + delta[0]
        y1 = y0 + delta[1]

        error_x = abs(x1 - x0)
        error_y = abs(y1 - y0)

        errors.append((error_x, error_y))

        if max(abs(f_val) for f_val in f_x) < eps:
            return x1, y1, iteration + 1, errors, J_x

        if max(error_x, error_y) < eps:
            return x1, y1, iteration + 1, errors, J_x

        x0, y0 = x1, y1

    return 0, 0, max_iter, [(0,0)], J_x


def solve_linear_system(J_x, f_x):
    n = len(J_x)
    wide_matrix = [J_x[i] + [-f_x[i]] for i in range(n)]

    for i in range(n):
        rotate = wide_matrix[i][i]
        if rotate == 0:
            return "err"

        wide_matrix[i] = [elem / rotate for elem in wide_matrix[i]]

        for j in range(i + 1, n):
            lamda = wide_matrix[j][i]
            wide_matrix[j] = [wide_matrix[j][k] - lamda * wide_matrix[i][k] for k in range(n + 1)]

    delta = [0] * n
    for i in range(n - 1, -1, -1):
        delta[i] = wide_matrix[i][-1] - sum(wide_matrix[i][j] * delta[j] for j in range(i + 1, n))

    return delta