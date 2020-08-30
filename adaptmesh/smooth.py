"""Perform mesh smoothing."""


from skfem import MeshTri
import optimesh


def cpt(m, smooth_steps=None, **params):

    if smooth_steps is None:
        smooth_steps = 50

    X, cells = optimesh.cpt.fixed_point_uniform(
        m.p.T,
        m.t.T,
        tol=0,
        max_num_steps=smooth_steps
    )

    return MeshTri(X.T, cells.T)
