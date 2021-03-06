from typing import List

from numpy import ndarray
from sklearn.metrics import accuracy_score


def get_npcer(false_negative: int, true_positive: int):
    return false_negative / (false_negative + true_positive)


def get_apcer(false_positive: int, true_negative: int):
    return false_positive / (true_negative + false_positive)


def get_acer(apcer: float, npcer: float):
    return (apcer + npcer) / 2.0


def get_metrics(pred: ndarray, targets: ndarray):
    negative_indices = targets == 1
    positive_indices = targets == 0

    true_negative = (pred[negative_indices] == 1).sum()
    true_positive = (pred[positive_indices] == 0).sum()

    false_negative = (pred[positive_indices] == 1).sum()
    false_positive = (pred[negative_indices] == 0).sum()

    npcer = get_npcer(false_negative, true_positive)
    apcer = get_apcer(false_positive, true_negative)

    acer = get_acer(apcer, npcer)

    return acer, apcer, npcer


def get_threshold(probs: ndarray, grid_density: int = 100):
    min_, max_ = min(probs), max(probs)
    thresholds = [min_]
    for i in range(grid_density + 1):
        thresholds.append(min_ + (i * (max_ - min_)) / float(grid_density))
    thresholds.append(1.1)
    return thresholds


def eval_from_scores(scores: ndarray, targets: ndarray):
    thrs = get_threshold(scores)
    best_acc = 0.0
    best_thr = -1
    for thr in thrs:
        acc = accuracy_score(targets, scores >= thr)
        if best_acc < acc:
            best_acc = acc
            best_thr = thr
            metrics = get_metrics(scores >= thr, targets)
    return metrics, best_thr, best_acc
