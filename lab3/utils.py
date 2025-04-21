def get_float(prompt, condition=lambda x: True, error_msg="Неверный ввод."):
    while True:
        try:
            v = float(input(prompt).replace(',', '.'))
            if condition(v):
                return v
            print(error_msg)
        except ValueError:
            print(error_msg)