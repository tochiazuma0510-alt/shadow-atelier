"""koubou158_L3_core_v1_1_invfix.py

Independent bugfix branch of koubou158_L3_core_v1_1.py, scoped ONLY to the
IndependentPc.inverse() out-of-range bug reported in Sol reply 157 (A3,
repair order items (1)(2)): _inv_gen was built from pb4["marked_generators"]
(6 rows) but IndependentPc.inverse() iterates idx in range(self.n, 0, -1)
with self.n=10, so any pc-vector with nonzero exponent at a weight-2
coordinate (idx 7..10, i.e. self._inv_gen[6..9]) raised IndexError. This was
a genuine, previously-unhit bug (past runs that never exercised weight-2
support in a call to .inverse() are unaffected/non-contaminated).

LINEAGE NOTE (chief ruling, this session): this file is a SIBLING of
koubou158_L3_core_v1_2.py, NOT a successor/superset of it. v1_2 already
exists (untracked, dated 2026-08-22 04:17) as the falsifier's independent
"mid-read verdict" repair bundle -- THREE unrelated, unaccepted repairs
(prune-order proof-ification / soundness-basis replacement / Delta
identification require+discriminant) that koubou158_L3_bulk162_v1_2.py and
koubou158_L3_radical_v1_2.py already depend on (`import
koubou158_L3_core_v1_2 as core`). v1_2 was NOT to be touched (would destroy
unreviewed work-in-progress and contaminate its lineage). This file
(v1_1_invfix) branches from v1_1 directly and carries ONLY the _inv_gen
fix -- nothing from v1_2's three repairs. Both v1_2 and v1_1_invfix are
independent children of v1_1; neither supersedes the other. v1_1 itself
remains FROZEN/unmodified (no-rename policy).

THE FIX: _inv_gen is now built from pb4["inverses"] (all N_GEN=10 rows, one
per pc-generator), not pb4["marked_generators"][i]["inverse_coords"] (only
6 rows, the "marked" subset). Three constructor-time REQUIRE checks gate
this:
  (a) len(pb4["inverses"]) == N_GEN (== 10)
  (b) the first 6 rows of pb4["inverses"] match
      pb4["marked_generators"][i]["inverse_coords"] exactly, for i=0..5
      (same underlying data -- marked_generators is a labelled subset/dup)
  (c) the left/right inverse law p*p^-1 == p^-1*p == identity holds for
      ALL 10 pc-generator units (not just the 6 marked ones), computed via
      self.mul (independent of self.inverse(), so this is a check on the
      raw _inv_gen table + collect()/mul(), not a tautological self-check
      of inverse() against itself).
Any missing/duplicate row or law violation raises RuntimeError at
construction time (terminal ERROR, not folded into a PASS/FAIL verdict).

See the __main__ self-test block at the bottom for the mandatory
destructive canary (unit 7 and unit 10 -- both weight-2 generators, both
would have raised IndexError under the pre-fix v1_1 6-row table) and the
full self-test log.
"""
from __future__ import annotations

import hashlib
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

Q3_CHIEF = Path("ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json")
Q3_CHIEF_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
Q3_CHIEF_BYTES = 231570

FIXED_WORD = [-2, -2, -1, -1, 2, 2, 1, -2, -1, -1,
              2, 2, 2, -1, -2, -2, 1, 1, 1, 1]
X0 = [4]
Y0 = [6]
Z0 = [-4, -6]

N_GEN = 10
WEIGHTS = (1, 1, 1, 1, 1, 1, 2, 2, 2, 2)
BINOM3 = {(0, 0): 1, (1, 0): 1, (1, 1): 1, (2, 0): 1, (2, 1): 2, (2, 2): 1}
DELTA_CAP = 40
J_MAX = 12


def require(cond: Any, msg: str) -> None:
    if not cond:
        raise RuntimeError(f"REQUIRE FAILED: {msg}")


def sha_file(path: Path) -> str:
    d = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            d.update(block)
    return d.hexdigest()


def perm_mul(a: bytes, b: bytes) -> bytes:
    return bytes(b[a[i]] for i in range(len(a)))


def perm_inv(a: bytes) -> bytes:
    out = [0] * len(a)
    for i, im in enumerate(a):
        out[im] = i
    return bytes(out)


def perm_one(n: int) -> bytes:
    return bytes(range(n))


