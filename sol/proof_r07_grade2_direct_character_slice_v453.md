# R07 A0: direct character-slice form of the grade-two projectors (v453)

Author: Sol / 2026-09-03

## 1. Setup and distinction

Use the four exact pure-\(Q_1\) words and the associated-grade operators
\(T_a\), \(a\in A=C_2^2\), of v447.  The source coordinate order in the
grade-one and grade-two engines is already the Fourier character order

\[
 \widehat A=((0,0),(0,1),(1,0),(1,1)).              \tag{1.1}
\]

For a pure homogeneous row write

\[
       \beta=(\beta_\mu)_{\mu\in\widehat A}.        \tag{1.2}
\]

This note concerns only the genuine associated-grade idempotents
\(e_\lambda\).  It makes no idempotence claim about the full filtered word
sums \(P_\chi\) used to reconstruct precision-one seeds in v451.

## 2. Diagonal-action lemma

V447 (2.1) gives the endpoint of the word \(w_a\) as \((1_P,a)\).  Its
possible upstairs kernel coordinate raises augmentation degree and therefore
vanishes on the associated grade.  By the definition of the already Fourier
transformed source coordinate,

\[
        (T_a\beta)_\mu=\mu(a)\beta_\mu.             \tag{2.1}
\]

This is one correlated action on all six occurrence tags, both Fox
components and all six degree-two monomials; (2.1) does not authorize any
tagwise or monomial-wise closure.

## 3. Direct-slice theorem

The legal projector is

\[
 e_\lambda=\sum_{a\in A}\lambda(a)T_a,             \tag{3.1}
\]

where the usual factor \(1/4\) is one in \(\mathbf F_3\).  Combining (2.1)
with character orthogonality gives

\[
 (e_\lambda\beta)_\mu
 =\left(\sum_{a\in A}\lambda(a)\mu(a)\right)\beta_\mu
 =\delta_{\lambda\mu}\beta_\mu.                   \tag{3.2}
\]

### Theorem 3.1

After the v447 endpoint/diagonal-action gate has been replayed once for a
run, the four Task565 degree-two packet rows associated to a defect \(\beta\)
are exactly

```text
packet[lambda] = beta[lambda]
```

in the registered character order.  No per-defect source-word action and no
per-defect Walsh transform is required.  The four packets together still
reconstruct \(\beta\), and every packet is a single width-36,288 row retaining
all six monomials coupled.

#### Proof

Equation (3.2) says precisely that \(e_\lambda\) zeros the other three
character slices and leaves slice \(\lambda\) unchanged.  The block closure
stores only that nonzero slice.  Summing the four installed slices restores
(1.2). \(\square\)

## 4. Fail-closed implementation gate

Direct slicing is legal only after producer and independent checker each
establish, from pinned data rather than a declared label, all of:

1. the four word endpoints are \((1_P,a)\) in the registered order;
2. the source array index has the character meaning (1.1);
3. the associated action of each word agrees with the four diagonal signs in
   (2.1), on a full six-monomial correlated canary for every character; and
4. the four direct slices agree with the four explicit word-sum projectors on
   those canaries.

The checker must still reconstruct and compare every actual defect slice.
The bounded word-sum canaries certify the once-per-run change of coordinates;
they do not replace complete packet checking.

## 5. Consequence

V452 Theorem 3.1 already reduced sixteen word actions per defect to four.
Theorem 3.1 above uses the stronger fact that Task565's stored coordinates are
already Fourier coordinates and reduces those four actions to zero after one
constant-size gate.  This removes the independently measured approximately
2.98-hour projector loop without changing a row, a packet, an orbit, or the
closure universe.

```text
DIRECT CHARACTER SLICES: paper theorem
TASK565 INTEGRATION / PRODUCTION: not yet accepted
GRADE MEMBERSHIP / A0 / COMMON / COFINAL LIFT / FAKE / IHARA: not declared
verified=false
```

`R07_GRADE2_DIRECT_CHARACTER_SLICE_V453_PAPER`

