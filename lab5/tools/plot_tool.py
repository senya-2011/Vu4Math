# tools/plot_utils.py

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_interpolation(xs, ys, x_val, methods_dict, num_points=500):
    """
    Строит:
      - интерполяционные полиномы из methods_dict (сплошная линия с t).
      - узловые точки и точку интерполяции
    methods_dict: {name: func(xs, ys, x) -> (poly_func, t)}
    """
    # Диапазон
    x_min, x_max = min(xs), max(xs)
    dx = (x_max - x_min) * 0.02 if x_max > x_min else 1.0
    x_vals = [x_min - dx + i * (x_max - x_min + 2 * dx) / num_points for i in range(num_points + 1)]

    # Создаем фигуру с увеличенным размером
    fig, ax = plt.subplots(figsize=(12, 8), dpi=100)

    # Интерполяционные многочлены
    for name, func in methods_dict.items():
        try:
            poly, t = func(xs, ys, x_val)
            y_interp = [poly(x) for x in x_vals]
            ax.plot(x_vals, y_interp, label=f"{name} (t={t:.3f})")
        except Exception as e:
            print(f"Error plotting {name}: {str(e)}")
            continue

    # Узловые точки и точка оценки
    ax.scatter(xs, ys, color='black', label='Узлы', zorder=5)
    try:
        # Первый полином для точки
        first_poly, _ = next(func(xs, ys, x_val) for func in methods_dict.values())
        y0 = first_poly(x_val)
        ax.scatter([x_val], [y0], color='red', s=100, label='Интерп. точка', zorder=6)
    except (StopIteration, AttributeError):
        pass

    # Настройка осей и легенды
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Интерполяция методов', fontsize=14, pad=20)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Выносим легенду за пределы графика
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        fontsize=10,
        frameon=True,
        shadow=True
    )

    # Автоматическая подгонка layout
    plt.tight_layout()

    return fig