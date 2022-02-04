import numpy


def runner(
    get_new_points,
    mesh,
    tol,
    max_num_steps,
    omega=1.0,
    method_name=None,
    verbose=False,
    callback=None,
    step_filename_format=None,
    uniform_density=False,
    implicit_surface=None,
    implicit_surface_tol=1.0e-10,
):
    k = 0

    if verbose:
        print("\nBefore:")
    if step_filename_format:
        mesh.save(
            step_filename_format.format(k),
            show_coedges=False,
            show_axes=False,
            cell_quality_coloring=("viridis", 0.0, 1.0, False),
        )

    if callback:
        callback(k, mesh)

    while True:
        k += 1

        new_points = get_new_points(mesh)
        diff = omega * (new_points - mesh.node_coords)

        # Some methods are stable (CPT), others can break down if the mesh isn't very
        # smooth. A break-down manifests, for example, in a step size that lets
        # triangles become fully flat or even "overshoot". After that, anything can
        # happen. To prevent this, restrict the maximum step size to half of the minimum
        # the incircle radius of all adjacent cells. This makes sure that triangles
        # cannot "flip".
        # <https://stackoverflow.com/a/57261082/353337>
        max_step = numpy.full(mesh.node_coords.shape[0], numpy.inf)
        numpy.minimum.at(
            max_step,
            mesh.cells["nodes"].reshape(-1),
            numpy.repeat(mesh.cell_inradius, 3),
        )
        max_step *= 0.5

        step_lengths = numpy.sqrt(numpy.einsum("ij,ij->i", diff, diff))
        # alpha = numpy.min(max_step / step_lengths)
        # alpha = numpy.min([alpha, 1.0])
        # diff *= alpha
        idx = step_lengths > max_step
        diff[idx] *= max_step[idx, None] / step_lengths[idx, None]

        mesh.node_coords += diff

        # project all points back to the surface
        if implicit_surface is not None:
            fval = implicit_surface.f(mesh.node_coords.T)
            while numpy.any(numpy.abs(fval) > implicit_surface_tol):
                grad = implicit_surface.grad(mesh.node_coords.T)
                grad_dot_grad = numpy.einsum("ij,ij->j", grad, grad)
                # The step is chosen in the direction of the gradient with a step size
                # such that, if the function was linear, the boundary (fval=0) would be
                # hit in one step.
                mesh.node_coords -= (grad * (fval / grad_dot_grad)).T
                # compute new value
                fval = implicit_surface.f(mesh.node_coords.T)

        mesh.update_values()
        mesh.flip_until_delaunay()

        # mesh.show()

        # Abort the loop if the update was small
        diff_norm_2 = numpy.einsum("ij,ij->i", diff, diff)
        is_final = numpy.all(diff_norm_2 < tol**2) or k >= max_num_steps

        if is_final or step_filename_format:
            if is_final:
                info = "{} steps".format(k)
                if method_name is not None:
                    if abs(omega - 1.0) > 1.0e-10:
                        method_name += ", relaxation parameter {}".format(
                            omega
                        )
                    info += " of " + method_name

                if verbose:
                    print("\nFinal ({}):".format(info))
            if step_filename_format:
                mesh.save(
                    step_filename_format.format(k),
                    show_coedges=False,
                    show_axes=False,
                    cell_quality_coloring=("viridis", 0.0, 1.0, False),
                )
        if callback:
            callback(k, mesh)

        if is_final:
            break

    return k, numpy.max(numpy.sqrt(diff_norm_2))


def get_new_points_volume_averaged(mesh, reference_points):
    scaled_rp = reference_points.T * mesh.cell_volumes

    n = mesh.node_coords.shape[0]
    new_points = numpy.zeros(mesh.node_coords.shape)
    for i in mesh.cells["nodes"].T:
        new_points += numpy.array(
            [numpy.bincount(i, vals, minlength=n) for vals in scaled_rp]
        ).T

    omega = numpy.zeros(n)
    for i in mesh.cells["nodes"].T:
        omega += numpy.bincount(i, mesh.cell_volumes, minlength=n)

    new_points /= omega[:, None]
    idx = mesh.is_boundary_node
    new_points[idx] = mesh.node_coords[idx]
    return new_points


def get_new_points_count_averaged(mesh, reference_points):
    # Estimate the density as 1/|tau|. This leads to some simplifcations: The new point
    # is simply the average of of the reference points (barycenters/cirumcenters) in the
    # star.
    n = mesh.node_coords.shape[0]

    new_points = numpy.zeros(mesh.node_coords.shape)
    for i in mesh.cells["nodes"].T:
        new_points += numpy.array(
            [
                numpy.bincount(i, vals, minlength=n)
                for vals in reference_points.T
            ]
        ).T

    omega = numpy.bincount(mesh.cells["nodes"].reshape(-1), minlength=n)

    new_points /= omega[:, None]

    # reset boundary nodes
    idx = mesh.is_boundary_node
    new_points[idx] = mesh.node_coords[idx]
    return new_points
