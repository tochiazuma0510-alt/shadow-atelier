"""Direct, lossless LS replay of the frozen 972-row canonical certificate.

This checker intentionally imports no producer, checker, or repository helper.
It reads the complete ``ihnec_r4b_run_20260801.json`` row list, pins the file
and canonical row-list digests, parses every GAP cycle string into a 36-point
permutation, reconstructs K(9) and PSL(2,8) independently, and tests both
Lochak--Schneps equations in every row.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, deque
from pathlib import Path
from typing import Iterable

Perm = tuple[int, ...]
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERT = ROOT / "search/certs/ihnec_r4b_run_20260801.json"
EXPECTED_CERT_SHA256 = "fdf5fd367cdd00e4aafde4d1ac4ef3708e6f3efd338f7b7945646879e0002fd2"
EXPECTED_ROW_SHA256 = "e9e1cb711dc700b3588902b7b05f83ae0ca1967983d70d46fc22825b96b0136c"
CHARMING = (0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17)


def mul(a: Perm, b: Perm) -> Perm:
    return tuple(b[i] for i in a)


def inv(a: Perm) -> Perm:
    r = [0] * len(a)
    for i, j in enumerate(a):
        r[j] = i
    return tuple(r)


def power(a: Perm, n: int) -> Perm:
    r = tuple(range(len(a)))
    if n < 0:
        return power(inv(a), -n)
    while n:
        if n & 1:
            r = mul(r, a)
        a = mul(a, a)
        n >>= 1
    return r


def paper_prod(word: Iterable[Perm]) -> Perm:
    letters = list(word)
    if not letters:
        raise ValueError("empty paper word")
    r = tuple(range(len(letters[0])))
    for letter in reversed(letters):
        r = mul(r, letter)
    return r


def parse_cycle(text: str, n: int = 36) -> Perm:
    out = list(range(1, n + 1))
    used: set[int] = set()
    for body in re.findall(r"\(([^()]*)\)", text):
        a = [int(x) for x in body.split(",") if x]
        if len(a) < 2:
            if a:
                raise ValueError(f"singleton cycle in {text!r}")
            continue
        if any(x < 1 or x > n for x in a) or len(set(a)) != len(a):
            raise ValueError(f"bad cycle in {text!r}")
        if used.intersection(a):
            raise ValueError(f"overlapping cycles in {text!r}")
        used.update(a)
        for u, v in zip(a, a[1:] + a[:1]):
            out[u - 1] = v
    if sorted(out) != list(range(1, n + 1)):
        raise ValueError(f"not a permutation: {text!r}")
    return tuple(v - 1 for v in out)


def restrict(p: Perm, offset: int, n: int) -> Perm:
    return tuple(p[offset + i] - offset for i in range(n))


def direct(a: Perm, b: Perm) -> Perm:
    out = list(range(len(a) + len(b)))
    out[:len(a)] = a
    out[len(a):] = [len(a) + j for j in b]
    return tuple(out)


def g9_marking() -> tuple[Perm, Perm]:
    r = tuple(list(range(1, 9)) + [0])
    s = tuple(8 - i for i in range(9))
    sr = mul(s, r)
    def b(p: Perm, k: int) -> Perm:
        out = list(range(27))
        for i, j in enumerate(p):
            out[k * 9 + i] = k * 9 + j
        return tuple(out)
    x = mul(mul(b(r, 0), b(s, 1)), b(s, 2))
    y = mul(mul(b(sr, 0), b(r, 1)), b(sr, 2))
    return x, y


def gf8_mul(a: int, b: int) -> int:
    z = 0
    for i in range(3):
        if (b >> i) & 1:
            z ^= a << i
    for i in (4, 3):
        if (z >> i) & 1:
            z ^= 11 << (i - 3)
    return z


def gf8_inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError
    for b in range(1, 8):
        if gf8_mul(a, b) == 1:
            return b
    raise AssertionError("GF(8) inverse failure")


def mat_perm(a: int, b: int, c: int, d: int) -> Perm:
    out = [0 if c == 0 else 1 + gf8_mul(a, gf8_inv(c))]
    for z in range(8):
        num = gf8_mul(a, z) ^ b
        den = gf8_mul(c, z) ^ d
        out.append(0 if den == 0 else 1 + gf8_mul(num, gf8_inv(den)))
    return tuple(out)


def psl_marking() -> tuple[Perm, Perm]:
    s = mat_perm(1, 0, 1, 1)
    t = mat_perm(4, 3, 1, 5)
    w = mul(s, inv(t))
    x = mul(w, w)
    y = mul(mul(inv(s), x), s)
    return x, y


def factor_images(x: Perm, y: Perm, expected_order: int) -> dict[str, object]:
    one = tuple(range(len(x)))
    tau_y = inv(mul(y, x))
    # Paper y^-1*x^-1 -> GAP x^-1*y^-1.  This is a deliberate
    # noncommutative binding: inv(x*y) is the rejected wrong value.
    assert tau_y == mul(inv(x), inv(y))
    assert tau_y != inv(mul(x, y))
    edges = ((x, y, y), (y, x, tau_y),
             (inv(x), inv(y), inv(y)),
             (inv(y), inv(x), inv(tau_y)))
    seen: dict[Perm, tuple[Perm, Perm]] = {one: (one, one)}
    todo = deque([one])
    while todo:
        g = todo.popleft(); th, ta = seen[g]
        for sg, sth, sta in edges:
            ng = mul(g, sg); pair = (mul(th, sth), mul(ta, sta))
            if ng not in seen:
                seen[ng] = pair; todo.append(ng)
            else:
                assert seen[ng] == pair, "map consistency drift"
    assert len(seen) == expected_order, (len(seen), expected_order)
    theta: set[Perm] = set(); tau: set[Perm] = set(); tau_xy: set[Perm] = set()
    for g, (th, ta) in seen.items():
        # Full paper-word reversal: theta^-1*g -> g*theta^-1;
        # tau^-1*h -> h*tau^-1; tau^-1*x*y*h -> h*y*x*tau^-1.
        theta.add(mul(g, inv(th)))
        tau.add(mul(g, inv(ta)))
        tau_xy.add(mul(mul(mul(g, y), x), inv(ta)))
    return {"seen": seen, "theta": theta, "tau": tau, "tau_xy": tau_xy}


def load_rows(path: Path) -> tuple[dict, list[tuple[int, str]], str, str]:
    raw = path.read_bytes()
    file_sha = hashlib.sha256(raw).hexdigest()
    if file_sha != EXPECTED_CERT_SHA256:
        raise ValueError(f"canonical cert SHA drift: {file_sha}")
    doc = json.loads(raw.decode("utf-8-sig"))
    if doc.get("schema") != "ihnec-r4b/v1":
        raise ValueError("certificate schema drift")
    scan = doc.get("scan", {})
    sample = doc.get("shadows_sample", {})
    if (scan.get("shadow_total"), sample.get("truncated"), sample.get("count_in_sample")) != (972, False, 972):
        raise ValueError("certificate is not the complete 972-row sample")
    items = sample.get("items")
    if not isinstance(items, list) or len(items) != 972:
        raise ValueError("row list length drift")
    row_json = json.dumps(items, ensure_ascii=True, separators=(",", ":")).encode()
    row_sha = hashlib.sha256(row_json).hexdigest()
    if row_sha != EXPECTED_ROW_SHA256:
        raise ValueError(f"canonical row SHA drift: {row_sha}")
    rows: list[tuple[int, str]] = []
    for item in items:
        if not isinstance(item.get("m"), int) or item["m"] not in CHARMING:
            raise ValueError("row m drift")
        if not isinstance(item.get("f"), str):
            raise ValueError("row f encoding drift")
        rows.append((item["m"], item["f"]))
    counts = Counter(m for m, _ in rows)
    if counts != Counter({m: 81 for m in CHARMING}) or len(set(rows)) != 972:
        raise ValueError(f"lossless m/f census drift: {counts}")
    return doc, rows, file_sha, row_sha


def audit(path: Path) -> dict:
    doc, rows, file_sha, row_sha = load_rows(path)
    g9x, g9y = g9_marking(); px, py = psl_marking()
    k9 = factor_images(g9x, g9y, 2916); psl = factor_images(px, py, 504)
    qx, qy = direct(g9x, px), direct(g9y, py)
    counts = {"q0_membership": 0, "theta": 0, "tau": 0, "both": 0}
    by_m: dict[str, dict[str, int]] = {}; failures = []
    for index, (m, text) in enumerate(rows, 1):
        f = parse_cycle(text); f9, fp = restrict(f, 0, 27), restrict(f, 27, 9)
        member = f9 in k9["seen"] and fp in psl["seen"]
        if member: counts["q0_membership"] += 1
        theta_ok = f9 in k9["theta"] and fp in psl["theta"]
        lhs = mul(power(qx, m), f)  # paper f*x^m, reversed for GAP
        lhs9, lhsp = restrict(lhs, 0, 27), restrict(lhs, 27, 9)
        branch = "tau" if (2 * m + 1) % 3 == 1 else "tau_xy"
        tau_ok = lhs9 in k9[branch] and lhsp in psl[branch]
        both = theta_ok and tau_ok
        counts["theta"] += int(theta_ok); counts["tau"] += int(tau_ok); counts["both"] += int(both)
        b = by_m.setdefault(str(m), {"rows": 0, "q0_membership": 0, "theta": 0, "tau": 0, "both": 0})
        b["rows"] += 1; b["q0_membership"] += int(member); b["theta"] += int(theta_ok)
        b["tau"] += int(tau_ok); b["both"] += int(both)
        if not both:
            failures.append({"row": index, "m": m, "f_cycle": text,
                             "q0_membership": member, "theta_equation": theta_ok,
                             "tau_equation": tau_ok, "branch": branch})
    return {
        "schema": "ls-d972-checker/v3", "input": str(path),
        "input_bytes": path.stat().st_size, "input_sha256": file_sha,
        "canonical_rows_sha256": row_sha, "producer_schema": doc["schema"],
        "q0_order": 2916 * 504, "m_ord": 18, "row_count": len(rows),
        "factor_orders": [len(k9["seen"]), len(psl["seen"])],
        "factor_image_sizes": {"G9": {k: len(k9[k]) for k in ("theta", "tau", "tau_xy")},
                                "PSL28": {k: len(psl[k]) for k in ("theta", "tau", "tau_xy")}},
        "counts": counts, "by_m": by_m, "failures": failures,
        "all_972_pass_both_equations": not failures,
        "paper_gap_receipt": {"tau_y": "inv(mul(y,x))=mul(inv(x),inv(y))",
                               "paper_f_xm": "mul(x^m,f)",
                               "paper_tau_inv_xy_h": "mul(h,y,x,tau(h)^-1)"},
        "terminal_status": "PASS_LS_ALL_972" if not failures else "LS_OBSTRUCTION_FOUND",
    }


def selftest() -> None:
    x, y = psl_marking()
    assert mul(x, y) != mul(y, x)
    assert paper_prod([inv(y), inv(x)]) == inv(mul(y, x))
    assert paper_prod([x, power(x, 2)]) == mul(power(x, 2), x)
    assert parse_cycle("()") == tuple(range(36))
    print("LS_D972_CHECKER_V3_SELFTEST_PASS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cert", type=Path, default=DEFAULT_CERT)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest(); return
    print(json.dumps(audit(args.cert), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
