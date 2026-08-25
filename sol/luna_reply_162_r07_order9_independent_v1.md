# Luna reply 162 — R07 order-9 independent replay v1

## 0. Scope and terminal

- Role: mechanical independent replay only.
- Narrow result: **PASS** for the claim that the fixed R07 pair has exact order (9) under the canonical finite GT-shadow composition law at the frozen (K_2) quotient.
- Final marker: `LUNA_R07_ORDER9_INDEPENDENT_REPLAY_PASS`.
- Evidence grade: **candidate (independent mechanical replay)**.  The implementation is independent of the producer, but this report does not self-promote the claim to project-level `cross-checked`, and it is not Lean `verified`.
- I did **not** open, import, execute, or copy helper code from `search/d972_rung_ordinary_idx3_producer_v2.py`.  No producer/checker implementation was read.  The replay was a fresh inline Python 3.13.14 implementation using only the standard library and the two pinned inputs below.
- No source/checker artifact was created, and no git or GHA operation was performed.  The only persistent write is this report.

## 1. Pinned inputs

1. `docs/week1-定義ノート.md`
   - SHA-256: `24db1372fd191659f1f0149cb669870dff470db1f779d3e5f83dba4171501c6c`
   - Used for the composition law and the (D_n^3) marked map.
2. `ci/ordinary_idx3_artifacts_32682548731/d972_rung_ordinary_idx3_producer_receipt_v2_20260824.json`
   - SHA-256: `48512270d265753944ff9b86d19fa5e84095ffffd8ae78beba969088c31053e9`
   - R07 datum is at JSON pointer `/registered_contract_snapshot/row36_raw_fibre/raw_roster/6`.
   - R07 row SHA-256: `eb89776d7f5f5551de12410adc176e96825aa130b47afa6df815797859ead440`.

The receipt fixes

\[
m=0,
\qquad
f=\bigl(((4,0),(32,0),(0,0)),\operatorname{id}_{9},0\bigr)
   \in G_{36}\times PSL(2,8)\times C_3.
\]

Its signed (x,y)-word, with `1,-1,2,-2` denoting
(x,x^{-1},y,y^{-1}), is

```text
[1,1,1,1,-2,-2,-2,-2,-1,2,-1,-1,-2,-1,-1,2,-1,-1,-2,-1,-1,-2,-1,-1,2,-1,1,2,1,1,-2,1,-1,-2,-1,-1,2,-1]
```

It has length (38).  The SHA-256 of its compact JSON serialization is
`6bd02922d1ccaf41323d68167269bc8d7087d11aacbcf206df2a933a3b32aa00`, exactly the receipt's `source_word_sha256`.

## 2. Independent reconstruction of the quotient law

I represented an element of (D_{36}) as

\[
(a,e)=r^a s^e,
\qquad a\in\mathbf Z/36,\quad e\in\mathbf Z/2.
\]

Using (sr^b=r^{-b}s), I implemented multiplication directly as

\[
(a,e)(b,d)=\bigl(a+(-1)^e b\pmod {36},\ e+d\pmod2\bigr).
\]

Thus

\[
(a,0)^{-1}=(-a,0),\qquad (a,1)^{-1}=(a,1).
\]

The implementation separately checked

```text
r^36       = (0,0)
s^2        = (0,0)
s r s^-1   = (35,0) = r^-1
```

The (G_{36}\leq D_{36}^3) operation was reconstructed componentwise.  The other two factors were implemented independently as follows:

- for one-line permutations, paper product (pq=p\circ q), hence `(p*q)[i] = p[q[i]]`;
- for (C_3), addition of exponents modulo (3).

The receipt's marked generators were transcribed as

\[
\begin{aligned}
x&=\bigl(((1,0),(0,1),(0,1)),
          [8,5,2,1,9,7,4,3,6],2\bigr),\\
y&=\bigl(((1,1),(1,0),(1,1)),
          [2,6,7,5,8,4,1,9,3],2\bigr).
\end{aligned}
\]

The signed word was accumulated from left to right in the paper product.  A raw replay gave

\[
W(x,y)=\bigl(((4,0),(32,0),(0,0)),[1,2,3,4,5,6,7,8,9],0\bigr)=f.
\]

This checks the frozen representative before using it in the automorphism calculation.

## 3. Direct replay of (E_{0,f}(f))

For (m=0), the definition gives

