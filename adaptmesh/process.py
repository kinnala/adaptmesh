"""The adaptive process."""


import warnings


def process(
    initial=None,
    solve=None,
    mark=None,
    refine=None,
    smooth=None,
    criterion=None,
    max_refloops=6,
    **params
):

    if initial is not None:
        if callable(initial):
            mesh = initial(**params)
        else:
            mesh = initial
    else:
        raise Exception("The initial mesh not given.")

    for itr in range(max_refloops):
        estimators = solve(mesh, **params)
        elements = mark(mesh, estimators, **params)
        mesh = refine(mesh, elements, **params)
        if smooth is not None:
            mesh = smooth(mesh, **params)
        if criterion is not None:
            if criterion(mesh, **params):
                break

    if itr == max_refloops:
        warnings.warn(
            "Criterion not satisfied in {} refinement loops.".format(itr)
        )

    return mesh
