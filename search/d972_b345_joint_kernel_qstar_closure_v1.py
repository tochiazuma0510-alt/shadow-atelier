"""Producer for the 157ee fixed-prefix whole-joint-kernel qstar certificate."""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import struct
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md")
TASK_SHA = "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4"
PREV = Path("search/d972_b345_triple_cube_raw_lambda_census_v1.py")
PREV_SHA = "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"
PREV_CHECKER = Path("search/check_d972_b345_triple_cube_raw_lambda_census_v1.py")
PREV_CHECKER_SHA = "677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce"
PREV_DRIVER = Path("search/d972_b345_triple_cube_raw_lambda_census_gha_driver_v1.g")
PREV_DRIVER_SHA = "29a31752d42bd3f5a0e7f27ca38495bdd54c9cc694d12ddf9fe637e8749975e9"
PREV_TASK = Path("sol/luna_task_157ed_b345_triple_cube_raw_lambda_census.md")
PREV_TASK_SHA = "15511f73e665a90f1e518383cb7bd218d8dd8e747026c498c3b4acce62837c2f"
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
SCHEMA = "d972-b345-joint-kernel-qstar-closure/v1"

TERMINALS = frozenset({
    "B345_JOINT_KERNEL_QSTAR_CLOSED",
    "B345_JOINT_KERNEL_QSTAR_ACTIVE",
    "B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE",
    "B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT",
})

P_RELATORS = [
    [-2,-2,1,1,2,1,2,1,1],
    [1,-2,-2,-2,-2,1,-2,-2,-2,-2],
    [-1,2,-1,-2,-1,-1,-2,-2,-1,-1,-2],
    [2,1,1,2,-1,2,-1,-1,2,-1,-1,2,-1],
    [-1,-2,-1,-1,-2,1,2,1,1,1,-2,-1,-1,-1],
]
G9_RELATORS = [
    [1,2,2,-1,2,2],
    [2,-1,-1,-2,-1,-1],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [2,1,-2,-2,-2,-2,-2,-2,-2,-2,1,2,1,-2,-2,-2,-2,-2,-2,-2,-2,1],
    [1,2,1,2,-1,-2,-1,-2,-1,-2,1,2,-1,-1,-1,-1,2,1,2,1,2,1,2,1,2,1,2,1,2,-1,2,1,1,1,1,2,-1,-2],
    [-1,-1,-1,2,1,2,-1,-2,-1,-2,-1,-2,-1,-2,-1,2,1,2,1,-2,-1,-1,-1,-2,1,-2,-1,-2,-1,-2,-1,-2,-1,-2,-1,-2,1,-2,1,-2],
    [1,-2,-1,-2,1,2,1,2,1,2,1,2,1,-2,-1,-2,1,1,1,1,1,1,-2,-1,-2,1,2,1,2,1,2,1,2,1,-2,-1,-2,1,1,1,1,1],
]
SPLIT_WORDS = [
    [1,-2,1,1,2,-1,-2,-2,1,-2,-1,-1,-2,-1,-1,-2,-2,1,-2,-2],
    [-1,-1,-2,-1,-1,2,1,2,1,1,2,1,2,2],
    [1,2,2,-1,2,2,1,1,2,1,1,2,-1,2,2,1,-2,-1,-1,2,-1],
    [-2,-2,-1,-2,-1,-1,-2,-1,-2,1,1,2,1,1,2],
]
FACTOR_PAYLOAD = [[504,2916,1469664], P_RELATORS, G9_RELATORS, SPLIT_WORDS]
FACTOR_PAYLOAD_SHA = "6eb95a6830b19e729c5e2a9b4f861fb6105ac0be1f1058cc566898d1b48758ba"
COMPLETE_RELATORS_SHA = "dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a"

EXPECTED = {
    "gamma_states": 243, "gamma_edges": 6318,
    "gamma_exponent": 9, "gamma_center": 27,
    "gamma_derived": 3, "gamma_cubes": 9,
    "gamma_frattini": 27, "gamma_frattini_quotient": 9,
    "action_relations": 104, "q0_relations": 19,
    "q0_order": 1469664, "P_order": 504, "G9_order": 2916,
}


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                ensure_ascii=True).encode("utf-8"))


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def require(value: Any, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def load_prev() -> Any:
    for path, digest in ((TASK, TASK_SHA), (PREV, PREV_SHA),
                         (PREV_CHECKER, PREV_CHECKER_SHA),
                         (PREV_DRIVER, PREV_DRIVER_SHA),
                         (PREV_TASK, PREV_TASK_SHA)):
        require((ROOT/path).is_file() and sha_file(ROOT/path) == digest,
                f"157ee authenticated pin: {path}")
    name = "_d972_157ee_pinned_157ed_producer"
    require(name not in sys.modules, "157ee module name unbound")
    spec = importlib.util.spec_from_file_location(name, ROOT/PREV)
    require(spec is not None and spec.loader is not None, "157ee module spec")
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None); raise
    return module


def pack_u16(rows: Iterable[int]) -> dict[str, Any]:
    values = [int(x) for x in rows]
    raw = b"".join(struct.pack("<H", x) for x in values)
    return {"encoding": "u16-le", "count": len(values),
            "byte_length": len(raw), "sha256": sha_bytes(raw),
            "base64": base64.b64encode(raw).decode("ascii"),
            "decoded_sha256": sha_obj(values)}


def pack_u8(rows: Iterable[int]) -> dict[str, Any]:
    values = [int(x) for x in rows]
    require(all(0 <= x <= 255 for x in values), "u8 range")
    raw = bytes(values)
    return {"encoding": "u8", "count": len(values),
            "byte_length": len(raw), "sha256": sha_bytes(raw),
            "base64": base64.b64encode(raw).decode("ascii"),
            "decoded_sha256": sha_obj(values)}


def pack_bytes(raw: bytes, encoding: str) -> dict[str, Any]:
    return {"encoding":encoding,"byte_length":len(raw),
            "sha256":sha_bytes(raw),
            "base64":base64.b64encode(raw).decode("ascii")}


def p_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]-1] for i in range(len(left)))


def p_inv(value: tuple[int, ...]) -> tuple[int, ...]:
    out = [0]*len(value)
    for index, image in enumerate(value, 1):
        out[image-1] = index
    return tuple(out)


def p_eval(word: Sequence[int], generators: Sequence[tuple[int, ...]]) \
        -> tuple[int, ...]:
    value = tuple(range(1, len(generators[0])+1))
    inverse = [p_inv(g) for g in generators]
    for letter in word:
        value = p_mul(value, generators[abs(letter)-1]
                      if letter > 0 else inverse[abs(letter)-1])
    return value


def enumerate_perm_group(generators: Sequence[tuple[int, ...]]) \
        -> tuple[list[tuple[int, ...]], dict[tuple[int, ...], int]]:
    identity = tuple(range(1, len(generators[0])+1))
    states = [identity]; ids = {identity: 0}
    for state in states:
        for generator in generators:
            value = p_mul(state, generator)
            if value not in ids:
                ids[value] = len(states); states.append(value)
    return states, ids


def substitute(old: Any, relator: Sequence[int], left: Sequence[int],
               right: Sequence[int]) -> list[int]:
    out: list[int] = []
    for letter in relator:
        word = left if abs(letter) == 1 else right
        out = old.reduce_word(out +
            (list(word) if letter > 0 else old.inv_word(word)))
    return out


def complete_relators(old: Any) -> list[list[int]]:
    p_rows = [substitute(old, row, SPLIT_WORDS[0], SPLIT_WORDS[1])
              for row in P_RELATORS]
    g_rows = [substitute(old, row, SPLIT_WORDS[2], SPLIT_WORDS[3])
              for row in G9_RELATORS]
    cross = [old.commutator(a, b) for a in SPLIT_WORDS[:2]
             for b in SPLIT_WORDS[2:]]
    split = [
        old.reduce_word([1]+old.inv_word(old.reduce_word(
            SPLIT_WORDS[0]+SPLIT_WORDS[2]))),
        old.reduce_word([2]+old.inv_word(old.reduce_word(
            SPLIT_WORDS[1]+SPLIT_WORDS[3]))),
    ]
    result = p_rows+g_rows+cross+split
    require(len(result) == 19 and sha_obj(result) == COMPLETE_RELATORS_SHA,
            "complete Q0 relator manifest")
    return result