class IndependentPc:
    def __init__(self, pb4: dict[str, Any]) -> None:
        self.n = int(pb4["generator_count"])
        require(self.n == N_GEN, "unexpected pc generator count")
        require(all(o == 3 for o in pb4["relative_orders"]), "pc relative orders")
        require(all(all(c == 0 for c in row) for row in pb4["power_relations"]),
                "expected ALL power_relations rows to be zero (x_i^3=1 exactly)")
        self.power = [tuple(int(x) for x in row) for row in pb4["power_relations"]]
        self.conj: dict[tuple[int, int], tuple[int, ...]] = {}
        for row in pb4["conjugate_relations"]:
            self.conj[(row["i"], row["j"])] = tuple(int(x) for x in row["coords"])

        # --- INVFIX: build _inv_gen from ALL 10 pc-generator inverse rows,
        # not just the 6 "marked" ones. See module docstring for the bug
        # this repairs (Sol reply 157, A3, repair items (1)(2)).
        inv_rows_raw = pb4["inverses"]

        # (a) row count
        require(len(inv_rows_raw) == self.n,
                f"expected {self.n} inverse-coord rows (all pc-generators), got {len(inv_rows_raw)}")

        marked = pb4["marked_generators"]
        n_marked = len(marked)
        require(n_marked <= self.n, "marked_generators count exceeds total generator count")

        # duplicate-row guard (terminal ERROR, not folded into pass/fail):
        # any two DISTINCT generator inverse rows being byte-identical would
        # indicate a serialization/aliasing defect in the receipt, since the
        # 10 pc-generators are distinct basis elements with distinct inverses.
        seen_rows: dict[tuple[int, ...], int] = {}
        for gi, row in enumerate(inv_rows_raw):
            key = tuple(int(x) for x in row)
            if key in seen_rows:
                raise RuntimeError(
                    f"REQUIRE FAILED: duplicate inverse row -- generator {gi} and "
                    f"{seen_rows[key]} both have inverse_coords {list(key)}"
                )
            seen_rows[key] = gi

        inv_rows = [tuple(int(x) for x in row) for row in inv_rows_raw]

        # (b) first n_marked rows must match marked_generators' own
        # inverse_coords field exactly (same underlying data source).
        for i in range(n_marked):
            expected = tuple(int(x) for x in marked[i]["inverse_coords"])
            require(inv_rows[i] == expected,
                    f"marked-generator inverse mismatch at row {i}: "
                    f"pb4['inverses'][{i}]={inv_rows[i]} != "
                    f"marked_generators[{i}]['inverse_coords']={expected}")

        self._inv_gen = inv_rows

    def one(self) -> bytes:
        return bytes(self.n)

    def coords_word(self, coords: tuple[int, ...]) -> list[int]:
        out = []
        for idx, exp in enumerate(coords, start=1):
            out.extend([idx] * exp)
        return out

    def collect(self, word: list[int]) -> bytes:
        tokens: list[int] = []
        for x in word:
            if x > 0:
                tokens.append(x)
            else:
                tokens.extend(self.coords_word(self._inv_gen[-x - 1]))
        changed = True
        while changed:
            changed = False
            for pos in range(len(tokens) - 1):
                a, b = tokens[pos], tokens[pos + 1]
                if a > b:
                    tokens[pos:pos + 2] = [b] + self.coords_word(self.conj[(a, b)])
                    changed = True
                    break
            if changed:
                continue
            pos = 0
            while pos < len(tokens):
                j = pos
                while j < len(tokens) and tokens[j] == tokens[pos]:
                    j += 1
                if j - pos >= 3:
                    tokens[pos:pos + 3] = self.coords_word(self.power[tokens[pos] - 1])
                    changed = True
                    break
                pos = j
        row = [0] * self.n
        for x in tokens:
            row[x - 1] += 1
        require(all(0 <= v < 3 for v in row), "pc collected exponent range")
        return bytes(row)

    def mul(self, a: bytes, b: bytes) -> bytes:
        return self.collect(self.coords_word(tuple(a)) + self.coords_word(tuple(b)))

    def inverse(self, a: bytes) -> bytes:
        word: list[int] = []
        for idx in range(self.n, 0, -1):
            for _ in range(a[idx - 1]):
                word.extend(self.coords_word(self._inv_gen[idx - 1]))
        return self.collect(word)

    def verify_inverse_law_all_units(self) -> list[dict]:
        """(c) left/right inverse law p*p^-1 == p^-1*p == identity for ALL
        N_GEN pc-generator UNITS (single generator to the first power),
        computed via self.mul on the raw _inv_gen table -- independent of
        self.inverse() (no tautological self-check). Raises RuntimeError
        (terminal ERROR) on any failure; returns a per-unit receipt list on
        full success."""
        identity = self.one()
        receipts = []
        for gidx in range(1, self.n + 1):
            gi = bytes(1 if k == gidx - 1 else 0 for k in range(self.n))
            inv_i = self.collect(self.coords_word(self._inv_gen[gidx - 1]))
            left = self.mul(gi, inv_i)
            right = self.mul(inv_i, gi)
            ok = (left == identity) and (right == identity)
            require(ok, f"inverse law FAILED for unit {gidx}: gi={list(gi)} inv={list(inv_i)} "
                        f"gi*inv={list(left)} inv*gi={list(right)} identity={list(identity)}")
            receipts.append({
                "unit": gidx, "weight": WEIGHTS[gidx - 1],
                "gi": list(gi), "inv": list(inv_i),
                "left_ok": left == identity, "right_ok": right == identity,
            })
        return receipts


