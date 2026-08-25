# Luna task 163: R07 g760 L3 full-legal target6 gate v1

Date: 2026-08-26
Role: Luna mechanical implementation/cross-check only
Requested reply: `sol/luna_reply_163_r07_760_l3_target6_v1.md`

## 1. Objective

Retarget the cross-checked C-13/L3 nonmembership machinery from its historical
20-letter base to the exact new commutator base

\[
g_{760}=w_2(w_3^{-1}w_2)^8y^{36}x^{-108}.
\]

Test the first literal hexagon coordinate (`target6`, frozen name
`hexagon_1_coface_0`) against the sum of

1. the complete C-13 legal-correction over-approximation
   \(\Sigma_g(K^{(31)}_{E_4})\), rebuilt with the **g760 prefix action**; and
2. the full translated PB4 presentation-boundary image
   \(\operatorname{im}D_2^{\rm full}\).

This is a fast fatal/survival gate for the explicit base.  It is not the
literal five-coface A.18 computation and it is not a registered-108-family
scan.  A proved nonmembership kills this explicit prefix at this edge; a
membership result is only inconclusive and sends the branch onward to the
actual normalized Brunnian/A.18 class.

Do not run a heavy local Python/GAP computation.  Implement and run only
bounded source self-tests locally, serially.  Prepare one fail-closed GHA
driver for the full producer followed by the structurally independent direct
enumeration checker.  The parent Sol session alone commits, pushes and
dispatches GHA.

## 2. Frozen mathematical statement

Use the exact conventions already cross-checked in C-13.  Put

\[
A=g_{760}(X_0,Y_0),\qquad B=g_{760}(X_0,Z_0),\qquad
C=g_{760}(Y_0,Z_0)
\]

with the frozen signed words

```text
X0 = [4]
Y0 = [6]
Z0 = [-4,-6]
```

and use the target word

\[
b_6(g_{760})=CB^{-1}A.
\]

Its left-Fox gradient is \(\nabla b_6(g_{760})\).  Let
\(\pi:E_4\twoheadrightarrow\Pi_4[3]\), let \(I\) be the augmentation
ideal of \(\mathbf F_3[\Pi_4[3]]\), and for each preregistered
\(2\le j\le J_{\max}\) compute membership of

\[
\pi_*\nabla b_6(g_{760})
\quad\text{in}\quad
\pi_*\Sigma_g(K^{(31)}_{E_4})+
\pi_*\operatorname{im}D_2^{\rm full}
\pmod {I^j}.
\tag{2.1}
\]

Here \(\Sigma_g\) is base-dependent: every prefix transport and every
`F-node` value must be recomputed with g760.  The historical C-13 space,
target gradient, rank constants and separator must not be imported as the
answer.  The PB4 relator roster and E4 quotient are base-independent but
must still be authenticated and independently reconstructed.

The sound negative implication to record is only

\[
\pi_*\nabla b_6(g_{760})\notin
\pi_*\Sigma_g(K^{(31)}_{E_4})+
\pi_*\operatorname{im}D_2^{\rm full}\pmod {I^j}
\Longrightarrow
\nabla b_6(g_{760})\notin
\Sigma_g(C_{\rm legal})+\operatorname{im}D_2^{\rm full}.
\tag{2.2}
\]

The two enlargements must be displayed: projection to the L3 quotient and
replacement of the literal legal-word image by the C-13 full-K
over-approximation.  Both are safe only in the nonmembership direction.
Membership in (2.1) is not a lift.

## 3. Required sources and pins

Read and authenticate in full before implementation:

- `provenance/CLAIMS.md`, entries C-12 and C-13, including the later Sol
  boundary corrections;
- `docs/対話帳.md`, T-64 through T-66;
- `sol/proof_r07_joint_derived_commutator_rebase_v92.md`;
- `sol/audit_r07_uniform_explicit_lift_checkpoint_v95.md`;
- `sol/luna_task_162_r07_760_commutator_affine_rhs_v3.md`;
- `sol/luna_reply_162_r07_760_commutator_affine_rhs_v3.md`;
- `search/certs/d972_r07_616_to_760_commutator_affine_rhs_preflight_v3_20260826.json`;
- `search/koubou158_L3_radical_v1_2.py` and its frozen core;
- `crosscheck/check_koubou158_L3_radical_v1.py`;
- the C-13 producer/checker receipts named in `provenance/CLAIMS.md`.

Reconstruct g760 from the pinned 616 parent and the literal tail.  Require

```text
length                  760
signed-list SHA-256     518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
free exponent sums      [0,0]
parent-616 SHA-256      3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90
```

The immutable implementation base is parent commit
`f3698fffd3b73370f753c4b0d9eb1e86751b1159`.  Pin exact source SHA/bytes
in the new driver.  Do not pin a mutable reply into a digest cycle.

