from services import DataReader
import operator
from functools import reduce
from models import *


def subsystem_naming():
    categoires = DataReader().read_subsystem_categories()
    subsystems = reduce(set.union, categoires.values())

    model = DataReader().read_network_model()
    model_subsystems = model.subsystems()

    print('Diff of cate from model', subsystems.difference(model_subsystems))
    print('Diff of model from cate', model_subsystems.difference(subsystems))
