def solve_euler(f, x0, y0, xn, h):
    n_steps = int((xn - x0) / h)
    xs = [x0 + i*h for i in range(n_steps + 1)]
    ys = [0.0] * (n_steps + 1)
    ys[0] = y0
    for i in range(n_steps):
        xi = xs[i]
        yi = ys[i]
        ys[i+1] = yi + h * f(xi, yi)
    return xs, ys

def runge_error(f, x0, y0, xn, h, method_func, p):
    _, ys_h = method_func(f, x0, y0, xn, h)
    y_end_h = ys_h[-1]
    _, ys_h2 = method_func(f, x0, y0, xn, h/2)
    y_end_h2 = ys_h2[-1]
    factor = 2**p - 1
    if factor == 0:
        return None
    return abs(y_end_h - y_end_h2) / factor
