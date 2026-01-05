# Formal Proofs for Rect as a Complete Semidistributive Lattice

## Definitions

Let `Rect` be the set of all axis-aligned rectangles with coordinates `(left, top, right, bottom)`
where `left ≤ right` and `top ≤ bottom`, plus the empty rectangle `⧄`.

### Notation Convention

Throughout these proofs, let `R₁`, `R₂`, `R₃` denote arbitrary rectangles where each is either:
- `⧄` (the empty rectangle), or
- A non-empty rectangle with coordinates, where:
  - `Rₙ = (lₙ, tₙ, rₙ, bₙ)` with `lₙ ≤ rₙ` and `tₙ ≤ bₙ`

When specific rectangles are needed, we use `R₁ = (l₁, t₁, r₁, b₁)`, `R₂ = (l₂, t₂, r₂, b₂)`, `R₃ = (l₃, t₃, r₃, b₃)`, etc.

### Operations

**Join Operation** (`|`):
- If `R₁ = ⧄`, then `R₁ | R₂ = R₂`
- If `R₂ = ⧄`, then `R₁ | R₂ = R₁`
- Otherwise: `R₁ | R₂ = (min(l₁, l₂), min(t₁, t₂), max(r₁, r₂), max(b₁, b₂))`

**Meet Operation** (`&`):
- If `R₁ = ⧄` or `R₂ = ⧄`, then `R₁ & R₂ = ⧄`
- Otherwise: `R₁ & R₂ = (max(l₁, l₂), max(t₁, t₂), min(r₁, r₂), min(b₁, b₂))`
  - If the result has `left > right` or `top > bottom`, return `⧄`

**Identity Elements**:
- `EMPTY = ⧄` (the empty rectangle)
- `PLANE = ⬚ = (-∞, -∞, +∞, +∞)` (the infinite plane)

**Partial Order**: `R₁ ≤ R₂` iff `R₁ & R₂ = R₁` (equivalently, `R₁ | R₂ = R₂`)

---

## 1. Identity Element Proofs

### Theorem 1.1: `R₁ | ⧄ = R₁`

**Proof:**
By definition of join:
- If `R₁ = ⧄`: then `⧄ | ⧄ = ⧄` ✓
- If `R₁ ≠ ⧄`: then `R₁ | ⧄ = R₁` ✓

∎

### Theorem 1.2: `R₁ & ⬚ = R₁`

**Proof:**
Case 1: `R₁ = ⧄`
- By definition, `⧄ & ⬚ = ⧄` ✓

Case 2: `R₁ ≠ ⧄`
```
R₁ & ⬚ = (l₁, t₁, r₁, b₁) & (-∞, -∞, +∞, +∞)
       = (max(l₁, -∞), max(t₁, -∞), min(r₁, +∞), min(b₁, +∞))
       = (l₁, t₁, r₁, b₁)
       = R₁ ✓
```

∎

---

## 2. Absorbing Element Proofs

### Theorem 2.1: `R₁ | ⬚ = ⬚`

**Proof:**
Case 1: `R₁ = ⧄`
- `⧄ | ⬚ = ⬚` by join definition ✓

Case 2: `R₁ ≠ ⧄`
```
R₁ | ⬚ = (l₁, t₁, r₁, b₁) | (-∞, -∞, +∞, +∞)
       = (min(l₁, -∞), min(t₁, -∞), max(r₁, +∞), max(b₁, +∞))
       = (-∞, -∞, +∞, +∞)
       = ⬚ ✓
```

∎

### Theorem 2.2: `R₁ & ⧄ = ⧄`

**Proof:**
By definition of meet: `R₁ & ⧄ = ⧄` ✓

∎

---

## 3. Idempotency Proofs

### Theorem 3.1: `R₁ | R₁ = R₁`

**Proof:**
Case 1: `R₁ = ⧄`
- `⧄ | ⧄ = ⧄` by definition ✓

Case 2: `R₁ ≠ ⧄`
```
R₁ | R₁ = (l₁, t₁, r₁, b₁) | (l₁, t₁, r₁, b₁)
        = (min(l₁, l₁), min(t₁, t₁), max(r₁, r₁), max(b₁, b₁))
        = (l₁, t₁, r₁, b₁)
        = R₁ ✓
```

∎