## 4. Producer implementation

Create a new versioned producer.  It may reuse the frozen C-13 producer
algorithm after authenticating it, but it must make all base-dependent
objects fresh:

1. g760 and the exact target word \(CB^{-1}A\);
2. its raw E4 Fox gradient and projected L3/Jennings rows;
3. every \(\Sigma_g\) correction row, including the base prefix factor
   `fbar_xz * fbar_yz^-1` in the frozen convention;
4. the complete legal-overapproximation ledger and its proof that the
   Schreier generating set spans the full C-13 \(K^{(31)}\) image;
5. the full PB4 \(D_2\) orbit closure at each tested \(j\);
6. fresh ranks, membership results, and a lossless separator whenever the
   target is outside.

Do not require the historical ranks 310/314/4.  Record them only as an
old-base comparison diagnostic.  A changed rank is permitted and is data.
The first-terminal rule and \(j\)-order must be preregistered.  Directly
verify every reported separator annihilates every generated correction and
boundary row and pairs nontrivially with the fresh target.

## 5. Independent checker

Create a checker which imports no new producer helper and does not accept a
serialized rank/membership boolean.  Follow the structurally independent
C-13 checker route:

- independently reconstruct the E4/PC arithmetic, Jennings basis and g760;
- reconstruct the C-13 Schreier/legal-overapproximation rows with an
  independently written expression path;
- enumerate all \(3^{10}=59049\) elements of \(\Pi_4[3]\) directly and all
  eleven PB4 relator translates (649,539 raw translated columns), rather
  than using the producer's BFS orbit-closure algorithm;
- recompute every rank and target reduction;
- replay the complete separator pairing, not merely its digest;
- compare the producer receipt only after the independent answer exists.

The checker may reuse frozen utilities which predate both new files only if
their exact path/SHA/bytes and their role are declared.  It must not import
`search/koubou158_L3_radical_v1_2.py`, its new successor, or any result
certificate as an input to the computation.

## 6. Exclusive terminals and claim boundary

Use exactly one terminal:

```text
R07_760_L3_TARGET6_NONMEMBER
R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE
R07_760_L3_TARGET6_UNKNOWN_RESOURCE
R07_760_L3_TARGET6_INPUT_STOP
```

`NONMEMBER` is admissible only with producer/checker agreement and the full
pairing replay described above.  Its meaning is: this **one explicit g760
prefix** cannot pass the first hexagon coordinate through this actual edge,
even after enlarging to the complete C-13 legal correction overapproximation
and full D2 boundary image.  It is not a statement about all bases, all 972
rows, fake shadows, or Ihara.

`MEMBER_INCONCLUSIVE` means only that the L3 screen did not kill the branch.
It does not provide coefficients at E4, does not solve target6, and does not
construct literal A.18.  RESOURCE and INPUT carry no mathematical claim.

Every receipt must set the following false:

```text
actual_A18_occurrence
normalized_Brunnian_class
compatible_cofinal_lift
ihara_witness
all_bases_obstruction
```

## 7. Destructive tests

At minimum reject these production-shaped mutations at distinct gates:

1. one sign in the tail `y^36*x^-108`;
2. base SHA changed while recomputed values are left untouched;
3. `C*B^-1*A` changed to either `C*B*A` or `A*B^-1*C`;
4. the prefix action changed to its inverse;
5. one PB4 relator coefficient/translation changed;
6. one Jennings projection coordinate changed;
7. one legal-overapproximation row omitted;
8. a forged separator which annihilates rows but also annihilates the
   target, or which pairs with the target but misses one row;
9. historical old20 target/rank data substituted for the fresh g760 data.

The bounded self-test must exercise both positive and negative toy
membership cases without enumerating the production 649,539 columns.

## 8. Authorized new files and GHA contract

Create only new versioned files in the following roles (choose these exact
names unless a version suffix is required to avoid an existing file):

```text
search/d972_r07_760_l3_target6_v1.py
crosscheck/check_d972_r07_760_l3_target6_v1.py
search/d972_r07_760_l3_target6_gha_driver_v1.g
search/certs/d972_r07_760_l3_target6_preflight_v1_20260826.json
sol/luna_reply_163_r07_760_l3_target6_v1.md
```

The GAP driver is an ASCII-only shell.  It authenticates all pins, accepts
exactly one selftest/full mode, deletes only its own stale output names, and
runs producer then checker serially under explicit shared limits.  It must
bind receipt SHA/bytes and exact terminal-marker counts fail-closed.  Heavy
full mode is GHA-only.  Report exact dispatch bindings, timeout expectation,
memory expectation and success markers.  Do not alter workflows, run git,
dispatch GHA, or edit the Sol reply.

Nothing in this task is Lean-verified.
