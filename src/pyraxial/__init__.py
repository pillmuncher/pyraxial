"""
An algebraic take on axis-aligned rectangles.

This module aims to simplify working with bounding boxes.


It defines the class Rect with the following methods and attributes:
  * Two binary operators `|` ("join") and `&` ("meet").
  * Two identity elements with respect to `|` and `&`, `Rect.EMPTY` and
    `Rect.PLANE`.
  * Two variadic class methods `Rect.bounding_box(*rects)` and
    `Rect.intersection(*rects)` as generalizations of `|` and `&` over
    arbitrary numbers of rectangles.
  * A set of operators that define containment relations between rectangles.
  * A class method `Rect.bounding_boxes(rects)` that computes the bounding boxes
    for all subsets of "transitively" intersecting rectangles in a given set of
    rectangles.


The `Rect` class together with the `|` and `&` operations and the identity
elements form a ***complete lattice*** so that for all Rect objects a, b and
c the following laws hold:


Identity Elements:

    a | Rect.EMPTY  ==  a
    a & Rect.PLANE  ==  a


Absorbing Elements:

    a | Rect.PLANE  ==  Rect.PLANE
    a & Rect.EMPTY  ==  Rect.EMPTY


Idempotency:

    a | a  ==  a
    a & a  ==  a


Commutativity:

    a | b  ==  b | a
    a & b  ==  b & a


Associativity:

    (a | b) | c  ==  a | (b | c)
    (a & b) & c  ==  a & (b & c)


Absorption:

    a | (a & b)  ==  a
    a & (a | b)  ==  a


Since these laws already define a partially ordered set, the following laws also
hold:


Least Element:

    Rect.EMPTY ≦ a


Greatest Element:

    a ≦ Rect.PLANE


Reflexivity:

    a ≦ a


Transitivity:

    a ≦ b  and  b ≦ c   🡒   a ≦ c


Antisymmetry:

    a ≦ b  and  b ≦ a   🡘   a == b


Monotonicity:

    a1 ≦ a2  and  b1 ≦ b2   🡒   a1 | b1  ≦  a2 | b2
    a1 ≦ a2  and  b1 ≦ b2   🡒   a1 & b1  ≦  a2 & b2


Semidistributivity:

    (a & b) | (a & c)  ≦  a & (b | c)
    a | (b & c)  ≦  (a | b) & (a | c)


Notice the absence of the laws of distribution and modularity.


A rectangle is created like so:

    r = Rect(box)

where box is an already existing Rect object, tuple, list, iterator or other
iterable, provided it is either empty or contains/yields four numbers that
denote the left, top, right and bottom coordinates (in that order).  If box is
empty or its values are such that the resulting Rect would have negative width
or height the result will be Rect.EMPTY. Otherwise, a ValueError is raised.

Coordinate values increase from left to right and from top to bottom.  Therefor,
if left ≦ right and top ≦ bottom the resulting rectangle will be a Rect with the
specified coordinates.  If left > right or top > bottom the resulting rectangle
will equal Rect.EMPTY.

Rect objects are immutable and the properties have no setters.

All method results are covariant under subtyping.

Rect() and bounding_boxes() accept any type of iterable.  The operators however
work reliably only on sequence-like objects, but not iterators.  If you pass an
iterator as an argument, the behavior will be undefined, probably raising an
exception, or worse, causing inexplicably wrong results.

Rects can be used as a drop-in in contexts where axis-aligned rectangles are
represented by 4-tuples, like e.g. Pillow's Image.crop() method. For contexts
where such rectangles are represented as pairs of point coordinates the class
method Rect.from_points() and the Rect.points property can be used.


See API documentation here:

https://pillmuncher.github.io/pyraxial


Here are some usage examples:

>>> from pyraxial import Rect

>>> a = Rect((1, 2, 3, 4))

>>> a.left, a.top, a.right, a.bottom
(1, 2, 3, 4)

>>> a.points
((1, 2), (3, 4))

>>> a.width, a.height
(2, 2)

>>> b = Rect((2, 3, 4, 5))

>>> a | b
Rect((1, 2, 4, 5))

>>> a & b
Rect((2, 3, 3, 4))

>>> a & Rect.EMPTY == Rect.EMPTY
True

>>> a | Rect.PLANE == Rect.PLANE
True

>>> a | Rect.EMPTY == a & Rect.PLANE == a
True

>>> rects = [Rect((1, 2, 3, 4)), Rect((2, 3, 4, 5)), Rect((3, 4, 5, 6))]

>>> Rect.bounding_box(*rects)
Rect((1, 2, 5, 6))

>>> Rect.intersection(*rects)
Rect((3, 4, 3, 4))

>>> Rect.bounding_box(Rect.EMPTY, *rects) == Rect.bounding_box(*rects)
True

>>> Rect.bounding_box(Rect.PLANE, *rects) == Rect.PLANE
True

>>> Rect.intersection(Rect.EMPTY, *rects) == Rect.EMPTY
True

>>> Rect.intersection(Rect.PLANE, *rects) == Rect.intersection(*rects)
True

>>> rects += [Rect((7, 8, 8, 9)), Rect((8, 7, 9, 8))]

>>> set(Rect.bounding_boxes(rects)) == set(
...    [Rect((1, 2, 5, 6)), Rect((7, 7, 9, 9))])
True
"""

