#!/usr/bin/env python3
"""Fail-closed checker for the W6 BOTTOM-UP exact-17 firing gate.

This checker only validates frozen structure and registered synthetic fixtures.
It does not enumerate groups, launch S1--S3.5/S9, or evaluate candidates.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[3]
MANIFEST_REL = "search/certs/w6_bu_firing_gate_manifest_v1.json"
SCHEMA_REL = "search/certs/w6_bu_firing_cert_schema_v1.json"
SOURCE_REL = "search/certs/h2_census_s4_20260805.json"
FIXTURE_DIR_REL = "search/probe/w6_bu_s0/firing_gate_fixtures_v1"
SOURCE_SHA256 = "4b8673209d55c46fe1bc01a1e2736df03f296cd7d775df6da98f8f582df73b30"
FREEZE_ID = "W6-BU-FREEZE2-EXACT17-F106"
FREEZE_AUTHORITY = "sol/sol_reply_106_math33.md F106-4"
PRE_AUTH_MANIFEST_SHA256 = "33554a07f019167ee193dfe09d5c3f67a23d39f70b0c992d91c1aafb8b262726"
EXPECTED_IDS = [
    "p2_d2_a0b0c1",
    "p2_d2_a0b1c0",
    "p2_d2_a2b0c0",
    "p2_d3_a1b0c1",
    "p2_d3_a1b1c0",
    "p2_d3_a3b0c0",
    "p2_d4_a0b0c2",
    "p2_d4_a0b1c1",
    "p2_d4_a0b2c0",
    "p2_d4_a2b0c1",
    "p2_d4_a2b1c0",
    "p2_d4_a4b0c0",
    "p3_d2_bruteforce_1",
    "p3_d2_bruteforce_2",
    "p3_d2_bruteforce_3",
    "p3_d2_bruteforce_4",
    "p3_d2_bruteforce_5",
]
DIMENSIONS = {2: {2, 3, 4}, 3: {2}}


class GateError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def fail(code: str, detail: str) -> None:
    raise GateError(code, detail)


def read_json(rel_or_path: str | Path) -> Any:
    path = Path(rel_or_path)
    if not path.is_absolute():
        path = REPO / path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("ARTIFACT_MISSING/STOP", str(path))
    except json.JSONDecodeError as exc:
        fail("JSON_PARSE_ERROR/STOP", f"{path}: {exc}")


def sha256_file(rel_or_path: str | Path) -> str:
    path = Path(rel_or_path)
    if not path.is_absolute():
        path = REPO / path
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    blob = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def row_projection(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keys = ("module_id", "p", "dim", "s3_inflated", "window_order")
    return [{key: row[key] for key in keys} for row in rows]


def validate_artifact_chain() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    manifest = read_json(MANIFEST_REL)
    schema = read_json(SCHEMA_REL)
    source = read_json(SOURCE_REL)

    if manifest.get("schema") != "w6-bu-firing-gate-manifest/v1":
        fail("MANIFEST_VERSION_MISMATCH/STOP", "manifest schema")
    expected_authorization = {
        "freeze_id": FREEZE_ID,
        "stage_unlock": True,
        "authority": FREEZE_AUTHORITY,
        "pre_authorization_manifest_sha256": PRE_AUTH_MANIFEST_SHA256,
        "dispatch_scope": "future workshop-only dispatch; no execution in task 106",
        "authorized_stages_after_future_unlock": ["S1", "S2", "S3", "S3.5"],
        "always_forbidden_here": [
            "S3.6", "S4", "S4prime", "S5", "S6", "S7", "S8", "S8.5", "S9",
            "exploration", "candidate_generation", "kill", "EMPTY",
        ],
    }
    if manifest.get("authorization") != expected_authorization:
        fail("AUTHORIZATION_BINDING_MISMATCH/STOP", "opaque freeze id, authority, scope, or lock set changed")
    if manifest.get("status") != "FROZEN; S1--S3.5 eligible only for future workshop dispatch; S3.6--S9 locked":
        fail("AUTHORIZATION_BINDING_MISMATCH/STOP", "manifest status changed")
    if schema.get("$id") != "urn:shadow-atelier:w6-bu-firing-cert:v1":
        fail("SCHEMA_VERSION_MISMATCH/STOP", "schema $id")
    if sha256_file(SOURCE_REL) != SOURCE_SHA256:
        fail("SOURCE_DIGEST_MISMATCH/STOP", SOURCE_REL)
    artifacts = manifest.get("artifacts", {})
    if artifacts.get("schema", {}).get("path") != SCHEMA_REL:
        fail("MANIFEST_SCHEMA_BINDING/STOP", "schema path")
    if artifacts.get("schema", {}).get("sha256") != sha256_file(SCHEMA_REL):
        fail("SCHEMA_DIGEST_MISMATCH/STOP", SCHEMA_REL)
    checker_binding = artifacts.get("checker", {})
    checker_rel = "search/probe/w6_bu_s0/check_firing_gate_v1.py"
    if checker_binding.get("path") != checker_rel or checker_binding.get("sha256") != sha256_file(checker_rel):
        fail("CHECKER_DIGEST_MISMATCH/STOP", checker_rel)
    for role, expected_path in (
        ("design_correction", "docs/notes/w6_bottomup_design_v4_1_addendum.md"),
        ("iso_erratum", "docs/notes/iso_r3r4_iffirst_freeze_v1_2_erratum.md"),
    ):
        binding = artifacts.get(role, {})
        if binding.get("path") != expected_path or binding.get("sha256") != sha256_file(expected_path):
            fail("DOCUMENT_DIGEST_MISMATCH/STOP", expected_path)
    source_binding = manifest.get("source_map", {})
    if source_binding.get("source_path") != SOURCE_REL or source_binding.get("source_sha256") != SOURCE_SHA256:
        fail("SOURCE_MAP_BINDING/STOP", "source path/digest")

    rows = source.get("rows")
    if not isinstance(rows, list) or source.get("row_count") != 17 or len(rows) != 17:
        fail("SOURCE_ROW_COUNT_MISMATCH/STOP", "source must contain exactly 17 rows")
    projection = row_projection(rows)
    projection_digest = canonical_sha256(projection)
    if source_binding.get("projection_sha256") != projection_digest:
        fail("SOURCE_PROJECTION_DIGEST_MISMATCH/STOP", projection_digest)
    if [row.get("module_id") for row in rows] != EXPECTED_IDS:
        fail("SOURCE_ROWSET_MISMATCH/STOP", "source order or ids changed")

    exact = manifest.get("exact_firing_universe", {})
    if exact != {
        "layer": "V-cen/S3-inflated",
        "dimension_by_prime": {"2": [2, 3, 4], "3": [2]},
        "window_order_lte": 8000,
        "expected_row_count": 17,
    }:
        fail("MANIFEST_UNIVERSE_MISMATCH/STOP", "exact firing universe")
    if manifest.get("denominator", {}).get("row_ids") != EXPECTED_IDS:
        fail("MANIFEST_DENOMINATOR_MISMATCH/STOP", "row ids/order")

    m8 = manifest.get("iso_gate_contract", {}).get("M-ISO-8", {})
    expected_m8 = {
        "real_verdict": "UNKNOWN(NONSHADOW_IN_DATUM)",
        "mutant_verdict": "UNKNOWN(NONSHADOW_IN_DATUM)",
        "detection_layer": "detail-element comparison only; verdict is insensitive",
        "real_witness_settled": False,
        "mutant_witness_settled": True,
        "isolated_false_witness_claim": False,
    }
    if m8 != expected_m8:
        fail("MISO8_SEMANTICS_STALE/STOP", "manifest does not bind v1.2 detail-level semantics")

    required_stops = {
        "DIMENSION_OUT_OF_SCOPE/STOP",
        "ORDER_CAP_EXCEEDED/STOP",
        "ROWSET_MISSING/STOP",
        "DUPLICATE_MODULE_ID/STOP",
        "SOURCE_MAP_MISSING/STOP",
        "SOURCE_DIGEST_MISMATCH/STOP",
        "AUTHORIZATION_BINDING_MISMATCH/STOP",
        "COUNT_ACCOUNTING_MISMATCH/STOP",
        "MISO8_SEMANTICS_STALE/STOP",
        "CLAIM_OVERREACH/STOP",
    }
    if not required_stops.issubset(set(manifest.get("stop_contract", []))):
        fail("STOP_CONTRACT_INCOMPLETE/STOP", "required stop codes missing")
    return manifest, schema, rows


def validate_cert(cert: dict[str, Any]) -> dict[str, Any]:
    manifest, _schema, source_rows = validate_artifact_chain()
    required_top = {
        "schema", "schema_sha256", "manifest", "run_class", "execution_authorized",
        "universe", "denominator", "source_map", "counts", "rows",
        "iso_gate_contract_snapshot", "claims", "status", "non_contact_declaration",
    }
    missing = sorted(required_top - set(cert))
    if missing:
        if "source_map" in missing:
            fail("SOURCE_MAP_MISSING/STOP", "source_map absent")
        if "counts" in missing:
            fail("COUNT_ACCOUNTING_MISMATCH/STOP", "counts absent")
        fail("SCHEMA_REQUIRED_FIELD_MISSING/STOP", ",".join(missing))
    if set(cert) != required_top:
        fail("SCHEMA_ADDITIONAL_FIELD/STOP", ",".join(sorted(set(cert) - required_top)))

    if cert["schema"] != "w6-bu-firing-cert/v1" or cert["schema_sha256"] != sha256_file(SCHEMA_REL):
        fail("SCHEMA_DIGEST_MISMATCH/STOP", "cert schema binding")
    manifest_ref = cert["manifest"]
    if manifest_ref != {"path": MANIFEST_REL, "sha256": sha256_file(MANIFEST_REL)}:
        fail("MANIFEST_DIGEST_MISMATCH/STOP", "cert manifest binding")
    run_class = cert["run_class"]
    if run_class == "SCHEMA_CALIBRATION_ONLY":
        if cert["execution_authorized"] is not False:
            fail("UNAUTHORIZED_EXECUTION/STOP", "calibration fixture cannot be authorized")
    elif run_class in {"S1", "S2", "S3", "S3.5"}:
        auth = manifest.get("authorization", {})
        if (not cert["execution_authorized"] or auth.get("freeze_id") != FREEZE_ID or
                auth.get("stage_unlock") is not True or auth.get("authority") != FREEZE_AUTHORITY or
                auth.get("dispatch_scope") != "future workshop-only dispatch; no execution in task 106"):
            fail("UNAUTHORIZED_EXECUTION/STOP", "Sol freeze id / authority / workshop-only scope mismatch")
    else:
        fail("RUN_CLASS_OUT_OF_SCOPE/STOP", str(run_class))

    expected_universe = {
        "layer": "V-cen/S3-inflated",
        "dimension_by_prime": {"2": [2, 3, 4], "3": [2]},
        "window_order_lte": 8000,
        "predicate_order": ["layer", "prime", "dimension_by_prime", "window_order_lte"],
    }
    if cert["universe"] != expected_universe:
        fail("UNIVERSE_MISMATCH/STOP", "cert universe")

    rows = cert["rows"]
    if not isinstance(rows, list):
        fail("SCHEMA_TYPE_ERROR/STOP", "rows must be an array")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            fail("SCHEMA_TYPE_ERROR/STOP", f"rows[{index}]")
        if row.get("s3_inflated") is not True:
            fail("LAYER_OUT_OF_SCOPE/STOP", f"rows[{index}]")
        p = row.get("p")
        dim = row.get("dim")
        if p not in DIMENSIONS:
            fail("PRIME_OUT_OF_SCOPE/STOP", f"rows[{index}].p={p}")
        if dim not in DIMENSIONS[p]:
            fail("DIMENSION_OUT_OF_SCOPE/STOP", f"rows[{index}] p={p}, dim={dim}")
        order = row.get("window_order")
        if not isinstance(order, int) or isinstance(order, bool):
            fail("SCHEMA_TYPE_ERROR/STOP", f"rows[{index}].window_order")
        if order > 8000:
            fail("ORDER_CAP_EXCEEDED/STOP", f"rows[{index}].window_order={order}")

    ids = [row.get("module_id") for row in rows]
    if len(ids) != len(set(ids)):
        fail("DUPLICATE_MODULE_ID/STOP", "row module_id duplicate")
    if len(ids) < 17 or set(ids) < set(EXPECTED_IDS):
        fail("ROWSET_MISSING/STOP", f"expected 17 ids, received {len(ids)}")
    if len(ids) > 17 or set(ids) > set(EXPECTED_IDS) or set(ids) != set(EXPECTED_IDS):
        fail("ROWSET_EXTRA/STOP", "unexpected module id")
    if ids != EXPECTED_IDS:
        fail("ROW_ORDER_MISMATCH/STOP", "source order changed")

    source_by_id = {row["module_id"]: row for row in source_rows}
    for index, row in enumerate(rows):
        source = source_by_id[row["module_id"]]
        for key in ("p", "dim", "s3_inflated", "window_order"):
            if row.get(key) != source.get(key):
                fail("SOURCE_ROW_MISMATCH/STOP", f"rows[{index}].{key}")
        if row.get("stage_status") not in {"NOT_RUN", "INVENTORY_ONLY", "UNKNOWN", "STOP"}:
            fail("SCHEMA_ENUM_ERROR/STOP", f"rows[{index}].stage_status")
        if row.get("stage_status") == "NOT_RUN" and row.get("stop_or_unknown") != "UNKNOWN(NOT_RUN_SCHEMA_FIXTURE)":
            fail("UNKNOWN_CONTRACT_MISMATCH/STOP", f"rows[{index}]")

    denominator = cert["denominator"]
    if denominator != {
        "unit": "V-cen module isomorphism type keyed by module_id",
        "expected_count": 17,
        "selected_row_count": 17,
        "row_ids": EXPECTED_IDS,
    }:
        fail("DENOMINATOR_MISMATCH/STOP", "exact 17-row denominator")

    source_map = cert["source_map"]
    expected_entries = [
        {"module_id": module_id, "source_pointer": f"/rows/{index}", "stage_tag": "FIRING_UNIVERSE_SELECTION"}
        for index, module_id in enumerate(EXPECTED_IDS)
    ]
    if source_map != {
        "source_path": SOURCE_REL,
        "source_sha256": SOURCE_SHA256,
        "json_pointer": "/rows",
        "projection_sha256": canonical_sha256(row_projection(source_rows)),
        "entries": expected_entries,
    }:
        fail("SOURCE_MAP_MISMATCH/STOP", "source map must rederive every row")

    counts = cert["counts"]
    required_count_keys = {
        "traversed_count", "accepted_count", "rejected_count", "traversed_unit", "accepted_unit", "relation", "witnesses"
    }
    if not isinstance(counts, dict) or set(counts) != required_count_keys:
        fail("COUNT_ACCOUNTING_MISMATCH/STOP", "distinct count fields required")
    values = [counts.get(key) for key in ("traversed_count", "accepted_count", "rejected_count")]
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
        fail("COUNT_ACCOUNTING_MISMATCH/STOP", "counts must be nonnegative integers")
    if counts["traversed_count"] != counts["accepted_count"] + counts["rejected_count"]:
        fail("COUNT_ACCOUNTING_MISMATCH/STOP", "traversed != accepted + rejected")
    if counts["traversed_unit"] != "enumerated parameter/lift before acceptance filters; never H1-conjugacy classes":
        fail("COUNT_UNIT_MISMATCH/STOP", "traversed unit")
    if counts["accepted_unit"] != "objects after all stage-local acceptance filters":
        fail("COUNT_UNIT_MISMATCH/STOP", "accepted unit")
    if counts["relation"] != "traversed_count = accepted_count + rejected_count; fields are not aliases":
        fail("COUNT_ACCOUNTING_MISMATCH/STOP", "relation text")
    witnesses = counts["witnesses"]
    if not isinstance(witnesses, list) or len(witnesses) != counts["traversed_count"]:
        fail("COUNT_WITNESS_MISMATCH/STOP", "one witness per traversal is required")
    traversal_ids = [item.get("traversal_id") for item in witnesses if isinstance(item, dict)]
    if len(traversal_ids) != len(witnesses) or len(set(traversal_ids)) != len(witnesses):
        fail("COUNT_WITNESS_MISMATCH/STOP", "traversal_id must be present and unique")
    accepted_witnesses = sum(item.get("disposition") == "ACCEPTED" for item in witnesses)
    rejected_witnesses = sum(item.get("disposition") == "REJECTED" for item in witnesses)
    if accepted_witnesses != counts["accepted_count"] or rejected_witnesses != counts["rejected_count"]:
        fail("COUNT_WITNESS_MISMATCH/STOP", "witness dispositions do not reproduce counts")
    if any(not isinstance(item.get("source_tag"), str) or not item["source_tag"] for item in witnesses):
        fail("COUNT_WITNESS_MISMATCH/STOP", "every witness needs a source_tag")
    if run_class == "SCHEMA_CALIBRATION_ONLY" and values != [19, 17, 2]:
        fail("COUNT_CALIBRATION_WEAK/STOP", "positive fixture must exercise traversed != accepted")

    expected_m8 = {
        "m_iso8_real_verdict": "UNKNOWN(NONSHADOW_IN_DATUM)",
        "m_iso8_mutant_verdict": "UNKNOWN(NONSHADOW_IN_DATUM)",
        "m_iso8_detection_layer": "detail-element comparison only; verdict is insensitive",
        "real_witness_settled": False,
        "mutant_witness_settled": True,
        "isolated_false_witness_claim": False,
    }
    if cert["iso_gate_contract_snapshot"] != expected_m8:
        fail("MISO8_SEMANTICS_STALE/STOP", "verdict mismatch attribution is forbidden")

    claims = cert["claims"]
    expected_claims = {
        "isolated_verdict": "UNKNOWN",
        "kill_claim": False,
        "candidate_found": False,
        "empty_claim": False,
        "scope_of_any_coverage": "exact firing universe only; no statement about W \\ W_adm or supplemental inventory",
    }
    if claims != expected_claims:
        fail("CLAIM_OVERREACH/STOP", "isolated=FALSE/kill/candidate/EMPTY are forbidden")

    status = cert["status"]
    if run_class == "SCHEMA_CALIBRATION_ONLY" and status != {
        "coverage_status": "NOT_RUN",
        "stop_code": None,
        "unknown_reason": "UNKNOWN(NOT_RUN_SCHEMA_FIXTURE)",
    }:
        fail("STATUS_OVERREACH/STOP", "calibration fixture must remain NOT_RUN/UNKNOWN")

    noncontact = cert["non_contact_declaration"]
    expected_noncontact = {
        "exploration": False,
        "candidate_generation": False,
        "kill": False,
        "empty_theorem": False,
        "im_R": False,
        "d_N": False,
        "sealed_quantities": False,
        "S9": False,
    }
    if noncontact != expected_noncontact:
        fail("NONCONTACT_BREACH/STOP", "all protected actions must be false")
    return {
        "verdict": "PASS",
        "row_count": 17,
        "projection_sha256": canonical_sha256(row_projection(source_rows)),
        "traversed_count": counts["traversed_count"],
        "accepted_count": counts["accepted_count"],
    }


def pointer_parent(value: Any, pointer: str) -> tuple[Any, str]:
    parts = pointer.lstrip("/").split("/")
    current = value
    for raw in parts[:-1]:
        key = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(key)] if isinstance(current, list) else current[key]
    return current, parts[-1].replace("~1", "/").replace("~0", "~")


def pointer_get(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    parent, key = pointer_parent(value, pointer)
    return parent[int(key)] if isinstance(parent, list) else parent[key]


def apply_patches(base: dict[str, Any], patches: list[dict[str, Any]]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for patch in patches:
        op = patch["op"]
        parent, key = pointer_parent(result, patch["path"])
        slot: int | str = int(key) if isinstance(parent, list) else key
        if op == "replace":
            parent[slot] = patch["value"]
        elif op == "remove":
            if isinstance(parent, list):
                parent.pop(slot)
            else:
                del parent[slot]
        elif op == "copy":
            parent[slot] = copy.deepcopy(pointer_get(result, patch["from"]))
        else:
            fail("MUTATION_SPEC_ERROR/STOP", f"unknown op {op}")
    return result


def load_case(path: Path) -> tuple[dict[str, Any], str, str | None]:
    value = read_json(path)
    if value.get("schema") == "w6-bu-firing-mutant/v1":
        base = read_json(value["base"])
        cert = apply_patches(base, value["patches"])
        return cert, value["mutation_id"], value["expected_stop"]
    return value, path.stem, None


def self_test() -> dict[str, Any]:
    fixture_dir = REPO / FIXTURE_DIR_REL
    paths = sorted(fixture_dir.glob("*.json"))
    if not paths:
        fail("FIXTURE_SET_MISSING/STOP", FIXTURE_DIR_REL)
    results: list[dict[str, Any]] = []
    for path in paths:
        cert, case_id, expected_stop = load_case(path)
        try:
            detail = validate_cert(cert)
            actual = "PASS"
        except GateError as exc:
            detail = {"detail": exc.detail}
            actual = exc.code
        expected = expected_stop or "PASS"
        matched = actual == expected
        results.append({
            "fixture": path.relative_to(REPO).as_posix(),
            "case_id": case_id,
            "expected": expected,
            "actual": actual,
            "matched": matched,
            "detail": detail,
        })
    if not all(item["matched"] for item in results):
        fail("SELF_TEST_FAILED/STOP", json.dumps(results, ensure_ascii=False))
    return {
        "schema": "w6-bu-firing-gate-receipt/v1",
        "checker_sha256": sha256_file("search/probe/w6_bu_s0/check_firing_gate_v1.py"),
        "schema_sha256": sha256_file(SCHEMA_REL),
        "manifest_sha256": sha256_file(MANIFEST_REL),
        "source_sha256": sha256_file(SOURCE_REL),
        "fixture_count": len(results),
        "positive_passed": sum(1 for item in results if item["expected"] == "PASS" and item["matched"]),
        "mutants_rejected": sum(1 for item in results if item["expected"] != "PASS" and item["matched"]),
        "all_expected_results_matched": True,
        "results": results,
        "non_contact_declaration": {
            "exploration": False,
            "S1_to_S3_5": False,
            "S9": False,
            "candidate_generation": False,
            "kill": False,
            "empty_theorem": False,
            "sealed_quantities": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", type=Path)
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            result = self_test()
        else:
            cert, case_id, expected_stop = load_case(args.check)
            result = {"case_id": case_id, "expected_stop": expected_stop, **validate_cert(cert)}
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except GateError as exc:
        print(json.dumps({"verdict": "STOP", "stop_code": exc.code, "detail": exc.detail}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
