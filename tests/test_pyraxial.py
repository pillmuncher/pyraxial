import pytest

from pyraxial import Rect


def assert_if(a, b):
    if a:
        assert b


def assert_raises(error, test):
    with pytest.raises(error):
        test()


def test_starimport():
    import pyraxial

    assert set(pyraxial.__all__) == set(["Rect"])


def test_new():
    a = Rect((1, 2, 3, 4))
    assert Rect.EMPTY == Rect(())
    assert Rect.EMPTY == Rect([])
    assert Rect.EMPTY == Rect(iter(()))
    assert Rect.EMPTY == Rect(Rect.EMPTY)
    assert a == Rect((1, 2, 3, 4))
    assert a == Rect([1, 2, 3, 4])
    assert a == Rect(iter((1, 2, 3, 4)))
    assert a == Rect(a)
    assert_raises(TypeError, lambda: Rect(1, 2, 3, 4))
    assert_raises(ValueError, lambda: Rect(1))
    assert_raises(ValueError, lambda: Rect((1, 2, 3)))
    assert_raises(ValueError, lambda: Rect(iter((1, 2, 3))))
    assert_raises(ValueError, lambda: Rect((1, 2, 3, 4, 5)))
    assert_raises(ValueError, lambda: Rect(iter((1, 2, 3, 4, 5))))


def test_from_size():
    assert Rect.from_size((1, 2)) == Rect((0, 0, 1, 2))


def test_from_points():
    p = 1, 2
    q = 3, 4
    r = Rect((1, 2, 3, 4))
    assert Rect.from_points(p, q) == r


def test_properties():
    assert_raises(IndexError, lambda: Rect.EMPTY.left)
    assert_raises(IndexError, lambda: Rect.EMPTY.top)
    assert_raises(IndexError, lambda: Rect.EMPTY.right)
    assert_raises(IndexError, lambda: Rect.EMPTY.bottom)
    assert_raises(IndexError, lambda: Rect.EMPTY.left_top)
    assert_raises(IndexError, lambda: Rect.EMPTY.right_top)
    assert_raises(IndexError, lambda: Rect.EMPTY.left_bottom)
    assert_raises(IndexError, lambda: Rect.EMPTY.right_bottom)
    assert_raises(IndexError, lambda: Rect.EMPTY.width)
    assert_raises(IndexError, lambda: Rect.EMPTY.height)
    assert_raises(IndexError, lambda: Rect.EMPTY.points)
    assert_raises(IndexError, lambda: Rect.EMPTY.size)
    assert_raises(IndexError, lambda: Rect.EMPTY.area)
    rects = (1, 2, 3, 4), (-4, -3, -2, -1), (-2, -1, 1, 2), (0, 0, 0, 0)
    for left, top, right, bottom in rects:
        a = Rect((left, top, right, bottom))
        assert a.left == left
        assert a.top == top
        assert a.right == right
        assert a.bottom == bottom
        assert a.left_top == (left, top)
        assert a.right_top == (right, top)
        assert a.left_bottom == (left, bottom)
        assert a.right_bottom == (right, bottom)
        assert a.width == abs(right - left)
        assert a.height == abs(bottom - top)
        assert a.points == ((left, top), (right, bottom))
        assert a.size == (abs(right - left), abs(bottom - top))
        assert a.area == abs((right - left) * (bottom - top))


def test_move():
    s = Rect((1, 2, 3, 4))
    t = Rect((2, 4, 4, 6))
    d = 1, 2
    assert s.move(d) == t
    assert Rect.EMPTY.move(d) == Rect.EMPTY
    assert Rect.PLANE.move(d) == Rect.PLANE


