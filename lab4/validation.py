def validate(input_str):
    lines = [line.strip() for line in input_str.splitlines() if line.strip()]
    if len(lines) != 2:
        raise ValueError(f"Ожидаются ровно две непустые строки, получено {len(lines)}")

    def parse_line(line, name):
        # Заменяем запятые на точки
        norm = line.replace(',', '.')
        tokens = norm.split()
        if not tokens:
            raise ValueError(f"Строка {name} пуста после разбиения")
        nums = []
        for tok in tokens:
            try:
                num = float(tok)
            except ValueError:
                raise ValueError(f"Невозможно преобразовать '{tok}' в число в строке {name}")
            nums.append(num)
        return nums

    x_list = parse_line(lines[0], 'X')
    y_list = parse_line(lines[1], 'Y')

    if len(x_list) != len(y_list):
        raise ValueError(f"Длина X ({len(x_list)}) и Y ({len(y_list)}) не совпадают")

    return x_list, y_list
