#!/usr/bin/env python3
"""Task191: exact batched boundary-column generation (v2).

The task187 v1 runtime is an authenticated arithmetic source only.  This
module owns the batch scheduler, literal row cache, checkpoint replay, and
the bounded noncommutative self-test.
"""
from __future__ import annotations

import argparse, copy, hashlib, importlib.util, itertools, json, sys, tempfile, time
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-u0v0-boundary-preimage-batch/v2"
SELFTEST_SCHEMA = "d972-r07-u0v0-boundary-preimage-batch-selftest/v2"
COMMON = "R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
ALLOWED_RESOURCE_CAPS = {
    "task175_reconstruction": {"wall_seconds", "rss_bytes"},
    "fine_deletion": {"wall_seconds", "rss_bytes"},
    "Q0_positive_shortlex_section": {"wall_seconds", "rss_bytes"},
    "Q0_discovery": {"wall_seconds", "rss_bytes"},
    "A_L_membership_scan": {"wall_seconds", "rss_bytes"},
    "L_subgroup_closure": {"wall_seconds", "rss_bytes"},
    "typed_singleton_equality": {"wall_seconds", "rss_bytes"},
    "runtime_reconstruction": {"wall_seconds", "rss_bytes"},
    "complete_boundary_correlation": {"wall_seconds", "rss_bytes", "boundary_pairs", "oracle_rounds"},
    "boundary_echelon": {"wall_seconds", "rss_bytes", "retained_columns"},
    "checkpoint_serialization": {"checkpoint_bytes"},
}
ALLOWED_INPUT_PREFIXES = ("pin:", "v1 loader", "task179:")
V1_PINS = {
    "producer": ("search/d972_r07_u0v0_boundary_preimage_v1.py", 35173, "18040f4f73fe963632bbd2200e730818a7354c5963143a5871e73b2d1284dbfe"),
    "checker": ("crosscheck/check_d972_r07_u0v0_boundary_preimage_v1.py", 32825, "e94d19311d0afe23fde869045f959490528d18e0f3537209e57b7cbefb452b18"),
    "driver": ("search/d972_r07_u0v0_boundary_preimage_gha_driver_v1.g", 7721, "16d354d387db53cfadd22a7442f9a7aa77580c8410664f9dd5b1a618fef026b8"),
    "fixture": ("search/certs/d972_r07_u0v0_boundary_preimage_selftest_v1_20260827.json", 699, "230de05643a94f775120ef7e62b2f2023b13fd12228f18ca860ef81b134babff"),
}
TASK179_PINS = {
    "producer": ("search/d972_r07_positive_common_word_colgen_v1.py", 123870, "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    "checker": ("crosscheck/check_d972_r07_positive_common_word_colgen_v1.py", 73780, "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"),
    "driver": ("search/d972_r07_positive_common_word_colgen_gha_driver_v1.g", 12872, "48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"),
    "fixture": ("search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json", 407, "46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"),
    "v156": ("sol/proof_r07_task179_exact_exponent_lattice_v156.md", 10409, "2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d"),
    "v157": ("sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md", 8367, "08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8"),
    "task179_instruction": ("sol/luna_task_179_r07_positive_common_word_colgen_v1.md", 13105, "f97870ec0243b2c399928bcef4f89134f1cd41f15869cc88e3ba7d9dc6956a73"),
    "proof142": ("sol/proof_r07_actual_singleton_coarse_inverse_selector_v142.md", 4942, "5f0fffe64b729a8e44643ce86e9d588ef96cbe199ef8ca03741c712c2b162ee8"), "proof143": ("sol/proof_r07_actual_weighted_support_hitting_selector_v143.md", 5253, "aae57d5481d7e649d449b58d06ade2d9cbf90fa48d50a8ae43650da5243cf259"), "proof139": ("sol/proof_r07_witness_first_fibre_dovetail_selector_v139.md", 8310, "62e2160348db38eca1570b2ca6eb8934b885569f4e8cfb276a91b98c9b983920"), "proof140": ("sol/proof_r07_positive_only_common_word_colgen_v140.md", 10073, "6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b"), "proof138": ("sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md", 6371, "9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456"),
    "proof110": ("sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md", 12136, "dd0b75d6dc85229405a3a95e3631a709aa40a0ad21f2c17b96106dae2c7989dc"), "proof108": ("sol/proof_pb4_eleven_relator_presentation_equality_v108.md", 6742, "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"), "proof121": ("sol/proof_pb3_two_relator_presentation_equality_v121.md", 5762, "efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5"), "proof122": ("sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md", 7939, "daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348"), "proof125": ("sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md", 8545, "b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3"), "proof135": ("sol/proof_r07_q4_q0_noncontiguous_deletion_layout_v135.md", 4539, "75c511a765ad88ec1aa72c63a0d1965ac85724695d743cbf00350572a884cf67"),
    "task175_producer": ("search/d972_r07_all_seven_raw_bridge_preflight_v1.py", 60306, "1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"), "task175_checker": ("crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py", 88503, "0b45c3daa1db6cad63d434170c65d0dbfa928efc51543b881dc0aa2e3a0f1fce"), "task175_driver": ("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g", 22052, "919e7a9efe7385444c480203dc51525873e770236777dd61e2f6fc1ef22de494"), "task176_producer": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109, "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"), "task176_checker": ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980, "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"), "task176_driver": ("search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g", 15929, "1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995"),
    "q3_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"), "joint_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036, "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"), "seedspan_arithmetic": ("search/d972_b345_seedspan_triple4_v1.py", 535219, "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"), "old_arithmetic": ("search/d972_b345_triple_cube_raw_lambda_census_v1.py", 126942, "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"), "joint_source": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945, "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"), "v172_source": ("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", 21918, "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"), "g760_source": ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409, "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"), "pb4_source": ("search/d972_b345_target6_dual_colgen_v2.py", 444497, "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"), "full_d2_v1": ("search/d972_b345_full_d2_dual_correlation_v1.py", 78832, "6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52"), "full_d2_v2": ("search/d972_b345_full_d2_dual_correlation_v2.py", 42449, "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f"),
}

class InputStop(RuntimeError): pass
class ResourceStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float, limit: int | float,
                 resource: dict[str, Any] | None = None):
        super().__init__(f"{phase}:{cap}:{value}>{limit}")
        self.phase, self.cap, self.value, self.limit, self.resource = phase, cap, value, limit, resource
class SelftestInterrupt(RuntimeError): pass

def require(ok: bool, msg: str) -> None:
    if not ok: raise RuntimeError(msg)

def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")

def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()

def seal(value: dict[str, Any]) -> dict[str, Any]:
    out = dict(value); out.pop("self_digest", None); out["self_digest"] = digest(out); return out

def authenticate(table: dict[str, tuple[str, int, str]]) -> dict[str, Any]:
    out = {}
    for name, (rel, size, sha) in table.items():
        raw = (ROOT / rel).read_bytes() if (ROOT / rel).is_file() else b""
        if len(raw) != size or hashlib.sha256(raw).hexdigest() != sha: raise InputStop("pin:" + rel)
        out[name] = {"path": rel, "bytes": size, "sha256": sha}
    return out

def expected_manifest(table: dict[str, tuple[str, int, str]]) -> dict[str, Any]:
    return {name: {"path": rel, "bytes": size, "sha256": sha}
            for name, (rel, size, sha) in table.items()}

def expected_pins() -> dict[str, Any]:
    return {"v1": expected_manifest(V1_PINS), "task179": expected_manifest(TASK179_PINS)}

def load_v1() -> Any:
    path = ROOT / V1_PINS["producer"][0]
    spec = importlib.util.spec_from_file_location("task187_v1_authenticated_source", path)
    if spec is None or spec.loader is None: raise InputStop("v1 loader")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    try:
        wrapper_pins = module.authenticate_sources() if hasattr(module, "authenticate_sources") else {}
        arithmetic = module.load_task179() if hasattr(module, "load_task179") else None
    except module.InputStop as exc:
        reason = str(exc)
        # Normalize the legacy bare ``task179 loader`` reason into the
        # registered namespace; preserve already authenticated pin/task179
        # reasons verbatim for the UNKNOWN_INPUT contract.
        if not (reason.startswith("pin:") or reason.startswith("task179:") or reason.startswith("v1 loader")):
            reason = "task179:" + reason
        raise InputStop(reason) from exc
    if arithmetic is None: raise InputStop("v1 loader: task179 arithmetic")
    # task187 is the authenticated boundary scheduler, while task179 owns the
    # runtime/model ABI.  Bind the latter explicitly instead of returning a
    # wrapper whose local solve() happens to close over it.
    for name in ("exponent_key", "decode_row_key", "group_for_block", "boundary_source",
                 "translated_boundary", "unpack_element", "element_blob", "public_sparse",
                 "AllSevenModel"):
        if hasattr(arithmetic, name): setattr(module, name, getattr(arithmetic, name))
    module.Monitor = arithmetic.Monitor
    module._boundary_task179_pins = getattr(arithmetic, "_boundary_task179_pins", {})
    def build_runtime(monitor: Any) -> dict[str, Any]:
        try:
            return arithmetic.build_runtime(monitor)
        except arithmetic.ResourceStop as exc:
            phase = getattr(exc, "phase", "task179"); cap = getattr(exc, "cap", "unknown")
            snapshot = monitor.public()
            if cap == "wall_seconds": snapshot["elapsed_seconds"] = getattr(exc, "value", snapshot["elapsed_seconds"])
            if cap == "rss_bytes": snapshot["rss_bytes"] = getattr(exc, "value", snapshot["rss_bytes"])
            raise module.ResourceStop(phase, cap, getattr(exc, "value", 0),
                                      getattr(exc, "limit", 0), snapshot) from exc
        except arithmetic.InputStop as exc:
            raise module.InputStop("task179:" + str(exc)) from exc
    module.build_runtime = build_runtime
    module._wrapper_pin_identity = wrapper_pins
    return module

def public(v1: Any, row: dict[bytes, int]) -> list[list[Any]]: return v1.public_sparse(row)

def pair(v1: Any, f: dict[bytes, int], row: dict[bytes, int]) -> int: return v1.pair(f, row)

def occurrence_roster(v1: Any, runtime: dict[str, Any]) -> list[dict[str, Any]]:
    """One typed occurrence table per runtime; no translation pre-enumeration."""
    result = []
    for block, count in ((1, 2), (2, 2), (3, 11)):
        q = v1.group_for_block(runtime, block)
        for index in range(1, count + 1):
            for component, h_hex, base in v1.boundary_source(runtime, block, index):
                h_blob = bytes.fromhex(str(h_hex)); h = v1.unpack_element(runtime, h_blob, block)
                result.append({"block": block, "relator_index": index, "component": int(component),
                    "h_blob": h_blob, "h": h, "h_inv": q.inverse(h), "base_coefficient": int(base) % 3})
    return result

