# Task933 — table-free endpoint selector v547 audit

Verdict: **PASS at paper level on the stated existing finite and marked
premises. Necessary mathematical corrections: none.**

I read the complete Task933 and v547. The previously audited v459/v545/v546
inputs remain premises; no historical calculation, code execution, git or
network operation was performed. Only this reply file was written.
`verified=false`.

## F1. Exponent quotient and the new marked basis — PASS

The actual lattice `epsilon(Omega)=18 Z^2` makes
`e(Theta(n))=epsilon(n)/2 mod 9` well-defined on Gamma0. The two specific
words r_x,r_y have images `(1,0),(0,1)`, so e is onto. Its target and
Gamma0_ab both have order `243/3=81`; therefore the induced abelianization
map is an isomorphism, not merely a quotient map.

Consequently these actual a,b generate Gamma0 modulo Phi, hence generate
Gamma0. The central-derived-subgroup and central-cube argument from v545
applies to them, giving the independent basis
`a^3,b^3,[a,b]` of Phi. In particular

\[
\Theta(w)\in\Phi(\Gamma_0)
\iff w\in N_0\text{ and }\epsilon(w)\in6\mathbb Z^2
\]

when w is understood to represent an element of Gamma0. The two cube
coordinates are exactly `epsilon_x(w)/6` and `epsilon_y(w)/6` modulo 3.
Changing the representative by Omega changes these integers by multiples
of 3. V547 (2.1)–(2.4) are justified.

## F2. Heisenberg handedness and omega — PASS

The marked relation `u3^u1=u3*u4` means
`u3*u1=u1*u3*u4`. Thus the normal form `u1^A u3^B u4^C`
has the positive cross term `B*A'` in its product. Multiplication by an
`x^sigma` letter contributes `sigma*B(prefix)`; multiplication by a y
letter contributes no central term. This proves the literal coefficient
formula and its compatibility with the actual first-E3 H projection.

The product/inverse rules (3.2) follow directly. The power rule (3.3) holds
for every integer m, including negative integers, with the integer
polynomial `binom(m,2)=m(m-1)/2`. These rules genuinely allow scalar SLP
evaluation without expanding the word.

For the convention `[u,v]=u^-1 v^-1 u v`, the commutator coefficient is
`B(u)A(v)-B(v)A(u)`. Therefore

\[
\omega([x,y])=-1=2,\qquad
\omega([r_x,r_y])=-2\cdot2=-4=2\pmod3.
\]

Since H has exponent 3, the H images of a^3 and b^3 vanish. The nonzero
commutator image makes this projection faithful on Gamma0', of order 3.
For `h=(a^3)^alpha(b^3)^beta[a,b]^gamma`, it follows that
`omega(w)=2 gamma`, hence `gamma=2 omega(w)`. Negation gives the inverse
endpoint's commutator exponent `-2 omega(w)=omega(w)`.

Thus the **plus sign** in the last factor of (4.2) is correct. First E3
still does not distinguish all of Phi: its kernel there is the cube plane,
of order 9. The two exponent readouts distinguish exactly that missing
plane. The earlier first-E3 warning is respected, not bypassed.

## F3. Simultaneous endpoint repair and exact normalization — PASS

Put `A=epsilon_x(w)`, `B=epsilon_y(w)` under (4.1), and let g represent
omega(w). The endpoint of the appended cube factors has coordinates
`(-A/6,-B/6,0)` modulo 3. By F1 these cancel the two cube coordinates of h.
What remains has commutator coordinate

\[
2\omega(w)+g=3\omega(w)=0\pmod3.
\]

Equivalently its H central coefficient is `omega(w)+2g=0`, and
faithfulness on Gamma0' forces the actual Delta endpoint to be identity.
This is an actual-kernel conclusion, not just vanishing of three unrelated
quotient measurements.

Using the **exact integer** cube powers gives ordinary exponent vector

\[
(A,B)-6(A/6,0)-6(0,B/6)=(0,0).
\]

The commutator has zero integer exponent. Hence the output lies in
`Omega intersect [F,F]`. All appended factors lie in Phi(N0), so their
mod-three Fox rows vanish at Q0 and every quotient of Q0. Fox additivity
proves (4.3) for the same literal w and output word. No separate c_x,c_y
normalization is needed; changing a cube exponent by a multiple of 3 is
exactly the old ninth-power adjustment.

## F4. Legal-cycle application and boundary — PASS

For a tau2-legal Q2 cycle, v542 supplies its fixed-order Schreier word.
The three zero carries put that word in N0, while its zero exponent rows
modulo 3 and its N0 parity give exact divisibility by 6. Thus (4.1) holds
and (5.1) follows. The alternative same-Phi argument reaches the same
conclusion.

The genuine advance over v545 is removal of the remaining 27-product
endpoint encoding: exact exponent sums and omega determine the repair
directly from the word/SLP, while exact normalization is included in those
same three factors. This does not bound expanded word length or make R a
homomorphism. Simultaneous Fox preservation on quotients of fixed Q0 does
not produce a compatible cofinal family beyond Q0.

The physical target equation, PB4 preservation, remaining H floors and
full A0 remain separate, exactly as the paper states. The running seed30
GHA `33946247365` does not acquire any prerequisite from this audit.

```text
TABLE-FREE EXPONENT+OMEGA READOUT:    PAPER AUDIT PASS
COMMUTATOR REPAIR SIGN +OMEGA:       CORRECT
EXACT INTEGER NORMALIZATION:        INCLUDED AND CORRECT
Q0 AND QUOTIENT FOX PRESERVATION:    PAPER AUDIT PASS
NECESSARY MATHEMATICAL CORRECTIONS:  NONE
PHYSICAL TARGET / A0 / COFINAL:      NOT SUPPLIED
SEED30 RELEASE DEPENDENCY:           NONE
verified=false
```
