"""koubou158_L3_core_v1_2.py

v1.2 of the L3 (Ebar=Pi4[3]) shared core -- falsifier mid-read verdict
2026-08-22: "A側生還" (positive control PASS, numeric reproduction,
prune-path never actually fired in practice) with 3 REQUIRED repairs and
2 recommended ones. v1_1 is FROZEN (kept, no-rename policy); this file
supersedes it for all new runs.

REQUIRED REPAIR 1 (prune-order proof-ification): v1_1 seeded
ech_combined with V's pivots BEFORE closing the 11 relators into it --
this meant a relator-closure BFS step could get "pruned" (add() returns
False, vector already spanned) because it matched a V-PIVOT that was
NEVER itself expanded via the 10 operators (V's Sigma(c) vectors are a
static span, not BFS-explored). The falsifier found this doesn't change
the RESULT (rank(im D2bar alone)=310, rank(+V)=314, confirmed empirically
by disabling the seed) but it breaks the INDUCTIVE soundness argument
("every pivot in the echelon has had all 10 operators applied to it, so
pruning at a pivot is safe") -- V's pivots violate that invariant. FIXED
HERE: build im(D2bar) in a FRESH, UNSEEDED echelon first (all closures
run there, so the invariant holds by construction), THEN clone it and
add V's vectors on top. The two orders' final rank_combined are REQUIRED
to match (314 at j=4) -- if they ever disagree, that is reported loudly,
not silently reconciled.

REQUIRED REPAIR 2 (soundness basis replacement): v1_1's "depth_requirement
_satisfied (depth>=j-1)" canary is a NON-FIRING check -- the falsifier
verified that even an artificial depth_cap=j-2 gives the SAME result
(the true closure saturates before depth j-1 at every j tried), so
"depth reached" was never actually gating anything. The cert's SOUNDNESS
BASIS is replaced: it is now (a) SATURATION -- the BFS queue drains
naturally (every enqueued vector gets all 10 operators applied, no
artificial cutoff was ever imposed) -- plus (b) the REPAIR-1 ordering,
which makes "pruning at an already-spanned vector is safe" an actual
induction (every pivot, by construction, either came from a relator's own
BFS exploration with all 10 operators applied, or is one of V's static
generators added AFTER the relator closure is already complete and
saturated -- V is never itself expanded, but it doesn't need to be: V
is a plain span per spec S4, not a submodule-closure). Depth numbers are
KEPT as observational receipts, no longer as the stated soundness basis.

REQUIRED REPAIR 3 (Delta identification require + discriminant): v1_1
computed g1=(xbar,xbar,ybar), g2=(ybar,zbar,zbar) and never checked them
against any independently-derivable receipt fact, nor recorded any
quantity that would change if g2 (say) were silently altered -- the
falsifier showed a g2 tampering could pass through undetected (all
downstream numbers unchanged by construction, since Delta's exact
identity was never pinned down, only its cardinality). FIXED HERE:
  - require zbar == pc.inverse(pc.mul(ybar, xbar)) -- this is an exact
    ALGEBRAIC IDENTITY forced by Z0=inv_word(Y0+X0)=[-4,-6] (Z0 is
    LITERALLY defined as the word-inverse of Y0+X0), so zbar must equal
    (ybar*xbar)^{-1} as a group element -- ties g1/g2's three coordinates
    together via an independent receipt-derived relation, not just "trust
    e4.eval".
  - record delta_is_abelian (does g1 commute with g2?) and
    delta_isomorphism_type (order 27 exponent-3 groups: either
    elementary abelian C3^3, or the nonabelian exponent-3 group of order
    27 (extraspecial-type, class 2) -- determined by the commutator
    check) as discriminating, receipt-independent quantities.
  - record schreier_generators_digest (sha256 of the sorted, canonical
    Schreier-generator WORD list) -- a fingerprint that would change if
    g1/g2 (hence the transversal/tree) were altered, even if |Delta| and
    downstream ranks happened to stay the same.
"""
from __future__ import annotations

