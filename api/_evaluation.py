from typing import List

from random import random
import numpy as np


def eval_decentralization(values: List[float]) -> float:
    values = np.array(values)
    mad = np.abs(np.subtract.outer(values, values)).mean()
    # Relative mean absolute difference
    rmad = mad/np.mean(values)
    # Gini coefficient
    g = 0.5 * rmad
    return g
    #  return random()




if __name__ == "__main__":
    rslt = eval_decentralization([100.0, 125.0, 2048.0, 480.0, 888.0]) 
    print(rslt)