from dataclasses import dataclass
from itertools import chain
from numbers import Real
from operator import itemgetter

from itree import ITree


__all__ = ["Rect"]


def bounded_by(*limiters):
    """
    Create a function from limiters that takes any number of rects and
    applies these limiters to their corresponding coordinates.
    """

    def bound(*rects):
        "Return the upper or lower bound of rects, depending on limiters."
        for limit, coordinates in zip(limiters, zip(*rects)):
            yield limit(coordinates)

    return bound


inflate = bounded_by(min, min, max, max)
deflate = bounded_by(max, max, min, min)


X0, Y0, X1, Y1 = range(4)

left = itemgetter(X0)
right = itemgetter(X1)
top = itemgetter(Y0)
bottom = itemgetter(Y1)

left_top = itemgetter(X0, Y0)
right_top = itemgetter(X1, Y0)
left_bottom = itemgetter(X0, Y1)
right_bottom = itemgetter(X1, Y1)

horizontal = itemgetter(X0, X1)
vertical = itemgetter(Y0, Y1)


def points(rect):
    """Return the left top and right bottom points of rect."""
    return left_top(rect), right_bottom(rect)


def width(rect):
    """Return the width of rect."""
    return right(rect) - left(rect)


def height(rect):
    """Return the height of rect."""
    return bottom(rect) - top(rect)


def size(rect):
    """Return the width and height of rect."""
    return width(rect), height(rect)


def area(rect):
    """Return the area of rect."""
    return width(rect) * height(rect)


prop_doc = "The {0} of the rectangle.".format
coor_doc = prop_doc("{0} coordinate").format


invalid = ValueError(
    'Argument "box" must be an iterable of zero or four numbers.')


class MetaRect(type(tuple)):
    """
    A metaclass so we can have covariant polymorphic subtypes.

    Really.
    """

    def __init__(cls, name, bases, cdict):
        """
        Set up the two identity elements.
        """
        # We must do this in a metaclass so users are able to properly subclass
        # Rect. Otherwise a method that's invoked on e.g. a module level
        # attribute EMPTY would always return a Rect instance, even if the user
        # had subclassed Rect.  Creating these constants automatically on a
        # per-class-level does the trick.
        inf = float("inf")
        cls.EMPTY = cls(())
        cls.PLANE = cls((-inf, -inf, inf, inf))


