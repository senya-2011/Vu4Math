import funcs
import methods
import utils

def main():
    print("Функции:")
    for k, (name, _, _, disc) in funcs.FUNCTIONS.items():
        status = f"разрыв в {disc}" if disc is not None else "непрерывна"
        print(f"{k}. {name}  |  {status}")

    choice = int(utils.get_float(
        "Выберите функцию (1-5): ",
        condition=lambda x: 1 <= x <= len(funcs.FUNCTIONS),
        error_msg="Введите целое число от 1 до 5."
    ))
    name, f, F, disc = funcs.FUNCTIONS[choice]

    a = utils.get_float("Введите a: ")
    b = utils.get_float("Введите b (> a): ",
                        condition=lambda x: x > a,
                        error_msg="b должно быть больше a.")
    eps = utils.get_float("Точность (0<eps<1): ",
                         condition=lambda x: 0 < x < 1,
                         error_msg="Точность должна быть в (0,1).")

    # Проверка крайних точек на совпадение с точкой разрыва
    if disc is not None:
        if a == disc:
            print("Точка a совпадает с точкой разрыва.")
            return
        if b == disc:
            print("Точка b совпадает с точкой разрыва.")
            return

    # Разбиваем [a, b] на сегменты, исключая окрестность точки разрыва
    segments = []
    if disc is not None and a < disc < b:
        max_delta = min(disc - a, b - disc)
        delta = utils.get_float(
            f"Введите отступ δ от точки разрыва {disc} (0 < δ < {max_delta:.6g}): ",
            condition=lambda d: 0 < d < max_delta,
            error_msg=f"δ должно быть >0 и < {max_delta:.6g}."
        )
        segments.append((a, disc - delta))
        segments.append((disc + delta, b))
    else:
        segments.append((a, b))

    # Точное значение интеграла через первообразную на каждом сегменте
    exact = sum(F(x2) - F(x1) for x1, x2 in segments)
    print(f"\nТочное значение интеграла: {exact}")

    methods_map = {
        1: (methods.mid_rectangle, 2, "Средние прям."),
        2: (methods.left_rectangle, 2, "Левые прям."),
        3: (methods.right_rectangle, 2, "Правые прям."),
        4: (methods.trapezoid, 2, "Трапеции"),
        5: (methods.simpson, 4, "Симпсон"),
    }

    print("\nВыберите метод:")
    for k, (_, _, nm) in methods_map.items():
        print(f"{k}. {nm}")
    print("6. Все методы сразу")

    m = int(utils.get_float(
        "Ваш выбор: ",
        condition=lambda x: 1 <= x <= 6,
        error_msg="Введите число от 1 до 6."
    ))
    choices = [m] if m != 6 else list(methods_map.keys())

    for key in choices:
        method, order, label = methods_map[key]
        total, iters = 0.0, 0
        for a1, b1 in segments:
            res, cnt = methods.approximate(method, f, a1, b1, eps, 4, order)
            total += res
            iters += cnt
        err = methods.runge_error(total, exact, order)
        print(f"\n{label}: значение = {total}, погрешность = {err*100:.6f}%, итераций = {iters}")

if __name__ == '__main__':
    while True:
        main()
