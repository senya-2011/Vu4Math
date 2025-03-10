import logic.properties as properties


def return_df(f):
    h = properties.h

    def df(x):
        return (f(x + h) - f(x - h)) / (2 * h)

    return df
