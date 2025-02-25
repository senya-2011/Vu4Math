import flet as ft
from flet_core import FilePickerResultEvent

import matrix_operations.matrix
import matrix_operations.read_matrix
import matrix_operations.random_matrix

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    def file_pick(e: FilePickerResultEvent):
        try:
            path = e.files[0].path
            matrix, eps = matrix_operations.read_matrix.read_matrix(path)
            result = matrix_operations.matrix.check_matrix(matrix, eps)
            output_text.value = result
            set_matrix_from_file(matrix, eps)
            page.update()
        except:
            output_text.value = "Неправильный файл!\nфайл должен состоять из матрицы + точности на последней строчке"
            page.update()

    def generate_matrix(e):
        set_matrix_from_file(matrix_operations.random_matrix.create_random_matrix(int(size_input.value)), float_input.value)

    def set_matrix_from_file(matrix, eps):

        float_input.value = str(eps)
        matrix_container.controls.clear()
        size_input.value = len(matrix)
        for row in matrix:
            row_controls = [ft.TextField(value=str(num), width=50) for num in row]
            matrix_container.controls.append(ft.Row(row_controls))

        page.update()

    page.title = "Вычислительная математика Лабораторная 1 | Алхимовици Арсений P3210"

    size_input = ft.TextField(label="Введите размер матрицы (от 1 до 20)", keyboard_type=ft.KeyboardType.NUMBER,
                              width=200, value="2")
    float_input = ft.TextField(label="Введите точность", keyboard_type=ft.KeyboardType.NUMBER, width=200, value="0.01")

    matrix_container = ft.Column()

    output_text = ft.Text(value="", size=16, width=600)

    scrollable_matrix = ft.ListView(
        controls=[matrix_container],
        height=300,
        width=1200,
        spacing=10
    )

    def update_matrix(e):
        size = size_input.value
        if size.isdigit() and 1 <= int(size) <= 20:
            size = int(size)
            matrix_container.controls.clear()

            for i in range(size):
                row = []
                for j in range(size + 1):
                    row.append(ft.TextField(value="1", width=50))
                matrix_container.controls.append(ft.Row(row))
            size_input.error_text = None
            page.update()
        else:
            size_input.error_text = "Число должно быть от 1 до 20"
            page.update()

    def calculate_matrix(e):
        try:
            size = int(size_input.value)
            if 0 < size <= 20:
                matrix = []
                for i in range(size):
                    row = []

                    for j in range(size + 1):
                        value = matrix_container.controls[i].controls[j].value.replace(",", ".")
                        row.append(float(value))
                    if len(row) != size + 1:
                        raise ValueError("Неверное количество элементов в строке.")
                    matrix.append(row)

                print("Матрица:")
                for row in matrix:
                    print(row)

                result = matrix_operations.matrix.check_matrix(matrix, float(float_input.value))

                output_text.value = result
                page.update()

            else:
                raise ValueError("Неверный размер матрицы!")
        except Exception as ex:
            output_text.value = f"Ошибка: {ex}"
            page.update()

    generate_button = ft.ElevatedButton("Создать матрицу", on_click=update_matrix)
    generate_random_button = ft.ElevatedButton("Создать рандомную матрицу", on_click=generate_matrix)
    calculate_button = ft.ElevatedButton("Посчитать", on_click=calculate_matrix)

    file_picker = ft.FilePicker(on_result=file_pick)
    page.overlay.append(file_picker)
    file_button = ft.ElevatedButton(
                 "Выбрать файл",
                 icon=ft.icons.FOLDER_OPEN,
                 on_click=lambda _: file_picker.pick_files(allow_multiple=True),
             )
    page.add(ft.Row([size_input, float_input, file_button, generate_random_button]), generate_button, scrollable_matrix, calculate_button,
             ft.Container(
                 ft.Column([output_text], scroll=True),
                 expand=True,
                 height=200,
                 border=ft.border.all(1),
                 padding=10
             )
             )

    update_matrix(None)

ft.app(target=main)
