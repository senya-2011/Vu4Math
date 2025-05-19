from tools.math_tools import *


# Интерполяция по формулам Гаусса
def gauss_forward(xs, ys, x):
    h = xs[1] - xs[0]
    n = len(xs)
    mid = n // 2
    table = finite_diff_table(ys)
    t = (x - xs[mid]) / h
    result = ys[mid]
    p = 1.0
    for k in range(1, mid + 1):
        if k % 2:
            idx = mid - (k // 2)
        else:
            idx = mid - (k // 2)
        p *= (t - (k - 1) / 2)
        result += p * table[k][idx] / factorial(k)
    return result


# Формула Гаусса (центральная, назад)
def gauss_backward(xs, ys, x):
    """Вторая формула Гаусса (центральная, назад)."""
    h = xs[1] - xs[0]
    n = len(xs)
    mid = n // 2
    table = finite_diff_table(ys)
    t = (x - xs[mid]) / h
    result = ys[mid]
    p = 1.0
    for k in range(1, mid + 1):
        if k % 2:
            idx = mid - (k // 2)
        else:
            idx = mid - (k // 2) - 1
        p *= (t + (k - 1) / 2)
        result += p * table[k][idx] / factorial(k)
    return result
