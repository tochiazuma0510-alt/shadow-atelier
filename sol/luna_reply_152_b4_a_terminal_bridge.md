# B4-A terminal bridge audit (fixed M / Q0 / 972 ledger)

Date: 2026-08-16
Role: Luna implementation/evidence audit.  This report is deliberately
restricted to the A-side implication.  It does not claim a global
non-arithmetic or Ihara conclusion.

## Executive verdict

The three requested implications do not close from the current artifacts.
The exact algebraic part of a finite norm witness does close, and the
paper-level descent implication also closes once the window and the defect
identification hypotheses are supplied.  The missing hypotheses are not
cosmetic:

| requested item | verdict for the current M/Q0/972 artifacts | reason |
|---|---|---|
| (i) M is an isolated member of `NFI_PB4(B4)` | **UNKNOWN** | the code certifies a finite marked PB3 quotient, not a typed finite-index normal PB4 subgroup with isolatedness; the intended `N_S4` isolated input is still UNKNOWN |
| (ii) 972 is every eligible lift/candidate | **UNKNOWN** | 972 is the frozen target-key set of one finite base scan; it is not a proof of all PB4 refinements or of the source fibers of a reduction map |
| (iii) norm nonidentity implies pentagon failure and a zero fiber | **conditional only** | finite-image nonidentity proves nonidentity in the presented quotient; `D` equals the paper pentagon defect only on the `(3.10)`/PENT-FORM domain, while the unconditional formula uses `\widetilde D`; a zero fiber additionally needs complete reduction-fiber enumeration |

Thus one strict nonidentity can be promoted to a local, typed A witness only
after the checklist in §7.  It cannot currently be promoted directly to
`B4_A_ZERO_FIBER`, and it cannot by itself prove a global genuine/Ihara
statement.

## 1. What is actually fixed and what the code proves

The universal producer builds the following marked presentation.

* `search/d972_dovetail_worker_v1.g:257-345` constructs the finite marked
  B3 quotient `Q=<s1,s2>` and checks braid/order gates.  The full marked
  quotient has order `8817984`; its pure kernel and compact pure model have
  order `1469664` (`:300-320`).  This is an exact finite permutation-model
  calculation for the chosen B3 construction.
* `search/d972_b4_universal_v2.g:83-100` transports the compact pure model to
  a two-generator marked fp presentation `B4Q0fp`, preserving the two marked
  generators and order `1469664`.
* `search/probe/hsp7_gap_v1/stage2_k05.g:19-54` constructs a six-generator
  presentation for `K(0,5)=PB4/<<Delta4^2>>`, with the ordered generators
  `(X12,X13,X14,X23,X24,X34)`.  The same file defines the rho dictionary and
  checks relator preservation at `:76-107`; its own `rho^5` check is deferred
  (`:109`).  `universal_v2.g:102-129` supplies the stronger rho/rho^5 checks
  used by the universal lane.
* `universal_v2.g:131-184` maps Q0 relators by `j(x)=X12`,
  `j(y)=X23` (therefore `U4`, not `U2`), adds all five rho-orbit copies, and
  checks the resulting 158 relators and rho descent.  At the presentation
  level this is a sound quotient
  \[
    U_M=F(X_{12},X_{13},X_{14},X_{23},X_{24},X_{34})/I_M,
  \]
  provided the stated K(0,5), coface, and rho semantics have been established.
* The canonical exact norm is
  \[
    D(f)=\rho^4(jf)\,\rho^3(jf)\,\rho^2(jf)\,\rho(jf)\,jf,
  \]
  evaluated in reverse orbit order in `universal_v2.g:215-229` and in
  `search/d972_b4_u_idrel_direct_logged_v1.g:154-169`.  The frozen word,
  relator, rho, target, and roof digests are respectively
  `ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e`,
  `12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e`,
  `23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed`,
  `9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62`, and
  `3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8`.

These are important closed *syntactic/algebraic presentation* gates.  They
are not yet the semantic statement that the presentation is the quotient
attached to an isolated `N in NFI_PB4(B4)`.

## 2. (i) The fixed M is not yet a proved isolated PB4 window

### 2.1 What can be closed

