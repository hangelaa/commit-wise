"""Model definitions shared by all notebooks."""

import numpy as np
from lightgbm import LGBMClassifier
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from xgboost import XGBClassifier

from src.data.split import FEATURES

SEED = 42


def make_logistic_regression():
    """Baseline: log1p on skewed features, standardization, balanced class weights."""
    log_features = [f for f in FEATURES if f != "ent"]
    preprocess = ColumnTransformer([
        ("log_and_scale", Pipeline([("log", FunctionTransformer(np.log1p)), ("scale", StandardScaler())]), log_features),
        ("scale_only", StandardScaler(), ["ent"]),
    ])
    return Pipeline([
        ("preprocess", preprocess),
        ("model", LogisticRegression(class_weight="balanced", max_iter=1000)),
    ])


def make_random_forest():
    return RandomForestClassifier(
        n_estimators=300, min_samples_leaf=5, class_weight="balanced_subsample",
        n_jobs=-1, random_state=SEED,
    )


def make_xgboost(y_train):
    ratio = (y_train == 0).sum() / (y_train == 1).sum()
    return XGBClassifier(
        n_estimators=300, learning_rate=0.05, max_depth=6, subsample=0.8,
        colsample_bytree=0.8, scale_pos_weight=ratio, eval_metric="logloss",
        n_jobs=-1, random_state=SEED,
    )


def make_lightgbm():
    return LGBMClassifier(
        n_estimators=300, learning_rate=0.05, num_leaves=31, subsample=0.8,
        subsample_freq=1, colsample_bytree=0.8, class_weight="balanced",
        n_jobs=-1, random_state=SEED, verbose=-1,
    )


def all_models(y_train):
    """Return the four models with their first-pass settings."""
    return {
        "logistic regression": make_logistic_regression(),
        "random forest": make_random_forest(),
        "xgboost": make_xgboost(y_train),
        "lightgbm": make_lightgbm(),
    }