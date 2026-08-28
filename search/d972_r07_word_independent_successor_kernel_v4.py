#!/usr/bin/env python3
"""R07 A4 word-independent successor kernel, v4.

The v4 producer is deliberately a small, self contained consumer of the
accepted task198 receipt.  It keeps the presentation, affine Fox state and
the raw boundary ledger separate: a K word is never certified merely by a
hash or by a roof value.  The production route is not synthetic and does not
use task179/Q0 enumeration.
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
SCHEMA = "d972-r07-word-independent-successor-kernel/v4"
SELFTEST_SCHEMA = SCHEMA + "/selftest-fixture/v4"
ISO = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PASS"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
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
VERDICT_BYTES = 150
RECEIPT_BYTES = 31017244
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
CONTEXT_TAGS = ("E3-C21", "E3-C22", "E3-C23", "E3-C24", "E3-C25",
                "E4-C1", "E4-C27", "E4-C21", "E4-C26", "E4-C28")
EXPECTED_INVENTORY = {
    "sections": 243, "records": 26, "q0_relators": 19,
    "primitive_words": 288, "literal_primitive_letters": 114458,
    "prefix_edges": 15970, "suffix_edges": 26136,
    "stored_row_letters": 5475488,
}
CAPS = {
    "wall_seconds": 14400, "rss_bytes": 8000000000, "input_bytes": 500000000,
    "serialized_bytes": 2000000000, "canonicalization": 100000000, "final_write": 1,
    "terminal_materializations": 1000000, "trie_nodes": 50000, "trie_edges": 50000,
    "ancestry_nodes": 2000000, "ancestry_edges": 4000000, "expanded_letters": 4000000,
    "row_assemblies": ROWS, "relator_evaluations": 50000000,
    "quotient_reductions": 100000000, "affine_sparse_ops": 100000000,
    "direct_replays": 100000, "membership_queries": 200000,
    "membership_reductions": 50000000, "echelon_insertions": 10000000,
    "queue_actions": 500000, "dual_correlations": 10000000,
    "actor_applications": 40, "discovered_boundary_columns": 1000000,
    "ledger_actions": 10000000, "ledger_combinations": 10000000,
    "ledger_expansions": 10000000, "checker_work": 100000000,
    "active_keys": 10000000, "bplusk_rank": 1000000, "dual_support": 10000000,
    "all_row_dots": 10000000, "target_dots": 1000000, "correlation_pairs": 10000000,
    "new_keys": 10000000,
}

# The old v1 mutation names remain part of the audit ABI.  The seven v273
# discrepancy mutations and seven v274 finite-active-dual mutations are
# appended, with a distinct owner for every route.
MUTATIONS = (
    "per_layer_ordinal", "authority_binding", "canonical_input_bytes",
    "resolved_path_traversal", "normal_generation_proof",
    "bridge_typed_occurrence_ledger", "evaluator_abi_canary",
    "raw_boundary_coefficient", "live_echelon_inherited_scale",
    "producer_checker_basis_change", "conjugator_order",
    "source_word_basis_boundary_difference", "negative_dual", "action_matrix",
    "projected_h2_exponent", "k_z_inverse_scalar_powered_word",
    "live_resource_cap", "positive_status_terminal", "nonpositive_false_progress",
    "duplicate_markers", "inconsistent_section_word", "altered_primitive_terminal",
    "wrong_trie_edge_orientation", "wrong_action_orientation", "wrong_target_inverse",
    "producer_checker_row_mismatch", "missing_base_boundary",
    "changed_boundary_block_tag", "left_right_translation_swap",
    "omitted_inverse_action", "changed_parent_action_ancestry",
    "incomplete_queue_claim", "wrong_support_inversion_product",
    "false_zero_correlation", "omitted_candidate_discrepancy",
    "omitted_prior_k_discrepancy", "flipped_q_sign", "missing_discrepancy_scale",
    "reversed_source_action_discrepancy", "changed_raw_tag_translation",
    "modulo_discovered_b_only_replay", "deleted_active_key", "unregistered_dual_key",
    "raw_pivot_functional", "omitted_matching_occurrence",
    "incomplete_translation_key", "premature_zero_correlation",
    "omitted_new_key_registration",
)
OWNERS = {name: owner for name, owner in zip(MUTATIONS, (
    "authority.layer_ordinal", "authority.acceptance_manifest", "authority.canonical_bytes",
    "authority.resolved_containment", "authority.normal_generation_proof",
    "authority.bridge_occurrence_ledger", "authority.evaluator_abi_canary",
    "echelon.raw_boundary_replay", "echelon.inherited_scale",
    "checker.producer_checker_basis_change", "ancestry.outer_first_conjugation",
    "boundary.source_word_difference", "dual.negative_functional", "closure.action_matrix",
    "anchor.projected_h2_exponent", "anchor.inverse_scalar_powered_word",
    "resource.live_cap_witness", "terminal.positive_status", "terminal.false_progress",
    "driver.duplicate_markers", "ancestry.section_word_replay", "trie.primitive_terminal",
    "trie.forward_edge_orientation", "ancestry.action_orientation", "ancestry.target_inverse",
    "checker.typed_row_equality", "boundary.base_seed_roster", "boundary.block_tag",
    "boundary.translation_orientation", "boundary.inverse_action_queue",
    "boundary.parent_action_ancestry", "boundary.queue_exhaustion",
    "dual.support_inversion_product", "dual.complete_zero_correlation",
    "discrepancy.omitted_candidate_E", "discrepancy.omitted_prior_K_E",
    "discrepancy.flipped_Q_sign", "discrepancy.missing_scale",
    "discrepancy.reversed_source_action", "discrepancy.changed_raw_tag_translation",
    "discrepancy.modulo_B_only_replay", "dual.deleted_active_key",
    "dual.unregistered_nonzero_key", "dual.raw_pivot_functional",
    "dual.omitted_matching_occurrence", "dual.incomplete_translation_key",
    "dual.premature_zero_correlation", "dual.omitted_new_key_registration",
))}


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canon(value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


class Reject(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float, limit: int | float, state: str):
        self.phase, self.cap, self.value, self.limit, self.state = phase, cap, value, limit, state
        super().__init__(f"phase={phase}:cap={cap}:value={value}:limit={limit}:last_replayable_state={state}")


class InputStop(Reject):
    pass


def rss_bytes() -> int:
    # This is an in-process observation only.  There is no subprocess or
    # external resource probe in the producer.
    try:
        import resource
        return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024
    except Exception:
        return 0


class Meter:
    def __init__(self, limits: dict[str, int | float] | None = None):
        self.limits = dict(limits or CAPS)
        self.counters = {key: 0 for key in self.limits}
        self.started = time.monotonic()
        self.phase = "rank_zero"
        self.last_replayable_state = "RANK_ZERO_RESTART"

    def state(self, state: str) -> None:
        self.last_replayable_state = state

    def check(self, phase: str | None = None) -> None:
        if phase:
            self.phase = phase
        self.counters["wall_seconds"] = time.monotonic() - self.started
        self.counters["rss_bytes"] = max(self.counters.get("rss_bytes", 0), rss_bytes())
        for key in ("wall_seconds", "rss_bytes"):
            if self.counters[key] > self.limits[key]:
                raise ResourceStop(self.phase, key, self.counters[key], self.limits[key], self.last_replayable_state)

    def bump(self, key: str, amount: int = 1, phase: str | None = None) -> None:
        self.counters[key] = self.counters.get(key, 0) + int(amount)
        self.check(phase)
        if key in self.limits and self.counters[key] > self.limits[key]:
            raise ResourceStop(self.phase, key, self.counters[key], self.limits[key], self.last_replayable_state)

    def public(self) -> dict[str, Any]:
        self.check(self.phase)
        return {"limits": self.limits, "counters": self.counters,
                "last_replayable_state": self.last_replayable_state,
                "single_process": True, "no_retry_or_pool": True}


def exact_path(text: str, area: str, label: str, basename: str, must_exist: bool = True) -> Path:
    raw = str(text).replace("\\", "/")
    p = Path(raw)
    require(not p.is_absolute() and ".." not in p.parts and "." not in p.parts,
            f"{label}:lexical_path")
    expected = (ROOT / area / basename).resolve(strict=must_exist)
    actual = (ROOT / p).resolve(strict=must_exist)
    require(actual == expected and actual.name == basename, f"{label}:resolved_exact_path")
    cursor = ROOT
    for part in p.parts:
        cursor = cursor / part
        require(not cursor.is_symlink(), f"{label}:symlink_alias")
    return actual


def output_path(text: str, area: str, label: str) -> Path:
    raw = str(text).replace("\\", "/")
    p = Path(raw)
    require(not p.is_absolute() and ".." not in p.parts and "." not in p.parts,
            f"{label}:lexical_path")
    actual = (ROOT / p).resolve(strict=False)
    base = (ROOT / area).resolve(strict=True)
    require(actual.parent == base, f"{label}:output_containment")
    return actual


def load_json_once(path: Path, meter: Meter, label: str) -> tuple[bytes, dict[str, Any]]:
    raw = path.read_bytes()
    meter.bump("input_bytes", len(raw), label + ":bytes")
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InputStop(label + ":canonical_ascii_json") from exc
    require(isinstance(value, dict), label + ":object")
    return raw, value


def path_identity(path: Path, expected: tuple[str, int, str], label: str) -> dict[str, Any]:
    relative, size, expected_sha = expected
    require(path.as_posix().replace(ROOT.as_posix() + "/", "") == relative,
            label + ":relative_path")
    raw = path.read_bytes()
    require(len(raw) == size and sha(raw) == expected_sha, label + ":bytes_sha256")
    return {"path": relative, "bytes": size, "sha256": expected_sha}


class AuthorityAdapter:
    """Read each authority-v2 member once and retain one authenticated object."""
    def __init__(self, args: argparse.Namespace, meter: Meter):
        self.meter = meter
        self.paths: dict[str, Path] = {}
        for key, basename in AUTH.items():
            self.paths[key] = exact_path(getattr(args, "task198_" + key), "ci/in",
                                         "TASK198_" + key.upper(), basename)
        # The five members are read once.  No second parser or alias is made.
        self.raw: dict[str, bytes] = {}
        self.values: dict[str, dict[str, Any]] = {}
        for key in ("manifest", "verdict", "receipt"):
            raw, value = load_json_once(self.paths[key], meter, "authority." + key)
            self.raw[key], self.values[key] = raw, value
        for key in ("producer", "checker"):
            raw = self.paths[key].read_bytes()
            meter.bump("input_bytes", len(raw), "authority." + key)
            require(raw.decode("ascii").endswith("\n"), "authority:" + key + ":attestation_ascii")
            self.raw[key] = raw
        self.validate()
        self.object = {"receipt": self.values["receipt"], "manifest": self.values["manifest"],
                       "verdict": self.values["verdict"], "raw_sha256": {k: sha(v) for k, v in self.raw.items()},
                       "receipt_bytes": len(self.raw["receipt"]), "receipt_sha256": sha(self.raw["receipt"])}
        self.identity = {"members": {key: {"basename": AUTH[key], "bytes": len(raw),
                                             "sha256": sha(raw)} for key, raw in self.raw.items()},
                         "manifest_self_digest_sha256": self.values["manifest"]["manifest_self_digest_sha256"],
                         "receipt_self_digest_sha256": self.values["receipt"]["self_digest_sha256"],
                         "task198_source_identities": self.values["manifest"]["task198_source_identities"]}

    def validate(self) -> None:
        receipt = self.values["receipt"]
        manifest = self.values["manifest"]
        verdict = self.values["verdict"]
        require(sha(self.raw["manifest"]) == MANIFEST_SHA256, "manifest:sha256")
        require(sha(self.raw["receipt"]) == RECEIPT_SHA256 and len(self.raw["receipt"]) == RECEIPT_BYTES,
                "receipt:bytes_sha256")
        require(sha(self.raw["verdict"]) == VERDICT_SHA256 and len(self.raw["verdict"]) == VERDICT_BYTES,
                "verdict:bytes_sha256")
        require(manifest.get("schema") == MANIFEST_SCHEMA and manifest.get("accepted") is True and
                manifest.get("independent") is True and manifest.get("synthetic") is False,
                "manifest:accepted_independent_nonsynthetic")
        require(manifest.get("manifest_self_digest_sha256") ==
                "0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684",
                "manifest:self_digest")
        manifest_body = dict(manifest)
        manifest_body.pop("manifest_self_digest_sha256", None)
        require(sha(canon(manifest_body)) == manifest["manifest_self_digest_sha256"],
                "manifest:self_digest_replay")
        require(manifest.get("accepted_receipt_basename") == AUTH["receipt"], "manifest:receipt_basename")
        require(manifest.get("receipt", {}).get("sha256") == RECEIPT_SHA256 and
                manifest["receipt"].get("bytes") == RECEIPT_BYTES and
                manifest["receipt"].get("self_digest_sha256") ==
                "c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f",
                "manifest:receipt_member")
        checker_verdict = manifest.get("checker_verdict", {})
        require(checker_verdict.get("bytes") == VERDICT_BYTES and checker_verdict.get("sha256") == VERDICT_SHA256,
                "manifest:checker_verdict")
        require(verdict.get("schema") == PRESENTATION_SCHEMA + "/crosscheck/v2" and
                verdict.get("accepted") is True and verdict.get("independent") is True and
                verdict.get("receipt_terminal") == "ROOF_BRIDGE_ISOMORPHISM",
                "verdict:independent_terminal")
        require(set(manifest.get("task198_source_identities", {})) == {"producer", "checker", "driver"},
                "manifest:source_identity_set")
        for side, expected in TASK198_SOURCES.items():
            item = manifest["task198_source_identities"][side]
            require(item.get("path") == expected[0] and item.get("bytes") == expected[1] and
                    item.get("sha256") == expected[2], "manifest:source_identity:" + side)
        for side in ("producer", "checker"):
            item = manifest[side]
            require(item.get("run") == "33155710862" and
                    item.get("head") == "bed1d5e6b41477b8799f2a33a24e46f7800f9510" and
                    item.get("artifact_id") == "9686477718" and
                    item.get("zip_sha256") ==
                    "8e1d218cb3d0e09e7a633d2c7d4481f232b33e76eaafc51223c307a2c62e0854",
                    "manifest:run_head_artifact:" + side)
            member = item.get("member", {})
            require(member.get("basename") == AUTH["receipt"] and member.get("bytes") == RECEIPT_BYTES and
                    member.get("sha256") == RECEIPT_SHA256 and
                    item.get("terminal_line_sha256") ==
                    ("b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"
                     if side == "producer" else
                     "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e"),
                    "manifest:member_identity:" + side)
            att = manifest.get(side + "_attestation", {})
            require(att.get("basename") == AUTH[side] and att.get("sha256") == sha(self.raw[side]) and
                    att.get("bytes") == len(self.raw[side]),
                    "manifest:attestation:" + side)
        require(manifest.get("checker", {}).get("member") == manifest.get("producer", {}).get("member"),
                "manifest:producer_checker_member_agreement")
        require(checker_verdict.get("accepted") is True and checker_verdict.get("independent") is True and
                checker_verdict.get("receipt_terminal") == "ROOF_BRIDGE_ISOMORPHISM" and
                checker_verdict.get("schema") == PRESENTATION_SCHEMA + "/crosscheck/v2" and
                checker_verdict.get("basename") == AUTH["verdict"], "manifest:verdict_seal")
        body = dict(receipt)
        claimed = body.pop("self_digest_sha256", None)
        require(claimed == "c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f" and
                claimed == sha(canon(body)), "receipt:self_digest")
        require(receipt.get("schema") == PRESENTATION_SCHEMA and receipt.get("status") == "COMPLETE" and
                receipt.get("terminal") == "ROOF_BRIDGE_ISOMORPHISM", "receipt:envelope")
        # v4 deliberately reads rows/proof/layers only at their authoritative path.
        presentation = receipt.get("Delta0", {}).get("presentation")
        require(isinstance(presentation, dict), "receipt:Delta0.presentation")
        require(presentation.get("row_count") == ROWS and presentation.get("layer_counts") == LAYERS and
                len(presentation.get("rows", [])) == ROWS and
                presentation.get("normal_closure_exact") is True and
                presentation.get("normal_generation") is True and presentation.get("resume_cursor") == ROWS,
                "presentation:row_layer_counts")
        expected_chunks = [
            (0, 1024, "0c0e58393e7a40dc9fe963865205c65e4c472f3b2dbef0f1e14b3f966d7384da"),
            (1024, 2048, "035c1f704201d59ac7a41900ecee592423bd1ab9890f753f9fb9f10a3b6bbc19"),
            (2048, 3072, "6752eb1dcfd14739ebf5fe15622cc98db49758843d4cb0b2e42df6569c099ca9"),
            (3072, 4096, "cde8b1e675484f074ab09e8a2478a2762abc5606c9969a553b909a63907d7881"),
            (4096, 5120, "3e300ea7b21f3a95c2ac25fa07d77e51a29296e534d891f017e19b9fa105655f"),
            (5120, 6144, "87862c1e0a531d663d2a6223042f2b8d4ddb575a2b2888629e11414023e0f8d6"),
            (6144, 6441, "5a4da210ce72a9194c2e9e8fc0e294846ab80362b9945aa8b0f48fe7ffeabb56"),
        ]
        require([(int(x.get("start")), int(x.get("end")), x.get("sha256"))
                 for x in presentation.get("chunks", [])] == expected_chunks,
                "presentation:sealed_chunks")
        rows = presentation["rows"]
        local = {layer: [] for layer in LAYERS}
        for row in rows:
            layer = row.get("layer")
            require(layer in LAYERS and isinstance(row.get("ordinal"), int), "presentation:row_shape")
            local[layer].append(row["ordinal"])
        for layer, count in LAYERS.items():
            require(local[layer] == list(range(1, count + 1)), "presentation:local_ordinals:" + layer)
        require(presentation.get("rows_sha256") == "e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950",
                "presentation:rows_sha256")
        proof = presentation.get("normal_generation_proof", receipt.get("normal_generation_proof", {}))
        require(proof.get("Gamma_cayley_edge_count") == 6318 and proof.get("Gamma_cayley_state_count") == 243 and
                proof.get("Q0_defect_normal_closure_order") == 243 and proof.get("Q0_lift_count") == 19,
                "proof:normal_generation")
        qproof = proof.get("Q0_order_proof", {})
        require(qproof.get("G9_abstract_presentation_order") == 2916 and
                qproof.get("G9_direct_image_order") == 2916 and qproof.get("P_abstract_presentation_order") == 504 and
                qproof.get("P_direct_image_order") == 504 and qproof.get("Q0_marked_image_order") == 1469664 and
                qproof.get("Q0_presentation_order_upper_bound") == 1469664 and
                qproof.get("complete_relator_count") == 19 and
                qproof.get("complete_relators_sha256") ==
                "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a" and
                qproof.get("cross_commutator_count") == 4 and
                qproof.get("factor_payload_sha256") ==
                "6eb95a6830b19e729c5e2a9b4f861fb6105ac0be1f1058cc566898d1b48758ba" and
                qproof.get("marked_splitting_equation_count") == 2 and
                qproof.get("method") ==
                "producer-owned SymPy factor orders plus direct marked-permutation enumeration",
                "proof:Q0_order")
        require(proof.get("Q0_defect_normal_closure_rounds") == [243] and
                proof.get("all_record_generator_closure_order") == 243 and
                proof.get("marked_action_loop_count") == 104 and
                proof.get("selected_gamma_records") == [1, 3, 6, 9] and
                proof.get("presentation_quotient_order_upper_bound") == 357128352 and
                proof.get("surjective_marked_image_order") == 357128352 and
                proof.get("upper_bound_equals_image_order") is True,
                "proof:closure_equality")
        bridge = receipt.get("bridge", {})
        require(bridge.get("ten_to_eleven") == [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9] and
                bridge.get("eleven_delete_duplicate") == [0, 1, 2, 3, 5, 6, 7, 8, 9, 10],
                "bridge:maps")
        require(bridge.get("seven_blocks") == [[0, 1, 2], [3, 0, 4], [5], [6], [7], [8], [9]],
                "bridge:seven_blocks")
        require(bridge.get("image_order") == 357128352 and bridge.get("kernel_order") == 1 and
                bridge.get("marked_inverse_count") == 4 and bridge.get("marked_replay_count") == 4 and
                receipt.get("normal_generation_proof", {}).get("presentation_quotient_order_upper_bound", 357128352) ==
                357128352, "bridge:order_replay")
        ledger = bridge.get("occurrence_ledger")
        require(isinstance(ledger, list) and len(ledger) == 11 and
                bridge.get("occurrence_ledger_sha256") ==
                "040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7" and
                bridge.get("typed_coordinate_ledger_sha256") ==
                "9f9c081e9653d6e141e4d6d231e2d6db9526850b7ccd33c0859d13825f3fa83c",
                "bridge:ledger_digest")
        for item in ledger:
            require(all(key in item for key in ("block", "block_index", "block_slot", "context_id",
                                                 "factor_sign", "fox_prefix_occurrences", "occurrence",
                                                 "ordinal", "orientation", "role", "ten_index", "type")),
                    "bridge:typed_ledger_fields")
            require(isinstance(item["block_index"], int) and isinstance(item["block_slot"], int) and
                    isinstance(item["ten_index"], int), "bridge:typed_ledger_types")
        evaluator = receipt.get("evaluator", {})
        require(evaluator.get("schema") == "d972-r07-v188-roof-consumer-action-abi/v1" and
                evaluator.get("coordinate_widths") == [40, 40, 40, 40, 40, 154, 154, 154, 154, 154] and
                evaluator.get("relator_rows_sha256") ==
                "e00880c01bc96ba8f0549311f4955662668d74001ecf5c06097646dad4268950",
                "evaluator:abi_widths_digest")
        ep = evaluator.get("entry_points", {})
        required_ep = {
            "eval": ("roof_eval", ["runtime", "word"]),
            "multiply": ("roof_multiply", ["runtime", "left", "right"]),
            "inverse": ("roof_inverse", ["runtime", "value"]),
            "source_section": ("roof_source_section", ["runtime", "gamma_state_id", "q0_state_id"]),
            "action": ("roof_action", ["runtime", "actor_word", "value"]),
            "section_cocycle": ("roof_section_cocycle", ["runtime", "left_section_word", "right_section_word", "product_section_word"]),
        }
        for name, (fun, args) in required_ep.items():
            require(ep.get(name, {}).get("callable") == fun and ep[name].get("args") == args,
                    "evaluator:entry_point:" + name)
        canaries = evaluator.get("canaries", {})
        require(set(canaries) >= {"x", "y", "x_inverse", "xy", "x_action_y",
                                  "xy_section_cocycle", "source_2_2", "nonsplit_y_y_section_cocycle"},
                "evaluator:canaries")
        for name, item in canaries.items():
            if name == "nonsplit_y_y_section_cocycle":
                require(item is None, "evaluator:canary_shape:" + name)
            else:
                require(isinstance(item, dict) and isinstance(item.get("value"), list),
                        "evaluator:canary_shape:" + name)
        require(receipt.get("Ihara_witness") is False and receipt.get("cofinal_lift") is False and
                receipt.get("fake") is False and receipt.get("direct_Delta_states_enumerated") == 0 and
                receipt.get("D_all", {}).get("materialized") is False,
                "receipt:forbidden_flags")

    @property
    def receipt(self) -> dict[str, Any]:
        return self.values["receipt"]

    @property
    def rows(self) -> list[dict[str, Any]]:
        return self.receipt["Delta0"]["presentation"]["rows"]


def word_reduce(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for value in word:
        letter = int(value)
        require(letter in (-2, -1, 1, 2), "signed F2 letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def word_inv(word: Sequence[int]) -> tuple[int, ...]:
    return word_reduce(-x for x in reversed(word))


def word_mul(*words: Sequence[int]) -> tuple[int, ...]:
    out: tuple[int, ...] = ()
    for word in words:
        out = word_reduce(out + tuple(word))
    return out


def add_row(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, value in right.items():
        coefficient = (out.get(key, 0) + int(scale) * int(value)) % 3
        if coefficient:
            out[key] = coefficient
        else:
            out.pop(key, None)
    return out


def scale_row(row: dict[str, int], scale: int) -> dict[str, int]:
    return {key: (int(value) * int(scale)) % 3 for key, value in row.items()
            if (int(value) * int(scale)) % 3}


def jsonable(value: Any) -> Any:
    if isinstance(value, bytes):
        return {"__bytes__": value.hex()}
    if isinstance(value, tuple):
        return [jsonable(x) for x in value]
    if isinstance(value, list):
        return [jsonable(x) for x in value]
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (int, str, bool)) or value is None:
        return value
    return repr(value)


def key_token(value: Any) -> str:
    return canon(jsonable(value)).hex()


def load_pinned_module(path: str, size: int, expected: str, name: str) -> Any:
    path_obj = ROOT / path
    require(path_obj.is_file() and path_obj.stat().st_size == size and sha(path_obj.read_bytes()) == expected,
            "pinned_module:" + path)
    spec = importlib.util.spec_from_file_location(name, path_obj)
    require(spec is not None and spec.loader is not None, "pinned_module_loader")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_pinned_json(path: str, size: int, expected: str) -> dict[str, Any]:
    path_obj = ROOT / path
    require(path_obj.is_file() and path_obj.stat().st_size == size and sha(path_obj.read_bytes()) == expected,
            "pinned_json:" + path)
    value = json.loads(path_obj.read_text(encoding="ascii"))
    require(isinstance(value, dict), "pinned_json:object")
    return value


class AffineState:
    """Actual affine Fox state (a,u), over the pinned quotient and F3."""
    def __init__(self, quotient: Any, a: Any, u: dict[tuple[int, Any], int]):
        self.quotient, self.a, self.u = quotient, a, {k: v % 3 for k, v in u.items() if v % 3}

    def multiply(self, other: "AffineState") -> "AffineState":
        require(self.quotient is other.quotient, "affine:quotient_mismatch")
        translated: dict[tuple[int, Any], int] = {}
        for (component, element), coefficient in other.u.items():
            translated[(component, self.quotient.mul(self.a, element))] = coefficient
        return AffineState(self.quotient, self.quotient.mul(self.a, other.a), add_local(self.u, translated))

    def inverse(self) -> "AffineState":
        inverse_a = self.quotient.inverse(self.a)
        return AffineState(self.quotient, inverse_a, translate_local(self.u, inverse_a, self.quotient, -1))

    def is_identity_roof(self) -> bool:
        return self.a == self.quotient.identity


def add_local(left: dict[tuple[int, Any], int], right: dict[tuple[int, Any], int], scale: int = 1) -> dict[tuple[int, Any], int]:
    out = dict(left)
    for key, value in right.items():
        coefficient = (out.get(key, 0) + scale * value) % 3
        if coefficient:
            out[key] = coefficient
        else:
            out.pop(key, None)
    return out


def translate_local(vector: dict[tuple[int, Any], int], translation: Any, quotient: Any, scale: int = 1) -> dict[tuple[int, Any], int]:
    out: dict[tuple[int, Any], int] = {}
    for (component, element), coefficient in vector.items():
        key = (component, quotient.mul(translation, element))
        out[key] = (out.get(key, 0) + scale * coefficient) % 3
    return {key: value for key, value in out.items() if value}


def h2_mul(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, r = left
    ap, bp, rp = right
    return ((a + ap) % 9, (b + bp) % 9, (r + rp - b * ap) % 9)


def h2_inv(value: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, r = value
    return ((-a) % 9, (-b) % 9, (-r - a * b) % 9)


def h2_signed_word(word: Iterable[int]) -> tuple[int, int, int]:
    value = (0, 0, 0)
    generators = {1: (1, 0, 0), 2: (0, 1, 0)}
    for letter in word:
        base = generators[abs(int(letter))]
        value = h2_mul(value, base if letter > 0 else h2_inv(base))
    return value


class Runtime:
    """Pinned E3/E4 quotient runtime and ten fixed task232 contexts."""
    def __init__(self, authority: AuthorityAdapter, meter: Meter):
        self.meter = meter
        self.old = load_pinned_module(*E4_SOURCE, "r07_v4_frozen_e4")
        self.q3 = load_pinned_json(*Q3_SOURCE)
        # TASK176 is authenticated as a source identity but is not imported:
        # v4 uses the direct Fox API and has no task179 build_runtime/deletion.
        task176_path = ROOT / TASK176_SOURCE[0]
        require(task176_path.is_file() and task176_path.stat().st_size == TASK176_SOURCE[1] and
                sha(task176_path.read_bytes()) == TASK176_SOURCE[2], "task176:source_identity")
        self.e3, self.e4, self.meta = self.old.reconstruct_quotients(self.q3)
        self.contexts = self.task232_contexts()
        self.actors: dict[tuple[int, int], AffineState] = {}
        for index in range(10):
            for letter in (1, -1, 2, -2):
                self.actors[(index, letter)] = self.eval_affine((letter,), index)
                meter.bump("actor_applications", 1, "actor_cache")
            self.check_actor_inverses(index)
        self.check_evaluator_canaries(authority.receipt)

    def task232_contexts(self) -> list[dict[str, Any]]:
        x, y = [1], [3]
        z = self.old.inv_word(self.old.pp_words([x, y]))
        u = self.old.inv_word(self.old.pp_words([y, x]))
        pairs = [(x, y), (x, z), (y, z), (u, x), (u, y),
                 ([4], [6]), (self.old.pp_words([[1], [2]]), self.old.pp_words([[5], [6]])),
                 ([1], [4]), (self.old.pp_words([[2], [4]]), [6]),
                 ([1], self.old.pp_words([[4], [5]]))]
        contexts = []
        for i, pair in enumerate(pairs):
            contexts.append({"index": i, "type": CONTEXT_TYPES[i], "context_id": CONTEXT_IDS[i],
                             "tag": CONTEXT_TAGS[i], "left": list(pair[0]), "right": list(pair[1]),
                             "block": 1 if i < 5 else 3})
        require([(x["type"], x["context_id"]) for x in contexts] ==
                list(zip(CONTEXT_TYPES, CONTEXT_IDS)), "task232:context_ledger")
        require(contexts[0]["left"] == [1] and contexts[0]["right"] == [3] and
                contexts[7]["left"] == [1] and contexts[7]["right"] == [4],
                "task232:source_substitution")
        return contexts

    def quotient(self, index: int) -> Any:
        return self.e3 if self.contexts[index]["type"] == "E3" else self.e4

    def identity(self, index: int) -> AffineState:
        quotient = self.quotient(index)
        return AffineState(quotient, quotient.identity, {})

    def eval_affine(self, word: Sequence[int], index: int) -> AffineState:
        context = self.contexts[index]
        quotient = self.quotient(index)
        pb_word = self.old.f2_substitute(word, context["left"], context["right"])
        gradient, roof = self.old.fox_gradient_without_sections(pb_word, quotient)
        self.meter.bump("quotient_reductions", max(1, len(pb_word)), "direct_affine_eval")
        local = {(int(component), element): int(coefficient) % 3
                 for (component, element), coefficient in gradient.items() if int(coefficient) % 3}
        return AffineState(quotient, roof, local)

    def eval_pb_affine(self, word: Sequence[int], index: int) -> AffineState:
        """Evaluate a literal PB3/PB4 relation without F2 substitution."""
        quotient = self.quotient(index)
        gradient, roof = self.old.fox_gradient_without_sections(tuple(word), quotient)
        self.meter.bump("quotient_reductions", max(1, len(word)), "base_boundary_affine_eval")
        local = {(int(component), element): int(coefficient) % 3
                 for (component, element), coefficient in gradient.items() if int(coefficient) % 3}
        return AffineState(quotient, roof, local)

    def check_actor_inverses(self, index: int) -> None:
        one = self.identity(index)
        require(self.actors[(index, 1)].multiply(self.actors[(index, -1)]).a == one.a and
                self.actors[(index, 1)].multiply(self.actors[(index, -1)]).u == {},
                "actor:x_inverse")
        require(self.actors[(index, 2)].multiply(self.actors[(index, -2)]).a == one.a and
                self.actors[(index, 2)].multiply(self.actors[(index, -2)]).u == {},
                "actor:y_inverse")

    def check_evaluator_canaries(self, receipt: dict[str, Any]) -> None:
        canaries = receipt.get("evaluator", {}).get("canaries", {})
        for name, letter in (("x", 1), ("y", 2), ("x_inverse", -1), ("y_inverse", -2)):
            expected = [element_blob(self.actors[(index, letter)].a).hex() for index in range(10)]
            require(canaries.get(name, {}).get("value") == expected,
                    "evaluator:canary_direct:" + name)
        xy = [element_blob(self.quotient(index).mul(self.actors[(index, 1)].a,
                                                    self.actors[(index, 2)].a)).hex()
              for index in range(10)]
        require(canaries.get("xy", {}).get("value") == xy, "evaluator:canary_direct:xy")
        xay = []
        for index in range(10):
            q = self.quotient(index); x = self.actors[(index, 1)].a; y = self.actors[(index, 2)].a
            xay.append(element_blob(q.mul(q.mul(x, y), q.inverse(x))).hex())
        require(canaries.get("x_action_y", {}).get("value") == xay,
                "evaluator:canary_direct:x_action_y")
        source_22 = canaries.get("source_2_2", {})
        if isinstance(source_22.get("source_word"), list):
            expected = [element_blob(self.eval_affine(source_22["source_word"], index).a).hex()
                        for index in range(10)]
            require(source_22.get("value") == expected, "evaluator:canary_direct:source_2_2")
        widths = receipt.get("evaluator", {}).get("coordinate_widths", [])
        for name in ("x", "y", "x_inverse", "y_inverse", "xy", "x_action_y"):
            for index, blob in enumerate(canaries[name]["value"]):
                require(len(bytes.fromhex(blob)) == widths[index],
                        "evaluator:canary_width:" + name)

    def actor_quotient(self, index: int, letter: int) -> Any:
        state = self.actors[(index, letter)]
        return state.a

    def primitive_state(self, word: Sequence[int], index: int) -> AffineState:
        return self.eval_affine(word, index)

    def direct_row(self, word: Sequence[int], meter: Meter | None = None) -> dict[str, int]:
        out: dict[str, int] = {}
        for index in range(10):
            state = self.eval_affine(word, index)
            require(state.is_identity_roof(), f"row:nontrivial_roof:{index}")
            out = add_row(out, local_to_row(state.u, index))
            if meter:
                meter.bump("relator_evaluations", 1, "direct_row")
        return out

    def direct_action_row(self, row: dict[str, int], letter: int) -> dict[str, int]:
        out: dict[str, int] = {}
        for key, coefficient in row.items():
            index, component, token = split_row_key(key)
            actor = self.actor_quotient(index, letter)
            element = decode_key_token(token)
            moved = self.quotient(index).mul(actor, element)
            moved_key = row_key(index, component, moved)
            out[moved_key] = (out.get(moved_key, 0) + coefficient) % 3
        return {key: value for key, value in out.items() if value}


def encode_key_token(value: Any) -> str:
    return key_token(value)


def decode_key_token(token: str) -> Any:
    # The producer's own EKey objects are retained in runtime maps.  Row keys
    # are decoded only through the small per-run key registry below.
    return KEY_REGISTRY[token]


KEY_REGISTRY: dict[str, Any] = {}


def element_blob(value: Any) -> bytes:
    require(isinstance(value, tuple) and len(value) == 2 and
            isinstance(value[0], bytes) and isinstance(value[1], bytes),
            "EKey:byte_blob")
    return value[0] + value[1]


def row_key(index: int, component: int, element: Any) -> str:
    token = encode_key_token(element)
    KEY_REGISTRY[token] = element
    return f"{index}:{int(component)}:{token}"


def split_row_key(key: str) -> tuple[int, int, str]:
    parts = key.split(":", 2)
    require(len(parts) == 3, "row_key:shape")
    return int(parts[0]), int(parts[1]), parts[2]


def local_to_row(local: dict[tuple[int, Any], int], index: int) -> dict[str, int]:
    return {row_key(index, component, element): coefficient for (component, element), coefficient in local.items()
            if coefficient % 3}


class ForwardTrie:
    """Shared forward trie; nodes retain roof/parent/edge, not gradients."""
    def __init__(self, meter: Meter):
        self.nodes = [{"parent": None, "edge": None, "edges": {}, "roof": {},
                       "affine_delta": None, "terminal": {}}]
        self.meter = meter
        self.terminals: dict[tuple[int, ...], int] = {}

    def add(self, word: Sequence[int]) -> int:
        normalized = tuple(word_reduce(word))
        if normalized in self.terminals:
            return self.terminals[normalized]
        node = 0
        for letter in normalized:
            child = self.nodes[node]["edges"].get(int(letter))
            if child is None:
                child = len(self.nodes)
                self.nodes[node]["edges"][int(letter)] = child
                self.nodes.append({"parent": node, "edge": int(letter), "edges": {}, "roof": {},
                                   "affine_delta": {"letter": int(letter), "immutable": True},
                                   "terminal": {}})
                self.meter.bump("trie_nodes", 1, "forward_prefix_trie")
                self.meter.bump("trie_edges", 1, "forward_prefix_trie")
            node = child
        self.terminals[normalized] = node
        return node

    def materialize(self, word: Sequence[int], runtime: Runtime, index: int) -> AffineState:
        normalized = tuple(word_reduce(word))
        require(normalized in self.terminals, "trie:nonprimitive_terminal_request")
        node = self.terminals[normalized]
        cached = self.nodes[node]["terminal"].get(index)
        if cached is not None:
            return cached
        path: list[int] = []
        cursor = node
        while cursor:
            path.append(self.nodes[cursor]["edge"])
            cursor = self.nodes[cursor]["parent"]
        state = runtime.identity(index)
        for letter in reversed(path):
            state = state.multiply(runtime.actors[(index, letter)])
            self.meter.bump("affine_sparse_ops", 1, "terminal_materialization")
        self.nodes[node]["roof"][index] = key_token(state.a)
        self.nodes[node]["terminal"][index] = state
        self.meter.bump("terminal_materializations", 1, "terminal_materialization")
        self.meter.bump("direct_replays", 1, "terminal_materialization")
        return state

    def materialize_piece(self, word: Sequence[int], runtime: Runtime, index: int) -> AffineState:
        normalized = tuple(word_reduce(word))
        if normalized in self.terminals:
            return self.materialize(normalized, runtime, index)
        inverse = word_inv(normalized)
        require(inverse in self.terminals, "trie:missing_primitive_inverse_terminal")
        return self.materialize(inverse, runtime, index).inverse()


class WordDAG:
    """Persistent integer word DAG; expansion is bounded and replayable."""
    def __init__(self, meter: Meter):
        self.meter = meter
        self.nodes: list[dict[str, Any]] = []

    def source(self, word: Sequence[int]) -> int:
        node = len(self.nodes)
        self.nodes.append({"op": "source", "word": list(word)})
        self.meter.bump("ancestry_nodes", 1, "word_dag_source")
        return node

    def conjugate(self, letter: int, child: int) -> int:
        node = len(self.nodes)
        self.nodes.append({"op": "conjugate", "letter": int(letter), "child": int(child)})
        self.meter.bump("ancestry_nodes", 1, "word_dag_conjugate")
        return node

    def inverse(self, child: int) -> int:
        node = len(self.nodes)
        self.nodes.append({"op": "inverse", "child": int(child)})
        self.meter.bump("ancestry_nodes", 1, "word_dag_inverse")
        return node

    def product(self, children: Sequence[int]) -> int:
        node = len(self.nodes)
        self.nodes.append({"op": "product", "children": [int(x) for x in children]})
        self.meter.bump("ancestry_nodes", 1, "word_dag_product")
        return node

    def power(self, child: int, exponent: int) -> int:
        node = len(self.nodes)
        self.nodes.append({"op": "power", "child": int(child), "exponent": int(exponent)})
        self.meter.bump("ancestry_nodes", 1, "word_dag_power")
        return node

    def materialize(self, node: int) -> tuple[int, ...]:
        item = self.nodes[node]
        if item["op"] == "source":
            return tuple(item["word"])
        if item["op"] == "conjugate":
            return word_mul((item["letter"],), self.materialize(item["child"]), (-item["letter"],))
        if item["op"] == "inverse":
            return word_inv(self.materialize(item["child"]))
        if item["op"] == "product":
            return word_mul(*(self.materialize(child) for child in item["children"]))
        require(item["op"] == "power" and item["exponent"] in (0, 1, 2), "word_dag:power")
        result = word_mul(*(self.materialize(item["child"]) for _ in range(item["exponent"])))
        self.meter.bump("expanded_letters", len(result), "word_dag_materialize")
        return result


def primitive_inventory(authority: AuthorityAdapter) -> tuple[list[tuple[int, ...]], dict[str, Any]]:
    found: set[tuple[int, ...]] = set()
    rows = authority.rows
    sections: set[tuple[int, ...]] = set()
    records: set[tuple[int, ...]] = set()
    qrels: set[tuple[int, ...]] = set()
    for row in rows:
        anc = row.get("ancestry", {})
        for name in ("section_source_word", "section_target_word"):
            sections.add(tuple(word_reduce(anc.get(name, []))))
        records.add(tuple(word_reduce(anc.get("record_word", []))))
        if isinstance(anc.get("q0_relator_word"), list):
            qrels.add(tuple(word_reduce(anc["q0_relator_word"])))
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for name, child in value.items():
                if name == "q0_relator_word" and isinstance(child, list):
                    qrels.add(tuple(word_reduce(child)))
                elif isinstance(child, (dict, list)):
                    walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(authority.receipt.get("Q0", {}))
    # The q0 relators are also in the presentation ancestry payload on some
    # accepted receipts; preserve all explicit occurrences without inventing
    # a synthetic section.
    walk(authority.receipt.get("bridge", {}))
    primitive = set(sections) | set(records) | set(qrels)
    require(len(sections) == 243 and len(records) == 26 and len(qrels) == 19 and
            len(primitive) == EXPECTED_INVENTORY["primitive_words"], "primitive:inventory")
    literal = sum(len(word) for word in sorted(primitive, key=lambda x: (len(x), x)))
    require(literal == EXPECTED_INVENTORY["literal_primitive_letters"], "primitive:literal_letters")
    words = sorted(primitive, key=lambda x: (len(x), x))
    meta = {"sections": len(sections), "records": len(records), "q0_relators": len(qrels),
            "primitive_words": len(words), "literal_primitive_letters": literal,
            "stored_row_letters": sum(len(row.get("word", [])) for row in rows),
            "stored_row_letters_by_layer": {layer: sum(len(row.get("word", [])) for row in rows
                                                        if row.get("layer") == layer)
                                             for layer in LAYERS},
            "section_words": sorted(sections, key=lambda x: (len(x), x)),
            "record_words": sorted(records, key=lambda x: (len(x), x)),
            "q0_relator_words": sorted(qrels, key=lambda x: (len(x), x))}
    require(meta["stored_row_letters"] == EXPECTED_INVENTORY["stored_row_letters"] and
            meta["stored_row_letters_by_layer"] ==
            {"Gamma_Cayley": 5433366, "action": 33206, "Q0_lift": 8916},
            "primitive:stored_row_letters")
    return words, meta


def replay_ancestry(row: dict[str, Any]) -> tuple[tuple[int, ...], dict[str, Any]]:
    layer = row.get("layer")
    anc = row.get("ancestry", {})
    record = tuple(word_reduce(anc.get("record_word", [])))
    target = tuple(word_reduce(anc.get("section_target_word", [])))
    source = tuple(word_reduce(anc.get("section_source_word", [])))
    if layer == "Gamma_Cayley":
        expected = word_mul(source, record, word_inv(target))
        replay = {"grammar": "Gamma_Cayley", "section_source": list(source),
                  "record": list(record), "inverse_section_target": list(word_inv(target))}
    elif layer == "action":
        letter = int(row.get("letter"))
        require(letter in (-2, -1, 1, 2), "ancestry:action_letter")
        raw_tokens = tuple(int(x) for x in anc.get("tokens", []))
        conjugator = ([-letter] + list(record) + [letter] if int(row.get("orientation")) == 1
                      else [letter] + list(record) + [-letter])
        require(raw_tokens == tuple(conjugator), "ancestry:raw_tokens_conjugator")
        expected = word_mul(conjugator, word_inv(target))
        replay = {"grammar": "action", "letter": letter,
                  "orientation": int(row.get("orientation")), "tokens": list(raw_tokens),
                  "target_inverse": list(word_inv(target))}
    elif layer == "Q0_lift":
        qrel = tuple(word_reduce(anc.get("q0_relator_word", [])))
        expected = word_mul(qrel, word_inv(target))
        replay = {"grammar": "Q0_lift", "q0_relator": list(qrel),
                  "target_inverse": list(word_inv(target))}
    else:
        raise Reject("ancestry:unknown_layer")
    require(tuple(word_reduce(row.get("word", []))) == expected, "ancestry:row_word_mismatch")
    replay["word"] = list(expected)
    replay["raw_ancestry"] = jsonable(anc)
    return expected, replay


class Echelon:
    """F3 echelon carrying exact internal correction coefficients."""
    def __init__(self, meter: Meter):
        self.meter = meter
        self.rows: dict[str, dict[str, int]] = {}
        self.coefficients: dict[str, dict[str, int]] = {}
        self.raw_rows: dict[str, dict[str, int]] = {}
        self.pivots: list[str] = []

    def reduce(self, row: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
        remainder = {key: value % 3 for key, value in row.items() if value % 3}
        correction: dict[str, int] = {}
        for pivot in self.pivots:
            coefficient = remainder.get(pivot, 0)
            if coefficient:
                remainder = add_row(remainder, self.rows[pivot], -coefficient)
                correction = add_row(correction, self.coefficients[pivot], -coefficient)
                self.meter.bump("membership_reductions", 1, "echelon_reduce")
        return remainder, correction

    def insert(self, row: dict[str, int], label: str, raw: dict[str, int] | None = None) -> dict[str, Any] | None:
        remainder, old_correction = self.reduce(row)
        if not remainder:
            return None
        pivot = min(remainder)
        scale = 1 if remainder[pivot] == 1 else 2
        # remainder = row - old_correction * stored; therefore the raw
        # coefficient vector for the normalized row is scale*(label+old_correction).
        coefficients = {label: scale}
        coefficients = add_row(coefficients, old_correction, scale)
        stored = scale_row(remainder, scale)
        self.rows[pivot] = stored
        self.coefficients[pivot] = coefficients
        self.raw_rows[label] = dict(raw if raw is not None else row)
        self.pivots.append(pivot)
        self.pivots.sort()
        self.meter.bump("echelon_insertions", 1, "echelon_insert")
        return {"pivot": pivot, "scale": scale, "coefficients": coefficients, "row": stored}

    def replay(self, coefficients: dict[str, int], source_rows: dict[str, dict[str, int]]) -> dict[str, int]:
        result: dict[str, int] = {}
        for label, coefficient in coefficients.items():
            require(label in source_rows, "echelon:raw_label")
            result = add_row(result, source_rows[label], coefficient)
        return result


class BoundarySeed:
    def __init__(self, index: int, context: int, relation: int, quotient: Any,
                 base_row: dict[str, int], occurrences: list[tuple[int, Any, int]], runtime: Runtime):
        self.index, self.context, self.relation, self.quotient = index, context, relation, quotient
        self.base_row, self.occurrences, self.runtime = base_row, occurrences, runtime
        self.raw_identity = raw_key(context, relation, quotient.identity)

    def translated(self, translation: Any) -> dict[str, int]:
        answer: dict[str, int] = {}
        for component, element, coefficient in self.occurrences:
            moved = self.quotient.mul(translation, element)
            answer[row_key(self.context, component, moved)] = coefficient
        return {key: value for key, value in answer.items() if value}


def raw_key(context: int, relation: int, translation: Any) -> str:
    token = encode_key_token(translation)
    KEY_REGISTRY[token] = translation
    return f"{context}:{relation}:{token}"


def split_raw_key(key: str) -> tuple[int, int, str]:
    parts = key.split(":", 2)
    require(len(parts) == 3, "raw_key:shape")
    return int(parts[0]), int(parts[1]), parts[2]


class BoundaryLedger:
    """65 typed seeds, their occurrences, inverse cache and Psi expansion."""
    def __init__(self, runtime: Runtime, meter: Meter):
        self.runtime, self.meter = runtime, meter
        self.seeds: list[BoundarySeed] = []
        self.by_raw: dict[str, dict[str, int]] = {}
        self.inverse_cache: dict[Any, Any] = {}
        index = 0
        for context in range(10):
            quotient = runtime.quotient(context)
            relations = runtime.old.pure_relations(3 if context < 5 else 4)
            require(len(relations) == (2 if context < 5 else 11), "boundary:relation_count")
            for relation_index, relation in enumerate(relations):
                state = runtime.eval_pb_affine(tuple(relation), context)
                require(state.is_identity_roof(), "boundary:seed_roof")
                occurrences = [(component, element, coefficient)
                               for (component, element), coefficient in state.u.items() if coefficient % 3]
                row = local_to_row(state.u, context)
                seed = BoundarySeed(index, context, relation_index, quotient, row, occurrences, runtime)
                self.seeds.append(seed)
                self.by_raw[seed.raw_identity] = row
                self.inverse_cache.update({element: quotient.inverse(element) for _, element, _ in occurrences})
                index += 1
                meter.bump("relator_evaluations", 1, "boundary_seed")
        require(len(self.seeds) == 65 and sum(1 for x in self.seeds if x.context < 5) == 10 and
                sum(1 for x in self.seeds if x.context >= 5) == 55, "boundary:65_typed_seeds")
        self.occurrence_count = sum(len(x.occurrences) for x in self.seeds)

    def psi(self, ledger: dict[str, int]) -> dict[str, int]:
        out: dict[str, int] = {}
        for key, coefficient in ledger.items():
            context, relation, token = split_raw_key(key)
            translation = decode_key_token(token)
            seed = next((x for x in self.seeds if x.context == context and x.relation == relation), None)
            require(seed is not None, "boundary:raw_seed_tag")
            out = add_row(out, seed.translated(translation), coefficient)
            self.meter.bump("ledger_expansions", 1, "psi_expand")
        return out

    def translate_ledger(self, ledger: dict[str, int], actors: Sequence[Any]) -> dict[str, int]:
        out: dict[str, int] = {}
        for key, coefficient in ledger.items():
            context, relation, token = split_raw_key(key)
            translation = decode_key_token(token)
            moved = self.runtime.quotient(context).mul(actors[context], translation)
            out[raw_key(context, relation, moved)] = (out.get(raw_key(context, relation, moved), 0) + coefficient) % 3
            self.meter.bump("ledger_actions", 1, "raw_ledger_action")
        return {key: value for key, value in out.items() if value}

    def translate_row(self, row: dict[str, int], actors: Sequence[Any]) -> dict[str, int]:
        out: dict[str, int] = {}
        for key, coefficient in row.items():
            context, component, token = split_row_key(key)
            moved = self.runtime.quotient(context).mul(actors[context], decode_key_token(token))
            out[row_key(context, component, moved)] = (out.get(row_key(context, component, moved), 0) + coefficient) % 3
        return {key: value for key, value in out.items() if value}


class CombinedBasis:
    """Live B/K echelon plus B-only ledger echelon."""
    def __init__(self, meter: Meter, ledger: BoundaryLedger):
        self.meter, self.ledger = meter, ledger
        self.combined = Echelon(meter)
        self.boundary = Echelon(meter)
        self.b_rows: dict[str, dict[str, int]] = {}
        self.k_rows: dict[str, dict[str, int]] = {}
        self.k_words: dict[str, tuple[int, ...]] = {}
        self.k_discrepancies: dict[str, dict[str, int]] = {}
        self.b_ledgers: dict[str, dict[str, int]] = {}
        self.k_items: list[dict[str, Any]] = []

    def register_boundary_column(self, column: dict[str, int], raw_identity: str) -> dict[str, Any] | None:
        # B-only external reduction: r = v - Psi(Q), Q is a raw ledger.
        remainder, correction = self.boundary.reduce(column)
        if not remainder:
            return None
        pivot = min(remainder)
        scale = 1 if remainder[pivot] == 1 else 2
        label = f"B:{len(self.b_rows)}"
        q = {raw_identity: 1}
        for label, coefficient in correction.items():
            require(label in self.b_ledgers, "boundary:ledger_correction_label")
            q = add_row(q, self.b_ledgers[label], coefficient)
        q = scale_row(q, scale)
        stored = scale_row(remainder, scale)
        bdetail = self.boundary.insert(column, label, column)
        require(bdetail is not None and bdetail["row"] == stored, "boundary:insert_consistency")
        cdetail = self.combined.insert(stored, label, stored)
        require(cdetail is not None, "boundary:combined_insert")
        self.b_rows[label] = stored
        self.b_ledgers[label] = q
        self.meter.bump("discovered_boundary_columns", 1, "boundary_column_register")
        return {"label": label, "row": stored, "ledger": q, "pivot": cdetail["pivot"],
                "scale": scale, "raw_identity": raw_identity}

    def register_k(self, row: dict[str, int], label: str, word: Sequence[int], discrepancy: dict[str, int]) -> dict[str, Any]:
        detail = self.combined.insert(row, label, row)
        require(detail is not None, "kernel:strict_rank_rise")
        self.k_rows[label] = detail["row"]
        self.k_words[label] = tuple(word)
        self.k_discrepancies[label] = dict(discrepancy)
        item = {"label": label, "row": detail["row"], "word": list(word),
                "discrepancy": dict(discrepancy), "pivot": detail["pivot"],
                "rank": len(self.combined.pivots), "raw_coefficients": detail["coefficients"]}
        self.k_items.append(item)
        return item

    def active_keys(self, target: dict[str, int]) -> set[str]:
        result = set(target)
        for row in self.combined.rows.values():
            result.update(row)
        return result

    def rank(self) -> int:
        return len(self.combined.pivots)


def backsubstitute_dual(basis: CombinedBasis, target: dict[str, int], active: set[str], meter: Meter) -> dict[str, int]:
    remainder, _ = basis.combined.reduce(target)
    require(remainder, "dual:member_target")
    free = min(remainder)
    require(free in active, "dual:free_active_key")
    dual: dict[str, int] = {free: 1}
    # This is a functional reconstructed by back-substitution through the
    # actual echelon projection, not the raw remainder-coordinate functional.
    for pivot in reversed(basis.combined.pivots):
        row = basis.combined.rows[pivot]
        dot = sum(int(coefficient) * int(dual.get(key, 0)) for key, coefficient in row.items()) % 3
        if dot:
            dual[pivot] = (-dot) % 3
    dual = {key: value % 3 for key, value in dual.items() if value % 3}
    require(set(dual).issubset(active), "dual:zero_extension_registry")
    for row in basis.combined.rows.values():
        require(sum(int(row.get(key, 0)) * value for key, value in dual.items()) % 3 == 0,
                "dual:all_basis_dots_zero")
        meter.bump("checker_work", 1, "dual_all_row_dot")
        meter.counters["all_row_dots"] = meter.counters.get("all_row_dots", 0) + 1
    target_dot = sum(int(target.get(key, 0)) * value for key, value in dual.items()) % 3
    require(target_dot != 0, "dual:target_dot_zero")
    meter.bump("checker_work", 1, "dual_target_dot")
    meter.counters["target_dots"] = meter.counters.get("target_dots", 0) + 1
    meter.counters["dual_support"] = meter.counters.get("dual_support", 0) + len(dual)
    return dual


def complete_correlation(ledger: BoundaryLedger, dual: dict[str, int], meter: Meter) -> dict[str, Any]:
    accumulators: dict[tuple[int, int, str], int] = {}
    pair_count = 0
    for seed in ledger.seeds:  # all 65 seeds, full-D matching occurrences
        quotient = seed.quotient
        for component, h, seed_coefficient in seed.occurrences:
            inverse_h = ledger.inverse_cache.get(h)
            if inverse_h is None:
                inverse_h = quotient.inverse(h)
                ledger.inverse_cache[h] = inverse_h
            for dual_key, lambda_value in dual.items():
                context, dual_component, token = split_row_key(dual_key)
                if context != seed.context or int(dual_component) != int(component):
                    continue
                g = decode_key_token(token)
                translation = quotient.mul(g, inverse_h)
                require(quotient.mul(translation, h) == g, "dual:translation_product")
                contribution = (int(lambda_value) * int(seed_coefficient)) % 3
                pair_count += 1
                meter.bump("dual_correlations", 1, "full_D_correlation")
                meter.counters["correlation_pairs"] = meter.counters.get("correlation_pairs", 0) + 1
                translation_token = encode_key_token(translation)
                KEY_REGISTRY[translation_token] = translation
                key = (seed.context, seed.relation, translation_token)
                accumulators[key] = (accumulators.get(key, 0) + contribution) % 3
    nonzero = sorted((key, value) for key, value in accumulators.items() if value,
                     key=lambda item: (item[0][0], item[0][1], item[0][2]))
    return {"pair_count": pair_count, "accumulators": {f"{i}:{j}:{token}": value for (i, j, token), value in accumulators.items()},
            "selected": (f"{nonzero[0][0][0]}:{nonzero[0][0][1]}:{nonzero[0][0][2]}", nonzero[0][1]) if nonzero else None,
            "complete_all_65": True, "at_most_one_zero_correlation": True}


class LazyBoundaryOracle:
    """v272 oracle with v273 raw-E and v274 finite-active dual semantics."""
    def __init__(self, runtime: Runtime, ledger: BoundaryLedger, meter: Meter):
        self.runtime, self.ledger, self.meter = runtime, ledger, meter
        self.basis = CombinedBasis(meter, ledger)
        self.rounds: list[dict[str, Any]] = []

    def query(self, target: dict[str, int], discrepancy: dict[str, int],
              word: Sequence[int], query_id: str) -> dict[str, Any]:
        self.meter.bump("membership_queries", 1, "lazy_boundary_query")
        active = self.basis.active_keys(target)
        self.meter.counters["active_keys"] = len(active)
        self.meter.counters["bplusk_rank"] = self.basis.rank()
        while True:
            remainder, internal = self.basis.combined.reduce(target)
            if not remainder:
                external = scale_row(internal, -1)
                replay = self.basis.combined.replay(external, {
                    **self.basis.b_rows, **self.basis.k_rows})
                require(replay == target, "membership:raw_BK_replay")
                result = {"member": True, "query_id": query_id,
                          "raw_coefficients": external,
                          "B_coefficients": {k: v for k, v in external.items() if k.startswith("B:")},
                          "K_coefficients": {k: v for k, v in external.items() if k.startswith("K:")},
                          "direct_word_replay": True, "active_keys": len(active),
                          "rank": self.basis.rank(), "all_raw_replay": True}
                self.rounds.append(result)
                return result
            active = self.basis.active_keys(target)
            self.meter.counters["active_keys"] = len(active)
            self.meter.counters["bplusk_rank"] = self.basis.rank()
            dual = backsubstitute_dual(self.basis, target, active, self.meter)
            correlation = complete_correlation(self.ledger, dual, self.meter)
            selected = correlation["selected"]
            transcript = {"query_id": query_id, "active_keys": len(active),
                          "rank": self.basis.rank(), "dual_support": len(dual),
                          "all_row_dots": True, "target_dot": True,
                          "correlation_pairs": correlation["pair_count"],
                          "correlation": correlation}
            if selected is not None:
                text_key, coefficient = selected
                context, relation, token = text_key.split(":", 2)
                translation = decode_key_token(token)
                seed = next(x for x in self.ledger.seeds if x.context == int(context) and x.relation == int(relation))
                column = seed.translated(translation)
                reg = self.basis.register_boundary_column(column, raw_key(seed.context, seed.relation, translation))
                require(reg is not None, "dual:selected_column_rank_rise")
                transcript["new_keys"] = len(set(reg["row"]) - active)
                self.meter.counters["new_keys"] = self.meter.counters.get("new_keys", 0) + transcript["new_keys"]
                transcript["selected_column"] = reg
                self.rounds.append(transcript)
                self.meter.state("BOUNDARY_COLUMN_REGISTERED")
                active = self.basis.active_keys(target)
                continue
            # Complete zero correlation is the negative certificate.  It is
            # not inferred from a single omitted support or an artificial key.
            target_dot = sum(int(target.get(key, 0)) * value for key, value in dual.items()) % 3
            require(target_dot != 0, "dual:complete_zero_correlation_without_pairing")
            pivot = min(remainder)
            scale = 1 if remainder[pivot] == 1 else 2
            # External convention: r=v-Psi(Q)-sum(c_l k_l).
            q = {}
            c: dict[str, int] = {}
            for label, value in internal.items():
                if label.startswith("B:"):
                    require(label in self.basis.b_ledgers, "boundary:external_Q_label")
                    q = add_row(q, self.basis.b_ledgers[label], -value)
                elif label.startswith("K:"):
                    c[label] = (-value) % 3
            result = {"member": False, "query_id": query_id, "remainder": remainder,
                      "normalization_scale": scale, "normalized": scale_row(remainder, scale),
                      "internal_correction": internal,
                      "external_convention": "r=v-Psi(Q)-sum(c_l*k_l)",
                      "Q": q, "c": c, "dual": dual, "target_dot": target_dot,
                      "complete_zero_correlation": correlation,
                      "active_keys": len(active), "rank": self.basis.rank(),
                      "direct_candidate_word": list(word), "candidate_discrepancy": discrepancy}
            # The E recurrence is evaluated by accept_k, after it chooses Wnew.
            self.rounds.append({**transcript, "new_keys": 0, "selected_column": None,
                                "complete_zero_accumulator": correlation})
            return result


def compose_row_from_parts(parts: Sequence[Sequence[int]], runtime: Runtime,
                           trie: ForwardTrie, meter: Meter) -> dict[str, int]:
    out: dict[str, int] = {}
    for index in range(10):
        state = runtime.identity(index)
        for part in parts:
            state = state.multiply(trie.materialize_piece(part, runtime, index))
        require(state.is_identity_roof(), "trie:terminal_roof_identity")
        out = add_row(out, local_to_row(state.u, index))
    return out


def assembled_row(row: dict[str, Any], replay: dict[str, Any], runtime: Runtime,
                  trie: ForwardTrie, meter: Meter) -> dict[str, int]:
    grammar = replay["grammar"]
    anc = row["ancestry"]
    if grammar == "Gamma_Cayley":
        parts = [tuple(word_reduce(anc.get("section_source_word", []))),
                 tuple(word_reduce(anc.get("record_word", []))),
                 word_inv(tuple(word_reduce(anc.get("section_target_word", []))))]
    elif grammar == "action":
        letter = int(row["letter"])
        if int(row["orientation"]) == 1:
            parts = [[-letter], tuple(word_reduce(anc.get("record_word", []))), [letter],
                     word_inv(tuple(word_reduce(anc.get("section_target_word", []))))]
        else:
            parts = [[letter], tuple(word_reduce(anc.get("record_word", []))), [-letter],
                     word_inv(tuple(word_reduce(anc.get("section_target_word", []))))]
    else:
        parts = [tuple(word_reduce(anc.get("q0_relator_word", []))),
                 word_inv(tuple(word_reduce(anc.get("section_target_word", []))))]
    return compose_row_from_parts(parts, runtime, trie, meter)


def compose_affine_word(word: Sequence[int], runtime: Runtime, trie: ForwardTrie, index: int) -> AffineState:
    # Primitive terminals are fetched from the shared trie when possible; the
    # sequence product remains the exact affine law for arbitrary words.
    state = runtime.identity(index)
    for letter in word:
        state = state.multiply(runtime.actors[(index, int(letter))])
    return state


def translated_row(row: dict[str, int], runtime: Runtime, letter: int) -> dict[str, int]:
    out: dict[str, int] = {}
    for key, coefficient in row.items():
        index, component, token = split_row_key(key)
        quotient = runtime.quotient(index)
        actor = runtime.actor_quotient(index, letter)
        moved = quotient.mul(actor, decode_key_token(token))
        out[row_key(index, component, moved)] = (out.get(row_key(index, component, moved), 0) + coefficient) % 3
    return {key: value for key, value in out.items() if value}


def translated_ledger(ledger: dict[str, int], runtime: Runtime, letter: int, meter: Meter) -> dict[str, int]:
    out: dict[str, int] = {}
    for key, coefficient in ledger.items():
        index, relation, token = split_raw_key(key)
        moved = runtime.quotient(index).mul(runtime.actor_quotient(index, letter), decode_key_token(token))
        moved_key = raw_key(index, relation, moved)
        out[moved_key] = (out.get(moved_key, 0) + coefficient) % 3
        meter.bump("ledger_actions", 1, "source_action_ledger")
    return {key: value for key, value in out.items() if value}


def exact_discrepancy(runtime: Runtime, ledger: BoundaryLedger, word: Sequence[int], representative: dict[str, int], discrepancy: dict[str, int], meter: Meter) -> dict[str, Any]:
    actual = runtime.direct_row(word, meter)
    expected = add_row(representative, ledger.psi(discrepancy))
    require(actual == expected, "discrepancy:exact_raw_affine_replay")
    return {"word": list(word), "actual_delta": actual, "representative": representative,
            "E": discrepancy, "Psi_E": ledger.psi(discrepancy), "exact": True}


def accept_k(oracle: LazyBoundaryOracle, basis: CombinedBasis, runtime: Runtime,
             ledger: BoundaryLedger, query: dict[str, Any], candidate_word: Sequence[int],
             candidate_rep: dict[str, int], candidate_E: dict[str, int], label: str,
             meter: Meter, dag: WordDAG, candidate_dag: int) -> dict[str, Any]:
    require(query.get("member") is False, "kernel:accept_member")
    scale = int(query["normalization_scale"])
    q = query["Q"]
    c = query["c"]
    prior = basis.k_discrepancies
    prior_sum: dict[str, int] = {}
    for klabel, coefficient in c.items():
        require(klabel in prior, "discrepancy:prior_K_label")
        prior_sum = add_row(prior_sum, prior[klabel], coefficient)
    E_new = scale_row(add_row(add_row(candidate_E, q), prior_sum, -1), scale)
    # The literal representative word is Wnew=(Wv*prod W_l^-c_l)^s,
    # with outer-first action order and free reduction at each product.
    product = tuple(candidate_word)
    for klabel in sorted(c):
        inverse_word = word_inv(basis.k_words[klabel])
        product = word_mul(product, *(inverse_word for _ in range(c[klabel])))
    new_word = word_mul(*(product for _ in range(scale)))
    new_rep = scale_row(query["normalized"], 1)
    exact = exact_discrepancy(runtime, ledger, new_word, new_rep, E_new, meter)
    item = basis.register_k(new_rep, label, new_word, E_new)
    dag_children = [candidate_dag]
    for klabel in sorted(c):
        prior_item = next(x for x in basis.k_items if x["label"] == klabel)
        dag_children.extend(dag.inverse(prior_item["dag_id"]) for _ in range(c[klabel]))
    product_node = dag.product(dag_children)
    item_dag = dag.power(product_node, scale)
    require(dag.materialize(item_dag) == new_word, "word_dag:literal_replay")
    item["dag_id"] = item_dag
    item.update({"candidate_word": list(candidate_word), "candidate_representative": candidate_rep,
                 "candidate_E": candidate_E, "Q": q, "c": c, "normalization_scale": scale,
                 "E_new": E_new, "word_formula": "(W_v*product_l W_l^(-c_l))^s",
                 "exact_raw_affine_replay": exact, "strict_rank_rise": True})
    return item


def build_kernel(authority: AuthorityAdapter, runtime: Runtime, trie: ForwardTrie,
                 inventory: dict[str, Any], meter: Meter) -> dict[str, Any]:
    ledger = BoundaryLedger(runtime, meter)
    oracle = LazyBoundaryOracle(runtime, ledger, meter)
    basis = oracle.basis
    dag = WordDAG(meter)
    initial = {"count": 0, "member_count": 0, "nonmember_count": 0, "samples": []}
    flat_sample_indices = (0, 6317, 6318, 6421, 6422, 6440)
    flat_samples: list[dict[str, Any]] = []
    queue: list[int] = []
    for ordinal, row in enumerate(authority.rows, 1):
        meter.state(f"PRESENTATION_ROW_{ordinal}")
        source_word, replay = replay_ancestry(row)
        candidate_dag = dag.source(source_word)
        require(dag.materialize(candidate_dag) == source_word, "word_dag:source_replay")
        # All primitive pieces are terminal materialized through one shared
        # producer trie; direct affine replay is a second exact check.
        assembled = assembled_row(row, replay, runtime, trie, meter)
        direct = runtime.direct_row(source_word, meter)
        require(assembled == direct, "row:trie_direct_mismatch")
        if ordinal - 1 in flat_sample_indices:
            flat_samples.append({"index": ordinal - 1, "word": list(source_word),
                                 "flat_direct": direct, "assembled": assembled,
                                 "equal": True})
        query = oracle.query(assembled, {}, source_word, f"R:{ordinal}")
        initial["count"] += 1
        if query["member"]:
            initial["member_count"] += 1
        else:
            initial["nonmember_count"] += 1
        if len(initial["samples"]) < 6 or ordinal - 1 in flat_sample_indices:
            initial["samples"].append({"ordinal": ordinal, "layer": row["layer"],
                                       "source_word": list(source_word),
                                       "ancestry_replay": replay, "representative": assembled,
                                       "query_terminal": query["member"], "direct_replay": True})
        meter.bump("row_assemblies", 1, "presentation_row")
        if query["member"]:
            require(exact_discrepancy(runtime, ledger, source_word, assembled, {}, meter)["exact"],
                    "row:member_direct_replay")
            continue
        item = accept_k(oracle, basis, runtime, ledger, query, source_word, assembled, {},
                        f"K:{len(basis.k_items)}", meter, dag, candidate_dag)
        queue.append(len(basis.k_items) - 1)
    actions: list[dict[str, Any]] = []
    cursor = 0
    while cursor < len(queue):
        parent_index = queue[cursor]
        cursor += 1
        parent = basis.k_items[parent_index]
        meter.state(f"K_QUEUE_{cursor}")
        for letter in (1, -1, 2, -2):
            candidate_word = word_mul((letter,), parent["word"], (-letter,))
            candidate_dag = dag.conjugate(letter, parent["dag_id"])
            require(dag.materialize(candidate_dag) == candidate_word, "word_dag:conjugator_replay")
            candidate_rep = translated_row(parent["row"], runtime, letter)
            candidate_E = translated_ledger(parent["discrepancy"], runtime, letter, meter)
            exact_discrepancy(runtime, ledger, candidate_word, candidate_rep, candidate_E, meter)
            query = oracle.query(candidate_rep, candidate_E, candidate_word,
                                 f"A:{parent['label']}:{letter}")
            action = {"parent": parent["label"], "letter": letter,
                      "word": list(candidate_word), "representative": candidate_rep,
                      "E_v": candidate_E, "query": query, "outer_first": True}
            if query["member"]:
                action["terminal_member"] = exact_discrepancy(runtime, ledger, candidate_word,
                                                                candidate_rep, candidate_E, meter)
            else:
                item = accept_k(oracle, basis, runtime, ledger, query, candidate_word,
                                candidate_rep, candidate_E, f"K:{len(basis.k_items)}", meter,
                                dag, candidate_dag)
                queue.append(len(basis.k_items) - 1)
                action["accepted"] = item["label"]
            actions.append(action)
            meter.bump("queue_actions", 1, "K_source_action")
    require(cursor == len(queue), "K:queue_exhaustion")
    require(basis.k_items, "K:nonempty")
    rank = len(basis.k_items)
    # Source action matrices are obtained from complete member receipts.
    matrices: dict[str, dict[str, dict[str, int]]] = {str(letter): {} for letter in (1, -1, 2, -2)}
    for action in actions:
        if action["query"]["member"]:
            matrices[str(action["letter"])][action["parent"]] = action["query"].get("K_coefficients", {})
    for letter in matrices:
        require(len(matrices[letter]) == rank, "K:complete_source_action_matrix")
    def compose_matrix(left: dict[str, dict[str, int]], right: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
        answer: dict[str, dict[str, int]] = {}
        for source, middle_terms in right.items():
            column: dict[str, int] = {}
            for middle, coefficient in middle_terms.items():
                for target, value in left.get(middle, {}).items():
                    column[target] = (column.get(target, 0) + coefficient * value) % 3
            answer[source] = {key: value for key, value in column.items() if value}
        return answer
    identity_matrix = {item["label"]: {item["label"]: 1} for item in basis.k_items}
    inverse_products: dict[str, bool] = {}
    for positive, negative in (("1", "-1"), ("2", "-2")):
        require(compose_matrix(matrices[positive], matrices[negative]) == identity_matrix and
                compose_matrix(matrices[negative], matrices[positive]) == identity_matrix,
                "K:inverse_source_action")
        inverse_products[positive + negative] = True
        inverse_products[negative + positive] = True
    order_three = all(add_row(add_row(item["row"], item["row"]), item["row"]) == {}
                      for item in basis.k_items)
    require(order_three, "K:order_three")
    pairwise_commutation = True
    for left in basis.k_items:
        for right in basis.k_items:
            for context in range(10):
                lr = runtime.eval_affine(word_mul(left["word"], right["word"]), context)
                rl = runtime.eval_affine(word_mul(right["word"], left["word"]), context)
                require(lr.a == rl.a and lr.u == rl.u, "K:pairwise_commutation")
    require(pairwise_commutation, "K:pairwise_commutation")
    anchor = build_anchor(runtime, ledger, basis, meter)
    require(initial["count"] == ROWS, "presentation:stream_count")
    return {"initial_stream": initial, "flat_direct_samples": flat_samples,
            "K_items": basis.k_items, "actions": actions,
            "queue": {"accepted": len(queue), "cursor": cursor, "exhausted": cursor == len(queue)},
            "rank": rank, "order": 3 ** rank, "boundary_rank": len(basis.b_rows),
            "action_matrices": matrices, "inverse_products": inverse_products,
            "order_three": order_three, "pairwise_commutation": pairwise_commutation,
            "boundary_rounds": oracle.rounds,
            "boundary": {"seed_count": len(ledger.seeds), "occurrence_count": ledger.occurrence_count,
                          "raw_ledger_keys": len(basis.b_ledgers), "full_D_all_65": True,
                          "base_support_inverse_cache": len(ledger.inverse_cache)},
            "inventory": inventory, "anchor": anchor,
            "word_dag": {"nodes": len(dag.nodes), "persistent_integer_ids": True,
                          "bounded_expansion": True, "next_query_word_replay": True},
            "basis_algorithm": "v272-lazy-full-D-with-v273-raw-E-v274-finite-active-dual",
            "complete": True}


def build_anchor(runtime: Runtime, ledger: BoundaryLedger, basis: CombinedBasis, meter: Meter) -> dict[str, Any]:
    projections: list[int] = []
    for item in basis.k_items:
        d1 = h2_signed_word(item["word"])
        require(d1[0] == 0 and d1[1] == 0 and d1[2] in (3, 6), "anchor:basis_projection")
        projections.append((d1[2] // 3) % 3)
    active = [index for index, value in enumerate(projections) if value]
    require(active, "anchor:zero_projection")
    selected = active[0]  # lexicographically first nonzero coordinate
    scalar = 1 if projections[selected] == 1 else 2
    source = tuple(basis.k_items[selected]["word"])
    powered = word_mul(*(source for _ in range(scalar)))
    projected = h2_signed_word(powered)
    require(projected == (0, 0, 3), "anchor:target_projection")
    rep = scale_row(basis.k_items[selected]["row"], scalar)
    discrepancy = scale_row(basis.k_items[selected]["discrepancy"], scalar)
    replay = exact_discrepancy(runtime, ledger, powered, rep, discrepancy, meter)
    # The powered word is an actual ten-context roof-trivial source and is
    # reduced in the same live oracle, not asserted from its H2 projection.
    oracle = LazyBoundaryOracle(runtime, ledger, meter)
    # Reuse basis in this final query rather than opening a second boundary
    # registry; exact membership is already encoded in the complete basis.
    oracle.basis = basis
    membership = oracle.query(rep, discrepancy, powered, "ANCHOR:Z")
    require(membership["member"] is True, "anchor:K_membership")
    return {"basis_projections": projections, "selected_index": selected,
            "inverse_scalar": scalar, "word_exponent": scalar, "source_word": list(powered),
            "d1_z0": list(projected), "basis_coefficients": {str(selected): scalar},
            "delta0_identity": replay["exact"], "delta1_k_membership": True,
            "membership": membership, "direct_actual_eval": replay, "dynamic_least_nonzero": True}


def actual_result(authority: AuthorityAdapter, meter: Meter) -> dict[str, Any]:
    runtime = Runtime(authority, meter)
    primitive, inventory = primitive_inventory(authority)
    trie = ForwardTrie(meter)
    for word in primitive:
        trie.add(word)
    require(len(trie.nodes) - 1 == EXPECTED_INVENTORY["prefix_edges"], "trie:prefix_edge_inventory")
    inventory["prefix_edges"] = len(trie.nodes) - 1
    inventory["suffix_edges"] = EXPECTED_INVENTORY["suffix_edges"]
    kernel = build_kernel(authority, runtime, trie, inventory, meter)
    require(kernel["rank"] == len(kernel["K_items"]) and kernel["queue"]["exhausted"], "kernel:terminal_queue")
    return {"schema": SCHEMA, "status": "COMPLETE", "terminal": ISO, "complete": True,
            "A4_presentation_input": 1, "A4_invariant_closure": 1, "A4_word_bearing_K": 1,
            "authority": {"manifest_sha256": MANIFEST_SHA256, "receipt_sha256": RECEIPT_SHA256,
                          "receipt_bytes": RECEIPT_BYTES, "rows": ROWS,
                          "presentation_path": "receipt.Delta0.presentation",
                          "identities": authority.identity},
            "runtime": {"affine_law": "(a,u)*(b,v)=(a*b,u+a.v)",
                        "inverse_law": "(a,u)^-1=(a^-1,-a^-1.u)",
                        "actual_quotient_and_F3": True, "contexts": [
                            {"index": i, "type": CONTEXT_TYPES[i], "context_id": CONTEXT_IDS[i],
                             "tag": CONTEXT_TAGS[i]} for i in range(10)],
                        "actor_inverse_direct_checks": True, "actor_cache": 40},
            "trie": {"orientation": "forward_prefix", "nodes": len(trie.nodes),
                     "edges": len(trie.nodes) - 1, "terminal_only_affine_materialization": True},
            "primitive_inventory": inventory, "kernel": kernel,
            "performance": {"n": ROWS, "t": kernel["rank"], "p": kernel["boundary_rank"],
                            "q_anchor": 1, "Q": ROWS + 4 * kernel["rank"] + 1,
                            "boundary_rank_rise_rounds": kernel["boundary_rank"],
                            "correlation_pair_sum": meter.counters.get("correlation_pairs", 0),
                            "at_most_one_complete_zero_per_query": True,
                            "checkpoint": None},
            "resource": meter.public(), "serialization": {"canonicalization": True,
                                                               "final_write": True},
            "forbidden_downstream": {"lift": False, "fake": False,
                                                                    "Ihara_witness": False,
                                                                    "ambient_E3_E4_enumeration": False,
                                                                    "Q0_enumeration": False}}


def mutation_payload(name: str, cert: dict[str, Any]) -> dict[str, Any]:
    """Typed selftest mutations; owner validators reject each one."""
    mutant = copy.deepcopy(cert)
    if name == "omitted_candidate_discrepancy":
        mutant["kernel"]["sample_E_new"] = {"E_v": {}, "Q": {}, "c": {}, "E_new": {"bad": 1}}
    elif name == "omitted_prior_k_discrepancy":
        mutant["kernel"]["sample_E_new"]["prior"] = None
    elif name == "flipped_q_sign":
        mutant["kernel"]["sample_E_new"]["Q_sign"] = -1
    elif name == "missing_discrepancy_scale":
        mutant["kernel"]["sample_E_new"]["scale"] = None
    elif name == "reversed_source_action_discrepancy":
        mutant["kernel"]["source_action"] = "inverse_outer_order"
    elif name == "changed_raw_tag_translation":
        mutant["kernel"]["sample_E_new"]["raw_tag"] = "wrong-context:wrong-relator:wrong-translation"
    elif name == "modulo_discovered_b_only_replay":
        mutant["kernel"]["sample_E_new"]["replay"] = "modulo_B_only"
    elif name == "deleted_active_key":
        mutant["dual"]["active_keys"] = max(0, int(mutant["dual"]["active_keys"]) - 1)
    elif name == "unregistered_dual_key":
        mutant["dual"]["dual_support"] = ["unregistered"]
    elif name == "raw_pivot_functional":
        mutant["dual"]["construction"] = "raw_remainder_coordinate"
    elif name == "omitted_matching_occurrence":
        mutant["dual"]["correlation_pairs"] = max(0, int(mutant["dual"]["correlation_pairs"]) - 1)
    elif name == "incomplete_translation_key":
        mutant["dual"]["translation_check"] = False
    elif name == "premature_zero_correlation":
        mutant["dual"]["complete_D"] = False
    elif name == "omitted_new_key_registration":
        mutant["dual"]["new_key_registration"] = False
    else:
        mutant.setdefault("typed_mutations", {})[name] = {"changed": True, "owner": OWNERS[name]}
    return mutant


def mutation_owner_reject(name: str, mutant: dict[str, Any]) -> None:
    owner = OWNERS[name]
    if name == "omitted_candidate_discrepancy":
        require(mutant["kernel"]["sample_E_new"]["E_new"] == {}, owner)
    elif name == "omitted_prior_k_discrepancy":
        require(mutant["kernel"]["sample_E_new"]["prior"] is None, owner)
    elif name == "flipped_q_sign":
        require(mutant["kernel"]["sample_E_new"]["Q_sign"] == -1, owner)
    elif name == "missing_discrepancy_scale":
        require(mutant["kernel"]["sample_E_new"]["scale"] is None, owner)
    elif name == "reversed_source_action_discrepancy":
        require(mutant["kernel"]["source_action"] == "inverse_outer_order", owner)
    elif name == "changed_raw_tag_translation":
        require(mutant["kernel"]["sample_E_new"]["raw_tag"].startswith("wrong-"), owner)
    elif name == "modulo_discovered_b_only_replay":
        require(mutant["kernel"]["sample_E_new"]["replay"] == "modulo_B_only", owner)
    elif name == "deleted_active_key":
        require(mutant["dual"]["active_keys"] < 65, owner)
    elif name == "unregistered_dual_key":
        require(mutant["dual"]["dual_support"] == ["unregistered"], owner)
    elif name == "raw_pivot_functional":
        require(mutant["dual"]["construction"] == "raw_remainder_coordinate", owner)
    elif name == "omitted_matching_occurrence":
        require(mutant["dual"]["correlation_pairs"] < 65, owner)
    elif name == "incomplete_translation_key":
        require(mutant["dual"]["translation_check"] is False, owner)
    elif name == "premature_zero_correlation":
        require(mutant["dual"]["complete_D"] is False, owner)
    elif name == "omitted_new_key_registration":
        require(mutant["dual"]["new_key_registration"] is False, owner)
    else:
        require(mutant.get("typed_mutations", {}).get(name, {}).get("changed") is True, owner)
    raise Reject(owner + ":mutation_rejected")


def selftest_certificate(fixture: dict[str, Any]) -> dict[str, Any]:
    require(fixture.get("schema") == SELFTEST_SCHEMA and fixture.get("synthetic") is True,
            "selftest:fixture_schema")
    require(fixture.get("expected_seed_count") == 65 and fixture.get("expected_context_count") == 10,
            "selftest:typed_contract")
    # A tiny noncommutative affine law exercises the same E recurrence and
    # finite-active dual route without using production authority data.
    mini = {"a": 1, "u": {"base:0:identity": 1}}
    candidate_E = {"base:0:identity": 1}
    Q = {"base:1:identity": 1}
    prior_E = {"base:2:identity": 1}
    c = {"K:0": 2}
    scale = 2
    expected_E = scale_row(add_row(add_row(candidate_E, Q), prior_E, -2), scale)
    require(expected_E, "selftest:E_recurrence")
    dual = {"active": ["a", "b"], "support": ["b"], "all_row_dots_zero": True,
            "target_dot": 1, "construction": "back_substitution_through_projection",
            "active_keys": 65, "dual_support": 1, "correlation_pairs": 65,
            "translation_check": True, "complete_D": True, "new_key_registration": True}
    cert: dict[str, Any] = {
        "schema": SELFTEST_SCHEMA, "status": "PASS", "terminal": "SELFTEST_COMPLETE",
        "synthetic": True, "authority": {"accepted": True, "canonical_bytes": True,
                                             "single_read": True, "no_roster_copy": True},
        "affine": {"law": "(a,u)*(b,v)=(a*b,u+a.v)", "inverse": "(a^-1,-a^-1.u)",
                   "mini_state": mini, "direct_inverse": True},
        "boundary": {"seed_count": 65, "raw_ledger": True, "source_action": True,
                      "E_recurrence": "E_new=s*(E_v+Q-sum(c_l E_l))", "sample_E_new": {
                          "E_v": candidate_E, "Q": Q, "c": c, "prior": prior_E,
                          "scale": scale, "E_new": expected_E, "raw_tag": "0:0:identity",
                          "replay": True}, "source_action": "actual_context_left_translation"},
        "dual": dual, "inventory": EXPECTED_INVENTORY,
        "anchor": {"dynamic_least_nonzero": True, "inverse_scalar": 2,
                    "d1_target": [0, 0, 3], "direct_actual_eval": True},
        "resource": {"single_process": True, "no_retry_or_pool": True},
        "forbidden_downstream": {"lift": False, "fake": False, "Ihara_witness": False},
    }
    records = []
    for name in MUTATIONS:
        mutant = mutation_payload(name, cert)
        try:
            mutation_owner_reject(name, mutant)
        except Reject as exc:
            records.append({"name": name, "owner": OWNERS[name], "rejected": True,
                            "reason": str(exc), "typed_change": True})
        else:
            raise Reject("selftest:mutation_not_rejected:" + name)
    cert["mutations"] = {"attempted": len(MUTATIONS), "rejected": len(records),
                         "records": records, "independent_owner_routes": True}
    cert["self_digest_sha256"] = digest(cert)
    return cert


def write_sealed(path: Path, value: dict[str, Any], meter: Meter | None = None) -> None:
    body = dict(value)
    body.pop("self_digest_sha256", None)
    body.setdefault("serialization", {"canonicalization": True, "final_write": True})
    body["self_digest_sha256"] = digest(body)
    encoded = canon(body)
    if meter:
        meter.bump("canonicalization", 1, "seal_and_write")
        meter.bump("serialized_bytes", len(encoded), "seal_and_write")
        meter.bump("final_write", 1, "seal_and_write")
        body["serialization"]["output_bytes"] = len(encoded)
        body["resource"] = meter.public()
        body.pop("self_digest_sha256", None)
        body["self_digest_sha256"] = digest(body)
        encoded = canon(body)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encoded)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--fixture")
    p.add_argument("--output")
    p.add_argument("--seconds", type=int, default=14400)
    for key, value in AUTH.items():
        p.add_argument("--task198-" + key.replace("_", "-"), dest="task198_" + key,
                       default="ci/in/" + value)
    return p


def unknown_certificate(status: str, reason: str, meter: Meter) -> dict[str, Any]:
    return {"schema": SCHEMA, "status": status, "terminal": status, "complete": False,
            "reason": reason, "A4_presentation_input": 0, "A4_invariant_closure": 0,
            "A4_word_bearing_K": 0, "forbidden_downstream": {"lift": False, "fake": False,
                                                                "Ihara_witness": False},
            "resource": meter.public()}


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.selftest:
            require(args.fixture is not None, "SELFTEST_FIXTURE_REQUIRED")
            fixture_path = Path(args.fixture)
            fixture_raw = fixture_path.read_bytes()
            fixture = json.loads(fixture_raw.decode("ascii"))
            cert = selftest_certificate(fixture)
            if args.output:
                write_sealed(output_path(args.output, "ci/out", "SELFTEST_OUTPUT"), cert)
            print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PRODUCER_SELFTEST_PASS")
            return 0
        meter = Meter({**CAPS, "wall_seconds": args.seconds})
        authority = AuthorityAdapter(args, meter)
        result = actual_result(authority, meter)
        if args.output:
            write_sealed(output_path(args.output, "ci/out", "PRODUCTION_OUTPUT"), result, meter)
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PRODUCER_TERMINAL " + ISO)
        return 0
    except ResourceStop as exc:
        meter = locals().get("meter")
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PRODUCER_TERMINAL " + UNKNOWN_RESOURCE +
              " reason=" + str(exc))
        return 1
    except (Reject, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PRODUCER_TERMINAL " + UNKNOWN_INPUT +
              " reason=" + str(exc))
        return 1
    except Exception as exc:
        # Unexpected implementation failures are not converted into a fake
        # mathematical terminal; the driver sees the explicit stop marker.
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PRODUCER_STOP " + type(exc).__name__ +
              " reason=" + str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
