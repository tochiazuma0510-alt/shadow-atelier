#!/usr/bin/env python3
"""R07 u0/v0 boundary-preimage decision (task 187).

The task179 producer is loaded only after byte authentication and is used as
an arithmetic source.  This module owns the boundary-only F3 echelon,
coefficient ancestry, and complete support-times-occurrence dual audit.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import itertools
import json
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-u0v0-boundary-preimage/v1"
SELFTEST_SCHEMA = "d972-r07-u0v0-boundary-preimage-selftest/v1"
COMMON = "R07_U0V0_BOUNDARY_PREIMAGE_V1"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
FIXTURE = ROOT / "search/certs/d972_r07_u0v0_boundary_preimage_selftest_v1_20260827.json"

PINS = {
    "task179_producer": ("search/d972_r07_positive_common_word_colgen_v1.py", 123870,
        "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    "task179_checker": ("crosscheck/check_d972_r07_positive_common_word_colgen_v1.py", 73780,
        "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"),
    "task179_driver": ("search/d972_r07_positive_common_word_colgen_gha_driver_v1.g", 12872,
        "48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"),
    "task179_fixture": ("search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json", 407,
        "46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"),
    "v156": ("sol/proof_r07_task179_exact_exponent_lattice_v156.md", 10409,
        "2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d"),
    "v157": ("sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md", 8367,
        "08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8"),
    "selftest_fixture": ("search/certs/d972_r07_u0v0_boundary_preimage_selftest_v1_20260827.json", 699,
        "230de05643a94f775120ef7e62b2f2023b13fd12228f18ca860ef81b134babff"),
}
MUTATIONS = (
    "roster_ordinal", "exponent_sign", "u0_formula", "v0_formula",
    "target_sign", "block_tag", "boundary_coefficient", "left_translation",
    "coefficient_two_inverse", "pivot_ancestry", "positive_residual",
    "terminal_dual_coefficient", "sampled_as_complete", "resource_stop_nonmember",
    "boundary_provenance",
)
ALLOWED_RESOURCE_CAPS = {
    "task175_reconstruction": {"wall_seconds", "rss_bytes"},
    "fine_deletion": {"wall_seconds", "rss_bytes"},
    "Q0_positive_shortlex_section": {"wall_seconds", "rss_bytes"},
    "Q0_discovery": {"wall_seconds", "rss_bytes"},
    "A_L_membership_scan": {"wall_seconds", "rss_bytes"},
    "L_subgroup_closure": {"wall_seconds", "rss_bytes"},
    "typed_singleton_equality": {"wall_seconds", "rss_bytes"},
    "runtime_reconstruction": {"wall_seconds", "rss_bytes"},
    "complete_boundary_correlation": {"wall_seconds", "rss_bytes", "boundary_pairs"},
    "boundary_echelon": {"wall_seconds", "rss_bytes", "retained_columns"},
}


class ResourceStop(RuntimeError):
    def __init__(self, phase: str, cap: str, value: int | float, limit: int | float,
                 resource: dict[str, Any] | None = None):
        super().__init__(f"{phase}:{cap}:{value}>{limit}")
        self.phase, self.cap, self.value, self.limit = phase, cap, value, limit
        self.resource = resource


class InputStop(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_obj(value: Any) -> str:
    return sha256(canonical(value))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value); result.pop("self_digest", None)
    result["self_digest"] = sha_obj(result)
    return result


def authenticate_sources() -> dict[str, dict[str, Any]]:
    result = {}
    for name, (rel, size, digest) in PINS.items():
        path = ROOT / rel
        raw = path.read_bytes() if path.is_file() else b""
        if len(raw) != size or sha256(raw) != digest:
            raise InputStop("pin:" + rel)
        result[name] = {"path": rel, "bytes": size, "sha256": digest}
    # The task179 producer authenticates every arithmetic source in its own
    # complete PINS table.  Calling that gate is part of this receipt.
    return result


def load_task179() -> Any:
    path = ROOT / PINS["task179_producer"][0]
    spec = importlib.util.spec_from_file_location("d972_task179_boundary_source", path)
    if spec is None or spec.loader is None:
        raise InputStop("task179 loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        module._boundary_task179_pins = module.authenticate_inputs()
    except module.InputStop as exc:
        raise InputStop("task179:" + str(exc)) from exc
    return module


def reduce_word(word: Iterable[int]) -> tuple[int, ...]:
    out: list[int] = []
    for raw in word:
        x = int(raw)
        require(x != 0 and abs(x) <= 2, "free-group letter")
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def inverse_word(word: Sequence[int]) -> tuple[int, ...]:
    return tuple(-int(x) for x in reversed(word))


def multiply(*words: Sequence[int]) -> tuple[int, ...]:
    out: tuple[int, ...] = ()
    for word in words:
        out = reduce_word(out + tuple(int(x) for x in word))
    return out


def power(word: Sequence[int], count: int) -> tuple[int, ...]:
    out: tuple[int, ...] = ()
    for _ in range(count):
        out = multiply(out, word)
    return out


def integer_exponent(word: Sequence[int]) -> tuple[int, int]:
    x = y = 0
    for letter in word:
        if letter == 1: x += 1
        elif letter == -1: x -= 1
        elif letter == 2: y += 1
        elif letter == -2: y -= 1
        else: raise RuntimeError("invalid signed letter")
    return x, y


def normalized_residue(word: Sequence[int]) -> tuple[int, int]:
    e = integer_exponent(word)
    require(e[0] % 18 == 0 and e[1] % 18 == 0, "integer exponent not divisible by 18")
    return (e[0] // 18 % 3, e[1] // 18 % 3)


def strip_exponents(v1: Any, row: dict[bytes, int]) -> dict[bytes, int]:
    answer = dict(row)
    for index in (1, 2):
        answer.pop(v1.exponent_key(index), None)
    require(not any(key.startswith(b"E") for key in answer), "unexpected exponent key")
    return answer


def add_scaled(target: dict[bytes, int], source: dict[bytes, int], scalar: int) -> None:
    scalar %= 3
    for key, value in source.items():
        z = (target.get(key, 0) + scalar * int(value)) % 3
        if z: target[key] = z
        else: target.pop(key, None)


def pair(functional: dict[bytes, int], row: dict[bytes, int]) -> int:
    return sum(int(a) * int(row.get(k, 0)) for k, a in functional.items()) % 3


class Echelon:
    """F3 echelon retaining every original-column coefficient ancestry."""
    def __init__(self) -> None:
        self.rows: dict[bytes, dict[bytes, int]] = {}
        self.ancestry: dict[bytes, dict[int, int]] = {}
        self.order: list[bytes] = []

    @staticmethod
    def combine(left: dict[int, int], right: dict[int, int], scalar: int) -> None:
        for key, value in right.items():
            z = (left.get(key, 0) + scalar * value) % 3
            if z: left[key] = z
            else: left.pop(key, None)

    def reduce(self, source: dict[bytes, int]) -> tuple[dict[bytes, int], dict[int, int]]:
        row = dict(source); coeff: dict[int, int] = {}
        for pivot in self.order:
            value = row.get(pivot, 0)
            if value:
                add_scaled(row, self.rows[pivot], -value)
                self.combine(coeff, self.ancestry[pivot], value)
        return row, coeff

    def add(self, source: dict[bytes, int], column_id: int) -> tuple[bytes, dict[int, int]]:
        row = dict(source); ancestry = {column_id: 1}
        for pivot in self.order:
            value = row.get(pivot, 0)
            if value:
                add_scaled(row, self.rows[pivot], -value)
                self.combine(ancestry, self.ancestry[pivot], -value)
        require(row, "dependent boundary column")
        pivot = min(row); inv = 1 if row[pivot] == 1 else 2
        self.rows[pivot] = {k: inv * v % 3 for k, v in row.items() if inv * v % 3}
        self.ancestry[pivot] = {k: inv * v % 3 for k, v in ancestry.items() if inv * v % 3}
        self.order.append(pivot)
        return pivot, self.ancestry[pivot]

    def dual(self, target: dict[bytes, int]) -> dict[bytes, int]:
        remainder, _ = self.reduce(target)
        require(remainder, "dual requested after membership")
        functional = {min(remainder): 1}
        for pivot in reversed(self.order):
            value = -sum(c * functional.get(k, 0) for k, c in self.rows[pivot].items() if k != pivot) % 3
            if value: functional[pivot] = value
            else: functional.pop(pivot, None)
        require(all(pair(functional, self.rows[p]) == 0 for p in self.order), "dual annihilation")
        require(pair(functional, target) != 0, "dual target pairing")
        return functional


class Budget:
    def __init__(self, args: argparse.Namespace):
        self.start = time.monotonic()
        self.limits = {"wall_seconds": int(args.seconds), "boundary_pairs": int(args.boundary_pairs),
                       "fibre_scans": int(args.fibre_scans), "candidate_words": int(args.candidate_words),
                       "retained_columns": int(args.retained_columns), "checkpoint_bytes": int(args.checkpoint_bytes),
                       "rss_bytes": int(args.rss_bytes), "oracle_rounds": int(args.oracle_rounds),
                       "global_roster": 357128352}
        self.counters = {name: 0 for name in self.limits if name != "rss_bytes" and name != "wall_seconds"}
        self.phase = "initialization"

    def rss(self) -> int:
        try:
            import resource
            value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            return value if sys.platform == "darwin" else value * 1024
        except (ImportError, AttributeError):
            return 0

    def check(self, phase: str = "search") -> None:
        self.phase = phase
        elapsed = time.monotonic() - self.start
        rss = self.rss()
        if elapsed > self.limits["wall_seconds"]:
            raise ResourceStop(phase, "wall_seconds", elapsed, self.limits["wall_seconds"], self.snapshot(elapsed, rss))
        if rss and rss > self.limits["rss_bytes"]:
            raise ResourceStop(phase, "rss_bytes", rss, self.limits["rss_bytes"], self.snapshot(elapsed, rss))

    def bump(self, name: str, amount: int = 1, phase: str = "search") -> None:
        self.phase = phase; self.counters[name] += amount
        if self.counters[name] > self.limits[name]:
            elapsed = time.monotonic() - self.start; rss = self.rss()
            raise ResourceStop(phase, name, self.counters[name], self.limits[name], self.snapshot(elapsed, rss))
        if (self.counters[name] & 4095) == 0:
            self.check(phase)

    def snapshot(self, elapsed: float, rss: int) -> dict[str, Any]:
        return {"phase": self.phase, "elapsed_seconds": elapsed, "rss_bytes": rss,
                "limits": dict(self.limits), "counters": dict(self.counters), "single_process": True}

    def public(self) -> dict[str, Any]:
        return self.snapshot(time.monotonic() - self.start, self.rss())


def full_boundary_correlation(v1: Any, runtime: dict[str, Any], dual: dict[bytes, int], budget: Budget) -> dict[str, Any]:
    """Scan all PB3/PB4 translated occurrences; no sampled early exit."""
    support: dict[tuple[int, int], list[tuple[bytes, int, Any]]] = {}
    for key, coefficient in dual.items():
        if key[:1] == b"R":
            block, component, blob = v1.decode_row_key(key)
            support.setdefault((block, component), []).append(
                (blob, coefficient, v1.unpack_element(runtime, blob, block)))
    accumulated: dict[tuple[int, bytes, int], int] = {}
    contributors: dict[tuple[int, bytes, int], list[dict[str, Any]]] = {}
    for block, count in ((1, 2), (2, 2), (3, 11)):
        quotient = v1.group_for_block(runtime, block)
        for index in range(1, count + 1):
            source = v1.boundary_source(runtime, block, index)
            occurrences = []
            for component0, h_hex, base0 in source:
                h_blob = bytes.fromhex(str(h_hex)); h = v1.unpack_element(runtime, h_blob, block)
                occurrences.append((int(component0), h_blob, h, quotient.inverse(h), int(base0)))
            for component, h_blob, h, h_inv, base0 in occurrences:
                for g_blob, lam, g in support.get((block, component), []):
                    budget.bump("boundary_pairs", 1, "complete_boundary_correlation")
                    translation = quotient.mul(g, h_inv)
                    require(quotient.mul(translation, h) == g, "left translation t*h=g")
                    t_blob = v1.element_blob(runtime, translation)
                    k = (block, t_blob, index)
                    z = (base0 * int(lam)) % 3
                    accumulated[k] = (accumulated.get(k, 0) + z) % 3
                    contributors.setdefault(k, []).append({"component": component,
                        "g_hex": g_blob.hex(), "h_hex": h_blob.hex(),
                        "lambda_coefficient": int(lam), "base_coefficient": base0 % 3})
    for key in contributors:
        contributors[key].sort(key=lambda row: (int(row["component"]), str(row["g_hex"]),
                                                  str(row["h_hex"]), int(row["lambda_coefficient"]),
                                                  int(row["base_coefficient"])))
    active_internal = sorted((b, t, i) for (b, t, i), value in accumulated.items() if value % 3)
    active = [[b, t.hex(), i] for b, t, i in active_internal]
    return {"complete": True, "sampled": False, "active": active,
            "scanned_occurrences": sum(len(v) for v in contributors.values()),
            "contributors": {f"{b}:{t.hex()}:{i}": rows for (b, t, i), rows in contributors.items()},
            "accumulated": {f"{b}:{t.hex()}:{i}": int(value) % 3
                            for (b, t, i), value in accumulated.items() if value % 3}}


def make_target(v1: Any, runtime: dict[str, Any], model: Any, word: Sequence[int]) -> tuple[dict[bytes, int], dict[str, Any]]:
    raw, replay = model.direct_column([], list(word))
    stripped = strip_exponents(v1, raw)
    target = {}; add_scaled(target, stripped, -1)
    return target, {"A": v1.public_sparse(stripped), "A_sha256": sha_obj(v1.public_sparse(stripped)),
                    "target": v1.public_sparse(target), "target_sha256": sha_obj(v1.public_sparse(target)),
                    "direct_replay": replay}


def registered_words(runtime: dict[str, Any]) -> dict[str, tuple[int, ...]]:
    result = {}
    for ordinal in (3, 9, 12):
        matches = [row["word"] for row in runtime["roster"]
                   if row.get("layer") == "q0_relator" and int(row.get("ordinal")) == ordinal]
        require(len(matches) == 1, "registered q0 relator ordinal")
        result[str(ordinal)] = tuple(matches[0])
    return result


def build_u0v0(runtime: dict[str, Any]) -> dict[str, tuple[int, ...]]:
    r = registered_words(runtime)
    v0 = multiply(r["9"], r["12"], power(inverse_word(r["3"]), 2))
    u0 = multiply(r["9"], power(inverse_word(v0), 8))
    require(integer_exponent(v0) == (0, 18) and integer_exponent(u0) == (18, 0), "u0/v0 integer exponents")
    for word in (r["3"], r["9"], r["12"], u0, v0):
        require(runtime["joint_group"].eval(list(word)) == runtime["joint_group"].identity, "joint-kernel word")
    return {**r, "u0": u0, "v0": v0}


def boundary_column(v1: Any, runtime: dict[str, Any], provenance: dict[str, Any]) -> dict[bytes, int]:
    return v1.translated_boundary(runtime, int(provenance["block"]), int(provenance["base_relator_index"]),
                                  bytes.fromhex(provenance["translation_hex"]))


def toy_complete_correlation(dual: dict[bytes, int], rows: Sequence[dict[bytes, int]]) -> dict[str, Any]:
    active = [index for index, row in enumerate(rows, 1) if pair(dual, row)]
    return {"complete": True, "sampled": False, "active": active,
            "pairings": [pair(dual, row) for row in rows]}


def toy_perm_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i] - 1] for i in range(len(left)))


def toy_perm_inv(value: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(value)
    for index, image in enumerate(value, 1): out[image - 1] = index
    return tuple(out)


def toy_key(block: int, component: int, value: tuple[int, ...]) -> bytes:
    require(block in (1, 2) and component in (1, 2, 3), "toy typed block")
    return b"R" + bytes((block, component)) + bytes(value)


def toy_left_translation(block: int, translation: tuple[int, ...], source: Sequence[tuple[int, tuple[int, ...], int]]) -> dict[bytes, int]:
    answer = {}
    for component, h, coefficient in source:
        g = toy_perm_mul(translation, h)
        key = toy_key(block, component, g)
        answer[key] = (answer.get(key, 0) + coefficient) % 3
    return {key: value for key, value in answer.items() if value}


def solve(args: argparse.Namespace) -> dict[str, Any]:
    pins = authenticate_sources()
    v1 = load_task179()
    budget = Budget(args)
    monitor = v1.Monitor(args)
    try:
        runtime = v1.build_runtime(monitor)
    except v1.ResourceStop as exc:
        phase = getattr(exc, "phase", "task179"); cap = getattr(exc, "cap", "unknown")
        monitor.phase = phase
        snapshot = monitor.public()
        if cap == "wall_seconds": snapshot["elapsed_seconds"] = getattr(exc, "value", snapshot["elapsed_seconds"])
        if cap == "rss_bytes": snapshot["rss_bytes"] = getattr(exc, "value", snapshot["rss_bytes"])
        raise ResourceStop(phase, cap,
                           getattr(exc, "value", 0), getattr(exc, "limit", 0), snapshot) from exc
    except v1.InputStop as exc:
        raise InputStop("task179:" + str(exc)) from exc
    budget.check("runtime_reconstruction")
    words = build_u0v0(runtime)
    model = v1.AllSevenModel(runtime)
    targets = {}
    for label in ("u0", "v0"):
        target, public = make_target(v1, runtime, model, words[label])
        targets[label] = {"word": list(words[label]), "integer_exponent": list(integer_exponent(words[label])),
                          "normalized_residue": list(normalized_residue(words[label])), **public,
                          "target_row": target, "decision": None, "chain": [], "terminal_dual": None}
    echelon = Echelon(); columns: list[dict[str, Any]] = []; transitions = []
    unresolved = ["u0", "v0"]
    while unresolved:
        for label in list(unresolved):
            item = targets[label]; target = item["target_row"]
            remainder, solution = echelon.reduce(target)
            if not remainder:
                chain = [[int(k), int(v) % 3] for k, v in sorted(solution.items())]
                literal = {}; [add_scaled(literal, columns[k - 1]["row_dict"], c) for k, c in chain]
                require(literal == target, label + " boundary sum")
                item["decision"] = "MEMBER_D"; item["chain"] = chain
                item["literal_boundary_sum"] = v1.public_sparse(literal)
                item["zero_residual"] = v1.public_sparse({})
                item["zero_residual_sha256"] = sha_obj([])
                unresolved.remove(label)
                continue
            dual = echelon.dual(target)
            correlation = full_boundary_correlation(v1, runtime, dual, budget)
            budget.check("complete_boundary_correlation")
            if not correlation["active"]:
                item["decision"] = "NONMEMBER_D"
                item["terminal_dual"] = {"row": v1.public_sparse(dual), "row_sha256": sha_obj(v1.public_sparse(dual)),
                    "pairing_target": pair(dual, target), "annihilates_retained": True,
                    "full_correlation": correlation}
                unresolved.remove(label)
                continue
            block, translation_hex, index = correlation["active"][0]
            translation_blob = bytes.fromhex(translation_hex)
            provenance = {"family": "boundary", "block": block, "base_relator_index": index,
                "translation_hex": translation_blob.hex(), "left_translation": "t=g*h^-1; t*h=g",
                "active_key": [block, translation_blob.hex(), index],
                "complete_support_occurrence_accumulation": True,
                "contributing_pairs": correlation["contributors"].get(f"{block}:{translation_blob.hex()}:{index}", []),
                "scalar": 0}
            row = boundary_column(v1, runtime, provenance)
            before = len(echelon.order); budget.bump("retained_columns", 1, "boundary_echelon")
            pivot, ancestry = echelon.add(row, len(columns) + 1)
            budget.check("boundary_echelon")
            require(len(echelon.order) == before + 1, "retained boundary row did not raise rank")
            provenance["scalar"] = pair(dual, row)
            record = {"column_id": len(columns) + 1, "rank_before": before, "rank_after": len(echelon.order),
                "family": "boundary", "sparse_row": v1.public_sparse(row),
                "sparse_row_sha256": sha_obj(v1.public_sparse(row)), "active_dual": v1.public_sparse(dual),
                "active_dual_sha256": sha_obj(v1.public_sparse(dual)), "dual_pairing": pair(dual, row),
                "pivot_hex": pivot.hex(), "pivot_ancestry": [[k, v] for k, v in sorted(ancestry.items())],
                "provenance": provenance, "row_dict": row}
            require(record["dual_pairing"] != 0, "ACTIVE dual gate")
            columns.append(record)
            transitions.append({"column_id": record["column_id"], "rank_before": before,
                                "rank_after": len(echelon.order), "pivot_hex": pivot.hex(),
                                "pivot_ancestry": record["pivot_ancestry"], "target_reconsidered": ["u0", "v0"]})
    for item in targets.values(): item.pop("target_row")
    for record in columns: record.pop("row_dict")
    both = all(item["decision"] == "MEMBER_D" for item in targets.values())
    return {"schema": SCHEMA, "status": "PASS", "terminal": COMMON,
            "pins": pins, "task179_arithmetic_authentication": "delegated complete v1 PINS",
            "task179_arithmetic_pins": v1._boundary_task179_pins,
            "words": {k: list(v) for k, v in words.items()}, "targets": targets,
            "columns": columns, "rank_transitions": transitions, "rank": len(echelon.order),
            "finite_consequence": "nu(ker(A on correction plus boundary coefficients)) = F3^2" if both else None,
            "normalization_rule": "c1=c q(u0,a) q(v0,b), d1=d-a*d_u-b*d_v; q(w,0)=1, q(w,1)=w^-1, q(w,2)=w; registered cubes exactify the integer exponent" if both else None,
            "q_table": {"q(w,0)": "1", "q(w,1)": "w^-1", "q(w,2)": "w"} if both else None,
            "word_exponents": {k: list(integer_exponent(v)) for k, v in words.items()},
            "claims": {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False},
            "resource": budget.public()}


def toy_echelon_selftest() -> dict[str, Any]:
    identity, sigma, tau = (1, 2, 3), (2, 1, 3), (1, 3, 2)
    require(toy_perm_mul(sigma, tau) != toy_perm_mul(tau, sigma), "toy noncommutativity")
    source_one = [(1, identity, 1), (2, sigma, 1)]
    source_two = [(1, identity, 1), (2, tau, 1)]
    first = toy_left_translation(1, tau, source_one)
    second = toy_left_translation(1, tau, source_two)
    a = toy_key(1, 1, toy_perm_mul(tau, identity))
    b = toy_key(1, 2, toy_perm_mul(tau, sigma))
    c = toy_key(1, 3, identity)
    d = toy_key(1, 2, identity)
    require(first == {a: 1, b: 1} and second == {a: 1, d: 1} and
            toy_perm_mul(tau, identity) == (1, 3, 2), "toy left translation")
    inverse_row = toy_left_translation(1, toy_perm_inv(tau), [(1, identity, 2)])
    require(inverse_row == {toy_key(1, 1, toy_perm_inv(tau)): 2}, "toy coefficient-two inverse")
    boundary = [first, second]
    full_family = [toy_left_translation(1, translation, source)
                   for translation in itertools.permutations((1, 2, 3))
                   for source in (source_one, source_two)]
    require(len(full_family) == 12 and len({tuple(sorted(row.items())) for row in full_family}) == 12,
            "toy complete translated family")
    require(d in toy_left_translation(1, toy_perm_inv(sigma), source_one), "toy in-orbit boundary check")
    inside = first; outside = {c: 1}
    e = Echelon(); rows = []
    for row in boundary:
        pivot, ancestry = e.add(row, len(rows) + 1)
        rows.append({"row": row, "pivot": pivot.hex(), "ancestry": sorted(ancestry.items())})
    rem, coeff = e.reduce(inside); require(not rem and coeff == {1: 1}, "toy positive chain")
    full_e = Echelon()
    for number, row in enumerate(full_family, 1):
        if full_e.reduce(row)[0]: full_e.add(row, number)
    dual = full_e.dual(outside); correlation = toy_complete_correlation(dual, full_family)
    require(pair(dual, outside) != 0 and correlation == {"complete": True, "sampled": False,
            "active": [], "pairings": [0] * 12}, "toy terminal dual")
    state = {"roster_ordinal": 3, "exponent_sign": 1, "u0_formula": "r9*v0^-8", "v0_formula": "r9*r12*r3^-2",
             "target_sign": -1, "block_tag": 1, "boundary_coefficient": 1, "left_translation": "t*h=g",
             "coefficient_two_inverse": True, "pivot_ancestry": [[1, 2], [2, 1]], "positive_residual": [],
             "terminal_dual_coefficient": 1, "sampled_as_complete": False, "resource_stop_nonmember": False,
             "boundary_provenance": True, "resource_stop": True}
    def valid(x: dict[str, Any]) -> None:
        roster = {3: (1, 2, 1, -2), 9: (1, 2), 12: (2, 1)}
        selected = roster.get(x["roster_ordinal"])
        require(selected is not None and x["exponent_sign"] in (1, -1), "toy roster replay")
        signed = tuple(x["exponent_sign"] * letter for letter in selected)
        require(integer_exponent(signed) == (2, 0), "toy exponent-sign replay")
        v0_expected = multiply(roster[9], roster[12], inverse_word(roster[3]), inverse_word(roster[3]))
        v0_value = (v0_expected if x["v0_formula"] == "r9*r12*r3^-2"
                    else multiply(roster[9], roster[12], roster[3], roster[3]))
        require(v0_value == v0_expected, "toy v0 formula replay")
        u0_expected = multiply(roster[9], *([inverse_word(v0_expected)] * 8))
        u0_value = (u0_expected if x["u0_formula"] == "r9*v0^-8"
                    else multiply(roster[9], *([v0_expected] * 8)))
        require(u0_value == u0_expected, "toy u0 formula replay")
        signed_target = {key: (x["target_sign"] * value) % 3 for key, value in inside.items()}
        require(x["target_sign"] == -1 and signed_target == {key: (-value) % 3 for key, value in inside.items()},
                "toy target-sign replay")
        require(x["block_tag"] in (1, 2, 3) and toy_key(x["block_tag"], 1, tau) == a and
                all(key[:2] == b"R\x01" for key in first), "toy block arithmetic")
        translated = toy_left_translation(1, tau, [(1, identity, x["boundary_coefficient"]), (2, sigma, 1)])
        require(x["boundary_coefficient"] in (1, 2) and translated == first and
                toy_left_translation(1, tau, source_one) == first and x["left_translation"] == "t*h=g",
                "toy translated boundary arithmetic")
        require(x["coefficient_two_inverse"] is True and
                toy_left_translation(1, toy_perm_inv(tau), [(1, identity, 2)]) == inverse_row and
                inverse_row[toy_key(1, 1, toy_perm_inv(tau))] == 2,
                "toy coefficient/residual arithmetic")
        residual = dict(inside); add_scaled(residual, inside, -1)
        require(x["positive_residual"] == [] and not residual, "toy positive residual arithmetic")
        require(x["terminal_dual_coefficient"] == dual.get(c) == 1 and
                x["sampled_as_complete"] is False and x["resource_stop_nonmember"] is False and
                x["boundary_provenance"] is True and
                c not in set().union(*(row.keys() for row in full_family)),
                "toy terminal/provenance arithmetic")
        actual = Echelon()
        for number, row in enumerate(boundary, 1):
            pivot, ancestry = actual.add(row, number)
            if number == 2:
                require(ancestry == dict(x["pivot_ancestry"]), "toy ancestry mutation")
            require(pivot in actual.rows and ancestry, "toy pivot replay")
        complete = Echelon()
        for number, row in enumerate(full_family, 1):
            if complete.reduce(row)[0]: complete.add(row, number)
        candidate_dual = complete.dual(outside)
        require(not actual.reduce(inside)[0] and pair(candidate_dual, outside) != 0 and
                toy_complete_correlation(candidate_dual, full_family) == correlation and
                all(pair(candidate_dual, row) == 0 for row in full_family), "toy complete replay")
    mutators = [
        lambda x: x.__setitem__("roster_ordinal", 4), lambda x: x.__setitem__("exponent_sign", -1),
        lambda x: x.__setitem__("u0_formula", "r9*v0^8"), lambda x: x.__setitem__("v0_formula", "r9*r12*r3^2"),
        lambda x: x.__setitem__("target_sign", 1), lambda x: x.__setitem__("block_tag", 2),
        lambda x: x.__setitem__("boundary_coefficient", 2), lambda x: x.__setitem__("left_translation", "h*t=g"),
        lambda x: x.__setitem__("coefficient_two_inverse", False), lambda x: x.__setitem__("pivot_ancestry", []),
        lambda x: x.__setitem__("positive_residual", [["bad", 1]]), lambda x: x.__setitem__("terminal_dual_coefficient", 2),
        lambda x: x.__setitem__("sampled_as_complete", True), lambda x: x.__setitem__("resource_stop_nonmember", True),
        lambda x: x.__setitem__("boundary_provenance", False),
    ]
    rejected = 0
    for mutate in mutators:
        candidate = copy.deepcopy(state); mutate(candidate)
        try: valid(candidate)
        except RuntimeError: rejected += 1
    probe = Budget(argparse.Namespace(seconds=999, boundary_pairs=0,
                    fibre_scans=10**9, candidate_words=10**9,
                    retained_columns=0, checkpoint_bytes=10**12,
                    rss_bytes=10**18, oracle_rounds=10**6))
    stopped = False
    try: probe.bump("boundary_pairs", 1, "toy_resource_stop")
    except ResourceStop: stopped = True
    require(stopped, "toy ResourceStop path")
    require(rejected == len(MUTATIONS), "toy mutation suite")
    transition_public = [{"row": [[k.hex(), int(v)] for k, v in sorted(item["row"].items())],
                          "pivot": item["pivot"], "ancestry": [[int(k), int(v)] for k, v in item["ancestry"]]}
                         for item in rows]
    return {"schema": SELFTEST_SCHEMA, "status": "PASS", "terminal": COMMON + "_SELFTEST_PASS",
            "mutation_controls": {"attempted": len(MUTATIONS), "rejected": rejected, "names": list(MUTATIONS)},
            "toy": {"boundary_rows": [[k.hex(), v] for k, v in sorted(first.items())],
                    "inside_target": [[k.hex(), v] for k, v in sorted(inside.items())],
                    "outside_target": [[k.hex(), v] for k, v in sorted(outside.items())],
                    "positive_chain": [[1, 1]],
                    "negative_dual": [[k.hex(), v] for k, v in sorted(dual.items())],
                    "full_correlation": True, "rank_transitions": transition_public,
                    "noncommutative": {"sigma": list(sigma), "tau": list(tau),
                        "sigma_tau": list(toy_perm_mul(sigma, tau)), "tau_sigma": list(toy_perm_mul(tau, sigma)),
                        "left_translation": True, "block_tagging": True,
                        "coefficient_two_inverse": True, "resource_stop": stopped}}}


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value) + b"\n")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), default=None)
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--output", "--receipt", dest="output", type=Path, default=None)
    p.add_argument("--seconds", type=int, default=19800)
    p.add_argument("--boundary-pairs", type=int, default=8000000)
    p.add_argument("--fibre-scans", type=int, default=80000000)
    p.add_argument("--candidate-words", type=int, default=2000000)
    p.add_argument("--retained-columns", type=int, default=250000)
    p.add_argument("--checkpoint-bytes", type=int, default=4000000000)
    p.add_argument("--rss-bytes", type=int, default=5700000000)
    p.add_argument("--oracle-rounds", type=int, default=1)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    mode = "SELFTEST" if args.selftest else (args.mode or "SELFTEST")
    if mode == "SELFTEST":
        receipt = toy_echelon_selftest()
        if args.output: write_json(args.output, seal(receipt))
        print("R07_U0V0_BOUNDARY_PREIMAGE_V1_PRODUCER_SELFTEST_PASS")
        return 0
    output = args.output or (ROOT / "ci/out/d972_r07_u0v0_boundary_preimage_v1.json")
    try:
        receipt = solve(args)
    except InputStop as exc:
        receipt = {"schema": SCHEMA, "status": UNKNOWN_INPUT, "terminal": f"{UNKNOWN_INPUT}:{exc}",
                   "reason": str(exc), "pins": authenticate_sources(), "negative_claim": False,
                   "claims": {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False}}
    except ResourceStop as exc:
        resource = dict(exc.resource or {})
        require(resource.get("phase") == exc.phase, "resource snapshot phase")
        resource.update({"terminal_cap": exc.cap, "terminal_value": exc.value,
                          "terminal_limit": exc.limit})
        receipt = {"schema": SCHEMA, "status": UNKNOWN_RESOURCE,
                   "terminal": f"{UNKNOWN_RESOURCE}:{exc.phase}:{exc.cap}:{exc.value}>{exc.limit}",
                   "reason": str(exc), "pins": authenticate_sources(), "negative_claim": False,
                   "claims": {"raw_task179_word": False, "cofinal_lift": False, "fake": False, "ihara": False},
                   "resource": resource}
    write_json(output, seal(receipt))
    print("R07_U0V0_BOUNDARY_PREIMAGE_V1_PRODUCER_TERMINAL " + receipt["terminal"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
