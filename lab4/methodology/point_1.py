"""
Вычислить меру отклонения: S = ...
для всех исследуемых функций
"""


def calc_measure_of_deviation(errors):
    squared = [error ** 2 for error in errors]
    return sum(squared) / len(squared)
