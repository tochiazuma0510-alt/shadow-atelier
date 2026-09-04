# R07 actual scalar blockwise Fubini lemma v540

## 1. Purpose and fixed notation

This note proves that the actual grade-two scalar test of v533--v536 can be
evaluated from the Task554 parents one block at a time.  It is a memory
normal form only.  It changes neither the relation family, its order, nor the
sign convention.

Let `P_0,...,P_8058` be the canonical P1 rows in the fixed global order

```text
old character blocks:  ranks 505,503,503,503
new character blocks:  ranks 1509,1512,1512,1512.
```

Write their offsets as `o_a` and `n_b`.  For one raw covector `q` and the
four actor adjoints `q_t=T_t^*q`, put

```text
v_i     = <q,P_i>,
v_i^t   = <q_t,P_i>,             t in [1,-1,2,-2].             (1.1)
```

These five 8,059-entry vectors are the only data needed from the 292 MB P1
cache after its single pass.

For an expression `e=[[i_1,c_1],...]` in a local rank-r basis define

```text
Eval(e,u) = sum_j c_j u[i_j]  in F3.                            (1.2)
```

Task554's canonical normal-form condition makes the indices strictly
increasing and the coefficients lie in `{1,2}`.

## 2. The fixed relations

For seed `s=0,...,43`, let `e^old_(a,s)` be the prepare record's
`old_blocks[a].record.seed_reductions[s]`.  Let `O(a,s)` be the corresponding
global defect-origin id and let `e^new_(b,O)` be block b's
`origin_reductions[O]`.  The scalar tested by v533 is exactly

```text
R_seed(s) = direct_seed(s)
            - sum_a Eval(e^old_(a,s), v on old block a)
            - sum_(a,b) Eval(e^new_(b,O(a,s)), v on new block b).   (2.1)
```

For an old pivot `(a,p)` and actor slot t, let `e^old_(a,p,t)` be the
prepare `actor_transitions[p][t]`, and let `O(a,p,t)` be its global origin
id.  The tested scalar is

```text
R_old(a,p,t) = v^(t)_(o_a+p)
               - Eval(e^old_(a,p,t), v on old block a)
               - sum_b Eval(e^new_(b,O(a,p,t)), v on new block b). (2.2)
```

For a new pivot `(b,p)` and actor slot t, with transition
`e^newact_(b,p,t)`, it is

```text
R_new(b,p,t) = v^(t)_(n_b+p)
               - Eval(e^newact_(b,p,t), v on new block b).          (2.3)
```

The public v15 `_global_relations` followed by `_pair` is precisely
(2.1)--(2.3): first 44 seeds, then the four actors for every old row in
character order, then the four actors for every new row in character order.
There are

```text
44 + 4*(2014+6045) = 32280                                      (2.4)
```

scalars.

## 3. Blockwise algorithm

Allocate one 32,280-trit result array in the final order.

1. From the prepare body, initialize the 44 seed entries with
   `direct_seed` minus all old seed evaluations.
2. From the same prepare body, initialize all 8,056 old-actor entries with
   `v^t_(o_a+p)` minus the old transition evaluation.
3. For `b=0,1,2,3` in order, parse and authenticate only block b.
   For every one of the 8,100 defect origins, subtract the evaluation of
   `origin_reductions[O]` from the unique seed or old-actor accumulator named
   by the prepare `defect_origins[O]` record.
4. While block b is resident, fill its 4*rank(b) new-actor positions using
   (2.3).  Then release the parsed block before opening block b+1.
5. Scan the final array in the order (2.4).  The first nonzero entry is the
   v534 Violation; all zero entries give ScalarEOF.

The prepare origin roster is a bijection onto the 44 seed plus 8,056
old-actor slots: each old block contributes `44+4*r_a`, and

```text
sum_a (44+4*r_a) = 4*44 + 4*2014 = 8232,                       (3.1)
```

while Task554's actual prepare has 8,232 defect origins.  (The full 8,100
number sometimes attached to this lane is not the Task554 defect-origin
count; production readers must use and check 8,232.)  Every target block has
one `origin_reductions` expression for each of these 8,232 origins.

Thus step 3 visits each pair `(b,O)` exactly once, exactly as the inner
target-block loop of `_global_relations`.  Finite commutativity and
associativity in F3 allow those four summands to be accumulated in block
order.  No term is omitted or duplicated.  Equations (2.1)--(2.3) prove that
the resulting scalar array is identical entry-by-entry to materializing the
complete nested relation object and then calling `_pair`.

## 4. Receipt and memory boundary

The semantic identity of the relation family is fixed by:

- the exact prepare body/head hashes;
- the four exact block body/head hashes and parent joins;
- ranks, origin roster and actor order;
- the exact evaluator executable hash;
- the final 32,280-entry scalar rolling hash.

A downstream receipt need not hash a second giant serialization of relation
lists already authenticated inside those fixed parent bodies.  It must bind
all five parent identities, the value-vector hashes, the order constants and
the scalar rolling hash.  Reordering, removing or resealing a parent changes
that identity before any upper claim.

At no point is a dense defect matrix present.  Apart from the five value
vectors and the tiny accumulator, the resident Task554 data are bounded by

```text
one authenticated prepare body + one authenticated block body.             (4.1)
```

This replaces simultaneous retention of four large blocks plus a duplicated
global-relation tree.  The P1 cache and instruction stream remain file-backed.

## 5. Claim boundary

This lemma proves an exact evaluation and resource equivalence.  It does not
state that any actual scalar is zero or nonzero.  Those values belong to the
Task908 run and independent checker.

```text
BLOCKWISE_SCALAR_EQUIVALENCE=PROVED
RELATION_COUNT=32280
TASK554_DEFECT_ORIGINS=8232
DENSE_DEFECT_MATRIX=false
SCALAR_RESULT=NOT_RUN
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
