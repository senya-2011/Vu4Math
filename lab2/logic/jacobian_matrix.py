import logic.properties as properties


def finite_difference_derivative(f, x, y, var, dx):
    if var == 'x':
        return (f(x + dx, y) - f(x, y)) / dx
    elif var == 'y':
        return (f(x, y + dx) - f(x, y)) / dx


def jacobian(f1, f2, x, y, dx=properties.def_dx):
    df1_dx = finite_difference_derivative(f1, x, y, 'x', dx)
    df1_dy = finite_difference_derivative(f1, x, y, 'y', dx)
    df2_dx = finite_difference_derivative(f2, x, y, 'x', dx)
    df2_dy = finite_difference_derivative(f2, x, y, 'y', dx)

    return [
        [df1_dx, df1_dy],
        [df2_dx, df2_dy]
    ]
