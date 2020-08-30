"""Marking the elements to refine."""


from skfem import adaptive_theta


def adaptive_theta(m, estimators, theta=0.5, **params):
    return adaptive_theta(m, estimators, theta=theta)
