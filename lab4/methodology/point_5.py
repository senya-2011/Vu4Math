import os
import math
import matplotlib.pyplot
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import lab.methodology.point_3 as point_3
import lab.methodology.point_4 as point_4
import lab.methodology.task_4_5 as task_4_5

RESULT_DIR = 'static/result'


def save_approximation_plot(x_list, y_list, model_name, coeffs,
                             xmin_bound=None, xmax_bound=None,
                             ymin_bound=None, ymax_bound=None,
                             filename=None):
    """
    Сохраняет график для одной модели, с возможностью задания отдельных границ:
      xmin_bound, xmax_bound — границы по оси X
      ymin_bound, ymax_bound — границы по оси Y
    """
    # формируем плотный диапазон X
    x_min, x_max = min(x_list), max(x_list)
    delta = (x_max - x_min) * 0.1
    xs = [x_min - delta + i * (x_max - x_min + 2 * delta) / 500 for i in range(501)]

    # вычисляем аппроксимацию
    y_pred = []
    for x in xs:
        if model_name == 'Linear':
            a, b = coeffs; y_pred.append(a * x + b)
        elif model_name == 'Quadratic':
            a, b, c = coeffs; y_pred.append(a * x**2 + b * x + c)
        elif model_name == 'Cubic':
            a, b, c, d = coeffs; y_pred.append(a * x**3 + b * x**2 + c * x + d)
        elif model_name == 'Exponential':
            a, b = coeffs; y_pred.append(a * math.exp(b * x))
        elif model_name == 'Logarithmic':
            a, b = coeffs; y_pred.append(a + b * math.log(x) if x > 0 else float('nan'))
        elif model_name == 'Power':
            a, b = coeffs; y_pred.append(a * (x**b) if x > 0 else float('nan'))
        else:
            raise ValueError(f"Unknown model: {model_name}")

    # строим фигуру
    plt.figure()
    plt.scatter(x_list, y_list, label='data', color='black')
    plt.plot(xs, y_pred, label=model_name)
    plt.title(f"Approximation: {model_name}")
    plt.xlabel('x'); plt.ylabel('y')
    plt.legend(); plt.grid(True)

    # применение отдельных границ
    if xmin_bound is not None and xmax_bound is not None:
        plt.xlim(xmin_bound, xmax_bound)
    if ymin_bound is not None and ymax_bound is not None:
        plt.ylim(ymin_bound, ymax_bound)

    # сохранение
    fname = filename or f"{model_name.lower()}_plot.png"
    path = os.path.join(RESULT_DIR, fname)
    plt.savefig(path); plt.close()
    return path


def save_combined_plot(x_list, y_list, predictions,
                       xmin_bound=None, xmax_bound=None,
                       ymin_bound=None, ymax_bound=None,
                       filename='combined_plot.png'):
    """
    Сохраняет общий график всех моделей, с отдельными границами:
      xmin_bound, xmax_bound — для X
      ymin_bound, ymax_bound — для Y
    """
    x_min, x_max = min(x_list), max(x_list)
    delta = (x_max - x_min) * 0.1
    xs = [x_min - delta + i * (x_max - x_min + 2 * delta) / 500 for i in range(501)]

    plt.figure()
    plt.scatter(x_list, y_list, label='data', color='black')
    for name, coeffs, _ in predictions:
        ys = []
        for x in xs:
            if name == 'Linear': a, b = coeffs; ys.append(a * x + b)
            elif name == 'Quadratic': a, b, c = coeffs; ys.append(a * x**2 + b * x + c)
            elif name == 'Cubic': a, b, c, d = coeffs; ys.append(a * x**3 + b * x**2 + c * x + d)
            elif name == 'Exponential': a, b = coeffs; ys.append(a * math.exp(b * x))
            elif name == 'Logarithmic': a, b = coeffs; ys.append(a + b * math.log(x) if x > 0 else float('nan'))
            elif name == 'Power': a, b = coeffs; ys.append(a * (x**b) if x > 0 else float('nan'))
        plt.plot(xs, ys, label=name)
    plt.title('All Approximations')
    plt.xlabel('x'); plt.ylabel('y')
    plt.legend(); plt.grid(True)

    # отдельные границы
    if xmin_bound is not None and xmax_bound is not None:
        plt.xlim(xmin_bound, xmax_bound)
    if ymin_bound is not None and ymax_bound is not None:
        plt.ylim(ymin_bound, ymax_bound)

    path = os.path.join(RESULT_DIR, filename)
    plt.savefig(path); plt.close()
    return path


def run_full_pipeline(x_list, y_list, save_plots=True,
                      xmin_bound=None, xmax_bound=None,
                      ymin_bound=None, ymax_bound=None):
    """
    Вычисляет все модели, сохраняет графики с указанными границами:
    xmin_bound, xmax_bound, ymin_bound, ymax_bound — отдельные границы.
    """
    results, best = point_4.evaluate_and_select_best(x_list, y_list)
    predictions = point_3.generate_all_predictions(x_list, y_list)
    stats = task_4_5.calc_r2_and_pearson(x_list, y_list)

    plots = {}
    if save_plots:
        for name, coeffs, _ in predictions:
            plots[name] = save_approximation_plot(
                x_list, y_list, name, coeffs,
                xmin_bound, xmax_bound,
                ymin_bound, ymax_bound)
        plots['Combined'] = save_combined_plot(
            x_list, y_list, predictions,
            xmin_bound, xmax_bound,
            ymin_bound, ymax_bound)

    return {
        'predictions': predictions,
        'results': results,
        'best': best,
        'stats': stats,
        'plots': plots
    }
