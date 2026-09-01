#!/usr/bin/env python3
"""Exact Task455 carrier-v2 provenance successor of task193 checker-v5."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = (
    "crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v5.py",
    7795,
    "941eab0d9c60726436c866427de04b7c25b4ae1934fbf0a1d464f2010a7e2b9e",
)
PATCHES = (
    (
        b'"""Independent Task452 firewall and frozen-v4 task193 replay."""',
        b'"""Independent Task455 carrier-v2 firewall and frozen-v4 task193 replay."""',
        1,
    ),
    (
        b'd972-r07-second-frattini-affine-prefix-compiler/v5',
        b'd972-r07-second-frattini-affine-prefix-compiler/v6',
        1,
    ),
    (
        b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V5',
        b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V6',
        2,
    ),
    (
        b'("search/d972_r07_task451_task193_carrier_v1.py",8553,"18c4932cbff5fbd5885ea03e80cd7f5c9f9c10bdbf4c7cc043985d3196042644")',
        b'("search/d972_r07_task451_task193_carrier_v2.py",3530,"abe7d2ad15a48d641a41f51fb69c1d989224e96d024b688859a6ab141b176bf3")',
        1,
    ),
    (
        b'("crosscheck/check_d972_r07_task451_task193_carrier_v1.py",8516,"82c5e7caa314e530782843bef81e66c431198fdc2d1c479886a14166f0fa1e73")',
        b'("crosscheck/check_d972_r07_task451_task193_carrier_v2.py",3584,"8a27b06155bf94a99a38a8fd891bb811e2c0958db5ac7f39312403337a8c878b")',
        1,
    ),
    (
        b'("search/d972_r07_task451_task193_carrier_gha_driver_v1.g",2499,"cdf8f4276740a18fc312de3dfca8669a0c8afd424d2551f00596e6d63251cf6a")',
        b'("search/d972_r07_task451_task193_carrier_gha_driver_v2.g",2502,"6c0b9cc285796f4c91987e2eacfb4907e7c27867379132fdf1f8194aa9505c67")',
        1,
    ),
    (
        b'd972-r07-task451-task193-carrier/v1',
        b'd972-r07-task451-task193-carrier/v2',
        2,
    ),
    (
        b'R07_TASK451_TASK193_CARRIER_V1',
        b'R07_TASK451_TASK193_CARRIER_V2',
        2,
    ),
    (
        b'"driver":{"path":"search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v1.g","bytes":2569,"sha256":"6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000"}',
        b'"driver":{"path":"search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g","bytes":2387,"sha256":"8f8c803cff86fbb4bb774570cb596e9e5a8262c05321e955e2cf0de545df60dc"}',
        1,
    ),
    (
        b'3316809e483223ec571ca7d6976dc1317c892441',
        b'7498d381de7180c8ca562fba5cf3bc15323d522c',
        1,
    ),
    (b'"task454_v4_checker"', b'"task457_v6_v4_checker"', 1),
    (b'/checker-verdict/v5', b'/checker-verdict/v6', 2),
    (b'v5 envelope', b'v6 envelope', 1),
)
GENERATED_BYTES = 7809
GENERATED_SHA256 = "6f7bcbef4bc98d1cee1669c221affed45c614ab8d8cc4a5e8f064ebf251eca48"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _generate() -> tuple[bytes, list[dict[str, object]]]:
    path = ROOT / OWNER[0]
    raw = path.read_bytes()
    if len(raw) != OWNER[1] or _sha(raw) != OWNER[2]:
        raise RuntimeError("task193-v5 checker owner pin drift")
    report = []
    for old, new, expected in PATCHES:
        old_before = raw.count(old)
        new_before = raw.count(new)
        if old_before != expected or new_before != 0:
            raise RuntimeError(
                "checker source-patch cardinality drift:"
                + old.decode("ascii")
            )
        raw = raw.replace(old, new)
        old_after = raw.count(old)
        new_after = raw.count(new)
        if old_after != 0 or new_after != expected:
            raise RuntimeError(
                "checker source-patch postcondition drift:"
                + new.decode("ascii")
            )
        report.append(
            {
                "old": old.decode("ascii"),
                "new": new.decode("ascii"),
                "old_before": old_before,
                "new_before": new_before,
                "old_after": old_after,
                "new_after": new_after,
            }
        )
    return raw, report


_SOURCE, _REPORT = _generate()
if "--source-patch-info" in sys.argv[1:]:
    print(
        json.dumps(
            {
                "owner": {"path": OWNER[0], "bytes": OWNER[1], "sha256": OWNER[2]},
                "generated": {"bytes": len(_SOURCE), "sha256": _sha(_SOURCE)},
                "patches": _REPORT,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    raise SystemExit(0)
if len(_SOURCE) != GENERATED_BYTES or _sha(_SOURCE) != GENERATED_SHA256:
    raise RuntimeError("task193-v6 generated checker pin drift")
exec(compile(_SOURCE, str(ROOT / OWNER[0]), "exec"), globals(), globals())
