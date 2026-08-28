# R07 stable positive-carrier projection v289

Author: Sol / 2026-08-29

Status: paper-grade semantic interface theorem.  V284 proves that an
accepted history-free A0 positive can feed the v225 A2 specializer, but names
the then-current v7 dialect.  This note factors that argument into one stable
semantic carrier and a finite, versioned decoder obligation.  It prevents a
future positive v8/v9/v10 receipt from being stranded merely because A2
hard-codes an older search schema.  It does not accept A0-v10, execute A2,
construct a compatible lift, prove a fake statement, or give an Ihara
witness.  `verified=false`.

## 1. Search certificates and the A2 premise are different types

Let \(R\) be a positive A0 producer receipt, \(V\) its helper-nonshared
checker verdict, and \(M\) the portable transport owner binding their exact
bytes.  The search dialect may change when checkpoint, selected-support, or
task176 reconstruction is repaired.  A2 does not use any of those search
choices.  Its mathematical input is the literal triple

\[
 (g_0,a,f),\qquad g_0=g_{760},\qquad
 f=\operatorname{red}(g_0a),
\tag{1.1}
\]

together with the independently accepted direct replay of that same triple.
Here \(a\) is a right correction; changing it changes the candidate, whereas
changing only the search history does not.

A **registered A0 dialect** \(d\) consists of exact producer/verdict schemas,
exact positive terminals, exact source identities, and two separately
implemented decoders

\[
 D_d^{\rm prod}(R,V,M),\qquad D_d^{\rm chk}(R,V,M).
\tag{1.2}
\]

The tag is closed: an unknown schema, terminal, or source identity is an
input stop.  There is no rule saying that a larger version number is
automatically compatible.

## 2. Stable carrier object

Both decoders must authenticate before extracting data:

1. the physical byte counts and SHA-256 values of \(R,V,M\), their canonical
   self seals, immutable run head, and producer/checker source identities;
2. the exact positive producer and checker terminals and the verdict's
   physical binding to the staged receipt;
3. the common frozen \(g_{760}\), task198 roof/interface, old-row, q3/E4,
   and all other identities named by that dialect's accepted positive gate;
4. that UNKNOWN, resource, hard-stop, SELFTEST, all-false, or separator
   terminals are absent; and
5. that the dialect-specific checker, not a producer Boolean, accepted the
   selected actual sparse equality, correction word, and direct all-seven
   replay.

Each decoder then returns the stable semantic carrier

\[
 \mathcal C=(g_0,a,f,\omega,\iota),
\tag{2.1}
\]

where \(\omega\) is the literal eleven-occurrence/direct H1/H2/P replay and
\(\iota\) is the complete raw identity tuple of \(R,V,M\) and the registered
dialect.  Acceptance requires

\[
 D_d^{\rm prod}(R,V,M)=D_d^{\rm chk}(R,V,M)=\mathcal C,
\tag{2.2}
\]

\[
 a=\operatorname{red}(a),\qquad
 f=\operatorname{red}(f)=\operatorname{red}(g_0a),
\qquad \operatorname{exp}(a)=(0,0),
\tag{2.3}
\]

and exact equality between the words and typed replay values in \(\omega\)
and the independently reconstructed values.  A hash, copied
`all_eleven_and_direct_all_seven` flag, or matching word length cannot replace
these equalities.

The carrier is an internal typed value.  If it is serialized as an adapter
receipt, that receipt is only cross-checked after a second implementation
reconstructs (2.1)--(2.3) from the original \(R,V,M\).  A2 producer and A2
checker may instead perform the two decodings directly.

## 3. Projection soundness

### Theorem 3.1 (VERSIONED POSITIVE-CARRIER PROJECTION)

Suppose a registered dialect \(d\) passes (2.2)--(2.3).  Then the carrier
\(\mathcal C\) supplies exactly the literal task192 premise used by the v225
actual first-edge endpoint specializer.  No discovery basis, dual, checkpoint
row, unselected task176 section, worker schedule, or search completeness
claim is a premise of A2.

#### Proof

The dialect-specific positive checker reconstructs every selected old and
new sparse summand and the fixed target, then proves their complete equality.
Every correction summand is promoted to its literal factor; coefficient two
is interpreted as the inverse word and its row is checked with the negative
\(\mathbf F_3\)-coefficient.  Multiplication in the registered order gives
the word \(a\).  The direct evaluator then constructs the right-corrected
word and all typed occurrence/direct values.  Conditions (2.2)--(2.3)
compare those reconstructed objects with the extracted carrier.

V225 assumes precisely a literal base word, a literal right correction, the
freely reduced corrected word, and their accepted replay.  These are
\((g_0,a,f,\omega)\).  The objects used only to discover the selected support
do not occur in that premise.  Hence the carrier supplies the v225 input.
\(\square\)