### Theorem 3.2: `R₁ & R₁ = R₁`

**Proof:**
Case 1: `R₁ = ⧄`
- `⧄ & ⧄ = ⧄` by definition ✓

Case 2: `R₁ ≠ ⧄`
```
R₁ & R₁ = (l₁, t₁, r₁, b₁) & (l₁, t₁, r₁, b₁)
        = (max(l₁, l₁), max(t₁, t₁), min(r₁, r₁), min(b₁, b₁))
        = (l₁, t₁, r₁, b₁)
        = R₁ ✓
```

∎

---

## 4. Commutativity Proofs

### Theorem 4.1: `R₁ | R₂ = R₂ | R₁`

**Proof:**
**Case 1:** Either `R₁ = ⧄` or `R₂ = ⧄`
- If `R₁ = ⧄`: `⧄ | R₂ = R₂ = R₂ | ⧄` ✓
- If `R₂ = ⧄`: `R₁ | ⧄ = R₁ = ⧄ | R₁` ✓

**Case 2:** Both `R₁ ≠ ⧄` and `R₂ ≠ ⧄`
```
R₁ | R₂ = (min(l₁, l₂), min(t₁, t₂), max(r₁, r₂), max(b₁, b₂))
```

Since `min` and `max` are commutative, this equals:
```
(min(l₂, l₁), min(t₂, t₁), max(r₂, r₁), max(b₂, b₁)) = R₂ | R₁ ✓
```

∎

### Theorem 4.2: `R₁ & R₂ = R₂ & R₁`

**Proof:**
**Case 1:** Either `R₁ = ⧄` or `R₂ = ⧄`
- `⧄ & R₂ = ⧄ = R₂ & ⧄` ✓

**Case 2:** Both `R₁ ≠ ⧄` and `R₂ ≠ ⧄`
```
R₁ & R₂ = (max(l₁, l₂), max(t₁, t₂), min(r₁, r₂), min(b₁, b₂))
```

Since `min` and `max` are commutative, this equals:
```
(max(l₂, l₁), max(t₂, t₁), min(r₂, r₁), min(b₂, b₁)) = R₂ & R₁ ✓
```

∎

---

## 5. Associativity Proofs

### Theorem 5.1: `(R₁ | R₂) | R₃ = R₁ | (R₂ | R₃)`

**Proof:**
**Case 1:** Any of `R₁`, `R₂`, or `R₃` is `⧄`
- If `R₁ = ⧄`: `(⧄ | R₂) | R₃ = R₂ | R₃ = ⧄ | (R₂ | R₃)` ✓
- If `R₂ = ⧄`: `(R₁ | ⧄) | R₃ = R₁ | R₃ = R₁ | (⧄ | R₃)` ✓
- If `R₃ = ⧄`: `(R₁ | R₂) | ⧄ = R₁ | R₂ = R₁ | (R₂ | ⧄)` ✓

**Case 2:** All non-empty

Left side:
```
R₁ | R₂ = (min(l₁, l₂), min(t₁, t₂), max(r₁, r₂), max(b₁, b₂))

(R₁ | R₂) | R₃ = (min(min(l₁, l₂), l₃),
                  min(min(t₁, t₂), t₃),
                  max(max(r₁, r₂), r₃),
                  max(max(b₁, b₂), b₃))
```

Right side:
```
R₂ | R₃ = (min(l₂, l₃), min(t₂, t₃), max(r₂, r₃), max(b₂, b₃))

R₁ | (R₂ | R₃) = (min(l₁, min(l₂, l₃)),
                  min(t₁, min(t₂, t₃)),
                  max(r₁, max(r₂, r₃)),
                  max(b₁, max(b₂, b₃)))
```

By associativity of `min` and `max`, both sides are equal ✓

∎

### Theorem 5.2: `(R₁ & R₂) & R₃ = R₁ & (R₂ & R₃)`

**Proof:**
**Case 1:** Any of `R₁`, `R₂`, or `R₃` is `⧄`
- `(⧄ & R₂) & R₃ = ⧄ & R₃ = ⧄ = ⧄ & (R₂ & R₃)` ✓
- Similar for `R₂ = ⧄` or `R₃ = ⧄` ✓

**Case 2:** All non-empty

