"""Refine the mesh."""


def rgb(m, elems, **params):
    m = m.refined(elems)
    return m
