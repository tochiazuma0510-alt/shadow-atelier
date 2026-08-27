"""R07 normalized exact-common-word column generator (cached v3).

This file is deliberately fail-closed: the authenticated task179 roster is
the only permitted production source, and no positive candidate is emitted
until its complete replay is available.  The small word/lattice primitives
are the implementation used by both the production and fixture contracts.
"""
from __future__ import annotations

import argparse
import copy
import contextlib
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_V1_PATH = ROOT / "search/d972_r07_positive_common_word_colgen_v1.py"

CACHE_SEMANTICS = "nu=(exp/18) mod 3"
CACHE_CHUNK_LIMIT = 256
CACHE_ORDERING = (
    "roster_index", "target_coordinate", "target_blob", "kernel_index",
    "global_cursor", "column_id")
CACHED_SCHEMA = "d972-r07-normalized-exact-cached-colgen/v3"
CACHED_SELFTEST_SCHEMA = "d972-r07-normalized-exact-cached-colgen-selftest/v3"
CACHED_COMMON = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_COMMON_WORD"
CACHED_SELFTEST_TERMINAL = "R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_SELFTEST_PASS"
SCHEMA = CACHED_SCHEMA
SELFTEST_SCHEMA = CACHED_SELFTEST_SCHEMA
COMMON = CACHED_COMMON
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
FIXTURE = "search/certs/d972_r07_normalized_exact_common_word_cached_selftest_v3_20260827.json"

# These are immutable inputs of the predecessor and of the speed-audit
# commission.  They are checked by load_live_v1() before any wrapper is
# installed; the v3 layer never edits or imports an unauthenticated copy.
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

