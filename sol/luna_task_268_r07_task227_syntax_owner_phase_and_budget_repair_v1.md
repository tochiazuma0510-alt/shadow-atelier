# Luna task 268 - task227 syntax, owner, phase, and budget repair v1

Role: bounded implementation repair only. Read task265 and all current task227
files. Do not run Python, Node, GAP, git, GHA, or network. Edit only the same
five task227 files plus its existing Luna reply.

## Exact parent rejection after task265

1. Producer lines 310-313 contain an `if ... else ... else` structure. This is
   a Python syntax error, so the return is not executable.
2. `occurrence_basis_row` still replaces the first row by the shape-valid row
   `[[[0,0,0,0],0,1]]`. It passes `CASE_OCCURRENCE_BASIS` and is first rejected
   by ancestry, contrary to the fixed owner gate. The checker has the same
   ordering defect. Use a canonical, decodable row with out-of-roster ordinal
   11 (or an equivalent replacement) so the first natural failure is exactly
   producer `CASE_OCCURRENCE_BASIS` / checker `occurrence basis row`; do not
   rely on a decoder exception.
3. Checker `validate_resource` accepts either phase in every context. SELFTEST
   cases must require exactly `selftest`; production MEMBER/NONMEMBER must
   require exactly `production`. Thread the expected phase through the
   independent checker and keep all other sealed fields exact.
4. A single SELFTEST `Budget` calls `closure` five times, and every closure
   calls `actor_roster`, whose declared `checker_roster` cap is exactly 729.
   The second case therefore necessarily returns UNKNOWN_RESOURCE before the
   commissioned cases/mutations. Do not raise or bypass the cap. Establish
   the actor-roster and Q axioms once per SELFTEST invocation, reuse that exact
   structural result for its five toy closures, and keep production closure's
   structural check mandatory. The independent-orbit rebuild must still use
   the active invocation budget as required by task265.

Repair these four issues, preserve the exact NONMEMBER remainder equation,
independent canonical block echelon, 24 fixed mutations, sealed canary, actual
production path, caps, typed UNKNOWN vocabulary, and false conclusions.
Refresh driver/fixture/reply identities and report UNEXECUTED. Parent Sol will
perform another whole-file audit before GHA.

A3 remains 0/3 until actual accepted task226 input is consumed.
