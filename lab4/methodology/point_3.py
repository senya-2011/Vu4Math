"""
Сформировать массивы предполагаемых эмпирических
зависимостей (Y(x_i), E_i)
"""

import math
import lab.methodology.point_2 as point_2

def generate_all_predictions(x_list, y_list):
    models = [
        ('Linear', point_2.approx_linear),
        ('Quadratic', point_2.approx_quadratic),
        ('Cubic', point_2.approx_cubic),
        ('Exponential', point_2.approx_exponential),
        ('Logarithmic', point_2.approx_logarithmic),
        ('Power', point_2.approx_power),
    ]
    all_preds = []
    for name, approx_fn in models:
        coeffs = approx_fn(x_list, y_list)
        y_pred = []
        for x in x_list:
            if name == 'Linear':
                a, b = coeffs
                y_pred.append(a * x + b)
            elif name == 'Quadratic':
                a, b, c = coeffs
                y_pred.append(a * x**2 + b * x + c)
            elif name == 'Cubic':
                a, b, c, d = coeffs
                y_pred.append(a * x**3 + b * x**2 + c * x + d)
            elif name == 'Exponential':
                a, b = coeffs
                y_pred.append(a * math.exp(b * x))
            elif name == 'Logarithmic':
                a, b = coeffs
                y_pred.append(a + b * math.log(x) if x > 0 else float('nan'))
            elif name == 'Power':
                a, b = coeffs
                y_pred.append(a * (x**b) if x > 0 else float('nan'))
        all_preds.append((name, coeffs, y_pred))
    return all_preds