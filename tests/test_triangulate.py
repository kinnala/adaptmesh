from adaptmesh import triangulate


def test_square():
    m = triangulate([(0., 0.),
                     (1., 0.),
                     (1., 1.),
                     (0., 1.)])
    assert m.t.shape[1] == 52
