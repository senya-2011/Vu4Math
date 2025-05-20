import math

FUNCTIONS = {
    1: ("sin(x)", lambda x: math.sin(x), lambda x: -math.cos(x), None),
    2: ("exp(x)", lambda x: math.exp(x), lambda x: math.exp(x), None),
    3: ("1/x^2", lambda x: 1/x**2, lambda x: -1/x, 0),
    4: ("1/(1+x^2)", lambda x: 1/(1+x**2), lambda x: math.atan(x), None),
    5: ("-1/x", lambda x: -1/x, lambda x: -math.log(abs(x)), 0),
}