class JointGroup:
    def __init__(self, old: Any, e3: Any, e4: Any,
                 contexts: Sequence[tuple[Any, Any]],
                 words: Sequence[Sequence[int]]) -> None:
        self.old, self.e3, self.e4 = old, e3, e4
        self.contexts = list(contexts); self.words = [list(x) for x in words]
        self.identity = (e3.identity, tuple(e4.identity for _ in contexts))
        self.generators = [self.eval(word) for word in self.words]
        self.states = [self.identity]
        self.ids = {self.key(self.identity): 0}
        self.parent: list[int | None] = [None]
        self.parent_generator: list[int | None] = [None]
        for state_id, state in enumerate(self.states):
            for generator_id, generator in enumerate(self.generators):
                value = self.mul(state, generator); key = self.key(value)
                if key not in self.ids:
                    self.ids[key] = len(self.states); self.states.append(value)
                    self.parent.append(state_id)
                    self.parent_generator.append(generator_id)
        require(len(self.states) == EXPECTED["gamma_states"],
                "Gamma state count")
        self.transitions = [[self.ids[self.key(self.mul(state, generator))]
                             for generator in self.generators]
                            for state in self.states]

    def blob(self, value: Any) -> bytes:
        return bytes(self.old._element_blob(value))

    def key(self, state: tuple[Any, tuple[Any, ...]]) -> tuple[bytes, ...]:
        return (self.blob(state[0]),)+tuple(self.blob(x) for x in state[1])

    def mul(self, left: Any, right: Any) -> Any:
        return (self.e3.mul(left[0], right[0]),
                tuple(self.e4.mul(left[1][i], right[1][i])
                      for i in range(len(self.contexts))))

    def inverse(self, value: Any) -> Any:
        return (self.e3.inverse(value[0]),
                tuple(self.e4.inverse(x) for x in value[1]))

    def eval(self, word: Sequence[int]) -> Any:
        return (self.e3.eval(self.old.embed_f2_pb3(word)),
                tuple(self.e4.eval(word, [left, right])
                      for left, right in self.contexts))

    def section_factors(self, state_id: int) -> list[int]:
        answer = []
        while state_id:
            generator = self.parent_generator[state_id]
            parent = self.parent[state_id]
            require(generator is not None and parent is not None,
                    "Gamma section parent")
            answer.append(generator); state_id = parent
        answer.reverse(); return answer

    def section_word(self, state_id: int) -> list[int]:
        out: list[int] = []
        for generator in self.section_factors(state_id):
            out = self.old.reduce_word(out+self.words[generator])
        return out

    def closure_ids(self, generators: Iterable[int]) -> set[int]:
        rows = list(dict.fromkeys(int(x) for x in generators))
        seen = {0}; queue = [0]
        for state in queue:
            for generator in rows:
                target = self.ids[self.key(self.mul(
                    self.states[state], self.states[generator]))]
                if target not in seen:
                    seen.add(target); queue.append(target)
        return seen

    def invariants(self) -> dict[str, Any]:
        inverse = [self.ids[self.key(self.inverse(x))] for x in self.states]
        def mul_id(a: int, b: int) -> int:
            return self.ids[self.key(self.mul(self.states[a], self.states[b]))]
        greedy: list[int] = []; subgroup = {0}
        for index in range(len(self.generators)):
            generator = self.ids[self.key(self.generators[index])]
            if generator not in subgroup:
                greedy.append(generator); subgroup = self.closure_ids(greedy)
        orders = []
        for value in range(len(self.states)):
            product = 0
            for exponent in range(1, 28):
                product = mul_id(product, value)
                if product == 0:
                    orders.append(exponent); break
        center = [value for value in range(len(self.states))
                  if all(mul_id(value, generator) == mul_id(generator, value)
                         for generator in greedy)]
        commutators = []
        for left in greedy:
            for right in greedy:
                commutators.append(mul_id(mul_id(inverse[left], inverse[right]),
                                          mul_id(left, right)))
        derived = self.closure_ids(commutators)
        cubes = self.closure_ids(mul_id(mul_id(x, x), x)
                                 for x in range(len(self.states)))
        frattini = self.closure_ids(derived | cubes)
        unseen = set(range(len(self.states))); conjugacy_sizes = []
        while unseen:
            seed = min(unseen); orbit = {seed}; queue = [seed]
            for value in queue:
                for generator in greedy:
                    target = mul_id(mul_id(inverse[generator], value), generator)
                    if target not in orbit:
                        orbit.add(target); queue.append(target)
            unseen -= orbit; conjugacy_sizes.append(len(orbit))
        x_state, y_state = self.eval([1]), self.eval([2])
        normal = True
        for outer in (x_state, y_state):
            outer_inverse = self.inverse(outer)
            for generator in greedy:
                conjugate = self.mul(self.mul(
                    outer_inverse, self.states[generator]), outer)
                normal &= self.key(conjugate) in self.ids
        depth = [0]*len(self.states)
        for state in range(1, len(self.states)):
            parent = self.parent[state]
            require(parent is not None, "Gamma parent depth")
            depth[state] = depth[parent]+1
        result = {
            "order": len(self.states),
            "edge_count": len(self.states)*len(self.generators),
            "generator_count": len(self.generators),
            "greedy_generator_state_ids": [x+1 for x in greedy],
            "greedy_generator_count": len(greedy),
            "max_section_factors": max(depth),
            "order_distribution": {str(k): v for k, v in
                                   sorted(Counter(orders).items())},
            "exponent": max(orders), "center_order": len(center),
            "derived_order": len(derived), "cube_subgroup_order": len(cubes),
            "frattini_order": len(frattini),
            "frattini_quotient_order": len(self.states)//len(frattini),
            "frattini_dimension_F3": 2,
            "derived_in_center": derived <= set(center),
            "conjugacy_class_size_distribution": {str(k): v for k, v in
                sorted(Counter(conjugacy_sizes).items())},
            "normal_under_x_y": bool(normal),
            "state_rows_sha256": sha_obj([[x.hex() for x in self.key(state)]
                                           for state in self.states]),
            "transition_rows_sha256": sha_obj(self.transitions),
        }
        require(result["order_distribution"] == {"1":1,"3":26,"9":216}
                and result["exponent"] == 9 and result["center_order"] == 27
                and result["derived_order"] == 3
                and result["cube_subgroup_order"] == 9
                and result["frattini_order"] == 27
                and result["frattini_quotient_order"] == 9
                and result["conjugacy_class_size_distribution"] ==
                    {"1":27,"3":72} and result["normal_under_x_y"] is True
                and result["max_section_factors"] == 4,
                "Gamma exact invariants")
        return result

    def public(self) -> dict[str, Any]:
        transitions = [x+1 for row in self.transitions for x in row]
        parents = [0 if x is None else x+1 for x in self.parent]
        generators = [0 if x is None else x+1 for x in self.parent_generator]
        state_rows = [self.key(state) for state in self.states]
        widths = [len(blob) for blob in state_rows[0]]
        require(all([len(blob) for blob in row] == widths
                    for row in state_rows), "Gamma canonical state widths")
        state_bytes = b"".join(blob for row in state_rows for blob in row)
        return {**self.invariants(),
                "transitions": pack_u16(transitions),
                "section_parent_states": pack_u16(parents),
                "section_parent_generators": pack_u8(generators),
                "canonical_states": {**pack_bytes(
                    state_bytes,"state-major exact blobs: E3 then 31 E4"),
                    "state_count":len(state_rows),
                    "factor_widths_bytes":widths,
                    "row_width_bytes":sum(widths)},
                "canonical_state_key": "E3 blob then 31 E4 blobs",
                "first_seen_BFS": True}


