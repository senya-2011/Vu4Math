import os

def read_xy_from_txt_filepath(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        return read_xy_from_txt_file(file)

def read_xy_from_txt_file(file):
    lines = file.readlines()

    if len(lines) != 2:
        raise ValueError("Файл должен содержать две строки (x и y)")

    def parse_line(line):
        tokens = line.replace(',', '.').split()
        if not (8 <= len(tokens) <= 12):
            raise ValueError("Каждая строка должна содержать от 8 до 12 чисел")
        try:
            return [float(tok) for tok in tokens]
        except ValueError as e:
            raise ValueError(f"Невозможно преобразовать значение в число: {e}")

    x_list = parse_line(lines[0])
    y_list = parse_line(lines[1])

    if len(x_list) != len(y_list):
        raise ValueError(
            f"Длины списков x ({len(x_list)}) и y ({len(y_list)}) не совпадают"
        )
    x_list = parse_line(lines[0])
    if any(x <= 0 for x in x_list):
        raise ValueError("Все значения X должны быть больше 0")
    return x_list, y_list