For a normal finite-index subgroup `N` of a group `G`, the paper defines
`NFI(G)` as the finite-index normal subgroups (`papers/txt/2008.00066-what-are-gt-shadows.txt:441-448`).
For `N in NFI_PB4(B4)`, the paper defines the induced PB3/PB2 subgroups by
the five coface maps and states that they are finite-index normal subgroups
(`:581-610`).  Therefore the following elementary conditional lemma is
available and is the right semantic bridge:

**Window typing lemma.**  If a subgroup `N` is explicitly given as a normal
finite-index subgroup of `B4`, and the six coface maps are the paper's maps
(A.18), then the induced PB3 subgroup is the object whose marked quotient is
being scanned.  If, in addition, the induced PB3 quotient is the fixed Q0
quotient and the K(0,5) central quotient is handled by an explicit PB4 map,
then the 158-relator presentation is a quotient presentation for the
corresponding coface roof.

This is a conditional statement; it does not turn a finite presentation into
a PB4 subgroup automatically.

The intersection-isolated argument is also elementary once its hypotheses are
typed.  If `N1,...,Nr` are isolated finite-index normal subgroups of PB3 and
`M=intersection Ni`, then for any shadow `t` at M, reduction to each `Ni` is
settled, so
\[
  \ker T_t=T_t^{-1}(\cap_i(N_i/M))=\cap_i N_i=M.
\]
This is the argument recorded in
`docs/notes/d972_h1_adjudication_v1.md:36-53`.  Consequently the intended
route
\[
  K^{(9)}\text{ isolated}\quad\&\quad N_{S4}\text{ isolated}
  \Longrightarrow M=K^{(9)}\cap N_{S4}\text{ isolated}
\]
is valid *if* the two displayed subgroups are the correctly typed PB3
objects.  `K^(9)` is treated as isolated by the cited theorem, but the same
note explicitly records `N_S4` isolated as UNKNOWN (`:56-63`, `:84-101`).

### 2.2 What remains open

The current base code proves `|PB3/M|=1469664` for its marked permutation
construction, but it does not prove all of the following:

1. that the intended `M=K^(9) cap N_S4` is the kernel of the exact displayed
   map, rather than only a quotient with the expected order;
2. that `M` has been lifted/typed as a normal finite-index subgroup of `B4`
   (the paper's A.18 coface construction is not itself a proof that a
   two-generator PB3 quotient is a PB4 NFI window);
3. that the central `Delta4^2` quotient used in `K(0,5)` has been connected
   to the chosen PB4 normal subgroup with the required kernel inclusion; or
4. that every GT-shadow at M is settled.

The fourth point is visible directly in
`search/d972_dovetail_worker_v1.g:484-490`: `settled` is computed and counted,
but the row is appended regardless of its value.  The universal driver checks
only `B4Res.shadow_count=972` (`search/d972_b4_universal_v2.g:186-189`); it
does not require `settled_count=shadow_count`.  The finite H1 note gives the
correct missing experiment: measure the exact `N_S4` quotient, enumerate all
its shadows, check each kernel, and require all shadows settled
(`d972_h1_adjudication_v1.md:84-101`).

**Verdict for (i):** Q0 is a finite marked PB3 quotient candidate.  The claim
that the fixed M is an isolated `NFI_PB4(B4)` window remains UNKNOWN.  It can
be closed either by a direct PB4 kernel/normality/isolatedness certificate, or
by a fully typed `M=K^(9) cap N_S4` proof together with the missing `N_S4`
isolated certificate and the PB4 lift/central-kernel certificate.

## 3. (ii) 972 is not yet an all-lifts/all-candidates theorem

`D972ScanCalibrationBase` does perform a substantial finite enumeration:
`search/d972_dovetail_worker_v1.g:451-490` loops over the registered charming
`m` residues and every element of the derived subgroup of the compact Q0
model, checks the theta/tau equations, the two literal equations, and
surjectivity, then computes a canonical target key.  The frozen check at
`:496-510` proves that the resulting target-key set has 972 distinct keys and
the pinned digest.  This closes the following narrow statement:

> In this particular marked finite Q0 model, the registered scan produced the
> exact frozen list of 972 distinct target keys.

It does **not** close the stronger statement needed for A:

