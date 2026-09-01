# Luna reply 450 — R07 A0 rank-51 checkpoint resume v6

Status: **bounded continuation transport complete; no production/GHA/git**.

## Exact outputs

| path | bytes | SHA256 |
|---|---:|---|
| `search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json` | 10934 | `a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4` |
| `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v6.py` | 3590 | `e902468fca7ead498e78c06496ccea596c10a1904e571f5d6b709962458b1739` |
| `search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v6.g` | 2792 | `312d588b58a929cfc1789d506c67507a67419d7e17727c7c8fb6bd660b3340d5` |
| `sol/luna_reply_450_r07_a0_rank51_checkpoint_resume_v6.md` | self-referential | not driver-pinned |

The frozen checkpoint was transferred byte-for-byte with `apply_patch`. Its independently rechecked authenticated fields are rank 51, accepted count 8, round 9, and internal state SHA256 `22dcfdfb396524ea5853488aa2ad52d28b4f7d10164123bc83f121e59dd83159`.

## Transport implementation

- The v6 checker pins and delegates the full v5 checker at 2,859 bytes / `e783028862bbae84acf769ec64de9693dfae1c4c99e9444e8e92af76e08a2da0`.
- Before delegation it independently authenticates the repository checkpoint's bytes, outer SHA, v3 schema/binding, internal canonical state seal, and registered rank/count/round.
- The final accepted-source list must contain the frozen eight records as an exact ordered prefix.
- Final accepted count and physical rank cannot decrease from 8 and 51; final round cannot decrease from 9.
- The delegated v5 checker still authenticates the final durable checkpoint and independently replays every final source and terminal profile.
- The v6 driver pins the unchanged v3 producer, v6 checker, and frozen checkpoint. It copies the frozen input into a fresh direct child of `ci/out`, authenticates the copy, and passes it through `--resume`.
- The continuation command uses 7,200 seconds, 4,800,000,000 RSS bytes, and 64 new rises. Artifact, output checkpoint, and logs use fresh v6 paths.
- The driver contains one production process, an external v6 preamble requirement, and no production fixture/self-test.

No actor-adapted quotient, new store, closure, or search-universe change was introduced.

## Bounded gates

```text
PYTHONPYCACHEPREFIX=%TEMP%\task450_pycache python -m py_compile crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v6.py
python crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v6.py --self-test
rg -n -- "--resume|--seconds 7200|--rss-bytes 4800000000|--max-rises 64|SELFTEST|FIXTURE|actor|closure" search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v6.g
```

Compile and checker self-test passed. Mutations rejected:

- frozen checkpoint internal seal drift;
- alteration of the eight-record prefix;
- decreasing final rank;
- decreasing final accepted count;
- decreasing final round.

Static driver inspection confirmed the exact resume/cap command and absence of SELFTEST, FIXTURE, actor, or closure paths.

No local heavy production, Q0 computation, checkpoint replay, GHA dispatch, workflow edit, commit, push, or other git operation was performed.
