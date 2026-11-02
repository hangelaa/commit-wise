"""Evaluation metrics shared by all notebooks."""

import numpy as np
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

def best_threshold(y_true, proba):
    """Return the threshold (searched from 0.05 to 0.95) that maximizes MCC."""
    grid = np.arange(0.05, 0.96, 0.01)
    scores = [matthews_corrcoef(y_true, proba >= t) for t in grid]
    return grid[int(np.argmax(scores))]


def effort_curve(y_true, score, effort):
    """Inspect commits from the highest score down; return (effort share used, share of bugs found)."""
    order = np.argsort(-np.asarray(score))
    bugs = np.asarray(y_true)[order]
    cost = np.asarray(effort)[order]
    return np.cumsum(cost) / cost.sum(), np.cumsum(bugs) / bugs.sum()


def recall_at_effort(y_true, score, effort, share=0.2):
    """Share of bug-inducing commits found when `share` of the total effort is spent."""
    effort_share, found = effort_curve(y_true, score, effort)
    i = np.searchsorted(effort_share, share, side="right")
    return found[i - 1] if i > 0 else 0.0