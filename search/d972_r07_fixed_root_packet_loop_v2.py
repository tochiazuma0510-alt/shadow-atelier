#!/usr/bin/env python3
"""Fixed44 primal packet and bounded changing-separator root loop: candidate.

Task950. Immutable Task904 + seed30 + seed34 are retained premises.
The two saved materializer generations retain their distinct rho2 metadata.
The packet contains complete raw-seed-minus-fixed-canonical-P1 defects.
Only the new packet and new pivot prefix are computed here. ROOT_SEEDS_ZERO
annihilates this fixed list; it is not an image-saturation certificate.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import time
from typing import Any
import uuid

import numpy as np


SCHEMA = "d972.r07.fixed-root-packet-loop.v2"
SEARCH = Path(__file__).resolve().parent
ZERO_HEAD = "0" * 64
NSEEDS, P1_ROWS = 44, 8059
TOP_WIDTH, TOP_BYTES = 36288, 9072
LOWER_WIDTH, PHYSICAL_WIDTH, PHYSICAL_BYTES = 96776, 48384, 12096
START_RANK, START_GENERATION = 1356, 8061
START_HEAD = "d467e4e60b8bff88272cddd4b01d630d763e863b4500015c7c6c077b23ddf26b"
START_LAMBDA = "f7406d70211ab02acf08a895d127d17e7dab179454916a90ea40cb11152e12dd"
START_TARGET = "46a6b8281587a13236fd9af00eab9825a2d956dd878613af14182b5f9ae94c49"
MODULE_PINS = {
    "d972_r07_actual_root_seed_materializer_v3.py": "36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332",
    "d972_r07_rank1355_root_seed_scalars_v1.py": "973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb",
    "d972_r07_actual_grade2_root_scalar_batch_v2.py": "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856",
    "d972_r07_targeted_grade2_owner_generated_join_v15.py": "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632",
}
DATA_PINS = {
    "scratchpad/fuda1_a0_rmax_data.g": {"bytes": 4709,
        "sha256": "625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"},
    "scratchpad/a0_paper_words_v1.json": {"bytes": 115928,
        "sha256": "90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"},
}
SEED34_ARTIFACT = {
    "run": 33956437467, "attempt": 1,
    "head": "b9ae78b0950b186463849c3ec874f6474f359851", "id": 9966542166,
    "name": "d972-r07-actual-root-seed-materializer-v3-candidate-33956437467-1",
    "bytes": 984053,
    "sha256": "sha256:a4cb9f63a470636628d9ef02a5b5e55d90fe3b0a2c70f2012d32c9517d87defc",
}
SEED34_FILES = {
    "output/manifest.json": (1813, "0acac7c5cbe15375c25ccc4c9109dad449ed38e60898b68ca0b7b3cda4fcda52"),
    "output/result.json": (3135681, "3a8357365f4e5f3f7d281b811d36d49e4f334cbec3828c82833ae1b1d5af0242"),
    "output/instruction.json": (147200, "790af5b3556c78ec2b81f45602aa50779435f46ddde57a8e5b5414566813dc7f"),
    "checker-result.json": (1570, "0e514b8833c37333ec9643775f5d752958a1a1a35dd6673ff65fdb620b6a556c"),
    "source-receipt.json": (1304, "0a037063a25b161566791638e025d301bc2275b50f4896176897271f528f9451"),
}
LAYOUT_BASE_FILES = {
    "state/manifest.json": (7780, "d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b"),
    "output/result.json": (457791, "d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968"),
    "checker-result.json": (515, "2cad883205a5a1dc6e8795567004e071c3a7868351cf1d801727a695b43aa433"),
}
LAYOUT_SEED30_FILES = {
    "output/manifest.json": (1810, "7673b3c0ba5b23080ab51490e1ab9e72fe92f8afe313bf1b465d3892e8836f7d"),
    "output/result.json": (2903961, "60e47f7c673942611647a69087d29bd0223e40394144b43aae9e0f55da10fb8b"),
    "output/instruction.json": (143336, "64396583ac9f991af40cd9997310a308c18facc0d2aaca336e2b508473b488d5"),
    "checker-result.json": (1383, "d9368b9ace442ef0d4bfb2099ace1c982b995eb428bfc8d46920633a198c4491"),
    "source-receipt.json": (1632, "f8932ca0b08d6dd7a42fb2560ee5c30adffe39c18d5eafd40a9d1e18ac3a6b30"),
}
RHO2_IDENTITY = {
    "artifact": {"run": 33839962829, "attempt": 1,
        "head": "17a8439c766d92719d7ae7d35846ea444da598fa", "id": 9925190479,
        "name": "task640-fresh-rho2-v17-33839962829-1", "bytes": 6049643,
        "sha256": "sha256:01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4"},
    "manifest_sha256": "55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488",
    "packed_sha256": "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e",
}
RHO2_PREMISE_FLAG = "target_derivation_accepted_as_premise"
SCOPE = {"characters": [0, 1, 2, 3], "seeds": list(range(44)),
         "order": "character-major/seed0-through43", "declared_pair_count": 176,
         "max_appends": 176, "actor_origins_executed": 0, "orbit_rows_executed": 0}
CLAIMS = {"FIXED_ROOT_PACKET_LOOP_CANDIDATE": True,
          "GRADE2_MEMBER": "NOT_DECIDED", "GRADE2_NONMEMBER": "NOT_DECIDED",
          "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED",
          "COFINAL_LIFT": "NOT_DECLARED", "FAKE": "NOT_DECLARED",
          "IHARA": "NOT_DECLARED", "verified": False}
EVENT_ORDER = "old-source,then-target/source,stored-term-order"
STARTED = time.monotonic()
STOP_REQUESTED = False
DEADLINE: float | None = None


class ResourceStop(RuntimeError):
    pass


def check_deadline(phase: str) -> None:
    if STOP_REQUESTED or (DEADLINE is not None and time.monotonic() >= DEADLINE):
        raise ResourceStop(phase)


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(kind: str, body: dict[str, Any]) -> dict[str, Any]:
    require("sha256" not in body and "schema" not in body, "seal_reserved_keys")
    unsigned = {"schema": SCHEMA + "." + kind, **body}
    return {**unsigned, "sha256": sha(canonical(unsigned))}


def sealed_ok(value: Any, kind: str | None = None) -> bool:
    return (isinstance(value, dict) and
            (kind is None or value.get("schema") == SCHEMA + "." + kind) and
            value.get("sha256") == sha(canonical(
                {key: item for key, item in value.items() if key != "sha256"})))


def progress(phase: str, **fields: Any) -> None:
    print(json.dumps({"phase": phase, "elapsed_seconds": round(time.monotonic() - STARTED, 3),
                      **fields}, sort_keys=True), file=sys.stderr, flush=True)
    if phase.startswith("packet-") and phase not in ("packet-durable", "packet-resumed"):
        check_deadline(phase)


def receipt(name: str, raw: bytes) -> dict[str, Any]:
    return {"file": name, "bytes": len(raw), "sha256": sha(raw)}


def read_json(path: Path, *, kind: str | None = None) -> Any:
    require(path.is_file() and not path.is_symlink() and path.stat().st_size <= 1 << 28,
            "json_regular_file:" + path.name)
    raw = path.read_bytes()
    value = json.loads(raw.decode("ascii"))
    require(canonical(value) == raw and (kind is None or sealed_ok(value, kind)),
            "canonical_sealed_json:" + path.name)
    return value


def base_parent_layout(manifest: Any, result: Any) -> dict[str, Any]:
    """The original target relation remains an exact accepted premise."""
    manifest_pin = LAYOUT_BASE_FILES["state/manifest.json"][1]
    target = result["target_reduction"]
    require(result["schema"] == "d972.r07.physical-state.Separator.v1" and
            target["schema"] == "d972.r07.physical-state.target-reduction.v1" and
            manifest["schema"] == "d972.r07.physical-state.v1", "layout_base_schemas")
    require(result["state_manifest_sha256"] == manifest_pin and
            target["state_head"] == manifest["instructions"]["final_head"] and
            target["state_rank"] == manifest["rank"] == 1354 and
            target["state_generation"] == manifest["generation"] == 8059,
            "layout_base_target_manifest")
    require(target["rho2_sha256"] == RHO2_IDENTITY["packed_sha256"], "layout_base_rho2_identity")
    require(sha(canonical(manifest)) == manifest_pin and
            sha(canonical(result)) == LAYOUT_BASE_FILES["output/result.json"][1], "layout_base_exact_pins")
    return {"result_schema": result["schema"], "target_schema": target["schema"],
        "state_manifest_sha256": manifest_pin, "result_sha256": sha(canonical(result)),
        "target_sha256": sha(canonical(target)), "rho2_sha256": target["rho2_sha256"]}


def saved_parent_layout(base_manifest: Any, base_result: Any, manifest: Any,
                        result: Any, payloads: dict[str, bytes]) -> dict[str, Any]:
    """One strict schema-aware join shared by actual production and metadata CLI.

    No absent key is synthesized. Legacy admission depends on its exact saved
    result/target/payload identity and on the separately named DERIVED chain.
    """
    base = base_parent_layout(base_manifest, base_result)
    target, rho2 = result["target"], result["parents"]["rho2"]
    schema = result["schema"]
    require(schema in ("d972.r07.actual-seed30-materializer.v1.result",
                       "d972.r07.actual-root-seed-materializer.v3.result"), "layout_materializer_schema")
    legacy = schema == "d972.r07.actual-seed30-materializer.v1.result"
    role = "seed30" if legacy else "seed34"
    pins = LAYOUT_SEED30_FILES if legacy else SEED34_FILES
    expected_target = ("d972.r07.actual-seed30-materializer.v1.target-update" if legacy else
                       "d972.r07.actual-root-seed-materializer.v3.target-update")
    require(target["schema"] == expected_target, "layout_target_schema")
    if legacy:
        require(RHO2_PREMISE_FLAG not in rho2, "layout_legacy_flag_absent")
        require(set(rho2) == set(RHO2_IDENTITY), "layout_legacy_rho2_keys")
    else:
        require(RHO2_PREMISE_FLAG in rho2 and rho2[RHO2_PREMISE_FLAG] is True,
                "layout_v3_explicit_premise_flag")
        require(set(rho2) == set(RHO2_IDENTITY) | {RHO2_PREMISE_FLAG}, "layout_v3_rho2_keys")
    identity = {key: copy.deepcopy(rho2[key]) for key in RHO2_IDENTITY}
    require(identity == RHO2_IDENTITY and identity["packed_sha256"] == base["rho2_sha256"],
            "layout_original_rho2_identity")
    parent = result["parents"]["state"]
    if legacy:
        require(parent["manifest_sha256"] == base["state_manifest_sha256"] and
                target["parent_result_sha256"] == base["result_sha256"] and
                target["parent_target_sha256"] == base["target_sha256"] and
                target["old_remainder_sha256"] == sha(bytes.fromhex(base_result["target_reduction"]["remainder"])),
                "layout_legacy_base_target_join")
    else:
        require(parent["base"]["manifest_sha256"] == base["state_manifest_sha256"] and
                parent["base"]["target_sha256"] == base["target_sha256"] and
                parent["manifest_sha256"] == LAYOUT_SEED30_FILES["output/manifest.json"][1] and
                target["parent_result_sha256"] == LAYOUT_SEED30_FILES["output/result.json"][1] and
                target["parent_target_sha256"] == parent["delta"]["target_sha256"] and
                target["old_remainder_sha256"] == parent["delta"]["target_remainder"]["sha256"],
                "layout_v3_base_seed30_target_join")
    require(sealed_ok(manifest) and sealed_ok(result) and sealed_ok(target) and
            sha(canonical(manifest)) == pins["output/manifest.json"][1] and
            sha(canonical(result)) == pins["output/result.json"][1], "layout_saved_exact_pins")
    require(set(payloads) == {item["file"] for item in manifest["files"]} and
            all(receipt(item["file"], payloads[item["file"]]) == item for item in manifest["files"]),
            "layout_saved_payload_pins")
    require(sha(payloads["target-remainder.bin"]) == target["remainder_sha256"] and
            sha(payloads["physical-normalized.bin"]) == result["pivot"]["normalized_sha256"] and
            payloads["result.json"] == canonical(result), "layout_saved_target_payload_join")
    return {"role": role, "result_schema": schema, "target_schema": target["schema"],
        "manifest_sha256": pins["output/manifest.json"][1],
        "result_sha256": pins["output/result.json"][1], "target_sha256": sha(canonical(target)),
        "rho2_identity": identity, "target_derivation_flag_present": not legacy,
        "target_derivation_flag_value": None if legacy else True,
        "admission": "exact-accepted-legacy-target-chain" if legacy else "exact-accepted-v3-explicit-target-premise",
        "payloads": {"source_d_sha256": sha(payloads["source-d.bin"]),
            "physical_normalized_sha256": sha(payloads["physical-normalized.bin"]),
            "target_remainder_sha256": sha(payloads["target-remainder.bin"])}}


def parent_layout_receipt(base_manifest: Any, base_result: Any, deltas: list[Any]) -> dict[str, Any]:
    require([item["role"] for item in deltas] == ["seed30", "seed34"], "layout_parent_order")
    return seal("parent-layout", {"base": base_parent_layout(base_manifest, base_result),
        "deltas": deltas, "derivation_mode": "derived", "original_rho2_directly_read": False,
        "old_target_history_replayed": False})


def layout_fixed(root: Path, relative: str, pin: tuple[int, str]) -> bytes:
    """Byte/JSON fixture reader; never imports the numerical lineage."""
    require(relative and not Path(relative).is_absolute() and ".." not in Path(relative).parts and
            ":" not in relative and "\\" not in relative, "layout_relative_path")
    base = root.resolve()
    path = base
    for part in Path(relative).parts:
        path /= part
        require(not path.is_symlink(), "layout_fixture_symlink")
    require(path.is_file() and base in path.resolve().parents and path.stat().st_size == pin[0] and
            pin[0] <= 1 << 28, "layout_fixture_size")
    raw = path.read_bytes()
    require(len(raw) == pin[0] and sha(raw) == pin[1], "layout_fixture_digest")
    return raw


def layout_objects(root: Path, pins: dict[str, tuple[int, str]]) -> dict[str, Any]:
    objects = {}
    for name, pin in pins.items():
        raw = layout_fixed(root, name, pin)
        value = json.loads(raw.decode("ascii"))
        require(canonical(value) == raw, "layout_fixture_canonical")
        objects[name] = value
    require(objects["checker-result.json"]["status"] == "PASS", "layout_accepted_checker")
    return objects


def parent_layout_selftest(args: argparse.Namespace) -> dict[str, Any]:
    base = layout_objects(args.state_root, LAYOUT_BASE_FILES)
    base_manifest, base_result = base["state/manifest.json"], base["output/result.json"]
    fixtures = [{"role": "base", "run": 33891714539, "attempt": 1, "artifact_id": 9944214057,
        "files": [{"file": name, "bytes": pin[0], "sha256": pin[1]}
                  for name, pin in sorted(LAYOUT_BASE_FILES.items())]}]
    bundles = []
    deltas = []
    for role, root, pins, run, artifact in (
        ("seed30", args.delta_root, LAYOUT_SEED30_FILES, 33946247365, 9963533999),
        ("seed34", args.seed34_root, SEED34_FILES, 33956437467, 9966542166)):
        objects = layout_objects(root, pins)
        manifest, result = objects["output/manifest.json"], objects["output/result.json"]
        require(set(manifest["file_roster"]) == {path.name for path in (root / "output").iterdir()},
                "layout_actual_output_roster")
        payloads = {item["file"]: layout_fixed(root / "output", item["file"],
                    (item["bytes"], item["sha256"])) for item in manifest["files"]}
        deltas.append(saved_parent_layout(base_manifest, base_result, manifest, result, payloads))
        bundles.append((manifest, result, payloads))
        fixtures.append({"role": role, "run": run, "attempt": 1, "artifact_id": artifact,
            "files": [{"file": name, "bytes": pin[0], "sha256": pin[1]} for name, pin in sorted(pins.items())]})
    layout = parent_layout_receipt(base_manifest, base_result, deltas)
    v3_manifest, v3_result, v3_payloads = bundles[1]
    rejected_cases = []
    cases = (("v3-flag-false", "layout_v3_explicit_premise_flag"),
             ("v3-flag-missing", "layout_v3_explicit_premise_flag"),
             ("rho2-packed-identity", "layout_original_rho2_identity"),
             ("unexpected-parent-schema", "layout_materializer_schema"),
             ("base-target-manifest", "layout_base_target_manifest"))
    for name, wanted_reason in cases:
        changed_result = copy.deepcopy(v3_result)
        changed_base = copy.deepcopy(base_result)
        if name == "v3-flag-false":
            changed_result["parents"]["rho2"][RHO2_PREMISE_FLAG] = False
        elif name == "v3-flag-missing":
            del changed_result["parents"]["rho2"][RHO2_PREMISE_FLAG]
        elif name == "rho2-packed-identity":
            changed_result["parents"]["rho2"]["packed_sha256"] = ZERO_HEAD
        elif name == "unexpected-parent-schema":
            changed_result["schema"] = "d972.r07.actual-root-seed-materializer.v99.result"
        else:
            changed_base["state_manifest_sha256"] = ZERO_HEAD
        try:
            saved_parent_layout(base_manifest, changed_base, v3_manifest, changed_result, v3_payloads)
        except RuntimeError as exc:
            require(str(exc) == wanted_reason, "layout_mutation_rejection_reason:" + name)
            rejected_cases.append(name)
        else:
            raise RuntimeError("layout_mutation_accepted:" + name)
    return {"schema": SCHEMA + ".parent-layout-selftest", "status": "PASS", "metadata_only": True,
        "fixtures": fixtures, "parent_layout": layout, "rejected_cases": rejected_cases,
        "cross_checked": False, "verified": False}


def sync_directory(path: Path) -> None:
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def write_atomic(root: Path, name: str, raw: bytes, *, replace: bool = False) -> dict[str, Any]:
    require(Path(name).name == name and name not in ("", ".", "..") and
            not root.is_symlink() and not (root / name).is_symlink(), "output_path")
    target = root / name
    require(replace or not target.exists(), "fresh_file:" + name)
    temporary = root / ("." + name + ".pending-" + uuid.uuid4().hex)
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, target)
    sync_directory(root)
    return receipt(name, raw)


def write_json(root: Path, name: str, value: Any, *, replace: bool = False) -> dict[str, Any]:
    return write_atomic(root, name, canonical(value), replace=replace)


def publish_directory(pending: Path, final: Path) -> None:
    require(pending.parent == final.parent and not pending.is_symlink() and
            pending.is_dir() and not final.exists(), "publish_new_directory")
    sync_directory(pending)
    os.replace(pending, final)
    sync_directory(final.parent)


def dependencies() -> tuple[Any, Any, Any]:
    check_deadline("dependency-loading")
    for filename, wanted in MODULE_PINS.items():
        path = SEARCH / filename
        require(path.is_file() and not path.is_symlink() and sha(path.read_bytes()) == wanted,
                "accepted_module_pin:" + filename)
    for filename, pin in DATA_PINS.items():
        path = SEARCH.parent / filename
        require(path.is_file() and not path.is_symlink() and path.stat().st_size == pin["bytes"] and
                sha(path.read_bytes()) == pin["sha256"], "raw_source_data_pin:" + filename)
    if str(SEARCH) not in sys.path:
        sys.path.insert(0, str(SEARCH))

    def load(filename: str, name: str) -> Any:
        spec = importlib.util.spec_from_file_location(name, SEARCH / filename)
        require(spec is not None and spec.loader is not None, "module_spec")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

    materializer = load("d972_r07_actual_root_seed_materializer_v3.py", "task945_own_v3")
    descriptors = load("d972_r07_rank1355_root_seed_scalars_v1.py", "task945_own_descriptors")
    root_v2 = materializer.dependencies()
    check_deadline("dependency-loading")
    return materializer, root_v2, descriptors


def load_saved_delta(m: Any, root: Path, pins: dict[str, tuple[int, str]],
                     state: dict[str, Any], seed: int, wanted_head: str,
                     wanted_lambda: str, wanted_target: str) -> dict[str, Any]:
    """Authenticate and attach one accepted saved delta; do not re-eliminate it."""
    objects = {name: m.read_json_exact(m.safe_file(root, name), *pin)[0]
               for name, pin in pins.items()}
    manifest, result = objects["output/manifest.json"], objects["output/result.json"]
    instruction, checked = objects["output/instruction.json"], objects["checker-result.json"]
    require(all(m.sealed_ok(obj) for obj in (manifest, result, result["pivot"], result["target"])) and
            manifest["mode"] == "parent-plus-one-pivot-delta" and
            manifest["parent_state_head"] == state["head"] and
            manifest["parent_state_manifest_sha256"] == state["manifest_sha256"] and
            manifest["state_head"] == wanted_head and
            manifest["rank_before"] == state["rank"] and
            manifest["rank_after"] == state["rank"] + 1 and
            manifest["terminal"] == result["kind"] == checked["kind"] == "Separator" and
            checked["status"] == "PASS" and checked["manifest_sha256"] == pins["output/manifest.json"][1] and
            checked["result_sha256"] == pins["output/result.json"][1] and
            checked["instruction_sha256"] == pins["output/instruction.json"][1] and
            checked["state_head"] == wanted_head and checked["rank_after"] == state["rank"] + 1 and
            checked["new_pivots"] == 1 and checked["old_state_derivation_premise"] is True and
            all(obj["verified"] is False and obj["cross_checked"] is False
                for obj in (manifest, result, checked, objects["source-receipt.json"])),
            "saved_delta_authority:" + str(seed))
    parent = result["parents"]["state"]
    require(parent["head"] == state["head"] and parent["rank"] == state["rank"] and
            parent["generation"] == state["generation"] and
            parent["manifest_sha256"] == state["manifest_sha256"] and
            result["target"]["parent_target_sha256"] == state["target_sha256"] and
            result["target"]["parent_result_sha256"] == state["result_sha256"],
            "saved_delta_parent_target_join:" + str(seed))
    if seed == 30:
        require(parent["artifact"] == m.STATE_ARTIFACT and
                parent["physical_sha256"] == m.STATE_PHYSICAL_SHA256 and
                parent["companion_sha256"] == m.STATE_COMPANION_SHA256 and
                parent["instruction_sha256"] == m.STATE_INSTRUCTION_SHA256 and
                parent["checker_sha256"] == state["base_checker_sha256"], "seed30_base_join")
        state["base_parent"] = parent
    else:
        require(parent["mode"] == "immutable-state-plus-one-accepted-delta" and
                parent["base"] == state["base_parent"] and
                parent["delta"]["artifact"] == m.DELTA_ARTIFACT and
                parent["delta"]["files"] == [
                    {"file": name, "bytes": pin[0], "sha256": pin[1]}
                    for name, pin in sorted(m.DELTA_FILES.items())] and
                parent["delta"]["target_sha256"] == state["target_sha256"] and
                parent["delta"]["physical"]["sha256"] == sha(state["rows"][-1]),
                "seed34_base_seed30_join")
    output = root / "output"
    require(set(manifest["file_roster"]) == {p.name for p in output.iterdir()}, "saved_delta_roster")
    payloads = {item["file"]: m.read_exact(m.safe_file(output, item["file"]),
                item["bytes"], item["sha256"]) for item in manifest["files"]}
    state["saved_parent_layouts"].append(saved_parent_layout(
        state["layout_base_manifest"], state["layout_base_result"], manifest, result, payloads))
    unsigned = {key: value for key, value in instruction.items() if key != "rolling_sha256"}
    lead = instruction["lead"]
    require(instruction["predecessor"] == state["head"] and
            sha(bytes.fromhex(state["head"]) + canonical(unsigned)) ==
            instruction["rolling_sha256"] == wanted_head and
            instruction["offer"] == state["generation"] and
            instruction["generation"] == result["pivot"]["generation_after"] == state["generation"] + 1 and
            instruction["rank"] == result["pivot"]["rank_after"] == state["rank"] + 1 and
            instruction["physical_offset"] == state["rank"] * PHYSICAL_BYTES and
            instruction["delta_physical_offset"] == 0 and
            instruction["sigma"] == result["pivot"]["scale"] and
            lead == result["pivot"]["lead"] and lead not in state["leads"] and
            result["pivot"]["head_after"] == result["target"]["state_head"] == wanted_head and
            result["raw_seed"]["seed"] == seed and result["raw_seed"]["character"] == 0,
            "saved_delta_append_join")
    normalized, target, lam_raw = (payloads[name] for name in
                                  ("physical-normalized.bin", "target-remainder.bin", "lambda.bin"))
    require(sha(normalized) == result["pivot"]["normalized_sha256"] == instruction["physical"]["sha256"] and
            sha(target) == result["target"]["remainder_sha256"] == wanted_target and
            sha(lam_raw) == result["separator"]["lambda_sha256"] == wanted_lambda,
            "saved_delta_payload_join")
    row, target_dense, lam = (m.unpack(raw, PHYSICAL_WIDTH) for raw in (normalized, target, lam_raw))
    require(row[lead] == 1 and target_dense[lead] == 0 and
            all(row[index] == target_dense[index] == 0 for index in state["leads"]) and
            m.dot(lam, row) == 0 and m.dot(lam, target_dense) == 1 and
            m.dot(lam, m.unpack(state["target_raw"], PHYSICAL_WIDTH)) == 1,
            "saved_delta_direct_rows")
    state["records"].append({"offer": instruction["offer"], "lead": lead,
        "physical_offset": instruction["physical_offset"], "rank": instruction["rank"],
        "rolling_sha256": wanted_head})
    state["rows"].append(normalized)
    state["leads"].append(lead)
    state["previous_target_raw"] = state["target_raw"]
    state.update({"head": wanted_head, "generation": state["generation"] + 1,
        "rank": state["rank"] + 1, "target_raw": target, "lambda_raw": lam_raw,
        "lambda": lam, "target_sha256": sha(canonical(result["target"])),
        "result_sha256": pins["output/result.json"][1],
        "manifest_sha256": pins["output/manifest.json"][1]})
    state["accepted_target_derivation_parents"].append({"role": "seed" + str(seed),
        "manifest_sha256": state["manifest_sha256"], "result_sha256": state["result_sha256"],
        "target_sha256": state["target_sha256"], "state_head": wanted_head})
    state["saved_sources"][seed] = payloads["source-d.bin"]
    state["saved_parents"].append(result["parents"])
    return state


def load_start(m: Any, args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    old = m.validate_old_state(args.state_root)
    check_deadline("accepted-base-loading")
    base_result, _ = m.read_json_exact(m.safe_file(args.state_root, "output/result.json"),
                                      *m.STATE_RESULT_PIN)
    require(m.DELTA_FILES == LAYOUT_SEED30_FILES, "layout_legacy_pin_source_join")
    target_raw = bytes.fromhex(old["target"]["remainder"])
    m.validate_packed(target_raw, PHYSICAL_WIDTH)
    state = {"rows": old["packed_rows"], "records": old["records"], "leads": old["leads"],
        "rank": m.STATE_RANK, "generation": m.STATE_GENERATION, "head": m.STATE_HEAD,
        "target_raw": target_raw, "target_sha256": old["target_sha256"],
        "result_sha256": old["result_sha256"], "manifest_sha256": old["manifest_sha256"],
        "base_checker_sha256": old["checker_sha256"], "saved_sources": {}, "saved_parents": [],
        "layout_base_manifest": old["manifest"], "layout_base_result": base_result,
        "saved_parent_layouts": [],
        "accepted_target_derivation_parents": [{"role": "base",
            "manifest_sha256": old["manifest_sha256"], "result_sha256": old["result_sha256"],
            "target_sha256": old["target_sha256"], "state_head": m.STATE_HEAD}]}
    del old
    load_saved_delta(m, args.delta_root, m.DELTA_FILES, state, 30, m.CURRENT_HEAD,
                     m.CURRENT_LAMBDA_SHA256, m.CURRENT_TARGET_REMAINDER_SHA256)
    check_deadline("accepted-seed30-loading")
    load_saved_delta(m, args.seed34_root, SEED34_FILES, state, 34, START_HEAD, START_LAMBDA, START_TARGET)
    check_deadline("accepted-seed34-loading")
    state["parent_layout"] = parent_layout_receipt(
        state["layout_base_manifest"], state["layout_base_result"], state["saved_parent_layouts"])
    del state["layout_base_manifest"], state["layout_base_result"]
    require(state["rank"] == START_RANK and state["generation"] == START_GENERATION,
            "fixed_rank1356_start")
    state["start_target_raw"] = state["target_raw"]
    state["completed_steps"] = 0
    state["kind"] = "Separator"
    state["step_manifest_sha256"] = None
    m.check_final_separator(state["lambda"], state["rows"],
                            state["previous_target_raw"], state["target_raw"])
    check_deadline("accepted-start-direct-pairings")
    start = seal("start", {"rank": START_RANK, "generation": START_GENERATION,
        "state_head": START_HEAD, "lambda_sha256": START_LAMBDA,
        "target_remainder_sha256": START_TARGET, "base_manifest_sha256": m.STATE_MANIFEST_SHA256,
        "seed30_manifest_sha256": m.DELTA_FILES["output/manifest.json"][1],
        "seed34_manifest_sha256": SEED34_FILES["output/manifest.json"][1],
        "parent_layout": state["parent_layout"],
        "accepted_target_derivation_parents": state["accepted_target_derivation_parents"]})
    return state, start


def owner_and_tables(m: Any, base: Any, descriptors: Any, args: argparse.Namespace,
                     state: dict[str, Any]) -> tuple[dict[str, Any], Any, Any, list[Any]]:
    p1_parent, task554, table_parents = descriptors.pinned_parent_descriptors(base, args)
    p1 = base.validate_p1(p1_parent)
    base.validate_task554(task554)
    tables = []
    for character in range(4):
        table = base.ARITH.read_task712_envelope(table_parents[character], character)
        base.check_table_transpose(table["forward"]["B"], table["adjoint"]["B"])
        tables.append(table)
        check_deadline("task712-table-loading-" + str(character))
    require([layout["role"] for layout in state["saved_parent_layouts"]] == ["seed30", "seed34"],
            "fixed_owner_saved_layout_order")
    for parents, layout in zip(state["saved_parents"], state["saved_parent_layouts"]):
        require(descriptors.without_roots(p1_parent) == parents["p1"] and
                task554["artifacts"] == parents["task554"]["artifacts"] and
                list(base.TASK554_BODY_DIGESTS) == parents["task554"]["body_sha256"] and
                base.TASK712_PARENT == parents["task712"]["artifact"] and
                all(table["manifest_sha256"] == parents["task712"]["manifest_sha256"] for table in tables) and
                parents["rho2"]["packed_sha256"] == m.RHO2_SHA256 and
                {key: parents["rho2"][key] for key in RHO2_IDENTITY} == layout["rho2_identity"],
                "fixed_owner_saved_parent_joins")
    owner = seal("owner", {"formula_id": m.V541_FORMULA_ID, "scope": SCOPE,
        "p1_parent": descriptors.without_roots(p1_parent),
        "task554_parent": descriptors.without_roots(task554),
        "task712_parent": copy.deepcopy(base.TASK712_PARENT),
        "task712_manifest_sha256": [table["manifest_sha256"] for table in tables],
        "word_dictionary_sha256": base.ARITH.WORD_SHA,
        "relator_dictionary_sha256": base.ARITH.WORD_RELATOR_SHA})
    return owner, p1, task554, tables


def collect_relations(m: Any, base: Any, parent: Any) -> tuple[Any, np.ndarray, list[Any]]:
    events: list[list[dict[str, Any]]] = [[] for _ in range(NSEEDS)]
    segments: list[dict[str, Any]] = []

    def append(expression: Any, source: int, target: int | None, seed: int,
               offset: int, body_sha: str) -> None:
        for ordinal, (local, coefficient) in enumerate(expression):
            events[seed].append({"event_id": len(events[seed]),
                "body_role": "prepare-old" if target is None else "new-block",
                "task554_body_sha256": body_sha, "source_character": source,
                "target_character": target, "seed": seed,
                "origin_id": m.ORIGIN_RANGES[source][0] + seed, "term_ordinal": ordinal,
                "local_index": int(local), "global_index": offset + int(local),
                "coefficient": int(coefficient)})

    progress("packet-relations", bodies=0, total=5)
    prepare = base._state_descriptor(parent["prepare"], -1, need_blobs=True)
    for source, old in enumerate(prepare["body"]["old_blocks"]):
        for seed in range(NSEEDS):
            append(old["record"]["seed_reductions"][seed], source, None, seed,
                   m.OLD_OFFSETS[source], prepare["body_sha256"])
        segments.append({"kind": "old", "owner": source, "start": m.OLD_OFFSETS[source],
            "rows": m.OLD_RANKS[source], "root": prepare["root"],
            "body_sha256": prepare["body_sha256"],
            "lower_descriptor": copy.deepcopy(old["lower_basis_blob"]),
            "grade_descriptor": copy.deepcopy(old["lifted_grade_blob"])})
    del old, prepare
    for target in range(4):
        progress("packet-relations", bodies=target + 1, total=5)
        block = base._state_descriptor(parent["blocks"][target], target, need_blobs=True)
        for source in range(4):
            for seed in range(NSEEDS):
                append(block["body"]["origin_reductions"][m.ORIGIN_RANGES[source][0] + seed],
                       source, target, seed, m.NEW_OFFSETS[target], block["body_sha256"])
        segments.append({"kind": "new", "owner": target, "start": m.NEW_OFFSETS[target],
            "rows": m.NEW_RANKS[target], "root": block["root"],
            "body_sha256": block["body_sha256"],
            "basis_descriptor": copy.deepcopy(block["body"]["basis_blob"])})
        del block
    require([item["start"] for item in segments] == [*m.OLD_OFFSETS, *m.NEW_OFFSETS] and
            sum(item["rows"] for item in segments) == P1_ROWS, "packet_segments")
    # All literal contributions exist and are sealed before numerical collection.
    heads = []
    for seed_events in events:
        rolling = ZERO_HEAD
        for event in seed_events:
            rolling = sha(bytes.fromhex(rolling) + canonical(event))
            event["rolling_sha256"] = rolling
        heads.append(rolling)
    coefficients = np.zeros((NSEEDS, P1_ROWS), dtype=np.uint8)
    records = []
    for seed, seed_events in enumerate(events):
        for event in seed_events:
            node, value = event["global_index"], event["coefficient"]
            require(0 <= node < P1_ROWS and value in (1, 2), "packet_event_range")
            coefficients[seed, node] = (int(coefficients[seed, node]) + value) % 3
        records.append(seal("seed-relation", {"seed": seed, "raw_events": seed_events,
            "raw_event_count": len(seed_events), "raw_event_final_head": heads[seed],
            "final_coefficients": [[int(node), int(coefficients[seed, node])]
                for node in np.flatnonzero(coefficients[seed])]}))
    progress("packet-relations", bodies=5, total=5,
             raw_events=sum(len(item) for item in events))
    return seal("relations", {"event_order": EVENT_ORDER, "seeds": records}), coefficients, segments


def raw_accumulators(m: Any, base: Any) -> tuple[np.ndarray, np.ndarray, list[Any]]:
    top = np.empty((NSEEDS, 4, TOP_WIDTH), dtype=np.uint8)
    lower = np.empty((NSEEDS, LOWER_WIDTH), dtype=np.uint8)
    context, words = base.source_context()
    check_deadline("packet-raw-context")
    receipts = []
    for seed in range(NSEEDS):
        relator = tuple(int(value) for value in words["relators"][seed])
        parts = tuple(np.asarray(part, dtype=np.uint8)
                      for part in base.ARITH._seed_evaluate_seed(context, relator))
        d0, d1, d2, auxiliary = parts
        require(d0.shape == (4, m.SOURCE0C) and d1.shape == (4, m.SOURCE1C) and
                d2.shape == (4, TOP_WIDTH) and auxiliary.shape == (8,) and
                all(not np.any(part > 2) for part in parts), "raw_packet_seed_shape")
        if seed == 2:
            require(sha(m.pack(d2[0])) == base.SEED2_RAW_PACKED_SHA256 and
                    int(np.count_nonzero(d2[0])) == 568, "raw_seed2_lambda_independent_pin")
        top[seed] = d2
        lower[seed, :24192] = d0.reshape(-1)
        lower[seed, 24192:96768] = d1.reshape(-1)
        lower[seed, 96768:] = auxiliary
        receipts.append(seal("raw-seed", {"seed": seed, "compact_word": list(relator),
            "compact_word_sha256": sha(canonical(list(relator))),
            "word_dictionary_sha256": base.ARITH.WORD_SHA,
            "relator_dictionary_sha256": base.ARITH.WORD_RELATOR_SHA,
            "components": [m.component_receipt(name, value)
                for name, value in zip(("d0", "d1", "d2", "aux"), parts)]}))
        progress("packet-raw-seeds", seed=seed, completed=seed + 1, total=NSEEDS)
    return top, lower, receipts


def subtract_p1(m: Any, p1: Any, relations: Any, coefficients: np.ndarray,
                top: np.ndarray) -> tuple[dict[int, Any], dict[str, Any]]:
    referenced = {event["global_index"] for relation in relations["seeds"]
                  for event in relation["raw_events"]}
    refs: dict[int, Any] = {}
    p1_sha, row_sha = [], []
    cache_hash, instruction_hash = hashlib.sha256(), hashlib.sha256()
    predecessor, instruction_offset = ZERO_HEAD, 0
    arithmetic_rows = 0
    with m.safe_file(p1["root"], p1["cache"]["path"]).open("rb", buffering=1 << 20) as cache, \
            m.safe_file(p1["root"], p1["instruction"]["path"]).open("rb", buffering=1 << 20) as instructions:
        for node in range(P1_ROWS):
            raw = cache.read(m.P1_ROW_BYTES)
            line = instructions.readline()
            require(len(raw) == m.P1_ROW_BYTES and line.endswith(b"\n") and b"\r" not in line and
                    not np.any(np.frombuffer(raw, dtype=np.uint8) > 80), "packet_p1_stream_row")
            record = json.loads(line.decode("ascii"))
            predecessor = m.validate_p1_instruction(record, node, line, raw, predecessor, p1_sha, row_sha)
            p1_sha.append(record["p1_sha256"])
            row_sha.append(record["row_receipt"]["sha256"])
            if node in referenced:
                refs[node] = {"node": node, "instruction_offset": instruction_offset,
                    "instruction_length": len(line), "instruction_sha256": sha(line),
                    "ancestry_sha256": record["ancestry_sha256"], "predecessor": record["predecessor"],
                    "p1_sha256": record["p1_sha256"], "row_sha256": record["row_receipt"]["sha256"],
                    "origin_sha256": sha(canonical(record["origin"])),
                    "reductions_sha256": sha(canonical(record["reductions"])), "scale": record["scale"],
                    "literal_input_sha256": record["literal_input_sha256"],
                    "lift_components": [{"role": "p1-degree2", "bytes": len(raw), "sha256": sha(raw)}]}
            selected = np.flatnonzero(coefficients[:, node])
            if len(selected):
                arithmetic_rows += 1
                dense = m.unpack(raw, m.P1_ROW_TRITS).reshape(4, TOP_WIDTH)
                for seed in selected:
                    m.add_scaled(top[seed], dense, 3 - int(coefficients[seed, node]))
                del dense
            cache_hash.update(raw)
            instruction_hash.update(line)
            instruction_offset += len(line)
            if (node + 1) % 512 == 0 or node + 1 == P1_ROWS:
                progress("packet-p1-subtraction", rows=node + 1, total=P1_ROWS)
        require(cache.read(1) == instructions.read(1) == b"", "packet_p1_eof")
    require(cache_hash.hexdigest() == p1["cache"]["sha256"] and
            instruction_hash.hexdigest() == p1["instruction"]["sha256"] and
            instruction_offset == p1["instruction"]["bytes"] and
            predecessor == p1["manifest"]["ancestry_sha256"] and set(refs) == referenced,
            "packet_p1_terminal")
    return refs, {"manifest_sha256": p1["manifest_sha256"],
        "cache_sha256": cache_hash.hexdigest(), "instruction_sha256": instruction_hash.hexdigest(),
        "instruction_final_head": predecessor, "rows": P1_ROWS, "cache_passes": 1,
        "instruction_passes": 1, "referenced_roots": len(refs), "arithmetic_rows": arithmetic_rows}


def subtract_lower(m: Any, segments: list[Any], coefficients: np.ndarray,
                   lower: np.ndarray, refs: dict[int, Any]) -> dict[str, Any]:
    d0 = lower[:, :24192].reshape(NSEEDS, 4, m.SOURCE0C)
    d1 = lower[:, 24192:96768].reshape(NSEEDS, 4, m.SOURCE1C)
    auxiliary = lower[:, 96768:]
    blob_receipts = []
    for segment in segments:
        character = segment["owner"]
        descriptors = ([(segment["lower_descriptor"], "old-lower"),
                        (segment["grade_descriptor"], "old-grade")]
                       if segment["kind"] == "old" else [(segment["basis_descriptor"], "new-grade")])
        for descriptor, kind in descriptors:
            row_bytes = (descriptor["width"] + 3) // 4
            require(descriptor["rows"] == segment["rows"] and
                    descriptor["bytes"] == row_bytes * segment["rows"], "packet_lower_dimensions")
            digest = hashlib.sha256()
            with m.safe_file(segment["root"], descriptor["file"]).open("rb", buffering=1 << 20) as stream:
                for local in range(segment["rows"]):
                    raw = stream.read(row_bytes)
                    require(len(raw) == row_bytes, "packet_lower_eof")
                    dense = m.unpack(raw, descriptor["width"])
                    node = segment["start"] + local
                    for seed in np.flatnonzero(coefficients[:, node]):
                        coefficient = 3 - int(coefficients[seed, node])
                        if kind == "old-lower":
                            require(dense.size == m.SOURCE0C + 8, "old_lower_width")
                            m.add_scaled(d0[seed, character], dense[:m.SOURCE0C], coefficient)
                            m.add_scaled(auxiliary[seed], dense[m.SOURCE0C:], coefficient)
                        elif kind == "old-grade":
                            m.add_scaled(d1[seed], dense.reshape(4, m.SOURCE1C), coefficient)
                        else:
                            m.add_scaled(d1[seed, character], dense, coefficient)
                    if node in refs:
                        refs[node]["lift_components"].append({"role": kind, "bytes": len(raw), "sha256": sha(raw)})
                    digest.update(raw)
                    if (local + 1) % 512 == 0:
                        progress("packet-lower-subtraction", character=character, component=kind,
                                 rows=local + 1, total=segment["rows"])
                require(stream.read(1) == b"", "packet_lower_trailing")
            require(digest.hexdigest() == descriptor["sha256"], "packet_lower_digest")
            role = kind.split("-")[0] + "-" + str(character) + "-" + kind.split("-")[1]
            blob_receipts.append({"role": role, "task554_body_sha256": segment["body_sha256"],
                "descriptor": descriptor, "full_file_authenticated": True})
            progress("packet-lower-subtraction", blobs=len(blob_receipts), total=12)
    require(len(blob_receipts) == 12, "packet_twelve_lower_blobs")
    return {"receipts": blob_receipts, "full_blob_files": 12, "blob_passes": 12,
        "total_authenticated_bytes": sum(item["descriptor"]["bytes"] for item in blob_receipts)}


def projector_receipts(m: Any, base: Any) -> list[Any]:
    projectors = []
    for character, label in enumerate(m.CHARACTERS):
        factors = []
        for pure_label in m.CHARACTERS:
            word = list(base.ARITH.SEED_PURE_WORDS[pure_label])
            factors.append({"label": list(pure_label), "pure_word": word,
                "pure_word_sha256": sha(canonical(word)),
                "source_character_sign": int(base.ARITH._seed_cv(label, pure_label))})
        require(all(item["source_character_sign"] in (1, 2) for item in factors), "projector_signs")
        projectors.append({"character": character, "character_label": list(label), "factors": factors})
    return projectors


def build_packet(m: Any, base: Any, p1: Any, task554: Any, owner_sha: str,
                 state: dict[str, Any], output: Path) -> dict[str, Any]:
    relations, coefficients, segments = collect_relations(m, base, task554)
    top, lower, raw_seeds = raw_accumulators(m, base)
    refs, p1_pass = subtract_p1(m, p1, relations, coefficients, top)
    lower_pass = subtract_lower(m, segments, coefficients, lower, refs)
    seed_receipts = []
    packed_rows: dict[tuple[int, int], bytes] = {}
    for seed in range(NSEEDS):
        require(not np.any(lower[seed]), "complete_packet_seed_lower_zero:" + str(seed))
        top_rows = []
        for character in range(4):
            # v453 applies only now: the entire complete lower part is zero.
            raw = m.pack(top[seed, character])
            packed_rows[character, seed] = raw
            top_rows.append({"character": character, "seed": seed,
                "offset": (character * NSEEDS + seed) * TOP_BYTES, "length": TOP_BYTES,
                "sha256": sha(raw), "support": int(np.count_nonzero(top[seed, character]))})
        seed_receipts.append({"seed": seed, "lower_width": LOWER_WIDTH,
            "lower_nonzero_count": 0, "lower_zero_count": LOWER_WIDTH,
            "lower_dense_sha256": sha(lower[seed].tobytes()),
            "reduced_components": [m.component_receipt(name, value) for name, value in (
                ("d0", lower[seed, :24192].reshape(4, m.SOURCE0C)),
                ("d1", lower[seed, 24192:96768].reshape(4, m.SOURCE1C)),
                ("d2", top[seed]), ("aux", lower[seed, 96768:]))],
            "top_rows": top_rows})
    del top, lower, coefficients
    regressions = []
    for seed in (30, 34):
        require(packed_rows[0, seed] == state["saved_sources"][seed], "saved_source_packet_bytes:" + str(seed))
        regressions.append({"seed": seed, "character": 0, "bytes": TOP_BYTES,
                            "sha256": sha(state["saved_sources"][seed])})
    packet_receipts = seal("packet-receipts", {"raw_seeds": raw_seeds, "seeds": seed_receipts,
        "p1_pass": p1_pass, "lower_pass": lower_pass,
        "regression": {"seed2_char0_raw": {"seed": 2, "character": 0,
            "packed_sha256": base.SEED2_RAW_PACKED_SHA256, "support": 568,
            "lambda_independent": True, "scalar_assertion_retired": True},
            "saved_sources": regressions},
        "premises": {"complete_defect_lower_zero_executed": True,
            "v453_direct_slice_after_complete_lower_zero": True,
            "structural_slicing_retained_as_premise": True, "word_projector_replayed": False,
            "projector_order": [list(label) for label in m.CHARACTERS],
            "projectors": projector_receipts(m, base)}})
    roots = seal("p1-roots", {"roots": [refs[node] for node in sorted(refs)]})
    top_raw = b"".join(packed_rows[character, seed] for character in range(4) for seed in range(NSEEDS))
    require(len(top_raw) == 1596672, "fixed_packet_bytes")
    pending = output / (".packet-pending-" + uuid.uuid4().hex)
    pending.mkdir()
    files = [write_atomic(pending, "tops.bin", top_raw),
             write_json(pending, "relations.json", relations), write_json(pending, "p1-roots.json", roots),
             write_json(pending, "receipts.json", packet_receipts)]
    manifest = seal("packet-manifest", {"owner_sha256": owner_sha,
        "files": sorted(files, key=lambda item: item["file"]),
        "file_roster": sorted([item["file"] for item in files] + ["manifest.json"]),
        "candidate": True, "cross_checked": False, "verified": False})
    write_json(pending, "manifest.json", manifest)
    publish_directory(pending, output / "packet")
    progress("packet-durable", seeds=NSEEDS, packed_bytes=len(top_raw),
             literal_roots=len(refs), manifest_sha256=sha(canonical(manifest)))
    return {"manifest": manifest, "manifest_sha256": sha(canonical(manifest)),
            "tops": top_raw, "relations": relations, "roots": roots, "receipts": packet_receipts}


def authenticated_directory(m: Any, path: Path, kind: str, wanted_sha: str | None = None
                            ) -> tuple[Any, dict[str, bytes]]:
    manifest = read_json(m.safe_file(path, "manifest.json"), kind=kind)
    require(wanted_sha is None or sha(canonical(manifest)) == wanted_sha, "directory_manifest_pin")
    require(manifest["candidate"] is True and manifest["cross_checked"] is False and
            manifest["verified"] is False and
            manifest["file_roster"] == sorted({item["file"] for item in manifest["files"]} | {"manifest.json"}) and
            len(manifest["files"]) + 1 == len(manifest["file_roster"]) and
            set(manifest["file_roster"]) == {p.name for p in path.iterdir()}, "complete_directory_roster")
    payloads = {item["file"]: m.read_exact(m.safe_file(path, item["file"]),
                item["bytes"], item["sha256"], cap=1 << 28) for item in manifest["files"]}
    return manifest, payloads


def decoded_sealed(raw: bytes, kind: str) -> Any:
    value = json.loads(raw.decode("ascii"))
    require(canonical(value) == raw and sealed_ok(value, kind), "payload_seal:" + kind)
    return value


def load_packet(m: Any, output: Path, owner_sha: str, state: Any,
                wanted_sha: str | None) -> dict[str, Any]:
    manifest, payloads = authenticated_directory(m, output / "packet", "packet-manifest", wanted_sha)
    require(manifest["owner_sha256"] == owner_sha and set(payloads) ==
            {"tops.bin", "relations.json", "p1-roots.json", "receipts.json"} and
            len(payloads["tops.bin"]) == 1596672 and
            not np.any(np.frombuffer(payloads["tops.bin"], dtype=np.uint8) > 80), "saved_packet_owner_payload")
    relations = decoded_sealed(payloads["relations.json"], "relations")
    roots = decoded_sealed(payloads["p1-roots.json"], "p1-roots")
    receipts = decoded_sealed(payloads["receipts.json"], "packet-receipts")
    require(relations["event_order"] == EVENT_ORDER and len(relations["seeds"]) == NSEEDS and
            all(sealed_ok(item, "seed-relation") and item["seed"] == seed
                for seed, item in enumerate(relations["seeds"])) and
            len(receipts["seeds"]) == len(receipts["raw_seeds"]) == NSEEDS,
            "saved_packet_relation_roster")
    for seed, item in enumerate(receipts["seeds"]):
        require(item["seed"] == seed and item["lower_width"] == item["lower_zero_count"] == LOWER_WIDTH and
                item["lower_nonzero_count"] == 0 and len(item["top_rows"]) == 4,
                "saved_packet_lower_receipt")
        for character, row in enumerate(item["top_rows"]):
            offset = (character * NSEEDS + seed) * TOP_BYTES
            require(row["character"] == character and row["seed"] == seed and
                    row["offset"] == offset and row["length"] == TOP_BYTES and
                    row["sha256"] == sha(payloads["tops.bin"][offset:offset + TOP_BYTES]),
                    "saved_packet_slice_receipt")
    for seed in (30, 34):
        require(payloads["tops.bin"][seed * TOP_BYTES:(seed + 1) * TOP_BYTES] ==
                state["saved_sources"][seed], "resume_saved_source_join")
    progress("packet-resumed", seeds=NSEEDS, manifest_sha256=sha(canonical(manifest)))
    return {"manifest": manifest, "manifest_sha256": sha(canonical(manifest)),
            "tops": payloads["tops.bin"], "relations": relations, "roots": roots, "receipts": receipts}


def packet_row(packet: Any, character: int, seed: int) -> bytes:
    require(type(character) is int and 0 <= character < 4 and
            type(seed) is int and 0 <= seed < NSEEDS, "packet_row_indices")
    offset = (character * NSEEDS + seed) * TOP_BYTES
    return packet["tops"][offset:offset + TOP_BYTES]


def scan_roots(m: Any, base: Any, tables: list[Any], packet: Any,
               state: Any) -> tuple[Any, list[np.ndarray]]:
    roots = []
    root_receipts = []
    values = [[0] * NSEEDS for _ in range(4)]
    active = []
    for character in range(4):
        q = base.ARITH.sparse_adjoint(tables[character]["forward"]["B"],
                                     TOP_WIDTH, PHYSICAL_WIDTH, state["lambda"])
        require(q.shape == (TOP_WIDTH,) and not np.any(q > 2), "fresh_four_root_shape")
        roots.append(q)
        support = int(np.count_nonzero(q))
        root_receipts.append({"character": character, "support": support,
            "packed_sha256": sha(m.pack(q)),
            "B_adj_identity": tables[character]["identity"]["adjoint:B"]})
        if support:
            active.append(character)
            for seed in range(NSEEDS):
                values[character][seed] = m.dot(q, m.unpack(packet_row(packet, character, seed), TOP_WIDTH))
        progress("current-root-scan", step=state["completed_steps"], rank=state["rank"],
                 character=character, root_support=support, declared_pairs=(character + 1) * NSEEDS)
    first = next(({"character": character, "seed": seed, "index": character * NSEEDS + seed,
                   "scalar": values[character][seed]}
                  for character in range(4) for seed in range(NSEEDS) if values[character][seed]), None)
    return seal("root-scan", {"generation": state["generation"], "rank": state["rank"],
        "state_head": state["head"], "lambda_sha256": sha(state["lambda_raw"]),
        "roots": root_receipts, "values": values, "declared_pair_count": 176,
        "nonzero_root_blocks": active, "nonzero_root_block_count": len(active),
        "informative_pair_count": len(active) * NSEEDS,
        "nonzero_pair_count": sum(value != 0 for row in values for value in row), "first_hit": first}), roots


def derived_rho2(m: Any, state: Any, step: int) -> dict[str, Any]:
    return {"mode": "derived", "value": 1, "original_rho2_directly_read": False,
        "original_rho2_packed_sha256": m.RHO2_SHA256,
        "accepted_target_derivation_parents": state["accepted_target_derivation_parents"],
        "accepted_identity_convention": {
            "base": "rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)",
            "saved_deltas": "parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)"},
        "new_identity_convention": "parent_remainder - child_remainder = target.scalar * normalized_row",
        "newly_executed_target_steps": step}


def next_separator(m: Any, state: Any, normalized: bytes, lead: int,
                   target: bytes, step: int) -> tuple[Any, bytes]:
    free = m.first_nonzero(target, PHYSICAL_WIDTH)
    require(free is not None and free[0] not in set(state["leads"]) | {lead}, "current_free_coordinate")
    functional = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    functional[free[0]] = free[1]
    all_rows = [*state["rows"], normalized]
    all_records = [*state["records"], {"offer": state["generation"], "lead": lead}]
    for count, (record, raw) in enumerate(zip(reversed(all_records), reversed(all_rows)), start=1):
        row = m.unpack(raw, PHYSICAL_WIDTH)
        coordinate = record["lead"]
        require(row[coordinate] == 1 and functional[coordinate] == 0, "next_lambda_pivot_coordinate")
        functional[coordinate] = (-m.dot(row, functional)) % 3
        require(m.dot(row, functional) == 0, "next_lambda_reverse_equation")
        if count % 256 == 0 or count == len(all_rows):
            progress("next-lambda", step=step, rows=count, total=len(all_rows))
    direct = m.check_final_separator(functional, all_rows, state["target_raw"], target)
    raw_lambda = m.pack(functional)
    return {"free_coordinate": free[0], "free_value": free[1], "lambda_sha256": sha(raw_lambda),
            "direct_pairing": direct, "lambda_rho2": derived_rho2(m, state, step)}, raw_lambda


def literal_reference(packet: Any, tables: Any, selection: Any, source: bytes) -> Any:
    character, seed = selection["character"], selection["seed"]
    return {"defect_operation": "ordered-product", "seed": seed,
        "seed_relation_sha256": packet["relations"]["seeds"][seed]["sha256"],
        "p1_roots_sha256": sha(canonical(packet["roots"])),
        "compact_word_sha256": packet["receipts"]["raw_seeds"][seed]["compact_word_sha256"],
        "p1_factor_order": "event_id-ascending", "p1_exponent_rule": "(3-coefficient)%3",
        "literal_coefficient_collection": False, "character": character,
        "projector_receipt_sha256": sha(canonical(packet["receipts"]["premises"]["projectors"][character])),
        "actor_path": [], "forward_B": tables[character]["identity"]["forward:B"],
        "source_d_sha256": sha(source), "parent_state_ancestry_premise": True,
        "normalized_exponent_pair": "NOT_REPLAYED", "eleven_slot_replay": False,
        "full_A0_witness": False, "grade2_positive_terminal_complete": False}


def head_record(state: Any, owner_sha: str, packet: Any, start: Any, source: Any) -> Any:
    return seal("head", {"owner_sha256": owner_sha, "producer_sha256": source["producer_sha256"],
        "packet_manifest_sha256": packet["manifest_sha256"], "start_sha256": sha(canonical(start)),
        "completed_steps": state["completed_steps"], "step_manifest_sha256": state["step_manifest_sha256"],
        "rank": state["rank"], "generation": state["generation"], "state_head": state["head"],
        "kind": state["kind"]})


def append_step(m: Any, state: Any, packet: Any, tables: Any, roots: Any,
                scan: Any, owner_sha: str, output: Path) -> None:
    selection = scan["first_hit"]
    require(selection is not None and state["completed_steps"] < 176, "bounded_nonzero_root_required")
    step = state["completed_steps"] + 1
    character, seed = selection["character"], selection["seed"]
    progress("selected-root", step=step, rank=state["rank"], character=character, seed=seed,
             scalar=selection["scalar"])
    source = packet_row(packet, character, seed)
    dense = m.unpack(source, TOP_WIDTH)
    physical = m.apply_sparse(tables[character]["forward"]["B"], TOP_WIDTH, PHYSICAL_WIDTH, dense)
    q_d, lambda_g = m.dot(roots[character], dense), m.dot(state["lambda"], physical)
    require(q_d == lambda_g == selection["scalar"] and q_d in (1, 2), "selected_forward_adjoint_pairing")
    physical_raw = m.pack(physical)
    remainder, reductions = m.physical_reduce(physical_raw, state["records"], state["rows"])
    require(m.dot(state["lambda"], m.unpack(remainder, PHYSICAL_WIDTH)) == q_d,
            "selected_reduction_pairing")
    normalized, lead, scale = m.normalize_pivot(remainder, state["leads"])
    target, target_scalar = m.update_target(state["target_raw"], normalized, lead, state["leads"])
    kind = "Member" if m.first_nonzero(target, PHYSICAL_WIDTH) is None else "Separator"
    separator, lambda_raw = (None, None)
    if kind == "Separator":
        separator, lambda_raw = next_separator(m, state, normalized, lead, target, step)
    instruction = {"schema": SCHEMA + ".instruction", "step": step, "predecessor": state["head"],
        "offer": state["generation"], "generation": state["generation"] + 1,
        "rank": state["rank"] + 1, "lead": lead, "sigma": scale,
        "physical_offset": state["rank"] * PHYSICAL_BYTES, "selected": selection,
        "packet_manifest_sha256": packet["manifest_sha256"],
        "relation_sha256": packet["relations"]["seeds"][seed]["sha256"],
        "p1_roots_sha256": sha(canonical(packet["roots"])),
        "physical_reductions": reductions, "physical_sha256": sha(normalized),
        "target_scalar": target_scalar, "target_remainder_sha256": sha(target)}
    new_head = sha(bytes.fromhex(state["head"]) + canonical(instruction))
    instruction["rolling_sha256"] = new_head
    result = seal("step-result", {"step": step, "kind": kind, "owner_sha256": owner_sha,
        "packet_manifest_sha256": packet["manifest_sha256"], "parent_state_head": state["head"],
        "state_head": new_head, "rank_before": state["rank"], "rank_after": state["rank"] + 1,
        "generation_before": state["generation"], "generation_after": state["generation"] + 1,
        "selection": selection, "scan": scan, "pairings": {"q_d": q_d, "lambda_G": lambda_g},
        "pivot": {"lead": lead, "scale": scale, "reductions": reductions, "normalized_sha256": sha(normalized)},
        "target": {"parent_remainder_sha256": sha(state["target_raw"]),
                   "remainder_sha256": sha(target), "scalar": target_scalar},
        "separator": separator, "literal": literal_reference(packet, tables, selection, source),
        "candidate": True, "cross_checked": False, "verified": False})
    steps = output / "steps"
    pending = steps / (".pending-" + str(step).zfill(6) + "-" + uuid.uuid4().hex)
    pending.mkdir()
    files = [write_atomic(pending, name, raw) for name, raw in (
        ("physical-raw.bin", physical_raw), ("physical-remainder.bin", remainder),
        ("physical-normalized.bin", normalized), ("target-remainder.bin", target),
        ("instruction.json", canonical(instruction)), ("result.json", canonical(result)))]
    if lambda_raw is not None:
        files.append(write_atomic(pending, "lambda.bin", lambda_raw))
    manifest = seal("step-manifest", {"step": step, "owner_sha256": owner_sha,
        "packet_manifest_sha256": packet["manifest_sha256"],
        "predecessor_step_manifest_sha256": state["step_manifest_sha256"],
        "parent_state_head": state["head"], "state_head": new_head,
        "rank": state["rank"] + 1, "generation": state["generation"] + 1, "kind": kind,
        "files": sorted(files, key=lambda item: item["file"]),
        "file_roster": sorted([item["file"] for item in files] + ["manifest.json"]),
        "candidate": True, "cross_checked": False, "verified": False})
    write_json(pending, "manifest.json", manifest)
    final = steps / str(step).zfill(6)
    if final.exists():
        # An orphan beyond the authenticated HEAD never becomes an implicit step.
        require(not final.is_symlink() and final.is_dir(), "orphan_step_directory")
        os.replace(final, steps / (".orphan-" + final.name + "-" + uuid.uuid4().hex))
        sync_directory(steps)
    publish_directory(pending, final)
    state["records"].append({"offer": instruction["offer"], "lead": lead,
        "physical_offset": instruction["physical_offset"], "rank": instruction["rank"],
        "rolling_sha256": new_head})
    state["rows"].append(normalized)
    state["leads"].append(lead)
    state["previous_target_raw"] = state["target_raw"]
    state.update({"rank": state["rank"] + 1, "generation": state["generation"] + 1,
        "head": new_head, "completed_steps": step, "step_manifest_sha256": sha(canonical(manifest)),
        "target_raw": target, "lambda_raw": lambda_raw, "kind": kind,
        "lambda": m.unpack(lambda_raw, PHYSICAL_WIDTH) if lambda_raw is not None else None})
    progress("step-durable", step=step, rank=state["rank"], seed=seed, character=character, kind=kind)


def load_prefix(m: Any, output: Path, state: Any, packet: Any, owner_sha: str,
                start: Any, source: Any, head: Any) -> None:
    """Load the authenticated whole prefix; arithmetic replay belongs to checker."""
    require(sealed_ok(head, "head") and head["owner_sha256"] == owner_sha and
            head["producer_sha256"] == source["producer_sha256"] and
            head["packet_manifest_sha256"] == packet["manifest_sha256"] and
            head["start_sha256"] == sha(canonical(start)) and
            type(head["completed_steps"]) is int and 0 <= head["completed_steps"] <= 176,
            "resume_head_owner_pins")
    for step in range(1, head["completed_steps"] + 1):
        require(state["kind"] == "Separator", "resume_step_after_member")
        manifest, payloads = authenticated_directory(
            m, output / "steps" / str(step).zfill(6), "step-manifest")
        require(manifest["step"] == step and manifest["owner_sha256"] == owner_sha and
                manifest["packet_manifest_sha256"] == packet["manifest_sha256"] and
                manifest["predecessor_step_manifest_sha256"] == state["step_manifest_sha256"] and
                manifest["parent_state_head"] == state["head"] and
                manifest["rank"] == state["rank"] + 1 and
                manifest["generation"] == state["generation"] + 1 and
                manifest["kind"] in ("Member", "Separator"), "resume_step_parent_chain")
        kind = manifest["kind"]
        wanted_files = {"physical-raw.bin", "physical-remainder.bin", "physical-normalized.bin",
                        "target-remainder.bin", "instruction.json", "result.json"}
        if kind == "Separator":
            wanted_files.add("lambda.bin")
        require(set(payloads) == wanted_files, "resume_step_payload_roster")
        instruction = json.loads(payloads["instruction.json"].decode("ascii"))
        unsigned = {key: value for key, value in instruction.items() if key != "rolling_sha256"}
        require(canonical(instruction) == payloads["instruction.json"] and
                instruction["schema"] == SCHEMA + ".instruction" and instruction["step"] == step and
                instruction["predecessor"] == state["head"] and
                instruction["rolling_sha256"] == manifest["state_head"] ==
                sha(bytes.fromhex(state["head"]) + canonical(unsigned)) and
                instruction["offer"] == state["generation"] and
                instruction["generation"] == manifest["generation"] and
                instruction["rank"] == manifest["rank"] and
                instruction["physical_offset"] == state["rank"] * PHYSICAL_BYTES and
                instruction["packet_manifest_sha256"] == packet["manifest_sha256"] and
                instruction["p1_roots_sha256"] == sha(canonical(packet["roots"])),
                "resume_instruction_chain")
        selection = instruction["selected"]
        packet_row(packet, selection["character"], selection["seed"])
        require(selection["index"] == selection["character"] * NSEEDS + selection["seed"] and
                selection["scalar"] in (1, 2) and instruction["relation_sha256"] ==
                packet["relations"]["seeds"][selection["seed"]]["sha256"], "resume_selected_packet_ref")
        result = decoded_sealed(payloads["result.json"], "step-result")
        require(result["step"] == step and result["kind"] == kind and
                result["owner_sha256"] == owner_sha and result["candidate"] is True and
                result["cross_checked"] is False and result["verified"] is False and
                result["packet_manifest_sha256"] == packet["manifest_sha256"] and
                result["parent_state_head"] == state["head"] and
                result["state_head"] == manifest["state_head"] and
                result["rank_before"] == state["rank"] and result["rank_after"] == manifest["rank"] and
                result["generation_before"] == state["generation"] and
                result["generation_after"] == manifest["generation"] and
                result["selection"] == selection and sealed_ok(result["scan"], "root-scan") and
                result["scan"]["first_hit"] == selection and
                result["scan"]["state_head"] == state["head"] and
                result["scan"]["generation"] == state["generation"] and
                result["scan"]["rank"] == state["rank"] and
                result["scan"]["lambda_sha256"] == sha(state["lambda_raw"]), "resume_step_result_join")
        normalized, target = payloads["physical-normalized.bin"], payloads["target-remainder.bin"]
        lead = instruction["lead"]
        row, target_dense = m.unpack(normalized, PHYSICAL_WIDTH), m.unpack(target, PHYSICAL_WIDTH)
        require(type(lead) is int and 0 <= lead < PHYSICAL_WIDTH and lead not in state["leads"] and
                m.first_nonzero(normalized, PHYSICAL_WIDTH) == (lead, 1) and
                all(row[index] == target_dense[index] == 0 for index in state["leads"]) and
                target_dense[lead] == 0 and instruction["sigma"] in (1, 2) and
                sha(normalized) == instruction["physical_sha256"] == result["pivot"]["normalized_sha256"] and
                result["pivot"]["lead"] == lead and result["pivot"]["scale"] == instruction["sigma"] and
                result["pivot"]["reductions"] == instruction["physical_reductions"] and
                result["target"] == {"parent_remainder_sha256": sha(state["target_raw"]),
                    "remainder_sha256": sha(target), "scalar": instruction["target_scalar"]} and
                sha(target) == instruction["target_remainder_sha256"] and
                instruction["target_scalar"] in (0, 1, 2) and
                (bool(np.any(target_dense)) == (kind == "Separator")), "resume_new_payload_metadata")
        lambda_raw = payloads.get("lambda.bin")
        if kind == "Separator":
            require(result["separator"]["lambda_sha256"] == sha(lambda_raw) and
                    result["separator"]["lambda_rho2"] == derived_rho2(m, state, step),
                    "resume_derived_separator_metadata")
            lam = m.unpack(lambda_raw, PHYSICAL_WIDTH)
        else:
            require(result["separator"] is None, "resume_member_separator")
            lam = None
        state["records"].append({"offer": instruction["offer"], "lead": lead,
            "physical_offset": instruction["physical_offset"], "rank": instruction["rank"],
            "rolling_sha256": instruction["rolling_sha256"]})
        state["rows"].append(normalized)
        state["leads"].append(lead)
        state["previous_target_raw"] = state["target_raw"]
        state.update({"head": manifest["state_head"], "rank": manifest["rank"],
            "generation": manifest["generation"], "kind": kind, "completed_steps": step,
            "step_manifest_sha256": sha(canonical(manifest)), "target_raw": target,
            "lambda_raw": lambda_raw, "lambda": lam})
        progress("resume-complete-step", step=step, rank=state["rank"], seed=selection["seed"])
    require(head_record(state, owner_sha, packet, start, source) == head, "resume_final_head_join")
    if state["kind"] == "Separator":
        m.check_final_separator(state["lambda"], state["rows"], state["previous_target_raw"], state["target_raw"])


def terminal_for(scan: Any, completed_steps: int, cap: int, resource_stop: bool) -> str | None:
    if scan["first_hit"] is None:
        return "ROOT_SEEDS_ZERO"
    if resource_stop:
        return "UNKNOWN_RESOURCE"
    if completed_steps >= cap:
        return "UNKNOWN_CAP"
    return None


def request_stop(_signal: int, _frame: Any) -> None:
    global STOP_REQUESTED
    STOP_REQUESTED = True


def run_actual(args: argparse.Namespace) -> Any:
    global DEADLINE
    output = args.output_root.resolve()
    parents = [args.state_root, args.delta_root, args.seed34_root, args.prepare_root,
               *args.block_root, args.p1_root, args.task712_root]
    require(not args.output_root.is_symlink(), "output_symlink")
    for path in parents:
        parent = path.resolve()
        require(path.is_dir() and output != parent and output not in parent.parents and
                parent not in output.parents, "disjoint_output_parents")
    require(args.resume == output.exists(), "existing_output_requires_resume")
    DEADLINE = STARTED + args.max_seconds if args.max_seconds is not None else None
    for signum in (signal.SIGINT, signal.SIGTERM):
        signal.signal(signum, request_stop)
    m, base, descriptors = dependencies()
    state, start = load_start(m, args)
    owner, p1, task554, tables = owner_and_tables(m, base, descriptors, args, state)
    owner_sha = sha(canonical(owner))
    source = seal("source", {"producer_sha256": sha(Path(__file__).read_bytes()),
        "modules": MODULE_PINS, "data": DATA_PINS, "python": sys.version, "numpy": np.__version__})
    if args.resume:
        for name, expected, kind in (("owner.json", owner, "owner"), ("start.json", start, "start"),
                                     ("source.json", source, "source")):
            require(read_json(m.safe_file(output, name), kind=kind) == expected,
                    "same_owner_resume_pin:" + name)
    else:
        output.mkdir(parents=True)
        for name, value in (("owner.json", owner), ("start.json", start), ("source.json", source)):
            write_json(output, name, value)
        (output / "steps").mkdir()
        sync_directory(output)
    require((output / "steps").is_dir() and not (output / "steps").is_symlink(), "steps_directory")
    head = read_json(m.safe_file(output, "HEAD"), kind="head") if (output / "HEAD").exists() else None
    require(head is None or (output / "packet").is_dir(), "head_requires_complete_packet")
    if (output / "packet").exists():
        packet = load_packet(m, output, owner_sha, state,
                             head["packet_manifest_sha256"] if head is not None else None)
    else:
        packet = build_packet(m, base, p1, task554, owner_sha, state, output)
    if head is not None:
        load_prefix(m, output, state, packet, owner_sha, start, source, head)
    else:
        head = head_record(state, owner_sha, packet, start, source)
        write_json(output, "HEAD", head)
    while True:
        scan = None
        if state["kind"] == "Member":
            terminal = "MEMBER_CANDIDATE"
            break
        scan, roots = scan_roots(m, base, tables, packet, state)
        resource_stop = STOP_REQUESTED or (args.max_seconds is not None and
                                           time.monotonic() - STARTED >= args.max_seconds)
        terminal = terminal_for(scan, state["completed_steps"], args.max_appends, resource_stop)
        if terminal is not None:
            break
        append_step(m, state, packet, tables, roots, scan, owner_sha, output)
        head = head_record(state, owner_sha, packet, start, source)
        write_json(output, "HEAD", head, replace=True)
        progress("head-advanced", step=state["completed_steps"], rank=state["rank"], head=state["head"])
    head = head_record(state, owner_sha, packet, start, source)
    require(read_json(m.safe_file(output, "HEAD"), kind="head") == head, "terminal_head_join")
    result = seal("result", {"status": "PASS", "terminal": terminal,
        "head_sha256": sha(canonical(head)), "packet_manifest_sha256": packet["manifest_sha256"],
        "owner_sha256": owner_sha, "completed_steps": state["completed_steps"], "rank": state["rank"],
        "generation": state["generation"], "state_head": state["head"], "scan": scan,
        "lambda_rho2": derived_rho2(m, state, state["completed_steps"]) if scan is not None else None,
        "scope": SCOPE, "claims": CLAIMS, "candidate": True, "cross_checked": False, "verified": False})
    write_json(output, "result.json", result, replace=args.resume or (output / "result.json").exists())
    progress("terminal", terminal=terminal, step=state["completed_steps"], rank=state["rank"],
             nonzero_root_blocks=scan["nonzero_root_blocks"] if scan is not None else None)
    return result


def selftest() -> Any:
    """Three changed-interface canaries; no historical input or old suite."""
    m, base, _ = dependencies()
    source_vector = np.zeros(TOP_WIDTH, dtype=np.uint8)
    source_vector[0] = 1
    second_vector = source_vector.copy()
    second_vector[0], second_vector[1] = 0, 1
    top = bytearray(1596672)
    for character, seed, row in ((1, 2, source_vector), (3, 7, second_vector)):
        offset = (character * NSEEDS + seed) * TOP_BYTES
        top[offset:offset + TOP_BYTES] = m.pack(row)
    empty_relations = [seal("seed-relation", {"seed": seed, "raw_events": [],
        "raw_event_count": 0, "raw_event_final_head": ZERO_HEAD, "final_coefficients": []})
        for seed in range(NSEEDS)]
    packet = {"manifest_sha256": sha(b"synthetic-packet"), "tops": bytes(top),
        "relations": seal("relations", {"event_order": EVENT_ORDER, "seeds": empty_relations}),
        "roots": seal("p1-roots", {"roots": []}),
        "receipts": {"raw_seeds": [{"compact_word_sha256": sha(b"synthetic-word")}] * NSEEDS,
                     "premises": {"projectors": projector_receipts(m, base)}}}
    tables = [{"forward": {"B": []}, "identity": {"forward:B": "synthetic-B-" + str(a),
               "adjoint:B": "synthetic-Badj-" + str(a)}} for a in range(4)]
    tables[1]["forward"]["B"] = [[0, 5, 1]]
    tables[3]["forward"]["B"] = [[1, 7, 1]]
    old = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    old[2] = 1
    target = old * 0
    target[5] = target[7] = 1
    lam = old * 0
    lam[5] = 1
    initial = {"rows": [m.pack(old)], "records": [{"offer": 0, "lead": 2, "physical_offset": 0}],
        "leads": [2], "rank": 1, "generation": 1, "head": sha(b"synthetic-start-head"),
        "lambda": lam, "lambda_raw": m.pack(lam), "target_raw": m.pack(target),
        "previous_target_raw": m.pack(target), "accepted_target_derivation_parents": [],
        "completed_steps": 0, "step_manifest_sha256": None, "kind": "Separator"}
    before, roots = scan_roots(m, base, tables, packet, initial)
    require(before["nonzero_root_blocks"] == [1] and before["first_hit"]["index"] == 46 and
            terminal_for(before, 0, 0, False) == "UNKNOWN_CAP" and
            terminal_for(before, 0, 176, True) == "UNKNOWN_RESOURCE", "live_root_and_cap_canary")
    owner_sha = sha(b"synthetic-owner")
    start = seal("start", {"synthetic_only": True})
    source = seal("source", {"producer_sha256": sha(b"synthetic-producer")})
    with tempfile.TemporaryDirectory(prefix="task945-canary-") as temporary:
        output = Path(temporary)
        (output / "steps").mkdir()
        initial_head = head_record(initial, owner_sha, packet, start, source)
        write_json(output, "HEAD", initial_head)
        produced = copy.deepcopy(initial)
        append_step(m, produced, packet, tables, roots, before, owner_sha, output)
        # The whole step exists while HEAD still names the previous state.
        require(read_json(output / "HEAD", kind="head") == initial_head and
                (output / "steps" / "000001" / "manifest.json").is_file(), "durable_before_head_canary")
        head = head_record(produced, owner_sha, packet, start, source)
        write_json(output, "HEAD", head, replace=True)
        (output / "steps" / ".pending-000002-synthetic").mkdir()
        (output / "steps" / ".orphan-000002-synthetic").mkdir()
        resumed = copy.deepcopy(initial)
        load_prefix(m, output, resumed, packet, owner_sha, start, source, head)
        require(resumed["rows"] == produced["rows"] and resumed["target_raw"] == produced["target_raw"] and
                resumed["lambda_raw"] == produced["lambda_raw"] and resumed["completed_steps"] == 1,
                "actual_prefix_roundtrip_canary")
        after, _ = scan_roots(m, base, tables, packet, resumed)
        require(after["nonzero_root_blocks"] == [3] and after["first_hit"]["index"] == 139,
                "fresh_active_character_after_append_canary")
        bad_head = seal("head", {key: value for key, value in head.items()
                                if key not in ("schema", "sha256", "owner_sha256")}
                        | {"owner_sha256": sha(b"wrong-owner")})
        try:
            load_prefix(m, output, copy.deepcopy(initial), packet, owner_sha, start, source, bad_head)
        except RuntimeError as exc:
            require(str(exc) == "resume_head_owner_pins", "owner_rejection_reason")
        else:
            raise RuntimeError("changed_owner_not_rejected")
    return {"status": "PASS", "synthetic_only": True, "tests": [
        "current-roots-and-nonempty-cap", "whole-step-before-head-and-prefix-resume",
        "postappend-character-change-and-owner-rejection"], "cross_checked": False, "verified": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--parent-layout-selftest", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max-appends", type=int, default=176)
    parser.add_argument("--max-seconds", type=float)
    names = ("state-root", "delta-root", "seed34-root", "prepare-root", "p1-root",
             "task712-root", "output-root")
    for name in names:
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--block-root", type=Path, action="append", default=[])
    args = parser.parse_args()
    paths = [getattr(args, name.replace("-", "_")) for name in names]
    try:
        require(0 <= args.max_appends <= 176 and
                (args.max_seconds is None or 0 < args.max_seconds < float("inf")), "bounded_resource_options")
        if args.parent_layout_selftest:
            require(not args.selftest and not args.resume and not args.block_root and
                    all(getattr(args, name) is not None for name in ("state_root", "delta_root", "seed34_root")) and
                    all(getattr(args, name) is None for name in
                        ("prepare_root", "p1_root", "task712_root", "output_root")),
                    "parent_layout_only_three_actual_roots")
            result = parent_layout_selftest(args)
        elif args.selftest:
            require(not any(path is not None for path in paths) and not args.block_root and not args.resume,
                    "selftest_without_actual_parents")
            result = selftest()
        else:
            require(all(path is not None for path in paths) and len(args.block_root) == 4,
                    "actual_fixed_parent_paths_required")
            result = run_actual(args)
        print(canonical(result).decode("ascii"), end="", flush=True)
        return 0
    except ResourceStop as exc:
        output = args.output_root.resolve() if args.output_root is not None else None
        head_raw = None
        if output is not None and (output / "HEAD").is_file() and not (output / "HEAD").is_symlink():
            head_raw = (output / "HEAD").read_bytes()
        diagnostic = seal("resource-stop", {"status": "UNKNOWN_RESOURCE", "terminal": "UNKNOWN_RESOURCE",
            "phase": str(exc), "complete_prefix_present": head_raw is not None,
            "head_sha256": sha(head_raw) if head_raw is not None else None,
            "candidate": False, "cross_checked": False, "verified": False})
        if output is not None and output.is_dir() and not output.is_symlink():
            write_json(output, "resource-stop.json", diagnostic, replace=True)
        progress("terminal", status="UNKNOWN_RESOURCE", phase_stopped=str(exc),
                 complete_prefix_present=head_raw is not None)
        print(canonical(diagnostic).decode("ascii"), end="", flush=True)
        return 3
    except Exception as exc:
        progress("terminal", status="REJECTED", reason=str(exc), error_type=type(exc).__name__)
        print(canonical({"status": "REJECTED", "reason": str(exc),
                         "cross_checked": False, "verified": False}).decode("ascii"), end="", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
