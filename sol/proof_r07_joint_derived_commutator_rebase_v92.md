# Joint-derived criterion for the admissible commutator rebase v92

Author: Sol / 2026-08-26

Status: paper proof.  The finite joint image for the frozen 616-letter branch
has not yet been constructed, so the application remains pending.
`verified=false`; no cofinal lift or Ihara witness is declared.

## 1. The complete exponent lattice without enumerating the kernel

Let \(F=F(x,y)\), let

\[
\Psi:F\longrightarrow B_1\times\cdots\times B_s
\tag{1.1}
\]

be the joint map formed from every settled literal evaluation which must be
preserved, and put

\[
N=\ker\Psi,\qquad G=\operatorname{im}\Psi.
\tag{1.2}
\]

Thus \(F/N\simeq G\).  Write

\[
\operatorname{exp}:F\longrightarrow F^{\rm ab}\simeq\mathbf Z^2
\tag{1.3}
\]

for the signed exponent map and \(L=\operatorname{exp}(N)\).

### Theorem 1.1 (JOINT-ABELIANIZATION-LATTICE)

The complete admissible exponent lattice is

\[
\boxed{
L=\ker\!\left(\mathbf Z^2=F^{\rm ab}
       \longrightarrow G^{\rm ab}\right).}
\tag{1.4}
\]

In particular, for every \(f\in F\),

\[
\boxed{
\operatorname{exp}(f)\in L
\quad\Longleftrightarrow\quad
\Psi(f)\in [G,G].}
\tag{1.5}
\]

#### Proof

Abelianizing the quotient map \(F\twoheadrightarrow F/N\simeq G\) gives a
surjection

\[
F/[F,F]\twoheadrightarrow G/[G,G].
\]

Its kernel is

\[
N[F,F]/[F,F],
\]

which is exactly the image of \(N\) under (1.3).  This proves (1.4).
Applying (1.4) to the exponent vector of \(f\) gives (1.5). \(\square\)

This replaces the incomplete procedure “find many words in \(N\), then hope
their exponent vectors generate \(L\)” by one exact finite abelianization
calculation.

## 2. Explicit commutator representative

### Theorem 2.1 (JOINT-DERIVED-COMMUTATOR-REBASE)

Let \(f\in F\), put \(g=\Psi(f)\), and suppose \(g\in[G,G]\).  Then there is
an explicit \(q\in[F,F]\) such that

\[
\Psi(q)=\Psi(f).
\tag{2.1}
\]

Consequently, with

\[
r=q^{-1}f,
\tag{2.2}
\]

one has

\[
r\in N,\qquad \operatorname{exp}(r)=\operatorname{exp}(f),
\qquad f r^{-1}=q\in[F,F].
\tag{2.3}
\]

Thus \(q\) is a raw free-commutator word having exactly the same value as
\(f\) under every settled map in (1.1).

#### Proof

Because \(F\twoheadrightarrow G\) is surjective,

\[
\Psi([F,F])=[G,G].
\]

The assumption therefore supplies \(q\in[F,F]\) with (2.1).  Equation
(2.2) gives \(\Psi(r)=g^{-1}g=1\), so \(r\in N\); since \(q\) has zero
exponent vector, \(\operatorname{exp}(r)=\operatorname{exp}(f)\).  Finally
\(f r^{-1}=f f^{-1}q=q\). \(\square\)

### Constructive form

For a finite joint image \(G=\langle a,b\rangle\), where
\(a=\Psi(x)\) and \(b=\Psi(y)\), the theorem has a finite certificate:

1. construct \(D=[G,G]\) and test \(g=\Psi(f)\in D\);
2. express \(g\) as a word in commutators of words in \(a,b\);
3. replace \(a,b\) by \(x,y\) in that expression to obtain
   \(q\in[F,F]\);
4. directly replay \(\Psi(q)=\Psi(f)\), and independently check
   \(\operatorname{exp}(q)=(0,0)\).

The membership test alone is a complete yes/no decision for the frozen joint
map.  A negative answer rejects only this admissible rebase at this prefix;
it is not an obstruction to every possible R07 lift.

### Corollary 2.2 (GENERATOR-ORDER SHORTCUT)

Let \(e=(u,v)=\operatorname{exp}(f)\), and write
\(a=\Psi(x), b=\Psi(y)\).  If

\[
a^u=1,\qquad b^v=1,
\tag{2.4}
\]

then the displayed word

\[
r=x^u y^v
\tag{2.5}
\]

already belongs to \(N\).  Hence

\[
\boxed{q=f r^{-1}\in[F,F],qquad \Psi(q)=\Psi(f).}
\tag{2.6}
\]

This shortcut is stronger than coordinatewise derived-subgroup membership:
it proves that one literal word is identity in the joint image itself, so
no subdirect-product correlation remains.  It is enough to pin the orders
of \(a\) and \(b\) in the joint image, equivalently the least common
multiples of their orders in every registered coordinate.

## 3. The frozen 616-letter branch

For

\[
f=w_{23}=w_2(w_3^{-1}w_2)^8,\qquad
\operatorname{exp}(f)=(108,-36),
\tag{3.1}
\]

take (1.1) to contain the constituent homomorphisms needed to preserve the
settled G36 and PSL mark, p2/p3 source and five cofaces, complete E3 value,
all five complete E4 coface values, and the frozen finite side gates.  It is
important to form their **joint image** \(G\), rather than checking the
derived subgroup in each coordinate separately: a subdirect product can
carry abelian diagonal correlations invisible in individual factors.

The exact next certificate is therefore

\[
\Psi(w_{23})\in[G,G]
\tag{3.2}
\]

together with the lifted commutator word \(q\).  If (3.2) passes, \(q\)
supersedes the tentative power word \(w_{23}y^{36}x^{-108}\) from v90--v91:
it is guaranteed to preserve every registered value and to be charming in
the raw free group, without enumerating \(N\) or guessing a generating set
for its exponent lattice.

Before constructing \(G'\), one should test Corollary 2.2.  In the present
notation it asks only for

\[
\Psi(x)^{108}=1,qquad \Psi(y)^{36}=1.
\tag{3.3}
\]

If these identities hold, then the tentative word is no longer tentative:

\[
\boxed{q=w_{23}y^{36}x^{-108}}
\tag{3.4}
\]

is the required explicit commutator rebase.  If either identity fails, the
complete joint-derived test (3.2), rather than a coordinatewise substitute,
is the fallback.

The two-hexagon and ordered A.18 identities are preserved provided (1.1)
contains every constituent substitution used in those products.  Later
normalized Brunnian corrections remain restricted to \([F,F]\), so every
subsequent partial product stays in \([F,F]\).

```text
GENERAL JOINT-ABELIANIZATION CRITERION:       PAPER_PROOF
GENERAL EXPLICIT COMMUTATOR REBASE:           PAPER_PROOF
COMPLETE-KERNEL ENUMERATION REQUIRED:         NO
616 JOINT IMAGE / DERIVED MEMBERSHIP:         PENDING FINITE CERTIFICATE
616 EXPLICIT q IN [F,F]:                      NOT YET MATERIALIZED
616 NEXT-CHIEF ACTUAL BETA:                   OPEN
COFINAL COMPATIBLE LIFT:                      NOT YET CONSTRUCTED
IHARA WITNESS:                                NOT DECLARED
```
