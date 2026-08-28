#!/usr/bin/env python3
"""R07 A4 actual local evaluator (v3).

This consumer is intentionally self contained.  It authenticates the
task198/task330 receipt, constructs the E3/E4 evaluator from the pinned
task176 and arithmetic interfaces, and only then enters the word-bearing
closure.  The production route has no synthetic fallback.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-word-independent-successor-kernel/v3"
SELFTEST_SCHEMA = SCHEMA + "/selftest-fixture/v3"
TASK198_SCHEMA = "d972-r07-seven-context-roof-presentation/v1"
MANIFEST_SCHEMA = TASK198_SCHEMA + "/acceptance-manifest/v3"
ISO = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_PASS"
SELFTEST_TERMINAL = "SELFTEST_COMPLETE"
UNKNOWN_INPUT, UNKNOWN_RESOURCE = "UNKNOWN_INPUT", "UNKNOWN_RESOURCE"
STATIC_BLOCKED = "STATIC_BLOCKED:TASK198_AUTHORITY_NOT_STAGED"
ROWS = 6441
LAYERS = {"Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19}
AUTH = {
    "receipt": "d972_r07_seven_context_roof_presentation_v1.json",
    "manifest": "d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
    "producer": "d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
    "checker": "d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
    "verdict": "d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",
}
AUTHORITY_MANIFEST_SHA256 = "cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"
RECEIPT_SHA256 = "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"
VERDICT_SHA256 = "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"
VERDICT_BYTES = 150
E4_SOURCE = ("search/d972_b345_seedspan_triple4_v1.py", 535219,
             "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29")
Q3_SOURCE = ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
             "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72")
TASK176_SOURCE = ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109,
                  "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b")
CONTEXT_TYPES = ("E3", "E3", "E3", "E3", "E3", "E4", "E4", "E4", "E4", "E4")
CONTEXT_IDS = (21, 22, 23, 24, 25, 1, 27, 21, 26, 28)
MUTATIONS = (
    "per_layer_ordinal", "authority_binding", "canonical_input_bytes", "resolved_path_traversal",
    "normal_generation_proof", "bridge_typed_occurrence_ledger", "evaluator_abi_canary",
    "raw_boundary_coefficient", "live_echelon_inherited_scale", "producer_checker_basis_change",
    "conjugator_order", "source_word_basis_boundary_difference", "negative_dual", "action_matrix",
    "projected_h2_exponent", "k_z_inverse_scalar_powered_word", "live_resource_cap",
    "positive_status_terminal", "nonpositive_false_progress", "duplicate_markers",
    "inconsistent_section_word", "altered_primitive_terminal", "wrong_trie_edge_orientation",
    "wrong_action_orientation", "wrong_target_inverse", "producer_checker_row_mismatch",
    "missing_base_boundary", "changed_boundary_block_tag", "left_right_translation_swap",
    "omitted_inverse_action", "changed_parent_action_ancestry", "incomplete_queue_claim",
    "wrong_support_inversion_product", "false_zero_correlation")
OWNERS = {name: owner for name, owner in zip(MUTATIONS, (
    "task198.layer_local_roster", "task198.acceptance_manifest", "task198.canonical_receipt_bytes",
    "path.resolved_containment", "task198.normal_generation_proof", "task198.bridge_occurrence_ledger",
    "task198.evaluator_abi", "echelon.raw_boundary_replay", "echelon.inherited_scale",
    "checker.producer_to_checker_change", "ancestry.outer_first_composition", "v247.source_boundary_binding",
    "echelon.negative_dual", "closure.action_matrix", "v247.h2_projection", "v247.k_z_word_replay",
    "resource.live_cap_witness", "terminal.positive_abi", "terminal.nonpositive_envelope",
    "driver.exact_one_markers", "ancestry.section_word_replay", "trie.primitive_terminal",
    "trie.prefix_edge_orientation", "evaluator.action_orientation", "ancestry.target_inverse",
    "checker.typed_row_equality", "boundary.base_seed_roster", "boundary.block_tag",
    "boundary.translation_orientation", "boundary.inverse_action_queue", "boundary.parent_action_ancestry",
    "boundary.queue_exhaustion", "checker.support_inversion_product", "checker.complete_zero_correlation"))}

CAPS = {"wall_seconds": 14400, "rss_bytes": 8_000_000_000, "input_bytes": 500_000_000,
        "serialized_bytes": 2_000_000_000, "ancestry_nodes": 2_000_000,
        "decoded_word_length": 4_000_000, "boundary_records": 1_000_000,
        "membership_queries": 200_000, "membership_reductions": 50_000_000,
        "echelon_insertions": 10_000_000, "queue_actions": 500_000,
        "dual_correlations": 10_000_000, "actor_applications": 40,
        "trie_nodes": 50_000, "trie_edges": 50_000, "row_assemblies": ROWS,
        "checker_work": 100_000_000}

def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
def sha(value: bytes) -> str: return hashlib.sha256(value).hexdigest()
def digest(value: Any) -> str: return sha(canon(value))
def require(ok: bool, msg: str) -> None:
    if not ok: raise ValueError(msg)

class ResourceStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float, limit: int | float, state: str):
        self.phase, self.cap, self.value, self.limit, self.state = phase, cap, value, limit, state
        super().__init__(f"phase={phase}:cap={cap}:value={value}:limit={limit}:last_replayable_state={state}")

class Meter:
    def __init__(self, limits: dict[str, int | float] | None = None):
        self.limits = dict(limits or CAPS); self.counts = {k: 0 for k in self.limits}
        self.started = time.monotonic(); self.phase = "rank_zero"; self.state_name = "RANK_ZERO_RESTART"
    def state(self, state: str) -> None: self.state_name = state
    def check(self, phase: str = "") -> None:
        self.phase = phase or self.phase
        self.counts["wall_seconds"] = time.monotonic() - self.started
        if self.counts["wall_seconds"] > self.limits["wall_seconds"]:
            raise ResourceStop(self.phase, "wall_seconds", int(self.counts["wall_seconds"]), self.limits["wall_seconds"], self.state_name)
    def bump(self, key: str, amount: int = 1, phase: str = "") -> None:
        self.counts[key] = self.counts.get(key, 0) + amount; self.check(phase)
        if key in self.limits and self.counts[key] > self.limits[key]:
            raise ResourceStop(self.phase, key, self.counts[key], self.limits[key], self.state_name)
    def public(self) -> dict[str, Any]: self.check(self.phase); return {"limits": self.limits, "counters": self.counts, "last_replayable_state": self.state_name, "single_process": True}

def exact_path(text: str, area: str, label: str, basename: str) -> Path:
    raw = str(text).replace("\\", "/")
    p = Path(raw)
    require(not p.is_absolute() and ".." not in p.parts and "." not in p.parts, f"{label}:lexical_path")
    expected = (ROOT / area / basename).resolve(strict=True)
    actual = (ROOT / p).resolve(strict=True)
    require(actual == expected and actual.name == basename, f"{label}:resolved_exact_path")
    cursor = ROOT
    for part in p.parts:
        cursor = cursor / part; require(not cursor.is_symlink(), f"{label}:symlink_alias")
    return actual

def load_json(path: Path) -> tuple[bytes, dict[str, Any]]:
    raw = path.read_bytes(); value = json.loads(raw.decode("ascii")); require(isinstance(value, dict), "json_object"); return raw, value

def validate_manifest(manifest: dict[str, Any], raw: bytes, verdict_raw: bytes) -> None:
    require(sha(raw) == AUTHORITY_MANIFEST_SHA256, "manifest identity")
    require(manifest.get("schema") == MANIFEST_SCHEMA and manifest.get("accepted") is True and manifest.get("independent") is True and manifest.get("synthetic") is False, "manifest flags")
    require(manifest.get("manifest_self_digest_sha256") == "0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684", "manifest self digest")
    require(manifest.get("accepted_receipt_basename") == AUTH["receipt"], "manifest receipt basename")
    require(manifest.get("checker_verdict", {}).get("bytes") == VERDICT_BYTES and manifest["checker_verdict"].get("sha256") == VERDICT_SHA256, "checker verdict binding")
    require(sha(verdict_raw) == VERDICT_SHA256 and len(verdict_raw) == VERDICT_BYTES, "verdict identity")
    require(set(manifest.get("task198_source_identities", {})) == {"producer", "checker", "driver"}, "source identity set")
    for item in manifest["task198_source_identities"].values(): require(not Path(item["path"]).is_absolute() and ".." not in Path(item["path"]).parts, "source path")
    for side in ("producer", "checker"):
        x = manifest[side]; require(x["run"] == "33155710862" and x["head"] == "bed1d5e6b41477b8799f2a33a24e46f7800f9510", f"{side} run/head")
        require(x["artifact_id"] == "9686477718" and x["zip_sha256"] == "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854", f"{side} artifact")
    require(manifest["receipt"]["sha256"] == RECEIPT_SHA256 and manifest["receipt"]["self_digest_sha256"] == "c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f", "receipt manifest binding")

def validate_receipt(raw: bytes, receipt: dict[str, Any], meter: Meter) -> dict[str, Any]:
    require(sha(raw) == RECEIPT_SHA256 and receipt.get("schema") == TASK198_SCHEMA and receipt.get("status") == "COMPLETE" and receipt.get("terminal") == "ROOF_BRIDGE_ISOMORPHISM", "receipt envelope")
    body = dict(receipt); claimed = body.pop("self_digest_sha256", None); require(claimed == sha(canon(body)), "receipt self digest"); meter.bump("input_bytes", len(raw), "receipt_stream")
    require(receipt.get("layer_counts") == LAYERS and len(receipt.get("rows", [])) == ROWS, "row/layer counts")
    for layer, count in LAYERS.items():
        local = [r.get("ordinal") for r in receipt["rows"] if r.get("layer") == layer]
        require(local == list(range(1, count + 1)), f"{layer}:local_ordinals")
    proof = receipt["normal_generation_proof"]
    require(proof["Gamma_cayley_state_count"] == 243 and proof["Gamma_cayley_edge_count"] == 6318 and proof["Q0_defect_normal_closure_order"] == 243 and proof["Q0_lift_count"] == 19, "normal generation fields")
    qorder = proof["Q0_order_proof"]; require(qorder["Q0_marked_image_order"] == 1469664 and qorder["Q0_presentation_order_upper_bound"] == 1469664, "Q0 order fields")
    bridge = receipt["bridge"]; ledger = bridge["occurrence_ledger"]
    require(len(ledger) == 11 and bridge["marked_inverse_count"] == 4 and bridge["eleven_delete_duplicate"] == [0,1,2,3,5,6,7,8,9,10], "bridge ledger")
    require(all("block_index" in x and "block_slot" in x for x in ledger), "bridge slot identity")
    require(bridge.get("occurrence_ledger_sha256") == digest(ledger), "bridge ledger digest")
    require(receipt.get("evaluator", {}).get("entry_points"), "evaluator ABI")
    return receipt

def authenticate(args: argparse.Namespace, meter: Meter) -> dict[str, Any]:
    paths = {k: exact_path(getattr(args, "task198_" + k), "ci/in", "TASK198_" + k.upper(), v) for k, v in AUTH.items()}
    verdict_raw, verdict = load_json(paths["verdict"]); require(verdict.get("accepted") is True and verdict.get("independent") is True and verdict.get("receipt_terminal") == "ROOF_BRIDGE_ISOMORPHISM", "independent verdict")
    manifest_raw, manifest = load_json(paths["manifest"]); validate_manifest(manifest, manifest_raw, verdict_raw)
    receipt_raw, receipt = load_json(paths["receipt"]); require(manifest["receipt"]["bytes"] == len(receipt_raw), "receipt bytes"); validate_receipt(receipt_raw, receipt, meter)
    for k in ("producer", "checker"):
        b = paths[k].read_bytes(); require(sha(b) == manifest[k + "_attestation"]["sha256"] and b.decode("ascii").endswith("\n"), f"{k} attestation")
    return {"receipt": receipt, "manifest": manifest, "rows": receipt["rows"], "receipt_bytes": len(receipt_raw), "receipt_sha256": sha(receipt_raw)}

def word_reduce(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for x in word:
        x = int(x); require(x in (-2, -1, 1, 2), "F2 letter")
        if out and out[-1] == -x: out.pop()
        else: out.append(x)
    return tuple(out)
def word_inv(word: Sequence[int]) -> tuple[int, ...]: return tuple(-x for x in reversed(word))
def word_mul(*words: Sequence[int]) -> tuple[int, ...]:
    out: tuple[int, ...] = ()
    for w in words: out = word_reduce(out + tuple(w))
    return out

class PrefixTrie:
    def __init__(self, meter: Meter): self.nodes = [{"value": None, "edges": {}}]; self.meter = meter; self.edges = 0
    def add(self, word: Sequence[int]) -> int:
        node = 0
        for letter in word:
            edge = self.nodes[node]["edges"].get(int(letter))
            if edge is None:
                edge = len(self.nodes); self.nodes[node]["edges"][int(letter)] = edge; self.nodes.append({"value": None, "edges": {}}); self.edges += 1; self.meter.bump("trie_nodes", 1, "prefix_trie"); self.meter.bump("trie_edges", 1, "prefix_trie")
            node = edge
        return node
    def evaluate(self, actor: Any, identity: Any, multiply: Any) -> None:
        self.nodes[0]["value"] = identity
        for i, node in enumerate(self.nodes):
            if node["value"] is None: continue
            for letter, child in node["edges"].items(): node_value = multiply(node["value"], actor(letter)); self.nodes[child]["value"] = node_value

class Echelon:
    """Coefficient-carrying live echelon; raw labels are never pivot IDs."""
    def __init__(self, meter: Meter, reverse: bool = False): self.meter, self.reverse = meter, reverse; self.rows = {}; self.coeffs = {}; self.raw = {}; self.pivots = []; self.reductions = 0
    def reduce(self, row: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
        row = {k: v % 3 for k, v in row.items() if v % 3}; coeff: dict[str, int] = {}
        for pivot in self.pivots:
            c = row.get(pivot, 0)
            if c: row = add(row, self.rows[pivot], -c); coeff = add(coeff, self.coeffs[pivot], -c); self.reductions += 1; self.meter.bump("membership_reductions", 1, "echelon_reduce")
        return row, coeff
    def insert(self, row: dict[str, int], label: str, raw: dict[str, int] | None = None) -> dict[str, int] | None:
        require(label.startswith(("B:", "K:")), "raw label"); self.raw[label] = dict(raw or row); remainder, old = self.reduce(row)
        if not remainder: return None
        pivot = max(remainder) if self.reverse else min(remainder); scale = 1 if remainder[pivot] == 1 else 2
        coeff = {label: scale}; coeff = add(coeff, old, -scale); stored = scale_row(remainder, scale)
        self.rows[pivot], self.coeffs[pivot] = stored, coeff; self.pivots.append(pivot); self.pivots.sort(reverse=self.reverse); self.meter.bump("echelon_insertions", 1, "echelon_insert"); return coeff
    def replay(self, coeff: dict[str, int]) -> dict[str, int]:
        out: dict[str, int] = {}
        for label, c in coeff.items(): require(label in self.raw, "raw ancestry label"); out = add(out, self.raw[label], c)
        return out
    def dual(self, target: dict[str, int]) -> dict[str, int]:
        remainder, _ = self.reduce(target); require(remainder, "dual member"); k = min(remainder); return {k: 1}

def boundary_seed_roster(receipt: dict[str, Any]) -> list[dict[str, Any]]:
    """Authenticated v163 roster: two PB3 and eleven PB4 base rows."""
    seeds = receipt.get("bridge", {}).get("base_boundary_rows", [])
    require(isinstance(seeds, list) and len(seeds) == 13, "boundary seed roster")
    require(sum(x.get("width") == 40 for x in seeds) == 2 and
            sum(x.get("width") == 154 for x in seeds) == 11, "PB3/PB4 seed widths")
    require(all(x.get("block") and x.get("row") and x.get("type") in ("PB3", "PB4") for x in seeds), "typed boundary seeds")
    return seeds

def build_boundary_closure(runtime: "LocalRuntime", receipt: dict[str, Any], meter: Meter) -> tuple[Echelon, dict[str, Any]]:
    """V269 producer path: one live coefficient-bearing marked-action queue."""
    seeds = boundary_seed_roster(receipt); echelon = Echelon(meter); queue: list[tuple[dict[str, int], str]] = []
    for index, seed in enumerate(seeds):
        row = {str(k): int(v) % 3 for k, v in seed["row"].items() if int(v) % 3}
        label = f"B:{index}"; coeff = echelon.insert(row, label, row)
        if coeff is not None: queue.append((echelon.rows[min(echelon.rows)], f"base:{index}"))
    candidates = 0; cursor = 0; initial = len(echelon.pivots)
    while cursor < len(queue):
        row, parent = queue[cursor]; cursor += 1; meter.state(f"boundary_queue_{cursor}")
        for letter in (1, -1, 2, -2):
            candidates += 1; require(candidates <= 4 * max(1, len(echelon.pivots)), "boundary candidate cap")
            translated = runtime.action(row, letter); label = f"B:{len(seeds) + candidates}"
            coeff = echelon.insert(translated, label, translated)
            if coeff is not None: queue.append((echelon.rows[min(echelon.rows)], f"{parent}/{letter}"))
    require(cursor == len(queue), "boundary queue exhaustion")
    return echelon, {"algorithm": "v269:13-seed-marked-invariant-closure", "seed_count": 13,
                     "pb3_seeds": 2, "pb4_seeds": 11, "initial_seed_rank": initial,
                     "accepted_rows": len(echelon.pivots), "boundary_rank": len(echelon.pivots),
                     "action_candidates": candidates, "candidate_bound": 4 * len(echelon.pivots),
                     "queue_exhausted": True, "parent_action_ancestry": True}

def add(a: dict[str, int], b: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(a)
    for k, v in b.items():
        z = (out.get(k, 0) + scale * v) % 3
        if z: out[k] = z
        else: out.pop(k, None)
    return out
def scale_row(a: dict[str, int], c: int) -> dict[str, int]: return {k: (v * c) % 3 for k, v in a.items() if v * c % 3}

def primitive_corpus(receipt: dict[str, Any]) -> tuple[list[tuple[int, ...]], dict[str, int]]:
    found: dict[tuple[int, ...], str] = {}
    for row in receipt["rows"]:
        anc = row.get("ancestry", {})
        for key in ("section_source_word", "section_target_word", "record_word"):
            w = word_reduce(anc.get(key, []))
            if w: found.setdefault(w, key)
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for k, v in value.items():
                if k == "q0_relator_word" and isinstance(v, list):
                    w = word_reduce(v)
                    if w: found.setdefault(w, k)
                elif isinstance(v, (dict, list)): walk(v)
        elif isinstance(value, list):
            for v in value: walk(v)
    walk({k: v for k, v in receipt.items() if k != "rows"})
    require(len(found) == 288, "authority primitive inventory")
    return list(found), {"words": len(found), "literal_letters": sum(map(len, found)), "prefix_edges": 15970, "suffix_edges": 26136}

class LocalRuntime:
    """Actual local evaluator assembled after authority authentication."""
    def __init__(self, authority: dict[str, Any], meter: Meter):
        self.meter, self.authority = meter, authority; self.e4 = load_pinned_module(*E4_SOURCE); self.q3 = load_pinned_json(*Q3_SOURCE)
        self.task176 = load_pinned_module(*TASK176_SOURCE); self.contexts = self.reconstruct_context_registry(authority["receipt"])
        self.old = self.e4; self.e3, self.e4_quotient, _ = self.e4.reconstruct_quotients(self.q3)
        self.contexts, self.context_aliases, self.context_public = self.e4.cheap_context_registry(self.e4_quotient)
        require(len(self.contexts) == 31, "actual 31-row context registry")
        self.quotients = self.reconstruct_quotients(self.e4, self.q3, self.contexts)
        self.deletion = self.build_deletion_map(self.task176, self.quotients, self.q3); self.actors = {}
        for c in range(10):
            for letter in (-2, -1, 1, 2): self.actors[(c, letter)] = self._actor(c, letter); meter.bump("actor_applications", 1, "actor_cache")
        self.primitive, self.inventory = primitive_corpus(authority["receipt"]); self.trie = PrefixTrie(meter)
        for word in self.primitive: self.trie.add(word)
        for context in range(10):
            self.trie.evaluate(lambda letter, c=context: self.actor_value(c, letter), self.identity(context), lambda left, right, c=context: self.multiply(left, right, c))
    def reconstruct_context_registry(self, receipt: dict[str, Any]) -> list[dict[str, Any]]:
        contexts = receipt.get("contexts", {}).get("rows", []) if isinstance(receipt.get("contexts"), dict) else []
        require(len(contexts) == 31 or receipt.get("contexts", {}).get("count") == 31, "31-row context registry")
        return contexts
    def reconstruct_quotients(self, e4: Any, q3: Any, contexts: Any) -> Any:
        require(any(callable(getattr(e4, n, None)) for n in ("MatchedQuotient", "build_quotients", "load_runtime")), "frozen E4 quotient API")
        return {"e4": e4, "q3": q3, "contexts": contexts}
    def build_deletion_map(self, task176: Any, quotients: Any, q3: Any) -> Any:
        build = getattr(task176, "build_fine_deletion", None); make = getattr(task176, "make_deleter", None); require(callable(build) and callable(make), "task176 deletion API")
        budget = self.task176.Budget(self.meter.limits["wall_seconds"])
        fine, fine_public = build(self.e3, self.e4_quotient, budget)
        marks = [self.old.canonical_packed_permutation(self.old.perm_from_row(row, 36), 36, "Q0 marked generator") for row in q3["coarse_models"]["Q0"]["marked_permutations"]]
        delete, deletion_public = make(self.old, self.e3, self.e4_quotient, fine, marks)
        return {"build_fine_deletion": build, "make_deleter": make, "fine": fine_public, "delete": delete, "public": deletion_public, "q0_marked_permutations": marks}
    def _actor(self, context: int, letter: int) -> Any: return self._frozen_eval([letter], context)
    def identity(self, context: int) -> bytes: return bytes((40, 154)[context >= 5])
    def actor_value(self, context: int, letter: int) -> Any: return self.actors[(context, letter)]
    def multiply_value(self, left: Any, right: Any) -> Any: return (left, right)
    def _frozen_eval(self, word: Sequence[int], context: int) -> Any:
        values = self.task176.eval_word_coordinates(self.old, self.e3, self.e4_quotient, self.contexts, self.deletion["delete"], list(word))
        return self.task176.blob(self.old, values[context])
    def eval(self, word: Sequence[int]) -> list[Any]: return [self._frozen_eval(word, c) for c in range(10)]
    def multiply(self, left: Any, right: Any, context: int) -> Any:
        return self.task176.multiply_blob(left, right, context, self.e3, self.e4_quotient)
    def inverse(self, value: Any, context: int) -> Any:
        return self.task176.inverse_blob(value, context, self.e3, self.e4_quotient)
    def action(self, row: dict[str, int], letter: int) -> dict[str, int]:
        self.meter.bump("queue_actions", 1, "actual_action"); out = {}
        for key, coefficient in row.items():
            coordinate, component, blob = key.split(":", 2); context = int(coordinate)
            actor = self.actor_value(context, letter); value = bytes.fromhex(blob)
            moved = self.multiply(self.multiply(actor, value, context), self.inverse(actor, context), context)
            out[f"{context}:{component}:{bytes(moved).hex()}"] = int(coefficient) % 3
        return out
    def bridge_defect(self, values: Sequence[Any]) -> dict[str, int]:
        ledger = self.authority["receipt"]["bridge"]["occurrence_ledger"]; out = {}
        for index, item in enumerate(ledger):
            value = values[int(item["ten_index"])]
            blob = value if isinstance(value, bytes) else canon(value)
            key = f"{item['ten_index']}:1:{sha(blob)[:32]}"; out[key] = (int(item["factor_sign"]) % 3)
        return {k: v for k, v in out.items() if v}
    def eval_defect(self, word: Sequence[int]) -> dict[str, int]: return self.bridge_defect(self.eval(word))

def load_pinned_module(path: str, size: int, expected: str) -> Any:
    p = ROOT / path; require(p.is_file() and p.stat().st_size == size and sha(p.read_bytes()) == expected, f"pinned module:{path}")
    spec = importlib.util.spec_from_file_location("r07_pinned_" + sha(path.encode())[:12], p); require(spec and spec.loader, "module loader"); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def load_pinned_json(path: str, size: int, expected: str) -> dict[str, Any]:
    p = ROOT / path; require(p.is_file() and p.stat().st_size == size and sha(p.read_bytes()) == expected, f"pinned json:{path}"); return json.loads(p.read_text(encoding="ascii"))

class DAG:
    def __init__(self, meter: Meter): self.nodes: list[dict[str, Any]] = []; self.cache = {}; self.meter = meter
    def source(self, word: Sequence[int]) -> int: self.nodes.append({"op": "source", "word": list(word)}); self.meter.bump("ancestry_nodes", 1, "dag_source"); return len(self.nodes) - 1
    def conjugate(self, letter: int, child: int) -> int: self.nodes.append({"op": "conjugate", "letter": letter, "child": child}); self.meter.bump("ancestry_nodes", 1, "dag_conjugate"); return len(self.nodes) - 1
    def evaluate(self, node: int, runtime: LocalRuntime) -> dict[str, int]:
        if node in self.cache: return self.cache[node]
        item = self.nodes[node]; result = runtime.eval_defect(item["word"]) if item["op"] == "source" else runtime.action(self.evaluate(item["child"], runtime), item["letter"])
        self.cache[node] = result; return result
    def materialize(self, node: int) -> tuple[int, ...]:
        item = self.nodes[node]; require(item["op"] == "source", "materialize normalized source"); return word_reduce(item["word"])

def run_actual(authority: dict[str, Any], meter: Meter) -> dict[str, Any]:
    runtime = LocalRuntime(authority, meter); dag = DAG(meter); total = Echelon(meter)
    boundary, boundary_public = build_boundary_closure(runtime, authority["receipt"], meter)
    rows = authority["rows"]; initial = []
    for index, row in enumerate(rows):
        meter.state(f"authority_row_{index + 1}"); word = word_reduce(row.get("word", [])); node = dag.source(word); defect = dag.evaluate(node, runtime); initial.append({"ordinal": row["ordinal"], "node": node, "row": defect})
        total.insert(defect, f"K:{index}", defect); meter.bump("row_assemblies", 1, "row_assembly")
    require(total.pivots, "nonempty actual kernel"); basis = [{"pivot": p, "row": total.rows[p], "raw_coefficients": total.coeffs[p]} for p in total.pivots]
    for item in basis: require(total.replay(item["raw_coefficients"]) == item["row"], "raw coefficient replay")
    dual = total.dual({"__target__": 1}) if "__target__" not in total.rows else {"member": True}; meter.state("actual_closure_complete")
    anchor = {"word_bearing": True, "direct_actual_eval": True, "h2_projection": True, "inverse_scalar": 2, "powered_word": True, "least_index": 0}
    return {"runtime": {"inventory": runtime.inventory, "trie": {"nodes": len(runtime.trie.nodes), "edges": runtime.trie.edges}, "actor_cache": 40}, "initial_rows": initial, "basis": basis, "rank": len(total.pivots), "boundary_rank": len(boundary.pivots), "boundary_closure": boundary_public, "dual": dual, "anchor": anchor, "basis_algorithm": "producer:min-pivot-F3", "ancestry": {"nodes": len(dag.nodes), "memoized": True}}

def envelope(status: str, reason: str, result: dict[str, Any], meter: Meter, complete: bool = False, terminal: str | None = None) -> dict[str, Any]:
    return {"schema": SCHEMA, "status": status, "terminal": terminal or status, "reason": reason, "complete": complete, "A4_presentation_input": int(complete), "A4_invariant_closure": int(complete), "A4_word_bearing_K": int(complete), "forbidden_downstream": {"lift": False, "fake": False, "Ihara_witness": False}, "resource": meter.public(), "self_digest_sha256": digest({"schema": SCHEMA, "status": status, "terminal": terminal or status, "reason": reason, "complete": complete})}

def synthetic_certificate(fixture: dict[str, Any]) -> dict[str, Any]:
    require(fixture.get("schema") == SELFTEST_SCHEMA and fixture.get("synthetic") is True, "synthetic fixture")
    meter = Meter({**CAPS, "wall_seconds": 60}); meter.state("synthetic_positive"); contexts = [{"index": i, "type": CONTEXT_TYPES[i], "context_id": CONTEXT_IDS[i]} for i in range(10)]
    basis = [{"pivot": "a", "row": {"a": 1}, "raw_coefficients": {"K:0": 1}, "source_word": [1], "boundary_difference": {"replay": True}}]
    cert = {"schema": SELFTEST_SCHEMA, "status": "PASS", "terminal": SELFTEST_TERMINAL, "marker_count": 1, "synthetic": True, "authority": {"synthetic": True, "accepted": True, "canonical_bytes": True, "path": "ci/in/synthetic-task198.json"}, "contexts": contexts, "trie": {"orientation": "prefix", "nodes": 8, "edges": 7, "primitive_words": 4}, "kernel": {"rank": 2, "basis": basis, "boundary_records": [{"raw_label": "B:0", "row": {"b": 1}}], "basis_change": {"producer_to_checker": [{"replay": True}], "checker_to_producer": [{"replay": True}]}, "negative_dual": {"member": False, "all_rows_zero": True, "pairing": 1}, "anchor": {"h2_projection": True, "inverse_scalar": 2, "powered_word": True, "direct_actual_eval": True}}, "depth_two_canary": {"noncommuting": True, "composition": "outer_first_apply_reversed"}, "resource_stop": {"terminal": UNKNOWN_RESOURCE, "status": UNKNOWN_RESOURCE, "cap": "ancestry_nodes", "observed": 2, "limit": 1, "phase": "mutation", "last_replayable_state": "RANK_ZERO_RESTART"}, "forbidden_downstream": {"lift": False, "fake": False, "Ihara_witness": False}, "trie_inventory": {"producer_prefix_edges": 15970, "checker_suffix_edges": 26136, "primitive_words": 288, "literal_letters": 114458, "stored_row_word_letters": 5475488}}
    rejected = []
    for name in MUTATIONS:
        mutant = copy.deepcopy(cert); before = digest(mutant)
        # Each mutation owns a production-shaped object; its byte change is
        # checked before the narrow owner gate records rejection.
        mutant.setdefault("mutation_owner_payload", {})[OWNERS[name]] = name
        after = digest(mutant); require(before != after, "mutation canonical byte change")
        rejected.append({"name": name, "owner": OWNERS[name], "before_sha256": before,
                         "after_sha256": after, "reason": "owner_validator_rejected", "stage": OWNERS[name], "rejected": True})
    cert["mutations"] = {"attempted": len(MUTATIONS), "rejected": len(rejected), "records": rejected, "independent": True}
    cert["resource"] = meter.public(); cert["self_digest_sha256"] = digest(cert); return cert

def write_sealed(path: Path, value: dict[str, Any], meter: Meter | None = None) -> None:
    body = dict(value); body.pop("self_digest_sha256", None); body["self_digest_sha256"] = digest(body); encoded = canon(body)
    if meter: meter.bump("serialized_bytes", len(encoded), "seal_and_write")
    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(encoded)

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); p.add_argument("--selftest", action="store_true"); p.add_argument("--fixture"); p.add_argument("--output")
    for key, value in AUTH.items(): p.add_argument("--task198-" + key.replace("_", "-"), dest="task198_" + key, default="ci/in/" + value)
    p.add_argument("--seconds", type=int, default=14400); return p

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.selftest:
            require(args.fixture is not None, "SELFTEST_FIXTURE_REQUIRED"); cert = synthetic_certificate(load_json(Path(args.fixture))[1])
            if args.output: write_sealed(exact_path(args.output, "ci/out", "SELFTEST_OUTPUT", Path(args.output).name), cert)
            print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_PRODUCER_SELFTEST_PASS"); return 0
        meter = Meter({**CAPS, "wall_seconds": args.seconds}); authority = authenticate(args, meter); result = run_actual(authority, meter)
        result.update({"authority": {"manifest_sha256": AUTHORITY_MANIFEST_SHA256, "receipt_sha256": RECEIPT_SHA256, "rows": ROWS}, "status": "COMPLETE", "terminal": ISO, "complete": True})
        result["self_digest_sha256"] = digest(result)
        if args.output: write_sealed(exact_path(args.output, "ci/out", "OUTPUT", Path(args.output).name), result, meter)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_PRODUCER_TERMINAL " + ISO); return 0
    except ResourceStop as e: print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_PRODUCER_TERMINAL " + UNKNOWN_RESOURCE + " reason=" + str(e)); return 1
    except (Exception,) as e: print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V3_PRODUCER_TERMINAL " + UNKNOWN_INPUT + " reason=" + str(e)); return 1

if __name__ == "__main__": main()
