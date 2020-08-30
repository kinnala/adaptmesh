from .process import process


def triangulate(
    corner_points,
    max_refloops=6,
    theta=0.8,
):
    from .initial import cdt
    from .solve import laplace
    from .mark import adaptive_theta
    from .refine import rgb
    from .smooth import cpt

    process(
        initial=cdt,
        solve=laplace,
        mark=adaptive_theta,
        refine=rgb,
        smooth=cpt,
        criterion=quality,
        corner_points=corner_points,
        max_refloops=max_refloops,
        theta=theta,
    )
