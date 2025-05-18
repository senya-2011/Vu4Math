"""
Определить среднеквадратичное отклонение для каждой
аппроксимирующей функции. Выбрать наименьшее значение и,
следовательно, наилучшее приближение
"""

import lab.methodology.point_3 as point_3
import lab.methodology.point_1 as point_1

def evaluate_and_select_best(x_list, y_list):
    all_preds = point_3.generate_all_predictions(x_list, y_list)
    results = []
    for name, coeffs, y_pred in all_preds:
        errors = [y - yp for y, yp in zip(y_list, y_pred)]
        mse = point_1.calc_measure_of_deviation(errors)
        results.append({
            'name': name,
            'coeffs': coeffs,
            'mse': mse
        })
    # находим модель с наименьшим MSE
    best = min(results, key=lambda r: r['mse'])
    return results, best
