# R07: eleven endpoint gates and the six-row precision-two restriction (v478)

Author: Sol / 2026-09-03

Status: second finite typing repair of v476.  This note pins v477 and replaces
only its display (2.1)--(2.4) by the correctly induced (Q_2)-filtration
grade below.  All other definitions, Theorem 3.1, proof, executable gates and
claim boundaries of v477 are incorporated unchanged.  It constructs no
payload or residual and proves no grade decision, A0, COMMON, cofinal lift,
fake, or Ihara conclusion.  `verified=false`.

## 1. Versioned replacement

The parent is
`sol/proof_r07_eleven_endpoint_six_row_restriction_repair_v477.md`,
8,668 bytes, SHA-256
`11aa7c86ddf2da6e936621534efa56d118d8546ece299b8952013835656b33e9`.
Its eleven-slot ledger, typed coordinate restriction

\[
 \pi_H:E_3^6\times E_4^5\longrightarrow E_3^6,
 \qquad(g_1,\ldots,g_{11})\longmapsto(g_1,\ldots,g_6),
\]

complete-root construction, endpoint gates, finer-signature regrouping,
prefix/sign formulas, direct all-seven canary and consumer boundary remain
literal premises of this successor.  The following section supersedes only
v477 (2.1)--(2.4).

## 2. Correct induced filtration type

Fix (k=\mathbf F_3), (Q_1=P\times A), and

\[
 1\longrightarrow V\longrightarrow Q_2\longrightarrow Q_1
 \longrightarrow1,
 \qquad |P|=504,\quad |A|=4,\quad V\cong C_3^3.
\]

Let

\[
 I_V=\operatorname{Aug}(k[V]),
 \qquad T_{\le2}=k[V]/I_V^3.                         \tag{2.1}
\]

The bare vector space (I_V^2/I_V^3) has dimension six.  The degree-two
module used by the first-rung engine is its (Q_1)-induced group-ring grade,
not the bare kernel grade:

\[
 \begin{aligned}
 G_2
   &:=k[Q_1]\otimes_k(I_V^2/I_V^3)\\
   &\cong
     \bigoplus_{\substack{\lambda\in\widehat A\\
                           \alpha\in\mathcal B_2}}
       k[P]e_\lambda u^\alpha,
       \qquad |\mathcal B_2|=6.                     \tag{2.2}
 \end{aligned}
\]

Thus

\[
 \dim_k G_2=|Q_1|\cdot6
             =4\cdot504\cdot6=12{,}096.             \tag{2.3}
\]

The full six-occurrence/two-Fox-component ambient, its registered truncation,
and the second associated grade are three different objects:

\[
 \mathcal O_H^{\rm full}
   =\bigoplus_{h\in H_6}k[Q_2]^{\oplus2},            \tag{2.4}
\]

\[
 \mathcal O_{H,\le2}
   =\bigoplus_{h\in H_6}
      \left(k[Q_1]\otimes_kT_{\le2}\right)^{\oplus2},
 \qquad
 \operatorname{gr}_2\mathcal O_{H,\le2}
   =\bigoplus_{h\in H_6}G_2^{\oplus2}.              \tag{2.5}
\]

Since (dim T_{\le2}=1+3+6=10), their respective dimensions are

\[
 \begin{aligned}
 \dim\mathcal O_H^{\rm full}
   &=6\cdot2\cdot54{,}432=653{,}184,\\
 \dim\mathcal O_{H,\le2}
   &=6\cdot2\cdot2016\cdot10=241{,}920,\\
 \dim\operatorname{gr}_2\mathcal O_{H,\le2}
   &=6\cdot2\cdot12{,}096=145{,}152.                \tag{2.6}
 \end{aligned}
\]

The eight registered source auxiliaries are outside
(\mathcal O_{H,\le2}), so a complete through-degree-two source tuple has
width (241{,}920+8=241{,}928).  Likewise the current PB4-dropped
two-hexagon target has

\[
 \dim G_2^{\oplus4}=48{,}384,
 \qquad 8{,}064+24{,}192+4=32{,}260                  \tag{2.7}
\]

new and lower/auxiliary coordinates respectively.  These dimensions do not
assert that a pentagon Fox change is zero; they describe the registered
two-hexagon codomain after the PB4 projection.

## 3. Retained theorem and executable consequence

For the exact complete-root leaf map (mu_1), after every eleven-slot
endpoint-one gate, retain

\[
 \Sigma_{11}(P)=
   (\eta_j\theta_j(P))_{j=1}^{11}\in E_3^6\times E_4^5,
 \qquad
 \bar\mu_{s,\tau}
  =\sum_{P:\Sigma_{11}(P)=\tau}\mu_1(s,P).
\]

Then the v477 theorem remains

\[
 D_h(C_1)=\sum_{s,\tau}\bar\mu_{s,\tau}
              (\pi_H\tau)_hD_h(r_s),
 \qquad h\in H_6.                                   \tag{3.1}
\]

Its proof is unchanged: the endpoint-one conjugate identity is summed over
the exact source leaves, and the complete eleven-endpoint fibres refine the
first-six fibres.  The filtration replacement above changes neither that
finite partition argument nor the occurrence-first prefix/sign maps.

Accordingly a future consumer must still authenticate all eleven E3/E4
slots and the direct H1/H2/pentagon canary, but it feeds only ordinals 1--6
into the present 145,152-to-48,384 graded physical map.  The five P endpoints
remain sealed source receipts for the full all-seven interpretation and a
future B4 target.  There is no `% 6`, no E4-to-E3 adapter, and no P-zero
claim.

```text
FORBIDDEN CONTROL BYTE IN v478:              ABSENT
BARE KERNEL GRADE I_V^2/I_V^3:               DIMENSION 6
INDUCED DEGREE-TWO MODULE G_2:                DIMENSION 12,096
FULL / TRUNCATED / GRADE-2 OCCURRENCE TYPES:  DISTINGUISHED
CURRENT LOWER / TOP PHYSICAL WIDTHS:          32,260 / 48,384
ELEVEN-ENDPOINT -> SIX-ROW OPERATION:          TYPED RESTRICTION
PENTAGON FOX CHANGE:                          NOT ASSERTED ZERO
TASK625 PAYLOAD / FRESH RHO2:                 NOT YET PRODUCED
A0 / COMMON / COFINAL LIFT / FAKE / IHARA:    NOT DECLARED
verified:                                      false
```

`R07_ELEVEN_ENDPOINT_SIX_ROW_RESTRICTION_V478_CANDIDATE`
