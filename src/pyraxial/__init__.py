"""
An algebraic take on axis-aligned rectangles.

This module aims to simplify working with bounding boxes.


It defines the class Rect with the following methods and attributes:
  - Two binary operators | ("join") and & ("meet").
  - Two identity elements with respect to | and &, Rect.EMPTY and Rect.PLANE.
  - Two polyadic class methods Rect.enclose(rects) and Rect.overlap(rects)
    as generalizations of | and & over arbitrary numbers of rectangles.
  - A set of operators that define containment relations between rectangles.
  - A class method Rect.closed_regions(rects) that computes the bounding boxes
    for all subsets of "transitively" overlapping rectangles in a given set of
    rectangles.


The Rect class together with the | and & operations and the identity elements
forms a complete lattice so that for all Rect objects a, b and c the following
laws hold:


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

    a ≦ b  and  b ≦ a   🡘   a = b


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
denote the left, top, right and bottom coordinates (in that order). Otherwise,
a ValueError is raised.

Coordinate values increase from left to right and from top to bottom.  Therefor,
if left ≦ right and top ≦ bottom the resulting rectangle will be a Rect with the
specified coordinates.  If left > right or top > bottom the resulting rectangle
will equal Rect.EMPTY.

Rect objects are immutable and the properties have no setters.

All method results are covariant under subtyping.

Rect() and closed_regions() accept any type of iterable.  The operators however
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

>>> Rect.enclose(*rects)
Rect((1, 2, 5, 6))

>>> Rect.overlap(*rects)
Rect((3, 4, 3, 4))

>>> Rect.enclose(Rect.EMPTY, *rects) == Rect.enclose(*rects)
True

>>> Rect.enclose(Rect.PLANE, *rects) == Rect.PLANE
True

>>> Rect.overlap(Rect.EMPTY, *rects) == Rect.EMPTY
True

>>> Rect.overlap(Rect.PLANE, *rects) == Rect.overlap(*rects)
True

>>> rects += [Rect((7, 8, 8, 9)), Rect((8, 7, 9, 8))]

>>> set(Rect.closed_regions(rects)) == set(
...    [Rect((1, 2, 5, 6)), Rect((7, 7, 9, 9))])
True
"""


from itertools import chain
from operator import itemgetter

from itree import ITree


__all__ = ['Rect']


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


prop_doc = 'The {0} of the rectangle.'.format
coor_doc = prop_doc('{0} coordinate').format


invalid = ValueError(
    'Argument "box" must be an iterable of zero or four numbers.')


class MetaRect(type(tuple)):
    """
    A metaclass so we can have covariant polymorphic subtypes.

    Really.
    """
    def __init__(cls, name, bases, cdict):
        """
        Set up the two identity elements. We must do this in a metaclass so
        users are able to properly subclass Rect. Otherwise a method that's
        invoked on e.g. a module level attribute EMPTY would always return a
        Rect instance, even if the user had subclassed Rect.  Creating these
        constants automatically on a per-class-level does the trick.
        """
        inf = float('inf')
        cls.EMPTY = cls(())
        cls.PLANE = cls((-inf, -inf, inf, inf))