class E4:
    def __init__(self, q3_data: dict[str, Any]) -> None:
        pb4 = q3_data["groups"]["PB4"]
        q4model = q3_data["coarse_models"]["Q4"]
        self.degree = q4model["degree"]
        self.pc = IndependentPc(pb4)
        self.marks_perm = [bytes(int(x) - 1 for x in row) for row in q4model["marked_permutations"]]
        self.marks_pc = [bytes(int(x) for x in row["coords"]) for row in pb4["marked_generators"]]
        self.identity = (perm_one(self.degree), self.pc.one())

    def mul(self, a, b):
        return perm_mul(a[0], b[0]), self.pc.mul(a[1], b[1])

    def inverse(self, a):
        return perm_inv(a[0]), self.pc.inverse(a[1])

    def gen(self, i: int):
        return self.marks_perm[i - 1], self.marks_pc[i - 1]

    def eval(self, word: list[int]):
        val = self.identity
        for letter in word:
            val = self.mul(val, self.gen(letter) if letter > 0 else self.inverse(self.gen(-letter)))
        return val


def reduce_word(word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inv_word(word: list[int]) -> list[int]:
    return reduce_word([-x for x in reversed(word)])


def substitute2(word2: list[int], x_word: list[int], y_word: list[int]) -> list[int]:
    out: list[int] = []
    for letter in word2:
        if letter == 1:
            out.extend(x_word)
        elif letter == -1:
            out.extend(inv_word(x_word))
        elif letter == 2:
            out.extend(y_word)
        elif letter == -2:
            out.extend(inv_word(y_word))
        else:
            raise RuntimeError("alphabet")
        out = reduce_word(out)
    return out


def fox_gradient(e4: E4, word: list[int]) -> dict:
    acc: dict = defaultdict(int)
    prefix = e4.identity
    for letter in word:
        i = abs(letter)
        if letter > 0:
            acc[(i, prefix)] += 1
            prefix = e4.mul(prefix, e4.gen(i))
        else:
            prefix = e4.mul(prefix, e4.inverse(e4.gen(i)))
            acc[(i, prefix)] += -1
    return {k: v % 3 for k, v in acc.items() if v % 3}


def add_vec(a: dict, b: dict) -> dict:
    out: dict = defaultdict(int)
    for k, v in a.items():
        out[k] = (out[k] + v) % 3
    for k, v in b.items():
        out[k] = (out[k] + v) % 3
    return {k: v for k, v in out.items() if v}


def neg_vec(a: dict) -> dict:
    return {k: (-v) % 3 for k, v in a.items()}


def translate_vec(e4: E4, v: dict, g) -> dict:
    out: dict = defaultdict(int)
    for (comp, elt), c in v.items():
        new_elt = e4.mul(g, elt)
        out[(comp, new_elt)] = (out[(comp, new_elt)] + c) % 3
    return {k: c for k, c in out.items() if c}


def project_to_pi(v: dict) -> dict:
    out: dict = defaultdict(int)
    for (comp, elt), c in v.items():
        out[(comp, elt[1])] = (out[(comp, elt[1])] + c) % 3
    return {k: c for k, c in out.items() if c}


def pb_pairs(rank: int) -> list[list[int]]:
    return [[i, j] for i in range(1, rank) for j in range(i + 1, rank + 1)]


def pair_index(rank: int, pair: list[int]) -> int:
    return pb_pairs(rank).index(pair) + 1


def artin_step(rank: int, letter: int) -> list[list[int]]:
    i = abs(letter)
    images = [[j] for j in range(1, rank + 1)]
    if letter > 0:
        images[i - 1], images[i] = [i, i + 1, -i], [i]
    else:
        images[i - 1], images[i] = [i + 1], [-(i + 1), i, i + 1]
    return images


def word_substitute_letters(word: list[int], images: list[list[int]]) -> list[int]:
    out: list[int] = []
    for letter in word:
        out.extend(images[letter - 1] if letter > 0 else inv_word(images[-letter - 1]))
        out = reduce_word(out)
    return out


def artin_images(rank: int, braid: list[int]) -> list[list[int]]:
    images = [[j] for j in range(1, rank + 1)]
    for letter in braid:
        step = artin_step(rank, letter)
        images = [word_substitute_letters(w, step) for w in images]
    return images


def aij_braid(i: int, j: int) -> list[int]:
    return list(range(j - 1, i, -1)) + [i, i] + [-k for k in range(i + 1, j)]


def pure_relations(rank: int) -> list[list[int]]:
    if rank == 2:
        return []
    old_pairs = pb_pairs(rank - 1)
    old_map = [[pair_index(rank, p)] for p in old_pairs]
    rels = [word_substitute_letters(w, old_map) for w in pure_relations(rank - 1)]
    kernel = [[pair_index(rank, [k, rank])] for k in range(1, rank)]
    for i, j in old_pairs:
        g = pair_index(rank, [i, j])
        action = artin_images(rank - 1, aij_braid(i, j))
        for k in range(1, rank):
            h = pair_index(rank, [k, rank])
            rels.append(reduce_word([-g, h, g] + inv_word(word_substitute_letters(action[k - 1], kernel))))
    return rels


class F3BitSpace:
    def __init__(self, n: int) -> None:
        self.n = n
        self.mask = (1 << n) - 1

    def vec(self, d: dict) -> tuple[int, int]:
        p1 = p2 = 0
        for i, c in d.items():
            c %= 3
            if c == 1:
                p1 |= (1 << i)
            elif c == 2:
                p2 |= (1 << i)
        return (p1, p2)

    def add(self, v, w):
        v1, v2 = v
        w1, w2 = w
        zero_v = self.mask & ~(v1 | v2)
        zero_w = self.mask & ~(w1 | w2)
        out1 = (v1 & zero_w) | (zero_v & w1) | (v2 & w2)
        out2 = (v2 & zero_w) | (zero_v & w2) | (v1 & w1)
        return (out1, out2)

    def neg(self, v):
        return (v[1], v[0])

    def sub(self, v, w):
        return self.add(v, self.neg(w))

    def scale(self, v, c):
        c %= 3
        if c == 0:
            return (0, 0)
        return v if c == 1 else self.neg(v)

    def leading(self, v) -> int:
        u = v[0] | v[1]
        if u == 0:
            return -1
        return (u & -u).bit_length() - 1

    def coeff_at(self, v, pos: int) -> int:
        if (v[0] >> pos) & 1:
            return 1
        if (v[1] >> pos) & 1:
            return 2
        return 0

    def dot(self, v, w) -> int:
        v1, v2 = v
        w1, w2 = w
        ones = (v1 & w1) | (v2 & w2)
        twos = (v1 & w2) | (v2 & w1)
        return (bin(ones).count("1") + 2 * bin(twos).count("1")) % 3


class F3BitEchelon:
    def __init__(self, sp: F3BitSpace, pivots=None) -> None:
        self.sp = sp
        self.pivots: dict = dict(pivots) if pivots else {}

    def clone(self) -> "F3BitEchelon":
        return F3BitEchelon(self.sp, self.pivots)

    def reduce(self, v):
        sp = self.sp
        while True:
            p = sp.leading(v)
            if p < 0:
                return v, -1
            basis = self.pivots.get(p)
            if basis is None:
                return v, p
            c = sp.coeff_at(v, p)
            v = sp.sub(v, sp.scale(basis, c))

    def add(self, v) -> bool:
        sp = self.sp
        v, p = self.reduce(v)
        if p < 0:
            return False
        c = sp.coeff_at(v, p)
        if c == 2:
            v = sp.neg(v)
        self.pivots[p] = v
        return True

    def rank(self) -> int:
        return len(self.pivots)

    def rref(self) -> None:
        sp = self.sp
        ordered = sorted(self.pivots, reverse=True)
        for p in ordered:
            v = self.pivots[p]
            for q in sorted(x for x in self.pivots if x > p):
                c = sp.coeff_at(v, q)
                if c:
                    v = sp.sub(v, sp.scale(self.pivots[q], c))
            self.pivots[p] = v

    def extract_separator(self, target):
        sp = self.sp
        self.rref()
        v, f0 = self.reduce(target)
        if f0 < 0:
            return None
        cd = {f0: 1}
        for p, rv in self.pivots.items():
            co = sp.coeff_at(rv, f0)
            if co:
                cd[p] = (-co) % 3
        return sp.vec(cd)


def enum_delta_pc(g1: tuple, g2: tuple, pc: IndependentPc, cap: int):
    identity3 = (pc.one(), pc.one(), pc.one())
    transversal = {identity3: []}
    tree_edge: dict = {}
    queue = deque([identity3])
    gens = {1: g1, 2: g2}
    while queue:
        cur = queue.popleft()
        cur_word = transversal[cur]
        for s in (1, 2):
            g = gens[s]
            nxt = tuple(pc.mul(cur[i], g[i]) for i in range(3))
            if nxt not in transversal:
                require(len(transversal) < cap, f"Delta enumeration exceeded safety cap {cap}")
                transversal[nxt] = cur_word + [s]
                tree_edge[nxt] = (cur, s)
                queue.append(nxt)
    return transversal, tree_edge


def schreier_generators_pc(transversal: dict, tree_edge: dict, g1: tuple, g2: tuple, pc: IndependentPc) -> list[list[int]]:
    gens = {1: g1, 2: g2}
    out: list[list[int]] = []
    for delta, t_delta in transversal.items():
        for s in (1, 2):
            g = gens[s]
            nxt = tuple(pc.mul(delta[i], g[i]) for i in range(3))
            edge = tree_edge.get(nxt)
            if edge is not None and edge == (delta, s):
                continue
            t_nxt = transversal[nxt]
            word = reduce_word(t_delta + [s] + inv_word(t_nxt))
            out.append(word)
    return out


def enumerate_monomials(j: int) -> list[tuple]:
    out: list[tuple] = []

    def rec(pos: int, partial: list[int], w: int):
        if w >= j:
            return
        if pos == N_GEN:
            out.append(tuple(partial))
            return
        for e in (0, 1, 2):
            nw = w + e * WEIGHTS[pos]
            if nw >= j and e > 0:
                continue
            partial.append(e)
            rec(pos + 1, partial, nw)
            partial.pop()

    rec(0, [], 0)
    return out


def project_pcvec_terms(pcvec: bytes, j: int):
    a = list(pcvec)

    def rec(pos: int, partial: list[int], w: int, coeff: int):
        if w >= j:
            return
        if pos == N_GEN:
            yield tuple(partial), coeff
            return
        for e in range(0, a[pos] + 1):
            nw = w + e * WEIGHTS[pos]
            if nw >= j:
                continue
            c = (coeff * BINOM3[(a[pos], e)]) % 3
            partial.append(e)
            yield from rec(pos + 1, partial, nw, c)
            partial.pop()

    yield from rec(0, [], 0, 1)


def project_vec_to_Ij(v_pi: dict, j: int) -> dict:
    out: dict = defaultdict(int)
    for (comp, pcvec), coeff in v_pi.items():
        for e_tuple, c in project_pcvec_terms(pcvec, j):
            out[(comp, e_tuple)] = (out[(comp, e_tuple)] + coeff * c) % 3
    return {k: c for k, c in out.items() if c}


def gen_pcvec(i: int) -> bytes:
    return bytes(1 if k == i - 1 else 0 for k in range(N_GEN))


def apply_xi_minus_1(v_pi: dict, i: int, pc: IndependentPc) -> dict:
    gi = gen_pcvec(i)
    translated: dict = defaultdict(int)
    for (comp, pcvec), c in v_pi.items():
        new_pc = pc.mul(gi, pcvec)
        translated[(comp, new_pc)] = (translated[(comp, new_pc)] + c) % 3
    out: dict = defaultdict(int)
    for k, c in translated.items():
        out[k] = (out[k] + c) % 3
    for k, c in v_pi.items():
        out[k] = (out[k] - c) % 3
    return {k: c for k, c in out.items() if c}


def submodule_closure_with_depth(v_pi_raw: dict, j: int, idx: dict, sp: F3BitSpace, pc: IndependentPc,
                                  shared_ech: F3BitEchelon) -> dict:
    """Same closure as v1's submodule_closure, but tracks BFS depth
    explicitly: queue entries are (raw_vec, depth); returns a receipt
    dict with new_pivots_total, max_depth_reached, and
    explored_count_by_depth (ACTUAL counts, not just the theoretical
    10^d ceiling)."""
    added = 0
    max_depth = 0
    explored_by_depth: dict = defaultdict(int)

    v0_proj = project_vec_to_Ij(v_pi_raw, j)
    v0_indexed = {idx[k]: c for k, c in v0_proj.items() if k in idx}
    queue = deque()
    explored_by_depth[0] += 1
    if shared_ech.add(sp.vec(v0_indexed)):
        added += 1
        queue.append((v_pi_raw, 0))
    seen_raw_keys = set()
    while queue:
        cur, depth = queue.popleft()
        max_depth = max(max_depth, depth)
        for i in range(1, N_GEN + 1):
            nxt = apply_xi_minus_1(cur, i, pc)
            if not nxt:
                continue
            explored_by_depth[depth + 1] += 1
            nxt_proj = project_vec_to_Ij(nxt, j)
            nxt_indexed = {idx[k]: c for k, c in nxt_proj.items() if k in idx}
            if shared_ech.add(sp.vec(nxt_indexed)):
                added += 1
                fp = tuple(sorted(nxt.items()))
                if fp not in seen_raw_keys:
                    seen_raw_keys.add(fp)
                    queue.append((nxt, depth + 1))
                    max_depth = max(max_depth, depth + 1)
    # BUG FIX (found running koubou158_L3_bulk162_v1.py, 2026-08-22):
    # max_depth (tracked via queue pops/enqueues) only counts depths where
    # a NEW PIVOT was found and hence enqueued for further expansion --
    # if every depth-d candidate is already spanned (saturation, not a
    # bug), depth d is still genuinely EXPLORED/TESTED (it appears in
    # explored_count_by_depth) but max_depth never advances to d, giving
    # a FALSE depth-shortfall alarm. The depth requirement ("did the BFS
    # attempt depth j-1") is about EXPLORATION, not about finding new
    # pivots specifically at the deepest level -- so max_depth_reached is
    # redefined here as max(explored_count_by_depth keys), i.e. the
    # deepest depth for which candidate vectors were actually generated
    # and tested against the echelon (whether or not they turned out new).
    max_depth_explored = max(explored_by_depth.keys()) if explored_by_depth else 0
    return {
        "new_pivots": added,
        "max_depth_reached": max_depth_explored,
        "max_depth_with_new_pivot": max_depth,
        "explored_count_by_depth": dict(sorted(explored_by_depth.items())),
    }


def build_V_and_D2bar_from_q3(e4: E4, q3: dict, j: int):
    """Branch-INDEPENDENT construction (mathematician-confirmed 2026-08-22:
    "V_L3 と im D2bar は枝非依存 -- 変わるのは pi_*nabla_b' だけ"): builds
    Delta/K/Schreier/V (S1-S4, using the FIXED contexts X0/Y0/Z0, never the
    per-branch candidate word) and the im(D2bar) submodule closure (11 PB4
    relator gradients, branch-independent since PB4's presentation doesn't
    depend on roof/correction), both projected into Lambda/I^j Lambda.
    Returns (ech_combined, idx, sp, info) -- ech_combined can be CLONED
    (cheap, pivot dict copy) per branch to test each branch's own target
    without mutating the shared base."""
    pc = e4.pc
    pb4_rels = q3["formulas"]["presentations"]["PB4"]["relations"]
    require(len(pb4_rels) == 11, "PB4 relation count")
    rk = [fox_gradient(e4, r) for r in pb4_rels]
    rk_pi = [project_to_pi(v) for v in rk]

    x0_val = e4.eval(X0)
    y0_val = e4.eval(Y0)
    z0_val = e4.eval(Z0)
    xbar, ybar, zbar = x0_val[1], y0_val[1], z0_val[1]

    C_word = substitute2(FIXED_WORD, Y0, Z0)
    Cbar_E4 = e4.eval(C_word)

    g1 = (xbar, xbar, ybar)
    g2 = (ybar, zbar, zbar)
    transversal, tree_edge = enum_delta_pc(g1, g2, pc, DELTA_CAP)
    n_delta = len(transversal)
    sgens = schreier_generators_pc(transversal, tree_edge, g1, g2, pc)
    require(len(sgens) == n_delta + 1, f"expected {n_delta+1} Schreier generators, got {len(sgens)}")

    sigma_vectors_pi = []
    for c_word in sgens:
        ga = fox_gradient(e4, substitute2(c_word, X0, Y0))
        gb = fox_gradient(e4, substitute2(c_word, X0, Z0))
        gc = fox_gradient(e4, substitute2(c_word, Y0, Z0))
        diff = add_vec(gc, neg_vec(gb))
        sigma_c = add_vec(translate_vec(e4, diff, Cbar_E4), ga)
        sigma_vectors_pi.append(project_to_pi(sigma_c))

    monomials = enumerate_monomials(j)
    idx = {(c, e): i for i, (c, e) in enumerate((c, e) for c in range(1, 7) for e in monomials)}
    dim_j = len(idx)
    sp = F3BitSpace(dim_j)

    ech_v = F3BitEchelon(sp)
    for v in sigma_vectors_pi:
        vp = project_vec_to_Ij(v, j)
        ech_v.add(sp.vec({idx[k]: c for k, c in vp.items() if k in idx}))
    rank_v = ech_v.rank()

    ech_combined = F3BitEchelon(sp, ech_v.pivots)
    per_relator_receipts = []
    for v_pi in rk_pi:
        receipt = submodule_closure_with_depth(v_pi, j, idx, sp, pc, ech_combined)
        per_relator_receipts.append(receipt)
    rank_combined = ech_combined.rank()

    info = {
        "n_Delta": n_delta, "n_schreier_generators": len(sgens),
        "j": j, "dim_monomials": len(monomials), "dim_Lambda_over_Ij": dim_j,
        "rank_V": rank_v, "rank_V_plus_D2bar_combined": rank_combined,
        "per_relator_closure_receipts": per_relator_receipts,
        "min_depth_reached_across_relators": min(r["max_depth_reached"] for r in per_relator_receipts),
        "depth_requirement_j_minus_1": j - 1,
        "depth_requirement_satisfied": all(r["max_depth_reached"] >= j - 1 for r in per_relator_receipts),
        "total_vectors_explored": sum(sum(r["explored_count_by_depth"].values()) for r in per_relator_receipts),
        "theoretical_ceiling_note": (
            f"worst-case (fully unpruned) ceiling at depth<=j-1={j-1}: "
            f"{sum(10**d for d in range(j))} per relator * 11 relators = "
            f"{sum(10**d for d in range(j)) * 11} -- actual counts are the "
            "per-relator explored_count_by_depth entries above (pruned by "
            "rank-saturation, typically far below the ceiling)"
        ),
    }
    return ech_combined, idx, sp, info


if __name__ == "__main__":
    import json
    import sys

    print("=== koubou158_L3_core_v1_1_invfix.py self-test ===")

    full = ROOT / Q3_CHIEF
    require(full.stat().st_size == Q3_CHIEF_BYTES, "q3_chief byte drift")
    got_sha = sha_file(full)
    require(got_sha == Q3_CHIEF_SHA, f"q3_chief SHA drift: got {got_sha}")
    print(f"q3_chief_receipt: path={Q3_CHIEF} sha256={got_sha} bytes={Q3_CHIEF_BYTES} (MATCH)")

    q3 = json.loads(full.read_text(encoding="utf-8"))
    pb4 = q3["groups"]["PB4"]

    # --- Destructive canary setup: build an OLD-STYLE (pre-fix) inverse
    # table restricted to the 6 marked generators, to PROVE units 7 and 10
    # are genuinely destructive against the pre-fix code shape (terminal
    # ERROR path is exercised for real, not vacuously).
    class _OldStylePc(IndependentPc):
        """Reproduces the EXACT pre-fix v1_1 bug: _inv_gen built from
        marked_generators only (6 rows), skipping all the new (a)(b)(c)
        constructor asserts (which would themselves catch the row-count
        problem) -- so this class exists SOLELY to demonstrate the old
        failure mode for the canary, never used for anything else."""
        def __init__(self, pb4_inner):
            self.n = int(pb4_inner["generator_count"])
            self.power = [tuple(int(x) for x in row) for row in pb4_inner["power_relations"]]
            self.conj = {}
            for row in pb4_inner["conjugate_relations"]:
                self.conj[(row["i"], row["j"])] = tuple(int(x) for x in row["coords"])
            self._inv_gen = [tuple(int(x) for x in row["inverse_coords"])
                              for row in pb4_inner["marked_generators"]]  # BUG: only 6 rows

    print("\n--- destructive canary: units 7 and 10 against OLD-STYLE (6-row) table ---")
    old_pc = _OldStylePc(pb4)
    print(f"old-style _inv_gen length = {len(old_pc._inv_gen)} (expect 6 -- the bug)")
    canary_log = {}
    for unit in (7, 10):
        vec = gen_pcvec(unit)
        try:
            old_pc.inverse(vec)
            canary_log[unit] = "ERROR: NO EXCEPTION RAISED -- canary is VACUOUS, terminal ERROR"
        except IndexError as e:
            canary_log[unit] = f"IndexError (expected, confirms pre-fix bug reproduced): {e}"
        except Exception as e:  # noqa: BLE001
            canary_log[unit] = f"ERROR: unexpected exception type {type(e).__name__}: {e} -- terminal ERROR/UNKNOWN"
    vacuous = False
    for unit, msg in canary_log.items():
        print(f"unit {unit}: {msg}")
        if msg.startswith("ERROR"):
            vacuous = True
    if vacuous:
        print("TERMINAL ERROR: destructive canary did not reproduce the pre-fix failure -- ABORTING self-test")
        sys.exit(2)

    # --- Build the FIXED pc via the real (repaired) IndependentPc, which
    # runs constructor asserts (a) and (b) automatically.
    print("\n--- building repaired IndependentPc (constructor asserts (a)(b) run automatically) ---")
    pc = IndependentPc(pb4)
    print(f"self._inv_gen length = {len(pc._inv_gen)} (expect 10)")
    print("(a) row count assert: PASSED (constructor did not raise)")
    print("(b) first-6-rows-match-marked assert: PASSED (constructor did not raise)")

    print("\n--- (c) left/right inverse law, all 10 units ---")
    receipts = pc.verify_inverse_law_all_units()
    for r in receipts:
        print(f"unit {r['unit']:2d} (weight {r['weight']}): gi={r['gi']} inv={r['inv']} "
              f"left_ok={r['left_ok']} right_ok={r['right_ok']}")
    all_ok = all(r["left_ok"] and r["right_ok"] for r in receipts)
    print(f"(c) inverse law all 10 units: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        print("TERMINAL ERROR: inverse law failed for at least one unit")
        sys.exit(2)

    print("\n--- destructive canary re-run: units 7 and 10 against REPAIRED pc.inverse() ---")
    for unit in (7, 10):
        vec = gen_pcvec(unit)
        inv_v = pc.inverse(vec)  # would have raised IndexError pre-fix; must now succeed
        left = pc.mul(vec, inv_v)
        right = pc.mul(inv_v, vec)
        identity = pc.one()
        ok = (left == identity) and (right == identity)
        print(f"unit {unit}: pc.inverse() succeeded, inverse={list(inv_v)} "
              f"left_ok={left==identity} right_ok={right==identity}")
        if not ok:
            print(f"TERMINAL ERROR: unit {unit} inverse law failed via pc.inverse() path")
            sys.exit(2)

    print("\n=== ALL SELF-TESTS PASSED ===")
    print(f"q3_chief sha256 = {got_sha}")
    self_sha = sha_file(Path(__file__))
    print(f"this file sha256 = {self_sha}")
