#!/usr/bin/env python3
"""Independent checker for task191's batched boundary preimage receipt."""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, itertools, json, math
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-u0v0-boundary-preimage-batch/v2"
SELFTEST_SCHEMA = "d972-r07-u0v0-boundary-preimage-batch-selftest/v2"
COMMON = "R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2"
UNKNOWN_RESOURCE, UNKNOWN_INPUT = "UNKNOWN_RESOURCE", "UNKNOWN_INPUT"
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
    "task179_instruction": ("sol/luna_task_179_r07_positive_common_word_colgen_v1.md", 13105, "f97870ec0243b2c399928bcef4f89134f1cd41f15869cc88e3ba7d9dc6956a73"), "proof142": ("sol/proof_r07_actual_singleton_coarse_inverse_selector_v142.md", 4942, "5f0fffe64b729a8e44643ce86e9d588ef96cbe199ef8ca03741c712c2b162ee8"), "proof143": ("sol/proof_r07_actual_weighted_support_hitting_selector_v143.md", 5253, "aae57d5481d7e649d449b58d06ade2d9cbf90fa48d50a8ae43650da5243cf259"), "proof139": ("sol/proof_r07_witness_first_fibre_dovetail_selector_v139.md", 8310, "62e2160348db38eca1570b2ca6eb8934b885569f4e8cfb276a91b98c9b983920"), "proof140": ("sol/proof_r07_positive_only_common_word_colgen_v140.md", 10073, "6d388a74c75d55d215b0035496c451aa9de5bbc7a8248c277e76021092b8562b"), "proof138": ("sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md", 6371, "9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456"), "proof110": ("sol/proof_r07_full_e4_seven_evaluation_orbit_selector_v110.md", 12136, "dd0b75d6dc85229405a3a95e3631a709aa40a0ad21f2c17b96106dae2c7989dc"), "proof108": ("sol/proof_pb4_eleven_relator_presentation_equality_v108.md", 6742, "4a228f2b055fae7657ac5ca5b2e242eb05afcb04f6fb75ae79e9e776b3bca42f"), "proof121": ("sol/proof_pb3_two_relator_presentation_equality_v121.md", 5762, "efd51ee51d496543e359704349877523a9d5d4aea686aee97e33c00dd6b84bd5"), "proof122": ("sol/proof_r07_e3_context_kernel_retraction_bridge_v122.md", 7939, "daadae2bed6a91ded8d3f1abec4d2fb6d379b80706f6387fa12abfd8f29e1348"), "proof125": ("sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md", 8545, "b82c81e0a053658fdb48cbb4d3054a094a57a81b2fd5d0153bcd0735ef4852b3"), "proof135": ("sol/proof_r07_q4_q0_noncontiguous_deletion_layout_v135.md", 4539, "75c511a765ad88ec1aa72c63a0d1965ac85724695d743cbf00350572a884cf67"),
    "task175_producer": ("search/d972_r07_all_seven_raw_bridge_preflight_v1.py", 60306, "1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa"), "task175_checker": ("crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py", 88503, "0b45c3daa1db6cad63d434170c65d0dbfa928efc51543b881dc0aa2e3a0f1fce"), "task175_driver": ("search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g", 22052, "919e7a9efe7385444c480203dc51525873e770236777dd61e2f6fc1ef22de494"), "task176_producer": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109, "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"), "task176_checker": ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980, "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"), "task176_driver": ("search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g", 15929, "1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995"), "q3_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"), "joint_receipt": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036, "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"), "seedspan_arithmetic": ("search/d972_b345_seedspan_triple4_v1.py", 535219, "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"), "old_arithmetic": ("search/d972_b345_triple_cube_raw_lambda_census_v1.py", 126942, "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"), "joint_source": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945, "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"), "v172_source": ("search/d972_r07_full_e4_joint_orbit_preflight_v7.py", 21918, "92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed"), "g760_source": ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409, "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"), "pb4_source": ("search/d972_b345_target6_dual_colgen_v2.py", 444497, "b361dc5e7b025bb7efe3507b145e5480c6c67dfecc2e712134a8d521585e73c7"), "full_d2_v1": ("search/d972_b345_full_d2_dual_correlation_v1.py", 78832, "6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52"), "full_d2_v2": ("search/d972_b345_full_d2_dual_correlation_v2.py", 42449, "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f"),
}
FIXTURE = ROOT / "search/certs/d972_r07_u0v0_boundary_preimage_batch_selftest_v2_20260827.json"
ALLOWED_RESOURCE_CAPS = {"task175_reconstruction": {"wall_seconds", "rss_bytes"}, "fine_deletion": {"wall_seconds", "rss_bytes"}, "Q0_positive_shortlex_section": {"wall_seconds", "rss_bytes"}, "Q0_discovery": {"wall_seconds", "rss_bytes"}, "A_L_membership_scan": {"wall_seconds", "rss_bytes"}, "L_subgroup_closure": {"wall_seconds", "rss_bytes"}, "typed_singleton_equality": {"wall_seconds", "rss_bytes"}, "runtime_reconstruction": {"wall_seconds", "rss_bytes"}, "complete_boundary_correlation": {"wall_seconds", "rss_bytes", "boundary_pairs", "oracle_rounds"}, "boundary_echelon": {"wall_seconds", "rss_bytes", "retained_columns"}, "checkpoint_serialization": {"checkpoint_bytes"}}
ALLOWED_INPUT_PREFIXES = ("pin:", "v1 loader", "task179:")

def require(ok: bool, msg: str) -> None:
    if not ok: raise RuntimeError(msg)
def canon(v: Any) -> bytes: return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
def digest(v: Any) -> str: return hashlib.sha256(canon(v)).hexdigest()
def public(row: dict[bytes, int]) -> list[list[Any]]: return [[k.hex(), int(row[k]) % 3] for k in sorted(row) if int(row[k]) % 3]
def auth(table: dict[str, tuple[str, int, str]]) -> dict[str, Any]:
    out = {}
    for name, (rel, size, sha) in table.items():
        raw = (ROOT / rel).read_bytes() if (ROOT / rel).is_file() else b""
        require(len(raw) == size and hashlib.sha256(raw).hexdigest() == sha, "pin:" + rel)
        out[name] = {"path": rel, "bytes": size, "sha256": sha}
    return out

def expected_manifest(table: dict[str, tuple[str, int, str]]) -> dict[str, Any]:
    return {name: {"path": rel, "bytes": size, "sha256": sha}
            for name, (rel, size, sha) in table.items()}

def expected_pins() -> dict[str, Any]:
    return {"v1": expected_manifest(V1_PINS), "task179": expected_manifest(TASK179_PINS)}


def validate_checkpoint_identity(value: Any) -> None:
    require(type(value) is dict and set(value) == {"path", "status", "bytes", "sha256"}, "checkpoint identity schema")
    path, status, size, sha = value["path"], value["status"], value["bytes"], value["sha256"]
    require((path is None or type(path) is str) and status in ("PRESENT", "ABSENT") and
            type(size) is int and not isinstance(size, bool) and size >= 0, "checkpoint identity types")
    if status == "ABSENT":
        require(size == 0 and sha is None and
                (path is None or not (Path(path) if Path(path).is_absolute() else ROOT / Path(path)).is_file()),
                "absent checkpoint identity")
        return
    require(type(path) is str and bool(path) and type(sha) is str and len(sha) == 64 and
            all(char in "0123456789abcdef" for char in sha.lower()), "present checkpoint identity")
    candidate = Path(path); candidate = candidate if candidate.is_absolute() else ROOT / candidate
    require(candidate.is_file(), "present checkpoint missing")
    raw = candidate.read_bytes()
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == sha.lower(), "present checkpoint digest")

