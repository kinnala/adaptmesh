"""Marking the elements to refine."""


from skfem import adaptive_theta as atheta


def adaptive_theta(m, estimators, theta=0.5, **params):
    return atheta(estimators, theta=theta)
