#!/usr/bin/env python3
"""Convention-repaired adapter for the total ordinary K2 roster producer.

The authenticated fixed-row36 K2 law is deliberately unchanged. Its G36/G9
marked generator is y=((1,1),(1,0),(1,1)). The independently frozen 972-row
word-key artifact serializes words through the compact permutation model whose
D9 coordinate decoder gives y=((-1,1),(1,0),(-1,1)). Row36 does not expose
this distinction; zero-based row81 is the first failure.

This v2 adapter pins and reuses the v1 producer, but dispatches only modulus-9
roof artifact word authentication to the compact-word convention. All K2
source enumeration, reduction coordinates, predicates, and fixed-row36
lineage replay continue to use the registered v1 K2 law.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
from pathlib import Path
import sys
from types import ModuleType
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REL = "search/d972_k2_total_fibre_roster_producer_v2.py"
CORE_REL = "search/d972_k2_total_fibre_roster_producer_v1.py"
CORE_BYTES = 44829
CORE_SHA256 = "cc518377347988c5ad531d0d5c0c5410d2c050a91439ccb27db6414ffae9c499"
OUTPUT_REL = "ci/out/d972_k2_total_fibre_roster_v2_20260825.json"
SCHEMA = "d972-k2-total-fibre-roster-producer/v2"
FINAL_MARKER = "D972_K2_TOTAL_FIBRE_ROSTER_PRODUCER_V2_FINAL"
PREFLIGHT_MARKER = "D972_K2_TOTAL_FIBRE_ROSTER_V2_PREFLIGHT_PASS"
SELFTEST_MARKER = "D972_K2_TOTAL_FIBRE_ROSTER_V2_SELFTEST_PASS"
CORE_SELFTEST_MARKER = "D972_K2_TOTAL_FIBRE_ROSTER_CORE_V1_SELFTEST_PASS"


def fail(code: str, detail: str) -> None:
    raise RuntimeError(f"STATE_STOP {code}: {detail}")


def require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        fail(code, detail)


def pin_core() -> dict:
    path = ROOT / CORE_REL
    require(path.is_file(), "CORE_MISSING", CORE_REL)
    raw = path.read_bytes()
    observed = hashlib.sha256(raw).hexdigest()
    require(
        (len(raw), observed) == (CORE_BYTES, CORE_SHA256),
        "CORE_PIN_MISMATCH",
        f"bytes={len(raw)},sha256={observed}",
    )
    return {"path": CORE_REL, "bytes": len(raw), "sha256": observed}


def load_core() -> tuple[ModuleType, dict]:
    core_pin = pin_core()
    path = ROOT / CORE_REL
    spec = importlib.util.spec_from_file_location("d972_k2_total_fibre_core_v1", path)
    require(spec is not None and spec.loader is not None, "CORE_IMPORT_SPEC", str(path))
    core = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = core
    spec.loader.exec_module(core)
    core.SOURCE_REL = SOURCE_REL
    core.DEFAULT_OUTPUT_REL = OUTPUT_REL
    core.SCHEMA = SCHEMA
    core.FINAL_MARKER = FINAL_MARKER
    core.SELFTEST_MARKER = CORE_SELFTEST_MARKER
    return core, core_pin


def roof_gy(fixed: ModuleType, modulus: int) -> tuple:
    """Compact word-key convention: y=(sr,r,sr), decoded as r^-1 s."""
    return (
        ((modulus - 1) % modulus, 1),
        (1 % modulus, 0),
        ((modulus - 1) % modulus, 1),
    )


def eval_roof_word_g(
    fixed: ModuleType, word: Iterable[int], modulus: int
) -> tuple:
    out = fixed.gid()
    x = fixed.gx(modulus)
    y = roof_gy(fixed, modulus)
    for letter in word:
        require(abs(int(letter)) in (1, 2), "ROOF_WORD_ALPHABET", repr(letter))
        value = x if abs(int(letter)) == 1 else y
        if int(letter) < 0:
            value = fixed.ginv(value, modulus)
        out = fixed.gmul(out, value, modulus)
    return out


def install_replay_dispatch(core: ModuleType) -> None:
    original_loader = core.load_fixed_producer

    def repaired_loader() -> ModuleType:
        fixed = original_loader()
        original_eval = fixed.eval_word_g

        def dispatched_eval(word: Iterable[int], modulus: int) -> tuple:
            if modulus == 9:
                return eval_roof_word_g(fixed, word, modulus)
            return original_eval(word, modulus)

        fixed._k2_v1_eval_word_g = original_eval
        fixed.eval_word_g = dispatched_eval
        return fixed

    core.load_fixed_producer = repaired_loader


def install_result_metadata(core: ModuleType, core_pin: dict) -> None:
    original_validate = core.validate_result

    def augmented_validate(result: dict, *args: object, **kwargs: object) -> None:
        # The same validator is used on tiny selftest fixtures. Only a full
        # artifact has input_pins/conventions and receives producer metadata.
        if result.get("schema") == SCHEMA and "input_pins" in result:
            require(
                all(pin.get("path") != CORE_REL for pin in result["input_pins"]),
                "CORE_PIN_DUPLICATE",
                CORE_REL,
            )
            result["input_pins"].append(core_pin)
            result["producer"]["adapter_core"] = core_pin
            result["producer"]["lineage"] = (
                "v2 convention-repair adapter over pinned v1 producer; "
                "producer-side and not independent"
            )
            result["claim_cover"]["claim_id"] = (
                "K2-TOTAL-FIBRE-ROSTER-OVER-X-V2"
            )
            result["conventions"]["frozen_roof_target_word_replay"] = (
                "G9 only: x=((1,0),(0,1),(0,1)), "
                "y=((-1,1),(1,0),(-1,1)); compact permutation word-key convention"
            )
            result["conventions"]["K2_source_law_unchanged"] = (
                "G36 and source-word replay retain fixed v1 "
                "y=((1,1),(1,0),(1,1))"
            )
            result["repair_v2"] = {
                "failed_GHA_run": 32810928194,
                "v1_failure": "STATE_STOP TARGET_WORD_REPLAY: 81",
                "first_mismatch_zero_based": 81,
                "v1_G9_word_mismatch_count_over_972": 810,
                "v2_roof_word_mismatch_count_over_972": 0,
                "PSL_word_mismatch_count_over_972": 0,
                "scope": "target artifact word authentication only",
                "K2_predicate_or_reduction_law_changed": False,
            }
            result["destructive_controls"]["full_run_fail_closed"].append(
                "all 972 compact-convention target word replays"
            )
        original_validate(result, *args, **kwargs)

    core.validate_result = augmented_validate


def configure_core() -> tuple[ModuleType, dict]:
    core, core_pin = load_core()
    install_replay_dispatch(core)
    install_result_metadata(core, core_pin)
    return core, core_pin


def replay_preflight(core: ModuleType) -> dict:
    _, _, words_artifact, _, _ = core.authenticate_inputs()
    fixed = core.load_fixed_producer()
    rows = words_artifact["rows"]
    old_mismatches: list[int] = []
    roof_mismatches: list[int] = []
    psl_mismatches: list[int] = []
    original_eval = fixed._k2_v1_eval_word_g
    for index, row in enumerate(rows):
        word = tuple(map(int, row[2]))
        target_g9 = core.decode_g9(row[1][1])
        target_p = core.decode_perm(row[1][2])
        if original_eval(word, 9) != target_g9:
            old_mismatches.append(index)
        if fixed.eval_word_g(word, 9) != target_g9:
            roof_mismatches.append(index)
        if fixed.eval_word_perm(word) != target_p:
            psl_mismatches.append(index)
    require(len(rows) == 972, "PREFLIGHT_TARGET_COUNT", str(len(rows)))
    require(
        old_mismatches and old_mismatches[0] == 81 and len(old_mismatches) == 810,
        "PREFLIGHT_V1_DIAGNOSIS",
        repr((old_mismatches[:3], len(old_mismatches))),
    )
    require(not roof_mismatches, "PREFLIGHT_ROOF_REPLAY", repr(roof_mismatches[:3]))
    require(not psl_mismatches, "PREFLIGHT_PSL_REPLAY", repr(psl_mismatches[:3]))
    return {
        "targets": len(rows),
        "v1_g9_mismatches": len(old_mismatches),
        "first_v1_mismatch": old_mismatches[0],
        "v2_roof_g9_mismatches": len(roof_mismatches),
        "psl_mismatches": len(psl_mismatches),
    }


def preflight() -> None:
    core, core_pin = configure_core()
    result = replay_preflight(core)
    print(
        f"{PREFLIGHT_MARKER} targets={result['targets']} "
        f"v1_g9_mismatches={result['v1_g9_mismatches']} "
        f"first_v1_mismatch={result['first_v1_mismatch']} "
        f"v2_roof_g9_mismatches={result['v2_roof_g9_mismatches']} "
        f"psl_mismatches={result['psl_mismatches']} "
        f"core_sha256={core_pin['sha256']}"
    )


def selftest() -> None:
    core, core_pin = configure_core()
    core.selftest()
    result = replay_preflight(core)
    fixed = core.load_fixed_producer()
    require(
        eval_roof_word_g(fixed, (2,), 9)
        != fixed._k2_v1_eval_word_g((2,), 9),
        "SELFTEST_CONVENTION_MUTANT",
        "roof y and fixed K2 y unexpectedly coincide",
    )
    print(
        f"{SELFTEST_MARKER} targets={result['targets']} "
        f"v1_g9_mismatches={result['v1_g9_mismatches']} "
        f"first_v1_mismatch={result['first_v1_mismatch']} "
        f"v2_roof_g9_mismatches=0 psl_mismatches=0 "
        f"convention_mutant_rejected=true core_sha256={core_pin['sha256']}"
    )


def execute(output: str) -> None:
    core, _ = configure_core()
    core.execute(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--selftest", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--output", default=OUTPUT_REL)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    if arguments.preflight:
        preflight()
    elif arguments.selftest:
        selftest()
    else:
        execute(arguments.output)
