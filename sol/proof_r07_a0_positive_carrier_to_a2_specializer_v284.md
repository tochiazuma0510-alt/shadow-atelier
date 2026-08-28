# R07 A0 positive carrier to A2 specializer v284

Author: Sol / 2026-08-29

Status: paper-grade semantic-adapter theorem.  This note proves that an
independently accepted A0-v7 COMMON receipt supplies exactly the two literal
word inputs required by v225, even though its search schema and certificate
shape differ from cached-v3.  It does not accept the in-progress v7 code,
produce an actual A0 word, execute A2, construct a compatible lift, prove a
fake statement, or give an Ihara witness.  `verified=false`.

## 1. The concrete downstream mismatch

The accepted SELFTEST implementation of the current A2 specializer reads a
task192 object only through the cached-v3 production dialect.  In particular
it requires

```text
schema   = d972-r07-normalized-exact-common-word-cached/v3
terminal = R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD
g0       = receipt.g760
a        = receipt.exactification.literal.c_exact
f        = receipt.exact_direct_replay.replay.corrected_word
```

and it requires the old production-binding attestation.  A0-v7 deliberately
has a different schema and terminal and, on COMMON, stores the same semantic
roles as

```text
g0 = receipt.g760
a  = receipt.correction_word
f  = receipt.corrected_word.
```

Consequently a successful v7 receipt would be rejected by the present A2
parser before specialization.  This is an ABI mismatch, not a mathematical
failure and not evidence against a witness.

## 2. Accepted positive carriers

Let `red` denote deterministic free reduction.  A **positive A0 carrier** is
a tuple

\[
 \mathcal A=(R,V,M),
\tag{2.1}
\]

where (R) is a producer receipt, (V) is a helper-nonshared positive
verdict, and (M) is the portable artifact/transport binding of their raw
bytes.  Acceptance means all of the following.

1. (M) binds the exact receipt and verdict byte counts and SHA-256 values,
   the immutable run head, the producer/checker identities, and their exact
   common positive terminal.
2. The self seals of (R) and (V) are valid, (V) is a positive PASS, and
   the portable byte count and SHA-256 extracted from
   `V.receipt_physical` equal the staged bytes of (R).  Original device and
   inode numbers are execution-time anti-TOCTOU data and are not asserted to
   survive artifact copying.
3. The schema-specific independent checker, rather than a consumer-supplied
   Boolean, has established the literal word and all-seven replay described
   below.

There are presently two admissible positive dialects.

- In cached-v3, put
  
  \[
    g_0=R.\texttt{g760},\qquad
    a=R.\texttt{exactification.literal.c\_exact},\qquad
    f=R.\texttt{exact\_direct\_replay.replay.corrected\_word}.
  \tag{2.2}
  \]

- In v7, require the exact terminal
  `R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V7_COMMON_WORD` and put

  \[
    g_0=R.\texttt{g760},\qquad
    a=R.\texttt{correction\_word},\qquad
    f=R.\texttt{corrected\_word}.
  \tag{2.3}
  \]

For either dialect define the normalized, internal-only carrier

\[
 \boxed{N(\mathcal A)=(g_0,a,f,\omega)},
\tag{2.4}
\]

where (omega) is the authenticated literal replay data.  The normalizer
must independently require