class ScalarEngine:
    def __init__(self, prev: Any, old: Any, e4: Any, oracle: Any,
                 words: Sequence[Sequence[int]], aliases: dict[str, int]) -> None:
        self.prev, self.old, self.e4, self.oracle = prev, old, e4, oracle
        self.words = [list(x) for x in words]; self.aliases = aliases
        self.leaves = prev.target_leaf_dp(old, e4, self.words)
        self.spec = {"a": (aliases["hexagon_1_fxy_0"]-1,
                           self.leaves["outer"]["h"]),
                     "b": (aliases["hexagon_1_fxz_0"]-1,
                           self.leaves["outer"]["C"]),
                     "c": (aliases["hexagon_1_fyz_0"]-1,
                           self.leaves["outer"]["C"])}
        z = old.inv_word(old.pp_words([[1],[2]])); mapping = old.cofaces(3)[0]
        def lift(word: Sequence[int]) -> list[int]:
            return old.word_substitute(old.embed_f2_pb3(word), mapping)
        operations = {"a": lambda w: old.f2_substitute(w,[1],[2]),
                      "b": lambda w: old.f2_substitute(w,[1],z),
                      "c": lambda w: old.f2_substitute(w,[2],z)}
        self.letters = {name: [old.fox_gradient_without_sections(
            lift(operation(word)), e4) for word in ([1],[2])]
            for name, operation in operations.items()}
        self.cache: dict[tuple[Any, ...], int] = {}

    def blob(self, value: Any) -> bytes:
        return bytes(self.old._element_blob(value))

    def token_data(self, name: str, kind: str, index: int) -> tuple[Any, Any]:
        if kind == "record":
            return (self.leaves[name]["gradients"][index],
                    self.leaves[name]["values"][index])
        gradient, value = self.letters[name][index]
        return gradient, value

    def token_scalar(self, name: str, kind: str, index: int, sign: int,
                     left: Any) -> int:
        key = (name, kind, index, sign, self.blob(left))
        if key in self.cache:
            return self.cache[key]
        gradient, value = self.token_data(name, kind, index); coefficient = 1
        if sign < 0:
            left = self.e4.mul(left, self.e4.inverse(value)); coefficient = 2
        total = 0
        for (component, element), term in gradient.items():
            total = (total + coefficient*int(term)*self.oracle.lookup(
                component, self.e4.mul(left, element))) % 3
        self.cache[key] = total; return total

    def route(self, name: str, tokens: Sequence[tuple[str,int,int]]) -> int:
        prefix = self.e4.identity; total = 0; outer = self.spec[name][1]
        for kind, index, sign in tokens:
            total = (total+self.token_scalar(
                name, kind, index, sign, self.e4.mul(outer, prefix))) % 3
            _, value = self.token_data(name, kind, index)
            prefix = self.e4.mul(prefix, value if sign > 0
                                 else self.e4.inverse(value))
        require(prefix == self.e4.identity, "typed relation route value")
        return total

    def vector(self, tokens: Sequence[tuple[str,int,int]]) -> tuple[int,int,int]:
        return tuple(self.route(name, tokens) for name in ("a","b","c"))  # type: ignore[return-value]

    @staticmethod
    def target(vector: Sequence[int]) -> int:
        return (int(vector[2])-int(vector[1])+int(vector[0])) % 3

    def edge_scalar(self, name: str, state_value: Any, generator: int) -> int:
        outer = self.spec[name][1]
        return self.token_scalar(name, "record", generator, 1,
                                 self.e4.mul(outer, state_value))


def token_word(old: Any, words: Sequence[Sequence[int]],
               token: tuple[str,int,int]) -> list[int]:
    kind, index, sign = token
    word = list(words[index]) if kind == "record" else ([1] if index == 0 else [2])
    return word if sign > 0 else old.inv_word(word)


def materialize_tokens(old: Any, words: Sequence[Sequence[int]],
                       tokens: Sequence[tuple[str,int,int]]) -> list[int]:
    out: list[int] = []
    for token in tokens:
        out = old.reduce_word(out+token_word(old, words, token))
    return out


def direct_canary(prev: Any, old: Any, e3: Any, e4: Any, contexts: Sequence[Any],
                  prefix: dict[str, Any], oracle: Any, word: Sequence[int],
                  expected: int, label: str, budget: Any) -> dict[str, Any]:
    require(e3.eval(old.embed_f2_pb3(word)) == e3.identity and
            all(e4.eval(word, [left,right]) == e4.identity
                for left,right in contexts), "direct canary typing")
    detail = old.affine_target6_formula(word, e4, include_gradient=True)
    raw = detail.pop("_direct_gradient")
    require(detail.pop("_direct_value") == e4.identity and
            detail["formula_equals_direct"] is True, "direct canary formula")
    direct = oracle.sparse(raw)
    remainder = old._affine_probe_remainder(
        raw, prefix, prefix["base_source_key"], budget)
    nf = prev.public_remainder_coefficient(remainder)
    require(direct == nf == expected, "direct/NF relation canary")
    return {"label": label, "word_length": len(word),
            "word_sha256": sha_obj(list(word)), "scalar": direct,
            "remainder_support": len(remainder),
            "remainder_sha256": sha_obj(sorted(remainder.items())),
            "formula_direct_equal": True, "NF_equal": True}


def internal_relations(group: JointGroup, engine: ScalarEngine) \
        -> tuple[dict[str, Any], list[tuple[str,int,int]],
                 list[tuple[str,int,int]] | None, list[int]]:
    potentials: list[tuple[int,int,int] | None] = [None]*len(group.states)
    potentials[0] = (0,0,0); queue = [0]
    for state in queue:
        assert potentials[state] is not None
        for generator, target in enumerate(group.transitions[state]):
            edge = tuple(engine.edge_scalar(
                name, group.states[state][1][engine.spec[name][0]], generator)
                for name in ("a","b","c"))
            value = tuple((potentials[state][i]+edge[i]) % 3 for i in range(3))
            if potentials[target] is None:
                potentials[target] = value; queue.append(target)
    require(all(value is not None for value in potentials),
            "internal potential covers Gamma")
    rows = []; first_active = None; first_active_tokens = None
    for state, transitions in enumerate(group.transitions):
        for generator, target in enumerate(transitions):
            edge = tuple(engine.edge_scalar(
                name, group.states[state][1][engine.spec[name][0]], generator)
                for name in ("a","b","c"))
            discrepancy = tuple((potentials[state][i]+edge[i]-
                                 potentials[target][i]) % 3 for i in range(3))
            scalar = engine.target(discrepancy)
            row = [state+1,generator+1,target+1,*discrepancy,scalar]
            rows.append(row)
            if scalar and first_active is None:
                first_active = ["internal", len(rows), scalar]
                first_active_tokens = (
                    [('record',x,1) for x in group.section_factors(state)] +
                    [('record',generator,1)] +
                    [('record',x,-1) for x in reversed(
                        group.section_factors(target))])
    flat = [value for row in rows for value in row[3:6]]
    public = {"row_count": len(rows), "all_component_zero": all(x == 0 for x in flat),
              "target_scalar_counts": {str(v): sum(row[6] == v for row in rows)
                                        for v in range(3)},
              "component_vector_distribution": {str(vector): sum(
                  tuple(row[3:6]) == vector for row in rows)
                  for vector in sorted(set(tuple(row[3:6]) for row in rows))},
              "rows_sha256": sha_obj(rows),
              "packed_component_vectors": pack_u8(flat),
              "presentation_complete_for_record_generators": True,
              "first_active": first_active}
    state, generator, target = 1, 0, group.transitions[1][0]
    tokens = ([('record',x,1) for x in group.section_factors(state)] +
              [('record',generator,1)] +
              [('record',x,-1) for x in reversed(group.section_factors(target))])
    return public, tokens, first_active_tokens, rows[26]


def action_relations(group: JointGroup, engine: ScalarEngine) \
        -> tuple[dict[str, Any], list[list[tuple[str,int,int]]]]:
    outer = [group.eval([1]), group.eval([2])]
    rows = []; tokens_all = []
    for record, generator in enumerate(group.generators):
        for letter, value in enumerate(outer):
            for orientation in (1,-1):
                if orientation == 1:
                    conjugate = group.mul(group.mul(group.inverse(value),
                                                     generator), value)
                    tokens = [('letter',letter,-1),('record',record,1),
                              ('letter',letter,1)]
                else:
                    conjugate = group.mul(group.mul(value, generator),
                                          group.inverse(value))
                    tokens = [('letter',letter,1),('record',record,1),
                              ('letter',letter,-1)]
                target = group.ids[group.key(conjugate)]
                tokens += [('record',x,-1)
                           for x in reversed(group.section_factors(target))]
                vector = engine.vector(tokens); scalar = engine.target(vector)
                rows.append([record+1,letter+1,orientation,target+1,
                             len(group.section_factors(target)),*vector,scalar])
                tokens_all.append(tokens)
    public = {"row_count": len(rows),
              "all_component_zero": all(row[-1] == 0 and row[5:8] == [0,0,0]
                                         for row in rows),
              "rows": rows, "rows_sha256": sha_obj(rows),
              "target_scalar_counts": {str(v): sum(row[-1] == v for row in rows)
                                        for v in range(3)},
              "conjugation_order": "record, x/y, g^-1*r*g then g*r*g^-1"}
    return public, tokens_all


