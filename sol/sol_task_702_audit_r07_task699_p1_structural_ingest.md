# Sol(max) Task702 — Task699 P1 structural-ingest code audit

Audit the current `search/d972_r07_grade2_specific_owner_prejoin_v1.py` at
Task699 SHA and the complete Task699 reply against Tasks647, 691, 698 and paper
v480/v481.

This is a bounded code/receipt audit.  Do not repeat the 1.7-GiB-RSS all-five
JSON replay and do not request generic hardening.  Static inspection, canonical
body/HEAD metadata reads, small fixtures and direct inspection of the compact
basis blobs are allowed if useful.

Decide exactly:

1. all four block roots/envelopes/body pins/parent/character/packet/rank/
   attempts/FIFO/actor-order/false-claim/typed-blob gates are live production
   gates;
2. all origin, actor, DAG, lead/scale/origin and strict-prior expressions are
   completely traversed with plain types and canonical DAG digest;
3. the same bytes used for each actual local lead are full-range/count/SHA/
   stable-identity bound, and all 6,045 rows are checked against declared lead
   and coefficient one;
4. v481 is applied with the exact old 2,014 summary, disjoint intervals and a
   shared global summarizer to justify 8,059 distinct normalized leads/rank;
5. only one large block object/one row is retained as claimed, and no dense
   family, Task640 join, precision-two computation or semantic equality is
   falsely declared.

Return `PASS_P1_STRUCTURAL_PRODUCER` or exact finite blockers.  A PASS still
does not replace the independent checker or the 44+4*8059 equality replay.
Write only `sol/sol_reply_702_audit_r07_task699_p1_structural_ingest.md` with
exact hashes and `verified=false`; edit/run/commit/GHA nothing else.
