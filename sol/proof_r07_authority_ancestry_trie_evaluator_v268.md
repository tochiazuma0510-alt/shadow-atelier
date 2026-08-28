# R07 authority-ancestry trie evaluator v268

Author: Sol / 2026-08-29

Status: paper/interface theorem after task198, task330, and v267.  It proves
that the actual A4 consumer can re-evaluate all 6,441 authenticated
presentation rows in the ten first-successor contexts without scanning each
long row word independently.  The authenticated row ancestry reduces the
group-word work to two small, independently evaluable primitive-word DAGs.
No A4 kernel or anchor has been computed.  No lift, fake, or Ihara witness is
declared.  `verified=false`.

## 1. Authenticated row grammar

Task330 accepts the task198 authority bundle.  Its presentation has three
literal blocks

\[
  6{,}318\;\texttt{Gamma_Cayley}
  \; +\;104\;\texttt{action}
  \; +\;19\;\texttt{Q0_lift}
  \;=\;6{,}441.
\tag{1.1}
\]

Let \(s_i\) be the retained `section_word` of Gamma state \(i\), let
\(r_j\) be the retained word of record generator \(j\), and let \(q_k\) run
through the nineteen retained Q0 relator words.  There are respectively 243, 26, and 19 of
these words.  The task198 constructor and every authenticated row record the
following literal ancestry.

For a Gamma edge \(i\mathbin{\xrightarrow{j}}t(i,j)\),

\[
 w_{i,j}=\operatorname{red}\bigl(s_i r_j s_{t(i,j)}^{-1}\bigr).
\tag{1.2}
\]

For \(a\in\{x,y\}\), the two action orientations are

\[
 \begin{aligned}
 w_{j,a,+}&=\operatorname{red}
       \bigl(a^{-1}r_ja\,s_{t(j,a,+)}^{-1}\bigr),\\
 w_{j,a,-}&=\operatorname{red}
       \bigl(ar_ja^{-1}\,s_{t(j,a,-)}^{-1}\bigr).
 \end{aligned}
\tag{1.3}
\]

Finally

\[
 w_{k}^{Q}=\operatorname{red}\bigl(q_ks_{t(k)}^{-1}\bigr).
\tag{1.4}
\]

The accepted receipt binds every state, target, generator, orientation,
primitive word, reduced row word, ordinal, seven chunk digest, and the whole
row digest.  A consumer must still replay (1.2)--(1.4) as literal signed-word
equalities, but it need not discover any missing section.

## 2. One trie evaluates all primitive words

Let \(G\) be any one of the ten actual E3/E4 context groups, with marked
evaluation \(\rho:F(x,y)\to G\).  Form the finite primitive corpus

\[
 \mathcal W=\{s_i:1\le i\le243\}
 \cup\{r_j:1\le j\le26\}
 \cup\{q_k:1\le k\le19\}.
\tag{2.1}
\]

Construct its prefix trie.  Give the root value \(1_G\), and if an edge
labelled by the signed letter \(e\in\{x^{\pm1},y^{\pm1}\}\) joins a node
\(u\) to \(ue\), put

\[
 V(ue)=V(u)\rho(e).
\tag{2.2}
\]

### Theorem 2.1 (ANCESTRY-TRIE EXACTNESS)

For every terminal primitive word \(v\in\mathcal W\), the trie value is
exactly \(V(v)=\rho(v)\).  Substitution of these terminal values into
(1.2)--(1.4) gives exactly \(\rho(w)\) for every one of the 6,441 accepted
rows.  Hence applying the authenticated ten-to-eleven and seven-block bridge
to those values returns exactly the same actual typed first-successor defect
rows as independent full-word evaluation.

#### Proof

Induction on trie depth proves (2.2) equals marked word evaluation at every
node.  Group evaluation is invariant under free cancellation, so

\[
 \rho(\operatorname{red}(uv^{-1}))=\rho(u)\rho(v)^{-1}.
\tag{2.3}
\]

Equations (1.2)--(1.4) and (2.3) therefore give the claimed value in each
case.  The task198 bridge is an authenticated deterministic function of the
ten values, so equal ten-tuples give equal eleven-occurrence and seven-block
rows. \(\square\)

This is not reuse of a producer's claimed defect vector.  It is a fresh group
evaluation of all literal primitive words, followed by a theorem-equivalent
factorization of every authenticated row word.

## 3. Independent reverse evaluator