def validate_final_checkpoint(receipt: dict[str, Any], identity: dict[str, Any]) -> None:
    candidate = Path(identity["path"]); candidate = candidate if candidate.is_absolute() else ROOT / candidate
    checkpoint = json.loads(candidate.read_text(encoding="ascii")); body = dict(checkpoint); claimed = body.pop("self_digest", None)
    require(type(claimed) is str and claimed == digest(body) and checkpoint.get("schema") == SCHEMA + "/checkpoint" and
            checkpoint.get("input_identity") == receipt.get("pins") and checkpoint.get("columns") == receipt.get("columns") and
            checkpoint.get("batch_records") == receipt.get("batch_records") and checkpoint.get("correlations") == receipt.get("correlations") and
            checkpoint.get("rank_transitions") == receipt.get("rank_transitions") and
            checkpoint.get("target_reconsideration_log") == receipt.get("target_reconsideration_log") and
            checkpoint.get("stats") == receipt.get("batch_stats") and checkpoint.get("unresolved") == [] and
            checkpoint.get("active_suffix") == [] and checkpoint.get("pending_batch") is None and
            checkpoint.get("target_progress") == receipt.get("targets"), "PASS checkpoint binding")


def validate_sealed_resource_checkpoint(identity: dict[str, Any], pins: dict[str, Any]) -> None:
    candidate = Path(identity["path"]); candidate = candidate if candidate.is_absolute() else ROOT / candidate
    checkpoint = json.loads(candidate.read_text(encoding="ascii")); body = dict(checkpoint); claimed = body.pop("self_digest", None)
    require(set(checkpoint) == {"schema", "input_identity", "columns", "batch_records", "correlations",
                                "rank_transitions", "unresolved", "active_suffix", "pending_batch",
                                "target_progress", "stats", "target_reconsideration_log", "self_digest"} and
            type(claimed) is str and claimed == digest(body) and checkpoint.get("schema") == SCHEMA + "/checkpoint" and
            checkpoint.get("input_identity") == pins and type(checkpoint.get("columns")) is list and
            type(checkpoint.get("batch_records")) is list and type(checkpoint.get("correlations")) is list and
            type(checkpoint.get("rank_transitions")) is list and type(checkpoint.get("unresolved")) is list and
            type(checkpoint.get("active_suffix")) is list and type(checkpoint.get("target_progress")) is dict and
            type(checkpoint.get("stats")) is dict and type(checkpoint.get("target_reconsideration_log")) is list,
            "sealed resumable checkpoint")
    require(all(type(item) is dict and "row_dict" not in item for item in checkpoint["columns"] + checkpoint["batch_records"]),
            "checkpoint private row leakage")


def validate_input_reason(reason: Any) -> None:
    require(type(reason) is str and bool(reason) and
            any(reason == prefix or reason.startswith(prefix) for prefix in ALLOWED_INPUT_PREFIXES),
            "authenticated input reason")


def parse_resource_terminal(receipt: dict[str, Any]) -> None:
    terminal = receipt.get("terminal")
    require(type(terminal) is str, "resource terminal type")
    parts = terminal.split(":")
    require(len(parts) == 4 and parts[0] == UNKNOWN_RESOURCE and parts[1] in ALLOWED_RESOURCE_CAPS and
            parts[2] in ALLOWED_RESOURCE_CAPS[parts[1]] and ">" in parts[3], "resource terminal")
    value_text, limit_text = parts[3].split(">", 1)
    try:
        value, limit = float(value_text), float(limit_text)
    except (TypeError, ValueError):
        raise RuntimeError("resource terminal numeric")
    require(math.isfinite(value) and math.isfinite(limit) and value > limit, "resource terminal bound")
    require(receipt.get("reason") == ":".join(parts[1:]), "resource reason")
    resource = receipt.get("resource")
    require(type(resource) is dict and resource.get("phase") == parts[1] and resource.get("cap") == parts[2], "resource identity")
    try:
        terminal_value, terminal_limit = float(resource.get("terminal_value")), float(resource.get("terminal_limit"))
    except (TypeError, ValueError):
        raise RuntimeError("resource receipt numeric")
    require(resource.get("terminal_cap") == parts[2] and resource.get("value") == value and
            resource.get("limit") == limit and terminal_value == value and terminal_limit == limit and
            isinstance(resource.get("limits"), dict), "resource receipt")
    registered = resource["limits"].get(parts[2])
    require(isinstance(registered, (int, float)) and not isinstance(registered, bool) and
            math.isfinite(float(registered)) and float(registered) == limit and value > float(registered),
            "registered resource limit")
def load_task179_checker() -> Any:
    path = ROOT / TASK179_PINS["checker"][0]; spec = importlib.util.spec_from_file_location("task179_independent_v2", path)
    require(spec is not None and spec.loader is not None, "task179 checker loader")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); mod._boundary_auth = mod.authenticate(); return mod
def inv(w: Sequence[int]) -> tuple[int, ...]: return tuple(-int(x) for x in reversed(w))
def mul(*words: Sequence[int]) -> tuple[int, ...]:
    out: tuple[int, ...] = ()
    for word in words:
        for x in word:
            x = int(x); out = out[:-1] if out and out[-1] == -x else out + (x,)
    return out
def exponent(w: Sequence[int]) -> tuple[int, int]: return (sum(1 if x == 1 else -1 if x == -1 else 0 for x in w), sum(1 if x == 2 else -1 if x == -2 else 0 for x in w))
def add(dst: dict[bytes, int], src: dict[bytes, int], scalar: int) -> None:
    for k, v in src.items():
        z = (dst.get(k, 0) + scalar * int(v)) % 3
        if z: dst[k] = z
        else: dst.pop(k, None)
def pair(f: dict[bytes, int], row: dict[bytes, int]) -> int: return sum(int(v) * int(row.get(k, 0)) for k, v in f.items()) % 3
def sparse(c: Any, rows: list[list[Any]]) -> dict[bytes, int]:
    require(type(rows) is list and all(type(x) is list and len(x) == 2 and type(x[0]) is str and type(x[1]) is int and not isinstance(x[1], bool) for x in rows), "sparse schema")
    return c.parse_sparse(rows)

class Space:
    def __init__(self) -> None: self.pivots: list[bytes] = []; self.rows: dict[bytes, dict[bytes, int]] = {}; self.origins: dict[bytes, dict[int, int]] = {}
    def reduce(self, source: dict[bytes, int]):
        row = dict(source); coeff: dict[int, int] = {}
        for p in self.pivots:
            z = row.get(p, 0)
            if z:
                add(row, self.rows[p], -z)
                for k, v in self.origins[p].items():
                    q = (coeff.get(k, 0) + z * v) % 3
                    if q: coeff[k] = q
                    else: coeff.pop(k, None)
        return row, coeff
    def add(self, source: dict[bytes, int], number: int):
        row = dict(source); origin = {number: 1}
        for p in self.pivots:
            z = row.get(p, 0)
            if z:
                add(row, self.rows[p], -z)
                for k, v in self.origins[p].items():
                    q = (origin.get(k, 0) - z * v) % 3
                    if q: origin[k] = q
                    else: origin.pop(k, None)
        require(row, "dependent row submitted as retained")
        p = min(row); scale = 1 if row[p] == 1 else 2
        self.rows[p] = {k: scale * v % 3 for k, v in row.items() if scale * v % 3}; self.origins[p] = {k: scale * v % 3 for k, v in origin.items() if scale * v % 3}; self.pivots.append(p)
        return p, self.origins[p]
    def dual(self, target: dict[bytes, int]):
        rem, _ = self.reduce(target); require(rem, "dual after membership"); f = {min(rem): 1}
        for p in reversed(self.pivots):
            z = -sum(v * f.get(k, 0) for k, v in self.rows[p].items() if k != p) % 3
            if z: f[p] = z
            else: f.pop(p, None)
        require(all(pair(f, self.rows[p]) == 0 for p in self.pivots) and pair(f, target), "terminal dual")
        return f

def words(rt: dict[str, Any]) -> dict[str, tuple[int, ...]]:
    out = {}
    for ordinal in (3, 9, 12):
        rows = [r["word"] for r in rt["obj"]["roster"] if r.get("layer") == "q0_relator" and int(r.get("ordinal")) == ordinal]
        require(len(rows) == 1, "registered ordinal"); out[str(ordinal)] = tuple(rows[0])
    out["v0"] = mul(out["9"], out["12"], inv(out["3"]), inv(out["3"])); out["u0"] = mul(out["9"], *([inv(out["v0"])] * 8))
    require(exponent(out["v0"]) == (0, 18) and exponent(out["u0"]) == (18, 0), "word exponents"); return out
