from simplegeom.geometry import LineString
from topomap.loopfactory import find_loops
from topomap.topomap import TopoMap

from . import ToPointsAndSegments, triangulate
from .delaunay import TriangleIterator, ccw, output_triangles

# from splitarea.flagging import MidpointHarvester
# from splitarea.densify import densify

#
# FIXME:
# - Happily converts a constrained Triangulation as well: can lead to problems!
# - Should embed the construction of the TopoMap object in the transformer
# - Left / Right references for faces on the boundary are not correctly set
#   (leading to problems for forming loops) -> should introduce the Universe
# - does not deal with SRID for the Topomap generated yet
#


class VoronoiTransformer(object):
    """Class to transform a Delaunay triangulation into a Voronoi diagram

    The class generates a series of segments, together with information how
    these should be glued together to the Voronoi diagram
    (start node id, end node id, left face id, right face id)
    """

    def __init__(self, triangulation):
        self.triangulation = triangulation

    def transform(self):
        """Calculate center of circumscribed circles for all triangles
        and generate a line segment from one triangle to its neighbours
        (this happens only once for every pair).
        """
        self.centers = {}
        for t in self.triangulation.triangles:
            self.centers[id(t)] = self.incenter(t)
        segments = []
        for t in self.triangulation.triangles:
            for side, n in enumerate(t.neighbours):
                if (
                    n is not None
                    and n is not self.triangulation.external
                    and id(t) < id(n)
                ):
                    start, end = id(t), id(n)
                    left = id(t.vertices[ccw(ccw(side))])
                    right = id(t.vertices[ccw(side)])
                    segments.append((start, end, left, right))
        self.segments = segments

    def incenter(self, t):
        (
            p0,
            p1,
            p2,
        ) = t.vertices
        ax, ay, bx, by, cx, cy, = (
            p0.x,
            p0.y,
            p1.x,
            p1.y,
            p2.x,
            p2.y,
        )
        a2 = pow(ax, 2) + pow(ay, 2)
        b2 = pow(bx, 2) + pow(by, 2)
        c2 = pow(cx, 2) + pow(cy, 2)
        UX = a2 * (by - cy) + b2 * (cy - ay) + c2 * (ay - by)
        UY = a2 * (cx - bx) + b2 * (ax - cx) + c2 * (bx - ax)
        D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        ux = UX / D
        uy = UY / D
        return (ux, uy)


def main():
    import json

    #     pts_segs = ToPointsAndSegments()
    #     pts_segs.add_polygon([[(0,0), (10,0), (5,10), (0,0)],
    #                           #[(2,2), (8,2), (6,4), (5,7), (2,2)]
    #                           ],
    #                          )
    #     pts_segs.add_polygon([[(10,0), (15,10), (5,10), (10,0)],
    #                           #[(2,2), (8,2), (6,4), (5,7), (2,2)]
    #                           ],
    #                          )
    # FIXME: does not work with this dataset yet, as the vertex density is not
    # high enough: should add more vertices (densify)
    with open(
        "/home/martijn/workspace/splitarea/data/sandro/poly.geojson"
    ) as fh:
        c = json.loads(fh.read())
    conv = ToPointsAndSegments()
    poly = c["features"][0]["geometry"]["coordinates"]
    rings = []
    for ring in poly:
        rings.append(
            #                      densify(
            [tuple(pt) for pt in ring]
            #                      , 5)
        )
    del poly
    conv.add_polygon(rings)
    dt = triangulate(conv.points, conv.infos, conv.segments)

    trafo = VoronoiTransformer(dt)
    trafo.transform()

    with open("/tmp/vroni.wkt", "w") as fh:
        fh.write("wkt;start;end;left;right\n")
        for (start, end, lft, rgt) in trafo.segments:
            fh.write(
                "LINESTRING({0[0]} {0[1]}, {1[0]} {1[1]});{2};{3};{4};{5}\n".format(
                    trafo.centers[start],
                    trafo.centers[end],
                    start,
                    end,
                    lft,
                    rgt,
                )
            )

    # FIXME: this should be part of the VoronoiTransformer !
    tm = TopoMap()
    for i, (start, end, lft, rgt) in enumerate(trafo.segments, start=1):
        tm.add_edge(
            i,
            start,
            end,
            lft,
            rgt,
            LineString([trafo.centers[start], trafo.centers[end]]),
        )
    find_loops(tm)
    with open("/tmp/geom.wkt", "w") as fh:
        fh.write("wkt\n")
        for face in tm.faces.itervalues():
            try:
                fh.write("{0}\n".format(face.multigeometry()[0]))
            except Exception:
                pass

    with open("/tmp/inside.wkt", "w") as fh:
        output_triangles([t for t in TriangleIterator(dt)], fh)


if __name__ == "__main__":
    main()