def test_eq():
    boxes = (
        (1, 2, 3, 4),
        (2, 3, 4, 5),
        (6, 7, 8, 9),
        (),
        [],
        Rect.EMPTY,
        Rect.PLANE,
    )
    from itertools import product

    for a, b in product(boxes, repeat=2):
        assert (tuple(a) == tuple(b)) == (Rect(a) == Rect(b))
        assert (tuple(a) == Rect(b)) == (Rect(a) == tuple(b))


def test_ne():
    boxes = (
        (1, 2, 3, 4),
        (2, 3, 4, 5),
        (6, 7, 8, 9),
        (),
        [],
        tuple(Rect.EMPTY),
        tuple(Rect.PLANE),
    )
    from itertools import product

    for a, b in product(boxes, repeat=2):
        assert (tuple(a) != tuple(b)) == (Rect(a) != Rect(b))
        assert (tuple(a) != Rect(b)) == (Rect(a) != tuple(b))


def test_le():
    a = Rect((1, 2, 3, 4))
    b = Rect((1, 1, 4, 4))
    z = Rect.EMPTY
    u = Rect.PLANE
    for x in a, b, z, u:
        assert x <= x
        assert tuple(x) <= x
        assert x <= tuple(x)
    for x, y in (z, a), (z, b), (a, u), (b, u), (a, b), (z, u):
        assert x <= y
        assert tuple(x) <= y
        assert x <= tuple(y)
        assert not y <= x
        assert not tuple(y) <= x
        assert not y <= tuple(x)


def test_ge():
    a = Rect((1, 2, 3, 4))
    b = Rect((1, 1, 4, 4))
    z = Rect.EMPTY
    u = Rect.PLANE
    for x in a, b, z, u:
        assert x >= x
        assert tuple(x) >= x
        assert x >= tuple(x)
    for x, y in (a, z), (b, z), (u, a), (u, b), (b, a), (u, z):
        assert x >= y
        assert tuple(x) >= y
        assert x >= tuple(y)
        assert not y >= x
        assert not tuple(y) >= x
        assert not y >= tuple(x)


def test_lt():
    a = Rect((1, 2, 3, 4))
    b = Rect((1, 1, 4, 4))
    z = Rect.EMPTY
    u = Rect.PLANE
    for x in a, b, z, u:
        assert not x < x
        assert not tuple(x) < x
        assert not x < tuple(x)
    for x, y in (z, a), (z, b), (a, u), (b, u), (a, b), (z, u):
        assert x < y
        assert tuple(x) < y
        assert x < tuple(y)
        assert not y < x
        assert not tuple(y) < x
        assert not y < tuple(x)


def test_gt():
    a = Rect((1, 2, 3, 4))
    b = Rect((1, 1, 4, 4))
    z = Rect.EMPTY
    u = Rect.PLANE
    for x in a, b, z, u:
        assert not x > x
        assert not tuple(x) > x
        assert not x > tuple(x)
    for x, y in (a, z), (b, z), (u, a), (u, b), (b, a), (u, z):
        assert x > y
        assert tuple(x) > y
        assert x > tuple(y)
        assert not y > x
        assert not tuple(y) > x
        assert not y > tuple(x)


def test_or():
    def test(a, b, c):
        assert (a | b) == c
        assert (a | tuple(b)) == c
        assert (tuple(a) | b) == c
        assert (a | list(b)) == c
        assert (list(a) | b) == c

    test(Rect((1, 1, 2, 2)), Rect((1, 1, 2, 2)), Rect((1, 1, 2, 2)))
    test(Rect((1, 1, 3, 3)), Rect((2, 2, 4, 4)), Rect((1, 1, 4, 4)))
    test(Rect((1, 1, 2, 2)), Rect((3, 3, 4, 4)), Rect((1, 1, 4, 4)))
    test(Rect((1, 1, 2, 2)), Rect((2, 2, 3, 3)), Rect((1, 1, 3, 3)))
    test(Rect((1, 1, 2, 2)), Rect.EMPTY, Rect((1, 1, 2, 2)))
    test(Rect.EMPTY, Rect((1, 1, 2, 2)), Rect((1, 1, 2, 2)))
    test(Rect.EMPTY, Rect.EMPTY, Rect.EMPTY)


