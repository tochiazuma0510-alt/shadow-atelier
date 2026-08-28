#!/usr/bin/env python3
"""Independent checker for the R07 word-independent successor kernel.

No producer helper is imported.  The toy replay below uses a separate pivot
order and independently reconstructs the typed rows, actions, and spans.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-word-independent-successor-kernel/v1"
SELFTEST_SCHEMA = "d972-r07-word-independent-successor-kernel-selftest/v1"
PASS = "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_CHECKER_PASS"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
CONTEXT_IDS = (21, 22, 23, 24, 25, 1, 27, 21, 26, 28)
CONTEXT_TYPES = ("E3", "E3", "E3", "E3", "E3", "E4", "E4", "E4", "E4", "E4")
CONTEXT_TAGS = ("E3-C21", "E3-C22", "E3-C23", "E3-C24", "E3-C25",
                "E4-C1", "E4-C27", "E4-C21", "E4-C26", "E4-C28")
MUTATION_COUNT = 57
TASK179_PIN = ("search/d972_r07_positive_common_word_colgen_v1.py", 123870,
               "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7")
TASK198_EXTERNAL_FIELDS = {
    "artifact_id", "zip_sha256", "run", "head", "member",
    "member_bytes", "member_sha256",
}
TASK176_EXTERNAL = {
    "artifact_id": "9635036013",
    "zip_sha256": "250e25c992cbe8562f59fb808a8b0d86a7b54fdb750a57f2b1cd1c6cd0c89912",
    "run": "33044121344",
    "head": "0533e42019c9f67f6cec3d1566152db17b903836",
    "member": "d972_r07_all_seven_extension_section_census_v1.json",
    "member_bytes": 13649089,
    "member_sha256": "715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41",
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


H2_IDENTITY = (0, 0, 0)


def h2_mul(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, r = left; ap, bp, rp = right
    return ((a + ap) % 9, (b + bp) % 9, (r + rp - b * ap) % 9)


def h2_inv(value: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, r = value
    return ((-a) % 9, (-b) % 9, (-r - a * b) % 9)


def free_reduce_word(word: list[int]) -> list[int]:
    stack: list[int] = []
    for letter in word:
        letter = int(letter)
        if stack and stack[-1] == -letter: stack.pop()
        else: stack.append(letter)
    return stack


def h2_signed_word(word: list[int]) -> tuple[int, int, int]:
    value = H2_IDENTITY
    generators = {1: (1, 0, 0), 2: (0, 1, 0)}
    for letter in word:
        base = generators[abs(int(letter))]
        value = h2_mul(value, base if letter > 0 else h2_inv(base))
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add(a: dict[str, int], b: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(a)
    for key, value in b.items():
        z = (out.get(key, 0) + scale * value) % 3
        if z: out[key] = z
        else: out.pop(key, None)
    return out


def act(row: dict[str, int], letter: int) -> dict[str, int]:
    out: dict[str, int] = {}
    for key, value in row.items():
        tag, coordinate = key.split(":")
        i = int(coordinate)
        if abs(letter) == 1:
            target = 1 - i
            out[f"{tag}:{target}"] = (out.get(f"{tag}:{target}", 0) + value) % 3
        elif i == 1:
            out[f"{tag}:1"] = (out.get(f"{tag}:1", 0) + value) % 3
            out[f"{tag}:0"] = (out.get(f"{tag}:0", 0) + (1 if letter == 2 else 2) * value) % 3
        else:
            out[f"{tag}:0"] = (out.get(f"{tag}:0", 0) + value) % 3
    return {k: v for k, v in out.items() if v % 3}


class IndependentEchelon:
    def __init__(self) -> None:
        self.rows: dict[str, dict[str, int]] = {}
        self.labels: dict[str, str] = {}
        self.pivots: list[str] = []

    def reduce(self, source: dict[str, int]) -> dict[str, int]:
        row = {k: v % 3 for k, v in source.items() if v % 3}
        # Maximum-pivot rows are appended in descending pivot order; eliminate
        # in that same order so a later smaller pivot cannot reintroduce it.
        for pivot in self.pivots:
            coefficient = row.get(pivot, 0)
            if coefficient: row = add(row, self.rows[pivot], -coefficient)
        return row

    def insert(self, source: dict[str, int], label: str | None = None) -> bool:
        row = self.reduce(source)
        if not row: return False
        pivot = max(row)
        scale = 1 if row[pivot] == 1 else 2
        self.rows[pivot] = {k: scale * v % 3 for k, v in row.items() if scale * v % 3}
        self.labels[pivot] = label or pivot
        self.pivots.append(pivot)
        return True

    def reduce_with_coeff(self, source: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
        row = {k: v % 3 for k, v in source.items() if v % 3}
        coefficients: dict[str, int] = {}
        for pivot in self.pivots:
            coefficient = row.get(pivot, 0)
            if coefficient:
                row = add(row, self.rows[pivot], -coefficient)
                label = self.labels[pivot]
                value = (coefficients.get(label, 0) - coefficient) % 3
                if value: coefficients[label] = value
                else: coefficients.pop(label, None)
        return row, coefficients

    def dual(self, target: dict[str, int]) -> dict[str, int]:
        remainder = self.reduce(target); require(remainder, "checker dual member")
        functional = {min(remainder): 1}
        for pivot in sorted(self.pivots):
            z = (-sum(v * functional.get(k, 0)
                      for k, v in self.rows[pivot].items() if k != pivot)) % 3
            if z: functional[pivot] = z
            else: functional.pop(pivot, None)
        return functional


def defect(seed: int) -> dict[str, int]:
    if seed % 3 == 0: return {f"{i}:0": 1 for i in range(10)}
    if seed % 3 == 1: return {f"{i}:1": 1 for i in range(10)}
    return {f"{i}:0": 2 for i in range(10)}


def in_span(candidate: dict[str, int], rows: list[dict[str, int]]) -> bool:
    e = IndependentEchelon()
    for row in rows: e.insert(row)
    return not e.reduce(candidate)


def replay_toy() -> dict[str, Any]:
    require(len(CONTEXT_IDS) == 10 and CONTEXT_IDS[0] == CONTEXT_IDS[7] == 21, "typed IDs")
    require(CONTEXT_TYPES[0] == "E3" and CONTEXT_TYPES[7] == "E4", "typed C21 separation")
    rows = [defect(i) for i in range(6)]
    boundary = [{"0:0": 1, "0:1": 1}, {"0:0": 2, "0:1": 2},
                {"1:0": 1}]
    e = IndependentEchelon(); queue: list[dict[str, int]] = []
    for row in rows:
        if e.insert(row): queue.append(row)
    cursor = 0; actions = 0
    while cursor < len(queue):
        row = queue[cursor]; cursor += 1
        for letter in (-2, -1, 1, 2):
            actions += 1
            moved = act(row, letter)
            if e.insert(moved): queue.append(moved)
    require(len(e.pivots) >= 2 and cursor == len(queue), "independent queue terminal")
    for row in rows:
        require(in_span(row, list(e.rows.values()) + boundary), "initial span")
    for row in list(e.rows.values()):
        for letter in (-2, -1, 1, 2):
            require(in_span(act(row, letter), list(e.rows.values()) + boundary), "translate span")
    return {"rank": len(e.pivots), "actions": actions,
            "pivots": sorted(e.pivots), "order": 3 ** len(e.pivots),
            "nilpotence_bound": 2 * len(e.pivots) + 1,
            "rows": list(e.rows.values()),
            "basis_digest": digest([e.rows[pivot] for pivot in sorted(e.pivots)]),
            "boundary": boundary,
            "contexts": [{"index": i, "context_id": CONTEXT_IDS[i], "type": CONTEXT_TYPES[i], "tag": CONTEXT_TAGS[i]}
                         for i in range(10)]}


def authenticate_task198(path: str, manifest_path: str, producer_attestation: str,
                         checker_attestation: str) -> dict[str, Any]:
    p = Path(path)
    require(not p.is_absolute() and p.as_posix().startswith("ci/in/"), "checker task198 guarded path")
    raw = (ROOT / p).read_bytes()
    receipt = json.loads(raw.decode("ascii"))
    require(receipt.get("schema") == "d972-r07-seven-context-roof-presentation/v1" and
            receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") == "ROOF_BRIDGE_ISOMORPHISM", "checker task198 envelope")
    body = dict(receipt); claimed = body.pop("self_digest_sha256", None)
    require(claimed == digest(body), "checker task198 seal")
    delta0 = receipt["Delta0"]; presentation = delta0["presentation"]
    require(delta0.get("order") == 357128352 and
            delta0.get("marked_generators") == {"x": [1], "y": [2]} and
            presentation.get("row_count") == 6441 and
            len(presentation.get("rows", [])) == 6441 and
            presentation.get("normal_closure_exact") is True and
            presentation.get("rows_sha256") == digest(presentation["rows"]),
            "checker complete task198 presentation")
    for i, row in enumerate(presentation["rows"], 1):
        require(type(row) is dict and type(row.get("word")) is list and
                row.get("ordinal") == i and
                all(type(x) is int and x in (-2, -1, 1, 2) for x in row["word"]),
                "checker literal presentation row")
    layers = {name: sum(row.get("layer") == name for row in presentation["rows"])
              for name in ("Gamma_Cayley", "action", "Q0_lift")}
    require(layers == {"Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19},
            "checker presentation layers")
    expected_chunks = []
    for start in range(0, 6441, 1024):
        part = presentation["rows"][start:start + 1024]
        expected_chunks.append({"start": start, "end": start + len(part),
                                "sealed": bool(part), "prefix_complete": True,
                                "sha256": digest(part)})
    require(type(presentation.get("chunks")) is list and
            presentation["chunks"] == expected_chunks and
            presentation.get("resume_cursor") == 6441,
            "checker presentation chunks")
    require(receipt.get("bridge", {}).get("branch") == "ROOF_BRIDGE_ISOMORPHISM" and
            receipt.get("bridge", {}).get("kernel_order") == 1 and
            receipt.get("evaluator", {}).get("schema") ==
            "d972-r07-v188-roof-consumer-action-abi/v1", "checker bridge ABI")
    manifest_p = Path(manifest_path)
    producer_p = Path(producer_attestation)
    checker_p = Path(checker_attestation)
    for sidecar in (manifest_p, producer_p, checker_p):
        require(not sidecar.is_absolute() and sidecar.as_posix().startswith("ci/in/"),
                "checker task198 guarded sidecar")
    manifest_raw = (ROOT / manifest_p).read_bytes()
    manifest = json.loads(manifest_raw.decode("ascii"))
    receipt_sha = hashlib.sha256(raw).hexdigest()
    require(type(manifest) is dict and manifest_raw == canonical(manifest) and
            set(manifest) == TASK198_EXTERNAL_FIELDS and
            manifest.get("member") == p.name and
            manifest.get("member_bytes") == len(raw) and
            manifest.get("member_sha256") == receipt_sha and
            type(manifest.get("artifact_id")) is str and bool(manifest["artifact_id"]) and
            type(manifest.get("run")) is str and bool(manifest["run"]) and
            type(manifest.get("head")) is str and len(manifest["head"]) == 40 and
            all(ch in "0123456789abcdef" for ch in manifest["head"]) and
            type(manifest.get("zip_sha256")) is str and len(manifest["zip_sha256"]) == 64 and
            all(ch in "0123456789abcdef" for ch in manifest["zip_sha256"]),
            "checker task198 manifest binding")
    task176_input = receipt.get("input", {}).get("task176", {})
    require(type(task176_input) is dict and
            all(task176_input.get(key) == value for key, value in TASK176_EXTERNAL.items()),
            "checker embedded external binding")
    require((ROOT / producer_p).read_text(encoding="ascii") ==
            "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_PRODUCER_TERMINAL ROOF_BRIDGE_ISOMORPHISM\n" and
            (ROOT / checker_p).read_text(encoding="ascii") ==
            "R07_SEVEN_CONTEXT_ROOF_PRESENTATION_V1_CHECKER_PASS terminal=ROOF_BRIDGE_ISOMORPHISM rows=6441\n",
            "checker task198 attestations")
    return {"receipt": receipt, "rows": presentation["rows"], "bytes": len(raw),
            "sha256": receipt_sha, "manifest": manifest}


def load_task179() -> Any:
    path, size, expected = TASK179_PIN
    source = ROOT / path; raw = source.read_bytes()
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == expected,
            "checker task179 pin")
    spec = importlib.util.spec_from_file_location("d232_checker_task179", source)
    require(spec is not None and spec.loader is not None, "checker task179 loader")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CheckerMonitor:
    def __init__(self) -> None:
        self.counters = {"boundary_pairs": 0, "fibre_scans": 0,
                         "candidate_words": 0, "retained_columns": 0,
                         "checkpoint_bytes": 0, "oracle_rounds": 0,
                         "global_roster": 0, "checker_work": 0}
        self.limits = {key: 10 ** 9 for key in self.counters}
        self.limits.update({"wall_seconds": 14400, "rss_bytes": 8000000000})
        self.phase = "checker"
        self.boundary_records: list[dict[str, Any]] = []
    @staticmethod
    def rss() -> int:
        try:
            import resource
            value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            return value if sys.platform == "darwin" else value * 1024
        except (ImportError, AttributeError):
            return 0
    def check(self, phase: str) -> None: self.phase = phase
    def bump(self, name: str, amount: int = 1, phase: str | None = None) -> None:
        self.phase = phase or self.phase; self.counters[name] += int(amount)
    def public(self) -> dict[str, Any]:
        return {"phase": self.phase, "counters": self.counters, "limits": self.limits,
                "rss_bytes": self.rss()}


def checker_contexts(old: Any) -> list[dict[str, Any]]:
    pp = old.pp_words
    z = old.inv_word(pp([[1], [3]])); u = old.inv_word(pp([[3], [1]]))
    pairs = [([1], [3]), ([1], z), ([3], z), (u, [1]), (u, [3]),
             ([4], [6]), (pp([[1], [2]]), pp([[5], [6]])), ([1], [4]),
             (pp([[2], [4]]), [6]), ([1], pp([[4], [5]]))]
    return [{"index": i, "type": CONTEXT_TYPES[i], "context_id": CONTEXT_IDS[i],
             "tag": CONTEXT_TAGS[i], "left": left, "right": right,
             "block": 1 if i < 5 else 3} for i, (left, right) in enumerate(pairs)]


def checker_defect(p179: Any, runtime: dict[str, Any], context: dict[str, Any], word: list[int]) -> tuple[dict[str, int], bool]:
    old = runtime["old"]; quotient = runtime["e3"] if context["type"] == "E3" else runtime["e4"]
    substituted = old.f2_substitute(word, context["left"], context["right"])
    gradient, value = old.fox_gradient_without_sections(substituted, quotient)
    row: dict[str, int] = {}
    for (component, element), coefficient in gradient.items():
        key = "%d:%d:%s" % (context["index"], int(component), p179.element_blob(runtime, element).hex())
        row[key] = (row.get(key, 0) + int(coefficient)) % 3
    return ({key: value for key, value in row.items() if value}, value == quotient.identity)


def checker_evaluate_source(p179: Any, runtime: dict[str, Any],
                            contexts: list[dict[str, Any]], word: list[int],
                            boundary: list[dict[str, int]],
                            krows: list[dict[str, int]],
                            monitor: CheckerMonitor) -> dict[str, Any]:
    """Independent evaluator ABI: ten Fox values plus complete membership."""
    defect: dict[str, int] = {}
    roofs = True
    values = []
    for context in contexts:
        part, identity = checker_defect(p179, runtime, context, word)
        defect = add(defect, part); roofs = roofs and identity
        values.append({"context": context["index"], "roof_identity": identity,
                       "chain": part})
    require(roofs, "checker evaluator roof reduction")
    member, proof = checker_membership(p179, runtime, monitor, boundary, krows, defect)
    return {"schema": SCHEMA + "/evaluator/v1", "source_word": list(word),
            "successor_values": values, "defect": defect,
            "membership": proof, "member": member}


def checker_evaluate_k_z(p179: Any, runtime: dict[str, Any],
                        contexts: list[dict[str, Any]], monitor: CheckerMonitor,
                        boundary: list[dict[str, int]], krows: list[dict[str, int]],
                        basis: list[dict[str, Any]]) -> dict[str, Any]:
    """Independently replay every basis source through H2(9), Delta0, and K."""
    projections: list[int] = []
    receipts: list[dict[str, Any]] = []
    for index, item in enumerate(basis):
        source = item.get("source_word")
        require(type(source) is list and source, "checker basis source word")
        d1_value = h2_signed_word(list(source))
        require(d1_value[0:2] == (0, 0) and d1_value[2] in (0, 3, 6),
                "checker basis D1 central")
        defect: dict[str, int] = {}; values: list[dict[str, Any]] = []
        for context in contexts:
            part, identity = checker_defect(p179, runtime, context, list(source))
            defect = add(defect, part)
            values.append({"context": context["index"], "roof_identity": identity,
                           "chain": part})
            require(identity, "checker basis Delta0 identity")
        member, membership = checker_membership(p179, runtime, monitor, boundary,
                                                 krows, defect)
        require(member, "checker basis K membership")
        exponent = (d1_value[2] // 3) % 3
        projections.append(exponent)
        receipts.append({"index": index, "source_word": list(source),
                         "d1_value": list(d1_value), "projected_exponent": exponent,
                         "roof_values": values, "delta0_identity": True,
                         "delta1_k_membership": True, "membership": membership,
                         "replay": True})
    active = [i for i, exponent in enumerate(projections) if exponent]
    require(active, "checker D1 projection zero")
    selected = active[0]; scalar = 1 if projections[selected] == 1 else 2
    source_word = free_reduce_word(receipts[selected]["source_word"] * scalar)
    d1_value = h2_signed_word(source_word)
    require(d1_value == (0, 0, 3), "checker selected D1 target")
    defect: dict[str, int] = {}; values: list[dict[str, Any]] = []
    for context in contexts:
        part, identity = checker_defect(p179, runtime, context, source_word)
        defect = add(defect, part)
        values.append({"context": context["index"], "roof_identity": identity,
                       "chain": part})
        require(identity, "checker selected Delta0 identity")
    member, membership = checker_membership(p179, runtime, monitor, boundary,
                                             krows, defect)
    require(member, "checker selected K membership")
    return {"basis_projections": projections,
            "basis_d1_values": [item["d1_value"] for item in receipts],
            "basis_receipts": receipts, "projected_coordinate": projections,
            "selected_index": selected, "inverse_scalar": scalar,
            "word_exponent": scalar, "source_word": source_word,
            "roof_values": values, "delta0_identity": True,
            "delta1_k_membership": True, "d1_z0": list(d1_value),
            "basis_coefficients": {str(selected): scalar},
            "membership": membership, "replay": True}


def checker_action(p179: Any, runtime: dict[str, Any], contexts: list[dict[str, Any]], row: dict[str, int], letter: int) -> dict[str, int]:
    answer: dict[str, int] = {}
    for context in contexts:
        quotient = runtime["e3"] if context["type"] == "E3" else runtime["e4"]
        actor_word = [1] if abs(letter) == 1 else [2]
        substituted = runtime["old"].f2_substitute(actor_word, context["left"], context["right"])
        _, actor_value = runtime["old"].fox_gradient_without_sections(substituted, quotient)
        if letter < 0: actor_value = quotient.inverse(actor_value)
        for key, coefficient in row.items():
            coord, component, blob = key.split(":", 2)
            if int(coord) != context["index"]: continue
            value = p179.unpack_element(runtime, bytes.fromhex(blob), context["block"])
            moved = quotient.mul(actor_value, value)
            moved_key = "%d:%d:%s" % (context["index"], int(component), p179.element_blob(runtime, moved).hex())
            answer[moved_key] = (answer.get(moved_key, 0) + coefficient) % 3
    return {key: value for key, value in answer.items() if value}


def checker_boundary_row(p179: Any, runtime: dict[str, Any], monitor: CheckerMonitor,
                         dual: dict[str, int]) -> dict[str, int] | None:
    """Independent reverse traversal of every translated PB boundary family."""
    for coordinate in reversed(range(10)):
        block = 1 if coordinate < 5 else 3
        support: dict[int, list[tuple[bytes, int]]] = {}
        for key, coefficient in dual.items():
            coord, component, blob = key.split(":", 2)
            if int(coord) == coordinate:
                support.setdefault(int(component), []).append(
                    (bytes.fromhex(blob), int(coefficient) % 3))
        if not support:
            continue
        quotient = runtime["e3"] if block == 1 else runtime["e4"]
        accumulated: dict[tuple[int, bytes], int] = {}
        for index in reversed(range(1, 3 if block in (1, 2) else 12)):
            for component0, h_hex, base0 in reversed(p179.boundary_source(runtime, block, index)):
                component = int(component0); h_blob = bytes.fromhex(str(h_hex))
                h = p179.unpack_element(runtime, h_blob, block)
                h_inv = quotient.inverse(h)
                for g_blob, coefficient in support.get(component, []):
                    monitor.bump("boundary_pairs", 1, "checker_support_correlation")
                    g = p179.unpack_element(runtime, g_blob, block)
                    translation = quotient.mul(g, h_inv)
                    require(quotient.mul(translation, h) == g,
                            "checker boundary translation")
                    t_blob = p179.element_blob(runtime, translation)
                    key = (index, t_blob)
                    contribution = (int(base0) * int(coefficient)) % 3
                    accumulated[key] = (accumulated.get(key, 0) + contribution) % 3
        active = [key for key, value in accumulated.items() if value]
        if not active:
            continue
        index, translation_blob = max(active, key=lambda item: (item[0], item[1]))
        raw_row = p179.translated_boundary(runtime, block, index, translation_blob)
        answer: dict[str, int] = {}
        for row_key, coefficient in raw_row.items():
            _, component, blob = p179.decode_row_key(row_key)
            own = "%d:%d:%s" % (coordinate, component, blob.hex())
            answer[own] = (answer.get(own, 0) + int(coefficient)) % 3
        answer = {key: value for key, value in answer.items() if value}
        correlation = sum(int(dual.get(key, 0)) * value for key, value in answer.items()) % 3
        require(correlation == accumulated[(index, translation_blob)] % 3 and correlation,
                "checker complete boundary correlation")
        monitor.boundary_records.append({"coordinate": coordinate, "block": block,
                                         "index": index,
                                         "translation_blob": translation_blob.hex(),
                                         "row": answer,
                                         "correlation": correlation})
        return answer
    return None


def checker_membership(p179: Any, runtime: dict[str, Any], monitor: CheckerMonitor,
                       boundary: list[dict[str, int]], krows: list[dict[str, int]],
                       candidate: dict[str, int]) -> tuple[bool, dict[str, Any]]:
    while True:
        monitor.bump("checker_work", 1, "checker_membership")
        total = IndependentEchelon()
        for index, row in enumerate(boundary): total.insert(row, "B:" + str(index))
        for index, row in enumerate(krows): total.insert(row, "K:" + str(index))
        remainder, coefficients = total.reduce_with_coeff(candidate)
        if not remainder:
            return True, {"boundary_complete": True, "replay": True,
                          "boundary_coefficients": {k: v for k, v in coefficients.items()
                                                     if k.startswith("B:")},
                          "k_coefficients": {k: v for k, v in coefficients.items()
                                              if k.startswith("K:")}}
        dual = total.dual(candidate)
        active = checker_boundary_row(p179, runtime, monitor, dual)
        if active is not None:
            boundary.append(active); monitor.bump("retained_columns", 1, "checker_boundary_insert"); continue
        pairing = sum(int(v) * int(dual.get(k, 0)) for k, v in candidate.items()) % 3
        require(pairing != 0, "checker negative dual pairing")
        pivot = max(remainder)
        scale = 1 if remainder[pivot] == 1 else 2
        return False, {"boundary_complete": True, "full_zero_correlation": True,
                       "dual": dual, "pairing": pairing,
                       "remainder": remainder, "normalization_scale": scale,
                       "normalized": {key: scale * value % 3 for key, value in remainder.items()
                                      if scale * value % 3},
                       "reduction_coefficients": coefficients,
                       "boundary_coefficients": {k: v for k, v in coefficients.items()
                                                  if k.startswith("B:")},
                       "k_coefficients": {k: v for k, v in coefficients.items()
                                           if k.startswith("K:")}}


def check_actual(receipt: dict[str, Any], args: argparse.Namespace) -> None:
    authenticated = authenticate_task198(args.task198_receipt, args.task198_manifest,
                                         args.task198_producer_attestation,
                                         args.task198_checker_attestation)
    p179 = load_task179()
    monitor = CheckerMonitor(); runtime = p179.build_runtime(monitor)
    contexts = checker_contexts(runtime["old"])
    e = IndependentEchelon(); queue: list[dict[str, int]] = []; boundary: list[dict[str, int]] = []
    action_receipts: list[dict[str, Any]] = []
    for ordinal, row in enumerate(authenticated["rows"], 1):
        monitor.bump("checker_work", 1, "checker_relator")
        defect, roof_identity = {}, True
        for context in contexts:
            part, identity = checker_defect(p179, runtime, context, list(row["word"]))
            defect = add(defect, part); roof_identity = roof_identity and identity
        require(roof_identity, "checker successor roof reduction")
        member, proof = checker_membership(p179, runtime, monitor, boundary,
                                           list(e.rows.values()), defect)
        if not member:
            normalized = proof["normalized"]
            if e.insert(normalized): queue.append(normalized)
    cursor = 0
    while cursor < len(queue):
        source = queue[cursor]; cursor += 1
        for letter in (-2, -1, 1, 2):
            moved = checker_action(p179, runtime, contexts, source, letter)
            member, proof = checker_membership(p179, runtime, monitor, boundary,
                                               list(e.rows.values()), moved)
            action_receipts.append({"basis": cursor - 1, "letter": letter,
                                    "row": moved, "membership": proof})
            if not member:
                normalized = proof["normalized"]
                if e.insert(normalized): queue.append(normalized)
    require(cursor == len(queue), "checker actual queue exhaustion")
    checker_matrices: dict[str, dict[str, dict[str, int]]] = {str(letter): {}
                                                                for letter in (1, -1, 2, -2)}
    for item in action_receipts:
        if item["membership"].get("member"):
            checker_matrices[str(item["letter"])] [str(item["basis"])] = dict(
                item["membership"].get("k_coefficients", {}))
    rank = len(e.pivots)
    require(all(len(checker_matrices[key]) == rank for key in checker_matrices),
            "checker action matrix completeness")

    def compose(left: dict[str, dict[str, int]],
                right: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
        answer: dict[str, dict[str, int]] = {}
        for source in range(rank):
            column: dict[str, int] = {}
            for middle, coefficient in right[str(source)].items():
                for target, value in left.get(middle[2:], {}).items():
                    column[target] = (column.get(target, 0) +
                                      int(coefficient) * int(value)) % 3
            answer[str(source)] = {k: v for k, v in column.items() if v}
        return answer
    identity = {str(i): {"K:" + str(i): 1} for i in range(rank)}
    inverse_products = {}
    for positive, negative in (("1", "-1"), ("2", "-2")):
        require(compose(checker_matrices[positive], checker_matrices[negative]) == identity and
                compose(checker_matrices[negative], checker_matrices[positive]) == identity,
                "checker inverse action matrices")
        inverse_products[positive + negative] = True
        inverse_products[negative + positive] = True
    kernel = receipt.get("result", {}).get("kernel", {})
    producer_basis = kernel.get("basis", [])
    producer_rows = [item.get("row", {}) for item in producer_basis]
    require(producer_rows and len(producer_rows) == len(e.pivots), "checker producer basis rank")
    require(len(kernel.get("initial_defects", [])) == 6441 and
            len(kernel.get("initial_replay_receipts", [])) == 6441 and
            len(kernel.get("translate_receipts", [])) == 4 * len(producer_rows) and
            all(type(item.get("source_word")) is list and len(item.get("values", [])) == 10
                for item in kernel.get("initial_defects", [])),
            "checker producer initial replay ledger")
    require(all(item.get("membership", {}).get("member") is True
                for item in kernel.get("initial_replay_receipts", [])) and
            all(item.get("membership", {}).get("member") is True
                for item in kernel.get("translate_receipts", [])),
            "checker producer terminal containments")
    require(kernel.get("basis_digest") == digest(producer_rows),
            "checker producer basis digest")
    for item in producer_basis:
        membership = item.get("membership", {})
        require(item.get("delta1_value") == item.get("row") and
                item.get("delta0_identity") is True and
                (type(item.get("source_word")) is list or
                 type(item.get("word_ancestry")) is list),
                "checker producer word-bearing basis")
        require(membership.get("member") is False and
                membership.get("full_zero_correlation") is True and
                membership.get("dual") and membership.get("pairing") and
                membership.get("boundary_coefficients") is not None and
                membership.get("k_coefficients") is not None,
                "checker producer negative membership")
        require(item.get("boundary_coefficients") is not None and
                item.get("prior_k_coefficients") is not None and
                item.get("boundary_value") is not None and item.get("ancestry"),
                "checker producer boundary ancestry")
    require(kernel.get("evaluator", {}).get("entry_point") ==
            "evaluate_roof_trivial_source" and
            isinstance(kernel.get("k_z_receipt"), dict),
            "checker producer evaluator ABI")
    producer_k_z = kernel["k_z_receipt"]
    projection = producer_k_z.get("projected_coordinate")
    require(type(projection) is list and len(projection) == len(producer_rows) and
            all(type(a) is int and a in (0, 1, 2) for a in projection) and any(projection) and
            type(producer_k_z.get("selected_index")) is int and
            producer_k_z.get("selected_index") == next(i for i, a in enumerate(projection) if a) and
            producer_k_z.get("inverse_scalar") in (1, 2) and
            projection[producer_k_z["selected_index"]] * producer_k_z["inverse_scalar"] % 3 == 1 and
            producer_k_z.get("word_exponent") == producer_k_z.get("inverse_scalar") and
            producer_k_z.get("source_word") and
            producer_k_z.get("delta0_identity") is True and
            producer_k_z.get("delta1_k_membership") is True and
            producer_k_z.get("d1_z0") == [0, 0, 3] and
            producer_k_z.get("basis_coefficients") in (
                {str(producer_k_z.get("selected_index")): producer_k_z.get("inverse_scalar")},
                {"K:" + str(producer_k_z.get("selected_index")): producer_k_z.get("inverse_scalar")}) and
            producer_k_z.get("basis_projections") == projection and
            type(producer_k_z.get("basis_d1_values")) is list and
            len(producer_k_z["basis_d1_values"]) == len(producer_rows) and
            type(producer_k_z.get("basis_receipts")) is list and
            len(producer_k_z["basis_receipts"]) == len(producer_rows) and
            producer_k_z.get("replay") is True,
            "checker producer k_z receipt")
    checker_k_z = checker_evaluate_k_z(p179, runtime, contexts, monitor, boundary,
                                       list(e.rows.values()), producer_basis)
    require(checker_k_z.get("basis_projections") == producer_k_z.get("basis_projections") and
            checker_k_z.get("basis_d1_values") == producer_k_z.get("basis_d1_values") and
            len(checker_k_z.get("basis_receipts", [])) == len(producer_k_z.get("basis_receipts", [])),
            "checker independent basis projections")
    for own, theirs in zip(checker_k_z["basis_receipts"], producer_k_z["basis_receipts"]):
        require(own.get("source_word") == theirs.get("source_word") and
                own.get("d1_value") == theirs.get("d1_value") and
                own.get("projected_exponent") == theirs.get("projected_exponent") and
                len(own.get("roof_values", [])) == len(theirs.get("roof_values", [])) and
                all(a.get("context") == b.get("context") and
                    a.get("roof_identity") is True and b.get("roof_identity") is True and
                    a.get("chain") == b.get("chain")
                    for a, b in zip(own["roof_values"], theirs["roof_values"])) and
                own.get("delta0_identity") is True and
                own.get("delta1_k_membership") is True and
                own.get("membership", {}).get("member") is True and
                theirs.get("membership", {}).get("member") is True and
                own.get("membership", {}).get("k_coefficients") ==
                theirs.get("membership", {}).get("k_coefficients"),
                "checker basis receipt replay")
    require(checker_k_z.get("projected_coordinate") == producer_k_z.get("projected_coordinate") and
            checker_k_z.get("selected_index") == producer_k_z.get("selected_index") and
            checker_k_z.get("inverse_scalar") == producer_k_z.get("inverse_scalar") and
            checker_k_z.get("word_exponent") == producer_k_z.get("word_exponent") and
            checker_k_z.get("source_word") == producer_k_z.get("source_word") and
            len(checker_k_z.get("roof_values", [])) == len(producer_k_z.get("roof_values", [])) and
            all(a.get("context") == b.get("context") and
                a.get("roof_identity") is True and b.get("roof_identity") is True and
                a.get("chain") == b.get("chain")
                for a, b in zip(checker_k_z["roof_values"], producer_k_z["roof_values"])) and
            checker_k_z.get("delta0_identity") is True and
            checker_k_z.get("delta1_k_membership") is True and
            checker_k_z.get("d1_z0") == [0, 0, 3] and
            checker_k_z.get("basis_coefficients") == producer_k_z.get("basis_coefficients") and
            checker_k_z.get("membership", {}).get("member") is True and
            producer_k_z.get("membership", {}).get("member") is True and
            checker_k_z.get("membership", {}).get("k_coefficients") ==
            producer_k_z.get("membership", {}).get("k_coefficients") and
            checker_k_z.get("replay") is True,
            "checker independent k_z receipt")
    require(kernel.get("action_matrices") and
            kernel.get("inverse_products") == {"1-1": True, "-11": True,
                                                "2-2": True, "-22": True},
            "checker producer action matrix ledger")
    require(kernel.get("order_three") is True and
            kernel.get("pairwise_commutation") is True and
            kernel.get("order") == 3 ** len(producer_rows) and
            kernel.get("nilpotence_bound") == 2 * len(producer_rows) + 1,
            "checker producer group ledger")
    for row in producer_rows:
        member, proof = checker_membership(p179, runtime, monitor, boundary,
                                           list(e.rows.values()), row)
        require(member and proof.get("boundary_complete") and
                "boundary_coefficients" in proof and "k_coefficients" in proof,
                "producer row in checker quotient span")
    for row in e.rows.values():
        member, proof = checker_membership(p179, runtime, monitor, boundary,
                                           producer_rows, row)
        require(member and proof.get("boundary_complete") and
                "boundary_coefficients" in proof and "k_coefficients" in proof,
                "checker row in producer quotient span")
    require(kernel.get("boundary_rank") == len(boundary),
            "checker complete boundary transcript rank")
    require(len(kernel.get("boundary_records", [])) == len(monitor.boundary_records),
            "checker active boundary transcript")
    require(all(record.get("row") and record.get("provenance")
                for record in kernel.get("boundary_records", [])),
            "checker producer boundary provenance")


def load(path: str) -> dict[str, Any]:
    obj = json.loads(Path(path).read_text(encoding="ascii"))
    require(type(obj) is dict, "receipt object")
    return obj


def validate_fixture(value: dict[str, Any]) -> None:
    require(value.get("rank", 0) >= 2 and value.get("order") == 3 ** value["rank"] and
            value.get("nilpotence_bound") == 2 * value["rank"] + 1,
            "checker fixture rank")
    require([(row.get("index"), row.get("type"), row.get("context_id"), row.get("tag"))
             for row in value.get("contexts", [])] ==
            list(zip(range(10), CONTEXT_TYPES, CONTEXT_IDS, CONTEXT_TAGS)) and
            len(value.get("successors", [])) == 10 and
            all(item.get("source_words") for item in value["successors"]) and
            value.get("successor_digest") == digest([item["source_words"] for item in value["successors"]]),
            "checker fixture contexts")
    require(value.get("roof_reductions") == [True] * 10 and
            value.get("affine_checks", {}).get("multiplication") is True and
            value["affine_checks"].get("inverse") is True and
            value["affine_checks"].get("crossed_derivation") is True,
            "checker fixture affine")
    require(value.get("queue_actions", 0) > 0 and len(value.get("basis", [])) == value["rank"] and
            all(item.get("row") and item.get("pivot") in item["row"] and item.get("ancestry")
                for item in value["basis"]) and
            value.get("basis_digest") == digest([item["row"] for item in value["basis"]]),
            "checker fixture basis")
    require(value.get("boundary") and value.get("boundary_digest") == digest(value["boundary"]) and
            any(set(row) & set(value["basis"][0]["row"]) for row in value["boundary"]),
            "checker fixture boundary")
    require(len(value.get("initial_membership", [])) == 6 and
            len(value.get("translate_membership", [])) == 4 * value["rank"] and
            all(item.get("member") is True for item in value["initial_membership"] + value["translate_membership"]),
            "checker fixture membership")
    require(value.get("alternate_rank") == value["rank"] and
            value.get("alternate_span_forward") is True and
            value.get("alternate_span_reverse") is True and
            value.get("negative_dual"), "checker fixture spans")
    require(value.get("action_matrices") and
            all(len(value["action_matrices"].get(str(letter), {})) == value["rank"]
                for letter in (1, -1, 2, -2)) and
            all(value.get("inverse_products", {}).values()), "checker fixture actions")
    require(value.get("order_three") is True and
            value.get("pairwise_commutation") is True, "checker fixture group replay")
    anchor = value.get("projection_anchor", {})
    receipts = value.get("basis_receipts", [])
    require(len(receipts) == value["rank"] and
            all(type(item.get("source_word")) is list and item.get("source_word") and
                all(type(letter) is int and letter in (-2, -1, 1, 2)
                    for letter in item["source_word"]) and
                (d1 := h2_signed_word(item["source_word"])) ==
                tuple(item.get("d1_value", [])) and
                d1[0:2] == (0, 0) and d1[2] in (0, 3, 6) and
                item.get("projected_exponent") == (d1[2] // 3) % 3 and
                len(item.get("roof_values", [])) == 10 and
                all(roof.get("roof_identity") is True
                    for roof in item["roof_values"]) and
                item.get("delta0_identity") is True and
                item.get("delta1_k_membership") is True and
                item.get("membership", {}).get("member") is True and
                item.get("replay") is True
                for item in receipts) and
            value.get("basis_projections") ==
            [item["projected_exponent"] for item in receipts] and
            value.get("basis_d1_values") ==
            [item["d1_value"] for item in receipts],
            "checker reconstructed projection receipts")
    projection = value["basis_projections"]
    require(any(projection), "checker projection nonzero")
    selected = next(i for i, exponent in enumerate(projection) if exponent)
    scalar = 1 if projection[selected] == 1 else 2
    require(anchor.get("projected_coordinate") == projection and
            anchor.get("selected_index") == selected and
            anchor.get("inverse_scalar") == scalar and
            anchor.get("word_exponent") == scalar and
            type(anchor.get("source_word")) is list and
            h2_signed_word(anchor["source_word"]) == (0, 0, 3) and
            anchor.get("source_word") ==
            free_reduce_word(receipts[selected]["source_word"] * scalar) and
            anchor.get("delta0_identity") is True and
            anchor.get("delta1_k_membership") is True and
            anchor.get("d1_z0") == [0, 0, 3] and
            anchor.get("basis_coefficients") == {str(selected): scalar} and
            len(anchor.get("roof_values", [])) == 10 and
            all(roof.get("roof_identity") is True
                for roof in anchor["roof_values"]) and
            anchor.get("membership", {}).get("member") is True and
            anchor.get("replay") is True, "checker fixture projection anchor")
    binding = value.get("task198_binding", {})
    require(binding.get("schema") == "d972-r07-seven-context-roof-presentation/v1" and
            binding.get("terminal") == "ROOF_BRIDGE_ISOMORPHISM" and
            all(binding.get(key) for key in ("run", "head", "artifact", "member", "checker",
                                              "delta1_bfs", "task192_word")) and
            binding.get("delta1_bfs") == "unused" and
            binding.get("task192_word") == "unused" and
            value.get("resource_terminal", {}).get("rank_zero") is True and
            all(flag is False for flag in value.get("forbidden_downstream", {}).values()),
            "checker fixture bindings")


def check_selftest(receipt: dict[str, Any], fixture: dict[str, Any] | None) -> None:
    require(receipt.get("schema") == SELFTEST_SCHEMA and receipt.get("status") == "PASS", "producer selftest envelope")
    body = dict(receipt); claimed = body.pop("self_digest_sha256", None)
    require(claimed == digest(body), "producer self digest")
    independent = replay_toy(); toy = receipt.get("toy", {})
    require(toy.get("rank") == independent["rank"] and toy.get("order") == independent["order"], "producer/checker rank span")
    require(receipt.get("pivot_scale_ancestry", {}).get("replayed") is True and
            receipt["pivot_scale_ancestry"].get("scale") == 2,
            "producer pivot-scale ancestry")
    require(toy.get("nilpotence_bound") == independent["nilpotence_bound"], "nilpotence bound")
    require(toy.get("basis_digest") == independent["basis_digest"], "independent basis digest")
    require(toy.get("boundary") == independent["boundary"] and
            any(set(row) & set(toy["basis"][0]["row"]) for row in toy["boundary"]),
            "complete boundary overlap")
    require(len(toy.get("contexts", [])) == 10, "producer typed contexts")
    require([(row.get("context_id"), row.get("type"), row.get("tag"))
             for row in toy["contexts"]] ==
            list(zip(CONTEXT_IDS, CONTEXT_TYPES, CONTEXT_TAGS)),
            "typed tag ledger")
    require(toy.get("roof_reductions") == [True] * 10 and
            toy.get("affine_checks", {}).get("multiplication") is True and
            toy.get("affine_checks", {}).get("inverse") is True and
            toy.get("affine_checks", {}).get("crossed_derivation") is True,
            "affine and roof replay")
    producer_rows = [row.get("row", {}) for row in toy.get("basis", [])]
    require(len(producer_rows) == independent["rank"] and
            all(in_span(row, independent["rows"] + independent["boundary"])
                for row in producer_rows) and
            all(in_span(row, producer_rows + independent["boundary"])
                for row in independent["rows"]),
            "bidirectional quotient K span")
    require(receipt.get("mutation_controls", {}).get("attempted") == MUTATION_COUNT and
            receipt.get("mutation_controls", {}).get("rejected") == MUTATION_COUNT, "mutation terminal")
    names = receipt.get("mutation_controls", {}).get("names", [])
    validate_fixture(toy)
    rejected = 0
    for name in names:
        mutant = copy.deepcopy(receipt)
        toy_mutant = mutant.get("toy", {})
        if name in ("task198_bytes", "task198_artifact"): toy_mutant["task198_binding"]["artifact"] = ""
        elif name == "task198_schema": toy_mutant["task198_binding"]["schema"] = "bad"
        elif name == "task198_terminal": toy_mutant["task198_binding"]["terminal"] = "UNKNOWN"
        elif name in ("task198_run", "task198_head"): toy_mutant["task198_binding"][name[8:]] = ""
        elif name in ("task198_member", "selftest_production"): toy_mutant["task198_binding"]["member"] = False
        elif name == "checker_acceptance": toy_mutant["task198_binding"]["checker"] = False
        elif name == "projected_coordinate": toy_mutant["projection_anchor"]["projected_coordinate"] = [1, 0]
        elif name == "selected_index": toy_mutant["projection_anchor"]["selected_index"] = -1
        elif name == "inverse_scalar": toy_mutant["projection_anchor"]["inverse_scalar"] = 0
        elif name == "word_exponent": toy_mutant["projection_anchor"]["word_exponent"] = 0
        elif name == "delta0_identity": toy_mutant["projection_anchor"]["delta0_identity"] = False
        elif name == "d1_z0_target": toy_mutant["projection_anchor"]["d1_z0"] = [0, 0, 2]
        elif name == "k_z_source_word": toy_mutant["projection_anchor"]["source_word"] = []
        elif name in ("presentation_word", "ancestry_word"): toy_mutant["basis"][0]["ancestry"] = []
        elif name in ("presentation_complete", "omitted_relator"): toy_mutant["initial_membership"].pop()
        elif name == "context_type": toy_mutant["contexts"][0]["type"] = "E4"
        elif name == "context_id": toy_mutant["contexts"][0]["context_id"] = 0
        elif name in ("source_substitution", "paper_product_order"): toy_mutant["successors"][0]["source_words"] = []
        elif name == "e3_c21_e4_c21_merge": toy_mutant["contexts"][7]["tag"] = "E3-C21"
        elif name == "repeated_e3_insertion": toy_mutant["contexts"].pop()
        elif name in ("affine_multiplication", "affine_inverse", "crossed_derivation_order"):
            toy_mutant["affine_checks"] = {}
        elif name == "roof_reduction": toy_mutant["roof_reductions"][0] = False
        elif name in ("raw_coordinate", "k_row_coefficient"): toy_mutant["basis"][0]["row"] = {}
        elif name == "block_tag": toy_mutant["contexts"][0]["tag"] = "bad"
        elif name == "omitted_boundary": toy_mutant["boundary"] = []
        elif name == "boundary_coefficient": toy_mutant["boundary"][0]["0:0"] = 2
        elif name == "false_positive_membership": toy_mutant["initial_membership"][0]["member"] = False
        elif name == "false_negative_dual": toy_mutant["negative_dual"] = {}
        elif name == "pivot": toy_mutant["basis"][0]["pivot"] = "bad"
        elif name == "omitted_generator_translate": toy_mutant["translate_membership"].pop()
        elif name == "early_queue_terminal": toy_mutant["queue_actions"] = 0
        elif name == "generator_action": toy_mutant["action_matrices"]["1"] = {}
        elif name == "generator_inverse": toy_mutant["inverse_products"]["1-1"] = False
        elif name in ("order_three", "commutator"): toy_mutant["order_three" if name == "order_three" else "pairwise_commutation"] = False
        elif name in ("rank", "order", "nilpotence_bound"): toy_mutant[name] = 0
        elif name == "delta1_bfs": toy_mutant["task198_binding"]["delta1_bfs"] = "bad"
        elif name == "task192_word": toy_mutant["task198_binding"]["task192_word"] = "bad"
        elif name == "traversal_stale": toy_mutant["alternate_span_forward"] = False
        elif name == "resource_stop_completion": toy_mutant["resource_terminal"]["rank_zero"] = False
        elif name == "false_ihara": toy_mutant["forbidden_downstream"]["Ihara_witness"] = True
        elif name.startswith("false_"): toy_mutant["forbidden_downstream"][name[6:]] = True
        try:
            validate_fixture(toy_mutant)
        except RuntimeError:
            rejected += 1
    require(rejected == len(names) == MUTATION_COUNT, "independent mutation replay")
    if fixture is not None:
        expected = fixture.get("expected", {})
        require(independent["rank"] >= expected.get("min_rank", 2), "fixture rank")
        require(expected.get("contexts", 10) == 10, "fixture contexts")


def check_production(args: argparse.Namespace) -> str:
    path = Path(args.producer_receipt)
    require(not path.is_absolute() and path.as_posix().startswith("ci/out/"), "producer guarded output")
    receipt = load(str(ROOT / path))
    require(receipt.get("schema") == SCHEMA, "producer schema")
    require(receipt.get("terminal") in (UNKNOWN_INPUT, "UNKNOWN_RESOURCE", "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PASS"), "producer terminal")
    body = dict(receipt); claimed = body.pop("self_digest_sha256", None)
    require(claimed == digest(body), "producer terminal digest")
    # A positive production receipt is accepted only after this independent
    # checker has itself authenticated the task198 terminal and all ten tags.
    if receipt.get("terminal") == "R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_PASS":
        result = receipt.get("result", {})
        require(result.get("presentation_rows") == 6441 and result.get("word_bearing") is True, "positive K input")
        evaluator = result.get("kernel", {}).get("evaluator", {})
        require(evaluator.get("schema") == SCHEMA + "/evaluator/v1" and
                evaluator.get("entry_point") == "evaluate_roof_trivial_source" and
                "basis_coordinates" in evaluator.get("returns", []) and
                "complete_boundary_receipt" in evaluator.get("returns", []),
                "positive evaluator ABI")
        check_actual(receipt, args)
    return str(receipt.get("terminal"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--fixture")
    parser.add_argument("--producer-receipt")
    parser.add_argument("--task198-receipt", default="ci/in/d972_r07_seven_context_roof_presentation_v1.json")
    parser.add_argument("--task198-manifest", default="ci/in/d972_r07_seven_context_roof_presentation_v1.manifest.json")
    parser.add_argument("--task198-producer-attestation", default="ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt")
    parser.add_argument("--task198-checker-attestation", default="ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            require(args.producer_receipt is not None, "checker receipt required")
            receipt_path = Path(args.producer_receipt)
            require(not receipt_path.is_absolute() and receipt_path.as_posix().startswith("ci/out/"), "checker guarded receipt")
            fixture = load(args.fixture) if args.fixture else None
            check_selftest(load(str(ROOT / receipt_path)), fixture)
            print(PASS + " terminal=SELFTEST_COMPLETE mutation_attempted=57 mutation_rejected=57")
            return 0
        require(args.producer_receipt is not None, "production receipt required")
        terminal = check_production(args)
        print(PASS + " terminal=" + terminal)
        return 0
    except (RuntimeError, OSError, json.JSONDecodeError) as exc:
        print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V1_CHECKER_NONPOSITIVE reason=" + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
