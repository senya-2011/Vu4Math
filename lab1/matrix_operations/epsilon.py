def get_epsilon():
    while True:
        try:
            return float(input("Введите точнось: ").strip())
        except ValueError:
            print("Нужно ввести число!")