# Task683 reply

The single producer defect is repaired: the first-six prefix comparison now
uses the authenticated Context field `physical_shifts`. The equality is
factored into `first_six_shift_gate`, shared by production and a live fixture
whose object has `physical_shifts` and no `shifts`; its one-entry mutation is
rejected.

The inert v7 workflow is a mechanical copy of released v6 with only v7
name/self-path/fire/artifact labels, the repaired producer SHA pin, and the
required `${{ false && (...) }}` job condition. All action pins, paths, caps,
downloads, copies, timeouts, uploads, and the checker SHA remain unchanged.
Both canonical and replayed Task625 verdict copies remain after successful
`cmp`.

Bounded results:

- serial `py_compile`: PASS;
- producer selftest: PASS, `first_six_shift_mutations=1`;
- checker selftest: PASS, `mutation_count=43`;
- safe YAML parse: PASS;
- producer context census: `aggregate_table`, `physical_shifts`, and
  `source_word_tags`, all present on the real grade1 Context;
- normalized v6-to-v7 comparison: PASS;
- immutable action-pin and inert-condition scans: PASS;
- post-`cmp` two-verdict-copy scan: PASS.

No parent replay or rho2 computation was run. Candidate only,
`verified=false`; no rho2, A0, fake, or Ihara claim is made. No git or GHA was
used.

READY_FOR_SOL_CONTEXT_AUDIT
