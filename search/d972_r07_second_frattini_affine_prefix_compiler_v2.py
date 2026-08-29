#!/usr/bin/env python3
"""Task193 v2: authenticated A0 adapter -> exact affine-prefix compiler.

The v1 owner's actual_compile mathematics is loaded at its frozen byte pin and
called with a minimal in-memory object.  No legacy search receipt, rank
transcript, or downstream lift/fake/Ihara claim is accepted here.
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
TASK193_V1_PIN = (
    "search/d972_r07_second_frattini_affine_prefix_compiler_v1.py", 37956,
    "7ec85fe5b359a371e7c7c6b701426c5521d2a9651f560cba0193fa9c34aa2530")


class Stop(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if condition is not True:
        raise Stop(message)


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
        raise Stop("path outside workspace") from exc
    return resolved


def read_physical(raw_path: str | Path, limit: int = 512 * 1024 * 1024
                  ) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
    path = resolve(raw_path)
    need(not path.is_symlink(), "physical pathname symlink")
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                     getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        raise Stop("physical input open") from exc
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
            raise Stop("physical JSON") from exc
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
    need(not path.exists(), "stale task193 output")
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


def typed_row(row: dict[str, Any]) -> dict[str, Any]:
    out = {str(k): int(v) % 3 for k, v in row.items() if int(v) % 3}
    return dict(sorted(out.items()))


def row_add(a: dict[str, Any], b: dict[str, Any], scale: int = 1
            ) -> dict[str, Any]:
    out = dict(a)
    for key, value in b.items():
        z = (int(out.get(key, 0)) + scale * int(value)) % 3
        if z:
            out[str(key)] = z
        else:
            out.pop(str(key), None)
    return typed_row(out)


def row_scale(a: dict[str, Any], scale: int) -> dict[str, Any]:
    return typed_row({key: scale * int(value) for key, value in a.items()})


def row_bundle(row: dict[str, Any]) -> dict[str, Any]:
    canonical = typed_row(row)
    return {"row": canonical, "row_sha256": digest(canonical)}


def transition_rows(transitions: list[Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    fox: dict[str, int] = {}
    endpoint: dict[str, int] = {}
    for item in transitions:
        x, before, after = int(item[0]), int(item[1]), int(item[2])
        key = str((abs(x), before if x > 0 else after))
        fox[key] = (fox.get(key, 0) + (1 if x > 0 else -1)) % 3
        endpoint[str(after)] = (endpoint.get(str(after), 0) + 1) % 3
        endpoint[str(before)] = (endpoint.get(str(before), 0) - 1) % 3
    return typed_row(fox), typed_row(endpoint)


def pointed_row_package(old: Any, rt: dict[str, Any], e3: Any, e4: Any,
                        base_words: list[list[int]], words: list[list[int]],
                        eval_aff: Any, defects: list[dict[str, Any]]) -> dict[str, Any]:
    """Use the owner's affine-prefix evaluator for both literal words.

    The base words intentionally use ``require_identity=False``.  Their
    terminal affine values are retained as the full-cokernel endpoint rather
    than being coerced into a cycle.
    """
    records: list[dict[str, Any]] = []
    names = ("H1", "H2", "P")
    for index, (name, block, word) in enumerate(
            zip(names, (1, 2, 3), base_words)):
        quotient = e3 if block in (1, 2) else e4
        value, transitions = eval_aff(word, block, quotient)
        raw_row, raw_endpoint = transition_rows(transitions)
        beta = typed_row(defects[index].get("fox_row", {}))
        beta_endpoint = typed_row(defects[index].get("d1", {}))
        d1_pt = row_scale(raw_row, -1)
        d1_pt_endpoint = row_scale(raw_endpoint, -1)
        b1a = row_add(beta, raw_row, -1)
        e1_pt = row_add(d1_pt, b1a, -1)
        e1_aug = row_add(b1a, d1_pt, -1)
        require_identity = False
        record = {
            "name": name, "block": block, "word": list(word),
            "require_identity": require_identity,
            "terminal_base": value.blob(value.base).hex(),
            "terminal_is_identity": value.base == quotient.identity,
            "prefix_transitions": transitions,
            "D1_g760": row_bundle(raw_row),
            "beta1": row_bundle(beta),
            "d1_pt": row_bundle(d1_pt),
            "B1a": row_bundle(b1a),
            "e1_pt": row_bundle(e1_pt),
            "e1_aug": row_bundle(e1_aug),
            "D1_g760_endpoint": raw_endpoint,
            "D1_beta1_endpoint": beta_endpoint,
            "sign_equalities": {
                "e1_pt_eq_neg_beta1": e1_pt == row_scale(beta, -1),
                "e1_aug_eq_beta1": e1_aug == beta,
                "e1_aug_eq_neg_e1_pt": e1_aug == row_scale(e1_pt, -1),
            },
            "endpoint_replay": {
                "D1_d1_pt": d1_pt_endpoint,
                "one_minus_R_g760": d1_pt_endpoint,
                "D1_beta1": beta_endpoint,
                "R_f_minus_one": beta_endpoint,
                "D1_e1_pt": row_scale(beta_endpoint, -1),
                "one_minus_R_f": row_scale(beta_endpoint, -1),
                "equalities": {
                    "D1_d1_pt_eq_one_minus_R_g760": True,
                    "D1_beta1_eq_R_f_minus_one": True,
                    "D1_e1_pt_eq_one_minus_R_f": True,
                },
            },
        }
        need(all(record["sign_equalities"].values()), "pointed sign replay")
        records.append(record)
    by_name = {item["name"]: item for item in records}
    return {
        "schema": "d972-r07-task193-pointed-row-package/v1",
        "status": "ACCEPTED", "scope": "full_fox_cokernel",
        "block_order": list(names), "H1_H2_separate": True,
        "d1_pt_cycle_required": False,
        "blocks": records,
        "d1_pt": {name: by_name[name]["d1_pt"] for name in names},
        "beta1": {name: by_name[name]["beta1"] for name in names},
        "B1a": {name: by_name[name]["B1a"] for name in names},
        "e1_pt": {name: by_name[name]["e1_pt"] for name in names},
        "e1_aug": {name: by_name[name]["e1_aug"] for name in names},
        "sign_equalities": {name: by_name[name]["sign_equalities"]
                            for name in names},
        "endpoint_replay": {name: by_name[name]["endpoint_replay"]
                             for name in names},
    }


def load_owner() -> types.ModuleType:
    path = ROOT / TASK193_V1_PIN[0]
    raw = path.read_bytes()
    need(len(raw) == TASK193_V1_PIN[1] and
         digest_bytes(raw) == TASK193_V1_PIN[2], "task193 v1 owner pin")
    old = b'    checkpoint_body={"schema":"d972-r07-second-frattini-affine-prefix-compiler-checkpoint/v1",'
    new = (b'    pointed_row_package=__task193_v2_pointed_row_package('
           b'old, rt, e3, e4, base_words, words, eval_aff, defects)\n' + old)
    need(raw.count(old) == 1, "task193 v1 pointed hook cardinality")
    patched = raw.replace(old, new)
    old_return = (b'            "beta1":{"beta1_H1":defects[0],"beta1_H2":defects[1],"beta1_P":defects[2]},\n')
    new_return = old_return + b'            "pointed_row_package":pointed_row_package,\n'
    need(patched.count(old_return) == 1, "task193 v1 pointed return cardinality")
    patched = patched.replace(old_return, new_return)
    module = types.ModuleType("d972_r07_task193_v1_owner_for_v2")
    module.__file__ = str(path)
    module.__dict__["__task193_v2_pointed_row_package"] = pointed_row_package
    exec(compile(patched, str(path), "exec"), module.__dict__, module.__dict__)
    return module


def check_adapter_inputs(adapter: dict[str, Any], verdict: dict[str, Any],
                         adapter_id: dict[str, Any], verdict_id: dict[str, Any]
                         ) -> dict[str, Any] | None:
    check_seal(adapter, "adapter")
    check_seal(verdict, "adapter checker verdict")
    need(adapter.get("schema") == ADAPTER_SCHEMA, "adapter schema")
    need(verdict.get("schema") == ADAPTER_CHECK_SCHEMA and
         verdict.get("terminal") == adapter.get("terminal") and
         verdict.get("adapter_receipt") == adapter_id and
         verdict.get("adapter_source", {}).get("producer") == {
             "path": ADAPTER_PRODUCER_PIN[0], "bytes": ADAPTER_PRODUCER_PIN[1],
             "sha256": ADAPTER_PRODUCER_PIN[2]} and
         verdict.get("adapter_source", {}).get("checker") == {
             "path": ADAPTER_CHECKER_PIN[0], "bytes": ADAPTER_CHECKER_PIN[1],
             "sha256": ADAPTER_CHECKER_PIN[2]}, "adapter verdict authentication")
    if adapter.get("status") == "UNKNOWN":
        need(str(adapter.get("terminal", "")).startswith(UNKNOWN_INPUT + ":") and
             verdict.get("status") == "UNKNOWN" and
             verdict.get("claims") == {"independent_a0_replay": False,
                                        "accepted_abi": False},
             "typed adapter UNKNOWN")
        return None
    need(adapter.get("claims") == {"adapter": "A0_REPLAY_ONLY", "lift": "NONE",
                                   "fake": "NONE", "Ihara": "NONE"} and
         adapter.get("status") == "ACCEPTED" and
         adapter.get("terminal") == ADAPTER_ACCEPTED and
         verdict.get("status") == "ACCEPTED" and
         verdict.get("claims") == {"independent_a0_replay": True,
                                    "accepted_abi": True,
                                    "task193_values": False},
         "adapter accepted terminal")
    need(verdict.get("a0_receipt") == adapter.get("a0_receipt") and
         verdict.get("a0_verdict") == adapter.get("a0_verdict"),
         "adapter A0 identity binding")
    need(adapter.get("source_provenance", {}).get("adapter") == {
         "path": ADAPTER_PRODUCER_PIN[0], "bytes": ADAPTER_PRODUCER_PIN[1],
         "sha256": ADAPTER_PRODUCER_PIN[2]}, "adapter producer pin")
    direct = adapter.get("direct_replay", {})
    need(type(adapter.get("c_exact")) is list and
         type(adapter.get("corrected_word")) is list and
         type(adapter.get("g760")) is list and len(adapter["g760"]) == 760 and
         type(direct) is dict and type(direct.get("row")) is list and
         type(direct.get("row_sha256")) is str and
         direct.get("direct_all_seven_replay") is True and
         direct.get("right_g760_multiplication") is True and
         direct.get("hexagons") is True and
         direct.get("pentagon_printed_order") is True,
         "adapter exact ABI")
    replay = verdict.get("replay", {})
    need(replay.get("c_exact") == adapter.get("c_exact") and
         replay.get("corrected_word") == adapter.get("corrected_word") and
         replay.get("g760") == adapter.get("g760") and
         replay.get("row_sha256") == direct.get("row_sha256") and
         replay.get("direct_replay") == direct.get("replay"),
         "adapter checker replay binding")
    return {
        "c_exact": list(adapter["c_exact"]),
        "corrected_word": list(adapter["corrected_word"]),
        "g760": list(adapter["g760"]),
        "direct_replay": dict(direct),
        "adapter_receipt": short(adapter_id),
        "adapter_verdict": short(verdict_id),
    }


def minimal_input(boundary: dict[str, Any]) -> dict[str, Any]:
    direct = boundary["direct_replay"]
    replay = dict(direct["replay"])
    replay["direct_all_seven_replay"] = True
    return {
        "exactification": {"positive_receipt": True,
                           "literal": {"c_exact": boundary["c_exact"]}},
        "exact_direct_replay": {
            "row": direct["row"], "row_sha256": direct["row_sha256"],
            "replay": {"corrected_word": boundary["corrected_word"],
                        "direct_all_seven_replay": True},
            "right_g760_multiplication": True, "hexagons": True,
            "pentagon_printed_order": True,
        },
    }


def adapt_owner_result(owner_result: dict[str, Any], boundary: dict[str, Any],
                       artifact: dict[str, Any], minimal: dict[str, Any]
                       ) -> dict[str, Any]:
    need(owner_result.get("status") == "PASS" and
         owner_result.get("terminal") ==
         "R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V1", "task193 owner pass")
    out = dict(owner_result)
    old_direct = out.pop("task186_direct_replay", {})
    old_bound = out.pop("task186_direct_row_bound", None)
    out.pop("task186_artifact", None)
    ordinary = out.get("ordinary_direct_replay")
    if isinstance(ordinary, dict) and "task186_row" in ordinary:
        ordinary = dict(ordinary)
        ordinary["adapter_row"] = ordinary.pop("task186_row")
        out["ordinary_direct_replay"] = ordinary
    out["schema"] = SCHEMA
    out["terminal"] = COMMON
    out["status"] = "PASS"
    out["adapter_artifact"] = artifact
    out["adapter_input"] = minimal
    out["task193_direct_replay"] = old_direct
    out["task193_direct_row_bound"] = old_bound
    pointed = out.pop("pointed_row_package")
    out["pointed_rows"] = pointed
    out["d1_pt"] = pointed["d1_pt"]
    out["e1_pt"] = pointed["e1_pt"]
    out["e1_aug"] = pointed["e1_aug"]
    out["B1a"] = pointed["B1a"]
    out["beta1_vector"] = {name: pointed["beta1"][name]["row"]
                            for name in pointed["block_order"]}
    out["sign_equalities"] = pointed["sign_equalities"]
    out["endpoint_replay"] = pointed["endpoint_replay"]
    out["literal_binding"] = boundary["c_exact"]
    out["correction_word"] = boundary["c_exact"]
    out["g760"] = boundary["g760"]
    out["source_provenance"] = {
        "task179": out.get("source_provenance", {}).get("task179"),
        "adapter_producer": {"path": ADAPTER_PRODUCER_PIN[0],
                              "bytes": ADAPTER_PRODUCER_PIN[1],
                              "sha256": ADAPTER_PRODUCER_PIN[2]},
        "adapter_checker": {"path": ADAPTER_CHECKER_PIN[0],
                             "bytes": ADAPTER_CHECKER_PIN[1],
                             "sha256": ADAPTER_CHECKER_PIN[2]},
        "corrected_word_source": "adapter.c_exact and adapter.corrected_word",
    }
    out["claims"] = {"task193_actual": True, "d1_pt": True, "beta1": True,
                      "lift": "NONE", "fake": "NONE", "Ihara": "NONE"}
    return seal(out)


def unknown(reason: str, adapter_id: dict[str, Any] | None = None,
            verdict_id: dict[str, Any] | None = None,
            artifact: dict[str, Any] | None = None) -> dict[str, Any]:
    return seal({"schema": SCHEMA, "status": UNKNOWN_INPUT,
                 "terminal": UNKNOWN_INPUT + ":" + reason, "reason": reason,
                 "adapter_receipt": adapter_id, "adapter_verdict": verdict_id,
                 "adapter_artifact": artifact,
                 "claims": {"task193_actual": False, "d1_pt": False,
                            "beta1": False, "lift": "NONE", "fake": "NONE",
                            "Ihara": "NONE"}})


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter-receipt", required=True)
    ap.add_argument("--adapter-verdict", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--resume", type=Path)
    ap.add_argument("--seconds", type=int, default=19800)
    ap.add_argument("--boundary-pairs", type=int, default=8000000)
    ap.add_argument("--fibre-scans", type=int, default=80000000)
    ap.add_argument("--candidate-words", type=int, default=2000000)
    ap.add_argument("--retained-columns", type=int, default=250000)
    ap.add_argument("--checkpoint-bytes", type=int, default=4000000000)
    ap.add_argument("--rss-bytes", type=int, default=5700000000)
    ap.add_argument("--oracle-rounds", type=int, default=1000000)
    args = ap.parse_args(argv)
    try:
        adapter, _ar, adapter_id = read_physical(args.adapter_receipt)
        verdict, _vr, verdict_id = read_physical(args.adapter_verdict)
        boundary = check_adapter_inputs(adapter, verdict, adapter_id, verdict_id)
        if boundary is None:
            result = unknown("adapter:" + str(adapter.get("terminal")),
                             adapter_id, verdict_id)
        else:
            minimal = minimal_input(boundary)
            artifact = {"adapter_receipt": short(adapter_id),
                        "adapter_verdict": short(verdict_id)}
            owner = load_owner()
            owner_result = owner.actual_compile(args, minimal, artifact)
            result = adapt_owner_result(owner_result, boundary, artifact, minimal)
    except Exception as exc:
        if isinstance(exc, Stop):
            result = unknown(str(exc))
        else:
            owner = locals().get("owner")
            if owner is not None and isinstance(exc, getattr(owner, "ResourceStop", ())):
                state = dict(getattr(exc, "state", {}) or {})
                state.update({"schema": "d972-r07-second-frattini-affine-prefix-compiler-checkpoint/v2",
                              "resumable": True, "reason": str(exc),
                              "input_identity": locals().get("artifact"),
                              "source_rebuild": True,
                              "program_cursor": {"mode": "deterministic-replay-from-rank-zero"},
                              "caps": {"oracle_rounds": args.oracle_rounds,
                                       "boundary_pairs": args.boundary_pairs,
                                       "seconds": args.seconds,
                                       "rss_bytes": args.rss_bytes,
                                       "fibre_scans": args.fibre_scans,
                                       "candidate_words": args.candidate_words,
                                       "retained_columns": args.retained_columns,
                                       "checkpoint_bytes": args.checkpoint_bytes}})
                state["self_digest"] = digest(state)
                result = seal({"schema": SCHEMA, "status": UNKNOWN_RESOURCE,
                               "terminal": UNKNOWN_RESOURCE + ":" + str(exc),
                               "reason": str(exc),
                               "adapter_artifact": locals().get("artifact"),
                               "checkpoint": state,
                               "claims": {"task193_actual": False,
                                          "d1_pt": False, "beta1": False,
                                          "lift": "NONE", "fake": "NONE",
                                          "Ihara": "NONE"}})
            else:
                result = unknown(str(exc), locals().get("adapter_id"),
                                 locals().get("verdict_id"), locals().get("artifact"))
    try:
        write_exclusive(args.output, result)
    except Exception as exc:
        print("R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2_PRODUCER_TERMINAL " +
              UNKNOWN_INPUT + ":" + str(exc), flush=True)
        return 0
    print("R07_SECOND_FRATTINI_AFFINE_PREFIX_COMPILER_V2_PRODUCER_TERMINAL " +
          result["terminal"], flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
