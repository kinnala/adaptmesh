from .process import process


def triangulate(
    corner_points, max_refloops=6, theta=0.8, smooth_steps=50, avg_quality=0.9
):
    from .initial import cdt
    from .solve import laplace
    from .mark import adaptive_theta
    from .refine import rgb
    from .smooth import cpt
    from .criterion import avg_quality

    return process(
        initial=cdt,
        solve=laplace,
        mark=adaptive_theta,
        refine=rgb,
        smooth=cpt,
        criterion=avg_quality,
        corner_points=corner_points,
        max_refloops=max_refloops,
        theta=theta,
    )
