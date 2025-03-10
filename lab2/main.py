import logic.chord_method
import logic.newton_method
import logic.simple_iteration_method
import logic.properties as properties
import math

def input_check(user_input):
    user_input = user_input.replace(" ", "")
    user_input = user_input.replace(",", ".")
    try:
        user_input = float(user_input)
    except:
        raise ValueError("Введите float!")

    return user_input

def f1(x):
    return round(x**3 - 2*x - 2, properties.def_round)

def f2(x):
    return round(math.exp(x) - 2*x - 2, properties.def_round)

def f3(x):
    return round(math.sin(x) + 0.5, properties.def_round)

def f4(x):
    return round(x**2 - 2, properties.def_round)

def f1_sys(x, y):
    return round(x - 0.3 + 0.1 * y ** 2, properties.def_round)


def f2_sys(x, y):
    return round(y - 0.7 + 0.2 * x ** 2, properties.def_round)

system_1 = [f1_sys, f2_sys]

print(logic.chord_method.calculate(f2, 1, 2))
print(logic.newton_method.calculate(f2, 1))
print(logic.simple_iteration_method.calculate(f2, 1, 2))
print(logic.newton_method.calculate_system(system_1, 0.1, 0.2))