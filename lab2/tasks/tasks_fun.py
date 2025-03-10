import numpy as np

def f1(x):
    return 3 * x ** 3 + 2 * x ** 2 - 1


def f2(x):
    return np.exp(x) - 2 * x - 2


def f3(x):
    return np.sin(x) - 0.2


def fun_31(x, y):
    return x**2 + y**2 - 20


def fun_32(x, y):
    return x*y - 20


def fun_11(x, y):
    return x + y - 3


def fun_12(x, y):
    return x**3 + (x**2) * y - 12


def fun_21(x, y):
    return x**3 + (y**3) - 7


def fun_22(x, y):
    return x * y * (x + y) + 2


system_1 = [fun_11, fun_12]
system_2 = [fun_21, fun_22]
system_3 = [fun_31, fun_32]
