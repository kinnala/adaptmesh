# adaptmesh

[![PyPI](https://img.shields.io/pypi/v/adaptmesh)](https://pypi.org/project/adaptmesh/)
[![PyPI - License](https://img.shields.io/pypi/l/adaptmesh)](https://opensource.org/licenses/MIT)
![ci](https://github.com/kinnala/adaptmesh/workflows/ci/badge.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4172331.svg)](https://doi.org/10.5281/zenodo.4172331)

Create triangular meshes by the adaptive process.

The user feeds in a polygon and a low quality mesh is created.  Then the low
quality mesh gets improved by adaptive finite elements and mesh smoothing.  The
approach is detailed [in the following paper](https://rakenteidenmekaniikka.journal.fi/article/view/99648):
```
@article{adaptmesh,
    title={A simple technique for unstructured mesh generation via adaptive finite elements},
    author={Gustafsson, Tom},
    volume={54},
    doi={10.23998/rm.99648},
    number={2},
    journal={Rakenteiden Mekaniikka},
    year={2021},
    pages={69--79}
}
```

`adaptmesh` ships with customized versions of the following packages:

- `tri v0.3.1.dev0` (ported to Python 3; Copyright (c) 2015 Martijn Meijers; MIT; [source](https://pypi.org/project/tri/))
- `optimesh v0.6.3` (trimmed down version with minor changes to the edge
  flipping; Copyright (c) 2018-2020 Nico Schlömer; the last version with MIT; [source](https://github.com/nschloe/optimesh/releases/tag/v0.6.3))
- `meshplex v0.12.3` (trimmed down version with minor changes, i.e. removal of
  unnecessary imports; Copyright (c) 2017-2020 Nico Schlömer; the last version with MIT; [source](https://github.com/nschloe/meshplex/releases/tag/v0.12.3))

## Installation

```
pip install adaptmesh
```

## Dependencies

- `numpy`
- `scipy`
- `matplotlib`
- `scikit-fem`

## Examples

The mesh generator is called through the function `adaptmesh.triangulate`.

### Square with default settings

```python
from adaptmesh import triangulate

m = triangulate([(0., 0.),
                 (1., 0.),
                 (1., 1.),
                 (0., 1.),])
                 
# m.p are the points
# m.t are the elements
```

![Example mesh 1](https://github.com/kinnala/adaptmesh/raw/master/svgs/ex1.svg)

### Non-convex shape

```python
from adaptmesh import triangulate

m = triangulate([(0.0, 0.0),
                 (1.1, 0.0),
                 (1.2, 0.5),
                 (0.7, 0.6),
                 (2.0, 1.0),
                 (1.0, 2.0),
                 (0.5, 1.5),], quality=0.95)  # default: 0.9
```

![Example mesh 2](https://github.com/kinnala/adaptmesh/raw/master/svgs/ex2.svg)

### Holes

```python
m = triangulate([(0., 0.),
                 (1., 0.),
                 (1., 1.),
                 (0., 1.),],
                holes=[[(.25, .25),
                        (.75, .25),
                        (.75, .75),
                        (.25, .75)]])
```

![Example mesh 3](https://github.com/kinnala/adaptmesh/raw/master/svgs/ex3.svg)

### Subdomains

```python
m1 = triangulate([(0., 0.),
                  (1., 0.),
                  (.7, 1.),
                  (0., 1.),],
                 split=[(1, 8),
                        (2, 6)],
                 quality=0.91)

m2 = triangulate([(0., 2.),
                  (2., 2.),
                  (2., 0.),
                  (1., 0.),
                  (.7, 1.),
                  (0., 1.)],
                 split=[(3, 8),
                        (4, 6)],
                 quality=0.91)

m = m1 + m2
```
Multiple meshes can be joined to emulate subdomains.  However, the nodes
must match.  Above, segments are splitted to facilitate the matching, e.g.,
`[(1, 8), (2, 6)]` means that the second and the third segments are split
using eight and six equispaced extra nodes, respectively.

![Example mesh 4](https://github.com/kinnala/adaptmesh/raw/master/svgs/ex4.svg)

## Licensing

The main source code of `adaptmesh` is distributed under the MIT License.

The licenses of the included packages can be found also in `LICENSE.md` and the
respective subdirectories, i.e. `./adaptmesh/*/LICENSE`. See `LICENSE.md` for
more information.

## Changelog

### Unreleased

### [0.3.3] - 2022-02-04

- Fixed: Properly respect segments in the initial triangulation.

### [0.3.2] - 2021-09-28

- Fixed: Rendering of README in pypi.

### [0.3.1] - 2021-09-28

- Fixed: Support for `scikit-fem>=4`.

### [0.3.0] - 2021-06-22

- Fixed: Support for `scikit-fem>=3`. Dependency update broke the mesh refinement.

### [0.2.0] - 2021-01-20

- Added: keyword argument `split` of `triangulate` allows further splitting
  the provided segments.  This is useful because the segment endpoints are
  always preserved in the final mesh.
- Added: keyword argument `holes` of `triangulate` allows specifying additional
  polygonal areas inside the domain that will be free of triangles in the final
  mesh.