def occurrences(c: Any, rt: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for block, rows in ((1, rt["obj"]["pb3_rows"]), (2, rt["obj"]["pb3_rows"]), (3, rt["obj"]["pb4_rows"])):
        q = rt["e3"] if block in (1, 2) else rt["e4"]
        for index, source in enumerate(rows, 1):
            for (component, h), coefficient in source.items(): out.append({"block": block, "relator_index": index, "component": int(component), "h": h, "h_inv": q.inverse(h), "base_coefficient": int(coefficient) % 3})
    return out
def public_occurrences(c: Any, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"block": int(x["block"]), "relator_index": int(x["relator_index"]), "component": int(x["component"]), "h_blob": c.element_blob(x["h"]).hex(), "base_coefficient": int(x["base_coefficient"])} for x in items]
def correlation(c: Any, rt: dict[str, Any], occ: list[dict[str, Any]], dual: dict[bytes, int]) -> dict[str, Any]:
    support = {}
    for key, value in dual.items():
        if key[:1] == b"R":
            b, comp, raw = c.decode_row_key(key); support.setdefault((b, comp), []).append((raw, int(value), c.parse_element(raw, b)))
    acc = {}; contributors = {}
    for item in occ:
        q = rt["e3"] if item["block"] in (1, 2) else rt["e4"]
        for g_raw, lam, g in support.get((item["block"], item["component"]), []):
            t = q.mul(g, item["h_inv"]); require(q.mul(t, item["h"]) == g, "translation reconstruction")
            tb = c.element_blob(t); key = (item["block"], tb, item["relator_index"]); acc[key] = (acc.get(key, 0) + lam * item["base_coefficient"]) % 3
            contributors.setdefault(key, []).append({"component": item["component"], "g_hex": g_raw.hex(), "h_hex": c.element_blob(item["h"]).hex(), "lambda_coefficient": lam, "base_coefficient": item["base_coefficient"]})
    for rows in contributors.values(): rows.sort(key=lambda x: (x["component"], x["g_hex"], x["h_hex"], x["lambda_coefficient"], x["base_coefficient"]))
    active = [[b, t.hex(), i] for b, t, i in sorted((b, t, i) for (b, t, i), v in acc.items() if v % 3)]
    return {"complete": True, "sampled": False, "active": active, "scanned_occurrences": sum(len(x) for x in contributors.values()), "contributors": {f"{b}:{t.hex()}:{i}": x for (b, t, i), x in contributors.items()}, "accumulated": {f"{b}:{t.hex()}:{i}": int(v) for (b, t, i), v in acc.items() if v % 3}}

