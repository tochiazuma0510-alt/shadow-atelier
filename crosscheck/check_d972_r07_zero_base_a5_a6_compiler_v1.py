#!/usr/bin/env python3
"""Helper-nonshared checker for the zero-base A5/A6 production receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-zero-base-a5-a6-compiler/v1"
MANIFEST_SCHEMA = SCHEMA + "/actual-input-manifest"
MEMBER = "R07_ZERO_BASE_A5_A6_MEMBER"
NONMEMBER = "R07_ZERO_BASE_A5_A6_NONMEMBER"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
MOD = 3
ROLES = ("a3_zero", "task198", "a4", "a0", "task193_actual")


class CheckStop(RuntimeError):
    pass


def need(ok: bool, reason: str) -> None:
    if ok is not True:
        raise CheckStop(reason)


def packed(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha(value: object) -> str:
    return hashlib.sha256(packed(value)).hexdigest()


def f3(value: int) -> int:
    need(type(value) is int, "F3 coefficient")
    return value % MOD


def sparse(value: object) -> dict[str, int]:
    need(isinstance(value, dict), "sparse vector")
    return dict(sorted((str(k), f3(v)) for k, v in value.items() if f3(v)))


def plus(left: dict[str, int], right: dict[str, int], scalar: int = 1):
    out = dict(left)
    for key, value in right.items():
        value2 = f3(out.get(key, 0) + scalar * value)
        if value2:
            out[key] = value2
        else:
            out.pop(key, None)
    return dict(sorted(out.items()))


def scale(value: dict[str, int], scalar: int):
    return sparse({key: scalar * n for key, n in value.items()})


def flatten(z: dict[str, int], eta: dict[str, int]):
    return {**{"z:" + k: v for k, v in z.items()},
            **{"eta:" + k: v for k, v in eta.items()}}


def remap(value: dict[str, int], mapping: dict[str, str]):
    out = {}
    for key, coefficient in value.items():
        target = mapping.get(key, key)
        out[target] = f3(out.get(target, 0) + coefficient)
    return sparse(out)


class ReverseEchelon:
    """Different pivot direction from the producer, with raw-row transforms."""

    def __init__(self):
        self.rows = {}

    def reduce(self, row, transform):
        work, tr = sparse(row), sparse(transform)
        for pivot in sorted(self.rows, reverse=True):
            coefficient = work.get(pivot, 0)
            if coefficient:
                old = self.rows[pivot]
                work = plus(work, old["row"], -coefficient)
                tr = plus(tr, old["transform"], -coefficient)
        return work, tr

    def insert(self, row, label):
        remainder, transform = self.reduce(row, {label: 1})
        if not remainder:
            return "DEPENDENT"
        pivot = sorted(remainder, reverse=True)[0]
        inverse = 1 if remainder[pivot] == 1 else 2
        self.rows[pivot] = {"row": scale(remainder, inverse),
                            "transform": scale(transform, inverse)}
        return "ACCEPTED"


def path_for(value):
    need(isinstance(value, str) and value, "member path")
    path = Path(value)
    need(not path.is_absolute() and ".." not in path.parts and
         value.replace("\\", "/") == path.as_posix(), "member path")
    candidate = ROOT / path
    need(not candidate.is_symlink(), "member link")
    target = candidate.resolve()
    need(str(target).startswith(str(ROOT.resolve()) + os.sep), "member containment")
    need(target.is_file() and not target.is_symlink(), "member file")
    return target


def read_descriptor(value):
    need(isinstance(value, dict) and isinstance(value.get("path"), str),
         "member descriptor")
    target = path_for(value["path"])
    raw = target.read_bytes()
    need(value.get("bytes") == len(raw), "member byte count")
    need(value.get("sha256") == hashlib.sha256(raw).hexdigest(), "member SHA")
    try:
        obj = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CheckStop("member JSON") from exc
    need(isinstance(obj, dict), "member object")
    claimed = obj.get("self_digest_sha256")
    if claimed is not None:
        body = dict(obj)
        body.pop("self_digest_sha256", None)
        need(claimed == sha(body), "upstream self seal")
    return obj


def role_descriptor(role, name):
    need(isinstance(role, dict), name + " role")
    value = role.get("receipt", role.get("producer", role.get("file")))
    need(isinstance(value, dict), name + " receipt descriptor")
    return value


def checker_descriptor(role, name):
    need(isinstance(role, dict), name + " role")
    value = role.get("verdict", role.get("checker"))
    need(isinstance(value, dict), name + " checker descriptor")
    return value


def empty(value):
    return value in ({}, [], None)


def load_bundle(manifest_path):
    raw = Path(manifest_path).read_bytes()
    manifest = json.loads(raw)
    need(manifest.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    members = manifest.get("members")
    need(isinstance(members, dict), "manifest members")
    for name in ROLES:
        need(name in members, "missing owner:" + name)
    objects = {name: read_descriptor(role_descriptor(members[name], name))
               for name in ROLES}
    verdicts = {name: read_descriptor(checker_descriptor(members[name], name))
                for name in ROLES}
    for name in ROLES:
        need(isinstance(verdicts[name].get("terminal"), str),
             name + " checker terminal")
    a3 = objects["a3_zero"]
    result = a3.get("result", a3)
    need(a3.get("terminal") == "R07_PRE_A0_A3_PROJECTED_MEMBER" or
         result.get("terminal") == "R07_PRE_A0_A3_PROJECTED_MEMBER",
         "A3 zero terminal")
    need(empty(result.get("target")) and empty(result.get("lambda")) and
         empty(result.get("kappa0")), "A3 nonzero base")
    common = manifest.get("common_identity")
    need(isinstance(common, dict) and common, "common identity")
    return {"objects": objects, "verdicts": verdicts,
            "manifest_sha256": hashlib.sha256(raw).hexdigest()}


def field(obj, *keys):
    value = obj
    for key in keys:
        need(isinstance(value, dict) and key in value,
             "missing field:" + ".".join(keys))
        value = value[key]
    return value


def state(bundle):
    objects = bundle["objects"]
    runtime = field(objects["task198"], "evaluator", "zero_base")
    d1, w, cmap = sparse(field(runtime, "d1")), sparse(field(runtime, "w")), field(runtime, "C")
    actions = field(runtime, "marked_actions")
    need(isinstance(cmap, dict) and isinstance(actions, list) and actions,
         "task198 runtime")
    for action in actions:
        need(isinstance(action, dict) and isinstance(action.get("name"), str), "marked action")
        need(isinstance(action.get("z"), dict) and isinstance(action.get("eta"), dict),
             "marked action map")
    roster = field(objects["a4"], "kernel", "K_roster")
    need(isinstance(roster, list) and roster, "A4 K roster")
    for item in roster:
        need(isinstance(item, dict) and isinstance(item.get("word"), list), "A4 word")
        seed = item.get("seed")
        need(isinstance(seed, dict) and isinstance(seed.get("z"), dict) and
             isinstance(seed.get("eta"), dict), "A4 zero-base seed")
    task193 = objects["task193_actual"]
    task193_result = task193.get("result", task193)
    beta = task193_result.get("beta1_vector")
    if beta is None:
        beta_blob = task193_result.get("beta1")
        beta = beta_blob.get("vector") if isinstance(beta_blob, dict) else beta_blob
    need(isinstance(beta, dict), "task193 beta1 vector")
    a0_result = objects["a0"].get("result", objects["a0"])
    correction_word = a0_result.get("correction_word")
    need(isinstance(correction_word, list), "A0 literal correction word")
    need(task193_result.get("literal_binding", task193_result.get("correction_word")) ==
         correction_word, "task193 A0 word binding")
    exact_target = objects["task193_actual"].get("eta_c")
    if exact_target is None:
        exact_target = objects["task193_actual"].get("result", {}).get("eta_c")
    exact_bound = isinstance(exact_target, dict) and all(
        isinstance(action.get("exact"), dict) for action in actions) and all(
        isinstance(item.get("seed", {}).get("exact"), dict) for item in roster)
    return {"d1": d1, "w": w, "C": cmap, "actions": actions,
            "roster": roster, "e1": scale(sparse(beta), -1),
            "exact_target": sparse(exact_target) if exact_bound else None,
            "exact_bound": exact_bound}


def apply_c(eta, cmap):
    out = {}
    for key, coefficient in eta.items():
        images = cmap.get(key, [])
        need(isinstance(images, list), "C coordinate image")
        for target, scalar in images:
            out[str(target)] = f3(out.get(str(target), 0) + coefficient * scalar)
    return sparse(out)


def replay(bundle):
    s = state(bundle)
    pre, joint, augmented = ReverseEchelon(), ReverseEchelon(), ReverseEchelon()
    rows, queue = [], []
    a5_hit = None
    augmented_target = None
    if s["exact_bound"]:
        augmented_target = {"z:" + key: value for key, value in s["e1"].items()}
        augmented_target.update({"exact:" + key: value
                                 for key, value in s["exact_target"].items()})
    target = {"z:" + key: value for key, value in s["e1"].items()}

    def accept(z, eta, parent, action, terms, exact):
        label = "row:" + str(len(rows))
        decision = pre.insert(flatten(z, eta), label)
        row = {"id": label, "z": z, "eta": eta, "exact": exact, "terms": terms,
               "parent": parent, "action": action, "pre_decision": decision}
        rows.append(row)
        if decision == "ACCEPTED":
            queue.append(len(rows) - 1)
            row["joint_decision"] = joint.insert(
                flatten(z, apply_c(eta, s["C"])), label)
            if s["exact_bound"]:
                row["augmented_decision"] = augmented.insert(
                    {**flatten(z, apply_c(eta, s["C"])),
                     **{"exact:" + k: v for k, v in exact.items()}}, label)
        return decision

    for index, item in enumerate(s["roster"]):
        seed = item["seed"]
        item_exact = sparse(seed.get("exact", {})) if s["exact_bound"] else {}
        accept(sparse(seed["z"]), sparse(seed["eta"]), None, "seed",
               [{"coefficient": 1, "prefix": [], "kernel_index": index}],
               item_exact)
    remainder, coefficients = joint.reduce(target, {})
    if not remainder:
        a5_hit = coefficients
    if augmented_target is not None:
        aug_rem, aug_coefficients = augmented.reduce(augmented_target, {})
        if not aug_rem:
            return MEMBER, cursor if 'cursor' in locals() else 0, aug_coefficients, rows
    cursor = 0
    while cursor < len(queue):
        parent_index = queue[cursor]
        cursor += 1
        parent = rows[parent_index]
        for action in s["actions"]:
            terms = []
            for term in parent["terms"]:
                prefix = list(term["prefix"])
                if action.get("prefix_letter") is not None:
                    prefix.append(int(action["prefix_letter"]))
                terms.append({"coefficient": term["coefficient"],
                              "prefix": prefix,
                              "kernel_index": term["kernel_index"]})
            action_exact = remap(parent.get("exact", {}), action.get("exact", {})) if s["exact_bound"] else {}
            decision = accept(remap(parent["z"], action["z"]),
                              remap(parent["eta"], action["eta"]),
                              parent_index, action["name"], terms, action_exact)
            if decision != "ACCEPTED":
                continue
            remainder, coefficients = joint.reduce(target, {})
            if not remainder:
                a5_hit = coefficients
            if augmented_target is not None:
                aug_rem, aug_coefficients = augmented.reduce(augmented_target, {})
                if not aug_rem:
                    return MEMBER, cursor, aug_coefficients, rows
    if a5_hit is not None:
        return MEMBER, len(queue), a5_hit, rows
    return NONMEMBER, len(rows), {}, rows


def output(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(packed(value) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    terminal, accepted, reason = UNKNOWN_INPUT + ":uninitialized", "REJECTED", "uninitialized"
    try:
        receipt = json.loads(Path(args.receipt).read_bytes())
        claimed = receipt.get("self_digest_sha256")
        body = dict(receipt)
        body.pop("self_digest_sha256", None)
        need(claimed == sha(body), "producer seal")
        bundle = load_bundle(args.manifest)
        terminal2, _, _, _ = replay(bundle)
        terminal = receipt.get("terminal")
        need(terminal == terminal2, "terminal/replay mismatch")
        accepted = "ACCEPTED"
        reason = "independent replay"
    except (CheckStop, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError, UnicodeError) as exc:
        terminal = UNKNOWN_INPUT + ":" + str(exc).replace("\n", " ")
        accepted, reason = "REJECTED", str(exc)
    verdict = {"schema": SCHEMA + "/checker-verdict/v1", "status": accepted,
               "terminal": terminal, "independent": "HELPER_NONSHARED",
               "receipt_sha256": hashlib.sha256(Path(args.receipt).read_bytes()).hexdigest(),
               "reason": reason,
               "claims": {"A5": "NONE", "A6": "NONE", "lift": "NONE",
                          "fake": "NONE", "Ihara": "NONE"}}
    verdict["self_digest_sha256"] = sha(verdict)
    output(args.output, verdict)
    print("R07_ZERO_BASE_A5_A6_CHECKER_TERMINAL " + terminal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