def test_and():
    def test(a, b, c):
        assert (a & b) == c
        assert (a & tuple(b)) == c
        assert (tuple(a) & b) == c
        assert (a & list(b)) == c
        assert (list(a) & b) == c

    test(Rect((1, 1, 2, 2)), Rect((1, 1, 2, 2)), Rect((1, 1, 2, 2)))
    test(Rect((1, 1, 3, 3)), Rect((2, 2, 4, 4)), Rect((2, 2, 3, 3)))
    test(Rect((1, 1, 2, 2)), Rect((3, 3, 4, 4)), Rect.EMPTY)
    test(Rect((1, 1, 2, 2)), Rect((2, 2, 3, 3)), Rect((2, 2, 2, 2)))
    test(Rect((1, 1, 2, 2)), Rect.EMPTY, Rect.EMPTY)
    test(Rect.EMPTY, Rect((1, 1, 2, 2)), Rect.EMPTY)
    test(Rect.EMPTY, Rect.EMPTY, Rect.EMPTY)


def test_mul():
    a = Rect((1, 2, 3, 4))
    b = Rect((2, 4, 6, 8))
    assert (Rect.EMPTY * 2) == Rect.EMPTY
    assert (2 * Rect.EMPTY) == Rect.EMPTY
    assert (a * 2) == b
    assert (2 * a) == b


def test_repr():
    assert repr(Rect.EMPTY) == "Rect(())"
    assert repr(Rect.PLANE) == "Rect((-inf, -inf, inf, inf))"
    assert repr(Rect((1, 2, 3, 4))) == "Rect((1, 2, 3, 4))"


def test_str():
    assert str(Rect.EMPTY) == "()"
    assert str(Rect.PLANE) == "(-inf, -inf, inf, inf)"
    assert str(Rect((1, 2, 3, 4))) == "(1, 2, 3, 4)"


def test_identity_elements():
    for a in Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4)):
        assert (a | Rect.EMPTY) == a
        assert (a & Rect.PLANE) == a


def test_absorbing_elements():
    for a in (Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4))):
        assert (a | Rect.PLANE) == Rect.PLANE
        assert (a & Rect.EMPTY) == Rect.EMPTY


def test_bounding_box():
    from itertools import permutations

    a = Rect((1, 2, 3, 4))
    assert Rect.bounding_box() == Rect.EMPTY
    assert Rect.bounding_box(Rect.EMPTY) == Rect.EMPTY
    assert Rect.bounding_box(Rect.EMPTY, Rect.EMPTY) == Rect.EMPTY
    assert Rect.bounding_box(a) == a
    assert Rect.bounding_box(a, a) == a
    assert Rect.bounding_box(a, Rect.EMPTY) == a
    assert Rect.bounding_box(Rect.EMPTY, a) == a
    rects = (Rect.EMPTY, Rect((1, 2, 3, 4)),
             Rect((2, 3, 4, 5)), Rect((6, 7, 8, 9)))
    expected = Rect((1, 2, 8, 9))
    for a, b, c, d in permutations(rects):
        assert Rect.bounding_box(a, b, c, d) == expected


def test_intersection():
    a = Rect((1, 2, 3, 4))
    b = Rect((2, 3, 4, 5))
    c = Rect((2, 3, 3, 4))
    d = Rect((5, 6, 7, 8))
    assert Rect.intersection() == Rect.PLANE
    assert Rect.intersection(Rect.EMPTY) == Rect.EMPTY
    assert Rect.intersection(Rect.EMPTY, Rect.EMPTY) == Rect.EMPTY
    assert Rect.intersection(a) == a
    assert Rect.intersection(a, a) == a
    assert Rect.intersection(a, Rect.EMPTY) == Rect.EMPTY
    assert Rect.intersection(Rect.EMPTY, a) == Rect.EMPTY
    assert Rect.intersection(a, b) == c
    assert Rect.intersection(b, a) == c
    assert Rect.intersection(a, d) == Rect.EMPTY
    assert Rect.intersection(d, a) == Rect.EMPTY


