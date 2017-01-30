import cobra as cb

from .base_subsystem_fba import BaseSubsystemFBA
from models import *


class TreeSubsystemFBA(BaseSubsystemFBA):
    '''Extending tree subsystem fba analysis implementation'''

    def __init__(self, model: cb.Model):
        super().__init__(model)
        self.model = {}

    def analyze(self, measured_metabolites):
        '''Implement extanding tree in there'''
        pass
