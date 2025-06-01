import math
import methods.langrange as langrange
import methods.newton as newton
import methods.gauss as gauss
import methods.extra_task as extra_task
import tools.plot_tool as plot_utils

# Обёртки методов, возвращающие (poly_func, t)

def lagrange(xs, ys, x0):
    # Для Лагранжа t = (x0 - x1) / h, где h = xs[1]-xs[0]
    # if len(xs) > 1:
    #     h = xs[1] - xs[0]
    #     t = (x0 - xs[0]) / h if h != 0 else None
    # else:
    #     t = None
    t = None
    def poly(x): return langrange.lagrange(xs, ys, x)
    return poly, t


def newton_divided(xs, ys, x0):
    # стандартная разделённая разность, t относительна первого узла
    #h = xs[1] - xs[0]
    #t = (x0 - xs[0]) / h if h != 0 else None
    t = None
    def poly(x): return newton.newton_divided(xs, ys, x)
    return poly, t


def newton_forward(xs, ys, x0):
    h = xs[1] - xs[0]
    t = (x0 - xs[0]) / h if h != 0 else None
    def poly(x): return newton.newton_forward(xs, ys, x)
    return poly, t


def newton_backward(xs, ys, x0):
    h = xs[1] - xs[0]
    t = (x0 - xs[-1]) / h if h != 0 else None
    def poly(x): return newton.newton_backward(xs, ys, x)
    return poly, t


def gauss_forward(xs, ys, x0):
    h = xs[1] - xs[0]
    mid = len(xs)//2
    t = (x0 - xs[mid]) / h if h != 0 else None
    def poly(x): return gauss.gauss_forward(xs, ys, x)
    return poly, t


def gauss_backward(xs, ys, x0):
    h = xs[1] - xs[0]
    mid = len(xs)//2
    t = (x0 - xs[mid]) / h if h != 0 else None
    def poly(x): return gauss.gauss_backward(xs, ys, x)
    return poly, t


def stirling(xs, ys, x0):
    h = xs[1] - xs[0]
    mid = len(xs)//2
    t = (x0 - xs[mid]) / h if h != 0 else None
    def poly(x): return extra_task.stirling(xs, ys, x)
    return poly, t


def bessel(xs, ys, x0):
    h = xs[1] - xs[0]
    mid = len(xs)//2
    t = (x0 - xs[mid]) / h if h != 0 else None
    def poly(x): return extra_task.bessel(xs, ys, x)
    return poly, t

GENERATORS = {
    'sin(x)': math.sin,
    'x^3': lambda x: x**3
}

# Функция для вызова plot
def make_plot(xs, ys, x_val, methods_dict):
    return plot_utils.plot_interpolation(
        xs, ys, x_val,
        methods_dict
    )