\[
 \boxed{f=\operatorname{red}(g_0a)}.
\tag{2.5}

It is a tagged sum parser: a document may satisfy exactly one registered
dialect.  Relabelling a v7 object as cached-v3, copying old attestations, or
accepting an unknown/resource terminal is forbidden.

## 3. V7 supplies the v225 word premise

### Proposition 3.1 (V7 POSITIVE-CARRIER SOUNDNESS)

If the helper-nonshared v7 checker accepts a COMMON receipt under its full
selected-support contract, then (2.3) satisfies (2.5), and (a) has the
literal right-correction and eleven-occurrence/direct-all-seven properties
required of the task192 input in v225.

#### Proof

The v7 checker first reconstructs the fixed H1/H2/P target.  For every
selected old symbol it reconstructs the typed boundary provenance, and for
every selected new symbol it directly reconstructs its boundary or
correction row.  It then checks the full sparse equality, rather than a
producer digest or Boolean.

For a correction coefficient two it explicitly replaces the selected word
by its inverse and checks that the corresponding direct row is the negative
row over \(\mathbf F_3\).  It multiplies the resulting finite correction
factors in their canonical order to obtain the literal word (a), verifies
its exponent pair and joint-kernel value, and calls the independent direct
column evaluator on ((1,a)).  That evaluator constructs

\[
 f=\operatorname{red}(g_0a),
\tag{3.1}
\]

evaluates all eleven typed occurrences, evaluates the direct H1, H2, and P
relations, and requires equality of the occurrence and direct Fox columns.
The checker finally requires its reconstructed (a,f) and replay object to
equal the fields in (R).  Thus (2.5), literal right multiplication, all
eleven occurrences, and direct all-seven replay are independently derived.
\(\square\)

The heuristic checkpoint basis is absent from the conclusion.  It proposes
the finite selected support, but v278 and the v7 checker reconstruct every
summand used in the accepted equality.  Therefore no cached-v3 path parity or
unselected checkpoint provenance is a premise of Proposition 3.1.

## 4. Extensionality of the A2 construction

Let (T_{198}) be the accepted, word-independent task198 roof interface.
V225 constructs

\[
 \mathcal S_{\rm PB}(g_0,f)=
 \left((B(o),\rho_o,\sigma_o,P_o,\xi_o)_{o=1}^{11},
       (\epsilon_B)_{B=H1,H2,P}\right)
\tag{4.1}
\]

from (g_0,a,f), the task198 ledger, and pinned literal PB constructors.

### Theorem 4.1 (A0-CARRIER EXTENSIONALITY)

For every accepted positive carrier \(\mathcal A\), the v225 package

\[
 \mathcal S_{\rm PB}\bigl(N(\mathcal A),T_{198}\bigr)
\tag{4.2}
\]

depends only on the normalized literal words (g_0,a,f), their accepted
replay, and (T_{198}).  It is independent of whether the carrier was found
by cached-v3 or v7, of the checkpoint columns, the search duals, the order in
which discovery rows were inserted, and the selected-support size.

#### Proof

Inspect the defining equations of v225.  Each
(r_o=\rho_o(g_0)), signed factor, prefix (Q_o), (P_o), and
(\xi_o=r_o^{-1}-1) is a deterministic function of (g_0) and the fixed
task198 occurrence ledger.  The residual is

\[
 e_B=-\delta_B R_B(f),
 \qquad
 \epsilon_B=1-\overline{R_B(f)},
\tag{4.3}
\]

and (f=\operatorname{red}(g_0a)) by (2.5).  The projected values
(w,\bar\epsilon_1,u_0) are then deterministic applications of the pinned
Q3/Q4 and (D_1\) maps.  None of these formulas reads a search basis, a dual,
or a discovery transcript.  Proposition 3.1 supplies the same literal
premise in the v7 case.  Hence (4.2) is extensional in the claimed data.
\(\square\)

Different accepted correction words need not be equal.  The theorem says
that each independently accepted word gives its own valid A2 specialization;
it does not identify a future v7 word with a hypothetical cached-v3 word.

## 5. Binding implementation contract

The next A2 production revision must preserve the accepted mathematical
specializer and replace only its hard-coded predecessor parser by two
independent implementations of (2.4): one in the producer and one in the A2
checker.

For the v7 branch each implementation must:

1. read the v7 receipt, v7 verdict, and portable artifact binding as separate
   immutable byte owners;
2. verify their schemas, seals, common terminal, raw byte hashes, source and
   producer/checker pins, and the receipt-byte binding in the verdict;
3. reject every UNKNOWN terminal and every all-false/nonpositive verdict;
4. extract (g_0,a,f) by (2.3), freely reduce them, and require (2.5);
5. require the independently derived v7 verdict field
   `all_eleven_and_direct_all_seven=true`, while also checking that the
   receipt's literal replay has the correct words and replay shape;
6. feed only the normalized (g_0,a,f) and authenticated task198 data into
   the existing v225 construction; and
7. bind the exact three predecessor bytes into the A2 result and verdict.

The A2 checker must not import the producer normalizer.  Mutation tests must
physically alter, before validation, the receipt terminal/schema, verdict
status, portable receipt hash, (g_0), (a), (f), correction order, one
all-seven replay value, and task198 binding.  Each must reach and be rejected
by its narrow owner.

No 86 MB checkpoint replay, triangular-basis rebuild, boundary epoch, or Q0
construction belongs in A2.  Those establish the upstream positive receipt.
The additional consumer work is linear in the three literal words, eleven
substituted relation words, and the small acceptance envelopes.

If A0-v7 returns UNKNOWN, no normalized carrier and no A2 actual output may
be emitted.  A typed UNKNOWN is not a negative or nonexistence result.

## 6. Fixed frontier

```text
A0-v7 COMMON -> v225 semantic sufficiency:     PROVED ON PAPER
CURRENT A2 HARD-CODED CACHED-v3 PARSER:         INCOMPATIBLE WITH V7
SEARCH-HISTORY/CHECKPOINT DATA NEEDED BY A2:    NO
V7 IMPLEMENTATION / AUDIT / EXECUTION:          PENDING
A2 V7-CARRIER IMPLEMENTATION / SELFTEST:        NOT YET COMMISSIONED
ACTUAL A0 / ACTUAL A2:                          0/1 / 0/1
COMPATIBLE LIFT / FAKE / IHARA:                 NONE
```

`R07_A0_POSITIVE_CARRIER_TO_A2_SPECIALIZER_V284_PAPER_GRADE`
