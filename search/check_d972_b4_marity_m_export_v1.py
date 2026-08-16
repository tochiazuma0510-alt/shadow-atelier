#!/usr/bin/env python3
"""Helper-independent checker for the Phase-A PB3/M exporter artifact."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT = ROOT / "ci" / "out" / "d972_b4_marity_m_export_v1.json"


def load(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    validate(obj, str(path))
    return obj


def validate(obj: dict, source: str = "artifact") -> None:
    if not isinstance(obj, dict):
        raise AssertionError(f"{source}: top-level object required")
    if obj.get("schema") != "d972-b4-marity-m-export/v1":
        raise AssertionError(f"{source}: schema drift")
    if obj.get("status") != "PROVED_M_PB3_TYPED":
        raise AssertionError(f"{source}: status drift")
    if obj.get("source_group") != "PB3" or obj.get("target_group") != "PB3/M":
        raise AssertionError(f"{source}: group type drift")
    presentation = obj.get("presentation")
    if presentation != {
        "name": "B3",
        "generators": ["s1", "s2"],
        "relator": "s1*s2*s1*(s2*s1*s2)^-1",
        "relator_replay": True,
    }:
        raise AssertionError(f"{source}: B3 presentation/relator replay drift")
    components = obj.get("components")
    if not isinstance(components, list) or len(components) != 2:
        raise AssertionError(f"{source}: exactly two components required")
    by_name = {c.get("name"): c for c in components}
    if set(by_name) != {"K^(9)", "N_S4"}:
        raise AssertionError(f"{source}: named component drift")
    expected = {
        "K^(9)": (27, 2916),
        "N_S4": (9, 504),
    }
    for name, (degree, order) in expected.items():
        c = by_name[name]
        if c.get("target_degree") != degree or c.get("target_order") != order:
            raise AssertionError(f"{source}: {name} order/degree drift")
        if c.get("marked_generator_labels") != ["s1", "s2"]:
            raise AssertionError(f"{source}: {name} markings drift")
        images = c.get("generator_images")
        if not isinstance(images, list) or len(images) != 2:
            raise AssertionError(f"{source}: {name} image pair missing")
        for image in images:
            if not isinstance(image, list) or sorted(image) != list(range(1, degree + 1)):
                raise AssertionError(f"{source}: {name} image is not a permutation")
        if c.get("braid_relator_replay") is not True:
            raise AssertionError(f"{source}: {name} relator replay is not true")

    combined = obj.get("combined")
    if not isinstance(combined, dict):
        raise AssertionError(f"{source}: combined object missing")
    if combined.get("target_name") != "M" or combined.get("target_definition") != "K^(9) intersect N_S4":
        raise AssertionError(f"{source}: M definition drift")
    if combined.get("target_degree") != 36 or combined.get("target_order") != 1469664:
        raise AssertionError(f"{source}: M degree/order drift")
    if combined.get("M_ord") != 18 or combined.get("marked_generator_labels") != ["s1", "s2"]:
        raise AssertionError(f"{source}: M markings/order drift")
    if combined.get("generator_names") != ["XM", "YM"]:
        raise AssertionError(f"{source}: XM/YM names missing")
    images = combined.get("generator_images")
    if not isinstance(images, list) or len(images) != 2:
        raise AssertionError(f"{source}: M image pair missing")
    for image in images:
        if not isinstance(image, list) or sorted(image) != list(range(1, 37)):
            raise AssertionError(f"{source}: M image is not a permutation")
    for i in range(2):
        expected_image = by_name["K^(9)"]["generator_images"][i] + [x + 27 for x in by_name["N_S4"]["generator_images"][i]]
        if images[i] != expected_image:
            raise AssertionError(f"{source}: M image is not the lossless 27+9 block sum")
    if combined.get("braid_relator_replay") is not True:
        raise AssertionError(f"{source}: M relator replay is not true")

    proof = obj.get("named_intersection_proof")
    if not isinstance(proof, dict):
        raise AssertionError(f"{source}: named-intersection proof missing")
    if proof.get("status") != "PROVED_BY_COMMON_B3_KERNEL_IDENTITY":
        raise AssertionError(f"{source}: named-intersection proof status drift")
    if proof.get("named_intersection") != "M=K^(9) intersect N_S4":
        raise AssertionError(f"{source}: named-intersection name drift")
    if proof.get("identity") != "ker(delta_M)=ker(q_K9) intersect ker(q_N_S4)":
        raise AssertionError(f"{source}: kernel identity drift")
    if proof.get("component_orders") != [2916, 504] or proof.get("diagonal_order") != 1469664:
        raise AssertionError(f"{source}: proof order anchors drift")
    boundary = obj.get("phase_boundary")
    if not isinstance(boundary, dict) or boundary.get("B4_stable") is not False:
        raise AssertionError(f"{source}: B4_stable must be explicit false")
    if boundary.get("pb4_pc_presentation") != "MISSING" or boundary.get("full_972_fibers") != "MISSING":
        raise AssertionError(f"{source}: missing-dependency gate was weakened")


def selftest() -> None:
    # A synthetic valid artifact is unnecessary: the static contract is tested
    # against the committed exporter shape and two fail-closed mutations.
    fixture = {
        "schema": "d972-b4-marity-m-export/v1",
        "status": "PROVED_M_PB3_TYPED",
        "source_group": "PB3", "target_group": "PB3/M",
        "presentation": {"name": "B3", "generators": ["s1", "s2"], "relator": "s1*s2*s1*(s2*s1*s2)^-1", "relator_replay": True},
        "components": [
            {"name": "K^(9)", "target_degree": 27, "target_order": 2916, "marked_generator_labels": ["s1", "s2"], "generator_images": [list(range(1, 28)), list(range(1, 28))], "braid_relator_replay": True},
            {"name": "N_S4", "target_degree": 9, "target_order": 504, "marked_generator_labels": ["s1", "s2"], "generator_images": [list(range(1, 10)), list(range(1, 10))], "braid_relator_replay": True},
        ],
        "combined": {"target_name": "M", "target_definition": "K^(9) intersect N_S4", "target_degree": 36, "target_order": 1469664, "M_ord": 18, "marked_generator_labels": ["s1", "s2"], "generator_names": ["XM", "YM"], "generator_images": [list(range(1, 28)) + list(range(28, 37)), list(range(1, 28)) + list(range(28, 37))], "braid_relator_replay": True},
        "named_intersection_proof": {"status": "PROVED_BY_COMMON_B3_KERNEL_IDENTITY", "named_intersection": "M=K^(9) intersect N_S4", "identity": "ker(delta_M)=ker(q_K9) intersect ker(q_N_S4)", "component_orders": [2916, 504], "diagonal_order": 1469664},
        "phase_boundary": {"B4_stable": False, "pb4_pc_presentation": "MISSING", "full_972_fibers": "MISSING"},
    }
    validate(fixture, "selftest fixture")
    bad = copy.deepcopy(fixture)
    bad["phase_boundary"]["B4_stable"] = True
    try:
        validate(bad, "B4 mutation")
    except AssertionError:
        pass
    else:
        raise AssertionError("B4_stable mutation accepted")
    bad = copy.deepcopy(fixture)
    bad["combined"]["generator_images"][0][27] = 1
    try:
        validate(bad, "block mutation")
    except AssertionError:
        pass
    else:
        raise AssertionError("block-sum mutation accepted")
    print("D972_B4_MARITY_M_EXPORT_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--check", type=Path, default=DEFAULT_ARTIFACT)
    args = parser.parse_args()
    if args.selftest:
        selftest()
    else:
        load(args.check)
        print("D972_B4_MARITY_M_EXPORT_V1_CHECK_PASS", args.check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
