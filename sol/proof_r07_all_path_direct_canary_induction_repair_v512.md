# R07 all-path direct-canary induction repair v512

Author: root Sol / 2026-09-04

Status: finite amendment of v509 required by the Task789 hostile audit.
The universal conjugate-Fox reduction survives.  This note pins the actual
base-word-dependent occurrence prefixes, the observable finite receipt and
the producer's stronger joint-context guard.  It does not remove the full
21,287-bucket precision-two aggregation, produce rho2, or declare A0, COMMON,
a compatible lift, fake, or Ihara.  `verified=false`.

## 1. Correct eleven-prefix identity

Retain Task789's notation

\[
 \bar q_o=\eta_o\theta_o,\qquad
 \bar D_o=D_{\eta_o}\theta_o,\qquad
 C_{s,P}=P r_sP^{-1}.                                  \tag{1.1}
\]

After the reached-seed endpoint gate
\(\bar q_o(r_s)=1\), the exact left-Fox identity is

\[
 \bar D_o(C_{s,P})=\bar q_o(P)\bar D_o(r_s).          \tag{1.2}
\]

Let \(g\) be the fixed base correction word and put
\(G_{ab}=\eta_{ab}\theta_{ab}(g)\).  The derivative terms belonging to
unchanged copies of \(g\) cancel when the corrected printed equation is
subtracted from the base printed equation.  Their evaluated group factors
do not disappear: they remain as left multipliers of (1.2).  In the exact
registered slot order the required prefix table is

| slot | typed label and sign | actual prefix \(U_o\) |
|---:|---|---|
| 1 | `H1_fxy +` | \(G_{yz}G_{xz}^{-1}G_{xy}=1\) |
| 2 | `H1_fxz -` | \(G_{yz}\) |
| 3 | `H1_fyz +` | \(G_{yz}\) |
| 4 | `H2_fux -` | \(G_{uy}G_{xy}^{-1}\) |
| 5 | `H2_fxy -` | \(G_{uy}\) |
| 6 | `H2_fuy +` | \(G_{uy}\) |
| 7 | `P_b1 +` | \(G_4^{-1}G_2^{-1}G_0G_3G_1=1\) |
| 8 | `P_b2 +` | \(G_4^{-1}G_2^{-1}G_0G_3\) |
| 9 | `P_b3 +` | \(G_4^{-1}G_2^{-1}G_0\) |
| 10 | `P_b5_inverse -` | \(G_4^{-1}\) |
| 11 | `P_b4_inverse -` | \(1\) |

Thus the repaired formula replacing the loose meaning of v509 (2.1) is

\[
 \boxed{
 \mathscr D(s,P)=\sum_{o=1}^{11}\epsilon_o
 L_{U_o}L_{\bar q_o(P)}\bar D_o(r_s)+e(r_s),}
 \qquad
 (\epsilon_o)=(+,-,+,-,-,+,+,+,+,-,-).               \tag{1.3}
\]

Here \(L_h\) denotes left translation by the exact group value \(h\), and
the derivative in (1.3) is unsigned.  An implementation may instead put the
sign into the seed derivative, but it must not apply the sign twice.

## 2. Right-extension induction

For the fixed signed actor order \((-2,-1,1,2)\), define

\[
 S_o(())=1,\qquad A_o(t)=\bar q_o(t),\qquad
 S_o(Pt)=S_o(P)A_o(t).                                  \tag{2.1}
\]

Require
\(A_o(-1)=A_o(1)^{-1}\) and
\(A_o(-2)=A_o(2)^{-1}\) in every typed slot.  Induction on the exact
right-extension trie proves \(S_o(P)=\bar q_o(P)\) for every reached path.
The noncommuting order is `parent * atom`; `atom * parent` is not an
equivalent convention.

Combining (2.1) with (1.2)--(1.3) proves the all-path generic/direct identity
from one empty-path base call for each reached seed and four typed atoms.  It
does not license right multiplication of an already formed group-algebra
row: first extend the endpoint and then left-translate the fixed seed row.

## 3. Observable finite certificate

For each implementation side, the reduced canary emits one canonical
receipt with:

1. the sorted raw reached-seed roster before coefficient cancellation;
2. for every reached seed \(s\), the empty-path generic/direct row encoded
   as `(seed, nnz, canonical_sparse_row_sha256)`;
3. the exact completion count, which is 23 on the actual v14 parent;
4. all four typed eleven-slot atom signatures in order \((-2,-1,1,2)\);
5. both inverse equalities, one independently evaluated noncommuting
   two-letter order anchor, the eleven labels/signs and the prefix-table
   contract (1.3); and
6. one rolling canonical digest and EOF.

The independent checker reconstructs this receipt using its own all-seven
owner and local group/Fox arithmetic.  It neither imports the producer nor
trusts a producer digest without recomputing the rows.  A slot-10 sign or
prefix mutation, an E4-to-E3 slot mutation, a pentagon factor-order mutation
and `atom * parent` must all reach the live validators and be rejected.

The producer's existing generic empty-path call also checks the six E3
components plus all 31 registered E4 joint contexts.  Successful base calls
for all reached seeds therefore propagate this stronger joint endpoint guard
to every conjugate.  The eleven slots alone must not be cited as proving the
31-context statement.

## 4. Loops which remain exact and complete

Only the generic printed-equation replay schedule is replaced.  The
successor must retain:

- the exact Task601 graph, root and leaf ancestry;
- raw reached-seed extraction, canonical exact `(seed,path)` collection and
  coefficient cancellation only after that collection;
- the full typed eleven-slot trie and all path/signature receipts;
- the complete nonzero `(seed,signature)` bucket table;
- every reached-seed endpoint gate;
- precision-two evaluation and accumulation for every one of the
  \(G=21{,}287\) nonzero buckets on both producer and checker;
- the complete 32,260 lower/auxiliary and 48,384 top comparisons, packing,
  parent receipts, and all false claim flags.

On the actual v14 input the expensive generic calls become

\[
 21{,}287\longrightarrow23
 \quad\text{per side},\qquad
 \frac{21{,}287}{23}=925.5217\ldots .                  \tag{4.1}
\]

This removes 21,264 generic calls per side, or 99.89195 percent.  It does
not predict the runtime of the retained full precision-two bucket loop.

## 5. Exact frontier

```text
CONJUGATE FOX IDENTITY:                         PAPER-CLOSED
ACTUAL ELEVEN G-DEPENDENT PREFIX TABLE:         PINNED BY (1.3)
RIGHT-EXTENSION FOUR-ATOM INDUCTION:            PAPER-CLOSED
OBSERVABLE 23-BASE/FOUR-ATOM CERTIFICATE:       SPECIFIED FOR IMPLEMENTATION
GENERIC DIRECT CALLS PER SIDE:                  23 ON ACTUAL V14 PARENT
FULL PRECISION-TWO BUCKETS PER SIDE:            21,287; MUST REMAIN
SAFE TO IMPLEMENT A0 SUCCESSOR:                 YES (TASK789)
FRESH RHO2 / A0:                               NOT YET PRODUCED
COMMON / COMPATIBLE LIFT / FAKE / IHARA:        NOT CLAIMED
verified=false
```

`R07_ALL_PATH_DIRECT_CANARY_INDUCTION_REPAIR_V512`
