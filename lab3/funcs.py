import math

# Определение функций и их первообразных в виде словаря:
# ключ: номер варианта
# значение: (название, функция, первообразная, точка разрыва или None)
FUNCTIONS = {
    1: ("sin(x)", lambda x: math.sin(x), lambda x: -math.cos(x), None),
    2: ("exp(x)", lambda x: math.exp(x), lambda x: math.exp(x), None),
    3: ("1/x^2", lambda x: 1/x**2, lambda x: -1/x, 0),
    4: ("1/(1+x^2)", lambda x: 1/(1+x**2), lambda x: math.atan(x), None),
    5: ("ln(x)", lambda x: math.log(x), lambda x: x*math.log(x)-x, 0),
}