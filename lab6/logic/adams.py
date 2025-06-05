from logic.runge_kutta import solve_rk4

def solve_adams4(f, x0, y0, xn, h):
    n_steps = int((xn - x0) / h)
    xs = [x0 + i*h for i in range(n_steps + 1)]
    ys = [0.0] * (n_steps + 1)
    ys[0] = y0

    if n_steps < 3:
        xs_rk, ys_rk = solve_rk4(f, x0, y0, xn, h)
        return xs_rk, ys_rk

    xs_init, ys_init = solve_rk4(f, x0, y0, x0 + 3*h, h)
    for i in range(4):
        ys[i] = ys_init[i]

    def Fi(i):
        return f(xs[i], ys[i])


    for i in range(3, n_steps):

        P = ys[i] + (h/24) * (
            55*Fi(i) - 59*Fi(i-1) + 37*Fi(i-2) - 9*Fi(i-3)
        )

        ys[i+1] = ys[i] + (h/24) * (
            9 * f(xs[i+1], P) + 19*Fi(i) - 5*Fi(i-1) + Fi(i-2)
        )
    return xs, ys

def max_error_adams(f_exact, xs, ys):

    max_err = 0.0
    for xi, yi in zip(xs, ys):
        y_ex = f_exact(xi)
        err = abs(yi - y_ex)
        if err > max_err:
            max_err = err
    return max_err
