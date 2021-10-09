import unittest

from pyraxial import Rect


class TestRect(unittest.TestCase):

    def assertIf(self, a, b):
        if a:
            assert b

    def test_starimport(self):
        import pyraxial
        self.assertEqual(set(pyraxial.__all__), set(['Rect']))

    def test_new(self):
        a = Rect((1, 2, 3, 4))
        self.assertEqual(Rect.EMPTY, Rect(()))
        self.assertEqual(Rect.EMPTY, Rect([]))
        self.assertEqual(Rect.EMPTY, Rect(iter(())))
        self.assertEqual(Rect.EMPTY, Rect(Rect.EMPTY))
        self.assertEqual(a, Rect((1, 2, 3, 4)))
        self.assertEqual(a, Rect([1, 2, 3, 4]))
        self.assertEqual(a, Rect(iter((1, 2, 3, 4))))
        self.assertEqual(a, Rect(a))
        self.assertRaises(TypeError, lambda: Rect(1, 2, 3, 4))
        self.assertRaises(ValueError, lambda: Rect(1))
        self.assertRaises(ValueError, lambda: Rect((1, 2, 3)))
        self.assertRaises(ValueError, lambda: Rect(iter((1, 2, 3))))
        self.assertRaises(ValueError, lambda: Rect((1, 2, 3, 4, 5)))
        self.assertRaises(ValueError, lambda: Rect(iter((1, 2, 3, 4, 5))))

    def test_from_rect(self):
        types = (iter, tuple, list, Rect)
        a = ()
        for t in types:
            self.assertEqual(Rect.EMPTY, Rect.from_rect(t(a)))
        a = 1, 2, 3, 4
        for t in types:
            self.assertEqual((Rect((1, 2, 3, 4))), Rect.from_rect(t(a)))

    def test_from_size(self):
        self.assertEqual(Rect.from_size((1, 2)), Rect((0, 0, 1, 2)))

    def test_from_points(self):
        p = 1, 2
        q = 3, 4
        r = Rect((1, 2, 3, 4))
        self.assertEqual(Rect.from_points(p, q), r)

    def test_properties(self):
        self.assertRaises(IndexError, lambda: Rect.EMPTY.left)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.top)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.right)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.bottom)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.left_top)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.right_top)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.left_bottom)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.right_bottom)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.width)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.height)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.points)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.size)
        self.assertRaises(IndexError, lambda: Rect.EMPTY.area)
        rects = (1, 2, 3, 4), (-4, -3, -2, -1), (-2, -1, 1, 2), (0, 0, 0, 0)
        for left, top, right, bottom in rects:
            a = Rect((left, top, right, bottom))
            self.assertEqual(a.left, left)
            self.assertEqual(a.top, top)
            self.assertEqual(a.right, right)
            self.assertEqual(a.bottom, bottom)
            self.assertEqual(a.left_top, (left, top))
            self.assertEqual(a.right_top, (right, top))
            self.assertEqual(a.left_bottom, (left, bottom))
            self.assertEqual(a.right_bottom, (right, bottom))
            self.assertEqual(a.width, abs(right - left))
            self.assertEqual(a.height, abs(bottom - top))
            self.assertEqual(a.points, ((left, top), (right, bottom)))
            self.assertEqual(a.size, (abs(right - left), abs(bottom - top)))
            self.assertEqual(a.area, abs((right - left) * (bottom - top)))

    def test_move(self):
        s = Rect((1, 2, 3, 4))
        t = Rect((2, 4, 4, 6))
        d = 1, 2
        self.assertEqual(s.move(d), t)
        self.assertEqual(Rect.EMPTY.move(d), Rect.EMPTY)
        self.assertEqual(Rect.PLANE.move(d), Rect.PLANE)

    def test_eq(self):
        boxes = (
            (1, 2, 3, 4),
            (2, 3, 4, 5),
            (6, 7, 8, 9),
            (),
            [],
            Rect.EMPTY,
            Rect.PLANE)
        from itertools import product
        for a, b in product(boxes, repeat=2):
            self.assertEqual(tuple(a) == tuple(b), Rect(a) == Rect(b))
            self.assertEqual(tuple(a) == Rect(b), Rect(a) == tuple(b))

    def test_ne(self):
        boxes = (
            (1, 2, 3, 4),
            (2, 3, 4, 5),
            (6, 7, 8, 9),
            (),
            [],
            tuple(Rect.EMPTY),
            tuple(Rect.PLANE))
        from itertools import product
        for a, b in product(boxes, repeat=2):
            self.assertEqual(tuple(a) != tuple(b), Rect(a) != Rect(b))
            self.assertEqual(tuple(a) != Rect(b), Rect(a) != tuple(b))

    def test_le(self):
        a = Rect((1, 2, 3, 4))
        b = Rect((1, 1, 4, 4))
        z = Rect.EMPTY
        u = Rect.PLANE
        for x in a, b, z, u:
            self.assertTrue(x <= x)
            self.assertTrue(tuple(x) <= x)
            self.assertTrue(x <= tuple(x))
        for x, y in (z, a), (z, b), (a, u), (b, u), (a, b), (z, u):
            self.assertTrue(x <= y)
            self.assertTrue(tuple(x) <= y)
            self.assertTrue(x <= tuple(y))
            self.assertFalse(y <= x)
            self.assertFalse(tuple(y) <= x)
            self.assertFalse(y <= tuple(x))

    def test_ge(self):
        a = Rect((1, 2, 3, 4))
        b = Rect((1, 1, 4, 4))
        z = Rect.EMPTY
        u = Rect.PLANE
        for x in a, b, z, u:
            self.assertTrue(x >= x)
            self.assertTrue(tuple(x) >= x)
            self.assertTrue(x >= tuple(x))
        for x, y in (a, z), (b, z), (u, a), (u, b), (b, a), (u, z):
            self.assertTrue(x >= y)
            self.assertTrue(tuple(x) >= y)
            self.assertTrue(x >= tuple(y))
            self.assertFalse(y >= x)
            self.assertFalse(tuple(y) >= x)
            self.assertFalse(y >= tuple(x))

    def test_lt(self):
        a = Rect((1, 2, 3, 4))
        b = Rect((1, 1, 4, 4))
        z = Rect.EMPTY
        u = Rect.PLANE
        for x in a, b, z, u:
            self.assertFalse(x < x)
            self.assertFalse(tuple(x) < x)
            self.assertFalse(x < tuple(x))
        for x, y in (z, a), (z, b), (a, u), (b, u), (a, b), (z, u):
            self.assertTrue(x < y)
            self.assertTrue(tuple(x) < y)
            self.assertTrue(x < tuple(y))
            self.assertFalse(y < x)
            self.assertFalse(tuple(y) < x)
            self.assertFalse(y < tuple(x))

    def test_gt(self):
        a = Rect((1, 2, 3, 4))
        b = Rect((1, 1, 4, 4))
        z = Rect.EMPTY
        u = Rect.PLANE
        for x in a, b, z, u:
            self.assertFalse(x > x)
            self.assertFalse(tuple(x) > x)
            self.assertFalse(x > tuple(x))
        for x, y in (a, z), (b, z), (u, a), (u, b), (b, a), (u, z):
            self.assertTrue(x > y)
            self.assertTrue(tuple(x) > y)
            self.assertTrue(x > tuple(y))
            self.assertFalse(y > x)
            self.assertFalse(tuple(y) > x)
            self.assertFalse(y > tuple(x))

    def test_or(self):
        def test(a, b, c):
            self.assertEqual(a | b, c)
            self.assertEqual(a | tuple(b), c)
            self.assertEqual(tuple(a) | b, c)
            self.assertEqual(a | list(b), c)
            self.assertEqual(list(a) | b, c)
        test(Rect((1, 1, 2, 2)), Rect((1, 1, 2, 2)), Rect((1, 1, 2, 2)))
        test(Rect((1, 1, 3, 3)), Rect((2, 2, 4, 4)), Rect((1, 1, 4, 4)))
        test(Rect((1, 1, 2, 2)), Rect((3, 3, 4, 4)), Rect((1, 1, 4, 4)))
        test(Rect((1, 1, 2, 2)), Rect((2, 2, 3, 3)), Rect((1, 1, 3, 3)))
        test(Rect((1, 1, 2, 2)), Rect.EMPTY, Rect((1, 1, 2, 2)))
        test(Rect.EMPTY, Rect((1, 1, 2, 2)), Rect((1, 1, 2, 2)))
        test(Rect.EMPTY, Rect.EMPTY, Rect.EMPTY)

    def test_and(self):
        def test(a, b, c):
            self.assertEqual(a & b, c)
            self.assertEqual(a & tuple(b), c)
            self.assertEqual(tuple(a) & b, c)
            self.assertEqual(a & list(b), c)
            self.assertEqual(list(a) & b, c)
        test(Rect((1, 1, 2, 2)), Rect((1, 1, 2, 2)), Rect((1, 1, 2, 2)))
        test(Rect((1, 1, 3, 3)), Rect((2, 2, 4, 4)), Rect((2, 2, 3, 3)))
        test(Rect((1, 1, 2, 2)), Rect((3, 3, 4, 4)), Rect.EMPTY)
        test(Rect((1, 1, 2, 2)), Rect((2, 2, 3, 3)), Rect((2, 2, 2, 2)))
        test(Rect((1, 1, 2, 2)), Rect.EMPTY, Rect.EMPTY)
        test(Rect.EMPTY, Rect((1, 1, 2, 2)), Rect.EMPTY)
        test(Rect.EMPTY, Rect.EMPTY, Rect.EMPTY)

    def test_mul(self):
        a = Rect((1, 2, 3, 4))
        b = Rect((2, 4, 6, 8))
        self.assertEqual(Rect.EMPTY * 2, Rect.EMPTY)
        self.assertEqual(2 * Rect.EMPTY, Rect.EMPTY)
        self.assertEqual(a * 2, b)
        self.assertEqual(2 * a, b)

    def test_repr(self):
        self.assertEqual(repr(Rect.EMPTY), 'Rect(())')
        self.assertEqual(repr(Rect.PLANE), 'Rect((-inf, -inf, inf, inf))')
        self.assertEqual(repr(Rect((1, 2, 3, 4))), 'Rect((1, 2, 3, 4))')

    def test_str(self):
        self.assertEqual(str(Rect.EMPTY), '()')
        self.assertEqual(str(Rect.PLANE), '(-inf, -inf, inf, inf)')
        self.assertEqual(str(Rect((1, 2, 3, 4))), '(1, 2, 3, 4)')

    def test_identity_elements(self):
        for a in Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4)):
            self.assertEqual(a | Rect.EMPTY, a)
            self.assertEqual(a & Rect.PLANE, a)

    def test_absorbing_elements(self):
        for a in (Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4))):
            self.assertEqual(a | Rect.PLANE, Rect.PLANE)
            self.assertEqual(a & Rect.EMPTY, Rect.EMPTY)

    def test_enclose(self):
        from itertools import permutations
        a = Rect((1, 2, 3, 4))
        self.assertEqual(Rect.enclose(), Rect.EMPTY)
        self.assertEqual(Rect.enclose(Rect.EMPTY), Rect.EMPTY)
        self.assertEqual(Rect.enclose(Rect.EMPTY, Rect.EMPTY), Rect.EMPTY)
        self.assertEqual(Rect.enclose(a), a)
        self.assertEqual(Rect.enclose(a, a), a)
        self.assertEqual(Rect.enclose(a, Rect.EMPTY), a)
        self.assertEqual(Rect.enclose(Rect.EMPTY, a), a)
        rects = (
            Rect.EMPTY,
            Rect((1, 2, 3, 4)),
            Rect((2, 3, 4, 5)),
            Rect((6, 7, 8, 9))
        )
        expected = Rect((1, 2, 8, 9))
        for a, b, c, d in permutations(rects):
            self.assertEqual(Rect.enclose(a, b, c, d), expected)

    def test_overlap(self):
        a = Rect((1, 2, 3, 4))
        b = Rect((2, 3, 4, 5))
        c = Rect((2, 3, 3, 4))
        d = Rect((5, 6, 7, 8))
        self.assertEqual(Rect.overlap(), Rect.PLANE)
        self.assertEqual(Rect.overlap(Rect.EMPTY), Rect.EMPTY)
        self.assertEqual(Rect.overlap(Rect.EMPTY, Rect.EMPTY), Rect.EMPTY)
        self.assertEqual(Rect.overlap(a), a)
        self.assertEqual(Rect.overlap(a, a), a)
        self.assertEqual(Rect.overlap(a, Rect.EMPTY), Rect.EMPTY)
        self.assertEqual(Rect.overlap(Rect.EMPTY, a), Rect.EMPTY)
        self.assertEqual(Rect.overlap(a, b), c)
        self.assertEqual(Rect.overlap(b, a), c)
        self.assertEqual(Rect.overlap(a, d), Rect.EMPTY)
        self.assertEqual(Rect.overlap(d, a), Rect.EMPTY)

    def test_idempotency(self):
        for a in Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4)):
            self.assertEqual(a | a, a)
            self.assertEqual(a & a, a)

    def test_associativity(self):
        from itertools import product
        rects = (
            Rect.EMPTY, Rect.PLANE,
            Rect((1, 2, 3, 4)), Rect((2, 3, 4, 5)), Rect((6, 7, 8, 9))
        )
        for a, b, c in product(rects, repeat=3):
            self.assertEqual((a | b) | c, a | (b | c))
            self.assertEqual((a & b) & c, a & (b & c))

    def test_commutativity(self):
        from itertools import product
        rects = (
            Rect.EMPTY, Rect.PLANE,
            Rect((1, 2, 3, 4)), Rect((2, 3, 4, 5)), Rect((6, 7, 8, 9))
        )
        for a, b in product(rects, repeat=2):
            self.assertEqual(a | b, b | a)
            self.assertEqual(a & b, b & a)

    def test_absorbtion(self):
        from itertools import product
        rects = (
            Rect.EMPTY, Rect.PLANE,
            Rect((1, 2, 3, 4)), Rect((2, 3, 4, 5)), Rect((6, 7, 8, 9))
        )
        for a, b in product(rects, repeat=2):
            self.assertEqual(a | (a & b), a)
            self.assertEqual(a & (a | b), a)

    def test_least_element(self):
        for a in Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4)):
            self.assertTrue(Rect.EMPTY <= a)
            self.assertTrue(a >= Rect.EMPTY)

    def test_greatest_element(self):
        for a in Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4)):
            self.assertTrue(a <= Rect.PLANE)
            self.assertTrue(Rect.PLANE >= a)

    def test_reflexivity(self):
        for a in Rect.EMPTY, Rect.PLANE, Rect((1, 2, 3, 4)):
            self.assertTrue(a <= a)
            self.assertTrue(a >= a)

    def test_transitivity(self):
        from itertools import product
        rects = (
            Rect.EMPTY, Rect.PLANE,
            Rect((1, 2, 3, 4)), Rect((2, 3, 4, 5)), Rect((6, 7, 8, 9)),
            Rect((1, 1, 9, 9)), Rect((0, 0, 10, 10))
        )
        for a, b, c in product(rects, repeat=3):
            self.assertIf(a <= b and b <= c, a <= c)
            self.assertIf(a >= b and b >= c, a >= c)
            self.assertIf(a < b and b < c, a < c)
            self.assertIf(a > b and b > c, a > c)

    def test_antisymmetry(self):
        from itertools import product
        rects = (
            Rect.EMPTY, Rect.PLANE,
            Rect((1, 2, 3, 4)), Rect((2, 3, 4, 5)), Rect((6, 7, 8, 9)),
            Rect((1, 1, 9, 9)), Rect((0, 0, 10, 10))
        )
        for a, b in product(rects, repeat=2):
            self.assertEqual(a <= b and b <= a, a == b)
            self.assertEqual(a >= b and b >= a, a == b)

    def test_monotonicity(self):
        from itertools import product
        rects = (
            Rect.EMPTY, Rect.PLANE,
            Rect((1, 2, 3, 4)), Rect((2, 3, 4, 5)), Rect((6, 7, 8, 9)),
            Rect((1, 1, 9, 9)), Rect((0, 0, 10, 10))
        )
        for a1, a2, b1, b2 in product(rects, repeat=4):
            self.assertIf(a1 <= a2 and b1 <= b2, a1 | b1 <= a2 | b2)
            self.assertIf(a1 <= a2 and b1 <= b2, a1 & b1 <= a2 & b2)
            self.assertIf(a1 >= a2 and b1 >= b2, a1 | b1 >= a2 | b2)
            self.assertIf(a1 >= a2 and b1 >= b2, a1 & b1 >= a2 & b2)

    def test_semidistributivity(self):
        from itertools import product
        rects = (
            Rect.EMPTY, Rect.PLANE,
            Rect((1, 2, 3, 4)), Rect((2, 3, 4, 5)), Rect((6, 7, 8, 9)),
            Rect((1, 1, 9, 9)), Rect((0, 0, 10, 10))
        )
        for a, b, c in product(rects, repeat=3):
            self.assertTrue(a & (b | c) >= (a & b) | (a & c))
            self.assertTrue(a | (b & c) <= (a | b) & (a | c))

    def test_closed_regions(self):
        from itertools import permutations
        data = [
            [[ # an empty list returns an empty list.

            ], [

            ]],
            [[ # Rect.EMPTY overlaps nothing.
                Rect.EMPTY,
            ], [

            ]],
            [[ # Several Rect.EMPTY also overlap nothing.
                Rect.EMPTY,
                Rect.EMPTY,
                Rect.EMPTY,
            ], [

            ]],
            [[ # Any non-empty Rect overlaps Rect.EMPTY.
                Rect.EMPTY,
                [1, 1, 2, 2],
            ], [
                [1, 1, 2, 2],
            ]],
            [[ # Rect.PLANE overlaps Rect.PLANE.
                Rect.PLANE,
            ], [
                Rect.PLANE,
            ]],
            [[ # Rect.PLANE overlaps all other Rects.
                [1, 1, 2, 2],
                [3, 3, 4, 4],
                Rect.EMPTY,
                Rect.PLANE,
            ], [
                Rect.PLANE,
            ]],
            [[ # Identical Rects overlap the same area.
                [1, 1, 2, 2],
                [1, 1, 2, 2],
            ], [
                [1, 1, 2, 2],
            ]],
            [[ # Overlapping Rects overlap. Duh.
                [1, 1, 3, 3],
                [2, 2, 4, 4],
            ], [
                [1, 1, 4, 4],
            ]],
            [[ # Non-overlapping Rects don't overlap. Duh.
                [1, 1, 2, 2],
                [3, 3, 4, 4],
            ], [
                [1, 1, 2, 2],
                [3, 3, 4, 4],
            ]],
            [[ # A completely envelopped Rect gets absorbed.
                [1, 1, 4, 4],
                [2, 2, 3, 3],
            ], [
                [1, 1, 4, 4],
            ]],
            [[ # Adjacent Rects overlap.
                [1, 1, 2, 2],
                [2, 2, 3, 3],
            ], [
                [1, 1, 3, 3],
            ]],
            [[ # "Transitively" overlapping Rects get joined into the same BBox.
                [1, 2, 3, 4],
                [2, 3, 4, 5],
                [4, 5, 6, 7],
                [5, 6, 7, 8],
            ], [
                [1, 2, 7, 8],
            ]],
            [[ # And so on.
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
            ], [
                [1, 2, 3, 4],
                [5, 6, 7, 8],
                [11, 12, 13, 14],
                [15, 16, 17, 18],
                [10, 20, 30, 40],
                [50, 60, 70, 80],
            ]],
        ]
        for rects, expected in data:
            rects = map(Rect, rects)
            result = set(Rect.closed_regions(rects))
            expected = set(map(Rect, expected))
            self.assertEqual(result, expected)
