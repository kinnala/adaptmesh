from .process import process


def triangulate(
    corner_points, max_refloops=10, theta=0.8, smooth_steps=50, quality=0.9
):
    from .criterion import avg_quality
    from .initial import cdt
    from .mark import adaptive_theta
    from .refine import rgb
    from .smooth import cpt
    from .solve import laplace

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
        smooth_steps=smooth_steps,
        quality=quality,
    )
