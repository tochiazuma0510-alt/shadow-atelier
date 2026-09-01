#!/usr/bin/env python3
"""Exact Task453-provenance successor of the helper-nonshared carrier checker."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = (
    "crosscheck/check_d972_r07_task451_task193_carrier_v1.py",
    8516,
    "82c5e7caa314e530782843bef81e66c431198fdc2d1c479886a14166f0fa1e73",
)
PATCHES = (
    (
        b'd972-r07-task451-task193-carrier/v1',
        b'd972-r07-task451-task193-carrier/v2',
        1,
    ),
    (
        b'R07_TASK451_TASK193_CARRIER_V1',
        b'R07_TASK451_TASK193_CARRIER_V2',
        2,
    ),
    (
        b'("search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v1.g",2569,"6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000")',
        b'("search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g",2387,"8f8c803cff86fbb4bb774570cb596e9e5a8262c05321e955e2cf0de545df60dc")',
        1,
    ),
    (
        b'3316809e483223ec571ca7d6976dc1317c892441',
        b'7498d381de7180c8ca562fba5cf3bc15323d522c',
        1,
    ),
    (b'"carrier_check_p451"', b'"task453_carrier_v2_check_p451"', 1),
    (b'"carrier_check_v1"', b'"task453_carrier_v2_check_v1"', 1),
    (b'"carrier_check_v4"', b'"task453_carrier_v2_check_v4"', 1),
    (b'"carrier_check_v12"', b'"task453_carrier_v2_check_v12"', 1),
    (b'"carrier_check_p435"', b'"task453_carrier_v2_check_p435"', 1),
    (
        b'"carrier_check_exact_c451"',
        b'"task453_carrier_v2_check_exact_c451"',
        1,
    ),
)
GENERATED_BYTES = 8582
GENERATED_SHA256 = "86c0e347b32f371cf5fc3f489a491ce92f2c25fb5b5aed7148d230230d994592"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _generate() -> tuple[bytes, list[dict[str, object]]]:
    path = ROOT / OWNER[0]
    raw = path.read_bytes()
    if len(raw) != OWNER[1] or _sha(raw) != OWNER[2]:
        raise RuntimeError("carrier-v1 checker owner pin drift")
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
    raise RuntimeError("carrier-v2 generated checker pin drift")
exec(compile(_SOURCE, str(ROOT / OWNER[0]), "exec"), globals(), globals())
