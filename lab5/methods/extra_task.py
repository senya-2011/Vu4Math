from tools.math_tools import finite_diff_table, factorial

def stirling(xs, ys, x):
    m = len(xs)
    if m < 2:
        return ys[0] if m == 1 else 0.0

    h = xs[1] - xs[0]
    N = m - 1

    diffs = finite_diff_table(ys)

    alpha = N // 2
    x0 = xs[alpha]
    t = (x - x0) / h

    res = diffs[0][alpha]

    prod_even = 1.0
    prod_odd = t

    for k in range(1, N + 1):
        if k % 2 == 1:
            j = (k - 1) // 2
            if j > 0:
                prod_odd *= (t*t - j*j)
            idx = alpha - j
            if idx > 0:
                d_center = 0.5 * (diffs[k][idx] + diffs[k][idx-1])
            else:
                d_center = diffs[k][idx]
            term = (prod_odd * d_center) / factorial(k)
        else:
            j = k // 2
            if j > 0:
                prod_even *= (t*t - (j-1)*(j-1))
            idx = alpha - j
            term = (prod_even * diffs[k][idx]) / factorial(k)

        res += term

    return res


def bessel(xs, ys, x):
    m = len(xs)
    if m < 2:
        return ys[0] if m == 1 else 0.0

    h = xs[1] - xs[0]
    N = m - 1

    diffs = finite_diff_table(ys)

    i1 = (N // 2) + 1
    i0 = i1 - 1

    x0 = xs[i0]
    t = (x - x0) / h

    res = 0.5 * (diffs[0][i0] + diffs[0][i1])

    res += (t - 0.5) * diffs[1][i0]

    for k in range(2, N + 1):
        if k % 2 == 0:
            j = k // 2
            prod = 1.0
            for shift in range(-j, j):
                prod *= (t + shift)
            idx = i0 - j + 1
            diff_avg = 0.5 * (diffs[k][idx] + diffs[k][idx-1])
            term = prod * diff_avg / factorial(k)
        else:
            j = (k - 1) // 2
            prod = (t - 0.5)
            for shift in range(-j, j):
                prod *= (t + shift)
            idx = i0 - j
            diff_val = diffs[k][idx]
            term = prod * diff_val / factorial(k)

        res += term

    return res
