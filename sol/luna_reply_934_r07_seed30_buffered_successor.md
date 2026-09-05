# Task934 -- one-line buffered producer successor

## F1. Completed scope

Created `search/d972_r07_actual_seed30_materializer_v2.py` by copying the
frozen v1 through `apply_patch` and changing only its P1 instruction stream
buffering setting, at line 731:

```diff
-            instruction_path.open("rb", buffering=0) as instruction_stream:
+            instruction_path.open("rb", buffering=1 << 20) as instruction_stream:
```

The binary cache reader remains unchanged. All arithmetic, selection,
constants, schemas/ABI, output, CLI and existing tests are byte-for-byte
unchanged outside that single setting. No new test was added.

Read-only whole-source comparison confirmed that applying exactly that
replacement to v1 gives the complete v2 source. V1 was not edited.

## F2. Frozen source receipts

```text
v2 path: search/d972_r07_actual_seed30_materializer_v2.py
v2 bytes: 79657
v2 SHA256: 01a74d8d772e64c9f4b1a2c52d028e6e653a6445e3039c4736e1ab6ba3ea484e
v2 LF: 1563; CR: 0; final LF: present

preserved v1 bytes: 79651
preserved v1 SHA256: 3ce9293e05f06bf343bd2a54af0ab84ae67f4b922a428cd3c73e38944d6de55c
```

These receipts come from read-only PowerShell `Get-FileHash`, file-size
inspection and whole-text comparison, not Python execution. The exact v2
path, bytes and SHA were sent to Task930 for its separately authorized
workflow v2 / reply935. Checker v1 and its pin are unchanged.

## F3. Runtime and claim boundary

The concrete avoidable setting was unbuffered `readline()` on the accepted
349,055,442-byte P1 instruction file. V2 uses a 1 MiB binary buffer. No
profile was taken; neither time spent at that line nor a speedup is claimed.

Root subsequently reported run33946247365 completed SUCCESS with the actual
rank1354-to1355 append and next Separator. This worker did not cancel that
run, dispatch v2, or repeat the successful seed materialization. V2 is
retained for the next real task, not an identical replay.

No local Python/GAP execution, network, credentials, git, GHA or new test
execution occurred. There is no new worker commit SHA or run ID to record.
Only the new producer v2 and this reply were edited by this worker. The
executed v1 sources/workflow remain immutable. This buffering-only handoff
does not promote any mathematical claim: `verified=false`.
