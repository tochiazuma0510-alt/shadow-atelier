#!/usr/bin/env python3
"""R07 zero-base A5/A6 production compiler.

This file has no SELFTEST path.  It is deliberately an adapter: absent or
unaccepted upstream owners produce a sealed UNKNOWN_INPUT, never a guessed
MEMBER result.  The streaming membership order is v348: full pre-C closure,
then T(a,b)=(a,Cb), with early MEMBER and exhaustion-only NONMEMBER.
"""
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
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
MOD = 3
REQUIRED_ROLES = ("a3_zero", "task198", "a4", "a0", "task193_actual")
CLAIMS = {"A5": "NONE", "A6": "NONE", "lift": "NONE",
          "fake": "NONE", "Ihara": "NONE"}


class Stop(RuntimeError):
    pass


class ResourceStop(Stop):
    def __init__(self, phase: str, cap: str, value: int, limit: int):
        super().__init__(phase)
        self.phase, self.cap, self.value, self.limit = phase, cap, value, limit


def require(ok: bool, message: str) -> None:
    if ok is not True:
        raise Stop(message)


def canon(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(value: object) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def f3(value: int) -> int:
    require(type(value) is int, "F3 coefficient")
    return value % MOD


def vec(value: object) -> dict[str, int]:
    require(isinstance(value, dict), "sparse vector")
    out = {}
    for key, value0 in value.items():
        value1 = f3(value0)
        if value1:
            out[str(key)] = value1
    return dict(sorted(out.items()))


def add(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    out = dict(left)
    for key, value in right.items():
        n = f3(out.get(key, 0) + scale * value)
        if n:
            out[key] = n
        else:
            out.pop(key, None)
    return dict(sorted(out.items()))


def mul_scalar(value: dict[str, int], scalar: int) -> dict[str, int]:
    return vec({key: scalar * n for key, n in value.items()})


def flat(z: dict[str, int], eta: dict[str, int]) -> dict[str, int]:
    return {**{"z:" + key: value for key, value in z.items()},
            **{"eta:" + key: value for key, value in eta.items()}}


def flat_aug(z: dict[str, int], eta: dict[str, int], exact: dict[str, int]) -> dict[str, int]:
    return {**{"z:" + key: value for key, value in z.items()},
            **{"eta:" + key: value for key, value in eta.items()},
            **{"exact:" + key: value for key, value in exact.items()}}


def image(value: dict[str, int], mapping: dict[str, str]) -> dict[str, int]:
    out = {}
    for key, coefficient in value.items():
        target = mapping.get(key, key)
        out[target] = f3(out.get(target, 0) + coefficient)
    return vec(out)


class Echelon:
    """One-pass sparse F3 echelon; each pivot owns a raw-row transform."""

    def __init__(self) -> None:
        self.rows: dict[str, dict] = {}

    def reduce(self, row: dict[str, int], transform: dict[str, int]):
        work, tr = vec(row), vec(transform)
        for pivot in sorted(self.rows):
            coefficient = work.get(pivot, 0)
            if coefficient:
                stored = self.rows[pivot]
                work = add(work, stored["row"], -coefficient)
                tr = add(tr, stored["transform"], -coefficient)
        return work, tr

    def insert(self, row: dict[str, int], label: str):
        transform = {label: 1}
        remainder, representation = self.reduce(row, transform)
        if not remainder:
            return {"accepted": "DEPENDENT", "remainder": remainder,
                    "transform": representation}
        pivot = sorted(remainder)[0]
        inverse = 1 if remainder[pivot] == 1 else 2
        normalized = mul_scalar(remainder, inverse)
        normalized_transform = mul_scalar(representation, inverse)
        self.rows[pivot] = {"row": normalized, "transform": normalized_transform}
        return {"accepted": "ACCEPTED", "remainder": normalized,
                "transform": normalized_transform, "pivot": pivot}


def safe_path(raw: object) -> Path:
    require(type(raw) is str and raw and "\x00" not in raw, "manifest member path")
    path = Path(raw)
    require(not path.is_absolute() and ".." not in path.parts and
            raw.replace("\\", "/") == path.as_posix(), "manifest member path")
    candidate = ROOT / path
    require(not candidate.is_symlink(), "manifest member link")
    target = candidate.resolve()
    require(str(target).startswith(str(ROOT.resolve()) + os.sep),
            "manifest member containment")
    require(target.is_file() and not target.is_symlink(), "manifest member file")
    return target


def member_bytes(descriptor: object) -> tuple[bytes, dict]:
    require(isinstance(descriptor, dict), "member descriptor")
    path = safe_path(descriptor.get("path"))
    raw = path.read_bytes()
    require(descriptor.get("bytes") == len(raw), "member byte count")
    require(descriptor.get("sha256") == hashlib.sha256(raw).hexdigest(),
            "member SHA")
    return raw, descriptor


def json_member(descriptor: object) -> dict:
    raw, _ = member_bytes(descriptor)
    try:
        value = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise Stop("member JSON") from exc
    require(isinstance(value, dict), "member object")
    return value


def descriptor(role: object, name: str) -> dict:
    require(isinstance(role, dict), name + " role")
    candidate = role.get("receipt", role.get("producer", role.get("file")))
    require(isinstance(candidate, dict), name + " receipt descriptor")
    return candidate


def checker_descriptor(role: object, name: str) -> dict:
    require(isinstance(role, dict), name + " role")
    candidate = role.get("verdict", role.get("checker"))
    require(isinstance(candidate, dict), name + " checker descriptor")
    return candidate


def seal(value: dict, expected_schema: str | None = None,
         expected_terminal: str | None = None) -> None:
    require(isinstance(value.get("schema"), str), "upstream schema")
    if expected_schema is not None:
        require(value.get("schema") == expected_schema, "upstream schema")
    if expected_terminal is not None:
        require(value.get("terminal") == expected_terminal, "upstream terminal")
    claimed = value.get("self_digest_sha256")
    if claimed is not None:
        body = dict(value)
        body.pop("self_digest_sha256", None)
        require(claimed == digest(body), "upstream self seal")


def empty_sparse(value: object) -> bool:
    return value == {} or value == [] or value == None


def load_bundle(path: str) -> dict:
    raw = Path(path).read_bytes()
    manifest = json.loads(raw)
    require(manifest.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    roles = manifest.get("members")
    require(isinstance(roles, dict), "manifest members")
    for role_name in REQUIRED_ROLES:
        require(role_name in roles, "missing owner:" + role_name)
    objects, verdicts = {}, {}
    for role_name in REQUIRED_ROLES:
        role = roles[role_name]
        if role_name in ("a3_zero", "a4", "a0", "task193_actual"):
            receipt = descriptor(role, role_name)
            objects[role_name] = json_member(receipt)
            seal(objects[role_name])
        else:
            receipt = descriptor(role, role_name)
            objects[role_name] = json_member(receipt)
            seal(objects[role_name])
        verdicts[role_name] = json_member(checker_descriptor(role, role_name))
        require(isinstance(verdicts[role_name].get("terminal"), str),
                role_name + " checker terminal")
    a3 = objects["a3_zero"]
    result = a3.get("result", a3)
    require(a3.get("terminal") == "R07_PRE_A0_A3_PROJECTED_MEMBER" or
            result.get("terminal") == "R07_PRE_A0_A3_PROJECTED_MEMBER",
            "A3 zero terminal")
    require(empty_sparse(result.get("target")) and
            empty_sparse(result.get("lambda")) and
            empty_sparse(result.get("kappa0")), "A3 nonzero base")
    common = manifest.get("common_identity")
    require(isinstance(common, dict) and common, "common identity")
    return {"manifest": manifest, "objects": objects, "verdicts": verdicts,
            "manifest_sha256": hashlib.sha256(raw).hexdigest()}


def nested(value: dict, *keys: str):
    current = value
    for key in keys:
        require(isinstance(current, dict) and key in current, "missing field:" + ".".join(keys))
        current = current[key]
    return current


def input_state(bundle: dict) -> dict:
    objects = bundle["objects"]
    task198 = objects["task198"]
    runtime = task198.get("evaluator", {}).get("zero_base")
    require(isinstance(runtime, dict), "task198 zero-base runtime")
    d1 = vec(nested(runtime, "d1"))
    w = vec(nested(runtime, "w"))
    cmap = nested(runtime, "C")
    require(isinstance(cmap, dict), "printed block map")
    actions = nested(runtime, "marked_actions")
    require(isinstance(actions, list) and actions, "marked actions")
    for action in actions:
        require(isinstance(action, dict) and isinstance(action.get("name"), str),
                "marked action")
        require(isinstance(action.get("z"), dict) and
                isinstance(action.get("eta"), dict), "marked action map")
    a4 = objects["a4"]
    roster = nested(a4, "kernel", "K_roster")
    require(isinstance(roster, list) and roster, "A4 K roster")
    for item in roster:
        require(isinstance(item, dict) and isinstance(item.get("word"), list),
                "A4 word-bearing item")
        require(isinstance(item.get("seed"), dict) and
                isinstance(item["seed"].get("z"), dict) and
                isinstance(item["seed"].get("eta"), dict), "A4 zero-base seed")
    task193 = objects["task193_actual"]
    task193_result = task193.get("result", task193)
    beta = task193_result.get("beta1_vector")
    if beta is None:
        beta_blob = task193_result.get("beta1")
        beta = beta_blob.get("vector") if isinstance(beta_blob, dict) else beta_blob
    require(isinstance(beta, dict), "task193 beta1 vector")
    e1 = mul_scalar(vec(beta), -1)
    a0 = objects["a0"]
    a0_result = a0.get("result", a0)
    correction_word = a0_result.get("correction_word")
    require(isinstance(correction_word, list), "A0 literal correction word")
    binding = task193_result.get("literal_binding", task193_result.get("correction_word"))
    require(binding == correction_word, "task193 A0 word binding")
    exact_target = task193.get("eta_c", task193.get("result", {}).get("eta_c"))
    exact_bound = isinstance(exact_target, dict) and all(
        isinstance(action.get("exact"), dict) for action in actions) and all(
        isinstance(item.get("seed", {}).get("exact"), dict) for item in roster)
    return {"d1": d1, "w": w, "C": cmap, "actions": actions,
            "roster": roster, "e1": e1,
            "exact_target": vec(exact_target) if exact_bound else None,
            "exact_bound": exact_bound,
            "a0": objects["a0"], "task198": task198,
            "task193": task193}


def c_apply(eta: dict[str, int], cmap: dict) -> dict[str, int]:
    out = {}
    for key, coefficient in eta.items():
        images = cmap.get(key, [])
        require(isinstance(images, list), "C coordinate image")
        for target, scalar in images:
            out[str(target)] = f3(out.get(str(target), 0) + coefficient * scalar)
    return vec(out)


def terms_add(left: list[dict], right: list[dict], scalar: int) -> list[dict]:
    table = {}
    for term in left + right:
        key = (tuple(term["prefix"]), int(term["kernel_index"]))
        coefficient = term["coefficient"] if term in left else scalar * term["coefficient"]
        table[key] = f3(table.get(key, 0) + coefficient)
    return [{"coefficient": coefficient, "prefix": list(prefix),
             "kernel_index": index}
            for (prefix, index), coefficient in sorted(table.items()) if coefficient]


def compile_actual(bundle: dict) -> tuple[str, dict]:
    state = input_state(bundle)
    pre, joint, augmented = Echelon(), Echelon(), Echelon()
    raw_rows, queue = [], []
    accepted_ids = []
    a5_hit = None
    augmented_target = None
    if state["exact_bound"]:
        augmented_target = {"z:" + key: value for key, value in state["e1"].items()}
        augmented_target.update({"exact:" + key: value
                                 for key, value in state["exact_target"].items()})
    for index, item in enumerate(state["roster"]):
        seed = item["seed"]
        z, eta = vec(seed["z"]), vec(seed["eta"])
        label = "seed:" + str(index)
        terms = [{"coefficient": 1, "prefix": [], "kernel_index": index}]
        exact = vec(seed.get("exact", {})) if state["exact_bound"] else {}
        row = flat(z, eta)
        pre_record = pre.insert(row, label)
        raw_rows.append({"id": label, "z": z, "eta": eta, "exact": exact, "terms": terms,
                         "parent": None, "action": "seed",
                         "pre_decision": pre_record["accepted"]})
        if pre_record["accepted"] == "ACCEPTED":
            accepted_ids.append(label)
            queue.append(len(raw_rows) - 1)
            jrow = flat(z, c_apply(eta, state["C"]))
            jrec = joint.insert(jrow, label)
            raw_rows[-1]["joint_decision"] = jrec["accepted"]
            if state["exact_bound"]:
                arec = augmented.insert(flat_aug(z, c_apply(eta, state["C"]), exact), label)
                raw_rows[-1]["augmented_decision"] = arec["accepted"]
    target = {"z:" + key: value for key, value in state["e1"].items()}
    rem, target_coefficients = joint.reduce(target, {})
    if not rem:
        a5_hit = target_coefficients
    aug_coefficients = {}
    if augmented_target is not None:
        aug_rem, aug_coefficients = augmented.reduce(augmented_target, {})
        if not aug_rem:
            return member_result(bundle, state, raw_rows, aug_coefficients,
                                 "EARLY_AUGMENTED_MEMBER", len(queue), pre,
                                 joint, augmented, "AUGMENTED_MEMBER")
    cursor = 0
    while cursor < len(queue):
        parent_index = queue[cursor]
        cursor += 1
        parent = raw_rows[parent_index]
        for action in state["actions"]:
            z = image(parent["z"], action["z"])
            eta = image(parent["eta"], action["eta"])
            prefix_letter = action.get("prefix_letter")
            terms = []
            for term in parent["terms"]:
                prefix = list(term["prefix"])
                if prefix_letter is not None:
                    prefix.append(int(prefix_letter))
                terms.append({"coefficient": term["coefficient"],
                              "prefix": prefix,
                              "kernel_index": term["kernel_index"]})
            label = "row:" + str(len(raw_rows))
            rec = pre.insert(flat(z, eta), label)
            exact = image(parent.get("exact", {}), action.get("exact", {})) if state["exact_bound"] else {}
            raw_rows.append({"id": label, "z": z, "eta": eta, "exact": exact, "terms": terms,
                             "parent": parent_index, "action": action["name"],
                             "pre_decision": rec["accepted"]})
            if rec["accepted"] != "ACCEPTED":
                continue
            accepted_ids.append(label)
            queue.append(len(raw_rows) - 1)
            jrec = joint.insert(flat(z, c_apply(eta, state["C"])), label)
            raw_rows[-1]["joint_decision"] = jrec["accepted"]
            if state["exact_bound"]:
                arec = augmented.insert(flat_aug(z, c_apply(eta, state["C"]), exact), label)
                raw_rows[-1]["augmented_decision"] = arec["accepted"]
            rem, target_coefficients = joint.reduce(target, {})
            if not rem:
                a5_hit = target_coefficients
            if augmented_target is not None:
                aug_rem, aug_coefficients = augmented.reduce(augmented_target, {})
                if not aug_rem:
                    return member_result(bundle, state, raw_rows,
                                         aug_coefficients, "EARLY_AUGMENTED_MEMBER",
                                         cursor, pre, joint, augmented,
                                         "AUGMENTED_MEMBER")
    if a5_hit is not None:
        return member_result(bundle, state, raw_rows, a5_hit,
                             "EXHAUSTED_A5_MEMBER", cursor, pre, joint,
                             augmented, "A5_ONLY_AUGMENTED_NOT_BOUND" if
                             not state["exact_bound"] else
                             "A5_MEMBER_AUGMENTED_NO_HIT_UNKNOWN")
    dual = {key[3:]: value for key, value in rem.items() if key.startswith("z:")}
    return {"schema": SCHEMA, "status": "COMPLETE", "terminal": NONMEMBER,
            "manifest_sha256": bundle["manifest_sha256"],
            "zero_base": "A3 target/lambda/kappa0 empty",
            "closure": "EXHAUSTED", "candidate_count": len(raw_rows),
            "pre_rank": len(pre.rows), "joint_rank": len(joint.rows),
            "augmented_status": "NOT_BOUND" if not state["exact_bound"] else
                                "CANONICAL_NO_HIT_UNKNOWN",
            "remainder": dual, "dual": {"functional": dual,
            "scope": "authenticated fixed lower word"},
            "claims": dict(CLAIMS)}


def member_result(bundle: dict, state: dict, rows: list[dict], coefficients: dict,
                  closure: str, queue_head: int, pre: Echelon,
                  joint: Echelon, augmented: Echelon,
                  augmented_status: str) -> tuple[str, dict]:
    terms = []
    for row in rows:
        coefficient = coefficients.get(row["id"], 0)
        if coefficient:
            for term in row["terms"]:
                terms.append({"coefficient": f3(coefficient * term["coefficient"]),
                              "prefix_DAG_node": term["prefix"],
                              "original_A4_kernel_word_index": term["kernel_index"]})
    collected = {}
    for term in terms:
        key = (tuple(term["prefix_DAG_node"]),
               term["original_A4_kernel_word_index"])
        collected[key] = f3(collected.get(key, 0) + term["coefficient"])
    polynomial = [{"coefficient": coefficient, "prefix_DAG_node": list(prefix),
                   "original_A4_kernel_word_index": index}
                  for (prefix, index), coefficient in sorted(collected.items())
                  if coefficient]
    return MEMBER, {"schema": SCHEMA, "status": "COMPLETE", "terminal": MEMBER,
        "manifest_sha256": bundle["manifest_sha256"],
        "zero_base": "A3 target/lambda/kappa0 empty", "closure": closure,
        "queue_head": queue_head, "candidate_count": len(rows),
        "pre_rank": len(pre.rows), "joint_rank": len(joint.rows),
        "member": {"mu1": "theta", "target": state["e1"],
                   "joint_coefficients": coefficients},
        "a6": {"language": "factored", "records": polynomial,
               "ancestry_rows": [{"id": row["id"], "parent": row["parent"],
                                   "action": row["action"],
                                   "pre_decision": row["pre_decision"],
                                   "joint_decision": row.get("joint_decision"),
                                   "augmented_decision": row.get("augmented_decision"),
                                   "terms": row["terms"]} for row in rows]},
        "augmented": {"status": augmented_status,
                       "rank": len(augmented.rows),
                       "target": state["exact_target"]},
        "claims": dict(CLAIMS)}


def envelope(terminal: str, result: dict) -> dict:
    body = {"schema": SCHEMA, "terminal": terminal, "result": result}
    body["self_digest_sha256"] = digest(body)
    return body


def atomic_write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(canon(value) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    terminal, result = UNKNOWN_INPUT + ":uninitialized", {"reason": "uninitialized",
        "claims": dict(CLAIMS)}
    try:
        bundle = load_bundle(args.manifest)
        terminal, result = compile_actual(bundle)
    except ResourceStop as exc:
        terminal = (UNKNOWN_RESOURCE + ":phase=" + exc.phase + ":cap=" + exc.cap +
                    ":value=" + str(exc.value) + ":limit=" + str(exc.limit))
        result = {"reason": terminal, "claims": dict(CLAIMS)}
    except (Stop, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as exc:
        terminal = UNKNOWN_INPUT + ":" + str(exc).replace("\n", " ")
        result = {"reason": str(exc), "claims": dict(CLAIMS)}
    atomic_write(Path(args.output), envelope(terminal, result))
    print("R07_ZERO_BASE_A5_A6_PRODUCER_TERMINAL " + terminal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
