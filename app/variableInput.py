import numpy as np


def randomize():
    # BW = np.random.normal(11.5,1)
    BW = 11.5
    VFC = np.random.normal(0.15, 0.3)
    return {
        'BW': BW,
        'VFC': VFC
    }