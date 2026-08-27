#!/usr/bin/env python3
"""Independent checker for the task187 u0/v0 boundary preimages.

No producer module is imported.  The task179 checker supplies its separately
implemented finite-group/Fox arithmetic; row-space and correlation replay are
owned here.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-u0v0-boundary-preimage/v1"
COMMON = "R07_U0V0_BOUNDARY_PREIMAGE_V1"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
FIXTURE = ROOT / "search/certs/d972_r07_u0v0_boundary_preimage_selftest_v1_20260827.json"
PINS = {
    "task179_producer": ("search/d972_r07_positive_common_word_colgen_v1.py", 123870, "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    "task179_checker": ("crosscheck/check_d972_r07_positive_common_word_colgen_v1.py", 73780, "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"),
    "task179_driver": ("search/d972_r07_positive_common_word_colgen_gha_driver_v1.g", 12872, "48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"),
    "task179_fixture": ("search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json", 407, "46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"),
    "v156": ("sol/proof_r07_task179_exact_exponent_lattice_v156.md", 10409, "2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d"),
    "v157": ("sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md", 8367, "08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8"),
    "selftest_fixture": ("search/certs/d972_r07_u0v0_boundary_preimage_selftest_v1_20260827.json", 699, "230de05643a94f775120ef7e62b2f2023b13fd12228f18ca860ef81b134babff"),
}
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
EXPECTED_RESOURCE_LIMITS = {"wall_seconds": 19800.0, "boundary_pairs": 8000000,
    "fibre_scans": 80000000, "candidate_words": 2000000, "retained_columns": 250000,
    "checkpoint_bytes": 4000000000, "rss_bytes": 5700000000, "oracle_rounds": 1,
    "global_roster": 357128352}

def require(ok: bool, msg: str) -> None:
    if not ok: raise RuntimeError(msg)
def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
def digest(value: Any) -> str: return hashlib.sha256(canon(value)).hexdigest()
def validate_seal(value: dict[str, Any]) -> None:
    claimed = value.get("self_digest"); body = dict(value); body.pop("self_digest", None)
    require(type(claimed) is str and claimed == digest(body), "receipt self digest")
def auth() -> dict[str, Any]:
    result = {}
    for name, (rel, size, sha) in PINS.items():
        raw = (ROOT / rel).read_bytes() if (ROOT / rel).is_file() else b""
        require(len(raw) == size and hashlib.sha256(raw).hexdigest() == sha, "pin:" + rel)
        result[name] = {"path": rel, "bytes": size, "sha256": sha}
    return result
def load_checker() -> Any:
    path = ROOT / PINS["task179_checker"][0]
    spec = importlib.util.spec_from_file_location("d972_task179_independent_boundary", path)
    require(spec is not None and spec.loader is not None, "checker loader")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    module._boundary_auth = module.authenticate()
    return module
def inv(word: Sequence[int]) -> tuple[int, ...]: return tuple(-x for x in reversed(word))
def mul(*words: Sequence[int]) -> tuple[int, ...]:
    out = ()
    for word in words:
        for x in word:
            if out and out[-1] == -int(x): out = out[:-1]
            else: out += (int(x),)
    return out
def exponent(word: Sequence[int]) -> tuple[int, int]:
    return (sum(1 if x == 1 else -1 if x == -1 else 0 for x in word),
            sum(1 if x == 2 else -1 if x == -2 else 0 for x in word))
def add(target: dict[bytes, int], source: dict[bytes, int], scalar: int) -> None:
    for k, v in source.items():
        z = (target.get(k, 0) + scalar * int(v)) % 3
        if z: target[k] = z
        else: target.pop(k, None)
def pair(f: dict[bytes, int], row: dict[bytes, int]) -> int:
    return sum(v * row.get(k, 0) for k, v in f.items()) % 3
def sparse(c: Any, rows: list[list[Any]]) -> dict[bytes, int]:
    require(type(rows) is list and all(type(item) is list and len(item) == 2 and type(item[0]) is str and
                                       type(item[1]) is int and not isinstance(item[1], bool) for item in rows),
            "canonical sparse schema")
    return c.parse_sparse(rows)
def public(row: dict[bytes, int]) -> list[list[Any]]:
    return [[k.hex(), int(row[k]) % 3] for k in sorted(row) if int(row[k]) % 3]

class Space:
    def __init__(self) -> None:
        self.pivots: list[bytes] = []; self.rows: dict[bytes, dict[bytes, int]] = {}; self.origins = {}
    def reduce(self, source: dict[bytes, int]):
        row = dict(source); coeff = {}
        for p in self.pivots:
            z = row.get(p, 0)
            if z:
                add(row, self.rows[p], -z)
                for k, v in self.origins[p].items():
                    q = (coeff.get(k, 0) + z * v) % 3
                    if q: coeff[k] = q
                    else: coeff.pop(k, None)
        return row, coeff
    def add(self, source: dict[bytes, int], column: int):
        row = dict(source); coeff = {column: 1}
        for p in self.pivots:
            z = row.get(p, 0)
            if z:
                add(row, self.rows[p], -z)
                for k, v in self.origins[p].items():
                    q = (coeff.get(k, 0) - z * v) % 3
                    if q: coeff[k] = q
                    else: coeff.pop(k, None)
        require(row, "dependent retained boundary row")
        pivot = min(row); scale = 1 if row[pivot] == 1 else 2
        self.rows[pivot] = {k: scale * v % 3 for k, v in row.items() if scale * v % 3}
        self.origins[pivot] = {k: scale * v % 3 for k, v in coeff.items() if scale * v % 3}
        self.pivots.append(pivot)
        return pivot, self.origins[pivot]
    def dual(self, target: dict[bytes, int]):
        rem, _ = self.reduce(target); require(rem, "dual after membership")
        f = {min(rem): 1}
        for p in reversed(self.pivots):
            z = -sum(v * f.get(k, 0) for k, v in self.rows[p].items() if k != p) % 3
            if z: f[p] = z
            else: f.pop(p, None)
        require(all(pair(f, self.rows[p]) == 0 for p in self.pivots) and pair(f, target), "terminal dual")
        return f

def words(rt: dict[str, Any]) -> dict[str, tuple[int, ...]]:
    result = {}
    for ordinal in (3, 9, 12):
        found = [r["word"] for r in rt["obj"]["roster"] if r.get("layer") == "q0_relator" and int(r.get("ordinal")) == ordinal]
        require(len(found) == 1, "registered ordinal")
        result[str(ordinal)] = tuple(found[0])
    result["v0"] = mul(result["9"], result["12"], inv(result["3"]), inv(result["3"]))
    result["u0"] = mul(result["9"], *([inv(result["v0"])] * 8))
    require(exponent(result["v0"]) == (0, 18) and exponent(result["u0"]) == (18, 0), "integer exponent")
    return result

def direct_replay(rt: dict[str, Any], relator: Sequence[int]) -> dict[str, Any]:
    """Recompute the producer's three quotient identities independently."""
    c = rt["checker"]; obj = rt["obj"]
    conjugate = c.reduce_word(tuple() + tuple(relator) + c.inverse(tuple()))
    require(obj["joint"].eval(conjugate) == obj["joint"].identity, "independent conjugate")
    corrected = c.reduce_word(tuple(obj["g760"]) + tuple(conjugate))
    base_hex = c.hexagon_words(obj["g760"]); new_hex = c.hexagon_words(corrected)
    quotient_values = []
    for block, quotient, base, new in (
            (1, rt["e3"], c.embed_pb3(base_hex[0]), c.embed_pb3(new_hex[0])),
            (2, rt["e3"], c.embed_pb3(base_hex[1]), c.embed_pb3(new_hex[1])),
            (3, rt["e4"], c.pentagon_word(obj["g760"]), c.pentagon_word(corrected))):
        _difference, base_value, new_value = c.raw_difference(quotient, base, new)
        require(base_value == quotient.identity and new_value == quotient.identity, "independent quotient identity")
        quotient_values.append(c.element_blob(new_value).hex())
    return {"delta_word": [], "relator_word": list(relator), "conjugate_word": list(conjugate),
            "corrected_word": list(corrected), "quotient_value_blobs": quotient_values,
            "eleven_occurrence_replay": True, "all_seven_direct": True}