class Rect(tuple, metaclass=MetaRect):

    __slots__ = ()

    left = property(left, doc=coor_doc('left'))
    right = property(right, doc=coor_doc('right'))
    top = property(top, doc=coor_doc('top'))
    bottom = property(bottom, doc=coor_doc('bottom'))

    left_top = property(left_top, doc=coor_doc('left top'))
    right_top = property(right_top, doc=coor_doc('right top'))
    left_bottom = property(left_bottom, doc=coor_doc('left bottom'))
    right_bottom = property(right_bottom, doc=coor_doc('right bottom'))

    vertical = property(
        vertical, doc=prop_doc('top and bottom coordinates'))
    horizontal = property(
        horizontal, doc=prop_doc('left and right coordinates'))

    points = property(
        points, doc=prop_doc('left top and right bottom coordinates'))

    width = property(width, doc=prop_doc('width'))
    height = property(height, doc=prop_doc('height'))

    size = property(size, doc=prop_doc('width and height'))
    area = property(area, doc=prop_doc('area'))

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
        if not box:
            return tuple.__new__(cls)
        if len(box) != 4:
            raise invalid
        if box[X0] > box[X1] or box[Y0] > box[Y1]:
            return tuple.__new__(cls)
        return tuple.__new__(cls, box)

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
    def enclose(cls, *rects):
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
    def overlap(cls, *rects):
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
        Partition rects into distinct sets of transitively overlapping
        rectangles.

        In other words, find all distinct sets of connected rectangles.
        Two rectangles A and B are connected, if they either overlap or if there
        exists a rectangle C such that both A and B are connected to C.

        Since Rect.EMPTY overlaps nothing and is overlapped by any other rect,
        it is always discarded.

        Time complexity is O(n log n + k) with respect to the number of distinct
        rects n and the number of overlaps k. I hope.
        """
        return _connected_components(rects)

    @classmethod
    def enclosures(cls, rects):
        """
        Enclose each distinct set of transitively overlapping rectangles in
        rects by a bounding box.

        In other words, enclose each distinct set of connected rectangles.
        Two rectangles A and B are connected, if they either overlap or if there
        exists a rectangle C such that both A and B are connected to C.

        Since Rect.EMPTY overlaps nothing and is overlapped by any other rect,
        it is always discarded.

        Time complexity is O(n log n + k) with respect to the number n
        of distinct rects and the number k of overlaps. I hope.
        """
        for region in _connected_components(rects):
            yield cls.enclose(*region)

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

        r1 | r2 | ... | rn is equivalent to Rect.enclose(r1, r2, ..., rn).
        """
        return self.enclose(self, other)

    __ror__ = __or__

    def __and__(self, other):
        """
        The meet operator.

        Return the greatest rectangle that is contained in both self and other
        or return Rect.EMPTY, if self and other don't overlap or one of them is
        Rect.EMPTY.  This is also called the greatest lower bound or infimum of
        self and other.

        r1 & r2 & ... & rn is equivalent to Rect.overlap(r1, r2, ..., rn).
        """
        return self.overlap(self, other)

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
        return self == self.overlap(self, other)

    def __ge__(self, other):
        """
        Return True if self contains other, otherwise return False.
        """
        return self == self.enclose(self, other)

    def __lt__(self, other):
        """
        Return True if other contains, but is not equal to self, otherwise
        return False.
        """
        return other != self == self.overlap(self, other)

    def __gt__(self, other):
        """
        Return True if self contains, but is not equal to other, otherwise
        return False.
        """
        return other != self == self.enclose(self, other)

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
        return '{0}({1})'.format(type(self).__name__, self)

    __hash__ = tuple.__hash__  # classes that derive from a hashable class but
                               # override __eq__ must also define __hash__ to
                               # be hashable.


def _connected_components(rects):
    # Implementation of the well known connected components algorithm.
    # This works because we view overlapping rectangles as connected nodes
    # in a graph.
    #
    # As Alan Kay puts it: point of view is worth 80 IQ points.

    # EMPTY overlaps nothing and is overlapped by any other rect:
    rects = set(filter(None, rects))

    # Helper class for ITree:
    class Interval:
        __slots__ = 'rect', 'start', 'end'
        def __init__(self, rect, orientation):
            self.rect = rect
            self.start, self.end = orientation(rect)

    # Collect overlapping rects into adjacency sets by intersecting search
    # results from a horizontal and a vertical Interval Tree:
    htree = ITree(Interval(rect, horizontal) for rect in rects)
    vtree = ITree(Interval(rect, vertical) for rect in rects)
    neighbors = {}
    for rect in rects:
        neighbors[rect] = (
            frozenset(found.rect for found in
                htree.search(Interval(rect, horizontal)))
            & frozenset(found.rect for found in
                vtree.search(Interval(rect, vertical))))

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
