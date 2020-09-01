"""Perform mesh smoothing."""


from skfem import MeshTri

from .optimesh.cpt import fixed_point_uniform


def cpt(m, smooth_steps=None, **params):

    if smooth_steps is None:
        smooth_steps = 50

    X, cells = fixed_point_uniform(
        m.p.T, m.t.T, tol=0, max_num_steps=smooth_steps
    )

    return MeshTri(X.T, cells.T)
