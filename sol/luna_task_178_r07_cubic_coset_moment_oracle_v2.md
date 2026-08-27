# Luna task 178 — R07 cubic/coset moment oracle v2

Commissioner: Sol / 2026-08-27

Role: Luna implementation and independent-checker work only.  Do not change
the mathematics or widen the registered R07 universe.

## 1. Objective

Implement a versioned, bounded SELFTEST for the exact combination

\[
 \text{v134 cubic moment}
 +\text{v136 resource caps}
 +\text{v137 coarse-}C_i\text{-coset anchor oracle}.
\]

Task177 v1 tested weighted Boolean cells, but its toy coarse Gamma image was
too simple.  V2 must make \(C_i=c_i\Phi_i(\Gamma)\) nontrivial and must reject
the unsound replacement of a thick \(C_i\)-coset bucket by literal coarse
equality.

Production remains fail-closed until positive task175 and task176 run IDs,
head SHAs, receipt hashes, and checker-verdict hashes are registered by the
parent.  Do not emit a common word, separator, cofinal lift, fake, or Ihara
claim from an unpinned input.

## 2. Authorized new files only

- `search/d972_r07_cubic_coset_moment_oracle_v2.py`
- `crosscheck/check_d972_r07_cubic_coset_moment_oracle_v2.py`
- `search/d972_r07_cubic_coset_moment_oracle_gha_driver_v2.g`
- `search/certs/d972_r07_cubic_coset_moment_oracle_selftest_v2_20260827.json`
- `sol/luna_reply_178_r07_cubic_coset_moment_oracle_v2.md`

Do not modify task177 v1.  Do not run local Python, Node, GAP, or git.  The
parent will audit, commit, push, and dispatch GHA.

## 3. Pinned theorem inputs

Pin exact bytes and SHA-256 for:

- v134 `sol/proof_r07_cubic_character_moment_selector_v134.md`;
- v136 `sol/proof_r07_cubic_moment_exact_resource_cap_v136.md`;
- v137 `sol/proof_r07_coarse_anchor_multi_projection_oracle_v137.md`;
- task177 v1 producer/checker/fixture/driver; and
- the task178 instruction itself.

Any pin drift is `UNKNOWN_INPUT`, never SELFTEST PASS.

## 4. Required noncommutative fixture

Use \(G=D_6=C_3\rtimes C_2\), with rotation \(r\), reflection \(s\),
\(srs=r^{-1}\),

\[
 1\to\Gamma=\langle r\rangle\to G\to Q=C_2\to1,
 \qquad s(0)=1,\ s(1)=s.
\]

Use at least two linked coordinates.  A canonical choice is

\[
 \Phi_0(g)=g,
 \qquad \Phi_1(g)=\alpha(g),
 \quad \alpha(r)=r^{-1},\ \alpha(s)=s.
\]

Take the coarse maps to be the literal D6 values, so

\[
 C_0=C_1=C_3
\]

is nontrivial.  The simultaneous Gamma image is the graph

\[
 A_{01}=\{(r^j,r^{-j}):j\in\mathbf F_3\},
\]

not \(C_3\times C_3\).  Producer and checker must demonstrate
noncommutativity and linked-graph strictness by direct operations.

Include a target whose anchor coarse value differs literally from the
section coarse value but lies in the same left \(C_i\)-coset.  The thick
bucket

\[
 B_i(u)=\{q:u\,b_i(q)^{-1}\in C_i\}
\]

must find it, while a literal-equality bucket must miss it and be rejected.
Return a source word \(u_\gamma u_{s(q)}\), replay both coordinates, and
check the fibre order by v137 (4.2).

## 5. Exact cubic moment

Build a weighted \(\mathbf F_3\) test row with:

- same-target cancellation before merge;
- two linked coordinates;
- a nonzero constant \(K\) in at least one case;
- one positive ACTIVE case; and
- one all-zero negative control.

Represent \(A+B\omega\) as signed integer pair `(A,B)` and implement only
the exact law

\[
 (A,B)(C,D)=(AC-BD,AD+BC-BD).
\]

Rebuild v134 (3.3) from partial target tuples via the thick coset oracle.
Compare the result with a direct six-element D6 enumeration, then recover
\((n_0,n_1,n_2)\) by v134 (2.5).  Require integral, nonnegative counts with
sum six.  The negative control is accepted only at `(A,B)=(6,0)`.

Apply v136-style counters to the toy arity and expose checked signed-64
guards even though Python integers are unbounded.

## 6. Independent checker

The checker must not import the producer, task177 implementation, or any
producer helper.  Use a distinct representation, preferably permutations of
three points for D6.  Independently rebuild:

- Gamma, Q section, both coordinate maps, `C_i`, and linked `A_S`;
- left coset canonicalization and bucket membership;
- residual side/order and source word;
- partial-fibre membership and kernel orders;
- exact Eisenstein arithmetic and recovered value counts; and
- direct enumeration equality.

No whole-fixture equality or self-digest-only oracle is sufficient.

## 7. Semantic mutations

Pass every mutation through the normal producer/checker semantic validator.
At minimum reject these 14 cases:

1. same-target merge cancellation;
2. `C_i` falsely replaced by the identity;
3. thick coset bucket replaced by literal equality;
4. left/right residual order swap;
5. wrong anchor bucket state;
6. different Gamma states chosen in the two coordinates;
7. wrong `A_S` graph orientation;
8. wrong kernel order;
9. one partial target membership bit;
10. one `omega^c-1` pair;
11. one Eisenstein multiplication coordinate;
12. constant `K`;
13. one recovered `n_j`; and
14. word-bearing section/Gamma concatenation.

Mutation cancellation is a hard SELFTEST failure.  Report attempted and
rejected counts separately.

## 8. Production seal and resources

Include outside-repository fixed-width/mmap primitives for a future index

```text
(coordinate, canonical C_i-coset key) -> ordered Q0 state IDs
```

and typed cache keys for `(ordered subset, complete target tuple)`.  Do not
materialize any repository-local large table.  Production mode must return
exactly

```text
UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED
```

until the parent version-registers both positive prerequisite receipts.
Registered caps must convert incomplete bucket/index/moment work to
`UNKNOWN_RESOURCE`, never to zero correlation.

## 9. Driver contract

Use an externally bound quote-free mode variable, producer then checker
strictly serial, exact stage files, source/fixture/proof pins, clean-log
gates, terminal agreement, and lossless external `printf '%s\n'` final
sentinel.  Reject literal backslash-newline in the generated shell.  Test
both SELFTEST and the typed sealed PRODUCTION envelope after the parent
commits the bundle.

Expected SELFTEST terminal shape:

```text
R07_CUBIC_COSET_MOMENT_ORACLE_V2_PRODUCER_SELFTEST_PASS mutations=14 rejected=14 gamma_coarse_order=3 linked_graph_order=3
R07_CUBIC_COSET_MOMENT_ORACLE_V2_CHECKER_SELFTEST_PASS mutations=14 rejected=14 gamma_coarse_order=3 linked_graph_order=3
R07_CUBIC_COSET_MOMENT_ORACLE_V2_GHA_DRIVER_PASS mode=SELFTEST terminal=FIXTURE_PASS
```

## 10. Reply

Report exact files, bytes, SHA-256 values, static helper-nonsharing audit,
all registered mutations, mode preambles, exact expected lines, and honest
boundaries.  State explicitly that local execution was not performed and
that actual R07 production/common word remains pending.
