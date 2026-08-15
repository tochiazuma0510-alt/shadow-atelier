# Luna task 152 — GHA DMTCP packaging repair and campaign continuation

## Authority and terminal condition

Researcher direct instruction: inspect GHA run `31902666498`, take over the execution side, and continue toward the 972-roof A/B decision. Partial mathematical results are not terminal. Sol retains the B-proof lane; Luna owns Linux execution, workflow/runtime repair, checkpoint/resume, and exact receipts.

Read `AGENTS.md`, `ops/inbox_codex/sol_task_152_pushback.txt`, `sol/sol_reply_152_pushback.md`, and the six d972 v2 files before acting.

## Observed failure

- workflow: `.github/workflows/d972-dovetail-v2.yml`
- run ID: `31902666498`
- source commit: `acfb39415a9eca599fcc3659c110a6ba2170276d`
- job: `95055698114`
- failed step: `Install and inventory GAP plus DMTCP`
- exact cause: Ubuntu 24.04 apt reports `Package 'dmtcp' has no installation candidate` and exits 100.
- no producer, checker, smoke test, checkpoint, or mathematical campaign ran; no predecessor artifact exists.

## Required work

1. Independently inspect the run/log and the frozen v2 contract.
2. Repair DMTCP provisioning reproducibly. Prefer the smallest robust change. Pin runner/release/source and integrity metadata as needed; do not silently weaken version, workflow-content, secret, smoke, or restart gates.
3. Update every affected manifest/hash/self-test binding. Do not leave a stale recorded SHA.
4. Run all locally possible static/self-tests. Audit YAML and every embedded Python/bash block.
5. Do not commit, push, or dispatch: AGENTS.md reserves credentials and GitHub mutations to the parent broker. Tell Sol exactly which files changed and their hashes; Sol will broker the commit/push/dispatch.
6. After the parent supplies the next run ID, monitor it, inspect artifacts, and continue repairing/resuming until either:
   - a fail-closed A receipt plus `final-v2-completion.json` is produced, or
   - execution is healthy and checkpointed as `UNKNOWN_RESUME`, in which case give the exact next dispatch parameters immediately.
7. Never infer B from timeout, cap, all-pass prefix, or nontermination.

## Worktree discipline

The worktree is heavily dirty with unrelated researcher files. Change only the d972 v2 files strictly required for this repair and your reply `sol/luna_reply_152_gha_repair.md`. Preserve every unrelated modification.

## Reply

Write a full receipt to `sol/luna_reply_152_gha_repair.md`, including commands, hashes, exact failure/repair logic, tests, and the requested next workflow dispatch.
