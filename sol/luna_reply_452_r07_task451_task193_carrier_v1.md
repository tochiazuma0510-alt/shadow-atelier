# Luna reply 452: Task451 positive -> task193 literal carrier v1

Status: **REPAIRED / BOUNDED GATES PASS / PRODUCTION NOT RUN**

## Outputs

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_task451_task193_carrier_v1.py` | 8553 | `18c4932cbff5fbd5885ea03e80cd7f5c9f9c10bdbf4c7cc043985d3196042644` |
| `crosscheck/check_d972_r07_task451_task193_carrier_v1.py` | 8516 | `82c5e7caa314e530782843bef81e66c431198fdc2d1c479886a14166f0fa1e73` |
| `search/d972_r07_task451_task193_carrier_gha_driver_v1.g` | 2499 | `cdf8f4276740a18fc312de3dfca8669a0c8afd424d2551f00596e6d63251cf6a` |

No optional repository fixture was created. Temporary fixture output was written under `%TEMP%`.

## Implemented boundary

- Exact-pins the current Task451 producer/checker/driver and frozen rank-51 certificate.
- Physically binds the Task451 result, durable checkpoint (path/bytes/SHA), exact checker PASS log, fixed source head `3316809e483223ec571ca7d6976dc1317c892441`, and positive numeric run/artifact ids.
- Producer and carrier checker both load the exact pinned Task451 checker and invoke `C451.check(result)`. Thus the PASS log is not used as a substitute for batch/echelon/action/positive replay.
- Accepts only the exact positive `COMMON_CANDIDATE` envelope and extracts only `terminal_replay.literal_word`.
- Reconstructs `g760` and the target through the pinned v12/p435 physical bootstrap (no Q0 store, selector scan, task193 legacy envelope, or old adapter relabel).
- Computes `corrected_word=free_reduce(g760+correction_word)` and replays exact exponent zero, ten-coordinate joint identity, `AllSevenModel.direct_column`, eleven-occurrence/direct equality, target ownership, correction ownership, and selected action ancestry.
- Uses the task193 historical sparse digest framing `u32be(len(key)) || key || coefficient`; it does not expose v12's little-endian row digest as the carrier digest.
- Requires reconstructed `g760` to be exactly 760 valid F2 letters. The carrier embeds the freshly computed complete `replay` dictionary and explicitly fixes `hexagons=true` and `pentagon_printed_order=true`; the independent checker reconstructs and compares all three.
- Emits canonical `self_digest` seals on the accepted carrier and checker verdict, only the literal carrier and immutable provenance. A2/lift/fake/Ihara claims remain false.
- The checker does not import the adapter producer. It independently parses/reduces the three words and reconstructs the same physical evaluator gates.

## Bounded gates

Commands:

```text
$env:PYTHONPYCACHEPREFIX="$env:TEMP\task452_pyc2"
python -m py_compile search/d972_r07_task451_task193_carrier_v1.py crosscheck/check_d972_r07_task451_task193_carrier_v1.py
python -B search/d972_r07_task451_task193_carrier_v1.py --mode FIXTURE --output "$env:TEMP\task452_fixture2.json"
python -B crosscheck/check_d972_r07_task451_task193_carrier_v1.py --self-test
```

Terminals:

```text
R07_TASK451_TASK193_CARRIER_V1 status=FIXTURE
R07_TASK451_TASK193_CARRIER_V1_CHECKER_SELFTEST_PASS
```

The checker self-test rejected 18 mutations: exact terminal, result identity, checkpoint identity, checker marker, fixed source head, run id, artifact id, literal word, g760, multiplication order/corrected word, occurrence gate, exponent gate, joint-kernel gate, action ancestry, legacy sparse-row digest, full replay, hexagon convention, and printed-order pentagon convention. It explicitly records `actual_task451_positive=false`.

## Reuse boundary and limitations

The direct evaluator is the pinned current Task451 physical dependency chain: v12/p435 -> task413/task198 runtime -> accepted `AllSevenModel`. This is evaluator reuse only; no Task451 search is rerun and no task193 values are computed. The real positive artifact was not available/run locally, so production remains pending an independently accepted Task451 positive input. No commit, push, GHA dispatch, workflow edit, or production bootstrap was performed.
