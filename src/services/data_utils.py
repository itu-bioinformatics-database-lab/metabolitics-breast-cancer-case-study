"""Utils for common data operations"""
from collections import defaultdict
import pandas as pd


def filter_by_label(X, y, label):
    """Select items with label from dataset"""
    return list(zip(*filter(lambda t: t[1] == label, zip(X, y))))


def average_by_label(X, y, label):
    """returns average dictinary from list of dictionary for give label"""
    return defaultdict(int,
                       pd.DataFrame.from_records(
                           filter_by_label(X, y, label)[0]).mean().to_dict())
