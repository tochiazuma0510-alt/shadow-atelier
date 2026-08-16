#!/usr/bin/env python3
"""Fail-closed calibration diagnostic for the D972 v2.x lane.

This is a diagnostic wrapper, not a replacement for the v2 terminal checker.
Fresh mode first obtains the two-generator presentation from the pinned v2
worker/manifest input, then independently reconstructs the calibration GAP
program.  Optional state mode replays the same program from a v2 state
artifact.  Both modes make the quotient generator correspondence explicit
and record bounded process output without turning any failure into A or B.

The map remains Q -> BQ.  The only source-level change is replacing the
implicit ``GeneratorsOfGroup(Q)`` list by images of the two named free
generators under the explicit quotient projection.  Exact relation, order,
generation, image, surjectivity, and bijection gates are retained.  Any gate
failure is UNKNOWN and is emitted with a receipt.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
V2_CHECKER = ROOT / "search" / "check_d972_dovetail_v2.py"
V2_MANIFEST = ROOT / "search" / "d972_dovetail_manifest_v2.json"
V2_WORKER = ROOT / "search" / "d972_dovetail_worker_v2.g"
EXPECTED_V2_CHECKER_SHA256 = (
    "624436f2d6a5ed4ad72a92ec5360fa22acbfe792e5dad56c1f6a267858baa8b1"
)
EXPECTED_V2_MANIFEST_SHA256 = (
    "0f90776483342f84eb4424e4fbc4a8e7407672a070f3ed493260b3c09a1963f8"
)
EXPECTED_V2_WORKER_SHA256 = (
    "93d54d70a42ad283d95fed981eb2732ed8c8dd7fb37da5772fd6d486038f69f2"
)
EXPECTED_V2_UNIVERSE_ID = (
    "B3-stable-marked-extensions-over-K9-intersection-NS4-k-ge-3/v2"
)
EXPECTED_V2_INPUT_DIGEST = (
    "48d2d91ef56f2cc73a75b559aed378f48d5d28d1e04a964ccfd6fb5502713969"
)
EXPECTED_TARGET_KEY_SHA256 = (
    "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
)
SCHEMA = "d972-calibration-diagnostic/v4"
MAX_EXCERPT_CHARS = 4096
ZERO_SHA = "0" * 64

OLD_QTOBASE = (
    "qToBase:=GroupHomomorphismByImages(Q,BQ,qg,[bs1,bs2]);;\n"
    "if qToBase=fail or not IsBijective(qToBase) then "
    "Error(\"calibration presentation/base mismatch\"); fi;"
)
OLD_QBLOCK_PREFIX = (
    'FQ:=FreeGroup(2,"r");; Q:=FQ/MakeRels(FQ,{qrels});; '
    "qg:=GeneratorsOfGroup(Q);;\n"
)

# This keeps the old Q -> BQ direction.  qg is now explicitly the image of
# the named FQ generators, so a GAP implementation cannot silently choose a
# different GeneratorsOfGroup(Q) ordering.  All gates are deliberately
# stronger than the old single IsBijective test.
FIXED_QTOBASE = r'''FQgens:=GeneratorsOfGroup(FQ);;
relatorsQ:=MakeRels(FQ,{qrels});;
NQ:=NormalClosure(FQ,Group(relatorsQ));;
Q:=FQ/NQ;;
qProjection:=NaturalHomomorphismByNormalSubgroup(FQ,NQ);;
qg:=List(FQgens,x->Image(qProjection,x));;
if Length(FQgens)<>2 or Length(qg)<>2 then
  Error("calibration quotient generator arity drift");
fi;
freeToBase:=GroupHomomorphismByImages(FQ,BQ,FQgens,[bs1,bs2]);;
if freeToBase=fail then Error("calibration free-generator map failure"); fi;
for rel in relatorsQ do
  if Image(freeToBase,rel)<>One(BQ) then
    Error("calibration quotient relation is false in base");
  fi;
od;
qToBase:=GroupHomomorphismByImages(Q,BQ,qg,[bs1,bs2]);;
if qToBase=fail then Error("calibration presentation/base map failure"); fi;
if Size(Group(qg))<>Size(Q) then
  Error("calibration quotient generator image does not generate Q");
fi;
if Size(Q)<>Size(BQ) or Size(BQ)<>8817984 then
  Error("calibration quotient/base order mismatch");
fi;
if Size(Image(qToBase))<>Size(BQ) or not IsSurjective(qToBase) or
   not IsBijective(qToBase) then
  Error("calibration presentation/base bijection failure");
fi;'''


class DiagnosticStop(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DiagnosticStop(message)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp",
                                     dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=True, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def bounded_excerpt(text: str, limit: int = MAX_EXCERPT_CHARS) -> str:
    require(limit >= 128, "diagnostic excerpt limit too small")
    if len(text) <= limit:
        return text
    marker = "\n...<bounded diagnostic excerpt>...\n"
    room = limit - len(marker)
    left = room // 2
    right = room - left
    return text[:left] + marker + text[-right:]


def load_v2_checker() -> Any:
    require(V2_CHECKER.is_file(), "v2 checker source is absent")
    require(sha_file(V2_CHECKER) == EXPECTED_V2_CHECKER_SHA256,
            "v2 checker source digest drift")
    require(V2_MANIFEST.is_file() and sha_file(V2_MANIFEST) ==
            EXPECTED_V2_MANIFEST_SHA256, "v2 manifest source digest drift")
    spec = importlib.util.spec_from_file_location("d972_checker_v2_diag_source",
                                                  V2_CHECKER)
    require(spec is not None and spec.loader is not None,
            "v2 checker import specification unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_frozen_manifest() -> dict[str, Any]:
    require(V2_MANIFEST.is_file(), "v2 manifest source is absent")
    value = json.loads(V2_MANIFEST.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "v2 manifest is not an object")
    universe_id = value.get("universe_id")
    input_digest = value.get("search_input_set_sha256")
    require(isinstance(universe_id, str) and universe_id,
            "v2 manifest universe_id is absent")
    require(isinstance(input_digest, str) and len(input_digest) == 64 and
            all(c in "0123456789abcdef" for c in input_digest),
            "v2 manifest search_input_set_sha256 is malformed")
    require(universe_id == EXPECTED_V2_UNIVERSE_ID and
            input_digest == EXPECTED_V2_INPUT_DIGEST,
            "v2 manifest frozen universe/input binding drift")
    return value


def strict_q_relators(value: Any) -> list[list[int]]:
    require(isinstance(value, list) and value, "q_relators absent")
    result: list[list[int]] = []
    for index, row in enumerate(value):
        require(isinstance(row, list) and row,
                f"q_relators[{index}] is empty or not a list")
        checked: list[int] = []
        for letter in row:
            require(isinstance(letter, int) and not isinstance(letter, bool) and
                    letter in {-2, -1, 1, 2},
                    f"q_relators[{index}] has an invalid signed generator")
            checked.append(letter)
        result.append(checked)
    return result


def worker_stream_fields(text: str) -> dict[str, Any]:
    raw = text.encode("utf-8", errors="replace")
    return {
        "bytes": len(raw),
        "sha256": sha_bytes(raw),
        "excerpt": bounded_excerpt(text),
    }


def validate_frozen_worker_output(path: Path, manifest: dict[str, Any]) -> tuple[
        dict[str, Any], list[list[int]], bytes]:
    require(path.is_file(), f"fresh frozen-v2 worker output is absent: {path}")
    raw = path.read_bytes()
    require(raw, "fresh frozen-v2 worker output is empty")
    try:
        text = raw.decode("utf-8")
        envelope = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DiagnosticStop("fresh frozen-v2 worker output is not one JSON envelope") from exc
    require(isinstance(envelope, dict),
            "fresh frozen-v2 worker envelope is not an object")
    require(envelope.get("schema") == "d972_dovetail_worker/v2" and
            envelope.get("mode") == "base-presentation" and
            envelope.get("status") == "PASS",
            "fresh frozen-v2 worker envelope is not a PASS base-presentation")
    require(envelope.get("universe_id") == manifest["universe_id"] and
            envelope.get("input_digest") == manifest["search_input_set_sha256"],
            "fresh frozen-v2 worker input/universe binding drift")
    for key in ("payload_sha256", "checkpoint_sha256"):
        value = envelope.get(key)
        require(isinstance(value, str) and len(value) == 64 and
                all(c in "0123456789abcdef" for c in value),
                f"fresh frozen-v2 worker {key} is malformed")
    payload = envelope.get("payload")
    require(isinstance(payload, dict) and
            payload.get("schema") == "d972_dovetail_worker/v1" and
            payload.get("mode") == "base-presentation" and
            payload.get("status") == "PASS",
            "fresh frozen-v2 worker payload schema/mode drift")
    require(payload.get("q_order") == 8817984 and
            payload.get("qbar_size") == 8817984 and
            payload.get("fp_generator_count") == 2 and
            payload.get("braid") is True,
            "fresh frozen-v2 worker exact base order/generator/braid gates failed")
    q_relators = strict_q_relators(payload.get("q_relators"))
    require(payload.get("fp_relators") == q_relators,
            "fresh frozen-v2 worker fp/q relator lists disagree")
    require(payload.get("fp_relator_count") == len(q_relators),
            "fresh frozen-v2 worker relator count drift")
    return envelope, q_relators, raw


def run_frozen_base_presentation(legacy: Any, manifest: dict[str, Any],
                                 output_path: Path) -> tuple[
        dict[str, Any] | None, list[list[int]] | None, dict[str, Any]]:
    """Run only the frozen v2 presentation producer; never infer A/B here."""
    require(V2_WORKER.is_file(), "frozen v2 worker source is absent")
    require(sha_file(V2_WORKER) == EXPECTED_V2_WORKER_SHA256,
            "frozen v2 worker source digest drift")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.unlink()
    except FileNotFoundError:
        pass
    environment = os.environ.copy()
    for name in ("D972_TASK_G", "D972_TASK", "D972_TASK_DIGEST",
                 "D972_DMTCP_CONTRACT_SHA256", "D972_DMTCP_IMAGE_MANIFEST_SHA256"):
        environment.pop(name, None)
    environment.update({
        "D972_WORKER_MODE": "base-presentation",
        "D972_WORKER_OUTPUT": str(output_path.resolve()),
        "D972_UNIVERSE_ID": manifest["universe_id"],
        "D972_INPUT_DIGEST": manifest["search_input_set_sha256"],
        "D972_DMTCP_ENABLED": "0",
        "D972_DMTCP_GENERATION": "0",
        "D972_HEARTBEAT": "",
    })
    info: dict[str, Any] = {
        "worker_source_sha256": sha_file(V2_WORKER),
        "worker_mode": "base-presentation",
        "worker_output_present": False,
    }
    try:
        command, command_mode = legacy.select_gap_command(V2_WORKER)
        info["worker_command_mode"] = command_mode
        info["worker_command_argv"] = [
            (Path(item).name if item == command[0] else item)
            for item in command
        ]
    except (DiagnosticStop, OSError, ValueError) as exc:
        info.update({
            "worker_command_mode": "unavailable",
            "worker_command_argv": [],
            "worker_returncode": None,
            "worker_stdout_bytes": 0,
            "worker_stdout_sha256": sha_bytes(b""),
            "worker_stdout_excerpt": "",
            "worker_stderr_bytes": 0,
            "worker_stderr_sha256": sha_bytes(b""),
            "worker_stderr_excerpt": "",
            "worker_error": str(exc),
        })
        return None, None, info
    timeout_value = os.environ.get("D972_CALIBRATION_WORKER_TIMEOUT", "10800")
    try:
        completed = subprocess.run(
            command, cwd=ROOT, env=environment, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=int(timeout_value),
            check=False,
        )
        info["worker_returncode"] = completed.returncode
        for stream_name, stream_text in (("stdout", completed.stdout or ""),
                                          ("stderr", completed.stderr or "")):
            fields = worker_stream_fields(stream_text)
            for field, value in fields.items():
                info[f"worker_{stream_name}_{field}"] = value
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or b"") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = (exc.stderr or b"") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        info["worker_returncode"] = None
        for stream_name, stream_text in (("stdout", stdout), ("stderr", stderr)):
            if isinstance(stream_text, bytes):
                stream_text = stream_text.decode("utf-8", errors="replace")
            fields = worker_stream_fields(stream_text)
            for field, value in fields.items():
                info[f"worker_{stream_name}_{field}"] = value
        info["worker_error"] = "TimeoutExpired"
        info["worker_output_present"] = False
        return None, None, info
    except (OSError, ValueError) as exc:
        info["worker_returncode"] = None
        info["worker_stdout_bytes"] = 0
        info["worker_stdout_sha256"] = sha_bytes(b"")
        info["worker_stdout_excerpt"] = ""
        info["worker_stderr_bytes"] = 0
        info["worker_stderr_sha256"] = sha_bytes(b"")
        info["worker_stderr_excerpt"] = ""
        info["worker_error"] = type(exc).__name__
        info["worker_output_present"] = False
        return None, None, info
    if output_path.is_file():
        raw = output_path.read_bytes()
        info["worker_output_present"] = True
        info["worker_output_bytes"] = len(raw)
        info["worker_output_sha256"] = sha_bytes(raw)
        info["worker_output_excerpt"] = bounded_excerpt(
            raw.decode("utf-8", errors="replace"))
        info["worker_output_artifact"] = str(output_path).replace("\\", "/")
    else:
        info["worker_output_present"] = False
    if info.get("worker_returncode") != 0:
        info["worker_error"] = "worker_nonzero_exit"
        return None, None, info
    try:
        envelope, q_relators, _ = validate_frozen_worker_output(output_path, manifest)
    except (DiagnosticStop, OSError, ValueError, KeyError,
            TypeError, json.JSONDecodeError) as exc:
        info["worker_error"] = str(exc)
        return None, None, info
    info["worker_envelope_schema"] = envelope["schema"]
    info["worker_universe_id"] = envelope["universe_id"]
    info["worker_input_digest"] = envelope["input_digest"]
    info["worker_payload_sha256"] = envelope["payload_sha256"]
    info["worker_checkpoint_sha256"] = envelope["checkpoint_sha256"]
    info["worker_q_relators_sha256"] = sha_bytes(canonical_bytes(q_relators))
    return envelope, q_relators, info


def load_state(path: Path, legacy_v1: Any) -> tuple[dict[str, Any], list[list[int]]]:
    require(path.is_file(), f"state file is absent: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "state is not an object")
    # The v2 checker remains the authority for the v1 mathematical state
    # schema/hash.  Binding is disabled only for the checkout-independent
    # diagnostic; source and checker digests are still fixed above.
    legacy_v1.validate_state_core(value, bind_current=False)
    status = value.get("status", {})
    require(status.get("terminal") is False and
            status.get("code") in {
                "INITIALIZED", "CALIBRATION_PENDING", "CHECKER_PENDING",
                "UNKNOWN/RESUME", "CONTINUE", "CALIBRATION_STOP",
            }, "diagnostic requires a nonterminal v2 state")
    worker = value.get("receipts", {}).get("producer_preflight", {}).get("worker", {})
    q_relators = strict_q_relators(worker.get("q_relators"))
    return value, q_relators


def build_fixed_script(legacy: Any, q_relators: list[list[int]],
                       target_keys: list[str]) -> str:
    original = legacy.independent_calibration_gap_script(q_relators, target_keys)
    qrels_json = json.dumps(q_relators, separators=(",", ":"))
    old_qblock = (OLD_QBLOCK_PREFIX.replace("{qrels}", qrels_json) +
                  OLD_QTOBASE)
    require(original.count(old_qblock) == 1,
            "v2 calibration qToBase source shape drift")
    rendered_fixed_qtobase = FIXED_QTOBASE.replace("{qrels}", qrels_json)
    fixed_block = 'FQ:=FreeGroup(2,"r");;\n' + rendered_fixed_qtobase
    fixed = original.replace(old_qblock, fixed_block)
    require(fixed.count(OLD_QTOBASE) == 0 and
            fixed.count(rendered_fixed_qtobase) == 1 and
            "{qrels}" not in fixed,
            "qToBase replacement was not unique")
    require("qToBase:=GroupHomomorphismByImages(Q,BQ,qg,[bs1,bs2]);;" in fixed and
            "not IsBijective(qToBase)" in fixed and
            "Size(Q)<>Size(BQ)" in fixed and
            "Image(freeToBase,rel)" in fixed,
            "fixed calibration script lost a required gate")
    fixed.encode("ascii")
    return fixed


def base_receipt(source_mode: str, q_relators: list[list[int]],
                 target_keys: list[str], script: str,
                 state_path: Path | None = None,
                 state: dict[str, Any] | None = None) -> dict[str, Any]:
    require(source_mode in {"state-artifact", "fresh-frozen-v2"},
            "unknown calibration diagnostic source mode")
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "RUNNING",
        "terminal_authority": "UNKNOWN_ONLY_UNTIL_V2_CALIBRATION_PASS",
        "source_mode": source_mode,
        "v2_checker_sha256": sha_file(V2_CHECKER),
        "v2_manifest_sha256": sha_file(V2_MANIFEST),
        "q_relators_sha256": sha_bytes(canonical_bytes(q_relators)),
        "target_key_count": len(target_keys),
        "target_key_order_sha256": sha_bytes(("\n".join(target_keys) + "\n").encode()),
        "script_sha256": sha_bytes(script.encode("ascii")),
        "script_variant": "explicit-free-generator-quotient-v4",
        "map_direction": "Q_to_BQ",
        "bounded_output_limit_chars": MAX_EXCERPT_CHARS,
    }
    if source_mode == "state-artifact":
        require(state_path is not None and state is not None,
                "state source metadata is absent")
        receipt["source_state_sha256"] = sha_file(state_path)
        receipt["source_status_code"] = state.get("status", {}).get("code")
        receipt["source_sequence"] = state.get("hash_chain", {}).get("sequence")
    else:
        receipt["v2_worker_sha256"] = sha_file(V2_WORKER)
        receipt["frozen_worker_mode"] = "base-presentation"
    return receipt


def add_result_fields(receipt: dict[str, Any], returncode: int | None,
                      stdout: str = "", stderr: str = "",
                      command_mode: str | None = None,
                      command: list[str] | None = None,
                      error: str | None = None) -> None:
    receipt["returncode"] = returncode
    receipt["stdout_bytes"] = len(stdout.encode("utf-8", errors="replace"))
    receipt["stderr_bytes"] = len(stderr.encode("utf-8", errors="replace"))
    receipt["stdout_sha256"] = sha_bytes(stdout.encode("utf-8", errors="replace"))
    receipt["stderr_sha256"] = sha_bytes(stderr.encode("utf-8", errors="replace"))
    receipt["stdout_excerpt"] = bounded_excerpt(stdout)
    receipt["stderr_excerpt"] = bounded_excerpt(stderr)
    if command_mode is not None:
        receipt["command_mode"] = command_mode
    if command is not None:
        receipt["command_argv"] = [
            (Path(item).name if item == command[0] else
             "<generated-script>" if item.endswith(".g") else item)
            for item in command
        ]
    if error is not None:
        receipt["diagnostic_error"] = error


def finish_receipt(path: Path, receipt: dict[str, Any]) -> None:
    body = copy.deepcopy(receipt)
    body.pop("receipt_sha256", None)
    receipt["receipt_sha256"] = sha_bytes(canonical_bytes(body))
    atomic_json(path, receipt)


def base_source_receipt(source_mode: str) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "DIAGNOSTIC_STOP",
        "terminal_authority": "UNKNOWN_ONLY",
        "source_mode": source_mode,
        "v2_checker_sha256": sha_file(V2_CHECKER),
        "v2_manifest_sha256": sha_file(V2_MANIFEST),
        "bounded_output_limit_chars": MAX_EXCERPT_CHARS,
    }
    if source_mode == "fresh-frozen-v2":
        receipt["v2_worker_sha256"] = sha_file(V2_WORKER)
        receipt["frozen_worker_mode"] = "base-presentation"
        receipt.update({
            "worker_source_sha256": sha_file(V2_WORKER),
            "worker_mode": "base-presentation",
            "worker_command_mode": "unavailable",
            "worker_command_argv": [],
            "worker_returncode": None,
            "worker_stdout_bytes": 0,
            "worker_stdout_sha256": sha_bytes(b""),
            "worker_stdout_excerpt": "",
            "worker_stderr_bytes": 0,
            "worker_stderr_sha256": sha_bytes(b""),
            "worker_stderr_excerpt": "",
            "worker_output_present": False,
        })
    return receipt


def attach_worker_info(receipt: dict[str, Any], info: dict[str, Any]) -> None:
    for key, value in info.items():
        receipt[key] = value


def diagnose(args: argparse.Namespace) -> int:
    receipt_path = args.receipt
    script_output = args.script_output
    source_mode = "fresh-frozen-v2" if args.mode == "fresh" else "state-artifact"
    receipt: dict[str, Any] = base_source_receipt(source_mode)
    if args.mode == "state" and args.state is not None and args.state.is_file():
        receipt["source_state_sha256"] = sha_file(args.state)
    try:
        checker_v2 = load_v2_checker()
        legacy_v1 = checker_v2.load_legacy()
        manifest = load_frozen_manifest()
        target_keys = checker_v2.canonical_target_keys()
        require(len(target_keys) == 972 and
                sha_bytes(("\n".join(target_keys) + "\n").encode()) ==
                EXPECTED_TARGET_KEY_SHA256,
                "canonical target-key order digest drift")
        if args.mode == "state":
            state, q_relators = load_state(args.state, legacy_v1)
        else:
            require(args.state is None,
                    "fresh calibration mode cannot receive a state artifact")
            worker_output = args.worker_output
            require(worker_output is not None,
                    "fresh calibration mode requires --worker-output")
            envelope, q_relators, worker_info = run_frozen_base_presentation(
                legacy_v1, manifest, worker_output)
            attach_worker_info(receipt, worker_info)
            if envelope is None or q_relators is None:
                receipt["diagnostic_error"] = worker_info.get(
                    "worker_error", "fresh frozen-v2 worker did not produce a receipt")
                add_result_fields(receipt, None, error=receipt["diagnostic_error"])
                finish_receipt(receipt_path, receipt)
                print(receipt["diagnostic_error"], file=sys.stderr)
                return 2
        script = build_fixed_script(checker_v2, q_relators, target_keys)
        if args.mode == "state":
            receipt = base_receipt("state-artifact", q_relators, target_keys,
                                   script, args.state, state)
        else:
            worker_info_copy = {
                key: value for key, value in receipt.items()
                if key.startswith("worker_") or key in {
                    "v2_worker_sha256", "frozen_worker_mode",
                }
            }
            receipt = base_receipt("fresh-frozen-v2", q_relators, target_keys,
                                   script)
            receipt.update(worker_info_copy)
        if script_output is not None:
            script_output.parent.mkdir(parents=True, exist_ok=True)
            script_output.write_text(script, encoding="ascii", newline="\n")
            require(sha_file(script_output) == receipt["script_sha256"],
                    "generated script output digest mismatch")
            receipt["script_artifact"] = str(script_output).replace("\\", "/")
        handle = tempfile.NamedTemporaryFile(
            mode="w", encoding="ascii", newline="\n", prefix="d972-calibration-v4-",
            suffix=".g", delete=False,
        )
        script_path = Path(handle.name)
        try:
            with handle:
                handle.write(script)
                handle.flush()
                os.fsync(handle.fileno())
            command, command_mode = legacy_v1.select_gap_command(script_path)
            completed = subprocess.run(
                command, cwd=ROOT, capture_output=True, text=True,
                encoding="utf-8", errors="replace", check=False,
            )
        finally:
            try:
                script_path.unlink()
            except FileNotFoundError:
                pass
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        add_result_fields(receipt, completed.returncode, stdout, stderr,
                          command_mode, command)
        if completed.returncode != 0:
            receipt["status"] = "CALIBRATION_UNKNOWN_GAP_EXIT"
            receipt["failure_preserves"] = [
                "script_sha256", "stdout_sha256", "stderr_sha256",
                "stdout_excerpt", "stderr_excerpt",
            ]
            finish_receipt(receipt_path, receipt)
            print(f"CALIBRATION_UNKNOWN_GAP_EXIT {completed.returncode}", file=sys.stderr)
            return 2
        receipt["status"] = "CALIBRATION_PASS_CANDIDATE"
        receipt["calibration_pass_requires"] = [
            "parse all D972_CAL_ROW/SUMMARY/FIBERS",
            "v2 producer/frozen calibration comparison",
            "v2 state transition and independent receipt validation",
        ]
        finish_receipt(receipt_path, receipt)
        print(f"CALIBRATION_PASS_CANDIDATE {receipt['script_sha256']}")
        return 0
    except (DiagnosticStop, OSError, ValueError, KeyError, TypeError,
            json.JSONDecodeError) as exc:
        add_result_fields(receipt, None, error=str(exc))
        finish_receipt(receipt_path, receipt)
        print(str(exc), file=sys.stderr)
        return 3


def self_test() -> int:
    checker_v2 = load_v2_checker()
    q_relators = [[1, -2], [2, -1]]
    target_keys = ["toy"]
    script = build_fixed_script(checker_v2, q_relators, target_keys)
    rendered_fixed_qtobase = FIXED_QTOBASE.replace(
        "{qrels}", json.dumps(q_relators, separators=(",", ":")))
    require(script.count(rendered_fixed_qtobase) == 1 and
            "{qrels}" not in script,
            "self-test replacement count")
    require("relatorsQ:=MakeRels(FQ,[[1,-2],[2,-1]]);;" in script,
            "self-test q-relator syntax substitution")
    bad_script = script.replace("[[1,-2],[2,-1]]", "{qrels}")
    try:
        require("{qrels}" not in bad_script,
                "self-test accepted an unsubstituted qrels placeholder")
    except DiagnosticStop:
        pass
    else:
        raise DiagnosticStop("self-test placeholder negative was not triggered")
    require("NormalClosure(FQ,Group(relatorsQ))" in script and
            "NaturalHomomorphismByNormalSubgroup(FQ,NQ)" in script and
            "Size(Image(qToBase))<>Size(BQ)" in script,
            "self-test explicit quotient/bijection gates")
    sample = "x" * (MAX_EXCERPT_CHARS + 100)
    excerpt = bounded_excerpt(sample)
    require(len(excerpt) <= MAX_EXCERPT_CHARS and
            "bounded diagnostic excerpt" in excerpt,
            "self-test bounded output")
    receipt = {
        "schema": SCHEMA, "status": "CALIBRATION_UNKNOWN_GAP_EXIT",
        "script_sha256": sha_bytes(script.encode("ascii")),
        "stdout_sha256": sha_bytes(b"out"), "stderr_sha256": sha_bytes(b"err"),
        "stdout_excerpt": "out", "stderr_excerpt": "err",
    }
    with tempfile.TemporaryDirectory(prefix="d972-diag-selftest-") as directory:
        finish_receipt(Path(directory) / "receipt.json", receipt)
    print(json.dumps({
        "schema": SCHEMA, "status": "PASS",
        "explicit_q_generator_projection": True,
        "map_direction": "Q_to_BQ",
        "order_relation_bijection_gates": True,
        "bounded_stdout_stderr": True,
        "negative_exit_receipt": True,
    }, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--mode", choices=("fresh", "state"), default="fresh")
    parser.add_argument("--state", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--script-output", type=Path)
    parser.add_argument("--worker-output", type=Path)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    if args.self_test:
        require(args.state is None and args.receipt is None,
                "self-test does not accept runtime paths")
        return self_test()
    require(args.receipt is not None,
            "--receipt is required")
    if args.mode == "state":
        require(args.state is not None and args.worker_output is None,
                "state mode requires --state and forbids --worker-output")
    else:
        require(args.state is None and args.worker_output is not None,
                "fresh mode forbids --state and requires --worker-output")
    return diagnose(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (DiagnosticStop, OSError, ValueError, KeyError, TypeError,
            json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(3)
