"""The adaptive process."""


import warnings

from skfem.visuals.matplotlib import draw


def process(
    initial=None,
    solve=None,
    mark=None,
    refine=None,
    smooth=None,
    criterion=None,
    max_refloops=6,
    verbose=False,
    **params
):

    if initial is not None:
        if callable(initial):
            mesh = initial(**params)
        else:
            mesh = initial
    else:
        raise Exception("The initial mesh not given.")

    if verbose:
        draw(mesh)

    for itr in range(max_refloops):
        estimators = solve(mesh, **params)
        elements = mark(mesh, estimators, **params)
        mesh = refine(mesh, elements, **params)
        if verbose:
            draw(mesh)
        if smooth is not None:
            mesh = smooth(mesh, **params)
            if verbose:
                draw(mesh)
        if criterion is not None:
            if criterion(mesh, **params):
                break

    if itr == max_refloops - 1:
        warnings.warn(
            "Criterion not satisfied in {} refinement loops.".format(
                max_refloops
            )
        )

    return mesh
