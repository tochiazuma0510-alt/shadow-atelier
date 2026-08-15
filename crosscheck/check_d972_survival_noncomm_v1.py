#!/usr/bin/env python3
"""Independent checker for task 134.

This checker does not import the producer.  It represents truncated Magnus
series as frozensets of literal binary words (the producer uses packed integer
bit masks), and it reconstructs G9 as a degree-27 permutation group (the
producer uses dihedral coordinate triples).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import sys
import tempfile
import time
from collections import Counter, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRODUCER = ROOT / "search/certs/d972_survival_noncomm_v1_20260815.json"
DEFAULT_INPUT = ROOT / "search/certs/nf972_sourcemap_a_tuples_v2_20260804.json"
DEFAULT_OUTPUT = ROOT / "crosscheck/verdicts/d972_survival_noncomm_v1_20260815.json"
DEFAULT_CHECKPOINT = ROOT / "crosscheck/verdicts/.d972_survival_noncomm_v1_checkpoint.json"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def atomic_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(obj, fh, ensure_ascii=False, sort_keys=True, indent=2)
            fh.write("\n")
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise


class Clock:
    def __init__(self, seconds: float):
        self.start = time.monotonic()
        self.seconds = seconds

    def check(self, where: str) -> None:
        if time.monotonic() - self.start > self.seconds:
            raise TimeoutError(f"hard timeout at {where}")

    def ms(self) -> int:
        return round(1000 * (time.monotonic() - self.start))


Word = tuple[int, ...]
Element = frozenset[Word]
IDENTITY: Element = frozenset()


class DenseMagnus:
    def __init__(self, cutoff: int):
        self.cutoff = cutoff
        self.x: Element = frozenset({(0,)})
        self.y: Element = frozenset({(1,)})

    @staticmethod
    def xor_sets(*sets: set[Word]) -> set[Word]:
        out: set[Word] = set()
        for source in sets:
            for word in source:
                if word in out:
                    out.remove(word)
                else:
                    out.add(word)
        return out

    def mul(self, a: Element, b: Element) -> Element:
        product: set[Word] = set()
        for left in a:
            for right in b:
                word = left + right
                if len(word) < self.cutoff:
                    if word in product:
                        product.remove(word)
                    else:
                        product.add(word)
        return frozenset(self.xor_sets(set(a), set(b), product))

    def power(self, a: Element, n: int) -> Element:
        if n < 0:
            return self.power(self.inverse(a), -n)
        out = IDENTITY
        base = a
        while n:
            if n & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            n >>= 1
        return out

    def order(self, a: Element) -> int:
        out = IDENTITY
        for n in range(1, 65):
            out = self.mul(out, a)
            if out == IDENTITY:
                return n
        raise AssertionError("dense element order bound")

    def inverse(self, a: Element) -> Element:
        return self.power(a, self.order(a) - 1)

    def comm(self, a: Element, b: Element) -> Element:
        return self.mul(self.mul(self.mul(self.inverse(a), self.inverse(b)), a), b)

    def closure(self, generators) -> set[Element]:
        gs = []
        for g in generators:
            gs.extend((g, self.inverse(g)))
        seen = {IDENTITY}
        todo = deque([IDENTITY])
        while todo:
            a = todo.popleft()
            for g in gs:
                b = self.mul(a, g)
                if b not in seen:
                    seen.add(b)
                    todo.append(b)
        return seen

    @staticmethod
    def key(a: Element):
        return tuple(sorted(a))

    def enumerate_with_actions(self, clock: Clock):
        x, y = self.x, self.y
        xi, yi = self.inverse(x), self.inverse(y)
        order = self.order(x)
        gens = (x, y, xi, yi)
        increments = ((1, 0), (0, 1), (-1, 0), (0, -1))
        theta_gens = (y, x, yi, xi)
        tau_x = y
        tau_y = self.inverse(self.mul(x, y))
        tau_gens = (tau_x, tau_y, self.inverse(tau_x), self.inverse(tau_y))

        exponents = {IDENTITY: (0, 0)}
        theta = {IDENTITY: IDENTITY}
        tau = {IDENTITY: IDENTITY}
        todo = deque([IDENTITY])
        count = 0
        while todo:
            a = todo.popleft()
            ea = exponents[a]
            for g, tg, ug, inc in zip(gens, theta_gens, tau_gens, increments):
                b = self.mul(a, g)
                eb = ((ea[0] + inc[0]) % order, (ea[1] + inc[1]) % order)
                bt = self.mul(theta[a], tg)
                bu = self.mul(tau[a], ug)
                if b in exponents:
                    if exponents[b] != eb or theta[b] != bt or tau[b] != bu:
                        raise AssertionError("dense BFS collision")
                else:
                    exponents[b] = eb
                    theta[b] = bt
                    tau[b] = bu
                    todo.append(b)
            count += 1
            if count % 512 == 0:
                clock.check("dense_enumeration")
        if any(theta[theta[a]] != a for a in exponents):
            raise AssertionError("dense theta order")
        if any(tau[tau[tau[a]]] != a for a in exponents):
            raise AssertionError("dense tau order")
        return exponents, theta, tau, order


def generators_for(group: DenseMagnus, subgroup: set[Element]) -> list[Element]:
    chosen = []
    generated = {IDENTITY}
    for a in sorted(subgroup, key=group.key):
        if a not in generated:
            chosen.append(a)
            generated = group.closure(chosen)
    if generated != subgroup:
        raise AssertionError("dense generator extraction")
    return chosen


def coset_reps(group: DenseMagnus, whole: set[Element], normal: set[Element]):
    unseen = set(whole)
    reps = []
    while unseen:
        r = min(unseen, key=group.key)
        coset = {group.mul(r, n) for n in normal}
        if len(coset) != len(normal):
            raise AssertionError("dense coset size")
        reps.append(r)
        unseen -= coset
    return reps


def perm_compose(p, q):
    return tuple(q[p[i]] for i in range(len(p)))


def perm_inverse(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def perm_direct(*blocks):
    out = []
    offset = 0
    for block in blocks:
        out.extend(offset + x for x in block)
        offset += len(block)
    return tuple(out)


def perm_closure(generators):
    generators = tuple(generators)
    if not generators:
        raise ValueError("perm_closure needs a generator")
    ident = tuple(range(len(generators[0])))
    gs = []
    for g in generators:
        gs.extend((g, perm_inverse(g)))
    seen = {ident}
    todo = deque([ident])
    while todo:
        a = todo.popleft()
        for g in gs:
            b = perm_compose(a, g)
            if b not in seen:
                seen.add(b)
                todo.append(b)
    return seen


def perm_comm(a, b):
    return perm_compose(perm_compose(perm_compose(perm_inverse(a), perm_inverse(b)), a), b)


def independent_g9_audit():
    r = tuple((i + 1) % 9 for i in range(9))
    s = tuple((-i) % 9 for i in range(9))
    ident9 = tuple(range(9))
    rs = perm_compose(r, s)
    x = perm_direct(r, s, s)
    y = perm_direct(rs, r, rs)
    group = perm_closure((x, y))
    comm = perm_comm(x, y)
    conjugates = {comm}
    todo = deque([comm])
    conjugators = (x, y, perm_inverse(x), perm_inverse(y))
    while todo:
        a = todo.popleft()
        for g in conjugators:
            c = perm_compose(perm_compose(perm_inverse(g), a), g)
            if c not in conjugates:
                conjugates.add(c)
                todo.append(c)
    derived = perm_closure(conjugates)
    if len(group) != 2916 or len(derived) != 729:
        raise AssertionError("permutation G9 audit")
    return {"order": len(group), "derived_order": len(derived), "abelianization": [2, 2]}


def checkpoint(path: Path, stage: str, clock: Clock, extra=None):
    obj = {
        "schema": "d972-survival-noncomm-checker-checkpoint/v1",
        "stage": stage,
        "complete": stage == "complete",
        "elapsed_ms": clock.ms(),
    }
    if extra:
        obj.update(extra)
    atomic_json(path, obj)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--producer", type=Path, default=DEFAULT_PRODUCER)
    ap.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    ap.add_argument("--hard-timeout-seconds", type=float, default=120.0)
    args = ap.parse_args()
    clock = Clock(args.hard_timeout_seconds)

    producer = json.loads(args.producer.read_text(encoding="utf-8"))
    inp = json.loads(args.input.read_text(encoding="utf-8"))
    tuples = inp["tuples"]
    if len(tuples) != 972 or len({json.dumps(t, separators=(",", ":")) for t in tuples}) != 972:
        raise AssertionError("checker input cardinality")

    g9 = independent_g9_audit()
    checkpoint(args.checkpoint, "g9_complete", clock)

    group = DenseMagnus(5)
    exponents, theta, tau, generator_order = group.enumerate_with_actions(clock)
    if len(exponents) != 8192 or generator_order != 8:
        raise AssertionError("checker P anchor")
    wker = {a for a, e in exponents.items() if e[0] % 2 == 0 and e[1] % 2 == 0}
    if len(wker) != 2048:
        raise AssertionError("checker W_ker order")
    wgens = generators_for(group, wker)
    wderived = group.closure([group.comm(a, b) for a in wgens for b in wgens])
    wcenter = {a for a in wker if all(group.mul(a, g) == group.mul(g, a) for g in wgens)}
    if len(wderived) != 8 or len(wcenter) != 256 or wderived == {IDENTITY}:
        raise AssertionError("checker W_ker structure")

    wab_reps = coset_reps(group, wker, wderived)
    if len(wab_reps) != 256:
        raise AssertionError("checker Wab order")
    wab_order_hist = Counter()
    for a in wab_reps:
        for order in (1, 2, 4, 8):
            if group.power(a, order) in wderived:
                wab_order_hist[order] += 1
                break
    rank2torsion = int(math.log2(wab_order_hist[1] + wab_order_hist[2]))
    total_log = int(math.log2(len(wab_reps)))
    rank4 = total_log - rank2torsion
    rank2 = rank2torsion - rank4
    wab_invariants = [2] * rank2 + [4] * rank4
    if wab_invariants != [2, 2, 4, 4, 4]:
        raise AssertionError("checker Wab invariants")

    frattini_w = group.closure(list(wderived) + [group.mul(a, a) for a in wker])
    mod2_reps = coset_reps(group, wker, frattini_w)
    counts = {"theta": 0, "tau": 0, "both": 0}
    for a in mod2_reps:
        one = group.mul(a, theta[a]) in frattini_w
        ta = tau[a]
        two = group.mul(group.mul(a, ta), tau[ta]) in frattini_w
        counts["theta"] += int(one)
        counts["tau"] += int(two)
        counts["both"] += int(one and two)
    if len(mod2_reps) != 32 or counts != {"theta": 8, "tau": 16, "both": 4}:
        raise AssertionError("checker pre-screen")
    d_value = int(math.log2(counts["both"]))
    checkpoint(args.checkpoint, "prescreen_complete", clock, {"d": d_value})

    derived_p = {a for a, e in exponents.items() if e == (0, 0)}
    if len(derived_p) != 128:
        raise AssertionError("checker derived fiber")
    if any(group.mul(a, b) != group.mul(b, a) for a in derived_p for b in derived_p):
        raise AssertionError("checker derived fiber nonabelian")

    m_counts = Counter(int(t[0]) for t in tuples)
    per_m_raw = {}
    survival_distribution = Counter()
    direct_fixture_count = 0
    for base_m in sorted(m_counts):
        compatible = [m for m in range(72) if m % 18 == base_m % 18 and math.gcd(2 * m + 1, 72) == 1]
        if len(compatible) != 4:
            raise AssertionError("checker m fiber")
        total = 0
        cells = []
        for fine_m in compatible:
            c1 = c2 = both = surj_count = 0
            first = None
            ypow = group.power(group.y, fine_m)
            for i, f in enumerate(sorted(derived_p, key=group.key)):
                h1 = group.mul(theta[f], f) == IDENTITY
                ymf = group.mul(f, ypow)
                t1 = tau[ymf]
                h2 = group.mul(group.mul(ymf, t1), tau[t1]) == IDENTITY
                u = 2 * fine_m + 1
                surj = (u % 2) == 1
                c1 += int(h1)
                c2 += int(h2)
                surj_count += int(surj)
                if h1 and h2 and surj:
                    both += 1
                    if first is None:
                        first = f
                if i % 64 == 0:
                    clock.check(f"checker_survival_{base_m}_{fine_m}")
            if (c1, c2, both, surj_count) != (32, 16, 4, 128):
                raise AssertionError("checker cell counters")
            if first is None:
                raise AssertionError("checker direct fixture missing")
            u = 2 * fine_m + 1
            ga = group.power(group.x, u)
            gb = group.mul(group.mul(first, group.power(group.y, u)), group.inverse(first))
            if len(group.closure((ga, gb))) != 8192:
                raise AssertionError("checker direct generation")
            direct_fixture_count += 1
            cells.append([fine_m, c1, c2, both, surj_count])
            total += both
        if total != 16:
            raise AssertionError("checker per-target total")
        per_m_raw[str(base_m)] = {"target_count": m_counts[base_m], "cells": cells, "total": total}
        survival_distribution[total] += m_counts[base_m]
    if survival_distribution != Counter({16: 972}):
        raise AssertionError("checker distribution")
    checkpoint(args.checkpoint, "sweep_complete", clock)

    expected = {
        "g9_order": producer["g9_bridge_audit"]["order"],
        "g9_derived_order": producer["g9_bridge_audit"]["derived_order"],
        "P_order": producer["inventory"][-1]["P_order"],
        "W_ker_order": producer["candidate"]["W_ker"]["order"],
        "W_ker_derived_order": producer["candidate"]["W_ker"]["derived_order"],
        "W_ker_center_order": producer["candidate"]["W_ker"]["center_order"],
        "Wab_invariants": producer["candidate"]["W_ker"]["abelianization_invariants"],
        "d": producer["prescreen"]["mod2"]["d"],
        "derived_fiber_order": producer["survival_sweep"]["f_fiber_denominator"],
        "distribution": producer["survival_sweep"]["target_survival_distribution"],
        "direct_fixture_count": producer["survival_sweep"]["prop34_reduction"]["direct_generation_fixture_count"],
    }
    observed = {
        "g9_order": g9["order"],
        "g9_derived_order": g9["derived_order"],
        "P_order": len(exponents),
        "W_ker_order": len(wker),
        "W_ker_derived_order": len(wderived),
        "W_ker_center_order": len(wcenter),
        "Wab_invariants": wab_invariants,
        "d": d_value,
        "derived_fiber_order": len(derived_p),
        "distribution": {str(k): v for k, v in sorted(survival_distribution.items())},
        "direct_fixture_count": direct_fixture_count,
    }
    agreement = expected == observed
    if not agreement:
        raise AssertionError(f"producer/checker mismatch: expected={expected!r} observed={observed!r}")

    result = {
        "schema": "d972-survival-noncomm-crosscheck/v1",
        "generated_at_local_date": "2026-08-15",
        "generated_by": {
            "script": "crosscheck/check_d972_survival_noncomm_v1.py",
            "python": platform.python_version(),
            "representation": "frozenset of literal binary monomials; degree-27 permutation G9",
        },
        "producer": {
            "path": str(args.producer.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha(args.producer),
        },
        "input": {
            "path": str(args.input.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha(args.input),
        },
        "agreement": agreement,
        "expected": expected,
        "observed": observed,
        "raw": {
            "mod2_kernel_counts": counts,
            "Wab_order_histogram": {str(k): v for k, v in sorted(wab_order_hist.items())},
            "per_m": per_m_raw,
        },
        "grading": {
            "producer_checker_match": True,
            "lean_certificate": False,
        },
        "runtime": {
            "hard_timeout_seconds": args.hard_timeout_seconds,
            "wall_ms": clock.ms(),
            "checkpoint": str(args.checkpoint.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    atomic_json(args.output, result)
    checkpoint(args.checkpoint, "complete", clock, {"output_sha256": sha(args.output)})
    print(json.dumps({
        "agreement": agreement,
        "output": str(args.output),
        "distribution": dict(survival_distribution),
        "wall_ms": clock.ms(),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except Exception as exc:
        print(f"INTEGRITY_STOP: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
    raise SystemExit(code)
