# Task427 v9 — bootstrap namespace fix

Created only the four authorized v9 outputs. The v8 search, quotient, memory, resource, and claim logic was preserved; the producer bootstrap namespace was corrected in `run()` so BASE is loaded before all receipt/q3/compact operations:

```python
t413 = v3.load(v3.T413, "task427_task413")
base = t413["bound_module"](t413["BASE"], "task427_base")
receipt = t413["load_json"](base, t413["JOINT"])
q3 = t413["load_json"](base, t413["Q3"])
pres = base["compact"](receipt, q3)
```

The same `base` object is reused for the remaining roof, acceptance, layout, and task176 calls. There is no v8 runtime import and the sole runtime dependency remains the pinned v3 module. Identifiers, schemas, checkpoint headers, markers, paths, and driver variables are v9-specific.

## Bounded gates

Passed:

```text
python -m py_compile search/d972_r07_a0_pb34_direct_quotient_owner_v9.py crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v9.py
python -B search/d972_r07_a0_pb34_direct_quotient_owner_v9.py --mode FIXTURE
R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V9 FIXTURE_PASS
python -B crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v9.py --self-test
R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V9_PASS {"fresh_object_mutation_gates":3,"status":"FIXTURE_PASS"}
```

The required seconds=0 bootstrap smoke was attempted once, single-process, without a checkpoint and with the output in `%TEMP%`. It reached the pinned task198 runtime construction but the local Windows environment rejected the frozen same-handle identity gate before either owner marker:

```text
R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V9 UNKNOWN
artifact reason: pinned.r07_v6_frozen_e4:windows_same_handle_identity_unavailable
markers: phase=preflight owner_v9=BOUND — absent; phase=runtime_bootstrap owner_v9=READY — absent
```

This is the known local-platform ABI gate; no seed/parent/action work or checkpoint was entered or created. The Linux GHA environment is required to exercise the two bootstrap markers and expected `UNKNOWN_RESOURCE:time_limit` path. I do not relabel this environment failure as a time-limit success.

No production search, GHA dispatch, commit, or push was performed.

## Exact output seals

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_pb34_direct_quotient_owner_v9.py` | 26006 | `98efac926970a5c3aa23a43b100ae64c52ce60ab0313d151f88b4dc37e6bd611` |
| `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v9.py` | 7392 | `641a4af5523ff365d56ccd283d518263a00fc1a397f8b806f8da3698b9edc0de` |
| `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v9.g` | 2897 | `77456628d92b76f4d149b3bb7d9a69ccb5bf3bdc76f1358b63a8a60dde39a121` |

The driver pins the exact producer/checker bytes and SHA values, uses distinct v9 input/output checkpoint names, preserves the 4.8 GB cap and live tee logs, and rejects stale output checkpoints.

V9_LOCAL_NO-GO: Windows same-handle identity gate prevented the mandated bootstrap smoke from certifying the two markers; code is ready for Linux GHA verification after the namespace fix.

## Parent Linux-GHA adjudication and dispatch

Independent Sol audit found the v9 namespace correction, unchanged v8 memory
logic, exact pins and fresh driver **GO for Linux GHA**.  The Windows
same-handle stop above is platform-specific and remains honestly recorded.

- superseded fail-closed run: `33317727481` / job `99274129809`, commit
  `b7225a9d59495e19ab8a2d146a473e9254a91f62`, result `UNKNOWN`, reason
  `"'load'"`, no checkpoint and no search work;
- v9 dispatch commit: `530a29014fc0de20176d4f41a5032ffa787e973f`;
- branch: `sol/r07-explicit-lift-20260825`;
- workflow: `gap-run.yml`;
- run id: `33318299384`;
- job id: `99275661576`;
- script: `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v9.g`;
- fresh input checkpoint: absent;
- timeout: owner `9000` seconds; workflow `180` minutes;
- initial state at dispatch: `in_progress`.
