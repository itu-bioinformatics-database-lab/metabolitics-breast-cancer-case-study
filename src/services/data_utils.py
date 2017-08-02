"""Utils for common data operations"""
from typing import Dict, List
from collections import defaultdict

import pandas as pd
from scipy.spatial.distance import cosine, correlation


def filter_by_label(X, y, label):
    """Select items with label from dataset"""
    return list(zip(*filter(lambda t: t[1] == label, zip(X, y))))


def average_by_label(X, y, label):
    """returns average dictinary from list of dictionary for give label"""
    return defaultdict(float,
                       pd.DataFrame.from_records(
                           filter_by_label(X, y, label)[0]).mean().to_dict())


def similarty_dict(x: Dict, y: List[Dict], metric=correlation):
    """Calculate dictance of one vector in dict format to other dictinary in list of dict"""
    vecs = pd.DataFrame([x] + y).fillna(0).values
    return [1 - metric(vecs[0], v) for v in vecs[1:]]