class Rect(tuple, metaclass=MetaRect):
    __slots__ = ()

    left = property(left, doc=coor_doc("left"))
    right = property(right, doc=coor_doc("right"))
    top = property(top, doc=coor_doc("top"))
    bottom = property(bottom, doc=coor_doc("bottom"))

    left_top = property(left_top, doc=coor_doc("left top"))
    right_top = property(right_top, doc=coor_doc("right top"))
    left_bottom = property(left_bottom, doc=coor_doc("left bottom"))
    right_bottom = property(right_bottom, doc=coor_doc("right bottom"))

    vertical = property(vertical, doc=prop_doc("top and bottom coordinates"))
    horizontal = property(horizontal, doc=prop_doc(
        "left and right coordinates"))

    points = property(points, doc=prop_doc(
        "left top and right bottom coordinates"))

    width = property(width, doc=prop_doc("width"))
    height = property(height, doc=prop_doc("height"))

    size = property(size, doc=prop_doc("width and height"))
    area = property(area, doc=prop_doc("area"))

    def __new__(cls, box):
        """
        Create a new axis-aligned rectangle of type Rect from box.

        box must be an iterable of either zero or four numbers.  These are taken
        to be the left, top, right and bottom coordinates (in that order) of the
        rectangle.  If box is empty or its values are such that the resulting
        Rect would have negative width or height the result will be Rect.EMPTY.

        Raises ValueError if box is not iterable or of the wrong size.
        """
        try:
            box = tuple(box)
        except TypeError:
            raise invalid
        match box:
            case (x0, y0, x1, y1) if x0 <= x1 and y0 <= y1:
                return tuple.__new__(cls, box)
            case (x0, y0, x1, y1):
                return tuple.__new__(cls)
            case ():
                return tuple.__new__(cls)
            case _:
                raise invalid

    @classmethod
    def from_size(cls, size):
        """
        Takes a pair of numbers that represent the width and height of
        a rectangle and returns the rectangle Rect((0, 0, width, height)).
        """
        return cls.from_points((0, 0), size)

    @classmethod
    def from_points(cls, left_top, right_bottom):
        """
        Takes two pairs pf numbers (left, top) and (right, bottom) and returns
        the rectangle Rect((left, top, right, bottom)).
        """
        return cls(chain(left_top, right_bottom))

    @classmethod
    def bounding_box(cls, *rects):
        """
        Return the smallest rectangle that contains all rects, or Rect.EMPTY,
        if rects is empty.  This is also called the smallest upper bound or
        supremum of rects.  In computer graphics programming this is known as
        the minimal bounding box of rects.

        If any of the rects equals Rect.PLANE, the result will also be
        Rect.PLANE.
        """
        return cls(inflate(*filter(None, rects)))

    @classmethod
    def intersection(cls, *rects):
        """
        Return the greatest rectangle that is contained in all rects, or
        Rect.PLANE, if rects is empty.  This is also called the greatest lower
        bound or infimum of rects.

        If any of the rects equals Rect.EMPTY, the result will also be
        Rect.EMPTY.
        """
        return cls(deflate(cls.PLANE, *rects))

    @classmethod
    def partitions(cls, rects):
        """
        Partition rects into distinct sets of transitively intersecting
        rectangles.

        In other words, find all distinct sets of connected rectangles.  Two
        rectangles A and B are connected, if they either intersect or if there
        exists a rectangle C such that both A and B are connected to C.

        Since Rect.EMPTY trivially intersects with any other rect,
        it is always discarded.

        Time complexity is O(n log n + k) with respect to the number of distinct
        rects n and the number of intersections k. I hope.
        """
        return _connected_components(rects)

    @classmethod
    def bounding_boxes(cls, rects):
        """
        Join each distinct set of transitively intersecting rectangles in
        rects into a bounding box.

        In other words, the bounding box is the distinct set of connected
        rectangles.  Two rectangles A and B are connected, if they either
        intersect or if there exists a rectangle C such that both A and B are
        connected to C.

        Since Rect.EMPTY intersects with nothing and is intersected by any other
        rect, it is always discarded.

        Time complexity is O(n log n + k) with respect to the number n
        of distinct rects and the number k of intersection. I hope.
        """
        for region in cls.partitions(rects):
            yield cls.bounding_box(*region)

    def move(self, offsets):
        """
        Takes a pair of offsets (horizontal, vertical) and returns
        Rect((left+horizontal, top+vertical, right+horizontal, bottom+vertical)).
        """
        return type(self)(p + d for p, d in zip(self, tuple(offsets) * 2))

    def __or__(self, other):
        """
        The join operator.

        Return the smallest rectangle that contains both self and other or
        return Rect.EMPTY, if both are Rect.EMPTY.  This is also called the
        smallest upper bound or supremum of self and other.  In computer
        graphics programming this is known as the minimal bounding box of self
        and other.

        r1 | r2 | ... | rn is equivalent to Rect.bounding_box(r1, r2, ..., rn).
        """
        return self.bounding_box(self, other)

    __ror__ = __or__

    def __and__(self, other):
        """
        The meet operator.

        Return the greatest rectangle that is contained in both self and other
        or return Rect.EMPTY, if self and other don't intersect or one of them
        is Rect.EMPTY.  This is also called the greatest lower bound or infimum
        of self and other.

        r1 & r2 & ... & rn is equivalent to Rect.ntersection(r1, r2, ..., rn).
        """
        return self.intersection(self, other)

    __rand__ = __and__

    def __eq__(self, other):
        """
        Return True if self and other are rectangles with same coordinates,
        otherwise return False.
        """
        return isinstance(other, tuple) and tuple(self) == other

    def __ne__(self, other):
        """
        Return True if self and other are rectangles with different
        coordinates, otherwise return False.
        """
        return not isinstance(other, tuple) or tuple(self) != other

    def __le__(self, other):
        """
        Return True if other contains self, otherwise return False.
        """
        return self == self.intersection(self, other)

    def __ge__(self, other):
        """
        Return True if self contains other, otherwise return False.
        """
        return self == self.bounding_box(self, other)

    def __lt__(self, other):
        """
        Return True if other contains, but is not equal to self, otherwise
        return False.
        """
        return other != self == self.intersection(self, other)

    def __gt__(self, other):
        """
        Return True if self contains, but is not equal to other, otherwise
        return False.
        """
        return other != self == self.bounding_box(self, other)

    def __mul__(self, scalar):
        """
        Return a new rectangle with the coordinates multiplied by scalar.

        scalar must be a number.
        """
        return type(self)(value * scalar for value in self)

    __rmul__ = __mul__

    def __str__(self):
        """
        x.__str__() <==> str(x)
        """
        return str(tuple(self))

    def __repr__(self):
        """
        x.__repr__() <==> repr(x)
        """
        return "{0}({1})".format(type(self).__name__, self)

    # classes that derive from a hashable class but override __eq__ must also
    # define __hash__ to be hashable.
    __hash__ = tuple.__hash__