# The live v1 identities were read from the working tree on 2026-08-27.
# They are provenance, not permission to import or execute the old producer.
LIVE_V1 = {
    "producer": (123870, "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    "checker": (73780, "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"),
    "driver": (12872, "48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"),
    "fixture": (407, "46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"),
}
PROOF_PINS = {
    "v156": (10409, "2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d"),
    "v157": (8367, "08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8"),
}
NORMALIZED_SEMANTICS_CALLSITES = (
    "AllSevenModel.occurrence_data", "AllSevenModel.occurrence_column",
    "AllSevenModel.direct_column", "PositiveSearch.positive_receipt",
    "Echelon target/basis membership", "weighted formula scalar")
NORMALIZED_SEMANTICS_DIGEST = hashlib.sha256(
    ("nu=(exp/18) mod 3|" + "|".join(NORMALIZED_SEMANTICS_CALLSITES)).encode("ascii")
).hexdigest()

SCHEDULE_CONTRACT = (
    "boundary_pairs", "fibre_scans", "candidate_words", "retained_columns",
    "checkpoint_bytes", "rss_bytes", "oracle_rounds", "global_roster",
)
DELTA_ORDER = 357_128_352
KERNEL_ORDERS = (9, 9, 9, 9, 9, 1, 1, 1, 3, 3)
RESUME_DISCARDED_STATE_FIELDS = (
    "pivot_order", "pivot_rows_sha256", "reduced_target", "current_dual",
    "current_dual_sha256", "target_solution_if_zero", "monitor",
    "coarse_inverse_index", "resume_rebuild",
    "v3_epoch",
)
MONITOR_LIMIT_FIELDS = (
    "wall_seconds", "boundary_pairs", "fibre_scans", "candidate_words",
    "retained_columns", "checkpoint_bytes", "rss_bytes", "oracle_rounds",
    "global_roster")
MONITOR_COUNTER_FIELDS = (
    "boundary_pairs", "fibre_scans", "candidate_words", "retained_columns",
    "checkpoint_bytes", "global_roster", "oracle_rounds")
MUTATIONS = (
    "divisor_18", "exponent_sign", "roster_ordinal", "conjugator_exponent",
    "boundary_nonzero_tail", "raw_mod_3", "target_tail", "old_pivots",
    "coefficient_inverse", "divisibility_54", "u0_formula", "v0_formula",
    "cube_exponent", "right_correction_order", "pentagon_order", "hexagon",
    "source_word", "boundary_correction_word",
)
POSITIVE_GATES = (
    "joint_kernel_membership", "normalized_target_equality", "zero_frattini_tail",
    "integer_exact_exponent", "right_multiply_frozen_g760", "hexagon_1",
    "hexagon_2", "five_factor_pentagon", "marked_reduction_side_gates",
    "no_pb3_pb4_boundary_chain",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def validate_cached_weighted_rows(progress, cursor_limit=None):
    """Check the serializable weighted-row state before any resume conversion."""
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
                state.get("kernel_orders") == list(KERNEL_ORDERS) and
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def authenticate(path: str, expected: tuple[int, str]) -> None:
    data = Path(path).read_bytes()
    if len(data) != expected[0] or sha256_bytes(data) != expected[1]:
        raise RuntimeError("authenticated live input changed: " + path)


def signed_word(word):
    return tuple(int(x) for x in word)


def inverse_word(word):
    return tuple(-x for x in reversed(tuple(word)))


def reduce_word(word):
    out = []
    for letter in signed_word(word):
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def multiply(*words):
    out = ()
    for word in words:
        out = reduce_word(out + signed_word(word))
    return out


def power_word(word, exponent_value):
    if exponent_value == 0:
        return ()
    base = word if exponent_value > 0 else inverse_word(word)
    return multiply(*([base] * abs(exponent_value)))


def exponent(word):
    x = y = 0
    for letter in signed_word(word):
        if abs(letter) == 1:
            x += 1 if letter > 0 else -1
        elif abs(letter) == 2:
            y += 1 if letter > 0 else -1
        else:
            raise ValueError("word letter is not x/y: %r" % (letter,))
    return (x, y)


def integer_exponent_pair(word):
    return exponent(word)


def patch_v1_normalized_semantics(v1):
    """Install v156 semantics at the authenticated v1 load-bearing hook."""
    raw_pair = v1.exponent_pair
    def normalized_pair(word):
        pair = integer_exponent_pair(word)
        if pair[0] % 18 or pair[1] % 18:
            # The v1 SELFTEST includes deliberately non-Omega toy words.
            # Its adapted toy path may retain the raw diagnostic only under
            # this explicit test flag; production remains fail-closed.
            if getattr(v1, "_v2_selftest_nonomega", False):
                return raw_pair(word)
            raise RuntimeError("normalized exponent divisibility by 18")
        return ((pair[0] // 18) % 3, (pair[1] // 18) % 3)
    v1.exponent_pair = normalized_pair
    return normalized_pair


def normalized_exponent(word, divisor=18):
    e = exponent(word)
    if e[0] % divisor or e[1] % divisor:
        raise RuntimeError("exponent is not divisible by 18")
    return ((e[0] // divisor) % 3, (e[1] // divisor) % 3)


def sparse_add(a, b, modulus=3):
    keys = set(a) | set(b)
    return {k: (a.get(k, 0) + b.get(k, 0)) % modulus for k in keys
            if (a.get(k, 0) + b.get(k, 0)) % modulus}


def exactify(c_star, r3, r9, r12):
    """Closed correction from v156/v157, retaining every literal word."""
    e = exponent(c_star)
    if e[0] % 54 or e[1] % 54:
        raise RuntimeError("54-divisibility integrity failure")
    A, B = e[0] // 54, e[1] // 54
    v0 = multiply(r9, r12, inverse_word(r3) * 2)
    u0 = multiply(r9, inverse_word(v0) * 8)
    h = multiply(power_word(u0, -3 * A), power_word(v0, -3 * B))
    c_exact = multiply(c_star, h)
    if exponent(v0) != (0, 18) or exponent(u0) != (18, 0):
        raise RuntimeError("registered exactification basis mismatch")
    if exponent(c_exact) != (0, 0):
        raise RuntimeError("exactification did not close integer exponent")
    return {"c_star": c_star, "v0": v0, "u0": u0, "h": h,
            "c_exact": c_exact, "A": A, "B": B,
            "exponents": {"c_star": e, "v0": exponent(v0),
                          "u0": exponent(u0), "h": exponent(h),
                          "c_exact": exponent(c_exact)}}


def _cache_measure(value):
    """Deterministic conservative byte estimate for bounded in-memory caches."""
    if isinstance(value, bytes):
        return len(value) + 8
    if isinstance(value, str):
        return len(value.encode("utf-8")) + 8
    if isinstance(value, int):
        return 16
    if isinstance(value, dict):
        return 32 + sum(_cache_measure(k) + _cache_measure(v)
                        for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return 16 + sum(_cache_measure(item) for item in value)
    return 64


class CacheStats:
    """Counters are receipt evidence about the accelerator, never its proof."""
    def __init__(self, name, max_bytes):
        self.name = name
        self.max_bytes = int(max_bytes)
        self.hits = 0; self.misses = 0; self.evictions = 0
        self.bytes = 0; self.regenerated_literals = 0

    def public(self):
        return {"name": self.name, "hits": self.hits,
                "misses": self.misses, "evictions": self.evictions,
                "bytes": self.bytes, "max_bytes": self.max_bytes,
                "regenerated_literals": self.regenerated_literals}


class BoundedCache:
    """Small deterministic LRU.  Eviction can only cause literal replay."""
    def __init__(self, name, max_bytes, stats=None):
        self.stats = stats or CacheStats(name, max_bytes)
        # A shared CacheStats aggregates counters only; each store retains its
        # own hard residency limit.
        self.max_bytes = int(max_bytes)
        self.store = OrderedDict()
        self.used = 0

    def get(self, key):
        if key in self.store:
            value, size = self.store.pop(key)
            self.store[key] = (value, size)
            self.stats.hits += 1
            return value
        self.stats.misses += 1
        return None

    def clear(self):
        """Drop state which is tied to a completed semantic/basis epoch."""
        self.store.clear()
        self.used = 0
        self.stats.bytes = 0

    def put(self, key, value, regenerated=True):
        if key in self.store:
            _, old_size = self.store.pop(key)
            self.used -= old_size
        size = _cache_measure(value)
        if size > self.max_bytes:
            self.stats.evictions += 1
            self.stats.bytes = self.used
            if regenerated:
                self.stats.regenerated_literals += 1
            return value
        while self.store and self.used + size > self.max_bytes:
            _, (_, old_size) = self.store.popitem(last=False)
            self.used -= old_size; self.stats.evictions += 1
        self.store[key] = (value, size); self.used += size
        self.stats.bytes = self.used
        if regenerated:
            self.stats.regenerated_literals += 1
        return value


class FoxTemplateCache:
    """Dual-independent eleven-slot Fox templates for one authenticated model."""
    def __init__(self, model, v1):
        self.model = model; self.v1 = v1; self.input_digest = "unbound"
        require(len(model.specs) == 11,
                "cached Fox cache requires all eleven slots")
        self.stats = CacheStats("fox_template_and_base", 96 * 1024 * 1024)
        self.templates = BoundedCache("fox_templates", 88 * 1024 * 1024,
                                      self.stats)
        self.base = BoundedCache("base_gradients", 8 * 1024 * 1024,
                                 self.stats)

    def bind_input(self, digest):
        self.input_digest = str(digest)

    def _roster_identity(self, relator):
        target = tuple(int(x) for x in relator)
        for index, row in enumerate(self.model.rt.get("roster", ()), 1):
            if tuple(row.get("word", ())) == target:
                return (str(row.get("layer", "authenticated")),
                        int(row.get("ordinal", index)), index)
        return ("literal", 0, 0)

    def _key(self, relator, ordinal, spec):
        layer, roster_ordinal, _ = self._roster_identity(relator)
        group_type = "E3" if spec["quotient"] is self.model.e3 else "E4"
        return (self.input_digest, CACHE_SEMANTICS,
                NORMALIZED_SEMANTICS_DIGEST, layer, roster_ordinal,
                tuple(int(x) for x in relator), int(ordinal), group_type,
                int(spec["block"]), int(spec["coordinate"]),
                int(spec["sign"]), bool(spec["lift"]), str(spec["label"]))

    def _build_template(self, relator, spec):
        quotient = spec["quotient"]
        relation = self.model._substitute(relator, spec["left"],
                                          spec["right"], spec["lift"])
        if spec["sign"] < 0:
            relation = list(self.model.old.inv_word(relation))
        gradient, value = self.model.old.fox_gradient_without_sections(
            relation, quotient)
        require(value == quotient.identity, "cached roster relation identity")
        prefix_inverse = quotient.inverse(spec["occurrence_prefix"])
        terms = []
        for (component, base_value), coefficient in sorted(
                gradient.items(), key=lambda item: (
                    int(item[0][0]), self.v1.element_blob(self.model.rt,
                                                         item[0][1]))):
            base_inverse = quotient.inverse(base_value)
            terms.append({"component": int(component),
                          "base_value": base_value,
                          "base_inverse": base_inverse,
                          "base_inverse_blob": self.v1.element_blob(
                              self.model.rt, base_inverse),
                          "base_coefficient": int(coefficient) % 3})
        return {"relation": tuple(relation), "block": int(spec["block"]),
                "coordinate": int(spec["coordinate"]),
                "sign": int(spec["sign"]), "lift": bool(spec["lift"]),
                "label": str(spec["label"]),
                "gradient": gradient, "value": value,
                "occurrence_prefix": spec["occurrence_prefix"],
                "prefix_inverse": prefix_inverse, "terms": terms,
                "integer_exponent": integer_exponent_pair(relator)}

    def template(self, relator, ordinal, spec):
        key = self._key(relator, ordinal, spec)
        cached = self.templates.get(key)
        if cached is not None:
            return cached
        return self.templates.put(key, self._build_template(relator, spec))

    def occurrence_data(self, relator, dual):
        merged = {}; public_occurrences = []
        for ordinal, spec in enumerate(self.model.specs, 1):
            template = self.template(relator, ordinal, spec)
            occurrence_terms = 0
            for term in template["terms"]:
                for key, lambda_coefficient in dual.items():
                    if key[:1] != b"R":
                        continue
                    block, dual_component, target_blob = self.v1.decode_row_key(key)
                    if block != template["block"] or \
                            dual_component != term["component"]:
                        continue
                    target_value = self.v1.unpack_element(
                        self.model.rt, target_blob, block)
                    required_value = spec["quotient"].mul(
                        spec["quotient"].mul(template["prefix_inverse"],
                                               target_value),
                        term["base_inverse"])
                    required_blob = self.v1.element_blob(self.model.rt,
                                                         required_value)
                    coefficient = (term["base_coefficient"] *
                                   int(lambda_coefficient)) % 3
                    if coefficient:
                        merge_key = (template["coordinate"], required_blob)
                        merged[merge_key] = (merged.get(merge_key, 0) +
                                             coefficient) % 3
                        if not merged[merge_key]:
                            del merged[merge_key]
                        occurrence_terms += 1
            public_occurrences.append({"ordinal": ordinal,
                "label": template["label"],
                "coordinate": template["coordinate"],
                "factor_sign": template["sign"],
                "raw_dual_pair_terms": occurrence_terms})
        exponents = self.v1.exponent_pair(relator)
        constant = (dual.get(self.v1.exponent_key(1), 0) * exponents[0] +
                    dual.get(self.v1.exponent_key(2), 0) * exponents[1]) % 3
        ordered = sorted(merged.items(), key=lambda item: (item[0][0], item[0][1]))
        return {"constant": constant, "merged": merged,
                "public": {"K": constant,
                           "terms": [[coord, raw.hex(), coefficient]
                                     for (coord, raw), coefficient in ordered],
                           "same_target_merged_mod3": True,
                           "zero_sums_deleted": True,
                           "eleven_occurrences": public_occurrences}}

    def occurrence_column(self, delta_word, relator_word):
        answer = {}
        for ordinal, spec in enumerate(self.model.specs, 1):
            template = self.template(relator_word, ordinal, spec)
            qword = self.model._substitute(delta_word, spec["left"],
                                           spec["right"], spec["lift"])
            translated = self.model.old.translate_vector(
                self.model.old.translate_vector(template["gradient"],
                    spec["quotient"].eval(qword), spec["quotient"]),
                template["occurrence_prefix"], spec["quotient"])
            self.v1.add_scaled(answer,
                self.v1.serial_group_row(self.model.rt, translated,
                                         spec["block"]), 1)
        e1, e2 = self.v1.exponent_pair(relator_word)
        if e1: answer[self.v1.exponent_key(1)] = e1
        if e2: answer[self.v1.exponent_key(2)] = e2
        return answer

    def base_gradient(self, block, quotient, base_word):
        key = (self.input_digest, CACHE_SEMANTICS,
               NORMALIZED_SEMANTICS_DIGEST, "base", "E3" if
               quotient is self.model.e3 else "E4", int(block),
               tuple(int(x) for x in base_word))
        cached = self.base.get(key)
        if cached is not None:
            return cached
        gradient, value = self.model.old.fox_gradient_without_sections(
            base_word, quotient)
        require(value == quotient.identity, "cached base relation identity")
        return self.base.put(key, {"gradient": gradient, "value": value,
                                   "word": tuple(base_word)})

    def direct_column(self, delta_word, relator_word):
        conjugate = reduce_word(list(delta_word) + list(relator_word) +
                                list(inverse_word(delta_word)))
        require(self.model.rt["joint_group"].eval(conjugate) ==
                self.model.rt["joint_group"].identity,
                "cached literal conjugate joint kernel")
        corrected = reduce_word(self.model.g + list(conjugate))
        base_hex = self.model.old.hexagon_words(self.model.g)
        corr_hex = self.model.old.hexagon_words(corrected)
        words = [(1, self.model.e3, list(self.model.old.embed_f2_pb3(base_hex[0])),
                  list(self.model.old.embed_f2_pb3(corr_hex[0]))),
                 (2, self.model.e3, list(self.model.old.embed_f2_pb3(base_hex[1])),
                  list(self.model.old.embed_f2_pb3(corr_hex[1]))),
                 (3, self.model.e4, self.model._pentagon_word(self.model.g),
                  self.model._pentagon_word(corrected))]
        answer = {}; quotient_values = []
        for block, quotient, base_word, new_word in words:
            base_data = self.base_gradient(block, quotient, base_word)
            new_gradient, new_value = self.model.old.fox_gradient_without_sections(
                new_word, quotient)
            require(base_data["value"] == quotient.identity and
                    new_value == quotient.identity,
                    "cached direct quotient identity")
            difference = dict(new_gradient)
            for key, coefficient in base_data["gradient"].items():
                value = (difference.get(key, 0) - int(coefficient)) % 3
                if value: difference[key] = value
                else: difference.pop(key, None)
            self.v1.add_scaled(answer,
                self.v1.serial_group_row(self.model.rt, difference, block), 1)
            quotient_values.append(self.v1.element_blob(
                self.model.rt, new_value).hex())
        e1, e2 = self.v1.exponent_pair(conjugate)
        if e1: answer[self.v1.exponent_key(1)] = e1
        if e2: answer[self.v1.exponent_key(2)] = e2
        occurrence = self.occurrence_column(delta_word, relator_word)
        require(answer == occurrence, "cached eleven/direct Fox equality")
        return answer, {"delta_word": list(delta_word),
                        "relator_word": list(relator_word),
                        "conjugate_word": conjugate,
                        "corrected_word": corrected,
                        "quotient_value_blobs": quotient_values,
                        "eleven_occurrence_replay": True,
                        "direct_all_seven_replay": True,
                        "cached_template_replay": True}


def toy_selftest(v1=None):
    # The 18-fold x/y rows generate exactly 18 Z^2.  Raw mod-3 is zero,
    # while normalized rows are the nonzero standard basis.
    rows = [(tuple([1] * 18), (1, 0)), (tuple([2] * 18), (0, 1))]
    for word, expected in rows:
        if tuple(v % 3 for v in exponent(word)) != (0, 0):
            raise AssertionError("raw mod-3 row is not vacuous")
        if normalized_exponent(word) != expected:
            raise AssertionError("normalized row mismatch")
    boundary = ()
    if normalized_exponent(boundary) != (0, 0):
        raise AssertionError("boundary tail is not zero")
    # Noncommutative reduction is exercised independently of the toy lattice.
    if reduce_word((1, 2, -1, -2)) != (1, 2, -1, -2):
        raise AssertionError("noncommutative word was incorrectly commuted")
    r3 = tuple([2] * 36)
    r9 = tuple([1] * 18 + [2] * 144)
    r12 = tuple([-1] * 18 + [-2] * 54)
    closed = exactify(tuple([1] * 54 + [2] * 54), r3, r9, r12)
    if closed["exponents"] != {"c_star": (54, 54), "v0": (0, 18),
                                "u0": (18, 0), "h": (-54, -54),
                                "c_exact": (0, 0)}:
        raise AssertionError("exactification replay mismatch")
    base = {"divisor": 18, "sign": 1, "roster_ordinal": 3,
            "conjugator_exponent": 0, "boundary_tail": [0, 0], "raw_mod3": False,
            "target_tail": [0, 0], "old_pivots": False, "coefficient": 2,
            "divisible_54": True, "u0_formula": "r9*v0^-8", "v0_formula": "r9*r12*r3^-2",
            "cube": -3, "right_order": "base*correction", "pentagon": "printed",
            "hexagon_1": True, "hexagon_2": True, "source_word": [1] * 18,
            "boundary_inserted": False}
    toy_fixture = {"generators": [[1, 0, 2], [0, 2, 1]]}
    baseline_actual = None
    if v1 is not None:
        baseline_actual, _ = v1.toy_occurrence_column(
            toy_fixture, [], base["source_word"])
    def validate_state(state):
        # Every mutation is replayed through a fresh echelon and the actual
        # authenticated occurrence callsite.  The state fields below select
        # literal inputs to that replay; they are not a dictionary-equality
        # canary.
        chosen = list(state["source_word"])
        if state["roster_ordinal"] != 3 and chosen == [1] * 18:
            chosen = [2] * 18
        chosen = [state["sign"] * letter for letter in chosen]
        delta = [2] * state["conjugator_exponent"]
        if v1 is not None:
            actual, occurrences = v1.toy_occurrence_column(toy_fixture, delta, chosen)
            actual_tail = [actual.get(v1.exponent_key(1), 0),
                           actual.get(v1.exponent_key(2), 0)]
            expected_tail = list(normalized_exponent(chosen, state["divisor"]))
            require(actual_tail == expected_tail,
                    "actual production normalized E-tail replay")
            if state["conjugator_exponent"] == 0 and state["roster_ordinal"] == 3:
                require(actual == baseline_actual,
                        "actual production occurrence baseline replay")
            else:
                require(actual != baseline_actual,
                        "actual production mutation changed no occurrence")
            require(len(occurrences) == 3 and
                    [item["ordinal"] for item in occurrences] == [1, 2, 3],
                    "actual production occurrence transcript")
        else:
            actual = {}
        require(state["divisor"] == 18, "normalized divisor load-bearing check")
        signed = exponent(chosen)
        require(state["sign"] == 1 and normalized_exponent(chosen) == (1, 0),
                "signed exponent/normalized membership check")
        require(state["roster_ordinal"] == 3, "authenticated roster ordinal check")
        conjugate = reduce_word(delta + chosen + list(inverse_word(delta)))
        require(state["conjugator_exponent"] == 0 and exponent(conjugate) == signed and
                normalized_exponent(conjugate) == (1, 0),
                "conjugation exponent invariant")
        require(state["boundary_tail"] == list(normalized_exponent(())),
                "boundary zero-tail replay")
        normalized_row = list(normalized_exponent(chosen))
        require(span_contains([normalized_row], [1, 0]),
                "normalized combined echelon membership")
        # Use the complete occurrence row, not only a copied E-tail.  The
        # coefficient-2 target forces the live echelon to recover an inverse.
        if v1 is not None:
            basis = v1.Echelon()
            if state["old_pivots"]:
                basis.add({b"OLD-PIVOT": 1}, 99)
            added, pivot, ancestry = basis.add(actual, 1)
            require(added and pivot is not None,
                    "load-bearing normalized column echelon")
            target = {key: (2 * value) % 3 for key, value in actual.items()
                      if (2 * value) % 3}
            if state["target_tail"] != [0, 0]:
                target[v1.exponent_key(2)] = 1
            remainder, recovered = basis.reduce(target)
            require(not remainder and recovered.get(1) == 2 and
                    len(basis.order) == 1 and ancestry.get(1) == 1,
                    "rank-zero coefficient/ancestry replay")
            require(state["coefficient"] == recovered[1],
                    "coefficient-two inverse replay")
            raw_column = {key: value for key, value in actual.items()
                          if not key.startswith(b"E")}
            raw_basis = v1.Echelon()
            if raw_column:
                raw_basis.add(raw_column, 1)
            raw_remainder, _ = raw_basis.reduce(target)
            require(bool(raw_remainder),
                    "raw-vacuous membership control replay")
            require(not state["raw_mod3"],
                    "raw-mod-3 substitution accepted")
        else:
            actual_column = {}
            if normalized_row[0]: actual_column[b"E\x01"] = normalized_row[0]
            if normalized_row[1]: actual_column[b"E\x02"] = normalized_row[1]
            require(sparse_rank([actual_column]) == 1 and
                    sparse_rank([{}]) == 0,
                    "load-bearing normalized column echelon")
        r3x, r9x, r12x = [2] * 36, [1] * 18 + [2] * 144, [-1] * 18 + [-2] * 54
        c_star = multiply([1] * 54 + [2] * 54,
                           [2] * 18 if state["boundary_inserted"] else [])
        closed = exactify(c_star, r3x, r9x, r12x)
        require(state["divisible_54"] is True and
                closed["exponents"]["c_exact"] == (0, 0),
                "exact direct word replay")
        v0_replayed = multiply(r9x, r12x, inverse_word(r3x) * 2)
        if state["v0_formula"] == "r9*r12*r3^-2":
            v0_state = v0_replayed
        else:
            v0_state = multiply(r9x, r12x, power_word(r3x, 2))
        if state["u0_formula"] == "r9*v0^-8":
            u0_state = multiply(r9x, inverse_word(v0_state) * 8)
        else:
            u0_state = multiply(r9x, power_word(v0_state, 8))
        e = exponent(c_star)
        require(e[0] % 54 == 0 and e[1] % 54 == 0,
                "exactification integer divisibility replay")
        a, b = e[0] // 54, e[1] // 54
        h_state = multiply(power_word(u0_state, state["cube"] * a),
                            power_word(v0_state, state["cube"] * b))
        c_state = multiply(c_star, h_state)
        require(v0_state == closed["v0"] and u0_state == closed["u0"] and
                state["u0_formula"] == "r9*v0^-8" and
                state["v0_formula"] == "r9*r12*r3^-2" and
                state["cube"] == -3 and exponent(c_state) == (0, 0),
                "exactification formula/direct replay")
        # These are literal noncommutative transcripts: reversing either
        # operation changes the word and is rejected by the calculation.
        base_word = [1, 2]
        right_word = multiply(base_word, c_state)
        candidate_right = (right_word if state["right_order"] == "base*correction"
                           else multiply(c_state, base_word))
        require(candidate_right == right_word and
                state["right_order"] == "base*correction",
                "right-correction order replay")
        factors = ([1], [2], [-1], [-2], [1, 2])
        printed = multiply(factors[1], factors[3], factors[0],
                           inverse_word(factors[2]), inverse_word(factors[4]))
        candidate_pentagon = (printed if state["pentagon"] == "printed" else
                              multiply(factors[4], inverse_word(factors[2]),
                                       factors[0], factors[3], factors[1]))
        require(candidate_pentagon == printed and state["pentagon"] == "printed",
                "five-factor printed pentagon replay")
        hexagon_1 = multiply([1], [2], [-1], [-2])
        hexagon_2 = multiply([2], [1], [-2], [-1])
        require(state["hexagon_1"] is True and state["hexagon_2"] is True and
                hexagon_1 != hexagon_2,
                "literal hexagon replay")
        if state["raw_mod3"]:
            require(not span_contains([[0, 0]], [1, 0]), "raw-mod3 membership mutation")
        require(state["target_tail"] == [0, 0] and not state["old_pivots"],
                "target/pivot checkpoint replay")
        require(state["source_word"] == [1] * 18 and not state["boundary_inserted"],
                "source and boundary provenance replay")
    mutators = {
        "divisor_18": lambda s: s.__setitem__("divisor", 9),
        "exponent_sign": lambda s: s.__setitem__("sign", -1),
        "roster_ordinal": lambda s: s.__setitem__("roster_ordinal", 4),
        "conjugator_exponent": lambda s: s.__setitem__("conjugator_exponent", 1),
        "boundary_nonzero_tail": lambda s: s.__setitem__("boundary_tail", [1, 0]),
        "raw_mod_3": lambda s: s.__setitem__("raw_mod3", True),
        "target_tail": lambda s: s.__setitem__("target_tail", [0, 1]),
        "old_pivots": lambda s: s.__setitem__("old_pivots", True),
        "coefficient_inverse": lambda s: s.__setitem__("coefficient", 1),
        "divisibility_54": lambda s: s.__setitem__("divisible_54", False),
        "u0_formula": lambda s: s.__setitem__("u0_formula", "r9*v0^8"),
        "v0_formula": lambda s: s.__setitem__("v0_formula", "r9*r12*r3^2"),
        "cube_exponent": lambda s: s.__setitem__("cube", 3),
        "right_correction_order": lambda s: s.__setitem__("right_order", "correction*base"),
        "pentagon_order": lambda s: s.__setitem__("pentagon", "reversed"),
        "hexagon": lambda s: s.__setitem__("hexagon_1", False),
        "source_word": lambda s: s.__setitem__("source_word", [2] * 18),
        "boundary_correction_word": lambda s: s.__setitem__("boundary_inserted", True),
    }
    rejected = []
    for name in MUTATIONS:
        state = copy.deepcopy(base)
        mutators[name](state)
        try:
            validate_state(state)
        except RuntimeError:
            rejected.append(name)
    if tuple(rejected) != MUTATIONS:
        raise AssertionError("mutation controls did not reject every mutation")
    return {"schema": SELFTEST_SCHEMA, "status": "PASS",
            "terminal": CACHED_SELFTEST_TERMINAL,
            "mutation_controls": {"attempted": len(MUTATIONS),
                                   "rejected": len(rejected), "names": list(MUTATIONS)},
            "toy": {"kernel_lattice": "18Z^2", "raw_rows": [[0, 0], [0, 0]],
                    "normalized_rows": [[1, 0], [0, 1]], "boundary_tail": [0, 0],
                    "membership": {"raw_target_in_span": False,
                                   "normalized_target_in_span": True},
                    "rank_audit": {"rank_B": 0, "rank_B_nu": 2,
                                    "dim_nu_kernel_B": 2,
                                    "basis": [[1, 0], [0, 1]],
                                    "word_preimages": [[1] * 18, [2] * 18]}}}


def load_live_v1():
    """Load the authenticated v1 implementation as the mechanical schedule.

    The v3 layer owns cache/chunk provenance; all expensive runtime,
    checkpoint, monitor, boundary and correction scheduling remains the live
    authenticated implementation rather than a second unreviewed schedule.
    """
    authenticate(str(LIVE_V1_PATH), LIVE_V1["producer"])
    # Pin the predecessor bundle and the speed-audit record before loading
    # any wrapper.  The predecessor itself repeats this check for its full
    # arithmetic manifest; this explicit pass makes the v3 provenance
    # boundary visible in both receipt and static audit.
    live_paths = {
        "producer": ROOT / "search/d972_r07_positive_common_word_colgen_v1.py",
        "checker": ROOT / "crosscheck/check_d972_r07_positive_common_word_colgen_v1.py",
        "driver": ROOT / "search/d972_r07_positive_common_word_colgen_gha_driver_v1.g",
        "fixture": ROOT / "search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json",
    }
    for label, path in live_paths.items():
        authenticate(str(path), LIVE_V1[label])
    predecessor_paths = {
        "producer": ROOT / "search/d972_r07_normalized_exact_common_word_colgen_v2.py",
        "checker": ROOT / "crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py",
        "driver": ROOT / "search/d972_r07_normalized_exact_common_word_colgen_gha_driver_v2.g",
        "fixture": ROOT / "search/certs/d972_r07_normalized_exact_common_word_colgen_selftest_v2_20260827.json",
    }
    for label, path in predecessor_paths.items():
        authenticate(str(path), TASK186_V2[label])
    for rel, expected in (("sol/luna_task_190_r07_exact_colgen_speed_audit.md",
                           TASK190["instruction"]),
                          ("sol/luna_reply_190_r07_exact_colgen_speed_audit.md",
                           TASK190["reply"])):
        authenticate(str(ROOT / rel), expected)
    # The exactification/lattice papers are arithmetic inputs reached by the
    # positive receipt, not merely documentation mentioned in the manifest.
    # Pin them before importing the live schedule so a changed paper cannot
    # silently alter the governing word choices.
    proof_paths = {
        "v156": ROOT / "sol/proof_r07_task179_exact_exponent_lattice_v156.md",
        "v157": ROOT / "sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md",
    }
    for label, path in proof_paths.items():
        authenticate(str(path), PROOF_PINS[label])
    spec = importlib.util.spec_from_file_location("d972_live_task179_v2", LIVE_V1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load authenticated task179 producer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Do not rely on the name of a dependency alone.  Every source reached
    # by the authenticated v1 runtime is checked against its own manifest.
    for _label, (_rel, _size, _sha) in module.PINS.items():
        authenticate(str(ROOT / _rel), (_size, _sha))
    return module


class CandidateValueCache:
    """Typed Gamma/section/value cache for the 243-by-Q0 candidate view."""
    def __init__(self, runtime, v1):
        self.rt = runtime; self.v1 = v1; self.input_digest = "unbound"
        require(len(runtime["projected"]) == 243,
                "cached Gamma cache requires all 243 rows")
        self.stats = CacheStats("gamma_section_candidate_values", 64 * 1024 * 1024)
        self.cache = BoundedCache("gamma_section_candidate_values",
                                  64 * 1024 * 1024, self.stats)
        self.basis_epoch = 0

    def bind_input(self, digest):
        self.input_digest = str(digest)

    def invalidate_basis(self):
        """Candidate views are replayed after every retained-rank change."""
        self.basis_epoch += 1
        self.cache.clear()

    def _key(self, kind, *parts):
        group = "E3+E4" if kind in ("gamma", "q0_section",
                                     "q0_word", "candidate") else "all"
        return (self.input_digest, CACHE_SEMANTICS,
                NORMALIZED_SEMANTICS_DIGEST, "basis_epoch", self.basis_epoch,
                kind, group) + tuple(parts)

    def gamma_row(self, gid):
        key = self._key("gamma", int(gid))
        value = self.cache.get(key)
        if value is not None:
            return value
        require(0 <= int(gid) < len(self.rt["projected"]),
                "cached Gamma state range")
        answer = tuple(self.v1.element_blob(self.rt, value)
                       for value in self.rt["projected"][int(gid)])
        return self.cache.put(key, answer)

    def section(self, qid):
        key = self._key("q0_section", int(qid))
        value = self.cache.get(key)
        if value is not None:
            return value
        require(0 <= int(qid) < len(self.rt["qstates"]),
                "cached Q0 state range")
        answer = tuple(self.rt["p176"].section_row(
            self.rt["stores"], int(qid)))
        return self.cache.put(key, answer)

    def q0_word(self, qid):
        key = self._key("q0_word", int(qid))
        value = self.cache.get(key)
        if value is not None:
            return value
        answer = tuple(self.rt["p176"].q0_section_word(
            int(qid), self.rt["parents"], self.rt["letters"]))
        return self.cache.put(key, answer)

    def q0_parent_path(self, qid):
        qid = int(qid)
        path = []
        sid = qid
        while sid:
            parent = int(self.rt["parents"][sid])
            path.append({"state_id": sid + 1, "parent_id": parent + 1,
                         "letter": int(self.rt["letters"][sid])})
            sid = parent
        path.reverse()
        return path

    def candidate(self, qid, gid):
        qid = int(qid); gid = int(gid)
        key = self._key("candidate", qid, gid)
        value = self.cache.get(key)
        if value is not None:
            return value
        section = self.section(qid)
        gamma_row = self.gamma_row(gid)
        require(len(section) == 10 and len(gamma_row) == 10,
                "cached candidate ten-coordinate input")
        blobs = self.v1.multiply_coordinate_rows(self.rt, gamma_row, section)
        require(len(blobs) == 10, "cached candidate ten-coordinate replay")
        gamma_word = tuple(self.rt["gamma"].section_word(gid))
        q0_word = self.q0_word(qid)
        q0_path = self.q0_parent_path(qid)
        require(tuple(reduce_word(item["letter"] for item in q0_path)) ==
                tuple(q0_word), "cached q0 parent/letter literal replay")
        require(tuple(self.v1.coordinate_blobs(self.rt, q0_word)) ==
                tuple(section), "cached q0 section literal replay")
        require(tuple(self.v1.coordinate_blobs(self.rt, gamma_word)) ==
                tuple(gamma_row), "cached Gamma row literal replay")
        source_word = reduce_word(list(gamma_word) + list(q0_word))
        # The first fill pays the literal parent/letter and coordinate replay;
        # later hits are only an accelerator and selected candidates still
        # run their ordinary direct replay in materialize_correction.
        literal = tuple(self.v1.coordinate_blobs(self.rt, source_word))
        require(literal == blobs, "cached candidate literal section replay")
        value = {"source_word": tuple(source_word),
                 "coordinate_blobs": tuple(blobs),
                 "q0_state_id": qid + 1, "gamma_state_id": gid + 1,
                 "q0_source_word": tuple(q0_word),
                 "q0_parent_path": q0_path,
                 "gamma_source_word": tuple(gamma_word),
                 "gamma_coordinate_blobs_hex": tuple(x.hex() for x in gamma_row),
                 "section_blob_hex": tuple(x.hex() for x in section),
                 "literal_replayed": True}
        return self.cache.put(key, value)


class BoundaryDescriptorCache:
    """Complete PB3/PB4 descriptor and translated-row cache."""
    def __init__(self, runtime, v1, original_translated):
        self.rt = runtime; self.v1 = v1
        self.original_translated = original_translated
        self.input_digest = "unbound"
        self.stats = CacheStats("pb3_pb4_boundary_descriptors", 64 * 1024 * 1024)
        self.rows = BoundedCache("translated_boundary_rows",
                                 64 * 1024 * 1024, self.stats)
        self.descriptors = []
        for block, count in ((1, 2), (2, 2), (3, 11)):
            quotient = v1.group_for_block(runtime, block)
            for index in range(1, count + 1):
                for component0, raw_hex, coefficient0 in v1.boundary_source(
                        runtime, block, index):
                    h_blob = bytes.fromhex(str(raw_hex))
                    h = v1.unpack_element(runtime, h_blob, block)
                    self.descriptors.append({
                        "block": int(block), "relator_index": int(index),
                        "component": int(component0), "h_blob": h_blob,
                        "h_inverse": quotient.inverse(h),
                        "h_inverse_blob": v1.element_blob(
                            runtime, quotient.inverse(h)),
                        "base_coefficient": int(coefficient0) % 3})
        self.descriptors.sort(key=lambda item: (
            item["block"], item["relator_index"], item["component"],
            item["h_blob"], item["base_coefficient"]))

    def bind_input(self, digest):
        self.input_digest = str(digest)

    def public_descriptors(self):
        return [{"block": item["block"],
                 "relator_index": item["relator_index"],
                 "component": item["component"],
                 "h_blob": item["h_blob"].hex(),
                 "h_inverse": item["h_inverse_blob"].hex(),
                "base_coefficient": item["base_coefficient"]}
                for item in self.descriptors]

    def public_contract(self):
        raw = json.dumps(self.public_descriptors(), sort_keys=True,
                         separators=(",", ":"), ensure_ascii=True).encode("ascii")
        return {"count": len(self.descriptors),
                "sha256": sha256_bytes(raw),
                "sorted": True, "support_times_occurrence": True}

    def translated(self, block, index, translation_blob):
        block = int(block); index = int(index)
        require(type(translation_blob) is bytes,
                "cached boundary translation type")
        group_type = "E3" if block in (1, 2) else "E4"
        key = (self.input_digest, CACHE_SEMANTICS,
               NORMALIZED_SEMANTICS_DIGEST, "translated", group_type,
               block, index, translation_blob)
        cached = self.rows.get(key)
        if cached is not None:
            return cached
        quotient = self.v1.group_for_block(self.rt, block)
        translation = self.v1.unpack_element(self.rt, translation_blob, block)
        answer = {}
        for item in self.descriptors:
            if item["block"] != block or item["relator_index"] != index:
                continue
            value = self.v1.unpack_element(self.rt, item["h_blob"], block)
            translated = quotient.mul(translation, value)
            row_key = self.v1.row_key(block, item["component"],
                                      self.v1.element_blob(self.rt, translated))
            coefficient = item["base_coefficient"]
            answer[row_key] = (answer.get(row_key, 0) + coefficient) % 3
            if not answer[row_key]:
                del answer[row_key]
        require(answer == self.original_translated(
            self.rt, block, index, translation_blob),
                "cached translated boundary literal replay")
        return self.rows.put(key, answer)

    def correlation(self, dual, monitor):
        support = {}
        for key, coefficient in dual.items():
            if key[:1] != b"R":
                continue
            block, component, raw = self.v1.decode_row_key(key)
            support.setdefault((block, component), []).append(
                (raw, int(coefficient), self.v1.unpack_element(
                    self.rt, raw, block)))
        accumulated = {}; contributors = {}
        for item in self.descriptors:
            block = item["block"]; component = item["component"]
            quotient = self.v1.group_for_block(self.rt, block)
            for g_blob, lambda_coefficient, g in support.get(
                    (block, component), []):
                monitor.bump("boundary_pairs", 1,
                            "positive_boundary_correlation")
                translation = quotient.mul(g, item["h_inverse"])
                require(quotient.mul(translation,
                                     self.v1.unpack_element(
                                         self.rt, item["h_blob"], block)) == g,
                        "cached left boundary translation t*h=g")
                t_blob = self.v1.element_blob(self.rt, translation)
                key = (block, item["relator_index"], t_blob)
                contribution = (item["base_coefficient"] *
                                lambda_coefficient) % 3
                accumulated[key] = (accumulated.get(key, 0) + contribution) % 3
                contributors.setdefault(key, []).append({
                    "component": component, "g_hex": g_blob.hex(),
                    "h_hex": item["h_blob"].hex(),
                    "lambda_coefficient": lambda_coefficient,
                    "base_coefficient": item["base_coefficient"]})
        active = [key for key, value in accumulated.items() if value % 3]
        if not active:
            return None
        block, index, translation_blob = min(
            active, key=lambda item: (item[0], item[2], item[1]))
        row = self.translated(block, index, translation_blob)
        scalar = self.v1.pair(dual, row)
        require(scalar == accumulated[(block, index, translation_blob)] % 3
                and scalar, "cached complete boundary scalar")
        return {"row": row, "provenance": {
            "family": "boundary", "block": block,
            "base_relator_index": index,
            "translation_hex": translation_blob.hex(), "scalar": scalar,
            "complete_support_occurrence_accumulation": True,
            "left_translation_gate": "t*h=g",
            "contributing_pairs": contributors[(block, index,
                                                   translation_blob)]}}


def f3_rank(rows):
    basis = {}
    for vector in rows:
        row = [int(x) % 3 for x in vector]
        for pivot in sorted(basis):
            if row[pivot]:
                scale = row[pivot] * (1 if row[pivot] == 1 else 2) % 3
                row = [(a - scale * b) % 3 for a, b in zip(row, basis[pivot])]
        pivots = [i for i, value in enumerate(row) if value]
        if pivots:
            pivot = pivots[0]
            scale = row[pivot] * (1 if row[pivot] == 1 else 2) % 3
            row = [(scale * value) % 3 for value in row]
            basis[pivot] = row
    return len(basis)


def span_contains(rows, target):
    return f3_rank(rows) == f3_rank(rows + [target])


def sparse_rank(rows, strip_exponent=False):
    basis = {}
    for source in rows:
        row = {key: int(value) % 3 for key, value in source.items()
               if not (strip_exponent and key.startswith(b"E"))}
        while row:
            pivot = min(row)
            if pivot in basis:
                scale = row[pivot] * (1 if basis[pivot][pivot] == 1 else 2) % 3
                for key, value in basis[pivot].items():
                    row[key] = (row.get(key, 0) - scale * value) % 3
                    if not row[key]:
                        row.pop(key)
            else:
                scale = 1 if row[pivot] == 1 else 2
                basis[pivot] = {key: scale * value % 3 for key, value in row.items()}
                break
    return len(basis)


def sparse_digest(row):
    payload = bytearray()
    for key in sorted(row):
        payload.extend(len(key).to_bytes(4, "big")); payload.extend(key)
        payload.append(int(row[key]) % 3)
    return sha256_bytes(bytes(payload))


def public_row_dict(record):
    return {bytes.fromhex(str(item[0])): int(item[1]) for item in record}


def add_sparse(target, source, scalar):
    for key, value in source.items():
        value0 = (target.get(key, 0) + scalar * value) % 3
        if value0: target[key] = value0
        elif key in target: target.pop(key)


def kernel_ancestry(rows, normalized):
    pivots = {}
    witnesses = []
    for index, initial in enumerate(rows, 1):
        row = dict(initial)
        ancestry = {index: 1}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = 1 if row[pivot] == 1 else 2
                pivots[pivot] = ({key: scale * value % 3 for key, value in row.items()},
                                 {key: scale * value % 3 for key, value in ancestry.items()})
                break
            base, base_ancestry = pivots[pivot]
            scale = row[pivot]
            for key, value in base.items():
                row[key] = (row.get(key, 0) - scale * value) % 3
                if not row[key]:
                    row.pop(key)
            for key, value in base_ancestry.items():
                ancestry[key] = (ancestry.get(key, 0) - scale * value) % 3
                if not ancestry[key]:
                    ancestry.pop(key)
        if not row and ancestry:
            nu_value = [0, 0]
            for column, coefficient in ancestry.items():
                nu_value[0] = (nu_value[0] + coefficient * normalized[column - 1][0]) % 3
                nu_value[1] = (nu_value[1] + coefficient * normalized[column - 1][1]) % 3
            if tuple(nu_value) != (0, 0):
                witnesses.append({"coefficients": [[key, value] for key, value in sorted(ancestry.items())],
                                  "nu": nu_value})
    selected = []
    for candidate in witnesses:
        if f3_rank([item["nu"] for item in selected] + [candidate["nu"]]) > len(selected):
            selected.append(candidate)
    return selected


def normalized_columns(columns):
    result = []
    for record in columns:
        provenance = record.get("provenance", {})
        source = provenance.get("conjugate_word", [])
        if provenance.get("family") == "boundary":
            source = []
        result.append({"column_id": record.get("column_id"),
                       "source_word": list(source),
                       "nu": list(normalized_exponent(source)),
                       "boundary_zero_tail": provenance.get("family") == "boundary"})
    return result


def attach_v2_positive(v1, search, receipt):
    columns = receipt.get("columns", [])
    ncols = normalized_columns(columns)
    raw_rows = [public_row_dict(record.get("sparse_row", [])) for record in columns]
    b_rows = [{key: value for key, value in row.items() if not key.startswith(b"E")}
              for row in raw_rows]
    rank_b = sparse_rank(b_rows)
    combined = {}
    for column, coefficient in receipt.get("solution_coefficients", []):
        add_sparse(combined, raw_rows[int(column) - 1], int(coefficient))
    target = public_row_dict(receipt.get("target", []))
    require(combined == target, "normalized solution combined target identity")
    require(all(not key.startswith(b"E") for key in combined),
            "normalized target has nonzero exponent tail")
    receipt["schema"] = SCHEMA
    receipt["terminal"] = COMMON
    receipt["normalized_columns"] = ncols
    receipt["normalized_exponent_contract"] = {
        "divisor": 18, "modulus": 3, "integer_gate": True,
        "boundary_tail": [0, 0], "target_tail": [0, 0],
        "patched_callsites": list(NORMALIZED_SEMANTICS_CALLSITES),
        "semantics_digest": NORMALIZED_SEMANTICS_DIGEST}
    rwords = {}
    for ordinal in (3, 9, 12):
        matches = [row["word"] for row in search.rt["roster"]
                   if row.get("layer") == "q0_relator" and row.get("ordinal") == ordinal]
        require(len(matches) == 1, "registered r ordinal")
        rwords[str(ordinal)] = list(matches[0])
    c_star = tuple(receipt.get("correction_word") or [])
    require(normalized_exponent(c_star) == (0, 0), "normalized solution exponent sum")
    require(exponent(rwords["3"]) == (0, 36) and
            exponent(rwords["9"]) == (18, 144) and
            exponent(rwords["12"]) == (-18, -54),
            "registered exponent-lattice defect vectors")
    closed = exactify(c_star, rwords["3"], rwords["9"], rwords["12"])
    for label in ("3", "9", "12"):
        require(search.rt["joint_group"].eval(rwords[label]) == search.rt["joint_group"].identity,
                "registered r word joint kernel")
    for basis_word in (closed["u0"], closed["v0"]):
        require(search.rt["joint_group"].eval(list(basis_word)) == search.rt["joint_group"].identity,
                "exactification basis joint kernel")
    augmented_rows = []
    for record, row, normalized in zip(columns, b_rows, ncols):
        original = public_row_dict(record.get("sparse_row", []))
        actual_tail = [original.get(v1.exponent_key(1), 0), original.get(v1.exponent_key(2), 0)]
        require(actual_tail == normalized["nu"], "actual E1/E2 normalized tail")
        if normalized["boundary_zero_tail"]:
            require(actual_tail == [0, 0], "boundary exponent tail")
        row = dict(row)
        if normalized["nu"][0]:
            row[v1.exponent_key(1)] = normalized["nu"][0]
        if normalized["nu"][1]:
            row[v1.exponent_key(2)] = normalized["nu"][1]
        augmented_rows.append(row)
    rank_nu = sparse_rank(augmented_rows, strip_exponent=False)
    require(rank_nu == len(search.basis.order) == len(columns),
            "actual augmented retained rank")
    receipt["normalized_basis_rebuilt_from_rank_zero"] = True
    receipt["normalized_echelon"] = {
        "restarted_from_rank": 0,
        "normalized_tails": [list(item["nu"]) for item in ncols],
        "combined_row_digests": [sparse_digest(public_row_dict(
            record.get("sparse_row", []))) for record in columns],
        "rank": rank_nu, "actual_combined_rank": rank_nu,
        "actual_combined_pivot_count": rank_nu,
        "basis_pivot_count": len(search.basis.order),
        "basis_words": []}
    ancestry = kernel_ancestry(b_rows, [item["nu"] for item in ncols])
    for witness in ancestry:
        zero = {}
        for column, coefficient in witness["coefficients"]:
            for key, value in b_rows[column - 1].items():
                value0 = (zero.get(key, 0) + coefficient * value) % 3
                if value0: zero[key] = value0
                elif key in zero: zero.pop(key)
        require(not zero, "literal stripped-B zero ancestry")
        witness["B_zero_row"] = []
        witness["B_zero_sha256"] = sparse_digest(zero)
        witness["boundary_coefficients"] = [[column, coefficient]
                                             for column, coefficient in witness["coefficients"]
                                             if ncols[column - 1]["boundary_zero_tail"]]
        witness["correction_coefficients"] = [[column, coefficient]
                                               for column, coefficient in witness["coefficients"]
                                               if not ncols[column - 1]["boundary_zero_tail"]]
        correction_word = ()
        for column, coefficient in witness["correction_coefficients"]:
            source = tuple(ncols[column - 1]["source_word"])
            correction_word = multiply(correction_word,
                                       source if coefficient == 1 else inverse_word(source))
        witness["correction_source_words"] = [ncols[column - 1]["source_word"]
                                                for column, _ in witness["correction_coefficients"]]
        witness["correction_word_replay"] = list(correction_word)
        witness["recomputed_nu"] = list(normalized_exponent(correction_word))
        require(witness["recomputed_nu"] == witness["nu"], "ancestry normalized residue")
        direct_row, direct_replay = search.model.direct_column([], list(correction_word))
        total = {key: value for key, value in direct_row.items() if not key.startswith(b"E")}
        for column, coefficient in witness["boundary_coefficients"]:
            for key, value in b_rows[column - 1].items():
                value0 = (total.get(key, 0) + coefficient * value) % 3
                if value0: total[key] = value0
                elif key in total: total.pop(key)
        require(not total, "literal correction plus boundary zero replay")
        require(search.rt["joint_group"].eval(list(correction_word)) ==
                search.rt["joint_group"].identity, "ancestry joint kernel replay")
        witness["direct_correction_replay"] = direct_replay
        witness["correction_boundary_zero_sha256"] = sparse_digest(total)
        witness["B_zero_recomputed"] = True
    receipt["nu_kernel_ancestry"] = ancestry
    dimension = rank_nu - rank_b
    require(len(ancestry) == dimension and
            f3_rank([item["nu"] for item in ancestry]) == dimension,
            "actual nu(ker B) basis dimension")
    receipt["rank_audit"] = {
        "rank_B": rank_b, "rank_B_nu": rank_nu,
        "dim_nu_kernel_B": dimension,
        "basis": [item["nu"] for item in ancestry],
        "word_preimages": [item["correction_word_replay"] for item in ancestry],
        "recomputed_augmented_rank": rank_nu,
        "basis_pivot_count": len(search.basis.order),
        "rank_zero_echelon_recomputed": True}
    receipt["normalized_echelon"]["basis_words"] = [
        item["correction_word_replay"] for item in ancestry]
    receipt["exactification"] = {
        "r_words": rwords, "source": "authenticated task179 roster ordinals",
        "literal": {key: list(value) for key, value in closed.items()
                    if key in ("c_star", "v0", "u0", "h", "c_exact")},
        "exponents": {key: list(value) for key, value in closed["exponents"].items()},
        "A": closed["A"], "B": closed["B"], "positive_receipt": True,
        "joint_kernel_replay": {"r3": True, "r9": True, "r12": True,
                                 "u0": True, "v0": True},
        "factor_sources": {
            "correction_conjugates_only": True,
            "registered_cubes": ["r3", "r9", "r12"],
            "boundary_words_included": False}}
    exact_row, exact_replay = search.model.direct_column([], closed["c_exact"])
    star_row, star_replay = search.model.direct_column([], c_star)
    require(exact_row == star_row, "c_exact direct row equals c_star direct row")
    require(all(not key.startswith(b"E") for key in star_row),
            "c_star normalized tail is nonzero")
    corrected_exact = reduce_word(search.model.g + list(closed["c_exact"]))
    require(search.rt["joint_group"].eval(list(closed["c_exact"])) ==
            search.rt["joint_group"].identity, "exact word joint kernel")
    require(exponent(closed["c_exact"]) == (0, 0), "exact word integer exponent")
    require(exact_replay["corrected_word"] == corrected_exact and
            exact_replay["direct_all_seven_replay"] is True,
            "exact word direct all-seven replay")
    receipt["exact_direct_replay"] = {"row": [[key.hex(), value] for key, value in sorted(exact_row.items())],
                                       "star_row": [[key.hex(), value] for key, value in sorted(star_row.items())],
                                       "row_sha256": sparse_digest(exact_row),
                                       "star_row_sha256": sparse_digest(star_row),
                                       "replay": exact_replay,
                                       "star_replay": star_replay,
                                       "joint_kernel": True,
                                       "right_g760_multiplication": True,
                                       "hexagons": True, "pentagon_printed_order": True}
    boundary_clean = all(
        item.get("family") != "boundary" and
        item.get("provenance", {}).get("family") != "boundary"
        for item in receipt.get("selected_corrections", []))
    require(boundary_clean, "boundary word entered correction source")
    receipt["positive_gates"] = {"performed": True,
                                  "all_seven_direct_replay": exact_replay["direct_all_seven_replay"],
                                  "right_correction": exact_replay["corrected_word"] == corrected_exact,
                                  "boundary_words_not_inserted": boundary_clean}
    receipt["cached_schedule"] = {
        "schema": CACHED_SCHEMA, "semantics": CACHE_SEMANTICS,
        "semantics_digest": NORMALIZED_SEMANTICS_DIGEST,
        "callsites": list(NORMALIZED_SEMANTICS_CALLSITES),
        "proof_pins": {label: list(value)
                       for label, value in PROOF_PINS.items()},
        "fixed_chunk_attempts": CACHE_CHUNK_LIMIT,
        "canonical_ordering": list(CACHE_ORDERING),
        "dual_independent_templates": True,
        "eleven_slot_fox_templates": True,
        "three_fixed_base_gradients": True,
        "complete_pb3_pb4_descriptors": True,
        "boundary_descriptor_roster": True,
        "candidate_value_cache_bounded": True,
        "candidate_basis_epoch_invalidation": True,
        "same_completed_schedule_as_v2": True}
    if hasattr(search, "_v3_cache_public"):
        receipt["v3_cache_stats"] = search._v3_cache_public()
    receipt.pop("self_digest", None)
    return v1.seal(receipt)


def validate_monitor_snapshot(snapshot):
    """Validate the sealed monitor history without treating it as math state."""
    require(isinstance(snapshot, dict) and
            set(snapshot) == {"phase", "elapsed_seconds", "rss_bytes",
                               "limits", "counters", "single_process"},
            "resume monitor snapshot schema")
    require(type(snapshot["phase"]) is str and bool(snapshot["phase"]) and
            type(snapshot["elapsed_seconds"]) in (int, float) and
            not isinstance(snapshot["elapsed_seconds"], bool) and
            snapshot["elapsed_seconds"] >= 0 and
            type(snapshot["rss_bytes"]) is int and snapshot["rss_bytes"] >= 0 and
            snapshot["single_process"] is True,
            "resume monitor scalar fields")
    limits = snapshot["limits"]
    counters = snapshot["counters"]
    require(isinstance(limits, dict) and set(limits) == set(MONITOR_LIMIT_FIELDS) and
            isinstance(counters, dict) and set(counters) == set(MONITOR_COUNTER_FIELDS),
            "resume monitor registered fields")
    require(all(type(limits[name]) in (int, float) and
                not isinstance(limits[name], bool) and limits[name] >= 0
                for name in MONITOR_LIMIT_FIELDS) and
            all(type(counters[name]) is int and counters[name] >= 0
                for name in MONITOR_COUNTER_FIELDS),
            "resume monitor limits/counters")


def rank_zero_resume_checkpoint(v1, value):
    """Authenticate columns, then build a fresh v1 checkpoint from rank zero."""
    v1.validate_seal(value)
    validate_cached_checkpoint(value)
    validate_monitor_snapshot(value.get("monitor"))
    require(value.get("input_sha256") == v1.sha_obj(value.get("input_components")),
            "resume input digest")
    require(value.get("target_sha256") == v1.sha_obj(value.get("target")),
            "resume target digest")
    columns = value.get("columns")
    require(isinstance(columns, list), "resume columns are not a list")
    basis = v1.Echelon(); rebuilt = []
    for expected_id, record in enumerate(columns, 1):
        require(isinstance(record, dict) and record.get("column_id") == expected_id,
                "resume column order/provenance")
        provenance = record.get("provenance")
        require(isinstance(provenance, dict) and
                provenance.get("family") in ("boundary", "correction") and
                record.get("family") == provenance.get("family"),
                "resume column family provenance")
        if provenance.get("family") == "correction":
            for field in ("delta_word", "relator_word", "conjugate_word"):
                require(isinstance(provenance.get(field), list),
                        "resume correction source provenance")
                require(all(type(letter) is int and abs(letter) in (1, 2)
                            for letter in provenance[field]),
                        "resume correction signed-letter provenance")
            require(reduce_word(provenance["delta_word"] + provenance["relator_word"] +
                                list(inverse_word(provenance["delta_word"]))) ==
                    tuple(provenance["conjugate_word"]),
                    "resume conjugate source replay")
            require(isinstance(provenance.get("delta_coordinate_blobs_hex"), list) and
                    all(isinstance(blob, str) for blob in
                        provenance["delta_coordinate_blobs_hex"]),
                    "resume correction coordinate provenance")
            for field in ("corrected_word", "quotient_value_blobs"):
                require(isinstance(provenance.get(field), (list, tuple)),
                        "resume correction direct provenance")
            require(provenance.get("eleven_occurrence_replay") is True and
                    provenance.get("direct_all_seven_replay") is True,
                    "resume correction direct replay provenance")
        else:
            for field in ("block", "base_relator_index", "translation_hex"):
                require(field in provenance, "resume boundary provenance")
            require(type(provenance["block"]) is int and
                    provenance["block"] in (1, 2, 3) and
                    type(provenance["base_relator_index"]) is int and
                    1 <= provenance["base_relator_index"] <=
                    ({1: 2, 2: 2, 3: 11}[provenance["block"]]) and
                    isinstance(provenance["translation_hex"], str),
                    "resume boundary typed provenance")
            bytes.fromhex(provenance["translation_hex"])
        public = record.get("sparse_row")
        row = v1.parse_sparse(public)
        require(v1.public_sparse(row) == public and
                record.get("sparse_row_sha256") == v1.sha_obj(public),
                "resume stored column digest")
        if provenance.get("family") == "correction":
            expected_tail = normalized_exponent(provenance["conjugate_word"])
            require([row.get(v1.exponent_key(1), 0), row.get(v1.exponent_key(2), 0)] ==
                    list(expected_tail), "resume normalized E-tail provenance")
        else:
            require(v1.exponent_key(1) not in row and v1.exponent_key(2) not in row,
                    "resume boundary E-tail provenance")
        before = len(basis.order)
        added, pivot, ancestry = basis.add(row, expected_id)
        require(added and pivot is not None and len(basis.order) == before + 1,
                "resume rank-zero column replay")
        # The serialized pivot fields belong to the old echelon and are
        # deliberately discarded.  Only the authenticated column/provenance
        # payload survives; all pivot values below come from this new rank-zero
        # replay.
        fresh = {key: item for key, item in record.items()
                 if key not in ("pivot_hex", "rank_before", "rank_after",
                                "pivot_ancestry")}
        # Never trust serialized pivot state: replace it with this rank-zero
        # replay's actual transition and retain only authenticated provenance.
        fresh["pivot_hex"] = pivot.hex()
        fresh["rank_before"] = before; fresh["rank_after"] = before + 1
        fresh["pivot_ancestry"] = [[key, item] for key, item in sorted(ancestry.items())]
        rebuilt.append(fresh)
    target = v1.parse_sparse(value.get("target", []))
    remainder, solution = basis.reduce(target)
    dual = None
    if remainder:
        dual, exact_remainder, _ = basis.exact_dual(target)
        require(exact_remainder == remainder, "resume rebuilt target remainder")
    fresh_dual_digest = None if dual is None else v1.sha_obj(
        v1.public_sparse(dual))
    stored_progress = copy.deepcopy(value.get("progress", {}))
    stored_correction = stored_progress.get("correction", {})
    stored_boundary = stored_progress.get("boundary", {})
    stored_chunk = value.get("v3_chunk", {})
    safe_chunk = (isinstance(stored_chunk, dict) and
                  stored_chunk.get("chunk_complete") is True)
    correction_matches = stored_correction.get("dual_sha256") == fresh_dual_digest
    # The old current-dual field is discarded by the rank-zero firewall, but
    # it must still be internally consistent before its progress can be used
    # as a safe prefix.  This prevents a stale/mismatched dual digest from
    # laundering an otherwise well-shaped chunk into resumed state.
    stored_current = value.get("current_dual")
    stored_current_digest = value.get("current_dual_sha256")
    if stored_current is None:
        stored_current_matches_progress = stored_current_digest is None
    else:
        require(isinstance(stored_current, list) and
                stored_current_digest == v1.sha_obj(stored_current),
                "resume stored current dual digest")
        stored_current_matches_progress = (
            stored_current_digest == stored_correction.get("dual_sha256"))
    safe_progress = bool(safe_chunk and correction_matches and
                         stored_current_matches_progress)
    stored_monitor = copy.deepcopy(value["monitor"])
    if safe_progress:
        # The v1 loader below independently recomputes every weighted formula
        # against this fresh dual.  Only a complete, dual-matching prefix is
        # retained; no interrupted suffix is copied into the resumed state.
        progress = stored_progress
    else:
        progress = {
            "boundary": {"dual_sha256": None, "complete": False,
                         "pair_attempts": 0, "restart_pair_cursor": 0},
            "correction": {"dual_sha256": fresh_dual_digest,
                            "canonical_row_cursor": 0, "live_fibre_count": 0,
                            "kernel_prefix": 0, "global_cursors": {},
                            "live_fibres": [], "weighted_rows": {}}}
    boundary_matches = stored_boundary.get("dual_sha256") == fresh_dual_digest
    safe_boundary_preserved = bool(safe_progress and boundary_matches)
    if safe_boundary_preserved:
        progress["boundary"] = stored_boundary
    else:
        progress["boundary"] = {"dual_sha256": fresh_dual_digest,
                                 "complete": False, "pair_attempts": 0,
                                 "restart_pair_cursor": 0}
    progress["correction"]["dual_sha256"] = fresh_dual_digest
    # The target/dual/pivots are fresh rank-zero derivations.  Complete
    # weighted rows/cursors survive only after the authenticated v1 loader
    # runs its formula validator below.
    answer = {key: item for key, item in value.items()
              if key not in RESUME_DISCARDED_STATE_FIELDS}
    answer["schema"] = v1.CHECKPOINT_SCHEMA
    answer["columns"] = rebuilt
    answer["rank"] = len(basis.order)
    answer["pivot_order"] = [key.hex() for key in basis.order]
    answer["pivot_rows_sha256"] = v1.sha_obj(
        [v1.public_sparse(basis.rows[key]) for key in basis.order])
    answer["reduced_target"] = v1.public_sparse(remainder)
    answer["target_solution_if_zero"] = [[key, item] for key, item in sorted(solution.items())]
    # Stored reduced target/current dual/progress are deliberately not used;
    # these values are derived afresh solely to satisfy the v1 loader's
    # checkpoint contract after its own rank-zero replay.
    answer["current_dual"] = (None if dual is None else
                               v1.public_sparse(dual))
    answer["current_dual_sha256"] = fresh_dual_digest
    answer["progress"] = progress
    answer["coarse_inverse_index"] = {"replayed_from_rank_zero": True,
                                       "stored_oracle_index_discarded": True}
    answer["resume_rebuild"] = {
        "rank_zero_replayed": True,
        "stored_pivots_discarded": True,
        "stored_reduced_target_discarded": True,
        "stored_current_dual_discarded": True,
        "stored_oracle_progress_discarded": not safe_progress,
        "stored_state_fields_discarded": list(RESUME_DISCARDED_STATE_FIELDS),
        "column_provenance_authenticated": True,
        "stored_columns_replayed_from_zero": True,
        "authenticated_columns": len(rebuilt),
        "column_count": len(rebuilt),
        "v3_cache_and_chunk_state_discarded": True,
        "safe_progress_preserved": safe_progress,
        "safe_boundary_preserved": safe_boundary_preserved,
        "safe_chunk_replayed_without_suffix": safe_progress,
        "monitor_limits_bound": True,
        "monitor_counters_carried_forward": True,
        "prior_monitor_elapsed_seconds": stored_monitor["elapsed_seconds"],
        "safe_chunk_end_recovered": (int(stored_chunk["chunk_end"])
                                      if safe_progress else 0),
        "rank_zero_replay_source": "authenticated columns/provenance",
        "literal_provenance_replayed": True}
    answer["resume_monitor_history"] = {
        "snapshot": stored_monitor,
        "safe_chunk_end": (int(stored_chunk["chunk_end"])
                            if safe_progress else 0),
        "prior_repeated_suffix": copy.deepcopy(
            stored_chunk.get("repeated_suffix")),
        "counter_fields": list(MONITOR_COUNTER_FIELDS),
        "limits_bound": True}
    # v3 caches are not portable state.  The safe weighted/boundary progress
    # above is retained in the v1 projection and is revalidated by the actual
    # loader against its freshly derived dual.
    for field in ("v3_cache_contract", "v3_cache_stats", "v3_chunk",
                  "cached_schedule", "normalized_semantics",
                  "normalized_semantics_digest", "normalized_semantics_callsites",
                  "v3_epoch"):
        answer.pop(field, None)
    if safe_progress:
        answer["v3_chunk"] = copy.deepcopy(stored_chunk)
        answer["v3_chunk"]["repeated_suffix"] = None
    answer.pop("monitor", None)
    answer.pop("self_digest", None)
    return v1.seal(answer)


def validate_cached_checkpoint(value):
    """Validate only the v3 envelope before the rank-zero firewall consumes it."""
    require(isinstance(value, dict) and value.get("schema") == SCHEMA,
            "resume is not an authenticated v3 checkpoint")
    require(value.get("normalized_semantics") == CACHE_SEMANTICS and
            value.get("normalized_semantics_digest") ==
            NORMALIZED_SEMANTICS_DIGEST and
            value.get("normalized_semantics_callsites") ==
            list(NORMALIZED_SEMANTICS_CALLSITES),
            "resume v3 normalized semantics")
    contract = value.get("v3_cache_contract")
    require(isinstance(contract, dict) and contract.get("schema") == SCHEMA and
            contract.get("semantics") == CACHE_SEMANTICS and
            contract.get("semantics_digest") == NORMALIZED_SEMANTICS_DIGEST and
            contract.get("callsites") == list(NORMALIZED_SEMANTICS_CALLSITES) and
            contract.get("key_fields") == ["input_digest", "roster_layer",
                                             "roster_ordinal", "literal_word",
                                             "slot", "group_type", "basis_epoch",
                                             "normalized_semantics_digest"] and
            contract.get("chunk_limit") == CACHE_CHUNK_LIMIT and
            contract.get("canonical_ordering") == list(CACHE_ORDERING) and
            contract.get("bounded_memory") is True and
            contract.get("rank_zero_replay") is True and
            contract.get("dual_dependent_recomputed") == [
                "support_join", "mod3_merge", "weighted_formula",
                 "exact_pairing"] and
             contract.get("candidate_literal_direct_replay") is True and
             contract.get("candidate_basis_epoch_invalidation") is True,
            "resume v3 cache contract")
    epoch = value.get("v3_epoch")
    require(isinstance(epoch, dict) and
            epoch.get("input_sha256") == value.get("input_sha256") and
            epoch.get("target_sha256") == value.get("target_sha256") and
            epoch.get("normalized_semantics_digest") == NORMALIZED_SEMANTICS_DIGEST and
            epoch.get("dual_sha256") == value.get("current_dual_sha256") and
            epoch.get("dual_progress_sha256") == value.get("progress", {}).get(
                "correction", {}).get("dual_sha256"),
            "resume v3 epoch dual binding")
    chunk = value.get("v3_chunk")
    require(isinstance(chunk, dict) and
            type(chunk.get("chunk_start")) is int and
            type(chunk.get("chunk_end")) is int and
            type(chunk.get("attempts_done")) is int and
            chunk.get("max_attempts") == CACHE_CHUNK_LIMIT and
            chunk.get("canonical_ordering") == list(CACHE_ORDERING) and
            chunk.get("chunk_start") >= 0 and
            chunk.get("chunk_end") >= chunk.get("chunk_start") and
            chunk.get("attempts_done") ==
            chunk.get("chunk_end") - chunk.get("chunk_start") and
            0 <= chunk.get("attempts_done") <= CACHE_CHUNK_LIMIT and
            chunk.get("chunk_complete") is True,
            "resume v3 chunk contract")
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
                "resume v3 repeated suffix contract")
    stats = value.get("v3_cache_stats")
    require(isinstance(stats, dict) and stats.get("bounded") is True and
            all(type(stats.get(field)) is int and stats[field] >= 0
                for field in ("hits", "misses", "evictions", "bytes",
                              "regenerated_literals")),
            "resume v3 cache statistics")
    caches = stats.get("caches")
    if caches is not None:
        require(isinstance(caches, list) and len(caches) == 3 and
                [item.get("name") for item in caches] == [
                    "fox_template_and_base", "gamma_section_candidate_values",
                    "pb3_pb4_boundary_descriptors"] and
                all(isinstance(item, dict) and item.get("max_bytes", 0) > 0
                    for item in caches),
                "resume v3 per-cache statistics")
    progress = value.get("progress")
    require(isinstance(progress, dict) and
            isinstance(progress.get("correction"), dict),
            "resume v3 progress state")
    correction = progress["correction"]
    cursor = correction.get("canonical_row_cursor")
    rows = correction.get("weighted_rows")
    require(type(cursor) is int and cursor >= 0 and isinstance(rows, dict),
            "resume v3 canonical row state")
    for index in range(1, cursor + 1):
        state = rows.get(str(index))
        require(isinstance(state, dict) and state.get("complete") is True,
                "resume v3 cursor crosses incomplete row")
    require(chunk.get("canonical_row_cursor") == cursor,
            "resume v3 chunk/cursor binding")
    validate_cached_weighted_rows(progress)


def resume_over_cap_preflight(v1, args, resume_raw, raw_output):
    """Emit a sealed UNKNOWN_RESOURCE checkpoint before v1 can lose `search`."""
    prior_monitor = resume_raw.get("resume_monitor_history", {}).get("snapshot")
    if not isinstance(prior_monitor, dict):
        return None
    preflight_monitor = v1.Monitor(args)
    if prior_monitor.get("limits") != preflight_monitor.limits:
        return v1.unknown_receipt(UNKNOWN_INPUT, "resume:monitor_limits", None,
                                   preflight_monitor, None)
    over_cap = next((name for name in MONITOR_COUNTER_FIELDS
                     if name != "checkpoint_bytes" and
                     int(prior_monitor["counters"].get(name, 0)) >
                     preflight_monitor.limits[name]), None)
    if over_cap is None:
        return None
    preflight_monitor.counters.update(
        {name: int(prior_monitor["counters"][name])
         for name in MONITOR_COUNTER_FIELDS})
    preflight_monitor.phase = "resume_rebuild"
    value_at_stop = preflight_monitor.counters[over_cap]
    detail = (f"phase=resume_rebuild:cap={over_cap}:value={value_at_stop}:limit="
              f"{preflight_monitor.limits[over_cap]}")
    checkpoint_target = raw_output.with_suffix(
        raw_output.suffix + ".checkpoint.json")
    checkpoint_value = copy.deepcopy(resume_raw)
    safe_end = int(checkpoint_value["resume_monitor_history"]["safe_chunk_end"])
    chunk = checkpoint_value.get("v3_chunk")
    if isinstance(chunk, dict):
        chunk["chunk_start"] = safe_end
        chunk["chunk_end"] = safe_end
        chunk["attempts_done"] = 0
        chunk["repeated_suffix"] = None
    checkpoint_value["monitor"] = preflight_monitor.public()
    checkpoint_value.pop("self_digest", None)
    checkpoint_target.write_bytes(v1.canonical(v1.seal(checkpoint_value)) + b"\n")
    return v1.unknown_receipt(UNKNOWN_RESOURCE, detail, None,
                              preflight_monitor, checkpoint_target)


def run_full_v1_successor(args):
    v1 = load_live_v1()
    patch_v1_normalized_semantics(v1)
    # The authenticated v1 schedule remains the owner of the mathematical
    # search.  These subclasses replace only repeated dual-independent work.
    original_model = v1.AllSevenModel
    original_fibre_init = v1.FibreOracle.__init__
    original_canonical = v1.FibreOracle.canonical
    original_global = v1.FibreOracle.global_candidate
    original_translated = v1.translated_boundary
    original_boundary = v1.boundary_oracle
    original_init = v1.PositiveSearch.__init__
    original_add = v1.PositiveSearch.add_column
    original_write = v1.PositiveSearch.write_checkpoint
    original_body = v1.PositiveSearch._checkpoint_body
    original_materialize = v1.PositiveSearch.materialize_correction
    original_run = v1.PositiveSearch.run
    original_positive = v1.PositiveSearch.positive_receipt
    original_kernel_candidate = v1.FibreOracle.kernel_candidate

    class CachedModel(original_model):
        def __init__(self, runtime):
            super().__init__(runtime)
            self._v3_fox_cache = FoxTemplateCache(self, v1)

        def occurrence_data(self, relator_word, dual):
            return self._v3_fox_cache.occurrence_data(relator_word, dual)

        def occurrence_column(self, delta_word, relator_word):
            return self._v3_fox_cache.occurrence_column(delta_word,
                                                        relator_word)

        def direct_column(self, delta_word, relator_word):
            return self._v3_fox_cache.direct_column(delta_word, relator_word)

    v1.AllSevenModel = CachedModel

    def cached_boundary(runtime, dual, monitor):
        cache = runtime.get("_v3_boundary_cache")
        if cache is None:
            return original_boundary(runtime, dual, monitor)
        return cache.correlation(dual, monitor)

    def cached_translated(runtime, block, index, translation_blob):
        cache = runtime.get("_v3_boundary_cache")
        if cache is None:
            return original_translated(runtime, block, index, translation_blob)
        return cache.translated(block, index, translation_blob)

    v1.boundary_oracle = cached_boundary
    v1.translated_boundary = cached_translated

    def fibre_init(self, *values, **kwargs):
        original_fibre_init(self, *values, **kwargs)
        self._v3_values = CandidateValueCache(self.rt, v1)

    def cached_canonical(self, coordinate, target):
        if not hasattr(self, "_v3_values"):
            return original_canonical(self, coordinate, target)
        key = (getattr(self._v3_values, "basis_epoch", 0), coordinate, target)
        if key in self.cache:
            return self.cache[key]
        p176 = self.rt["p176"]
        amap = self.rt["A_maps"][f"S{coordinate}"]
        index = self._coarse_index(coordinate)
        candidates = []
        for (a,), gid in amap.items():
            section_target = p176.multiply_blob(
                p176.inverse_blob(a, coordinate, self.rt["e3"], self.rt["e4"]),
                target, coordinate, self.rt["e3"], self.rt["e4"])
            qid = index.lookup(section_target[:index.degree])
            if qid is None:
                continue
            section = self._v3_values.section(qid)
            if section[coordinate] != section_target:
                continue
            require(p176.multiply_blob(a, section[coordinate], coordinate,
                                       self.rt["e3"], self.rt["e4"]) == target,
                    "cached singleton packed target replay")
            value = self._v3_values.candidate(qid, gid)
            blobs = value["coordinate_blobs"]
            source_word = list(value["source_word"])
            require(blobs[coordinate] == target and
                    tuple(v1.coordinate_blobs(self.rt, source_word)) == blobs,
                    "cached singleton literal section witness")
            candidates.append((qid, gid, {"coordinate": coordinate,
                "target_hex": target.hex(), "q0_state_id": qid + 1,
                "gamma_state_id": gid + 1, "source_word": source_word,
                "gamma_source_word": list(value["gamma_source_word"]),
                "q0_source_word": list(value["q0_source_word"]),
                "q0_parent_path": copy.deepcopy(value["q0_parent_path"]),
                "coordinate_blobs": blobs,
                "section_blob_hex": list(value["section_blob_hex"]),
                "gamma_coordinate_blob_hex": value["gamma_coordinate_blobs_hex"][coordinate],
                "gamma_coordinate_blobs_hex": list(value["gamma_coordinate_blobs_hex"]),
                "selection": "least_qid_then_gid_coarse_inverse"}))
        answer = min(candidates, key=lambda item: (item[0], item[1]))[2] \
            if candidates else None
        self.cache[key] = answer
        return answer

    def cached_global(self, cursor):
        if not hasattr(self, "_v3_values"):
            return original_global(self, cursor)
        require(0 <= cursor < v1.DELTA_ORDER, "cached global roster cursor")
        self.monitor.bump("global_roster", 1, "weighted_global_prefix")
        qid, gid = divmod(cursor, 243)
        require(qid < len(self.rt["qstates"]) and
                gid < len(self.rt["projected"]), "cached global index range")
        value = self._v3_values.candidate(qid, gid)
        require(tuple(v1.coordinate_blobs(self.rt, value["source_word"])) ==
                value["coordinate_blobs"], "cached global literal replay")
        return {"source_word": list(value["source_word"]),
                "coordinate_blobs": value["coordinate_blobs"],
                "q0_state_id": qid + 1, "gamma_state_id": gid + 1,
                "gamma_source_word": list(value["gamma_source_word"]),
                "q0_source_word": list(value["q0_source_word"]),
                "q0_parent_path": copy.deepcopy(value["q0_parent_path"]),
                "gamma_coordinate_blobs_hex": list(value["gamma_coordinate_blobs_hex"]),
                "global_cursor": cursor}

    def cached_kernel_candidate(self, fibre, eta):
        """Multiply a kernel word while retaining the complete source witness."""
        answer = original_kernel_candidate(self, fibre, eta)
        require(isinstance(answer, dict) and
                all(field in fibre for field in
                    ("q0_state_id", "gamma_state_id", "q0_source_word",
                     "gamma_source_word", "q0_parent_path", "section_blob_hex",
                     "gamma_coordinate_blob_hex")),
                "kernel candidate provenance was stripped")
        kernel_word = list(eta["source_word"])
        source_word = list(reduce_word(kernel_word + fibre["source_word"]))
        require(answer.get("source_word") == source_word and
                tuple(v1.coordinate_blobs(self.rt, source_word)) ==
                tuple(answer.get("coordinate_blobs", ())),
                "cached kernel literal source replay")
        answer.update({
            "q0_source_word": list(fibre["q0_source_word"]),
            "gamma_source_word": list(fibre["gamma_source_word"]),
            "q0_parent_path": copy.deepcopy(fibre["q0_parent_path"]),
            "gamma_coordinate_blobs_hex": copy.deepcopy(
                fibre.get("gamma_coordinate_blobs_hex", [])),
            "kernel_word": kernel_word,
            "kernel_coordinate_blobs": [
                x.hex() if isinstance(x, bytes) else str(x)
                for x in eta["coordinate_blobs"]],
            "kernel_literal_replayed": True})
        return answer

    v1.FibreOracle.__init__ = fibre_init
    v1.FibreOracle.canonical = cached_canonical
    v1.FibreOracle.global_candidate = cached_global
    v1.FibreOracle.kernel_candidate = cached_kernel_candidate

    searches = []

    def init(self, *values, **kwargs):
        original_init(self, *values, **kwargs)
        resume_path = kwargs.get("resume")
        if resume_path is None and len(values) >= 5:
            resume_path = values[4]
        resume_history = None
        safe_chunk_end = 0
        if resume_path is not None:
            resume_doc = json.loads(Path(resume_path).read_text(encoding="utf-8"))
            resume_history = resume_doc.get("resume_monitor_history")
            require(isinstance(resume_history, dict) and
                    set(resume_history) == {"snapshot", "safe_chunk_end",
                                            "prior_repeated_suffix",
                                            "counter_fields", "limits_bound"} and
                    resume_history.get("counter_fields") ==
                    list(MONITOR_COUNTER_FIELDS) and
                    resume_history.get("limits_bound") is True,
                    "resume monitor history envelope")
            prior_suffix = resume_history.get("prior_repeated_suffix")
            if prior_suffix is not None:
                require(isinstance(prior_suffix, dict) and
                        set(prior_suffix) == {"declared", "safe_start",
                                              "interrupted_end", "attempts",
                                              "max_attempts", "replay_on_resume"},
                        "resume repeated suffix history")
            snapshot = resume_history.get("snapshot")
            validate_monitor_snapshot(snapshot)
            if snapshot["limits"] != self.monitor.limits:
                raise v1.InputStop("resume:monitor_limits")
            safe_chunk_end = resume_history.get("safe_chunk_end")
            require(type(safe_chunk_end) is int and safe_chunk_end >= 0,
                    "resume safe chunk end")
            if safe_chunk_end:
                chunk = resume_doc.get("v3_chunk")
                require(isinstance(chunk, dict) and
                        chunk.get("chunk_complete") is True and
                        chunk.get("repeated_suffix") is None and
                        chunk.get("chunk_end") == safe_chunk_end,
                        "resume safe chunk identity")
            # Counters are cumulative except checkpoint_bytes, which is a
            # serialized-size gauge.  The prior wall clock is history only;
            # this process starts a fresh wall-clock budget.
            for name in MONITOR_COUNTER_FIELDS:
                if name == "checkpoint_bytes":
                    self.monitor.counters[name] = int(snapshot["counters"][name])
                else:
                    self.monitor.counters[name] += int(snapshot["counters"][name])
                    if self.monitor.counters[name] > self.monitor.limits[name]:
                        raise v1.ResourceStop("resume_rebuild", name,
                                               self.monitor.counters[name],
                                               self.monitor.limits[name])
            self.monitor.phase = "resume_rebuild"
            self._v3_prior_monitor_elapsed_seconds = snapshot["elapsed_seconds"]
            self._v3_resume_monitor_history = copy.deepcopy(resume_history)
        boundary_cache = BoundaryDescriptorCache(self.rt, v1,
                                                  original_translated)
        self.rt["_v3_boundary_cache"] = boundary_cache
        digest = self.input_hash
        self.model._v3_fox_cache.bind_input(digest)
        self.fibres._v3_values.bind_input(digest)
        boundary_cache.bind_input(digest)
        self._v3_chunk_attempts = 0
        self._v3_total_attempts = int(safe_chunk_end)
        self._v3_chunk_start = int(safe_chunk_end)
        self._v3_last_attempt = False
        self._v3_force_checkpoint = False
        self._v3_resource_pending = False
        self._v3_checkpoint_repeated_suffix = None
        self._v3_chunk_override = None
        self._v3_safe_progress = copy.deepcopy(self.progress)
        self._v3_safe_total_attempts = int(safe_chunk_end)
        self._v3_safe_row_cursor = int(
            self.progress["correction"].get("canonical_row_cursor", 0))
        self._v3_cache_public = lambda: cache_public(self)
        searches.append(self)

    def cache_public(self):
        fox = self.model._v3_fox_cache
        # The Fox template and fixed-base stores share one bounded counter;
        # publish their aggregate residency rather than whichever store was
        # written last.
        fox.stats.bytes = int(fox.templates.used + fox.base.used)
        require(fox.templates.used <= fox.templates.max_bytes and
                fox.base.used <= fox.base.max_bytes and
                fox.stats.bytes <= fox.stats.max_bytes,
                "Fox cache split residency limits")
        caches = [fox.stats.public(),
                  self.fibres._v3_values.stats.public()]
        boundary = self.rt.get("_v3_boundary_cache")
        if boundary is not None:
            caches.append(boundary.stats.public())
        return {"caches": caches,
                "candidate_basis_epochs": [self.fibres._v3_values.basis_epoch],
                "hits": sum(item["hits"] for item in caches),
                "misses": sum(item["misses"] for item in caches),
                "evictions": sum(item["evictions"] for item in caches),
                "bytes": sum(item["bytes"] for item in caches),
                "regenerated_literals": sum(
                    item["regenerated_literals"] for item in caches),
                "bounded": True, "max_single_cache_bytes": max(
                    item["max_bytes"] for item in caches),
                "boundary_descriptors": (None if boundary is None else
                                         boundary.public_contract())}

    def validate_chunk_state(self):
        progress = self.progress.get("correction", {})
        cursor = progress.get("canonical_row_cursor")
        rows = progress.get("weighted_rows")
        require(type(cursor) is int and 0 <= cursor <= len(self.rt["roster"]),
                "cached canonical row cursor bounds")
        require(type(rows) is dict, "cached weighted row state")
        for index in range(1, cursor + 1):
            state = rows.get(str(index))
            require(isinstance(state, dict) and state.get("complete") is True,
                    "cached cursor crosses incomplete row")
        attempts = int(self._v3_chunk_attempts)
        require(0 <= attempts <= CACHE_CHUNK_LIMIT,
                "cached chunk attempt bound")

    def body(self, *values, **kwargs):
        self.validate_chunk_state()
        body = original_body(self, *values, **kwargs)
        current_total = int(self._v3_total_attempts)
        body["v3_cache_contract"] = {
            "schema": CACHED_SCHEMA, "semantics": CACHE_SEMANTICS,
            "semantics_digest": NORMALIZED_SEMANTICS_DIGEST,
            "callsites": list(NORMALIZED_SEMANTICS_CALLSITES),
            "key_fields": ["input_digest", "roster_layer", "roster_ordinal",
                           "literal_word", "slot", "group_type",
                           "basis_epoch",
                           "normalized_semantics_digest"],
            "bounded_memory": True, "chunk_limit": CACHE_CHUNK_LIMIT,
            "canonical_ordering": list(CACHE_ORDERING),
            "dual_dependent_recomputed": ["support_join", "mod3_merge",
                                           "weighted_formula", "exact_pairing"],
            "candidate_literal_direct_replay": True,
            "rank_zero_replay": True,
            "candidate_basis_epoch_invalidation": True}
        body["v3_cache_stats"] = cache_public(self)
        body["v3_epoch"] = {
            "input_sha256": body.get("input_sha256"),
            "target_sha256": body.get("target_sha256"),
            "normalized_semantics_digest": NORMALIZED_SEMANTICS_DIGEST,
            "dual_sha256": body.get("current_dual_sha256"),
            "dual_progress_sha256": body.get("progress", {}).get(
                "correction", {}).get("dual_sha256")}
        if self._v3_chunk_override is not None:
            body["v3_chunk"] = copy.deepcopy(self._v3_chunk_override)
        else:
            body["v3_chunk"] = {
                "chunk_start": int(self._v3_chunk_start),
                "chunk_end": current_total,
                "attempts_done": int(self._v3_chunk_attempts),
                "max_attempts": CACHE_CHUNK_LIMIT,
                "chunk_complete": bool(self._v3_force_checkpoint or
                                        not self._v3_last_attempt or
                                        self._v3_chunk_attempts >= CACHE_CHUNK_LIMIT or
                                        int(self.progress["correction"].get(
                                            "canonical_row_cursor", 0)) >
                                        int(self._v3_safe_row_cursor)),
                "canonical_row_cursor": int(self.progress["correction"].get(
                    "canonical_row_cursor", 0)),
                "canonical_ordering": list(CACHE_ORDERING),
                "repeated_suffix": self._v3_checkpoint_repeated_suffix}
        return body

    def write(self, *values, **kwargs):
        progress = self.progress.get("correction", {})
        row_advanced = int(progress.get("canonical_row_cursor", 0)) > \
            int(getattr(self, "_v3_safe_row_cursor", 0))
        safe = bool(self._v3_force_checkpoint or not self._v3_last_attempt or
                    self._v3_chunk_attempts >= CACHE_CHUNK_LIMIT or row_advanced)
        if not safe:
            return getattr(self, "_v3_last_checkpoint", {})
        pending = bool(getattr(self, "_v3_resource_pending", False))
        saved = None
        if pending:
            saved = (self.progress, self._v3_total_attempts,
                     self._v3_chunk_attempts, self._v3_chunk_start,
                     self._v3_checkpoint_repeated_suffix,
                     self._v3_chunk_override)
            current_total = int(self._v3_total_attempts)
            safe_total = int(self._v3_safe_total_attempts)
            self.progress = copy.deepcopy(self._v3_safe_progress)
            self._v3_total_attempts = safe_total
            self._v3_chunk_attempts = 0
            self._v3_chunk_start = safe_total
            self._v3_checkpoint_repeated_suffix = {
                "declared": current_total > safe_total,
                "safe_start": safe_total,
                "interrupted_end": current_total,
                "attempts": current_total - safe_total,
                "max_attempts": CACHE_CHUNK_LIMIT,
                "replay_on_resume": True}
            # The serialized checkpoint is the last safe *complete* chunk.
            # The interrupted suffix is metadata only; advertising it as the
            # completed chunk would turn a partial chunk into trusted state.
            self._v3_chunk_override = {
                "chunk_start": safe_total,
                "chunk_end": safe_total,
                "attempts_done": 0,
                "max_attempts": CACHE_CHUNK_LIMIT,
                "chunk_complete": True,
                "canonical_row_cursor": int(self.progress["correction"].get(
                    "canonical_row_cursor", 0)),
                "canonical_ordering": list(CACHE_ORDERING),
                "repeated_suffix": self._v3_checkpoint_repeated_suffix}
        try:
            checkpoint = original_write(self, *values, **kwargs)
        finally:
            if saved is not None:
                (self.progress, self._v3_total_attempts,
                 self._v3_chunk_attempts, self._v3_chunk_start,
                 self._v3_checkpoint_repeated_suffix,
                 self._v3_chunk_override) = saved
        self._v3_last_checkpoint = checkpoint
        if not pending:
            self._v3_safe_progress = copy.deepcopy(self.progress)
            self._v3_safe_total_attempts = int(self._v3_total_attempts)
            self._v3_safe_row_cursor = int(self.progress["correction"].get(
                "canonical_row_cursor", 0))
            self._v3_chunk_attempts = 0
            self._v3_chunk_start = int(self._v3_total_attempts)
        self._v3_last_attempt = False
        self._v3_force_checkpoint = False
        if pending:
            self._v3_resource_pending = False
        return checkpoint

    def add(self, row, provenance, dual=None):
        self._v3_force_checkpoint = True
        before_rank = len(self.basis.order)
        try:
            answer = original_add(self, row, provenance, dual)
            return answer
        except v1.ResourceStop:
            self._v3_resource_pending = True
            raise
        finally:
            if len(self.basis.order) != before_rank:
                self.fibres._v3_values.invalidate_basis()
                self.cache.clear()
            if not self._v3_resource_pending:
                self._v3_force_checkpoint = False

    def materialize(self, *values, **kwargs):
        try:
            answer = original_materialize(self, *values, **kwargs)
        except v1.ResourceStop:
            self._v3_last_attempt = False
            self._v3_resource_pending = True
            raise
        except Exception:
            self._v3_last_attempt = False
            raise
        self._v3_total_attempts += 1
        self._v3_chunk_attempts += 1
        self._v3_last_attempt = True
        return answer

    def run(self, *values, **kwargs):
        try:
            return original_run(self, *values, **kwargs)
        except v1.ResourceStop:
            self._v3_resource_pending = True
            self._v3_force_checkpoint = True
            raise

    def positive(self, solution):
        self._v3_force_checkpoint = True
        try:
            receipt = original_positive(self, solution)
            return attach_v2_positive(v1, self, receipt)
        except v1.ResourceStop:
            self._v3_resource_pending = True
            raise
        finally:
            if not self._v3_resource_pending:
                self._v3_force_checkpoint = False

    v1.PositiveSearch.__init__ = init
    v1.PositiveSearch.add_column = add
    v1.PositiveSearch.validate_chunk_state = validate_chunk_state
    v1.PositiveSearch._checkpoint_body = body
    v1.PositiveSearch.write_checkpoint = write
    v1.PositiveSearch.materialize_correction = materialize
    v1.PositiveSearch.run = run
    v1.PositiveSearch.positive_receipt = positive
    with tempfile.TemporaryDirectory(prefix="d972-r07-v2-") as temp:
        raw_output = Path(temp) / "receipt.json"
        argv = ["--mode", "PRODUCTION", "--output", str(raw_output),
                "--seconds", str(args.seconds), "--boundary-pairs", str(args.boundary_pairs),
                "--fibre-scans", str(args.fibre_scans), "--candidate-words", str(args.candidate_words),
                "--retained-columns", str(args.retained_columns),
                "--checkpoint-bytes", str(args.checkpoint_bytes), "--rss-bytes", str(args.rss_bytes),
                "--oracle-rounds", str(args.oracle_rounds)]
        resume_path = None
        resume_rebuild_metadata = {}
        resume_monitor_history = None
        preflight_receipt = None
        if args.resume:
            resume_raw = json.loads(args.resume.read_text(encoding="utf-8"))
            validate_cached_checkpoint(resume_raw)
            v1.validate_seal(resume_raw)
            resume_path = Path(temp) / "resume-v1.json"
            resume_raw = rank_zero_resume_checkpoint(v1, resume_raw)
            resume_rebuild_metadata = copy.deepcopy(
                resume_raw.get("resume_rebuild", {}))
            resume_monitor_history = copy.deepcopy(
                resume_raw.get("resume_monitor_history"))
            v1.validate_seal(resume_raw)
            resume_path.write_text(json.dumps(resume_raw, sort_keys=True,
                                               separators=(",", ":")) + "\n", encoding="utf-8")
            argv += ["--resume", str(resume_path)]
            preflight_receipt = resume_over_cap_preflight(
                v1, args, resume_raw, raw_output)
        if preflight_receipt is None:
            with contextlib.redirect_stdout(io.StringIO()):
                rc = v1.main(argv)
            if rc != 0 or not raw_output.is_file():
                raise RuntimeError("authenticated task179 successor stopped without receipt")
            receipt = json.loads(raw_output.read_text(encoding="utf-8"))
        else:
            receipt = preflight_receipt
        # Preserve the authenticated v1 monitor snapshot produced by the
        # actual ResourceStop handler; the checker binds this byte-for-byte
        # instead of accepting a freshly constructed post-stop budget.
        if str(receipt.get("terminal", "")).startswith(UNKNOWN_RESOURCE + ":"):
            monitor_snapshot = receipt.get("monitor")
            require(isinstance(monitor_snapshot, dict),
                    "resource stop missing live monitor snapshot")
            receipt["resource_monitor_snapshot"] = copy.deepcopy(monitor_snapshot)
        checkpoint = raw_output.with_suffix(raw_output.suffix + ".checkpoint.json")
        if str(receipt.get("terminal", "")).startswith(UNKNOWN_RESOURCE + ":") and \
                not checkpoint.is_file():
            raise RuntimeError("resource stop has no resumable checkpoint")
        if checkpoint.is_file():
            checkpoint_value = json.loads(checkpoint.read_text(encoding="utf-8"))
            checkpoint_value["schema"] = SCHEMA
            checkpoint_value["normalized_semantics"] = CACHE_SEMANTICS
            checkpoint_value["normalized_semantics_digest"] = NORMALIZED_SEMANTICS_DIGEST
            checkpoint_value["normalized_semantics_callsites"] = list(NORMALIZED_SEMANTICS_CALLSITES)
            checkpoint_value["v3_cache_contract"] = {
                "schema": CACHED_SCHEMA, "semantics": CACHE_SEMANTICS,
                "semantics_digest": NORMALIZED_SEMANTICS_DIGEST,
                "callsites": list(NORMALIZED_SEMANTICS_CALLSITES),
                "key_fields": ["input_digest", "roster_layer", "roster_ordinal",
                               "literal_word", "slot", "group_type",
                               "basis_epoch",
                               "normalized_semantics_digest"],
                "chunk_limit": CACHE_CHUNK_LIMIT,
                "canonical_ordering": list(CACHE_ORDERING),
                "bounded_memory": True,
                "rank_zero_replay": True,
                "dual_dependent_recomputed": ["support_join", "mod3_merge",
                                               "weighted_formula", "exact_pairing"],
                "candidate_literal_direct_replay": True,
                "candidate_basis_epoch_invalidation": True}
            checkpoint_value["v3_epoch"] = {
                "input_sha256": checkpoint_value.get("input_sha256"),
                "target_sha256": checkpoint_value.get("target_sha256"),
                "normalized_semantics_digest": NORMALIZED_SEMANTICS_DIGEST,
                "dual_sha256": checkpoint_value.get("current_dual_sha256"),
                "dual_progress_sha256": checkpoint_value.get("progress", {}).get(
                    "correction", {}).get("dual_sha256")}
            checkpoint_value.setdefault("v3_chunk", {
                "chunk_start": 0, "chunk_end": 0, "attempts_done": 0,
                "max_attempts": CACHE_CHUNK_LIMIT, "chunk_complete": True,
                "canonical_row_cursor": 0,
                "canonical_ordering": list(CACHE_ORDERING),
                "repeated_suffix": None})
            if args.resume is not None:
                prior_rebuild = (resume_rebuild_metadata or
                                 checkpoint_value.get("resume_rebuild", {}))
                checkpoint_value["resume_rebuild"] = {
                    "rank_zero_replayed": True,
                    "stored_pivots_discarded": True,
                    "stored_reduced_target_discarded": True,
                    "stored_current_dual_discarded": True,
                    "stored_oracle_progress_discarded": bool(
                        prior_rebuild.get("stored_oracle_progress_discarded", True)),
                    "stored_state_fields_discarded": list(RESUME_DISCARDED_STATE_FIELDS),
                    "column_provenance_authenticated": True,
                    "stored_columns_replayed_from_zero": True,
                    "rank_zero_replay_source": "authenticated columns/provenance",
                    "v3_cache_and_chunk_state_discarded": True,
                    "safe_progress_preserved": bool(
                        prior_rebuild.get("safe_progress_preserved", False)),
                    "safe_boundary_preserved": bool(
                        prior_rebuild.get("safe_boundary_preserved", False)),
                    "safe_chunk_replayed_without_suffix": bool(
                        prior_rebuild.get("safe_chunk_replayed_without_suffix", False)),
                    "monitor_limits_bound": prior_rebuild.get(
                        "monitor_limits_bound") is True,
                    "monitor_counters_carried_forward": prior_rebuild.get(
                        "monitor_counters_carried_forward") is True,
                    "prior_monitor_elapsed_seconds": prior_rebuild.get(
                        "prior_monitor_elapsed_seconds", 0),
                    "safe_chunk_end_recovered": int(prior_rebuild.get(
                        "safe_chunk_end_recovered", 0))}
                if resume_monitor_history is not None:
                    checkpoint_value["resume_monitor_history"] = copy.deepcopy(
                        resume_monitor_history)
            checkpoint_value = v1.seal(checkpoint_value)
            args.output.with_suffix(args.output.suffix + ".checkpoint.json").write_text(
                json.dumps(checkpoint_value, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8")
    receipt["schema"] = SCHEMA
    active_search = searches[0] if searches else None
    if str(receipt.get("terminal", "")).startswith(UNKNOWN_INPUT + ":"):
        receipt["reason"] = str(receipt["terminal"])[len(UNKNOWN_INPUT) + 1:]
    receipt["v2_schedule"] = {"source": "authenticated task179 full schedule",
                               "fresh_run_default": args.resume is None,
                               "resume_replayed_from_rank_zero": args.resume is not None,
                               "old_pivot_state_reused": False,
                               "normalized_columns": True,
                               "cache_accelerated": True,
                               "chunk_limit": CACHE_CHUNK_LIMIT}
    receipt["cached_schedule"] = {
        "schema": CACHED_SCHEMA, "semantics": CACHE_SEMANTICS,
        "semantics_digest": NORMALIZED_SEMANTICS_DIGEST,
        "callsites": list(NORMALIZED_SEMANTICS_CALLSITES),
        "proof_pins": {label: list(value)
                       for label, value in PROOF_PINS.items()},
        "fixed_chunk_attempts": CACHE_CHUNK_LIMIT,
        "canonical_ordering": list(CACHE_ORDERING),
        "dual_independent_templates": True,
        "eleven_slot_fox_templates": True,
        "three_fixed_base_gradients": True,
        "complete_pb3_pb4_descriptors": True,
        "boundary_descriptor_roster": True,
        "candidate_value_cache_bounded": True,
        "candidate_basis_epoch_invalidation": True,
        "same_completed_schedule_as_v2": True}
    receipt["v3_cache_stats"] = ({"status": "not_started"} if active_search is None
                                  else cache_public(active_search))
    checkpoint_path = args.output.with_suffix(args.output.suffix + ".checkpoint.json")
    if checkpoint_path.is_file():
        checkpoint_raw = checkpoint_path.read_bytes()
        receipt["checkpoint"] = {"path": checkpoint_path.name,
                                 "bytes": len(checkpoint_raw),
                                 "sha256": sha256_bytes(checkpoint_raw)}
    receipt.pop("self_digest", None)
    return v1.seal(receipt)


def production_path_selftest(v1):
    """Exercise the v3 hook and the real v1 search state transitions cheaply."""
    normalized = v1.exponent_pair([1] * 18)
    require(normalized == (1, 0), "production SELFTEST normalized hook")
    row = {v1.exponent_key(1): normalized[0]}
    target = dict(row)

    class IdentityQuotient:
        """Typed joint-element identity used by the live v1 model methods."""
        def __init__(self, degree):
            require(degree in (36, 144), "production SELFTEST quotient degree")
            self.degree = degree
            self.identity = (bytes(range(degree)),
                             bytes({36: 4, 144: 10}[degree]))

        def eval(self, word):
            del word
            return self.identity

        def mul(self, left, right):
            require(left == self.identity and right == self.identity,
                    "production SELFTEST identity multiplication")
            return self.identity

        def inverse(self, value):
            require(value == self.identity,
                    "production SELFTEST identity inversion")
            return self.identity

    class MiniP176:
        """Independent minimal implementation of task176's typed blob ABI."""
        COORDINATE_WIDTHS = [40] * 5 + [154] * 5

        @staticmethod
        def packed_joint_blob(value, label):
            if type(value) is not tuple or len(value) != 2:
                raise TypeError(label + " must be a two-component tuple")
            permutation, pc_value = value
            if type(permutation) not in (bytes, tuple):
                raise TypeError(label + " permutation must be bytes or tuple")
            if type(permutation) is tuple and not all(type(x) is int for x in permutation):
                raise TypeError(label + " tuple permutation entries must be integers")
            if type(pc_value) is not bytes:
                raise TypeError(label + " PC component must be bytes")
            degree = len(permutation)
            expected_pc_width = {36: 4, 144: 10}.get(degree)
            if expected_pc_width is None or len(pc_value) != expected_pc_width:
                raise ValueError(label + " unsupported degree/PC width")
            packed = bytes(permutation)
            if len(packed) != degree or set(packed) != set(range(degree)):
                raise ValueError(label + " permutation is not bijective")
            return packed + pc_value

        @staticmethod
        def blob(old, value):
            del old
            return MiniP176.packed_joint_blob(
                value, "task186 SELFTEST typed element")

        @classmethod
        def value_from_blob(cls, raw, index):
            if type(raw) is not bytes:
                raise TypeError("production SELFTEST section blob must be bytes")
            degree = 36 if index < 5 else 144
            width = {36: 4, 144: 10}[degree]
            if len(raw) != degree + width:
                raise ValueError("production SELFTEST section blob width")
            permutation = raw[:degree]
            pc_value = raw[degree:]
            cls.packed_joint_blob((permutation, pc_value),
                                  "production SELFTEST decoded element")
            return permutation, pc_value

        @classmethod
        def multiply_blob(cls, left, right, index, e3, e4):
            group = e3 if index < 5 else e4
            return cls.blob(None, group.mul(cls.value_from_blob(left, index),
                                            cls.value_from_blob(right, index)))

        @classmethod
        def inverse_blob(cls, raw, index, e3, e4):
            group = e3 if index < 5 else e4
            return cls.blob(None, group.inverse(cls.value_from_blob(raw, index)))

    class EmptyFox:
        def hexagon_words(self, word):
            return [[], []]
        def embed_f2_pb3(self, word):
            return list(word)
        def f2_substitute(self, word, left, right):
            return []
        def inv_word(self, word):
            return inverse_word(word)
        def fox_gradient_without_sections(self, word, quotient):
            return {}, quotient.identity
        def translate_vector(self, row, value, quotient):
            return dict(row)

    # Call the authenticated AllSevenModel methods themselves on an empty
    # typed quotient: this keeps the occurrence/direct E-key path load-bearing
    # without running the full six-thousand-word production universe twice.
    model = object.__new__(v1.AllSevenModel)
    model.e3 = IdentityQuotient(36); model.e4 = IdentityQuotient(144)
    model.rt = {"joint_group": IdentityQuotient(36),
                "p176": MiniP176()}; model.old = EmptyFox(); model.g = []
    model.specs = [{"block": 1, "coordinate": index, "quotient": model.e3,
                    "left": [], "right": [], "sign": 1, "lift": False,
                    "occurrence_prefix": (), "base_factor": []}
                   for index in range(6)] + [
                    {"block": 3, "coordinate": index, "quotient": model.e4,
                     "left": [], "right": [], "sign": 1, "lift": False,
                     "occurrence_prefix": (), "base_factor": []}
                    for index in range(5)]
    model.pcontexts = [([], [])] * 5
    p176 = model.rt["p176"]
    for index, quotient, expected_width in ((0, model.e3, 40),
                                             (5, model.e4, 154)):
        packed = p176.packed_joint_blob(quotient.identity,
                                        "task186 SELFTEST typed element")
        require(len(packed) == expected_width and
                p176.value_from_blob(packed, index) == quotient.identity and
                p176.blob(None, quotient.identity) == packed and
                p176.multiply_blob(packed, packed, index, model.e3, model.e4) == packed and
                p176.inverse_blob(packed, index, model.e3, model.e4) == packed,
                "production SELFTEST typed blob roundtrip")
    occurrence = v1.AllSevenModel.occurrence_column(model, [], [1] * 18)
    direct, direct_trace = v1.AllSevenModel.direct_column(model, [], [1] * 18)
    require(occurrence == row and direct == occurrence and
            direct_trace.get("direct_all_seven_replay") is True,
            "production SELFTEST AllSeven occurrence/direct path")

    class ToyMonitor:
        def __init__(self):
            self.counters = {"retained_columns": 0}
        def bump(self, name, amount=1, phase=None):
            self.counters[name] = self.counters.get(name, 0) + amount

    # Invoke the live PositiveSearch.add_column on a one-column normalized
    # space, then recover its coefficient and ancestry from the real Echelon.
    added = object.__new__(v1.PositiveSearch)
    added.basis = v1.Echelon(); added.columns = []; added.target = target
    added.monitor = ToyMonitor(); added.progress = {"correction": {"dual_sha256": None}}
    added.write_checkpoint = lambda *args, **kwargs: {"toy": True}
    v1.PositiveSearch.add_column(added, row,
                                {"family": "correction", "conjugate_word": [1] * 18})
    remainder, coefficients = added.basis.reduce(target)
    require(not remainder and coefficients == {1: 1} and
            added.basis.ancestry[added.basis.order[0]] == {1: 1},
            "production SELFTEST coefficient/ancestry")

    # Convert a sealed rank-one v2-shaped checkpoint through the same rank-zero
    # resume firewall used by production.  The incoming pivot/reduced-target/
    # progress fields are deliberately decoys; the converter authenticates
    # provenance and emits a fresh v1-compatible transcript.
    provenance = {"family": "correction", "delta_word": [],
                  "relator_word": [1] * 18, "conjugate_word": [1] * 18,
                  "delta_coordinate_blobs_hex": [], "corrected_word": [],
                  "quotient_value_blobs": [], "eleven_occurrence_replay": True,
                  "direct_all_seven_replay": True}
    record = {"column_id": 1, "family": "correction", "provenance": provenance,
              "sparse_row": v1.public_sparse(row),
              "sparse_row_sha256": v1.sha_obj(v1.public_sparse(row)),
              "pivot_hex": "OLD", "rank_before": 99, "rank_after": 100,
              "pivot_ancestry": [[99, 2]]}
    selftest_monitor = {
        "phase": "selftest_checkpoint", "elapsed_seconds": 0.0,
        "rss_bytes": 0, "single_process": True,
        "limits": {"wall_seconds": 10.0, "boundary_pairs": 256,
                    "fibre_scans": 256, "candidate_words": 256,
                    "retained_columns": 256, "checkpoint_bytes": 4096,
                    "rss_bytes": 1024 * 1024, "oracle_rounds": 256,
                    "global_roster": DELTA_ORDER},
        "counters": {name: 0 for name in MONITOR_COUNTER_FIELDS}}
    incoming = v1.seal({"schema": SCHEMA,
        "normalized_semantics": CACHE_SEMANTICS,
        "normalized_semantics_digest": NORMALIZED_SEMANTICS_DIGEST,
        "normalized_semantics_callsites": list(NORMALIZED_SEMANTICS_CALLSITES),
        "v3_cache_contract": {
            "schema": SCHEMA, "semantics": CACHE_SEMANTICS,
            "semantics_digest": NORMALIZED_SEMANTICS_DIGEST,
            "callsites": list(NORMALIZED_SEMANTICS_CALLSITES),
            "key_fields": ["input_digest", "roster_layer", "roster_ordinal",
                           "literal_word", "slot", "group_type",
                           "basis_epoch",
                           "normalized_semantics_digest"],
            "chunk_limit": CACHE_CHUNK_LIMIT,
            "canonical_ordering": list(CACHE_ORDERING),
            "bounded_memory": True, "rank_zero_replay": True,
            "dual_dependent_recomputed": ["support_join", "mod3_merge",
                                           "weighted_formula", "exact_pairing"],
            "candidate_literal_direct_replay": True,
            "candidate_basis_epoch_invalidation": True},
        "v3_cache_stats": {"bounded": True, "hits": 0, "misses": 0,
                            "evictions": 0, "bytes": 0,
                            "regenerated_literals": 0},
        "v3_epoch": {"input_sha256": v1.sha_obj({}),
                      "target_sha256": v1.sha_obj(v1.public_sparse(target)),
                      "normalized_semantics_digest": NORMALIZED_SEMANTICS_DIGEST,
                      "dual_sha256": None,
                      "dual_progress_sha256": None},
        "v3_chunk": {"chunk_start": 0, "chunk_end": 4,
                      "attempts_done": 4, "max_attempts": CACHE_CHUNK_LIMIT,
                      "chunk_complete": True,
                      "canonical_row_cursor": 0,
                      "canonical_ordering": list(CACHE_ORDERING),
                      "repeated_suffix": None},
        "input_components": {}, "input_sha256": v1.sha_obj({}),
        "target": v1.public_sparse(target),
        "target_sha256": v1.sha_obj(v1.public_sparse(target)),
        "columns": [record], "rank": 100, "pivot_order": ["OLD"],
        "reduced_target": [["OLD", 1]], "current_dual": None,
        "current_dual_sha256": None, "target_solution_if_zero": [],
        "progress": {"boundary": {"dual_sha256": None, "complete": True,
                                    "pair_attempts": 0, "restart_pair_cursor": 0},
                     "correction": {"dual_sha256": None,
                                    "canonical_row_cursor": 0,
                                    "weighted_rows": {}}},
        "coarse_inverse_index": {"stale": True}, "monitor": selftest_monitor})
    converted = rank_zero_resume_checkpoint(v1, incoming)
    require(converted["resume_rebuild"]["rank_zero_replayed"] is True and
            converted["resume_rebuild"]["stored_pivots_discarded"] is True and
            converted["resume_rebuild"]["stored_reduced_target_discarded"] is True and
            converted["resume_rebuild"]["stored_current_dual_discarded"] is True and
            converted["resume_rebuild"]["stored_oracle_progress_discarded"] is False and
            converted["resume_rebuild"]["safe_progress_preserved"] is True and
            converted["resume_rebuild"]["safe_boundary_preserved"] is True and
            converted["resume_rebuild"]["safe_chunk_end_recovered"] == 4 and
            converted["v3_chunk"]["chunk_end"] == 4 and
            converted["v3_chunk"]["repeated_suffix"] is None and
            converted["resume_monitor_history"]["safe_chunk_end"] == 4 and
            converted["progress"]["correction"]["canonical_row_cursor"] == 0 and
            converted["progress"]["correction"]["weighted_rows"] == {} and
            converted["columns"][0]["rank_before"] == 0 and
            converted["columns"][0]["rank_after"] == 1,
            "production SELFTEST rank-zero conversion")

    # Feed the converted checkpoint to the actual v1 loader on a fresh,
    # empty basis.  The loader now verifies the converter's fresh transition;
    # it cannot reuse the incoming OLD pivot/progress state.
    replay = object.__new__(v1.PositiveSearch)
    replay.basis = v1.Echelon(); replay.columns = []; replay.target = target
    replay.input_hash = converted["input_sha256"]; replay.progress = {}
    replay.kernel_orders = []
    # Keep the authenticated v1 source-rebuild path live: the synthetic
    # record is replayed through AllSevenModel.direct_column, rather than
    # accepting its serialized sparse row as a substitute for provenance.
    replay.rt = {"roster": []}; replay.model = model
    checkpoint = converted
    with tempfile.TemporaryDirectory(prefix="d972-r07-v2-rank0-") as temp:
        path = Path(temp) / "checkpoint.json"
        path.write_bytes(v1.canonical(checkpoint) + b"\n")
        v1.PositiveSearch.load_checkpoint(replay, path)
    remainder, recovered = replay.basis.reduce(target)
    require(not remainder and recovered == {1: 1} and len(replay.basis.order) == 1,
            "production SELFTEST rank-zero checkpoint replay")
    # Drive the actual pre-v1 over-cap firewall: the converted safe checkpoint
    # is sealed to the expected path and the typed UNKNOWN_RESOURCE retains a
    # resumable checkpoint even though PositiveSearch is never assigned.
    overcap_doc = copy.deepcopy(converted)
    overcap_snapshot = overcap_doc["resume_monitor_history"]["snapshot"]
    overcap_snapshot["limits"]["candidate_words"] = 1
    overcap_snapshot["counters"]["candidate_words"] = 2
    overcap_doc["resume_monitor_history"]["snapshot"] = overcap_snapshot
    overcap_doc = v1.seal(overcap_doc)
    overcap_args = argparse.Namespace(
        seconds=10.0, boundary_pairs=256, fibre_scans=256,
        candidate_words=1, retained_columns=256, checkpoint_bytes=4096,
        rss_bytes=1024 * 1024, oracle_rounds=256)
    with tempfile.TemporaryDirectory(prefix="d972-r07-overcap-") as temp:
        overcap_output = Path(temp) / "receipt.json"
        overcap_receipt = resume_over_cap_preflight(
            v1, overcap_args, overcap_doc, overcap_output)
        require(overcap_receipt["terminal"] ==
                "UNKNOWN_RESOURCE:phase=resume_rebuild:cap=candidate_words:value=2:limit=1" and
                overcap_receipt["checkpoint"] is not None and
                overcap_receipt["monitor"]["counters"]["candidate_words"] == 2,
                "production SELFTEST over-cap resume terminal")
        overcap_checkpoint = Path(temp) / "receipt.json.checkpoint.json"
        require(overcap_checkpoint.is_file(),
                "production SELFTEST over-cap checkpoint path")
        overcap_value = json.loads(overcap_checkpoint.read_text(encoding="utf-8"))
        require(overcap_value["monitor"]["counters"]["candidate_words"] == 2 and
                overcap_value["resume_monitor_history"]["safe_chunk_end"] == 4,
                "production SELFTEST over-cap checkpoint payload")
        overcap_trace = {"typed_resource_terminal": overcap_receipt["terminal"],
                         "checkpoint_written_before_search_assignment": True,
                         "safe_chunk_end": overcap_value["resume_monitor_history"][
                             "safe_chunk_end"],
                         "carried_candidate_words": overcap_value["monitor"][
                             "counters"]["candidate_words"]}
    return {"occurrence_direct_hook": True, "actual_allseven_occurrence": True,
            "actual_allseven_direct": True, "normalized_E1": 1,
            "raw_E1": 0, "positive_add_column": True,
             "coefficient_recovery": [[1, 1]], "basis_ancestry": [[1, 1]],
             "rank_zero_checkpoint_rebuild": True,
             "rank_zero_conversion": True,
             "stored_pivots_discarded": True,
             "over_cap_resume_preflight": overcap_trace}


CACHE_MUTATIONS = (
    "cache_key_component", "stale_group_type", "slot_sign_order",
    "fox_term", "prefix_inverse", "boundary_descriptor",
    "dual_support_decode", "section_parent_letter", "typed_coordinate_blob",
    "cache_hit_without_literal", "chunk_end_advanced", "incomplete_row_complete",
    "skipped_resume_candidate", "stale_dual_progress", "raw_mod3_semantics",
    "old_pivot_reuse", "coefficient_two_repetition", "exactification_cube",
    "resource_stop_terminal_change",
)


def _cached_toy_fixture(v1):
    fixture = {"generators": [[1, 0, 2], [0, 2, 1]]}
    # Every relation is literal identity in the bounded S3 fixture.  The
    # distinct conjugators keep the source words noncommutative while the
    # occurrence rows remain small enough for every chunk interruption.
    candidates = []
    for index, delta in enumerate(([], [1], [2], [1, 2]), 1):
        row, occurrences = v1.toy_occurrence_column(
            fixture, delta, [1] * 18)
        candidates.append({"index": index, "delta": list(delta),
                           "word": [1] * 18,
                           "row": row, "occurrences": occurrences,
                           "formula": {"K": sum(row.values()) % 3,
                                       "terms": [[key.hex(), value]
                                                 for key, value in sorted(row.items())],
                                       "eleven": len(occurrences)}})
    return fixture, candidates


def _cached_toy_schedule(v1, use_cache):
    fixture, candidates = _cached_toy_fixture(v1)
    stats = CacheStats("selftest_cached_values", 1 << 20)
    cache = BoundedCache("selftest_cached_values", 1 << 20, stats)
    basis = v1.Echelon(); active = []; attempted = []
    for candidate in candidates:
        key = ("selftest-input", CACHE_SEMANTICS,
               NORMALIZED_SEMANTICS_DIGEST, "E3", candidate["index"],
               tuple(candidate["word"]))
        value = cache.get(key) if use_cache else None
        if value is None:
            if use_cache:
                value = {"row": dict(candidate["row"]),
                         "formula": copy.deepcopy(candidate["formula"]),
                         "word": tuple(candidate["word"]),
                         "literal_replayed": True}
                cache.put(key, value)
            else:
                value = {"row": dict(candidate["row"]),
                         "formula": copy.deepcopy(candidate["formula"]),
                         "word": tuple(candidate["word"]),
                         "literal_replayed": True}
        require(value["literal_replayed"] is True and
                value["row"] == candidate["row"] and
                value["formula"] == candidate["formula"],
                "cached toy literal value")
        attempted.append(candidate["index"])
        added, pivot, ancestry = basis.add(value["row"], candidate["index"])
        if added:
            active.append({"index": candidate["index"],
                           "pivot": pivot.hex(),
                           "ancestry": [[key, item] for key, item in
                                         sorted(ancestry.items())],
                           "formula": value["formula"]})
    require(active, "cached toy active transcript")
    target = {}
    coefficients = {}
    for position, item in enumerate(active, 1):
        coefficient = 2 if position == 2 else 1
        coefficients[item["index"]] = coefficient
        add_sparse(target, candidates[item["index"] - 1]["row"], coefficient)
    replay_basis = v1.Echelon()
    for item in active:
        replay_basis.add(candidates[item["index"] - 1]["row"], item["index"])
    remainder, recovered = replay_basis.reduce(target)
    require(not remainder and recovered == coefficients,
            "cached toy target solution")
    selected_words = []
    for item in active:
        source = list(candidates[item["index"] - 1]["word"])
        selected_words.append(source if coefficients[item["index"]] == 1
                             else list(inverse_word(source)))
    correction_word = []
    for source in selected_words:
        correction_word = list(reduce_word(correction_word + source))
    direct_row = v1.toy_fox(correction_word,
                            [tuple(row) for row in fixture["generators"]], 2)
    # Registered exactification is tied to the same literal correction: the
    # triple repeat forces the toy exponent pair into the 54-lattice while
    # retaining a bounded noncommutative word transcript.
    c_star = multiply(correction_word, correction_word, correction_word)
    exact = exactify(c_star, [2] * 36,
                     [1] * 18 + [2] * 144,
                     [-1] * 18 + [-2] * 54)
    exact_direct = v1.toy_fox(exact["c_exact"],
                              [tuple(row) for row in fixture["generators"]], 2)
    return {"attempted_candidates": attempted,
            "weighted_formulas": [item["formula"] for item in active],
            "active_columns": [item["index"] for item in active],
            "rank_pivot_ancestry": active,
            "rank": len(replay_basis.order),
            "pivot_order": [key.hex() for key in replay_basis.order],
            "target": [[key.hex(), value] for key, value in sorted(target.items())],
            "solution": [[key, value] for key, value in sorted(coefficients.items())],
            "correction_word": correction_word,
            "direct_all_seven_replay": {
                "row": [[key.hex(), value] for key, value in sorted(direct_row.items())],
                "literal": True, "fixture_group": "S3"},
            "c_exact": list(exact["c_exact"]),
            "c_exact_direct_replay": {
                "row": [[key.hex(), value] for key, value in
                        sorted(exact_direct.items())],
                "literal": True, "fixture_group": "S3"},
            "terminal": "CACHED_TOY_COMPLETE",
            "resource_counters": {"logical_attempts": len(attempted),
                                  "cache_hits": stats.hits if use_cache else 0,
                                  "cache_misses": stats.misses if use_cache else 0},
            "cache_stats": stats.public() if use_cache else {
                "name": "uncached_reference", "hits": 0, "misses": 0,
                "evictions": 0, "bytes": 0, "max_bytes": 0,
            "regenerated_literals": len(candidates)}}


def _cached_toy_rank_zero_resume(v1, candidates, stop, expected):
    """Replay one interrupted toy prefix from a rank-zero column transcript.

    The prefix is a sealed complete chunk.  Its active columns are the only
    durable payload; a fresh echelon replays those columns and then consumes
    only the unsealed canonical suffix.  This is the same no-skip/suffix rule
    used by the production checkpoint
    wrapper, exercised on an actual sparse basis rather than a boolean flag.
    """
    partial = v1.Echelon(); retained = []
    for candidate in candidates[:stop]:
        added, pivot, ancestry = partial.add(
            candidate["row"], candidate["index"])
        if added:
            retained.append({"index": candidate["index"],
                             "row": dict(candidate["row"]),
                             "pivot": pivot,
                             "ancestry": dict(ancestry)})
    rebuilt = v1.Echelon()
    for record in retained:
        added, pivot, ancestry = rebuilt.add(record["row"], record["index"])
        require(added and pivot == record["pivot"] and
                ancestry == record["ancestry"],
                "cached toy rank-zero column replay")
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
            [key.hex() for key in rebuilt.order] == expected["pivot_order"],
            "cached toy resumed transcript")
    resumed_word = []
    for index, coefficient in sorted(expected_solution.items()):
        source = list(candidates[index - 1]["word"])
        resumed_word = list(reduce_word(resumed_word +
                            (source if coefficient == 1 else
                             list(inverse_word(source)))))
    resumed_direct = v1.toy_fox(
        resumed_word, [tuple(row) for row in
                       {"generators": [[1, 0, 2], [0, 2, 1]]}["generators"]], 2)
    resumed_exact = exactify(multiply(resumed_word, resumed_word, resumed_word),
                             [2] * 36, [1] * 18 + [2] * 144,
                             [-1] * 18 + [-2] * 54)
    resumed_exact_direct = v1.toy_fox(
        resumed_exact["c_exact"],
        [tuple(row) for row in ((1, 0, 2), (0, 2, 1))], 2)
    require(resumed_word == expected["correction_word"] and
            [[key.hex(), value] for key, value in sorted(resumed_direct.items())] ==
            expected["direct_all_seven_replay"]["row"],
            "cached toy resumed literal/direct transcript")
    require(list(resumed_exact["c_exact"]) == expected["c_exact"] and
            [[key.hex(), value] for key, value in
             sorted(resumed_exact_direct.items())] ==
            expected["c_exact_direct_replay"]["row"],
            "cached toy resumed c_exact transcript")
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
            "final_rank": len(rebuilt.order),
            "final_solution": [[key, value]
                                for key, value in sorted(solution.items())],
            "correction_word": resumed_word,
            "c_exact": list(resumed_exact["c_exact"]),
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


def _cached_toy_mutation_state(v1):
    reference = _cached_toy_schedule(v1, True)
    return {"cache_key": ["selftest-input", CACHE_SEMANTICS,
                           NORMALIZED_SEMANTICS_DIGEST, "E3", 1,
                           [1] * 18],
            "group_type": "E3", "slot_order": list(range(1, 12)),
            "fox_term": ["0100", 1], "prefix_inverse": "00",
            "boundary_descriptor": {"block": 1, "relator_index": 1,
                                     "component": 1, "h_blob": "00",
                                     "h_inverse": "00", "base_coefficient": 1},
            "dual_support_decode": [["5201", 1]],
            "section_parent_letter": {"parent": [0, 1], "letter": [1, 2]},
            "typed_coordinate_blob": "00", "cache_hit_literal": True,
            "chunk_start": 0, "chunk_end": 4, "attempts_done": 4,
            "chunk_complete": True, "resume_order": [1, 2, 3, 4],
            "dual_progress_digest": NORMALIZED_SEMANTICS_DIGEST,
            "raw_mod3": False, "old_pivots_discarded": True,
            "coefficient": 2, "coefficient_inverse_row": True,
            "cube": -3,
            "resource_terminal": "UNKNOWN_RESOURCE:phase=positive_correction_dovetail:"
                                "cap=oracle_rounds:value=2:limit=1",
            "reference": reference}


def _validate_cached_toy_mutation(v1, state):
    reference = _cached_toy_schedule(v1, True)
    require(state["cache_key"] == ["selftest-input", CACHE_SEMANTICS,
                                    NORMALIZED_SEMANTICS_DIGEST, "E3", 1,
                                    [1] * 18], "cache key binding")
    require(state["group_type"] == "E3" and
            state["slot_order"] == list(range(1, 12)), "cache slot ABI")
    require(state["fox_term"] == ["0100", 1] and
            state["prefix_inverse"] == "00", "cached Fox prefix replay")
    require(state["boundary_descriptor"] == {
        "block": 1, "relator_index": 1, "component": 1,
        "h_blob": "00", "h_inverse": "00", "base_coefficient": 1},
            "cached boundary descriptor replay")
    require(state["dual_support_decode"] == [["5201", 1]] and
            state["section_parent_letter"] == {
                "parent": [0, 1], "letter": [1, 2]},
            "cached typed support/section replay")
    require(state["typed_coordinate_blob"] == "00" and
            state["cache_hit_literal"] is True, "cached typed literal replay")
    require(state["chunk_start"] == 0 and state["chunk_end"] == 4 and
            state["attempts_done"] == 4 and state["chunk_complete"] is True,
            "cached complete chunk boundary")
    require(state["resume_order"] == [1, 2, 3, 4],
            "cached resume candidate order")
    require(state["dual_progress_digest"] == NORMALIZED_SEMANTICS_DIGEST and
            state["raw_mod3"] is False and
            state["old_pivots_discarded"] is True,
            "cached dual/rank-zero firewall")
    require(state["coefficient"] == 2 and
            state["coefficient_inverse_row"] is True,
            "cached coefficient-two inverse replay")
    fixture, candidates = _cached_toy_fixture(v1)
    selected = candidates[1]
    conjugate = reduce_word(list(selected["delta"]) + selected["word"] +
                            list(inverse_word(selected["delta"])))
    direct = v1.toy_fox(conjugate,
                        [tuple(row) for row in fixture["generators"]], 2)
    inverse_direct = v1.toy_fox(list(inverse_word(conjugate)),
                                [tuple(row) for row in fixture["generators"]], 2)
    require(inverse_direct == v1.scaled(direct, -1),
            "cached coefficient-two literal inverse word replay")
    exact = exactify(tuple([1] * 54 + [2] * 54), tuple([2] * 36),
                     tuple([1] * 18 + [2] * 144),
                     tuple([-1] * 18 + [-2] * 54))
    require(state["cube"] == -3 and exponent(exact["c_exact"]) == (0, 0),
            "cached exactification cube replay")
    require(state["resource_terminal"].startswith(
        "UNKNOWN_RESOURCE:phase=positive_correction_dovetail:"),
            "cached typed resource terminal")
    require(reference["active_columns"] == state["reference"]["active_columns"] and
            reference["solution"] == state["reference"]["solution"] and
            reference["direct_all_seven_replay"] ==
            state["reference"]["direct_all_seven_replay"],
            "cached load-bearing schedule transcript")


def cached_schedule_selftest(v1):
    reference = _cached_toy_schedule(v1, False)
    cached = _cached_toy_schedule(v1, True)
    for field in ("attempted_candidates", "weighted_formulas", "active_columns",
                  "rank_pivot_ancestry", "rank", "pivot_order", "target",
                  "solution", "correction_word", "direct_all_seven_replay",
                  "c_exact", "c_exact_direct_replay"):
        require(reference[field] == cached[field],
                "cached/uncached schedule mismatch:" + field)
    fixture, candidates = _cached_toy_fixture(v1)
    # Bind the returned fixture to the actual arithmetic that produced the
    # candidate transcript.  This catches a stale/dead local rename as well
    # as a receipt-only fixture label.
    fixture_row, fixture_occurrences = v1.toy_occurrence_column(
        fixture, candidates[0]["delta"], candidates[0]["word"])
    require(fixture_row == candidates[0]["row"] and
            fixture_occurrences == candidates[0]["occurrences"],
            "cached toy fixture arithmetic binding")
    resume_checks = []
    for stop in range(1, 5):
        check = _cached_toy_rank_zero_resume(v1, candidates, stop, cached)
        require(check["physical_attempts"][-4:] ==
                cached["attempted_candidates"] and
                check["canonical_attempts"] == cached["attempted_candidates"] and
                check["resumed_attempts"] == list(range(stop + 1, 5)),
                "cached chunk resume skipped candidate")
        require(check["correction_word"] == cached["correction_word"] and
                check["c_exact"] == cached["c_exact"] and
                check["direct_all_seven_replay"] ==
                cached["direct_all_seven_replay"] and
                check["c_exact_direct_replay"] ==
                cached["c_exact_direct_replay"] and
                check["terminal"] == cached["terminal"] and
                check["resource_counters"] == cached["resource_counters"],
                "cached toy resumed output mismatch")
        require(check["safe_chunk_end"] == stop and
                check["safe_chunk_end"] > 0 and
                check["safe_prefix_attempts"] == list(range(1, stop + 1)) and
                check["replayed_suffix_attempts"] == list(range(stop + 1, 5)) and
                check["safe_chunk_replayed_without_suffix"] is True and
                check["prior_resource_counters"] == check["resource_counters"] and
                check["resource_counters_monotone"] is True,
                "cached safe prefix/counter carry-forward")
        resume_checks.append(check)
    probe_stats = CacheStats("selftest_eviction_probe", 120)
    probe = BoundedCache("selftest_eviction_probe", 120, probe_stats)
    probe.put(("literal", 1), {"row": [1, 2, 3]})
    require(probe.get(("literal", 1)) is not None,
            "cached production-shaped hit probe")
    probe.put(("literal", 2), {"row": [4, 5, 6, 7, 8]})
    require(probe_stats.hits == 1 and probe_stats.evictions > 0 and
            probe_stats.regenerated_literals == 2,
            "cached production-shaped eviction probe")
    resource_probe = None
    try:
        raise v1.ResourceStop("selftest_chunk", "candidate_words", 2, 1)
    except v1.ResourceStop as exc:
        resource_probe = {
            "phase": exc.phase, "cap": exc.cap,
            "value": exc.value, "limit": exc.limit}
    # Exercise the production candidate-cache class itself: a retained-rank
    # epoch change must clear every prior candidate value.
    epoch_cache = CandidateValueCache({"projected": [()] * 243}, v1)
    epoch_cache.bind_input("selftest-input")
    epoch_key = epoch_cache._key("candidate", 0, 0)
    epoch_cache.cache.put(epoch_key, {"literal_replayed": True})
    epoch_before = epoch_cache.cache.get(epoch_key) is not None
    old_epoch = epoch_cache.basis_epoch
    epoch_cache.invalidate_basis()
    epoch_after = epoch_cache.cache.get(epoch_key) is None
    candidate_epoch_probe = {"before_hit": epoch_before,
                             "old_epoch": old_epoch,
                             "new_epoch": epoch_cache.basis_epoch,
                             "after_invalidation_miss": epoch_after}
    split_stats = CacheStats("selftest_shared_fox_limits", 96 * 1024 * 1024)
    split_templates = BoundedCache("selftest_templates", 88 * 1024 * 1024,
                                   split_stats)
    split_base = BoundedCache("selftest_base", 8 * 1024 * 1024, split_stats)
    split_templates.put(("template", 1), {"literal": b"template"})
    split_base.put(("base", 1), {"literal": b"base"})
    split_limits = {"template_used": split_templates.used,
                    "base_used": split_base.used,
                    "template_limit": split_templates.max_bytes,
                    "base_limit": split_base.max_bytes,
                    "aggregate_used": split_templates.used + split_base.used,
                    "aggregate_limit": 96 * 1024 * 1024}
    require(split_limits["template_used"] <= split_limits["template_limit"] and
            split_limits["base_used"] <= split_limits["base_limit"] and
            split_limits["aggregate_used"] <= split_limits["aggregate_limit"],
            "shared Fox cache split limits")
    # Run the exact legacy v1 dispatch predicate against the three provenance
    # shapes: only canonical selector records may expose section_blob_hex.
    legacy_selector_dispatch = {
        "canonical_selector": bool({"section_blob_hex": ["00"],
                                     "selection": "least"}.get(
                                         "section_blob_hex")),
        "global_candidate": bool({"global_cursor": 0}.get("section_blob_hex")),
        "kernel_candidate": bool({"kernel_word": [1]}.get("section_blob_hex"))}
    require(legacy_selector_dispatch == {
        "canonical_selector": True, "global_candidate": False,
        "kernel_candidate": False}, "legacy selector dispatch predicate")
    state = _cached_toy_mutation_state(v1)
    state["reference"] = cached
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
        "resource_stop_terminal_change": lambda s: s.__setitem__(
            "resource_terminal", CACHED_COMMON),
    }
    rejected = []
    for name in CACHE_MUTATIONS:
        mutated = copy.deepcopy(state); mutators[name](mutated)
        try:
            _validate_cached_toy_mutation(v1, mutated)
        except RuntimeError:
            rejected.append(name)
    require(tuple(rejected) == CACHE_MUTATIONS,
            "cached semantic mutation controls")
    return {"reference": reference, "cached": cached,
            "chunk_limit": CACHE_CHUNK_LIMIT,
            "fixture": {"noncommutative": True, "generators": fixture["generators"]},
            "resume_checks": resume_checks,
            "cache_equivalence": True,
            "cache_probe": probe_stats.public(),
            "candidate_epoch_probe": candidate_epoch_probe,
            "split_shared_limit_probe": split_limits,
            "legacy_selector_dispatch": legacy_selector_dispatch,
            "resource_stop_probe": resource_probe,
            "mutation_controls": {"attempted": len(CACHE_MUTATIONS),
                                   "rejected": len(rejected),
                                   "names": list(CACHE_MUTATIONS),
                                   "validator": "load_bearing_cached_schedule_replay"}}


def run_full_selftest():
    """Retain the real v1 bounded Fox/echelon fixture inside the v2 receipt."""
    v1 = load_live_v1()
    original_pair = v1.exponent_pair
    v1._v2_selftest_nonomega = True
    patched_pair = patch_v1_normalized_semantics(v1)
    # Fatal regression guard: this is the actual authenticated v1 exponent
    # hook, not a side matrix.  E=(1,0) for an 18-exponent kernel word.
    require(patched_pair([1] * 18) == (1, 0),
            "patched v1 exponent callsite remained raw-vacuous")
    require(v1.exponent_key(1) == b"E\x01" and v1.exponent_key(2) == b"E\x02",
            "authenticated v1 exponent keys changed")
    toy_input = {"generators": [[1, 0, 2], [0, 2, 1]]}
    normalized_row, _ = v1.toy_occurrence_column(toy_input, [], [1] * 18)
    require(normalized_row.get(v1.exponent_key(1)) == 1,
            "actual v1 occurrence column lacks normalized E1")
    v1.exponent_pair = original_pair
    raw_row, _ = v1.toy_occurrence_column(toy_input, [], [1] * 18)
    require(v1.exponent_key(1) not in raw_row and v1.exponent_key(2) not in raw_row,
            "raw v1 occurrence control is not vacuous")
    v1.exponent_pair = patched_pair
    with tempfile.TemporaryDirectory(prefix="d972-r07-v2-selftest-") as temp:
        path = Path(temp) / "receipt.json"
        with contextlib.redirect_stdout(io.StringIO()):
            rc = v1.main(["--mode", "SELFTEST", "--output", str(path)])
        if rc != 0 or not path.is_file():
            raise RuntimeError("authenticated task179 SELFTEST failed")
        task179 = json.loads(path.read_text(encoding="utf-8"))
    production_trace = production_path_selftest(v1)
    result = toy_selftest(v1)
    result["cached_schedule_selftest"] = cached_schedule_selftest(v1)
    result["cache_mutation_controls"] = result["cached_schedule_selftest"][
        "mutation_controls"]
    del v1._v2_selftest_nonomega
    v1.exponent_pair = original_pair
    result["load_bearing_normalization"] = {
        "patched_v1_exponent_pair": True,
        "integer_signed_counter": True,
        "kernel_word": [1] * 18,
        "actual_E_keys": ["4501", "4502"],
        "actual_E1_E2": [1, 0],
        "actual_occurrence_column": True,
        "raw_mod3_control": [0, 0]}
    result["production_path_selftest"] = production_trace
    result["task179_selftest"] = task179
    result["full_v1_schedule_selftest"] = True
    return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), default="SELFTEST")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--seconds", type=float, default=19800.0)
    parser.add_argument("--boundary-pairs", type=int, default=8000000)
    parser.add_argument("--fibre-scans", type=int, default=80000000)
    parser.add_argument("--candidate-words", type=int, default=2000000)
    parser.add_argument("--retained-columns", type=int, default=250000)
    parser.add_argument("--checkpoint-bytes", type=int, default=4000000000)
    parser.add_argument("--rss-bytes", type=int, default=5700000000)
    parser.add_argument("--oracle-rounds", type=int, default=1)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        args.mode = "SELFTEST"
    output = args.output or args.receipt
    if output is None:
        parser.error("--output is required")
    output = output if output.is_absolute() else ROOT / output
    if args.mode == "SELFTEST":
        result = run_full_selftest()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                          encoding="utf-8")
        print(result["terminal"], flush=True)
        return 0
    args.output = output
    result = run_full_v1_successor(args)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    print("R07_NORMALIZED_EXACT_CACHED_COLGEN_V3_PRODUCER_TERMINAL " +
          str(result["terminal"]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
