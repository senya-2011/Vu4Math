import logic.properties as properties
import logic.derivative_function as derivative_fun


def calculate(f, a, b, eps=properties.def_eps):
    df = derivative_fun.return_df(f)
    df_a = abs(df(a))
    df_b = abs(df(b))
    max_df = max(df_a, df_b)

    if (max_df == 0):
        return 0,0,0
    else:
        lamda = 1 / max_df
        current_x = (a + b) / 2

    if df(current_x) > 0:
        lamda = -lamda

    for i in range(properties.max_iter):
        f_c = f(current_x)
        next_x = current_x + lamda * f_c
        if (abs(next_x - current_x) < eps):
            return f(next_x), next_x, i + 1
        current_x = next_x

    return f(current_x), current_x, properties.max_iter
