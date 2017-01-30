'''Extantion Methods for Metabolites'''

import math
import json

import cobra as cb


def connected_subsystems(self):
    '''Connected Subsystem of metabolite'''
    return set([r.subsystem for r in self.reactions])


def is_border(self):
    ''' Extantion method to check metabolite in model is border'''
    return len(self.connected_subsystems()) > 1


def is_currency(self, by='subsystem'):
    ''' Extantion method to check metabolite in model is currency'''
    if self.id in self.currency_list:
        return True
    if by == 'reaction':
        return len(self.reactions) >= self.currency_threshold
    elif by == 'subsystem':
        return len(self.connected_subsystems()) > self.currency_threshold
    else:
        raise ValueError('by should be either subsystem or reactions')


cb.Metabolite.connected_subsystems = connected_subsystems
cb.Metabolite.is_border = is_border
cb.Metabolite.currency_threshold = math.inf
cb.Metabolite.currency_list = set(
    json.load(open('../dataset/currency/currency_metabolites.json')))
cb.Metabolite.is_currency = is_currency