def boundary_correlation(c: Any, rt: dict[str, Any], dual: dict[bytes, int]) -> dict[str, Any]:
    support = {}
    for key, value in dual.items():
        if key[:1] == b"R":
            b, component, raw = c.decode_row_key(key)
            support.setdefault((b, component), []).append((raw, value, c.parse_element(raw, b)))
    acc = {}; contributors = {}
    for block, count in ((1, 2), (2, 2), (3, 11)):
        q = rt["e3"] if block in (1, 2) else rt["e4"]
        source_rows = rt["obj"]["pb3_rows"] if block in (1, 2) else rt["obj"]["pb4_rows"]
        for index in range(1, count + 1):
            occurrences = [(component, h, q.inverse(h), int(coefficient))
                           for (component, h), coefficient in source_rows[index - 1].items()]
            for component, h, h_inv, base_coefficient in occurrences:
                for g_raw, lam, g in support.get((block, component), []):
                    t = q.mul(g, h_inv)
                    require(q.mul(t, h) == g, "independent t*h=g")
                    t_raw = c.element_blob(t); key = (block, t_raw, index)
                    acc[key] = (acc.get(key, 0) + int(lam) * base_coefficient) % 3
                    contributors.setdefault(key, []).append({"component": int(component), "g_hex": g_raw.hex(), "h_hex": c.element_blob(h).hex(), "lambda_coefficient": int(lam), "base_coefficient": base_coefficient % 3})
    for key in contributors:
        contributors[key].sort(key=lambda row: (int(row["component"]), str(row["g_hex"]),
                                                  str(row["h_hex"]), int(row["lambda_coefficient"]),
                                                  int(row["base_coefficient"])))
    return {"complete": True, "sampled": False,
            "active": [[b, t.hex(), i] for (b, t, i), v in sorted(acc.items()) if v % 3],
            "scanned_occurrences": sum(len(x) for x in contributors.values()),
            "contributors": {f"{b}:{t.hex()}:{i}": x for (b, t, i), x in contributors.items()},
            "accumulated": {f"{b}:{t.hex()}:{i}": int(v) for (b, t, i), v in acc.items() if v % 3}}

