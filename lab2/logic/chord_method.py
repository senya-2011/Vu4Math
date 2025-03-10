import logic.root_checker as root_checker
import logic.properties as properties


def calculate(f, a, b, eps=properties.def_eps):
    f_a, f_b = f(a), f(b)

    if not root_checker.is_roots(f(a), f(b)):
        return 0,0,0

    for i in range(properties.max_iter):
        c = (a * f_b - b * f_a) / (f_b - f_a)
        f_c = f(c)

        if abs(f_c) < eps:
            return f(c), c, i + 1
        elif root_checker.is_roots(f_a, f_c):
            b, f_b = c, f_c
        else:
            a, fa = c, f_c

    return f((a + b) / 2), (a + b) / 2, properties.max_iter
