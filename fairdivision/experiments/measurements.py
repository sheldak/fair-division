import matplotlib.pyplot as plt
import numpy as np
import time
from typing import Any, Callable

from fairdivision.utils.checkers import *

# Measuring time

def with_duration(function: Callable, *args: Any) -> tuple[Any, float]:
    """
    Calls `function` with given `args` as arguments and returns its result together with the time of execution.
    """

    start_time = time.time()
    result = function(*args)
    duration = time.time() - start_time

    return result, duration


def initialize_statistics(labels: list[str]) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    """
    Initializes means per each label and standard deviations per each label.

    Both means and standard deeviations are dictionaries that contain an empty numpy array for every label in `labels`.
    """

    means_per_labels = {label: np.array([]) for label in labels}
    stds_per_labels = {label: np.array([]) for label in labels}

    return means_per_labels, stds_per_labels


def durations_to_statistics(measurements: list[dict[str, list[int]]], label: str) -> tuple[np.float64, np.float64]:
    """
    Calculates mean and standard deviation from collected `measurement` for a particular `label`.

    `measurements` is a list containing a dictionary for every iteration of experiment. Each iteration has to run the
    same algorithm and return a dictionary mapping labels to lists of durations. The function calculates mean and
    standard deviation of the sums of durations for the given `label` over all iterations.
    """

    durations = np.array(list(map(lambda durations: sum(durations[label]), measurements)))

    mean = np.mean(durations)
    standard_deviation = np.std(durations)

    return mean, standard_deviation


def update_statistics(
        means_per_label: dict[str, np.ndarray],
        stds_per_label: dict[str, np.ndarray],
        measurements: list[dict[str, list[int]]],
        labels: list[str]) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    """
    For every label in `labels`, adds mean and standard deviation calcualted from `measurements` to given
    `means_per_label` and `stds_per_label`.
    """

    for label in labels:
        mean, std = durations_to_statistics(measurements, label)
        means_per_label[label] = np.concatenate((means_per_label[label], np.array([mean])))
        stds_per_label[label] = np.concatenate((stds_per_label[label], np.array([std])))

    return means_per_label, stds_per_label


def draw_statistics(
        x: np.ndarray,
        y_means_per_labels: dict[str, np.ndarray],
        y_stds_per_labels: dict[str, np.ndarray],
        xlabel: str,
        ylabel: str,
        title: str) -> None:
    """
    Plots a mean value with corresponding standard deviation for each label on one figure.
    """

    plt.figure(figsize=(15, 6))

    plt.xlim(x[0], x[-1])
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.yscale('log')

    zipped = list(zip(y_means_per_labels.items(), y_stds_per_labels.items()))
    zipped_and_sorted = sorted(zipped, key=lambda z: z[0][1][-1], reverse=True)

    for (label, means), (_, stds) in zipped_and_sorted:
        plt.plot(x, means, label=label)
        plt.fill_between(x, means - stds, means + stds, alpha=0.3)
        
    plt.legend()
    plt.title(title)

    plt.show()
