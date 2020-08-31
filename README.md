# adaptmesh

[![PyPI](https://img.shields.io/pypi/v/adaptmesh)](https://pypi.org/project/adaptmesh/)
[![PyPI - License](https://img.shields.io/pypi/l/adaptmesh)](https://opensource.org/licenses/MIT)

Create triangular meshes by harnessing the power of the adaptive process.

## Installation

```
pip install adaptmesh
```

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

The main source code of `adaptmesh` is distributed under the MIT License; see
LICENSE.

`adaptmesh` ships with customized versions of the following packages:

-   `tri` (ported to Python 3; MIT)
-   `optimesh` (forked from v0.6.2; last version with MIT - later versions are
    GPLv3; trimmed down version with minor changes)
-   `meshplex` (forked from v0.12.3; last version with MIT - later versions are
    GPLv3; trimmed down version with minor changes)
