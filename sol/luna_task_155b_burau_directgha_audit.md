# Luna task 155b — independent static audit of direct GHA lane

Audit `.github/workflows/d972-burau-direct-v1.yml` adversarially against
`sol/luna_task_155_burau_directgha.md` and the actual public interface/markers
of `search/d972_b4_burau_fiber_v2.g`.

Write only `sol/luna_reply_155b_burau_directgha_audit.md`.  Do not edit the
workflow or any producer/checker, run local GAP, commit, push, or dispatch.

At minimum check:

1. closed workflow inputs and least privileges;
   verify the exact-branch push trigger, dynamic two-lane a=2/4 matrix, and
   strict selftest-before-full control flow (a failing selftest cannot reach
   full); also check that manual dispatch does not duplicate matrix lanes;
2. all three official URLs/SHA256 bindings and archive-layout handling;
3. GAP core build/root selection, required GAPDoc discovery, and JSON build
   against the same exact GAP 4.16.0 root;
4. generated driver variable names/modes/output and actual producer marker
   strings;
5. preservation of GAP exit status through `tee`, syntax/error rejection,
   exact marker cardinality, full-receipt JSON gates, and no producer/workflow
   self-promotion;
6. artifact-on-failure behavior and YAML/shell syntax;
7. any blocker/high issue that could prevent the script from running or could
   create a false A/B result.

Use read-only/static checks only.  Return PASS or FAIL, prioritized findings
with exact line references, and the workflow SHA256 you audited.
