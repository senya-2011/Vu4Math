import funcs
import methods
import utils

def main():
    print("Доступные функции:")
    for k, (name, _, _, disc) in funcs.FUNCTIONS.items():
        status = f"разрыв в {disc}" if disc is not None else "непрерывна"
        print(f"{k}. {name}  |  {status}")

    choice = int(utils.get_float("Выберите функцию (1-5): ",
                                 condition=lambda x: 1 <= x <= len(funcs.FUNCTIONS)))
    name, f, F, disc = funcs.FUNCTIONS[choice]

    a = utils.get_float("Введите a: ")
    b = utils.get_float("Введите b (> a): ", condition=lambda x: x > a)
    eps = utils.get_float("Точность (0<eps<1): ", condition=lambda x: 0 < x < 1)

    if disc is not None:
        delta = utils.get_float("Отступ от точки разрыва: ")
        if a == disc: a += delta
        if b == disc: b -= delta

    # сегментация при разрыве
    segments = [(a, b)]
    if disc is not None and a < disc < b:
        segments = [(a, disc - delta), (disc + delta, b)]

    exact = sum(F(x2) - F(x1) for x1, x2 in segments)
    print(f"\nТочное значение интеграла: {exact}")

    methods_map = {
        1: (methods.mid_rectangle, 2, "Средние прям."),
        2: (methods.left_rectangle, 2, "Левые прям."),
        3: (methods.right_rectangle, 2, "Правые прям."),
        4: (methods.trapezoid, 2, "Трапеции"),
        5: (methods.simpson, 4, "Симпсон"),
    }

    print("Выберите метод (1-5) или 6-все:")
    for k, (_, _, nm) in methods_map.items(): print(f"{k}. {nm}")
    print("6. Все методы")

    m = int(utils.get_float("Ваш выбор: ", condition=lambda x: 1 <= x <= 6))
    choices = [m] if m != 6 else list(methods_map.keys())

    for key in choices:
        method, order, label = methods_map[key]
        total, iters = 0, 0
        for a1, b1 in segments:
            res, cnt = methods.approximate(method, f, a1, b1, eps, 4, order)
            total += res; iters += cnt
        err = methods.runge_error(total, exact, order)
        print(f"\n{label}: значение={total}, погр={err*100:.6f}%, итераций={iters}")

if __name__ == '__main__':
    main()
