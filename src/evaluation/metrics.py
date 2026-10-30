"""Evaluation metrics shared by all notebooks."""

from sklearn.metrics import (
    average_precision_score,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate(y_true, proba, threshold=0.5):
    """Return the main classification metrics for predicted bug probabilities."""
    pred = proba >= threshold
    return {
        "ROC-AUC": roc_auc_score(y_true, proba),
        "PR-AUC": average_precision_score(y_true, proba),
        "precision": precision_score(y_true, pred, zero_division=0),
        "recall": recall_score(y_true, pred),
        "F1": f1_score(y_true, pred),
        "MCC": matthews_corrcoef(y_true, pred),
        "bug share": y_true.mean(),
    }