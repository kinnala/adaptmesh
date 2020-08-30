"""Stopping criteria for the adaptive process."""


import numpy as np
from .meshplex import MeshTri


def avg_quality(m, avg_quality=0.9, **params):
    mp = MeshTri(m.p.T, m.t.T)
    if np.mean(mp.cell_quality) > avg_quality:
        return True
    return False