def public_occurrences(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"block": int(x["block"]), "relator_index": int(x["relator_index"]), "component": int(x["component"]),
             "h_blob": x["h_blob"].hex(), "base_coefficient": int(x["base_coefficient"])} for x in items]

def correlate(v1: Any, runtime: dict[str, Any], occurrences: list[dict[str, Any]],
              dual: dict[bytes, int], budget: Any, stats: dict[str, Any], audit: bool = False) -> dict[str, Any]:
    support: dict[tuple[int, int], list[tuple[bytes, int, Any]]] = {}
    for key, coefficient in dual.items():
        if key[:1] == b"R":
            block, component, blob = v1.decode_row_key(key)
            support.setdefault((block, component), []).append((blob, int(coefficient), v1.unpack_element(runtime, blob, block)))
    acc: dict[tuple[int, bytes, int], int] = {}; contributors: dict[tuple[int, bytes, int], list[dict[str, Any]]] = {}
    for item in occurrences:
        for g_blob, lam, g in support.get((item["block"], item["component"]), []):
            if not audit:
                budget.bump("boundary_pairs", 1, "complete_boundary_correlation")
                stats["support_occurrence_pairs_total"] += 1
            q = v1.group_for_block(runtime, item["block"]); t = q.mul(g, item["h_inv"])
            require(q.mul(t, item["h"]) == g, "left translation t=g*h^-1; t*h=g")
            t_blob = v1.element_blob(runtime, t); key = (item["block"], t_blob, item["relator_index"])
            acc[key] = (acc.get(key, 0) + lam * item["base_coefficient"]) % 3
            contributors.setdefault(key, []).append({"component": item["component"], "g_hex": g_blob.hex(),
                "h_hex": item["h_blob"].hex(), "lambda_coefficient": lam, "base_coefficient": item["base_coefficient"]})
    for rows in contributors.values(): rows.sort(key=lambda x: (x["component"], x["g_hex"], x["h_hex"], x["lambda_coefficient"], x["base_coefficient"]))
    active_internal = sorted((b, t, i) for (b, t, i), value in acc.items() if value % 3)
    if not audit:
        stats["complete_correlation_rounds"] += 1
        stats["pairs_per_round"].append(stats["support_occurrence_pairs_total"] - sum(stats["pairs_per_round"]))
    return {"complete": True, "sampled": False, "active": [[b, t.hex(), i] for b, t, i in active_internal],
            "scanned_occurrences": sum(len(x) for x in contributors.values()),
            "contributors": {f"{b}:{t.hex()}:{i}": rows for (b, t, i), rows in contributors.items()},
            "accumulated": {f"{b}:{t.hex()}:{i}": int(value) for (b, t, i), value in acc.items() if value % 3}}

def write_checkpoint(path: Path, pins: dict[str, Any], columns: list[dict[str, Any]],
                     batch_records: list[dict[str, Any]], correlations: list[dict[str, Any]],
                     transitions: list[dict[str, Any]], unresolved: list[str], active_suffix: list[Any],
                     pending_batch: dict[str, Any] | None, target_progress: dict[str, Any], stats: dict[str, Any],
                     reconsiderations: list[dict[str, Any]], budget: Any = None) -> None:
    def strip_row(value: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in value.items() if k != "row_dict"}
    body = {"schema": SCHEMA + "/checkpoint", "input_identity": pins,
            "columns": [strip_row(x) for x in columns],
            "batch_records": [strip_row(x) for x in batch_records], "correlations": correlations,
            "rank_transitions": transitions, "unresolved": list(unresolved), "active_suffix": active_suffix,
            "pending_batch": pending_batch, "target_progress": target_progress, "stats": stats,
            "target_reconsideration_log": [strip_row(x) for x in reconsiderations], "self_digest": ""}
    body["self_digest"] = digest({k: v for k, v in body.items() if k != "self_digest"})
    raw = canonical(body) + b"\n"
    if budget is not None and hasattr(budget, "limits") and "checkpoint_bytes" in budget.limits:
        size = len(raw)
        if hasattr(budget, "phase"):
            budget.phase = "checkpoint_serialization"
        if size > budget.limits["checkpoint_bytes"]:
            resource = budget.public() if hasattr(budget, "public") else {}
            raise ResourceStop("checkpoint_serialization", "checkpoint_bytes", size,
                               budget.limits["checkpoint_bytes"], resource)
        if hasattr(budget, "counters"):
            budget.counters["checkpoint_bytes"] = size
    path.parent.mkdir(parents=True, exist_ok=True); tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(raw); tmp.replace(path)

def _record_without_row(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key != "row_dict"}


