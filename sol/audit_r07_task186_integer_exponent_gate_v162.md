# R07 task186 integer-exponent gate v162

Author: Sol / 2026-08-27

Status: mathematical/static implementation audit.  This note records a fatal
defect found in the third task186 delivery and adds a no-repeat promotion
gate.  No GHA task186 run has been dispatched.  No common word, compatible
cofinal lift, fake, or Ihara witness is declared.

## 1. The two exponent maps are different

For a signed word (w\in F(x,y)), write

\[
 \epsilon_{\bf Z}(w)=
 \left(\#x-\#x^{-1},\#y-\#y^{-1}\right)\in{\bf Z}^2.
 \tag{1.1}
\]

The old task179 function

```text
search/d972_r07_positive_common_word_colgen_v1.py:318--320
```

does **not** return (1.1).  It returns

\[
 \epsilon_3(w)=\epsilon_{\bf Z}(w)\pmod3.
 \tag{1.2}
\]

V156 proves that every registered correction word (w\in\Omega) has

\[
 \epsilon_{\bf Z}(w)\in18{\bf Z}^2.
 \tag{1.3}
\]

Consequently task179's old value is identically zero on the full 6,441-word
roster.  The required normalized map is instead

\[
 \boxed{
 \nu(w)=\frac{\epsilon_{\bf Z}(w)}{18}\pmod3.}
 \tag{1.4}
\]

There is no function (f:{\bf F}_3^2\to{\bf F}_3^2) recovering (1.4) from
(1.2): the division must occur over the integers before reduction modulo
three.

## 2. Fatal defect in the third delivery

The third producer had identity

```text
bytes   29711
sha256  59858dc526345dbfc2883386967fdd9709413ace48787ec0ac27d222e8d1bee3
```

and used, at its then-current lines 488--494,

```text
raw_exponent = v1.exponent_pair
pair = raw_exponent(word)
require(pair[0] % 18 == 0 and pair[1] % 18 == 0, ...)
return ((pair[0] // 18) % 3, (pair[1] // 18) % 3)
```

But `pair` in this code is the already reduced value (1.2).  On every roster
word it equals `(0,0)`, passes the displayed divisibility check vacuously,
and returns `(0,0)`.  Therefore the actual E1/E2 rows, echelon, duals, oracle
scalars, target reduction, and recovered solution all remain the withdrawn
raw-vacuous computation.  Post-processing a side list with fresh integer
exponents cannot repair the search that already ran.

The third delivery is rejected before execution.

## 3. Correct load-bearing replacement

Before constructing the task179 runtime or `PositiveSearch`, the successor
must replace the module-global `exponent_pair` with a function that:

1. iterates over the literal signed letters;
2. computes both coordinates of (1.1) as Python integers;
3. rejects any letter outside `+-1,+-2`;
4. checks both coordinates are divisible by 18;
5. divides both integer coordinates by 18; and only then
6. reduces the two quotients modulo three.

Because Python function globals are resolved at call time, a correctly timed
replacement reaches the task179 call sites

```text
AllSevenModel.occurrence_data
AllSevenModel.occurrence_column
AllSevenModel.direct_column
PositiveSearch.positive_receipt
weighted dual/formula scalar construction
```

provided it occurs before any production model/search construction.  The
checker must implement the integer count independently and patch the
authenticated helper-nonshared task179 checker before its replay.  Patching
only the producer or only a receipt-side audit is insufficient.

## 4. Literal row-equality canary

Let `E1=b"E"+bytes([1])` and `E2=b"E"+bytes([2])` be the actual task179
sparse keys.  For every retained correction column with literal conjugate
word (w_j), the producer and independent checker must require

\[
 \texttt{row}_j|_{\{E1,E2\}}=\nu(w_j),
 \tag{4.1}
\]

and every boundary column must have zero restriction.  They must then rebuild
the combined rows from rank zero and require their pivot/rank transcript to
equal the production transcript.  Synthetic keys such as `V2-NU-0` used only
after the search do not establish (4.1).

The registered words provide non-vacuous static canaries:

\[
\begin{aligned}
 \epsilon_{\bf Z}(r_3)&=(0,36),\\
 \epsilon_{\bf Z}(r_9)&=(18,144),\\
 \epsilon_{\bf Z}(r_{12})&=(-18,-54),\\
 \nu(r_3)&=(0,2),\\
 \nu(r_9)&=(1,2),\\
 \nu(r_{12})&=(2,0).
\end{aligned}
\tag{4.2}
\]

At least one production-like SELFTEST path must call the actual patched
occurrence/direct-column machinery on a word of integer exponent `(18,0)`
and observe the literal `E1` coefficient one.  Calling the old function and
then dividing its output must fail this canary.

## 5. Other third-delivery blockers retained from V160

Even after correcting (1.4), promotion still requires all V160 gates:

1. actual stripped and augmented ranks, with
   `rank_aug == production pivot count == retained independent column count`;
2. independent coefficient ancestry for a basis of (N(\ker A));
3. correction sources built from literal `conjugate_word`, never the
   unconjugated relator when the retained column was translated;
4. a complete replay of each source correction plus its separately typed
   boundary chain to zero;
5. sealed v2 checkpoints whose columns are replayed from rank zero under
   (1.4), with no stale raw pivot/dual/oracle state;
6. direct comparison of the `c_star` and `c_exact` all-seven rows, not a
   copied boolean; and
7. a helper-nonshared checker and production-like destructive SELFTEST.

The third delivery also changed checkpoint schema/tag fields without
resealing, leaving stale `self_digest`, and its checker rebuilt synthetic
normalized rows without comparing the actual serialized E1/E2 entries.
Those defects remain hard stops.

```text
TASK179 exponent_pair:                         ALREADY MOD 3
DIVIDE task179 exponent_pair BY 18:            INVALID / VACUOUS
INTEGER COUNT THEN DIVIDE 18 THEN MOD 3:       REQUIRED
THIRD TASK186 DELIVERY:                        REJECTED
TASK186 GHA SELFTEST / PRODUCTION:             NOT DISPATCHED
EXACT FIRST-EDGE COMMON WORD:                  NOT YET CONSTRUCTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:        NOT DECLARED
```

`R07_TASK186_INTEGER_EXPONENT_GATE_V162`