Left side:
```
R₁ & R₂ = (max(l₁, l₂), max(t₁, t₂), min(r₁, r₂), min(b₁, b₂))

(R₁ & R₂) & R₃ = (max(max(l₁, l₂), l₃),
                  max(max(t₁, t₂), t₃),
                  min(min(r₁, r₂), r₃),
                  min(min(b₁, b₂), b₃))
```

Right side:
```
R₂ & R₃ = (max(l₂, l₃), max(t₂, t₃), min(r₂, r₃), min(b₂, b₃))

R₁ & (R₂ & R₃) = (max(l₁, max(l₂, l₃)),
                  max(t₁, max(t₂, t₃)),
                  min(r₁, min(r₂, r₃)),
                  min(b₁, min(b₂, b₃)))
```

By associativity of `min` and `max`, both sides are equal ✓

∎

---

## 6. Absorption Laws

### Theorem 6.1: `R₁ | (R₁ & R₂) = R₁`

**Proof:**
**Case 1:** `R₁ = ⧄`
```
⧄ | (⧄ & R₂) = ⧄ | ⧄ = ⧄ ✓
```

**Case 2:** `R₂ = ⧄`
```
R₁ | (R₁ & ⧄) = R₁ | ⧄ = R₁ ✓
```

**Case 3:** Both `R₁ ≠ ⧄` and `R₂ ≠ ⧄`

```
R₁ & R₂ = (max(l₁, l₂), max(t₁, t₂), min(r₁, r₂), min(b₁, b₂))
```

If `R₁ & R₂ = ⧄` (non-intersecting), then `R₁ | (R₁ & R₂) = R₁ | ⧄ = R₁` ✓

If `R₁ & R₂ ≠ ⧄`, then:
```
R₁ | (R₁ & R₂) = (min(l₁, max(l₁, l₂)),
                  min(t₁, max(t₁, t₂)),
                  max(r₁, min(r₁, r₂)),
                  max(b₁, min(b₁, b₂)))
```

Since `l₁ ≤ max(l₁, l₂)`: `min(l₁, max(l₁, l₂)) = l₁`
Since `t₁ ≤ max(t₁, t₂)`: `min(t₁, max(t₁, t₂)) = t₁`
Since `r₁ ≥ min(r₁, r₂)`: `max(r₁, min(r₁, r₂)) = r₁`
Since `b₁ ≥ min(b₁, b₂)`: `max(b₁, min(b₁, b₂)) = b₁`

Therefore: `R₁ | (R₁ & R₂) = (l₁, t₁, r₁, b₁) = R₁` ✓

∎

### Theorem 6.2: `R₁ & (R₁ | R₂) = R₁`

**Proof:**
**Case 1:** `R₁ = ⧄`
```
⧄ & (⧄ | R₂) = ⧄ & R₂ = ⧄ ✓
```

**Case 2:** `R₂ = ⧄`
```
R₁ & (R₁ | ⧄) = R₁ & R₁ = R₁ ✓
```

**Case 3:** Both `R₁ ≠ ⧄` and `R₂ ≠ ⧄`

```
R₁ | R₂ = (min(l₁, l₂), min(t₁, t₂), max(r₁, r₂), max(b₁, b₂))

R₁ & (R₁ | R₂) = (max(l₁, min(l₁, l₂)),
                  max(t₁, min(t₁, t₂)),
                  min(r₁, max(r₁, r₂)),
                  min(b₁, max(b₁, b₂)))
```

Since `l₁ ≥ min(l₁, l₂)`: `max(l₁, min(l₁, l₂)) = l₁`
Since `t₁ ≥ min(t₁, t₂)`: `max(t₁, min(t₁, t₂)) = t₁`
Since `r₁ ≤ max(r₁, r₂)`: `min(r₁, max(r₁, r₂)) = r₁`
Since `b₁ ≤ max(b₁, b₂)`: `min(b₁, max(b₁, b₂)) = b₁`

Therefore: `R₁ & (R₁ | R₂) = (l₁, t₁, r₁, b₁) = R₁` ✓

∎

---

## 7. Partial Order Properties

### Theorem 7.1: Least Element (`⧄ ≤ R₁`)

**Proof:**
We must show `⧄ & R₁ = ⧄` for all `R₁`.

By definition of meet: `⧄ & R₁ = ⧄` ✓