def validate_prod(receipt: dict[str, Any]) -> None:
    require(receipt.get("pins") == {"v1": auth(V1_PINS), "task179": auth(TASK179_PINS)}, "receipt pins")
    c = load_task179_checker(); rt = c.independent_runtime(); ws = words(rt); require(receipt.get("schema") == SCHEMA and receipt.get("status") == "PASS" and receipt.get("terminal") == COMMON, "receipt envelope")
    require(receipt.get("v1_arithmetic_authentication") is True and
            receipt.get("words") == {label: list(ws[label]) for label in ("u0", "v0")} and
            receipt.get("cache_key") == "(block,translation_blob,relator_index)", "receipt load-bearing identity")
    require(receipt.get("mathematical_space") == "span of every left translate of the 2 PB3 and 11 PB4 boundary rows", "space binding")
    require(receipt.get("full_active_batch_transcript") is True and receipt.get("post_membership_suffix_processed") is True, "full ACTIVE transcript contract")
    require(receipt.get("claims") == {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False}, "receipt claims")
    final_checkpoint = receipt.get("checkpoint_identity"); validate_checkpoint_identity(final_checkpoint)
    require(final_checkpoint.get("status") == "PRESENT", "PASS checkpoint identity")
    validate_final_checkpoint(receipt, final_checkpoint)
    space = Space(); occ = occurrences(c, rt); rows: list[dict[bytes, int]] = []; expected = {}; expected_columns = []
    require(receipt.get("boundary_occurrence_roster") == public_occurrences(c, occ), "occurrence roster replay")
    for label in ("u0", "v0"):
        raw, replay = c.direct_correction(rt, [], list(ws[label])); raw = {k: v for k, v in raw.items() if not k.startswith(b"E")}; target = {}; add(target, raw, -1); expected[label] = target
        integer = exponent(ws[label]); require(integer[0] % 18 == 0 and integer[1] % 18 == 0, label + " exponent divisibility")
        normalized = [integer[0] // 18 % 3, integer[1] // 18 % 3]
        item = receipt["targets"][label]; direct = item.get("direct_replay")
        require(tuple(item["word"]) == ws[label] and item["integer_exponent"] == list(integer) and
                item["normalized_residue"] == normalized and item["A"] == public(raw) and
                item["A_sha256"] == digest(public(raw)) and item["target"] == public(target) and
                item["target_sha256"] == digest(public(target)) and type(direct) is dict and
                direct.get("delta_word") == [] and direct.get("relator_word") == list(ws[label]) and
                direct.get("conjugate_word") == list(replay["conjugate_word"]) and
                direct.get("corrected_word") == list(replay["corrected_word"]) and
                direct.get("eleven_occurrence_replay") is True and direct.get("direct_all_seven_replay") is True,
                label + " target")
    batches = receipt.get("correlations", []); records = receipt.get("batch_records", []); by_batch = {}; transition_map = {}; terminal_batches = {}
    decisions_state = {"u0": "UNRESOLVED", "v0": "UNRESOLVED"}
    require(type(batches) is list and type(records) is list, "receipt transcript schema")
    for rec in records:
        require(type(rec) is dict and type(rec.get("batch_id")) is int and not isinstance(rec.get("batch_id"), bool) and rec["batch_id"] > 0, "batch record id")
        by_batch.setdefault(rec["batch_id"], []).append(rec)
    for transition in receipt.get("rank_transitions", []):
        require(type(transition) is dict and type(transition.get("batch_id")) is int and not isinstance(transition.get("batch_id"), bool) and
                type(transition.get("batch_position")) is int and not isinstance(transition.get("batch_position"), bool), "rank transition schema")
        key = (transition["batch_id"], transition["batch_position"]); require(key not in transition_map, "duplicate rank transition"); transition_map[key] = transition
    require(set(by_batch).issubset(set(range(1, len(batches) + 1))), "unknown batch id")
    for batch_id, batch in enumerate(batches, 1):
        label = batch.get("target_label"); require(label in expected and decisions_state[label] == "UNRESOLVED", "batch target label"); expected_dual = space.dual(expected[label]); dual = sparse(c, batch["dual"]); require(dual == expected_dual, "fresh pre-batch dual")
        corr = correlation(c, rt, occ, dual); require(corr == batch["correlation"] and corr["complete"] and not corr["sampled"], "complete correlation replay")
        batch_rows = sorted(by_batch.get(batch_id, []), key=lambda x: int(x.get("batch_position", 0)))
        require([rec.get("batch_position") for rec in batch_rows] == list(range(len(batch_rows))) and len(batch_rows) == len(corr["active"]), "ACTIVE list materialization")
        for position, rec in enumerate(batch_rows):
            p = rec.get("provenance"); require(rec.get("target_label") == label and rec.get("batch_id") == batch_id and
                type(rec.get("batch_position")) is int and not isinstance(rec.get("batch_position"), bool) and
                type(rec.get("rank_before")) is int and not isinstance(rec.get("rank_before"), bool) and
                type(rec.get("rank_after")) is int and not isinstance(rec.get("rank_after"), bool) and
                rec.get("batch_position") == position and rec.get("classification") in ("retained", "dependent"), "batch record binding")
            require(type(p) is dict and p.get("family") == "boundary" and p.get("left_translation") == "t=g*h^-1; t*h=g" and
                    p.get("complete_support_occurrence_accumulation") is True and p.get("active_key") == corr["active"][position] and
                    p.get("contributing_pairs") == corr["contributors"].get(f"{corr['active'][position][0]}:{corr['active'][position][1]}:{corr['active'][position][2]}", []), "canonical ACTIVE provenance")
            require(p.get("block") == corr["active"][position][0] and p.get("base_relator_index") == corr["active"][position][2] and
                    p.get("translation_hex") == corr["active"][position][1], "active source binding")
            row = c.boundary_row(rt, int(p["block"]), int(p["base_relator_index"]), p["translation_hex"]); require(public(row) == rec["sparse_row"] and rec["sparse_row_sha256"] == digest(rec["sparse_row"]), "literal cached row")
            require(rec.get("active_dual") == batch.get("dual") and rec.get("active_dual_sha256") == digest(rec.get("active_dual")) and
                    rec.get("dual_pairing") == pair(dual, row) and p.get("pre_batch_dual_pairing") == pair(dual, row), "active dual provenance")
            if rec["classification"] == "retained":
                column_id = rec.get("column_id"); require(type(column_id) is int and not isinstance(column_id, bool) and column_id == len(rows) + 1, "retained column id")
                before = len(space.pivots); pivot, ancestry = space.add(row, column_id); require(before == rec["rank_before"] and rec["rank_after"] == len(space.pivots) == before + 1 and pivot.hex() == rec["pivot_hex"] and rec["pivot_ancestry"] == [[k, v] for k, v in sorted(ancestry.items())] and rec.get("dual_pairing") == pair(dual, row) != 0, "retained rank replay"); rows.append(row); expected_columns.append(rec)
            elif rec["classification"] == "dependent":
                rem, dependency = space.reduce(row); require(not rem, "dependent batch row"); rebuilt = {}; chain = rec["dependency_chain"]
                require(type(chain) is list and all(type(item) is list and len(item) == 2 and type(item[0]) is int and
                                                    not isinstance(item[0], bool) and 1 <= item[0] <= len(rows) and
                                                    type(item[1]) is int and not isinstance(item[1], bool) and item[1] in (1, 2)
                                                    for item in chain), "dependent ancestry schema")
                for k, v in chain: add(rebuilt, rows[k - 1], v)
                require(rebuilt == row and chain == [[key, value] for key, value in sorted(dependency.items())] and
                        rec["rank_before"] == rec["rank_after"] == len(space.pivots), "dependent ancestry replay")
            else: raise RuntimeError("unknown batch classification")
            decisions = {}
            for target_label in ("u0", "v0"):
                trial, _ = space.reduce(expected[target_label])
                if not trial:
                    decisions_state[target_label] = "MEMBER_D"
                decisions[target_label] = decisions_state[target_label]
            transition = transition_map.get((batch_id, position)); require(transition is not None and transition.get("classification") == rec["classification"] and transition.get("rank_before") == rec["rank_before"] and transition.get("rank_after") == rec["rank_after"] and transition.get("target_reconsidered") == decisions, "target reconsideration replay")
        if not corr["active"]:
            require(decisions_state[label] == "UNRESOLVED", "empty batch after target decision")
            terminal_batches[label] = {"dual": dual, "public_dual": batch["dual"], "correlation": corr}
            decisions_state[label] = "NONMEMBER_D"
    expected_record_keys = [(batch_id, position) for batch_id, batch in enumerate(batches, 1)
                            for position in range(len(batch["correlation"]["active"]))]
    actual_record_keys = [(int(rec["batch_id"]), int(rec["batch_position"])) for rec in records]
    require(actual_record_keys == expected_record_keys, "canonical batch transcript order")
    log_entries = receipt.get("target_reconsideration_log", []); require(type(log_entries) is list, "target reconsideration schema")
    log_map = {}
    for point in log_entries:
        require(type(point) is dict and type(point.get("batch_id")) is int and not isinstance(point.get("batch_id"), bool) and
                type(point.get("batch_position")) is int and not isinstance(point.get("batch_position"), bool), "target log schema")
        key = (point["batch_id"], point["batch_position"]); require(key not in log_map, "duplicate target log"); log_map[key] = point
    record_keys = {(int(rec["batch_id"]), int(rec["batch_position"])) for rec in records}
    require(set(transition_map) == record_keys and set(log_map) == record_keys and len(transition_map) == len(records), "target reconsideration transcript")
    require([(int(x["batch_id"]), int(x["batch_position"])) for x in receipt.get("rank_transitions", [])] == expected_record_keys and
            [(int(x["batch_id"]), int(x["batch_position"])) for x in log_entries] == expected_record_keys,
            "canonical target transcript order")
    for point in log_entries:
        key = (point["batch_id"], point["batch_position"]); require(transition_map.get(key, {}).get("target_reconsidered") == point.get("decisions"), "target reconsideration log")
    stats = receipt.get("batch_stats")
    require(type(stats) is dict, "batch statistics schema")
    expected_stats = {"complete_correlation_rounds": len(batches), "support_occurrence_pairs_total": 0,
        "pairs_per_round": [], "active_total": 0, "retained_total": 0, "dependent_total": 0,
        "cache_hits": 0, "cache_misses": 0, "rank_gains": [], "target_reconsiderations": len(records)}
    for batch in batches:
        current = batch["correlation"]; scanned = int(current["scanned_occurrences"])
        expected_stats["support_occurrence_pairs_total"] += scanned
        expected_stats["pairs_per_round"].append(scanned); expected_stats["active_total"] += len(current["active"])
    seen_active = set()
    for rec in records:
        if rec["classification"] == "retained":
            expected_stats["retained_total"] += 1; expected_stats["rank_gains"].append(int(rec["rank_after"]))
        else:
            expected_stats["dependent_total"] += 1
        active = rec["provenance"]["active_key"]; cache_key = (int(active[0]), str(active[1]), int(active[2]))
        if cache_key in seen_active: expected_stats["cache_hits"] += 1
        else: expected_stats["cache_misses"] += 1; seen_active.add(cache_key)
    require(stats == expected_stats, "batch statistics replay")
    require(receipt.get("columns") == expected_columns, "retained column transcript")
    require(receipt.get("rank") == len(space.pivots), "final rank")
    for label in ("u0", "v0"):
        item = receipt["targets"][label]; rem, coeff = space.reduce(expected[label]); decision = item.get("decision")
        require(decision == decisions_state[label], label + " decision state")
        if decision == "MEMBER_D":
            chain = [[int(k), int(v)] for k, v in item["chain"]]; combined = {}; [add(combined, rows[k - 1], v) for k, v in chain]; require(not rem and combined == expected[label] and chain == [[int(k), int(v)] for k, v in sorted(coeff.items())], label + " member chain")
        elif decision == "NONMEMBER_D":
            require(rem, label + " nonmember remainder"); require(label in terminal_batches, label + " terminal batch")
            terminal_batch = terminal_batches[label]; d = item["terminal_dual"]; f = sparse(c, d["row"])
            require(d["row"] == terminal_batch["public_dual"] and f == terminal_batch["dual"] and
                    d["annihilates_retained"] is True and d["row_sha256"] == digest(d["row"]) and
                    d["pairing_target"] == pair(f, expected[label]) != 0 and
                    all(pair(f, row) == 0 for row in rows) and
                    d["full_correlation"] == terminal_batch["correlation"] and
                    d["full_correlation"]["active"] == [] and
                    d["full_correlation"]["complete"] is True and
                    d["full_correlation"]["sampled"] is False, label + " terminal dual")
        else: raise RuntimeError(label + " untyped decision")


def validate_unknown(receipt: dict[str, Any]) -> None:
    require(receipt.get("schema") == SCHEMA and receipt.get("status") in (UNKNOWN_RESOURCE, UNKNOWN_INPUT), "unknown schema")
    pins = expected_pins()
    require(receipt.get("pins") == pins and {"v1": auth(V1_PINS), "task179": auth(TASK179_PINS)} == pins and
            receipt.get("claims") == {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False}, "unknown identity")
    require(type(receipt.get("reason")) is str and bool(receipt["reason"]), "unknown reason type")
    validate_checkpoint_identity(receipt.get("checkpoint_identity"))
    if receipt["status"] == UNKNOWN_RESOURCE:
        parse_resource_terminal(receipt)
        identity = receipt["checkpoint_identity"]
        state = receipt.get("checkpoint_state")
        require(state in ("RESUMABLE", "INITIAL_ABSENT") and
                ((state == "RESUMABLE" and identity["status"] == "PRESENT") or
                 (state == "INITIAL_ABSENT" and identity["status"] == "ABSENT")), "resource checkpoint state")
        if identity["status"] == "PRESENT":
            require(receipt.get("resource", {}).get("counters", {}).get("checkpoint_bytes") == identity["bytes"],
                    "resource checkpoint byte binding")
            validate_sealed_resource_checkpoint(identity, pins)
        else:
            require(receipt.get("resource", {}).get("phase") in {
                "task175_reconstruction", "fine_deletion", "Q0_positive_shortlex_section", "Q0_discovery",
                "A_L_membership_scan", "L_subgroup_closure", "typed_singleton_equality", "runtime_reconstruction",
                "complete_boundary_correlation", "checkpoint_serialization"}, "initial resource phase")
        require("input_failure" not in receipt, "resource input failure field")
    else:
        validate_input_reason(receipt["reason"])
        terminal = receipt.get("terminal")
        require(type(terminal) is str and terminal == UNKNOWN_INPUT + ":" + receipt["reason"] and
                receipt.get("checkpoint_identity", {}).get("status") == "ABSENT", "input terminal")
        require("resource" not in receipt and receipt.get("input_failure") == {
            "class": "InputStop", "reason": receipt["reason"], "expected_pins": pins}, "input resource/failure fields")


TOY_IDENTITY = (1, 2, 3); TOY_SIGMA = (2, 1, 3); TOY_TAU = (1, 3, 2); TOY_CYCLE = (2, 3, 1)
TOY_TARGET_U = b"R" + bytes((1, 1)) + bytes(TOY_IDENTITY)
TOY_TARGET_V = b"R" + bytes((2, 1)) + bytes(TOY_IDENTITY)


def toy_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]: return tuple(int(left[int(index) - 1]) for index in right)
def toy_inv(value: Sequence[int]) -> tuple[int, ...]:
    result = [0] * len(value)
    for index, image in enumerate(value, 1): result[int(image) - 1] = index
    return tuple(result)
