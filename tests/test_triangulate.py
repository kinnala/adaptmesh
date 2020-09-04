import pytest

from adaptmesh import triangulate
from adaptmesh.criterion import avg_quality


def test_square():
    m = triangulate([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
    assert m.t.shape[1] == 52


@pytest.mark.parametrize("x1", [0.0, 0.3])
@pytest.mark.parametrize("x2", [1.0, 0.7])
@pytest.mark.parametrize("x3", [1.0, 0.5])
@pytest.mark.parametrize("y1", [0.0, 0.27])
@pytest.mark.parametrize("y2", [0.0, -0.4])
@pytest.mark.parametrize("y3", [1.0, 1.3])
def test_triangle(x1, x2, x3, y1, y2, y3):
    quality = 0.91
    m = triangulate(
        [(x1, y1), (x2, y2), (x3, y3)], quality=quality, max_refloops=15
    )
    is_quality = avg_quality(m, quality=quality)
    assert is_quality
