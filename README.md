# adaptmesh

[![PyPI](https://img.shields.io/pypi/v/adaptmesh)](https://pypi.org/project/adaptmesh/)
[![PyPI - License](https://img.shields.io/pypi/l/adaptmesh)](https://opensource.org/licenses/MIT)
![ci](https://github.com/kinnala/adaptmesh/workflows/ci/badge.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4172331.svg)](https://doi.org/10.5281/zenodo.4172331)

Create triangular meshes by the adaptive process.

The user feeds in a polygon and a low quality mesh is created.  Then the low
quality mesh gets improved by adaptive finite elements and mesh smoothing.  The
approach is detailed [here](https://arxiv.org/abs/2011.07919).

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
```

![img](https://user-images.githubusercontent.com/973268/91669738-02ff7b80-eb20-11ea-94c5-dfdc4365c9e6.png)

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

![img](https://user-images.githubusercontent.com/973268/91669743-14488800-eb20-11ea-8a16-0089d8ca081c.png)

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

![img](https://user-images.githubusercontent.com/973268/104822154-39c4fc80-5849-11eb-9f2c-057c05314b0c.png)

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

![img](https://user-images.githubusercontent.com/973268/104823817-a6de8f00-5855-11eb-9da4-6ff09aa5391b.png)

## Licensing

The main source code of `adaptmesh` is distributed under the MIT License.

`adaptmesh` ships with customized versions of the following packages:

- `tri v0.3.1.dev0` (ported to Python 3; MIT)
- `optimesh v0.6.2` (trimmed down version with minor changes to the edge
  flipping; the last version with MIT)
- `meshplex v0.12.3` (trimmed down version with minor changes, i.e. removal of
  unnecessary imports; the last version with MIT)

The licenses of the included packages can be found also in `LICENSE.md` and the
respective subdirectories, i.e. `./adaptmesh/*/LICENSE`. See `LICENSE.md` for
more information.

## Changelog

### Unreleased

### [0.2.0] - 2021-01-20

- Added: keyword argument `split` of `triangulate` allows further splitting
  the provided segments.  This is useful because the segment endpoints are
  always preserved in the final mesh.
- Added: keyword argument `holes` of `triangulate` allows specifying additional
  polygonal areas inside the domain that will be free of triangles in the final
  mesh.