def factor_presentation(q3: dict[str, Any], old: Any) -> tuple[
        dict[str, Any], list[list[int]]]:
    require(sha_obj(FACTOR_PAYLOAD) == FACTOR_PAYLOAD_SHA,
            "factor payload SHA")
    marked = q3["coarse_models"]["Q0"]["marked_permutations"]
    require(len(marked) == 2 and all(len(row) == 36 for row in marked),
            "Q0 marked permutations")
    qgens = [tuple(row) for row in marked]
    pgens = [tuple(row[:9]) for row in marked]
    ggens = [tuple(value-9 for value in row[9:]) for row in marked]
    p_states, _ = enumerate_perm_group(pgens)
    g_states, _ = enumerate_perm_group(ggens)
    require(len(p_states) == 504 and len(g_states) == 2916 and
            len(p_states)*len(g_states) == 1469664 and
            int(q3["coarse_models"]["Q0"]["order_decimal"]) == 1469664,
            "Q0 direct factor orders")
    pid, gid = tuple(range(1,10)), tuple(range(1,28))
    split_values = [(p_eval(word,pgens),p_eval(word,ggens))
                    for word in SPLIT_WORDS]
    require(split_values == [(pgens[0],gid),(pgens[1],gid),
                             (pid,ggens[0]),(pid,ggens[1])],
            "Q0 split-word images")
    require(all(p_eval(row,pgens) == pid for row in P_RELATORS) and
            all(p_eval(row,ggens) == gid for row in G9_RELATORS),
            "factor relator images")
    relators = complete_relators(old)
    qid = tuple(range(1,37))
    require(all(p_eval(row,qgens) == qid for row in relators),
            "complete relators in Q0")
    return {"factor_payload_sha256": FACTOR_PAYLOAD_SHA,
            "P_order": 504, "G9_order": 2916, "Q0_order": 1469664,
            "P_state_count": len(p_states), "G9_state_count": len(g_states),
            "P_relator_count": len(P_RELATORS),
            "G9_relator_count": len(G9_RELATORS),
            "split_word_lengths": list(map(len,SPLIT_WORDS)),
            "split_word_sha256": sha_obj(SPLIT_WORDS),
            "complete_relator_count": len(relators),
            "complete_relators_sha256": sha_obj(relators),
            "completeness_argument":
              "factor presentations plus cross commutation and x/y splitting",
            "producer_factor_enumeration": "independent marked-permutation BFS"}, relators


def q0_relations(group: JointGroup, engine: ScalarEngine,
                 relators: Sequence[Sequence[int]]) \
        -> tuple[dict[str, Any], list[list[tuple[str,int,int]]]]:
    relation_ids = [group.ids[group.key(group.eval(row))] for row in relators]
    normal_generators = list(dict.fromkeys(relation_ids))
    x, y = group.eval([1]), group.eval([2])
    rounds = []
    while True:
        subgroup = group.closure_ids(normal_generators); additions = []
        for outer in (x,y):
            inverse = group.inverse(outer)
            for generator in normal_generators:
                value = group.mul(group.mul(inverse, group.states[generator]), outer)
                target = group.ids[group.key(value)]
                if target not in subgroup and target not in additions:
                    additions.append(target)
        if not additions:
            break
        normal_generators += additions
        rounds.append({"added":len(additions),
                       "order_after":len(group.closure_ids(normal_generators))})
    require(len(group.closure_ids(normal_generators)) == 243,
            "Q0 relator defects normally generate Gamma")
    rows = []; token_rows = []
    for ordinal, (relator, target) in enumerate(zip(relators,relation_ids),1):
        tokens = [('letter',abs(x)-1,1 if x>0 else -1) for x in relator]
        tokens += [('record',x,-1)
                   for x in reversed(group.section_factors(target))]
        vector = engine.vector(tokens); scalar = engine.target(vector)
        rows.append([ordinal,len(relator),target+1,
                     len(group.section_factors(target)),*vector,scalar])
        token_rows.append(tokens)
    public = {"row_count": len(rows), "rows": rows,
              "rows_sha256": sha_obj(rows),
              "all_component_zero": all(row[4:7] == [0,0,0]
                                         and row[-1] == 0 for row in rows),
              "relator_image_subgroup_order": len(group.closure_ids(relation_ids)),
              "relator_image_normal_closure_order":
                  len(group.closure_ids(normal_generators)),
              "normal_closure_rounds": rounds,
              "target_scalar_counts": {str(v):sum(row[-1] == v for row in rows)
                                        for v in range(3)}}
    return public, token_rows


def decode_u16(field: dict[str, Any], label: str) -> list[int]:
    require(set(field) == {"encoding","count","byte_length","sha256",
                           "base64","decoded_sha256"} and
            field["encoding"] == "u16-le", label+" u16 schema")
    raw = base64.b64decode(field["base64"], validate=True)
    require(len(raw) == field["byte_length"] == 2*field["count"] and
            sha_bytes(raw) == field["sha256"], label+" u16 bytes")
    values = [struct.unpack_from("<H",raw,2*i)[0]
              for i in range(field["count"])]
    require(sha_obj(values) == field["decoded_sha256"],
            label+" u16 decoded")
    return values


def decode_u8(field: dict[str, Any], label: str) -> list[int]:
    require(set(field) == {"encoding","count","byte_length","sha256",
                           "base64","decoded_sha256"} and
            field["encoding"] == "u8", label+" u8 schema")
    raw = base64.b64decode(field["base64"], validate=True)
    values = list(raw)
    require(len(raw) == field["byte_length"] == field["count"] and
            sha_bytes(raw) == field["sha256"] and
            sha_obj(values) == field["decoded_sha256"], label+" u8 bytes")
    return values


def validate_packed_cayley(public: dict[str, Any], order: int,
                           generator_count: int) -> list[list[int]]:
    transitions_flat = decode_u16(public["transitions"],"Cayley transitions")
    parents = decode_u16(public["section_parent_states"],"Cayley parents")
    generators = decode_u8(public["section_parent_generators"],
                           "Cayley parent generators")
    require(len(transitions_flat) == order*generator_count and
            len(parents) == len(generators) == order,
            "Cayley packed dimensions")
    transitions = [transitions_flat[i*generator_count:(i+1)*generator_count]
                   for i in range(order)]
    require(all(1 <= x <= order for row in transitions for x in row) and
            parents[0] == generators[0] == 0,"Cayley ranges/root")
    for state in range(1,order):
        require(1 <= parents[state] <= state and
                1 <= generators[state] <= generator_count and
                transitions[parents[state]-1][generators[state]-1] == state+1,
                "Cayley first-seen section tree")
    states = public["canonical_states"]
    require(set(states) == {"encoding","byte_length","sha256","base64",
                            "state_count","factor_widths_bytes",
                            "row_width_bytes"} and
            states["encoding"] == "state-major exact blobs: E3 then 31 E4" and
            states["state_count"] == order and
            states["row_width_bytes"] == sum(states["factor_widths_bytes"]) and
            all(isinstance(x,int) and x > 0
                for x in states["factor_widths_bytes"]),
            "Cayley canonical state schema")
    raw = base64.b64decode(states["base64"],validate=True)
    require(len(raw) == states["byte_length"] == order*states["row_width_bytes"]
            and sha_bytes(raw) == states["sha256"],
            "Cayley canonical state bytes")
    widths = states["factor_widths_bytes"]; rows = []; offset = 0
    for _ in range(order):
        row = []
        for width in widths:
            row.append(raw[offset:offset+width]); offset += width
        rows.append(row)
    require(len({tuple(row) for row in rows}) == order and
            public["state_rows_sha256"] ==
                sha_obj([[blob.hex() for blob in row] for row in rows]) and
            public["transition_rows_sha256"] ==
                sha_obj([[x-1 for x in row] for row in transitions]),
            "Cayley canonical state/transition binding")
    return transitions


