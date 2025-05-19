def factorial(n):
    factorial_n = 1
    for i in range(2, n + 1):
        factorial_n *= i
    return factorial_n

def finite_diff_table(y_vals):
    n = len(y_vals)
    table = [list(y_vals)]
    for level in range(1, n):
        prev = table[-1]
        diff = [prev[i + 1] - prev[i] for i in range(len(prev) - 1)]
        table.append(diff)
    return table
