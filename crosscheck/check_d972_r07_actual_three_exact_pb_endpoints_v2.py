#!/usr/bin/env python3
"""Independent checker for task292 exact PB endpoints v2.

This module imports no producer/helper module.  Its Artin evaluator acts on
one free-basis word at a time, rather than maintaining the producer's tuple
and composing it by tuple substitution.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-actual-three-exact-pb-endpoints/v2"
FIXTURE_SCHEMA = SCHEMA + "/selftest-fixture"
VERDICT_SCHEMA = SCHEMA + "/verdict"
ZERO = "R07_THREE_EXACT_PB_ENDPOINTS_ZERO"
NONZERO = "R07_THREE_EXACT_PB_ENDPOINTS_NONZERO"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
FIXTURE = "search/certs/d972_r07_actual_three_exact_pb_endpoints_selftest_v2_20260828.json"
PRODUCTION_BLOCK_REASON = (
    "task285 accepted MEMBER/M ABI unavailable; "
    "a future accepted ABI requires a new explicit binding version"
)
FORBIDDEN_CONCLUSIONS = {
    "A8_boundary_extracted": False,
    "A9_lift": False,
    "mixed_prime": False,
    "perfect_core": False,
    "fake": False,
    "Ihara": False,
}
BLOCKS = ("H1", "H2", "P")
RANK = {"H1": 3, "H2": 3, "P": 4}
MUTATIONS = [
    "source_word", "pair_order", "coefficient", "block", "position", "type",
    "rho", "sign", "prefix", "inverse_slot", "xi", "epsilon",
    "artin_factor_order", "normal_form", "bucket_deletion", "M_digest",
    "upstream_seal", "full_C1_row", "terminal", "resource_terminal",
    "checkpoint_owner",
]
GATES = {
    "source_word": "source word gate", "pair_order": "pair order gate",
    "coefficient": "coefficient gate", "block": "block gate",
    "position": "position gate", "type": "type gate", "rho": "rho gate",
    "sign": "sign gate", "prefix": "prefix gate",
    "inverse_slot": "inverse slot gate", "xi": "xi gate",
    "epsilon": "epsilon gate", "artin_factor_order": "Artin factor order gate",
    "normal_form": "normal form gate", "bucket_deletion": "bucket collection gate",
    "M_digest": "M digest gate", "upstream_seal": "upstream seal gate",
    "full_C1_row": "full-C1 row gate", "terminal": "terminal gate",
    "resource_terminal": "resource terminal gate",
    "checkpoint_owner": "checkpoint owner gate",
}


class CheckStop(RuntimeError):
    pass


class MutationAccepted(RuntimeError):
    pass


class CheckerResource(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int, limit: int):
        super().__init__(phase)
        self.phase, self.cap, self.value, self.limit = phase, cap, value, limit


class CheckerBudget:
    caps = {"input_bytes": 2_100_000_000, "artin_letters": 80_000_000,
            "word_letters": 80_000_000, "sparse_terms": 20_000_000,
            "wall_seconds": 21600}

    def __init__(self) -> None:
        self.used = {key: 0 for key in self.caps}
        self.started = time.monotonic()

    def bump(self, cap: str, amount: int, phase: str) -> None:
        self.used[cap] += amount
        self.used["wall_seconds"] = max(
            self.used["wall_seconds"], int(time.monotonic() - self.started))
        if self.used[cap] > self.caps[cap]:
            raise CheckerResource(phase, cap, self.used[cap], self.caps[cap])
        if self.used["wall_seconds"] > self.caps["wall_seconds"]:
            raise CheckerResource(phase, "wall_seconds", self.used["wall_seconds"],
                                  self.caps["wall_seconds"])


CHECK_BUDGET: CheckerBudget | None = None


def meter(cap: str, amount: int, phase: str) -> None:
    if CHECK_BUDGET is not None:
        CHECK_BUDGET.bump(cap, amount, phase)


def need(ok: bool, reason: str) -> None:
    if ok is not True:
        raise CheckStop(reason)


def packed(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def hexdigest(value: object) -> str:
    return hashlib.sha256(packed(value)).hexdigest()


def check_seal(value: dict) -> None:
    need(type(value) is dict and type(value.get("self_digest_sha256")) is str,
         "receipt seal gate")
    body = dict(value)
    claimed = body.pop("self_digest_sha256")
    need(claimed == hexdigest(body), "receipt seal gate")


def cancel(word: list[int], width: int | None = None) -> list[int]:
    result: list[int] = []
    for letter in word:
        need(type(letter) is int and letter != 0, "word gate")
        if width is not None:
            need(abs(letter) <= width, "word width gate")
        if result and result[-1] + letter == 0:
            result.pop()
        else:
            result.append(letter)
    return result


def reverse_inverse(word: list[int]) -> list[int]:
    return [-value for value in word[::-1]]


def replace_letters(word: list[int], images: list[list[int]], width: int | None = None) -> list[int]:
    expanded: list[int] = []
    for letter in word:
        pos = abs(letter) - 1
        need(0 <= pos < len(images), "substitution gate")
        image = images[pos]
        expanded += image if letter > 0 else reverse_inverse(image)
    return cancel(expanded, width)


def pure_pairs(strands: int) -> list[list[int]]:
    return [[a, b] for a in range(1, strands) for b in range(a + 1, strands + 1)]


def pure_number(strands: int, pair: list[int]) -> int:
    need(pair in pure_pairs(strands), "pure pair gate")
    return pure_pairs(strands).index(pair) + 1


def pure_to_artin(a: int, b: int) -> list[int]:
    need(1 <= a < b, "pure factor gate")
    going = list(range(b - 1, a, -1))
    return going + [a, a] + [-j for j in range(a + 1, b)]


def sigma_substitution(strands: int, sigma: int) -> dict[int, list[int]]:
    i = abs(sigma)
    need(1 <= i < strands, "Artin sigma gate")
    table = {j: [j] for j in range(1, strands + 1)}
    if sigma > 0:
        table[i], table[i + 1] = [i, i + 1, -i], [i]
    else:
        table[i], table[i + 1] = [i + 1], [-(i + 1), i, i + 1]
    return table


def push_one_sigma(free_word: list[int], strands: int, sigma: int) -> list[int]:
    table = sigma_substitution(strands, sigma)
    output: list[int] = []
    for letter in free_word:
        image = table[abs(letter)]
        output += image if letter > 0 else reverse_inverse(image)
    return cancel(output, strands)


def expand_pb(strands: int, pb_word: list[int]) -> list[int]:
    pairs = pure_pairs(strands)
    output: list[int] = []
    for letter in pb_word:
        need(1 <= abs(letter) <= len(pairs), "PB width gate")
        factor = pure_to_artin(*pairs[abs(letter) - 1])
        output += factor if letter > 0 else reverse_inverse(factor)
    return output


ARTIN_CACHE: dict[tuple[int, tuple[int, ...]], tuple[tuple[int, ...], ...]] = {}


def exact_key(strands: int, pb_word: list[int]) -> tuple[tuple[int, ...], ...]:
    reduced = cancel(pb_word, len(pure_pairs(strands)))
    cache_key = (strands, tuple(reduced))
    if cache_key not in ARTIN_CACHE:
        braid_word = expand_pb(strands, reduced)
        meter("artin_letters", len(braid_word), "checker Artin action")
        basis_images = []
        for basis in range(1, strands + 1):
            image = [basis]
            for sigma in braid_word:
                image = push_one_sigma(image, strands, sigma)
                meter("word_letters", len(image), "checker Artin image")
            basis_images.append(tuple(image))
        ARTIN_CACHE[cache_key] = tuple(basis_images)
    return ARTIN_CACHE[cache_key]


def braid_basis_images(strands: int, braid_word: list[int]) -> list[list[int]]:
    answer = []
    for basis in range(1, strands + 1):
        image = [basis]
        for sigma in braid_word:
            image = push_one_sigma(image, strands, sigma)
        answer.append(image)
    return answer


def presentation_relators(strands: int) -> list[list[int]]:
    if strands == 2:
        return []
    inherited_pairs = pure_pairs(strands - 1)
    inclusion = [[pure_number(strands, pair)] for pair in inherited_pairs]
    relators = [replace_letters(row, inclusion) for row in
                presentation_relators(strands - 1)]
    kernel = [[pure_number(strands, [j, strands])] for j in range(1, strands)]
    for pair in inherited_pairs:
        conjugator = pure_number(strands, pair)
        action = braid_basis_images(strands - 1, pure_to_artin(*pair))
        for j in range(1, strands):
            target = pure_number(strands, [j, strands])
            transported = replace_letters(action[j - 1], kernel)
            relators.append(cancel([-conjugator, target, conjugator] +
                                    reverse_inverse(transported)))
    return relators


def substitute_two(word: list[int], rho: dict, width: int) -> list[int]:
    return replace_letters(word, [rho["x"], rho["y"]], width)


def collect_group(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    meter("sparse_terms", len(rows), "checker group collection")
    table: dict[tuple[tuple[int, ...], ...], dict] = {}
    for index, row in enumerate(rows, 1):
        key = tuple(tuple(part) for part in row["full_artin_key"])
        if key not in table:
            table[key] = {"full_artin_key": row["full_artin_key"],
                          "representative_word": row["free_reduced_word"],
                          "integer_sum": 0, "contributors": []}
        table[key]["integer_sum"] += row["coefficient"]
        table[key]["contributors"].append({"term_index": index,
            "coefficient": row["coefficient"], "origin": row["origin"]})
    kept, deleted = [], []
    for key in sorted(table, key=repr):
        row = table[key]
        row["coefficient_mod_3"] = row["integer_sum"] % 3
        (kept if row["coefficient_mod_3"] else deleted).append(row)
    return kept, deleted


def collect_chain(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    meter("sparse_terms", len(rows), "checker chain collection")
    table: dict[tuple[int, tuple[tuple[int, ...], ...]], dict] = {}
    for index, row in enumerate(rows, 1):
        signature = tuple(tuple(part) for part in row["full_artin_key"])
        key = (row["component"], signature)
        if key not in table:
            table[key] = {"component": row["component"],
                          "full_artin_key": row["full_artin_key"],
                          "representative_word": row["free_reduced_group_word"],
                          "integer_sum": 0, "contributors": []}
        table[key]["integer_sum"] += row["coefficient"]
        table[key]["contributors"].append({"term_index": index,
            "coefficient": row["coefficient"], "origin": row["origin"]})
    kept, deleted = [], []
    for key in sorted(table, key=repr):
        row = table[key]
        row["coefficient_mod_3"] = row["integer_sum"] % 3
        (kept if row["coefficient_mod_3"] else deleted).append(row)
    return kept, deleted


def fox_expand(sources: list[dict], strands: int, owner: dict) -> list[dict]:
    width = len(pure_pairs(strands))
    result = []
    for source_index, source in enumerate(sources, 1):
        coeff = source["coefficient"]
        left = cancel(source["left_word"], width)
        cursor: list[int] = []
        for word_index, letter in enumerate(source["fox_word"], 1):
            need(1 <= abs(letter) <= width, "Fox source word gate")
            if letter > 0:
                group = left + cursor
                component, local = letter, 1
                cursor = cancel(cursor + [letter], width)
            else:
                cursor = cancel(cursor + [letter], width)
                group = left + cursor
                component, local = -letter, -1
            reduced = cancel(group, width)
            result.append({"component": component, "coefficient": coeff * local,
                "unreduced_group_word": group, "free_reduced_group_word": reduced,
                "full_artin_key": [list(part) for part in exact_key(strands, reduced)],
                "origin": dict(owner, source_index=source_index,
                    fox_letter_index=word_index,
                    source_provenance=source.get("provenance"))})
    return result


def boundary_one(chain: list[dict], strands: int, phase: str) -> list[dict]:
    result = []
    for index, term in enumerate(chain, 1):
        for slot, word, sign in (
                ("gx", term["unreduced_group_word"] + [term["component"]], 1),
                ("g", term["unreduced_group_word"], -1)):
            reduced = cancel(word, len(pure_pairs(strands)))
            result.append({"coefficient": term["coefficient"] * sign,
                "unreduced_word": word, "free_reduced_word": reduced,
                "full_artin_key": [list(part) for part in exact_key(strands, reduced)],
                "origin": {"kind": phase, "chain_term": index,
                    "endpoint_slot": slot, "chain_origin": term["origin"]}})
    return result


def collect_m(terms: list[dict]) -> dict:
    normalized, table = [], {}
    for index, term in enumerate(terms, 1):
        left, right = cancel(term["U"], 2), cancel(term["V"], 2)
        row = {"input_index": index, "coefficient": term["coefficient"],
               "U": left, "V": right, "ancestry": term.get("ancestry")}
        normalized.append(row)
        key = (tuple(left), tuple(right))
        if key not in table:
            table[key] = {"U": left, "V": right, "integer_sum": 0,
                          "input_indices": [], "ancestry": []}
        table[key]["integer_sum"] += term["coefficient"]
        table[key]["input_indices"].append(index)
        table[key]["ancestry"].append(term.get("ancestry"))
    collected, deleted = [], []
    for key in sorted(table):
        row = table[key]
        row["coefficient"] = row["integer_sum"] % 3
        (collected if row["coefficient"] else deleted).append(row)
    immutable = {"modulus": 3, "ordered_pair_convention": "U_minus_V",
                 "terms": [{"coefficient": row["coefficient"], "U": row["U"],
                            "V": row["V"], "ancestry": row["ancestry"]}
                           for row in collected]}
    return {"precollection_terms": normalized, "collected_terms": collected,
            "zero_deletions": deleted, "immutable_payload": immutable,
            "immutable_digest_sha256": hexdigest(immutable)}


def check_roster(rows: list[dict]) -> None:
    need(len(rows) == 11, "position gate")
    blocks = ["H1"] * 3 + ["H2"] * 3 + ["P"] * 5
    positions = [1, 2, 3, 1, 2, 3, 1, 2, 3, 5, 4]
    types = ["E3"] * 6 + ["E4"] * 5
    for index, row in enumerate(rows):
        need(row["ordinal"] == index + 1, "position gate")
        need(row["block"] == blocks[index], "block gate")
        need(row["position"] == positions[index], "position gate")
        need(row["type"] == types[index], "type gate")
        need(row["rank"] == RANK[blocks[index]], "type gate")
    need([row["ordinal"] for row in rows if row.get("repeated_e3_key") == "E3_xy"] ==
         [1, 5], "position gate")
    need([(row["type"], row["ordinal"]) for row in rows
          if row.get("registry_label") == "C21"] ==
         [("E3", 1), ("E3", 5), ("E4", 9)], "type gate")


def occurrence_replay(literal: dict) -> list[dict]:
    rows = copy.deepcopy(literal["occurrences"])
    check_roster(rows)
    output = []
    for row in rows:
        strands = row["rank"]
        width = len(pure_pairs(strands))
        row["rho"] = {"x": cancel(row["rho"]["x"], width),
                      "y": cancel(row["rho"]["y"], width)}
        row["prefix_word"] = cancel(row["prefix_word"], width)
        row["P_word"] = row["prefix_word"]
        chain = fox_expand(row["d_sources"], strands,
                           {"kind": "occurrence_d", "ordinal": row["ordinal"]})
        xi_raw = boundary_one(chain, strands, "xi")
        xi, deleted = collect_group(xi_raw)
        row["d_chain_uncollected"] = chain
        row["xi_unreduced_terms"] = xi_raw
        row["xi_terms"] = xi
        row["xi_zero_deletions"] = deleted
        output.append(row)
    return output


def endpoint_replay(block: str, occurrences: list[dict], m: dict,
                    epsilon_raw: list[dict]) -> dict:
    strands, width = RANK[block], len(pure_pairs(RANK[block]))
    raw = copy.deepcopy(epsilon_raw)
    for occurrence in occurrences:
        if occurrence["block"] != block:
            continue
        for m_index, mterm in enumerate(m["collected_terms"], 1):
            for side, word, side_sign in (("U", mterm["U"], 1),
                                          ("V", mterm["V"], -1)):
                value = substitute_two(word, occurrence["rho"], width)
                for xi_index, xi in enumerate(occurrence["xi_terms"], 1):
                    unreduced = occurrence["prefix_word"] + value + xi["representative_word"]
                    reduced = cancel(unreduced, width)
                    raw.append({"coefficient": -occurrence["sigma"] *
                                mterm["coefficient"] * side_sign *
                                xi["coefficient_mod_3"],
                        "unreduced_word": unreduced, "free_reduced_word": reduced,
                        "full_artin_key": [list(part) for part in exact_key(strands, reduced)],
                        "origin": {"kind": "minus_M_star_xi", "block": block,
                            "occurrence_ordinal": occurrence["ordinal"],
                            "position": occurrence["position"], "type": occurrence["type"],
                            "registry_label": occurrence["registry_label"],
                            "sigma": occurrence["sigma"],
                            "prefix_word": occurrence["prefix_word"],
                            "inverse_slot": occurrence["inverse_slot"],
                            "rho": occurrence["rho"], "M_term": m_index,
                            "pair_side": side, "pair_side_sign": side_sign,
                            "source_F2_word": word,
                            "rho_evaluated_word": value,
                            "xi_term": xi_index}})
    buckets, deleted = collect_group(raw)
    return {"unreduced_terms": raw, "buckets": buckets,
            "zero_deletions": deleted, "zero": not buckets}


def c1_replay(block: str, occurrences: list[dict], m: dict,
              epsilon_chain: list[dict]) -> dict:
    strands, width = RANK[block], len(pure_pairs(RANK[block]))
    raw = [dict(row, origin=dict(row["origin"], z_source="epsilon"))
           for row in epsilon_chain]
    for occurrence in occurrences:
        if occurrence["block"] != block:
            continue
        for m_index, mterm in enumerate(m["collected_terms"], 1):
            for side, word, side_sign in (("U", mterm["U"], 1),
                                          ("V", mterm["V"], -1)):
                value = substitute_two(word, occurrence["rho"], width)
                for d_index, dterm in enumerate(occurrence["d_chain_uncollected"], 1):
                    unreduced = (occurrence["prefix_word"] + value +
                                 dterm["unreduced_group_word"])
                    reduced = cancel(unreduced, width)
                    raw.append({"component": dterm["component"],
                        "coefficient": -occurrence["sigma"] *
                                       mterm["coefficient"] * side_sign *
                                       dterm["coefficient"],
                        "unreduced_group_word": unreduced,
                        "free_reduced_group_word": reduced,
                        "full_artin_key": [list(part) for part in exact_key(strands, reduced)],
                        "origin": {"kind": "minus_M_star_d", "block": block,
                            "occurrence_ordinal": occurrence["ordinal"],
                            "position": occurrence["position"], "type": occurrence["type"],
                            "registry_label": occurrence["registry_label"],
                            "sigma": occurrence["sigma"],
                            "prefix_word": occurrence["prefix_word"],
                            "inverse_slot": occurrence["inverse_slot"],
                            "rho": occurrence["rho"], "M_term": m_index,
                            "pair_side": side, "pair_side_sign": side_sign,
                            "source_F2_word": word,
                            "rho_evaluated_word": value,
                            "d_term": d_index}})
    support, deletions = collect_chain(raw)
    replay_chain = [{"component": row["component"],
        "coefficient": row["coefficient_mod_3"],
        "unreduced_group_word": row["representative_word"],
        "free_reduced_group_word": row["representative_word"],
        "full_artin_key": row["full_artin_key"],
        "origin": {"kind": "collected_z", "contributors": row["contributors"]}}
        for row in support]
    boundary = boundary_one(replay_chain, strands, "D1_z")
    buckets, d1_deleted = collect_group(boundary)
    return {"z_uncollected_terms": raw, "z_finite_support": support,
            "z_zero_deletions": deletions, "D1_z_unreduced_terms": boundary,
            "D1_z_buckets": buckets, "D1_z_zero_deletions": d1_deleted,
            "D1_z_zero": not buckets,
            "complete_presentation": "PB" + str(strands)}


def presentation(strands: int) -> dict:
    identity = tuple((j,) for j in range(1, strands + 1))
    rows = []
    for index, relator in enumerate(presentation_relators(strands), 1):
        key = exact_key(strands, relator)
        need(key == identity, "presentation identity gate")
        fox_row = fox_expand(
            [{"coefficient": 1, "left_word": [], "fox_word": relator,
              "provenance": "complete_PB_presentation_relator"}],
            strands, {"kind": "D2_relator", "relator_index": index})
        d1d2_terms = boundary_one(fox_row, strands, "D1_D2_relator")
        d1d2_buckets, d1d2_deletions = collect_group(d1d2_terms)
        need(not d1d2_buckets, "presentation D1D2 gate")
        rows.append({"index": index, "relator": relator,
                     "expanded_artin_word": expand_pb(strands, relator),
                     "full_artin_key": [list(part) for part in key],
                     "identity": True, "D2_fox_row": fox_row,
                     "D1_D2_unreduced_terms": d1d2_terms,
                     "D1_D2_buckets": d1d2_buckets,
                     "D1_D2_zero_deletions": d1d2_deletions,
                     "D1_D2_zero": True})
    need(len(rows) == (2 if strands == 3 else 11), "presentation roster gate")
    return {"group": "PB" + str(strands), "generator_pairs": pure_pairs(strands),
            "relator_count": len(rows), "relators": rows,
            "complete_fixed_roster": True}


def replay_literal(literal: dict) -> dict:
    m = collect_m(literal["M_terms"])
    occurrences = occurrence_replay(literal)
    epsilon_chains, epsilon, endpoints = {}, {}, {}
    for block in BLOCKS:
        chain = fox_expand(literal["epsilon_sources"][block], RANK[block],
                           {"kind": "epsilon", "block": block})
        raw = boundary_one(chain, RANK[block], "epsilon")
        buckets, deleted = collect_group(raw)
        epsilon_chains[block] = chain
        epsilon[block] = {"unreduced_terms": raw, "buckets": buckets,
                          "zero_deletions": deleted}
        endpoints[block] = endpoint_replay(block, occurrences, m, raw)
    first = next((block for block in BLOCKS if endpoints[block]["buckets"]), None)
    terminal = ZERO if first is None else NONZERO + " block=" + first
    full = {"performed": first is None,
            "presentation_boundary_quotient": "complete_fixed_PB_presentation",
            "q_B_extracted": False, "blocks": {}}
    if first is None:
        for block in BLOCKS:
            full["blocks"][block] = c1_replay(block, occurrences, m,
                                               epsilon_chains[block])
            need(full["blocks"][block]["D1_z_zero"], "full-C1 replay gate")
    else:
        full["reason"] = "endpoint obstruction in " + first
    ledger_keys = ("ordinal", "block", "position", "type", "registry_label",
                   "repeated_e3_key", "rank", "sigma", "prefix_word",
                   "inverse_slot", "orientation", "rho", "P_word")
    return {"terminal": terminal, "M": m, "occurrences": occurrences,
            "occurrence_ledger": [{key: row[key] for key in ledger_keys}
                                  for row in occurrences],
            "epsilon_chains": epsilon_chains, "epsilon": epsilon,
            "endpoints": endpoints, "full_C1_replay": full,
            "complete_presentations": {"PB3": presentation(3),
                                       "PB4": presentation(4)}}


def fixture_occurrences(active: dict[str, bool]) -> list[dict]:
    blocks = ["H1"] * 3 + ["H2"] * 3 + ["P"] * 5
    positions = [1, 2, 3, 1, 2, 3, 1, 2, 3, 5, 4]
    types = ["E3"] * 6 + ["E4"] * 5
    signs = [1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1]
    rows = []
    for index in range(1, 12):
        block = blocks[index - 1]
        enabled = index in (1, 4, 7) or (
            index == 2 and active["H1"] or index == 5 and active["H2"] or
            index == 8 and active["P"])
        rows.append({"ordinal": index, "block": block,
            "position": positions[index - 1], "type": types[index - 1],
            "registry_label": "C21" if index in (1, 5, 9) else "C" + str(20 + index),
            "repeated_e3_key": "E3_xy" if index in (1, 5) else None,
            "rank": RANK[block], "rho": {"x": [1], "y": [2]},
            "sigma": signs[index - 1], "prefix_word": [],
            "inverse_slot": index in (2, 5, 8, 10, 11),
            "orientation": "inverse" if index in (2, 5, 8, 10, 11) else "direct",
            "d_sources": ([{"coefficient": 1, "left_word": [],
                            "fox_word": [-2, -1],
                            "provenance": "synthetic_inverse_rho_g0"}]
                          if enabled else [])})
    return rows


def expected_literal(kind: str) -> dict:
    active = {"H1": True, "H2": True, "P": True}
    if kind == "H1_NONZERO": active["H1"] = False
    if kind == "H2_NONZERO": active["H2"] = False
    if kind == "P_NONZERO": active["P"] = False
    if kind == "COEFFICIENT_COLLISION":
        terms = [{"coefficient": 1, "U": [1], "V": [2], "ancestry": "collision_a"},
                 {"coefficient": 2, "U": [1], "V": [2], "ancestry": "collision_b"}]
    else:
        terms = [{"coefficient": 1, "U": [1], "V": [2],
                  "ancestry": "fixture_pair"}]
    return {"schema": SCHEMA + "/literal-input", "mode": "SELFTEST",
            "source_words": {"g0": [1, 2], "corrected": [1, 2, -2, 2]},
            "M_terms": terms, "occurrences": fixture_occurrences(active),
            "epsilon_sources": {"H1": [], "H2": [], "P": []}}


def compare_literal(actual: dict, expected: dict) -> None:
    need(type(actual) is dict, "source word gate")
    need(actual.get("schema") == expected["schema"] and
         actual.get("mode") == "SELFTEST", "source word gate")
    need(actual.get("source_words") == expected["source_words"], "source word gate")
    am, em = actual.get("M_terms"), expected["M_terms"]
    need(type(am) is list and len(am) == len(em), "coefficient gate")
    for got, want in zip(am, em):
        need(got.get("U") == want["U"] and got.get("V") == want["V"],
             "pair order gate")
        need(got.get("coefficient") == want["coefficient"], "coefficient gate")
        need(got.get("ancestry") == want["ancestry"], "coefficient gate")
    ao, eo = actual.get("occurrences"), expected["occurrences"]
    need(type(ao) is list and len(ao) == 11, "position gate")
    for got, want in zip(ao, eo):
        need(got.get("block") == want["block"], "block gate")
        need(got.get("ordinal") == want["ordinal"] and
             got.get("position") == want["position"], "position gate")
        need(got.get("type") == want["type"] and
             got.get("registry_label") == want["registry_label"] and
             got.get("repeated_e3_key") == want["repeated_e3_key"] and
             got.get("rank") == want["rank"], "type gate")
        need(got.get("rho") == want["rho"], "rho gate")
        need(got.get("sigma") == want["sigma"], "sign gate")
        need(got.get("prefix_word") == want["prefix_word"], "prefix gate")
        need(got.get("inverse_slot") == want["inverse_slot"] and
             got.get("orientation") == want["orientation"], "inverse slot gate")
        need(got.get("d_sources") == want["d_sources"], "source word gate")
    need(actual.get("epsilon_sources") == expected["epsilon_sources"],
         "epsilon gate")


def check_case(case: dict, fixture_row: dict) -> None:
    need(case.get("case_id") == fixture_row["case_id"] and
         case.get("kind") == fixture_row["kind"], "source word gate")
    expected = expected_literal(fixture_row["kind"])
    compare_literal(case.get("literal_input"), expected)
    replay = replay_literal(case["literal_input"])
    compiled = case.get("compiled")
    need(type(compiled) is dict, "normal form gate")
    need(compiled.get("mode") == "SELFTEST" and
         compiled.get("source_words") == case["literal_input"]["source_words"],
         "source word gate")
    need(case.get("terminal") == fixture_row["expected_terminal"] == replay["terminal"],
         "terminal gate")
    need(compiled.get("M") == replay["M"], "M digest gate")
    need(compiled.get("M", {}).get("immutable_digest_sha256") ==
         replay["M"]["immutable_digest_sha256"], "M digest gate")
    need(compiled.get("occurrence_ledger") == replay["occurrence_ledger"],
         "position gate")
    need(compiled.get("typed_coordinate_registry") == {
        "coordinate_count": 10, "occurrence_count": 11,
        "ten_to_eleven": [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9],
        "repeated_E3_positions": [1, 5],
        "typed_C21_positions": {"E3": [1, 5], "E4": [9]}},
        "type gate")
    got_occ = compiled.get("occurrences")
    need(type(got_occ) is list and len(got_occ) == 11, "xi gate")
    for got, want in zip(got_occ, replay["occurrences"]):
        need(got == want, "xi gate")
    need(compiled.get("epsilon_literal_sources") ==
         case["literal_input"]["epsilon_sources"], "epsilon gate")
    need(compiled.get("epsilon_chains") == replay["epsilon_chains"] and
         compiled.get("epsilon") == replay["epsilon"], "epsilon gate")
    got_endpoints = compiled.get("endpoints")
    need(type(got_endpoints) is dict, "normal form gate")
    for block in BLOCKS:
        got, want = got_endpoints.get(block), replay["endpoints"][block]
        need(type(got) is dict and got.get("unreduced_terms") == want["unreduced_terms"],
             "normal form gate")
        need(got.get("buckets") == want["buckets"] and
             got.get("zero_deletions") == want["zero_deletions"] and
             got.get("zero") == want["zero"], "bucket collection gate")
    need(compiled.get("complete_presentations") == replay["complete_presentations"],
         "Artin factor order gate")
    normal = compiled.get("normal_form", {})
    need(normal.get("Aij_braid_words") == {
        "PB3": [pure_to_artin(*pair) for pair in pure_pairs(3)],
        "PB4": [pure_to_artin(*pair) for pair in pure_pairs(4)]},
        "Artin factor order gate")
    need(normal.get("name") == "full-faithful-Artin-action-tuple" and
         normal.get("basis") == {"PB3": [1, 2, 3], "PB4": [1, 2, 3, 4]} and
         normal.get("pure_generator_order") == "lexicographic_i_then_j" and
         normal.get("composition") == "producer_left_to_right_step_substitution" and
         normal.get("hash_is_equality_key") is False and
         normal.get("finite_quotient_is_equality_key") is False,
         "normal form gate")
    need(compiled.get("endpoint_formula") ==
         "epsilon_B-sum_o sigma_o P_o sum_i a_i(rho_o(U_i)-rho_o(V_i)) xi_o",
         "normal form gate")
    need(compiled.get("full_C1_replay") == replay["full_C1_replay"],
         "full-C1 row gate")
    bindings = compiled.get("bindings", {})
    need(bindings.get("future_a5_a6", {}).get("seal") ==
         "synthetic-future-a5-a6-canary" and
         bindings.get("task226", {}).get("seal") == "task226-selftest-canary" and
         bindings.get("task193", {}).get("seal") == "task193-selftest-canary" and
         bindings.get("task198", {}).get("seal") == "task198-selftest-canary",
         "upstream seal gate")
    need(compiled.get("checkpoint_contract", {}).get("owner") == "task292-producer",
         "checkpoint owner gate")
    claims = compiled.get("forbidden_conclusions", {})
    need(set(claims) == {"A8_boundary_extracted", "A9_lift", "mixed_prime",
                         "perfect_core", "fake", "Ihara"} and
         all(value is False for value in claims.values()),
         "forbidden conclusion gate")
    if fixture_row["kind"] == "ZERO_CROSS_OCCURRENCE":
        pairs = {"H1": {1, 2}, "H2": {4, 5}, "P": {7, 8}}
        for block, pair in pairs.items():
            witnessed = False
            for deletion in replay["endpoints"][block]["zero_deletions"]:
                ordinals = {row["origin"].get("occurrence_ordinal")
                            for row in deletion["contributors"]
                            if row["origin"].get("kind") == "minus_M_star_xi"}
                witnessed = witnessed or pair.issubset(ordinals)
            need(witnessed, "bucket collection gate")
    if fixture_row["kind"] == "COEFFICIENT_COLLISION":
        need(replay["M"]["collected_terms"] == [] and
             len(replay["M"]["zero_deletions"]) == 1,
             "coefficient gate")


def check_selftest(result: dict, fixture: dict) -> None:
    need(type(result) is dict, "terminal gate")
    need(result.get("mode") == "SELFTEST", "terminal gate")
    need(result.get("mutation_controls") == MUTATIONS, "mutation roster gate")
    need(result.get("checkpoint_contract", {}).get("owner") == "task292-producer",
         "checkpoint owner gate")
    probes = result.get("terminal_probes", {})
    need(type(probes.get("input")) is str and probes["input"].startswith("UNKNOWN_INPUT:") and
         probes.get("resource") ==
         "UNKNOWN_RESOURCE:phase=selftest_probe:cap=word_letters:value=2:limit=1",
         "resource terminal gate")
    claims = result.get("forbidden_conclusions", {})
    need(set(claims) == {"A8_boundary_extracted", "A9_lift", "mixed_prime",
                         "perfect_core", "fake", "Ihara"} and
         all(value is False for value in claims.values()), "forbidden conclusion gate")
    cases, rows = result.get("cases"), fixture.get("cases")
    need(type(cases) is list and len(cases) == len(rows) == 5, "terminal gate")
    for case, row in zip(cases, rows):
        check_case(case, row)
    guards = result.get("guard_cases")
    need(type(guards) is list and [row.get("name") for row in guards] ==
         fixture.get("typed_swap_guards") and all(row.get("rejected") is True for row in guards),
         "type gate")
    need("typed occurrence position" in guards[0].get("reason", "") and
         "typed occurrence type" in guards[1].get("reason", ""), "type gate")


def mutate(receipt: dict, name: str) -> None:
    result = receipt["result"]
    primary = result["cases"][0]
    compiled = primary["compiled"]
    if name == "source_word":
        primary["literal_input"]["occurrences"][0]["d_sources"][0]["fox_word"][0] = -1
    elif name == "pair_order":
        term = primary["literal_input"]["M_terms"][0]
        term["U"], term["V"] = term["V"], term["U"]
    elif name == "coefficient":
        primary["literal_input"]["M_terms"][0]["coefficient"] = 2
    elif name == "block":
        primary["literal_input"]["occurrences"][0]["block"] = "H2"
    elif name == "position":
        primary["literal_input"]["occurrences"][0]["position"] = 2
    elif name == "type":
        primary["literal_input"]["occurrences"][0]["type"] = "E4"
    elif name == "rho":
        row = primary["literal_input"]["occurrences"][0]["rho"]
        row["x"], row["y"] = row["y"], row["x"]
    elif name == "sign":
        primary["literal_input"]["occurrences"][0]["sigma"] = -1
    elif name == "prefix":
        primary["literal_input"]["occurrences"][0]["prefix_word"] = [1]
    elif name == "inverse_slot":
        primary["literal_input"]["occurrences"][0]["inverse_slot"] = True
    elif name == "xi":
        compiled["occurrences"][0]["xi_terms"][0]["coefficient_mod_3"] = 2
    elif name == "epsilon":
        compiled["epsilon"]["H1"]["zero_deletions"].append({"mutated": True})
    elif name == "artin_factor_order":
        words = compiled["normal_form"]["Aij_braid_words"]["PB4"]
        words[0], words[1] = words[1], words[0]
    elif name == "normal_form":
        compiled["endpoints"]["H1"]["unreduced_terms"][0]["full_artin_key"][0].append(1)
    elif name == "bucket_deletion":
        result["cases"][1]["compiled"]["endpoints"]["H1"]["buckets"].pop()
    elif name == "M_digest":
        compiled["M"]["immutable_digest_sha256"] = "0" * 64
    elif name == "upstream_seal":
        compiled["bindings"]["future_a5_a6"]["seal"] = "mutated"
    elif name == "full_C1_row":
        compiled["full_C1_replay"]["blocks"]["H1"]["z_uncollected_terms"].pop()
    elif name == "terminal":
        receipt["terminal"] = NONZERO + " block=H1"
    elif name == "resource_terminal":
        result["terminal_probes"]["resource"] = UNKNOWN_RESOURCE + ":bad"
    elif name == "checkpoint_owner":
        result["checkpoint_contract"]["owner"] = "mutated"
    else:
        raise CheckStop("unregistered mutation")
    body = dict(receipt)
    body.pop("self_digest_sha256", None)
    receipt["self_digest_sha256"] = hexdigest(body)


def mutation_owner(receipt: dict, name: str) -> object:
    result = receipt["result"]
    primary = result["cases"][0]
    literal = primary["literal_input"]
    compiled = primary["compiled"]
    if name == "source_word": return literal["occurrences"][0]["d_sources"][0]["fox_word"]
    if name == "pair_order": return [literal["M_terms"][0]["U"], literal["M_terms"][0]["V"]]
    if name == "coefficient": return literal["M_terms"][0]["coefficient"]
    if name in ("block", "position", "type"):
        return literal["occurrences"][0][name]
    if name == "rho": return literal["occurrences"][0]["rho"]
    if name == "sign": return literal["occurrences"][0]["sigma"]
    if name == "prefix": return literal["occurrences"][0]["prefix_word"]
    if name == "inverse_slot": return literal["occurrences"][0]["inverse_slot"]
    if name == "xi": return compiled["occurrences"][0]["xi_terms"]
    if name == "epsilon": return compiled["epsilon"]["H1"]
    if name == "artin_factor_order": return compiled["normal_form"]["Aij_braid_words"]
    if name == "normal_form": return compiled["endpoints"]["H1"]["unreduced_terms"][0]["full_artin_key"]
    if name == "bucket_deletion": return result["cases"][1]["compiled"]["endpoints"]["H1"]["buckets"]
    if name == "M_digest": return compiled["M"]["immutable_digest_sha256"]
    if name == "upstream_seal": return compiled["bindings"]["future_a5_a6"]
    if name == "full_C1_row": return compiled["full_C1_replay"]["blocks"]["H1"]["z_uncollected_terms"]
    if name == "terminal": return receipt["terminal"]
    if name == "resource_terminal": return result["terminal_probes"]["resource"]
    if name == "checkpoint_owner": return result["checkpoint_contract"]["owner"]
    raise CheckStop("unregistered mutation owner")


def mutation_checks(receipt: dict, fixture: dict) -> list[dict]:
    output = []
    for name in MUTATIONS:
        changed = copy.deepcopy(receipt)
        before = hexdigest(mutation_owner(changed, name))
        mutate(changed, name)
        after = hexdigest(mutation_owner(changed, name))
        need(before != after, "mutation owner unchanged:" + name)
        try:
            validate_selftest_receipt(changed, fixture)
        except CheckStop as exc:
            reason = str(exc)
            need(GATES[name].lower() in reason.lower(),
                 "mutation gate mismatch:" + name + ":" + reason)
            output.append({"name": name, "expected_gate": GATES[name],
                           "observed_reason": reason, "owner_before": before,
                           "owner_after": after, "rejected": True})
        else:
            raise MutationAccepted("accepted mutation:" + name)
    need(len(output) == len(MUTATIONS), "mutation roster gate")
    return output


def validate_selftest_receipt(receipt: dict, fixture: dict) -> None:
    check_seal(receipt)
    need(receipt.get("schema") == SCHEMA, "terminal gate")
    terminal_kind(receipt.get("terminal"))
    need(receipt.get("terminal") == ZERO, "terminal gate")
    check_selftest(receipt.get("result"), fixture)


def terminal_kind(terminal: str) -> str:
    need(type(terminal) is str, "terminal gate")
    if terminal == ZERO:
        return ZERO
    if terminal in tuple(NONZERO + " block=" + block for block in BLOCKS):
        return NONZERO
    if terminal.startswith(UNKNOWN_INPUT + ":") and len(terminal) > len(UNKNOWN_INPUT) + 1:
        return UNKNOWN_INPUT
    if terminal.startswith(UNKNOWN_RESOURCE + ":phase="):
        fields = terminal.split(":")
        need(len(fields) == 5 and fields[1].startswith("phase=") and
             fields[2].startswith("cap=") and fields[3].startswith("value=") and
             fields[4].startswith("limit=") and
             bool(fields[1][6:]) and bool(fields[2][4:]) and
             fields[3][6:].isdigit() and fields[4][6:].isdigit(),
             "resource terminal gate")
        return UNKNOWN_RESOURCE
    raise CheckStop("terminal gate")


def load_fixture(path: str) -> tuple[bytes, dict]:
    p = Path(path)
    need(not p.is_absolute() and ".." not in p.parts and
         path.replace("\\", "/") == p.as_posix(), "fixture path gate")
    raw = (ROOT / p).read_bytes()
    meter("input_bytes", len(raw), "checker fixture input")
    value = json.loads(raw)
    need(value.get("schema") == FIXTURE_SCHEMA and
         value.get("production_input") is False and
         value.get("mutation_controls") == MUTATIONS, "fixture gate")
    need(value.get("claims") == {
        "A8_boundary_extracted": False, "A9_lift": False,
        "mixed_prime": False, "perfect_core": False,
        "fake": False, "Ihara": False}, "fixture gate")
    return raw, value


def output_path(path: str) -> Path:
    p = Path(path)
    need(not p.is_absolute() and ".." not in p.parts and
         path.replace("\\", "/") == p.as_posix() and path.startswith("ci/out/"),
         "verdict path gate")
    target = ROOT / p
    need(not target.exists(), "stale verdict refused")
    return target


def main(argv: list[str] | None = None) -> int:
    global CHECK_BUDGET
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--fixture", default=FIXTURE)
    ap.add_argument("--verdict", required=True)
    args = ap.parse_args(argv)
    CHECK_BUDGET = CheckerBudget()
    terminal = UNKNOWN_INPUT + ":uninitialized"
    accepted = False
    reason = None
    mutations = []
    receipt_raw = b""
    try:
        target = output_path(args.verdict)
        receipt_path = Path(args.receipt)
        need(not receipt_path.is_absolute() and ".." not in receipt_path.parts and
             args.receipt.replace("\\", "/") == receipt_path.as_posix() and
             args.receipt.startswith("ci/out/"), "receipt path gate")
        receipt_raw = (ROOT / receipt_path).read_bytes()
        meter("input_bytes", len(receipt_raw), "checker receipt input")
        receipt = json.loads(receipt_raw)
        need(receipt_raw == packed(receipt), "receipt canonical gate")
        check_seal(receipt)
        terminal = receipt.get("terminal")
        terminal_kind(terminal)
        if args.selftest:
            fixture_raw, fixture = load_fixture(args.fixture)
            validate_selftest_receipt(receipt, fixture)
            mutations = mutation_checks(receipt, fixture)
            accepted = True
        else:
            # No accepted task285 MEMBER/M ABI exists.  Authenticate only the
            # v2 producer's deterministic typed blocker; read no task285 file.
            blocked_reason = PRODUCTION_BLOCK_REASON
            need(receipt.get("schema") == SCHEMA and
                 terminal == UNKNOWN_INPUT + ":" + blocked_reason and
                 receipt.get("result") == {
                     "reason": blocked_reason,
                     "checkpoint_contract": {"owner": "task292-producer"},
                     "forbidden_conclusions": FORBIDDEN_CONCLUSIONS,
                 }, "production ABI unavailable gate")
            accepted = True
    except CheckerResource as exc:
        reason = {"phase": exc.phase, "cap": exc.cap,
                  "value": exc.value, "limit": exc.limit}
        accepted = False
        terminal = (UNKNOWN_RESOURCE + ":phase=" + exc.phase + ":cap=" + exc.cap +
                    ":value=" + str(exc.value) + ":limit=" + str(exc.limit))
        target = output_path(args.verdict) if 'target' not in locals() else target
    except (CheckStop, MutationAccepted, KeyError, ValueError, TypeError,
            FileNotFoundError, json.JSONDecodeError, UnicodeError) as exc:
        reason = str(exc)
        accepted = False
        terminal = UNKNOWN_INPUT + ":" + reason
        target = output_path(args.verdict) if 'target' not in locals() else target
    verdict = {"schema": VERDICT_SCHEMA, "terminal": terminal,
               "accepted": accepted, "independent": True,
               "mathematical_zero_accepted": accepted and terminal == ZERO and args.selftest,
               "production_member_authenticated": False,
               "producer_imported": False,
               "normal_form_boundary":
                   "pointwise Artin action on each free basis word",
               "receipt_path": args.receipt,
               "receipt_bytes": len(receipt_raw),
               "receipt_sha256": hashlib.sha256(receipt_raw).hexdigest(),
               "mutation_results": mutations,
               "production_binding": {"present": False,
                                      "reason": PRODUCTION_BLOCK_REASON},
               "forbidden_conclusions": dict(FORBIDDEN_CONCLUSIONS),
               "resource_meter": {"caps": CHECK_BUDGET.caps,
                                  "used": CHECK_BUDGET.used},
               "reason": reason}
    verdict["self_digest_sha256"] = hexdigest(verdict)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(packed(verdict))
    print(("D292_CHECKER_PASS" if accepted else "D292_CHECKER_REJECT") +
          " terminal=" + terminal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
