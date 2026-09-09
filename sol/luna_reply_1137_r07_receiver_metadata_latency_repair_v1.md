Luna Task1137: minimal NoReparse latency repair completed for root review.

The final fail-closed helper takes 0.1612241 / 0.1579373 seconds against baseline 0.7170711 / 0.6815554 seconds on the same 64 preregistered actual inventory paths (818 ancestor visits per trial): total wall ratio 4.3822. This measures the helper, not full reception ETA. Final benchmark native exit 0, chunk 07abf1; PowerShell 5.1.19041.6456 / Framework 4.0.30319.42000. Result: `%TEMP%/shadow-atelier-audit163/task1137/no-reparse-benchmark-v2.json`, 1838 B / 19bf146bbb0ed58b120f6c3a3458dcbf326095fd2161212a48d3c18f0c22d076. The timed script loads the final 559 B helper verbatim; v1's provider-fallback prototype is not the adopted candidate.

Candidate base: `%TEMP%/shadow-atelier-audit163/task1137/review-snapshot-v1/`.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| receiver/root-review-receiver-v5-directory-stability-attributes-v6.ps1 | 527401 | 6a8e1a516365e2d32a0da232452ba0bbad8b15d05ad306087aefd25a61aaf7ec |
| preflight74/authenticated-empty-directory-preflight-attributes-v2.ps1 | 48246 | 95651f413ed0181c4b04437cce6e37f3752254d81bfab8ef90b82e841290c9a8 |
| root-directory-stability-broker-attributes-v6.ps1 | 18571 | 426b79a03913602b2ace8b262c062615488ad1c9cafd6b8b5d9ca98bbad4ebc7 |
| proposal-runtime-closure-v1.json | 3911 | f4b2a556b15aedd857dcdf2e571976439c7a0a951144c51a63b12c5f753d7df6 |

Receiver baseline R198-205 and old74 R86-93 contain identical 401-byte NoReparse bodies. Each is replaced by the same 558-byte body (559 B standalone including final LF), preserving all prefix/suffix bytes. Broker changes only two receiver and three old74 path literals. Closure remains 14 members; 12 are byte-identical. Forward/reverse raw joins: `task1137/core-source-raw-joins-v1.json`, 11946 B / 8d8b42748dd4c58ad476aa5f3e8df0c4a2b3b84f39e0cd37c29e559da08fe356.

The common guard still walks every ancestor in GetFullPath/GetDirectoryName order. A successful first GetAttributes establishes presence; the second fresh GetAttributes supplies the reparse flag. First-read FileNotFound/DirectoryNotFound mean absence of that node only, so remaining ancestors are still checked. All other first-read errors and every second-read error propagate; there is no provider retry or attribute cache. For stable ordinary filesystem paths with successful or missing-node observations, this retains the existing-node reparse gate. Provider exception compatibility and arbitrary concurrent-mutation timing equivalence are not claimed. All direct callers are retained verbatim: receiver baseline R145/207/311/692/1001/1075/1878/2103/4149; old74 R118/145/160/196/221/381/408/427/433/439. Their path containment, existence/hash checks, inventories, leases/finally and final typed checks remain unchanged, as do cost-v5, JSON type/value rules and earlier empty-keyset repairs.

Thirteen bounded controls match: ordinary file/directory, missing leaf/ancestor, file used as ancestor, invalid control character, trailing dot/space, junction at leaf/ancestor/above a missing descendant, and the same missing path before/after later junction creation. Native exit 0, chunk c3e8f1; result `task1137/no-reparse-essential-controls-v2.json`, 12826 B / d04202b2e9c3a19bfcc10e970a7c1034b0e389379fab7e55a30865a9e6615929. AccessDenied was not induced; rejection rests on the uncaught-error branch, not an empirical compatibility claim. Harness v1 failed before the first control because Compare resolved to Compare-Object (exit 1, chunk ddbabb); v2 only renames the harness function and fixture/output IDs. The failed harness and registration remain preserved.

Reproduce the bounded helper benchmark with `& "$env:TEMP/shadow-atelier-audit163/task1137/benchmark-no-reparse-v2.ps1" -TaskRoot "$env:TEMP/shadow-atelier-audit163/task1137"` in a freshly registered output version: current output files intentionally refuse overwrite. No new full receiver, recursive parent scan, Git/GHA/network, credentials or mathematical execution/import/AST was used. PID5612/6392 and their active sources were not touched. This handback does not form the final typed receipt; root owns independent adoption and activation. Full native execution provenance and supporting pins are in `task1137/author-final-handback-v1.json`.

TASK1137_VERDICT: CONDITIONAL_GO_MINIMAL_METADATA_REPAIR_FOR_ROOT_REVIEW; FULL_TYPED_RECEPTION_PENDING