def validate_internal_public(public: dict[str, Any],
                             transitions: Sequence[Sequence[int]],
                             require_zero: bool) -> None:
    require(set(public) == {"row_count","all_component_zero",
            "target_scalar_counts","component_vector_distribution",
            "rows_sha256","packed_component_vectors",
            "presentation_complete_for_record_generators","first_active"},
            "internal relation schema")
    components = decode_u8(public["packed_component_vectors"],
                           "internal components")
    row_count = sum(map(len,transitions))
    require(public["row_count"] == row_count and len(components) == 3*row_count,
            "internal relation dimensions")
    rows = []; first = None
    for ordinal in range(row_count):
        state = ordinal//len(transitions[0]); generator = ordinal%len(transitions[0])
        vector = components[3*ordinal:3*ordinal+3]
        require(all(x in (0,1,2) for x in vector),"internal F3 components")
        scalar = (vector[2]-vector[1]+vector[0])%3
        rows.append([state+1,generator+1,transitions[state][generator],
                     *vector,scalar])
        if scalar and first is None: first = ["internal",ordinal+1,scalar]
    vectors = [tuple(row[3:6]) for row in rows]
    require(public["rows_sha256"] == sha_obj(rows) and
            public["target_scalar_counts"] ==
                {str(v):sum(row[6] == v for row in rows) for v in range(3)} and
            public["component_vector_distribution"] ==
                {str(vector):sum(x == vector for x in vectors)
                 for vector in sorted(set(vectors))} and
            public["first_active"] == first and
            public["all_component_zero"] == all(x == 0 for x in components) and
            public["presentation_complete_for_record_generators"] is True and
            (not require_zero or public["all_component_zero"] is True),
            "internal relation binding")


