from adaptmesh import initial


def test_nonconvex():
    pts = [
        (0.0, 0.0),
        (1.1, 0.0),
        (1.2, 0.5),
        (0.7, 0.6),
        (2.0, 1.0),
        (1.0, 2.0),
        (0.5, 1.5),
    ]

    m = initial.cdt(pts)
    boundary_pts = set(map(tuple, m.p.T[m.boundary_nodes()]))
    assert boundary_pts == set(pts)