\[
E_{0,f}(x)=x,
\qquad
E_{0,f}(y)=f^{-1}yf.
\]

The direct product inverse is

\[
f^{-1}=\bigl(((32,0),(4,0),(0,0)),\operatorname{id}_9,0\bigr).
\]

Direct multiplication, without a producer helper, gave

\[
f^{-1}yf
=\bigl(((29,1),(1,0),(1,1)),
       [2,6,7,5,8,4,1,9,3],2\bigr).
\]

For example, the first dihedral coordinate is

\[
(32,0)(1,1)(4,0)=(33,1)(4,0)=(29,1).
\]

Replaying the same frozen 38-letter word with
(x\mapsto x) and (y\mapsto f^{-1}yf) returned

\[
W\bigl(x,f^{-1}yf\bigr)
=\bigl(((4,0),(32,0),(0,0)),\operatorname{id}_9,0\bigr)
=f.
\]

Therefore the literal quotient replay establishes

\[
E_{0,f}(f)=f.
\]

## 4. Exact order under the GT-shadow composition law

The authoritative law is

\[
[m_1,f_1]\circ[m_2,f_2]
=\bigl[2m_1m_2+m_1+m_2,\ f_1E_{m_1,f_1}(f_2)\bigr].
\]

Because (m=0), the first coordinate stays (0).  Since (E=E_{0,f}) is a homomorphism and (E(f)=f), right-associated induction gives

\[
[0,f]^k=[0,f^k]\qquad(k\geq0).
\]

All (PSL(2,8)) and (C_3) coordinates of (f^k) are trivial.  The independently generated (G_{36}) power table is

| (k) | first coordinate | second coordinate | third coordinate |
|---:|:---:|:---:|:---:|
| 0 | `(0,0)` | `(0,0)` | `(0,0)` |
| 1 | `(4,0)` | `(32,0)` | `(0,0)` |
| 2 | `(8,0)` | `(28,0)` | `(0,0)` |
| 3 | `(12,0)` | `(24,0)` | `(0,0)` |
| 4 | `(16,0)` | `(20,0)` | `(0,0)` |
| 5 | `(20,0)` | `(16,0)` | `(0,0)` |
| 6 | `(24,0)` | `(12,0)` | `(0,0)` |
| 7 | `(28,0)` | `(8,0)` | `(0,0)` |
| 8 | `(32,0)` | `(4,0)` | `(0,0)` |
| 9 | `(0,0)` | `(0,0)` | `(0,0)` |

Thus (f^9=1), while (f^k\neq1) for every (1\leq k<9).  Equivalently, each of the first two rotation factors has order
(36/\gcd(36,4)=9).  Consequently

\[
\boxed{\operatorname{ord}([0,f])=9}.
\]

## 5. Destructive orientation controls

Two deliberately incorrect implementations were run against the frozen word:

1. **Wrong semidirect side.** Replacing the correct sign
   (a+(-1)^e b) by (a+(-1)^d b), while retaining the same stored coordinates, produced

   ```text
   G36 = ((14,0),(32,0),(22,0))
   ```

   rather than (f).

2. **Wrong reflection inverse.** Replacing the correct
   ((a,1)^{-1}=(a,1)) by ((-a,1)) produced

   ```text
   G36 = ((6,0),(32,0),(34,0))
   ```

   rather than (f).

Both are genuinely destructive controls for the dihedral coordinate convention used in the positive replay.

For completeness, two tempting controls were **blind on this particular row**: reversing accumulator order and replacing (f^{-1}yf) by (fyf^{-1}) each happened to return the same final (f).  They were therefore recorded as insensitive and were not counted as orientation evidence.

## 6. Machine receipt

The successful inline run printed

```text
TRANSCRIPT_CANONICAL_JSON_SHA256=fe784c78a992d7a08734809b47d372d17119898e588e89e0b2ca374f48007514
FINAL_MARKER=LUNA_R07_ORDER9_INDEPENDENT_REPLAY_PASS
```

The assertions in that run pinned both input hashes, the frozen word hash, the two positive equalities
(W(x,y)=f) and (W(x,f^{-1}yf)=f), all eight strict nonidentity tests (f^k\neq1) for (1\leq k\leq8), the identity (f^9=1), and rejection by both destructive controls.

This terminal concerns only the fixed R07 order computation.  It makes no arithmeticity, witness, or broader ladder claim.
