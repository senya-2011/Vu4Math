from tools.math_tools import *


# Многочлен Ньютона с разделёнными разностями
def newton_divided(xs, ys, x):
    """
    Интерполяция Ньютона (разделённые разности).
    """
    n = len(xs)
    coeff = list(ys)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coeff[i] = (coeff[i] - coeff[i - 1]) / (xs[i] - xs[i - j])
    result = coeff[0]
    prod = 1.0
    for i in range(1, n):
        prod *= (x - xs[i - 1])
        result += coeff[i] * prod
    return result

# Многочлен Ньютона с конечными разностями (прямая формула)
def newton_forward(xs, ys, x):
    """Формула прямых конечных разностей. Только для равноотстоящих узлов."""
    h = xs[1] - xs[0]
    table = finite_diff_table(ys)
    t = (x - xs[0]) / h
    result = ys[0]
    for k in range(1, len(xs)):
        coeff = 1.0
        for j in range(k):
            coeff *= (t - j)
        result += coeff * table[k][0] / factorial(k)
    return result

# Многочлен Ньютона с конечными разностями (обратная формула)
def newton_backward(xs, ys, x):
    """Формула обратных конечных разностей. Только для равноотстоящих узлов."""
    h = xs[1] - xs[0]
    table = finite_diff_table(ys)
    n = len(xs)
    t = (x - xs[-1]) / h
    result = ys[-1]
    for k in range(1, n):
        coeff = 1.0
        for j in range(k):
            coeff *= (t + j)
        result += coeff * table[k][n - k - 1] / factorial(k)
    return result
