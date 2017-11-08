"""Utils for common data operations"""
from typing import Dict, List
from collections import defaultdict

import pandas as pd
from scipy.spatial.distance import pdist, squareform, cosine, correlation
from sklearn.feature_selection import VarianceThreshold
from statsmodels.sandbox.stats.multicomp import multipletests
from sklearn.feature_selection import f_classif


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


def feature_importance_anova(X,
                             y,
                             threshold=0.001,
                             correcting_multiple_hypotesis=True,
                             method='fdr_bh',
                             alpha=0.1,
                             sort_by='pval'):
    '''
    Provide signifance for features in dataset with anova using multiple hypostesis testing
    :X: List of dict with key as feature names and values as features
    :y: Labels
    :threshold: Low-variens threshold to eliminate low varience features
    :correcting_multiple_hypotesis: corrects p-val with multiple hypotesis testing
    :method: method of multiple hypotesis testing
    :alpha: alpha of multiple hypotesis testing
    :sort_by: sorts output dataframe by pval or F
    :return: DataFrame with F and pval for each feature with their average values 
    '''
    df = variance_threshold_on_df(
        pd.DataFrame.from_records(X), threshold=threshold)

    F, pvals = f_classif(df.values, y)

    if correcting_multiple_hypotesis:
        _, pvals, _, _ = multipletests(pvals, alpha=alpha, method=method)

    df['labels'] = y
    df_mean = df.groupby('labels').mean().T

    df_mean['F'] = F
    df_mean['pval'] = pvals

    return df_mean.sort_values(sort_by, ascending=True)
