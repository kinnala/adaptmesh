"""Tri - Constrained Delaunay Triangulation of Planar Straight Line Graphs
"""

__version__ = "0.3.1.dev0"
__license__ = "MIT License"
__author__ = "Martijn Meijers"

from .delaunay import ToPointsAndSegments, triangulate  # noqa

__all__ = ["triangulate"]
