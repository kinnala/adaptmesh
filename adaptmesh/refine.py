"""Refine the mesh."""


def rgb(m, elems, **params):
    m.refine(elems)
    return m
