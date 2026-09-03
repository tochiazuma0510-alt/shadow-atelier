# Luna Task621: four finite Task620 release repairs

Role: Luna implementation.  Read the full Task620 reply
`sol/sol_reply_620_audit_r07_task601_packed_memory_release_v2.md`
(`3741a8027cf73e04ea865a20dcb070b7d2f92d1b419aaedbdd15df998969552d`).
Make exactly the four finite repairs below.  This is not permission for a
redesign or any additional optimization.

Edit only the same four Task601 files:

1. `search/d972_r07_a0_grade1_selected_slp_v1.py`;
2. `search/check_d972_r07_a0_grade1_selected_slp_v1.py`;
3. `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml`;
4. `sol/luna_reply_601_r07_grade1_selected_slp_v1.md`.

## Mandatory repairs

1. In producer `append_row`, keep the exact length and canonical packed-byte
   `<=80` gates, but replace the Python generator byte scan by one bounded
   NumPy/C-level scan over its existing memoryview.  Do not add a row copy.
2. In checker `validate_physical_streams`, replay the lower recurrence before
   the standalone router only for `declared_lower` pivots.  Least closure
   already contains every dependency of those pivots.  Keep the one full
   receipt canonicality scan and keep the later standalone all-8,059 online
   reroute, which still reconstructs every accepted lower row.  Reuse the
   already constructed `physical["basis"]` `RowView` inside the independent
   final basis comparison; do not construct or scan a second basis view.
3. Add one tiny checker selftest which deliberately leaves at least one
   authenticated node/edge/row cursor unconsumed, calls `finish()`, and
   requires `authoritative_cursor_exhaustion`.  Keep the existing content
   mismatch fixture.
4. Add negative forbidden-state fixtures through the production predicates:
   mutate the compact leaf header's `states_exported` byte from zero to one
   and require rejection; inject a `states` member into derived metadata and
   require rejection by the same validation boundary used in production (a
   small factored predicate is acceptable).  Do not build a new fixture
   framework.

Nothing else changes: all mathematics, 8,059 offers, counts/ranks, 3,317
coefficients, receipts, compact leaf format, character-wise lifetimes, exact
online cursors, basis/MEMBER checks, false/null claims, resource limits and
`[fire-grade1-selected-slp-v2]` marker stay fixed.

Run only serial `py_compile`, the two selftests, YAML parse and exact workflow
pin inspection.  Do not run the real route, production, GHA or mutating git.
Refresh the producer/checker/reply SHA pins after the quartet is stable and
update the Task601 reply truthfully.  Report final bytes/lines/SHA and test
outputs to root.  The same Sol(max) Task620 audit must pass before launch.