def toy_row(block: int, index: int, translation: bytes) -> dict[bytes, int]:
    t = tuple(translation)
    if (block, index, t) == (1, 1, TOY_IDENTITY): return {TOY_TARGET_U: 1}
    if (block, index, t) == (1, 1, TOY_TAU): return {TOY_TARGET_U: 1, b"B": 1}
    if (block, index, t) == (1, 1, TOY_SIGMA): return {TOY_TARGET_U: 2, b"B": 1}
    if (block, index, t) == (1, 1, TOY_CYCLE): return {TOY_TARGET_U: 1, b"C": 1}
    return {}
def toy_sparse(rows: Any) -> dict[bytes, int]:
    require(type(rows) is list and all(type(row) is list and len(row) == 2 and type(row[0]) is str and type(row[1]) is int and not isinstance(row[1], bool) for row in rows), "toy sparse")
    result = {}
    for key, value in rows:
        byte_key = bytes.fromhex(key); residue = int(value) % 3
        if residue: result[byte_key] = residue
    return result
def toy_correlation(dual: dict[bytes, int]) -> dict[str, Any]:
    support = {}
    for key, value in dual.items():
        if key[:1] == b"R": support.setdefault((key[1], key[2]), []).append((key[3:], int(value)))
    accumulated = {}; contributors = {}
    for translation in (TOY_IDENTITY, TOY_TAU, TOY_SIGMA, TOY_CYCLE):
        h = toy_inv(translation)
        for g_blob, coefficient in support.get((1, 1), []):
            g = tuple(g_blob); t = toy_mul(g, toy_inv(h)); require(toy_mul(t, h) == g, "toy t*h=g")
            key = (1, bytes(t), 1); accumulated[key] = (accumulated.get(key, 0) + coefficient) % 3
            contributors.setdefault(key, []).append({"component": 1, "g_hex": g_blob.hex(), "h_hex": bytes(h).hex(), "lambda_coefficient": coefficient, "base_coefficient": 1})
    for rows in contributors.values(): rows.sort(key=lambda row: (row["component"], row["g_hex"], row["h_hex"], row["lambda_coefficient"], row["base_coefficient"]))
    active = sorted((block, translation, index) for (block, translation, index), value in accumulated.items() if value % 3)
    return {"complete": True, "sampled": False, "active": [[block, translation.hex(), index] for block, translation, index in active],
        "scanned_occurrences": sum(len(rows) for rows in contributors.values()),
        "contributors": {f"{block}:{translation.hex()}:{index}": rows for (block, translation, index), rows in contributors.items()},
        "accumulated": {f"{block}:{translation.hex()}:{index}": int(value) for (block, translation, index), value in accumulated.items() if value % 3}}


