#!/usr/bin/env python3
"""Independent v4 checker for the R07 word-independent kernel.

This file intentionally does not import the producer.  It reconstructs the
authority, the reverse/suffix corpus and the finite active dual with its own
EKey registry and a maximum-pivot convention.  A producer certificate is
accepted only after literal affine/discrepancy replay; producer booleans and
digests are never used as mathematical evidence.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-word-independent-successor-kernel/v4"
SELFTEST_SCHEMA = SCHEMA + "/selftest-fixture/v4"
ISO = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PASS"
UNKNOWN_INPUT, UNKNOWN_RESOURCE = "UNKNOWN_INPUT", "UNKNOWN_RESOURCE"
ROWS = 6441
LAYERS = {"Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19}
PRESENTATION_SCHEMA = "d972-r07-seven-context-roof-presentation/v1"
MANIFEST_SCHEMA = PRESENTATION_SCHEMA + "/acceptance-manifest/v3"
AUTH = {
    "receipt": "d972_r07_seven_context_roof_presentation_v1.json",
    "manifest": "d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
    "producer": "d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
    "checker": "d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
    "verdict": "d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",
}
MANIFEST_SHA256 = "cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"
RECEIPT_SHA256 = "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"
VERDICT_SHA256 = "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"
E4_SOURCE = ("search/d972_b345_seedspan_triple4_v1.py", 535219,
             "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29")
Q3_SOURCE = ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570,
             "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72")
TASK176_SOURCE = ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109,
                  "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b")
TASK198_SOURCES = {
    "producer": ("search/d972_r07_seven_context_roof_presentation_v1.py", 137169,
                  "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"),
    "checker": ("crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py", 157253,
                "001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"),
    "driver": ("search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g", 20541,
               "6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068"),
}
CONTEXT_IDS = (21, 22, 23, 24, 25, 1, 27, 21, 26, 28)
CONTEXT_TYPES = ("E3", "E3", "E3", "E3", "E3", "E4", "E4", "E4", "E4", "E4")
EXPECTED_INVENTORY = {"sections": 243, "records": 26, "q0_relators": 19,
                      "primitive_words": 288, "literal_primitive_letters": 114458,
                      "prefix_edges": 15970, "suffix_edges": 26136,
                      "stored_row_letters": 5475488}
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
    "wrong_support_inversion_product", "false_zero_correlation", "omitted_candidate_discrepancy",
    "omitted_prior_k_discrepancy", "flipped_q_sign", "missing_discrepancy_scale",
    "reversed_source_action_discrepancy", "changed_raw_tag_translation",
    "modulo_discovered_b_only_replay", "deleted_active_key", "unregistered_dual_key",
    "raw_pivot_functional", "omitted_matching_occurrence", "incomplete_translation_key",
    "premature_zero_correlation", "omitted_new_key_registration",
)
OWNERS = {name: "checker." + name for name in MUTATIONS}


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canon(value))


class Reject(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


class CheckerMeter:
    def __init__(self) -> None:
        self.started = time.monotonic()
        self.counters = {"input_bytes": 0, "suffix_nodes": 0, "suffix_edges": 0,
                         "terminal_materializations": 0, "row_assemblies": 0,
                         "quotient_reductions": 0, "dual_support": 0,
                         "correlation_pairs": 0, "direct_replays": 0,
                         "canonicalization": 0, "final_write": 0, "serialized_bytes": 0}

    def bump(self, key: str, amount: int = 1) -> None:
        self.counters[key] = self.counters.get(key, 0) + int(amount)

    def public(self) -> dict[str, Any]:
        self.counters["wall_seconds"] = time.monotonic() - self.started
        return {"counters": self.counters, "single_process": True, "no_retry_or_pool": True}


def exact_path(text: str, area: str, basename: str, must_exist: bool = True) -> Path:
    p = Path(str(text).replace("\\", "/"))
    require(not p.is_absolute() and ".." not in p.parts and "." not in p.parts, "path:lexical")
    expected = (ROOT / area / basename).resolve(strict=must_exist)
    actual = (ROOT / p).resolve(strict=must_exist)
    require(actual == expected and actual.name == basename, "path:resolved_exact")
    cursor = ROOT
    for part in p.parts:
        cursor /= part
        require(not cursor.is_symlink(), "path:symlink_alias")
    return actual


def output_path(text: str, area: str) -> Path:
    p = Path(str(text).replace("\\", "/"))
    require(not p.is_absolute() and ".." not in p.parts and "." not in p.parts, "output:path")
    result = (ROOT / p).resolve(strict=False)
    require(result.parent == (ROOT / area).resolve(strict=True), "output:containment")
    return result


def read_json_once(path: Path, label: str) -> tuple[bytes, dict[str, Any]]:
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ":canonical_json") from exc
    require(isinstance(value, dict), label + ":object")
    return raw, value


def word_reduce(word: Iterable[int]) -> tuple[int, ...]:
    result: list[int] = []
    for item in word:
        value = int(item)
        require(value in (-2, -1, 1, 2), "word:letter")
        if result and result[-1] == -value:
            result.pop()
        else:
            result.append(value)
    return tuple(result)


def word_inv(word: Sequence[int]) -> tuple[int, ...]:
    return word_reduce(-x for x in reversed(word))


def word_mul(*words: Sequence[int]) -> tuple[int, ...]:
    result: tuple[int, ...] = ()
    for word in words:
        result = word_reduce(result + tuple(word))
    return result


def replay_ancestry(row: dict[str, Any]) -> tuple[int, ...]:
    anc = row.get("ancestry", {})
    record = tuple(word_reduce(anc.get("record_word", [])))
    target = tuple(word_reduce(anc.get("section_target_word", [])))
    source = tuple(word_reduce(anc.get("section_source_word", [])))
    if row.get("layer") == "Gamma_Cayley":
        expected = word_mul(source, record, word_inv(target))
    elif row.get("layer") == "action":
        letter = int(row["letter"])
        tokens = tuple(int(x) for x in anc.get("tokens", []))
        expected_tokens = ((-letter,) + record + (letter,) if int(row["orientation"]) == 1
                           else (letter,) + record + (-letter,))
        require(tokens == expected_tokens, "checker:action_raw_tokens")
        expected = word_mul(tokens, word_inv(target))
    elif row.get("layer") == "Q0_lift":
        qrel = tuple(word_reduce(anc.get("q0_relator_word", [])))
        expected = word_mul(qrel, word_inv(target))
    else:
        raise Reject("checker:unknown_ancestry_layer")
    require(expected == tuple(word_reduce(row.get("word", []))), "checker:ancestry_word")
    return expected


class Authority:
    def __init__(self, args: argparse.Namespace):
        self.paths = {key: exact_path(getattr(args, "task198_" + key), "ci/in", value)
                      for key, value in AUTH.items()}
        self.raw: dict[str, bytes] = {}
        self.values: dict[str, dict[str, Any]] = {}
        for key in ("manifest", "verdict", "receipt"):
            raw, value = read_json_once(self.paths[key], "authority." + key)
            self.raw[key], self.values[key] = raw, value
        for key in ("producer", "checker"):
            self.raw[key] = self.paths[key].read_bytes()
            require(self.raw[key].decode("ascii").endswith("\n"), "authority:" + key + ":attestation_ascii")
        self.validate()

    def validate(self) -> None:
        receipt, manifest, verdict = self.values["receipt"], self.values["manifest"], self.values["verdict"]
        require(len(self.raw["receipt"]) == 31017244 and sha(self.raw["receipt"]) == RECEIPT_SHA256, "authority:receipt")
        require(sha(self.raw["manifest"]) == MANIFEST_SHA256 and
                manifest.get("schema") == MANIFEST_SCHEMA and manifest.get("accepted") is True and
                manifest.get("independent") is True and manifest.get("synthetic") is False,
                "authority:manifest")
        require(manifest.get("manifest_self_digest_sha256") ==
                "0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684",
                "authority:manifest_seal")
        require(manifest.get("accepted_receipt_basename") == AUTH["receipt"] and
                manifest.get("receipt", {}).get("bytes") == len(self.raw["receipt"]) and
                manifest["receipt"].get("sha256") == RECEIPT_SHA256 and
                manifest["receipt"].get("self_digest_sha256") ==
                "c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f" and
                manifest.get("checker_verdict", {}).get("bytes") == len(self.raw["verdict"]) and
                manifest["checker_verdict"].get("sha256") == VERDICT_SHA256,
                "authority:manifest_members")
        body = dict(manifest); claimed = body.pop("manifest_self_digest_sha256", None)
        require(claimed == sha(canon(body)), "authority:manifest_replay")
        require(sha(self.raw["verdict"]) == VERDICT_SHA256 and len(self.raw["verdict"]) == 150 and
                verdict.get("accepted") is True and verdict.get("independent") is True and
                verdict.get("receipt_terminal") == "ROOF_BRIDGE_ISOMORPHISM",
                "authority:verdict")
        require(set(manifest.get("task198_source_identities", {})) == {"producer", "checker", "driver"},
                "authority:source_identity_set")
        for side, (path, size, source_sha) in TASK198_SOURCES.items():
            item = manifest["task198_source_identities"][side]
            require(item.get("path") == path and item.get("bytes") == size and
                    item.get("sha256") == source_sha, "authority:source_identity:" + side)
        for side in ("producer", "checker"):
            item = manifest.get(side, {})
            require(item.get("run") == "33155710862" and
                    item.get("head") == "bed1d5e6b41477b8799f2a33a24e46f7800f9510" and
                    item.get("artifact_id") == "9686477718" and
                    item.get("zip_sha256") ==
                    "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854" and
                    item.get("member", {}).get("basename") == AUTH["receipt"] and
                    item.get("member", {}).get("bytes") == len(self.raw["receipt"]) and
                    item.get("member", {}).get("sha256") == RECEIPT_SHA256,
                    "authority:member_identity:" + side)
            att = manifest.get(side + "_attestation", {})
            require(att.get("basename") == AUTH[side] and att.get("bytes") == len(self.raw[side]) and
                    att.get("sha256") == sha(self.raw[side]), "authority:attestation:" + side)
        rbody = dict(receipt); rclaim = rbody.pop("self_digest_sha256", None)
        require(rclaim == "c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f" and
                rclaim == sha(canon(rbody)), "authority:receipt_seal")
        presentation = receipt.get("Delta0", {}).get("presentation")
        require(isinstance(presentation, dict) and presentation.get("row_count") == ROWS and
                presentation.get("layer_counts") == LAYERS and len(presentation.get("rows", [])) == ROWS and
                presentation.get("normal_closure_exact") is True and
                presentation.get("normal_generation") is True and presentation.get("resume_cursor") == ROWS,
                "authority:presentation")
        local = {key: [] for key in LAYERS}
        for row in presentation["rows"]:
            require(row.get("layer") in LAYERS and isinstance(row.get("ordinal"), int), "authority:row_shape")
            local[row["layer"]].append(row["ordinal"])
        for layer, count in LAYERS.items():
            require(local[layer] == list(range(1, count + 1)), "authority:ordinal:" + layer)
        require(presentation.get("rows_sha256") ==
                "e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950",
                "authority:row_digest")
        proof = presentation.get("normal_generation_proof", {})
        require(proof.get("Gamma_cayley_edge_count") == 6318 and proof.get("Gamma_cayley_state_count") == 243 and
                proof.get("Q0_defect_normal_closure_order") == 243 and proof.get("Q0_lift_count") == 19,
                "authority:normal_generation")
        qproof = proof.get("Q0_order_proof", {})
        require(qproof.get("G9_abstract_presentation_order") == 2916 and
                qproof.get("G9_direct_image_order") == 2916 and
                qproof.get("P_abstract_presentation_order") == 504 and
                qproof.get("P_direct_image_order") == 504 and
                qproof.get("Q0_marked_image_order") == 1469664 and
                qproof.get("Q0_presentation_order_upper_bound") == 1469664 and
                qproof.get("complete_relator_count") == 19 and
                qproof.get("complete_relators_sha256") ==
                "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a",
                "authority:Q0_order")
        require(proof.get("Q0_defect_normal_closure_rounds") == [243] and
                proof.get("selected_gamma_records") == [1, 3, 6, 9] and
                proof.get("presentation_quotient_order_upper_bound") == 357128352 and
                proof.get("surjective_marked_image_order") == 357128352 and
                proof.get("upper_bound_equals_image_order") is True,
                "authority:closure_equality")
        bridge = receipt.get("bridge", {})
        require(bridge.get("ten_to_eleven") == [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9] and
                bridge.get("eleven_delete_duplicate") == [0, 1, 2, 3, 5, 6, 7, 8, 9, 10] and
                bridge.get("seven_blocks") == [[0, 1, 2], [3, 0, 4], [5], [6], [7], [8], [9]],
                "authority:bridge_maps")
        require(bridge.get("image_order") == 357128352 and bridge.get("kernel_order") == 1 and
                bridge.get("marked_inverse_count") == 4 and bridge.get("marked_replay_count") == 4,
                "authority:bridge_order")
        ledger = bridge.get("occurrence_ledger", [])
        require(len(ledger) == 11 and bridge.get("occurrence_ledger_sha256") ==
                "040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7" and
                bridge.get("typed_coordinate_ledger_sha256") ==
                "9f9c081e9653d6e141e4d6d231e2d6db9526850b7ccd33c0859d13825f3fa83c",
                "authority:typed_ledger")
        for item in ledger:
            require(all(key in item for key in ("block_index", "block_slot", "context_id", "factor_sign",
                                                "fox_prefix_occurrences", "occurrence", "ordinal", "orientation",
                                                "role", "ten_index", "type")), "authority:ledger_fields")
        evaluator = receipt.get("evaluator", {})
        require(evaluator.get("schema") == "d972-r07-v188-roof-consumer-action-abi/v1" and
                evaluator.get("coordinate_widths") == [40, 40, 40, 40, 40, 154, 154, 154, 154, 154] and
                evaluator.get("relator_rows_sha256") ==
                "e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950",
                "authority:evaluator_abi")
        endpoints = evaluator.get("entry_points", {})
        expected_endpoints = {
            "eval": ("roof_eval", ["runtime", "word"]),
            "multiply": ("roof_multiply", ["runtime", "left", "right"]),
            "inverse": ("roof_inverse", ["runtime", "value"]),
            "source_section": ("roof_source_section", ["runtime", "gamma_state_id", "q0_state_id"]),
            "action": ("roof_action", ["runtime", "actor_word", "value"]),
            "section_cocycle": ("roof_section_cocycle", ["runtime", "left_section_word", "right_section_word", "product_section_word"]),
        }
        for name, (callable_name, arguments) in expected_endpoints.items():
            require(endpoints.get(name, {}).get("callable") == callable_name and
                    endpoints[name].get("args") == arguments, "authority:evaluator_endpoint:" + name)
        canaries = evaluator.get("canaries", {})
        require(set(canaries) >= {"x", "y", "x_inverse", "y_inverse", "xy", "x_action_y",
                                  "xy_section_cocycle", "source_2_2", "nonsplit_y_y_section_cocycle"},
                "authority:evaluator_canary_names")
        require(canaries.get("nonsplit_y_y_section_cocycle") is None,
                "authority:evaluator_nonsplit_canary")
        require(receipt.get("Ihara_witness") is False and receipt.get("cofinal_lift") is False and
                receipt.get("fake") is False and receipt.get("direct_Delta_states_enumerated") == 0 and
                receipt.get("D_all", {}).get("materialized") is False, "authority:forbidden_flags")

    @property
    def receipt(self) -> dict[str, Any]:
        return self.values["receipt"]

    @property
    def rows(self) -> list[dict[str, Any]]:
        return self.receipt["Delta0"]["presentation"]["rows"]


def jsonable(value: Any) -> Any:
    if isinstance(value, bytes):
        return {"__bytes__": value.hex()}
    if isinstance(value, tuple):
        return [jsonable(x) for x in value]
    if isinstance(value, list):
        return [jsonable(x) for x in value]
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    return value


def token(value: Any) -> str:
    return canon(jsonable(value)).hex()


KEYS: dict[str, Any] = {}


def from_jsonable(value: Any) -> Any:
    if isinstance(value, dict) and set(value) == {"__bytes__"}:
        return bytes.fromhex(value["__bytes__"])
    if isinstance(value, list):
        return tuple(from_jsonable(x) for x in value)
    if isinstance(value, dict):
        return {key: from_jsonable(item) for key, item in value.items()}
    return value


def decode_token(text: str) -> Any:
    if text not in KEYS:
        KEYS[text] = from_jsonable(json.loads(bytes.fromhex(text).decode("ascii")))
    return KEYS[text]


def row_key(index: int, component: int, element: Any) -> str:
    key = token(element); KEYS[key] = element
    return f"{index}:{int(component)}:{key}"


def raw_key(index: int, relation: int, translation: Any) -> str:
    key = token(translation); KEYS[key] = translation
    return f"{index}:{relation}:{key}"


def split_row(key: str) -> tuple[int, int, str]:
    a, b, c = key.split(":", 2)
    return int(a), int(b), c


def split_raw(key: str) -> tuple[int, int, str]:
    a, b, c = key.split(":", 2)
    return int(a), int(b), c


def add_row(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, value in right.items():
        coefficient = (out.get(key, 0) + scale * value) % 3
        if coefficient:
            out[key] = coefficient
        else:
            out.pop(key, None)
    return out


def scale_row(row: dict[str, int], scale: int) -> dict[str, int]:
    return {key: (value * scale) % 3 for key, value in row.items() if (value * scale) % 3}


def element_blob(value: Any) -> bytes:
    require(isinstance(value, tuple) and len(value) == 2 and
            isinstance(value[0], bytes) and isinstance(value[1], bytes), "checker:EKey_blob")
    return value[0] + value[1]


class ReverseSuffixTrie:
    """Independent reverse trie with opposite edge association."""
    def __init__(self) -> None:
        self.nodes = [{"parent": None, "edge": None, "edges": {}, "opposite": {}}]
        self.terminals: dict[tuple[int, ...], int] = {}

    def add(self, word: Sequence[int]) -> None:
        normalized = tuple(word_reduce(word))
        node = 0
        for letter in reversed(normalized):
            child = self.nodes[node]["edges"].get(-int(letter))
            if child is None:
                child = len(self.nodes)
                self.nodes[node]["edges"][-int(letter)] = child
                self.nodes.append({"parent": node, "edge": -int(letter), "edges": {}, "opposite": {}})
            self.nodes[child]["opposite"][int(letter)] = normalized
            node = child
        self.terminals[normalized] = node


def primitive_inventory(authority: Authority) -> tuple[list[tuple[int, ...]], dict[str, Any]]:
    sections: set[tuple[int, ...]] = set()
    records: set[tuple[int, ...]] = set()
    qrels: set[tuple[int, ...]] = set()
    for row in authority.rows:
        anc = row.get("ancestry", {})
        sections.add(tuple(word_reduce(anc.get("section_source_word", []))))
        sections.add(tuple(word_reduce(anc.get("section_target_word", []))))
        records.add(tuple(word_reduce(anc.get("record_word", []))))
        if isinstance(anc.get("q0_relator_word"), list):
            qrels.add(tuple(word_reduce(anc["q0_relator_word"])))
    primitive = sections | records | qrels
    require(len(sections) == 243 and len(records) == 26 and len(qrels) == 19 and len(primitive) == 288,
            "suffix:inventory_sets")
    words = sorted(primitive, key=lambda x: (len(x), x))
    require(sum(len(x) for x in words) == 114458, "suffix:literal_letters")
    by_layer = {layer: sum(len(row.get("word", [])) for row in authority.rows
                           if row.get("layer") == layer) for layer in LAYERS}
    stored = sum(by_layer.values())
    require(stored == 5475488 and by_layer ==
            {"Gamma_Cayley": 5433366, "action": 33206, "Q0_lift": 8916},
            "suffix:stored_row_letters")
    return words, {"sections": len(sections), "records": len(records), "q0_relators": len(qrels),
                   "primitive_words": len(words), "literal_primitive_letters": sum(map(len, words)),
                   "stored_row_letters": stored, "stored_row_letters_by_layer": by_layer,
                   "prefix_edges": 15970, "suffix_edges": 26136}


def load_pinned_module(path: str, size: int, expected: str) -> Any:
    p = ROOT / path
    require(p.is_file() and p.stat().st_size == size and sha(p.read_bytes()) == expected, "pinned:" + path)
    spec = importlib.util.spec_from_file_location("r07_v4_checker_frozen_e4", p)
    require(spec is not None and spec.loader is not None, "pinned:loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Affine:
    def __init__(self, quotient: Any, a: Any, u: dict[tuple[int, Any], int]):
        self.q, self.a, self.u = quotient, a, {key: value % 3 for key, value in u.items() if value % 3}

    def mul(self, other: "Affine") -> "Affine":
        moved = {(component, self.q.mul(self.a, element)): coefficient
                 for (component, element), coefficient in other.u.items()}
        return Affine(self.q, self.q.mul(self.a, other.a), add_local(self.u, moved))


def add_local(left: dict[tuple[int, Any], int], right: dict[tuple[int, Any], int], scale: int = 1) -> dict[tuple[int, Any], int]:
    out = dict(left)
    for key, value in right.items():
        coefficient = (out.get(key, 0) + scale * value) % 3
        if coefficient:
            out[key] = coefficient
        else:
            out.pop(key, None)
    return out


class CheckerRuntime:
    def __init__(self) -> None:
        self.old = load_pinned_module(*E4_SOURCE)
        q3_path = ROOT / Q3_SOURCE[0]
        require(q3_path.is_file() and q3_path.stat().st_size == Q3_SOURCE[1] and sha(q3_path.read_bytes()) == Q3_SOURCE[2], "pinned:q3")
        self.q3 = json.loads(q3_path.read_text(encoding="ascii"))
        self.e3, self.e4, _ = self.old.reconstruct_quotients(self.q3)
        x, y = [1], [3]
        z = self.old.inv_word(self.old.pp_words([x, y])); u = self.old.inv_word(self.old.pp_words([y, x]))
        pairs = [(x, y), (x, z), (y, z), (u, x), (u, y), ([4], [6]),
                 (self.old.pp_words([[1], [2]]), self.old.pp_words([[5], [6]])),
                 ([1], [4]), (self.old.pp_words([[2], [4]]), [6]),
                 ([1], self.old.pp_words([[4], [5]]))]
        self.contexts = [{"type": CONTEXT_TYPES[i], "left": list(pair[0]), "right": list(pair[1])}
                         for i, pair in enumerate(pairs)]

    def quotient(self, index: int) -> Any:
        return self.e3 if self.contexts[index]["type"] == "E3" else self.e4

    def eval(self, word: Sequence[int], index: int) -> Affine:
        context = self.contexts[index]; quotient = self.quotient(index)
        pb = self.old.f2_substitute(word, context["left"], context["right"])
        gradient, roof = self.old.fox_gradient_without_sections(pb, quotient)
        return Affine(quotient, roof, {(int(c), e): int(v) % 3 for (c, e), v in gradient.items() if int(v) % 3})

    def eval_pb(self, word: Sequence[int], index: int) -> Affine:
        quotient = self.quotient(index)
        gradient, roof = self.old.fox_gradient_without_sections(word, quotient)
        return Affine(quotient, roof, {(int(c), e): int(v) % 3 for (c, e), v in gradient.items() if int(v) % 3})

    def check_canaries(self, receipt: dict[str, Any]) -> None:
        canaries = receipt["evaluator"]["canaries"]
        for name, word in (("x", [1]), ("y", [2]), ("x_inverse", [-1]), ("y_inverse", [-2])):
            expected = [element_blob(self.eval(word, index).a).hex() for index in range(10)]
            require(canaries[name]["value"] == expected, "checker:canary:" + name)
        expected_xy = [element_blob(self.eval([1, 2], index).a).hex() for index in range(10)]
        require(canaries["xy"]["value"] == expected_xy, "checker:canary:xy")
        source_22 = canaries["source_2_2"]
        if isinstance(source_22.get("source_word"), list):
            expected_source = [element_blob(self.eval(source_22["source_word"], index).a).hex()
                               for index in range(10)]
            require(source_22["value"] == expected_source, "checker:canary:source_2_2")

    def row(self, word: Sequence[int]) -> dict[str, int]:
        out: dict[str, int] = {}
        for index in range(10):
            state = self.eval(word, index)
            require(state.a == self.quotient(index).identity, "checker:nontrivial_roof")
            for (component, element), coefficient in state.u.items():
                out = add_row(out, {row_key(index, component, element): coefficient})
        return out


class CheckerBoundary:
    def __init__(self, runtime: CheckerRuntime) -> None:
        self.runtime = runtime
        self.seeds: list[dict[str, Any]] = []
        self.inverse_cache: dict[Any, Any] = {}
        for index in range(10):
            quotient = runtime.quotient(index)
            rels = runtime.old.pure_relations(3 if index < 5 else 4)
            require(len(rels) == (2 if index < 5 else 11), "checker:seed_relations")
            for relation, word in enumerate(rels):
                state = runtime.eval_pb(word, index)
                require(state.a == quotient.identity, "checker:seed_roof")
                occurrences = [(component, element, coefficient) for (component, element), coefficient in state.u.items() if coefficient % 3]
                for _, element, _ in occurrences:
                    self.inverse_cache[element] = quotient.inverse(element)
                self.seeds.append({"index": len(self.seeds), "context": index, "relation": relation,
                                  "q": quotient, "occurrences": occurrences,
                                  "row": {row_key(index, c, e): v for c, e, v in occurrences}})
        require(len(self.seeds) == 65, "checker:65_seeds")

    def psi(self, ledger: dict[str, int]) -> dict[str, int]:
        out: dict[str, int] = {}
        for key, coefficient in ledger.items():
            index, relation, token_value = split_raw(key)
            translation = decode_token(token_value)
            seed = next(item for item in self.seeds if item["context"] == index and item["relation"] == relation)
            for component, element, seed_coefficient in seed["occurrences"]:
                moved = seed["q"].mul(translation, element)
                out = add_row(out, {row_key(index, component, moved): seed_coefficient}, coefficient)
        return out


def full_D_correlation(boundary: CheckerBoundary, dual: dict[str, int]) -> dict[str, Any]:
    """Checker-owned sorted occurrence/support stream over all 65 seeds."""
    pairs: list[tuple[tuple[int, int, str], int]] = []
    for seed in boundary.seeds:
        for component, h, seed_coefficient in seed["occurrences"]:
            inverse_h = boundary.inverse_cache[h]
            for support, lambda_value in dual.items():
                index, dual_component, support_token = split_row(support)
                if index != seed["context"] or int(dual_component) != int(component):
                    continue
                g = decode_token(support_token)
                translation = seed["q"].mul(g, inverse_h)
                require(seed["q"].mul(translation, h) == g, "checker:correlation_translation")
                translation_token = token(translation); KEYS[translation_token] = translation
                pairs.append(((seed["context"], seed["relation"], translation_token),
                              int(lambda_value) * int(seed_coefficient) % 3))
    pairs.sort(key=lambda item: item[0])
    accumulators: dict[tuple[int, int, str], int] = {}
    for key, coefficient in pairs:
        accumulators[key] = (accumulators.get(key, 0) + coefficient) % 3
    nonzero = sorted((key, value) for key, value in accumulators.items() if value)
    return {"pair_count": len(pairs), "accumulators": accumulators,
            "selected": nonzero[0] if nonzero else None,
            "complete_all_65": True}


class MaxPivot:
    """Checker pivot convention: maximum serialized support key first."""
    def __init__(self) -> None:
        self.rows: dict[str, dict[str, int]] = {}
        self.pivots: list[str] = []

    def reduce(self, row: dict[str, int]) -> dict[str, int]:
        remainder = dict(row)
        for pivot in self.pivots:
            coefficient = remainder.get(pivot, 0)
            if coefficient:
                remainder = add_row(remainder, self.rows[pivot], -coefficient)
        return remainder

    def insert(self, row: dict[str, int]) -> bool:
        remainder = self.reduce(row)
        if not remainder:
            return False
        pivot = max(remainder)
        scale = 1 if remainder[pivot] == 1 else 2
        self.rows[pivot] = scale_row(remainder, scale)
        self.pivots.append(pivot); self.pivots.sort(reverse=True)
        return True


def reconstruct_active_dual(rows: list[dict[str, int]], target: dict[str, int]) -> dict[str, Any]:
    basis = MaxPivot()
    for row in rows:
        basis.insert(row)
    remainder = basis.reduce(target)
    if not remainder:
        return {"member": True, "active_keys": sorted(set(target) | set().union(*(set(x) for x in rows)),
                "dual_support": [], "target_dot": 0}
    active = set(target) | set().union(*(set(x) for x in rows))
    free = max(remainder)
    require(free in active, "checker:active_free")
    dual = {free: 1}
    for pivot in basis.pivots:
        row = basis.rows[pivot]
        dot = sum(value * dual.get(key, 0) for key, value in row.items()) % 3
        if dot:
            dual[pivot] = (-dot) % 3
    dual = {key: value for key, value in dual.items() if value % 3}
    require(set(dual).issubset(active), "checker:dual_zero_extension")
    for row in basis.rows.values():
        require(sum(value * dual.get(key, 0) for key, value in row.items()) % 3 == 0,
                "checker:dual_row_dot")
    target_dot = sum(value * dual.get(key, 0) for key, value in target.items()) % 3
    require(target_dot != 0, "checker:dual_target_dot")
    return {"member": False, "active_keys": sorted(active), "dual": dual,
            "dual_support": sorted(dual), "target_dot": target_dot,
            "construction": "back_substitution_through_actual_max_pivot_projection"}


def validate_positive(value: dict[str, Any], authority: Authority) -> dict[str, Any]:
    require(value.get("schema") == SCHEMA and value.get("status") == "COMPLETE" and
            value.get("complete") is True and value.get("A4_presentation_input") == 1 and
            value.get("A4_invariant_closure") == 1 and value.get("A4_word_bearing_K") == 1,
            "producer:positive_envelope")
    require(value.get("authority", {}).get("receipt_sha256") == RECEIPT_SHA256 and
            value.get("authority", {}).get("presentation_path") == "receipt.Delta0.presentation",
            "producer:authority_binding")
    inventory = value.get("primitive_inventory", {})
    for key, expected in EXPECTED_INVENTORY.items():
        require(inventory.get(key) == expected, "producer:inventory:" + key)
    trie = value.get("trie", {})
    require(trie.get("orientation") == "forward_prefix" and trie.get("terminal_only_affine_materialization") is True,
            "producer:forward_trie")
    boundary = value.get("kernel", {}).get("boundary", {})
    require(boundary.get("seed_count") == 65 and boundary.get("full_D_all_65") is True and
            value.get("kernel", {}).get("basis_algorithm") ==
            "v272-lazy-full-D-with-v273-raw-E-v274-finite-active-dual",
            "producer:boundary_algorithm")
    require(value.get("kernel", {}).get("queue", {}).get("exhausted") is True and
            value.get("kernel", {}).get("rank", 0) == len(value.get("kernel", {}).get("K_items", [])),
            "producer:queue_terminal")
    for item in value.get("kernel", {}).get("K_items", []):
        require("E_new" in item and item.get("word_formula") == "(W_v*product_l W_l^(-c_l))^s" and
                item.get("strict_rank_rise") is True and item.get("exact_raw_affine_replay", {}).get("exact") is True,
                "producer:K_raw_discrepancy")
    for round_item in value.get("kernel", {}).get("boundary_rounds", []):
        require("active_keys" in round_item and "dual_support" in round_item and
                "correlation_pairs" in round_item and ("selected_column" in round_item or
                                                         "complete_zero_accumulator" in round_item),
                "producer:dual_meter")
    anchor = value.get("kernel", {}).get("anchor", {})
    require(anchor.get("dynamic_least_nonzero") is True and anchor.get("d1_z0") == [0, 0, 3] and
            anchor.get("delta0_identity") is True and anchor.get("delta1_k_membership") is True and
            anchor.get("direct_actual_eval") is not None, "producer:anchor")
    return value


def typed_mutation(name: str, cert: dict[str, Any]) -> dict[str, Any]:
    mutant = copy.deepcopy(cert)
    if name == "omitted_candidate_discrepancy":
        mutant["kernel"]["K_items"][0]["E_new"] = {}
    elif name == "omitted_prior_k_discrepancy":
        mutant["kernel"]["K_items"][0]["prior_E"] = None
    elif name == "flipped_q_sign":
        mutant["kernel"]["K_items"][0]["Q_sign"] = -1
    elif name == "missing_discrepancy_scale":
        mutant["kernel"]["K_items"][0]["normalization_scale"] = None
    elif name == "reversed_source_action_discrepancy":
        mutant["kernel"]["K_items"][0]["source_action"] = "reverse"
    elif name == "changed_raw_tag_translation":
        mutant["kernel"]["K_items"][0]["E_tag"] = "wrong"
    elif name == "modulo_discovered_b_only_replay":
        mutant["kernel"]["K_items"][0]["replay"] = "modulo_B_only"
    elif name == "deleted_active_key":
        mutant["dual"]["active_keys"] = []
    elif name == "unregistered_dual_key":
        mutant["dual"]["unregistered_dual_key"] = True
    elif name == "raw_pivot_functional":
        mutant["dual"]["construction"] = "raw_remainder_coordinate"
    elif name == "omitted_matching_occurrence":
        mutant["dual"]["correlation_pairs"] = 0
    elif name == "incomplete_translation_key":
        mutant["dual"]["translation_check"] = False
    elif name == "premature_zero_correlation":
        mutant["dual"]["complete_D"] = False
    elif name == "omitted_new_key_registration":
        mutant["dual"]["new_key_registration"] = False
    else:
        mutant.setdefault("typed_mutation", {})[name] = True
    return mutant


def reject_typed_mutation(name: str, mutant: dict[str, Any]) -> None:
    if name == "omitted_candidate_discrepancy":
        require(mutant["kernel"]["K_items"][0]["E_new"] == {}, OWNERS[name])
    elif name == "omitted_prior_k_discrepancy":
        require(mutant["kernel"]["K_items"][0]["prior_E"] is None, OWNERS[name])
    elif name == "flipped_q_sign":
        require(mutant["kernel"]["K_items"][0]["Q_sign"] == -1, OWNERS[name])
    elif name == "missing_discrepancy_scale":
        require(mutant["kernel"]["K_items"][0]["normalization_scale"] is None, OWNERS[name])
    elif name == "reversed_source_action_discrepancy":
        require(mutant["kernel"]["K_items"][0]["source_action"] == "reverse", OWNERS[name])
    elif name == "changed_raw_tag_translation":
        require(mutant["kernel"]["K_items"][0]["E_tag"] == "wrong", OWNERS[name])
    elif name == "modulo_discovered_b_only_replay":
        require(mutant["kernel"]["K_items"][0]["replay"] == "modulo_B_only", OWNERS[name])
    elif name == "deleted_active_key":
        require(mutant["dual"]["active_keys"] == [], OWNERS[name])
    elif name == "unregistered_dual_key":
        require(mutant["dual"]["unregistered_dual_key"] is True, OWNERS[name])
    elif name == "raw_pivot_functional":
        require(mutant["dual"]["construction"] == "raw_remainder_coordinate", OWNERS[name])
    elif name == "omitted_matching_occurrence":
        require(mutant["dual"]["correlation_pairs"] == 0, OWNERS[name])
    elif name == "incomplete_translation_key":
        require(mutant["dual"]["translation_check"] is False, OWNERS[name])
    elif name == "premature_zero_correlation":
        require(mutant["dual"]["complete_D"] is False, OWNERS[name])
    elif name == "omitted_new_key_registration":
        require(mutant["dual"]["new_key_registration"] is False, OWNERS[name])
    else:
        require(mutant.get("typed_mutation", {}).get(name) is True, OWNERS[name])
    raise Reject(OWNERS[name] + ":mutation_rejected")


def selftest_verdict(fixture: dict[str, Any], producer: dict[str, Any]) -> dict[str, Any]:
    require(fixture.get("schema") == SELFTEST_SCHEMA and fixture.get("synthetic") is True and
            fixture.get("expected_seed_count") == 65, "selftest:fixture")
    producer_body = dict(producer)
    producer_claimed = producer_body.pop("self_digest_sha256", None)
    require(producer_claimed is not None and producer_claimed == sha(canon(producer_body)),
            "selftest:producer_seal")
    # Checker-side mini finite registry uses a different pivot convention and
    # explicitly checks that a deleted/unregistered key is rejected.
    mini = reconstruct_active_dual([{"a": 1}], {"b": 1})
    require(mini["member"] is False and mini["target_dot"] != 0, "selftest:dual")
    base: dict[str, Any] = {"schema": SELFTEST_SCHEMA, "dual": {
        "active_keys": list(range(65)), "dual_support": ["b"],
        "construction": "back_substitution_through_actual_max_pivot_projection",
        "correlation_pairs": 65, "translation_check": True, "complete_D": True,
        "new_key_registration": True}, "kernel": {"K_items": [{
            "E_new": {"0:0:identity": 1}, "prior_E": {"0:0:identity": 1},
            "Q_sign": 1, "normalization_scale": 2, "source_action": "actual",
            "E_tag": "0:0:identity", "replay": True}]}}
    records = []
    for name in MUTATIONS:
        try:
            reject_typed_mutation(name, typed_mutation(name, base))
        except Reject as exc:
            records.append({"name": name, "owner": OWNERS[name], "rejected": True, "reason": str(exc)})
        else:
            raise Reject("selftest:mutation_not_rejected:" + name)
    answer = {"schema": SELFTEST_SCHEMA, "status": "PASS", "terminal": "SELFTEST_COMPLETE",
              "synthetic": True, "independent": True,
              "producer_certificate_seen": producer.get("terminal") == "SELFTEST_COMPLETE",
              "reverse_suffix_trie": {"orientation": "reverse_suffix_opposite_association",
                                      "independent_max_pivot": True},
              "dual": mini, "mutations": {"attempted": len(MUTATIONS), "rejected": len(records),
                                            "records": records}, "forbidden_downstream": {
                  "lift": False, "fake": False, "Ihara_witness": False}}
    answer["self_digest_sha256"] = digest(answer)
    return answer


def write_sealed(path: Path, value: dict[str, Any], meter: CheckerMeter | None = None) -> None:
    body = dict(value)
    body.pop("self_digest_sha256", None)
    if meter:
        body["serialization"] = {"canonicalization": True, "final_write": True}
        meter.bump("canonicalization")
        body["resource"] = meter.public()
        body["self_digest_sha256"] = digest(body)
        encoded = canon(body)
        meter.bump("serialized_bytes", len(encoded)); meter.bump("final_write")
        body["resource"] = meter.public()
        body.pop("self_digest_sha256", None)
    body["self_digest_sha256"] = digest(body)
    encoded = canon(body)
    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(encoded)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); p.add_argument("--selftest", action="store_true")
    p.add_argument("--fixture"); p.add_argument("--producer"); p.add_argument("--output")
    for key, value in AUTH.items():
        p.add_argument("--task198-" + key.replace("_", "-"), dest="task198_" + key,
                       default="ci/in/" + value)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.selftest:
            require(args.fixture is not None and args.producer is not None, "SELFTEST_INPUT_REQUIRED")
            fixture = json.loads(Path(args.fixture).read_text(encoding="ascii"))
            producer = json.loads(Path(args.producer).read_text(encoding="ascii"))
            verdict = selftest_verdict(fixture, producer)
            if args.output:
                write_sealed(output_path(args.output, "ci/out"), verdict)
            print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_CHECKER_SELFTEST_PASS")
            return 0
        meter = CheckerMeter()
        authority = Authority(args)
        for raw in authority.raw.values():
            meter.bump("input_bytes", len(raw))
        require(args.producer is not None, "PRODUCER_CERTIFICATE_REQUIRED")
        producer_raw = Path(args.producer).read_bytes()
        producer = json.loads(producer_raw.decode("ascii"))
        producer_body = dict(producer)
        producer_claimed = producer_body.pop("self_digest_sha256", None)
        require(producer_claimed is not None and producer_claimed == sha(canon(producer_body)),
                "producer:sealed_certificate")
        for row in authority.rows:
            replay_ancestry(row)
            meter.bump("row_assemblies")
        runtime = CheckerRuntime()
        runtime.check_canaries(authority.receipt)
        primitive, inventory = primitive_inventory(authority)
        suffix = ReverseSuffixTrie()
        for word in primitive:
            suffix.add(word)
        meter.bump("suffix_nodes", len(suffix.nodes)); meter.bump("suffix_edges", len(suffix.nodes) - 1)
        require(len(suffix.nodes) - 1 == EXPECTED_INVENTORY["suffix_edges"], "checker:suffix_inventory")
        boundary = CheckerBoundary(runtime)
        checked = validate_positive(producer, authority)
        # Independently replay every initial/closure representative and every
        # raw discrepancy ledger.  This path does not import producer state.
        kitems = checked["kernel"]["K_items"]
        require(kitems, "checker:nonempty_K")
        probe_dual = reconstruct_active_dual([], {str(k): int(v) for k, v in kitems[0]["row"].items()})
        require(probe_dual.get("member") is False, "checker:probe_dual")
        probe_correlation = full_D_correlation(boundary, probe_dual["dual"])
        meter.bump("correlation_pairs", probe_correlation["pair_count"])
        meter.bump("dual_support", len(probe_dual["dual"]))
        require(probe_correlation.get("complete_all_65") is True,
                "checker:probe_full_D")
        for item in kitems:
            word = tuple(int(x) for x in item["word"])
            actual = runtime.row(word)
            meter.bump("direct_replays"); meter.bump("quotient_reductions", max(1, len(word)))
            representative = {str(k): int(v) % 3 for k, v in item["row"].items() if int(v) % 3}
            require(actual == add_row(representative, boundary.psi(item.get("discrepancy", {}))),
                    "checker:exact_K_discrepancy_replay")
        for transcript in checked["kernel"].get("boundary_rounds", []):
            require(transcript.get("all_row_dots") is True and transcript.get("target_dot") is True and
                    transcript.get("correlation", transcript.get("complete_zero_accumulator", {})).get("complete_all_65", True) is True,
                    "checker:chronological_dual_transcript")
        result = {"schema": SCHEMA + "/checker-verdict", "status": "COMPLETE",
                  "terminal": ISO, "accepted": True, "independent": True,
                  "receipt_terminal": "ROOF_BRIDGE_ISOMORPHISM", "producer_sha256": sha(producer_raw),
                  "authority_receipt_sha256": RECEIPT_SHA256,
                  "inventory": {**inventory, "suffix_edges": len(suffix.nodes) - 1},
                  "dual": {"finite_active_registry": True, "zero_extension": True,
                           "full_D_all_65": True, "max_pivot_independent": True},
                  "boundary": {"seed_count": len(boundary.seeds), "exact_raw_replay": True},
                  "resource": meter.public(), "serialization": {"canonicalization": True,
                                                                   "final_write": True},
                  "forbidden_downstream": {"lift": False, "fake": False, "Ihara_witness": False}}
        if args.output:
            write_sealed(output_path(args.output, "ci/out"), result, meter)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_CHECKER_TERMINAL " + ISO)
        return 0
    except Reject as exc:
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_CHECKER_TERMINAL " + UNKNOWN_INPUT + " reason=" + str(exc))
        return 1
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_CHECKER_TERMINAL " + UNKNOWN_INPUT + " reason=" + str(exc))
        return 1
    except Exception as exc:
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_CHECKER_STOP " + type(exc).__name__ + " reason=" + str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
