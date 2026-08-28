#!/usr/bin/env python3
"""Task 292: exact PB3/PB4 endpoint compiler v2.

The equality key is the complete faithful Artin action on a free basis.  No
finite quotient, digest, or external normal-form helper is used as an equality
oracle.  The independent checker contains a separately written evaluator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-actual-three-exact-pb-endpoints/v2"
FIXTURE_SCHEMA = SCHEMA + "/selftest-fixture"
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
BLOCK_RANK = {"H1": 3, "H2": 3, "P": 4}
MUTATIONS = [
    "source_word", "pair_order", "coefficient", "block", "position", "type",
    "rho", "sign", "prefix", "inverse_slot", "xi", "epsilon",
    "artin_factor_order", "normal_form", "bucket_deletion", "M_digest",
    "upstream_seal", "full_C1_row", "terminal", "resource_terminal",
    "checkpoint_owner",
]


class Stop(RuntimeError):
    pass


class ResourceStop(Stop):
    def __init__(self, phase: str, cap: str, value: int, limit: int):
        super().__init__(phase)
        self.phase, self.cap, self.value, self.limit = phase, cap, value, limit


def require(ok: bool, message: str) -> None:
    if ok is not True:
        raise Stop(message)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def envelope(terminal: str, result: dict) -> dict:
    out = {"schema": SCHEMA, "terminal": terminal, "result": result}
    out["self_digest_sha256"] = digest(out)
    return out


def unknown_input(reason: str) -> str:
    return UNKNOWN_INPUT + ":" + reason.replace("\n", " ")


def unknown_resource(exc: ResourceStop) -> str:
    return (UNKNOWN_RESOURCE + ":phase=" + exc.phase + ":cap=" + exc.cap +
            ":value=" + str(exc.value) + ":limit=" + str(exc.limit))


class Budget:
    CAPS = {
        "input_bytes": 2_100_000_000,
        "word_letters": 20_000_000,
        "artin_letters": 40_000_000,
        "sparse_terms": 4_000_000,
        "serialized_bytes": 400_000_000,
        "wall_seconds": 21600,
    }

    def __init__(self) -> None:
        self.used = {name: 0 for name in self.CAPS}
        self.started = time.monotonic()

    def bump(self, cap: str, amount: int, phase: str) -> None:
        require(cap in self.CAPS and type(amount) is int and amount >= 0,
                "resource meter input")
        self.used[cap] += amount
        elapsed = int(time.monotonic() - self.started)
        self.used["wall_seconds"] = max(self.used["wall_seconds"], elapsed)
        if self.used[cap] > self.CAPS[cap]:
            raise ResourceStop(phase, cap, self.used[cap], self.CAPS[cap])
        if self.used["wall_seconds"] > self.CAPS["wall_seconds"]:
            raise ResourceStop(phase, "wall_seconds", self.used["wall_seconds"],
                               self.CAPS["wall_seconds"])

    def receipt(self) -> dict:
        return {"caps": dict(self.CAPS), "used": dict(self.used)}


def reduce_word(word: list[int], width: int | None = None) -> list[int]:
    answer: list[int] = []
    for letter in word:
        require(type(letter) is int and letter != 0, "word letter")
        if width is not None:
            require(abs(letter) <= width, "word width")
        if answer and answer[-1] == -letter:
            answer.pop()
        else:
            answer.append(letter)
    return answer


def inverse_word(word: list[int]) -> list[int]:
    return [-letter for letter in reversed(word)]


def substitute(word: list[int], images: list[list[int]], width: int | None = None) -> list[int]:
    answer: list[int] = []
    for letter in word:
        index = abs(letter) - 1
        require(0 <= index < len(images), "substitution letter")
        image = images[index]
        answer.extend(image if letter > 0 else inverse_word(image))
    return reduce_word(answer, width)


def substitute_f2(word: list[int], left: list[int], right: list[int], width: int) -> list[int]:
    return substitute(word, [left, right], width)


def pair_list(rank: int) -> list[list[int]]:
    return [[i, j] for i in range(1, rank) for j in range(i + 1, rank + 1)]


def pair_index(rank: int, pair: list[int]) -> int:
    pairs = pair_list(rank)
    require(pair in pairs, "pure generator pair")
    return pairs.index(pair) + 1


def aij_braid(i: int, j: int) -> list[int]:
    require(1 <= i < j, "Aij indices")
    return list(range(j - 1, i, -1)) + [i, i] + [
        -k for k in range(i + 1, j)
    ]


def artin_step(rank: int, letter: int) -> list[list[int]]:
    i = abs(letter)
    require(1 <= i < rank, "Artin letter")
    images = [[j] for j in range(1, rank + 1)]
    if letter > 0:
        images[i - 1] = [i, i + 1, -i]
        images[i] = [i]
    else:
        images[i - 1] = [i + 1]
        images[i] = [-(i + 1), i, i + 1]
    return images


def artin_images(rank: int, braid_word: list[int], budget: Budget | None = None) -> list[list[int]]:
    images = [[i] for i in range(1, rank + 1)]
    for letter in braid_word:
        if budget is not None:
            budget.bump("artin_letters", 1, "Artin action")
        step = artin_step(rank, letter)
        images = [substitute(image, step, rank) for image in images]
        if budget is not None:
            budget.bump("word_letters", sum(len(image) for image in images),
                        "Artin image expansion")
    return images


def expand_pure(rank: int, pure_word: list[int]) -> list[int]:
    pairs = pair_list(rank)
    expanded: list[int] = []
    for letter in pure_word:
        require(1 <= abs(letter) <= len(pairs), "PB word width")
        base = aij_braid(*pairs[abs(letter) - 1])
        expanded.extend(base if letter > 0 else inverse_word(base))
    return expanded


class ExactArtin:
    def __init__(self, budget: Budget):
        self.budget = budget
        self.cache: dict[tuple[int, tuple[int, ...]], tuple[tuple[int, ...], ...]] = {}

    def key(self, rank: int, word: list[int]) -> tuple[tuple[int, ...], ...]:
        width = len(pair_list(rank))
        reduced = reduce_word(list(word), width)
        cache_key = (rank, tuple(reduced))
        if cache_key not in self.cache:
            expanded = expand_pure(rank, reduced)
            self.budget.bump("word_letters", len(reduced), "PB word staging")
            self.cache[cache_key] = tuple(tuple(row) for row in
                                          artin_images(rank, expanded, self.budget))
        return self.cache[cache_key]


def pure_relations(rank: int) -> list[list[int]]:
    if rank == 2:
        return []
    old_pairs = pair_list(rank - 1)
    old_map = [[pair_index(rank, pair)] for pair in old_pairs]
    answer = [substitute(word, old_map) for word in pure_relations(rank - 1)]
    kernel = [[pair_index(rank, [k, rank])] for k in range(1, rank)]
    for i, j in old_pairs:
        conjugator = pair_index(rank, [i, j])
        action = artin_images(rank - 1, aij_braid(i, j))
        for k in range(1, rank):
            target = pair_index(rank, [k, rank])
            rhs = substitute(action[k - 1], kernel)
            answer.append(reduce_word([-conjugator, target, conjugator] +
                                      inverse_word(rhs)))
    return answer


def presentation_certificate(rank: int, normalizer: ExactArtin) -> dict:
    identity = tuple((i,) for i in range(1, rank + 1))
    rows = []
    for index, relator in enumerate(pure_relations(rank), 1):
        key = normalizer.key(rank, relator)
        require(key == identity, "complete presentation identity")
        fox_row = chain_sources(
            [{"coefficient": 1, "left_word": [], "fox_word": relator,
              "provenance": "complete_PB_presentation_relator"}],
            rank, normalizer, {"kind": "D2_relator", "relator_index": index})
        d1d2_terms = endpoint_of_chain(fox_row, rank, normalizer, "D1_D2_relator")
        d1d2_buckets, d1d2_deletions = collect_group_terms(d1d2_terms)
        require(not d1d2_buckets, "complete presentation D1D2 identity")
        rows.append({
            "index": index,
            "relator": relator,
            "expanded_artin_word": expand_pure(rank, relator),
            "full_artin_key": [list(row) for row in key],
            "identity": True,
            "D2_fox_row": fox_row,
            "D1_D2_unreduced_terms": d1d2_terms,
            "D1_D2_buckets": d1d2_buckets,
            "D1_D2_zero_deletions": d1d2_deletions,
            "D1_D2_zero": True,
        })
    require(len(rows) == (2 if rank == 3 else 11),
            "complete presentation cardinality")
    return {
        "group": "PB" + str(rank),
        "generator_pairs": pair_list(rank),
        "relator_count": len(rows),
        "relators": rows,
        "complete_fixed_roster": True,
    }


def chain_sources(sources: list[dict], rank: int, normalizer: ExactArtin,
                  owner: dict) -> list[dict]:
    width = len(pair_list(rank))
    terms: list[dict] = []
    for source_index, source in enumerate(sources, 1):
        coefficient = source.get("coefficient")
        left = source.get("left_word")
        fox_word = source.get("fox_word")
        require(type(coefficient) is int and type(left) is list and type(fox_word) is list,
                "literal Fox source")
        left_reduced = reduce_word(left, width)
        cursor: list[int] = []
        for word_index, letter in enumerate(fox_word, 1):
            require(type(letter) is int and 1 <= abs(letter) <= width,
                    "Fox word letter")
            if letter > 0:
                group_word = left_reduced + cursor
                component = letter
                local = 1
                cursor = reduce_word(cursor + [letter], width)
            else:
                cursor = reduce_word(cursor + [letter], width)
                group_word = left_reduced + cursor
                component = -letter
                local = -1
            reduced = reduce_word(group_word, width)
            terms.append({
                "component": component,
                "coefficient": coefficient * local,
                "unreduced_group_word": group_word,
                "free_reduced_group_word": reduced,
                "full_artin_key": [list(row) for row in normalizer.key(rank, reduced)],
                "origin": dict(owner, source_index=source_index,
                               fox_letter_index=word_index,
                               source_provenance=source.get("provenance")),
            })
    normalizer.budget.bump("sparse_terms", len(terms), "literal Fox expansion")
    return terms


def endpoint_of_chain(chain: list[dict], rank: int, normalizer: ExactArtin,
                      phase: str) -> list[dict]:
    terms: list[dict] = []
    for index, row in enumerate(chain, 1):
        coefficient = row["coefficient"]
        group_word = row["unreduced_group_word"]
        component = row["component"]
        positive = group_word + [component]
        for slot, word, sign in (("gx", positive, 1), ("g", group_word, -1)):
            reduced = reduce_word(word, len(pair_list(rank)))
            terms.append({
                "coefficient": coefficient * sign,
                "unreduced_word": word,
                "free_reduced_word": reduced,
                "full_artin_key": [list(x) for x in normalizer.key(rank, reduced)],
                "origin": {"kind": phase, "chain_term": index,
                           "endpoint_slot": slot, "chain_origin": row["origin"]},
            })
    normalizer.budget.bump("sparse_terms", len(terms), "D1 expansion")
    return terms


def collect_group_terms(terms: list[dict]) -> tuple[list[dict], list[dict]]:
    table: dict[tuple[tuple[int, ...], ...], dict] = {}
    for index, term in enumerate(terms, 1):
        key = tuple(tuple(row) for row in term["full_artin_key"])
        if key not in table:
            table[key] = {
                "full_artin_key": term["full_artin_key"],
                "representative_word": term["free_reduced_word"],
                "integer_sum": 0,
                "contributors": [],
            }
        table[key]["integer_sum"] += term["coefficient"]
        table[key]["contributors"].append({
            "term_index": index,
            "coefficient": term["coefficient"],
            "origin": term["origin"],
        })
    kept, deleted = [], []
    for key in sorted(table, key=lambda x: repr(x)):
        row = table[key]
        row["coefficient_mod_3"] = row["integer_sum"] % 3
        if row["coefficient_mod_3"]:
            kept.append(row)
        else:
            deleted.append(row)
    return kept, deleted


def collect_chain_terms(terms: list[dict]) -> tuple[list[dict], list[dict]]:
    table: dict[tuple[int, tuple[tuple[int, ...], ...]], dict] = {}
    for index, term in enumerate(terms, 1):
        artin = tuple(tuple(row) for row in term["full_artin_key"])
        key = (term["component"], artin)
        if key not in table:
            table[key] = {
                "component": term["component"],
                "full_artin_key": term["full_artin_key"],
                "representative_word": term["free_reduced_group_word"],
                "integer_sum": 0,
                "contributors": [],
            }
        table[key]["integer_sum"] += term["coefficient"]
        table[key]["contributors"].append({
            "term_index": index,
            "coefficient": term["coefficient"],
            "origin": term["origin"],
        })
    kept, deleted = [], []
    for key in sorted(table, key=lambda x: repr(x)):
        row = table[key]
        row["coefficient_mod_3"] = row["integer_sum"] % 3
        if row["coefficient_mod_3"]:
            kept.append(row)
        else:
            deleted.append(row)
    return kept, deleted


def aggregate_m(raw_terms: list[dict]) -> dict:
    require(type(raw_terms) is list, "M term roster")
    normalized, table = [], {}
    for index, term in enumerate(raw_terms, 1):
        require(type(term) is dict and type(term.get("coefficient")) is int,
                "M coefficient")
        left = reduce_word(term.get("U", []), 2)
        right = reduce_word(term.get("V", []), 2)
        require(left != right, "M diagonal pair")
        row = {
            "input_index": index,
            "coefficient": term["coefficient"],
            "U": left,
            "V": right,
            "ancestry": term.get("ancestry"),
        }
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
    immutable = {
        "modulus": 3,
        "ordered_pair_convention": "U_minus_V",
        "terms": [{"coefficient": row["coefficient"], "U": row["U"],
                   "V": row["V"], "ancestry": row["ancestry"]}
                  for row in collected],
    }
    return {
        "precollection_terms": normalized,
        "collected_terms": collected,
        "zero_deletions": deleted,
        "immutable_payload": immutable,
        "immutable_digest_sha256": digest(immutable),
    }


def validate_occurrence_roster(rows: list[dict]) -> None:
    require(type(rows) is list and len(rows) == 11, "eleven occurrence roster")
    expected_blocks = ["H1"] * 3 + ["H2"] * 3 + ["P"] * 5
    expected_types = ["E3"] * 6 + ["E4"] * 5
    expected_positions = [1, 2, 3, 1, 2, 3, 1, 2, 3, 5, 4]
    repeated_positions, c21 = [], []
    for index, row in enumerate(rows, 1):
        require(row.get("ordinal") == index and row.get("block") == expected_blocks[index - 1],
                "typed occurrence position")
        require(row.get("position") == expected_positions[index - 1],
                "typed occurrence position")
        require(row.get("type") == expected_types[index - 1], "typed occurrence type")
        require(row.get("rank") == BLOCK_RANK[row["block"]], "typed occurrence rank")
        require(row.get("sigma") in (-1, 1), "occurrence sign")
        require(type(row.get("prefix_word")) is list and type(row.get("rho")) is dict,
                "occurrence prefix/rho")
        if row.get("registry_label") == "C21":
            c21.append((row["type"], row["ordinal"]))
        if row.get("repeated_e3_key") == "E3_xy":
            repeated_positions.append(row["ordinal"])
    require(repeated_positions == [1, 5], "repeated E3 positions")
    require(c21 == [("E3", 1), ("E3", 5), ("E4", 9)],
            "typed C21 distinction")


def build_occurrences(literal: dict, normalizer: ExactArtin) -> list[dict]:
    rows = literal.get("occurrences")
    validate_occurrence_roster(rows)
    answer = []
    for row in rows:
        rank = row["rank"]
        width = len(pair_list(rank))
        left = reduce_word(row["rho"].get("x", []), width)
        right = reduce_word(row["rho"].get("y", []), width)
        prefix = reduce_word(row["prefix_word"], width)
        sources = row.get("d_sources")
        require(type(sources) is list, "occurrence literal d sources")
        d_chain = chain_sources(sources, rank, normalizer,
                                {"kind": "occurrence_d", "ordinal": row["ordinal"]})
        xi_terms = endpoint_of_chain(d_chain, rank, normalizer, "xi")
        xi_collection, xi_deletions = collect_group_terms(xi_terms)
        built = dict(row)
        built["rho"] = {"x": left, "y": right}
        built["prefix_word"] = prefix
        built["P_word"] = prefix
        built["d_chain_uncollected"] = d_chain
        built["xi_unreduced_terms"] = xi_terms
        built["xi_terms"] = xi_collection
        built["xi_zero_deletions"] = xi_deletions
        answer.append(built)
    return answer


def endpoint_terms_for_block(block: str, occurrences: list[dict], m: dict,
                             epsilon_terms: list[dict], normalizer: ExactArtin) -> list[dict]:
    rank = BLOCK_RANK[block]
    width = len(pair_list(rank))
    terms = [dict(row) for row in epsilon_terms]
    for occurrence in occurrences:
        if occurrence["block"] != block:
            continue
        for m_index, mterm in enumerate(m["collected_terms"], 1):
            for side, source_word, side_sign in (
                    ("U", mterm["U"], 1), ("V", mterm["V"], -1)):
                rho_word = substitute_f2(source_word, occurrence["rho"]["x"],
                                         occurrence["rho"]["y"], width)
                for xi_index, xi in enumerate(occurrence["xi_terms"], 1):
                    raw = (list(occurrence["prefix_word"]) + rho_word +
                           list(xi["representative_word"]))
                    reduced = reduce_word(raw, width)
                    coefficient = (-occurrence["sigma"] * mterm["coefficient"] *
                                   side_sign * xi["coefficient_mod_3"])
                    terms.append({
                        "coefficient": coefficient,
                        "unreduced_word": raw,
                        "free_reduced_word": reduced,
                        "full_artin_key": [list(x) for x in normalizer.key(rank, reduced)],
                        "origin": {
                            "kind": "minus_M_star_xi", "block": block,
                            "occurrence_ordinal": occurrence["ordinal"],
                            "position": occurrence["position"], "type": occurrence["type"],
                            "registry_label": occurrence["registry_label"],
                            "sigma": occurrence["sigma"],
                            "prefix_word": occurrence["prefix_word"],
                            "inverse_slot": occurrence["inverse_slot"],
                            "rho": occurrence["rho"], "M_term": m_index,
                            "pair_side": side, "pair_side_sign": side_sign,
                            "source_F2_word": source_word,
                            "rho_evaluated_word": rho_word,
                            "xi_term": xi_index,
                        },
                    })
    normalizer.budget.bump("sparse_terms", len(terms), "endpoint expansion")
    return terms


def full_chain_for_block(block: str, occurrences: list[dict], m: dict,
                         epsilon_chain: list[dict], normalizer: ExactArtin) -> dict:
    rank = BLOCK_RANK[block]
    width = len(pair_list(rank))
    raw = [dict(row, origin=dict(row["origin"], z_source="epsilon"))
           for row in epsilon_chain]
    for occurrence in occurrences:
        if occurrence["block"] != block:
            continue
        for m_index, mterm in enumerate(m["collected_terms"], 1):
            for side, source_word, side_sign in (
                    ("U", mterm["U"], 1), ("V", mterm["V"], -1)):
                rho_word = substitute_f2(source_word, occurrence["rho"]["x"],
                                         occurrence["rho"]["y"], width)
                for d_index, dterm in enumerate(occurrence["d_chain_uncollected"], 1):
                    group_word = (list(occurrence["prefix_word"]) + rho_word +
                                  list(dterm["unreduced_group_word"]))
                    reduced = reduce_word(group_word, width)
                    coefficient = (-occurrence["sigma"] * mterm["coefficient"] *
                                   side_sign * dterm["coefficient"])
                    raw.append({
                        "component": dterm["component"],
                        "coefficient": coefficient,
                        "unreduced_group_word": group_word,
                        "free_reduced_group_word": reduced,
                        "full_artin_key": [list(x) for x in normalizer.key(rank, reduced)],
                        "origin": {
                            "kind": "minus_M_star_d", "block": block,
                            "occurrence_ordinal": occurrence["ordinal"],
                            "position": occurrence["position"], "type": occurrence["type"],
                            "registry_label": occurrence["registry_label"],
                            "sigma": occurrence["sigma"],
                            "prefix_word": occurrence["prefix_word"],
                            "inverse_slot": occurrence["inverse_slot"],
                            "rho": occurrence["rho"], "M_term": m_index,
                            "pair_side": side, "pair_side_sign": side_sign,
                            "source_F2_word": source_word,
                            "rho_evaluated_word": rho_word,
                            "d_term": d_index,
                        },
                    })
    normalizer.budget.bump("sparse_terms", len(raw), "full-C1 expansion")
    support, deletions = collect_chain_terms(raw)
    replay_chain = []
    for row in support:
        replay_chain.append({
            "component": row["component"],
            "coefficient": row["coefficient_mod_3"],
            "unreduced_group_word": row["representative_word"],
            "free_reduced_group_word": row["representative_word"],
            "full_artin_key": row["full_artin_key"],
            "origin": {"kind": "collected_z", "contributors": row["contributors"]},
        })
    d1_terms = endpoint_of_chain(replay_chain, rank, normalizer, "D1_z")
    d1_support, d1_deletions = collect_group_terms(d1_terms)
    return {
        "z_uncollected_terms": raw,
        "z_finite_support": support,
        "z_zero_deletions": deletions,
        "D1_z_unreduced_terms": d1_terms,
        "D1_z_buckets": d1_support,
        "D1_z_zero_deletions": d1_deletions,
        "D1_z_zero": not d1_support,
    }


def compile_literal(literal: dict, bindings: dict, budget: Budget) -> tuple[str, dict]:
    require(type(literal) is dict and literal.get("schema") == SCHEMA + "/literal-input",
            "literal input schema")
    normalizer = ExactArtin(budget)
    m = aggregate_m(literal.get("M_terms"))
    claimed_m = literal.get("M_immutable_digest_sha256")
    if claimed_m is not None:
        require(claimed_m == m["immutable_digest_sha256"], "M immutable digest")
    occurrences = build_occurrences(literal, normalizer)
    epsilon_chains, epsilon = {}, {}
    for block in BLOCKS:
        rank = BLOCK_RANK[block]
        sources = literal.get("epsilon_sources", {}).get(block)
        require(type(sources) is list, "epsilon literal source")
        chain = chain_sources(sources, rank, normalizer,
                              {"kind": "epsilon", "block": block})
        endpoint = endpoint_of_chain(chain, rank, normalizer, "epsilon")
        buckets, deletions = collect_group_terms(endpoint)
        epsilon_chains[block] = chain
        epsilon[block] = {"unreduced_terms": endpoint, "buckets": buckets,
                          "zero_deletions": deletions}

    endpoints = {}
    first_nonzero = None
    for block in BLOCKS:
        raw = endpoint_terms_for_block(block, occurrences, m,
                                       epsilon[block]["unreduced_terms"], normalizer)
        buckets, deletions = collect_group_terms(raw)
        endpoints[block] = {
            "unreduced_terms": raw,
            "buckets": buckets,
            "zero_deletions": deletions,
            "zero": not buckets,
        }
        if buckets and first_nonzero is None:
            first_nonzero = block
    terminal = ZERO if first_nonzero is None else NONZERO + " block=" + first_nonzero

    presentations = {
        "PB3": presentation_certificate(3, normalizer),
        "PB4": presentation_certificate(4, normalizer),
    }
    full_c1 = {
        "performed": first_nonzero is None,
        "presentation_boundary_quotient": "complete_fixed_PB_presentation",
        "q_B_extracted": False,
        "blocks": {},
    }
    if first_nonzero is None:
        for block in BLOCKS:
            replay = full_chain_for_block(block, occurrences, m,
                                          epsilon_chains[block], normalizer)
            require(replay["D1_z_zero"], "full-C1 endpoint replay")
            require(replay["D1_z_buckets"] == endpoints[block]["buckets"],
                    "endpoint/full-C1 agreement")
            replay["complete_presentation"] = "PB" + str(BLOCK_RANK[block])
            full_c1["blocks"][block] = replay
    else:
        full_c1["reason"] = "endpoint obstruction in " + first_nonzero

    result = {
        "mode": literal.get("mode"),
        "bindings": bindings,
        "source_words": literal.get("source_words"),
        "M": m,
        "occurrence_ledger": [{k: row[k] for k in (
            "ordinal", "block", "position", "type", "registry_label",
            "repeated_e3_key", "rank", "sigma", "prefix_word", "inverse_slot",
            "orientation", "rho", "P_word")}
            for row in occurrences],
        "typed_coordinate_registry": {
            "coordinate_count": 10,
            "occurrence_count": 11,
            "ten_to_eleven": [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9],
            "repeated_E3_positions": [1, 5],
            "typed_C21_positions": {"E3": [1, 5], "E4": [9]},
        },
        "occurrences": occurrences,
        "epsilon_literal_sources": literal.get("epsilon_sources"),
        "epsilon_chains": epsilon_chains,
        "epsilon": epsilon,
        "endpoint_formula": "epsilon_B-sum_o sigma_o P_o sum_i a_i(rho_o(U_i)-rho_o(V_i)) xi_o",
        "endpoints": endpoints,
        "full_C1_replay": full_c1,
        "complete_presentations": presentations,
        "normal_form": {
            "name": "full-faithful-Artin-action-tuple",
            "basis": {"PB3": [1, 2, 3], "PB4": [1, 2, 3, 4]},
            "pure_generator_order": "lexicographic_i_then_j",
            "Aij_braid_words": {
                "PB3": [aij_braid(*pair) for pair in pair_list(3)],
                "PB4": [aij_braid(*pair) for pair in pair_list(4)],
            },
            "composition": "producer_left_to_right_step_substitution",
            "hash_is_equality_key": False,
            "finite_quotient_is_equality_key": False,
        },
        "checkpoint_contract": {
            "owner": "task292-producer",
            "resume_requires_same_input_digest": True,
            "partial_result_is_never_nonzero_or_zero": True,
        },
        "resource_meter": budget.receipt(),
        "forbidden_conclusions": {
            "A8_boundary_extracted": False,
            "A9_lift": False,
            "mixed_prime": False,
            "perfect_core": False,
            "fake": False,
            "Ihara": False,
        },
    }
    return terminal, result


def fixture_occurrences(active_second: dict[str, bool]) -> list[dict]:
    blocks = ["H1"] * 3 + ["H2"] * 3 + ["P"] * 5
    positions = [1, 2, 3, 1, 2, 3, 1, 2, 3, 5, 4]
    types = ["E3"] * 6 + ["E4"] * 5
    signs = [1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1]
    rows = []
    for index, (block, position, typ, sign) in enumerate(
            zip(blocks, positions, types, signs), 1):
        pair_active = index in (1, 4, 7) or (
            index == 2 and active_second["H1"] or
            index == 5 and active_second["H2"] or
            index == 8 and active_second["P"])
        rank = BLOCK_RANK[block]
        rows.append({
            "ordinal": index,
            "block": block,
            "position": position,
            "type": typ,
            "registry_label": "C21" if index in (1, 5, 9) else "C" + str(20 + index),
            "repeated_e3_key": "E3_xy" if index in (1, 5) else None,
            "rank": rank,
            "rho": {"x": [1], "y": [2]},
            "sigma": sign,
            "prefix_word": [],
            "inverse_slot": index in (2, 5, 8, 10, 11),
            "orientation": "inverse" if index in (2, 5, 8, 10, 11) else "direct",
            "d_sources": ([{"coefficient": 1, "left_word": [],
                             "fox_word": [-2, -1],
                             "provenance": "synthetic_inverse_rho_g0"}]
                          if pair_active else []),
        })
    return rows


def make_fixture_literal(case: dict) -> dict:
    kind = case["kind"]
    active = {"H1": True, "H2": True, "P": True}
    if kind == "H1_NONZERO":
        active["H1"] = False
    elif kind == "H2_NONZERO":
        active["H2"] = False
    elif kind == "P_NONZERO":
        active["P"] = False
    require(kind in ("ZERO_CROSS_OCCURRENCE", "H1_NONZERO", "H2_NONZERO",
                     "P_NONZERO", "COEFFICIENT_COLLISION"), "fixture case kind")
    if kind == "COEFFICIENT_COLLISION":
        terms = [
            {"coefficient": 1, "U": [1], "V": [2], "ancestry": "collision_a"},
            {"coefficient": 2, "U": [1], "V": [2], "ancestry": "collision_b"},
        ]
    else:
        terms = [{"coefficient": 1, "U": [1], "V": [2],
                  "ancestry": "fixture_pair"}]
    return {
        "schema": SCHEMA + "/literal-input",
        "mode": "SELFTEST",
        "source_words": {"g0": [1, 2], "corrected": [1, 2, -2, 2]},
        "M_terms": terms,
        "occurrences": fixture_occurrences(active),
        "epsilon_sources": {"H1": [], "H2": [], "P": []},
    }


def selftest_result(fixture: dict, budget: Budget) -> tuple[str, dict]:
    require(fixture.get("schema") == FIXTURE_SCHEMA, "fixture schema")
    require(fixture.get("production_input") is False, "fixture production flag")
    require(fixture.get("mutation_controls") == MUTATIONS, "fixture mutation roster")
    require(fixture.get("typed_swap_guards") ==
            ["repeated_E3_slot_swap", "typed_C21_E3_E4_swap"],
            "fixture typed swap roster")
    require(fixture.get("claims") == {
        "A8_boundary_extracted": False, "A9_lift": False,
        "mixed_prime": False, "perfect_core": False,
        "fake": False, "Ihara": False}, "fixture claim boundary")
    cases = []
    expected = {
        "ZERO_CROSS_OCCURRENCE": ZERO,
        "H1_NONZERO": NONZERO + " block=H1",
        "H2_NONZERO": NONZERO + " block=H2",
        "P_NONZERO": NONZERO + " block=P",
        "COEFFICIENT_COLLISION": ZERO,
    }
    for case in fixture.get("cases", []):
        literal = make_fixture_literal(case)
        terminal, result = compile_literal(literal, {
            "future_a5_a6": {"mode": "SELFTEST_CANARY",
                              "seal": "synthetic-future-a5-a6-canary"},
            "task226": {"mode": "SELFTEST", "seal": "task226-selftest-canary"},
            "task193": {"mode": "SELFTEST", "seal": "task193-selftest-canary"},
            "task198": {"mode": "SELFTEST", "seal": "task198-selftest-canary"},
        }, budget)
        require(terminal == expected[case["kind"]] == case["expected_terminal"],
                "fixture expected terminal")
        if case["kind"] == "ZERO_CROSS_OCCURRENCE":
            expected_pairs = {"H1": {1, 2}, "H2": {4, 5}, "P": {7, 8}}
            for block, pair in expected_pairs.items():
                witnessed = False
                for deletion in result["endpoints"][block]["zero_deletions"]:
                    ordinals = {row["origin"].get("occurrence_ordinal")
                                for row in deletion["contributors"]
                                if row["origin"].get("kind") == "minus_M_star_xi"}
                    witnessed = witnessed or pair.issubset(ordinals)
                require(witnessed, "cross-occurrence cancellation fixture")
        if case["kind"] == "COEFFICIENT_COLLISION":
            require(result["M"]["collected_terms"] == [] and
                    len(result["M"]["zero_deletions"]) == 1,
                    "coefficient collision/zero deletion fixture")
        cases.append({"case_id": case["case_id"], "kind": case["kind"],
                      "literal_input": literal, "terminal": terminal,
                      "compiled": result})
    require([row["kind"] for row in cases] == [
        "ZERO_CROSS_OCCURRENCE", "H1_NONZERO", "H2_NONZERO", "P_NONZERO",
        "COEFFICIENT_COLLISION"], "fixture case coverage")
    guard_cases = []
    base = make_fixture_literal({"kind": "ZERO_CROSS_OCCURRENCE"})
    repeated = json.loads(json.dumps(base))
    repeated["occurrences"][0]["ordinal"], repeated["occurrences"][4]["ordinal"] = 5, 1
    typed = json.loads(json.dumps(base))
    typed["occurrences"][0]["type"], typed["occurrences"][8]["type"] = "E4", "E3"
    for name, value, expected_reason in (
            ("repeated_E3_slot_swap", repeated, "typed occurrence position"),
            ("typed_C21_E3_E4_swap", typed, "typed occurrence type")):
        try:
            compile_literal(value, {}, budget)
        except Stop as exc:
            require(expected_reason in str(exc), "typed swap guard reason")
            guard_cases.append({"name": name, "rejected": True,
                                "reason": str(exc)})
        else:
            raise Stop("typed swap guard accepted")
    require(len(guard_cases) == 2, "typed swap guard coverage")
    resource_probe = (UNKNOWN_RESOURCE +
                      ":phase=selftest_probe:cap=word_letters:value=2:limit=1")
    return ZERO, {
        "mode": "SELFTEST",
        "cases": cases,
        "guard_cases": guard_cases,
        "mutation_controls": MUTATIONS,
        "terminal_probes": {
            "input": unknown_input("selftest_probe"),
            "resource": resource_probe,
        },
        "checkpoint_contract": {
            "owner": "task292-producer",
            "resume_requires_same_input_digest": True,
            "partial_result_is_never_nonzero_or_zero": True,
        },
        "resource_meter": budget.receipt(),
        "forbidden_conclusions": {
            "A8_boundary_extracted": False, "A9_lift": False,
            "mixed_prime": False, "perfect_core": False,
            "fake": False, "Ihara": False,
        },
    }


def production_literal(_args: argparse.Namespace, _budget: Budget) -> tuple[dict, dict]:
    """Fail closed without reading or pinning any rejected task285 artifact."""
    raise Stop(PRODUCTION_BLOCK_REASON)


def safe_output_path(path: str) -> Path:
    p = Path(path)
    require(not p.is_absolute() and ".." not in p.parts and
            path.replace("\\", "/") == p.as_posix() and path.startswith("ci/out/"),
            "output path")
    target = ROOT / p
    require(not target.exists(), "stale output refused")
    return target


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("output")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--fixture", default=FIXTURE)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    budget = Budget()
    terminal = unknown_input("uninitialized")
    result: dict = {"reason": "uninitialized"}
    target: Path | None = None
    try:
        target = safe_output_path(args.output)
        if args.selftest:
            raw = (ROOT / args.fixture).read_bytes()
            budget.bump("input_bytes", len(raw), "fixture input")
            fixture = json.loads(raw)
            terminal, result = selftest_result(fixture, budget)
        else:
            literal, bindings = production_literal(args, budget)
            terminal, result = compile_literal(literal, bindings, budget)
    except ResourceStop as exc:
        terminal = unknown_resource(exc)
        result = {"reason": {"phase": exc.phase, "cap": exc.cap,
                             "value": exc.value, "limit": exc.limit},
                  "checkpoint_contract": {"owner": "task292-producer"},
                  "forbidden_conclusions": dict(FORBIDDEN_CONCLUSIONS)}
    except (Stop, KeyError, ValueError, TypeError, FileNotFoundError,
            json.JSONDecodeError, UnicodeError) as exc:
        terminal = unknown_input(str(exc))
        result = {"reason": str(exc),
                  "checkpoint_contract": {"owner": "task292-producer"},
                  "forbidden_conclusions": dict(FORBIDDEN_CONCLUSIONS)}
    if target is not None:
        receipt = envelope(terminal, result)
        payload = canonical(receipt)
        try:
            budget.bump("serialized_bytes", len(payload), "receipt serialization")
        except ResourceStop as exc:
            terminal = unknown_resource(exc)
            result = {"reason": {"phase": exc.phase, "cap": exc.cap,
                                 "value": exc.value, "limit": exc.limit},
                      "checkpoint_contract": {"owner": "task292-producer"},
                      "forbidden_conclusions": dict(FORBIDDEN_CONCLUSIONS)}
        else:
            if type(result) is dict and "resource_meter" in result:
                result["resource_meter"] = budget.receipt()
        receipt = envelope(terminal, result)
        payload = canonical(receipt)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
    print("D292_PRODUCER_PASS terminal=" + terminal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