> every eligible GT-shadow at the PB4 window, and every possible lift of each
> target shadow through every relevant isolated refinement, occurs exactly once
> in that list.

There are three separate gaps.

* The code's `candidate_count` is the size of the finite loop, not a proof that
  the loop parametrizes all classes in `GT^heart(M)`.  The quotient marking,
  charming representative theorem, onto condition, and the relation between
  `D=DerivedSubgroup(compact)` and the paper's `F2/N_F2` classes must be proved
  together.
* `settled=false` rows are retained.  Thus even the interpretation “972 are
  all shadows of an isolated M” is not justified by the current receipt.
* A reduction fiber is a different object.  For `K <= M`, the paper's map is
  \[
    R_{K,M}:GT^heart(K)\longrightarrow GT^heart(M),
  \]
  and a lift may use `(m1,f1)` with
  `m1 = m (mod N_ord)` and `f1 N_F2=f N_F2`
  (`papers/txt/2008.00066-what-are-gt-shadows.txt:3014-3029`).  A target-key
  digest at M does not enumerate the source rows or prove this reduction map
  is complete.  The phase-2 note correctly says that a finite 972 value by
  itself stays UNKNOWN and that a cofinal chain/source enumeration is needed
  (`docs/notes/d972_phase2_cofinal_execution_v1.md:1-4`, `:12-23`, `:48-67`).

In particular, `Length(targetKeys)=972` is a cardinality/digest gate, not an
exhaustivity theorem.  It does not rule out a missing candidate paired with a
duplicate representation, a non-settled row, an unregistered m-class, or a
refinement lift whose source representative is not in the base loop.

## 4. (iii) Norm nonidentity, the actual pentagon, and the zero fiber

### 4.1 The algebraic implication that is sound

Let `F` be the free group on the six named K(0,5) generators and let `I_M` be
the normal closure of the 158 frozen relators.  If an independently checked
finite tuple `pi_i` of generator images satisfies every one of the 158
relators, it factors through `U_M=F/I_M`.  If the exact norm word `D` has
`pi(D) != 1`, then
\[
  D\notin I_M,\qquad D\ne1\text{ in }U_M.
\]
This is a one-line quotient argument and is fully replayable.  The current
finite-image checker checks the six images, all 158 relators, rho^5, the exact
972 word/key binding, and the nonidentity witness
(`search/check_d972_b4_finite_image_v2.py:298-415`).  A receipt passing those
gates is therefore a valid **local presentation nonidentity** result.

By contrast, a nonempty reduced word from bounded or nonconfluent KBMAG is not
such a witness.  The direct IdRel lane explicitly records that a reduced word
is UNKNOWN and only promotes the all-486 identity case
(`search/d972_b4_u_idrel_direct_logged_v1.g:1-19`).  IdRel's logged product of
original relators proves identity when replayed; it cannot prove nonidentity
unless accompanied by a complete word problem/finite quotient certificate.

### 4.2 The semantic defect is not automatically the current D

The paper's GT-pair definition requires both hexagons (2.18),(2.19) and the
pentagon (2.20) (`papers/txt/2008.00066-what-are-gt-shadows.txt:906-930`).
The five-factor word used by the universal lane is the `PENT_W` word
\[
 D=f_5f_4f_3f_2f_1
   =\bar\rho^4(jf)\bar\rho^3(jf)\bar\rho^2(jf)\bar\rho(jf)jf.
\]
The repository's independently written PENT-FORM note gives the precise
qualification:

* On the `(3.10)`/condition-(I) domain,
  `(2.20) <=> D=1` (PENT-FORM),
  `docs/notes/b4_direct_adjudication_feasibility_v1_2.md:117-128`.
* Unconditionally for `f in [F2,F2]`, the word corresponding to (2.20) is
  \[
  \widetilde D(f)=f(x_{45},x_{34})^{-1}f(x_{12},x_{15})^{-1}
     f(x_{23},x_{34})f(x_{45},x_{51})f(x_{12},x_{23}),
  \]
  not the current D (`:130-146`).  D and `\widetilde D` agree only after the
  condition-(I) substitutions (`:138-143`).
