#!/usr/bin/env python3
"""Independent Task496 v5-carrier firewall and frozen Task193 replay."""
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
        b'"""Independent Task496 v5-carrier firewall and frozen Task193 replay."""',
        1,
    ),
    (b'd972-r07-second-frattini-affine-prefix-compiler/v5',
     b'd972-r07-second-frattini-affine-prefix-compiler/v6', 1),
    (b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V5',
     b'R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V6', 2),
    (
        b'("search/d972_r07_task451_task193_carrier_v1.py",8553,"18c4932cbff5fbd5885ea03e80cd7f5c9f9c10bdbf4c7cc043985d3196042644")',
        b'("search/d972_r07_rank99_v5_task193_carrier_v1.py",17290,"34983cfaec66f426bdfc63eae5230c27a34f02c847f6154ba81771e6c995b0cd")',
        1,
    ),
    (
        b'("crosscheck/check_d972_r07_task451_task193_carrier_v1.py",8516,"82c5e7caa314e530782843bef81e66c431198fdc2d1c479886a14166f0fa1e73")',
        b'("crosscheck/check_d972_r07_rank99_v5_task193_carrier_v1.py",17400,"fde1cf20ed2111bddabb47abd8fd6c165db3f6e4f4c00a4acf493ceb9c0f169b")',
        1,
    ),
    (
        b'("search/d972_r07_task451_task193_carrier_gha_driver_v1.g",2499,"cdf8f4276740a18fc312de3dfca8669a0c8afd424d2551f00596e6d63251cf6a")',
        b'("search/d972_r07_rank99_v5_task193_carrier_gha_driver_v1.g",3019,"9bb7dc6778517089f3ae77f94a99d065330635552443f8e701f1e9df8dd46b99")',
        1,
    ),
    (b'd972-r07-task451-task193-carrier/v1',
     b'd972-r07-rank99-v5-task193-carrier/v1', 2),
    (b'R07_TASK451_TASK193_CARRIER_V1',
     b'R07_RANK99_V5_TASK193_CARRIER_V1', 2),
    (
        b'"producer":{"path":"search/d972_r07_a0_dual_anchored_active_batch_v1.py","bytes":13834,"sha256":"ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b"}',
        b'"producer":{"path":"search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py","bytes":104031,"sha256":"25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09"}',
        1,
    ),
    (
        b'"checker":{"path":"crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v1.py","bytes":13725,"sha256":"5c2f76b825bd920245d0200f29ff860ba93a32663ef5db9567bc499a86f7ff8a"}',
        b'"checker":{"path":"crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py","bytes":71589,"sha256":"970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d"}',
        1,
    ),
    (
        b'"driver":{"path":"search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v1.g","bytes":2569,"sha256":"6910d38adc56a564b4cd80211bb994de72fd77bf2da6abd8df2df5597ab9a000"}',
        b'"driver":{"path":"search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v5.g","bytes":9425,"sha256":"bed9105b36fef5e59120d954029ec507b16f393ab2859a7599867a19156b1b5d"}',
        1,
    ),
    (b'3316809e483223ec571ca7d6976dc1317c892441',
     b'dd6d90b64e2bfba73d7f131f4da876235746f314', 1),
    (b'task451_result', b'v5_result', 1),
    (b'task451_checkpoint', b'v5_checkpoint', 1),
    (b'task451_checker_log', b'v5_checker_log', 1),
    (b'"task454_v4_checker"', b'"task496_v5_checker"', 1),
    (b'/checker-verdict/v5', b'/checker-verdict/v6', 2),
    (b'v5 envelope', b'v6 envelope', 1),
    (b'actual_task451_positive', b'actual_common', 1),
)
GENERATED_BYTES = 7831
GENERATED_SHA256 = "b1e7b9047b839fcf5306cf32bb7876f4d55ef8e5f1eb0c48829a348811911ea3"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _generate() -> tuple[bytes, list[dict[str, object]]]:
    path = ROOT / OWNER[0]
    raw = path.read_bytes()
    if len(raw) != OWNER[1] or _sha(raw) != OWNER[2]:
        raise RuntimeError("task193-v5 checker owner pin drift")
    report: list[dict[str, object]] = []
    for old, new, expected in PATCHES:
        old_before = raw.count(old)
        new_before = raw.count(new)
        if old_before != expected or new_before != 0:
            raise RuntimeError("checker source-patch cardinality drift:" + old.decode("ascii"))
        raw = raw.replace(old, new)
        old_after = raw.count(old)
        new_after = raw.count(new)
        if old_after != 0 or new_after != expected:
            raise RuntimeError("checker source-patch postcondition drift:" + new.decode("ascii"))
        report.append({"old": old.decode("ascii"), "new": new.decode("ascii"),
                       "old_before": old_before, "new_before": new_before,
                       "old_after": old_after, "new_after": new_after})
    return raw, report


_SOURCE, _REPORT = _generate()
if "--source-patch-info" in sys.argv[1:]:
    print(json.dumps({"owner": {"path": OWNER[0], "bytes": OWNER[1], "sha256": OWNER[2]},
                      "generated": {"bytes": len(_SOURCE), "sha256": _sha(_SOURCE)},
                      "patches": _REPORT}, sort_keys=True, separators=(",", ":")))
    raise SystemExit(0)
if GENERATED_BYTES and (len(_SOURCE) != GENERATED_BYTES or _sha(_SOURCE) != GENERATED_SHA256):
    raise RuntimeError("task193-v6 generated checker pin drift")
exec(compile(_SOURCE, str(ROOT / OWNER[0]), "exec"), globals(), globals())
