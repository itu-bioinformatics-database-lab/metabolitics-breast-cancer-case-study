"""Utils for common data operations"""
from typing import Dict, List
from collections import defaultdict

import pandas as pd
from scipy.spatial.distance import pdist, squareform, cosine, correlation
from sklearn.feature_selection import VarianceThreshold


def filter_by_label(X, y, label, reverse=False):
    """Select items with label from dataset"""
    return list(
        zip(*filter(lambda t: (not reverse) == (t[1] == label), zip(X, y))))


def average_by_label(X, y, label):
    """returns average dictinary from list of dictionary for give label"""
    return defaultdict(float,
                       pd.DataFrame.from_records(
                           filter_by_label(X, y, label)[0]).mean().to_dict())


def similarty_dict(x: Dict, y: List[Dict], metric=correlation):
    """Calculate dictance of one vector in dict format to other dictinary in list of dict"""
    vecs = pd.DataFrame([x] + y).fillna(0).values
    return [1 - metric(vecs[0], v) for v in vecs[1:]]


def convert_df_to_squareform(df: pd.DataFrame, metric=correlation):
    """Converts pandas dataframe with columns into squareformed dataframe"""
    df_squareform = pd.DataFrame(squareform(pdist(df.T, metric)))
    df_squareform.columns = df.columns
    df_squareform.index = df.columns
    return df_squareform

def variance_threshold_on_df(df: pd.DataFrame, threshold=0):
    vt = VarianceThreshold(threshold)
    vt.fit(df.values)
    return df.iloc[:, vt.variances_ > threshold] 

    
    
