from scipy.sparse import coo_matrix, csgraph
import cobra as cb
import numpy as np


class MetabolicAdjMatrix:

    def __init__(self, model: cb.Model):
        self.model = model

    def is_connected_component(self):
        ''' Check network is connected component'''
        pass

    def _border_sub_adj_list(self):
        subsystems = set([r.subsystem for r in self.model.reactions])
        indexes = dict(map(lambda x: (x[1], x[0]), enumerate(subsystems)))
        adj_list = set()
        for m in self.model.metabolites:
            if m.is_border() and not m.is_currency():
                con_sub = list(m.connected_subsystems())
                for i in range(len(con_sub)):
                    for j in range(i + 1, len(con_sub)):
                        source = indexes[con_sub[i]]
                        target = indexes[con_sub[j]]
                        adj_list.add((source, target))
        return (list(adj_list), len(indexes))

    def _adj_list_to_adj_matrix(self, adj_list, num_of_nodes):
        if not adj_list:
            raise ValueError('Adj list cannot be zero')
        (i_indices, j_indices) = zip(*adj_list)
        coos = (np.ones(len(adj_list)), (i_indices, j_indices))
        return coo_matrix(coos, shape=(num_of_nodes, num_of_nodes))

    def to_subsystem_adj_matrix(self):
        (adj_list, num_of_nodes) = self._border_sub_adj_list()
        return self._adj_list_to_adj_matrix(adj_list, num_of_nodes)

    def is_subsystem_level_connected_component(self):
        return csgraph.connected_components(self.to_subsystem_adj_matrix())
