from tools.math_tools import *


def stirling(pol_xs, pol_ys, x):
    """Схема Стирлинга для равноотстоящих узлов"""
    n = len(pol_xs) - 1
    mid = n // 2
    diffs = finite_diff_table(pol_ys)
    h = pol_xs[1] - pol_xs[0]
    t = (x - pol_xs[mid]) / h
    # dts: последовательность шагов для центральной схемы
    dts = [(j // 2) * ((-1) ** (j)) for j in range(n + 1)]
    result = pol_ys[mid]
    for k in range(1, n + 1):
        # выбор центрального элемента конечных разностей
        idx = len(diffs[k]) // 2
        term = 1.0
        for j in range(k):
            term *= (t - dts[j])
        result += term * diffs[k][idx] / factorial(k)
    return result


def bessel(pol_xs, pol_ys, x):
    """Схема Бесселя для равноотстоящих узлов"""
    n = len(pol_xs) - 1
    mid = n // 2
    diffs = finite_diff_table(pol_ys)
    h = pol_xs[1] - pol_xs[0]
    t = (x - pol_xs[mid]) / h
    # dts: последовательность шагов для центральной схемы
    dts = [(j // 2) * ((-1) ** (j)) for j in range(n + 1)]
    result = pol_ys[mid]
    for k in range(1, n + 1):
        idx = len(diffs[k]) // 2
        # первая часть
        term1 = 1.0
        for j in range(k):
            term1 *= (t - dts[j])
        # вторая часть (сдвиг на 0.5)
        term2 = 1.0
        for j in range(k):
            term2 *= (t + dts[j])
        result += 0.5 * (term1 + term2) * diffs[k][idx] / factorial(k)
    return result