def validate_toy_production(receipt: dict[str, Any]) -> None:
    body = dict(receipt); claimed = body.pop("self_digest", None)
    require(type(claimed) is str and claimed == digest(body), "toy production seal")
    require(receipt.get("schema") == SCHEMA and receipt.get("status") == "PASS" and receipt.get("terminal") == COMMON, "toy production envelope")
    identity = receipt.get("checkpoint_identity")
    require(type(identity) is dict and set(identity) == {"path", "status", "bytes", "sha256"} and
            identity.get("path") == "embedded://task191-toy-final" and identity.get("status") == "PRESENT" and
            type(identity.get("bytes")) is int and identity["bytes"] >= 1 and
            type(identity.get("sha256")) is str and len(identity["sha256"]) == 64,
            "toy final checkpoint identity")
    resource = receipt.get("resource")
    require(type(resource) is dict and resource.get("phase") == "checkpoint_serialization" and
            resource.get("limits") == {"wall_seconds": 100, "boundary_pairs": 100,
                "retained_columns": 100, "checkpoint_bytes": 1000000, "oracle_rounds": 100} and
            resource.get("counters", {}).get("boundary_pairs") == 4 and
            resource.get("counters", {}).get("retained_columns") == 3 and
            resource.get("counters", {}).get("oracle_rounds") == 2 and
            resource.get("counters", {}).get("checkpoint_bytes") == identity["bytes"],
            "toy final resource meter")
    expected = {"u0": {TOY_TARGET_U: 2}, "v0": {TOY_TARGET_V: 2}}
    for label, word in (("u0", [1]), ("v0", [2])):
        item = receipt.get("targets", {}).get(label); raw = {key: 1 for key in expected[label]}; target = expected[label]
        require(type(item) is dict and item.get("word") == word and item.get("A") == public(raw) and item.get("target") == public(target) and
                item.get("integer_exponent") == ([1, 0] if label == "u0" else [0, 1]) and
                item.get("normalized_residue") == [0, 0] and item.get("A_sha256") == digest(public(raw)) and
                item.get("target_sha256") == digest(public(target)) and type(item.get("direct_replay")) is dict and
                item["direct_replay"] == {"word": word, "direct_key": next(iter(raw)).hex(), "prefix": []}, "toy target literal")
    batches = receipt.get("correlations"); records = receipt.get("batch_records"); require(type(batches) is list and type(records) is list and len(batches) == 2, "toy batch count")
    by_batch: dict[int, list[dict[str, Any]]] = {}
    for record in records:
        require(type(record) is dict and type(record.get("batch_id")) is int and record["batch_id"] > 0, "toy batch id")
        by_batch.setdefault(record["batch_id"], []).append(record)
    require(set(by_batch).issubset({1, 2}), "toy unknown batch")
    space = Space(); row_by_id: dict[int, dict[bytes, int]] = {}; transition_map = {}; log_map = {}; expected_columns = []
    for transition in receipt.get("rank_transitions", []): transition_map[(transition["batch_id"], transition["batch_position"])] = transition
    for point in receipt.get("target_reconsideration_log", []): log_map[(point["batch_id"], point["batch_position"])] = point
    for batch_id, batch in enumerate(batches, 1):
        label = batch.get("target_label"); require(label == ("u0" if batch_id == 1 else "v0"), "toy batch label")
        dual = toy_sparse(batch.get("dual")); expected_dual = {TOY_TARGET_U: 1} if batch_id == 1 else {TOY_TARGET_V: 1}
        require(dual == expected_dual and batch.get("dual") == public(expected_dual), "toy dual")
        corr = toy_correlation(dual); require(batch.get("correlation") == corr and corr["complete"] is True and corr["sampled"] is False, "toy correlation")
        rows = sorted(by_batch.get(batch_id, []), key=lambda record: int(record.get("batch_position", -1)))
        require([record.get("batch_position") for record in rows] == list(range(len(rows))) and len(rows) == len(corr["active"]), "toy active positions")
        for position, record in enumerate(rows):
            active = corr["active"][position]; provenance = record.get("provenance")
            require(record.get("target_label") == label and record.get("batch_id") == batch_id and record.get("batch_position") == position and
                    type(provenance) is dict and provenance.get("family") == "boundary" and provenance.get("block") == active[0] and
                    provenance.get("base_relator_index") == active[2] and provenance.get("translation_hex") == active[1] and
                    provenance.get("active_key") == active and provenance.get("left_translation") == "t=g*h^-1; t*h=g" and
                    provenance.get("complete_support_occurrence_accumulation") is True and
                    provenance.get("contributing_pairs") == corr["contributors"].get(f"{active[0]}:{active[1]}:{active[2]}", []), "toy source provenance")
            row = toy_row(active[0], active[2], bytes.fromhex(active[1])); row_public = public(row)
            require(record.get("sparse_row") == row_public and record.get("sparse_row_sha256") == digest(row_public) and
                    record.get("active_dual") == batch["dual"] and record.get("active_dual_sha256") == digest(batch["dual"]) and
                    record.get("dual_pairing") == pair(dual, row) and provenance.get("pre_batch_dual_pairing") == pair(dual, row), "toy row literal")
            before = len(space.pivots)
            if record.get("classification") == "retained":
                column_id = record.get("column_id"); require(column_id == len(row_by_id) + 1, "toy retained column id")
                pivot, ancestry = space.add(row, column_id); require(record.get("rank_before") == before and record.get("rank_after") == len(space.pivots) and
                    record.get("pivot_hex") == pivot.hex() and record.get("pivot_ancestry") == [[key, value] for key, value in sorted(ancestry.items())], "toy retained replay")
                row_by_id[column_id] = row; expected_columns.append(record)
            else:
                require(record.get("classification") == "dependent" and "column_id" not in record and record.get("rank_before") == before and record.get("rank_after") == before, "toy dependent classification")
                remainder, dependency = space.reduce(row); rebuilt = {}
                for column_id, coefficient in record.get("dependency_chain", []): require(column_id in row_by_id, "toy dependency id"); add(rebuilt, row_by_id[column_id], coefficient)
                require(not remainder and rebuilt == row and record.get("dependency_chain") == [[key, value] for key, value in sorted(dependency.items())], "toy dependent replay")
            decisions = {}
            for target_label, target in expected.items(): decisions[target_label] = "MEMBER_D" if not space.reduce(target)[0] else "UNRESOLVED"
            expected_transition = {"batch_id": batch_id, "batch_position": position, "classification": record["classification"], "rank_before": record["rank_before"], "rank_after": record["rank_after"], "target_reconsidered": decisions}
            require(transition_map.get((batch_id, position)) == expected_transition and log_map.get((batch_id, position)) == {"batch_id": batch_id, "batch_position": position, "decisions": decisions}, "toy target transcript")
    require(len(records) == len(transition_map) == len(log_map) == 4 and receipt.get("rank") == len(space.pivots) == 3 and
            receipt.get("columns") == expected_columns, "toy final transcript")
    for label, target in expected.items():
        item = receipt["targets"][label]; remainder, coefficients = space.reduce(target)
        if label == "u0":
            chain = [[int(key), int(value)] for key, value in sorted(coefficients.items())]; rebuilt = {}
            for column_id, coefficient in chain: add(rebuilt, row_by_id[column_id], coefficient)
            require(not remainder and item.get("decision") == "MEMBER_D" and item.get("chain") == chain and item.get("literal_boundary_sum") == public(rebuilt), "toy member target")
        else:
            terminal = item.get("terminal_dual"); expected_dual = {TOY_TARGET_V: 1}
            require(remainder and item.get("decision") == "NONMEMBER_D" and type(terminal) is dict and
                    terminal.get("row") == public(expected_dual) and terminal.get("row_sha256") == digest(public(expected_dual)) and
                    terminal.get("pairing_target") == pair(expected_dual, target) != 0 and terminal.get("annihilates_retained") is True and
                    terminal.get("full_correlation") == toy_correlation(expected_dual) and
                    terminal["full_correlation"].get("active") == [], "toy nonmember target")


def validate_toy_checkpoint(checkpoint: dict[str, Any]) -> None:
    body = dict(checkpoint); claimed = body.pop("self_digest", None)
    require(type(claimed) is str and claimed == digest(body), "toy checkpoint seal")
    require(checkpoint.get("schema") == SCHEMA + "/checkpoint" and checkpoint.get("input_identity") == {"v1": {"toy": {"path": "toy", "bytes": 1, "sha256": "0" * 64}}, "task179": {}}, "toy checkpoint identity")
    pending = checkpoint.get("pending_batch"); require(type(pending) is dict and pending.get("batch_id") == 1 and pending.get("next_position") == 2 and
        pending.get("target_label") == "u0" and pending.get("dual") == public({TOY_TARGET_U: 1}) and
        pending.get("correlation") == checkpoint["correlations"][0]["correlation"] and checkpoint.get("active_suffix") == pending["correlation"]["active"][2:], "toy checkpoint suffix")
    require(len(checkpoint.get("columns", [])) == 2 and len(checkpoint.get("batch_records", [])) == 2 and
        len(checkpoint.get("rank_transitions", [])) == 2 and len(checkpoint.get("target_reconsideration_log", [])) == 2 and
        checkpoint.get("unresolved") == ["v0"] and checkpoint.get("target_progress", {}).get("u0", {}).get("decision") == "MEMBER_D" and
        checkpoint.get("target_progress", {}).get("v0", {}).get("decision") is None, "toy checkpoint transcript")
    space = Space(); rows_by_id = {}; expected_keys = [(1, 0), (1, 1)]; expected_columns = []
    for record in sorted(checkpoint["batch_records"], key=lambda value: value["batch_position"]):
        active = checkpoint["correlations"][0]["correlation"]["active"][record["batch_position"]]; row = toy_row(active[0], active[2], bytes.fromhex(active[1]))
        position = record["batch_position"]
        require(record["batch_id"] == 1 and position in (0, 1) and record["target_label"] == "u0" and
                record["sparse_row"] == public(row) and record["sparse_row_sha256"] == digest(public(row)) and
                record["active_dual"] == public({TOY_TARGET_U: 1}) and record["active_dual_sha256"] == digest(record["active_dual"]) and
                record["dual_pairing"] == pair({TOY_TARGET_U: 1}, row) and record["provenance"]["active_key"] == active, "toy checkpoint row")
        if record["classification"] == "retained":
            cid = record["column_id"]; pivot, ancestry = space.add(row, cid); rows_by_id[cid] = row; expected_columns.append(record)
            require(record["rank_before"] == position and record["rank_after"] == position + 1 and
                    record["pivot_hex"] == pivot.hex() and record["pivot_ancestry"] == [[key, value] for key, value in sorted(ancestry.items())], "toy checkpoint pivot")
        else: raise RuntimeError("toy checkpoint prefix unexpectedly dependent")
        decisions = {"u0": "MEMBER_D", "v0": "UNRESOLVED"}
        expected_transition = {"batch_id": 1, "batch_position": position, "classification": "retained",
            "rank_before": position, "rank_after": position + 1, "target_reconsidered": decisions}
        require(checkpoint["rank_transitions"][position] == expected_transition and
                checkpoint["target_reconsideration_log"][position] == {"batch_id": 1, "batch_position": position, "decisions": decisions},
                "toy checkpoint target transcript")
    require([(record["batch_id"], record["batch_position"]) for record in checkpoint["batch_records"]] == expected_keys and
            [(record["batch_id"], record["batch_position"]) for record in checkpoint["rank_transitions"]] == expected_keys and
            [(record["batch_id"], record["batch_position"]) for record in checkpoint["target_reconsideration_log"]] == expected_keys and
            checkpoint.get("stats") == {"complete_correlation_rounds": 1, "support_occurrence_pairs_total": 4,
                "pairs_per_round": [4], "active_total": 4, "retained_total": 2, "dependent_total": 0,
                "cache_hits": 0, "cache_misses": 2, "rank_gains": [1, 2], "target_reconsiderations": 2} and
            checkpoint.get("columns") == expected_columns, "toy checkpoint transcript state")