This is positive-only.  If a speculative search returns UNKNOWN or exhausts
a resource cap, no carrier exists and no negative A2 conclusion follows.

## 4. A2 is extensional in the stable carrier

Let \(T_{198}\) be the accepted word-independent roof interface.  V225
constructs, occurrence by occurrence,

\[
 \mathcal S_{\rm PB}(\mathcal C,T_{198})=
 \left((B(o),\rho_o,\sigma_o,P_o,\xi_o)_{o=1}^{11},
       (\epsilon_B)_{B=H1,H2,P},w,\bar\epsilon_1,u_0\right).
\tag{4.1}
\]

### Theorem 4.1 (DIALECT-INDEPENDENT A2 EXTENSIONALITY)

For a fixed carrier value and fixed \(T_{198}\), the complete package in
(4.1) is independent of the registered search dialect which produced the
carrier.

#### Proof

Every prefix, sign, group-basis value and
\(\xi_o=\rho_o(g_0)^{-1}-1\) is a deterministic function of \(g_0\) and
the task198 occurrence ledger.  Every corrected residual is evaluated from
\(f\), and the projected values \(w,\bar\epsilon_1,u_0\) are deterministic
applications of the pinned q3/Q4 and matching \(D_1\) maps.  The formulas do
not read a search pivot, dual, checkpoint, cursor, selected-support size, or
task176 parent tree.  Equal inputs therefore give equal outputs. \(\square\)

Two different accepted correction words give two different carriers and
may give different A2 packages.  Extensionality removes schema dependence;
it does not identify distinct mathematical candidates.

## 5. Registration obligation for v10 and later

The pending v10 dialect can be registered after, and only after, an
independent code/performance PASS and an accepted positive execution.  Its
local decoder obligation is finite:

1. require schema `d972-r07-history-free-positive-fast-resume/v10` and the
   exact v10 COMMON producer/checker terminals;
2. authenticate the accepted v10 receipt, verdict, portable binding, source
   graph, and versioned task176 recovery-v2 identity;
3. extract `g760`, `correction_word`, `corrected_word`, and the final literal
   replay from their frozen v10 locations;
4. independently enforce (2.3) and equality with the verdict's reconstructed
   positive result; and
5. emit only (2.1), not the discovery checkpoint or its heavy decoded
   task176 owners, to the mathematical A2 specializer.

The last item is a transport reduction, not a weakening.  The v10 checker
must inspect the heavy owners in order to accept \(R,V,M\); after that
acceptance, A2 authenticates their exact transitive identity through
\(\iota\) and independently recomputes the v225 mathematics from the literal
words and task198.  Reopening the 86 MB old checkpoint or the complete
task176 section roster inside A2 would add cost without adding an A2
equality.

A later v11 needs a new closed tag and two decoder branches, but Theorems 3.1
and 4.1 do not change.  A decoder branch is rejected if it imports a producer
helper, accepts a positive Boolean, omits the receipt/verdict byte binding,
or silently maps an unknown field layout to the last known layout.

## 6. Minimal implementation and mutation contract

The next A2 production revision should retain the already accepted v225
specializer and replace its cached-v3-only predecessor parser by a closed
dialect registry.  The producer and checker implement the registry
separately.  Both compare the resulting stable carrier before performing
their independent PB construction.

Required ordinary-validator mutations include the dialect tag, producer and
checker terminal, receipt physical SHA, verdict receipt binding, run head,
one letter in each of \(g_0,a,f\), multiplication order, free reduction,
coefficient-two inverse, one occurrence replay, one direct block replay,
task198 identity, and recovery-v2 identity.  Each mutation changes a physical
owner before the normal validator and reaches its narrow rejection.  A
mutation name, expected-failure branch, or copied before/after digest is not
a test.

The adapter work is linear in the three literal words and their small replay
envelopes.  It must not launch a boundary search, reconstruct all task176 Q0
sections, rebuild A0's DAG/echelon, or claim cached-v3 trajectory parity.

## 7. Fixed frontier

```text
VERSIONED A0 POSITIVE -> STABLE SEMANTIC CARRIER:  PAPER PROOF
STABLE CARRIER -> V225 A2 PREMISE:                 PAPER PROOF
A2 MATHEMATICS DEPENDS ON A0 SEARCH DIALECT:       NO
NEW DIALECT NEEDS A CLOSED LOCAL DECODER:          YES
PENDING V10 IMPLEMENTATION / AUDIT / EXECUTION:    NOT ACCEPTED
ACTUAL A0 COMMON / ACTUAL A2 SPECIALIZATION:       0/1 / 0/1
COMPATIBLE LIFT / FAKE / IHARA:                    NONE
```

`R07_STABLE_POSITIVE_CARRIER_PROJECTION_V289_PAPER_GRADE`
