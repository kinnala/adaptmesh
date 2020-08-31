"""Solvers take a mesh and return elementwise error estimate."""


import numpy as np
from skfem import (
    ElementTriP1,
    FacetBasis,
    Functional,
    InteriorBasis,
    condense,
    solve,
)
from skfem.helpers import grad
from skfem.models.poisson import laplace as laplacian
from skfem.models.poisson import unit_load


def laplace(m, **params):
    """Solve the Laplace equation using the FEM.

    Parameters
    ----------
    m
        A Mesh object.

    """
    e = ElementTriP1()
    basis = InteriorBasis(m, e)
    A = laplacian.assemble(basis)
    b = unit_load.assemble(basis)
    u = solve(*condense(A, b, I=m.interior_nodes()))

    # evaluate the error estimators
    fbasis = [FacetBasis(m, e, side=i) for i in [0, 1]]
    w = {"u" + str(i + 1): fbasis[i].interpolate(u) for i in [0, 1]}

    @Functional
    def interior_residual(w):
        h = w.h
        return h ** 2

    eta_K = interior_residual.elemental(basis)

    @Functional
    def edge_jump(w):
        h = w.h
        n = w.n
        dw1 = grad(w["u1"])
        dw2 = grad(w["u2"])
        return h * ((dw1[0] - dw2[0]) * n[0] + (dw1[1] - dw2[1]) * n[1]) ** 2

    eta_E = edge_jump.elemental(fbasis[0], **w)

    tmp = np.zeros(m.facets.shape[1])
    np.add.at(tmp, fbasis[0].find, eta_E)
    eta_E = np.sum(0.5 * tmp[m.t2f], axis=0)

    return eta_E + eta_K