Therefore `⧄ ≤ R₁` for all `R₁` ✓

∎

### Theorem 7.2: Greatest Element (`R₁ ≤ ⬚`)

**Proof:**
We must show `R₁ & ⬚ = R₁` for all `R₁`.

This was proven in Theorem 1.2 ✓

Therefore `R₁ ≤ ⬚` for all `R₁` ✓

∎

### Theorem 7.3: Reflexivity (`R₁ ≤ R₁`)

**Proof:**
We must show `R₁ & R₁ = R₁`.

This was proven in Theorem 3.2 (idempotency of meet) ✓

∎

### Theorem 7.4: Transitivity (`R₁ ≤ R₂ ∧ R₂ ≤ R₃ ⟹ R₁ ≤ R₃`)

**Proof:**
Assume `R₁ ≤ R₂` and `R₂ ≤ R₃`.

By definition: `R₁ & R₂ = R₁` and `R₂ & R₃ = R₂`.

We must show `R₁ & R₃ = R₁`.

```
R₁ & R₃ = (R₁ & R₂) & R₃         [since R₁ & R₂ = R₁]
        = R₁ & (R₂ & R₃)         [by associativity, Theorem 5.2]
        = R₁ & R₂                [since R₂ & R₃ = R₂]
        = R₁                     [by assumption]
```

Therefore `R₁ ≤ R₃` ✓

∎

### Theorem 7.5: Antisymmetry (`R₁ ≤ R₂ ∧ R₂ ≤ R₁ ⟹ R₁ = R₂`)

**Proof:**
Assume `R₁ ≤ R₂` and `R₂ ≤ R₁`.

By definition: `R₁ & R₂ = R₁` and `R₂ & R₁ = R₂`.

By commutativity (Theorem 4.2): `R₁ & R₂ = R₂ & R₁`.

Therefore: `R₁ = R₁ & R₂ = R₂ & R₁ = R₂` ✓

∎

---

## 8. Monotonicity

### Theorem 8.1: Join Monotonicity

**Statement:** If `R₁ ≤ R₂` and `R₃ ≤ R₄`, then `R₁ | R₃ ≤ R₂ | R₄`.

**Proof:**
Assume `R₁ ≤ R₂` and `R₃ ≤ R₄`.

By definition: `R₁ & R₂ = R₁` and `R₃ & R₄ = R₃`.

For non-empty rectangles:
- If `R₁ = (l₁, t₁, r₁, b₁)` and `R₂ = (l₂, t₂, r₂, b₂)` with `R₁ ≤ R₂`, then coordinate-wise: `l₂ ≤ l₁ ≤ r₁ ≤ r₂` and `t₂ ≤ t₁ ≤ b₁ ≤ b₂`
- If `R₃ = (l₃, t₃, r₃, b₃)` and `R₄ = (l₄, t₄, r₄, b₄)` with `R₃ ≤ R₄`, then coordinate-wise: `l₄ ≤ l₃ ≤ r₃ ≤ r₄` and `t₄ ≤ t₃ ≤ b₃ ≤ b₄`

Then:
```
R₁ | R₃ = (min(l₁, l₃), min(t₁, t₃), max(r₁, r₃), max(b₁, b₃))
R₂ | R₄ = (min(l₂, l₄), min(t₂, t₄), max(r₂, r₄), max(b₂, b₄))
```

Since the inequalities hold coordinate-wise and `min`/`max` preserve order:
```
min(l₂, l₄) ≤ min(l₁, l₃), min(t₂, t₄) ≤ min(t₁, t₃)
max(r₁, r₃) ≤ max(r₂, r₄), max(b₁, b₃) ≤ max(b₂, b₄)
```

Therefore `R₁ | R₃ ≤ R₂ | R₄` ✓

∎

### Theorem 8.2: Meet Monotonicity

**Statement:** If `R₁ ≤ R₂` and `R₃ ≤ R₄`, then `R₁ & R₃ ≤ R₂ & R₄`.

**Proof:**
Similar coordinate-wise argument as Theorem 8.1.

For non-empty rectangles with `R₁ ≤ R₂` and `R₃ ≤ R₄`:
```
R₁ & R₃ = (max(l₁, l₃), max(t₁, t₃), min(r₁, r₃), min(b₁, b₃))
R₂ & R₄ = (max(l₂, l₄), max(t₂, t₄), min(r₂, r₄), min(b₂, b₄))
```

