import logging
import cobra as cb
import numpy as np

from models import MetabolicAdjMatrix

optimal_currency_logger = logging.getLogger('optimal_currency')
optimal_currency_logger.setLevel(logging.INFO)
optimal_currency_logger.addHandler(
    logging.FileHandler('../logs/optimal_currency.log'))


def optimal_currency_threshold(model, try_range):
    adj = MetabolicAdjMatrix(model).to_subsystem_adj_matrix()

    optimal_currency_logger.info('no threshold \n %s' % adj.todense())

    for i in range(try_range[0], try_range[1]):
        cb.Metabolite.currency_threshold = i
        t_adj = MetabolicAdjMatrix(model).to_subsystem_adj_matrix()

        optimal_currency_logger.info(
            'for threshold= %d \n %s' % (i, t_adj.todense()))
        optimal_currency_logger.info(
            'diff= \n %s' % (t_adj.todense() - adj.todense()))
        ndiff = -(t_adj.todense() - adj.todense()).sum()
        optimal_currency_logger.info('number of diff= %d' % ndiff)

        if np.array_equal(adj.todense(), t_adj.todense()):
            return i
