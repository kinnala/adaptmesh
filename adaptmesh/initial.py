"""Creation of initial meshes."""
import matplotlib.path as mpltPath
import numpy as np
from skfem import MeshTri

from .tri import triangulate


def cdt(corner_points=None, **params):
    """Create a CDT mesh using tri."""
    if corner_points is None:
        raise Exception("Parameter 'corner_points' required.")

    points = corner_points.copy()
    segments = [(i, (i + 1) % len(points)) for i in range(len(points))]
    hpaths = []

    if "split" in params:
        for seg, N in params["split"]:
            t = np.linspace(0, 1, N)
            x1 = points[segments[seg][0]]
            x2 = points[segments[seg][1]]
            X = x1[0] * t + (1 - t) * x2[0]
            Y = x1[1] * t + (1 - t) * x2[1]
            X = X[1:-1]
            Y = Y[1:-1]
            previx = segments[seg][0]
            for i in range(len(X)):
                points.append((X[i], Y[i]))
                segments.append((previx, len(points) - 1))
                previx = len(points) - 1
            segments.append((len(points) - 1, segments[seg][1]))
        for seg, _ in params["split"]:
            segments.pop(seg)

    if "holes" in params:
        for hole in params["holes"]:
            N = len(points)
            for point in hole:
                points.append(point)
            for i in range(len(hole)):
                segments.append((N + i, N + (i + 1) % len(hole)))
            hpaths.append(
                mpltPath.Path([[point[0], point[1]] for point in hole])
            )

    dt = triangulate(points, segments=segments)

    # find triangles inside the polygon
    p, t = [], []
    verts = {}
    i = 0
    path = mpltPath.Path([[point[0], point[1]] for point in corner_points])

    for triangle in dt.triangles:

        # validate triangle
        if not triangle.is_finite:
            continue

        # add new vertices and calculate middle point for pruning
        newtri = []
        mpx, mpy = 0.0, 0.0
        for vert in triangle.vertices:
            if (vert.x, vert.y) not in verts:
                verts[(vert.x, vert.y)] = i
                p.append([vert.x, vert.y])
                i += 1
            newtri.append(verts[(vert.x, vert.y)])
            mpx += vert.x
            mpy += vert.y

        mpx /= 3.0
        mpy /= 3.0

        if not path.contains_point([mpx, mpy]):
            continue

        discard = False
        for hpath in hpaths:
            if hpath.contains_point([mpx, mpy]):
                discard = True
                break
        if discard:
            continue

        t.append(newtri)

    m = MeshTri(np.array(p).T, np.array(t).T)

    return m
