"""Creation of initial meshes."""


import matplotlib.path as mpltPath
import numpy as np
from skfem import MeshTri

from .tri import ToPointsAndSegments, triangulate


def cdt(corner_points=None, **params):
    """Create a CDT mesh using tri."""
    if corner_points is None:
        raise Exception("Parameter 'corner_points' required.")

    points = corner_points
    segs = ToPointsAndSegments()
    segs.add_polygon([points])
    dt = triangulate(segs.points, segs.segments)

    # find triangles inside the polygon
    p, t = [], []
    verts = {}
    i = 0
    path = mpltPath.Path([[point[0], point[1]] for point in points])

    for triangle in dt.triangles:

        # validate triangle
        if not triangle.is_finite:
            continue

        # add new verts
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

        t.append(newtri)

    m = MeshTri(np.array(p).T, np.array(t).T)
    m.refine()

    return m
