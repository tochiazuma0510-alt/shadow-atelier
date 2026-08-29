#!/usr/bin/env python3
"""Independent A4 v22 checker: v19 with corrected final file pin.

This version is byte-for-byte the finalized v19 implementation with only its
version labels advanced.  It includes the v16-parity receipt_bytes authority
field and the explicit legacy-authority migration needed to consume the
unchanged embedded v25 checker checkpoint during RESUME.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v17.py")
OWNER_BYTES = 7574
OWNER_SHA256 = "0b0281af7d38f4c255f7cd3346dc816987da863a29275a2c6c1851366171cef0"
OWNER_GENERATED_BYTES = 266860
OWNER_GENERATED_SHA256 = "78409970ed60b7e5d97335592275716adb298ed85e65b49829c66bacc98f1d92"
RESULT_GENERATED_BYTES = 268101
RESULT_GENERATED_SHA256 = "28cba6455e249edac835babb63b099940d91965d4e7c0f1d6a5310c57d569d18"

PATCHES = (
    (
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v15.py"',
        b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v16.py"',
    ),
    (
        b'''            "task198": {key: {"path": "ci/in/" + AUTH[key], "bytes": len(raw), "sha256": sha(raw)}''',
        b'''            "task198": {key: {"path": AUTH[key], "bytes": len(raw), "sha256": sha(raw)}''',
    ),
    (
        b'''    require(claimed == digest(value) and value.get("schema") == SCHEMA + "/checkpoint/v1" and
            value.get("owner") == "producer" and reference.get("owner") == "producer" and
            value.get("code_sha256") == reference.get("code_sha256") and
            value.get("code_sha256") == sha((ROOT / PRODUCER_CODE_PATH).read_bytes()) and''',
        b'''    require(claimed == digest(value) and
            value.get("schema") in (PRODUCER_CHECKPOINT_SCHEMA, LEGACY_PRODUCER_CHECKPOINT_SCHEMA) and
            value.get("owner") == "producer" and reference.get("owner") == "producer" and
            value.get("code_sha256") == reference.get("code_sha256") and
            value.get("code_sha256") == (LEGACY_PRODUCER_CODE_SHA256 if
                                          value.get("schema") == LEGACY_PRODUCER_CHECKPOINT_SCHEMA else
                                          sha((ROOT / PRODUCER_CODE_PATH).read_bytes())) and''',
    ),
    (
        b'''    require(value.get("schema") == SCHEMA + "/checkpoint/v1" and value.get("authority") == authority.identity and
            value.get("owner") == "checker" and
            value.get("code_sha256") == sha(Path(__file__).read_bytes()), "checker:checkpoint_identity")''',
        b'''    require(value.get("schema") == SCHEMA + "/checkpoint/v1" and value.get("authority") == authority.identity and
            value.get("owner") == "checker" and
            value.get("code_sha256") in (sha(Path(__file__).read_bytes()), LEGACY_CHECKER_CODE_SHA256),
            "checker:checkpoint_identity")''',
    ),
    (
        b'''            "receipt_sha256": RECEIPT_SHA, "manifest_sha256": MANIFEST_SHA,\n''',
        b'''            "receipt_sha256": RECEIPT_SHA, "receipt_bytes": RECEIPT_BYTES,\n            "manifest_sha256": MANIFEST_SHA,\n''',
    ),
    (
        b'''    require(value.get("schema") == SCHEMA + "/checkpoint/v1" and value.get("authority") == authority.identity and
            value.get("owner") == "checker" and
            value.get("code_sha256") in (sha(Path(__file__).read_bytes()), LEGACY_CHECKER_CODE_SHA256),
            "checker:checkpoint_identity")''',
        b'''    legacy_authority = dict(authority.identity)
    legacy_authority.pop("receipt_bytes", None)
    legacy_task198 = {key: dict(item) for key, item in authority.identity["task198"].items()}
    require(set(legacy_task198) == {"checker", "manifest", "producer", "receipt", "verdict"},
            "checker:legacy_task198_keys")
    for item in legacy_task198.values():
        item["path"] = "ci/in/" + item["path"]
    legacy_authority["task198"] = legacy_task198
    current_code_sha = sha(Path(__file__).read_bytes())
    require(value.get("schema") == SCHEMA + "/checkpoint/v1" and
            value.get("owner") == "checker" and
            ((value.get("authority") == authority.identity and
              value.get("code_sha256") == current_code_sha) or
             (value.get("authority") == legacy_authority and
              value.get("code_sha256") == LEGACY_CHECKER_CODE_SHA256)),
            "checker:checkpoint_identity")''',
    ),
)


def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v22 checker: frozen v17 owner drift")
    owner_ns: dict[str, Any] = {
        "__name__": "_r07_a4_v17_owner",
        "__file__": str(OWNER.resolve()),
        "__package__": None,
        "__cached__": None,
    }
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if (len(raw) != OWNER_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256):
        raise SystemExit("v22 checker: frozen v17 generated source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v22 checker: audited site is not unique")
        raw = raw.replace(old, new)
    schema_anchor = b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v16.py"\n'
    schema_block = (schema_anchor +
                    b'PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v24"\n'
                    b'LEGACY_PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v1"\n'
                    b'LEGACY_PRODUCER_CODE_SHA256 = "964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7"\n'
                    b'LEGACY_CHECKER_CODE_SHA256 = "0b0281af7d38f4c255f7cd3346dc816987da863a29275a2c6c1851366171cef0"\n')
    if raw.count(schema_anchor) != 1:
        raise SystemExit("v22 checker: producer schema anchor is not unique")
    raw = raw.replace(schema_anchor, schema_block)
    if (len(raw) != RESULT_GENERATED_BYTES or
            hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256):
        raise SystemExit("v22 checker: resulting generated source drift")
    return raw


def main() -> None:
    raw = restore_frozen()
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)


if __name__ == "__main__":
    main()


