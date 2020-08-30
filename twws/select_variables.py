from typing import Optional

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import make_union, make_pipeline
from sklearn.base import TransformerMixin

from lightgbm import LGBMRegressor
import optuna


def get_units_only(df):

    df = df.loc[df.special_category.isin([np.nan, 'renown']), :]
    df = df.loc[~df.caste.isin(['Lord', 'Hero']), :]

    return df


class Selector(TransformerMixin):

    def __init__(self, variables: list) -> None:
        self.variables = variables

    def fit(self, x: pd.DataFrame, y: Optional[pd.Series] = None) -> TransformerMixin:
        return self

    def transform(self, x: pd.DataFrame) -> pd.DataFrame:
        return x.loc[:, self.variables]
