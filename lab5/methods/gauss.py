from tools.math_tools import *


def gauss_forward(xs, ys, x):
    h = xs[1] - xs[0]
    n = len(xs)
    mid = n // 2
    table = finite_diff_table(ys)
    t = (x - xs[mid]) / h
    result = ys[mid]
    p = 1.0

    for k in range(1, mid + 1):
        if k % 2 == 1:
            idx = mid - (k // 2)
        else:
            idx = mid - (k // 2) - 1

        if not (0 <= idx < len(table[k])):
            raise IndexError(f"gauss_forward: k={k}, idx={idx}, len(table[{k}])={len(table[k])}")

        p *= (t - (k - 1) / 2)
        result += p * table[k][idx] / factorial(k)

    return result


def gauss_backward(xs, ys, x):
    h = xs[1] - xs[0]
    n = len(xs)
    mid = n // 2
    table = finite_diff_table(ys)
    t = (x - xs[mid]) / h
    result = ys[mid]
    p = 1.0

    for k in range(1, mid + 1):
        if k % 2 == 1:
            idx = mid - (k // 2)
        else:
            idx = mid - (k // 2) - 1

        if not (0 <= idx < len(table[k])):
            raise IndexError(f"gauss_backward: k={k}, idx={idx}, len(table[{k}])={len(table[k])}")

        p *= (t + (k - 1) / 2)
        result += p * table[k][idx] / factorial(k)

    return result