def _toy_expected_target_progress() -> dict[str, Any]:
    result = {}
    for label, word, key, integer in (("u0", [1], TOY_TARGET_U, [1, 0]), ("v0", [2], TOY_TARGET_V, [0, 1])):
        raw = {key: 1}; target = {key: 2}; raw_public = public(raw); target_public = public(target)
        result[label] = {"word": word, "integer_exponent": integer, "normalized_residue": [0, 0],
            "A": raw_public, "A_sha256": digest(raw_public), "target": target_public,
            "target_sha256": digest(target_public),
            "direct_replay": {"word": word, "direct_key": key.hex(), "prefix": []},
            "decision": None, "chain": [], "terminal_dual": None}
    result["u0"].update({"decision": "MEMBER_D", "chain": [[1, 2]],
        "literal_boundary_sum": public({TOY_TARGET_U: 2}), "zero_residual": [],
        "zero_residual_sha256": digest([])})
    return result


def validate_toy_resource_checkpoint(checkpoint: dict[str, Any]) -> None:
    body = dict(checkpoint); claimed = body.pop("self_digest", None)
    require(set(checkpoint) == {"schema", "input_identity", "columns", "batch_records", "correlations",
                                "rank_transitions", "unresolved", "active_suffix", "pending_batch",
                                "target_progress", "stats", "target_reconsideration_log", "self_digest"} and
            type(claimed) is str and claimed == digest(body), "toy resource checkpoint seal")
    require(checkpoint.get("schema") == SCHEMA + "/checkpoint" and
            checkpoint.get("input_identity") == {"v1": {"toy": {"path": "toy", "bytes": 1, "sha256": "0" * 64}}, "task179": {}},
            "toy resource checkpoint input")
    require(checkpoint.get("pending_batch") is None and checkpoint.get("active_suffix") == [] and
            checkpoint.get("unresolved") == ["v0"] and checkpoint.get("target_progress") == _toy_expected_target_progress(),
            "toy resource checkpoint state")
    batches = checkpoint.get("correlations"); records = checkpoint.get("batch_records")
    require(type(batches) is list and len(batches) == 1 and type(records) is list and len(records) == 4,
            "toy resource checkpoint transcript size")
    batch = batches[0]; dual = toy_sparse(batch.get("dual")); expected_dual = {TOY_TARGET_U: 1}
    require(batch.get("target_label") == "u0" and dual == expected_dual and batch.get("dual") == public(expected_dual),
            "toy resource checkpoint dual")
    corr = toy_correlation(dual); require(batch.get("correlation") == corr and corr["complete"] is True and corr["sampled"] is False,
                                          "toy resource checkpoint correlation")
    rows = sorted(records, key=lambda record: int(record.get("batch_position", -1)))
    require([record.get("batch_position") for record in rows] == [0, 1, 2, 3] and
            [(record.get("batch_id"), record.get("batch_position")) for record in records] == [(1, 0), (1, 1), (1, 2), (1, 3)],
            "toy resource checkpoint positions")
    transitions = checkpoint.get("rank_transitions"); logs = checkpoint.get("target_reconsideration_log")
    require(type(transitions) is list and type(logs) is list and len(transitions) == len(logs) == len(rows),
            "toy resource checkpoint logs")
    transition_map = {(item.get("batch_id"), item.get("batch_position")): item for item in transitions}
    log_map = {(item.get("batch_id"), item.get("batch_position")): item for item in logs}
    require(len(transition_map) == 4 and len(log_map) == 4, "toy resource checkpoint log keys")
    space = Space(); row_by_id: dict[int, dict[bytes, int]] = {}; expected_columns = []
    decisions = {"u0": "MEMBER_D", "v0": "UNRESOLVED"}
    for position, record in enumerate(rows):
        active = corr["active"][position]; provenance = record.get("provenance")
        require(record.get("batch_id") == 1 and record.get("target_label") == "u0" and
                record.get("batch_position") == position and type(provenance) is dict and
                provenance.get("family") == "boundary" and provenance.get("active_key") == active and
                provenance.get("block") == active[0] and provenance.get("base_relator_index") == active[2] and
                provenance.get("translation_hex") == active[1] and
                provenance.get("left_translation") == "t=g*h^-1; t*h=g" and
                provenance.get("complete_support_occurrence_accumulation") is True and
                provenance.get("contributing_pairs") == corr["contributors"].get(f"{active[0]}:{active[1]}:{active[2]}", []),
                "toy resource checkpoint provenance")
        row = toy_row(active[0], active[2], bytes.fromhex(active[1])); row_public = public(row)
        require(record.get("sparse_row") == row_public and record.get("sparse_row_sha256") == digest(row_public) and
                record.get("active_dual") == batch["dual"] and record.get("active_dual_sha256") == digest(batch["dual"]) and
                record.get("dual_pairing") == pair(dual, row) and provenance.get("pre_batch_dual_pairing") == pair(dual, row),
                "toy resource checkpoint row")
        before = len(space.pivots)
        if record.get("classification") == "retained":
            column_id = record.get("column_id")
            require(column_id == len(row_by_id) + 1 and record.get("rank_before") == before,
                    "toy resource checkpoint retained id")
            pivot, ancestry = space.add(row, column_id)
            require(record.get("rank_after") == len(space.pivots) == before + 1 and
                    record.get("pivot_hex") == pivot.hex() and
                    record.get("pivot_ancestry") == [[key, value] for key, value in sorted(ancestry.items())],
                    "toy resource checkpoint retained replay")
            row_by_id[column_id] = row; expected_columns.append(record)
        else:
            require(record.get("classification") == "dependent" and "column_id" not in record and
                    record.get("rank_before") == record.get("rank_after") == before,
                    "toy resource checkpoint dependent class")
            remainder, dependency = space.reduce(row); rebuilt = {}
            chain = record.get("dependency_chain")
            require(type(chain) is list and all(type(item) is list and len(item) == 2 for item in chain),
                    "toy resource checkpoint dependency schema")
            for column_id, coefficient in chain:
                require(type(column_id) is int and column_id in row_by_id and type(coefficient) is int and coefficient in (1, 2),
                        "toy resource checkpoint dependency id")
                add(rebuilt, row_by_id[column_id], coefficient)
            require(not remainder and rebuilt == row and
                    chain == [[key, value] for key, value in sorted(dependency.items())],
                    "toy resource checkpoint dependent replay")
        expected_transition = {"batch_id": 1, "batch_position": position,
            "classification": record["classification"], "rank_before": record["rank_before"],
            "rank_after": record["rank_after"], "target_reconsidered": decisions}
        require(transition_map.get((1, position)) == expected_transition and
                log_map.get((1, position)) == {"batch_id": 1, "batch_position": position, "decisions": decisions},
                "toy resource checkpoint decision transcript")
        require("row_dict" not in record, "toy resource checkpoint hidden row")
    require(checkpoint.get("columns") == expected_columns and len(expected_columns) == 3 and
            checkpoint.get("rank_transitions") == [transition_map[(1, position)] for position in range(4)] and
            checkpoint.get("target_reconsideration_log") == [log_map[(1, position)] for position in range(4)] and
            checkpoint.get("stats") == {"complete_correlation_rounds": 1, "support_occurrence_pairs_total": 4,
                "pairs_per_round": [4], "active_total": 4, "retained_total": 3, "dependent_total": 1,
                "cache_hits": 0, "cache_misses": 4, "rank_gains": [1, 2, 3], "target_reconsiderations": 4},
            "toy resource checkpoint final state")


