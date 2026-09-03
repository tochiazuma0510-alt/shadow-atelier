# R07: eleven endpoint gates and the six-row precision-two restriction (v477)

Author: Sol / 2026-09-03

Status: repaired successor to v476.  It incorporates the sole finite repair
R1 of Sol(max) Task633 and retains the executable elaboration of Task630.  It
constructs no payload or residual and proves no grade decision, A0, COMMON,
cofinal lift, fake, or Ihara conclusion.  `verified=false`.

## 1. Exact occurrence ledger and typed restriction

Let (J_{11}) be the following ordered heterogeneous ledger.  The order,
sign and quotient type are part of the data.

| ordinal | label | quotient | sign | endpoint-coordinate |
|---:|---|---|---:|---:|
| 1 | `H1_fxy` | (E_3) | (+) | 0 |
| 2 | `H1_fxz` | (E_3) | (-) | 1 |
| 3 | `H1_fyz` | (E_3) | (+) | 2 |
| 4 | `H2_fux` | (E_3) | (-) | 3 |
| 5 | `H2_fxy` | (E_3) | (-) | 0 |
| 6 | `H2_fuy` | (E_3) | (+) | 4 |
| 7 | `P_b1` | (E_4) | (+) | 5 |
| 8 | `P_b2` | (E_4) | (+) | 6 |
| 9 | `P_b3` | (E_4) | (+) | 7 |
| 10 | `P_b5_inverse` | (E_4) | (-) | 8 |
| 11 | `P_b4_inverse` | (E_4) | (-) | 9 |

Thus the coordinate materialization is

```text
(0,1,2,3,0,4,5,6,7,8,9).
```

The repeated coordinate zero gives two distinct typed slots.  The pentagon
factor order is `b1,b2,b3,b5^-1,b4^-1`; neither coordinate deduplication nor
sorting by printed label is permitted.  Put

\[
 H_6=(1,2,3,4,5,6),\qquad P_5=(7,8,9,10,11).
\]

The operation used below is only the coordinate restriction

\[
 \pi_H:E_3^6\times E_4^5\longrightarrow E_3^6,
 \qquad(g_1,\ldots,g_{11})\longmapsto(g_1,\ldots,g_6).       \tag{1.1}
\]

It is not an action map from five pentagon rows to six hexagon rows.

## 2. Full ambient, truncation, and degree-two module

Fix (k=\mathbf F_3), (Q_1=P\times A), and

\[
 1\longrightarrow V\longrightarrow Q_2\longrightarrow Q_1
 \longrightarrow1,
 \qquad |P|=504,\quad |A|=4,\quad V\cong C_3^3.
\]

Let (I\) be the augmentation ideal of (k[V]), and write

\[
 T_{\le2}=k[V]/I^3,
 \qquad
 G_2=I^2/I^3
 =\bigoplus_{\substack{\lambda\in\widehat A\\
                        \alpha\in\mathcal B_2}}
       k[P]e_\lambda u^\alpha,
 \qquad |\mathcal B_2|=6.                              \tag{2.1}
\]

The natural full six-occurrence/two-Fox-component ambient is

\[
 \mathcal O_H^{\rm full}
   =\bigoplus_{h\in H_6}k[Q_2]^{\oplus2}.              \tag{2.2}
\]

It is not the stored degree-two source.  The registered filtration first
projects (2.2) to the through-degree-two module and then to its second grade:

\[
 \mathcal O_{H,\le2}
   =\bigoplus_{h\in H_6}
      \left(k[Q_1]\otimes T_{\le2}\right)^{\oplus2},
 \qquad
 \operatorname{gr}_2\mathcal O_{H,\le2}
   =\bigoplus_{h\in H_6}G_2^{\oplus2}.                \tag{2.3}
\]

Consequently

\[
 \dim G_2=4\cdot6\cdot504=12{,}096,
\]

\[
 \dim\mathcal O_H^{\rm full}=6\cdot2\cdot54{,}432
   =653{,}184,
 \quad
 \dim\mathcal O_{H,\le2}=6\cdot2\cdot2016\cdot10
   =241{,}920,
\]

and

\[
 \dim\operatorname{gr}_2\mathcal O_{H,\le2}
   =6\cdot2\cdot12{,}096=145{,}152.                  \tag{2.4}
\]

The current v437/v451 physical target is the PB4-dropped two-hexagon
projection.  Its new second grade and complete lower/auxiliary part have

\[
 \dim G_2^{\oplus4}=48{,}384,
 \qquad 8{,}064+24{,}192+4=32{,}260.                 \tag{2.5}
\]

Thus the current target contains precisely the six H occurrence inputs after
(2.3), and no pentagon Fox-row coordinate.  This is a statement about the
registered codomain, not a claim that a pentagon change vanishes.

## 3. Complete source and endpoint formula

The authoritative source objects are ordered and noncommutative:

```text
C_T  = OrderedProduct(3317 selected GradeNodeRef powers)
C_<1 = RegisteredPriorProduct(prepare.canonical_solution.terms)
C_1  = Compose(C_<1,C_T), prior followed by update.
```

Independently traverse the selected roots and the stored prior terms to obtain

\[
 \mu_T(s,P),\qquad \mu_{<1}(s,P).
\]

The compact `R07LEAF1` stream is compared only with 
(\mu_T\).  After the three roots and every endpoint-one condition have been
authenticated, Fox evaluation permits the evaluation-level sum