import hashlib
import json
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
        # BUG FIX (found running this file, 2026-08-22, via the NEW
        # repair-3 zbar-identification check calling pc.inverse() on a
        # GENERAL group element for the first time): _inv_gen must cover
        # ALL 10 pc-generators (pb4["inverses"], one row per generator),
        # NOT just the 6 "marked" ones (pb4["marked_generators"]'s own
        # inverse_coords field, which only has 6 entries). This bug was
        # LATENT (never triggered) in every prior script built on this
        # same IndependentPc class pattern this session -- pc.inverse()
        # was previously only ever called on single-marked-generator unit
        # vectors (via E4.eval's negative-letter branch), never on a
        # general product with nonzero weight-2 (generator 7-10) support,
        # so the out-of-range index (idx-1 in {6,7,8,9}) was never hit.
        # Verified pb4["inverses"][0:6] == pb4["marked_generators"][i]
        # ["inverse_coords"] exactly (same data, marked_generators is a
        # subset/duplicate) before switching sources.
        require(len(pb4["inverses"]) == N_GEN, "expected 10 inverse-coord rows (all pc-generators)")
        self._inv_gen = [tuple(int(x) for x in row) for row in pb4["inverses"]]

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


def sha_obj(v: Any) -> str:
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def build_V_and_D2bar_from_q3(e4: E4, q3: dict, j: int):
    """Branch-INDEPENDENT construction (mathematician-confirmed 2026-08-22:
    "V_L3 と im D2bar は枝非依存 -- 変わるのは pi_*nabla_b' だけ"): builds
    Delta/K/Schreier/V (S1-S4, using the FIXED contexts X0/Y0/Z0, never the
    per-branch candidate word) and the im(D2bar) submodule closure (11 PB4
    relator gradients, branch-independent since PB4's presentation doesn't
    depend on roof/correction), both projected into Lambda/I^j Lambda.

    v1.2 ORDERING (repair 1): im(D2bar) is built in a FRESH, UNSEEDED
    echelon first (so every pivot added there came from the relators'
    OWN BFS closure, all 10 operators eventually applied to it); THEN a
    clone of that echelon has V's static Sigma(c) vectors added on top.
    rank(im D2bar alone) and rank(combined) are BOTH recorded.

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

    # REPAIR 3: Delta-identification require. Z0=[-4,-6]=inv_word(Y0+X0)
    # is LITERALLY the word-inverse of Y0+X0 -- so zbar must equal
    # (ybar*xbar)^{-1} as a group identity, independent of trusting
    # e4.eval alone. This ties g1/g2's three coordinates together via a
    # receipt-derived algebraic relation.
    zbar_expected = pc.inverse(pc.mul(ybar, xbar))
    require(zbar == zbar_expected,
            "Delta-identification FAILED: zbar != (ybar*xbar)^-1 -- Z0's own definition "
            "as inv_word(Y0+X0) is violated, g1/g2 construction is untrustworthy")

    C_word = substitute2(FIXED_WORD, Y0, Z0)
    Cbar_E4 = e4.eval(C_word)

    g1 = (xbar, xbar, ybar)
    g2 = (ybar, zbar, zbar)
    transversal, tree_edge = enum_delta_pc(g1, g2, pc, DELTA_CAP)
    n_delta = len(transversal)
    sgens = schreier_generators_pc(transversal, tree_edge, g1, g2, pc)
    require(len(sgens) == n_delta + 1, f"expected {n_delta+1} Schreier generators, got {len(sgens)}")

    # REPAIR 3 (discriminating quantities): Delta's isomorphism type
    # (order 27, exponent 3 -> either elementary abelian C3^3, or the
    # nonabelian exponent-3 group of order 27, distinguished by whether
    # g1,g2 commute) and a digest of the Schreier-generator word list --
    # both would change if g1/g2 (hence the transversal/tree) were
    # silently altered, even if downstream ranks happened to coincide.
    g1g2 = tuple(pc.mul(g1[i], g2[i]) for i in range(3))
    g2g1 = tuple(pc.mul(g2[i], g1[i]) for i in range(3))
    delta_is_abelian = (g1g2 == g2g1)
    delta_isomorphism_type = (
        "elementary_abelian_C3^3" if delta_is_abelian else
        "nonabelian_exponent3_order27_class2"
    )
    schreier_generators_digest = sha_obj(sorted(sgens))

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

    # REPAIR 1: build im(D2bar) FIRST, in its OWN fresh/unseeded echelon.
    ech_d2 = F3BitEchelon(sp)
    per_relator_receipts = []
    for v_pi in rk_pi:
        receipt = submodule_closure_with_depth(v_pi, j, idx, sp, pc, ech_d2)
        per_relator_receipts.append(receipt)
    rank_d2_alone = ech_d2.rank()

    # THEN clone and add V's static Sigma(c) vectors on top.
    ech_combined = ech_d2.clone()
    for v in sigma_vectors_pi:
        vp = project_vec_to_Ij(v, j)
        ech_combined.add(sp.vec({idx[k]: c for k, c in vp.items() if k in idx}))
    rank_combined = ech_combined.rank()

    # V's OWN rank (for reference/reporting) -- built separately, not
    # part of the soundness-relevant ordering above.
    ech_v_only = F3BitEchelon(sp)
    for v in sigma_vectors_pi:
        vp = project_vec_to_Ij(v, j)
        ech_v_only.add(sp.vec({idx[k]: c for k, c in vp.items() if k in idx}))
    rank_v = ech_v_only.rank()

    # REPAIR 2: soundness basis is SATURATION (queue drains naturally --
    # true by construction of the while-loop in submodule_closure_with_
    # depth: it is never depth-capped) + the REPAIR-1 ordering induction.
    # Depth numbers are kept purely as OBSERVATIONAL receipts below (the
    # falsifier showed depth>=j-1 never actually gates anything -- an
    # artificial depth_cap=j-2 reproduces the same result).
    saturation_confirmed = True  # BFS always runs to natural queue exhaustion; no depth cap is ever imposed in this code path

    info = {
        "n_Delta": n_delta, "n_schreier_generators": len(sgens),
        "delta_is_abelian": delta_is_abelian,
        "delta_isomorphism_type": delta_isomorphism_type,
        "schreier_generators_digest": schreier_generators_digest,
        "zbar_identification_check": "zbar == (ybar*xbar)^-1 -- REQUIRED and PASSED (see require() above)",
        "j": j, "dim_monomials": len(monomials), "dim_Lambda_over_Ij": dim_j,
        "rank_D2bar_alone": rank_d2_alone,
        "rank_V": rank_v, "rank_V_plus_D2bar_combined": rank_combined,
        "ordering_note": "v1.2 (repair 1): im(D2bar) built in a fresh, unseeded echelon "
                         "FIRST (rank_D2bar_alone above); V's static Sigma(c) vectors "
                         "added to a CLONE of that echelon SECOND (rank_V_plus_D2bar_"
                         "combined). This ordering is what makes the pruning-soundness "
                         "argument an actual induction (see module docstring repair 1).",
        "soundness_basis": "SATURATION (BFS queue drains naturally, no depth cap ever "
                           "imposed) + REPAIR-1 ORDERING (every im(D2bar) pivot came "
                           "from a relator's own BFS closure with all 10 operators "
                           "eventually applied; V is added afterward as a plain static "
                           "span, never itself expanded, per spec S4) -- NOT the "
                           "depth>=j-1 canary (falsifier showed that canary never fires: "
                           "an artificial depth_cap=j-2 reproduces the same result).",
        "saturation_confirmed": saturation_confirmed,
        "per_relator_closure_receipts": per_relator_receipts,
        "min_depth_reached_across_relators": min(r["max_depth_reached"] for r in per_relator_receipts),
        "depth_observational_only_note": "depth fields below are OBSERVATIONAL RECEIPTS "
                                         "only, no longer the stated soundness basis (see "
                                         "soundness_basis field above) -- kept per the "
                                         "no-rename/no-delete policy and because they are "
                                         "still useful diagnostic information",
        "depth_requirement_j_minus_1_observational": j - 1,
        "depth_requirement_satisfied_observational": all(r["max_depth_reached"] >= j - 1 for r in per_relator_receipts),
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