def validate_production(receipt: dict[str, Any]) -> None:
    c = load_checker(); rt = c.independent_runtime(); ws = words(rt)
    require(receipt.get("pins") == auth(), "receipt pins")
    require(receipt.get("task179_arithmetic_pins") == c._boundary_auth, "task179 arithmetic source pins")
    require(receipt.get("status") == "PASS" and receipt.get("terminal") == COMMON, "receipt envelope")
    claims = receipt.get("claims", {})
    require(receipt.get("negative_claim") is not True and
            claims.get("raw_task179_word") is False and claims.get("cofinal_lift") is False and
            claims.get("fake") is False and claims.get("ihara") is False, "PASS claim boundary")
    require(receipt.get("words") == {k: list(v) for k, v in ws.items()}, "literal u0/v0 words")
    require(receipt.get("word_exponents") == {k: list(exponent(v)) for k, v in ws.items()}, "all integer word exponents")
    joint = rt["obj"]["joint"]
    require(all(joint.eval(list(ws[k])) == joint.identity for k in ("3", "9", "12", "u0", "v0")), "all joint-kernel words")
    require(tuple(receipt["targets"]["u0"]["normalized_residue"]) == (1, 0) and
            tuple(receipt["targets"]["v0"]["normalized_residue"]) == (0, 1), "normalized residues")
    space = Space(); rebuilt = []; transitions = []
    expected_targets = {}
    for label in ("u0", "v0"):
        raw, _ = c.direct_correction(rt, [], list(ws[label])); raw = {k: v for k, v in raw.items() if not k.startswith(b"E")}
        target = {}; add(target, raw, -1); expected_targets[label] = (raw, target)
        item = receipt["targets"][label]
        require(tuple(item["word"]) == ws[label] and tuple(item["integer_exponent"]) == exponent(ws[label]), label + " word")
        require(item["A"] == public(raw) and item["target"] == public(target), label + " direct row")
        require(item["A_sha256"] == digest(public(raw)) and item["target_sha256"] == digest(public(target)), label + " digest")
        expected_replay = direct_replay(rt, list(ws[label]))
        transcript = item.get("direct_replay", {})
        require(transcript.get("delta_word") == [] and transcript.get("relator_word") == list(ws[label]) and
                transcript.get("conjugate_word") == expected_replay.get("conjugate_word") and
                transcript.get("corrected_word") == expected_replay.get("corrected_word") and
                type(transcript.get("quotient_value_blobs")) is list and
                len(transcript.get("quotient_value_blobs")) == 3 and
                all(type(blob) is str for blob in transcript.get("quotient_value_blobs")) and
                transcript.get("quotient_value_blobs") == expected_replay.get("quotient_value_blobs") and
                transcript.get("eleven_occurrence_replay") is True and
                transcript.get("direct_all_seven_replay") is True and
                expected_replay.get("all_seven_direct") is True, label + " direct replay transcript")
    for rec in receipt.get("columns", []):
        cid = int(rec["column_id"]); require(cid == len(rebuilt) + 1 and rec["rank_before"] == len(space.pivots), "column order")
        require(rec.get("family") == "boundary", "column family")
        p = rec["provenance"]; require(p.get("family") == "boundary" and
            int(p.get("block")) in (1, 2, 3) and int(p.get("base_relator_index")) >= 1 and
            isinstance(p.get("translation_hex"), str) and p.get("left_translation") == "t=g*h^-1; t*h=g" and
            p.get("active_key") == [int(p.get("block")), p.get("translation_hex"), int(p.get("base_relator_index"))] and
            p.get("complete_support_occurrence_accumulation") is True and isinstance(p.get("contributing_pairs"), list), "boundary provenance")
        row = c.boundary_row(rt, int(p["block"]), int(p["base_relator_index"]), p["translation_hex"])
        require(public(row) == rec["sparse_row"] and rec["sparse_row_sha256"] == digest(rec["sparse_row"]), "boundary row replay")
        dual = sparse(c, rec["active_dual"])
        valid_duals = []
        for _label in ("u0", "v0"):
            _remainder, _ = space.reduce(expected_targets[_label][1])
            if _remainder:
                valid_duals.append(space.dual(expected_targets[_label][1]))
        require(any(dual == candidate for candidate in valid_duals), "active dual replay")
        corr = boundary_correlation(c, rt, dual); key = f"{p['block']}:{p['translation_hex']}:{p['base_relator_index']}"
        require(all(type(item) is list and len(item) == 3 and type(item[0]) is int and
                    type(item[1]) is str and type(item[2]) is int for item in corr["active"]),
                "active schema")
        least = min(corr["active"], key=lambda item: (item[0], bytes.fromhex(item[1]), item[2]), default=None)
        require(least is not None and key == f"{least[0]}:{least[1]}:{least[2]}", "least ACTIVE selection")
        require(key in corr["accumulated"] and corr["accumulated"][key] != 0 and
                corr["contributors"].get(key) == p.get("contributing_pairs") and
                rec["dual_pairing"] == pair(dual, row) and p.get("scalar") == rec["dual_pairing"] and
                rec.get("active_dual_sha256") == digest(rec.get("active_dual")), "complete ACTIVE correlation")
        pivot, ancestry = space.add(row, cid)
        computed_after = len(space.pivots)
        require(rec["rank_after"] == computed_after == rec["rank_before"] + 1 and
                rec["pivot_hex"] == pivot.hex() and rec["pivot_ancestry"] == [[k, v] for k, v in sorted(ancestry.items())], "pivot ancestry/rank")
        transitions.append({"column_id": cid, "rank_before": rec["rank_before"], "rank_after": computed_after,
                            "pivot_hex": pivot.hex(), "pivot_ancestry": [[k, v] for k, v in sorted(ancestry.items())],
                            "target_reconsidered": ["u0", "v0"]})
        rebuilt.append(row)
    require(receipt.get("rank_transitions") == transitions and receipt.get("rank") == len(space.pivots), "rank transition transcript")
    for label in ("u0", "v0"):
        target = expected_targets[label][1]; item = receipt["targets"][label]; decision = item["decision"]
        rem, coeff = space.reduce(target)
        if decision == "MEMBER_D":
            chain = [[int(k), int(v)] for k, v in item["chain"]]; combined = {}
            for k, v in chain: add(combined, rebuilt[k - 1], v)
            require(not rem and chain == sorted(chain) and chain == [[int(k), int(v)] for k, v in sorted(coeff.items())] and combined == target and item["literal_boundary_sum"] == public(target), label + " chain")
            residual = dict(expected_targets[label][0]); add(residual, combined, 1); require(not residual, label + " A+d residual")
            require(item.get("zero_residual") == [] and item.get("zero_residual_sha256") == digest([]), label + " zero residual")
        elif decision == "NONMEMBER_D":
            require(rem, label + " nonmember remainder"); d = item["terminal_dual"]; dual = sparse(c, d["row"])
            require(d.get("row_sha256") == digest(d.get("row")) and d.get("annihilates_retained") is True and
                    dual == space.dual(target) and d["pairing_target"] == pair(dual, target) != 0, label + " terminal dual")
            corr = boundary_correlation(c, rt, dual); require(corr == d["full_correlation"] and not corr["active"] and corr["complete"] and not corr["sampled"], label + " complete negative correlation")
        else: raise RuntimeError("untyped decision")
    both = all(receipt["targets"][label]["decision"] == "MEMBER_D" for label in ("u0", "v0"))
    if both:
        require(receipt.get("finite_consequence") == "nu(ker(A on correction plus boundary coefficients)) = F3^2" and
                receipt.get("normalization_rule") == "c1=c q(u0,a) q(v0,b), d1=d-a*d_u-b*d_v; q(w,0)=1, q(w,1)=w^-1, q(w,2)=w; registered cubes exactify the integer exponent" and
                receipt.get("q_table") == {"q(w,0)": "1", "q(w,1)": "w^-1", "q(w,2)": "w"}, "finite consequence/rule")
    else:
        require(receipt.get("finite_consequence") is None and receipt.get("normalization_rule") is None and receipt.get("q_table") is None, "conditional consequence")

