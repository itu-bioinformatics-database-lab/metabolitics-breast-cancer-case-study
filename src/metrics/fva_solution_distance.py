import numpy as np

__all__ = [
    'diff_mix_max_fva_solution',
    'fva_solution_distance',
    'diff_range_solutions',
]


def diff_mix_max_fva_solution(x):
    return sum(v - x['%s_min' % k[:-4]]
               for k, v in x.items() if k[-3:] == 'max')


def fva_solution_distance(X):
    return np.mean([diff_mix_max_fva_solution(x) for x in X])


def _diff_range_solution(x_healty, x_disease):
    return np.mean([
        (x_healty['%s_max' % k[:-4]] - x_disease['%s_min' % k[:-4]]) /
        (x_healty['%s_min' % k[:-4]] - x_disease['%s_max' % k[:-4]] + 1e-10)
        for k in x_healty if k[-3:] == 'max'])


def diff_range_solutions(X_h, X_d):
    return np.mean([_diff_range_solution(x1, x2) for x1, x2 in zip(X_h, X_d)])