def _connected_components(rects):
    # This is the well known connected components algorithm.
    # It works here because we view intersecting rectangles as
    # connected nodes in a graph.
    #
    # As Alan Kay puts it: point of view is worth 80 IQ points.

    # EMPTY intersects with any other rect.
    # Equal rects intersect each other trivially.
    rects = frozenset(filter(None, rects))

    # Helper class for ITree:
    @dataclass(eq=True, frozen=True, slots=True)
    class Interval:
        rect: Rect
        start: Real
        end: Real

    # Collect intersecting rects into adjacency sets by intersecting
    # search results from a horizontal and a vertical Interval Tree:
    htree = ITree(Interval(rect, *horizontal(rect)) for rect in rects)
    vtree = ITree(Interval(rect, *vertical(rect)) for rect in rects)
    neighbors = {}
    for rect in rects:
        neighbors[rect] = frozenset(
            {i.rect for i in htree.search(Interval(rect, *horizontal(rect)))}
            & {i.rect for i in vtree.search(Interval(rect, *vertical(rect)))}
        )

    # Join adjacency sets into connected components:
    def component(node):
        todo = set([node])
        while todo:
            node = todo.pop()
            seen.add(node)
            todo |= neighbors[node] - seen
            yield node

    seen = set()
    for node in neighbors:
        if node not in seen:
            yield set(component(node))