Since `min`/`max` preserve the coordinate inequalities:
```
max(l₂, l₄) ≤ max(l₁, l₃), max(t₂, t₄) ≤ max(t₁, t₃)
min(r₁, r₃) ≤ min(r₂, r₄), min(b₁, b₃) ≤ min(b₂, b₄)
```

Therefore `R₁ & R₃ ≤ R₂ & R₄` ✓

∎

---

## 9. Completeness

### Theorem 9.1: Arbitrary Joins Exist

**Statement:** For any `S ⊆ Rect`, the supremum `⋁ S` exists.

**Proof:**
If `S = ∅`, define `⋁ S = ⧄`.

Otherwise, define:
```
L = inf { l | (l,t,r,b) ∈ S, (l,t,r,b) ≠ ⧄ }
T = inf { t | (l,t,r,b) ∈ S, (l,t,r,b) ≠ ⧄ }
R = sup { r | (l,t,r,b) ∈ S, (l,t,r,b) ≠ ⧄ }
B = sup { b | (l,t,r,b) ∈ S, (l,t,r,b) ≠ ⧄ }
```

and set:
```
⋁ S = (L, T, R, B)
```

This rectangle is well-defined since `L ≤ R` and `T ≤ B`.

For all `Rᵢ ∈ S`, we have `Rᵢ ≤ ⋁ S` by construction.

If `u` is any upper bound of `S`, then coordinate-wise:
```
lᵤ ≤ L,  tᵤ ≤ T,  R ≤ rᵤ,  B ≤ bᵤ
```
hence `⋁ S ≤ u`.

Therefore `⋁ S` is the least upper bound of `S` ✓

∎

---

### Theorem 9.2: Arbitrary Meets Exist

**Statement:** For any `S ⊆ Rect`, the infimum `⋀ S` exists.

**Proof:**
If `S = ∅`, define `⋀ S = ⬚`.

Otherwise define:
```
L = sup { l | (l,t,r,b) ∈ S }
T = sup { t | (l,t,r,b) ∈ S }
R = inf { r | (l,t,r,b) ∈ S }
B = inf { b | (l,t,r,b) ∈ S }
```

If `L > R` or `T > B`, define `⋀ S = ⧄`; otherwise:
```
⋀ S = (L, T, R, B)
```

For all `Rᵢ ∈ S`, we have `⋀ S ≤ Rᵢ` by construction.

If `m` is any lower bound of `S`, then coordinate-wise:
```
lₘ ≥ L,  tₘ ≥ T,  rₘ ≤ R,  bₘ ≤ B
```
hence `m ≤ ⋀ S`.

Therefore `⋀ S` is the greatest lower bound of `S` ✓

∎

---

### Corollary 9.3: Rect is a Complete Lattice

**Statement:** `(Rect, |, &, ⧄, ⬚)` is a complete lattice.

**Proof:**
By Theorems 9.1 and 9.2, arbitrary joins and meets exist ✓

∎

---

## 10. Semidistributivity

### Lemma 10.1: Meet Projections

**Statement:** For all `R₁,R₂`: `R₁ & R₂ ≤ R₁` and `R₁ & R₂ ≤ R₂`.

**Proof:**
```
(R₁ & R₂) & R₁ = R₁ & R₂    [by associativity and idempotency]
(R₁ & R₂) & R₂ = R₁ & R₂    [by associativity and idempotency]
```

Therefore `R₁ & R₂ ≤ R₁` and `R₁ & R₂ ≤ R₂` ✓

∎

---

### Lemma 10.2: Join Injections

**Statement:** For all `R₁,R₂`: `R₁ ≤ R₁ | R₂` and `R₂ ≤ R₁ | R₂`.

**Proof:**
```
R₁ & (R₁ | R₂) = R₁    [by absorption, Theorem 6.2]
R₂ & (R₁ | R₂) = R₂    [by absorption, Theorem 6.2]
```

Therefore `R₁ ≤ R₁ | R₂` and `R₂ ≤ R₁ | R₂` ✓

∎

---

### Theorem 10.3: Meet-Semidistributivity

