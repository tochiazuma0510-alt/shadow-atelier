#!/usr/bin/env python3
"""Independent A4 v24 checker: v23 arithmetic with delta-chain transport pins."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

OWNER = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v23.py")
OWNER_BYTES = 2554
OWNER_SHA256 = "c9fcbf9b4c8d56a6dd773c878b87014cc24e6bdc23e649109de75ebf5963adce"
OWNER_GENERATED_BYTES = 268101
OWNER_GENERATED_SHA256 = "6bee9fe57b9d10af5e9ef024a8510cc94a7733869b5a88cb04ecd494eef5c786"
RESULT_GENERATED_BYTES = 272663
RESULT_GENERATED_SHA256 = "55f10d5a6339d3ababca981766aa7509933355d4a7054e6a742a68f5bfc333b6"

DELTA_BLOCK = b'''\
PRODUCER_DELTA_SCHEMA = SCHEMA + "/delta/v1"
PRODUCER_DELTA_HEAD_SCHEMA = SCHEMA + "/head/v1"
PRODUCER_LEGACY_BASE_BYTES = 25581
PRODUCER_LEGACY_BASE_SHA256 = "595213bab8936ef10e94ce90ccf526c105d02d871d4dc5d02b6c76cb51593445"
PRODUCER_LEGACY_BASE_CODE_SHA256 = "964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7"

def _producer_delta_digest(value: Any) -> str:
    return digest(value)

def _producer_delta_chain(value: dict[str, Any], prior: str) -> str:
    unsigned = dict(value); unsigned.pop("chain", None)
    return sha((str(prior) + _producer_delta_digest(unsigned)).encode("ascii"))

def validate_delta_terminal_chain(reference: dict[str, Any], meter: Meter) -> None:
    require(set(reference) == {"kind", "path", "bytes", "sha256", "owner", "base",
                               "last_sequence", "last_segment", "last_segment_sha256",
                               "last_row", "next_row", "chain", "checkpoint_self_digest_sha256",
                               "replayable", "sealed"} and reference.get("kind") == "delta_chain" and
            reference.get("owner") == "producer" and reference.get("replayable") is True and
            reference.get("sealed") is True, "checker:delta_reference_shape")
    head_path = checkpoint_input(Path(reference["path"]), "CHECKER_DELTA_HEAD")
    raw = read_once(head_path, (head_path.as_posix().replace(ROOT.as_posix() + "/", ""),
                                int(reference["bytes"]), reference["sha256"]), meter,
                    "checker.delta_head", terminal_transport=True)
    require(len(raw) == int(reference["bytes"]) and sha(raw) == reference["sha256"],
            "checker:delta_head_physical")
    head = json.loads(raw.decode("ascii")); claimed = head.pop("self_digest_sha256", None)
    require(claimed == digest(head) and claimed == reference["checkpoint_self_digest_sha256"] and
            head.get("schema") == PRODUCER_DELTA_HEAD_SCHEMA and head.get("owner") == "producer",
            "checker:delta_head_seal")
    base = head.get("base", {}); base_path = head_path.with_name(str(base.get("path", "")))
    base_raw = base_path.read_bytes()
    require(base == {"path": base_path.name, "bytes": len(base_raw), "sha256": sha(base_raw)} and
            len(base_raw) == PRODUCER_LEGACY_BASE_BYTES and sha(base_raw) == PRODUCER_LEGACY_BASE_SHA256,
            "checker:delta_base_identity")
    count = int(head.get("segment_count", 0)); previous = None; chain = "0" * 64
    for sequence in range(1, count + 1):
        segment_path = head_path.with_name(head_path.name + ".delta.%08d.json" % sequence)
        require(segment_path.exists(), "checker:delta_missing_segment")
        segment_raw = segment_path.read_bytes(); segment = json.loads(segment_raw.decode("ascii"))
        seal_value = segment.pop("self_digest_sha256", None)
        require(seal_value == digest(segment) and segment.get("schema") == PRODUCER_DELTA_SCHEMA and
                segment.get("owner") == "producer" and segment.get("sequence") == sequence and
                segment.get("base") == base and segment.get("previous") == previous,
                "checker:delta_segment_seal")
        chain = _producer_delta_chain(segment, chain)
        require(segment.get("chain") == chain, "checker:delta_chain_digest")
        previous = sha(segment_raw)
    require(head.get("last_sequence") == count and head.get("last_segment_sha256") == previous and
            head.get("chain") == chain and reference.get("base") == base and
            reference.get("last_sequence") == count and reference.get("last_segment") == head.get("last_segment") and
            reference.get("last_segment_sha256") == previous and reference.get("last_row") == head.get("last_row") and
            reference.get("next_row") == head.get("next_row") and reference.get("chain") == chain,
            "checker:delta_terminal_binding")
    if count:
        require(head.get("next_row") == segment.get("next_row") and
                head.get("last_row") == (segment.get("ordinal") if segment.get("kind") == "row" else ROWS) and
                25 < int(head.get("next_row", 0)) <= ROWS + 1,
                "checker:delta_head_ahead")
    else:
        require(head.get("next_row") == 25 and head.get("last_row") == 24,
                "checker:delta_empty_head")
    require(len(list(head_path.parent.glob(head_path.name + ".delta.*.json"))) == count,
            "checker:delta_orphan_segment")
'''

PATCHES = (
    (b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v17.py"',
     b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v18.py"'),
    (b'PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v25"',
     b'PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v26"'),
)

def restore_frozen() -> bytes:
    owner_raw = OWNER.read_bytes()
    if len(owner_raw) != OWNER_BYTES or hashlib.sha256(owner_raw).hexdigest() != OWNER_SHA256:
        raise SystemExit("v24 checker: frozen v23 owner drift")
    owner_ns: dict[str, Any] = {"__name__": "_r07_a4_v23_owner", "__file__": str(OWNER.resolve()),
                                "__package__": None, "__cached__": None}
    exec(compile(owner_raw, str(OWNER), "exec"), owner_ns, owner_ns)
    raw = owner_ns["restore_frozen"]()
    if len(raw) != OWNER_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != OWNER_GENERATED_SHA256:
        raise SystemExit("v24 checker: frozen v23 generated source drift")
    anchor = b'PRODUCER_CHECKPOINT_SCHEMA = SCHEMA + "/checkpoint/v25"\n'
    if raw.count(anchor) != 1:
        raise SystemExit("v24 checker: schema anchor drift")
    raw = raw.replace(anchor, anchor + DELTA_BLOCK)
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v24 checker: audited site is not unique")
        raw = raw.replace(old, new)
    marker = b'def validate_terminal_checkpoint(reference: dict[str, Any], authority: Authority | None, meter: Meter) -> None:\n    require(isinstance(reference, dict), "checker:terminal_checkpoint_shape")\n'
    replacement = marker + b'    if reference.get("kind") == "delta_chain":\n        validate_delta_terminal_chain(reference, meter)\n        return\n'
    if raw.count(marker) != 1:
        raise SystemExit("v24 checker: terminal hook drift")
    raw = raw.replace(marker, replacement)
    if len(raw) != RESULT_GENERATED_BYTES or hashlib.sha256(raw).hexdigest() != RESULT_GENERATED_SHA256:
        raise SystemExit("v24 checker: resulting generated source drift")
    return raw

def main() -> None:
    raw = restore_frozen(); ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
                                   "__package__": None, "__cached__": None}
    exec(compile(raw, str(Path(__file__).resolve()), "exec"), ns, ns)

if __name__ == "__main__":
    main()
