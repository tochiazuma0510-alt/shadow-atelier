# Task432 A0 prefix-positive probe v1 dispatch audit

Date: 2026-08-31  
Scope: v408, task432, the wrapper/driver/reply, and the unchanged pinned v12
producer/checker only.  No checkpoint, download, production, or dispatch was
run.

## Verdict

**GO for the immediate GHA prefix probe.**

1. Theorem 2.1 of v408 is sound with a nonempty frontier.  Every retained
   normalized pivot is already an element of the full occurrence correction
   image, so its span is a subspace of that image.  A solve after physical
   aggregation and the six-action space therefore implies the full A0 solve.
   The converse is not used: prefix failure and every resource terminal remain
   UNKNOWN and cannot support NONMEMBER.
2. Wrapper lines 9--15 pin the exact 51884-byte v12 producer at SHA-256
   `3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3`.
   Lines 27--40 independently require the immutable relative regular,
   non-symlink sequence-40 input at 326449173 bytes and SHA-256
   `0b3169fe6e7051fe46a28bb966ffd3dfeada841dce1a6fe2358959dd99402ff1`.
   The pinned v12 `cp_read` then performs its unique exact
   `parent -> occurrence_queue` normalization and every ordinary state gate.
3. `FalseTruthDeque` changes only queue truth (wrapper lines 43--48).  The v12
   module has no other use of its imported `deque`: restoration constructs the
   same 906-element queue, records its length/content, and only v12 line 474's
   `while queue` actor loop is skipped.  Rank 1316, frontier 906, pivot rows,
   expressions, and sources remain available for physical aggregation.  No
   child actor is evaluated; occurrence row payload is released only after its
   aggregate is inserted, while the expression/source DAG needed by positive
   replay remains retained.
4. The call fixes `resume_v11_url=None`, `checkpoint=None`, 9000 seconds, and
   4800000000 bytes (wrapper lines 76--82), restores the original deque in
   `finally`, and has no checkpoint writer.  The driver passes no checkpoint
   output to either producer or checker.  The recovered input is read only and
   input/artifact paths are distinct.
5. Resource exceptions are retained inside `a0` but normalized to top-level
   `UNKNOWN`; `six_action_exhausted` becomes the explicit positive-only UNKNOWN
   reason (wrapper lines 96--105).  Any foreign terminal, including a future
   NONMEMBER or COMMON_WORD, is also forced to UNKNOWN.  All promotion flags
   remain false.  Consequently the unchanged checker needs no output
   checkpoint and accepts the existing UNKNOWN ABI.
6. A `COMMON_CANDIDATE` can arise only from unchanged v12 `positive`, which
   reconstructs selected pivot atoms, checks every physical source digest and
   selected action row, exactifies to exponent pair `(0,0)`, replays joint
   identity and all-seven direct Fox/quotient equality, and checks
   target+correction+actions=0.  The wrapper does not promote that candidate;
   the unchanged v12 candidate checker is still the next envelope gate.
7. Driver line 18 retains the exact v12 release URL, six-name v12 roster,
   duplicate/extra/path rejection, zip and checkpoint pins, same-directory
   temporaries, regular/dangling-symlink gates, hash-bound seal, and fresh
   exact receipt.  In-memory reconstruction gave 91 `Concatenation` parts,
   exactly `bash -lc <one-line payload>`, one quoted hash-bound receipt after
   both validation branches, and all six v12 names in both branches.  Task432
   recovery/artifact/log/receipt paths are distinct from task431.
8. Driver lines 23 and 26 require exactly one producer marker and exactly one
   checker PASS marker.  There is no output-checkpoint path or argument.

Actual identities agree with the driver and Luna reply:

- wrapper: 6270 bytes, SHA-256
  `b48d84850a6c0033e62f3e2ebe41bdf14b73f68dcb0670ba06dcf9e825a38bbd`
- driver: 7620 bytes, SHA-256
  `1ebe5d486882dad8674359cbdd5e6afb59945e67cc27d47aeef4cebd1b6c05ba`
- unchanged checker: 13334 bytes, SHA-256
  `e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`

Bounded commands performed: in-memory wrapper compilation, unchanged checker
`--self-test`, driver-command reconstruction, file SHA/byte checks, and
`git diff --check` on the three task432 outputs.  The 326 MB checkpoint was not
opened locally, and no wrapper production/fixture, download, workflow change,
commit, push, or dispatch was performed.

GO
