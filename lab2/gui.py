import flet as ft
import tasks.tasks_fun as tasks
import logic.chord_method
import logic.newton_method
import logic.simple_iteration_method
import logic.plot_builder as plot
import logic.properties as properties
import os
import glob


def main(page):
    def format_output(method_name, f, x, iters):
        if f == 0 and x == 0 and iters == 0:
            return f"{method_name}: не сошлось за максимально кол-во итераций\n\n"
        else:
            return (f"{method_name}:\n"
                    f"Итераций: {iters}\n"
                    f"x = {x:.6f}\n"
                    f"f(x) = {f:.6f}\n\n")

    page.window_height = 1000
    page.title = "Алхимовици Арсений  | P3210 | Лаб2"
    page.theme_mode = ft.ThemeMode.LIGHT

    graph_image = ft.Image(src="./graph.png")
    graph_image2 = ft.Image(src="./graph.png")

    def input_check(user_input):
        user_input = user_input.replace(" ", "")
        user_input = user_input.replace(",", ".")
        try:
            user_input = float(user_input)
        except:
            raise ValueError("Введите float!")

        return user_input

    def button_clicked_page_1(e):
        if cg.value == "1":
            fun = tasks.f1
        elif cg.value == "2":
            fun = tasks.f2
        else:
            fun = tasks.f3

        a_value = input_check(a.value)
        b_value = input_check(b.value)
        c_value = input_check(c.value)
        f_chord, x_chord, iters_chord = logic.chord_method.calculate(fun, a_value, b_value, c_value)
        f_newton, x_newton, iters_newton = logic.newton_method.calculate(fun, (a_value + b_value) / 2, c_value)
        f_simple, x_simple, iters_simple = logic.simple_iteration_method.calculate(fun, a_value, b_value, c_value)

        output = format_output("Метод хорд", f_chord, x_chord, iters_chord) + \
                 format_output("Метод Ньютона", f_newton, x_newton, iters_newton) + \
                 format_output("Метод простой итерации", f_simple, x_simple, iters_simple)

        t.value = output

        files = glob.glob("graph*.png")

        for file in files:
            try:
                os.remove(file)
            except Exception as e:
                pass

        properties.img_i += 1
        plot.makeplot(fun, a_value, b_value)
        graph_image.src = f"./graph{properties.img_i}.png"
        graph_image.update()

        page.update()

    def button_clicked_page_2(e):
        if cg2.value == "1":
            fun = tasks.system_1
        elif cg2.value == "2":
            fun = tasks.system_2
        else:
            fun = tasks.system_3

        x_value = input_check(x0.value)
        y_value = input_check(y0.value)
        eps_value = input_check(eps.value)

        x, y, max_iter, errors, jacobian_matrix = logic.newton_method.calculate_system(fun, x_value, y_value, eps_value)

        if(max_iter==properties.max_iter or max_iter==0):
            output = f"Метод Ньютона:\n" \
                     f"Матрица Якоба: {jacobian_matrix}\n" \
                     f"Метод не сошелся\n"
        else:
            output = f"Метод Ньютона:\n" \
                     f"Матрица Якоба: {jacobian_matrix}\n" \
                     f"Итераций: {max_iter}\n" \
                     f"x = {x:.6f}, y = {y:.6f}\n" \
                     f"Вектор погрешности: \n"
            error_str = "".join([f"Итерация {i}: [Δx={dx:.6f}, Δy={dy:.6f}]\n" for i, (dx, dy) in enumerate(errors, 1)])
            output += error_str

        t2.value = output

        files = glob.glob("graph*.png")

        for file in files:
            try:
                os.remove(file)
            except Exception as e:
                pass

        properties.img_i += 1
        plot.makeplot_system(fun[0], fun[1], x_value, y_value)
        graph_image2.src = f"./graph{properties.img_i}.png"
        graph_image2.update()

        page.update()

    t = ft.Text()
    t2 = ft.Text()

    button1 = ft.ElevatedButton(text='Рассчитать', on_click=button_clicked_page_1)

    button2 = ft.ElevatedButton(text='Рассчитать', on_click=button_clicked_page_2)

    cg = ft.RadioGroup(content=ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Radio(value=1),
                ft.Image(src="images/img4.png", width=200, height=100),
            ])
        ),
        ft.Container(
            content=ft.Row([
                ft.Radio(value=2),
                ft.Image(src="images/img5.png", width=200, height=100),
            ])
        ),
        ft.Container(
            content=ft.Row([
                ft.Radio(value=3),
                ft.Image(src="images/img6.png", width=200, height=100),
            ])
        ),
    ]))

    cg2 = ft.RadioGroup(content=ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Radio(value=1),
                ft.Image(src="images/img1.png", width=200, height=100),
            ])
        ),
        ft.Container(
            content=ft.Row([
                ft.Radio(value=2),
                ft.Image(src="images/img2.png", width=200, height=100),
            ])
        ),
        ft.Container(
            content=ft.Row([
                ft.Radio(value=3),
                ft.Image(src="images/img3.png", width=200, height=100),
            ])
        ),
    ]))

    a = ft.TextField(label="a", value="1")
    b = ft.TextField(label="b", value="5")
    c = ft.TextField(label="eps", value="0.01")

    x0 = ft.TextField(label="x0", value="1")
    y0 = ft.TextField(label="y0", value="5")
    eps = ft.TextField(label="eps", value="0.01")

    def switch_page(e):
        page.controls.clear()

        page.add(page_mode)

        if page_mode.value == "Уравнения":
            page.add(
                ft.Row([

                    ft.Column([
                        ft.Row([a, b, c]),
                        ft.Text("Выберите вариант:"),
                        cg,
                        button1,
                        t
                    ], expand=1),

                    ft.Container(
                        graph_image,
                        alignment=ft.alignment.center_right,
                        expand=0
                    )
                ], expand=True)
            )
        elif page_mode.value == "Система Уравнений":
            page.add(
                ft.Row([
                    ft.Column([
                        ft.Row([x0, y0, eps]),
                        ft.Text("Выберите вариант:"),
                        cg2,
                        button2,
                        t2
                    ], expand=1),

                    ft.Container(
                        graph_image2,
                        alignment=ft.alignment.center_right,
                        expand=0
                    )
                ], expand=True)
            )

        page.update()

    page_mode = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="Уравнения", label="Уравнения"),
        ft.Radio(value="Система Уравнений", label="Система Уравнений")
    ]), on_change=switch_page)

    switch_page(None)


ft.app(main)
