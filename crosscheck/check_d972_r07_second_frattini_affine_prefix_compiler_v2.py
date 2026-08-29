#!/usr/bin/env python3
"""Independent task193-v2 checker.

The adapter receipt and its independent checker verdict are authenticated
first.  The frozen task193-v1 checker is then source-patched only at its input
firewall and at the v239 pointed-row hook; its independent affine/Fox replay
remains the checking mathematics and never invokes a legacy checker.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import stat
import types
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-second-frattini-affine-prefix-compiler/v2"
COMMON = "R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
ADAPTER_SCHEMA = "d972-r07-history-free-task193-compat-adapter/v3"
ADAPTER_ACCEPTED = "R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_A0_REPLAY"
ADAPTER_CHECK_SCHEMA = ADAPTER_SCHEMA + "/checker-verdict/v3"
ADAPTER_PRODUCER_PIN = (
    "search/d972_r07_history_free_task193_compat_adapter_v3.py", 14038,
    "7be27b31f0c6e4acf0948341dfaae9d9d880b204774d04660a77982c0546245c")
ADAPTER_CHECKER_PIN = (
    "crosscheck/check_d972_r07_history_free_task193_compat_adapter_v3.py", 16804,
    "f123daeec769aff9254bf913514f0792f20a2f32725aa19bd0020dc84e4c0c6f")
TASK193_V1_CHECKER_PIN = (
    "crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v1.py",
    33149, "278903c62c8f742cb985f44267f5f428c12dac9c514117f91eb6ae0daea17940")
TASK179_CHECKER_PIN = (
    "crosscheck/check_d972_r07_positive_common_word_colgen_v1.py", 73780,
    "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d")
MAX_BYTES = 512 * 1024 * 1024


class CheckStop(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if condition is not True:
        raise CheckStop(message)


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def digest_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("self_digest", None)
    body["self_digest"] = digest(body)
    return body


def check_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest")
    body = dict(value)
    body.pop("self_digest", None)
    need(type(claimed) is str and claimed == digest(body), label + " seal")


def resolve(raw: str | Path) -> Path:
    path = Path(raw)
    resolved = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise CheckStop("path outside workspace") from exc
    return resolved


def read_physical(raw_path: str | Path, limit: int = MAX_BYTES
                  ) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
    path = resolve(raw_path)
    need(not path.is_symlink(), "physical pathname symlink")
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                     getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        raise CheckStop("physical input open") from exc
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
             0 < before.st_size <= limit, "physical input owner")
        raw = bytearray()
        while len(raw) < before.st_size:
            chunk = os.read(fd, min(1 << 20, before.st_size - len(raw)))
            need(bool(chunk), "physical input short read")
            raw.extend(chunk)
        need(not os.read(fd, 1), "physical input long read")
        after = os.fstat(fd)
        need((before.st_dev, before.st_ino, before.st_size, before.st_nlink,
              before.st_mtime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
              after.st_mtime_ns), "physical input changed")
        path_after = os.lstat(path)
        need(not stat.S_ISLNK(path_after.st_mode) and
             (path_after.st_dev, path_after.st_ino, path_after.st_size,
              path_after.st_nlink, path_after.st_mtime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
              after.st_mtime_ns), "physical pathname changed")
        raw_bytes = bytes(raw)
        try:
            value = json.loads(raw_bytes.decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise CheckStop("physical JSON") from exc
        need(type(value) is dict and raw_bytes == canon(value) + b"\n",
             "canonical JSON input")
        return value, raw_bytes, {
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "bytes": len(raw_bytes), "sha256": digest_bytes(raw_bytes),
        }
    finally:
        os.close(fd)


def write_exclusive(raw_path: str | Path, value: Any) -> None:
    path = resolve(raw_path)
    need(not path.exists(), "stale checker output")
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canon(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        view = memoryview(raw)
        while view:
            view = view[os.write(fd, view):]
        os.fsync(fd)
    finally:
        os.close(fd)


def short(identity: dict[str, Any]) -> dict[str, Any]:
    return {k: identity[k] for k in ("path", "bytes", "sha256")}


def legacy_sparse_digest(row: list[list[Any]]) -> str:
    payload = bytearray()
    previous: bytes | None = None
    for item in row:
        need(type(item) is list and len(item) == 2 and
             type(item[0]) is str and type(item[1]) is int and item[1] in (1, 2),
             "adapter sparse row entry")
        key = bytes.fromhex(item[0])
        need(item[0] == key.hex() and (previous is None or previous < key),
             "adapter sparse row order")
        previous = key
        payload.extend(len(key).to_bytes(4, "big")); payload.extend(key)
        payload.append(item[1])
    return digest_bytes(bytes(payload))


def short_pin(pin: tuple[str, int, str]) -> dict[str, Any]:
    return {"path": pin[0], "bytes": pin[1], "sha256": pin[2]}


def adapter_boundary(adapter: dict[str, Any], verdict: dict[str, Any],
                     adapter_id: dict[str, Any], verdict_id: dict[str, Any]
                     ) -> dict[str, Any] | None:
    check_seal(adapter, "adapter")
    check_seal(verdict, "adapter checker verdict")
    need(adapter.get("schema") == ADAPTER_SCHEMA, "adapter schema")
    need(verdict.get("schema") == ADAPTER_CHECK_SCHEMA and
         verdict.get("terminal") == adapter.get("terminal") and
         verdict.get("adapter_receipt") == adapter_id and
         verdict.get("adapter_source", {}).get("producer") == short_pin(ADAPTER_PRODUCER_PIN) and
         verdict.get("adapter_source", {}).get("checker") == short_pin(ADAPTER_CHECKER_PIN),
         "adapter verdict binding")
    if adapter.get("status") == "UNKNOWN":
        need(str(adapter.get("terminal", "")).startswith(UNKNOWN_INPUT + ":") and
             verdict.get("status") == "UNKNOWN" and
             verdict.get("claims") == {"independent_a0_replay": False,
                                        "accepted_abi": False},
             "adapter typed UNKNOWN")
        return None
    need(adapter.get("claims") == {"adapter": "A0_REPLAY_ONLY", "lift": "NONE",
                                   "fake": "NONE", "Ihara": "NONE"} and
         verdict.get("a0_receipt") == adapter.get("a0_receipt") and
         verdict.get("a0_verdict") == adapter.get("a0_verdict") and
         adapter.get("status") == "ACCEPTED" and
         adapter.get("terminal") == ADAPTER_ACCEPTED and
         verdict.get("status") == "ACCEPTED" and
         verdict.get("claims") == {"independent_a0_replay": True,
                                    "accepted_abi": True,
                                    "task193_values": False},
         "adapter accepted terminal")
    need(adapter.get("source_provenance", {}).get("adapter") ==
         short_pin(ADAPTER_PRODUCER_PIN), "adapter producer pin")
    direct = adapter.get("direct_replay")
    need(type(adapter.get("c_exact")) is list and
         type(adapter.get("corrected_word")) is list and
         type(adapter.get("g760")) is list and len(adapter["g760"]) == 760 and
         type(direct) is dict and type(direct.get("row")) is list and
         direct.get("row_sha256") == legacy_sparse_digest(direct["row"]),
         "adapter exact ABI")
    need(direct.get("direct_all_seven_replay") is True and
         direct.get("right_g760_multiplication") is True and
         direct.get("hexagons") is True and
         direct.get("pentagon_printed_order") is True,
         "adapter four replay flags")
    replay = verdict.get("replay", {})
    need(replay.get("c_exact") == adapter.get("c_exact") and
         replay.get("corrected_word") == adapter.get("corrected_word") and
         replay.get("g760") == adapter.get("g760") and
         replay.get("row_sha256") == direct.get("row_sha256") and
         replay.get("direct_replay") == direct.get("replay"),
         "adapter checker replay")
    return {"c_exact": list(adapter["c_exact"]),
            "corrected_word": list(adapter["corrected_word"]),
            "g760": list(adapter["g760"]), "direct_replay": dict(direct),
            "adapter_receipt": short(adapter_id),
            "adapter_verdict": short(verdict_id)}


def minimal_from_boundary(boundary: dict[str, Any]) -> dict[str, Any]:
    direct = boundary["direct_replay"]
    return {"exactification": {"positive_receipt": True,
                               "literal": {"c_exact": boundary["c_exact"]}},
            "exact_direct_replay": {
                "row": direct["row"], "row_sha256": direct["row_sha256"],
                "replay": {"corrected_word": boundary["corrected_word"],
                            "direct_all_seven_replay": True},
                "right_g760_multiplication": True, "hexagons": True,
                "pentagon_printed_order": True}}


def _typed(row: dict[str, Any]) -> dict[str, Any]:
    return dict(sorted((str(k), int(v) % 3) for k, v in row.items()
                       if int(v) % 3))


def _add(a: dict[str, Any], b: dict[str, Any], scale: int = 1) -> dict[str, Any]:
    out = dict(a)
    for key, value in b.items():
        z = (int(out.get(key, 0)) + scale * int(value)) % 3
        if z:
            out[str(key)] = z
        else:
            out.pop(str(key), None)
    return _typed(out)


def _scale(a: dict[str, Any], scale: int) -> dict[str, Any]:
    return _typed({key: scale * int(value) for key, value in a.items()})


def _transitions(transitions: list[Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    fox: dict[str, int] = {}; endpoint: dict[str, int] = {}
    for item in transitions:
        x, before, after = int(item[0]), int(item[1]), int(item[2])
        key = str((abs(x), before if x > 0 else after))
        fox[key] = (fox.get(key, 0) + (1 if x > 0 else -1)) % 3
        endpoint[str(after)] = (endpoint.get(str(after), 0) + 1) % 3
        endpoint[str(before)] = (endpoint.get(str(before), 0) - 1) % 3
    return _typed(fox), _typed(endpoint)


def _chain_map(raw: list[Any]) -> dict[bytes, int]:
    return {bytes.fromhex(str(k)): int(v) % 3 for k, v in raw}


def pointed_replay(r: dict[str, Any], rt: dict[str, Any], c: Any, mod: Any,
                   spaces: dict[int, Any], eq: dict[str, Any], roster: dict[str, Any],
                   correlation: Any, pair: Any, dcursor: int, qcursor: int) -> None:
    package = r.get("pointed_rows")
    need(type(package) is dict and package.get("schema") ==
         "d972-r07-task193-pointed-row-package/v1" and
         package.get("status") == "ACCEPTED" and
         package.get("scope") == "full_fox_cokernel" and
         package.get("block_order") == ["H1", "H2", "P"] and
         package.get("H1_H2_separate") is True and
         package.get("d1_pt_cycle_required") is False,
         "pointed package envelope")
    records = package.get("blocks")
    need(type(records) is list and len(records) == 3 and
         [x.get("name") for x in records] == ["H1", "H2", "P"] and
         [x.get("block") for x in records] == [1, 2, 3],
         "pointed block roster")

    class IndependentPair:
        def __init__(self, quotient: Any, block: int, base: Any,
                     chain: dict[bytes, int]):
            self.q = quotient; self.block = block; self.base = base
            self.chain = dict(chain)
        def blob(self, value: Any) -> bytes:
            return c.element_blob(value)
        def unpack(self, key: bytes) -> Any:
            return mod.parse_element(key, self.block)
        def mul(self, other: Any) -> Any:
            moved = {mod.row_key(self.block, key[2],
                                 self.blob(self.q.mul(self.base,
                                     self.unpack(key[5:])))): value
                     for key, value in other.chain.items()}
            return IndependentPair(self.q, self.block,
                                   self.q.mul(self.base, other.base),
                                   _add(self.chain, moved))
        def inv(self) -> Any:
            base = self.q.inverse(self.base)
            moved = {mod.row_key(self.block, key[2],
                                 self.blob(self.q.mul(base,
                                     self.unpack(key[5:])))): (-value) % 3
                     for key, value in self.chain.items()}
            return IndependentPair(self.q, self.block, base, moved)

    def pair_public(item: Any, block: int, label: int) -> None:
        need(0 <= label < len(roster[str(block)]), "pointed affine label")
        expected = roster[str(block)][label]
        diff = _add(item.chain, _chain_map(expected["chain"]), -1)
        rem, _ = spaces[block].reduce(diff)
        if rem:
            dual = spaces[block].dual(rem)
            corr = correlation(dual, block)
            need(pair(dual, diff) != 0 and corr.get("zero") is True,
                 "pointed affine representative separation")
        need(item.blob(item.base).hex() == expected["base"],
             "pointed affine base")

    def replay_item(item: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        external = int(item["block"]); internal = 1 if external in (1, 2) else 3
        quotient = rt["e3"] if external in (1, 2) else rt["e4"]
        gens = [IndependentPair(quotient, internal, quotient.eval([i]),
                                {mod.row_key(internal, i,
                                             c.element_blob(quotient.identity)): 1})
                for i in range(1, 4 if external in (1, 2) else 7)]
        current = IndependentPair(quotient, internal, quotient.identity, {})
        transitions = item.get("prefix_transitions")
        need(type(transitions) is list and transitions and
             [int(x[0]) for x in transitions] == item.get("word"),
             "pointed signed-word replay")
        for transition in transitions:
            need(type(transition) is list and len(transition) == 5,
                 "pointed transition shape")
            x, before, after = int(transition[0]), int(transition[1]), int(transition[2])
            pair_public(current, internal, before)
            current = current.mul(gens[abs(x) - 1] if x > 0
                                  else gens[abs(x) - 1].inv())
            pair_public(current, internal, after)
        need(current.blob(current.base).hex() == item.get("terminal_base"),
             "pointed terminal base")
        need(item.get("terminal_is_identity") is (current.base == quotient.identity),
             "pointed terminal identity flag")
        if item.get("require_identity") is True:
            need(current.base == quotient.identity, "unexpected pointed identity gate")
        return _transitions(transitions)

    base_g760 = list(rt["obj"]["g760"])
    base_hex = c.hexagon_words(base_g760)
    base_words = [list(c.embed_pb3(base_hex[0])),
                  list(c.embed_pb3(base_hex[1]))]
    contexts = c.pentagon_context_words()
    base_factors = [c.f2_substitute(base_g760, left, right)
                    for left, right in contexts]
    base_words.append(list(c.paper_product(
        base_factors[1], base_factors[3], base_factors[0],
        c.inverse(base_factors[2]), c.inverse(base_factors[4]))))
    need([item.get("word") for item in records] == base_words,
         "pointed g760 hexagon/pentagon word order")

    beta = r.get("beta1", {})
    for item, beta_name in zip(records, ("beta1_H1", "beta1_H2", "beta1_P")):
        raw, endpoint = replay_item(item)
        need(item["D1_g760"]["row"] == raw and
             item["D1_g760"]["row_sha256"] == digest(raw) and
             item["D1_g760_endpoint"] == endpoint,
             "pointed base Fox row")
        beta_item = beta.get(beta_name)
        need(type(beta_item) is dict and
             _typed(beta_item.get("fox_row", {})) == item["beta1"]["row"] and
             _typed(beta_item.get("d1", {})) == item["D1_beta1_endpoint"],
             "pointed corrected Fox row")
        d1_pt = _scale(raw, -1)
        b1a = _add(item["beta1"]["row"], raw, -1)
        e1_pt = _add(d1_pt, b1a, -1)
        e1_aug = _add(b1a, d1_pt, -1)
        for field, value in (("d1_pt", d1_pt), ("B1a", b1a),
                             ("e1_pt", e1_pt), ("e1_aug", e1_aug)):
            need(item[field]["row"] == value and
                 item[field]["row_sha256"] == digest(value),
                 "pointed derived row:" + field)
        need(item["sign_equalities"] == {
            "e1_pt_eq_neg_beta1": e1_pt == _scale(item["beta1"]["row"], -1),
            "e1_aug_eq_beta1": e1_aug == item["beta1"]["row"],
            "e1_aug_eq_neg_e1_pt": e1_aug == _scale(e1_pt, -1)},
             "pointed sign equalities")
        ep = item["endpoint_replay"]
        need(ep.get("D1_d1_pt") == _scale(endpoint, -1) and
             ep.get("one_minus_R_g760") == _scale(endpoint, -1) and
             ep.get("D1_beta1") == item["D1_beta1_endpoint"] and
             ep.get("R_f_minus_one") == item["D1_beta1_endpoint"] and
             ep.get("D1_e1_pt") == _scale(item["D1_beta1_endpoint"], -1) and
             ep.get("one_minus_R_f") == _scale(item["D1_beta1_endpoint"], -1) and
             ep.get("equalities") == {
                 "D1_d1_pt_eq_one_minus_R_g760": True,
                 "D1_beta1_eq_R_f_minus_one": True,
                 "D1_e1_pt_eq_one_minus_R_f": True},
             "pointed endpoint identities")
    for field in ("d1_pt", "beta1", "B1a", "e1_pt", "e1_aug"):
        need(package.get(field) == {item["name"]: item[field] for item in records},
             "pointed aggregate:" + field)

    # The base-prefix evaluator runs after the v1 maps.  Extend, rather than
    # replace, the already replayed decision/query chronology for that tail.
    decisions = r["affine_labels"]["decisions"]
    seen = {"1": [], "3": []}
    for decision in decisions[:dcursor]:
        block = str(decision.get("block")); candidate = int(decision.get("candidate"))
        proof = decision.get("proof", {}); base = str(decision.get("base_hex"))
        if proof.get("new") is True:
            need(candidate == len(seen[block]), "pointed prior label chronology")
            seen[block].append(base)
        else:
            need(0 <= candidate < len(seen[block]) and seen[block][candidate] == base,
                 "pointed prior merge chronology")
    dcur, qcur = dcursor, qcursor
    for item in records:
        block = str(1 if int(item["block"]) in (1, 2) else 3)
        for transition in item["prefix_transitions"]:
            for label in transition[1:3]:
                need(dcur < len(decisions), "pointed missing label decision")
                decision = decisions[dcur]; dcur += 1
                need(str(decision.get("block")) == block and
                     int(decision.get("candidate")) == int(label),
                     "pointed label decision order")
                base = str(decision.get("base_hex")); proof = decision.get("proof", {})
                same = [i for i, value in enumerate(seen[block]) if value == base]
                if same:
                    need(same[0] == int(label) and proof.get("new") is not True,
                         "pointed canonical merge")
                    need(qcur < len(eq["transcript"]), "pointed missing equality query")
                    query = eq["transcript"][qcur]; qcur += 1
                    got = query.get("result", {})
                    need(all(got.get(k) == proof.get(k)
                             for k in ("equal", "chain", "dual", "correlation",
                                       "pairing", "full_zero_correlation")
                             if k in got or k in proof),
                         "pointed query proof binding")
                else:
                    need(int(label) == len(seen[block]) and proof.get("new") is True,
                         "pointed first encounter")
                    seen[block].append(base)
    need(dcur == len(decisions) and qcur == len(eq["transcript"]),
         "complete pointed label/query chronology")
    need(seen == {key: [str(x.get("base")) for x in value]
                  for key, value in roster.items()}, "pointed final label roster")


def _minimal_for_shim(result: dict[str, Any]) -> dict[str, Any]:
    return result["adapter_input"]


def _pointed_hook(r: dict[str, Any], rt: dict[str, Any], c: Any, mod: Any,
                  spaces: dict[int, Any], eq: dict[str, Any], roster: dict[str, Any],
                  correlation: Any, pair: Any, parse_sparse: Any,
                  public_sparse: Any, dcursor: int, qcursor: int) -> None:
    pointed_replay(r, rt, c, mod, spaces, eq, roster, correlation, pair,
                   dcursor, qcursor)


def load_v1_checker() -> types.ModuleType:
    path = ROOT / TASK193_V1_CHECKER_PIN[0]
    raw = path.read_bytes()
    need(len(raw) == TASK193_V1_CHECKER_PIN[1] and
         digest_bytes(raw) == TASK193_V1_CHECKER_PIN[2], "task193 v1 checker pin")
    old = (b'    art=r.get("task186_artifact",{}); path=Path(str(art.get("path",""))); path=path if path.is_absolute() else ROOT/path\n'
           b'    raw=path.read_bytes(); require(len(raw)==art.get("bytes") and hashlib.sha256(raw).hexdigest()==art.get("sha256"),"task186 artifact identity")\n'
           b'    t=json.loads(raw.decode("utf-8")); tb=dict(t); tc=tb.pop("self_digest",None)\n'
           b'    require(tc==digest(tb) and t.get("schema")==TASK186_SCHEMA and t.get("status")=="COMMON_WORD" and\n'
           b'            t.get("terminal")=="R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD" and\n'
           b'            art.get("checker_terminal")==TASK186_LINE,"task186 attested envelope")\n'
           b'    auth(ROOT/TASK186_CHECKER[0],TASK186_CHECKER)\n'
           b'    tspec=importlib.util.spec_from_file_location("task186_independent_checker",ROOT/TASK186_CHECKER[0]); require(tspec and tspec.loader,"task186 checker loader")\n'
           b'    tmod=importlib.util.module_from_spec(tspec); tspec.loader.exec_module(tmod)\n'
           b'    require(tmod.full_independent_production(t,path)==TASK186_LINE,"task186 independent replay")\n'
           b'    exact=t.get("exact_direct_replay",{}).get("replay",{}).get("corrected_word")\n'
           b'    require(type(exact) is list and exact and r.get("corrected_word")==exact and t.get("exactification",{}).get("positive_receipt") is True,"task186 exact word")\n'
           b'    td=t.get("exact_direct_replay",{}); rd=r.get("task186_direct_replay",{}); require(rd.get("corrected_word")==exact and rd.get("row")==td.get("row") and rd.get("row_sha256")==td.get("row_sha256") and rd.get("all_seven") is True,"task186 direct row binding")\n')
    new = (b'    minimal=__task193_v2_minimal_for_shim(r)\n'
           b'    exact=minimal["exactification"]["literal"]["c_exact"]\n'
           b'    require(type(exact) is list and exact and r.get("corrected_word")==exact,"adapter exact word")\n'
           b'    td=minimal["exact_direct_replay"]; rd=r.get("task193_direct_replay",{})\n'
           b'    require(rd.get("corrected_word")==exact and rd.get("row")==td.get("row") and rd.get("row_sha256")==td.get("row_sha256") and rd.get("all_seven") is True,"adapter direct row binding")\n')
    need(raw.count(old) == 1, "task193 v1 checker adapter hook cardinality")
    patched = raw.replace(old, new)
    for old_ref, new_ref in (
        (b'r.get("task186_direct_replay",{})', b'r.get("task193_direct_replay",{})'),
        (b'r.get("task186_direct_row_bound")', b'r.get("task193_direct_row_bound")'),
        (b'dr.get("task186_row")', b'dr.get("adapter_row")'),
        (b'tmod.sparse_digest', b'__task193_v2_sparse_digest')):
        need(patched.count(old_ref) == 1, "task193 v1 checker reference cardinality")
        patched = patched.replace(old_ref, new_ref)
    chronology = b'    require(dcursor==len(decisions) and qcursor==len(eq["transcript"]),"complete label/query chronology")\n'
    hook = (b'    __task193_v2_pointed_hook(r, rt, c, mod, spaces, eq, roster, correlation, pair, parse_sparse, public_sparse, dcursor, qcursor)\n')
    need(patched.count(chronology) == 1, "task193 v1 checker chronology cardinality")
    patched = patched.replace(chronology, hook)
    module = types.ModuleType("d972_r07_task193_v1_checker_for_v2")
    module.__file__ = str(path)
    module.__dict__["__task193_v2_minimal_for_shim"] = _minimal_for_shim
    module.__dict__["__task193_v2_sparse_digest"] = legacy_sparse_digest
    module.__dict__["__task193_v2_pointed_hook"] = _pointed_hook
    exec(compile(patched, str(path), "exec"), module.__dict__, module.__dict__)
    return module


def load_task179_checker() -> types.ModuleType:
    path = ROOT / TASK179_CHECKER_PIN[0]
    raw = path.read_bytes()
    need(len(raw) == TASK179_CHECKER_PIN[1] and
         digest_bytes(raw) == TASK179_CHECKER_PIN[2], "task179 checker pin")
    spec = importlib.util.spec_from_file_location(
        "d972_r07_task179_checker_for_task193_v2", path)
    need(spec is not None and spec.loader is not None, "task179 checker loader")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def check_result(result: dict[str, Any], boundary: dict[str, Any],
                 adapter_id: dict[str, Any], verdict_id: dict[str, Any]) -> None:
    check_seal(result, "task193 result")
    need(result.get("schema") == SCHEMA and result.get("status") == "PASS" and
         result.get("terminal") == COMMON and
         result.get("adapter_artifact") == {"adapter_receipt": short(adapter_id),
                                             "adapter_verdict": short(verdict_id)} and
         result.get("literal_binding") == boundary["c_exact"] and
         result.get("correction_word") == boundary["c_exact"] and
         result.get("corrected_word") == boundary["corrected_word"] and
         result.get("g760") == boundary["g760"], "task193 result envelope")
    need(result.get("adapter_input") == minimal_from_boundary(boundary),
         "task193 minimal adapter input")
    direct = result.get("task193_direct_replay", {})
    need(direct.get("row") == boundary["direct_replay"]["row"] and
         direct.get("row_sha256") == boundary["direct_replay"]["row_sha256"] and
         direct.get("right_g760_multiplication") is True and
         direct.get("hexagons") is True and
         direct.get("pentagon_printed_order") is True and
         direct.get("all_seven") is True, "task193 direct boundary")
    need(result.get("task193_direct_row_bound") == direct.get("row") and
         result.get("claims") == {"task193_actual": True, "d1_pt": True,
                                   "beta1": True, "lift": "NONE",
                                   "fake": "NONE", "Ihara": "NONE"},
         "task193 claims")
    pointed = result.get("pointed_rows")
    need(type(pointed) is dict and
         result.get("d1_pt") == pointed.get("d1_pt") and
         result.get("e1_pt") == pointed.get("e1_pt") and
         result.get("e1_aug") == pointed.get("e1_aug") and
         result.get("B1a") == pointed.get("B1a") and
         result.get("beta1_vector") == {
             name: pointed.get("beta1", {}).get(name, {}).get("row")
             for name in pointed.get("block_order", [])} and
         result.get("sign_equalities") == pointed.get("sign_equalities") and
         result.get("endpoint_replay") == pointed.get("endpoint_replay"),
         "pointed top-level binding")
    need("task186_artifact" not in result and
         "task186_direct_replay" not in result and
         "task186_checker" not in str(result.get("source_provenance", {})),
         "legacy input claims absent")


def check_unknown_result(result: dict[str, Any]) -> None:
    check_seal(result, "task193 result")
    need(result.get("schema") == SCHEMA and
         result.get("status") in (UNKNOWN_INPUT, UNKNOWN_RESOURCE) and
         str(result.get("terminal", "")).startswith(str(result.get("status")) + ":"),
         "typed task193 terminal")
    claims = result.get("claims", {})
    need(claims.get("task193_actual") is False and claims.get("d1_pt") is False and
         claims.get("beta1") is False and claims.get("lift") == "NONE" and
         claims.get("fake") == "NONE" and claims.get("Ihara") == "NONE",
         "typed task193 unknown claims")
    need("task186_artifact" not in result and
         "task186_direct_replay" not in result, "unknown legacy fields absent")
    if result.get("status") == UNKNOWN_RESOURCE:
        cp = result.get("checkpoint")
        need(type(cp) is dict and cp.get("resumable") is True and
             type(cp.get("self_digest")) is str and
             cp["self_digest"] == digest({k: v for k, v in cp.items()
                                           if k != "self_digest"}),
             "task193 resource checkpoint")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter-receipt", required=True)
    ap.add_argument("--adapter-verdict", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args(argv)
    try:
        adapter, _ar, adapter_id = read_physical(args.adapter_receipt)
        verdict, _vr, verdict_id = read_physical(args.adapter_verdict)
        boundary = adapter_boundary(adapter, verdict, adapter_id, verdict_id)
        result, _rr, _result_id = read_physical(args.receipt)
        if result.get("status") in (UNKNOWN_INPUT, UNKNOWN_RESOURCE):
            check_unknown_result(result)
            if boundary is None:
                need(result.get("terminal") == UNKNOWN_INPUT + ":adapter:" +
                     str(adapter.get("terminal")), "adapter unknown propagation")
        else:
            need(boundary is not None, "accepted result requires adapter")
            check_result(result, boundary, adapter_id, verdict_id)
            shim = dict(result)
            shim["schema"] = "d972-r07-second-frattini-affine-prefix-compiler/v1"
            shim["terminal"] = "R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1"
            shim["status"] = "PASS"
            # The patched v1 checker sees only this in-memory compatibility
            # view; the physical result remains the dedicated v2 schema.
            checker = load_v1_checker()
            checker.independent_production(shim)
        result_is_accepted = result.get("status") == "PASS"
        out = seal({"schema": SCHEMA + "/checker-verdict/v2",
                    "status": result.get("status"),
                    "terminal": result.get("terminal"),
                    "receipt": {"path": str(resolve(args.receipt).relative_to(ROOT)).replace("\\", "/"),
                                "bytes": _result_id["bytes"], "sha256": _result_id["sha256"]},
                    "adapter_receipt": adapter_id,
                    "adapter_verdict": verdict_id,
                    "claims": {"independent_adapter_authentication": boundary is not None,
                               "independent_task193_replay": result_is_accepted,
                               "pointed_rows": result_is_accepted}})
        write_exclusive(args.output, out)
        print("R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2_CHECKER_PASS terminal=" +
              str(result.get("terminal")), flush=True)
        return 0
    except (CheckStop, OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print("R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2_CHECKER_ERROR " +
              str(exc), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
