![GitHub release (latest by date)](https://img.shields.io/github/v/release/pillmuncher/pyraxial)
[![license](https://img.shields.io/badge/license-MIT-blue)](https://img.shields.io/badge/license-MIT-blue)
[![Build Status](https://app.travis-ci.com/pillmuncher/pyraxial.svg?branch=main)](https://app.travis-ci.com/pillmuncher/pyraxial)
[![codecov](https://codecov.io/gh/pillmuncher/pyraxial/branch/main/graph/badge.svg?token=3Q4CRWL8SX)](https://codecov.io/gh/pillmuncher/pyraxial)
# pyraxial
## An algebraic take on axis-aligned rectangles.

This module aims to simplify working with bounding boxes.


It defines the class Rect with the following methods and attributes:
  - Two binary operators `|` ("join") and `&` ("meet").
  - Two identity elements with respect to `|` and `&`, `Rect.EMPTY` and `Rect.PLANE`.
  - Two polyadic class methods `Rect.enclose(rects)` and `Rect.overlap(rects)`
    as generalizations of `|` and `&` over arbitrary numbers of rectangles.
  - A set of operators that define containment relations between rectangles.
  - A class method `Rect.enclosures(rects)` that computes the bounding boxes
    for all subsets of "transitively" overlapping rectangles in a given set of
    rectangles.


The `Rect` class together with the `|` and `&` operations and the identity elements
forms a ***complete lattice*** so that for all Rect objects a, b and c the
following laws hold:

### Identity Elements:
```
    a | Rect.EMPTY  ==  a
    a & Rect.PLANE  ==  a
```

### Absorbing Elements:
```
    a | Rect.PLANE  ==  Rect.PLANE
    a & Rect.EMPTY  ==  Rect.EMPTY
```

### Idempotency:
```
    a | a  ==  a
    a & a  ==  a
```

### Commutativity:
```
    a | b  ==  b | a
    a & b  ==  b & a
```

### Associativity:
```
    (a | b) | c  ==  a | (b | c)
    (a & b) & c  ==  a & (b & c)
```

### Absorption:
```
    a | (a & b)  ==  a
    a & (a | b)  ==  a
```



Since these laws already define a *partially ordered set*, the following laws also hold:

### Least Element:
```
    Rect.EMPTY ≦ a
```

### Greatest Element:
```
    a ≦ Rect.PLANE
```

### Reflexivity:
```
    a ≦ a
```

### Transitivity:
```
    a ≦ b  and  b ≦ c   🡒   a ≦ c
```

### Antisymmetry:
```
    a ≦ b  and  b ≦ a   🡘   a = b
```

### Monotonicity:
```
    a1 ≦ a2  and  b1 ≦ b2   🡒   a1 | b1  ≦  a2 | b2
    a1 ≦ a2  and  b1 ≦ b2   🡒   a1 & b1  ≦  a2 & b2
```

### Semidistributivity:
```
    (a & b) | (a & c)  ≦  a & (b | c)
    a | (b & c)  ≦  (a | b) & (a | c)
```

Notice the absence of the laws of distribution and modularity.


A rectangle is created like so:
```
    r = Rect(box)
```

where `box` is an already existing `Rect` object, tuple, list, iterator or other
iterable, provided it is either empty or contains/yields four numbers that
denote the `left`, `top`, `right` and `bottom` coordinates (in that order). Otherwise,
a `ValueError` is raised.

Coordinate values increase from left to right and from top to bottom.  Therefor,
if `left ≦ right` and `top ≦ bottom` the resulting rectangle will be a Rect with the
specified coordinates.  If `left > right` or `top > bottom` the resulting rectangle
will equal `Rect.EMPTY`.

`Rect` objects are immutable and the properties have no setters.

All method results are *covariant under subtyping*.


`Rect()` and `enclosures()` accept any type of iterable.  The operators however
work reliably only on sequence-like objects, but not iterators.  If you pass an
iterator as an argument, the behavior will be undefined, probably raising an
exception, or worse, causing inexplicably wrong results.

Rects can be used as a drop-in in contexts where axis-aligned rectangles are
represented by 4-tuples, like e.g. Pillow's `Image.crop()` method. For contexts
where such rectangles are represented as pairs of point coordinates the class
method `Rect.from_points` and the `Rect.points` property can be used.


### See API documentation here:
[https://pillmuncher.github.io/pyraxial](https://pillmuncher.github.io/pyraxial)