def test_idempotency():
    for a in Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4)):
        assert (a | a) == a
        assert (a & a) == a


def test_associativity():
    from itertools import product

    rects = (
        Rect.EMPTY,
        Rect.PLANE,
        Rect((1, 2, 3, 4)),
        Rect((2, 3, 4, 5)),
        Rect((6, 7, 8, 9)),
    )
    for a, b, c in product(rects, repeat=3):
        assert ((a | b) | c) == (a | (b | c))
        assert ((a & b) & c) == (a & (b & c))


def test_commutativity():
    from itertools import product

    rects = (
        Rect.EMPTY,
        Rect.PLANE,
        Rect((1, 2, 3, 4)),
        Rect((2, 3, 4, 5)),
        Rect((6, 7, 8, 9)),
    )
    for a, b in product(rects, repeat=2):
        assert (a | b) == (b | a)
        assert (a & b) == (b & a)


def test_absorbtion():
    from itertools import product

    rects = (
        Rect.EMPTY,
        Rect.PLANE,
        Rect((1, 2, 3, 4)),
        Rect((2, 3, 4, 5)),
        Rect((6, 7, 8, 9)),
    )
    for a, b in product(rects, repeat=2):
        assert (a | (a & b)) == a
        assert (a & (a | b)) == a


def test_least_element():
    for a in Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4)):
        assert Rect.EMPTY <= a
        assert a >= Rect.EMPTY


def test_greatest_element():
    for a in Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4)):
        assert a <= Rect.PLANE
        assert Rect.PLANE >= a


def test_reflexivity():
    for a in Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4)):
        assert a <= a
        assert a >= a


def test_transitivity():
    from itertools import product

    rects = (
        Rect.EMPTY,
        Rect.PLANE,
        Rect((1, 2, 3, 4)),
        Rect((2, 3, 4, 5)),
        Rect((6, 7, 8, 9)),
        Rect((1, 1, 9, 9)),
        Rect((0, 0, 10, 10)),
    )
    for a, b, c in product(rects, repeat=3):
        assert_if(a <= b and b <= c, a <= c)
        assert_if(a >= b and b >= c, a >= c)
        assert_if(a < b and b < c, a < c)
        assert_if(a > b and b > c, a > c)


def test_antisymmetry():
    from itertools import product

    rects = (
        Rect.EMPTY,
        Rect.PLANE,
        Rect((1, 2, 3, 4)),
        Rect((2, 3, 4, 5)),
        Rect((6, 7, 8, 9)),
        Rect((1, 1, 9, 9)),
        Rect((0, 0, 10, 10)),
    )
    for a, b in product(rects, repeat=2):
        assert (a <= b and b <= a) == (a == b)
        assert (a >= b and b >= a) == (a == b)


def test_monotonicity():
    from itertools import product

    rects = (
        Rect.EMPTY,
        Rect.PLANE,
        Rect((1, 2, 3, 4)),
        Rect((2, 3, 4, 5)),
        Rect((6, 7, 8, 9)),
        Rect((1, 1, 9, 9)),
        Rect((0, 0, 10, 10)),
    )
    for a1, a2, b1, b2 in product(rects, repeat=4):
        assert_if(a1 <= a2 and b1 <= b2, a1 | b1 <= a2 | b2)
        assert_if(a1 <= a2 and b1 <= b2, a1 & b1 <= a2 & b2)
        assert_if(a1 >= a2 and b1 >= b2, a1 | b1 >= a2 | b2)
        assert_if(a1 >= a2 and b1 >= b2, a1 & b1 >= a2 & b2)


