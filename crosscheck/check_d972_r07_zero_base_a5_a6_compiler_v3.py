#!/usr/bin/env python3
"""Independent checker for the R07 direct-relator A5/A6 v3 receipt.

The producer is never imported.  The checker restores the frozen independent
v14 arithmetic and replays either the finite MEMBER terms or the complete
NONMEMBER invariant-span certificate.
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
import types
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-zero-base-a5-a6-compiler/v3"
CHECK_SCHEMA = SCHEMA + "/checker-verdict/v3"
CHECKER_LINE = "R07_ZERO_BASE_A5_A6_COMPILER_V3_CHECKER"
MEMBER = "R07_ZERO_BASE_A5_A6_MEMBER"
NONMEMBER = "R07_ZERO_BASE_A5_A6_NONMEMBER"
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
    "crosscheck/check_d972_r07_word_independent_successor_kernel_v14.py", 8074,
    "7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47")
PRODUCER_PIN = (
    "search/d972_r07_zero_base_a5_a6_compiler_v3.py", 59239,
    "c287011d5e573452094e62c76020ab4b1076bc427103174b1771a22a1bb4fbd8")
TASK198_DEFAULTS = {
    "receipt": "ci/in/d972_r07_seven_context_roof_presentation_v1.json",
    "manifest": "ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",
    "producer": "ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",
    "checker": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",
    "verdict": "ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",
}
BLOCKS = ("H1", "H2", "P")
BLOCK_DOMAIN = {"H1": "1", "H2": "1", "P": "3"}
ACTION_LETTERS = (1, -1, 2, -2)


class Reject(RuntimeError):
    pass


def require(value: bool, message: str) -> None:
    if value is not True: raise Reject(message)


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()
def digest(value: Any) -> str: return sha(canon(value))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value); body.pop("self_digest_sha256", None)
    body["self_digest_sha256"] = digest(body); return body


def add(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, raw in right.items():
        value = (out.get(key, 0) + int(scale) * int(raw)) % MODULUS
        if value: out[key] = value
        else: out.pop(key, None)
    return out


def scaled(row: dict[str, int], factor: int) -> dict[str, int]:
    return {key: int(value) * int(factor) % MODULUS for key, value in row.items()
            if int(value) * int(factor) % MODULUS}


def word_reduce(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for raw in word:
        letter = int(raw); require(letter in ACTION_LETTERS, "word:letter")
        if out and out[-1] == -letter: out.pop()
        else: out.append(letter)
    return tuple(out)


def word_mul(*words: Sequence[int]) -> tuple[int, ...]:
    return word_reduce(letter for word in words for letter in word)


def word_inv(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(-int(letter) for letter in reversed(tuple(word)))


def inside(raw: str | Path, area: str | None = None, must_exist: bool = True) -> Path:
    text = str(raw).replace("\\", "/"); path = Path(text)
    require(not path.is_absolute() and ".." not in path.parts and "." not in path.parts,
            "path:lexical")
    try:
        value = (ROOT / path).resolve(strict=must_exist); value.relative_to(ROOT.resolve())
        if area is not None: value.relative_to((ROOT / area).resolve(strict=True))
    except (OSError, ValueError) as exc: raise Reject("path:containment:" + text) from exc
    if must_exist:
        cursor = ROOT
        for part in path.parts:
            cursor /= part; require(not stat.S_ISLNK(os.lstat(cursor).st_mode), "path:symlink")
    return value


def read_json(raw: str | Path, label: str, area: str = "ci/in"
              ) -> tuple[dict[str, Any], dict[str, Any]]:
    path = inside(raw, area); before = path.stat(); data = path.read_bytes(); after = path.stat()
    require((before.st_dev, before.st_ino, before.st_size,
             getattr(before, "st_mtime_ns", 0)) ==
            (after.st_dev, after.st_ino, after.st_size,
             getattr(after, "st_mtime_ns", 0)), label + ":changed")
    try: value = json.loads(data.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise Reject(label + ":json") from exc
    require(type(value) is dict, label + ":object")
    return value, {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data),
                   "sha256": sha(data)}


def check_self(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256", value.get("self_digest"))
    body = dict(value); body.pop("self_digest_sha256", None); body.pop("self_digest", None)
    require(type(claimed) is str and claimed == digest(body), label + ":seal")


def check_pin(pin: tuple[str, int, str], label: str) -> dict[str, Any]:
    raw = inside(pin[0]).read_bytes()
    require(len(raw) == pin[1] and sha(raw) == pin[2], label + ":pin")
    return {"path": pin[0], "bytes": pin[1], "sha256": pin[2]}


def load_helper() -> types.ModuleType:
    path = inside(TASK198_WRAPPER_PIN[0]); wrapper_raw = path.read_bytes()
    require(len(wrapper_raw) == TASK198_WRAPPER_PIN[1] and
            sha(wrapper_raw) == TASK198_WRAPPER_PIN[2], "task198:v14_wrapper_pin")
    spec = importlib.util.spec_from_file_location("r07_task198_v14_checker_wrapper", path)
    require(spec is not None and spec.loader is not None, "task198:wrapper_loader")
    wrapper = importlib.util.module_from_spec(spec); spec.loader.exec_module(wrapper)
    source = Path(wrapper.SOURCE); raw = source.read_bytes()
    require(len(raw) == int(wrapper.SOURCE_BYTES) and
            sha(raw) == str(wrapper.SOURCE_SHA256), "task198:frozen_checker_pin")
    for index, (old, new) in enumerate(wrapper.PATCHES):
        require(type(old) is bytes and type(new) is bytes and old and new and old != new,
                "task198:patch_nonempty:" + str(index))
        require(raw.count(old) == 1, "task198:patch_cardinality:" + str(index))
        raw = raw.replace(old, new)
    module = types.ModuleType("r07_task198_v14_arithmetic_for_a5_v3")
    module.__file__ = str(source); module.__package__ = None
    exec(compile(raw, str(source), "exec"), module.__dict__, module.__dict__)
    for name in ("Meter", "Authority", "CheckerArithmetic", "Boundary", "CState",
                 "row_key", "decode_token", "correlate", "element_blob"):
        require(hasattr(module, name), "task198:checker_symbol:" + name)
    return module


def load_task193(receipt_path: str, verdict_path: str
                 ) -> tuple[dict[str, Any], dict[str, Any]]:
    sources = {"producer": check_pin(TASK193_PRODUCER_PIN, "task193:producer"),
               "checker": check_pin(TASK193_CHECKER_PIN, "task193:checker"),
               "driver": check_pin(TASK193_DRIVER_PIN, "task193:driver")}
    receipt, rid = read_json(receipt_path, "task193:receipt")
    verdict, vid = read_json(verdict_path, "task193:verdict")
    check_self(receipt, "task193:receipt"); check_self(verdict, "task193:verdict")
    require(receipt.get("schema") == TASK193_SCHEMA and receipt.get("status") == "PASS" and
            receipt.get("terminal") == TASK193_TERMINAL, "task193:positive")
    require(verdict.get("schema") == TASK193_CHECK_SCHEMA and verdict.get("status") == "PASS" and
            verdict.get("terminal") == TASK193_TERMINAL, "task193:checker_positive")
    bound = verdict.get("receipt", {})
    require(bound.get("bytes") == rid["bytes"] and bound.get("sha256") == rid["sha256"],
            "task193:verdict_binding")
    require(verdict.get("claims", {}).get("independent_task193_replay") is True and
            verdict.get("claims", {}).get("pointed_rows") is True, "task193:claims")
    return receipt, {"receipt": rid, "verdict": vid, "sources": sources}


def zkey(block: str, component: int, label: int) -> str:
    return "z|" + block + "|" + str(int(component)) + "|" + str(int(label))


def etakey(occurrence: int, label: int) -> str:
    return "eta|" + str(int(occurrence)) + "|" + str(int(label))


def ckey(block: str, label: int) -> str:
    return "c|" + block + "|" + str(int(label))


def parts(key: str) -> tuple[str, ...]: return tuple(key.split("|"))


class SmallEchelon:
    def __init__(self, reverse: bool = False):
        self.reverse = reverse; self.pivots: list[str] = []; self.rows: dict[str, dict[str, int]] = {}

    def reduce(self, source: dict[str, int]) -> dict[str, int]:
        row = {key: int(value) % MODULUS for key, value in source.items() if int(value) % MODULUS}
        for pivot in self.pivots:
            factor = row.get(pivot, 0)
            if factor: row = add(row, self.rows[pivot], -factor)
        return row

    def insert(self, source: dict[str, int]) -> bool:
        row = self.reduce(source)
        if not row: return False
        pivot = max(row) if self.reverse else min(row); factor = 1 if row[pivot] == 1 else 2
        self.pivots.append(pivot); self.rows[pivot] = scaled(row, factor); return True

    def dual(self, target: dict[str, int]) -> tuple[dict[str, int], int]:
        remainder = self.reduce(target); require(bool(remainder), "dual:member")
        free = max(remainder) if self.reverse else min(remainder); dual = {free: 1}
        for pivot in reversed(self.pivots):
            value = sum(int(v) * dual.get(k, 0) for k, v in self.rows[pivot].items()) % MODULUS
            if value: dual[pivot] = (-value) % MODULUS
            else: dual.pop(pivot, None)
        pairing = sum(int(v) * dual.get(k, 0) for k, v in target.items()) % MODULUS
        require(pairing != 0 and all(sum(int(v) * dual.get(k, 0)
                                         for k, v in row.items()) % MODULUS == 0
                                     for row in self.rows.values()), "dual:replay")
        return dual, pairing


def signature(state: Any) -> tuple[Any, tuple[Any, ...]]:
    return state.a, tuple(sorted((int(c), e, int(v) % MODULUS)
                                 for (c, e), v in state.u.items() if int(v) % MODULUS))


class CheckerUniverse:
    def __init__(self, helper: Any, arithmetic: Any, boundary: Any, meter: Any,
                 domain: str, roster: list[dict[str, Any]]):
        self.h, self.arithmetic, self.boundary, self.meter = helper, arithmetic, boundary, meter
        self.domain, self.context = domain, 0 if domain == "1" else 5
        self.q = arithmetic.quotient(self.context); self.degree = 36 if domain == "1" else 144
        self.states: list[Any] = []; self.words: list[tuple[int, ...] | None] = []
        self.by_base: dict[str, list[int]] = {}; self.inner = SmallEchelon(reverse=True)
        self.cache: dict[Any, bool] = {}
        for ordinal, public in enumerate(roster):
            state = self.decode(public); self.states.append(state); self.words.append(None)
            self.by_base.setdefault(self.h.element_blob(state.a).hex(), []).append(ordinal)
        require(bool(self.states), "task193:empty_roster:" + domain)

    def split(self, raw: bytes) -> Any:
        require(len(raw) == (40 if self.degree == 36 else 154), "affine:element_width")
        return raw[:self.degree], raw[self.degree:]

    def decode(self, public: dict[str, Any]) -> Any:
        require(type(public) is dict and type(public.get("base")) is str and
                type(public.get("chain")) is list, "affine:public")
        local: dict[Any, int] = {}
        for pair in public["chain"]:
            require(type(pair) is list and len(pair) == 2, "affine:chain_pair")
            raw = bytes.fromhex(str(pair[0])); value = int(pair[1]) % MODULUS
            require(len(raw) >= 5 and raw[:1] == b"R" and raw[1] == int(self.domain),
                    "affine:chain_tag")
            width = int.from_bytes(raw[3:5], "big"); require(len(raw) == 5 + width,
                                                               "affine:chain_width")
            key = (int(raw[2]), self.split(raw[5:]))
            if value: local[key] = (local.get(key, 0) + value) % MODULUS
        return self.h.CState(self.q, self.split(bytes.fromhex(public["base"])),
                             {key: value for key, value in local.items() if value})

    def bind(self, label: int, word: Sequence[int]) -> None:
        require(0 <= int(label) < len(self.states), "affine:label")
        if self.words[int(label)] is None: self.words[int(label)] = word_reduce(word)

    def equal(self, left: Any, right: Any) -> bool:
        if left.a != right.a: return False
        difference = self.h.add_local(left.u, right.u, -1)
        if not difference: return True
        sig = tuple(sorted((int(c), e, int(v) % MODULUS)
                           for (c, e), v in difference.items()))
        if sig in self.cache: return self.cache[sig]
        target = {self.h.row_key(self.context, int(c), e): int(v) % MODULUS
                  for (c, e), v in difference.items() if int(v) % MODULUS}
        while True:
            remainder = self.inner.reduce(target)
            if not remainder: self.cache[sig] = True; return True
            free = max(remainder); dual: dict[str, int] = {free: 1}
            for pivot in reversed(self.inner.pivots):
                value = sum(int(v) * dual.get(k, 0)
                            for k, v in self.inner.rows[pivot].items()) % MODULUS
                if value: dual[pivot] = (-value) % MODULUS
                else: dual.pop(pivot, None)
            correlation = self.h.correlate(self.boundary, dual, self.meter)
            selected = correlation.get("selected")
            if selected is None: self.cache[sig] = False; return False
            context, relation, token, _scalar = selected
            require(int(context) == self.context, "inner:context")
            seed = self.boundary.by_key[(int(context), int(relation))]
            require(self.inner.insert(seed.translate(self.h.decode_token(str(token)))),
                    "inner:rank")

    def intern(self, state: Any, word: Sequence[int] | None = None) -> int:
        blob = self.h.element_blob(state.a).hex()
        for label in self.by_base.get(blob, []):
            if signature(state) == signature(self.states[label]) or self.equal(state, self.states[label]):
                if word is not None: self.bind(label, word)
                return label
        label = len(self.states); self.states.append(state)
        self.words.append(word_reduce(word) if word is not None else None)
        self.by_base.setdefault(blob, []).append(label); return label


class CheckerModel:
    def __init__(self, helper: Any, authority: Any, arithmetic: Any, boundary: Any,
                 task193: dict[str, Any]):
        self.h, self.authority, self.a, self.boundary = helper, authority, arithmetic, boundary
        self.task193 = task193
        labels = task193.get("affine_labels", {}).get("first_encounter_roster", {})
        require(type(labels) is dict and type(labels.get("1")) is list and
                type(labels.get("3")) is list, "task193:roster")
        self.u = {domain: CheckerUniverse(helper, arithmetic, boundary, authority.meter,
                                          domain, labels[domain]) for domain in ("1", "3")}
        self.gens: dict[tuple[str, int], Any] = {}
        for domain, universe in self.u.items():
            width = 3 if domain == "1" else 6
            for component in range(1, width + 1):
                state = arithmetic.base((component,), universe.context)
                self.gens[domain, component] = state
                self.gens[domain, -component] = state.inv()
        self.bind_transitions(); self.d1, self.e1 = self.pointed_rows()
        self.occ = self.occurrence_package(); self.fixed = add(self.d1, self.occ["w"])
        self.outer = self.outer_seeds(); self.actions = {
            letter: self.source_actors((letter,)) for letter in ACTION_LETTERS}

    def eval_outer(self, domain: str, word: Sequence[int], expected: Sequence[Any] | None = None
                   ) -> tuple[Any, dict[tuple[int, int], int], tuple[int, ...]]:
        universe = self.u[domain]
        current = self.h.CState(universe.q, universe.q.identity, {})
        prefix: tuple[int, ...] = (); row: dict[tuple[int, int], int] = {}
        for index, raw in enumerate(word):
            letter = int(raw); before = universe.intern(current, prefix)
            current = current.mul(self.gens[domain, letter]); prefix = word_mul(prefix, (letter,))
            after = universe.intern(current, prefix)
            if expected is not None:
                item = expected[index]
                require(int(item[0]) == letter and int(item[1]) == before and
                        int(item[2]) == after, "task193:transition")
            key = (abs(letter), before if letter > 0 else after)
            value = (row.get(key, 0) + (1 if letter > 0 else -1)) % MODULUS
            if value: row[key] = value
            else: row.pop(key, None)
        return current, row, prefix

    def records(self) -> list[tuple[str, dict[str, Any]]]:
        out = [("1" if int(item.get("block", 0)) in (1, 2) else "3", item)
               for item in self.task193.get("base_boundary_rows", [])]
        out += [("1" if item.get("name") in ("H1", "H2") else "3", item)
                for item in self.task193.get("pointed_rows", {}).get("blocks", [])]
        for name, key in (("H1", "beta1_H1"), ("H2", "beta1_H2"), ("P", "beta1_P")):
            item = self.task193.get("beta1", {}).get(key)
            if type(item) is dict: out.append((BLOCK_DOMAIN[name], item))
        out += [("1" if int(item.get("block", 0)) in (1, 2) else "3", item)
                for item in self.task193.get("marked_map_identities", {}).get("map_replays", [])]
        return out

    def bind_transitions(self) -> None:
        for domain, item in self.records():
            word, transitions = item.get("word", item.get("target_word")), item.get("prefix_transitions")
            if type(word) is list and type(transitions) is list and len(word) == len(transitions):
                self.eval_outer(domain, word, transitions)

    @staticmethod
    def receipt_row(bundle: Any) -> dict[tuple[int, int], int]:
        raw = bundle.get("row") if type(bundle) is dict and "row" in bundle else bundle
        require(type(raw) is dict, "task193:row")
        out = {}
        for key, value in raw.items():
            parsed = ast.literal_eval(str(key)); require(type(parsed) is tuple and len(parsed) == 2,
                                                      "task193:row_key")
            if int(value) % MODULUS: out[int(parsed[0]), int(parsed[1])] = int(value) % MODULUS
        return out

    def pointed_rows(self) -> tuple[dict[str, int], dict[str, int]]:
        pointed = self.task193.get("pointed_rows", {})
        require(pointed.get("schema") == "d972-r07-task193-pointed-row-package/v1" and
                pointed.get("status") == "ACCEPTED", "task193:pointed")
        records = {str(item.get("name")): item for item in pointed.get("blocks", [])}
        d1: dict[str, int] = {}; e1: dict[str, int] = {}
        for block in BLOCKS:
            item = records[block]; domain = BLOCK_DOMAIN[block]
            _state, raw, _ = self.eval_outer(domain, item["word"], item["prefix_transitions"])
            rd, re = self.receipt_row(item["d1_pt"]), self.receipt_row(item["e1_pt"])
            require(scaled(raw, -1) == rd, "task193:d1:" + block)
            beta = self.task193.get("beta1", {})["beta1_" + block]
            _state, beta_raw, _ = self.eval_outer(domain, beta["word"], beta["prefix_transitions"])
            require(scaled(beta_raw, -1) == re, "task193:e1:" + block)
            d1.update({zkey(block, c, label): value for (c, label), value in rd.items()})
            e1.update({zkey(block, c, label): value for (c, label), value in re.items()})
        return d1, e1

    def substituted(self, source: Sequence[int], item: dict[str, Any]) -> tuple[int, ...]:
        context = self.a.contexts[int(item["ten_index"])]
        return tuple(self.h.checker_word_substitute(tuple(source),
                                                    (context["left"], context["right"])))

    def occurrence_states(self, source: Sequence[int]) -> tuple[list[Any], list[tuple[int, ...]]]:
        states = [self.a.direct(tuple(source), index) for index in range(10)]
        words = [self.substituted(source, item)
                 for item in self.authority.receipt["bridge"]["occurrence_ledger"]]
        return states, words

    @staticmethod
    def signed(states: list[Any], words: list[tuple[int, ...]], item: dict[str, Any]
               ) -> tuple[Any, tuple[int, ...]]:
        state = states[int(item["ten_index"])]; word = words[int(item["ordinal"]) - 1]
        return (state.inv(), word_inv(word)) if int(item["factor_sign"]) < 0 else (state, word)

    def block_products(self, states: list[Any], words: list[tuple[int, ...]]
                       ) -> dict[str, tuple[Any, tuple[int, ...]]]:
        ledger = self.authority.receipt["bridge"]["occurrence_ledger"]
        answer = {}
        for block in BLOCKS:
            items = [item for item in ledger if (str(item["block"]).startswith("P")
                                                  if block == "P" else item["block"] == block)]
            universe = self.u[BLOCK_DOMAIN[block]]
            state = self.h.CState(universe.q, universe.q.identity, {}); word: tuple[int, ...] = ()
            for item in reversed(items):
                factor, factor_word = self.signed(states, words, item)
                state = state.mul(factor); word = word_mul(word, factor_word)
            answer[block] = state, word
        return answer

    def translate_z(self, row: dict[tuple[int, int], int], block: str, actor: Any,
                    actor_word: Sequence[int]) -> dict[tuple[int, int], int]:
        universe = self.u[BLOCK_DOMAIN[block]]; out = {}
        for (component, label), coefficient in row.items():
            old_word = universe.words[label]
            moved = actor.mul(universe.states[label])
            target = (component, universe.intern(
                moved, word_mul(actor_word, old_word) if old_word is not None else None))
            out[target] = (out.get(target, 0) + int(coefficient)) % MODULUS
        return {key: value for key, value in out.items() if value}

    def occurrence_package(self) -> dict[str, Any]:
        ledger = self.authority.receipt["bridge"]["occurrence_ledger"]
        g760 = self.task193.get("g760")
        require(type(g760) is list and len(g760) == 760 and len(ledger) == 11,
                "occurrence:owners")
        states, words = self.occurrence_states(g760); by_ord = {int(x["ordinal"]): x for x in ledger}
        prefixes = []; w: dict[str, int] = {}; decomposition = {block: {} for block in BLOCKS}
        for item in ledger:
            ordinal = int(item["ordinal"]); block = "P" if str(item["block"]).startswith("P") else str(item["block"])
            domain = BLOCK_DOMAIN[block]; universe = self.u[domain]
            qstate = self.h.CState(universe.q, universe.q.identity, {}); qword: tuple[int, ...] = ()
            for prefix_ordinal in item["fox_prefix_occurrences"]:
                factor, factor_word = self.signed(states, words, by_ord[int(prefix_ordinal)])
                qstate = qstate.mul(factor); qword = word_mul(qword, factor_word)
            raw_state, raw_word = states[int(item["ten_index"])], words[ordinal - 1]
            if int(item["factor_sign"]) > 0:
                pstate, pword = qstate.mul(raw_state), word_mul(qword, raw_word)
            else: pstate, pword = qstate, qword
            inverse_state, drow, _ = self.eval_outer(domain, word_inv(raw_word))
            require(signature(inverse_state) == signature(raw_state.inv()), "occurrence:inverse")
            decomposition[block] = add(decomposition[block],
                                       self.translate_z(drow, block, pstate, pword),
                                       int(item["factor_sign"]))
            left = pstate.mul(raw_state.inv()); left_word = word_mul(pword, word_inv(raw_word))
            llabel, rlabel = universe.intern(left, left_word), universe.intern(pstate, pword)
            w = add(w, {etakey(ordinal, llabel): int(item["factor_sign"]),
                        etakey(ordinal, rlabel): -int(item["factor_sign"])})
            prefixes.append({"block": block, "domain": domain, "pstate": pstate,
                             "pword": pword})
        for block in BLOCKS:
            expected = {(int(p[2]), int(p[3])): value for key, value in self.d1.items()
                        if (p := parts(key))[1] == block}
            require(decomposition[block] == expected, "occurrence:d1:" + block)
        return {"w": w, "prefixes": prefixes}

    def source_actors(self, source: Sequence[int]) -> dict[str, Any]:
        states, words = self.occurrence_states(source); blocks = self.block_products(states, words)
        occurrence = []
        for item, prefix in zip(self.authority.receipt["bridge"]["occurrence_ledger"],
                                self.occ["prefixes"]):
            qstate, qword = states[int(item["ten_index"])], words[int(item["ordinal"]) - 1]
            pstate, pword = prefix["pstate"], prefix["pword"]
            occurrence.append((pstate.mul(qstate).mul(pstate.inv()),
                               word_mul(pword, qword, word_inv(pword))))
        return {"blocks": blocks, "occurrences": occurrence}

    def action(self, row: dict[str, int], actors: dict[str, Any]) -> dict[str, int]:
        out = {}
        for key, coefficient in row.items():
            p = parts(key)
            if p[0] == "z":
                block, component, label = p[1], int(p[2]), int(p[3]); universe = self.u[BLOCK_DOMAIN[block]]
                actor, actor_word = actors["blocks"][block]; old_word = universe.words[label]
                target = zkey(block, component, universe.intern(
                    actor.mul(universe.states[label]),
                    word_mul(actor_word, old_word) if old_word is not None else None))
            elif p[0] == "eta":
                ordinal, label = int(p[1]), int(p[2]); prefix = self.occ["prefixes"][ordinal - 1]
                universe = self.u[prefix["domain"]]; actor, actor_word = actors["occurrences"][ordinal - 1]
                old_word = universe.words[label]
                target = etakey(ordinal, universe.intern(
                    actor.mul(universe.states[label]),
                    word_mul(actor_word, old_word) if old_word is not None else None))
            else: raise Reject("action:coordinate")
            value = (out.get(target, 0) + int(coefficient)) % MODULUS
            if value: out[target] = value
            else: out.pop(target, None)
        return out

    def action_word(self, row: dict[str, int], word: Sequence[int]) -> dict[str, int]:
        current = dict(row)
        for letter in reversed(tuple(word)): current = self.action(current, self.actions[int(letter)])
        return current

    @staticmethod
    def project(row: dict[str, int]) -> dict[str, int]:
        out = {}
        for key, coefficient in row.items():
            p = parts(key)
            if p[0] == "z": target = key
            elif p[0] == "eta":
                ordinal, label = int(p[1]), int(p[2])
                target = ckey("H1" if ordinal <= 3 else "H2" if ordinal <= 6 else "P", label)
            else: raise Reject("project:coordinate")
            value = (out.get(target, 0) + int(coefficient)) % MODULUS
            if value: out[target] = value
            else: out.pop(target, None)
        return out

    def seed(self, index: int) -> dict[str, int]:
        word = tuple(int(x) for x in self.authority.rows[int(index) - 1]["word"])
        return add(self.action(self.fixed, self.source_actors(word)), self.fixed, -1)

    def outer_seeds(self) -> dict[str, Any]:
        seeds = {block: [] for block in BLOCKS}; by_component = {}
        for block in BLOCKS:
            domain = BLOCK_DOMAIN[block]; universe = self.u[domain]
            relations = self.h.checker_pure_relations(3 if domain == "1" else 4)
            require(len(relations) == (2 if domain == "1" else 11), "outer:relations")
            for relation, word in enumerate(relations):
                state, row, _ = self.eval_outer(domain, word)
                identity = self.h.CState(universe.q, universe.q.identity, {})
                require(universe.intern(state) == universe.intern(identity, ()), "outer:identity")
                seeds[block].append(row)
                for (component, label), coefficient in row.items():
                    by_component.setdefault((block, component), []).append(
                        (relation, label, coefficient))
        return {"seeds": seeds, "by_component": by_component}

    def boundary_row(self, block: str, relation: int, word: Sequence[int]) -> dict[str, int]:
        domain = BLOCK_DOMAIN[block]; state, _row, reduced = self.eval_outer(domain, word)
        moved = self.translate_z(self.outer["seeds"][block][int(relation)], block,
                                 state, reduced)
        return {zkey(block, component, label): value
                for (component, label), value in moved.items()}

    def boundary_zero(self, dual: dict[str, int]) -> bool:
        accumulator = {}
        for key, lambda_value in dual.items():
            p = parts(key)
            if p[0] != "z": continue
            block, component, glabel = p[1], int(p[2]), int(p[3]); universe = self.u[BLOCK_DOMAIN[block]]
            g = universe.states[glabel]
            for relation, hlabel, coefficient in self.outer["by_component"].get((block, component), []):
                translation = g.mul(universe.states[hlabel].inv()); tlabel = universe.intern(translation)
                signature0 = (block, relation, tlabel)
                accumulator[signature0] = (accumulator.get(signature0, 0) +
                                            int(lambda_value) * int(coefficient)) % MODULUS
        return not any(accumulator.values())

    def boundary_select(self, dual: dict[str, int]) -> dict[str, int] | None:
        accumulator = {}; translations = {}
        for key, lambda_value in dual.items():
            p = parts(key)
            if p[0] != "z": continue
            block, component, glabel = p[1], int(p[2]), int(p[3]); universe = self.u[BLOCK_DOMAIN[block]]
            g = universe.states[glabel]
            for relation, hlabel, coefficient in self.outer["by_component"].get((block, component), []):
                translation = g.mul(universe.states[hlabel].inv()); tlabel = universe.intern(translation)
                key0 = (block, relation, tlabel)
                accumulator[key0] = (accumulator.get(key0, 0) +
                                     int(lambda_value) * int(coefficient)) % MODULUS
                translations[key0] = translation
        active = sorted(key for key, value in accumulator.items() if value)
        if not active: return None
        block, relation, label = active[0]; universe = self.u[BLOCK_DOMAIN[block]]
        seed = self.outer["seeds"][block][relation]; out = {}
        actor = translations[(block, relation, label)]
        for (component, old_label), coefficient in seed.items():
            target = zkey(block, component,
                          universe.intern(actor.mul(universe.states[old_label])))
            out[target] = (out.get(target, 0) + int(coefficient)) % MODULUS
        row = {key: value for key, value in out.items() if value}
        require(sum(int(value) * dual.get(key, 0) for key, value in row.items()) % MODULUS ==
                accumulator[(block, relation, label)], "outer:correlation")
        return row


def coefficient_terms(raw: Any) -> dict[tuple[tuple[int, ...], int], int]:
    require(type(raw) is list, "member:coefficient_terms")
    out = {}
    for item in raw:
        require(type(item) is dict and type(item.get("prefix")) is list and
                type(item.get("relator_index")) is int and
                1 <= item["relator_index"] <= ROWS, "member:coefficient_item")
        prefix = tuple(int(x) for x in item["prefix"])
        require(word_reduce(prefix) == prefix, "member:prefix_reduced")
        value = int(item.get("coefficient", 0)) % MODULUS
        require(value != 0, "member:zero_coefficient")
        key = (prefix, int(item["relator_index"])); require(key not in out, "member:duplicate_term")
        out[key] = value
    return out


def boundary_terms(raw: Any) -> dict[tuple[str, int, tuple[int, ...]], int]:
    require(type(raw) is list, "member:boundary_slack")
    out = {}
    for item in raw:
        require(type(item) is dict and item.get("block") in BLOCKS and
                type(item.get("translation_word")) is list, "member:boundary_item")
        block, relation = str(item["block"]), int(item.get("relation", -1))
        require(0 <= relation < (2 if block != "P" else 11), "member:boundary_relation")
        word = tuple(int(x) for x in item["translation_word"])
        require(word_reduce(word) == word, "member:boundary_word")
        value = int(item.get("coefficient", 0)) % MODULUS
        require(value != 0, "member:boundary_zero")
        key = (block, relation, word); require(key not in out, "member:boundary_duplicate")
        out[key] = value
    return out


def replay_coefficient(model: CheckerModel,
                       terms: dict[tuple[tuple[int, ...], int], int],
                       projected: bool) -> dict[str, int]:
    out = {}; cache = {}
    for (prefix, relator), coefficient in terms.items():
        if relator not in cache: cache[relator] = model.seed(relator)
        row = model.action_word(cache[relator], prefix)
        out = add(out, model.project(row) if projected else row, coefficient)
    return out


def expected_m(model: CheckerModel,
               terms: dict[tuple[tuple[int, ...], int], int]) -> list[dict[str, Any]]:
    out = []
    for (prefix, relator), coefficient in sorted(
            terms.items(), key=lambda item: (item[0][1], item[0][0])):
        relator_word = tuple(int(x) for x in model.authority.rows[relator - 1]["word"])
        out.append({"coefficient": coefficient, "prefix": list(prefix),
                    "relator_index": relator,
                    "positive_word": list(word_mul(prefix, relator_word)),
                    "negative_word": list(prefix)})
    return out


def check_member(model: CheckerModel, result: dict[str, Any]) -> dict[str, Any]:
    require(result.get("terminal_kind") == "MEMBER" and
            result.get("raw_joint_equality") is True, "member:terminal")
    terms = coefficient_terms(result.get("coefficient_terms"))
    boundaries = boundary_terms(result.get("boundary_slack"))
    combined = replay_coefficient(model, terms, True)
    for (block, relation, word), coefficient in boundaries.items():
        combined = add(combined, model.boundary_row(block, relation, word), coefficient)
    require(combined == model.e1, "member:joint_equality")
    public = [{"coefficient": value, "prefix": list(prefix), "relator_index": relator}
              for (prefix, relator), value in sorted(
                  terms.items(), key=lambda item: (item[0][1], item[0][0]))]
    require(result.get("mu1") == {"language": "sum a_gj g(b_j-1)", "terms": public},
            "member:mu1")
    m = result.get("M", {})
    require(m.get("language") == "sum a_gj ((w r_j)-w)" and
            m.get("boundary_slack_excluded") is True and
            m.get("pairs") == expected_m(model, terms), "member:M")
    require(result.get("checks", {}).get("pointed_coordinate") is True and
            result.get("checks", {}).get("printed_occurrence_zero") is True and
            result.get("checks", {}).get("roof_fibre_pairs") is True,
            "member:checks")
    return {"terminal_kind": "MEMBER", "coefficient_terms": len(terms),
            "boundary_terms": len(boundaries), "M_pairs": len(m["pairs"]),
            "independent_raw_joint_replay": True}


def expand_node(nodes: list[dict[str, Any]], root: int
                ) -> dict[tuple[tuple[int, ...], int], int]:
    require(0 <= int(root) < len(nodes), "proof:root")
    out = {}; stack = [(int(root), 1, ())]
    while stack:
        index, scalar, prefix = stack.pop(); scalar %= MODULUS
        if not scalar: continue
        require(0 <= index < len(nodes), "proof:index")
        item = nodes[index]; kind = item.get("kind")
        if kind == "zero": require(index == 0, "proof:zero")
        elif kind == "seed":
            relator = int(item.get("relator", 0)); require(1 <= relator <= ROWS,
                                                           "proof:relator")
            key = (prefix, relator); value = (out.get(key, 0) + scalar) % MODULUS
            if value: out[key] = value
            else: out.pop(key, None)
        elif kind == "action":
            parent, letter = int(item.get("parent", -1)), int(item.get("letter", 0))
            require(parent < index and letter in ACTION_LETTERS, "proof:action")
            stack.append((parent, scalar, word_mul(prefix, (letter,))))
        elif kind == "linear":
            terms = item.get("terms"); require(type(terms) is list, "proof:linear")
            for pair in terms:
                require(type(pair) is list and len(pair) == 2 and 0 <= int(pair[0]) < index,
                        "proof:linear_edge")
                stack.append((int(pair[0]), scalar * int(pair[1]), prefix))
        elif kind == "boundary":
            raise Reject("proof:boundary_in_pre_basis")
        else: raise Reject("proof:kind")
    return out


def check_nonmember(model: CheckerModel, result: dict[str, Any]) -> dict[str, Any]:
    require(result.get("terminal_kind") == "NONMEMBER", "nonmember:terminal")
    complete = result.get("complete", {})
    require(complete == {"relator_roster": ROWS, "all_relators_processed": True,
                         "pre_action_queue_exhausted": True,
                         "complete_outer_boundary_zero_correlation": True,
                         "inner_boundary_families": 65}, "nonmember:complete")
    nodes, public_basis = result.get("proof_nodes"), result.get("pre_basis")
    require(type(nodes) is list and nodes and nodes[0] == {"kind": "zero"} and
            type(public_basis) is list, "nonmember:proof")
    pre = SmallEchelon(reverse=True); rows = []
    for item in public_basis:
        require(type(item) is dict and type(item.get("proof_node")) is int,
                "nonmember:basis_item")
        terms = expand_node(nodes, int(item["proof_node"]))
        require(bool(terms), "nonmember:basis_ancestry")
        row = replay_coefficient(model, terms, False)
        require(pre.insert(row), "nonmember:basis_independence"); rows.append(row)
    require(len(rows) == int(result.get("search", {}).get("pre_rank", -1)),
            "nonmember:pre_rank")
    for relator in range(1, ROWS + 1):
        require(not pre.reduce(model.seed(relator)), "nonmember:seed_span")
    for row in rows:
        for letter in ACTION_LETTERS:
            require(not pre.reduce(model.action(row, model.actions[letter])),
                    "nonmember:action_closure")
    joint = SmallEchelon(reverse=True)
    for row in rows: joint.insert(model.project(row))
    boundary_columns = 0
    while True:
        require(bool(joint.reduce(model.e1)), "nonmember:target_became_member")
        dual, pairing = joint.dual(model.e1)
        boundary = model.boundary_select(dual)
        if boundary is None: break
        require(joint.insert(boundary), "nonmember:boundary_rank"); boundary_columns += 1
    require(model.boundary_zero(dual) and pairing != 0, "nonmember:dual")
    return {"terminal_kind": "NONMEMBER", "pre_rank": len(rows),
            "joint_rank": len(joint.pivots), "boundary_columns": boundary_columns,
            "all_6441_seeds_and_actions_replayed": True,
            "complete_boundary_zero_correlation": True}


def check(args: argparse.Namespace) -> dict[str, Any]:
    helper = load_helper(); limits = dict(helper.CAPS)
    limits["wall_seconds"] = int(args.seconds); limits["rss_bytes"] = int(args.rss_bytes)
    try:
        meter = helper.Meter(limits); authority = helper.Authority(args, meter)
        arithmetic = helper.CheckerArithmetic(authority, meter); boundary = helper.Boundary(arithmetic, meter)
    except (helper.Reject, helper.ResourceStop) as exc:
        raise Reject(str(exc)) from exc
    task193, task193_id = load_task193(args.task193_receipt, args.task193_verdict)
    receipt, receipt_id = read_json(args.receipt, "producer:receipt", "ci/out")
    check_self(receipt, "producer:receipt")
    producer_source = check_pin(PRODUCER_PIN, "producer:source")
    require(receipt.get("source") == producer_source, "producer:source_binding")
    require(receipt.get("schema") == SCHEMA and receipt.get("status") == "COMPLETE" and
            receipt.get("terminal") in (MEMBER, NONMEMBER) and
            receipt.get("mode") == "PRODUCTION", "producer:envelope")
    require(receipt.get("owners", {}).get("task193_v3") == task193_id,
            "producer:task193_binding")
    task198_owner = receipt.get("owners", {}).get("task198", {})
    require(task198_owner.get("receipt_sha256") == authority.identity.get("receipt_sha256") and
            task198_owner.get("manifest_sha256") == authority.identity.get("manifest_sha256"),
            "producer:task198_binding")
    require(receipt.get("claims", {}).get("A7") == "NONE" and
            receipt.get("claims", {}).get("compatible_lift") == "NONE" and
            receipt.get("claims", {}).get("fake") == "NONE" and
            receipt.get("claims", {}).get("Ihara") == "NONE", "producer:frontier")
    model = CheckerModel(helper, authority, arithmetic, boundary, task193)
    result = receipt.get("result"); require(type(result) is dict, "producer:result")
    checked = check_member(model, result) if receipt["terminal"] == MEMBER else check_nonmember(model, result)
    require(checked["terminal_kind"] == result.get("terminal_kind"), "producer:terminal_kind")
    return seal({"schema": CHECK_SCHEMA, "status": "ACCEPTED",
                 "terminal": receipt["terminal"], "independent": True,
                 "receipt": receipt_id, "task193_v3": task193_id,
                 "task198": authority.identity, "replay": checked,
                 "claims": {"A5_terminal": True,
                            "A6_M": receipt["terminal"] == MEMBER,
                            "A7": "NONE", "compatible_lift": "NONE",
                            "fake": "NONE", "Ihara": "NONE"},
                 "resource": meter.public(strict=False)})


def output_path(raw: str) -> Path:
    path = Path(str(raw).replace("\\", "/")); require(not path.is_absolute() and
            ".." not in path.parts and "." not in path.parts, "output:lexical")
    target = (ROOT / path).resolve(strict=False)
    require(target.parent == (ROOT / "ci/out").resolve(strict=True), "output:containment")
    return target


def write_exclusive(raw: str, value: dict[str, Any]) -> None:
    path = output_path(raw); require(not path.exists(), "output:stale")
    encoded = canon(value) + b"\n"; fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        view = memoryview(encoded)
        while view: view = view[os.write(fd, view):]
        os.fsync(fd)
    finally: os.close(fd)


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(); ap.add_argument("--mode", choices=("PRODUCTION",), default="PRODUCTION")
    ap.add_argument("--task193-receipt", required=True); ap.add_argument("--task193-verdict", required=True)
    ap.add_argument("--receipt", required=True); ap.add_argument("--output", required=True)
    ap.add_argument("--seconds", type=int, default=14_400); ap.add_argument("--rss-bytes", type=int, default=8_000_000_000)
    for key, value in TASK198_DEFAULTS.items():
        ap.add_argument("--task198-" + key, dest="task198_" + key, default=value)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        require(args.seconds == 14_400 and args.rss_bytes == 8_000_000_000,
                "arguments:frozen_caps")
        verdict = check(args); write_exclusive(args.output, verdict)
        print(CHECKER_LINE + " terminal=" + verdict["terminal"], flush=True); return 0
    except (Reject, OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(CHECKER_LINE + "_ERROR " + str(exc), flush=True); return 1
    except Exception as exc:
        print(CHECKER_LINE + "_ERROR " + str(exc), flush=True); return 1


if __name__ == "__main__": raise SystemExit(main(sys.argv[1:]))