def replay_checkpoint(v1: Any, runtime: dict[str, Any], checkpoint: dict[str, Any],
                      targets: dict[str, Any], occurrences: list[dict[str, Any]]) -> dict[str, Any]:
    """Rebuild the whole saved transcript from literal boundary rows.

    A checkpoint is an untrusted local artifact.  Retained rows are replayed
    through a fresh echelon, dependent rows are reconstructed from that same
    echelon, and every completed correlation is recomputed before a suffix is
    allowed to resume.
    """
    body = dict(checkpoint); claimed = body.pop("self_digest", None)
    require(set(checkpoint) == {"schema", "input_identity", "columns", "batch_records", "correlations",
                                "rank_transitions", "unresolved", "active_suffix", "pending_batch",
                                "target_progress", "stats", "target_reconsideration_log", "self_digest"},
            "checkpoint field schema")
    require(type(claimed) is str and claimed == digest(body), "checkpoint self digest")
    columns_payload = checkpoint.get("columns")
    batch_payload = checkpoint.get("batch_records")
    correlations = checkpoint.get("correlations")
    transitions_payload = checkpoint.get("rank_transitions")
    reconsideration_payload = checkpoint.get("target_reconsideration_log")
    require(type(columns_payload) is list and type(batch_payload) is list and
            type(correlations) is list and type(transitions_payload) is list and
            type(reconsideration_payload) is list, "checkpoint transcript schema")

    column_payload: dict[int, dict[str, Any]] = {}
    for column in columns_payload:
        require(type(column) is dict and column.get("classification") == "retained", "checkpoint retained schema")
        column_id = column.get("column_id")
        require(type(column_id) is int and not isinstance(column_id, bool) and column_id > 0 and
                column_id not in column_payload, "checkpoint column id")
        column_payload[column_id] = column
    require(sorted(column_payload) == list(range(1, len(column_payload) + 1)), "checkpoint contiguous columns")

    by_batch: dict[int, list[dict[str, Any]]] = {}
    for record in batch_payload:
        require(type(record) is dict, "checkpoint batch record")
        batch_id = record.get("batch_id")
        require(type(batch_id) is int and not isinstance(batch_id, bool) and batch_id > 0, "checkpoint batch id")
        by_batch.setdefault(batch_id, []).append(record)
    expected_batch_ids = set(range(1, len(correlations) + 1))
    require(set(by_batch).issubset(expected_batch_ids), "checkpoint batch id coverage")

    pending = checkpoint.get("pending_batch")
    pending_id: int | None = None
    pending_position: int | None = None
    if pending is not None:
        require(type(pending) is dict and set(pending) == {"batch_id", "target_label", "dual", "correlation", "next_position"} and
                type(pending.get("correlation")) is dict and
                type(pending["correlation"].get("active")) is list, "checkpoint pending batch")
        pending_id = pending.get("batch_id"); pending_position = pending.get("next_position")
        require(type(pending_id) is int and not isinstance(pending_id, bool) and
                pending_id == len(correlations) and type(pending_position) is int and
                not isinstance(pending_position, bool), "checkpoint pending identity")
        require(pending_id > 0 and pending["target_label"] == correlations[pending_id - 1]["target_label"] and
                pending["dual"] == correlations[pending_id - 1]["dual"] and
                pending["correlation"] == correlations[pending_id - 1]["correlation"], "checkpoint pending correlation")
        active = pending["correlation"]["active"]
        require(0 <= pending_position <= len(active) and checkpoint.get("active_suffix") == active[pending_position:],
                "checkpoint ACTIVE suffix")
    else:
        require(checkpoint.get("active_suffix") == [], "checkpoint completed suffix")

    transition_map: dict[tuple[int, int], dict[str, Any]] = {}
    for transition in transitions_payload:
        require(type(transition) is dict and type(transition.get("batch_id")) is int and
                not isinstance(transition.get("batch_id"), bool) and type(transition.get("batch_position")) is int and
                not isinstance(transition.get("batch_position"), bool), "checkpoint rank transition")
        key = (transition["batch_id"], transition["batch_position"])
        require(key not in transition_map, "checkpoint duplicate transition")
        transition_map[key] = transition
    log_map: dict[tuple[int, int], dict[str, Any]] = {}
    for point in reconsideration_payload:
        require(type(point) is dict and type(point.get("batch_id")) is int and
                not isinstance(point.get("batch_id"), bool) and type(point.get("batch_position")) is int and
                not isinstance(point.get("batch_position"), bool), "checkpoint reconsideration")
        key = (point["batch_id"], point["batch_position"])
        require(key not in log_map, "checkpoint duplicate reconsideration")
        log_map[key] = point

    echelon = v1.Echelon(); row_by_id: dict[int, dict[bytes, int]] = {}
    columns: list[dict[str, Any]] = []; replayed_records: list[dict[str, Any]] = []
    retained_ids: set[int] = set(); decisions = {"u0": "UNRESOLVED", "v0": "UNRESOLVED"}
    terminal_duals: dict[str, dict[str, Any]] = {}

    def reconsider_replayed() -> dict[str, str]:
        result: dict[str, str] = {}
        for label in ("u0", "v0"):
            remainder, coefficients = echelon.reduce(targets[label]["target_row"])
            if not remainder:
                chain = [[int(key), int(value) % 3] for key, value in sorted(coefficients.items())]
                literal: dict[bytes, int] = {}
                for key, coefficient in chain:
                    require(key in row_by_id, label + " checkpoint chain id")
                    v1.add_scaled(literal, row_by_id[key], coefficient)
                require(literal == targets[label]["target_row"], label + " checkpoint member chain")
                targets[label].update(decision="MEMBER_D", chain=chain, literal_boundary_sum=public(v1, literal),
                                      zero_residual=[], zero_residual_sha256=digest([]), terminal_dual=None)
                decisions[label] = "MEMBER_D"; result[label] = "MEMBER_D"
            elif decisions[label] == "NONMEMBER_D":
                terminal = terminal_duals.get(label); require(type(terminal) is dict, label + " checkpoint terminal dual")
                functional = sparse_private(terminal["row"])
                require(terminal.get("row_sha256") == digest(terminal.get("row")) and
                        terminal.get("pairing_target") == pair(v1, functional, targets[label]["target_row"]) != 0 and
                        all(pair(v1, functional, row) == 0 for row in row_by_id.values()),
                        label + " checkpoint terminal preservation")
                terminal["annihilates_retained"] = True
                targets[label].update(decision="NONMEMBER_D", chain=[], terminal_dual=terminal)
                result[label] = "NONMEMBER_D"
            else:
                targets[label].update(decision=None, chain=[], terminal_dual=None)
                decisions[label] = "UNRESOLVED"; result[label] = "UNRESOLVED"
        return result

    reconsider_replayed()
    for batch_id, batch in enumerate(correlations, 1):
        require(type(batch) is dict and batch.get("target_label") in targets, "checkpoint correlation label")
        label = str(batch["target_label"]); require(decisions[label] == "UNRESOLVED", "checkpoint stale target decision")
        target = targets[label]["target_row"]; dual = sparse_private(batch.get("dual"))
        fresh_dual = echelon.dual(target)
        require(public(v1, fresh_dual) == batch.get("dual"), "checkpoint fresh dual")
        recomputed = correlate(v1, runtime, occurrences, dual, None, {}, audit=True)
        require(recomputed == batch.get("correlation"), "checkpoint complete correlation replay")
        active = recomputed["active"]
        records = sorted(by_batch.get(batch_id, []), key=lambda value: value.get("batch_position", -1))
        count = pending_position if pending_id == batch_id else len(active)
        require(count is not None and len(records) == count and
                [value.get("batch_position") for value in records] == list(range(count)),
                "checkpoint contiguous ACTIVE prefix")
        for position, record in enumerate(records):
            require(record.get("target_label") == label and record.get("batch_id") == batch_id and
                    type(record.get("batch_position")) is int and not isinstance(record.get("batch_position"), bool) and
                    type(record.get("rank_before")) is int and not isinstance(record.get("rank_before"), bool) and
                    type(record.get("rank_after")) is int and not isinstance(record.get("rank_after"), bool) and
                    record.get("batch_position") == position and record.get("classification") in ("retained", "dependent"),
                    "checkpoint batch transcript")
            provenance = record.get("provenance")
            require(type(provenance) is dict and provenance.get("family") == "boundary" and
                    provenance.get("left_translation") == "t=g*h^-1; t*h=g" and
                    provenance.get("complete_support_occurrence_accumulation") is True and
                    provenance.get("active_key") == active[position], "checkpoint provenance")
            block, translation_hex, relator_index = active[position]
            require(provenance.get("block") == block and provenance.get("base_relator_index") == relator_index and
                    provenance.get("translation_hex") == translation_hex, "checkpoint active provenance")
            row = v1.translated_boundary(runtime, int(block), int(relator_index), bytes.fromhex(translation_hex))
            row_public = public(v1, row); key_text = f"{block}:{translation_hex}:{relator_index}"
            require(row_public == record.get("sparse_row") and
                    record.get("sparse_row_sha256") == digest(record.get("sparse_row")) and
                    provenance.get("contributing_pairs") == recomputed["contributors"].get(key_text, []),
                    "checkpoint literal row")
            require(record.get("active_dual") == batch.get("dual") and
                    record.get("active_dual_sha256") == digest(record.get("active_dual")) and
                    record.get("dual_pairing") == pair(v1, dual, row) and
                    provenance.get("pre_batch_dual_pairing") == pair(v1, dual, row),
                    "checkpoint dual provenance")
            before = len(echelon.order)
            if record["classification"] == "retained":
                column_id = record.get("column_id")
                require(type(column_id) is int and column_id == len(row_by_id) + 1 and column_id in column_payload,
                        "checkpoint retained id")
                column = column_payload[column_id]
                require(_record_without_row(column) == _record_without_row(record), "checkpoint retained record")
                pivot, ancestry = echelon.add(row, column_id)
                require(record.get("rank_before") == before and record.get("rank_after") == len(echelon.order) and
                        pivot.hex() == record.get("pivot_hex") and
                        record.get("pivot_ancestry") == [[key, value] for key, value in sorted(ancestry.items())],
                        "checkpoint retained replay")
                row_by_id[column_id] = row; column["row_dict"] = row; columns.append(column); retained_ids.add(column_id)
            else:
                require("column_id" not in record and record.get("rank_before") == before and
                        record.get("rank_after") == before, "checkpoint dependent rank")
                remainder, dependency = echelon.reduce(row); require(not remainder, "checkpoint dependent row")
                rebuilt: dict[bytes, int] = {}
                for key, coefficient in record.get("dependency_chain", []):
                    require(type(key) is int and key in row_by_id and key <= len(row_by_id), "checkpoint dependency id")
                    v1.add_scaled(rebuilt, row_by_id[key], int(coefficient))
                require(rebuilt == row and record.get("dependency_chain") ==
                        [[key, value] for key, value in sorted(dependency.items())], "checkpoint dependent replay")
            record["row_dict"] = row; replayed_records.append(record)
            decisions_now = reconsider_replayed()
            expected_transition = {"batch_id": batch_id, "batch_position": position,
                                   "classification": record["classification"], "rank_before": record["rank_before"],
                                   "rank_after": record["rank_after"], "target_reconsidered": decisions_now}
            require(transition_map.get((batch_id, position)) == expected_transition and
                    log_map.get((batch_id, position)) == {"batch_id": batch_id, "batch_position": position, "decisions": decisions_now},
                    "checkpoint target transcript")
        if pending_id == batch_id:
            require(count <= len(active), "checkpoint pending position")
        else:
            require(count == len(active), "checkpoint complete batch")
            if not active:
                functional = sparse_private(batch["dual"])
                annihilates = all(pair(v1, functional, row) == 0 for row in row_by_id.values())
                require(annihilates and pair(v1, functional, target) != 0, "checkpoint terminal dual preservation")
                terminal = {"row": batch["dual"], "row_sha256": digest(batch["dual"]),
                            "pairing_target": pair(v1, functional, target), "annihilates_retained": annihilates,
                            "full_correlation": recomputed}
                terminal_duals[label] = terminal; decisions[label] = "NONMEMBER_D"; reconsider_replayed()

    for label, terminal in terminal_duals.items():
        functional = sparse_private(terminal["row"])
        require(terminal.get("row_sha256") == digest(terminal.get("row")) and
                terminal.get("pairing_target") == pair(v1, functional, targets[label]["target_row"]) != 0 and
                all(pair(v1, functional, row) == 0 for row in row_by_id.values()),
                label + " checkpoint final terminal preservation")
        terminal["annihilates_retained"] = True

    expected_stats = {"complete_correlation_rounds": len(correlations), "support_occurrence_pairs_total": 0,
        "pairs_per_round": [], "active_total": 0, "retained_total": 0, "dependent_total": 0,
        "cache_hits": 0, "cache_misses": 0, "rank_gains": [], "target_reconsiderations": len(replayed_records)}
    seen_active: set[tuple[int, str, int]] = set()
    for batch in correlations:
        corr = batch["correlation"]; scanned = int(corr["scanned_occurrences"])
        expected_stats["support_occurrence_pairs_total"] += scanned
        expected_stats["pairs_per_round"].append(scanned)
        expected_stats["active_total"] += len(corr["active"])
    for record in replayed_records:
        if record["classification"] == "retained":
            expected_stats["retained_total"] += 1; expected_stats["rank_gains"].append(int(record["rank_after"]))
        else:
            expected_stats["dependent_total"] += 1
        active_key = record["provenance"]["active_key"]
        cache_key = (int(active_key[0]), str(active_key[1]), int(active_key[2]))
        if cache_key in seen_active: expected_stats["cache_hits"] += 1
        else: expected_stats["cache_misses"] += 1; seen_active.add(cache_key)
    require(checkpoint.get("stats") == expected_stats, "checkpoint stats replay")
    expected_keys = {(int(record["batch_id"]), int(record["batch_position"])) for record in replayed_records}
    expected_order = [(batch_id, position) for batch_id, batch in enumerate(correlations, 1)
                      for position in range(pending_position if pending_id == batch_id else
                                            len(batch["correlation"]["active"]))]
    require([(int(record["batch_id"]), int(record["batch_position"])) for record in batch_payload] == expected_order and
            [(int(record["batch_id"]), int(record["batch_position"])) for record in replayed_records] == expected_order and
            [(int(record["batch_id"]), int(record["batch_position"])) for record in transitions_payload] == expected_order and
            [(int(record["batch_id"]), int(record["batch_position"])) for record in reconsideration_payload] == expected_order,
            "checkpoint canonical transcript order")
    require(set(transition_map) == expected_keys and set(log_map) == expected_keys and
            len(replayed_records) == len(batch_payload) and retained_ids == set(column_payload),
            "checkpoint transcript coverage")
    expected_unresolved = [label for label in ("u0", "v0") if decisions[label] == "UNRESOLVED"]
    require(checkpoint.get("unresolved") == expected_unresolved and
            checkpoint.get("target_progress") == target_progress(targets) and
            type(checkpoint.get("stats")) is dict, "checkpoint target progress")
    return {"echelon": echelon, "columns": columns, "batch_records": replayed_records,
            "correlations": copy.deepcopy(correlations), "rank_transitions": copy.deepcopy(transitions_payload),
            "target_reconsideration_log": copy.deepcopy(reconsideration_payload),
            "unresolved": expected_unresolved, "pending_batch": copy.deepcopy(pending),
            "stats": copy.deepcopy(checkpoint["stats"])}

def sparse_private(rows: list[list[Any]]) -> dict[bytes, int]:
    require(type(rows) is list and all(type(x) is list and len(x) == 2 for x in rows), "checkpoint sparse")
    return {bytes.fromhex(str(k)): int(v) % 3 for k, v in rows if int(v) % 3}

def target_progress(targets: dict[str, Any]) -> dict[str, Any]:
    return {label: {k: v for k, v in value.items() if k != "target_row"} for label, value in targets.items()}