def validate_completed_core(receipt: dict[str, Any]) -> None:
    gamma = receipt["gamma"]
    require(gamma["order"] == 243 and gamma["edge_count"] == 6318 and
            gamma["generator_count"] == 26 and gamma["exponent"] == 9 and
            gamma["center_order"] == 27 and gamma["derived_order"] == 3 and
            gamma["cube_subgroup_order"] == 9 and
            gamma["frattini_order"] == 27 and
            gamma["frattini_quotient_order"] == 9 and
            gamma["normal_under_x_y"] is True and
            gamma["max_section_factors"] == 4 and
            gamma["canonical_state_key"] == "E3 blob then 31 E4 blobs" and
            gamma["first_seen_BFS"] is True,"completed Gamma invariants")
    transitions = validate_packed_cayley(gamma,243,26)
    validate_internal_public(receipt["internal_relations"],transitions,
                             receipt["terminal_token"] ==
                             "B345_JOINT_KERNEL_QSTAR_CLOSED")
    action = receipt["action_relations"]
    require(set(action) == {"row_count","all_component_zero","rows",
            "rows_sha256","target_scalar_counts","conjugation_order"} and
            action["row_count"] == len(action["rows"]) == 104 and
            action["conjugation_order"] ==
                "record, x/y, g^-1*r*g then g*r*g^-1" and
            action["rows_sha256"] == sha_obj(action["rows"]),
            "completed action ledger")
    for ordinal,row in enumerate(action["rows"]):
        require(len(row) == 9 and row[:3] ==
                [ordinal//4+1,(ordinal//2)%2+1,1 if ordinal%2 == 0 else -1]
                and row[-1] == (row[7]-row[6]+row[5])%3,
                "action orientation/components")
    require(action["target_scalar_counts"] ==
            {str(v):sum(row[-1] == v for row in action["rows"])
             for v in range(3)} and
            action["all_component_zero"] == all(
                row[5:8] == [0,0,0] for row in action["rows"]),
            "action aggregate")
    q0 = receipt["q0_presentation"]
    require(q0["factor_payload_sha256"] == FACTOR_PAYLOAD_SHA and
            q0["P_order"] == q0["P_state_count"] == 504 and
            q0["G9_order"] == q0["G9_state_count"] == 2916 and
            q0["Q0_order"] == 1469664 and q0["P_relator_count"] == 5 and
            q0["G9_relator_count"] == 8 and q0["complete_relator_count"] == 19 and
            q0["split_word_sha256"] == sha_obj(SPLIT_WORDS) and
            q0["complete_relators_sha256"] == COMPLETE_RELATORS_SHA,
            "completed Q0 presentation")
    qrows = receipt["q0_relations"]
    require(qrows["row_count"] == len(qrows["rows"]) == 19 and
            qrows["rows_sha256"] == sha_obj(qrows["rows"]) and
            qrows["relator_image_normal_closure_order"] == 243 and
            all(len(row) == 8 and row[0] == i+1 and
                row[-1] == (row[6]-row[5]+row[4])%3
                for i,row in enumerate(qrows["rows"])) and
            qrows["target_scalar_counts"] ==
                {str(v):sum(row[-1] == v for row in qrows["rows"])
                 for v in range(3)} and
            qrows["all_component_zero"] == all(
                row[4:7] == [0,0,0] for row in qrows["rows"]),
            "completed Q0 relation ledger")
    require(receipt["base_target6"]["lambda"] == 2 and
            receipt["base_target6"]["negative_base_lambda"] == 1 and
            receipt["base_target6"]["direct_NF_equal"] is True and
            receipt["record_manifest"]["record_count"] == 26 and
            receipt["record_manifest"]["all_Q0_identity"] is True,
            "completed base/kernel binding")


TOP_KEYS = {"schema","task_sha256","terminal_token","status","reason",
            "claim","fixed_prefix_only","claim_flags","pins","source_hashes",
            "base_q3_replay",
            "normalized_inverse_fibre","directed_base_support","directed_surgery",
            "prefix","lambda_oracle","base_target6","record_manifest",
            "context_registry","gamma",
            "internal_relations","action_relations","q0_presentation",
            "q0_relations","direct_canaries","theorem_boundary","performance",
            "resource_guards","partial"}


def base_receipt(pins: dict[str,str], budget: Any) -> dict[str,Any]:
    return {"schema":SCHEMA,"task_sha256":TASK_SHA,
            "terminal_token":"B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT",
            "status":"B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT",
            "reason":"initializing","claim":"none","fixed_prefix_only":True,
            "claim_flags":{"whole_joint_kernel_fixed_prefix_closed":False,
                "new_qstar_direction_found":False,"full_D2_claimed":False,
                "full_H3_claimed":False,"lift_nonexistence_claimed":False,
                "B4_A_claimed":False,"B4_B_claimed":False},
            "pins":pins,"source_hashes":{"producer_path":str(Path(__file__).resolve().relative_to(ROOT)).replace('\\','/'),
                "producer_sha256":sha_file(Path(__file__).resolve())},
            "base_q3_replay":{},"normalized_inverse_fibre":{},
            "directed_base_support":{},"directed_surgery":{},"prefix":{},
            "lambda_oracle":{},"base_target6":{},"record_manifest":{},
            "context_registry":{},
            "gamma":{},"internal_relations":{},"action_relations":{},
            "q0_presentation":{},"q0_relations":{},"direct_canaries":[],
            "theorem_boundary":{"fixed_prefix_only":True,
                "joint_kernel":"ker(Q0 x E3 x 31 E4 contexts)",
                "full_D2_claimed":False,"full_H3_claimed":False,
                "lift_nonexistence_claimed":False,"B4_A_claimed":False,
                "B4_B_claimed":False,
                "raw_lambda_global_E4_invariance_claimed":False},
            "performance":budget.public(),"resource_guards":{},"partial":{}}


def validate_receipt(receipt: dict[str,Any]) -> None:
    require(set(receipt) == TOP_KEYS and receipt["schema"] == SCHEMA and
            receipt["task_sha256"] == TASK_SHA and
            receipt["terminal_token"] in TERMINALS and
            receipt["status"] == receipt["terminal_token"] and
            receipt["fixed_prefix_only"] is True,
            "157ee exact envelope")
    flags = receipt["claim_flags"]
    require(flags["full_D2_claimed"] is False and
            flags["full_H3_claimed"] is False and
            flags["lift_nonexistence_claimed"] is False and
            flags["B4_A_claimed"] is False and flags["B4_B_claimed"] is False,
            "157ee no overclaim")
    terminal = receipt["terminal_token"]
    if terminal in {"B345_JOINT_KERNEL_QSTAR_CLOSED",
                    "B345_JOINT_KERNEL_QSTAR_ACTIVE"}:
        validate_completed_core(receipt)
    if terminal == "B345_JOINT_KERNEL_QSTAR_CLOSED":
        require(receipt["reason"] == "joint_kernel_presentation_potential_zero" and
                receipt["claim"] == "fixed_prefix_whole_joint_kernel_qstar_closed" and
                flags["whole_joint_kernel_fixed_prefix_closed"] is True and
                flags["new_qstar_direction_found"] is False and
                receipt["internal_relations"]["all_component_zero"] is True and
                receipt["action_relations"]["all_component_zero"] is True and
                receipt["q0_relations"]["all_component_zero"] is True and
                receipt["base_target6"]["lambda"] == 2,
                "157ee closed terminal derivation")
    elif terminal == "B345_JOINT_KERNEL_QSTAR_ACTIVE":
        require(receipt["reason"] == "defining_relation_nonzero" and
                receipt["claim"] == "positive_new_fixed_prefix_qstar_direction" and
                flags["whole_joint_kernel_fixed_prefix_closed"] is False and
                flags["new_qstar_direction_found"] is True and
                not (receipt["internal_relations"]["all_component_zero"] and
                     receipt["action_relations"]["all_component_zero"] and
                     receipt["q0_relations"]["all_component_zero"]) and
                any(row["scalar"] in (1,2) for row in receipt["direct_canaries"]),
                "157ee active terminal derivation")
    elif terminal == "B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE":
        resource = receipt["partial"].get("resource",{})
        require(receipt["claim"] == "none" and
                flags["whole_joint_kernel_fixed_prefix_closed"] is False and
                flags["new_qstar_direction_found"] is False and
                set(receipt["partial"]) == {"phase","resource"} and
                set(resource) == {"cap_key","cap_reason","cap_limit",
                                  "observed_count","trigger_relation"} and
                receipt["reason"] == resource["cap_key"] ==
                    resource["cap_reason"] and
                resource["trigger_relation"] in {"gt","ge"} and
                ((resource["trigger_relation"] == "gt" and
                  resource["observed_count"] > resource["cap_limit"]) or
                 (resource["trigger_relation"] == "ge" and
                  resource["observed_count"] >= resource["cap_limit"])),
                "157ee resource boundary")
    else:
        require(receipt["reason"] == "authenticated_external_input" and
                receipt["claim"] == "none" and
                flags["whole_joint_kernel_fixed_prefix_closed"] is False and
                flags["new_qstar_direction_found"] is False,
                "157ee input boundary")


def run(q3_path: Path, seconds: float = 18000.0) -> dict[str,Any]:
    prev = load_prev(); budget = prev.Budget(seconds)
    pins = {"task_sha256":TASK_SHA,"157ed_producer_sha256":PREV_SHA,
            "157ed_checker_sha256":PREV_CHECKER_SHA,
            "157ed_driver_sha256":PREV_DRIVER_SHA,
            "157ed_task_sha256":PREV_TASK_SHA,"q3_artifact_sha256":Q3_SHA}
    receipt = base_receipt(pins,budget); phase = "authenticated_input"
    try:
        q3, old = prev.authenticated_input(q3_path)
        e3,e4,_ = old.reconstruct_quotients(q3)
        receipt["base_q3_replay"] = old.replay_base_q3(q3,e3,e4)
        normalized, raw_source_key, _ = old.normalized_inverse_fibre(q3,e4)
        receipt["normalized_inverse_fibre"] = normalized
        contexts,aliases,context_public = old.cheap_context_registry(e4)
        require(len(contexts) == 31 and len(context_public["named_uses"]) == 46,
                "joint context registry")
        receipt["context_registry"] = context_public
        words = [list(row["word"]) for row in q3["correction_fibre"]["records"]
                 if row["word"]]
        require(len(words) == 26 and len({tuple(x) for x in words}) == 26,
                "record manifest")
        q0_generators = [tuple(row) for row in
                         q3["coarse_models"]["Q0"]["marked_permutations"]]
        q0_identity = tuple(range(1, 37))
        require(len(q0_generators) == 2 and
                all(p_eval(word, q0_generators) == q0_identity
                    for word in words), "record words lie in kernel of Q0")
        receipt["record_manifest"] = {"record_count":26,
            "words_sha256":sha_obj(words),"record_order":"q3 nonempty rows 2..27",
            "total_letters":sum(map(len,words)),
            "lengths":list(map(len,words)),"all_Q0_identity":True}
        phase = "fresh_immutable_prefix"
        print("D972_B345_JOINT_KERNEL_QSTAR_PHASE fresh_immutable_prefix",flush=True)
        prefix, dependent = prev.build_instrumented_prefix(
            old,e4,budget,raw_source_key)
        receipt["directed_base_support"] = prefix["directed_base_support"]
        receipt["directed_surgery"] = prefix["directed_surgery"]
        receipt["prefix"] = {"counts":prev.PREFIX_COUNTS,
            "accounting":prefix["accounting"],
            "basis_gate":old.affine_basis_gate(prefix["basis"],prefix["pool"]),
            "prefix_pool_checkpoint":len(prefix["pool"].values),
            "dependent_events":dependent,
            "dependent_event_count":len(dependent),
            "dependent_event_sha256":sha_obj(dependent),
            "fresh_not_imported":True,"source_sha256":prev.STRONG_SHA}
        phase = "raw_lambda_oracle"
        oracle = prev.RawLambdaOracle(old,prefix,prev.validate_qstar_label(
            prev.QSTAR_LABEL,e4.degree+e4.pc.n),budget)
        pool = prefix["pool"]
        pivot_zero: list[int] = []
        for pivot in sorted(prefix["basis"].rows, key=pool.pivot_order):
            row_data = prefix["basis"].rows[pivot]
            row = row_data[0] if isinstance(row_data, tuple) else row_data
            pivot_zero.append(oracle.packed(row))
        require(pivot_zero == [0]*prev.PREFIX_COUNTS["pivots"],
                "pivot row lambda annihilation")
        dependent_zero: list[int] = []
        for event in dependent:
            packed: dict[int,int] = {}
            for component,blob_hex,coefficient in event["raw_column"]:
                identifier = pool.ids.get(bytes.fromhex(blob_hex))
                require(identifier is not None,
                        "dependent event pool binding")
                packed[old.pack_vector_key(component,identifier)] = coefficient
            remainder0 = old.affine_full_remainder(
                packed,prefix["basis"],pool,budget)
            value0 = oracle.packed(packed)
            require(not remainder0 and value0 == 0,
                    "dependent event lambda annihilation")
            dependent_zero.append(value0)
        require(dependent_zero == [0]*16,"dependent lambda vector")
        oracle.public.update({
            "pivot_annihilation_count":len(pivot_zero),
            "pivot_annihilation_sha256":sha_obj(pivot_zero),
            "dependent_annihilation_count":len(dependent_zero),
            "dependent_annihilation_sha256":sha_obj(dependent_zero),
        })
        receipt["lambda_oracle"] = oracle.public
        mapping = old.cofaces(3)[0]
        r0 = old.word_substitute(old.embed_f2_pb3(
            old.hexagon_words(old.FIXED_WORD)[0]),mapping)
        base_raw,base_value = old.fox_gradient_without_sections(r0,e4)
        require(base_value == e4.identity,"base target6 quotient")
        remainder = old._affine_probe_remainder(
            base_raw,prefix,prefix["base_source_key"],budget)
        base_lambda = oracle.sparse(base_raw)
        require(base_lambda == prev.public_remainder_coefficient(remainder) == 2,
                "base target6 qstar sign")
        receipt["base_target6"] = {"quotient_identity":True,"lambda":2,
            "negative_base_lambda":1,"remainder_support":len(remainder),
            "remainder_sha256":sha_obj(sorted(remainder.items())),
            "raw_gradient_support":len(base_raw),
            "raw_gradient_sha256":sha_obj(sorted(
                ([c,old._element_blob(v).hex(),int(x)%3]
                 for (c,v),x in base_raw.items()),key=lambda z:(z[0],z[1]))),
            "direct_NF_equal":True}
        phase = "finite_joint_presentation"
        group = JointGroup(old,e3,e4,contexts,words)
        receipt["gamma"] = group.public()
        engine = ScalarEngine(prev,old,e4,oracle,words,aliases)
        internal,internal_tokens,internal_active_tokens,_ = \
            internal_relations(group,engine)
        receipt["internal_relations"] = internal
        actions,action_tokens = action_relations(group,engine)
        receipt["action_relations"] = actions
        q0_public,relators = factor_presentation(q3,old)
        receipt["q0_presentation"] = q0_public
        q0_rows,q0_tokens = q0_relations(group,engine,relators)
        receipt["q0_relations"] = q0_rows
        all_active: list[tuple[str,int,int,list[tuple[str,int,int]]]] = []
        if internal["first_active"] is not None:
            _,ordinal,scalar = internal["first_active"]
            require(internal_active_tokens is not None,
                    "internal active relation witness")
            all_active.append(("internal",ordinal,scalar,
                               internal_active_tokens))
        for ordinal,(row,tokens) in enumerate(zip(actions["rows"],action_tokens),1):
            if row[-1]: all_active.append(("action",ordinal,row[-1],tokens))
        for ordinal,(row,tokens) in enumerate(zip(q0_rows["rows"],q0_tokens),1):
            if row[-1]: all_active.append(("q0",ordinal,row[-1],tokens))
        canary_specs: list[tuple[str,int,list[tuple[str,int,int]],int]] = []
        if all_active:
            category,ordinal,scalar,tokens = all_active[0]
            canary_specs.append((category,ordinal,tokens,scalar))
        else:
            canary_specs.extend([
                ("internal",1,internal_tokens,0),
                ("action",53,action_tokens[52],0),
                ("action",104,action_tokens[103],0),
                ("q0",1,q0_tokens[0],0),
                ("q0",18,q0_tokens[17],0),
            ])
        phase = "direct_canaries"
        budget.check(phase,force=True)
        receipt["direct_canaries"] = [direct_canary(
            prev,old,e3,e4,contexts,prefix,oracle,
            materialize_tokens(old,words,tokens),expected,
            f"{category}:{ordinal}",budget)
            for category,ordinal,tokens,expected in canary_specs]
        closed = (internal["all_component_zero"] and
                  actions["all_component_zero"] and
                  q0_rows["all_component_zero"] and not all_active)
        if closed:
            receipt["terminal_token"] = receipt["status"] = \
                "B345_JOINT_KERNEL_QSTAR_CLOSED"
            receipt["reason"] = "joint_kernel_presentation_potential_zero"
            receipt["claim"] = "fixed_prefix_whole_joint_kernel_qstar_closed"
            receipt["claim_flags"]["whole_joint_kernel_fixed_prefix_closed"] = True
        else:
            receipt["terminal_token"] = receipt["status"] = \
                "B345_JOINT_KERNEL_QSTAR_ACTIVE"
            receipt["reason"] = "defining_relation_nonzero"
            receipt["claim"] = "positive_new_fixed_prefix_qstar_direction"
            receipt["claim_flags"]["new_qstar_direction_found"] = True
        receipt["theorem_boundary"]["presentation_layers"] = {
            "Gamma_full_Cayley_relations":6318,
            "x_y_action_relations":104,"complete_Q0_relations":19,
            "Q0_relator_defects_normally_generate_Gamma":True,
            "mu_is_homomorphism_on_joint_kernel":True}
    except prev.AffineInput:
        receipt["terminal_token"] = receipt["status"] = \
            "B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT"
        receipt["reason"] = "authenticated_external_input"
        receipt["claim"] = "none"; receipt["partial"] = {"phase":phase}
    except BaseException as exc:
        if hasattr(exc,"cap_key") and hasattr(exc,"cap_limit"):
            cap_key = str(getattr(exc,"cap_key")); reason = str(getattr(exc,"reason",cap_key))
            require(reason == cap_key,"resource reason/key")
            receipt["terminal_token"] = receipt["status"] = \
                "B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE"
            receipt["reason"] = reason; receipt["claim"] = "none"
            receipt["partial"] = {"phase":phase,"resource":{
                "cap_key":cap_key,"cap_reason":reason,
                "cap_limit":int(getattr(exc,"cap_limit")),
                "observed_count":int(getattr(exc,"observed_count",0)),
                "trigger_relation":str(getattr(exc,"trigger_relation","gt"))}}
            receipt["resource_guards"] = {"hit":True,"reason":reason}
        else:
            raise
    receipt["performance"] = budget.public()
    validate_receipt(receipt)
    return receipt


def self_test() -> None:
    require(sha_obj(FACTOR_PAYLOAD) == FACTOR_PAYLOAD_SHA,
            "selftest factor payload")
    class Toy:
        @staticmethod
        def reduce_word(word: Sequence[int]) -> list[int]:
            out=[]
            for x in word:
                if out and out[-1] == -x: out.pop()
                else: out.append(x)
            return out
        @staticmethod
        def inv_word(word: Sequence[int]) -> list[int]:
            return [-x for x in reversed(word)]
        def commutator(self,a:Sequence[int],b:Sequence[int])->list[int]:
            return self.reduce_word(self.inv_word(a)+self.inv_word(b)+list(a)+list(b))
    rels = complete_relators(Toy())
    require(len(rels) == 19 and sha_obj(rels) == COMPLETE_RELATORS_SHA,
            "selftest complete relators")
    # Exact small nonabelian S3 packed Cayley fixture.
    a=(2,1,3); b=(2,3,1)
    states,ids=enumerate_perm_group([a,b]); generators=[a,b]
    require(len(states)==6 and p_eval([1,1],[a,b])==tuple(range(1,4)) and
            p_eval([2,2,2],[a,b])==tuple(range(1,4)),"selftest S3")
    transitions=[[ids[p_mul(state,g)]+1 for g in generators]
                 for state in states]
    parents=[0]; parent_generators=[0]
    for state in range(1,6):
        found=None
        for parent,row in enumerate(transitions[:state]):
            for generator,target in enumerate(row):
                if target == state+1: found=(parent+1,generator+1); break
            if found is not None: break
        require(found is not None,"selftest S3 section")
        parents.append(found[0]); parent_generators.append(found[1])
    state_raw=b"".join(bytes(state) for state in states)
    toy_group={"transitions":pack_u16(x for row in transitions for x in row),
      "section_parent_states":pack_u16(parents),
      "section_parent_generators":pack_u8(parent_generators),
      "canonical_states":{**pack_bytes(
          state_raw,"state-major exact blobs: E3 then 31 E4"),
          "state_count":6,"factor_widths_bytes":[3],"row_width_bytes":3},
      "state_rows_sha256":sha_obj([[bytes(state).hex()] for state in states]),
      "transition_rows_sha256":sha_obj([[x-1 for x in row]
                                         for row in transitions])}
    validate_packed_cayley(toy_group,6,2)
    for mutation in ("transition","section","state"):
        bad=json.loads(json.dumps(toy_group))
        if mutation == "transition":
            values=decode_u16(bad["transitions"],"toy transition")
            values[0]=1; bad["transitions"]=pack_u16(values)
            bad["transition_rows_sha256"]=sha_obj(
                [[x-1 for x in values[i*2:i*2+2]] for i in range(6)])
        elif mutation == "section":
            values=decode_u16(bad["section_parent_states"],"toy section")
            values[1]=2; bad["section_parent_states"]=pack_u16(values)
        else:
            raw=bytearray(base64.b64decode(bad["canonical_states"]["base64"]))
            raw[3:6]=raw[0:3]
            bad["canonical_states"].update(pack_bytes(
                bytes(raw),"state-major exact blobs: E3 then 31 E4"))
            bad["state_rows_sha256"]=sha_obj(
                [[bytes(raw[3*i:3*i+3]).hex()] for i in range(6)])
        try: validate_packed_cayley(bad,6,2)
        except RuntimeError: pass
        else: raise RuntimeError("selftest Cayley mutation "+mutation)

    # Production-shape completed fixture through the same terminal/core validator.
    order=243; generator_count=26
    tr=[[((state+generator+1)%order)+1 for generator in range(generator_count)]
        for state in range(order)]
    state_rows=[[bytes([state])] for state in range(order)]
    gamma={"order":243,"edge_count":6318,"generator_count":26,
      "greedy_generator_state_ids":[2,3],"greedy_generator_count":2,
      "max_section_factors":4,"order_distribution":{"1":1,"3":26,"9":216},
      "exponent":9,"center_order":27,"derived_order":3,
      "cube_subgroup_order":9,"frattini_order":27,
      "frattini_quotient_order":9,"frattini_dimension_F3":2,
      "derived_in_center":True,
      "conjugacy_class_size_distribution":{"1":27,"3":72},
      "normal_under_x_y":True,
      "state_rows_sha256":sha_obj([[x.hex() for x in row]
                                     for row in state_rows]),
      "transition_rows_sha256":sha_obj([[x-1 for x in row] for row in tr]),
      "transitions":pack_u16(x for row in tr for x in row),
      "section_parent_states":pack_u16([0]+list(range(1,order))),
      "section_parent_generators":pack_u8([0]+[1]*(order-1)),
      "canonical_states":{**pack_bytes(bytes(range(243)),
          "state-major exact blobs: E3 then 31 E4"),"state_count":243,
          "factor_widths_bytes":[1],"row_width_bytes":1},
      "canonical_state_key":"E3 blob then 31 E4 blobs",
      "first_seen_BFS":True}
    internal_rows=[[state+1,generator+1,tr[state][generator],0,0,0,0]
                   for state in range(243) for generator in range(26)]
    internal={"row_count":6318,"all_component_zero":True,
      "target_scalar_counts":{"0":6318,"1":0,"2":0},
      "component_vector_distribution":{"(0, 0, 0)":6318},
      "rows_sha256":sha_obj(internal_rows),
      "packed_component_vectors":pack_u8([0]*(6318*3)),
      "presentation_complete_for_record_generators":True,"first_active":None}
    action_rows=[[ordinal//4+1,(ordinal//2)%2+1,
       1 if ordinal%2==0 else -1,1,0,0,0,0,0] for ordinal in range(104)]
    action={"row_count":104,"all_component_zero":True,"rows":action_rows,
      "rows_sha256":sha_obj(action_rows),
      "target_scalar_counts":{"0":104,"1":0,"2":0},
      "conjugation_order":"record, x/y, g^-1*r*g then g*r*g^-1"}
    qrows=[[i+1,1,1,0,0,0,0,0] for i in range(19)]
    qrelations={"row_count":19,"rows":qrows,"rows_sha256":sha_obj(qrows),
      "all_component_zero":True,"relator_image_subgroup_order":243,
      "relator_image_normal_closure_order":243,"normal_closure_rounds":[],
      "target_scalar_counts":{"0":19,"1":0,"2":0}}
    qpublic={"factor_payload_sha256":FACTOR_PAYLOAD_SHA,"P_order":504,
      "G9_order":2916,"Q0_order":1469664,"P_state_count":504,
      "G9_state_count":2916,"P_relator_count":5,"G9_relator_count":8,
      "split_word_lengths":list(map(len,SPLIT_WORDS)),
      "split_word_sha256":sha_obj(SPLIT_WORDS),"complete_relator_count":19,
      "complete_relators_sha256":COMPLETE_RELATORS_SHA,
      "completeness_argument":"fixture","producer_factor_enumeration":"fixture"}
    completed={key:{} for key in TOP_KEYS}
    completed.update({"schema":SCHEMA,"task_sha256":TASK_SHA,
      "terminal_token":"B345_JOINT_KERNEL_QSTAR_CLOSED",
      "status":"B345_JOINT_KERNEL_QSTAR_CLOSED",
      "reason":"joint_kernel_presentation_potential_zero",
      "claim":"fixed_prefix_whole_joint_kernel_qstar_closed",
      "fixed_prefix_only":True,"claim_flags":{
       "whole_joint_kernel_fixed_prefix_closed":True,
       "new_qstar_direction_found":False,"full_D2_claimed":False,
       "full_H3_claimed":False,"lift_nonexistence_claimed":False,
       "B4_A_claimed":False,"B4_B_claimed":False},"gamma":gamma,
      "internal_relations":internal,"action_relations":action,
      "q0_presentation":qpublic,"q0_relations":qrelations,
      "base_target6":{"lambda":2,"negative_base_lambda":1,
                      "direct_NF_equal":True},
      "record_manifest":{"record_count":26,"all_Q0_identity":True},
      "direct_canaries":[{"scalar":0}],"partial":{}})
    validate_receipt(completed)
    for outer,key in (("gamma","order"),
                      ("action_relations","conjugation_order"),
                      ("q0_presentation","P_order"),
                      ("q0_presentation","split_word_sha256"),
                      ("q0_presentation","complete_relators_sha256"),
                      ("base_target6","lambda")):
        bad=json.loads(json.dumps(completed)); bad[outer][key]="mutated"
        try: validate_receipt(bad)
        except RuntimeError: pass
        else: raise RuntimeError("selftest completed mutation "+outer+"."+key)
    active=json.loads(json.dumps(completed)); active.update({
      "terminal_token":"B345_JOINT_KERNEL_QSTAR_ACTIVE",
      "status":"B345_JOINT_KERNEL_QSTAR_ACTIVE",
      "reason":"defining_relation_nonzero",
      "claim":"positive_new_fixed_prefix_qstar_direction"})
    active["claim_flags"]["whole_joint_kernel_fixed_prefix_closed"]=False
    active["claim_flags"]["new_qstar_direction_found"]=True
    active["q0_relations"]["rows"][0][4:8]=[1,0,0,1]
    active["q0_relations"]["rows_sha256"]=sha_obj(active["q0_relations"]["rows"])
    active["q0_relations"]["all_component_zero"]=False
    active["q0_relations"]["target_scalar_counts"]={"0":18,"1":1,"2":0}
    active["direct_canaries"]=[{"scalar":1}]
    validate_receipt(active)
    resource=json.loads(json.dumps(completed)); resource.update({
      "terminal_token":"B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE",
      "status":"B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE",
      "reason":"toy_cap","claim":"none",
      "partial":{"phase":"toy","resource":{"cap_key":"toy_cap",
        "cap_reason":"toy_cap","cap_limit":3,"observed_count":4,
        "trigger_relation":"gt"}}})
    resource["claim_flags"]["whole_joint_kernel_fixed_prefix_closed"]=False
    validate_receipt(resource)
    fake = {key:None for key in TOP_KEYS}
    fake.update({"schema":SCHEMA,"task_sha256":TASK_SHA,
        "terminal_token":"B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT",
        "status":"B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT",
        "reason":"authenticated_external_input","claim":"none",
        "fixed_prefix_only":True,"claim_flags":{
          "whole_joint_kernel_fixed_prefix_closed":False,
          "new_qstar_direction_found":False,"full_D2_claimed":False,
          "full_H3_claimed":False,"lift_nonexistence_claimed":False,
          "B4_A_claimed":False,"B4_B_claimed":False},"partial":{}})
    validate_receipt(fake)
    mutated=dict(fake);mutated["extra"]=1
    try: validate_receipt(mutated)
    except RuntimeError: pass
    else: raise RuntimeError("selftest extra schema mutation")
    print("D972_B345_JOINT_KERNEL_QSTAR_PRODUCER_SELFTEST_PASS "
          "factor_relators=19 nonabelian_fixture=S3 cayley_mutations=3 "
          "completed_core_mutations=6 terminals=4 schema_mutations=1")


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("q3",nargs="?");parser.add_argument("output",nargs="?")
    parser.add_argument("remaining_seconds",nargs="?",type=float,default=18000.0)
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:
        self_test(); return
    require(args.q3 is not None and args.output is not None,"producer arguments")
    output=(ROOT/Path(args.output)).resolve()
    require(output==(ROOT/Path("ci/out/d972_b345_joint_kernel_qstar_closure_v1.json")).resolve(),
            "fixed producer output")
    receipt=run((ROOT/Path(args.q3)).resolve(),args.remaining_seconds)
    raw=json.dumps(receipt,sort_keys=True,separators=(",",":"),ensure_ascii=True)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(raw+"\n",encoding="ascii")
    require(json.loads(output.read_text(encoding="ascii"))==receipt,"producer readback")
    print(receipt["terminal_token"])
    print("D972_B345_JOINT_KERNEL_QSTAR_PRODUCER_EXIT_ZERO")


if __name__ == "__main__":
    main()
