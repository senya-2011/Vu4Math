"""
Уточнить значения коэффициентов эмпирических функций,
минимизируя функцию S
"""

import math
import lab.methodology.logic as logic

# линейная аппроксимация: y = a*x + b
def approx_linear(x_list, y_list):
    design = [[x, 1.0] for x in x_list]
    return logic.solve_normal_equations(design, y_list)


# квадратичная аппроксимация: y = a*x^2 + b*x + c
def approx_quadratic(x_list, y_list):
    design = [[x ** 2, x, 1.0] for x in x_list]
    return logic.solve_normal_equations(design, y_list)


# кубическая аппроксимация: y = a*x^3 + b*x^2 + c*x + d
def approx_cubic(x_list, y_list):
    design = [[x ** 3, x ** 2, x, 1.0] for x in x_list]
    return logic.solve_normal_equations(design, y_list)


# экспоненциальная аппроксимация: y = a * exp(b*x)
def approx_exponential(x_list, y_list):
    # логарифмируем y, чтобы получить линейную зависимость ln(y) = ln(a) + b*x
    design = [[1.0, x] for x in x_list]
    y_log = [math.log(y_i) for y_i in y_list]
    ln_coeffs = logic.solve_normal_equations(design, y_log)
    a = math.exp(ln_coeffs[0])  # восстановление a
    b = ln_coeffs[1]
    return [a, b]


# логарифмическая аппроксимация: y = a + b*ln(x)
def approx_logarithmic(x_list, y_list):
    design = [[1.0, math.log(x)] for x in x_list]
    return logic.solve_normal_equations(design, y_list)


# степенная аппроксимация: y = a * x^b
def approx_power(x_list, y_list):
    # берем логарифмы: ln(y) = ln(a) + b*ln(x)
    design = [[1.0, math.log(x)] for x in x_list]
    y_log = [math.log(y_i) for y_i in y_list]
    ln_coeffs = logic.solve_normal_equations(design, y_log)
    a = math.exp(ln_coeffs[0])
    b = ln_coeffs[1]
    return [a, b]
