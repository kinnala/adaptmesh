# adaptmesh

[![PyPI](https://img.shields.io/pypi/v/adaptmesh)](https://pypi.org/project/adaptmesh/)
[![PyPI - License](https://img.shields.io/pypi/l/adaptmesh)](https://opensource.org/licenses/MIT)

Create triangular meshes by the adaptive process.

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

