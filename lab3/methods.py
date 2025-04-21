def runge_error(curr, prev, order):
    return abs(curr - prev) / (2**order - 1)


def mid_rectangle(f, a, b, n):
    h = (b - a) / n
    return sum(f(a + (i + 0.5) * h) for i in range(n)) * h


def left_rectangle(f, a, b, n):
    h = (b - a) / n
    return sum(f(a + i * h) for i in range(n)) * h


def right_rectangle(f, a, b, n):
    h = (b - a) / n
    return sum(f(a + (i + 1) * h) for i in range(n)) * h


def trapezoid(f, a, b, n):
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return total * h


def simpson(f, a, b, n):
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        coeff = 4 if i % 2 else 2
        total += coeff * f(a + i * h)
    return total * h / 3

def approximate(method, f, a, b, eps, n0, order):
    prev = method(f, a, b, n0)
    n = n0 * 2
    iters = 1
    while True:
        curr = method(f, a, b, n)
        iters += 1
        if runge_error(curr, prev, order) <= eps:
            return curr, iters
        prev, n = curr, n * 2