def test_semidistributivity():
    from itertools import product

    rects = (
        Rect.EMPTY,
        Rect.PLANE,
        Rect((1, 2, 3, 4)),
        Rect((2, 3, 4, 5)),
        Rect((6, 7, 8, 9)),
        Rect((1, 1, 9, 9)),
        Rect((0, 0, 10, 10)),
    )
    for a, b, c in product(rects, repeat=3):
        assert (a & (b | c)) >= ((a & b) | (a & c))
        assert (a | (b & c)) <= ((a | b) & (a | c))


def test_enclosures():
    from itertools import permutations

    data = [
        [
            [],  # an empty list returns an empty list.
            [],
        ],
        [
            [  # Rect.EMPTY intersects with nothing.
                Rect.EMPTY,
            ],
            [],
        ],
        [
            [  # Several Rect.EMPTY also intersect with nothing.
                Rect.EMPTY,
                Rect.EMPTY,
                Rect.EMPTY,
            ],
            [],
        ],
        [
            [  # Any non-empty Rect intersects with Rect.EMPTY.
                Rect.EMPTY,
                [1, 1, 2, 2],
            ],
            [
                [1, 1, 2, 2],
            ],
        ],
        [
            [  # Rect.PLANE intersects with Rect.PLANE.
                Rect.PLANE,
            ],
            [
                Rect.PLANE,
            ],
        ],
        [
            [  # Rect.PLANE intersects with all other Rects.
                [1, 1, 2, 2],
                [3, 3, 4, 4],
                Rect.EMPTY,
                Rect.PLANE,
            ],
            [
                Rect.PLANE,
            ],
        ],
        [
            [  # Identical Rects intersect with the same area.
                [1, 1, 2, 2],
                [1, 1, 2, 2],
            ],
            [
                [1, 1, 2, 2],
            ],
        ],
        [
            [  # Intersecting Rects intersect. Duh.
                [1, 1, 3, 3],
                [2, 2, 4, 4],
            ],
            [
                [1, 1, 4, 4],
            ],
        ],
        [
            [  # Non-intersecting Rects don't intersect. Duh.
                [1, 1, 2, 2],
                [3, 3, 4, 4],
            ],
            [
                [1, 1, 2, 2],
                [3, 3, 4, 4],
            ],
        ],
        [
            [  # A completely envelopped Rect gets absorbed.
                [1, 1, 4, 4],
                [2, 2, 3, 3],
            ],
            [
                [1, 1, 4, 4],
            ],
        ],
        [
            [  # Adjacent Rects intersect with each other.
                [1, 1, 2, 2],
                [2, 2, 3, 3],
            ],
            [
                [1, 1, 3, 3],
            ],
        ],
        [
            [  # "Transitively" intersecting Rects get joined into the same BBox.
                [1, 2, 3, 4],
                [2, 3, 4, 5],
                [4, 5, 6, 7],
                [5, 6, 7, 8],
            ],
            [
                [1, 2, 7, 8],
            ],
        ],
        [
            [  # And so on.
                [1, 2, 2, 3],
                [2, 3, 3, 4],
                [5, 6, 6, 7],
                [6, 7, 7, 8],
                [11, 12, 12, 13],
                [12, 13, 13, 14],
                [15, 16, 16, 17],
                [16, 17, 17, 18],
                [10, 20, 20, 30],
                [20, 30, 30, 40],
                [50, 60, 60, 70],
                [60, 70, 70, 80],
            ],
            [
                [1, 2, 3, 4],
                [5, 6, 7, 8],
                [11, 12, 13, 14],
                [15, 16, 17, 18],
                [10, 20, 30, 40],
                [50, 60, 70, 80],
            ],
        ],
    ]
    for rects, expected in data:
        rects = map(Rect, rects)
        result = set(Rect.bounding_boxes(rects))
        expected = set(map(Rect, expected))
        assert result == expected
