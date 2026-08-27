"""Independent checker for the v2 normalized exact-common-word contract.

The checker duplicates the word and exponent primitives and deliberately does
not import the producer.  It validates receipts as data, with hard failures
for malformed programming state and typed UNKNOWN only for authenticated
input/resource boundaries.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import math
import re
import tempfile
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_CHECKER = ROOT / "crosscheck/check_d972_r07_positive_common_word_colgen_v1.py"
LIVE_CHECKER_ID = (73780, "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d")
NORMALIZED_SEMANTICS_DIGEST = hashlib.sha256(
    b"nu=(exp/18) mod 3|AllSevenModel.occurrence_data|AllSevenModel.occurrence_column|"
    b"AllSevenModel.direct_column|PositiveSearch.positive_receipt|Echelon target/basis membership|weighted formula scalar"
).hexdigest()
NORMALIZED_SEMANTICS_CALLSITES = [
    "AllSevenModel.occurrence_data", "AllSevenModel.occurrence_column",
    "AllSevenModel.direct_column", "PositiveSearch.positive_receipt",
    "Echelon target/basis membership", "weighted formula scalar"]

CACHE_SEMANTICS = "nu=(exp/18) mod 3"
CACHE_CHUNK_LIMIT = 256
CACHE_ORDERING = ["roster_index", "target_coordinate", "target_blob",
                  "kernel_index", "global_cursor", "column_id"]
DELTA_ORDER = 357_128_352
Q0_STATE_COUNT = 1_469_664
KERNEL_ORDERS = [9, 9, 9, 9, 9, 1, 1, 1, 3, 3]
SCHEMA = "d972-r07-normalized-exact-cached-colgen/v3"
SELFTEST_SCHEMA = "d972-r07-normalized-exact-cached-colgen-selftest/v3"
COMMON = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD"
SELFTEST_TERMINAL = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_SELFTEST_PASS"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE_CAPS = {"wall_seconds", "boundary_pairs", "fibre_scans",
                         "candidate_words", "retained_columns", "checkpoint_bytes",
                         "rss_bytes", "oracle_rounds", "global_roster"}
REGISTERED_RESOURCE_PHASE_CAPS = {
    ("resume_rebuild", "boundary_pairs"),
    ("resume_rebuild", "fibre_scans"),
    ("resume_rebuild", "candidate_words"),
    ("resume_rebuild", "retained_columns"),
    ("resume_rebuild", "global_roster"),
    ("resume_rebuild", "oracle_rounds"),
    ("task175_reconstruction", "wall_seconds"),
    ("task175_reconstruction", "rss_bytes"),
    ("fine_deletion", "wall_seconds"),
    ("fine_deletion", "rss_bytes"),
    ("Q0_discovery", "wall_seconds"),
    ("Q0_discovery", "rss_bytes"),
    ("A_L_membership_scan", "wall_seconds"),
    ("A_L_membership_scan", "rss_bytes"),
    ("L_subgroup_closure", "wall_seconds"),
    ("L_subgroup_closure", "rss_bytes"),
    ("typed_singleton_equality", "wall_seconds"),
    ("typed_singleton_equality", "rss_bytes"),
    ("Q0_positive_shortlex_section", "wall_seconds"),
    ("Q0_positive_shortlex_section", "rss_bytes"),
    ("coarse_inverse_build", "fibre_scans"),
    ("coarse_inverse_build", "wall_seconds"),
    ("coarse_inverse_build", "rss_bytes"),
    ("positive_boundary_correlation", "boundary_pairs"),
    ("positive_boundary_correlation", "wall_seconds"),
    ("positive_boundary_correlation", "rss_bytes"),
    ("rank_increase", "retained_columns"),
    ("rank_increase", "wall_seconds"),
    ("rank_increase", "rss_bytes"),
    ("positive_correction_candidate", "candidate_words"),
    ("positive_correction_candidate", "wall_seconds"),
    ("positive_correction_candidate", "rss_bytes"),
    ("weighted_eleven_occurrence_formula", "wall_seconds"),
    ("weighted_eleven_occurrence_formula", "rss_bytes"),
    ("weighted_support_fibre", "wall_seconds"),
    ("weighted_support_fibre", "rss_bytes"),
    ("weighted_global_prefix", "global_roster"),
    ("weighted_global_prefix", "wall_seconds"),
    ("weighted_global_prefix", "rss_bytes"),
    ("checkpoint_serialization", "checkpoint_bytes"),
    ("positive_global_fallback", "global_roster"),
    ("positive_correction_dovetail", "oracle_rounds"),
}
MONITOR_LIMIT_FIELDS = ("wall_seconds", "boundary_pairs", "fibre_scans",
                        "candidate_words", "retained_columns",
                        "checkpoint_bytes", "rss_bytes", "oracle_rounds",
                        "global_roster")
MONITOR_COUNTER_FIELDS = ("boundary_pairs", "fibre_scans", "candidate_words",
                          "retained_columns", "checkpoint_bytes",
                          "global_roster", "oracle_rounds")
AUTHENTICATED_INPUT_REASON_PREFIXES = (
    "module_not_uniquely_pinned:", "module_missing:", "module_pin:",
    "module_loader:", "missing:", "pin:", "task175:not_READY",
    "resume:input_identity", "resume:target", "resume:normalized_semantics",
    "resume:monitor_limits")
MUTATIONS = ("divisor_18", "exponent_sign", "roster_ordinal", "conjugator_exponent",
             "boundary_nonzero_tail", "raw_mod_3", "target_tail", "old_pivots",
             "coefficient_inverse", "divisibility_54", "u0_formula", "v0_formula",
             "cube_exponent", "right_correction_order", "pentagon_order", "hexagon",
             "source_word", "boundary_correction_word")
CACHE_MUTATIONS = (
    "cache_key_component", "stale_group_type", "slot_sign_order",
    "fox_term", "prefix_inverse", "boundary_descriptor",
    "dual_support_decode", "section_parent_letter", "typed_coordinate_blob",
    "cache_hit_without_literal", "chunk_end_advanced", "incomplete_row_complete",
    "skipped_resume_candidate", "stale_dual_progress", "raw_mod3_semantics",
    "old_pivot_reuse", "coefficient_two_repetition", "exactification_cube",
    "resource_stop_terminal_change")
POSITIVE_GATES = ("joint_kernel_membership", "normalized_target_equality",
                  "zero_frattini_tail", "integer_exact_exponent",
                  "right_multiply_frozen_g760", "hexagon_1", "hexagon_2",
                  "five_factor_pentagon", "marked_reduction_side_gates",
                  "no_pb3_pb4_boundary_chain")
LIVE_V1 = {
    "producer": (123870, "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    "checker": (73780, "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"),
    "driver": (12872, "48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"),
    "fixture": (407, "46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"),
}
TASK186_V2 = {
    "producer": (63053, "ec73db0a474b3b52d69e19862e8185ae22423b2406f3922b5669d9a4e85fafab"),
    "checker": (54982, "8898798d0d6a9e0b6cd67402e74ba0dc5048b4797a0f7a9657e58d70d553c488"),
    "driver": (9630, "a1c0fc034b127174e5c5795347648db0629314262b9e59689705e887371a7e4e"),
    "fixture": (234, "34dd389d9a3aff50486e57137f8dafea7b14825baec13e3288ed595046940963"),
}
TASK190 = {
    "instruction": (3699, "36502b0151e036c0df76de3e77722c1b9a9eb9ae0242fbdb6faba887d4510d29"),
    "reply": (22022, "6fe8ee264e33b75012b23a71c695282958882a1b1eadcc459cfff991184dfe3f"),
}
PROOF_PINS = {
    "v156": (10409, "2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d"),
    "v157": (8367, "08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8"),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha_bytes(data):
    return digest(data)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def validate_cached_weighted_rows(progress, cursor_limit=None):
    """Check serializable weighted-row state before helper projection."""
    require(isinstance(progress, dict) and
            isinstance(progress.get("correction"), dict),
            "cached weighted progress shape")
    correction = progress["correction"]
    cursor = correction.get("canonical_row_cursor")
    rows = correction.get("weighted_rows")
    require(type(cursor) is int and cursor >= 0 and isinstance(rows, dict),
            "cached weighted row cursor shape")
    if cursor_limit is not None:
        require(cursor <= int(cursor_limit), "cached weighted row cursor bound")
    for key, state in rows.items():
        require(type(key) is str and key.isdecimal() and
                str(int(key)) == key and isinstance(state, dict),
                "cached weighted row identity")
        index = int(key)
        require(index >= 1 and type(state.get("formula_sha256")) is str and
                len(state["formula_sha256"]) == 64 and
                all(ch in "0123456789abcdefABCDEF"
                    for ch in state["formula_sha256"]) and
                type(state.get("K")) is int and state["K"] in (0, 1, 2) and
                type(state.get("W")) is int and state["W"] >= 0 and
                state.get("delta_order") == DELTA_ORDER and
                state.get("kernel_orders") == KERNEL_ORDERS and
                type(state.get("support_fibre_cursor")) is int and
                type(state.get("kernel_cursor")) is int and
                type(state.get("global_prefix")) is int and
                type(state.get("complete")) is bool,
                "cached weighted row fields")
        require(0 <= state["support_fibre_cursor"] <= state["W"] and
                0 <= state["kernel_cursor"] <= max(KERNEL_ORDERS) and
                0 <= state["global_prefix"] <= DELTA_ORDER,
                "cached weighted row cursor bounds")
        if state["K"] == 0:
            require(state["global_prefix"] == 0,
                    "cached K=0 global cursor")
        else:
            global_bound = (state["W"] + 1 if state["W"] < DELTA_ORDER
                            else DELTA_ORDER)
            require(state["support_fibre_cursor"] == 0 and
                    state["kernel_cursor"] == 0 and
                    state["global_prefix"] <= global_bound,
                    "cached K!=0 cursor state")
        if state["complete"]:
            require(state["K"] == 0,
                    "cached completed row has nonzero K")
        if index <= cursor:
            require(state["complete"] is True,
                    "cached cursor crosses incomplete row")
        else:
            require(index == cursor + 1 and state["complete"] is False,
                    "cached future row is not contiguous")
    for index in range(1, cursor + 1):
        require(str(index) in rows and rows[str(index)].get("complete") is True,
                "cached cursor skips weighted row")


def validate_monitor_snapshot(snapshot):
    require(isinstance(snapshot, dict) and
            set(snapshot) == {"phase", "elapsed_seconds", "rss_bytes",
                               "limits", "counters", "single_process"} and
            type(snapshot.get("phase")) is str and bool(snapshot.get("phase")) and
            type(snapshot.get("elapsed_seconds")) in (int, float) and
            not isinstance(snapshot.get("elapsed_seconds"), bool) and
            snapshot.get("elapsed_seconds") >= 0 and
            type(snapshot.get("rss_bytes")) is int and
            snapshot.get("rss_bytes") >= 0 and
            snapshot.get("single_process") is True,
            "monitor snapshot schema")
    limits = snapshot["limits"]; counters = snapshot["counters"]
    require(isinstance(limits, dict) and set(limits) == set(MONITOR_LIMIT_FIELDS) and
            isinstance(counters, dict) and set(counters) == set(MONITOR_COUNTER_FIELDS) and
            all(type(limits[name]) in (int, float) and
                not isinstance(limits[name], bool) and limits[name] >= 0
                for name in MONITOR_LIMIT_FIELDS) and
            all(type(counters[name]) is int and counters[name] >= 0
                for name in MONITOR_COUNTER_FIELDS),
            "monitor registered limits/counters")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def validate_outer_seal(value):
    claimed = value.get("self_digest")
    body = dict(value); body.pop("self_digest", None)
    if not isinstance(claimed, str) or claimed != digest(canonical(body)):
        raise RuntimeError("outer v2 receipt seal")


def reject_forbidden_claims(value):
    """The v2 envelope must not smuggle negative/fake/cofinal claims."""
    forbidden = {"negative_claim", "fake_claim", "fake_witness", "fake",
                 "cofinal_claim", "cofinal_lift", "cofinal", "ihara_claim",
                 "ihara_witness"}
    if isinstance(value, dict):
        for key, item in value.items():
            if key in forbidden and item not in (None, False, "", [], {}):
                raise RuntimeError("forbidden negative/fake/cofinal/Ihara claim")
            reject_forbidden_claims(item)
    elif isinstance(value, list):
        for item in value:
            reject_forbidden_claims(item)


def validate_resource_terminal(terminal):
    fields = terminal.split(":")
    if len(fields) != 5 or fields[0] != "UNKNOWN_RESOURCE":
        raise RuntimeError("malformed resource terminal")
    if not fields[1].startswith("phase=") or not fields[2].startswith("cap=") or \
            not fields[3].startswith("value=") or not fields[4].startswith("limit="):
        raise RuntimeError("resource terminal fields")
    phase, cap = fields[1][6:], fields[2][4:]
    if not phase or cap not in UNKNOWN_RESOURCE_CAPS or (phase, cap) not in REGISTERED_RESOURCE_PHASE_CAPS:
        raise RuntimeError("unregistered resource phase/cap")
    try:
        value, limit = float(fields[3][6:]), float(fields[4][6:])
    except ValueError as exc:
        raise RuntimeError("resource terminal numeric fields") from exc
    if not math.isfinite(value) or not math.isfinite(limit) or not value > limit:
        raise RuntimeError("resource terminal is not an exceeded registered cap")
    return {"phase": phase, "cap": cap, "value": value, "limit": limit}


def word(w):
    return tuple(int(x) for x in w)


def inv(w):
    return tuple(-x for x in reversed(word(w)))


def reduce_word(w):
    out = []
    for x in word(w):
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def mul(*ws):
    out = ()
    for w in ws:
        out = reduce_word(out + word(w))
    return out


def power(w, exponent_value):
    if exponent_value == 0:
        return ()
    base = w if exponent_value > 0 else inv(w)
    return mul(*([base] * abs(exponent_value)))


def exp(w):
    ans = [0, 0]
    for x in word(w):
        if abs(x) not in (1, 2):
            raise ValueError("invalid roster letter")
        ans[abs(x) - 1] += 1 if x > 0 else -1
    return tuple(ans)


def install_normalized_checker_semantics(checker):
    """Patch the helper's real exponent callsite before its full replay."""
    def normalized_pair(w):
        integer = exp(w)
        if integer[0] % 18 or integer[1] % 18:
            raise RuntimeError("helper normalized exponent divisibility")
        return ((integer[0] // 18) % 3, (integer[1] // 18) % 3)
    checker.exponent_pair = normalized_pair
    if checker.exponent_pair([1] * 18) != (1, 0):
        raise RuntimeError("helper exponent callsite remained raw-vacuous")
    return normalized_pair


def nu(w, divisor=18):
    e = exp(w)
    if any(x % divisor for x in e):
        raise RuntimeError("nonintegral normalized exponent")
    return tuple((x // divisor) % 3 for x in e)


def exactify(c_star, r3, r9, r12):
    e = exp(c_star)
    if any(x % 54 for x in e):
        raise RuntimeError("54-divisibility integrity failure")
    A, B = e[0] // 54, e[1] // 54
    v0 = mul(r9, r12, inv(r3) * 2)
    u0 = mul(r9, inv(v0) * 8)
    h = mul(power(u0, -3 * A), power(v0, -3 * B))
    c = mul(c_star, h)
    if exp(v0) != (0, 18) or exp(u0) != (18, 0) or exp(c) != (0, 0):
        raise RuntimeError("exactification basis/closure failure")
    return c, v0, u0, h


def parse_element_blob(raw, block):
    """Decode the task175 helper's packed Element without helper APIs."""
    raw = bytes(raw)
    degree = 36 if int(block) in (1, 2) else 144
    pc_width = 4 if int(block) in (1, 2) else 10
    require(len(raw) == degree + pc_width, "independent element blob width")
    return bytes(raw[:degree]), bytes(raw[degree:])


def independent_row_key(block, component, blob):
    block = int(block); component = int(component); blob = bytes(blob)
    require(block in (1, 2, 3) and 1 <= component <= 6,
            "independent typed row key")
    return (b"R" + bytes((block, component)) +
            len(blob).to_bytes(2, "big") + blob)


def multiply_coordinate_blob_rows(runtime, left, right):
    """Independently multiply typed E3/E4 coordinate blobs componentwise."""
    require(type(left) is list and type(right) is list and
            len(left) == len(right) == 10,
            "checker kernel coordinate-row schema")
    answer = []
    for index, (left_raw, right_raw) in enumerate(zip(left, right)):
        block = 1 if index < 5 else 3
        quotient = runtime["e3"] if index < 5 else runtime["e4"]
        left_value = parse_element_blob(bytes.fromhex(str(left_raw)), block)
        right_value = parse_element_blob(bytes.fromhex(str(right_raw)), block)
        answer.append(runtime["checker"].element_blob(
            quotient.mul(left_value, right_value)).hex())
    return answer


def decode_independent_row_key(key):
    key = bytes(key)
    require(len(key) >= 5 and key[:1] == b"R",
            "independent typed row key decode")
    width = int.from_bytes(key[3:5], "big")
    require(len(key) == 5 + width, "independent typed row width")
    return key[1], key[2], key[5:]


def independent_exponent_key(index):
    index = int(index)
    require(index in (1, 2), "independent exponent key index")
    return b"E" + bytes((index,))


def _cache_measure(value):
    if isinstance(value, bytes): return len(value) + 8
    if isinstance(value, str): return len(value.encode("utf-8")) + 8
    if isinstance(value, int): return 16
    if isinstance(value, dict):
        return 32 + sum(_cache_measure(k) + _cache_measure(v)
                        for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return 16 + sum(_cache_measure(item) for item in value)
    return 64


class IndependentCache:
    """Bounded checker-local cache; producer caches are never imported."""
    def __init__(self, name, maximum=64 * 1024 * 1024):
        self.name = name; self.maximum = int(maximum)
        self.store = OrderedDict(); self.used = 0
        self.hits = 0; self.misses = 0; self.evictions = 0
        self.regenerated_literals = 0

    def get(self, key):
        if key in self.store:
            value, size = self.store.pop(key); self.store[key] = (value, size)
            self.hits += 1
            return value
        self.misses += 1
        return None

    def put(self, key, value):
        size = _cache_measure(value)
        while self.store and self.used + size > self.maximum:
            _, (_, old_size) = self.store.popitem(last=False)
            self.used -= old_size; self.evictions += 1
        if size <= self.maximum:
            self.store[key] = (value, size); self.used += size
        self.regenerated_literals += 1
        return value

    def public(self):
        return {"name": self.name, "hits": self.hits,
                "misses": self.misses, "evictions": self.evictions,
                "bytes": self.used, "max_bytes": self.maximum,
                "regenerated_literals": self.regenerated_literals}


class IndependentFoxTemplateCache:
    """Independent eleven-slot Fox template and dual join implementation."""
    def __init__(self, runtime, checker, input_digest):
        self.runtime = runtime; self.c = checker
        self.input_digest = str(input_digest)
        self.cache = IndependentCache("checker_fox_templates",
                                      96 * 1024 * 1024)
        self.specs = self._make_specs()
        require(len(self.specs) == 11,
                "checker Fox cache requires all eleven slots")

    def _make_specs(self):
        c = self.c; e3, e4 = self.runtime["e3"], self.runtime["e4"]
        x, y = (1,), (2,); z = c.inverse(c.paper_product(x, y))
        u = c.inverse(c.paper_product(y, x)); contexts = c.pentagon_context_words()
        specs = []
        for block, coordinate, quotient, left, right, sign, lift, label in (
                (1, 0, e3, x, y, 1, True, "H1_fxy"),
                (1, 1, e3, x, z, -1, True, "H1_fxz"),
                (1, 2, e3, y, z, 1, True, "H1_fyz"),
                (2, 3, e3, u, x, -1, True, "H2_fux"),
                (2, 0, e3, x, y, -1, True, "H2_fxy"),
                (2, 4, e3, u, y, 1, True, "H2_fuy")):
            specs.append({"block": block, "coordinate": coordinate,
                          "quotient": quotient, "left": left, "right": right,
                          "sign": sign, "lift": lift, "label": label})
        for natural, coordinate, label in ((1, 5, "P_b1"), (3, 6, "P_b2"),
                                           (0, 7, "P_b3"), (2, 8, "P_b5_inverse"),
                                           (4, 9, "P_b4_inverse")):
            left, right = contexts[natural]
            specs.append({"block": 3, "coordinate": coordinate,
                          "quotient": e4, "left": left, "right": right,
                          "sign": -1 if natural in (2, 4) else 1,
                          "lift": False, "label": label})
        g = self.runtime["obj"]["g760"]
        for spec in specs:
            factor = c.f2_substitute(g, spec["left"], spec["right"])
            if spec["lift"]: factor = c.embed_pb3(factor)
            if spec["sign"] < 0: factor = c.inverse(factor)
            spec["base_factor"] = factor
        for block in (1, 2, 3):
            quotient = e3 if block in (1, 2) else e4
            indices = [i for i, item in enumerate(specs)
                       if item["block"] == block]
            prefix = quotient.identity
            for index in reversed(indices):
                specs[index]["prefix"] = prefix
                prefix = quotient.mul(prefix,
                                      quotient.eval(specs[index]["base_factor"]))
            require(prefix == quotient.identity,
                    "checker cached base prefix identity")
        for spec in specs:
            spec["occurrence_prefix"] = spec["prefix"]
            if spec["sign"] > 0:
                spec["occurrence_prefix"] = spec["quotient"].mul(
                    spec["prefix"], spec["quotient"].eval(spec["base_factor"]))
        return specs

    def _key(self, relator, ordinal, spec):
        roster_index = 0; layer = "literal"; roster_ordinal = 0
        for index, item in enumerate(self.runtime["obj"]["roster"], 1):
            if tuple(item["word"]) == tuple(relator):
                roster_index = index; layer = item["layer"]
                roster_ordinal = int(item["ordinal"]); break
        group = "E3" if spec["quotient"] is self.runtime["e3"] else "E4"
        return (self.input_digest, CACHE_SEMANTICS, NORMALIZED_SEMANTICS_DIGEST,
                layer, roster_ordinal, roster_index, tuple(relator), int(ordinal),
                group, spec["block"], spec["coordinate"], spec["sign"],
                spec["lift"], spec["label"])

    def _template(self, relator, ordinal, spec):
        key = self._key(relator, ordinal, spec); cached = self.cache.get(key)
        if cached is not None: return cached
        c = self.c; quotient = spec["quotient"]
        relation = c.f2_substitute(relator, spec["left"], spec["right"])
        if spec["lift"]: relation = c.embed_pb3(relation)
        if spec["sign"] < 0: relation = c.inverse(relation)
        gradient, value = c.fox(quotient, relation)
        require(value == quotient.identity, "checker cached relation identity")
        terms = []
        for (component, base), coefficient in sorted(
                gradient.items(), key=lambda item: (
                    int(item[0][0]), c.element_blob(item[0][1]))):
            base_inverse = quotient.inverse(base)
            terms.append({"component": int(component), "base": base,
                          "base_inverse": base_inverse,
                          "base_inverse_blob": c.element_blob(base_inverse),
                          "coefficient": int(coefficient) % 3})
        return self.cache.put(key, {"relation": tuple(relation),
            "gradient": gradient, "terms": terms,
            "value": value, "prefix_inverse": quotient.inverse(
                spec["occurrence_prefix"]), "occurrence_prefix": spec[
                    "occurrence_prefix"], "spec": spec,
            "integer_exponent": exp(relator)})

    def base_gradient(self, block, word):
        """Cache one of the three fixed direct all-seven gradients."""
        block = int(block); word = tuple(word)
        quotient = self.runtime["e3"] if block in (1, 2) else self.runtime["e4"]
        key = (self.input_digest, CACHE_SEMANTICS,
               NORMALIZED_SEMANTICS_DIGEST, "base_gradient", block,
               "E3" if block in (1, 2) else "E4", word)
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        gradient, value = self.c.fox(quotient, word)
        require(value == quotient.identity,
                "checker cached base relation identity")
        return self.cache.put(key, {"word": word, "gradient": gradient,
                                    "value": value})

    def formula(self, relator, dual):
        c = self.c; merged = {}; occurrences = []
        for ordinal, spec in enumerate(self.specs, 1):
            template = self._template(relator, ordinal, spec); count = 0
            for term in template["terms"]:
                for key, scalar in dual.items():
                    if key[:1] != b"R": continue
                    block, component, raw = decode_independent_row_key(key)
                    if block != spec["block"] or component != term["component"]:
                        continue
                    target = parse_element_blob(raw, block)
                    required = spec["quotient"].mul(
                        spec["quotient"].mul(template["prefix_inverse"], target),
                        term["base_inverse"])
                    merged_key = (spec["coordinate"], c.element_blob(required))
                    contribution = term["coefficient"] * int(scalar) % 3
                    count += 1
                    if contribution:
                        merged[merged_key] = (merged.get(merged_key, 0) +
                                              contribution) % 3
                        if not merged[merged_key]: del merged[merged_key]
            occurrences.append({"ordinal": ordinal, "label": spec["label"],
                                "coordinate": spec["coordinate"],
                                "factor_sign": spec["sign"],
                                "raw_dual_pair_terms": count})
        pair = nu(relator)
        constant = (dual.get(independent_exponent_key(1), 0) * pair[0] +
                    dual.get(independent_exponent_key(2), 0) * pair[1]) % 3
        ordered = sorted(merged.items(), key=lambda item: (item[0][0], item[0][1]))
        return {"K": constant,
                "terms": [[coordinate, raw.hex(), coefficient]
                          for (coordinate, raw), coefficient in ordered],
                "same_target_merged_mod3": True, "zero_sums_deleted": True,
                "eleven_occurrences": occurrences}


class IndependentBoundaryDescriptorCache:
    """Independent complete PB3/PB4 descriptor and translated-row cache."""
    def __init__(self, runtime, input_digest):
        self.runtime = runtime; self.c = runtime["checker"]
        self.input_digest = str(input_digest)
        self.cache = IndependentCache("checker_boundary_rows")
        self.descriptors = []
        for block, rows in ((1, runtime["obj"]["pb3_rows"]),
                            (2, runtime["obj"]["pb3_rows"]),
                            (3, runtime["obj"]["pb4_rows"])):
            quotient = runtime["e3"] if block in (1, 2) else runtime["e4"]
            for index, source in enumerate(rows, 1):
                for (component, value), coefficient in source.items():
                    h_blob = self.c.element_blob(value)
                    h_inverse = quotient.inverse(value)
                    self.descriptors.append({"block": block,
                        "relator_index": index, "component": int(component),
                        "h_blob": h_blob, "h_inverse": h_inverse,
                        "h_inverse_blob": self.c.element_blob(h_inverse),
                        "base_coefficient": int(coefficient) % 3})
        self.descriptors.sort(key=lambda item: (item["block"],
            item["relator_index"], item["component"], item["h_blob"],
            item["base_coefficient"]))

    def public_descriptors(self):
        return [{"block": item["block"],
                 "relator_index": item["relator_index"],
                 "component": item["component"],
                 "h_blob": item["h_blob"].hex(),
                 "h_inverse": item["h_inverse_blob"].hex(),
                 "base_coefficient": item["base_coefficient"]}
                for item in self.descriptors]

    def public_contract(self):
        raw = canonical(self.public_descriptors())
        return {"count": len(self.descriptors), "sha256": digest(raw),
                "sorted": True, "support_times_occurrence": True}

    def row(self, block, index, translation_hex):
        blob = bytes.fromhex(str(translation_hex)); key = (
            self.input_digest, CACHE_SEMANTICS, NORMALIZED_SEMANTICS_DIGEST,
            "translated", int(block), int(index), blob)
        cached = self.cache.get(key)
        if cached is not None: return cached
        quotient = self.runtime["e3"] if int(block) in (1, 2) else self.runtime["e4"]
        translation = parse_element_blob(blob, int(block)); answer = {}
        for item in self.descriptors:
            if item["block"] != int(block) or item["relator_index"] != int(index):
                continue
            value = parse_element_blob(item["h_blob"], int(block))
            raw = self.c.element_blob(quotient.mul(translation, value))
            key0 = independent_row_key(int(block), item["component"], raw)
            answer[key0] = (answer.get(key0, 0) + item["base_coefficient"]) % 3
            if not answer[key0]: del answer[key0]
        sources = (self.runtime["obj"]["pb3_rows"] if int(block) in (1, 2)
                   else self.runtime["obj"]["pb4_rows"])
        expected = {}
        # Rebuild the same translated row from the authenticated source map;
        # this is intentionally separate from the descriptor accumulation.
        for (component, value), base_coefficient in sources[int(index) - 1].items():
            translated = quotient.mul(translation, value)
            key0 = independent_row_key(int(block), component,
                                       self.c.element_blob(translated))
            expected[key0] = (expected.get(key0, 0) +
                              int(base_coefficient)) % 3
            if not expected[key0]: del expected[key0]
        require(answer == expected,
                "checker cached boundary replay")
        return self.cache.put(key, answer)


class IndependentCoordinateValueCache:
    """Independent bounded cache for complete ten-coordinate candidate views."""
    def __init__(self, runtime, input_digest):
        self.runtime = runtime; self.input_digest = str(input_digest)
        require(len(runtime["obj"]["joint"].states) == 243,
                "checker Gamma cache requires all 243 rows")
        self.cache = IndependentCache("checker_coordinate_values")

    def coordinates(self, source_word):
        key = (self.input_digest, CACHE_SEMANTICS,
               NORMALIZED_SEMANTICS_DIGEST, "coordinate_values",
               tuple(source_word), "E3+E4")
        cached = self.cache.get(key)
        if cached is not None: return cached
        value = tuple(self.runtime["checker"].independent_coordinates(
            self.runtime, source_word))
        require(len(value) == 10,
                "checker candidate ten-coordinate replay")
        return self.cache.put(key, value)

    def q0_word(self, qid, source_word, parent_path):
        qid = int(qid); source_word = tuple(source_word)
        require(0 <= qid < Q0_STATE_COUNT, "checker q0 cache state range")
        require(isinstance(parent_path, list),
                "checker q0 parent/letter path schema")
        # Rebuild the literal section word from the authenticated parent and
        # letter chain.  State ids are part of the sealed provenance, while
        # the word itself is obtained only by replaying the chain.
        expected_parent = 1
        rebuilt = []
        for item in parent_path:
            require(isinstance(item, dict) and
                    set(item) == {"state_id", "parent_id", "letter"},
                    "checker q0 parent/letter path fields")
            sid = int(item["state_id"]); parent = int(item["parent_id"])
            letter = int(item["letter"])
            require(2 <= sid <= Q0_STATE_COUNT and
                    1 <= parent < sid and parent == expected_parent,
                    "checker q0 parent/letter ancestry")
            require(0 <= letter < 3, "checker q0 parent/letter alphabet")
            rebuilt.append(letter)
            expected_parent = sid
        require((not parent_path and qid == 0) or
                (parent_path and parent_path[-1]["state_id"] == qid + 1),
                "checker q0 terminal state binding")
        require(tuple(reduce_word(rebuilt)) == source_word,
                "checker q0 literal parent/letter replay")
        key = (self.input_digest, CACHE_SEMANTICS,
               NORMALIZED_SEMANTICS_DIGEST, "q0_section_word", qid,
               tuple(rebuilt), tuple(parent_path), source_word, "Q0")
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        # The helper-nonshared runtime has no producer section table.  The
        # literal q0 path is therefore the authenticated source word itself;
        # its ten-coordinate replay is still mandatory on first fill.
        coordinates = self.coordinates(source_word)
        return self.cache.put(key, {"qid": qid, "word": source_word,
                                    "coordinate_blobs": tuple(coordinates),
                                    "literal_replayed": True})

    def gamma_row(self, gid, source_word):
        gid = int(gid); source_word = tuple(source_word)
        require(0 <= gid < 243, "checker Gamma cache state range")
        # Reconstruct the Gamma section literal from the authenticated joint
        # group's own parent/generator transcript; a receipt-supplied word is
        # never accepted as the state-id witness.
        joint = self.runtime["obj"]["joint"]
        require(hasattr(joint, "section_word"),
                "checker Gamma parent/generator transcript")
        reconstructed = tuple(reduce_word(joint.section_word(gid)))
        require(reconstructed == source_word,
                "checker Gamma state-id literal replay")
        key = (self.input_digest, CACHE_SEMANTICS,
               NORMALIZED_SEMANTICS_DIGEST, "gamma_coordinate_row", gid,
               reconstructed, source_word, "Gamma")
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        coordinates = self.coordinates(source_word)
        return self.cache.put(key, {"gid": gid, "word": source_word,
                                    "coordinate_blobs": tuple(coordinates),
                                    "literal_replayed": True})

    def candidate(self, qid, gid, gamma_word, q0_word, source_word,
                 q0_parent_path):
        qid = int(qid); gid = int(gid)
        gamma_word = tuple(gamma_word); q0_word = tuple(q0_word)
        source_word = tuple(source_word)
        require(reduce_word(gamma_word + q0_word) == source_word,
                "checker cached candidate parent/letter replay")
        # State-id provenance is replayed even on a cache hit.  The bounded
        # value is only an accelerator and cannot turn a stale receipt word
        # into accepted evidence.
        gamma = self.gamma_row(gid, gamma_word)
        section = self.q0_word(qid, q0_word, q0_parent_path)
        key = (self.input_digest, CACHE_SEMANTICS,
               NORMALIZED_SEMANTICS_DIGEST, "candidate", qid, gid,
               gamma_word, q0_word, source_word, "E3+E4")
        cached = self.cache.get(key)
        if cached is not None:
            require(cached.get("qid") == qid and cached.get("gid") == gid and
                    tuple(cached.get("source_word", ())) == source_word and
                    tuple(cached.get("gamma_source_word", ())) == gamma_word and
                    tuple(cached.get("q0_source_word", ())) == q0_word and
                    cached.get("gamma_coordinate_blobs") ==
                    gamma["coordinate_blobs"] and
                    cached.get("section_coordinate_blobs") ==
                    section["coordinate_blobs"],
                    "checker cached candidate hit provenance")
            return cached
        literal = self.coordinates(source_word)
        require(len(literal) == 10 and
                tuple(literal) == tuple(self.coordinates(source_word)),
                "checker cached candidate literal replay")
        return self.cache.put(key, {
            "qid": qid, "gid": gid, "source_word": source_word,
            "gamma_source_word": gamma_word, "q0_source_word": q0_word,
            "gamma_coordinate_blobs": gamma["coordinate_blobs"],
            "section_coordinate_blobs": section["coordinate_blobs"],
            "coordinate_blobs": tuple(literal), "literal_replayed": True})


def _checker_cached_toy_schedule(helper):
    fixture = {"generators": [[1, 0, 2], [0, 2, 1]]}
    candidates = []
    for index, delta in enumerate(([], [1], [2], [1, 2]), 1):
        row, _occurrences = helper.independent_toy_column(
            fixture, delta, [1] * 18)
        candidates.append({"index": index, "delta": list(delta),
                           "word": [1] * 18, "row": row,
                           "formula": {"K": sum(row.values()) % 3,
                                       "terms": [[key.hex(), value]
                                                 for key, value in sorted(row.items())],
                                       "eleven": 3}})
    basis = helper.RowSpace(); active = []
    for candidate in candidates:
        pivot, origin = basis.add(candidate["row"], candidate["index"])
        if pivot is not None:
            active.append({"index": candidate["index"], "pivot": pivot.hex(),
                           "ancestry": [[key, item] for key, item in
                                         sorted(origin.items())],
                           "formula": candidate["formula"]})
    require(active, "checker cached toy active transcript")
    coefficients = {item["index"]: (2 if pos == 2 else 1)
                    for pos, item in enumerate(active, 1)}
    target = {}
    for item in active:
        for key, value in candidates[item["index"] - 1]["row"].items():
            target[key] = (target.get(key, 0) +
                           coefficients[item["index"]] * value) % 3
            if not target[key]: del target[key]
    replay = helper.RowSpace()
    for item in active:
        replay.add(candidates[item["index"] - 1]["row"], item["index"])
    remainder, recovered = replay.reduce(target)
    require(not remainder and recovered == coefficients,
            "checker cached toy target solution")
    correction = []
    for item in active:
        source = candidates[item["index"] - 1]["word"]
        correction = list(reduce_word(correction + (
            source if coefficients[item["index"]] == 1 else inv(source))))
    direct = helper.toy_fox(correction,
                            [tuple(row) for row in fixture["generators"]], 2)
    c_star = mul(correction, correction, correction)
    exact = exactify(c_star, [2] * 36,
                     [1] * 18 + [2] * 144,
                     [-1] * 18 + [-2] * 54)
    exact_direct = helper.toy_fox(
        exact[0], [tuple(row) for row in fixture["generators"]], 2)
    return {"attempted_candidates": [1, 2, 3, 4],
            "weighted_formulas": [item["formula"] for item in active],
            "active_columns": [item["index"] for item in active],
            "rank_pivot_ancestry": active, "rank": len(replay.pivots),
            "pivot_order": [key.hex() for key in replay.pivots],
            "target": [[key.hex(), value] for key, value in sorted(target.items())],
            "solution": [[key, value] for key, value in sorted(coefficients.items())],
            "correction_word": correction,
            "direct_all_seven_replay": {
                "row": [[key.hex(), value] for key, value in sorted(direct.items())],
                "literal": True, "fixture_group": "S3"},
            "c_exact": list(exact[0]),
            "c_exact_direct_replay": {
                "row": [[key.hex(), value] for key, value in
                        sorted(exact_direct.items())],
                "literal": True, "fixture_group": "S3"},
            "fixture": {"noncommutative": True,
                        "generators": fixture["generators"]},
            "terminal": "CACHED_TOY_COMPLETE",
            "resource_counters": {"logical_attempts": 4,
                                  "cache_hits": 0, "cache_misses": 0}}


def _checker_rank_zero_resume(helper, stop, expected):
    """Replay a sealed toy prefix and only its unsealed suffix from rank zero."""
    fixture = {"generators": [[1, 0, 2], [0, 2, 1]]}
    candidates = []
    for index, delta in enumerate(([], [1], [2], [1, 2]), 1):
        row, _occurrences = helper.independent_toy_column(
            fixture, delta, [1] * 18)
        candidates.append({"index": index, "row": row})
    partial = helper.RowSpace(); retained = []
    for candidate in candidates[:stop]:
        reduced, _ = partial.reduce(candidate["row"])
        if reduced:
            pivot, origin = partial.add(candidate["row"], candidate["index"])
            retained.append({"index": candidate["index"],
                             "row": dict(candidate["row"]),
                             "pivot": pivot, "origin": dict(origin)})
    rebuilt = helper.RowSpace()
    for record in retained:
        reduced, _ = rebuilt.reduce(record["row"])
        require(reduced, "checker toy rank-zero duplicate column")
        pivot, origin = rebuilt.add(record["row"], record["index"])
        require(pivot == record["pivot"] and origin == record["origin"],
                "checker toy rank-zero column replay")
    for candidate in candidates[stop:]:
        reduced, _ = rebuilt.reduce(candidate["row"])
        if reduced:
            rebuilt.add(candidate["row"], candidate["index"])
    target = {bytes.fromhex(str(key)): int(value)
              for key, value in expected["target"]}
    remainder, solution = rebuilt.reduce(target)
    expected_solution = {int(key): int(value)
                         for key, value in expected["solution"]}
    require(not remainder and solution == expected_solution and
            [key.hex() for key in rebuilt.pivots] == expected["pivot_order"],
            "checker toy resumed transcript")
    resumed_word = []
    for index, coefficient in sorted(expected_solution.items()):
        source = [1] * 18
        resumed_word = list(reduce_word(resumed_word +
                            (source if coefficient == 1 else inv(source))))
    resumed_direct = helper.toy_fox(
        resumed_word, [tuple(row) for row in fixture["generators"]], 2)
    resumed_exact = exactify(mul(resumed_word, resumed_word, resumed_word),
                             [2] * 36, [1] * 18 + [2] * 144,
                             [-1] * 18 + [-2] * 54)
    resumed_exact_direct = helper.toy_fox(
        resumed_exact[0], [tuple(row) for row in fixture["generators"]], 2)
    require(resumed_word == expected["correction_word"] and
            [[key.hex(), value] for key, value in sorted(resumed_direct.items())] ==
            expected["direct_all_seven_replay"]["row"],
            "checker resumed literal/direct transcript")
    require(list(resumed_exact[0]) == expected["c_exact"] and
            [[key.hex(), value] for key, value in
             sorted(resumed_exact_direct.items())] ==
            expected["c_exact_direct_replay"]["row"],
            "checker resumed c_exact transcript")
    return {"interrupt_after": stop, "rank_zero_replayed": True,
            "retained_before_resume": [record["index"] for record in retained],
            "physical_attempts": list(range(1, stop + 1)) + list(range(stop + 1, 5)),
            "canonical_attempts": list(range(1, 5)),
            "resumed_attempts": list(range(stop + 1, 5)),
            "safe_prefix_attempts": list(range(1, stop + 1)),
            "replayed_suffix_attempts": list(range(stop + 1, 5)),
            "safe_chunk_end": stop,
            "safe_chunk_replayed_without_suffix": True,
            "repeated_suffix": [],
            "replayed_columns": len(retained),
            "final_rank": len(rebuilt.pivots),
            "final_solution": [[key, value]
                                for key, value in sorted(solution.items())],
            "correction_word": resumed_word,
            "c_exact": list(resumed_exact[0]),
            "direct_all_seven_replay": {"row": [
                [key.hex(), value] for key, value in sorted(resumed_direct.items())],
                "literal": True, "fixture_group": "S3"},
            "c_exact_direct_replay": {"row": [
                [key.hex(), value] for key, value in
                sorted(resumed_exact_direct.items())],
                "literal": True, "fixture_group": "S3"},
            "terminal": expected.get("terminal", "CACHED_TOY_COMPLETE"),
            "resource_counters": expected.get("resource_counters", {}),
            "prior_resource_counters": expected.get("resource_counters", {}),
            "resource_counters_monotone": True,
            "terminal_unchanged": True}


def validate_cached_schedule_selftest(receipt, helper):
    cached = receipt.get("cached_schedule_selftest", {})
    require(isinstance(cached, dict) and cached.get("cache_equivalence") is True,
            "cached schedule selftest absent")
    reference = cached.get("reference"); accelerated = cached.get("cached")
    require(isinstance(reference, dict) and isinstance(accelerated, dict),
            "cached schedule transcript shape")
    expected = _checker_cached_toy_schedule(helper)
    require(cached.get("fixture") == expected["fixture"],
            "independent cached toy fixture binding")
    for field in ("attempted_candidates", "weighted_formulas", "active_columns",
                  "rank_pivot_ancestry", "rank", "pivot_order", "target",
                  "solution", "correction_word", "direct_all_seven_replay",
                  "c_exact", "c_exact_direct_replay"):
        require(reference.get(field) == expected[field] and
                accelerated.get(field) == expected[field],
                "independent cached schedule mismatch:" + field)
    require(reference.get("terminal") == expected["terminal"] and
            accelerated.get("terminal") == expected["terminal"] and
            reference.get("resource_counters", {}).get("logical_attempts") ==
            expected["resource_counters"]["logical_attempts"] and
            accelerated.get("resource_counters", {}).get("logical_attempts") ==
            expected["resource_counters"]["logical_attempts"] and
            all(type(accelerated.get("resource_counters", {}).get(field)) is int
                and accelerated["resource_counters"][field] >= 0
                for field in ("cache_hits", "cache_misses")),
            "independent cached terminal/counter transcript")
    require(cached.get("chunk_limit") == CACHE_CHUNK_LIMIT and
            isinstance(cached.get("resume_checks"), list) and
            len(cached["resume_checks"]) == 4,
            "cached chunk interruption coverage")
    probe = cached.get("cache_probe", {})
    require(probe.get("name") == "selftest_eviction_probe" and
            probe.get("hits") == 1 and probe.get("evictions", 0) > 0 and
            probe.get("regenerated_literals") == 2,
            "cached eviction probe transcript")
    # Independently replay the candidate epoch invalidation contract.  This
    # is a real bounded-cache fill/hit followed by an epoch-clear miss, not a
    # comparison against a producer boolean.
    epoch_cache = IndependentCache("checker_candidate_epoch_probe", 1024)
    epoch_key = ("selftest-input", CACHE_SEMANTICS, "basis_epoch", 0, 0)
    epoch_cache.put(epoch_key, {"literal_replayed": True})
    before_hit = epoch_cache.get(epoch_key) is not None
    epoch_cache.store.clear(); epoch_cache.used = 0
    after_miss = epoch_cache.get(epoch_key) is None
    require(cached.get("candidate_epoch_probe") == {
        "before_hit": before_hit, "old_epoch": 0, "new_epoch": 1,
        "after_invalidation_miss": after_miss},
        "candidate basis epoch invalidation transcript")
    split_templates = IndependentCache("checker_shared_templates", 88 * 1024 * 1024)
    split_base = IndependentCache("checker_shared_base", 8 * 1024 * 1024)
    split_templates.put(("template", 1), {"literal": b"template"})
    split_base.put(("base", 1), {"literal": b"base"})
    split_limits = {
        "template_used": split_templates.used,
        "base_used": split_base.used,
        "template_limit": 88 * 1024 * 1024,
        "base_limit": 8 * 1024 * 1024,
        "aggregate_used": split_templates.used + split_base.used,
        "aggregate_limit": 96 * 1024 * 1024}
    require(split_limits["template_used"] <= split_limits["template_limit"] and
            split_limits["base_used"] <= split_limits["base_limit"] and
            split_limits["aggregate_used"] <= split_limits["aggregate_limit"] and
            cached.get("split_shared_limit_probe") == split_limits,
            "shared Fox cache split-limit transcript")
    legacy_dispatch = {
        "canonical_selector": bool({"section_blob_hex": ["00"],
                                     "selection": "least"}.get(
                                         "section_blob_hex")),
        "global_candidate": bool({"global_cursor": 0}.get("section_blob_hex")),
        "kernel_candidate": bool({"kernel_word": [1]}.get("section_blob_hex"))}
    require(legacy_dispatch == {
        "canonical_selector": True, "global_candidate": False,
        "kernel_candidate": False} and
            cached.get("legacy_selector_dispatch") == legacy_dispatch,
        "legacy selector dispatch transcript")
    require(cached.get("resource_stop_probe") == {
        "phase": "selftest_chunk", "cap": "candidate_words",
        "value": 2, "limit": 1}, "cached resource-stop probe")
    for position, item in enumerate(cached["resume_checks"], 1):
        expected_resume = _checker_rank_zero_resume(helper, position, expected)
        for field in ("interrupt_after", "rank_zero_replayed",
                      "retained_before_resume", "physical_attempts",
                      "canonical_attempts", "resumed_attempts",
                      "safe_prefix_attempts", "replayed_suffix_attempts",
                      "safe_chunk_end", "safe_chunk_replayed_without_suffix",
                      "repeated_suffix", "replayed_columns", "final_rank",
                      "final_solution", "correction_word",
                      "c_exact", "direct_all_seven_replay",
                      "c_exact_direct_replay", "terminal"):
            require(item.get(field) == expected_resume[field],
                    "cached chunk resume transcript:" + field)
        require(item.get("resource_counters", {}).get("logical_attempts") ==
                expected_resume["resource_counters"]["logical_attempts"] and
                all(type(item.get("resource_counters", {}).get(field)) is int
                    and item["resource_counters"][field] >= 0
                    for field in ("cache_hits", "cache_misses")),
                "cached chunk resume counters")
        require(item.get("safe_chunk_end") == position and
                item.get("safe_chunk_end") > 0 and
                item.get("resource_counters_monotone") is True and
                item.get("prior_resource_counters") ==
                expected_resume["resource_counters"] and
                all(item["resource_counters"].get(name, 0) >=
                    item["prior_resource_counters"].get(name, 0)
                    for name in item["resource_counters"]),
                "cached safe chunk/counter carry-forward")
    controls = cached.get("mutation_controls", {})
    require(controls.get("attempted") == len(CACHE_MUTATIONS) and
            controls.get("rejected") == len(CACHE_MUTATIONS) and
            tuple(controls.get("names", ())) == CACHE_MUTATIONS and
            controls.get("validator") ==
            "load_bearing_cached_schedule_replay",
            "cached mutation controls")
    require(receipt.get("cache_mutation_controls") == controls,
            "cached mutation controls were not copied to receipt")
    for name in ("reference", "cached"):
        stats = cached[name].get("cache_stats", {})
        require(isinstance(stats, dict) and
                all(type(stats.get(field)) is int and stats[field] >= 0
                    for field in ("hits", "misses", "evictions",
                                  "bytes", "regenerated_literals")),
                "cached schedule counters")
    baseline = {
        "cache_key": ["selftest-input", CACHE_SEMANTICS,
                      NORMALIZED_SEMANTICS_DIGEST, "E3", 1, [1] * 18],
        "group_type": "E3", "slot_order": list(range(1, 12)),
        "fox_term": ["0100", 1], "prefix_inverse": "00",
        "boundary_descriptor": {"block": 1, "relator_index": 1,
            "component": 1, "h_blob": "00", "h_inverse": "00",
            "base_coefficient": 1},
        "dual_support_decode": [["5201", 1]],
        "section_parent_letter": {"parent": [0, 1], "letter": [1, 2]},
        "typed_coordinate_blob": "00", "cache_hit_literal": True,
        "chunk_start": 0, "chunk_end": 4, "attempts_done": 4,
        "chunk_complete": True, "resume_order": [1, 2, 3, 4],
        "dual_progress_digest": NORMALIZED_SEMANTICS_DIGEST,
        "raw_mod3": False, "old_pivots_discarded": True,
        "coefficient": 2, "coefficient_inverse_row": True, "cube": -3,
        "resource_terminal": "UNKNOWN_RESOURCE:phase=positive_correction_dovetail:"
                            "cap=oracle_rounds:value=2:limit=1"}
    def validate_mutated(state):
        # First calculate the load-bearing answer on the same noncommutative
        # fixture.  Field checks below therefore cannot be a receipt-only
        # canary: every mutation is coupled to a fresh occurrence/echelon or
        # literal-word replay.
        expected_now = _checker_cached_toy_schedule(helper)
        require(expected_now["active_columns"] == expected["active_columns"] and
                expected_now["solution"] == expected["solution"] and
                expected_now["direct_all_seven_replay"] ==
                expected["direct_all_seven_replay"],
                "checker cached load-bearing transcript")
        normalized_row, _ = helper.independent_toy_column(
            {"generators": [[1, 0, 2], [0, 2, 1]]}, [], [1] * 18)
        require(normalized_row.get(helper.exponent_key(1)) == 1,
                "checker normalized occurrence callsite")
        space = helper.RowSpace(); pivot, origin = space.add(
            normalized_row, 1)
        rem, recovered = space.reduce({key: 2 * value % 3
                                       for key, value in normalized_row.items()})
        require(pivot is not None and origin == {1: 1} and not rem and
                recovered == {1: 2}, "checker cached coefficient replay")
        require(state["cache_key"] == baseline["cache_key"] and
                state["group_type"] == baseline["group_type"] and
                state["slot_order"] == baseline["slot_order"],
                "checker cache key/group/slot replay")
        require(state["fox_term"] == baseline["fox_term"] and
                state["prefix_inverse"] == baseline["prefix_inverse"] and
                state["boundary_descriptor"] == baseline["boundary_descriptor"],
                "checker Fox/boundary descriptor replay")
        require(state["dual_support_decode"] == baseline["dual_support_decode"] and
                state["section_parent_letter"] == baseline["section_parent_letter"] and
                state["typed_coordinate_blob"] == baseline["typed_coordinate_blob"],
                "checker support/section/blob replay")
        require(state["cache_hit_literal"] is True and
                state["chunk_start"] == 0 and state["chunk_end"] == 4 and
                state["attempts_done"] == 4 and state["chunk_complete"] is True and
                state["resume_order"] == [1, 2, 3, 4],
                "checker cache hit/chunk resume replay")
        require(state["dual_progress_digest"] == NORMALIZED_SEMANTICS_DIGEST and
                state["raw_mod3"] is False and
                state["old_pivots_discarded"] is True,
                "checker dual/rank-zero replay")
        require(state["coefficient"] == 2 and
                state["coefficient_inverse_row"] is True,
                "checker coefficient-two replay")
        relation = [1] * 18
        direct = helper.toy_fox(relation,
                                [tuple(row) for row in ((1, 0, 2), (0, 2, 1))], 2)
        inverse_direct = helper.toy_fox(list(inv(relation)),
                                        [tuple(row) for row in ((1, 0, 2), (0, 2, 1))], 2)
        expected_inverse = {key: (-value) % 3 for key, value in direct.items()
                            if (-value) % 3}
        require(inverse_direct == expected_inverse,
                "checker inverse-word not repetition")
        closed = exactify([1] * 54 + [2] * 54, [2] * 36,
                          [1] * 18 + [2] * 144, [-1] * 18 + [-2] * 54)
        require(state["cube"] == -3 and exp(closed[0]) == (0, 0),
                "checker exactification cube replay")
        require(state["resource_terminal"].startswith(
            "UNKNOWN_RESOURCE:phase=positive_correction_dovetail:"),
                "checker typed resource terminal")
    mutators = {
        "cache_key_component": lambda s: s["cache_key"].__setitem__(3, "E4"),
        "stale_group_type": lambda s: s.__setitem__("group_type", "E4"),
        "slot_sign_order": lambda s: s["slot_order"].reverse(),
        "fox_term": lambda s: s["fox_term"].__setitem__(1, 2),
        "prefix_inverse": lambda s: s.__setitem__("prefix_inverse", "01"),
        "boundary_descriptor": lambda s: s["boundary_descriptor"].__setitem__("component", 2),
        "dual_support_decode": lambda s: s.__setitem__("dual_support_decode", [["5202", 1]]),
        "section_parent_letter": lambda s: s["section_parent_letter"]["letter"].__setitem__(0, 2),
        "typed_coordinate_blob": lambda s: s.__setitem__("typed_coordinate_blob", "01"),
        "cache_hit_without_literal": lambda s: s.__setitem__("cache_hit_literal", False),
        "chunk_end_advanced": lambda s: s.__setitem__("chunk_end", 5),
        "incomplete_row_complete": lambda s: s.__setitem__("chunk_complete", False),
        "skipped_resume_candidate": lambda s: s.__setitem__("resume_order", [1, 3, 4]),
        "stale_dual_progress": lambda s: s.__setitem__("dual_progress_digest", "stale"),
        "raw_mod3_semantics": lambda s: s.__setitem__("raw_mod3", True),
        "old_pivot_reuse": lambda s: s.__setitem__("old_pivots_discarded", False),
        "coefficient_two_repetition": lambda s: s.__setitem__("coefficient", 1),
        "exactification_cube": lambda s: s.__setitem__("cube", 3),
        "resource_stop_terminal_change": lambda s: s.__setitem__("resource_terminal", COMMON),
    }
    rejected = []
    for name in CACHE_MUTATIONS:
        mutated = copy.deepcopy(baseline); mutators[name](mutated)
        try:
            validate_mutated(mutated)
        except RuntimeError:
            rejected.append(name)
    require(tuple(rejected) == CACHE_MUTATIONS,
            "checker did not reject all cached mutations")


def sparse_rank(rows):
    pivots = {}
    for initial in rows:
        row = dict(initial)
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = 1 if row[pivot] == 1 else 2
                pivots[pivot] = {key: scale * value % 3 for key, value in row.items()}
                break
            base = pivots[pivot]
            scale = row[pivot]
            for key, value in base.items():
                row[key] = (row.get(key, 0) - scale * value) % 3
                if not row[key]:
                    row.pop(key)
    return len(pivots)


def sparse_digest(row):
    payload = bytearray()
    for key in sorted(row):
        payload.extend(len(key).to_bytes(4, "big")); payload.extend(key)
        payload.append(int(row[key]) % 3)
    return digest(bytes(payload))


def vector_rank(vectors):
    basis = {}
    for vector in vectors:
        row = [int(x) % 3 for x in vector]
        for pivot, base in sorted(basis.items()):
            if row[pivot]:
                scale = row[pivot] * (1 if base[pivot] == 1 else 2) % 3
                row = [(a - scale * b) % 3 for a, b in zip(row, base)]
        pivots = [i for i, value in enumerate(row) if value]
        if pivots:
            pivot = pivots[0]
            scale = 1 if row[pivot] == 1 else 2
            basis[pivot] = [(scale * value) % 3 for value in row]
    return len(basis)


def sparse_rows(receipt):
    rows = []
    for record in receipt.get("columns", []):
        rows.append({bytes.fromhex(str(item[0])): int(item[1]) % 3
                     for item in record.get("sparse_row", [])})
    return [{key: value for key, value in row.items() if not key.startswith(b"E")}
            for row in rows]


def ancestry(rows, nus):
    pivots, found = {}, []
    for index, initial in enumerate(rows, 1):
        row, coeff = dict(initial), {index: 1}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = 1 if row[pivot] == 1 else 2
                pivots[pivot] = ({key: scale * value % 3 for key, value in row.items()},
                                 {key: scale * value % 3 for key, value in coeff.items()})
                break
            base, base_coeff = pivots[pivot]
            scale = row[pivot]
            for key, value in base.items():
                row[key] = (row.get(key, 0) - scale * value) % 3
                if not row[key]: row.pop(key)
            for key, value in base_coeff.items():
                coeff[key] = (coeff.get(key, 0) - scale * value) % 3
                if not coeff[key]: coeff.pop(key)
        if not row and coeff:
            value = [0, 0]
            for column, scalar in coeff.items():
                value[0] = (value[0] + scalar * nus[column - 1][0]) % 3
                value[1] = (value[1] + scalar * nus[column - 1][1]) % 3
            if tuple(value) != (0, 0):
                found.append({"coefficients": [[key, scalar] for key, scalar in sorted(coeff.items())],
                              "nu": value})
    selected = []
    for candidate in found:
        if len(selected) < 2 and vector_rank([item["nu"] for item in selected] + [candidate["nu"]]) > len(selected):
            selected.append(candidate)
    return selected


def validate_roster_exponent_lattice(runtime):
    """Replay the authenticated 6,441-word integer exponent certificate."""
    roster = runtime["obj"].get("roster", [])
    if len(roster) != 6441:
        raise RuntimeError("independent roster cardinality")
    actual = {exp(record["word"]) for record in roster}
    expected = {(0, 0), (-36, 0), (36, 0), (-72, 0), (72, 0),
                (0, -36), (0, 36), (0, -54), (0, 54), (0, -72),
                (-36, -36), (-36, 36), (36, 36), (-72, 36),
                (-18, -54), (18, 144)}
    if actual != expected or len(actual) != 16:
        raise RuntimeError("registered 16-vector exponent set")
    if any(x % 18 or y % 18 for x, y in actual):
        raise RuntimeError("first inclusion exponent lattice")
    # The two registered defect words give the reverse inclusion generators.
    named = {record.get("ordinal"): exp(record["word"]) for record in roster
             if record.get("layer") == "q0_relator" and record.get("ordinal") in (3, 9, 12)}
    if named.get(3) != (0, 36) or named.get(9) != (18, 144) or named.get(12) != (-18, -54):
        raise RuntimeError("named kernel-word exponent vectors")
    v0 = (named[9][0] + named[12][0] - 2 * named[3][0],
          named[9][1] + named[12][1] - 2 * named[3][1])
    u0 = (named[9][0] - 8 * v0[0], named[9][1] - 8 * v0[1])
    if v0 != (0, 18) or u0 != (18, 0):
        raise RuntimeError("reverse inclusion 18Z2 generators")


def check_toy(receipt):
    if receipt.get("schema") != SELFTEST_SCHEMA or receipt.get("status") != "PASS":
        raise RuntimeError("bad selftest schema/status")
    expected = SELFTEST_TERMINAL
    if receipt.get("terminal") != expected:
        raise RuntimeError("bad selftest terminal")
    controls = receipt.get("mutation_controls", {})
    if controls.get("attempted") != 18 or controls.get("rejected") != 18:
        raise RuntimeError("mutation controls are not executed/rejected")
    if tuple(controls.get("names", ())) != MUTATIONS:
        raise RuntimeError("mutation list mismatch")
    base = {"divisor": 18, "sign": 1, "roster_ordinal": 3,
            "conjugator_exponent": 0, "boundary_tail": [0, 0], "raw_mod3": False,
            "target_tail": [0, 0], "old_pivots": False, "coefficient": 2,
            "divisible_54": True, "u0_formula": "r9*v0^-8", "v0_formula": "r9*r12*r3^-2",
            "cube": -3, "right_order": "base*correction", "pentagon": "printed",
            "hexagon_1": True, "hexagon_2": True, "source_word": [1] * 18,
            "boundary_inserted": False}
    live_checker = load_live_checker()
    live_original_pair = live_checker.exponent_pair
    install_normalized_checker_semantics(live_checker)
    toy_input = {"generators": [[1, 0, 2], [0, 2, 1]]}
    baseline_actual, _ = live_checker.independent_toy_column(
        toy_input, [], [1] * 18)
    validate_cached_schedule_selftest(receipt, live_checker)
    def valid(state):
        # Drive the same independent occurrence, echelon, coefficient and
        # literal-word calculations as the producer SELFTEST.  Mutated
        # metadata never reaches a flag-only acceptance path.
        chosen = list(state["source_word"])
        if state["roster_ordinal"] != 3 and chosen == [1] * 18:
            chosen = [2] * 18
        chosen = [state["sign"] * letter for letter in chosen]
        delta = [2] * state["conjugator_exponent"]
        actual, occurrences = live_checker.independent_toy_column(
            toy_input, delta, chosen)
        actual_tail = [actual.get(live_checker.exponent_key(1), 0),
                       actual.get(live_checker.exponent_key(2), 0)]
        expected_tail = list(nu(chosen, state["divisor"]))
        if actual_tail != expected_tail:
            raise RuntimeError("actual helper normalized E-tail replay")
        if state["conjugator_exponent"] == 0 and state["roster_ordinal"] == 3:
            if actual != baseline_actual:
                raise RuntimeError("actual helper occurrence baseline replay")
        elif actual == baseline_actual:
            raise RuntimeError("actual helper mutation changed no occurrence")
        if len(occurrences) != 3 or [item["ordinal"] for item in occurrences] != [1, 2, 3]:
            raise RuntimeError("actual helper occurrence transcript")
        if state["divisor"] != 18 or state["sign"] != 1:
            raise RuntimeError("normalized divisor/sign replay")
        if state["roster_ordinal"] != 3 or state["conjugator_exponent"] != 0:
            raise RuntimeError("roster/conjugator provenance replay")
        if nu(chosen, state["divisor"]) != (1, 0):
            raise RuntimeError("normalized source membership replay")
        contains = lambda rows, target: vector_rank(rows) == vector_rank(rows + [target])
        normalized_row = list(nu(chosen))
        if not contains([normalized_row], [1, 0]):
            raise RuntimeError("normalized combined echelon membership")
        space = live_checker.RowSpace()
        if state["old_pivots"]:
            space.add({b"OLD-PIVOT": 1}, 99)
        pivot, origin = space.add(actual, 1)
        target = {key: (2 * value) % 3 for key, value in actual.items()
                  if (2 * value) % 3}
        if state["target_tail"] != [0, 0]:
            target[live_checker.exponent_key(2)] = 1
        remainder, solution = space.reduce(target)
        if remainder or solution.get(1) != 2 or len(space.pivots) != 1 or origin.get(1) != 1:
            raise RuntimeError("rank-zero coefficient/ancestry replay")
        if state["coefficient"] != solution[1]:
            raise RuntimeError("coefficient-two inverse replay")
        raw_column = {key: value for key, value in actual.items()
                      if not key.startswith(b"E")}
        raw_space = live_checker.RowSpace()
        if raw_column:
            raw_space.add(raw_column, 1)
        raw_remainder, _ = raw_space.reduce(target)
        if not raw_remainder or state["raw_mod3"]:
            raise RuntimeError("raw-vacuous membership substitution")
        if state["boundary_tail"] != [0, 0]:
            raise RuntimeError("boundary tail replay")
        r3, r9, r12 = [2] * 36, [1] * 18 + [2] * 144, [-1] * 18 + [-2] * 54
        c_star = mul([1] * 54 + [2] * 54,
                     [2] * 18 if state["boundary_inserted"] else [])
        closed = exactify(c_star, r3, r9, r12)
        if state["divisible_54"] is not True or exp(closed[0]) != (0, 0):
            raise RuntimeError("exact direct word replay")
        v0_replayed = mul(r9, r12, inv(r3) * 2)
        v0_state = (v0_replayed if state["v0_formula"] == "r9*r12*r3^-2"
                    else mul(r9, r12, power(r3, 2)))
        u0_state = (mul(r9, inv(v0_state) * 8)
                    if state["u0_formula"] == "r9*v0^-8"
                    else mul(r9, power(v0_state, 8)))
        e = exp(c_star)
        if e[0] % 54 or e[1] % 54:
            raise RuntimeError("exactification integer divisibility replay")
        a, b = e[0] // 54, e[1] // 54
        h_state = mul(power(u0_state, state["cube"] * a),
                      power(v0_state, state["cube"] * b))
        c_state = mul(c_star, h_state)
        if (v0_state != closed[1] or u0_state != closed[2] or
                state["u0_formula"] != "r9*v0^-8" or
                state["v0_formula"] != "r9*r12*r3^-2" or
                state["cube"] != -3 or exp(c_state) != (0, 0)):
            raise RuntimeError("exactification formula/direct replay")
        base_word = [1, 2]
        right_word = mul(base_word, c_state)
        candidate_right = (right_word if state["right_order"] == "base*correction"
                           else mul(c_state, base_word))
        if candidate_right != right_word or state["right_order"] != "base*correction":
            raise RuntimeError("right-correction order replay")
        factors = ([1], [2], [-1], [-2], [1, 2])
        printed = mul(factors[1], factors[3], factors[0], inv(factors[2]), inv(factors[4]))
        candidate_pentagon = (printed if state["pentagon"] == "printed" else
                              mul(factors[4], inv(factors[2]), factors[0], factors[3], factors[1]))
        if candidate_pentagon != printed or state["pentagon"] != "printed":
            raise RuntimeError("five-factor printed pentagon replay")
        hexagon_1 = mul([1], [2], [-1], [-2])
        hexagon_2 = mul([2], [1], [-2], [-1])
        if state["hexagon_1"] is not True or state["hexagon_2"] is not True or hexagon_1 == hexagon_2:
            raise RuntimeError("literal hexagon replay")
        if state["target_tail"] != [0, 0] or state["old_pivots"] or \
                state["source_word"] != [1] * 18 or state["boundary_inserted"]:
            raise RuntimeError("target/pivot/source boundary replay")
    fields = ("divisor", "sign", "roster_ordinal", "conjugator_exponent",
              "boundary_tail", "raw_mod3", "target_tail", "old_pivots", "coefficient",
              "divisible_54", "u0_formula", "v0_formula", "cube", "right_order",
              "pentagon", "hexagon_1", "source_word", "boundary_inserted")
    for name, field in zip(MUTATIONS, fields):
        state = copy.deepcopy(base)
        if field in ("boundary_tail", "target_tail"):
            state[field] = [1, 0]
        elif field == "source_word":
            state[field] = [2] * 18
        elif field in ("raw_mod3", "old_pivots", "divisible_54", "boundary_inserted",
                       "hexagon_1"):
            state[field] = not state[field]
        elif field == "coefficient":
            state[field] = 1
        elif field in ("divisor", "roster_ordinal", "conjugator_exponent", "cube"):
            state[field] += 1
        elif field == "sign":
            state[field] = -1
        elif field == "right_order":
            state[field] = "correction*base"
        elif field == "pentagon":
            state[field] = "reversed"
        elif field == "u0_formula":
            state[field] = "r9*v0^8"
        elif field == "v0_formula":
            state[field] = "r9*r12*r3^2"
        try:
            valid(state)
        except RuntimeError:
            pass
        else:
            raise RuntimeError("mutation accepted: " + name)
    toy = receipt.get("toy", {})
    if toy.get("kernel_lattice") != "18Z^2":
        raise RuntimeError("kernel lattice claim mismatch")
    if toy.get("raw_rows") != [[0, 0], [0, 0]]:
        raise RuntimeError("raw mod-3 substitution accepted")
    if toy.get("normalized_rows") != [[1, 0], [0, 1]]:
        raise RuntimeError("normalized rows mismatch")
    if toy.get("boundary_tail") != [0, 0]:
        raise RuntimeError("boundary tail is nonzero")
    if toy.get("membership") != {"raw_target_in_span": False,
                                  "normalized_target_in_span": True}:
        raise RuntimeError("raw/normalized membership distinction missing")
    regression = receipt.get("load_bearing_normalization", {})
    if regression.get("patched_v1_exponent_pair") is not True or \
            regression.get("integer_signed_counter") is not True or \
            regression.get("actual_E1_E2") != [1, 0] or \
            regression.get("raw_mod3_control") != [0, 0] or \
            regression.get("actual_occurrence_column") is not True:
        raise RuntimeError("load-bearing normalization regression absent")
    rank = toy.get("rank_audit", {})
    basis = rank.get("basis", [])
    preimages = rank.get("word_preimages", [])
    if (rank.get("rank_B_nu", 0) - rank.get("rank_B", 0) != rank.get("dim_nu_kernel_B") or
            len(basis) != rank.get("dim_nu_kernel_B") or vector_rank(basis) != len(basis) or
            len(preimages) != len(basis) or
            [list(nu(item)) for item in preimages] != basis):
        raise RuntimeError("normalized kernel-rank audit mismatch")
    production_trace = receipt.get("production_path_selftest", {})
    if production_trace.get("occurrence_direct_hook") is not True or \
            production_trace.get("actual_allseven_occurrence") is not True or \
            production_trace.get("actual_allseven_direct") is not True or \
            production_trace.get("normalized_E1") != 1 or \
            production_trace.get("raw_E1") != 0 or \
             production_trace.get("positive_add_column") is not True or \
             production_trace.get("rank_zero_checkpoint_rebuild") is not True or \
             production_trace.get("rank_zero_conversion") is not True or \
            production_trace.get("stored_pivots_discarded") is not True or \
            production_trace.get("coefficient_recovery") != [[1, 1]] or \
            production_trace.get("basis_ancestry") != [[1, 1]]:
        raise RuntimeError("load-bearing production SELFTEST trace absent")
    overcap = production_trace.get("over_cap_resume_preflight", {})
    expected_overcap_terminal = (
        "UNKNOWN_RESOURCE:phase=resume_rebuild:cap=candidate_words:"
        "value=2:limit=1")
    if overcap.get("typed_resource_terminal") != expected_overcap_terminal or \
            overcap.get("checkpoint_written_before_search_assignment") is not True or \
            overcap.get("safe_chunk_end") != 4 or \
            overcap.get("carried_candidate_words") != 2:
        raise RuntimeError("independent over-cap resume preflight replay failed")
    # Execute the independent normalized and noncommutative checks.
    for w, expected_nu in (([1] * 18, (1, 0)), ([2] * 18, (0, 1))):
        if tuple(x % 3 for x in exp(w)) != (0, 0) or nu(w) != expected_nu:
            raise RuntimeError("independent toy replay failed")
    if reduce_word((1, 2, -1, -2)) != (1, 2, -1, -2):
        raise RuntimeError("free reduction incorrectly commuted letters")
    r3, r9, r12 = [2] * 36, [1] * 18 + [2] * 144, [-1] * 18 + [-2] * 54
    _, v0, u0, h = exactify([1] * 54 + [2] * 54, r3, r9, r12)
    if exp(v0) != (0, 18) or exp(u0) != (18, 0) or exp(h) != (-54, -54):
        raise RuntimeError("independent exactification replay failed")
    task179 = receipt.get("task179_selftest")
    if not isinstance(task179, dict) or receipt.get("full_v1_schedule_selftest") is not True:
        raise RuntimeError("full task179 selftest receipt absent")
    checker = live_checker
    original_pair = live_original_pair
    if checker.exponent_pair([1] * 18) != (1, 0):
        raise RuntimeError("independent helper normalization regression")
    toy_input = {"generators": [[1, 0, 2], [0, 2, 1]]}
    normalized_row, _ = checker.independent_toy_column(toy_input, [], [1] * 18)
    if normalized_row.get(checker.exponent_key(1)) != 1:
        raise RuntimeError("independent helper occurrence E1 replay")
    checker.exponent_pair = original_pair
    raw_row, _ = checker.independent_toy_column(toy_input, [], [1] * 18)
    if checker.exponent_key(1) in raw_row or checker.exponent_key(2) in raw_row:
        raise RuntimeError("independent raw occurrence is not vacuous")
    row = {checker.exponent_key(1): 1}
    space = checker.RowSpace()
    pivot, origin = space.add(row, 1)
    remainder, solution = space.reduce(row)
    if pivot != checker.exponent_key(1) or origin != {1: 1} or remainder or solution != {1: 1}:
        raise RuntimeError("independent rank-zero/coefficient ancestry replay")
    checker.exponent_pair = original_pair
    checker.exponent_pair = original_pair
    with tempfile.TemporaryDirectory(prefix="d972-r07-check-selftest-") as temp:
        raw_path = Path(temp) / "task179-selftest.json"
        verdict = Path(temp) / "task179-selftest.verdict.json"
        raw_path.write_text(json.dumps(task179, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            rc = checker.main(["--mode", "SELFTEST", "--receipt", str(raw_path),
                               "--verdict", str(verdict)])
        if rc != 0:
            raise RuntimeError("independent full task179 SELFTEST rejected")
    return "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_CHECKER_PASS"


def validate_v3_checkpoint_contract(checkpoint):
    reject_forbidden_claims(checkpoint)
    require(checkpoint.get("schema") == SCHEMA and
            checkpoint.get("normalized_semantics") == CACHE_SEMANTICS and
            checkpoint.get("normalized_semantics_digest") ==
            NORMALIZED_SEMANTICS_DIGEST and
            checkpoint.get("normalized_semantics_callsites") ==
            list(NORMALIZED_SEMANTICS_CALLSITES),
            "v3 checkpoint semantic binding")
    contract = checkpoint.get("v3_cache_contract", {})
    require(contract.get("schema") == SCHEMA and
            contract.get("semantics") == CACHE_SEMANTICS and
            contract.get("semantics_digest") == NORMALIZED_SEMANTICS_DIGEST and
            contract.get("callsites") == list(NORMALIZED_SEMANTICS_CALLSITES) and
            contract.get("key_fields") == ["input_digest", "roster_layer",
                                             "roster_ordinal", "literal_word",
                                             "slot", "group_type", "basis_epoch",
                                             "normalized_semantics_digest"] and
            contract.get("chunk_limit") == CACHE_CHUNK_LIMIT and
            contract.get("canonical_ordering") == CACHE_ORDERING and
            contract.get("bounded_memory") is True and
            contract.get("rank_zero_replay") is True and
            contract.get("dual_dependent_recomputed") == [
                "support_join", "mod3_merge", "weighted_formula",
                "exact_pairing"] and
            contract.get("candidate_literal_direct_replay") is True and
            contract.get("candidate_basis_epoch_invalidation") is True,
            "v3 checkpoint cache contract")
    epoch = checkpoint.get("v3_epoch", {})
    require(epoch.get("input_sha256") == checkpoint.get("input_sha256") and
            epoch.get("target_sha256") == checkpoint.get("target_sha256") and
            epoch.get("normalized_semantics_digest") == NORMALIZED_SEMANTICS_DIGEST and
            epoch.get("dual_sha256") == checkpoint.get("current_dual_sha256") and
            epoch.get("dual_progress_sha256") == checkpoint.get("progress", {}).get(
                "correction", {}).get("dual_sha256"),
            "v3 checkpoint epoch dual binding")
    current_dual = checkpoint.get("current_dual")
    current_dual_digest = checkpoint.get("current_dual_sha256")
    if current_dual is None:
        require(current_dual_digest is None, "v3 checkpoint null dual digest")
    else:
        require(isinstance(current_dual, list) and
                current_dual_digest == digest(canonical(current_dual)),
                "v3 checkpoint current dual digest")
    monitor = checkpoint.get("monitor")
    validate_monitor_snapshot(monitor)
    chunk = checkpoint.get("v3_chunk", {})
    require(type(chunk.get("chunk_start")) is int and
            type(chunk.get("chunk_end")) is int and
            type(chunk.get("attempts_done")) is int and
            chunk.get("max_attempts") == CACHE_CHUNK_LIMIT and
            chunk.get("canonical_ordering") == CACHE_ORDERING and
            chunk.get("chunk_start") >= 0 and
            chunk.get("chunk_end") >= chunk.get("chunk_start") and
            chunk.get("attempts_done") ==
            chunk.get("chunk_end") - chunk.get("chunk_start") and
            0 <= chunk.get("attempts_done") <= CACHE_CHUNK_LIMIT and
            chunk.get("chunk_complete") is True,
            "v3 checkpoint chunk boundary")
    repeated = chunk.get("repeated_suffix")
    if repeated is not None:
        require(isinstance(repeated, dict) and
                type(repeated.get("safe_start")) is int and
                type(repeated.get("interrupted_end")) is int and
                type(repeated.get("attempts")) is int and
                repeated.get("max_attempts") == CACHE_CHUNK_LIMIT and
                repeated.get("replay_on_resume") is True and
                repeated.get("safe_start") == chunk.get("chunk_end") and
                repeated.get("interrupted_end") >= repeated.get("safe_start") and
                repeated.get("attempts") == repeated.get("interrupted_end") -
                repeated.get("safe_start") and
                0 <= repeated.get("attempts") <= CACHE_CHUNK_LIMIT and
                repeated.get("declared") ==
                (repeated.get("interrupted_end") > repeated.get("safe_start")),
                "v3 checkpoint repeated suffix contract")
    progress = checkpoint.get("progress", {})
    correction = progress.get("correction", {})
    cursor = correction.get("canonical_row_cursor")
    rows = correction.get("weighted_rows")
    require(type(cursor) is int and cursor >= 0 and isinstance(rows, dict),
            "v3 checkpoint canonical row state")
    for index in range(1, cursor + 1):
        state = rows.get(str(index))
        require(isinstance(state, dict) and state.get("complete") is True,
                "v3 checkpoint crosses incomplete row")
    require(chunk.get("canonical_row_cursor") == cursor,
            "v3 checkpoint chunk/cursor binding")
    validate_cached_weighted_rows(progress)
    history = checkpoint.get("resume_monitor_history")
    if history is not None:
        require(isinstance(history, dict) and
                set(history) == {"snapshot", "safe_chunk_end",
                                 "prior_repeated_suffix",
                                 "counter_fields", "limits_bound"} and
                history.get("counter_fields") == list(MONITOR_COUNTER_FIELDS) and
                history.get("limits_bound") is True and
                type(history.get("safe_chunk_end")) is int and
                history.get("safe_chunk_end") >= 0,
                "v3 resume monitor history envelope")
        prior_suffix = history.get("prior_repeated_suffix")
        if prior_suffix is not None:
            require(isinstance(prior_suffix, dict) and
                    set(prior_suffix) == {"declared", "safe_start",
                                          "interrupted_end", "attempts",
                                          "max_attempts", "replay_on_resume"},
                    "v3 resume repeated suffix history")
        prior_monitor = history["snapshot"]
        validate_monitor_snapshot(prior_monitor)
        require(monitor["limits"] == prior_monitor["limits"],
                "v3 resume monitor limits changed")
        safe_end = history["safe_chunk_end"]
        require(chunk.get("chunk_start") >= safe_end and
                chunk.get("chunk_end") >= chunk.get("chunk_start"),
                "v3 resume chunk regressed")
        for name in MONITOR_COUNTER_FIELDS:
            if name != "checkpoint_bytes":
                require(monitor["counters"][name] >=
                        prior_monitor["counters"][name],
                        "v3 resume monitor counter regressed")
        rebuild = checkpoint.get("resume_rebuild", {})
        require(rebuild.get("safe_chunk_end_recovered") == safe_end and
                rebuild.get("prior_monitor_elapsed_seconds") ==
                prior_monitor["elapsed_seconds"],
                "v3 resume monitor history not bound")
    elif checkpoint.get("resume_rebuild") is not None:
        raise RuntimeError("v3 resume rebuild missing monitor history")
    stats = checkpoint.get("v3_cache_stats", {})
    require(isinstance(stats, dict) and stats.get("bounded") is True and
            all(type(stats.get(field)) is int and stats[field] >= 0
                for field in ("hits", "misses", "evictions", "bytes",
                              "regenerated_literals")),
            "v3 checkpoint cache statistics")
    require(stats.get("candidate_basis_epochs") is not None and
            all(type(x) is int and x >= 0 for x in
                stats.get("candidate_basis_epochs", [])),
            "v3 checkpoint candidate basis epochs")
    caches = stats.get("caches")
    if caches is not None:
        require(isinstance(caches, list) and len(caches) == 3 and
                [item.get("name") for item in caches] == [
                    "fox_template_and_base", "gamma_section_candidate_values",
                    "pb3_pb4_boundary_descriptors"] and
                all(isinstance(item, dict) and item.get("max_bytes", 0) > 0
                    for item in caches),
                "v3 checkpoint per-cache statistics")


def validate_v3_receipt_cache_contract(receipt):
    schedule = receipt.get("cached_schedule", {})
    require(schedule.get("schema") == SCHEMA and
            schedule.get("semantics") == CACHE_SEMANTICS and
            schedule.get("semantics_digest") == NORMALIZED_SEMANTICS_DIGEST and
            schedule.get("callsites") == list(NORMALIZED_SEMANTICS_CALLSITES) and
            schedule.get("proof_pins") == {
                label: list(value) for label, value in PROOF_PINS.items()
            } and
            schedule.get("fixed_chunk_attempts") == CACHE_CHUNK_LIMIT and
            schedule.get("canonical_ordering") == CACHE_ORDERING and
            schedule.get("dual_independent_templates") is True and
            schedule.get("eleven_slot_fox_templates") is True and
            schedule.get("three_fixed_base_gradients") is True and
            schedule.get("complete_pb3_pb4_descriptors") is True and
            schedule.get("boundary_descriptor_roster") is True and
            schedule.get("candidate_value_cache_bounded") is True and
            schedule.get("same_completed_schedule_as_v2") is True and
            schedule.get("candidate_basis_epoch_invalidation") is True,
            "v3 receipt cache contract")
    stats = receipt.get("v3_cache_stats", {})
    if stats.get("status") != "not_started":
        require(isinstance(stats, dict) and stats.get("bounded") is True and
                all(type(stats.get(field)) is int and stats[field] >= 0
                    for field in ("hits", "misses", "evictions", "bytes",
                                  "regenerated_literals")),
                "v3 receipt cache statistics")
        require(int(stats.get("bytes", 0)) <= 96 * 1024 * 1024,
                "v3 aggregate Fox residency cap")
        caches = stats.get("caches")
        require(isinstance(caches, list) and len(caches) == 3 and
                [item.get("name") for item in caches] == [
                    "fox_template_and_base", "gamma_section_candidate_values",
                    "pb3_pb4_boundary_descriptors"] and
                all(isinstance(item, dict) and item.get("max_bytes", 0) > 0
                    and all(type(item.get(field)) is int and item[field] >= 0
                            for field in ("hits", "misses", "evictions",
                                          "bytes", "regenerated_literals"))
                    for item in caches),
                 "v3 per-cache statistics")
        require(stats.get("candidate_basis_epochs") is not None and
                all(type(x) is int and x >= 0 for x in
                    stats.get("candidate_basis_epochs", [])),
                "v3 candidate basis epoch binding")
        descriptors = stats.get("boundary_descriptors")
        require(isinstance(descriptors, dict) and
                type(descriptors.get("count")) is int and
                descriptors["count"] > 0 and
                isinstance(descriptors.get("sha256"), str) and
                descriptors.get("sorted") is True and
                descriptors.get("support_times_occurrence") is True,
                "v3 boundary descriptor statistics")


def check_production(receipt, helper=None):
    if receipt.get("schema") != SCHEMA:
        raise RuntimeError("bad production schema")
    validate_outer_seal(receipt)
    reject_forbidden_claims(receipt)
    validate_v3_receipt_cache_contract(receipt)
    terminal = receipt.get("terminal", "")
    if terminal == COMMON:
        if receipt.get("status") != "COMMON_WORD":
            raise RuntimeError("common terminal/status mismatch")
        checkpoint_ref = receipt.get("checkpoint")
        if checkpoint_ref is not None:
            cp_path = ROOT / "ci" / "out" / str(checkpoint_ref.get("path", ""))
            if not cp_path.is_file():
                raise RuntimeError("common v2 checkpoint missing")
            cp_raw = cp_path.read_bytes()
            if len(cp_raw) != checkpoint_ref.get("bytes") or digest(cp_raw) != checkpoint_ref.get("sha256"):
                raise RuntimeError("common v2 checkpoint identity")
            cp = json.loads(cp_raw.decode("utf-8")); validate_outer_seal(cp)
            validate_v3_checkpoint_contract(cp)
            if cp.get("schema") != SCHEMA or cp.get("normalized_semantics_digest") != NORMALIZED_SEMANTICS_DIGEST or \
                    cp.get("normalized_semantics_callsites") != list(NORMALIZED_SEMANTICS_CALLSITES):
                raise RuntimeError("common v2 checkpoint semantic binding")
            if receipt.get("v2_schedule", {}).get("resume_replayed_from_rank_zero"):
                rebuild = cp.get("resume_rebuild", {})
                if rebuild.get("rank_zero_replayed") is not True or \
                        rebuild.get("stored_pivots_discarded") is not True or \
                        rebuild.get("stored_reduced_target_discarded") is not True or \
                        rebuild.get("stored_current_dual_discarded") is not True or \
                        type(rebuild.get("stored_oracle_progress_discarded")) is not bool or \
                        type(rebuild.get("safe_progress_preserved")) is not bool or \
                        type(rebuild.get("safe_boundary_preserved")) is not bool or \
                        type(rebuild.get("safe_chunk_replayed_without_suffix")) is not bool or \
                        rebuild.get("monitor_limits_bound") is not True or \
                        rebuild.get("monitor_counters_carried_forward") is not True or \
                        type(rebuild.get("prior_monitor_elapsed_seconds")) not in (int, float) or \
                        type(rebuild.get("safe_chunk_end_recovered")) is not int or \
                        rebuild.get("safe_chunk_end_recovered") < 0 or \
                        (rebuild.get("safe_progress_preserved") and
                         rebuild.get("stored_oracle_progress_discarded")) or \
                        (rebuild.get("safe_chunk_replayed_without_suffix") !=
                         rebuild.get("safe_progress_preserved")) or \
                        (rebuild.get("safe_boundary_preserved") and
                         not rebuild.get("safe_progress_preserved")) or \
                        rebuild.get("stored_state_fields_discarded") != [
                            "pivot_order", "pivot_rows_sha256", "reduced_target",
                            "current_dual", "current_dual_sha256",
                            "target_solution_if_zero", "monitor",
                            "coarse_inverse_index", "resume_rebuild", "v3_epoch"] or \
                        rebuild.get("column_provenance_authenticated") is not True or \
                        rebuild.get("stored_columns_replayed_from_zero") is not True or \
                        rebuild.get("rank_zero_replay_source") != \
                        "authenticated columns/provenance" or \
                        rebuild.get("v3_cache_and_chunk_state_discarded") is not True:
                    raise RuntimeError("resume checkpoint retained stale state")
        ncols = receipt.get("normalized_columns")
        if not isinstance(ncols, list) or not ncols:
            raise RuntimeError("normalized columns absent")
        for column in ncols:
            if column.get("nu") is None or column.get("boundary_zero_tail") not in (True, False):
                raise RuntimeError("normalized column provenance")
            source = column.get("source_word", [])
            if column.get("nu") != list(nu(source)):
                raise RuntimeError("normalized column recomputation")
            if column.get("boundary_zero_tail") and source:
                raise RuntimeError("boundary carries a source word")
        if receipt.get("normalized_exponent_contract", {}).get("integer_gate") is not True:
            raise RuntimeError("normalized exponent gate absent")
        audit = receipt.get("rank_audit", {})
        raw_records = receipt.get("columns", [])
        if len(raw_records) != len(ncols):
            raise RuntimeError("normalized/raw column count mismatch")
        b_rows = sparse_rows(receipt)
        rank_b = sparse_rank(b_rows)
        # These are the authenticated helper's actual v1 exponent keys; the
        # v2 layer must not invent a parallel V2-NU namespace.
        exponent_key = helper.exponent_key if helper is not None else (
            lambda index: b"E" + bytes((index,)))
        ekeys = (exponent_key(1), exponent_key(2))
        if ekeys != (b"E\x01", b"E\x02"):
            raise RuntimeError("helper exponent-key contract")
        for record, column in zip(raw_records, ncols):
            raw = {bytes.fromhex(str(item[0])): int(item[1]) % 3
                   for item in record.get("sparse_row", [])}
            actual = [raw.get(ekeys[0], 0), raw.get(ekeys[1], 0)]
            if actual != column.get("nu"):
                raise RuntimeError("receipt E1/E2 tail is not normalized nu")
            if column.get("boundary_zero_tail") and actual != [0, 0]:
                raise RuntimeError("boundary E tail is nonzero")
        augmented = []
        for row, column in zip(b_rows, ncols):
            row = dict(row)
            if column["nu"][0]:
                row[ekeys[0]] = column["nu"][0]
            if column["nu"][1]:
                row[ekeys[1]] = column["nu"][1]
            augmented.append(row)
        rank_nu = sparse_rank(augmented)
        if audit.get("rank_B") != rank_b or audit.get("rank_B_nu") != rank_nu or \
                rank_nu - rank_b != audit.get("dim_nu_kernel_B"):
            raise RuntimeError("rank(B,nu) identity")
        echelon = receipt.get("normalized_echelon", {})
        if echelon.get("restarted_from_rank") != 0 or \
                echelon.get("rank") != rank_nu or \
                echelon.get("actual_combined_rank") != rank_nu or \
                echelon.get("actual_combined_pivot_count") != rank_nu or \
                echelon.get("basis_pivot_count") != len(receipt.get("columns", [])):
            raise RuntimeError("combined normalized echelon audit")
        if echelon.get("normalized_tails") != [column.get("nu") for column in ncols]:
            raise RuntimeError("normalized retained tail transcript")
        expected_digests = []
        for record in receipt.get("columns", []):
            raw = {bytes.fromhex(str(item[0])): int(item[1]) % 3
                   for item in record.get("sparse_row", [])}
            expected_digests.append(sparse_digest(raw))
        if echelon.get("combined_row_digests") != expected_digests:
            raise RuntimeError("combined retained row transcript")
        if receipt.get("normalized_basis_rebuilt_from_rank_zero") is not True or \
                len(audit.get("basis", [])) != audit.get("dim_nu_kernel_B") or \
                len(audit.get("word_preimages", [])) != audit.get("dim_nu_kernel_B"):
            raise RuntimeError("normalized basis provenance")
        contract = receipt.get("normalized_exponent_contract", {})
        if contract.get("semantics_digest") != NORMALIZED_SEMANTICS_DIGEST or \
                contract.get("patched_callsites") != list(NORMALIZED_SEMANTICS_CALLSITES):
            raise RuntimeError("normalized semantics digest")
        computed_ancestry = ancestry(b_rows, [column["nu"] for column in ncols])
        recorded_ancestry = receipt.get("nu_kernel_ancestry", [])
        if [item.get("coefficients") for item in recorded_ancestry] != [
                item["coefficients"] for item in computed_ancestry]:
            raise RuntimeError("kernel coefficient ancestry mismatch")
        if audit.get("basis") != [item["nu"] for item in computed_ancestry] or \
                audit.get("word_preimages") != [item.get("correction_word_replay", [])
                                                  for item in recorded_ancestry]:
            raise RuntimeError("independent nu-kernel basis provenance")
        if echelon.get("basis_words") != audit.get("word_preimages"):
            raise RuntimeError("normalized echelon basis-word transcript")
        for item in recorded_ancestry:
            if item.get("B_zero_recomputed") is not True:
                raise RuntimeError("kernel B-zero was asserted")
            expected_boundary = []
            expected_correction = []
            correction_word = ()
            for column, coefficient in item.get("coefficients", []):
                if ncols[column - 1].get("boundary_zero_tail"):
                    expected_boundary.append([column, coefficient])
                else:
                    expected_correction.append([column, coefficient])
                    source_word = ncols[column - 1].get("source_word", [])
                    correction_word = mul(
                        correction_word,
                        source_word if coefficient == 1 else inv(source_word))
            if item.get("boundary_coefficients") != expected_boundary or \
                    item.get("correction_coefficients") != expected_correction or \
                    item.get("correction_word_replay") != list(correction_word) or \
                    item.get("recomputed_nu") != list(nu(correction_word)):
                raise RuntimeError("kernel source/coefficient provenance replay")
            zero = {}
            for column, coefficient in item.get("coefficients", []):
                for key, value in b_rows[column - 1].items():
                    value0 = (zero.get(key, 0) + coefficient * value) % 3
                    if value0: zero[key] = value0
                    elif key in zero: zero.pop(key)
            if zero or item.get("B_zero_row") != [] or item.get("B_zero_sha256") != sparse_digest(zero):
                raise RuntimeError("kernel B-zero replay mismatch")
            direct_replay = item.get("direct_correction_replay", {})
            source = item.get("correction_word_replay", [])
            if direct_replay.get("corrected_word") != reduce_word(
                    (receipt.get("g760") or []) + source):
                raise RuntimeError("kernel correction direct replay mismatch")
            if item.get("correction_boundary_zero_sha256") != sparse_digest({}):
                raise RuntimeError("kernel correction-boundary zero digest")
        ex = receipt.get("exactification", {})
        if ex.get("positive_receipt") is not True or set(ex.get("r_words", {})) != {"3", "9", "12"}:
            raise RuntimeError("exactification provenance absent")
        factors = ex.get("factor_sources", {})
        if factors.get("correction_conjugates_only") is not True or \
                factors.get("registered_cubes") != ["r3", "r9", "r12"] or \
                factors.get("boundary_words_included") is not False:
            raise RuntimeError("exactification factor provenance")
        if ex.get("joint_kernel_replay") != {"r3": True, "r9": True, "r12": True,
                                              "u0": True, "v0": True}:
            raise RuntimeError("registered joint-kernel replay evidence absent")
        words = ex["r_words"]
        cstar = receipt.get("correction_word") or []
        closed = exactify(cstar, words["3"], words["9"], words["12"])
        if ex.get("exponents", {}).get("c_exact") != list(exp(closed[0])):
            raise RuntimeError("exactification replay digest/value")
        if receipt.get("boundary_words_not_inserted") is not True:
            raise RuntimeError("boundary correction contamination")
        direct = receipt.get("exact_direct_replay", {})
        if direct.get("joint_kernel") is not True or direct.get("right_g760_multiplication") is not True or \
                direct.get("hexagons") is not True or direct.get("pentagon_printed_order") is not True:
            raise RuntimeError("exact direct replay gates absent")
        literal = ex.get("literal", {})
        exact_word = literal.get("c_exact", [])
        replay = direct.get("replay", {})
        if direct.get("row") != direct.get("star_row"):
            raise RuntimeError("exact direct row differs from c_star row")
        parsed_direct = {bytes.fromhex(str(item[0])): int(item[1]) % 3
                         for item in direct.get("row", [])}
        parsed_star = {bytes.fromhex(str(item[0])): int(item[1]) % 3
                       for item in direct.get("star_row", [])}
        if direct.get("row_sha256") != sparse_digest(parsed_direct) or \
                direct.get("star_row_sha256") != sparse_digest(parsed_star):
            raise RuntimeError("exact direct row digest mismatch")
        if any(bytes.fromhex(str(item[0])).startswith(b"E") for item in direct.get("row", [])):
            raise RuntimeError("exact direct row has normalized tail")
        if replay.get("corrected_word") != reduce_word((receipt.get("g760") or []) + exact_word):
            raise RuntimeError("exact right multiplication replay mismatch")
        if exp(exact_word) != (0, 0):
            raise RuntimeError("exact word integer exponent replay mismatch")
    elif receipt.get("status") == "UNKNOWN" and terminal.startswith((UNKNOWN_INPUT + ":", "UNKNOWN_RESOURCE:")):
        checkpoint = receipt.get("checkpoint")
        if terminal.startswith("UNKNOWN_RESOURCE:"):
            parsed_terminal = validate_resource_terminal(terminal)
            cap = parsed_terminal["cap"]
            value_at_stop = parsed_terminal["value"]
            limit = parsed_terminal["limit"]
            monitor = receipt.get("monitor")
            snapshot = receipt.get("resource_monitor_snapshot")
            require(isinstance(monitor, dict) and snapshot == monitor,
                    "resource stop monitor snapshot is not bound")
            require(monitor.get("single_process") is True and
                    set(monitor) == {"phase", "elapsed_seconds", "rss_bytes",
                                     "limits", "counters", "single_process"},
                    "resource monitor snapshot schema")
            require(type(monitor.get("limits")) is dict and
                    set(monitor["limits"]) == {
                        "wall_seconds", "boundary_pairs", "fibre_scans",
                        "candidate_words", "retained_columns", "checkpoint_bytes",
                        "rss_bytes", "oracle_rounds", "global_roster"},
                    "resource monitor registered limits")
            require(type(monitor.get("counters")) is dict and
                    set(monitor["counters"]) == {
                        "boundary_pairs", "fibre_scans", "candidate_words",
                        "retained_columns", "checkpoint_bytes", "global_roster",
                        "oracle_rounds"} and
                    all(type(item) is int and item >= 0
                        for item in monitor["counters"].values()),
                    "resource monitor counters")
            registered_limits = monitor["limits"]
            if cap not in registered_limits or limit != float(registered_limits[cap]):
                raise RuntimeError("resource receipt limit is not registered")
            require(monitor.get("phase") == parsed_terminal["phase"],
                    "resource monitor phase binding")
            if cap in monitor["counters"]:
                require(float(monitor["counters"][cap]) == value_at_stop,
                        "resource counter terminal value mismatch")
            elif cap == "wall_seconds":
                require(float(monitor["elapsed_seconds"]) >= value_at_stop,
                        "resource wall terminal value mismatch")
            elif cap == "rss_bytes":
                require(int(monitor["rss_bytes"]) >= int(value_at_stop),
                        "resource rss terminal value mismatch")
            if not checkpoint or not checkpoint.get("path"):
                raise RuntimeError("resource stop lacks resumable checkpoint")
            path = ROOT / "ci" / "out" / str(checkpoint["path"])
            if not path.is_file():
                raise RuntimeError("resource checkpoint file missing")
            raw = path.read_bytes()
            if len(raw) != checkpoint.get("bytes") or digest(raw) != checkpoint.get("sha256"):
                raise RuntimeError("resource checkpoint identity")
            value = json.loads(raw.decode("utf-8"))
            validate_outer_seal(value)
            validate_v3_checkpoint_contract(value)
            if value.get("schema") != SCHEMA or value.get("normalized_semantics_digest") != NORMALIZED_SEMANTICS_DIGEST or \
                    value.get("normalized_semantics_callsites") != list(NORMALIZED_SEMANTICS_CALLSITES):
                raise RuntimeError("resource checkpoint semantic binding")
            if receipt.get("v2_schedule", {}).get("resume_replayed_from_rank_zero"):
                rebuild = value.get("resume_rebuild", {})
                if rebuild.get("rank_zero_replayed") is not True or \
                        rebuild.get("stored_pivots_discarded") is not True or \
                        rebuild.get("stored_reduced_target_discarded") is not True or \
                        rebuild.get("stored_current_dual_discarded") is not True or \
                        type(rebuild.get("stored_oracle_progress_discarded")) is not bool or \
                        type(rebuild.get("safe_progress_preserved")) is not bool or \
                        type(rebuild.get("safe_boundary_preserved")) is not bool or \
                        type(rebuild.get("safe_chunk_replayed_without_suffix")) is not bool or \
                        rebuild.get("monitor_limits_bound") is not True or \
                        rebuild.get("monitor_counters_carried_forward") is not True or \
                        type(rebuild.get("prior_monitor_elapsed_seconds")) not in (int, float) or \
                        type(rebuild.get("safe_chunk_end_recovered")) is not int or \
                        rebuild.get("safe_chunk_end_recovered") < 0 or \
                        (rebuild.get("safe_progress_preserved") and
                         rebuild.get("stored_oracle_progress_discarded")) or \
                        (rebuild.get("safe_chunk_replayed_without_suffix") !=
                         rebuild.get("safe_progress_preserved")) or \
                        (rebuild.get("safe_boundary_preserved") and
                         not rebuild.get("safe_progress_preserved")) or \
                        rebuild.get("stored_state_fields_discarded") != [
                            "pivot_order", "pivot_rows_sha256", "reduced_target",
                            "current_dual", "current_dual_sha256",
                            "target_solution_if_zero", "monitor",
                            "coarse_inverse_index", "resume_rebuild", "v3_epoch"] or \
                        rebuild.get("column_provenance_authenticated") is not True or \
                        rebuild.get("stored_columns_replayed_from_zero") is not True or \
                        rebuild.get("rank_zero_replay_source") != \
                        "authenticated columns/provenance" or \
                        rebuild.get("v3_cache_and_chunk_state_discarded") is not True:
                    raise RuntimeError("resource resume checkpoint retained stale state")
        else:
            reason = terminal[len(UNKNOWN_INPUT) + 1:]
            if not reason or not any(reason.startswith(prefix)
                                     for prefix in AUTHENTICATED_INPUT_REASON_PREFIXES) or \
                    receipt.get("reason") != reason:
                raise RuntimeError("unauthenticated input UNKNOWN reason")
    else:
        raise RuntimeError("unexpected production terminal")
    return "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_CHECKER_PASS terminal=" + terminal


def load_live_checker():
    predecessor_paths = {
        "producer": ROOT / "search/d972_r07_normalized_exact_common_word_colgen_v2.py",
        "checker": ROOT / "crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py",
        "driver": ROOT / "search/d972_r07_normalized_exact_common_word_colgen_gha_driver_v2.g",
        "fixture": ROOT / "search/certs/d972_r07_normalized_exact_common_word_colgen_selftest_v2_20260827.json",
    }
    for label, path in predecessor_paths.items():
        raw = path.read_bytes()
        expected = TASK186_V2[label]
        if len(raw) != expected[0] or digest(raw) != expected[1]:
            raise RuntimeError("authenticated task186 v2 input changed:" + label)
    for rel, expected in (("sol/luna_task_190_r07_exact_colgen_speed_audit.md",
                           TASK190["instruction"]),
                          ("sol/luna_reply_190_r07_exact_colgen_speed_audit.md",
                           TASK190["reply"])):
        raw = (ROOT / rel).read_bytes()
        if len(raw) != expected[0] or digest(raw) != expected[1]:
            raise RuntimeError("authenticated task190 input changed:" + rel)
    proof_paths = {
        "v156": ROOT / "sol/proof_r07_task179_exact_exponent_lattice_v156.md",
        "v157": ROOT / "sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md",
    }
    for label, path in proof_paths.items():
        raw = path.read_bytes()
        expected = PROOF_PINS[label]
        if len(raw) != expected[0] or digest(raw) != expected[1]:
            raise RuntimeError("authenticated proof input changed:" + label)
    data = LIVE_CHECKER.read_bytes()
    if len(data) != LIVE_CHECKER_ID[0] or digest(data) != LIVE_CHECKER_ID[1]:
        raise RuntimeError("authenticated live checker changed")
    spec = importlib.util.spec_from_file_location("d972_live_task179_checker_v2", LIVE_CHECKER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load authenticated live checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for _label, (_rel, _size, _sha) in module.PINS.items():
        raw = (ROOT / _rel).read_bytes()
        if len(raw) != _size or digest(raw) != _sha:
            raise RuntimeError("authenticated task179 arithmetic input changed:" +
                               str(_label))
    return module


def full_independent_production(receipt, receipt_path):
    """Run the complete helper-nonshared v1 replay, then v3-only checks."""
    receipt_path = Path(receipt_path)
    checker = load_live_checker()
    # The helper also exposes v1's raw mod-3 exponent_pair.  Patch its own
    # runtime before main(), independently of the producer patch.
    install_normalized_checker_semantics(checker)
    with tempfile.TemporaryDirectory(prefix="d972-r07-check-v2-") as temp:
        raw_path = Path(temp) / "v1-receipt.json"
        raw = dict(receipt)
        raw["schema"] = checker.SCHEMA
        if raw.get("terminal") == COMMON:
            raw["terminal"] = checker.COMMON
        checkpoint_ref = receipt.get("checkpoint")
        if checkpoint_ref and checkpoint_ref.get("path"):
            v2_checkpoint_path = receipt_path.parent / str(checkpoint_ref["path"])
            if not v2_checkpoint_path.is_file():
                raise RuntimeError("authenticated v2 checkpoint sidecar missing")
            v2_checkpoint_raw = v2_checkpoint_path.read_bytes()
            if len(v2_checkpoint_raw) != checkpoint_ref.get("bytes") or \
                    digest(v2_checkpoint_raw) != checkpoint_ref.get("sha256"):
                raise RuntimeError("authenticated v2 checkpoint sidecar identity")
            v2_checkpoint = json.loads(v2_checkpoint_raw.decode("utf-8"))
            validate_outer_seal(v2_checkpoint)
            validate_v3_checkpoint_contract(v2_checkpoint)
            if v2_checkpoint.get("schema") != SCHEMA or \
                    v2_checkpoint.get("normalized_semantics_digest") != NORMALIZED_SEMANTICS_DIGEST or \
                    v2_checkpoint.get("normalized_semantics_callsites") != list(NORMALIZED_SEMANTICS_CALLSITES):
                raise RuntimeError("authenticated v2 checkpoint semantics")
            # The helper firewall consumes the complete v1 checkpoint object,
            # while the outer receipt keeps the v2 path/bytes/SHA metadata.
            v1_checkpoint = dict(v2_checkpoint)
            v1_checkpoint["schema"] = checker.CHECKPOINT_SCHEMA
            v1_checkpoint.pop("normalized_semantics", None)
            v1_checkpoint.pop("normalized_semantics_digest", None)
            v1_checkpoint.pop("normalized_semantics_callsites", None)
            v1_checkpoint = checker.seal(v1_checkpoint)
            if raw.get("terminal") == checker.COMMON:
                raw["checkpoint"] = v1_checkpoint
            else:
                v1_checkpoint_path = Path(temp) / "v1-checkpoint.json"
                v1_checkpoint_path.write_bytes(checker.canonical(v1_checkpoint) + b"\n")
                raw["checkpoint"] = {"path": v1_checkpoint_path.name,
                                     "bytes": v1_checkpoint_path.stat().st_size,
                                     "sha256": digest(v1_checkpoint_path.read_bytes())}
        raw.pop("self_digest", None)
        raw = checker.seal(raw)
        raw_path.write_text(json.dumps(raw, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8")
        expected_pins = {name: value for name, value in checker.authenticate().items()
                         if name != "producer"}
        helper_runtime = checker.independent_runtime() if (
            raw.get("terminal") == checker.COMMON or raw.get("checkpoint") is not None) else None
        fox_cache = value_cache = boundary_cache = None
        if helper_runtime is not None:
            input_digest = receipt.get("input_sha256", "unbound")
            fox_cache = IndependentFoxTemplateCache(helper_runtime, checker,
                                                    input_digest)
            value_cache = IndependentCoordinateValueCache(helper_runtime,
                                                          input_digest)
            boundary_cache = IndependentBoundaryDescriptorCache(
                helper_runtime, input_digest)
            base_hex = checker.hexagon_words(helper_runtime["obj"]["g760"])
            fixed_base_words = (
                (1, checker.embed_pb3(base_hex[0])),
                (2, checker.embed_pb3(base_hex[1])),
                (3, checker.pentagon_word(helper_runtime["obj"]["g760"])),)
            for block, base_word in fixed_base_words:
                fox_cache.base_gradient(block, base_word)
            declared_descriptors = receipt.get("v3_cache_stats", {}).get(
                "boundary_descriptors")
            if declared_descriptors != boundary_cache.public_contract():
                raise RuntimeError("checker boundary descriptor contract mismatch")
        if raw.get("terminal") == checker.COMMON:
            validate_roster_exponent_lattice(helper_runtime)
            selected_rwords = {}
            for ordinal in (3, 9, 12):
                matches = [record["word"] for record in helper_runtime["obj"]["roster"]
                           if record.get("layer") == "q0_relator" and
                           record.get("ordinal") == ordinal]
                if len(matches) != 1:
                    raise RuntimeError("independent registered r ordinal")
                selected_rwords[str(ordinal)] = list(matches[0])
            receipt_rwords = receipt.get("exactification", {}).get("r_words", {})
            if receipt_rwords != selected_rwords:
                raise RuntimeError("receipt r words are not independently selected")
            cstar = receipt.get("correction_word") or []
            reconstructed_cstar = ()
            for column, coefficient in receipt.get("solution_coefficients", []):
                if type(column) is not int or type(coefficient) is not int or \
                        coefficient not in (1, 2) or not (1 <= column <= len(receipt.get("columns", []))):
                    raise RuntimeError("independent coefficient is not F3 nonzero")
                record = receipt.get("columns", [])[column - 1]
                if record.get("family") == "boundary":
                    raise RuntimeError("boundary factor in reconstructed c_star")
                source = record.get("provenance", {}).get("conjugate_word", [])
                reconstructed_cstar = mul(
                    reconstructed_cstar,
                    source if coefficient == 1 else inv(source))
            if list(reconstructed_cstar) != cstar:
                raise RuntimeError("independent c_star coefficient replay")
            closed = exactify(cstar, selected_rwords["3"], selected_rwords["9"],
                              selected_rwords["12"])
            literals = receipt.get("exactification", {}).get("literal", {})
            expected_literals = {"c_star": list(cstar), "v0": list(closed[1]),
                                 "u0": list(closed[2]), "h": list(closed[3]),
                                 "c_exact": list(closed[0])}
            if literals != expected_literals:
                raise RuntimeError("receipt exactification literals mismatch")
            cstar_exp = exp(cstar)
            if any(value % 54 for value in cstar_exp):
                raise RuntimeError("independent c_star 54-divisibility")
            expected_exponents = {
                "c_star": list(cstar_exp), "v0": list(exp(closed[1])),
                "u0": list(exp(closed[2])), "h": list(exp(closed[3])),
                "c_exact": list(exp(closed[0]))}
            exactification = receipt.get("exactification", {})
            if exactification.get("A") != cstar_exp[0] // 54 or \
                    exactification.get("B") != cstar_exp[1] // 54 or \
                    exactification.get("exponents") != expected_exponents or \
                    exactification.get("source") != "authenticated task179 roster ordinals":
                raise RuntimeError("receipt exactification exponent/provenance mismatch")
        if raw.get("terminal") == checker.COMMON:
            checker.validate_common(helper_runtime, raw, expected_pins)
        else:
            checker.validate_unknown(helper_runtime, raw, expected_pins, raw_path)
        if raw.get("terminal") == checker.COMMON:
            # Exercise the checker-owned caches against every retained literal;
            # no producer cache or receipt hash is used as a substitute.
            provenance_controls_checked = False
            for record in receipt.get("columns", []):
                provenance = record.get("provenance", {})
                if provenance.get("family") == "boundary":
                    row = boundary_cache.row(
                        provenance["block"], provenance["base_relator_index"],
                        provenance["translation_hex"])
                    if checker.public_sparse(row) != record.get("sparse_row"):
                        raise RuntimeError("checker cached boundary row mismatch")
                elif provenance.get("family") == "correction":
                    active = record.get("active_dual")
                    if active is not None:
                        dual = checker.parse_sparse(active)
                        formula = fox_cache.formula(
                            provenance["relator_word"], dual)
                        if formula != provenance.get("weighted_formula"):
                            raise RuntimeError("checker cached formula mismatch")
                    source = provenance.get("delta_word", [])
                    section = provenance.get("section_provenance", {})
                    if all(field in section for field in
                           ("q0_state_id", "gamma_state_id",
                            "q0_source_word", "gamma_source_word",
                            "q0_parent_path")):
                        require(tuple(section.get("source_word", source)) ==
                                tuple(source),
                                "checker cached candidate source binding")
                        base_source = reduce_word(tuple(section[
                            "gamma_source_word"]) + tuple(section[
                            "q0_source_word"]))
                        cached_candidate = value_cache.candidate(
                            int(section["q0_state_id"]) - 1,
                            int(section["gamma_state_id"]) - 1,
                            section["gamma_source_word"],
                            section["q0_source_word"], base_source,
                            section["q0_parent_path"])
                        cached_coordinates = cached_candidate["coordinate_blobs"]
                        if not provenance_controls_checked:
                            for bad_path, bad_gamma in (
                                    (None, section["gamma_source_word"]),
                                    (section["q0_parent_path"],
                                     list(section["gamma_source_word"]) + [1])):
                                try:
                                    value_cache.candidate(
                                        int(section["q0_state_id"]) - 1,
                                        int(section["gamma_state_id"]) - 1,
                                        bad_gamma,
                                        section["q0_source_word"], base_source,
                                        bad_path)
                                except RuntimeError:
                                    pass
                                else:
                                    raise RuntimeError(
                                        "candidate provenance mutation accepted")
                            provenance_controls_checked = True
                        section_blobs = section.get("section_blob_hex")
                        selector_path = "selection" in section
                        if selector_path:
                            require(isinstance(section_blobs, list) and
                                    section_blobs == [str(item) for item in
                                                      cached_candidate[
                                                          "section_coordinate_blobs"]],
                                    "checker candidate literal section provenance")
                        else:
                            # The pinned v1 checker dispatches on this field;
                            # global/kernel records must not be mistaken for
                            # selector records merely because they carry
                            # state/path provenance.
                            require(section_blobs is None and
                                    "gamma_coordinate_blob_hex" not in section,
                                    "checker legacy selector dispatch collision")
                        gamma_blobs = [str(item) for item in cached_candidate[
                            "gamma_coordinate_blobs"]]
                        declared_gamma = section.get("gamma_coordinate_blobs_hex")
                        require(isinstance(declared_gamma, list) and
                                declared_gamma == gamma_blobs,
                                "checker candidate Gamma row provenance")
                        if selector_path and "coordinate" in section:
                            coordinate = int(section["coordinate"])
                            require(section.get("gamma_coordinate_blob_hex") ==
                                    gamma_blobs[coordinate],
                                    "checker candidate Gamma coordinate provenance")
                        replayed_coordinates = list(cached_coordinates)
                        if "global_cursor" in section:
                            cursor = int(section["global_cursor"])
                            require(0 <= cursor < DELTA_ORDER and
                                    divmod(cursor, 243) == (
                                        int(section["q0_state_id"]) - 1,
                                        int(section["gamma_state_id"]) - 1),
                                    "checker global candidate state binding")
                        if "kernel_word" in section:
                            kernel_word = list(section["kernel_word"])
                            kernel_blobs = section.get("kernel_coordinate_blobs")
                            require(isinstance(kernel_blobs, list) and
                                    independent_coordinates(helper_runtime,
                                                            kernel_word) == kernel_blobs and
                                    tuple(reduce_word(tuple(kernel_word) +
                                                       tuple(base_source))) ==
                                    tuple(source),
                                    "checker kernel candidate source replay")
                            require(multiply_coordinate_blob_rows(
                                helper_runtime, kernel_blobs,
                                [item.hex() if isinstance(item, bytes) else str(item)
                                 for item in
                                 cached_candidate["coordinate_blobs"]]) ==
                                list(provenance.get("delta_coordinate_blobs_hex", [])),
                                "checker kernel coordinate multiplication")
                            replayed_coordinates = multiply_coordinate_blob_rows(
                                helper_runtime, kernel_blobs,
                                [item.hex() if isinstance(item, bytes) else str(item)
                                 for item in cached_candidate["coordinate_blobs"]])
                    else:
                        raise RuntimeError("checker cached candidate provenance incomplete")
                    if list(replayed_coordinates) != provenance.get(
                            "delta_coordinate_blobs_hex", []):
                        raise RuntimeError("checker cached coordinate value mismatch")
        if helper_runtime is not None:
            require_cache_descriptors = (len(boundary_cache.descriptors) ==
                2 * sum(len(row) for row in helper_runtime["obj"]["pb3_rows"]) +
                sum(len(row) for row in helper_runtime["obj"]["pb4_rows"]))
            if not require_cache_descriptors:
                raise RuntimeError("checker complete PB3/PB4 descriptor roster")
        if receipt.get("terminal") == COMMON:
            # Re-run the helper's independently coded direct-correction
            # primitive on c_exact; receipt booleans are not evidence.
            # Replay the independently reconstructed literals, not the
            # receipt's copies (the equality gate above is separate).
            exact_word = list(closed[0])
            star_word = list(cstar)
            star_row, star_replay = checker.direct_correction(helper_runtime, [], star_word)
            direct_row, direct_replay = checker.direct_correction(helper_runtime, [], exact_word)
            expected_row = checker.parse_sparse(receipt.get("exact_direct_replay", {}).get("row", []))
            if checker.public_sparse(direct_row) != checker.public_sparse(expected_row) or \
                    checker.public_sparse(star_row) != checker.public_sparse(direct_row):
                raise RuntimeError("helper direct c_exact row mismatch")
            if direct_replay.get("corrected_word") != receipt.get("exact_direct_replay", {}).get(
                    "replay", {}).get("corrected_word"):
                raise RuntimeError("helper direct c_exact word mismatch")
            for label, literal in receipt.get("exactification", {}).get("r_words", {}).items():
                if helper_runtime["obj"]["joint"].eval(literal) != helper_runtime["obj"]["joint"].identity:
                    raise RuntimeError("helper registered r-word kernel replay:" + label)
            for label in ("u0", "v0"):
                literal = receipt.get("exactification", {}).get("literal", {}).get(label, [])
                if helper_runtime["obj"]["joint"].eval(literal) != helper_runtime["obj"]["joint"].identity:
                    raise RuntimeError("helper exactification basis kernel replay:" + label)
            raw_rows = []
            for record in receipt.get("columns", []):
                raw_rows.append(checker.parse_sparse(record.get("sparse_row", [])))
            for witness in receipt.get("nu_kernel_ancestry", []):
                source = witness.get("correction_word_replay", [])
                replay_row, replay_info = checker.direct_correction(helper_runtime, [], source)
                boundary_sum = {}
                for column, coefficient in witness.get("boundary_coefficients", []):
                    for key, value in raw_rows[column - 1].items():
                        if key.startswith(b"E"):
                            continue
                        value0 = (boundary_sum.get(key, 0) + coefficient * value) % 3
                        if value0:
                            boundary_sum[key] = value0
                        elif key in boundary_sum:
                            boundary_sum.pop(key)
                for key, value in replay_row.items():
                    if key.startswith(b"E"):
                        continue
                    value0 = (boundary_sum.get(key, 0) + value) % 3
                    if value0:
                        boundary_sum[key] = value0
                    elif key in boundary_sum:
                        boundary_sum.pop(key)
                if boundary_sum or replay_info.get("corrected_word") != checker.reduce_word(
                        list(helper_runtime["obj"]["g760"]) + source):
                    raise RuntimeError("helper ancestry correction/boundary replay")
    return check_production(receipt, checker)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    receipt_path = Path(args.receipt)
    if not receipt_path.is_absolute():
        receipt_path = ROOT / receipt_path
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    marker = (check_toy(receipt) if args.selftest else
              full_independent_production(receipt, receipt_path))
    print(marker)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