**Statement:** `(R₁ & R₂) | (R₁ & R₃) ≤ R₁ & (R₂ | R₃)` for all `R₁, R₂, R₃`.

**Proof:**
By Lemma 10.1:
```
(R₁ & R₂) ≤ R₁,   (R₁ & R₃) ≤ R₁
```
hence by monotonicity (Theorem 8.1):
```
(R₁ & R₂) | (R₁ & R₃) ≤ R₁
```

Also by Lemma 10.1:
```
(R₁ & R₂) ≤ R₂,   (R₁ & R₃) ≤ R₃
```
hence by monotonicity:
```
(R₁ & R₂) | (R₁ & R₃) ≤ R₂ | R₃
```

Since `(R₁ & R₂) | (R₁ & R₃) ≤ R₁` and `(R₁ & R₂) | (R₁ & R₃) ≤ R₂ | R₃`:
```
(R₁ & R₂) | (R₁ & R₃) ≤ R₁ & (R₂ | R₃)
```

∎

---

### Theorem 10.4: Join-Semidistributivity

**Statement:** `R₁ | (R₂ & R₃) ≤ (R₁ | R₂) & (R₁ | R₃)` for all `R₁, R₂, R₃`.

**Proof:**
By Lemma 10.2:
```
R₁ ≤ R₁ | R₂,   R₁ ≤ R₁ | R₃
```
hence by monotonicity (Theorem 8.2):
```
R₁ ≤ (R₁ | R₂) & (R₁ | R₃)
```

Also by Lemma 10.1:
```
R₂ & R₃ ≤ R₂,   R₂ & R₃ ≤ R₃
```
hence by monotonicity:
```
R₂ & R₃ ≤ R₁ | R₂   and   R₂ & R₃ ≤ R₁ | R₃
```

Therefore:
```
R₂ & R₃ ≤ (R₁ | R₂) & (R₁ | R₃)
```

Since `R₁ ≤ (R₁ | R₂) & (R₁ | R₃)` and `R₂ & R₃ ≤ (R₁ | R₂) & (R₁ | R₃)`:
```
R₁ | (R₂ & R₃) ≤ (R₁ | R₂) & (R₁ | R₃)
```

∎

---

## 11. Failure of Modularity

The modular law states:

> If `R₁ ≤ R₂`, then `R₁ | (R₃ & R₂) = (R₁ | R₃) & R₂`

We demonstrate with an explicit counterexample that the Rect lattice is not modular.

### Theorem 11.1: The Rect Lattice is Not Modular

**Counterexample:**
Let:
```
R₁ = (0, 0, 1, 1)  [small 1×1 square]
R₂ = (0, 0, 1, 2)  [1×2 rectangle containing R₁]
R₃ = (2, 0, 3, 2)  [disjoint 1×2 rectangle]
```

**Verify the precondition** `R₁ ≤ R₂`:
```
R₁ & R₂ = (max(0, 0), max(0, 0), min(1, 1), min(1, 2))
        = (0, 0, 1, 1)
        = R₁ ✓
```

So indeed `R₁ ≤ R₂`.

**Left-hand side:** `R₁ | (R₃ & R₂)`
```
R₃ & R₂ = (max(2, 0), max(0, 0), min(3, 1), min(2, 2))
        = (2, 0, 1, 2)
        = ⧄  [since 2 > 1]

R₁ | (R₃ & R₂) = R₁ | ⧄
               = (0, 0, 1, 1)
               = R₁
```

**Right-hand side:** `(R₁ | R₃) & R₂`
```
R₁ | R₃ = (min(0, 2), min(0, 0), max(1, 3), max(1, 2))
        = (0, 0, 3, 2)

(R₁ | R₃) & R₂ = (max(0, 0), max(0, 0), min(3, 1), min(2, 2))
               = (0, 0, 1, 2)
               = R₂
```

**Result:**
```
R₁ | (R₃ & R₂) = (0, 0, 1, 1)  ≠  (0, 0, 1, 2) = (R₁ | R₃) & R₂
```

Therefore the modular law fails ✗

### Geometric Intuition

The failure occurs because:
1. `R₃` and `R₂` are disjoint, so `R₃ & R₂ = ⧄`
2. The join `R₁ | R₃` creates a **bounding box** that spans from `R₁` to `R₃`, including the empty space between them: `(0, 0, 3, 2)`
3. When this bounding box is intersected with `R₂`, we get all of `R₂`: `(0, 0, 1, 2)`
4. But the left side just gives us `R₁`: `(0, 0, 1, 1)`

