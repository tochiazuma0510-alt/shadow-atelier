# R07 physical relative-fibre selector: typed bridge to the v504 owner (v539)

Author: root Sol / 2026-09-04

Status: narrow addendum to v537, discharging the sole paper repair in the
Task873 audit.  It identifies the redundant inverse-system instruction owner
with the completed source and word-dependent physical map used in v504.  It
does not supply an actual kernel cover, A0 member, saturation certificate,
lift, fake, or Ihara witness.  `verified=false`.

## 1. Typed finite quotients

Retain all notation and hypotheses of v537.  For every registered level `n`,
let `P_n` be the finite quotient of v504's completed legal source at that
level, and let

```text
q_n : X_n -> P_n
```

impose exactly the pre-registered linear source relations which are redundant
in the universal instruction presentation `X_n`.  Let `rP_n:P_(n+1)->P_n`
be the v504 reduction.  Add the following three typed identities:

```text
q_n rX_n = rP_n q_(n+1),                              (1.1)
B_n      = B^504_(n,w0) q_n,                          (1.2)
z_n      = Phi^504_n(w0) in L_n.                      (1.3)
```

Here `B^504_(n,w0):P_n->L_n` is the finite quotient of v504's physical map
for the same fixed literal word `w0`; it is not an unrelated map called `B`.
Equation (1.3) identifies the v537 target constructed by structural evaluation
with the finite quotient of v504's target.  All three equations must be
checked on the registered instruction generators, relations, eleven
occurrences, normalized coordinates, side/boundary/localization data, and the
outer physical evaluation.

If the v504 source is retained in the redundant presentation, take
`P_n=X_n`, `q_n=id`, and (1.1)--(1.3) reduce to literal identifications.  No
inverse to `q_n` is assumed or needed.

## 2. Passage of the selected compatible point

Suppose v537 Sections 1--5 construct a compatible family

```text
x_n in X_n,
rX_n(x_(n+1))=x_n,
B_n(x_n)=z_n.                                         (2.1)
```

Define

```text
p_n := q_n(x_n) in P_n.                               (2.2)
```

Then (1.1) and (2.1) give

```text
rP_n(p_(n+1))
 = rP_n q_(n+1)(x_(n+1))
 = q_n rX_n(x_(n+1))
 = q_n(x_n)
 = p_n.                                               (2.3)
```

Thus `p=(p_n)` is an element of `P=lim P_n`, the completed source used by
v504.  Equations (1.2), (2.1), and (1.3) give at every level

```text
B^504_(n,w0)(p_n)
 = B^504_(n,w0)q_n(x_n)
 = B_n(x_n)
 = z_n
 = Phi^504_n(w0).                                     (2.4)
```

Equality in the inverse limit therefore yields

```text
B^504_(w0)(p)=Phi^504(w0),                            (2.5)
```

which is exactly the initial completed-source premise of v504 Theorem 6.1.

This argument does not use exactness of inverse limits or surjectivity of
`q:lim X_n->lim P_n`: the already constructed compatible family is mapped
componentwise.  It also does not infer a common word from values.  The point
`x` carries the one v537 literal/DAG ancestry, and each `q_n` merely takes its
registered source class.

## 3. Corrected v537-to-v504 implication

With (1.1)--(1.3), replace the informal v537 phrase
`Phi(w0) in B(X)` by the typed conclusion (2.5).  The maximum implication is

```text
complete first-rung literal A0 member in X_0
+ fixed-word target naturality
+ all-edge physical relative-kernel covers and word-bearing selectors in X_n
+ the generator-level quotient identities (1.1)--(1.3)
  => Phi^504(w0) in B^504_(w0)(P).
```

Only after this implication is combined with the separately required v504
compactness, strictness, separation, physical-jet saturation, side, Cauchy,
and continuity gates may one invoke its conditional Newton conclusion.
Grade-two membership alone is not the complete first-rung premise, and the
prepared A4 v10 successor-kernel fixture is not the physical kernel cover.

```text
X-TO-v504-P / B_(w0) TYPED BRIDGE:            PAPER-CLOSED
FIXED-WORD PHYSICAL SELECTOR THEOREM:          PAPER-CLOSED, CONDITIONAL
ACTUAL COMPLETE FIRST-RUNG A0 MEMBER:          OPEN
ACTUAL ALL-EDGE PHYSICAL KERNEL COVER:         OPEN
ACTUAL PHYSICAL-JET-SATURATION:                OPEN
COMPATIBLE R07 LIFT / FAKE / IHARA:            NOT DECLARED
verified=false
```

`R07_PHYSICAL_RELATIVE_FIBRE_SELECTOR_TYPE_BRIDGE_V539_CANDIDATE`
