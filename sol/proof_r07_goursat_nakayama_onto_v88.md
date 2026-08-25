# Goursat--Nakayama onto certificate for the R07 branch v88

Author: Sol / 2026-08-26

Status: paper proof.  Its application requires three finite generator/relator
receipts for the literal 616-letter source tuple.  Those receipts are not yet
reported.  `verified=false`; no cofinal lift or witness is declared.

## 1. A finite direct-product criterion

### Theorem 1.1 (GOURSAT--NAKAYAMA ONTO)

Let \(p\) be a prime, let \(P\) be a finite \(p\)-group, and let \(Q\) be a
finite group with

\[
p\nmid |Q^{\rm ab}|.
\tag{1.1}
\]

Put \(E=Q\times P\).  Let \(s_1,\ldots,s_d\in E\), and put
\(H=\langle s_1,\ldots,s_d\rangle\).  If

\[
\langle\operatorname{pr}_Q(s_i):1\leq i\leq d\rangle=Q
\tag{1.2}
\]

and the images of \(\operatorname{pr}_P(s_i)\) span

\[
P/\Phi(P)
\tag{1.3}
\]

over \(\mathbf F_p\), then

\[
\boxed{H=E.}
\tag{1.4}
\]

#### Proof

By the Burnside basis theorem, (1.3) implies
\(\operatorname{pr}_P(H)=P\).  Together with (1.2), \(H\) is a subdirect
subgroup of \(Q\times P\).

Goursat's lemma supplies normal subgroups \(N_Q\lhd Q\), \(N_P\lhd P\) and
an isomorphism

\[
Q/N_Q\simeq P/N_P
\tag{1.5}
\]

which measures the only possible failure of \(H\) to be the full direct
product.  The common quotient in (1.5) is a finite \(p\)-group.  If it were
nontrivial, it would have a quotient \(C_p\); hence \(Q\) would have a quotient
\(C_p\), contradicting (1.1).  Thus the common quotient is trivial and
Goursat gives \(H=Q\times P\). \(\square\)

### Corollary 1.2 (FINITE ENDOMORPHISM AUTOMORPHISM)

Let a marked presentation of \(E\) have generators \(a_1,\ldots,a_d\).  If
literal words \(s_i=s_i(a_1,\ldots,a_d)\) kill every defining relator, they
define an endomorphism \(\alpha:E\to E\).  If (1.2)--(1.3) hold for the
\(s_i\), then \(\alpha\) is surjective and hence, because \(E\) is finite, an
automorphism.

No displayed inverse tuple is needed for the mathematical onto conclusion.
An inverse tuple is a useful independently replayable certificate, but a
bounded search inside a specially shaped family of inverse words is not part
of the definition of surjectivity.

## 2. Application to the frozen q3 B4 target

The authenticated q3 construction gives

\[
E_4=Q_4\times\Pi_4[3]
\tag{2.1}
\]

because the common quotient is trivial.  It also gives

\[
|Q_4^{\rm ab}|=32.
\tag{2.2}
\]

Thus Theorem 1.1 applies with \(p=3\).  For a literal candidate word \(f\),
let

\[
(S_1(f),\ldots,S_6(f))
\tag{2.3}
\]

be the six printed PB4 source words for \(T^{PB_4}_{0,f}\).  Its complete onto
certificate may consist of exactly:

1. all eleven PB4 relators evaluated at (2.3) are the identity in \(E_4\);
2. the six \(Q_4\)-projections generate \(Q_4\), with a reproducible subgroup
   order/generator certificate;
3. the six \(\Pi_4[3]/\Phi(\Pi_4[3])\)-projections have full \(\mathbf F_3\)
   span, with the explicit matrix, rank and basis convention;
4. the direct-product binding (2.1) and the abelianization pin (2.2).

These four items prove that the source endomorphism is an automorphism.  They
are candidate-local and must be replayed for the 616-letter word; the old
20-letter inverse cache cannot certify them.

## 3. Effect on the 616 retarget

The 27 exponent-seven candidates requested as a small diagnostic remain
useful: a passing ST/TS tuple is a compact positive certificate.  But if that
registered family is empty, the onto gate remains decidable by Section 2.
Such an empty family is not a resource stop and not evidence that the source
endomorphism is non-surjective.

Consequently the fresh 616 handoff in v86 can replace

```text
find a GT-shaped inverse in the frozen 27-word family
```

by the exact candidate-local test

```text
PB4 relators + Q4 generation + full Pi4[3]/Phi span.
```

If it passes, the next load-bearing work is the 616-specific affine Fox/A.18
data \((E_{616},\mathscr P_{616},h_{616},\beta_{616})\), not a larger inverse
word hunt.

```text
GENERAL DIRECT-PRODUCT ONTO CRITERION:       PAPER_PROOF
OLD 27-INVERSE FAMILY NECESSARY:             NO
616 PB4 RELATOR REPLAY:                       PENDING
616 Q4 GENERATION:                            PENDING
616 Pi4[3]/PHI FULL SPAN:                     PENDING
616 ONTO:                                     UNKNOWN UNTIL THESE PASS
```