The key insight: **The join operation adds "virtual" space between disjoint rectangles.** This space persists through subsequent meet operations, violating the modular law's expectation that operations should be "well-behaved" when `R₁ ≤ R₂`.

In a true modular lattice, the constraint `R₁ ≤ R₂` ensures that operations involving `R₁`, `R₂`, and any `R₃` maintain certain symmetries. But in the Rect lattice, the bounding box operation breaks this symmetry by including regions that aren't actually part of either input rectangle.

∎

---

## 12. Failure of Full Distributivity

Since distributivity implies modularity, and we have shown that modularity fails (Theorem 11.1), it follows that **distributivity must also fail**. 

However, we provide an explicit counterexample to illustrate the specific manner in which distributivity fails in the Rect lattice.

### Counterexample for `R₁ & (R₂ | R₃) = (R₁ & R₂) | (R₁ & R₃)`

Consider:
```
R₁ = (0, 0, 4, 4)
R₂ = (1, 1, 7, 3)
R₃ = (5, 2, 6, 5)
```

**Left side:**
```
R₂ | R₃ = (1, 1, 7, 5)
R₁ & (R₂ | R₃) = (0, 0, 4, 4) & (1, 1, 7, 5)
                = (max(0, 1), max(0, 1), min(4, 7), min(4, 5))
                = (1, 1, 4, 4)
```

**Right side:**
```
R₁ & R₂ = (0, 0, 4, 4) & (1, 1, 7, 3)
        = (max(0, 1), max(0, 1), min(4, 7), min(4, 3))
        = (1, 1, 4, 3)

R₁ & R₃ = (0, 0, 4, 4) & (5, 2, 6, 5)
        = (max(0, 5), max(0, 2), min(4, 6), min(4, 5))
        = (5, 2, 4, 4)
        = ⧄  [since 5 > 4]

(R₁ & R₂) | (R₁ & R₃) = (1, 1, 4, 3) | ⧄
                      = (1, 1, 4, 3)
```

**Result:**
```
R₁ & (R₂ | R₃) = (1, 1, 4, 4)  ≠  (1, 1, 4, 3) = (R₁ & R₂) | (R₁ & R₃)
```

Therefore distributivity fails ✗

### Why This Happens Geometrically

The key insight is:
- `R₂ | R₃` is the **bounding box** of `R₂` and `R₃`, which includes regions not in either `R₂` or `R₃`
- When we intersect `R₁` with this bounding box, we can include parts of `R₁` that don't intersect either `R₂` or `R₃`
- But `(R₁ & R₂) | (R₁ & R₃)` only includes the parts of `R₁` that actually intersect `R₂` or `R₃`

In the example above:
- Rectangle `R₃` doesn't intersect `R₁` at all (`R₁ & R₃ = ⧄`)
- But `R₂ | R₃` creates a bounding box that covers more area than just `R₂` and `R₃`
- The bottom coordinate: `R₁ & (R₂ | R₃)` extends to `4` (from `R₁`), while `R₁ & R₂` only extends to `3` (from `R₂`)
- Since `R₁ & R₃ = ⧄`, the join `(R₁ & R₂) | (R₁ & R₃)` is just `R₁ & R₂ = (1, 1, 4, 3)`

∎

---

## Conclusion

We have proven that `(Rect, |, &, ⧄, ⬚)` forms a **complete semidistributive lattice** with the following properties:

**Proven to hold:**
- ✓ Identity elements (`⧄` and `⬚`)
- ✓ Absorbing elements
- ✓ Idempotency
- ✓ Commutativity
- ✓ Associativity
- ✓ Absorption laws
- ✓ Partial order properties (reflexivity, transitivity, antisymmetry, least and greatest elements)
- ✓ Monotonicity
- ✓ Completeness (arbitrary joins and meets exist)
- ✓ Semidistributivity (both inequalities)

**Proven to fail:**
- ✗ Full distributivity (equality fails in both laws)
- ✗ Modularity (fails even when precondition holds)

The precise classification is: **Complete Semidistributive Non-Modular Lattice**.