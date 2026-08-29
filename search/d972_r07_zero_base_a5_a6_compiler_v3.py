#!/usr/bin/env python3
"""Direct-relator A5/A6 compiler for the authenticated R07 owners.

Production only.  The 6,441 literal task198 relators are evaluated by the
frozen v12 runtime; task193-v3 supplies the actual pointed target.  No
serialized evaluator, action map, fixture, retry, or A7 assertion is an
accepted input.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import stat
import sys
import time
import types
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-zero-base-a5-a6-compiler/v3"
PRODUCER_LINE = "R07_ZERO_BASE_A5_A6_COMPILER_V3_PRODUCER_TERMINAL"
MEMBER = "R07_ZERO_BASE_A5_A6_MEMBER"
NONMEMBER = "R07_ZERO_BASE_A5_A6_NONMEMBER"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
ROWS = 6441
MODULUS = 3

TASK193_SCHEMA = "d972-r07-second-frattini-affine-prefix-compiler/v3"
TASK193_TERMINAL = "R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V3"
TASK193_CHECK_SCHEMA = TASK193_SCHEMA + "/checker-verdict/v3"
TASK193_PRODUCER_PIN = (
    "search/d972_r07_second_frattini_affine_prefix_compiler_v3.py", 2826,
    "1ac65ca533e11ac39def79c84de0bbdcb018d463ac10bca6158db254a61da741")
TASK193_CHECKER_PIN = (
    "crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v3.py", 2792,
    "5b3c5b3e607077e0bebcf0153c592465983ba210b768c93ea62aeb2201c905c6")
TASK193_DRIVER_PIN = (
    "search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v3.g", 5798,
    "c11074bd1e634aa38d4d164699542e17087e659115c31b8f5b8cc322dc5dfd84")
TASK198_WRAPPER_PIN = (
    "search/d972_r07_word_independent_successor_kernel_v12.py", 7209,
    "816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5")

TASK198_DEFAULTS = {
    "receipt": "ci/in/d972_r07_seven_context_roof_presentation_v1.json",
    "manifest": "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
    "producer": "ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
    "checker": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
    "verdict": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",
}
BLOCKS = ("H1", "H2", "P")
BLOCK_DOMAIN = {"H1": "1", "H2": "1", "P": "3"}
BLOCK_CONTEXT = {"H1": 0, "H2": 0, "P": 5}
ACTION_LETTERS = (1, -1, 2, -2)
TARGET_ORACLE_STRIDE = 64


class InputStop(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    pass


def need(value: bool, message: str) -> None:
    if value is not True:
        raise InputStop(message)


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha(canon(value))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value); body.pop("self_digest_sha256", None)
    body["self_digest_sha256"] = digest(body)
    return body


def add(left: dict[str, int], right: dict[str, int], scale: int = 1
        ) -> dict[str, int]:
    out = dict(left)
    for key, raw in right.items():
        value = (out.get(key, 0) + int(scale) * int(raw)) % MODULUS
        if value: out[key] = value
        else: out.pop(key, None)
    return out


def scaled(row: dict[str, int], factor: int) -> dict[str, int]:
    return {key: int(value) * int(factor) % MODULUS
            for key, value in row.items() if int(value) * int(factor) % MODULUS}


def word_reduce(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for raw in word:
        letter = int(raw); need(letter in ACTION_LETTERS, "word:letter")
        if out and out[-1] == -letter: out.pop()
        else: out.append(letter)
    return tuple(out)


def word_mul(*words: Sequence[int]) -> tuple[int, ...]:
    return word_reduce(letter for word in words for letter in word)


def word_inv(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(-int(letter) for letter in reversed(tuple(word)))


def _inside(raw: str | Path, area: str | None = None) -> Path:
    text = str(raw).replace("\\", "/"); path = Path(text)
    need(not path.is_absolute() and ".." not in path.parts and "." not in path.parts,
         "path:lexical")
    try:
        value = (ROOT / path).resolve(strict=True)
        value.relative_to(ROOT.resolve())
        if area is not None:
            value.relative_to((ROOT / area).resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise InputStop("path:containment:" + text) from exc
    cursor = ROOT
    for part in path.parts:
        cursor /= part; info = os.lstat(cursor)
        need(not stat.S_ISLNK(info.st_mode), "path:symlink")
    return value


def read_json(raw: str | Path, label: str) -> tuple[dict[str, Any], dict[str, Any]]:
    path = _inside(raw, "ci/in")
    before = path.stat(); data = path.read_bytes(); after = path.stat()
    need((before.st_dev, before.st_ino, before.st_size,
          getattr(before, "st_mtime_ns", 0)) ==
         (after.st_dev, after.st_ino, after.st_size,
          getattr(after, "st_mtime_ns", 0)), label + ":changed")
    try: value = json.loads(data.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InputStop(label + ":json") from exc
    need(type(value) is dict, label + ":object")
    return value, {"path": path.relative_to(ROOT).as_posix(),
                   "bytes": len(data), "sha256": sha(data)}


def check_pin(pin: tuple[str, int, str], label: str) -> dict[str, Any]:
    path = _inside(pin[0])
    raw = path.read_bytes()
    need(len(raw) == pin[1] and sha(raw) == pin[2], label + ":pin")
    return {"path": pin[0], "bytes": pin[1], "sha256": pin[2]}


def check_self(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256", value.get("self_digest"))
    body = dict(value); body.pop("self_digest_sha256", None); body.pop("self_digest", None)
    need(type(claimed) is str and claimed == digest(body), label + ":seal")


def load_task198() -> types.ModuleType:
    """Restore the frozen v12 executable core without invoking its main."""
    wrapper_path = _inside(TASK198_WRAPPER_PIN[0])
    wrapper_raw = wrapper_path.read_bytes()
    need(len(wrapper_raw) == TASK198_WRAPPER_PIN[1] and
         sha(wrapper_raw) == TASK198_WRAPPER_PIN[2], "task198:v12_wrapper_pin")
    spec = importlib.util.spec_from_file_location("r07_task198_v12_wrapper", wrapper_path)
    need(spec is not None and spec.loader is not None, "task198:wrapper_loader")
    wrapper = importlib.util.module_from_spec(spec); spec.loader.exec_module(wrapper)
    source = Path(wrapper.SOURCE); raw = source.read_bytes()
    need(len(raw) == int(wrapper.SOURCE_BYTES) and
         sha(raw) == str(wrapper.SOURCE_SHA256), "task198:frozen_source_pin")
    for index, pair in enumerate(wrapper.PATCHES):
        need(type(pair) is tuple and len(pair) == 2, "task198:patch_shape")
        old, new = pair
        need(type(old) is bytes and type(new) is bytes and old and new and old != new,
             "task198:patch_nonempty:" + str(index))
        need(raw.count(old) == 1, "task198:patch_cardinality:" + str(index))
        raw = raw.replace(old, new)
    module = types.ModuleType("r07_task198_v12_runtime_for_a5_v3")
    module.__file__ = str(source); module.__package__ = None
    exec(compile(raw, str(source), "exec"), module.__dict__, module.__dict__)
    for name in ("Meter", "AuthorityAdapter", "Runtime", "BoundaryLedger",
                 "AffineState", "row_key", "decode_token", "correlate",
                 "element_blob"):
        need(hasattr(module, name), "task198:runtime_symbol:" + name)
    return module


def load_task193(receipt_path: str, verdict_path: str
                 ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source_ids = {"producer": check_pin(TASK193_PRODUCER_PIN, "task193:producer"),
                  "checker": check_pin(TASK193_CHECKER_PIN, "task193:checker"),
                  "driver": check_pin(TASK193_DRIVER_PIN, "task193:driver")}
    receipt, receipt_id = read_json(receipt_path, "task193:receipt")
    verdict, verdict_id = read_json(verdict_path, "task193:verdict")
    check_self(receipt, "task193:receipt"); check_self(verdict, "task193:verdict")
    need(receipt.get("schema") == TASK193_SCHEMA and receipt.get("status") == "PASS" and
         receipt.get("terminal") == TASK193_TERMINAL, "task193:positive")
    need(verdict.get("schema") == TASK193_CHECK_SCHEMA and
         verdict.get("status") == "PASS" and
         verdict.get("terminal") == TASK193_TERMINAL, "task193:checker_positive")
    bound = verdict.get("receipt", {})
    need(bound.get("bytes") == receipt_id["bytes"] and
         bound.get("sha256") == receipt_id["sha256"], "task193:verdict_binding")
    claims = verdict.get("claims", {})
    need(claims.get("independent_task193_replay") is True and
         claims.get("pointed_rows") is True, "task193:checker_claims")
    need(receipt.get("claims", {}).get("lift") == "NONE" and
         receipt.get("claims", {}).get("fake") == "NONE" and
         receipt.get("claims", {}).get("Ihara") == "NONE", "task193:frontier")
    return receipt, {"receipt": receipt_id, "verdict": verdict_id,
                     "sources": source_ids}, verdict


class Budget:
    def __init__(self, limit: int):
        self.limit = int(limit); self.count = 0; self.started = time.monotonic()
        self.last_progress = -1.0e99

    def bump(self, amount: int, phase: str) -> None:
        self.count += int(amount)
        if self.count > self.limit:
            raise ResourceStop("phase=" + phase + ":cap=max_operations:value=" +
                               str(self.count) + ":limit=" + str(self.limit))

    def progress(self, phase: str, cursor: int, pre: int, joint: int,
                 labels: int) -> None:
        now = time.monotonic()
        if now - self.last_progress < 60.0: return
        self.last_progress = now
        print("A5_V3_PROGRESS phase=" + phase + " cursor=" + str(cursor) +
              " pre_rank=" + str(pre) + " joint_rank=" + str(joint) +
              " labels=" + str(labels) + " operations=" + str(self.count) +
              " elapsed=" + format(now - self.started, ".1f"), flush=True)


class WordDAG:
    def __init__(self):
        self.nodes: list[tuple[str, Any, Any]] = [("lit", (), None)]
        self.literal_cache: dict[tuple[int, ...], int] = {(): 0}
        self.op_cache: dict[tuple[str, int, int], int] = {}
        self.materialized: dict[int, tuple[int, ...]] = {0: ()}

    def literal(self, word: Sequence[int]) -> int:
        value = word_reduce(word)
        if value not in self.literal_cache:
            self.literal_cache[value] = len(self.nodes)
            self.nodes.append(("lit", value, None))
        return self.literal_cache[value]

    def concat(self, left: int, right: int) -> int:
        if left == 0: return right
        if right == 0: return left
        key = ("mul", int(left), int(right))
        if key not in self.op_cache:
            self.op_cache[key] = len(self.nodes); self.nodes.append(key)
        return self.op_cache[key]

    def inverse(self, node: int) -> int:
        key = ("inv", int(node), 0)
        if key not in self.op_cache:
            self.op_cache[key] = len(self.nodes); self.nodes.append(key)
        return self.op_cache[key]

    def word(self, node: int) -> tuple[int, ...]:
        if node in self.materialized: return self.materialized[node]
        kind, left, right = self.nodes[node]
        if kind == "lit": value = tuple(left)
        elif kind == "mul": value = word_mul(self.word(int(left)), self.word(int(right)))
        else: value = word_inv(self.word(int(left)))
        self.materialized[node] = value; return value


class Echelon:
    """Insertion-order GF(3) echelon with an external proof-node payload."""
    def __init__(self, budget: Budget, proof: "ProofDAG"):
        self.budget, self.proof = budget, proof
        self.pivots: list[str] = []
        self.rows: dict[str, dict[str, int]] = {}
        self.nodes: dict[str, int] = {}

    def reduce(self, source: dict[str, int]) -> tuple[dict[str, int], dict[str, int]]:
        row = {key: int(value) % MODULUS for key, value in source.items()
               if int(value) % MODULUS}
        coefficients: dict[str, int] = {}
        for pivot in self.pivots:
            factor = row.get(pivot, 0)
            if factor:
                row = add(row, self.rows[pivot], -factor)
                coefficients[pivot] = (coefficients.get(pivot, 0) + factor) % MODULUS
                self.budget.bump(len(self.rows[pivot]), "echelon_reduce")
        return row, {key: value for key, value in coefficients.items() if value}

    def insert(self, source: dict[str, int], source_node: int
               ) -> tuple[str, int] | None:
        remainder, old = self.reduce(source)
        if not remainder: return None
        pivot = min(remainder); factor = 1 if remainder[pivot] == 1 else 2
        stored = scaled(remainder, factor)
        node = self.proof.combine(source_node, factor,
                                  [(self.nodes[key], -factor * value)
                                   for key, value in old.items()])
        self.pivots.append(pivot); self.rows[pivot] = stored; self.nodes[pivot] = node
        self.budget.bump(len(stored), "echelon_insert")
        return pivot, node

    def solution(self, target: dict[str, int]) -> tuple[dict[str, int], int] | None:
        remainder, coefficients = self.reduce(target)
        if remainder: return None
        node = self.proof.linear([(self.nodes[key], value)
                                  for key, value in coefficients.items()])
        return coefficients, node

    def dual(self, target: dict[str, int]) -> tuple[dict[str, int], int, dict[str, int]]:
        remainder, _ = self.reduce(target)
        need(bool(remainder), "dual:member")
        free = min(remainder); dual: dict[str, int] = {free: 1}
        for pivot in reversed(self.pivots):
            value = sum(int(coefficient) * dual.get(key, 0)
                        for key, coefficient in self.rows[pivot].items()) % MODULUS
            if value: dual[pivot] = (-value) % MODULUS
            else: dual.pop(pivot, None)
        pairing = sum(int(value) * dual.get(key, 0)
                      for key, value in target.items()) % MODULUS
        need(pairing != 0 and all(sum(int(value) * dual.get(key, 0)
                                      for key, value in row.items()) % MODULUS == 0
                                  for row in self.rows.values()), "dual:replay")
        return dual, pairing, remainder


class ProofDAG:
    """Formal coefficient/boundary ancestry; no row is serialized as an input."""
    def __init__(self):
        self.nodes: list[dict[str, Any]] = [{"kind": "zero"}]

    def seed(self, relator: int) -> int:
        self.nodes.append({"kind": "seed", "relator": int(relator)})
        return len(self.nodes) - 1

    def boundary(self, block: str, relation: int, translation_word: Sequence[int]) -> int:
        self.nodes.append({"kind": "boundary", "block": block,
                           "relation": int(relation),
                           "translation_word": list(translation_word)})
        return len(self.nodes) - 1

    def action(self, parent: int, letter: int) -> int:
        self.nodes.append({"kind": "action", "parent": int(parent),
                           "letter": int(letter)})
        return len(self.nodes) - 1

    def linear(self, terms: Sequence[tuple[int, int]]) -> int:
        cleaned: dict[int, int] = {}
        for node, raw in terms:
            value = (cleaned.get(int(node), 0) + int(raw)) % MODULUS
            if value: cleaned[int(node)] = value
            else: cleaned.pop(int(node), None)
        if not cleaned: return 0
        self.nodes.append({"kind": "linear",
                           "terms": [[node, value] for node, value in cleaned.items()]})
        return len(self.nodes) - 1

    def combine(self, source: int, factor: int,
                old: Sequence[tuple[int, int]]) -> int:
        return self.linear([(source, factor), *old])

    def expand(self, node: int) -> tuple[dict[tuple[tuple[int, ...], int], int],
                                         dict[tuple[str, int, tuple[int, ...]], int]]:
        coefficient: dict[tuple[tuple[int, ...], int], int] = {}
        boundary: dict[tuple[str, int, tuple[int, ...]], int] = {}
        stack: list[tuple[int, int, tuple[int, ...]]] = [(int(node), 1, ())]
        while stack:
            current, scalar, prefix = stack.pop(); scalar %= MODULUS
            if not scalar or current == 0: continue
            item = self.nodes[current]; kind = item["kind"]
            if kind == "seed":
                key = (prefix, int(item["relator"]))
                value = (coefficient.get(key, 0) + scalar) % MODULUS
                if value: coefficient[key] = value
                else: coefficient.pop(key, None)
            elif kind == "boundary":
                key = (str(item["block"]), int(item["relation"]),
                       tuple(int(x) for x in item["translation_word"]))
                value = (boundary.get(key, 0) + scalar) % MODULUS
                if value: boundary[key] = value
                else: boundary.pop(key, None)
            elif kind == "action":
                stack.append((int(item["parent"]), scalar,
                              word_mul(prefix, (int(item["letter"]),))))
            elif kind == "linear":
                for child, value in item["terms"]:
                    stack.append((int(child), scalar * int(value), prefix))
            else:
                raise InputStop("proof:kind")
        return coefficient, boundary


def _state_signature(state: Any) -> tuple[Any, tuple[Any, ...]]:
    return state.a, tuple(sorted((int(component), element, int(value) % MODULUS)
                                 for (component, element), value in state.u.items()
                                 if int(value) % MODULUS))


class OuterUniverse:
    """Task193 label space reconstructed through the live task198 quotient."""
    def __init__(self, helper: Any, runtime: Any, boundary: Any, meter: Any,
                 domain: str, roster: list[dict[str, Any]], words: WordDAG,
                 budget: Budget):
        self.h, self.runtime, self.boundary, self.meter = helper, runtime, boundary, meter
        self.domain, self.context = domain, 0 if domain == "1" else 5
        self.q = runtime.quotient(self.context); self.degree = 36 if domain == "1" else 144
        self.words, self.budget = words, budget
        self.states: list[Any] = []; self.word_nodes: list[int | None] = []
        self.by_base: dict[str, list[int]] = {}; self.equal_cache: dict[Any, bool] = {}
        self.inner = Echelon(budget, ProofDAG())
        for ordinal, public in enumerate(roster):
            state = self.decode(public)
            self.states.append(state); self.word_nodes.append(None)
            self.by_base.setdefault(self.h.element_blob(state.a).hex(), []).append(ordinal)
        need(bool(self.states), "task193:empty_affine_roster:" + domain)

    def split_element(self, raw: bytes) -> Any:
        need(len(raw) == (40 if self.degree == 36 else 154), "affine:element_width")
        return raw[:self.degree], raw[self.degree:]

    def decode(self, public: dict[str, Any]) -> Any:
        need(type(public) is dict and type(public.get("base")) is str and
             type(public.get("chain")) is list, "affine:public_shape")
        base = self.split_element(bytes.fromhex(public["base"])); local: dict[Any, int] = {}
        for pair in public["chain"]:
            need(type(pair) is list and len(pair) == 2, "affine:chain_pair")
            raw = bytes.fromhex(str(pair[0])); value = int(pair[1]) % MODULUS
            need(len(raw) >= 5 and raw[:1] == b"R" and raw[1] == int(self.domain),
                 "affine:chain_tag")
            width = int.from_bytes(raw[3:5], "big")
            need(len(raw) == 5 + width, "affine:chain_width")
            key = (int(raw[2]), self.split_element(raw[5:]))
            if value: local[key] = (local.get(key, 0) + value) % MODULUS
        return self.h.AffineState(self.q, base, {key: value for key, value in local.items() if value})

    def bind_word(self, label: int, node: int) -> None:
        need(0 <= int(label) < len(self.states), "affine:label_range")
        if self.word_nodes[int(label)] is None: self.word_nodes[int(label)] = int(node)

    def _inner_row(self, local: dict[Any, int]) -> dict[str, int]:
        return {self.h.row_key(self.context, int(component), element): int(value) % MODULUS
                for (component, element), value in local.items() if int(value) % MODULUS}

    def _equal(self, left: Any, right: Any) -> bool:
        if left.a != right.a: return False
        difference = self.h.add_local(left.u, right.u, -1)
        if not difference: return True
        signature = tuple(sorted((int(c), e, int(v) % MODULUS)
                                 for (c, e), v in difference.items()))
        if signature in self.equal_cache: return self.equal_cache[signature]
        target = self._inner_row(difference)
        while True:
            remainder, _ = self.inner.reduce(target)
            if not remainder:
                self.equal_cache[signature] = True; return True
            dual, _pair, _ = self.inner.dual(target)
            correlation = self.h.correlate(self.boundary, dual, self.meter)
            selected = correlation.get("selected")
            if selected is None:
                self.equal_cache[signature] = False; return False
            context, relation, text, _scalar = selected
            need(int(context) == self.context, "inner_boundary:context")
            seed = self.boundary.seed_by_context_relation[(int(context), int(relation))]
            translation = self.h.decode_token(str(text))
            row = seed.translate(translation)
            inserted = self.inner.insert(row, 0)
            need(inserted is not None, "inner_boundary:rank")

    def intern(self, state: Any, word_node: int | None = None) -> int:
        blob = self.h.element_blob(state.a).hex()
        for label in self.by_base.get(blob, []):
            other = self.states[label]
            if _state_signature(state) == _state_signature(other) or self._equal(state, other):
                if word_node is not None: self.bind_word(label, word_node)
                return label
        label = len(self.states); self.states.append(state); self.word_nodes.append(word_node)
        self.by_base.setdefault(blob, []).append(label); self.budget.bump(1, "outer_label")
        return label

    def public_state(self, label: int) -> dict[str, Any]:
        state = self.states[int(label)]
        chain = []
        for (component, element), value in sorted(state.u.items(), key=lambda item:
                                                   (item[0][0], self.h.element_blob(item[0][1]))):
            raw = (b"R" + bytes((int(self.domain), int(component))) +
                   len(self.h.element_blob(element)).to_bytes(2, "big") +
                   self.h.element_blob(element))
            chain.append([raw.hex(), int(value) % MODULUS])
        return {"base": self.h.element_blob(state.a).hex(), "chain": chain}

    def label_word(self, label: int) -> tuple[int, ...]:
        node = self.word_nodes[int(label)]
        need(node is not None, "affine:missing_word_ancestry")
        return self.words.word(int(node))


def zkey(block: str, component: int, label: int) -> str:
    return "z|" + block + "|" + str(int(component)) + "|" + str(int(label))


def etakey(occurrence: int, label: int) -> str:
    return "eta|" + str(int(occurrence)) + "|" + str(int(label))


def ckey(block: str, label: int) -> str:
    return "c|" + block + "|" + str(int(label))


def parse_sparse_key(key: str) -> tuple[str, ...]:
    return tuple(key.split("|"))


class DirectEngine:
    def __init__(self, helper: Any, authority: Any, runtime: Any, boundary: Any,
                 task193: dict[str, Any], budget: Budget):
        self.h, self.authority, self.runtime = helper, authority, runtime
        self.boundary, self.task193, self.budget = boundary, task193, budget
        self.words = WordDAG(); self.proof = ProofDAG()
        labels = task193.get("affine_labels", {}).get("first_encounter_roster", {})
        need(type(labels) is dict and type(labels.get("1")) is list and
             type(labels.get("3")) is list, "task193:affine_roster")
        self.universe = {
            "1": OuterUniverse(helper, runtime, boundary, authority.meter, "1",
                               labels["1"], self.words, budget),
            "3": OuterUniverse(helper, runtime, boundary, authority.meter, "3",
                               labels["3"], self.words, budget),
        }
        self.generator: dict[tuple[str, int], tuple[Any, int]] = {}
        for domain, universe in self.universe.items():
            width = 3 if domain == "1" else 6
            for component in range(1, width + 1):
                state = runtime.eval_pb((component,), universe.context)
                node = self.words.literal((component,))
                self.generator[domain, component] = (state, node)
                inverse = state.inv(); inverse_node = self.words.literal((-component,))
                self.generator[domain, -component] = (inverse, inverse_node)
        self._bind_task193_transitions()
        self.d1, self.e1 = self._pointed_rows()
        self.occurrences = self._occurrence_package()
        self.fixed_pre = add(self.d1, self.occurrences["w"])
        self.target = dict(self.e1)
        self.outer_boundary = self._outer_boundary_seeds()
        self.action_cache: dict[tuple[int, str, int], int] = {}
        self.source_action: dict[int, dict[str, Any]] = {}
        for letter in ACTION_LETTERS:
            self.source_action[letter] = self._source_actors((letter,))

    def total_labels(self) -> int:
        return sum(len(value.states) for value in self.universe.values())

    def eval_outer(self, domain: str, word: Sequence[int],
                   expected: Sequence[Any] | None = None
                   ) -> tuple[Any, dict[tuple[int, int], int], int]:
        universe = self.universe[domain]
        current = self.h.AffineState(universe.q, universe.q.identity, {})
        current_node = 0; row: dict[tuple[int, int], int] = {}
        for index, raw in enumerate(word):
            letter = int(raw); need(1 <= abs(letter) <= (3 if domain == "1" else 6),
                                    "outer_word:letter")
            before = universe.intern(current, current_node)
            state, node = self.generator[domain, letter]
            current = current.mul(state); current_node = self.words.concat(current_node, node)
            after = universe.intern(current, current_node)
            if expected is not None:
                item = expected[index]
                need(type(item) is list and int(item[0]) == letter and
                     int(item[1]) == before and int(item[2]) == after,
                     "task193:prefix_transition")
            label = before if letter > 0 else after
            key = (abs(letter), label)
            value = (row.get(key, 0) + (1 if letter > 0 else -1)) % MODULUS
            if value: row[key] = value
            else: row.pop(key, None)
            self.budget.bump(1, "outer_word")
        return current, row, current_node

    def _transition_records(self) -> list[tuple[str, dict[str, Any]]]:
        records: list[tuple[str, dict[str, Any]]] = []
        for item in self.task193.get("base_boundary_rows", []):
            records.append(("1" if int(item.get("block", 0)) in (1, 2) else "3", item))
        for item in self.task193.get("pointed_rows", {}).get("blocks", []):
            records.append(("1" if item.get("name") in ("H1", "H2") else "3", item))
        beta = self.task193.get("beta1", {})
        for name, key in (("H1", "beta1_H1"), ("H2", "beta1_H2"), ("P", "beta1_P")):
            item = beta.get(key)
            if type(item) is dict: records.append((BLOCK_DOMAIN[name], item))
        for item in self.task193.get("marked_map_identities", {}).get("map_replays", []):
            records.append(("1" if int(item.get("block", 0)) in (1, 2) else "3", item))
        return records

    def _bind_task193_transitions(self) -> None:
        for domain, item in self._transition_records():
            word = item.get("word", item.get("target_word"))
            transitions = item.get("prefix_transitions")
            if type(word) is list and type(transitions) is list and len(word) == len(transitions):
                self.eval_outer(domain, word, transitions)

    @staticmethod
    def _receipt_row(bundle: Any) -> dict[tuple[int, int], int]:
        raw = bundle.get("row") if type(bundle) is dict and "row" in bundle else bundle
        need(type(raw) is dict, "task193:row_bundle")
        out: dict[tuple[int, int], int] = {}
        for key, value in raw.items():
            parsed = ast.literal_eval(str(key))
            need(type(parsed) is tuple and len(parsed) == 2, "task193:row_key")
            coefficient = int(value) % MODULUS
            if coefficient: out[int(parsed[0]), int(parsed[1])] = coefficient
        return out

    def _pointed_rows(self) -> tuple[dict[str, int], dict[str, int]]:
        pointed = self.task193.get("pointed_rows", {})
        need(pointed.get("schema") == "d972-r07-task193-pointed-row-package/v1" and
             pointed.get("status") == "ACCEPTED" and
             pointed.get("block_order") == list(BLOCKS), "task193:pointed_package")
        d1: dict[str, int] = {}; e1: dict[str, int] = {}
        records = {str(item.get("name")): item for item in pointed.get("blocks", [])}
        for block in BLOCKS:
            item = records.get(block); need(type(item) is dict, "task193:pointed_block")
            domain = BLOCK_DOMAIN[block]
            _state, raw, _node = self.eval_outer(domain, item["word"],
                                                  item["prefix_transitions"])
            expected_d1 = self._receipt_row(item["d1_pt"])
            expected_e1 = self._receipt_row(item["e1_pt"])
            need(scaled(raw, -1) == expected_d1, "task193:d1_direct:" + block)
            beta_item = self.task193.get("beta1", {}).get(
                "beta1_" + block if block != "P" else "beta1_P")
            need(type(beta_item) is dict, "task193:beta_record:" + block)
            _corrected, beta_raw, _ = self.eval_outer(domain, beta_item["word"],
                                                       beta_item["prefix_transitions"])
            need(scaled(beta_raw, -1) == expected_e1, "task193:e1_direct:" + block)
            for (component, label), value in expected_d1.items():
                d1[zkey(block, component, label)] = value
            for (component, label), value in expected_e1.items():
                e1[zkey(block, component, label)] = value
        return d1, e1

    def _substituted_word(self, source: Sequence[int], occurrence: dict[str, Any]
                          ) -> tuple[int, ...]:
        context = self.runtime.contexts[int(occurrence["ten_index"])]
        return tuple(self.runtime.old.f2_substitute(tuple(source),
                                                    context["left"], context["right"]))

    def _occurrence_states(self, source: Sequence[int]) -> tuple[list[Any], list[int]]:
        states = self.runtime.states_direct(tuple(source)); nodes = []
        ledger = self.authority.receipt["bridge"]["occurrence_ledger"]
        for item in ledger:
            nodes.append(self.words.literal(self._substituted_word(source, item)))
        return states, nodes

    def _signed_factor(self, states: list[Any], nodes: list[int], item: dict[str, Any]
                       ) -> tuple[Any, int]:
        index = int(item["ten_index"]); state, node = states[index], nodes[int(item["ordinal"]) - 1]
        if int(item["factor_sign"]) < 0: return state.inv(), self.words.inverse(node)
        return state, node

    def _block_products(self, states: list[Any], nodes: list[int]
                        ) -> dict[str, tuple[Any, int]]:
        ledger = self.authority.receipt["bridge"]["occurrence_ledger"]
        answer: dict[str, tuple[Any, int]] = {}
        for block in BLOCKS:
            items = [item for item in ledger if (str(item["block"]).startswith("P")
                                                  if block == "P" else item["block"] == block)]
            universe = self.universe[BLOCK_DOMAIN[block]]
            state = self.h.AffineState(universe.q, universe.q.identity, {}); node = 0
            for item in reversed(items):
                factor, factor_node = self._signed_factor(states, nodes, item)
                state = state.mul(factor); node = self.words.concat(node, factor_node)
            answer[block] = state, node
        return answer

    def translate_z(self, row: dict[tuple[int, int], int], block: str,
                    actor: Any, actor_node: int) -> dict[tuple[int, int], int]:
        universe = self.universe[BLOCK_DOMAIN[block]]; out: dict[tuple[int, int], int] = {}
        for (component, label), coefficient in row.items():
            moved = actor.mul(universe.states[label])
            old_node = universe.word_nodes[label]
            node = self.words.concat(actor_node, old_node) if old_node is not None else None
            target = (component, universe.intern(moved, node))
            out[target] = (out.get(target, 0) + int(coefficient)) % MODULUS
        return {key: value for key, value in out.items() if value}

    def _occurrence_package(self) -> dict[str, Any]:
        ledger = self.authority.receipt["bridge"]["occurrence_ledger"]
        need(type(ledger) is list and len(ledger) == 11, "task198:occurrence_ledger")
        g760 = self.task193.get("g760")
        need(type(g760) is list and len(g760) == 760, "task193:g760")
        states, nodes = self._occurrence_states(g760)
        prefixes: list[dict[str, Any]] = []; w: dict[str, int] = {}
        decomposed: dict[str, dict[tuple[int, int], int]] = {block: {} for block in BLOCKS}
        by_ordinal = {int(item["ordinal"]): item for item in ledger}
        for item in ledger:
            ordinal = int(item["ordinal"]); block = "P" if str(item["block"]).startswith("P") else str(item["block"])
            domain = BLOCK_DOMAIN[block]; universe = self.universe[domain]
            qstate = self.h.AffineState(universe.q, universe.q.identity, {}); qnode = 0
            for prefix_ordinal in item["fox_prefix_occurrences"]:
                factor_item = by_ordinal[int(prefix_ordinal)]
                factor, factor_node = self._signed_factor(states, nodes, factor_item)
                qstate = qstate.mul(factor); qnode = self.words.concat(qnode, factor_node)
            raw_state = states[int(item["ten_index"])]
            raw_node = nodes[ordinal - 1]
            if int(item["factor_sign"]) > 0:
                pstate, pnode = qstate.mul(raw_state), self.words.concat(qnode, raw_node)
            else:
                pstate, pnode = qstate, qnode
            inverse_word = word_inv(self._substituted_word(g760, item))
            inverse_state, drow, inverse_node = self.eval_outer(domain, inverse_word)
            need(_state_signature(inverse_state) == _state_signature(raw_state.inv()),
                 "occurrence:inverse_state")
            translated = self.translate_z(drow, block, pstate, pnode)
            decomposed[block] = add(decomposed[block], translated,
                                    int(item["factor_sign"]))
            left = pstate.mul(raw_state.inv()); left_node = self.words.concat(pnode,
                                                                              self.words.inverse(raw_node))
            left_label = universe.intern(left, left_node)
            right_label = universe.intern(pstate, pnode)
            w = add(w, {etakey(ordinal, left_label): int(item["factor_sign"]),
                        etakey(ordinal, right_label): -int(item["factor_sign"])})
            prefixes.append({"ordinal": ordinal, "block": block, "domain": domain,
                             "pstate": pstate, "pnode": pnode,
                             "raw_state": raw_state, "raw_node": raw_node})
        for block in BLOCKS:
            actual = {(int(parts[2]), int(parts[3])): value
                      for key, value in self.d1.items()
                      if (parts := parse_sparse_key(key))[1] == block}
            need(decomposed[block] == actual, "occurrence:d1_decomposition:" + block)
        return {"w": w, "prefixes": prefixes,
                "ledger_digest": digest(ledger), "d1_decomposition": True}

    def _outer_boundary_seeds(self) -> dict[str, Any]:
        seeds: dict[str, list[dict[str, Any]]] = {block: [] for block in BLOCKS}
        by_component: dict[tuple[str, int], list[tuple[int, int, int]]] = {}
        for block in BLOCKS:
            domain = BLOCK_DOMAIN[block]; universe = self.universe[domain]
            relations = self.runtime.old.pure_relations(3 if domain == "1" else 4)
            need(len(relations) == (2 if domain == "1" else 11),
                 "outer_boundary:relation_count")
            for relation, word in enumerate(relations):
                state, row, _ = self.eval_outer(domain, word)
                identity = self.h.AffineState(universe.q, universe.q.identity, {})
                need(universe.intern(state) == universe.intern(identity, 0),
                     "outer_boundary:relation_identity")
                seed = {"relation": relation, "row": row}
                seeds[block].append(seed)
                for (component, label), coefficient in row.items():
                    by_component.setdefault((block, component), []).append(
                        (relation, label, coefficient))
        return {"seeds": seeds, "by_component": by_component,
                "selected": set(), "pair_count": 0}

    def _source_actors(self, source: Sequence[int]) -> dict[str, Any]:
        states, nodes = self._occurrence_states(source)
        blocks = self._block_products(states, nodes)
        occurrence = []
        for item, prefix in zip(self.authority.receipt["bridge"]["occurrence_ledger"],
                                self.occurrences["prefixes"]):
            qstate = states[int(item["ten_index"])]
            qnode = nodes[int(item["ordinal"]) - 1]
            pstate, pnode = prefix["pstate"], prefix["pnode"]
            actor = pstate.mul(qstate).mul(pstate.inv())
            actor_node = self.words.concat(
                self.words.concat(pnode, qnode), self.words.inverse(pnode))
            occurrence.append((actor, actor_node))
        return {"blocks": blocks, "occurrences": occurrence}

    def action_pair(self, row: dict[str, int], actors: dict[str, Any]) -> dict[str, int]:
        out: dict[str, int] = {}
        for key, coefficient in row.items():
            parts = parse_sparse_key(key)
            if parts[0] == "z":
                block, component, label = parts[1], int(parts[2]), int(parts[3])
                universe = self.universe[BLOCK_DOMAIN[block]]
                actor, actor_node = actors["blocks"][block]
                state = actor.mul(universe.states[label]); old_node = universe.word_nodes[label]
                node = self.words.concat(actor_node, old_node) if old_node is not None else None
                target = zkey(block, component, universe.intern(state, node))
            elif parts[0] == "eta":
                occurrence, label = int(parts[1]), int(parts[2])
                prefix = self.occurrences["prefixes"][occurrence - 1]
                universe = self.universe[prefix["domain"]]
                actor, actor_node = actors["occurrences"][occurrence - 1]
                state = actor.mul(universe.states[label]); old_node = universe.word_nodes[label]
                node = self.words.concat(actor_node, old_node) if old_node is not None else None
                target = etakey(occurrence, universe.intern(state, node))
            else:
                raise InputStop("action:coordinate")
            value = (out.get(target, 0) + int(coefficient)) % MODULUS
            if value: out[target] = value
            else: out.pop(target, None)
        self.budget.bump(len(row), "pair_action")
        return out

    def action_source_word(self, row: dict[str, int], source: Sequence[int]) -> dict[str, int]:
        current = dict(row)
        for letter in reversed(tuple(source)):
            current = self.action_pair(current, self.source_action[int(letter)])
        return current

    @staticmethod
    def project(row: dict[str, int]) -> dict[str, int]:
        out: dict[str, int] = {}
        for key, coefficient in row.items():
            parts = parse_sparse_key(key)
            if parts[0] == "z": target = key
            elif parts[0] == "eta":
                ordinal, label = int(parts[1]), int(parts[2])
                target = ckey("H1" if ordinal <= 3 else "H2" if ordinal <= 6 else "P",
                              label)
            else: raise InputStop("project:coordinate")
            value = (out.get(target, 0) + int(coefficient)) % MODULUS
            if value: out[target] = value
            else: out.pop(target, None)
        return out

    def relator_seed(self, index: int) -> dict[str, int]:
        word = tuple(int(x) for x in self.authority.rows[int(index) - 1]["word"])
        actors = self._source_actors(word)
        return add(self.action_pair(self.fixed_pre, actors), self.fixed_pre, -1)

    def translated_outer_boundary(self, block: str, relation: int,
                                  translation: Any, translation_node: int
                                  ) -> dict[str, int]:
        seed = self.outer_boundary["seeds"][block][int(relation)]["row"]
        moved = self.translate_z(seed, block, translation, translation_node)
        return {zkey(block, component, label): value
                for (component, label), value in moved.items()}

    def correlate_outer(self, dual: dict[str, int]) -> dict[str, Any] | None:
        accumulator: dict[tuple[str, int, int], int] = {}
        translations: dict[tuple[str, int, int], tuple[Any, int]] = {}
        pairs = 0
        for key, lambda_value in dual.items():
            parts = parse_sparse_key(key)
            if parts[0] != "z": continue
            block, component, g_label = parts[1], int(parts[2]), int(parts[3])
            universe = self.universe[BLOCK_DOMAIN[block]]; g = universe.states[g_label]
            g_node = universe.word_nodes[g_label]
            need(g_node is not None, "outer_boundary:g_word")
            for relation, h_label, base_coefficient in self.outer_boundary[
                    "by_component"].get((block, component), []):
                h = universe.states[h_label]; h_node = universe.word_nodes[h_label]
                need(h_node is not None, "outer_boundary:h_word")
                translation = g.mul(h.inv())
                translation_node = self.words.concat(int(g_node), self.words.inverse(int(h_node)))
                label = universe.intern(translation, translation_node)
                signature = (block, int(relation), label)
                accumulator[signature] = (accumulator.get(signature, 0) +
                                          int(lambda_value) * int(base_coefficient)) % MODULUS
                translations[signature] = (translation, translation_node); pairs += 1
        self.outer_boundary["pair_count"] += pairs; self.budget.bump(pairs, "outer_correlation")
        for signature in sorted(key for key, value in accumulator.items() if value):
            if signature in self.outer_boundary["selected"]: continue
            self.outer_boundary["selected"].add(signature)
            block, relation, _label = signature; translation, node = translations[signature]
            row = self.translated_outer_boundary(block, relation, translation, node)
            scalar = sum(int(value) * dual.get(key, 0) for key, value in row.items()) % MODULUS
            need(scalar == accumulator[signature] and scalar != 0,
                 "outer_boundary:correlation_replay")
            return {"block": block, "relation": relation, "translation": translation,
                    "translation_node": node, "row": row, "scalar": scalar,
                    "pair_count": pairs}
        need(all(not value for key, value in accumulator.items()
                 if key in self.outer_boundary["selected"]),
             "outer_boundary:selected_not_annihilated")
        need(not any(value for key, value in accumulator.items()
                     if key not in self.outer_boundary["selected"]),
             "outer_boundary:unselected_nonzero")
        return None

    def replay_terms(self, coefficients: dict[tuple[tuple[int, ...], int], int],
                     boundaries: dict[tuple[str, int, tuple[int, ...]], int]
                     ) -> dict[str, int]:
        out: dict[str, int] = {}
        seed_cache: dict[int, dict[str, int]] = {}
        for (prefix, relator), coefficient in coefficients.items():
            if relator not in seed_cache: seed_cache[relator] = self.relator_seed(relator)
            row = self.action_source_word(seed_cache[relator], prefix)
            out = add(out, self.project(row), coefficient)
        for (block, relation, translation_word), coefficient in boundaries.items():
            domain = BLOCK_DOMAIN[block]; universe = self.universe[domain]
            state, _fox, node = self.eval_outer(domain, translation_word)
            row = self.translated_outer_boundary(block, relation, state, node)
            out = add(out, row, coefficient)
        return out

    def _target_oracle(self, joint: Echelon
                       ) -> tuple[tuple[dict[str, int], int] | None,
                                  tuple[dict[str, int], int] | None]:
        while True:
            solution = joint.solution(self.target)
            if solution is not None: return solution, None
            dual, pairing, _remainder = joint.dual(self.target)
            selected = self.correlate_outer(dual)
            if selected is None: return None, (dual, pairing)
            translation_word = self.words.word(int(selected["translation_node"]))
            node = self.proof.boundary(str(selected["block"]),
                                       int(selected["relation"]), translation_word)
            inserted = joint.insert(selected["row"], node)
            need(inserted is not None, "outer_boundary:joint_rank")

    @staticmethod
    def _public_coefficients(value: dict[tuple[tuple[int, ...], int], int]
                             ) -> list[dict[str, Any]]:
        return [{"coefficient": coefficient, "prefix": list(prefix),
                 "relator_index": relator}
                for (prefix, relator), coefficient in sorted(
                    value.items(), key=lambda item: (item[0][1], item[0][0]))]

    @staticmethod
    def _public_boundaries(value: dict[tuple[str, int, tuple[int, ...]], int]
                           ) -> list[dict[str, Any]]:
        return [{"block": block, "relation": relation,
                 "translation_word": list(word), "coefficient": coefficient}
                for (block, relation, word), coefficient in sorted(value.items())]

    def _member(self, node: int, pre: Echelon, joint: Echelon,
                seed_cursor: int, queue_cursor: int) -> dict[str, Any]:
        coefficients, boundaries = self.proof.expand(node)
        replay = self.replay_terms(coefficients, boundaries)
        need(replay == self.target, "member:raw_joint_replay")
        pairs = []
        for (prefix, relator), coefficient in sorted(
                coefficients.items(), key=lambda item: (item[0][1], item[0][0])):
            relator_word = tuple(int(x) for x in self.authority.rows[relator - 1]["word"])
            pairs.append({"coefficient": coefficient, "prefix": list(prefix),
                          "relator_index": relator,
                          "positive_word": list(word_mul(prefix, relator_word)),
                          "negative_word": list(prefix)})
        return {"terminal_kind": "MEMBER", "raw_joint_equality": True,
                "coefficient_terms": self._public_coefficients(coefficients),
                "boundary_slack": self._public_boundaries(boundaries),
                "mu1": {"language": "sum a_gj g(b_j-1)",
                         "terms": self._public_coefficients(coefficients)},
                "M": {"language": "sum a_gj ((w r_j)-w)", "pairs": pairs,
                      "boundary_slack_excluded": True},
                "search": {"relator_cursor": seed_cursor,
                           "queue_cursor": queue_cursor,
                           "positive_early_stop": True,
                           "pre_rank": len(pre.pivots), "joint_rank": len(joint.pivots)},
                "checks": {"pointed_coordinate": True,
                           "printed_occurrence_zero": True,
                           "roof_fibre_pairs": True,
                           "task193_sign": "d1=-D1(g760),e1=-beta1"}}

    def _nonmember(self, dual: dict[str, int], pairing: int,
                   pre: Echelon, joint: Echelon, queue_cursor: int
                   ) -> dict[str, Any]:
        # The independent checker replays these proof nodes, all 6,441 seed
        # containments, and four actions of every retained pre-C pivot.
        return {"terminal_kind": "NONMEMBER",
                "complete": {"relator_roster": ROWS,
                             "all_relators_processed": True,
                             "pre_action_queue_exhausted": queue_cursor == len(pre.pivots),
                             "complete_outer_boundary_zero_correlation": True,
                             "inner_boundary_families": 65},
                "pre_basis": [{"pivot": pivot, "row": pre.rows[pivot],
                               "proof_node": pre.nodes[pivot]}
                              for pivot in pre.pivots],
                "proof_nodes": self.proof.nodes,
                "dual": {"functional": dual, "target_pairing": pairing,
                         "joint_rank": len(joint.pivots)},
                "search": {"pre_rank": len(pre.pivots),
                           "joint_rank": len(joint.pivots),
                           "queue_cursor": queue_cursor}}

    def run(self) -> dict[str, Any]:
        pre = Echelon(self.budget, self.proof); joint = Echelon(self.budget, self.proof)
        queue_cursor = 0; rank_events = 0
        final_dual: tuple[dict[str, int], int] | None = None
        solution, final_dual = self._target_oracle(joint)
        if solution is not None: return self._member(solution[1], pre, joint, 0, 0)
        for relator in range(1, ROWS + 1):
            seed = self.relator_seed(relator); seed_node = self.proof.seed(relator)
            accepted = pre.insert(seed, seed_node)
            if accepted is not None:
                pivot, stored_node = accepted
                joint.insert(self.project(pre.rows[pivot]), stored_node)
                rank_events += 1; solution = joint.solution(self.target)
                if solution is not None:
                    return self._member(solution[1], pre, joint, relator, queue_cursor)
                if rank_events % TARGET_ORACLE_STRIDE == 0:
                    solution, final_dual = self._target_oracle(joint)
                    if solution is not None:
                        return self._member(solution[1], pre, joint, relator, queue_cursor)
            self.budget.progress("RELATORS", relator, len(pre.pivots), len(joint.pivots),
                                 self.total_labels())
            if relator % 32 == 0: self.authority.meter.check("A5_V3_RELATOR_" + str(relator))
        solution, final_dual = self._target_oracle(joint)
        if solution is not None: return self._member(solution[1], pre, joint, ROWS, 0)
        while queue_cursor < len(pre.pivots):
            pivot = pre.pivots[queue_cursor]; queue_cursor += 1
            parent_row, parent_node = pre.rows[pivot], pre.nodes[pivot]
            for letter in ACTION_LETTERS:
                candidate = self.action_pair(parent_row, self.source_action[letter])
                candidate_node = self.proof.action(parent_node, letter)
                accepted = pre.insert(candidate, candidate_node)
                if accepted is not None:
                    new_pivot, stored_node = accepted
                    joint.insert(self.project(pre.rows[new_pivot]), stored_node)
                    rank_events += 1; solution = joint.solution(self.target)
                    if solution is not None:
                        return self._member(solution[1], pre, joint, ROWS, queue_cursor)
                    if rank_events % TARGET_ORACLE_STRIDE == 0:
                        solution, final_dual = self._target_oracle(joint)
                        if solution is not None:
                            return self._member(solution[1], pre, joint, ROWS, queue_cursor)
            self.budget.progress("ACTION_QUEUE", queue_cursor, len(pre.pivots),
                                 len(joint.pivots), self.total_labels())
            self.authority.meter.check("A5_V3_ACTION_" + str(queue_cursor))
        solution, final_dual = self._target_oracle(joint)
        if solution is not None: return self._member(solution[1], pre, joint, ROWS, queue_cursor)
        need(final_dual is not None and queue_cursor == len(pre.pivots),
             "nonmember:incomplete")
        return self._nonmember(final_dual[0], final_dual[1], pre, joint, queue_cursor)


def source_identity() -> dict[str, Any]:
    raw = Path(__file__).read_bytes()
    return {"path": Path(__file__).resolve().relative_to(ROOT).as_posix(),
            "bytes": len(raw), "sha256": sha(raw)}


def build(args: argparse.Namespace) -> dict[str, Any]:
    helper = load_task198()
    try:
        limits = dict(helper.CAPS); limits["wall_seconds"] = int(args.seconds)
        limits["rss_bytes"] = int(args.rss_bytes)
        meter = helper.Meter(limits)
        authority = helper.AuthorityAdapter(args, meter)
        runtime = helper.Runtime(authority, meter)
        boundary = helper.BoundaryLedger(runtime, meter)
        task193, task193_identity, _task193_verdict = load_task193(
            args.task193_receipt, args.task193_verdict)
        budget = Budget(args.max_operations)
        engine = DirectEngine(helper, authority, runtime, boundary, task193, budget)
        result = engine.run()
    except helper.ResourceStop as exc:
        raise ResourceStop(str(exc)) from exc
    except (helper.InputStop, helper.Reject) as exc:
        raise InputStop(str(exc)) from exc
    return seal({"schema": SCHEMA, "status": "COMPLETE",
                 "terminal": MEMBER if result["terminal_kind"] == "MEMBER" else NONMEMBER,
                 "mode": "PRODUCTION", "result": result,
                 "owners": {"task198": authority.identity,
                            "task193_v3": task193_identity},
                 "source": source_identity(),
                 "arithmetic": {"task198_runtime": "v12 frozen executable owner",
                                "relator_count": ROWS,
                                "inner_boundary_families": 65,
                                "outer_blocks": list(BLOCKS),
                                "occurrence_count": 11,
                                "pre_C_action_closure": True,
                                "printed_C_after_action": True},
                 "resource": {"max_operations": args.max_operations,
                              "operations": budget.count,
                              "seconds_cap": args.seconds,
                              "rss_bytes_cap": args.rss_bytes,
                              "task198_meter": meter.public(strict=False)},
                 "claims": {"A5": result["terminal_kind"],
                            "A6_M": result["terminal_kind"] == "MEMBER",
                            "A7": "NONE", "compatible_lift": "NONE",
                            "fake": "NONE", "Ihara": "NONE"}})


def unknown(args: argparse.Namespace, status: str, reason: str) -> dict[str, Any]:
    return seal({"schema": SCHEMA, "status": status,
                 "terminal": status + ":" + reason, "mode": "PRODUCTION",
                 "reason": reason,
                 "inputs": {"task193_receipt": args.task193_receipt,
                            "task193_verdict": args.task193_verdict},
                 "claims": {"A5": "NONE", "A6_M": False, "A7": "NONE",
                            "compatible_lift": "NONE", "fake": "NONE",
                            "Ihara": "NONE"}})


def output_path(raw: str) -> Path:
    text = str(raw).replace("\\", "/"); path = Path(text)
    need(not path.is_absolute() and ".." not in path.parts and "." not in path.parts,
         "output:lexical")
    target = (ROOT / path).resolve(strict=False)
    need(target.parent == (ROOT / "ci/out").resolve(strict=True), "output:containment")
    return target


def write_exclusive(raw_path: str, value: dict[str, Any]) -> None:
    path = output_path(raw_path); need(not path.exists(), "output:stale")
    encoded = canon(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        view = memoryview(encoded)
        while view: view = view[os.write(fd, view):]
        os.fsync(fd)
    finally: os.close(fd)


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("PRODUCTION",), default="PRODUCTION")
    ap.add_argument("--task193-receipt", required=True)
    ap.add_argument("--task193-verdict", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--max-operations", type=int, default=2_000_000_000)
    ap.add_argument("--seconds", type=int, default=14_400)
    ap.add_argument("--rss-bytes", type=int, default=8_000_000_000)
    for key, value in TASK198_DEFAULTS.items():
        ap.add_argument("--task198-" + key, dest="task198_" + key, default=value)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        need(args.max_operations > 0 and args.seconds == 14_400 and
             args.rss_bytes == 8_000_000_000, "arguments:frozen_caps")
        result = build(args)
    except ResourceStop as exc:
        result = unknown(args, UNKNOWN_RESOURCE, str(exc))
    except (InputStop, OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        result = unknown(args, UNKNOWN_INPUT, str(exc))
    write_exclusive(args.output, result)
    print(PRODUCER_LINE + " " + str(result["terminal"]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
