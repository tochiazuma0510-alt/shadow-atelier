# Luna reply 515 — A4 positive forbidden-schema repair

Created: search/d972_r07_word_independent_successor_kernel_gha_driver_v46.g

Exact output bytes: 12544

SHA-256: d3a864e47ebe0255221ccafee15b09925b2e1e462b21d8d0158c2d9c9e0f97e7

Diff accounting: v46 preserves v45 byte-for-byte except for exactly two
positive-terminal predicate lines: producer PASS and checker PASS now require
the exact five-key false dictionary {lift:false,fake:false,Ihara:false,base_pairs:false,ambient_E3_E4_enumeration:false}.
Producer/checker RESOURCE predicates retain the exact three-key dictionary
{lift:false,fake:false,Ihara:false}. No other driver content changed.

Checks:

- GAP 4.16.0 ReadAsFunction parse-only: PASS; only expected unbound-global
  syntax warnings were emitted.
- Generated-shell bash -n: not run, because the driver was not exercised
  (running it would enter production traversal).
- Production traversal, GHA, git, and workflow actions: not run.