\[
 \mu_1=\mu_{<1}+\mu_T\pmod3.                          \tag{3.1}
\]

Equation (3.1) neither commutes nor identifies the source words, and the
ordered `Compose` root remains authoritative.

For each exact path (P), define the unsigned, typed signature

\[
 \Sigma_{11}(P)=
   \bigl(\eta_j\theta_j(P)\bigr)_{j\in J_{11}}
   \in E_3^6\times E_4^5.                             \tag{3.2}
\]

Before any grouping require

\[
 \eta_j\theta_j(r_s)=1                                \tag{3.3}
\]

for every reached seed and all eleven slots.  Then put

\[
 \bar\mu_{s,\tau}
  =\sum_{P:\Sigma_{11}(P)=\tau}\mu_1(s,P).           \tag{3.4}
\]

### Theorem 3.1 (full endpoint signature, six-row output)

For every (h\in H_6),

\[
 \boxed{
 D_h(C_1)=\sum_{s,\tau}\bar\mu_{s,\tau}
                 (\pi_H\tau)_hD_h(r_s).}             \tag{3.5}
\]

#### Proof

By (3.3), the endpoint-one Fox conjugate identity gives

\[
 D_h(Pr_sP^{-1})=\eta_h\theta_h(P)D_h(r_s).
\]

Sum this identity with the exact coefficients (3.1).  The fibres of
(\Sigma_{11}\) refine the fibres of (\pi_H\Sigma_{11}\); hence regrouping
the same finite sum by (3.4) proves (3.5).  No source edge or exact path is
identified by this regrouping. \(\square\)

Two paths may have the same six H endpoints and different five P endpoints.
They receive the same multiplier in (3.5) but remain separate complete
signature receipts.  This is why the finer eleven-slot grouping is safe and
why it supplies no algebraic eleven-to-six adapter.

## 4. Prefix, sign, and direct all-seven gate

Let (q_j=\eta_j(\theta_j(g)^{\epsilon_j})\).  The registered signed block
identities and occurrence prefixes are

```text
H1: q3 q2 q1 = 1;       U1=1,       U2=q3,       U3=q3
H2: q6 q5 q4 = 1;       U4=q6 q5,   U5=q6,       U6=q6
P:  q11 q10 q9 q8 q7=1; U7=1, U8=q11 q10 q9 q8,
                         U9=q11 q10 q9, U10=q11, U11=1.
```

For one leaf the full typed occurrence row is

\[
 \epsilon_jL_{U_j}L_{\eta_j\theta_j(P)}
 D_{\eta_j\theta_j}(r_s).                             \tag{4.1}
\]

Thus the path endpoint acts first, the fixed prefix second, and the sign
exactly once.  Neither prefix nor sign belongs to (3.2).  Appending a source
letter is right multiplication:

\[
 E_j(P\ell)=E_j(P)\eta_j\theta_j(\ell).              \tag{4.2}
\]

For every nonzero complete-root key, the future producer and checker must
compare the sum of all eleven rows (4.1) entrywise with the direct H1, H2 and
pentagon Fox difference for (gPr_sP^{-1}).  This all-seven canary
authenticates PP reversal, PB3 lift, E3/E4 type, inverses, prefix order and
signs.  It retains the five P rows as source receipts; it does not put them
in the PB4-dropped target of (2.5).

## 5. Executable boundary

A future consumer may form the current 48,384-trit row only after it has:

1. authenticated the final Task625 graph, fifteen receipts, independent
   verdict, exact three roots, and exact `R07LEAF1` stream;
2. reconstructed all eleven substitutions, endpoints, fixed prefixes and
   signs and passed (3.3), (4.1), and the direct all-seven comparison;
3. sealed every exact path-to-(\Sigma_{11}\) assignment before grouping;
4. compared entrywise Task565's six substitutions, kernel matrices, crossed
   cochains, signs, destination blocks and prefixes with ordinals 1--6;
5. pinned and replayed the PB4-drop/boundary projection and its commutation
   with filtration and physical aggregation;
6. replayed separately the selected grade-one physical update and the exact
   Task595 MEMBER coefficient equation; and
7. compared every one of the 32,260 lower/auxiliary coordinates with zero.

Only then may it seal the fresh 48,384 trits, the 12,096-byte registered
packing, and the target/lower/top digests.  That residual is merely the input
to the v474 grade-two decision.  Resource exhaustion is `UNKNOWN_RESOURCE`.

```text
ACTUAL ELEVEN ENDPOINT ORDER:                 FIXED ON PAPER
FULL / TRUNCATED / GRADE-2 SOURCE TYPES:      DISTINGUISHED
CURRENT 48,384-TRIT OUTPUT:                   FIRST SIX H OCCURRENCES ONLY
ELEVEN-TO-SIX ROW ADAPTER:                    NOT NEEDED / WRONG TYPE
FULL SIGNATURE -> SIX-ROW RESTRICTION:        PROVED ON PAPER
PENTAGON FOX CHANGE:                          NOT ASSERTED ZERO
TASK625 ACTUAL PAYLOAD / FRESH RHO2:          NOT YET PRODUCED
GRADE TWO / COMPLETE FIRST RUNG:              NOT DECIDED
FULL PB4 / A0 / COMMON / COFINAL LIFT:        NOT DECIDED
FAKE / IHARA:                                 NOT DECLARED
verified:                                      false
```

`R07_ELEVEN_ENDPOINT_SIX_ROW_RESTRICTION_V477_CANDIDATE`
