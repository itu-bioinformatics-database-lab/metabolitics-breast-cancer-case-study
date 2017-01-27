import unittest

import cobra as cb
import cobra.test
from .metabolite_extantions import *
from .metabolic_adj_matrix import MetabolicAdjMatrix
import math


class TestMetaboliteExtantion(unittest.TestCase):

    def setUp(self):
        self.model = cb.test.create_test_model('salmonella')
        self.h2o_c = self.model.metabolites.get_by_id('h2o_c')
        self.pglyc_c = self.model.metabolites.get_by_id('2pglyc_c')

    def test_is_border(self):
        self.assertEqual(self.h2o_c.is_border(), True)
        self.assertEqual(self.pglyc_c.is_border(), False)


class TestMetabolicAdjMatrix(unittest.TestCase):

    def setUp(self):
        self.model = cb.test.create_test_model('salmonella')
        self.salchs4_e = self.model.metabolites.get_by_id('salchs4_e')
        self.pglyc_c = self.model.metabolites.get_by_id('2pglyc_c')

        small_model = cb.Model('small_model')
        for r in self.salchs4_e.reactions:
            small_model.add_reaction(r)

        self.adj = MetabolicAdjMatrix(small_model)

        unconnected_model = cb.Model('unconnected_model')
        for r in self.salchs4_e.reactions:
            unconnected_model.add_reaction(r)

        for r in self.pglyc_c.reactions:
            unconnected_model.add_reaction(r)

        self.unconnected_adj = MetabolicAdjMatrix(unconnected_model)

    def test__border_sub_adj_list(self):
        (adj_list, num_of_nodes) = self.adj._border_sub_adj_list()

        self.assertListEqual(adj_list, [(0, 1)])
        self.assertEqual(num_of_nodes, 2)

        cb.Metabolite.currency_threshold = 1
        (adj_list, num_of_nodes) = self.adj._border_sub_adj_list()
        self.assertListEqual(adj_list, [])
        self.assertEqual(num_of_nodes, 2)
        cb.Metabolite.currency_threshold = math.inf

    def test_to_subsystem_adj_matrix(self):
        adj_matrix = self.adj.to_subsystem_adj_matrix()
        expected_adj_matrix = [[0.,  1.],
                               [0.,  0.]]
        self.assertEqual(adj_matrix.toarray().tolist(), expected_adj_matrix)

    def test_is_subsystem_level_connected_component(self):
        (num_comp, labels) = self.adj.is_subsystem_level_connected_component()
        self.assertEqual(num_comp, 1)

        sal_adj = MetabolicAdjMatrix(self.model)
        (num_comp, labels) = sal_adj.is_subsystem_level_connected_component()
        self.assertEqual(num_comp, 1)

        (num_comp, labels) = self.unconnected_adj.is_subsystem_level_connected_component()
        self.assertEqual(num_comp, 2)