def validate_selftest(receipt: dict[str, Any]) -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="ascii")); require(receipt.get("schema") == fixture["schema"], "fixture schema")
    names = ["roster_ordinal", "exponent_sign", "u0_formula", "v0_formula", "target_sign", "block_tag",
             "boundary_coefficient", "left_translation", "coefficient_two_inverse", "pivot_ancestry",
             "positive_residual", "terminal_dual_coefficient", "sampled_as_complete",
             "resource_stop_nonmember", "boundary_provenance"]
    controls = receipt.get("mutation_controls", {}); require(receipt.get("status") == "PASS" and
        controls.get("attempted") == 15 and controls.get("rejected") == 15 and controls.get("names") == names,
        "selftest mutations")
    toy = receipt.get("toy", {})
    def pm(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(left[right[i] - 1] for i in range(3))
    def pi(value: tuple[int, ...]) -> tuple[int, ...]:
        answer = [0, 0, 0]
        for i, image in enumerate(value, 1): answer[image - 1] = i
        return tuple(answer)
    def tk(block: int, component: int, value: tuple[int, ...]) -> bytes:
        require(block == 1 and component in (1, 2, 3), "checker toy typed key")
        return b"R" + bytes((block, component)) + bytes(value)
    def tl(translation: tuple[int, ...], source: Sequence[tuple[int, tuple[int, ...], int]]) -> dict[bytes, int]:
        answer: dict[bytes, int] = {}
        for component, h, coefficient in source:
            key = tk(1, component, pm(translation, h)); value = (answer.get(key, 0) + coefficient) % 3
            if value: answer[key] = value
            else: answer.pop(key, None)
        return answer
    identity, sigma, tau = (1, 2, 3), (2, 1, 3), (1, 3, 2)
    source_one = [(1, identity, 1), (2, sigma, 1)]; source_two = [(1, identity, 1), (2, tau, 1)]
    first = tl(tau, source_one); second = tl(tau, source_two)
    family = [tl(t, source) for t in itertools.permutations((1, 2, 3)) for source in (source_one, source_two)]
    outside = {tk(1, 3, identity): 1}; partial = Space()
    require(tk(1, 2, identity) in tl(pi(sigma), source_one), "checker toy in-orbit boundary")
    transitions = []
    for number, row in enumerate((first, second), 1):
        before = len(partial.pivots); pivot, ancestry = partial.add(row, number)
        require(len(partial.pivots) == before + 1, "checker toy rank")
        transitions.append({"row": public(row), "pivot": pivot.hex(), "ancestry": [[k, v] for k, v in sorted(ancestry.items())]})
    rem, chain = partial.reduce(first); require(not rem and chain == {1: 1}, "checker toy positive chain")
    complete = Space()
    for number, row in enumerate(family, 1):
        if complete.reduce(row)[0]: complete.add(row, number)
    dual = complete.dual(outside)
    require(len(family) == 12 and public(dual) == toy.get("negative_dual") and pair(dual, outside) == 1,
            "checker toy complete dual")
    require(all(pair(dual, row) == 0 for row in family) and
            all(tk(1, 3, identity) not in row for row in family), "checker toy full correlation")
    inverse_row = tl(pi(tau), [(1, identity, 2)])
    require(inverse_row == {tk(1, 1, pi(tau)): 2} and inverse_row[tk(1, 1, pi(tau))] == 2,
            "checker toy inverse coefficient")
    require(toy.get("boundary_rows") == public(first) and toy.get("inside_target") == public(first) and
            toy.get("outside_target") == public(outside) and toy.get("positive_chain") == [[1, 1]] and
            toy.get("rank_transitions") == transitions and toy.get("full_correlation") is True,
            "checker toy replay")
    nc = toy.get("noncommutative", {})
    require(nc.get("sigma") == list(sigma) and nc.get("tau") == list(tau) and
            nc.get("sigma_tau") == list(pm(sigma, tau)) and nc.get("tau_sigma") == list(pm(tau, sigma)) and
            nc.get("left_translation") is True and nc.get("block_tagging") is True and
            nc.get("coefficient_two_inverse") is True and nc.get("resource_stop") is True,
            "checker toy noncommutative arithmetic")
    state = {"roster_ordinal": 3, "exponent_sign": 1, "u0_formula": "r9*v0^-8", "v0_formula": "r9*r12*r3^-2",
             "target_sign": -1, "block_tag": 1, "boundary_coefficient": 1, "left_translation": "t*h=g",
             "coefficient_two_inverse": True, "pivot_ancestry": [[1, 2], [2, 1]], "positive_residual": [],
             "terminal_dual_coefficient": 1, "sampled_as_complete": False, "resource_stop_nonmember": False,
             "boundary_provenance": True}
    def validate_candidate(x: dict[str, Any]) -> None:
        roster = {3: (1, 2, 1, -2), 9: (1, 2), 12: (2, 1)}; selected = roster.get(x["roster_ordinal"])
        require(selected is not None and x["exponent_sign"] in (1, -1), "checker roster")
        signed = tuple(x["exponent_sign"] * letter for letter in selected)
        require(exponent(signed) == (2, 0), "checker signed exponent")
        v0 = mul(roster[9], roster[12], inv(roster[3]), inv(roster[3]))
        require((v0 if x["v0_formula"] == "r9*r12*r3^-2" else mul(roster[9], roster[12], roster[3], roster[3])) == v0, "checker v0 formula")
        u0 = mul(roster[9], *([inv(v0)] * 8))
        require((u0 if x["u0_formula"] == "r9*v0^-8" else mul(roster[9], *([v0] * 8))) == u0, "checker u0 formula")
        require(x["target_sign"] == -1 and {k: (x["target_sign"] * v) % 3 for k, v in first.items()} ==
                {k: (-v) % 3 for k, v in first.items()}, "checker target sign")
        require(x["block_tag"] == 1 and tk(x["block_tag"], 1, tau) == next(iter(first)), "checker block tag")
        require(tl(tau, [(1, identity, x["boundary_coefficient"]), (2, sigma, 1)]) == first and
                x["left_translation"] == "t*h=g", "checker translation coefficient")
        require(x["coefficient_two_inverse"] is True and inverse_row == {tk(1, 1, pi(tau)): 2}, "checker inverse")
        residual = dict(first); add(residual, first, -1); require(x["positive_residual"] == [] and not residual, "checker residual")
        require(x["terminal_dual_coefficient"] == dual.get(tk(1, 3, identity)) == 1 and
                x["sampled_as_complete"] is False and x["resource_stop_nonmember"] is False and
                x["boundary_provenance"] is True, "checker terminal fields")
        replay = Space()
        for number, row in enumerate((first, second), 1):
            pivot, ancestry = replay.add(row, number)
            if number == 2: require(ancestry == dict(x["pivot_ancestry"]), "checker ancestry")
        complete_replay = Space()
        for number, row in enumerate(family, 1):
            if complete_replay.reduce(row)[0]: complete_replay.add(row, number)
        candidate = complete_replay.dual(outside)
        require(not replay.reduce(first)[0] and pair(candidate, outside) == 1 and
                all(pair(candidate, row) == 0 for row in family) and x["terminal_dual_coefficient"] == candidate.get(tk(1, 3, identity)),
                "checker complete replay")
    rejected = 0
    mutations = [("roster_ordinal", 4), ("exponent_sign", -1), ("u0_formula", "r9*v0^8"),
                 ("v0_formula", "r9*r12*r3^2"), ("target_sign", 1), ("block_tag", 2),
                 ("boundary_coefficient", 2), ("left_translation", "h*t=g"),
                 ("coefficient_two_inverse", False), ("pivot_ancestry", []),
                 ("positive_residual", [["bad", 1]]), ("terminal_dual_coefficient", 2),
                 ("sampled_as_complete", True), ("resource_stop_nonmember", True),
                 ("boundary_provenance", False)]
    rejected = 0
    for field, value in mutations:
        candidate = copy.deepcopy(state); candidate[field] = value
        try: validate_candidate(candidate)
        except RuntimeError: rejected += 1
    require(rejected == len(mutations), "checker mutation replay")
    independent_toy = {"boundary_rows": public(first), "inside_target": public(first),
        "outside_target": public(outside), "positive_chain": [[1, 1]], "negative_dual": public(dual),
        "full_correlation": True, "rank_transitions": transitions,
        "noncommutative": {"sigma": list(sigma), "tau": list(tau), "sigma_tau": list(pm(sigma, tau)),
            "tau_sigma": list(pm(tau, sigma)), "left_translation": True, "block_tagging": True,
            "coefficient_two_inverse": True, "resource_stop": True}}
    for field in ("boundary_rows", "inside_target", "outside_target", "positive_chain", "negative_dual",
                  "full_correlation", "rank_transitions", "noncommutative"):
        require(toy.get(field) == independent_toy[field], "independent toy receipt field:" + field)
        require(fixture["expected"].get(field) == independent_toy[field], "independent toy fixture field:" + field)

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); p.add_argument("receipt", type=Path); p.add_argument("--selftest", action="store_true"); return p
def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv); receipt = json.loads(args.receipt.read_text(encoding="ascii"))
    try:
        validate_seal(receipt)
        if args.selftest: validate_selftest(receipt)
        elif receipt.get("status") in (UNKNOWN_RESOURCE, UNKNOWN_INPUT):
            require(receipt.get("pins") == auth(), "UNKNOWN pins")
            terminal = str(receipt.get("terminal", ""))
            require(terminal.startswith(receipt["status"] + ":") and type(receipt.get("reason")) is str and
                    bool(receipt.get("reason")) and type(receipt.get("claims")) is dict, "typed UNKNOWN")
            if receipt["status"] == UNKNOWN_RESOURCE:
                parts = terminal.split(":")
                require(len(parts) == 4 and ">" in parts[3] and parts[1] in ALLOWED_RESOURCE_CAPS and
                        parts[2] in ALLOWED_RESOURCE_CAPS[parts[1]], "resource cap terminal")
                phase, cap = parts[1], parts[2]
                value, limit = parts[3].split(">", 1)
                resource = receipt.get("resource", {})
                require(type(resource) is dict and resource.get("phase") == phase and
                        resource.get("terminal_cap") == cap and
                        str(resource.get("terminal_value")) == value and str(resource.get("terminal_limit")) == limit and
                        type(resource.get("elapsed_seconds")) in (int, float) and resource.get("elapsed_seconds") >= 0 and
                        type(resource.get("rss_bytes")) is int and resource.get("rss_bytes") >= 0 and
                        resource.get("single_process") is True and isinstance(resource.get("limits"), dict) and
                        isinstance(resource.get("counters"), dict) and
                        resource.get("limits", {}).get(cap) == resource.get("terminal_limit") and
                        (cap not in resource.get("counters", {}) or
                         resource.get("counters", {}).get(cap) == resource.get("terminal_value")) and
                        type(resource.get("terminal_cap")) is str and type(resource.get("terminal_limit")) in (int, float) and
                        type(resource.get("terminal_value")) in (int, float) and
                        resource.get("terminal_value") > resource.get("terminal_limit") and
                        resource.get("limits") == EXPECTED_RESOURCE_LIMITS and
                        set(resource.get("counters", {})) ==
                        {"boundary_pairs", "fibre_scans", "candidate_words", "retained_columns",
                         "checkpoint_bytes", "global_roster", "oracle_rounds"} and
                        all(type(v) is int and v >= 0 and v <= EXPECTED_RESOURCE_LIMITS[k]
                            for k, v in resource.get("counters", {}).items() if k != cap), "resource receipt binding")
                if cap == "wall_seconds":
                    require(resource["elapsed_seconds"] == resource["terminal_value"], "wall trigger snapshot")
                if cap == "rss_bytes":
                    require(resource["rss_bytes"] == resource["terminal_value"], "rss trigger snapshot")
                if cap in resource["counters"]:
                    require(resource["counters"][cap] == resource["terminal_value"], "counter trigger snapshot")
            require(receipt.get("negative_claim") is not True and
                    all(field not in receipt for field in ("decisions", "nonmember", "finite_consequence",
                                                           "normalization_rule", "q_table", "targets", "columns", "rank")) and
                    receipt.get("claims", {}).get("raw_task179_word") is False and
                    receipt.get("claims", {}).get("fake") is False and receipt.get("claims", {}).get("cofinal_lift") is False and
                    receipt.get("claims", {}).get("ihara") is False, "UNKNOWN claim boundary")
        else: validate_production(receipt)
    except (OSError, ValueError, RuntimeError) as exc:
        print("R07_U0V0_BOUNDARY_PREIMAGE_V1_CHECKER_FAIL " + str(exc)); return 1
    print("R07_U0V0_BOUNDARY_PREIMAGE_V1_CHECKER_PASS terminal=" + str(receipt.get("terminal")))
    return 0
if __name__ == "__main__": raise SystemExit(main())
