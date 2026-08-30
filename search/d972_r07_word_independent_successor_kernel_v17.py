#!/usr/bin/env python3
"""A4 v17 producer: v16 with an atomic checkpoint after each completed row.

The arithmetic, row order, compact state, and post-row queue cadence are
inherited byte-for-byte from v16.  This owner changes only checkpoint cadence
and the checkpoint identity migration: the sealed legacy v1 artifact is
accepted once by its exact physical seal, while every new checkpoint uses the
v25 schema and this v17 file identity.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v16.py")
OWNER_BYTES = 15991
OWNER_SHA256 = "bbd2c2093da3f18d2ea298c5d6955d987d4acbfc6eeb2dc9665abdad556bb2a7"
OWNER_GENERATED_BYTES = 232872
OWNER_GENERATED_SHA256 = "01aaff4b64d39b8f56569d079b10df2dc12657a6a7c4a7cefb7449241d303863"
RESULT_GENERATED_BYTES = 233607
RESULT_GENERATED_SHA256 = "5a58fa44602f853bd87fd4d4a98a2593f5ae2877c873e87b2a2f6b7a8f1c84c9"

PATCHES = (
    (
        b'''        if checkpoint_path is not None and checkpoint_writes_enabled and ordinal in {4, 8, 12, 16, 20, 24, 28, 32, 64, 128, 256, 512, 1024, 2048, 3072, 4096, 5120, 6144, ROWS}:''',
        b'''        if checkpoint_path is not None and checkpoint_writes_enabled:''',
    ),
    (
        b'''CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v24"
LEGACY_CHECKPOINT_SCHEMA = "d972-r07-word-independent-successor-kernel/v6/checkpoint/v1"
LEGACY_PRODUCER_CODE_SHA256 = "964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7"
''',
        b'''CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v25"
LEGACY_CHECKPOINT_SCHEMA = "d972-r07-word-independent-successor-kernel/v6/checkpoint/v1"
LEGACY_PRODUCER_CODE_SHA256 = "964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7"
LEGACY_CHECKPOINT_BYTES = 25581
LEGACY_CHECKPOINT_SHA256 = "595213bab8936ef10e94ce90ccf526c105d02d871d4dc5d02b6c76cb51593445"
LEGACY_CHECKPOINT_NEXT_ROW = 25
''',
    ),
    (
        b'''    require(checkpoint_schema in (CHECKPOINT_SCHEMA, LEGACY_CHECKPOINT_SCHEMA) and
            value.get("authority") == authority.identity and value.get("owner") == "producer" and
            checkpoint_code_sha == (LEGACY_PRODUCER_CODE_SHA256 if
                                    checkpoint_schema == LEGACY_CHECKPOINT_SCHEMA else
                                    sha(Path(__file__).read_bytes())), "checkpoint:identity")''',
        b'''    require(checkpoint_schema in (CHECKPOINT_SCHEMA, LEGACY_CHECKPOINT_SCHEMA) and
            value.get("authority") == authority.identity and value.get("owner") == "producer" and
            ((checkpoint_schema == LEGACY_CHECKPOINT_SCHEMA and
              len(raw) == LEGACY_CHECKPOINT_BYTES and sha(raw) == LEGACY_CHECKPOINT_SHA256 and
              value.get("next_row") == LEGACY_CHECKPOINT_NEXT_ROW and
              checkpoint_code_sha == LEGACY_PRODUCER_CODE_SHA256) or
             (checkpoint_schema == CHECKPOINT_SCHEMA and
              checkpoint_code_sha == sha(Path(__file__).read_bytes()))),
            "checkpoint:identity")''',
    ),
    (
        b'''        require(claimed == digest(body) and
                value.get("schema") in (CHECKPOINT_SCHEMA, LEGACY_CHECKPOINT_SCHEMA) and
                value.get("owner") == "producer" and isinstance(value.get("code_sha256"), str) and
                isinstance(value.get("next_state_canary"), str), "terminal:checkpoint_seal")''',
        b'''        require(claimed == digest(body) and
                value.get("schema") in (CHECKPOINT_SCHEMA, LEGACY_CHECKPOINT_SCHEMA) and
                value.get("owner") == "producer" and isinstance(value.get("code_sha256"), str) and
                ((value.get("schema") == LEGACY_CHECKPOINT_SCHEMA and
                  len(raw) == LEGACY_CHECKPOINT_BYTES and sha(raw) == LEGACY_CHECKPOINT_SHA256 and
                  value.get("next_row") == LEGACY_CHECKPOINT_NEXT_ROW and
                  value.get("code_sha256") == LEGACY_PRODUCER_CODE_SHA256) or
                 (value.get("schema") == CHECKPOINT_SCHEMA and
                  value.get("code_sha256") == sha(Path(__file__).read_bytes()))) and
                isinstance(value.get("next_state_canary"), str), "terminal:checkpoint_seal")''',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v17 producer: frozen v16 owner drift")
    owner_ns: dict[str, Any] = {
        "__name__": "_r07_a4_v16_owner",
        "__file__": str(OWNER.resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if (len(raw) != OWNER_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256):
        raise SystemExit("v17 producer: frozen v16 generated source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v17 producer: audited site is not unique")
        raw = raw.replace(old, new)
    if (len(raw) != RESULT_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256):
        raise SystemExit("v17 producer: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(OWNER), "exec"), ns, ns)


if __name__ == "__main__":
    main()
