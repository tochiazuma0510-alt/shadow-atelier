# Luna task 157cj — C2^24 fast lossless witness construction

## Role and scope

You are Luna. Diagnose and replace the bottleneck in the currently running
GHA run 32065265291 (commit c68df71c), whose full step spends hours in 24
calls to `PreImagesRepresentative` on the full joint permutation image in
`search/d972_d972core_c2six_intersection_v1.g:378-415`.

Do not run GAP locally. The user has prohibited concurrent local GAP jobs.
Do not use git, push, workflow dispatch, or credentials. Parent Sol is the
only broker.

## Objective

Prepare a mathematically exact, fail-closed v2 producer/checker/workflow that
constructs the same 24 lossless source words much faster, without building or
solving preimages in the full enormous `E^4 x H9` image for each target.

Preferred route to examine:

1. exploit solvability/derived length of `H9 <= G9^4` to make explicit source
   derived words whose H9 image is exactly identity;
2. retain pure-coordinate control in `E^4`;
3. solve word preimages coordinatewise in `E` (order 32256), or in another
   rigorously bounded small image, then replay the resulting signed source
   words in all E/P/G9 coordinates;
4. certify the same 24 distinct V^4 basis targets and rank 24.

You may choose a different construction if it is exact and demonstrably
smaller. Do not rely on the abstract Goursat existence argument in place of
actual lossless source words. Do not weaken any v1 hash, source, map,
independent replay, mutation, timeout, or terminal-status gate.

## Required outputs

Only create/modify these new versioned files:

- `search/d972_d972core_c2six_intersection_v2.g`
- `search/check_d972_d972core_c2six_intersection_v2.py`
- `.github/workflows/d972-d972core-c2six-intersection-v2.yml`
- `sol/luna_reply_157cj_c2_24_fast_witness.md`

The v2 workflow must be manual-dispatch capable and path-trigger only its own
frozen files/inputs. It must use GAP 4.16.0, exact SHA bindings, a materially
shorter bounded timeout, upload logs/receipt on every outcome, and report
UNKNOWN on timeout rather than a mathematical conclusion.

Run only Python/checker/static selftests that do not invoke GAP. Report exact
hashes and the expected GHA command. If a sound fast construction cannot be
completed from the frozen data, write an exact BLOCKED analysis instead of a
speculative implementation.