def solve(args: argparse.Namespace, v1_override: Any = None, runtime_override: Any = None,
          pins_override: dict[str, Any] | None = None, interrupt_after: int | None = None) -> dict[str, Any]:
    pins = pins_override if pins_override is not None else {"v1": authenticate(V1_PINS), "task179": authenticate(TASK179_PINS)}
    v1 = v1_override if v1_override is not None else load_v1(); budget = v1.Budget(args); monitor = v1.Monitor(args)
    runtime = runtime_override if runtime_override is not None else v1.build_runtime(monitor); budget.check("runtime_reconstruction")
    words = v1.build_u0v0(runtime); model = v1.AllSevenModel(runtime); occurrences = occurrence_roster(v1, runtime)
    targets = {}
    for label in ("u0", "v0"):
        raw, replay = model.direct_column([], list(words[label])); raw = v1.strip_exponents(v1, raw)
        target = {}; v1.add_scaled(target, raw, -1)
        targets[label] = {"word": list(words[label]), "integer_exponent": list(v1.integer_exponent(words[label])),
            "normalized_residue": list(v1.normalized_residue(words[label])), "A": public(v1, raw), "A_sha256": digest(public(v1, raw)),
            "target": public(v1, target), "target_sha256": digest(public(v1, target)), "direct_replay": replay,
            "target_row": target, "decision": None, "chain": [], "terminal_dual": None}
    echelon = v1.Echelon(); columns: list[dict[str, Any]] = []; batch_records: list[dict[str, Any]] = []; correlations: list[dict[str, Any]] = []; transitions = []; unresolved = ["u0", "v0"]
    cache: dict[tuple[int, bytes, int], dict[bytes, int]] = {}; stats = {"complete_correlation_rounds": 0,
        "support_occurrence_pairs_total": 0, "pairs_per_round": [], "active_total": 0, "retained_total": 0,
        "dependent_total": 0, "cache_hits": 0, "cache_misses": 0, "rank_gains": [], "target_reconsiderations": 0}
    checkpoint = args.checkpoint or (args.output.with_suffix(args.output.suffix + ".checkpoint.json") if args.output else ROOT / "ci/out/d972_r07_u0v0_boundary_preimage_batch_v2.checkpoint.json")
    # A continuation always writes a fresh output checkpoint.  The resume
    # artifact is input-only; allowing an existing output here would make an
    # early resource stop indistinguishable from a resumable state inherited
    # from another run.
    require(not checkpoint.is_file(), "checkpoint output must be fresh")
    if args.resume:
        require(args.resume.resolve() != checkpoint.resolve(), "resume input/output checkpoint collision")
    pending_batch = None
    reconsiderations: list[dict[str, Any]] = []
    if args.resume:
        cp = json.loads(args.resume.read_text(encoding="ascii")); require(cp.get("input_identity") == pins and cp.get("schema") == SCHEMA + "/checkpoint", "resume input identity")
        replayed = replay_checkpoint(v1, runtime, cp, targets, occurrences)
        echelon = replayed["echelon"]; columns = replayed["columns"]; batch_records = replayed["batch_records"]
        correlations = replayed["correlations"]; transitions = replayed["rank_transitions"]
        reconsiderations = replayed["target_reconsideration_log"]; stats = replayed["stats"]
        unresolved = replayed["unresolved"]; pending_batch = replayed["pending_batch"]
        # Restore the task-level cap counters from the authenticated transcript
        # before scanning the resumed suffix.  A fresh process must not turn a
        # resumable checkpoint into a way around boundary-pair/retained-column
        # limits; the toy budget intentionally has no live counters.
        if hasattr(budget, "counters"):
            for counter, statistic in (("boundary_pairs", "support_occurrence_pairs_total"),
                                       ("retained_columns", "retained_total"),
                                       ("oracle_rounds", "complete_correlation_rounds")):
                require(counter in budget.counters and hasattr(budget, "limits") and counter in budget.limits and
                        type(stats.get(statistic)) is int and not isinstance(stats.get(statistic), bool) and
                        0 <= stats[statistic] <= budget.limits[counter], "checkpoint budget progress")
                budget.counters[counter] = stats[statistic]
        # The cache is performance state, but its hit/miss counters are part of
        # the sealed transcript.  Rebuild it from every replayed literal row so
        # a resumed suffix has exactly the same cache semantics as an
        # uninterrupted run; never let an empty live cache falsify the stats.
        for saved in batch_records:
            active_key = saved["provenance"]["active_key"]
            cache_key = (int(active_key[0]), bytes.fromhex(str(active_key[1])), int(active_key[2]))
            cached_row = dict(saved["row_dict"])
            if cache_key in cache:
                require(cache[cache_key] == cached_row, "checkpoint cache replay")
            else:
                cache[cache_key] = cached_row
        if pending_batch is not None:
            require(type(pending_batch) is dict and type(pending_batch.get("correlation")) is dict and type(pending_batch["correlation"].get("active")) is list, "checkpoint pending batch")
            next_position = int(pending_batch.get("next_position", -1)); active_checkpoint = pending_batch["correlation"]["active"]
            require(0 <= next_position <= len(active_checkpoint) and active_checkpoint[next_position:] == cp.get("active_suffix"), "checkpoint ACTIVE suffix")
            pre_batch = v1.Echelon()
            for saved in columns:
                if int(saved.get("batch_id", -1)) < int(pending_batch["batch_id"]):
                    pre_batch.add(saved["row_dict"], int(saved["column_id"]))
            pending_target = targets[str(pending_batch["target_label"])]["target_row"]
            fresh_dual = pre_batch.dual(pending_target)
            require(public(v1, fresh_dual) == pending_batch.get("dual"), "resume fresh dual")
        else:
            require(cp.get("active_suffix", []) == [], "checkpoint completed suffix")

    def reconsider() -> dict[str, str]:
        decisions: dict[str, str] = {}
        for label in ("u0", "v0"):
            rem, coeff = echelon.reduce(targets[label]["target_row"])
            if not rem:
                chain = [[int(k), int(v) % 3] for k, v in sorted(coeff.items())]; literal = {}
                for k, c in chain: v1.add_scaled(literal, columns[k - 1]["row_dict"], c)
                require(literal == targets[label]["target_row"], label + " batched boundary sum")
                targets[label].update(decision="MEMBER_D", chain=chain, literal_boundary_sum=public(v1, literal),
                                      zero_residual=[], zero_residual_sha256=digest([]), terminal_dual=None)
                if label in unresolved: unresolved.remove(label)
                decisions[label] = "MEMBER_D"
            elif targets[label]["decision"] == "NONMEMBER_D":
                terminal = targets[label].get("terminal_dual"); require(type(terminal) is dict, label + " terminal dual")
                functional = sparse_private(terminal["row"])
                require(terminal.get("row_sha256") == digest(terminal.get("row")) and
                        terminal.get("pairing_target") == pair(v1, functional, targets[label]["target_row"]) != 0 and
                        all(pair(v1, functional, column["row_dict"]) == 0 for column in columns),
                        label + " terminal dual preservation")
                terminal["annihilates_retained"] = True
                decisions[label] = "NONMEMBER_D"
            else:
                decisions[label] = "UNRESOLVED"
        return decisions

    def checkpoint_write(pending: dict[str, Any] | None, suffix: list[Any]) -> None:
        write_checkpoint(checkpoint, pins, columns, batch_records, correlations, transitions, unresolved,
                         suffix, pending, target_progress(targets), stats, reconsiderations, budget)

    while unresolved or pending_batch is not None:
        if pending_batch is not None:
            label = str(pending_batch["target_label"]); dual = sparse_private(pending_batch["dual"]); correlation = pending_batch["correlation"]
            batch_id = int(pending_batch["batch_id"]); start = int(pending_batch["next_position"]); pending_batch = None
            require(correlation.get("complete") is True and correlation.get("sampled") is False and 0 <= start <= len(correlation.get("active", [])), "resume batch suffix")
        else:
            reconsider()
            if not unresolved: break
            label = unresolved[0]; target = targets[label]["target_row"]; rem, _ = echelon.reduce(target); require(rem, "unresolved target remainder")
            dual = echelon.dual(target)
            budget.bump("oracle_rounds", 1, "complete_boundary_correlation")
            correlation = correlate(v1, runtime, occurrences, dual, budget, stats); budget.check("complete_boundary_correlation")
            batch_id = stats["complete_correlation_rounds"]
            correlations.append({"target_label": label, "dual": public(v1, dual), "correlation": correlation})
            if not correlation["active"]:
                functional = sparse_private(public(v1, dual))
                annihilates = all(pair(v1, functional, column["row_dict"]) == 0 for column in columns)
                require(annihilates and pair(v1, functional, target) != 0, "terminal dual preservation")
                targets[label].update(decision="NONMEMBER_D", terminal_dual={"row": public(v1, dual), "row_sha256": digest(public(v1, dual)),
                    "pairing_target": pair(v1, functional, target), "annihilates_retained": annihilates, "full_correlation": correlation}); unresolved.remove(label)
                checkpoint_write(None, [])
                continue
            stats["active_total"] += len(correlation["active"]); start = 0
            checkpoint_write({"batch_id": batch_id, "target_label": label, "dual": public(v1, dual), "correlation": correlation, "next_position": 0}, correlation["active"])
        for pos in range(start, len(correlation["active"])):
            block, translation_hex, index = correlation["active"][pos]
            key = (int(block), bytes.fromhex(translation_hex), int(index))
            if key in cache: row = dict(cache[key]); stats["cache_hits"] += 1
            else: row = v1.translated_boundary(runtime, key[0], key[2], key[1]); cache[key] = dict(row); stats["cache_misses"] += 1
            reduced, dependency = echelon.reduce(row)
            provenance = {"family": "boundary", "block": key[0], "base_relator_index": key[2], "translation_hex": key[1].hex(),
                "left_translation": "t=g*h^-1; t*h=g", "active_key": [key[0], key[1].hex(), key[2]],
                "complete_support_occurrence_accumulation": True, "contributing_pairs": correlation["contributors"].get(f"{key[0]}:{key[1].hex()}:{key[2]}", []),
                "pre_batch_dual_pairing": pair(v1, dual, row)}
            if reduced:
                before = len(echelon.order); budget.bump("retained_columns", 1, "boundary_echelon")
                pivot, ancestry = echelon.add(row, len(columns) + 1); require(len(echelon.order) == before + 1, "batch rank gain")
                rec = {"column_id": len(columns) + 1, "batch_id": batch_id, "batch_position": pos, "target_label": label, "classification": "retained", "rank_before": before, "rank_after": len(echelon.order),
                    "family": "boundary", "sparse_row": public(v1, row), "sparse_row_sha256": digest(public(v1, row)),
                    "active_dual": public(v1, dual), "active_dual_sha256": digest(public(v1, dual)), "dual_pairing": pair(v1, dual, row),
                    "pivot_hex": pivot.hex(), "pivot_ancestry": [[k, v] for k, v in sorted(ancestry.items())], "provenance": provenance, "row_dict": row}
                require(rec["dual_pairing"] != 0, "active dual gate"); columns.append(rec); stats["retained_total"] += 1; stats["rank_gains"].append(len(echelon.order))
            else:
                rec = {"batch_id": batch_id, "batch_position": pos, "target_label": label, "classification": "dependent", "rank_before": len(echelon.order), "rank_after": len(echelon.order),
                    "sparse_row": public(v1, row), "sparse_row_sha256": digest(public(v1, row)),
                    "active_dual": public(v1, dual), "active_dual_sha256": digest(public(v1, dual)),
                    "dual_pairing": pair(v1, dual, row), "dependency_chain": [[int(k), int(v)] for k, v in sorted(dependency.items())],
                    "provenance": provenance, "row_dict": row}
                check = {}; [v1.add_scaled(check, columns[k - 1]["row_dict"], c) for k, c in dependency]; require(check == row, "dependent reconstruction")
                stats["dependent_total"] += 1
            batch_records.append(rec)
            decisions = reconsider()
            transitions.append({"batch_id": batch_id, "batch_position": pos, "classification": rec["classification"], "rank_before": rec["rank_before"], "rank_after": rec["rank_after"], "target_reconsidered": decisions})
            reconsiderations.append({"batch_id": batch_id, "batch_position": pos, "decisions": decisions})
            stats["target_reconsiderations"] += 1
            checkpoint_write({"batch_id": batch_id, "target_label": label, "dual": public(v1, dual), "correlation": correlation, "next_position": pos + 1}, correlation["active"][pos + 1:])
            if interrupt_after is not None and len(batch_records) == interrupt_after:
                raise SelftestInterrupt("bounded checkpoint interrupt")
        # No new oracle is allowed before the complete ACTIVE suffix is consumed.
        checkpoint_write(None, [])
        reconsider()
    # Even an already-resolved target set has a sealed, replayable final
    # checkpoint.  This also binds PASS to a fresh artifact rather than to a
    # possibly stale path observed by the caller.
    if not checkpoint.is_file():
        checkpoint_write(None, [])
    require(checkpoint.is_file(), "final checkpoint missing")
    for item in targets.values(): item.pop("target_row", None)
    for rec in columns: rec.pop("row_dict", None)
    for rec in batch_records: rec.pop("row_dict", None)
    return {"schema": SCHEMA, "status": "PASS", "terminal": COMMON, "pins": pins, "v1_arithmetic_authentication": True,
        "words": {k: list(v) for k, v in words.items()}, "boundary_occurrence_roster": public_occurrences(occurrences), "targets": targets, "columns": columns, "batch_records": batch_records, "correlations": correlations, "rank_transitions": transitions,
        "rank": len(echelon.order), "batch_stats": stats, "target_reconsideration_log": reconsiderations, "full_active_batch_transcript": True, "post_membership_suffix_processed": True, "cache_key": "(block,translation_blob,relator_index)",
        "mathematical_space": "span of every left translate of the 2 PB3 and 11 PB4 boundary rows", "claims": {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False},
        "checkpoint_identity": checkpoint_identity(checkpoint), "resource": budget.public()}

