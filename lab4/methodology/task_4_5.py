"""
4. Для линейной зависимости вычислить коэффициент корреляции
Пирсона;
5. Вычислить коэффициент детерминации, программа должна
выводить соответствующее сообщение в зависимости от
полученного значения R^2;
"""

import math
from lab.methodology.point_3 import generate_all_predictions


def calc_r2_and_pearson(x_list, y_list):
    """
      {
        'name': имя модели,
        'r2': значение R^2,
        'pearson_r': значение R для линейной или None,
        'reliability': строка с оценкой качества
      }
    """
    predictions = generate_all_predictions(x_list, y_list)
    mean_y = sum(y_list) / len(y_list)
    stats = []
    for name, coeffs, y_pred in predictions:
        ss_res = sum((y - yp) ** 2 for y, yp in zip(y_list, y_pred))
        ss_tot = sum((y - mean_y) ** 2 for y in y_list)
        r2 = 1 - ss_res / ss_tot if ss_tot != 0 else None
        pearson_r = None
        if name == 'Linear':
            mean_x = sum(x_list) / len(x_list)
            cov = var_x = var_y = 0.0
            for x, y in zip(x_list, y_list):
                dx = x - mean_x
                dy = y - (sum(y_list) / len(y_list))
                cov += dx * dy
                var_x += dx ** 2
                var_y += dy ** 2
            pearson_r = cov / math.sqrt(var_x * var_y) if var_x and var_y else None
        if r2 is None:
            reliability = 'Невозможно вычислить R²'
        elif r2 >= 0.95:
            reliability = 'Высокая точность аппроксимации (модель хорошо описывает явление)'
        elif r2 >= 0.75:
            reliability = 'Удовлетворительная аппроксимация (модель в целом адекватно описывает явление)'
        elif r2 >= 0.5:
            reliability = 'Слабая аппроксимация (модель слабо описывает явление)'
        else:
            reliability = 'Точность аппроксимации недостаточна и модель требует изменения'
        stats.append({
            'name': name,
            'r2': r2,
            'pearson_r': pearson_r,
            'reliability': reliability
        })
    return stats