def validate_toy_resource_unknown(receipt: dict[str, Any]) -> None:
    body = dict(receipt); claimed = body.pop("self_digest", None)
    require(type(claimed) is str and claimed == digest(body) and receipt.get("schema") == SCHEMA and
            receipt.get("status") == UNKNOWN_RESOURCE and
            receipt.get("terminal") == "UNKNOWN_RESOURCE:complete_boundary_correlation:boundary_pairs:5>4" and
            receipt.get("reason") == "complete_boundary_correlation:boundary_pairs:5>4" and
            receipt.get("pins") == {"v1": auth(V1_PINS), "task179": auth(TASK179_PINS)} and
            receipt.get("claims") == {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False},
            "toy resource unknown envelope")
    resource = receipt.get("resource")
    require(type(resource) is dict and resource.get("phase") == "complete_boundary_correlation" and
            resource.get("cap") == "boundary_pairs" and resource.get("value") == 5 and resource.get("limit") == 4 and
            resource.get("terminal_cap") == "boundary_pairs" and resource.get("terminal_value") == 5 and
            resource.get("terminal_limit") == 4 and resource.get("limits") == {"wall_seconds": 100, "boundary_pairs": 4, "retained_columns": 100,
                "checkpoint_bytes": 1000000, "oracle_rounds": 100} and
            resource.get("counters", {}).get("boundary_pairs") == 5 and resource.get("counters", {}).get("retained_columns") == 3 and
            resource.get("counters", {}).get("oracle_rounds") == 2 and
            resource.get("single_process") is True and resource.get("elapsed_seconds") == 0.0 and resource.get("rss_bytes") == 0,
            "toy resource unknown fields")
    identity = receipt.get("checkpoint_identity"); checkpoint = receipt.get("checkpoint")
    require(receipt.get("checkpoint_state") == "RESUMABLE" and type(identity) is dict and set(identity) == {"path", "status", "bytes", "sha256"} and
            identity.get("path") == "embedded://task191-resource-continuation" and identity.get("status") == "PRESENT" and
            type(identity.get("bytes")) is int and identity["bytes"] >= 1 and type(identity.get("sha256")) is str and
            len(identity["sha256"]) == 64 and type(checkpoint) is dict, "toy resource unknown checkpoint identity")
    raw = canon(checkpoint) + b"\n"
    require(identity["bytes"] == len(raw) and identity["sha256"] == hashlib.sha256(raw).hexdigest(),
            "toy resource unknown checkpoint digest")
    require(resource.get("counters", {}).get("checkpoint_bytes") == identity["bytes"],
            "toy resource unknown checkpoint byte meter")
    validate_toy_resource_checkpoint(checkpoint)


def validate_toy_cap_evidence(evidence: dict[str, Any], phase: str, cap: str,
                              limit: int, minimum_value: int = 1) -> None:
    require(type(evidence) is dict and set(evidence) == {"phase", "cap", "value", "limit", "checkpoint_after"} and
            evidence.get("phase") == phase and evidence.get("cap") == cap and
            type(evidence.get("value")) is int and evidence["value"] >= minimum_value and
            evidence.get("limit") == limit and evidence["value"] > limit and
            evidence.get("checkpoint_after") == {"status": "ABSENT", "bytes": 0, "sha256": None},
            "toy resource-cap evidence")


def validate_toy_resume_contract(contract: dict[str, Any]) -> None:
    require(type(contract) is dict and set(contract) == {"mode", "resume_input", "output_checkpoint", "output_receipt", "resume_arg"} and
            contract.get("mode") == "PRODUCTION", "toy resume contract schema")
    resume = contract["resume_input"]
    for path in (resume, contract["output_checkpoint"], contract["output_receipt"]):
        require(type(path) is str and bool(path) and path[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_" and
                ".." not in path and all(char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_./-" for char in path),
                "toy resume path safety")
    require(resume != contract["output_checkpoint"] and contract["resume_arg"] == "--resume " + resume,
            "toy resume input/output binding")


def validate_selftest(receipt: dict[str, Any]) -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="ascii")); require(receipt.get("schema") == SELFTEST_SCHEMA and receipt.get("status") == "PASS" and receipt.get("terminal") == COMMON + "_SELFTEST_PASS", "selftest envelope")
    expected = fixture["expected"]; toy = receipt["toy"]
    for field in ("active_count", "retained_count", "dependent_count", "complete", "sampled", "serial_rounds", "batch_rounds", "same_span", "inside_decision", "outside_decision", "checkpoint_interrupt_resume", "resource_resume_unknown", "oracle_round_cap", "checkpoint_byte_cap", "resume_driver_contract", "interrupt_position", "continuous_transcript", "resumed_transcript", "dependent_in_resumed_suffix", "continuous_decisions", "resumed_decisions", "continuous_rank_trace", "resumed_rank_trace", "continuous_transcript_sha256", "resumed_transcript_sha256"):
        require(toy.get(field) == expected["toy"].get(field), "independent toy receipt:" + field)
    require(receipt.get("mutation_controls") == expected["mutation_controls"], "mutation control receipt")
    require(toy["active_count"] >= 4 and toy["retained_count"] >= 2 and toy["dependent_count"] >= 1 and toy["batch_rounds"] < toy["serial_rounds"] and toy["same_span"] is True, "load-bearing batch toy")
    bundle = receipt.get("production_bundle")
    require(type(bundle) is dict and type(bundle.get("continuous_receipt")) is dict and type(bundle.get("resumed_receipt")) is dict and type(bundle.get("interrupted_checkpoint")) is dict and type(bundle.get("resource_unknown")) is dict and type(bundle.get("oracle_cap")) is dict and type(bundle.get("checkpoint_byte_cap")) is dict and type(bundle.get("resume_contract")) is dict, "production-shaped selftest bundle")
    validate_toy_production(bundle["continuous_receipt"]); validate_toy_production(bundle["resumed_receipt"])
    require(bundle["continuous_receipt"] == bundle["resumed_receipt"], "production resume literal equality")
    validate_toy_checkpoint(bundle["interrupted_checkpoint"])
    validate_toy_resource_unknown(bundle["resource_unknown"])
    validate_toy_cap_evidence(bundle["oracle_cap"], "complete_boundary_correlation", "oracle_rounds", 0)
    validate_toy_cap_evidence(bundle["checkpoint_byte_cap"], "checkpoint_serialization", "checkpoint_bytes", 1)
    validate_toy_resume_contract(bundle["resume_contract"])
    require(toy["continuous_transcript"] == toy["resumed_transcript"] and toy["dependent_in_resumed_suffix"] is True and
            toy["resumed_transcript"][int(toy["interrupt_position"])] == "dependent" and
            toy["continuous_decisions"] == toy["resumed_decisions"] and toy["continuous_rank_trace"] == toy["resumed_rank_trace"] and
            toy["continuous_transcript_sha256"] == digest(toy["continuous_transcript"]) and toy["resumed_transcript_sha256"] == digest(toy["resumed_transcript"]), "checkpoint interrupt/resume replay")

def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(); p.add_argument("receipt", type=Path); p.add_argument("--selftest", action="store_true"); args = p.parse_args(argv)
    try:
        receipt = json.loads(args.receipt.read_text(encoding="ascii")); body = dict(receipt); claimed = body.pop("self_digest", None); require(type(claimed) is str and claimed == digest(body), "receipt self digest")
        if args.selftest: validate_selftest(receipt)
        elif receipt.get("status") in (UNKNOWN_RESOURCE, UNKNOWN_INPUT):
            validate_unknown(receipt)
        else: validate_prod(receipt)
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, IndexError) as exc: print(COMMON + "_CHECKER_FAIL " + str(exc)); return 1
    print(COMMON + "_CHECKER_PASS terminal=" + str(receipt.get("terminal"))); return 0
if __name__ == "__main__": raise SystemExit(main())