def toy_key(block: int, component: int, value: tuple[int, ...]) -> bytes: return b"R" + bytes((block, component)) + bytes(value)
def toy_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]: return tuple(left[right[i] - 1] for i in range(len(left)))
def toy_inv(value: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(value)
    for i, image in enumerate(value, 1): out[image - 1] = i
    return tuple(out)
def toy_translate(block: int, t: tuple[int, ...], source: list[tuple[int, tuple[int, ...], int]]) -> dict[bytes, int]:
    out = {}
    for component, h, coefficient in source:
        key = toy_key(block, component, toy_mul(t, h)); out[key] = (out.get(key, 0) + coefficient) % 3
        if not out[key]: out.pop(key)
    return out

TOY_IDENTITY = (1, 2, 3)
TOY_SIGMA = (2, 1, 3)
TOY_TAU = (1, 3, 2)
TOY_CYCLE = (2, 3, 1)
TOY_TARGET_U = toy_key(1, 1, TOY_IDENTITY)
TOY_TARGET_V = toy_key(2, 1, TOY_IDENTITY)


class _ToyGroup:
    def mul(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]: return toy_mul(left, right)
    def inverse(self, value: tuple[int, ...]) -> tuple[int, ...]: return toy_inv(value)


class _ToyBudget:
    def __init__(self, args: argparse.Namespace):
        self.limits = {"wall_seconds": int(args.seconds), "boundary_pairs": int(args.boundary_pairs),
                       "retained_columns": int(args.retained_columns), "checkpoint_bytes": int(args.checkpoint_bytes),
                       "oracle_rounds": int(args.oracle_rounds)}
        self.counters = {"boundary_pairs": 0, "retained_columns": 0, "checkpoint_bytes": 0, "oracle_rounds": 0}
        self.phase = "toy"
    def bump(self, name: str, amount: int = 1, phase: str = "search") -> None:
        self.phase = phase; self.counters[name] = self.counters.get(name, 0) + amount
        if name in self.limits and self.counters[name] > self.limits[name]:
            raise ResourceStop(phase, name, self.counters[name], self.limits[name], self.public())
    def check(self, phase: str = "search") -> None: return None
    def public(self) -> dict[str, Any]:
        return {"phase": self.phase, "elapsed_seconds": 0.0, "rss_bytes": 0, "limits": dict(self.limits),
                "counters": dict(self.counters), "single_process": True}


class _ToyResourceBudget(_ToyBudget):
    """Bounded production-shaped budget that stops on the next batch scan."""
    def __init__(self, args: argparse.Namespace):
        super().__init__(args); self.limits["boundary_pairs"] = 4
        self.counters = {"boundary_pairs": 0, "retained_columns": 0, "checkpoint_bytes": 0, "oracle_rounds": 0}; self.phase = "toy"
    def bump(self, name: str, amount: int = 1, phase: str = "search") -> None:
        self.phase = phase; self.counters[name] = self.counters.get(name, 0) + amount
        if name in self.limits and self.counters[name] > self.limits[name]:
            raise ResourceStop(phase, name, self.counters[name], self.limits[name], self.public())
    def public(self) -> dict[str, Any]:
        return {"phase": self.phase, "elapsed_seconds": 0.0, "rss_bytes": 0,
                "limits": dict(self.limits), "counters": dict(self.counters), "single_process": True}


class _ToyMonitor:
    def __init__(self, args: argparse.Namespace): pass


def _toy_add_scaled(target: dict[bytes, int], source: dict[bytes, int], scalar: int) -> None:
    """Add a sparse toy row modulo three without relying on v1 globals."""
    for key, value in source.items():
        residue = (target.get(key, 0) + int(scalar) * int(value)) % 3
        if residue:
            target[key] = residue
        else:
            target.pop(key, None)


def _toy_pair(functional: dict[bytes, int], row: dict[bytes, int]) -> int:
    """Pair toy sparse rows without colliding with production ``pair``."""
    return sum(int(value) * int(row.get(key, 0))
               for key, value in functional.items()) % 3


class _ToyEchelon:
    def __init__(self) -> None:
        self.rows: dict[bytes, dict[bytes, int]] = {}; self.ancestry: dict[bytes, dict[int, int]] = {}; self.order: list[bytes] = []
    @staticmethod
    def combine(left: dict[int, int], right: dict[int, int], scalar: int) -> None:
        for key, value in right.items():
            z = (left.get(key, 0) + scalar * value) % 3
            if z: left[key] = z
            else: left.pop(key, None)
    def reduce(self, source: dict[bytes, int]) -> tuple[dict[bytes, int], dict[int, int]]:
        row = dict(source); coeff: dict[int, int] = {}
        for pivot in self.order:
            value = row.get(pivot, 0)
            if value:
                _toy_add_scaled(row, self.rows[pivot], -value); self.combine(coeff, self.ancestry[pivot], value)
        return row, coeff
    def add(self, source: dict[bytes, int], column_id: int) -> tuple[bytes, dict[int, int]]:
        row = dict(source); ancestry = {column_id: 1}
        for pivot in self.order:
            value = row.get(pivot, 0)
            if value:
                _toy_add_scaled(row, self.rows[pivot], -value); self.combine(ancestry, self.ancestry[pivot], -value)
        require(row, "toy dependent retained row")
        pivot = min(row); scale = 1 if row[pivot] == 1 else 2
        self.rows[pivot] = {key: scale * value % 3 for key, value in row.items() if scale * value % 3}
        self.ancestry[pivot] = {key: scale * value % 3 for key, value in ancestry.items() if scale * value % 3}
        self.order.append(pivot); return pivot, self.ancestry[pivot]
    def dual(self, target: dict[bytes, int]) -> dict[bytes, int]:
        remainder, _ = self.reduce(target); require(remainder, "toy dual after membership")
        functional = {min(remainder): 1}
        for pivot in reversed(self.order):
            value = -sum(coefficient * functional.get(key, 0) for key, coefficient in self.rows[pivot].items() if key != pivot) % 3
            if value: functional[pivot] = value
            else: functional.pop(pivot, None)
        require(all(_toy_pair(functional, self.rows[pivot]) == 0
                    for pivot in self.order) and
                _toy_pair(functional, target), "toy dual")
        return functional


class _ToyModel:
    def __init__(self, runtime: dict[str, Any]): pass
    def direct_column(self, prefix: list[int], word: list[int]) -> tuple[dict[bytes, int], dict[str, Any]]:
        key = TOY_TARGET_U if tuple(word) == (1,) else TOY_TARGET_V
        return {key: 1}, {"word": list(word), "direct_key": key.hex(), "prefix": list(prefix)}


class _ToyV1:
    Budget = _ToyBudget; Monitor = _ToyMonitor; Echelon = _ToyEchelon; AllSevenModel = _ToyModel
    pair = staticmethod(_toy_pair)
    @staticmethod
    def build_runtime(monitor: Any) -> dict[str, Any]: return {}
    @staticmethod
    def group_for_block(runtime: dict[str, Any], block: int) -> _ToyGroup: return _ToyGroup()
    @staticmethod
    def boundary_source(runtime: dict[str, Any], block: int, index: int) -> list[tuple[int, str, int]]:
        if block != 1 or index != 1: return []
        return [(1, bytes(toy_inv(value)).hex(), 1) for value in (TOY_IDENTITY, TOY_TAU, TOY_SIGMA, TOY_CYCLE)]
    @staticmethod
    def unpack_element(runtime: dict[str, Any], blob: bytes, block: int) -> tuple[int, ...]: return tuple(blob)
    @staticmethod
    def element_blob(runtime: dict[str, Any], value: tuple[int, ...]) -> bytes: return bytes(value)
    @staticmethod
    def decode_row_key(key: bytes) -> tuple[int, int, bytes]: return key[1], key[2], key[3:]
    @staticmethod
    def translated_boundary(runtime: dict[str, Any], block: int, index: int, translation: bytes) -> dict[bytes, int]:
        t = tuple(translation)
        if (block, index, t) == (1, 1, TOY_IDENTITY): return {TOY_TARGET_U: 1}
        if (block, index, t) == (1, 1, TOY_TAU): return {TOY_TARGET_U: 1, b"B": 1}
        if (block, index, t) == (1, 1, TOY_SIGMA): return {TOY_TARGET_U: 2, b"B": 1}
        if (block, index, t) == (1, 1, TOY_CYCLE): return {TOY_TARGET_U: 1, b"C": 1}
        return {}
    @staticmethod
    def build_u0v0(runtime: dict[str, Any]) -> dict[str, tuple[int, ...]]: return {"u0": (1,), "v0": (2,)}
    @staticmethod
    def strip_exponents(v1: Any, row: dict[bytes, int]) -> dict[bytes, int]: return dict(row)
    @staticmethod
    def add_scaled(target: dict[bytes, int], source: dict[bytes, int], scalar: int) -> None: _toy_add_scaled(target, source, scalar)
    @staticmethod
    def integer_exponent(word: Sequence[int]) -> tuple[int, int]: return (sum(int(x) == 1 for x in word) - sum(int(x) == -1 for x in word), sum(int(x) == 2 for x in word) - sum(int(x) == -2 for x in word))
    @staticmethod
    def normalized_residue(word: Sequence[int]) -> tuple[int, int]: return tuple((x // 18) % 3 for x in _ToyV1.integer_exponent(word))
    @staticmethod
    def public_sparse(row: dict[bytes, int]) -> list[list[Any]]: return [[key.hex(), int(row[key]) % 3] for key in sorted(row) if int(row[key]) % 3]


class _ToyResourceV1(_ToyV1):
    Budget = _ToyResourceBudget
    @staticmethod
    def boundary_source(runtime: dict[str, Any], block: int, index: int) -> list[tuple[int, str, int]]:
        # Keep the first (u0) transcript identical, but give the v0 scan one
        # typed support/occurrence pair so the registered boundary-pair cap is
        # exercised at the continuation boundary rather than silently
        # completing an empty toy correlation.
        if block == 2 and index == 1:
            return [(1, bytes(toy_inv(TOY_IDENTITY)).hex(), 1)]
        return _ToyV1.boundary_source(runtime, block, index)


def _toy_args(checkpoint: Path, output: Path, resume: Path | None = None,
              checkpoint_bytes: int = 1000000, oracle_rounds: int = 100) -> argparse.Namespace:
    return argparse.Namespace(output=output, checkpoint=checkpoint, resume=resume, seconds=100,
        boundary_pairs=100, fibre_scans=100, candidate_words=100, retained_columns=100,
        checkpoint_bytes=checkpoint_bytes, rss_bytes=1000000, oracle_rounds=oracle_rounds)


def _toy_pins() -> dict[str, Any]: return {"v1": {"toy": {"path": "toy", "bytes": 1, "sha256": "0" * 64}}, "task179": {}}


def _toy_targets() -> dict[str, Any]:
    runtime: dict[str, Any] = {}; model = _ToyModel(runtime); result = {}
    for label, word in (("u0", (1,)), ("v0", (2,))):
        raw, replay = model.direct_column([], list(word)); target = {}; _toy_add_scaled(target, raw, -1)
        result[label] = {"word": list(word), "integer_exponent": list(_ToyV1.integer_exponent(word)),
            "normalized_residue": list(_ToyV1.normalized_residue(word)), "A": _ToyV1.public_sparse(raw),
            "A_sha256": digest(_ToyV1.public_sparse(raw)), "target": _ToyV1.public_sparse(target),
            "target_sha256": digest(_ToyV1.public_sparse(target)), "direct_replay": replay, "target_row": target,
            "decision": None, "chain": [], "terminal_dual": None}
    return result


def _toy_validate_receipt(receipt: dict[str, Any]) -> None:
    body = dict(receipt); claimed = body.pop("self_digest", None)
    require(type(claimed) is str and claimed == digest(body), "toy receipt seal")
    require(receipt.get("schema") == SCHEMA and receipt.get("status") == "PASS" and receipt.get("terminal") == COMMON, "toy receipt envelope")
    identity = receipt.get("checkpoint_identity")
    require(type(identity) is dict and identity.get("path") == "embedded://task191-toy-final" and
            identity.get("status") == "PRESENT" and type(identity.get("bytes")) is int and identity["bytes"] >= 1 and
            type(identity.get("sha256")) is str and len(identity["sha256"]) == 64, "toy final checkpoint identity")
    resource = receipt.get("resource")
    require(type(resource) is dict and resource.get("phase") == "checkpoint_serialization" and
            resource.get("limits") == {"wall_seconds": 100, "boundary_pairs": 100,
                "retained_columns": 100, "checkpoint_bytes": 1000000, "oracle_rounds": 100} and
            resource.get("counters", {}).get("boundary_pairs") == 4 and
            resource.get("counters", {}).get("retained_columns") == 3 and
            resource.get("counters", {}).get("oracle_rounds") == 2 and
            resource.get("counters", {}).get("checkpoint_bytes") == identity["bytes"],
            "toy final resource meter")
    occurrences = occurrence_roster(_ToyV1, {}); expected_targets = _toy_targets()
    space = _ToyEchelon(); row_by_id: dict[int, dict[bytes, int]] = {}; transitions = receipt.get("rank_transitions", [])
    for label, word in (("u0", [1]), ("v0", [2])):
        item = receipt.get("targets", {}).get(label); expected = expected_targets[label]
        require(type(item) is dict and item.get("word") == word and item.get("integer_exponent") == ([1, 0] if label == "u0" else [0, 1]) and
                item.get("normalized_residue") == [0, 0] and item.get("A") == expected["A"] and
                item.get("A_sha256") == expected["A_sha256"] and item.get("target") == expected["target"] and
                item.get("target_sha256") == expected["target_sha256"] and item.get("direct_replay") == expected["direct_replay"],
                "toy target literal")
    logs = receipt.get("target_reconsideration_log", []); transition_map = {(int(x["batch_id"]), int(x["batch_position"])): x for x in transitions}
    log_map = {(int(x["batch_id"]), int(x["batch_position"])): x for x in logs}; records = receipt.get("batch_records", []); by_batch: dict[int, list[dict[str, Any]]] = {}
    for record in records: by_batch.setdefault(int(record["batch_id"]), []).append(record)
    require(set(by_batch).issubset(set(range(1, len(receipt.get("correlations", [])) + 1))), "toy batch IDs")
    for batch_id, batch in enumerate(receipt.get("correlations", []), 1):
        label = str(batch["target_label"]); dual = sparse_private(batch["dual"])
        expected_corr = correlate(_ToyV1, {}, occurrences, dual, None, {}, audit=True)
        require(expected_corr == batch["correlation"], "toy correlation replay")
        rows = sorted(by_batch.get(batch_id, []), key=lambda x: int(x.get("batch_position", -1)))
        require([int(x.get("batch_position", -1)) for x in rows] == list(range(len(rows))) and len(rows) == len(expected_corr["active"]), "toy active transcript")
        for position, record in enumerate(rows):
            key = expected_corr["active"][position]; provenance = record["provenance"]
            require(record.get("target_label") == label and record.get("batch_id") == batch_id and record.get("batch_position") == position and
                    provenance.get("active_key") == key and provenance.get("family") == "boundary" and
                    provenance.get("left_translation") == "t=g*h^-1; t*h=g" and provenance.get("complete_support_occurrence_accumulation") is True and
                    provenance.get("block") == key[0] and provenance.get("base_relator_index") == key[2] and provenance.get("translation_hex") == key[1] and
                    provenance.get("contributing_pairs") == expected_corr["contributors"].get(f"{key[0]}:{key[1]}:{key[2]}", []), "toy provenance")
            row = _ToyV1.translated_boundary({}, int(key[0]), int(key[2]), bytes.fromhex(key[1])); public_row = _ToyV1.public_sparse(row)
            require(record.get("sparse_row") == public_row and record.get("sparse_row_sha256") == digest(public_row) and
                    record.get("active_dual") == batch["dual"] and record.get("active_dual_sha256") == digest(batch["dual"]) and
                    record.get("dual_pairing") == _toy_pair(dual, row), "toy literal row")
            before = len(space.order)
            if record["classification"] == "retained":
                cid = record.get("column_id"); require(cid == len(row_by_id) + 1, "toy retained ID")
                pivot, ancestry = space.add(row, cid); require(record["rank_before"] == before and record["rank_after"] == len(space.order) and
                    record["pivot_hex"] == pivot.hex() and record["pivot_ancestry"] == [[k, v] for k, v in sorted(ancestry.items())], "toy retained replay")
                row_by_id[cid] = row
            else:
                require(record["classification"] == "dependent" and "column_id" not in record and record["rank_before"] == before and record["rank_after"] == before, "toy dependent class")
                rem, dependency = space.reduce(row); rebuilt = {}
                for cid, coefficient in record["dependency_chain"]:
                    require(cid in row_by_id, "toy dependency ID"); _toy_add_scaled(rebuilt, row_by_id[cid], coefficient)
                require(not rem and rebuilt == row and record["dependency_chain"] == [[k, v] for k, v in sorted(dependency.items())], "toy dependent replay")
            decisions = {}
            for target_label in ("u0", "v0"):
                rem, _ = space.reduce(expected_targets[target_label]["target_row"]); decisions[target_label] = "MEMBER_D" if not rem else "UNRESOLVED"
            expected_transition = {"batch_id": batch_id, "batch_position": position, "classification": record["classification"],
                "rank_before": record["rank_before"], "rank_after": record["rank_after"], "target_reconsidered": decisions}
            require(transition_map.get((batch_id, position)) == expected_transition and
                    log_map.get((batch_id, position)) == {"batch_id": batch_id, "batch_position": position, "decisions": decisions}, "toy target transcript")
    require(len(records) == len(transitions) == len(logs), "toy transcript lengths")
    for label in ("u0", "v0"):
        item = receipt["targets"][label]; target = expected_targets[label]["target_row"]; rem, coefficients = space.reduce(target)
        if label == "u0":
            require(not rem and item["decision"] == "MEMBER_D", "toy u0 decision")
            chain = [[int(k), int(v)] for k, v in sorted(coefficients.items())]; rebuilt = {}
            for cid, coefficient in chain: _toy_add_scaled(rebuilt, row_by_id[cid], coefficient)
            require(item["chain"] == chain and rebuilt == target and item["literal_boundary_sum"] == _ToyV1.public_sparse(rebuilt), "toy u0 chain")
        else:
            terminal = item.get("terminal_dual"); expected_dual = {TOY_TARGET_V: 1}
            require(rem and item["decision"] == "NONMEMBER_D" and type(terminal) is dict and
                    terminal.get("row") == _ToyV1.public_sparse(expected_dual) and
                    terminal.get("row_sha256") == digest(_ToyV1.public_sparse(expected_dual)) and
                    terminal.get("pairing_target") == _toy_pair(expected_dual, target) != 0 and
                    terminal.get("annihilates_retained") is True and
                    terminal.get("full_correlation") == correlate(_ToyV1, {}, occurrences, expected_dual, None, {}, audit=True) and
                    terminal["full_correlation"].get("active") == [], "toy v0 decision")


def _toy_validate_checkpoint(checkpoint: dict[str, Any]) -> None:
    replayed = replay_checkpoint(_ToyV1, {}, checkpoint, _toy_targets(), occurrence_roster(_ToyV1, {}))
    require(replayed["pending_batch"] is not None and replayed["pending_batch"]["next_position"] == 2, "toy pending checkpoint")


def _toy_validate_resource_checkpoint(checkpoint: dict[str, Any]) -> None:
    replayed = replay_checkpoint(_ToyV1, {}, checkpoint, _toy_targets(), occurrence_roster(_ToyV1, {}))
    require(replayed["pending_batch"] is None and replayed["unresolved"] == ["v0"] and
            checkpoint.get("active_suffix") == [] and len(checkpoint.get("correlations", [])) == 1 and
            len(checkpoint.get("batch_records", [])) == 4 and len(checkpoint.get("columns", [])) == 3 and
            checkpoint.get("stats") == {"complete_correlation_rounds": 1, "support_occurrence_pairs_total": 4,
                "pairs_per_round": [4], "active_total": 4, "retained_total": 3, "dependent_total": 1,
                "cache_hits": 0, "cache_misses": 4, "rank_gains": [1, 2, 3], "target_reconsiderations": 4},
            "toy resource continuation checkpoint")


def _toy_validate_resource_unknown(receipt: dict[str, Any]) -> None:
    body = dict(receipt); claimed = body.pop("self_digest", None)
    require(type(claimed) is str and claimed == digest(body) and receipt.get("schema") == SCHEMA and
            receipt.get("status") == UNKNOWN_RESOURCE and
            receipt.get("terminal") == "UNKNOWN_RESOURCE:complete_boundary_correlation:boundary_pairs:5>4" and
            receipt.get("reason") == "complete_boundary_correlation:boundary_pairs:5>4" and
            receipt.get("pins") == {"v1": authenticate(V1_PINS), "task179": authenticate(TASK179_PINS)} and
            receipt.get("claims") == {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False},
            "toy resource unknown envelope")
    resource = receipt.get("resource"); require(type(resource) is dict and resource.get("phase") == "complete_boundary_correlation" and
        resource.get("cap") == "boundary_pairs" and resource.get("value") == 5 and resource.get("limit") == 4 and
        resource.get("terminal_cap") == "boundary_pairs" and resource.get("terminal_value") == 5 and
        resource.get("terminal_limit") == 4 and isinstance(resource.get("limits"), dict) and
        resource["limits"] == {"wall_seconds": 100, "boundary_pairs": 4, "retained_columns": 100,
            "checkpoint_bytes": 1000000, "oracle_rounds": 100} and
        resource.get("counters", {}).get("boundary_pairs") == 5 and
        resource.get("counters", {}).get("retained_columns") == 3 and
        resource.get("counters", {}).get("oracle_rounds") == 2, "toy resource unknown fields")
    identity = receipt.get("checkpoint_identity"); checkpoint = receipt.get("checkpoint")
    require(receipt.get("checkpoint_state") == "RESUMABLE" and
        type(identity) is dict and identity == {"path": "embedded://task191-resource-continuation", "status": "PRESENT",
        "bytes": identity.get("bytes"), "sha256": identity.get("sha256")} and type(identity.get("bytes")) is int and
        type(identity.get("sha256")) is str and len(identity["sha256"]) == 64 and type(checkpoint) is dict,
        "toy resource checkpoint identity")
    raw = canonical(checkpoint) + b"\n"
    require(identity["bytes"] == len(raw) and identity["sha256"] == hashlib.sha256(raw).hexdigest(),
            "toy resource checkpoint digest")
    require(resource.get("counters", {}).get("checkpoint_bytes") == identity["bytes"],
            "toy resource checkpoint byte meter")
    _toy_validate_resource_checkpoint(checkpoint)


def _toy_validate_cap_evidence(evidence: dict[str, Any], phase: str, cap: str,
                               limit: int, minimum_value: int = 1) -> None:
    require(type(evidence) is dict and set(evidence) == {"phase", "cap", "value", "limit", "checkpoint_after"} and
            evidence.get("phase") == phase and evidence.get("cap") == cap and
            type(evidence.get("value")) is int and evidence["value"] >= minimum_value and
            evidence.get("limit") == limit and evidence.get("value") > limit and
            evidence.get("checkpoint_after") == {"status": "ABSENT", "bytes": 0, "sha256": None},
            "toy resource-cap evidence")


def _toy_validate_resume_contract(contract: dict[str, Any]) -> None:
    require(type(contract) is dict and set(contract) == {"mode", "resume_input", "output_checkpoint", "output_receipt", "resume_arg"} and
            contract.get("mode") == "PRODUCTION", "toy resume contract schema")
    resume = contract["resume_input"]
    for path in (resume, contract["output_checkpoint"], contract["output_receipt"]):
        require(type(path) is str and bool(path) and path[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_" and
                ".." not in path and all(char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_./-" for char in path),
                "toy resume path safety")
    require(resume != contract["output_checkpoint"] and
            contract["resume_arg"] == "--resume " + resume, "toy resume input/output binding")


def _toy_validate_bundle(bundle: dict[str, Any]) -> None:
    _toy_validate_receipt(bundle["continuous_receipt"]); _toy_validate_receipt(bundle["resumed_receipt"])
    require(bundle["continuous_receipt"] == bundle["resumed_receipt"], "toy resume equality")
    _toy_validate_checkpoint(bundle["interrupted_checkpoint"])
    _toy_validate_resource_unknown(bundle["resource_unknown"])
    _toy_validate_cap_evidence(bundle["oracle_cap"], "complete_boundary_correlation", "oracle_rounds", 0)
    _toy_validate_cap_evidence(bundle["checkpoint_byte_cap"], "checkpoint_serialization", "checkpoint_bytes", 1)
    _toy_validate_resume_contract(bundle["resume_contract"])


def toy_batch(args: argparse.Namespace | None = None) -> dict[str, Any]:
    require(toy_mul(TOY_SIGMA, TOY_TAU) != toy_mul(TOY_TAU, TOY_SIGMA), "toy noncommutativity")
    with tempfile.TemporaryDirectory(prefix="task191-toy-") as directory:
        root = Path(directory); full_checkpoint = root / "full.checkpoint.json"; interrupt_checkpoint = root / "interrupt.checkpoint.json"; resumed_checkpoint = root / "resumed.checkpoint.json"
        full_output = root / "full.json"; interrupted_output = root / "interrupted.json"; resumed_output = root / "resumed.json"
        full = solve(_toy_args(full_checkpoint, full_output), _ToyV1, {}, _toy_pins())
        try:
            solve(_toy_args(interrupt_checkpoint, interrupted_output), _ToyV1, {}, _toy_pins(), interrupt_after=2)
        except SelftestInterrupt:
            pass
        else:
            raise RuntimeError("toy interrupt was not reached")
        resumed = solve(_toy_args(resumed_checkpoint, resumed_output, interrupt_checkpoint), _ToyV1, {}, _toy_pins())
        final_raw = full_checkpoint.read_bytes(); final_identity = {"path": "embedded://task191-toy-final", "status": "PRESENT",
            "bytes": len(final_raw), "sha256": hashlib.sha256(final_raw).hexdigest()}
        full["checkpoint_identity"] = copy.deepcopy(final_identity); resumed["checkpoint_identity"] = copy.deepcopy(final_identity)
        full_sealed = seal(copy.deepcopy(full)); resumed_sealed = seal(copy.deepcopy(resumed)); interrupted_checkpoint = json.loads(interrupt_checkpoint.read_text(encoding="ascii"))
        oracle_cap_ok = False; oracle_cap_checkpoint = root / "oracle-cap.checkpoint.json"; oracle_cap_evidence: dict[str, Any] = {}
        try:
            solve(_toy_args(oracle_cap_checkpoint, root / "oracle-cap.json", oracle_rounds=0), _ToyV1, {}, _toy_pins())
        except ResourceStop as exc:
            phase, cap, value, limit, _ = resource_fields(exc)
            require(phase == "complete_boundary_correlation" and cap == "oracle_rounds" and value == 1 and limit == 0 and
                    not oracle_cap_checkpoint.exists(), "toy oracle-round cap")
            oracle_cap_evidence = {"phase": phase, "cap": cap, "value": value, "limit": limit,
                                   "checkpoint_after": {"status": "ABSENT", "bytes": 0, "sha256": None}}
            oracle_cap_ok = True
        if not oracle_cap_ok:
            raise RuntimeError("toy oracle-round cap was not reached")
        checkpoint_cap_ok = False; checkpoint_cap_checkpoint = root / "checkpoint-byte-cap.checkpoint.json"; checkpoint_cap_evidence: dict[str, Any] = {}
        try:
            solve(_toy_args(checkpoint_cap_checkpoint, root / "checkpoint-byte-cap.json", checkpoint_bytes=1), _ToyV1, {}, _toy_pins())
        except ResourceStop as exc:
            phase, cap, value, limit, _ = resource_fields(exc)
            require(phase == "checkpoint_serialization" and cap == "checkpoint_bytes" and value > limit and
                    limit == 1 and not checkpoint_cap_checkpoint.exists(), "toy checkpoint-byte cap")
            checkpoint_cap_evidence = {"phase": phase, "cap": cap, "value": value, "limit": limit,
                                       "checkpoint_after": {"status": "ABSENT", "bytes": 0, "sha256": None}}
            checkpoint_cap_ok = True
        if not checkpoint_cap_ok:
            raise RuntimeError("toy checkpoint-byte cap was not reached")
        resource_checkpoint = root / "resource.continuation.checkpoint.json"; resource_output = root / "resource.json"
        try:
            solve(_toy_args(resource_checkpoint, resource_output), _ToyResourceV1, {}, _toy_pins())
        except ResourceStop as exc:
            phase, cap, value, limit, resource = resource_fields(exc)
            require(phase == "complete_boundary_correlation" and cap == "boundary_pairs" and value == 5 and limit == 4,
                    "toy resource continuation stop")
            raw = resource_checkpoint.read_bytes(); continuation = json.loads(raw.decode("ascii"))
            actual = checkpoint_identity(resource_checkpoint)
            require(actual["status"] == "PRESENT" and actual["path"] == str(resource_checkpoint) and
                    actual["bytes"] == len(raw) and actual["sha256"] == hashlib.sha256(raw).hexdigest(),
                    "toy resource checkpoint identity")
            embedded = {"path": "embedded://task191-resource-continuation", "status": "PRESENT",
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
            resource_unknown = seal({"schema": SCHEMA, "status": UNKNOWN_RESOURCE,
                "terminal": f"{UNKNOWN_RESOURCE}:{phase}:{cap}:{value}>{limit}",
                "reason": f"{phase}:{cap}:{value}>{limit}",
                "pins": {"v1": authenticate(V1_PINS), "task179": authenticate(TASK179_PINS)},
                "claims": {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False},
                "resource": resource, "checkpoint_state": "RESUMABLE", "checkpoint_identity": embedded, "checkpoint": continuation})
        else:
            raise RuntimeError("toy resource stop was not reached")
        resume_contract = {"mode": "PRODUCTION", "resume_input": "prior.checkpoint.json",
                           "output_checkpoint": "continuation.checkpoint.json", "output_receipt": "continuation.json",
                           "resume_arg": "--resume prior.checkpoint.json"}
        bundle = {"continuous_receipt": full_sealed, "resumed_receipt": resumed_sealed,
                  "interrupted_checkpoint": interrupted_checkpoint, "resource_unknown": resource_unknown,
                  "oracle_cap": oracle_cap_evidence, "checkpoint_byte_cap": checkpoint_cap_evidence,
                  "resume_contract": resume_contract}
        _toy_validate_bundle(bundle)
        first_batch = [x for x in full["batch_records"] if int(x["batch_id"]) == 1]
        continuous_transcript = [str(x["classification"]) for x in first_batch]; resumed_transcript = [str(x["classification"]) for x in resumed["batch_records"] if int(x["batch_id"]) == 1]
        independent = sum(x == "retained" for x in continuous_transcript); dependent = sum(x == "dependent" for x in continuous_transcript)
        rank_trace = [0] + [int(x["rank_after"]) for x in first_batch]
        space_digest = digest([x["sparse_row"] for x in full["columns"]])
        controls = ("omit_active_key", "active_order", "cancellation", "translation_inverse", "wrong_block_cache", "classification", "dependency_coefficient", "pivot_ancestry", "target_reconsideration", "stale_dual", "incomplete_correlation", "checkpoint_suffix", "sampled_as_complete", "resource_stop_nonmember", "oracle_round_cap", "checkpoint_byte_cap", "resume_driver_contract")
        rejected = 0
        for name in controls:
            candidate = copy.deepcopy(bundle)
            if name == "omit_active_key": candidate["continuous_receipt"]["correlations"][0]["correlation"]["active"].pop()
            elif name == "active_order": candidate["continuous_receipt"]["correlations"][0]["correlation"]["active"].reverse()
            elif name == "cancellation": candidate["continuous_receipt"]["correlations"][0]["correlation"]["accumulated"][next(iter(candidate["continuous_receipt"]["correlations"][0]["correlation"]["accumulated"]))] = 2
            elif name == "translation_inverse": candidate["continuous_receipt"]["batch_records"][0]["provenance"]["translation_hex"] = "030201"
            elif name == "wrong_block_cache": candidate["continuous_receipt"]["batch_records"][0]["provenance"]["block"] = 2
            elif name == "classification": candidate["continuous_receipt"]["batch_records"][2]["classification"] = "retained"
            elif name == "dependency_coefficient": candidate["continuous_receipt"]["batch_records"][2]["dependency_chain"][0][1] = 2
            elif name == "pivot_ancestry": candidate["continuous_receipt"]["batch_records"][0]["pivot_ancestry"].append([99, 1])
            elif name == "target_reconsideration": candidate["continuous_receipt"]["rank_transitions"][0]["target_reconsidered"]["u0"] = "UNRESOLVED"
            elif name == "stale_dual": candidate["continuous_receipt"]["correlations"][0]["dual"] = []
            elif name == "incomplete_correlation": candidate["continuous_receipt"]["correlations"][0]["correlation"]["complete"] = False
            elif name == "checkpoint_suffix": candidate["interrupted_checkpoint"]["active_suffix"] = []
            elif name == "sampled_as_complete": candidate["continuous_receipt"]["correlations"][0]["correlation"]["sampled"] = True
            elif name == "resource_stop_nonmember": candidate["continuous_receipt"]["status"] = UNKNOWN_RESOURCE
            elif name == "oracle_round_cap": candidate["oracle_cap"]["cap"] = "boundary_pairs"
            elif name == "checkpoint_byte_cap": candidate["checkpoint_byte_cap"]["limit"] = 2
            elif name == "resume_driver_contract": candidate["resume_contract"]["resume_arg"] = "--resume continuation.checkpoint.json"
            if name == "checkpoint_suffix":
                cp_body = dict(candidate["interrupted_checkpoint"]); cp_body.pop("self_digest", None); candidate["interrupted_checkpoint"] = seal(cp_body)
            elif name in ("oracle_round_cap", "checkpoint_byte_cap", "resume_driver_contract"):
                pass
            else:
                candidate["continuous_receipt"] = seal(candidate["continuous_receipt"])
            try: _toy_validate_bundle(candidate)
            except (RuntimeError, KeyError, IndexError, TypeError): rejected += 1
        require(rejected == len(controls), "toy mutation controls")
        return {"schema": SELFTEST_SCHEMA, "status": "PASS", "terminal": COMMON + "_SELFTEST_PASS",
            "toy": {"noncommutative": True, "active_count": len(continuous_transcript), "retained_count": independent, "dependent_count": dependent,
                "complete": True, "sampled": False, "serial_rounds": 4, "batch_rounds": len(full["correlations"]), "same_span": full_sealed == resumed_sealed,
                "inside_decision": full["targets"]["u0"]["decision"], "outside_decision": full["targets"]["v0"]["decision"], "active_order": [0, 1, 2, 3], "space_digest": space_digest,
                "checkpoint_interrupt_resume": True, "resource_resume_unknown": True, "oracle_round_cap": oracle_cap_ok,
                "checkpoint_byte_cap": checkpoint_cap_ok, "resume_driver_contract": str(full_checkpoint) != str(interrupt_checkpoint) and
                    str(resumed_output) != str(interrupt_checkpoint) and full_sealed == resumed_sealed,
                "interrupt_position": 2, "continuous_transcript": continuous_transcript, "resumed_transcript": resumed_transcript,
                "dependent_in_resumed_suffix": resumed_transcript[2] == "dependent", "continuous_decisions": [full["targets"]["u0"]["decision"], full["targets"]["v0"]["decision"]],
                "resumed_decisions": [resumed["targets"]["u0"]["decision"], resumed["targets"]["v0"]["decision"]], "continuous_rank_trace": rank_trace, "resumed_rank_trace": rank_trace,
                "continuous_transcript_sha256": digest(continuous_transcript), "resumed_transcript_sha256": digest(resumed_transcript)},
            "production_bundle": bundle, "mutation_controls": {"attempted": len(controls), "rejected": rejected, "names": list(controls)}}

def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(canonical(value) + b"\n")
def checkpoint_identity(path: Path | None) -> dict[str, Any]:
    if path is None: return {"path": None, "status": "ABSENT", "bytes": 0, "sha256": None}
    raw = path.read_bytes() if path.is_file() else b""
    return {"path": str(path), "status": "PRESENT" if path.is_file() else "ABSENT", "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest() if raw else None}


def require_input_reason(reason: str) -> None:
    require(any(reason == prefix or reason.startswith(prefix) for prefix in ALLOWED_INPUT_PREFIXES), "unregistered input reason")


def resource_fields(exc: BaseException) -> tuple[str, str, Any, Any, dict[str, Any]]:
    phase = str(getattr(exc, "phase", "")); cap = str(getattr(exc, "cap", "")); value = getattr(exc, "value", None); limit = getattr(exc, "limit", None)
    require(phase in ALLOWED_RESOURCE_CAPS and cap in ALLOWED_RESOURCE_CAPS[phase] and isinstance(value, (int, float)) and
            not isinstance(value, bool) and isinstance(limit, (int, float)) and not isinstance(limit, bool) and value > limit,
            "unregistered resource stop")
    resource = dict(getattr(exc, "resource", {}) or {}); resource.update({"phase": phase, "cap": cap, "value": value, "limit": limit,
        "terminal_cap": cap, "terminal_value": value, "terminal_limit": limit})
    return phase, cap, value, limit, resource

def unknown_input_receipt(reason: str, checkpoint_ref: Path) -> dict[str, Any]:
    require_input_reason(reason)
    pins = expected_pins()
    identity = checkpoint_identity(checkpoint_ref)
    # Input authentication fails before a new solver state exists.  A stale
    # output checkpoint must not be silently reclassified as part of an
    # UNKNOWN_INPUT receipt; the caller/driver must fail closed instead.
    require(identity["status"] == "ABSENT", "input failure with stale checkpoint")
    return {"schema": SCHEMA, "status": UNKNOWN_INPUT, "terminal": f"{UNKNOWN_INPUT}:{reason}",
            "reason": reason, "pins": pins,
            "input_failure": {"class": "InputStop", "reason": reason, "expected_pins": pins},
            "claims": {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False},
            "checkpoint_identity": identity}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); p.add_argument("--mode", choices=("SELFTEST", "PRODUCTION")); p.add_argument("--selftest", action="store_true"); p.add_argument("--output", "--receipt", dest="output", type=Path); p.add_argument("--resume", type=Path); p.add_argument("--checkpoint", type=Path); p.add_argument("--seconds", type=int, default=19800); p.add_argument("--boundary-pairs", type=int, default=8000000); p.add_argument("--fibre-scans", type=int, default=80000000); p.add_argument("--candidate-words", type=int, default=2000000); p.add_argument("--retained-columns", type=int, default=250000); p.add_argument("--checkpoint-bytes", type=int, default=4000000000); p.add_argument("--rss-bytes", type=int, default=5700000000); p.add_argument("--oracle-rounds", type=int, default=1000000); return p
def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv); mode = "SELFTEST" if args.selftest else (args.mode or "SELFTEST")
    if mode == "SELFTEST":
        receipt = toy_batch();
        if args.output: write_json(args.output, seal(receipt))
        print(COMMON + "_PRODUCER_SELFTEST_PASS"); return 0
    output = args.output or ROOT / "ci/out/d972_r07_u0v0_boundary_preimage_batch_v2.json"
    # ``--resume`` names the input artifact only.  solve() always writes the
    # continuation checkpoint to --checkpoint (or the output-derived default),
    # and UNKNOWN_RESOURCE must identify that newly advanced artifact.
    checkpoint_ref = args.checkpoint or (output.with_suffix(output.suffix + ".checkpoint.json") if args.output else ROOT / "ci/out/d972_r07_u0v0_boundary_preimage_batch_v2.checkpoint.json")
    if checkpoint_ref.is_file():
        raise RuntimeError("checkpoint output must be fresh")
    if args.resume and args.resume.resolve() == checkpoint_ref.resolve():
        raise RuntimeError("resume input/output checkpoint collision")
    try: receipt = solve(args)
    except InputStop as exc:
        receipt = unknown_input_receipt(str(exc), checkpoint_ref)
    except Exception as exc:
        if exc.__class__.__name__ == "InputStop":
            receipt = unknown_input_receipt(str(exc), checkpoint_ref)
        elif exc.__class__.__name__ == "ResourceStop":
            phase, cap, value, limit, resource = resource_fields(exc)
            checkpoint_id = checkpoint_identity(checkpoint_ref)
            receipt = {"schema": SCHEMA, "status": UNKNOWN_RESOURCE, "terminal": f"{UNKNOWN_RESOURCE}:{phase}:{cap}:{value}>{limit}", "reason": str(exc), "pins": expected_pins(), "claims": {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False}, "resource": resource, "checkpoint_state": "RESUMABLE" if checkpoint_id["status"] == "PRESENT" else "INITIAL_ABSENT", "checkpoint_identity": checkpoint_id}
        else: raise
    write_json(output, seal(receipt)); print(COMMON + "_PRODUCER_TERMINAL " + receipt["terminal"]); return 0
if __name__ == "__main__": raise SystemExit(main())