A helper-nonshared checker need not repeat the prefix algorithm.  Build the
suffix trie obtained by reading each word in \(\mathcal W\) from right to
left.  Put \(W(\varnothing)=1_G\) and

\[
 W(eu)=\rho(e)W(u).
\tag{3.1}
\]

Induction from the right proves \(W(v)=\rho(v)\).  The checker then assembles
the same rows by (1.2)--(1.4), but in right-associated multiplication order,
and independently applies its own bridge glue.  It compares all 6,441 typed
rows, not only their ranks or a final digest.  Thus the two routes have
opposite trie orientation and opposite association order while sharing only
the authenticated mathematical input.

Direct full-word evaluation of a bounded deterministic sample and of every
newly materialized K/anchor word remains a useful canary.  It is not necessary
to rescan all 6,441 long presentation words after the two complete trie
replays agree and every literal ancestry equality (1.2)--(1.4) has been
checked.

## 4. Exact authority-bound work inventory

A read-only scan of the accepted receipt

```text
ci/in/d972_r07_seven_context_roof_presentation_v1.json
bytes  31,017,244
sha256 82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5
```

gives the following deterministic inventory.

| corpus | words | literal letters | prefix edges | suffix edges |
|---|---:|---:|---:|---:|
| Gamma sections | 243 | 106,872 | — | — |
| record words | 26 | 3,054 | — | — |
| Q0 relators | 19 | 4,532 | — | — |
| combined primitive corpus | 288 | 114,458 | 15,970 | 26,136 |

The 6,441 stored reduced row words contain 5,475,488 letters in total:

```text
Gamma_Cayley  5,433,366
action           33,206
Q0_lift           8,916
```

After primitive evaluation, row assembly requires at most

\[
 2(6{,}318)+3(104)+19=12{,}967
\tag{4.1}
\]

tuple multiplications, plus cached inverses.  Thus the producer uses at most
\(15{,}970+12{,}967=28{,}937\) ten-context tuple multiplications, and the
independent suffix checker at most
\(26{,}136+12{,}967=39{,}103\), before boundary and K closure work.  In
component-operation units these bounds are 289,370 and 391,030.  They replace
54,754,880 separate component letter steps from ten naive full-row scans.

The counts are reproduced by: parse the pinned receipt once; deduplicate
`section_source_word`/`section_target_word` by state id and `record_word` by
generator id; retain the nineteen `q0_relator_word` arrays; sum literal
lengths; then insert the 288 arrays into forward and reversed tries, counting
one new `(node,signed-letter)` edge.  No group computation is used in this
inventory.

The row arrays still must be streamed once for canonical authority, ordinal,
ancestry, reduction, and digest checks.  The speedup removes repeated
**group operations**, not proof obligations or input authentication.

## 5. A4 implementation consequence

V267's local evaluator can therefore be implemented with the following
strict division.

1. Authenticate the task330-accepted bundle and parse its one row roster.
2. Check every row against (1.2)--(1.4), its layer-local ordinal, and its
   bound chunk/whole-row digests.
3. Producer: evaluate the 288 primitive words by the prefix trie; checker:
   evaluate them by the suffix trie.
4. Assemble all 6,441 actual ten-context values and bridge them to typed
   first-successor rows.
5. Continue the coefficient-bearing invariant closure and complete boundary
   oracle of v267/task328.
6. Directly evaluate every **new** materialized K basis and v247 anchor word
   in the actual local group, since those words are not members of the
   authenticated task198 grammar.

No full Q0 enumeration, arbitrary Q0 source-section lookup, 6,441 independent
long-word scans, or second parsed authority roster is required.  A mismatch
in any literal ancestry equality, trie value, producer/checker row, bridge
row, or direct new-word replay is fatal; a resource cap gives only UNKNOWN.

```text
TASK198 AUTHORITY INPUT:                         PASS / A4 1/3 (task330)
6441 FULL LONG-WORD GROUP SCANS REQUIRED:        NO (PAPER PROOF)
PREFIX/SUFFIX HELPER-NONSHARED REPLAY:           PAPER CONSTRUCTION
ACTUAL TRIE IMPLEMENTATION / SELFTEST:           PENDING
ACTUAL A4 KERNEL / ANCHOR:                       NOT COMPUTED
LIFT / FAKE / IHARA:                             NONE
```

`R07_AUTHORITY_ANCESTRY_TRIE_EVALUATOR_V268_PAPER_GRADE`
