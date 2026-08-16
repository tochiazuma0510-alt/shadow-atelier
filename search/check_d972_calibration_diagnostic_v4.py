#!/usr/bin/env python3
"""Independent fail-closed checker for a v4 calibration diagnostic receipt."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-calibration-diagnostic/v4"
MAX_EXCERPT_CHARS = 4096
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
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
FIXED_MARKERS = (
    "FQgens:=GeneratorsOfGroup(FQ);;",
    "NQ:=NormalClosure(FQ,Group(relatorsQ));;",
    "qProjection:=NaturalHomomorphismByNormalSubgroup(FQ,NQ);;",
    "freeToBase:=GroupHomomorphismByImages(FQ,BQ,FQgens,[bs1,bs2]);;",
    "Image(freeToBase,rel)",
    "Size(Q)<>Size(BQ)",
    "not IsBijective(qToBase)",
)


class CheckStop(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckStop(message)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def strict_q_relators(value: Any) -> list[list[int]]:
    require(isinstance(value, list) and value,
            "fresh worker q_relators are absent")
    result: list[list[int]] = []
    for index, row in enumerate(value):
        require(isinstance(row, list) and row,
                f"fresh worker q_relators[{index}] is empty")
        checked: list[int] = []
        for letter in row:
            require(isinstance(letter, int) and not isinstance(letter, bool) and
                    letter in {-2, -1, 1, 2},
                    f"fresh worker q_relators[{index}] has invalid letter")
            checked.append(letter)
        result.append(checked)
    return result


def verify_worker_output(receipt: dict[str, Any], path: Path) -> None:
    require(path.is_file(), "fresh worker output artifact is absent")
    raw = path.read_bytes()
    require(len(raw) == receipt.get("worker_output_bytes") and
            sha_bytes(raw) == receipt.get("worker_output_sha256"),
            "fresh worker output digest/length mismatch")
    try:
        envelope = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CheckStop("fresh worker output is not one JSON envelope") from exc
    require(isinstance(envelope, dict) and
            envelope.get("schema") == "d972_dovetail_worker/v2" and
            envelope.get("mode") == "base-presentation" and
            envelope.get("status") == "PASS",
            "fresh worker envelope schema/mode/status drift")
    require(envelope.get("universe_id") == EXPECTED_V2_UNIVERSE_ID and
            envelope.get("input_digest") == EXPECTED_V2_INPUT_DIGEST,
            "fresh worker envelope universe/input binding drift")
    for key in ("payload_sha256", "checkpoint_sha256"):
        require(isinstance(envelope.get(key), str) and
                SHA_RE.fullmatch(envelope[key]),
                f"fresh worker envelope {key} malformed")
    payload = envelope.get("payload")
    require(isinstance(payload, dict) and
            payload.get("schema") == "d972_dovetail_worker/v1" and
            payload.get("mode") == "base-presentation" and
            payload.get("status") == "PASS" and
            payload.get("q_order") == 8817984 and
            payload.get("qbar_size") == 8817984 and
            payload.get("fp_generator_count") == 2 and
            payload.get("braid") is True,
            "fresh worker payload exact base gate drift")
    q_relators = strict_q_relators(payload.get("q_relators"))
    require(payload.get("fp_relators") == q_relators and
            payload.get("fp_relator_count") == len(q_relators),
            "fresh worker payload relator binding drift")
    require(receipt.get("worker_universe_id") == EXPECTED_V2_UNIVERSE_ID and
            receipt.get("worker_input_digest") == EXPECTED_V2_INPUT_DIGEST and
            receipt.get("worker_payload_sha256") == envelope["payload_sha256"] and
            receipt.get("worker_checkpoint_sha256") == envelope["checkpoint_sha256"] and
            receipt.get("worker_q_relators_sha256") ==
            sha_bytes(canonical_bytes(q_relators)),
            "fresh worker receipt/envelope binding drift")


def verify(receipt_path: Path, script_path: Path | None = None,
           worker_output_path: Path | None = None) -> dict[str, Any]:
    require(receipt_path.is_file(), "diagnostic receipt is absent")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    require(isinstance(receipt, dict) and receipt.get("schema") == SCHEMA,
            "diagnostic receipt schema drift")
    claimed = receipt.get("receipt_sha256")
    body = copy.deepcopy(receipt)
    body.pop("receipt_sha256", None)
    require(isinstance(claimed, str) and SHA_RE.fullmatch(claimed) and
            claimed == sha_bytes(canonical_bytes(body)),
            "diagnostic receipt digest mismatch")
    status = receipt.get("status")
    require(status in {"CALIBRATION_UNKNOWN_GAP_EXIT",
                       "CALIBRATION_PASS_CANDIDATE", "DIAGNOSTIC_STOP"},
            "diagnostic receipt status is not fail-closed v4")
    require(receipt.get("terminal_authority") in {
        "UNKNOWN_ONLY", "UNKNOWN_ONLY_UNTIL_V2_CALIBRATION_PASS",
    }, "diagnostic terminal authority drift")
    source_mode = receipt.get("source_mode")
    require(source_mode in {"state-artifact", "fresh-frozen-v2"},
            "diagnostic source mode is absent or invalid")
    if source_mode == "fresh-frozen-v2":
        require("source_state_sha256" not in receipt,
                "fresh diagnostic receipt unexpectedly binds a state artifact")
        require(receipt.get("v2_worker_sha256") == EXPECTED_V2_WORKER_SHA256,
                "fresh diagnostic v2 worker binding drift")
        require(V2_WORKER.is_file() and sha_file(V2_WORKER) ==
                EXPECTED_V2_WORKER_SHA256,
                "checked-out frozen v2 worker digest drift")
        require(receipt.get("frozen_worker_mode") == "base-presentation",
                "fresh diagnostic worker mode drift")
        for key in ("worker_source_sha256", "worker_stdout_sha256",
                    "worker_stderr_sha256"):
            value = receipt.get(key)
            require(isinstance(value, str) and SHA_RE.fullmatch(value),
                    f"fresh diagnostic {key} malformed")
        require(receipt["worker_source_sha256"] == EXPECTED_V2_WORKER_SHA256,
                "fresh diagnostic worker source binding drift")
        require(isinstance(receipt.get("worker_returncode"), int) or
                receipt.get("worker_returncode") is None,
                "fresh diagnostic worker return code malformed")
        for stream in ("stdout", "stderr"):
            require(isinstance(receipt.get(f"worker_{stream}_bytes"), int) and
                    receipt[f"worker_{stream}_bytes"] >= 0 and
                    isinstance(receipt.get(f"worker_{stream}_excerpt"), str) and
                    len(receipt[f"worker_{stream}_excerpt"]) <= MAX_EXCERPT_CHARS,
                    f"fresh diagnostic worker {stream} capture missing")
        present = receipt.get("worker_output_present")
        require(isinstance(present, bool),
                "fresh diagnostic worker output presence missing")
        if present:
            require(isinstance(receipt.get("worker_output_sha256"), str) and
                    SHA_RE.fullmatch(receipt["worker_output_sha256"]) and
                    isinstance(receipt.get("worker_output_bytes"), int) and
                    receipt["worker_output_bytes"] > 0 and
                    isinstance(receipt.get("worker_output_excerpt"), str) and
                    len(receipt["worker_output_excerpt"]) <= MAX_EXCERPT_CHARS,
                    "fresh diagnostic worker output capture malformed")
            require(worker_output_path is not None,
                    "fresh diagnostic worker output artifact was not supplied")
            verify_worker_output(receipt, worker_output_path)
        else:
            require(worker_output_path is None or not worker_output_path.is_file(),
                    "fresh diagnostic claims no worker output but artifact exists")
    else:
        require(isinstance(receipt.get("source_state_sha256"), str) and
                SHA_RE.fullmatch(receipt["source_state_sha256"]),
                "state diagnostic receipt source state digest missing")
    for key in ("source_state_sha256", "v2_checker_sha256",
                "v2_manifest_sha256", "q_relators_sha256",
                "target_key_order_sha256", "script_sha256"):
        if key in receipt:
            require(isinstance(receipt[key], str) and SHA_RE.fullmatch(receipt[key]),
                    f"diagnostic receipt {key} malformed")
    if "v2_checker_sha256" in receipt:
        require(receipt["v2_checker_sha256"] == EXPECTED_V2_CHECKER_SHA256,
                "diagnostic v2 checker binding drift")
    if "v2_manifest_sha256" in receipt:
        require(receipt["v2_manifest_sha256"] == EXPECTED_V2_MANIFEST_SHA256,
                "diagnostic v2 manifest binding drift")
    for stream in ("stdout", "stderr"):
        excerpt = receipt.get(f"{stream}_excerpt")
        require(isinstance(excerpt, str) and len(excerpt) <= MAX_EXCERPT_CHARS,
                f"diagnostic {stream} excerpt is not bounded")
        require(isinstance(receipt.get(f"{stream}_bytes"), int) and
                receipt[f"{stream}_bytes"] >= 0 and
                isinstance(receipt.get(f"{stream}_sha256"), str) and
                SHA_RE.fullmatch(receipt[f"{stream}_sha256"]),
                f"diagnostic {stream} digest/length missing")
    if status == "CALIBRATION_UNKNOWN_GAP_EXIT":
        require(isinstance(receipt.get("returncode"), int) and
                receipt["returncode"] != 0,
                "nonzero calibration status lacks nonzero GAP return code")
        require(set(receipt.get("failure_preserves", [])) >= {
            "script_sha256", "stdout_sha256", "stderr_sha256",
            "stdout_excerpt", "stderr_excerpt",
        }, "nonzero calibration receipt lost bounded diagnostics")
    if status == "CALIBRATION_PASS_CANDIDATE":
        require(receipt.get("returncode") == 0,
                "pass candidate has nonzero GAP return code")
    if script_path is not None and script_path.is_file():
        script = script_path.read_text(encoding="ascii")
        require(receipt.get("script_sha256") == sha_file(script_path),
                "generated script digest mismatch")
        require("{qrels}" not in script and
                "relatorsQ:=MakeRels(FQ," in script,
                "generated script has an unsubstituted/absent qrels block")
        for marker in FIXED_MARKERS:
            require(marker in script, f"generated script missing gate: {marker}")
        require("calibration presentation/base mismatch" not in script,
                "old single-gate qToBase block survived")
    elif status != "DIAGNOSTIC_STOP":
        raise CheckStop("non-stop diagnostic receipt lacks generated script")
    return receipt


def self_test() -> int:
    script = ("relatorsQ:=MakeRels(FQ,[[1,-2],[2,-1]]);;\n" +
              "\n".join(FIXED_MARKERS) + "\n")
    body = {
        "schema": SCHEMA,
        "status": "CALIBRATION_UNKNOWN_GAP_EXIT",
        "terminal_authority": "UNKNOWN_ONLY",
        "source_mode": "state-artifact",
        "source_state_sha256": "a" * 64,
        "v2_checker_sha256": EXPECTED_V2_CHECKER_SHA256,
        "v2_manifest_sha256": EXPECTED_V2_MANIFEST_SHA256,
        "q_relators_sha256": "b" * 64,
        "target_key_order_sha256": "c" * 64,
        "script_sha256": sha_bytes(script.encode("ascii")),
        "returncode": 1,
        "stdout_bytes": 3,
        "stderr_bytes": 3,
        "stdout_sha256": sha_bytes(b"out"),
        "stderr_sha256": sha_bytes(b"err"),
        "stdout_excerpt": "out",
        "stderr_excerpt": "err",
        "failure_preserves": ["script_sha256", "stdout_sha256", "stderr_sha256",
                              "stdout_excerpt", "stderr_excerpt"],
    }
    body["receipt_sha256"] = sha_bytes(canonical_bytes(body))
    with tempfile.TemporaryDirectory(prefix="d972-calibration-check-") as directory:
        root = Path(directory)
        receipt = root / "receipt.json"
        script_path = root / "generated.g"
        receipt.write_text(json.dumps(body, sort_keys=True) + "\n", encoding="utf-8")
        script_path.write_text(script, encoding="ascii", newline="\n")
        verify(receipt, script_path)
        bad_script_path = root / "bad-generated.g"
        bad_script_path.write_text(script.replace(
            "[[1,-2],[2,-1]]", "{qrels}"), encoding="ascii", newline="\n")
        bad_receipt = copy.deepcopy(body)
        bad_receipt["script_sha256"] = sha_file(bad_script_path)
        bad_receipt["receipt_sha256"] = sha_bytes(canonical_bytes(
            {key: value for key, value in bad_receipt.items()
             if key != "receipt_sha256"}))
        bad_receipt_path = root / "bad-receipt.json"
        bad_receipt_path.write_text(json.dumps(bad_receipt, sort_keys=True) +
                                    "\n", encoding="utf-8")
        try:
            verify(bad_receipt_path, bad_script_path)
        except CheckStop:
            pass
        else:
            raise CheckStop("self-test accepted unsubstituted qrels placeholder")
        tampered = copy.deepcopy(body)
        tampered["stderr_excerpt"] = "tampered"
        receipt.write_text(json.dumps(tampered, sort_keys=True) + "\n", encoding="utf-8")
        try:
            verify(receipt, script_path)
        except CheckStop:
            pass
        else:
            raise CheckStop("self-test accepted tampered receipt")
    print(json.dumps({
        "schema": SCHEMA, "status": "PASS", "bounded_excerpt_gate": True,
        "receipt_hash_gate": True, "script_binding_gate": True,
        "tamper_negative": True,
    }, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["--self-test"]:
        return self_test()
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--script", type=Path)
    parser.add_argument("--worker-output", type=Path)
    parsed = parser.parse_args(args)
    verified = verify(parsed.receipt, parsed.script, parsed.worker_output)
    print(f"VERIFIED_CALIBRATION_RECEIPT {verified['receipt_sha256']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckStop, OSError, ValueError, KeyError, TypeError,
            json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
