"""
Главный скрипт для выбора ОДУ и метода решения, вывода таблицы и графика.
"""

import math
from logic.euler import solve_euler, runge_error as runge_error_euler
from logic.runge_kutta import solve_rk4, runge_error as runge_error_rk4
from logic.adams import solve_adams4, max_error_adams

def ode1():
    def f(x, y):
        return y
    def exact(x, x0, y0):
        return y0 * math.exp(x - x0)
    desc = "y' = y"
    return f, exact, desc

def ode2():
    def f(x, y):
        return x - 2*y
    def exact(x, x0, y0):
        C = y0 - (x0/2 - 0.25)
        return x/2 - 0.25 + C * math.exp(-2*(x - x0))
    desc = "y' = x - 2y"
    return f, exact, desc

def ode3():
    def f(x, y):
        return y * (1 - y)
    def exact(x, x0, y0):
        return 1.0 / (1.0 + ((1 - y0) / y0) * math.exp(-(x - x0)))
    desc = "y' = y*(1 - y) (логистическое)"
    return f, exact, desc

def choose_ode():
    print("Выберите номер ОДУ:")
    print("1 - y' = y")
    print("2 - y' = x - 2y")
    print("3 - y' = y*(1 - y)")
    choice = input("Номер (1/2/3): ").strip()
    if choice == '1':
        return ode1()
    elif choice == '2':
        return ode2()
    elif choice == '3':
        return ode3()
    else:
        print("Неверный выбор. Берём ODE1 по умолчанию.")
        return ode1()

def input_float(prompt, default):
    """
    Считывает число с плавающей точкой, если пусто - возвращает default.
    """
    s = input(f"{prompt} [по умолчанию {default}]: ").strip()
    return float(s) if s else default

def choose_methods():
    """
    Читает строку, где пользователь вводит номера методов через запятую или пробел.
    Возвращает список уникальных строк-выборов ('1', '2', '3').
    """
    print("Выберите методы решения (через запятую или пробел):")
    print("1 - Метод Эйлера")
    print("2 - Метод Рунге–Кутты 4-го порядка")
    print("3 - Метод Адамса 4-го порядка (предиктор-корректор)")
    s = input("Номера (например, 1,2,3 или 1 3): ").strip()
    # Разбиваем по запятой или пробелу
    for sep in [',', ' ']:
        if sep in s:
            parts = [p.strip() for p in s.split(sep) if p.strip()]
            break
    else:
        parts = [s] if s else []
    # Оставляем только 1,2,3
    methods = []
    for p in parts:
        if p in ('1', '2', '3') and p not in methods:
            methods.append(p)
    if not methods:
        print("Ничего не выбрано, берём метод Эйлера по умолчанию.")
        return ['1']
    return methods

def main():
    # Выбор ОДУ
    f, exact_func, ode_desc = choose_ode()
    print(f"Выбрано ОДУ: {ode_desc}\n")

    # Ввод параметров
    x0 = input_float("Введите x0", 0.0)
    y0 = input_float("Введите y0", 1.0)
    xn = input_float("Введите xn (конечное значение x)", 1.0)
    h = input_float("Введите шаг h", 0.1)
    eps = input_float("Введите точность eps для оценки по Рунге", 1e-6)
    print()

    # Выбор нескольких методов
    methods = choose_methods()
    print(f"Выбраны методы: {', '.join(methods)}\n")

    # Список для хранения результатов (xs общий, solutions: [(ys_num, label)])
    xs = None
    solutions = []
    ys_exact = None

    # Обходим выбранные методы
    for m in methods:
        if m == '1':
            xs_e, ys_e = solve_euler(f, x0, y0, xn, h)
            if xs is None:
                xs = xs_e
                ys_exact = [exact_func(xi, x0, y0) for xi in xs]
            # Оценка погрешности по Рунге (в конце)
            err_est = runge_error_euler(f, x0, y0, xn, h, solve_euler, p=1)
            print(f"[Эйлер] Оценка погрешности по Рунге (на xn): {err_est:.6e}")
            solutions.append((ys_e, "Эйлер (p=1)"))

        elif m == '2':
            xs_rk, ys_rk = solve_rk4(f, x0, y0, xn, h)
            if xs is None:
                xs = xs_rk
                ys_exact = [exact_func(xi, x0, y0) for xi in xs]
            # Оценка погрешности по Рунге (в конце)
            err_est = runge_error_rk4(f, x0, y0, xn, h, solve_rk4, p=4)
            print(f"[Рунге–Кутты 4] Оценка погрешности по Рунге (на xn): {err_est:.6e}")
            solutions.append((ys_rk, "РК4 (p=4)"))

        elif m == '3':
            xs_ad, ys_ad = solve_adams4(f, x0, y0, xn, h)
            if xs is None:
                xs = xs_ad
                ys_exact = [exact_func(xi, x0, y0) for xi in xs]
            # Оценка погрешности по сравнению с точным
            err_est = max_error_adams(lambda x: exact_func(x, x0, y0), xs_ad, ys_ad)
            print(f"[Адамс 4] Макс. абсолютная погрешность (метод Адамса): {err_est:.6e}")
            solutions.append((ys_ad, "Адамс 4"))

    print("\nТаблица значений (x, y_num, y_exact, |error|) для каждого метода:")
    print("================================================================")
    # Выводим сразу по всем методам: для каждого x показываем ряд значений
    header = "   x    "
    for _, label in solutions:
        header += f" |  {label.center(12)}"
    header += " |   y_exact   |"
    print(header)
    # Строка форматирования: сначала x, потом для каждого метода y_num, потом y_exact
    for i, xi in enumerate(xs):
        row = f"{xi:8.6f} "
        for ys_num, _ in solutions:
            yi_num = ys_num[i]
            row += f" {yi_num:12.6f} "
        yi_ex = ys_exact[i]
        row += f" {yi_ex:12.6f} |"
        print(row)

    # Построение одного графика для всех методов
    title = f"Численное решение ({ode_desc}), h={h}"
    plot_multiple_solutions(xs, solutions, ys_exact, title=title)

if __name__ == "__main__":
    main()
