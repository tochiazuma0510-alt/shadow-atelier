# Task932 — bounded seed30 release audit

Role: independent mathematical/code auditor; no implementation or execution.
Read this full task and reply only to
`sol/sol_reply_932_audit_r07_seed30_release.md`.

1. Audit the frozen actual seed30 producer and independent checker:
   `search/d972_r07_actual_seed30_materializer_v1.py` (79651 bytes,
   SHA256 3ce9293e05f06bf343bd2a54af0ab84ae67f4b922a428cd3c73e38944d6de55c),
   `search/check_d972_r07_actual_seed30_materializer_v1.py` (62048 bytes,
   SHA256 f4f8ba2d342cb60e2c70b708b8847768a78ebde40dd0a52879f460cb558eab36).
   Read completed replies929/930 and task927 section5 / task928 for scope.
2. Focus only on actual release blockers: raw SeedRed30 order and full lower
   subtraction before projecting, selected support902, local P1 reduction
   index bases, B/pairings, insertion-order physical reduction and one saved
   target-remainder update, next separator/member-candidate distinction,
   independent checker agreement. Old fixed parent derivations are accepted
   premises, not subjects for a repeated historical audit.
3. Flag an avoidable major performance/memory trap if actually reachable.
   Do not request a generic resume engine, parent re-derivation, all-origin
   sweep, new actor anchor, paper adapter, or cosmetic tests. No local
   Python/GAP, no git or network mutation. Root reviews workflow and runs
   finite canaries plus actual arithmetic on GHA.
4. Return a short PASS/FAIL with exact locations and necessary fixes only.
   The seed30 scalar parent has workshop2096's limited cross-checked scope;
   do not claim stronger independence or promote full A0/verified status.
   This is a single-pivot delta, not a full grade2 membership proof.
