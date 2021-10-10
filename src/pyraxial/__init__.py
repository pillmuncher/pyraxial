"""
An algebraic take on axis-aligned rectangles.

This module aims to simplify working with bounding boxes.

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


__all__ = ['Rect']


from collections import defaultdict, OrderedDict
from dataclasses import dataclass
from itertools import chain
from operator import itemgetter

from itree import ITree


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
        Create a new paraxial rectangle of type Rect from box.

        box must be an iterable of zero or four numbers.  These are taken to
        be the left, top, right and bottom coordinates (in that order) of the
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
        Takes a sequence of two elements that represent the width and height
        of a rectangle, returning Rect((0, 0, width, height)).
        """
        return cls.from_points((0, 0), size)

    @classmethod
    def from_points(cls, left_top, right_bottom):
        """
        Takes two sequences (left, top) and (right, bottom) and return the
        rectangle Rect((left, top, right, bottom)).
        """
        return cls(chain(left_top, right_bottom))

    @classmethod
    def enclose(cls, *rects):
        """
        Return the smallest rectangle that contains all rects, or Rect.EMPTY,
        if rects is empty.  This is also called the smallest upper bound or
        supremum of rects.  In computer graphics programming this is known as
        the minimal bounding box of rects.

        Mathematically speaking, it maps P(RECT) --> RECT, where RECT is the
        set of all paraxial rectangles and P(RECT) is the power set of RECT.

        If any of the rects equals Rect.PLANE, the result will also be
        Rect.PLANE.
        """
        return cls(inflate(*filter(None, rects)))

    @classmethod
    def overlap(cls, *rects):
        """
        Return the biggest rectangle that is contained in all rects, or
        Rect.PLANE, if rects is empty.  This is also called the greatest lower
        bound or infimum of rects.

        Mathematically speaking, it maps P(RECT) --> RECT, where RECT is the
        set of all paraxial rectangles and P(RECT) is the power set of RECT.

        If any of the rects equals Rect.EMPTY, the result will also be
        Rect.EMPTY.
        """
        return cls(deflate(Rect.PLANE, *rects))


    @classmethod
    def all_overlapping_areas(cls, rects):
        """
        Generate all sets of transitively overlapping rectangles in rects.

        In other words, find all sets of connected rectangles.  Two rectangles
        A and B are connected, if they either overlap or if there exists a
        rectangle C such that both A and B are connected to C.

        Since Rect.EMPTY has no area, rects that equal Rect.EMPTY are silently
        ignored.

        Time complexity is O(n log n + k) with respect to the number of distinct
        rects n and the number of overlaps k. I hope.
        """

        # Implementation of the well known connected components algorithm for
        # graphs. This works because we view overlapping rectangles as
        # connected nodes in a graph.
        #
        # As Alan Kay puts it: point of view is worth 80 IQ points.

        rects = set(rects)
        # EMPTY has no area:
        rects.discard(cls.EMPTY)

        # Helper class for ITree. Used in the Sweep Line algorithm below.
        @dataclass
        class Interval:

            rect: Rect

            @property
            def start(self):
                return self.rect.left

            @property
            def end(self):
                return self.rect.right

        # Sweep Line algorithm to set up adjacency sets, AKA neighbors:
        neighbors = defaultdict(set)
        status = ITree()
        events = sorted(chain.from_iterable(
                ((r.left, False, r), (r.right, True, r)) for r in rects))
        for _, is_right, rect in events:
            for interval in status.search(Interval(rect)):
                if rect & interval.rect:
                    neighbors[rect].add(interval.rect)
                    neighbors[interval.rect].add(rect)
            if is_right:
                status.remove(Interval(rect))
            else:
                status.insert(Interval(rect))

        # Collect the connected components:
        seen = set()

        def component(node, neighbors=neighbors, seen=seen, see=seen.add):
            """
            Generate all nodes of the component to which node belongs.
            """
            todo = set([node])
            next_todo = todo.pop
            while todo:
                node = next_todo()
                see(node)
                todo |= neighbors[node] - seen
                yield node

        for node in neighbors:
            if node not in seen:
                yield component(node)

    @classmethod
    def closed_regions(cls, rects):
        """
        Generate the bounding boxes of all closed regions in rects.

        In other words, find all sets of connected rectangles and generate the
        bounding box of each set.  Two rectangles A and B are connected, if
        they either overlap or if there exists a rectangle C such that both A
        and B are connected to C.

        Since Rect.EMPTY has no area, it also covers no region.

        Time complexity is O(n log n + k) with respect to the number n
        of distinct rects and the number k of overlaps. I hope.
        """

        for region in cls.all_overlapping_areas(rects):
            yield cls.enclose(*region)


    def move(self, offsets):
        """
        Takes a sequence of two offsets (horizontal, vertical) and return
        Rect((left+horizontal, top+vertical, right+horizontal, bottom+vertical)).
        """
        return type(self)(p + d for p, d in zip(self, tuple(offsets) * 2))

    def __or__(self, other):
        """
        The join operator.

        Return the smallest rectangle that contains both self and other or
        return Rect.EMPTY, if both are Rect.EMPTY.  This is also called the
        smallest upper bound or supremum of self and other.  In computer
        graphics programming this is known as the bounding box of self and
        other.

        r1 | r2 | ... | rn is equivalent to Rect.enclose(r1, r2, ..., rn).
        """
        return self.enclose(self, other)

    __ror__ = __or__

    def __and__(self, other):
        """
        The meet operator.

        Return the biggest rectangle that is contained in both self and other
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
        Return a new paraxial rectangle with the coordinates scaled by scalar.

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