* The same note records a concrete failure of the unqualified implication:
  on `\widetilde N_core`, `PENT_W` fails while (2.20) is true for all 252
  charming examples (`:78-92`, summarized at `:154-160`).  Therefore the
  general implication `D != 1 => (2.20) fails` cannot be used without its
  domain hypotheses.

There is a second quotient-inclusion condition.  The B4-DIR statement in the
same note (`:97-100`) says that `PENT_W` failure implies (2.20) failure when
the tested PB4 window subgroup is contained in the inverse image `L` of the
finite quotient W.  Outside that inclusion the B4-VAC example is a direct
counterexample.  A finite image of U_M must therefore be connected to an
actual PB4 quotient and its kernel inclusion; an arbitrary finite image of an
abstract six-generator presentation is not enough.

### 4.3 Why one failed norm is not automatically a zero reduction fiber

Suppose a target key `t` really is an element of `GT^heart(M)`.  If
`K <= M` and a lift `t_K` existed, the paper's reduction map would put its
reduction in `GT^heart(M)` (`papers/...:3014-3029`).  Hence a correctly typed
failure of (2.20) for the target class at M would contradict the existence of
that lift.  This gives the useful conditional implication:

\[
\begin{split}
&t\in GT^heart(M),\quad D_t\text{ is the paper's (2.20) defect},\\
&\pi(D_t)\ne1\text{ in a sound quotient of the M-window}
\quad\Longrightarrow\quad
\operatorname{Im}(R_{K,M})\text{ does not contain }t
\end{split}
\]
for every `K <= M` to which the quotient/inclusion proof applies.

The hypotheses are essential.  The current 972 rows are candidate rows before
the universal norm test, and the producer does not bind an `isolated=true`
gate or a complete source reduction map.  Consequently a failed D currently
shows at most “this candidate is not a pentagon solution in the tested
presentation/finite quotient”.  It does not show that the target key is an
eligible target GT-shadow with an empty K-fiber.  The actual shadow-fiber
worker has the stronger structure: complete source rows, an exact target-key
map, `isolated`, `exactFibers`, and a nonempty `zeroKeys` gate.  Those are the
right ingredients; a bare 972 norm bit is not a substitute.

## 5. Minimal counterexamples to the tempting shortcuts

1. **PENT_W shortcut:** the recorded B4-VAC window has 252 concrete charming
   rows with `D != 1` but (2.20) true.  This refutes an unconditional
   `PENT_W-FAIL => pentagon-FAIL` bridge.
2. **D versus `\widetilde D`:** for a row outside condition (I), changing the
   first two factors from `f_5,f_4` to their reversed inverse factors changes
   the word.  PENT-FORM' proves the latter is the pentagon defect; PENT-FORM
   proves equality with D only on S1.  Thus a D witness without an S1/I gate is
   not a pentagon witness.
3. **972 cardinality shortcut:** a list can have 972 distinct keys while
   containing an unsettled candidate and omitting a source lift.  The worker's
   own `settled` field is evidence of this logical distinction: it records the
   predicate but does not filter rows (`d972_dovetail_worker_v1.g:484-490`).
4. **finite-presentation shortcut:** a relator-preserving map from the six
   generators only proves a quotient of U_M.  Without a PB4 kernel map and the
   `N <= L`/central compatibility statement, it is not a finite NFI_PB4 window.

## 6. What “one strict nonidentity” may legitimately mean

Accept a norm as strict nonidentity only in one of these two forms:

* an independently replayed finite quotient witness: all six generator images,
  all 158 relators, rho descent/rho^5, exact word/key binding, and a nonidentity
  image; or
* a complete confluent/automatic word problem certificate whose axiom checks
  and relator provenance are independently replayed, so a nonempty normal form
  is provably nonidentity.

An IdRel log is sufficient for a positive identity chain, not for a negative
word.  A bounded or nonconfluent `ReducedForm` is UNKNOWN.  Under the first
form, the current finite-image checker can establish
`B4_A_LOCAL_PRESENTATION_NONIDENTITY` (or, after the semantic checks below,
`B4_A_LOCAL_TYPED_PENTAGON_FAIL`).  It must not emit `B4_A_ZERO_FIBER` by
itself.

## 7. Minimum terminal-A theorem/checklist

The following is the smallest sound contract for promoting one witness to a
zero-fiber A terminal.  Every item is required; a missing item is UNKNOWN.

### A. Window/type certificate

1. Give an explicit `N <= PB4`, prove `N normal in B4` and finite index, and
   bind the quotient map on the six PB4 generators.  Record the treatment of
   `Delta4^2` and prove that the K(0,5) quotient used by U_M is the stated
   PB4 quotient (or prove the exact kernel inclusion needed by B4-DIR).
2. Prove the induced PB3 subgroup is the fixed M/Q0, not merely an isomorphic
   group of the expected order.  Bind marked generators and the five A.18
   coface maps.
3. Prove isolatedness: either enumerate every M-shadow and show
   `ker(T)=M`, or prove the typed intersection theorem with isolated inputs
   (including the still-missing `N_S4` isolated certificate).  Require
   `settled_count=shadow_count`, not just `shadow_count=972`.

### B. Complete target and source ledger

4. Prove the candidate loop is a complete enumeration of `GT^heart(M)`:
   all m classes modulo `N_ord`, all F2 classes, charming/commutator condition,
   both hexagons, onto, and representative independence.  The 972 target
   digest is a binding check, not this proof.
5. For a zero-fiber claim, enumerate the relevant source `GT^heart(K)` rows
   for the declared refinement K and replay the exact reduction map
   `R_{K,M}`.  Check all source rows, all target keys, and the exact fibers;
   require the target key in the declared target set and in `zeroKeys`.
   If the claim ranges over every refinement, provide the cofinal family/theorem
   or a single finite K whose missing fiber is enough for the stated claim; do
   not infer cofinality from one 972 scan.  The phase-2 note explicitly keeps
   this finite-972-to-global step UNKNOWN (`d972_phase2_cofinal_execution_v1.md:1-4`,
   `:67-84`).

### C. Exact presentation/norm certificate

6. Pin the canonical source/relator/rho/roof/word-key digests listed in §1;
   reconstruct `j(x)=U1`, `j(y)=U4`, rho orbit/order, and all 158 relators
   independently.  A finite witness must pass every relator and rho gate.
7. Verify the witness word is exactly the target row's norm, not a substituted
   or factorwise word.  Bind the target key, m, F2 representative, and index.

### D. Pentagon bridge

8. Either (a) prove condition (I)/(3.10) for the witness and use
   `PENT-FORM` to identify `D` with (2.20), or (b) evaluate the unconditional
   `\widetilde D` and use `PENT-FORM'`.  Also check the A.18 orientation,
   `x51=x15`, rho direction, and the relevant PB4 quotient/kernel inclusion
   from B4-DIR.  A D-only witness outside S1 is not enough.

### E. Fiber/terminal gate

9. If the desired conclusion is only a finite non-survival witness, emit
   `B4_A_WITNESS_CROSSCHECKED` with the finite K/W and the failed target.
   Emit `B4_A_ZERO_FIBER` only after the complete source/fiber gates in B5,
   including isolatedness and independent producer/checker agreement.
10. State the scope exactly: a zero fiber proves that this target shadow is
    not genuine by Corollary 3.13 (the paper's `:3022-3029`), not that every
    shadow is non-genuine, not that `M` is globally cofinal, and not an Ihara
    non-arithmetic theorem.

## Final adjudication

The current universal lane has a sound and valuable finite-presentation
nonidentity route, but its JSON field `soundness` is stronger than the gates
actually established (`search/d972_b4_universal_v2.g:245-249`).  The exact
statement currently justified by a passing finite-image witness is:

> the pinned six-generator word is nontrivial in a checked finite quotient of
> the 158-relator presentation U_M.

After A1--A3 and D8 are supplied, this becomes a typed pentagon failure and,
with B5, a zero reduction fiber.  Until then the correct labels are
`UNKNOWN` for the isolated PB4 window, `UNKNOWN` for all-lifts completeness,
and `B4_A_LOCAL_PRESENTATION_NONIDENTITY` (or
`B4_A_LOCAL_TYPED_PENTAGON_FAIL` only when the defect bridge is explicitly
checked).  No current artifact justifies `B4_A_ZERO_FIBER` or a global
genuine/Ihara conclusion.
