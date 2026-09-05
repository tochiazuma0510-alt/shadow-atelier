# Task925 independent Sol(max) audit of v543

## Verdict

**PASS for the stated prospective linear-algebra equivalence.**  The chain

```text
Conn -> mu -> F_lambda on the complete source
     -> tree potential + five tau coefficients + two nu tests
     -> a <=6-fundamental-cycle violation
     -> subtraction of the full P1 truncation
```

is correct under the finite-map and parent-binding premises stated below.
It is not an actual oracle receipt, a production-route replacement, or an
A0 result.  `verified=false`.

## 1. Conn gives the lower multiplier

Let `E=F3^8059`, let `B:E -> W2` send the standard basis to the canonical
lifts `btilde_i`, and put

```text
q = ell B,       h = G B.
```

Because the `pi(btilde_i)` are a basis of `W1`, `pi B:E -> W1` is an
isomorphism.  The asserted completeness of Conn is precisely

```text
span(Conn) = h(ker q).
```

Thus `lambda(Conn)=0` says that the scalar functional `lambda h` kills
`ker q`.  It consequently descends through `q` to a functional on
`image(q)=ell(W2)`, and any linear extension to `L` is the required `mu`.
This proves (2.2), including independence from the chosen expression in
the `ell_i`.  Since every value of `ell` on `W2` lies in `image(q)`, the
extension of `mu` outside that subspace never enters the test.  No additional
lower closure is needed.

This step is conditional on Conn containing the images of **all** lower
relations for these exact 8,059 canonical lifts, not merely a sampled or
rank-incomplete relation list.  That is the v530 parent premise used by
v543, rather than a new conclusion of v543.

## 2. The complete-separator equivalence

Define on `W2`

```text
H(u) = lambda G(u) - mu ell(u).
```

Equation (2.2) gives `H(Ba)=0` for every `a in E`.  Also every `u in W2`
has a unique P1 coefficient vector `a` with
`pi(u)=pi(Ba)`, so

```text
u = Ba + v,       v in ker pi <= ker ell.
```

It follows that `H(u)=lambda G(v)`.  Therefore `H` vanishes on all of
`W2` exactly when `lambda` kills `G(ker pi)`.  Together with
`lambda(Conn)=0` and

```text
G(ker ell) = span(Conn) + G(ker pi),
```

this is exactly

```text
lambda(M2)=0  iff  H(W2)=0.
```

Finally `F_lambda=H Psi`, and the assumed surjectivity of `Psi:D -> W2`
turns `H(W2)=0` into `F_lambda(D)=0`.  Thus Theorem 2.1 is sound.  The
subtraction by `mu ell` is indispensable; omitting it would indeed test all
legal source values rather than the lower-zero fibre.

## 3. Tree potential, five coefficients, and the two auxiliary directions

Using the assumed same-owner raw-chain extension, write

```text
F_lambda(z,eta)=f(z)+b(eta).
```

Since `D=ker(tau) x F3^2`, vanishing on `D` is equivalent to the two
independent conditions

```text
b=0,       f|ker(tau)=0.
```

The first condition is exactly the two evaluations on `e_x,e_y`; the eight
stored P1 auxiliary coordinates do not create eight source variables.

For the second condition, the non-tree fundamental cycles `z_e` form a
basis of `Z`.  With the stated `head-tail` boundary convention, tree
integration gives

```text
f(z_e)=f(e)-p(head(e))+p(tail(e))=r_e.
```

Because `tau:Z -> F3^5` is onto, the columns `t_e=tau(z_e)` span `F3^5`,
so five independent ones exist.  They determine a unique
`a in (F3^5)*`.  A functional on `Z` kills `ker tau` if and only if it
factors through `tau`; checking `r_e=a(t_e)` on the complete fundamental
cycle basis is exactly that factorization test.  Equivalently,

```text
f = partial* p + a tilde_tau,       b=0,
```

with the signs in (3.2)--(3.6) consistent.  Theorem 3.1 is correct.

This requires the raw cochain `f`, the tree edge convention, and `tau`
columns to use the same Fox handedness and coordinate order.  V543 states
this requirement; no convention-free mixing is licensed.

## 4. Sparse violation and full P1 subtraction

If one non-tree edge fails, its endpoint column has the unique expansion

```text
t_e = sum_i d_i t_(e_i).
```

Then the cycle in (4.1) lies in `ker tau`, uses at most the failed cycle
plus the five selected cycles, and has

```text
F_lambda(z,0)=r_e-a(t_e) != 0.
```

If an auxiliary evaluation fails, `(0,e_x)` or `(0,e_y)` is already a
legal augmented-source witness.  Thus the “at most six” claim concerns
fundamental-cycle terms only, as stated, and is exact.

For either witness put `u=Psi(z,eta)` and choose the full P1 coefficient
vector `a` with `pi(u)=pi(Ba)`.  Then `v=u-Ba` lies in `ker pi`.  Moreover

```text
mu ell(u) = mu ell(Ba) = lambda G(Ba),
```

so

```text
lambda G(v)=lambda G(u)-lambda G(Ba)=F_lambda(z,eta) != 0.
```

This proves the full-P1 subtraction claim.  It is not enough to subtract
only the physical lower coordinates; the use of the complete `pi(u)` is
essential and is correctly present in v543.  Given the v542 materializer
and word-bearing canonical P1 lifts, products/inverses realize the same
linear subtraction in `Omega`.  No expression of the selected chord in the
44-seed actor closure is required.

## 5. Premises and one narrow missing display condition

The equivalence is conditional on the following unexported or inherited
data, all substantially acknowledged in v543:

1. `Psi` is a **well-defined linear same-owner factorization through the
   pair `(J_Q2,nu)`**, is onto the complete `W2`, and uses full filtered—not
   prematurely homogeneous—evaluation.
2. `pi` is onto; the named `btilde_i` are the exact word-bearing lifts whose
   P1 images form the accepted 8,059-row basis; and the Conn artifact is
   parent-bound to those same lifts and their same `ell_i,g_i` evaluations.
3. The normalized two-plane is retained faithfully in the complete
   auxiliary block.  The actual `mu`, raw adjoint `(f,b)`, marked tree and
   all `t_e` columns still need independent receipts.
4. Literal subtraction requires the canonical P1 lifts to carry replayable
   `Omega` word/DAG ancestry, not just value rows.

There is one narrow missing hypothesis only if “rank-raising for the
**current** separator” means rank-raising beyond Conn against an already
enlarged current echelon `S_current`: add explicitly

```text
lambda(S_current)=0,       Conn <= S_current.
```

The displayed assumptions (2.1) alone prove that the violating row is
outside `span(Conn)`; annihilation of the full current span is what proves
it is outside that larger span.  A separator produced from that current
echelon has this property automatically, but its parent binding should be
stated.  This does not affect Theorems 2.1 or 3.1.

No other mathematical premise is missing from the claimed equivalence.
In particular, it neither predicts whether a comparison fails nor supplies
the actual adapters, measurements, MEMBER, PB4 block, later grades, or
cofinal lift.
