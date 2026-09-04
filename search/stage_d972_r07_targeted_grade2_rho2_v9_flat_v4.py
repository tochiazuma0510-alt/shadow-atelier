#!/usr/bin/env python3
"""Offline, fail-closed stager for the accepted Task640 rho2-v9 artifact.

The input is the exact directory shape emitted by actions/download-artifact:
``task640-payload/`` plus ``task640-verdict.json``.  The output is a fresh
flat directory for the targeted grade-two consumer.  This executable has no
GitHub client, credential lookup, or directory-name provenance shortcut.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any


ACQUISITION_SCHEMA = "d972.r07.targeted-grade2.rho2-v9.acquisition.v1"
ACQUISITION_FIELDS = {
    "schema": ACQUISITION_SCHEMA,
    "repository": "tochiazuma0510-alt/shadow-atelier",
    "run_id": 33839962829,
    "run_attempt": 1,
    "head_sha": "17a8439c766d92719d7ae7d35846ea444da598fa",
    "workflow_path": ".github/workflows/d972-r07-a0-fresh-precision2-endpoint-v17.yml",
    "workflow_id": 349904905,
    "event": "push",
    "conclusion": "success",
    "artifact_id": 9925190479,
    "artifact_name": "task640-fresh-rho2-v17-33839962829-1",
    "artifact_archive_bytes": 6049643,
    "artifact_digest": "sha256:01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4",
}

PAYLOAD_SCHEMA = "d972.r07.a0.fresh-precision2-endpoint-signature.v9"
PAYLOAD_MARKER = "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CANDIDATE"
CHECKER_SCHEMA = "d972.r07.a0.fresh-precision2-endpoint-signature.v9.checker"
CHECKER_MARKER = "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CHECKER_PASS"
MANIFEST_BYTES = 26047
MANIFEST_SHA256 = "55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488"
VERDICT_BYTES = 418
VERDICT_SHA256 = "cdf0654738a10acf59844df3b9dda5ab8efdf2e387bba7d69b691a4ad46b2848"
PAYLOAD_RECEIPTS = {
    "rho2_packed": {"file": "rho2.bin", "bytes": 12096,
                    "sha256": "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e"},
    "rho2_dense": {"file": "rho2-dense.bin", "bytes": 48384,
                   "sha256": "abfafbc7521af43c75f1b5a73a6da5d37b90ec1648b649401d684a58cf16752e"},
    "lower_dense": {"file": "lower-dense.bin", "bytes": 32260,
                    "sha256": "c5657f998c12426cb1f2c1b4ae1e3a99ce4df9d61101eb33fba7921303bb4830"},
    "target_dense": {"file": "target-dense.bin", "bytes": 80644,
                     "sha256": "122dca3cf3dc3299214f1ba4c2bc5b82dbe64e510f8aef482329316c2a935ea2"},
    "path_signatures": {"file": "path-signatures.json", "bytes": 28393211,
                        "sha256": "ef7fbd1d44647c058b33a1c18894ff5411dcd7870e7cf7e24b6763b68557ab25"},
    "signature_buckets": {"file": "signature-buckets.json", "bytes": 46469668,
                          "sha256": "e67876dce3bb144ad6afa4895236c8fc37fbc0488c135f9903d8288039829c43"},
    "roots": {"file": "authenticated-roots.json", "bytes": 255846,
              "sha256": "af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5"},
}
PAYLOAD_DIR = "task640-payload"
INPUT_VERDICT = "task640-verdict.json"
OUTPUT_ROSTER = tuple(sorted(
    ["manifest.json", INPUT_VERDICT, "acquisition.json"] +
    [record["file"] for record in PAYLOAD_RECEIPTS.values()]))
CHUNK_BYTES = 1 << 20
SMALL_JSON_CAP = 2 * 1024 * 1024


def fail(reason: str) -> None:
    raise RuntimeError(reason)


def require(condition: bool, reason: str) -> None:
    if not condition:
        fail(reason)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                        ensure_ascii=True) + "\n").encode("ascii")


def safe_child(root: Path, name: str) -> Path:
    """Join one exact basename; no traversal or directory-name trust."""
    require(isinstance(name, str) and name and Path(name).name == name and
            name not in (".", "..") and "\\" not in name and "/" not in name,
            "unsafe_basename")
    return root / name


def regular(path: Path) -> os.stat_result:
    info = path.lstat()
    require(not stat.S_ISLNK(info.st_mode) and stat.S_ISREG(info.st_mode),
            "unsafe_file:" + str(path))
    return info


def directory(path: Path) -> os.stat_result:
    info = path.lstat()
    require(not stat.S_ISLNK(info.st_mode) and stat.S_ISDIR(info.st_mode),
            "unsafe_directory:" + str(path))
    return info


def exact_roster(path: Path, names: list[str], reason: str) -> None:
    directory(path)
    actual = sorted(entry.name for entry in path.iterdir())
    require(actual == sorted(names), reason + ":roster")


def stream_receipt(path: Path, expected: dict[str, Any], reason: str,
                   cap: int | None = None) -> dict[str, Any]:
    """Hash one source exactly once with a bounded buffer."""
    info = regular(path)
    expected_bytes = expected.get("bytes")
    expected_sha = expected.get("sha256")
    require(isinstance(expected_bytes, int) and expected_bytes >= 0 and
            isinstance(expected_sha, str) and len(expected_sha) == 64,
            reason + ":expected")
    if cap is not None:
        require(expected_bytes <= cap, "UNKNOWN_RESOURCE:" + reason + ":cap")
    require(info.st_size == expected_bytes, reason + ":size")
    hasher = hashlib.sha256()
    total = 0
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(CHUNK_BYTES)
            if not chunk:
                break
            total += len(chunk)
            hasher.update(chunk)
    after = path.stat()
    require(total == expected_bytes and hasher.hexdigest() == expected_sha and
            after.st_size == info.st_size and
            after.st_mtime_ns == info.st_mtime_ns,
            reason + ":digest")
    return {"file": expected["file"], "bytes": total,
            "sha256": hasher.hexdigest()}


def small_json(path: Path, expected_bytes: int, expected_sha: str,
               reason: str) -> tuple[dict[str, Any], bytes]:
    info = regular(path)
    require(info.st_size == expected_bytes and expected_bytes <= SMALL_JSON_CAP,
            reason + ":size")
    raw = path.read_bytes()
    require(len(raw) == expected_bytes and sha(raw) == expected_sha,
            reason + ":digest")
    try:
        value = json.loads(raw.decode("ascii"))
    except (UnicodeError, ValueError) as exc:
        raise RuntimeError(reason + ":json") from exc
    require(isinstance(value, dict) and canonical(value) == raw,
            reason + ":canonical")
    return value, raw


def validate_acquisition(path: Path) -> tuple[dict[str, Any], bytes]:
    expected = canonical(ACQUISITION_FIELDS)
    value, raw = small_json(path, len(expected), sha(expected),
                            "acquisition")
    require(value == ACQUISITION_FIELDS, "acquisition:fields")
    return value, raw


def validate_input_roster(root: Path, contract: dict[str, Any] | None = None
                          ) -> dict[str, Path]:
    root = root.absolute()
    records = PAYLOAD_RECEIPTS if contract is None else contract["payload_receipts"]
    directory(root)
    exact_roster(root, [PAYLOAD_DIR, INPUT_VERDICT], "input")
    payload = safe_child(root, PAYLOAD_DIR)
    exact_roster(payload, ["manifest.json"] +
                 [record["file"] for record in records.values()],
                 "payload")
    paths = {"manifest": safe_child(payload, "manifest.json"),
             "verdict": safe_child(root, INPUT_VERDICT)}
    for key, record in records.items():
        paths[key] = safe_child(payload, record["file"])
    for path in paths.values():
        regular(path)
    return paths


def validate_input(root: Path, contract: dict[str, Any] | None = None
                   ) -> tuple[dict[str, Path], dict[str, Any], bytes,
                              dict[str, Any], bytes]:
    expected_manifest_bytes = MANIFEST_BYTES if contract is None else contract[
        "manifest_bytes"]
    expected_manifest_sha = MANIFEST_SHA256 if contract is None else contract[
        "manifest_sha256"]
    expected_verdict_bytes = VERDICT_BYTES if contract is None else contract[
        "verdict_bytes"]
    expected_verdict_sha = VERDICT_SHA256 if contract is None else contract[
        "verdict_sha256"]
    records = PAYLOAD_RECEIPTS if contract is None else contract["payload_receipts"]
    paths = validate_input_roster(root, contract)
    manifest, manifest_raw = small_json(paths["manifest"], expected_manifest_bytes,
                                        expected_manifest_sha, "manifest")
    require(manifest.get("schema") == PAYLOAD_SCHEMA and
            manifest.get("marker") == PAYLOAD_MARKER and
            manifest.get("files") == records,
            "manifest:v9_contract")
    verdict, verdict_raw = small_json(paths["verdict"], expected_verdict_bytes,
                                      expected_verdict_sha, "verdict")
    packed = records["rho2_packed"]
    lower_checked = (32260 if contract is None else
                     contract["lower_coordinates_checked"])
    top_checked = (48384 if contract is None else
                   contract["top_coordinates_checked"])
    require(verdict.get("schema") == CHECKER_SCHEMA and
            verdict.get("marker") == CHECKER_MARKER and
            verdict.get("payload_manifest_sha256") == expected_manifest_sha and
            verdict.get("rho2_sha256") == packed["sha256"] and
            verdict.get("lower_coordinates_checked") == lower_checked and
            verdict.get("top_coordinates_checked") == top_checked and
            verdict.get("cross_checked") is False and
            verdict.get("verified") is False,
            "verdict:v9_contract")
    # Payload bytes are authenticated by the single bounded copy/hash pass in
    # ``stage_flat``.  Avoid a preflight hash here: a second traversal would
    # add no assurance and would defeat the streaming boundary.
    return paths, manifest, manifest_raw, verdict, verdict_raw


def destination_absent(path: Path) -> None:
    try:
        path.lstat()
    except FileNotFoundError:
        return
    fail("output_exists")


def fsync_directory(path: Path) -> None:
    """Best-effort directory barrier; rename remains same-volume atomic."""
    try:
        descriptor = os.open(str(path), os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    except OSError:
        pass
    finally:
        os.close(descriptor)


def copy_stream(source: Path, destination: Path, expected: dict[str, Any],
                reason: str) -> dict[str, Any]:
    """Copy and authenticate one file without retaining its contents."""
    source_info = regular(source)
    require(source_info.st_size == expected["bytes"], reason + ":size")
    destination.parent.mkdir(parents=True, exist_ok=True)
    hasher = hashlib.sha256()
    total = 0
    with source.open("rb") as inp, destination.open("xb") as out:
        while True:
            chunk = inp.read(CHUNK_BYTES)
            if not chunk:
                break
            out.write(chunk)
            total += len(chunk)
            hasher.update(chunk)
        out.flush()
        os.fsync(out.fileno())
    after = source.stat()
    require(total == expected["bytes"] and hasher.hexdigest() ==
            expected["sha256"] and after.st_size == source_info.st_size and
            after.st_mtime_ns == source_info.st_mtime_ns,
            reason + ":digest")
    return {"file": destination.name, "bytes": total,
            "sha256": hasher.hexdigest()}


def write_bytes(destination: Path, raw: bytes, reason: str) -> dict[str, Any]:
    with destination.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return {"file": destination.name, "bytes": len(raw), "sha256": sha(raw)}


def output_roster(root: Path, roster: tuple[str, ...] = OUTPUT_ROSTER) -> None:
    exact_roster(root, list(roster), "output")
    for name in roster:
        regular(safe_child(root, name))


def stage_flat(input_root: Path, output_root: Path,
               acquisition_path: Path, contract: dict[str, Any] | None = None,
               trace: dict[str, Any] | None = None) -> dict[str, Any]:
    """Validate, stream-copy, then atomically promote one fresh flat root."""
    output = output_root.absolute()
    destination_absent(output)
    parent = output.parent
    parent.mkdir(parents=True, exist_ok=True)
    directory(parent)
    paths, _manifest, manifest_raw, _verdict, verdict_raw = validate_input(
        input_root.absolute(), contract)
    if trace is not None:
        trace["validate_input_reached"] = True
    _acquisition, acquisition_raw = validate_acquisition(
        acquisition_path.absolute())
    staging = Path(tempfile.mkdtemp(prefix="." + output.name + ".stage-",
                                    dir=str(parent)))
    try:
        receipts: dict[str, dict[str, Any]] = {}
        # The two envelopes are bounded (26,047 and 418 bytes), so retain the
        # already authenticated bytes rather than hashing either envelope a
        # second time during promotion.
        receipts["manifest"] = write_bytes(
            safe_child(staging, "manifest.json"), manifest_raw,
            "stage:manifest")
        records = PAYLOAD_RECEIPTS if contract is None else contract[
            "payload_receipts"]
        for key, expected in records.items():
            receipts[key] = copy_stream(
                paths[key], safe_child(staging, expected["file"]), expected,
                "stage:" + key)
            if trace is not None:
                trace["copy_calls"] = int(trace.get("copy_calls", 0)) + 1
        receipts["verdict"] = write_bytes(
            safe_child(staging, INPUT_VERDICT), verdict_raw,
            "stage:verdict")
        receipts["acquisition"] = write_bytes(
            safe_child(staging, "acquisition.json"), acquisition_raw,
            "stage:acquisition")
        roster = OUTPUT_ROSTER if contract is None else contract["output_roster"]
        output_roster(staging, roster)
        fsync_directory(staging)
        destination_absent(output)
        os.rename(staging, output)
        if trace is not None:
            trace["promotion_reached"] = True
        fsync_directory(parent)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        raise
    return {
        "schema": "d972.r07.targeted-grade2.rho2-v9.flat-stage.v2",
        "input_layout": [PAYLOAD_DIR + "/manifest.json",
                         PAYLOAD_DIR + "/<seven manifest-listed files>",
                         INPUT_VERDICT],
        "output_roster": list(OUTPUT_ROSTER),
        "manifest": receipts["manifest"],
        "payload": [receipts[key] for key in (PAYLOAD_RECEIPTS if contract is None
                                               else contract["payload_receipts"])],
        "verdict": receipts["verdict"],
        "acquisition": receipts["acquisition"],
        "acquisition_schema": ACQUISITION_SCHEMA,
        "atomic_promotion": "same-volume directory rename; destination must be absent",
        "staged_output_bytes": len(manifest_raw) + len(verdict_raw) +
                               sum(record["bytes"] for record in records.values()) +
                               len(acquisition_raw),
    }


def _expect_reject(call: Any) -> None:
    try:
        call()
    except (RuntimeError, OSError, ValueError):
        return
    fail("fixture_accept")


def _fixture_contract() -> dict[str, Any]:
    """Return a tiny dependency-injected contract with production shapes."""
    payload = {
        "rho2_packed": bytes((1, 0, 0)),
        "rho2_dense": bytes((1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
        "lower_dense": bytes(4),
        "target_dense": bytes((2, 1, 0, 2)),
        "path_signatures": b"{}\n",
        "signature_buckets": b"[]\n",
        "roots": canonical({"C_1": {"type": "Compose", "left": "C_<1",
                                       "right": "C_T"}}),
    }
    records = {key: {"file": PAYLOAD_RECEIPTS[key]["file"],
                     "bytes": len(raw), "sha256": sha(raw)}
               for key, raw in payload.items()}
    manifest_raw = canonical({"schema": PAYLOAD_SCHEMA,
                              "marker": PAYLOAD_MARKER, "files": records})
    verdict_raw = canonical({"schema": CHECKER_SCHEMA,
                             "marker": CHECKER_MARKER,
                             "payload_manifest_sha256": sha(manifest_raw),
                             "rho2_sha256": records["rho2_packed"]["sha256"],
                             "lower_coordinates_checked": 4,
                             "top_coordinates_checked": 12,
                             "cross_checked": False, "verified": False})
    output_roster = tuple(sorted(["manifest.json", INPUT_VERDICT,
                                  "acquisition.json"] +
                                 [record["file"] for record in records.values()]))
    return {"payload": payload, "payload_receipts": records,
            "manifest": manifest_raw, "manifest_bytes": len(manifest_raw),
            "manifest_sha256": sha(manifest_raw), "verdict": verdict_raw,
            "verdict_bytes": len(verdict_raw), "verdict_sha256": sha(verdict_raw),
            "lower_coordinates_checked": 4, "top_coordinates_checked": 12,
            "output_roster": output_roster}


def _write_fixture_input(root: Path, contract: dict[str, Any],
                         acquisition: bytes) -> None:
    payload = root / PAYLOAD_DIR
    payload.mkdir(parents=True)
    (payload / "manifest.json").write_bytes(contract["manifest"])
    for key, raw in contract["payload"].items():
        (payload / contract["payload_receipts"][key]["file"]).write_bytes(raw)
    (root / INPUT_VERDICT).write_bytes(contract["verdict"])


def _default_branch_fixture(expected_acquisition: bytes) -> dict[str, Any]:
    """Reach promotion and normal return with ``contract=None`` cheaply."""
    fixture = _fixture_contract()
    verdict = json.loads(fixture["verdict"].decode("ascii"))
    verdict["lower_coordinates_checked"] = 32260
    verdict["top_coordinates_checked"] = 48384
    verdict_raw = canonical(verdict)
    fixture = dict(fixture)
    fixture.update({"verdict": verdict_raw, "verdict_bytes": len(verdict_raw),
                    "verdict_sha256": sha(verdict_raw)})
    saved = {name: globals()[name] for name in (
        "MANIFEST_BYTES", "MANIFEST_SHA256", "VERDICT_BYTES",
        "VERDICT_SHA256", "PAYLOAD_RECEIPTS", "OUTPUT_ROSTER")}
    try:
        globals().update({"MANIFEST_BYTES": fixture["manifest_bytes"],
                          "MANIFEST_SHA256": fixture["manifest_sha256"],
                          "VERDICT_BYTES": fixture["verdict_bytes"],
                          "VERDICT_SHA256": fixture["verdict_sha256"],
                          "PAYLOAD_RECEIPTS": fixture["payload_receipts"],
                          "OUTPUT_ROSTER": fixture["output_roster"]})
        with tempfile.TemporaryDirectory(
                prefix="rho2-v9-stage-default-fixture-") as temp:
            base = Path(temp)
            input_root = base / "input"
            _write_fixture_input(input_root, fixture, expected_acquisition)
            acquisition = base / "acquisition.json"
            acquisition.write_bytes(expected_acquisition)
            output = base / "flat"
            trace: dict[str, Any] = {}
            result = stage_flat(input_root, output, acquisition,
                                contract=None, trace=trace)
            require(trace.get("copy_calls") == len(fixture["payload"]) and
                    trace.get("promotion_reached") is True and output.is_dir(),
                    "fixture_default_branch_promotion")
            expected_bytes = (len(fixture["manifest"]) + len(verdict_raw) +
                              sum(len(raw) for raw in fixture["payload"].values()) +
                              len(expected_acquisition))
            require(result["staged_output_bytes"] == expected_bytes and
                    result["output_roster"] == list(fixture["output_roster"]),
                    "fixture_default_branch_return")
            return {"promoted": True, "returned": True,
                    "staged_output_bytes": expected_bytes}
    finally:
        globals().update(saved)


def selftest() -> None:
    """Exercise the reached production staging path with tiny bytes."""
    expected_acquisition = canonical(ACQUISITION_FIELDS)
    require(len(expected_acquisition) > 0 and
            json.loads(expected_acquisition.decode("ascii")) ==
            ACQUISITION_FIELDS, "fixture_acquisition_canonical")
    for key in ACQUISITION_FIELDS:
        altered = dict(ACQUISITION_FIELDS)
        altered[key] = ("mutated" if isinstance(altered[key], str)
                        else int(altered[key]) + 1)
        require(altered != ACQUISITION_FIELDS, "fixture_acquisition_copy")

    default_branch = _default_branch_fixture(expected_acquisition)
    contract = _fixture_contract()
    require(contract["lower_coordinates_checked"] == 4 and
            contract["top_coordinates_checked"] == 12,
            "fixture_contract_dimensions")
    with tempfile.TemporaryDirectory(prefix="rho2-v9-stage-fixture-") as temp:
        base = Path(temp)
        input_root = base / "input"
        _write_fixture_input(input_root, contract, expected_acquisition)
        acq_path = base / "acquisition.json"
        acq_path.write_bytes(expected_acquisition)
        paths = validate_input_roster(input_root, contract)
        require(paths["manifest"].name == "manifest.json" and
                paths["verdict"].name == INPUT_VERDICT, "fixture_flat_input")
        validate_acquisition(acq_path)
        for key, old in ACQUISITION_FIELDS.items():
            altered = dict(ACQUISITION_FIELDS)
            altered[key] = ((old + 1) if isinstance(old, int)
                            else ("mutated" if key != "schema"
                                  else ACQUISITION_SCHEMA + ".mutated"))
            acq_path.write_bytes(canonical(altered))
            _expect_reject(lambda: validate_acquisition(acq_path))
        acq_path.write_bytes(expected_acquisition)

        # One-byte mutations run through production validate_input/small_json
        # or copy_stream, rather than an unused receipt helper.
        positive_trace: dict[str, Any] = {}
        positive = stage_flat(input_root, base / "flat", acq_path, contract,
                              positive_trace)
        require(positive_trace.get("validate_input_reached") is True and
                positive_trace.get("copy_calls") == len(contract["payload"]) and
                positive_trace.get("promotion_reached") is True and
                (base / "flat").is_dir(), "fixture_positive_reached")
        for key, raw in contract["payload"].items():
            staged_name = contract["payload_receipts"][key]["file"]
            require((base / "flat" / staged_name).read_bytes() == raw,
                    "fixture_payload_bytes:" + key)
        require((base / "flat" / "manifest.json").read_bytes() ==
                contract["manifest"] and
                (base / "flat" / INPUT_VERDICT).read_bytes() ==
                contract["verdict"] and
                (base / "flat" / "acquisition.json").read_bytes() ==
                expected_acquisition and
                positive["output_roster"] == list(contract["output_roster"]),
                "fixture_flat_bytes_receipts")

        # Rebuild the input for every attempt so every rejection has a fresh
        # absent destination and can be checked for false promotion.
        for label, rel in (("manifest", Path(PAYLOAD_DIR) / "manifest.json"),
                           ("verdict", Path(INPUT_VERDICT))):
            candidate = input_root / rel
            original = candidate.read_bytes()
            candidate.write_bytes(original[:-1] + bytes((original[-1] ^ 1,)))
            trace: dict[str, Any] = {}
            _expect_reject(lambda trace=trace: stage_flat(
                input_root, base / ("reject-" + label), acq_path, contract,
                trace))
            require(trace.get("promotion_reached") is not True and
                    trace.get("copy_calls", 0) == 0,
                    "fixture_no_promotion_" + label)
            candidate.write_bytes(original)
        for key, rel in ((key, Path(PAYLOAD_DIR) /
                          contract["payload_receipts"][key]["file"])
                         for key in contract["payload"]):
            candidate = input_root / rel
            original = candidate.read_bytes()
            candidate.write_bytes(original[:-1] + bytes((original[-1] ^ 1,)))
            trace = {}
            _expect_reject(lambda trace=trace: stage_flat(
                input_root, base / ("reject-" + key), acq_path, contract,
                trace))
            require(trace.get("promotion_reached") is not True and
                    trace.get("copy_calls", 0) < len(contract["payload"]),
                    "fixture_no_promotion_" + key)
            candidate.write_bytes(original)

        # Exact safe roster mutations.
        payload = input_root / PAYLOAD_DIR
        extra = payload / "extra.bin"
        extra.write_bytes(b"x")
        _expect_reject(lambda: validate_input_roster(input_root))
        extra.unlink()
        missing = payload / contract["payload_receipts"]["rho2_packed"]["file"]
        missing.unlink()
        _expect_reject(lambda: validate_input_roster(input_root))
        missing.write_bytes(b"x")
        nested = payload / "nested"
        nested.mkdir()
        _expect_reject(lambda: validate_input_roster(input_root))
        nested.rmdir()
        _expect_reject(lambda: safe_child(payload, "../escape"))

        link_result = "SKIPPED_NO_SYMLINK_PRIVILEGE"
        link = payload / "rho2.bin"
        try:
            missing.unlink()
            os.symlink(str(missing), str(link))
        except (OSError, NotImplementedError):
            if link.is_symlink():
                link.unlink()
            missing.write_bytes(b"x")
        else:
            link_result = "PASS"
            _expect_reject(lambda: validate_input_roster(input_root))
            link.unlink()
            missing.write_bytes(b"x")

        # An existing destination is never overwritten, even before source
        # validation can spend time on large files.
        existing = base / "existing"
        existing.mkdir()
        existing_trace: dict[str, Any] = {}
        _expect_reject(lambda: stage_flat(input_root, existing, acq_path,
                                          contract, existing_trace))
        require(existing_trace.get("promotion_reached") is not True and
                existing_trace.get("copy_calls", 0) == 0,
                "fixture_existing_no_success")

        # Acquisition absence and unbound/mutated identity are explicit.
        _expect_reject(lambda: validate_acquisition(base / "absent.json"))
        unbound = base / "unbound.json"
        altered_acq = dict(ACQUISITION_FIELDS)
        altered_acq["artifact_id"] += 1
        unbound.write_bytes(canonical(altered_acq))
        _expect_reject(lambda: validate_acquisition(unbound))

    require(PAYLOAD_SCHEMA.endswith(".v9") and
            CHECKER_SCHEMA.endswith(".v9.checker") and
            PAYLOAD_MARKER.endswith("_V9_CANDIDATE") and
            CHECKER_MARKER.endswith("_V9_CHECKER_PASS"),
            "fixture_v9_tuple")
    print(json.dumps({
        "selftest": "PASS",
        "flat_roster": "PASS",
        "exact_v9_tuple": "PASS",
        "acquisition_schema": ACQUISITION_SCHEMA,
        "acquisition_mutations": "PASS",
        "input_roster_mutations": "PASS",
        "manifest_verdict_payload_mutations": "PASS",
        "nested_unflattened_extra_missing_traversal": "PASS",
        "link_mutation": link_result,
        "overwrite_rejected": "PASS",
        "atomic_promotion": "PASS",
        "positive_stage_path": "PASS",
        "negative_no_promotion_success": "PASS",
        "production_default_return": ("PASS" if default_branch["returned"]
                                      else "FAIL"),
        "production_default_promotion": ("PASS" if default_branch["promoted"]
                                         else "FAIL"),
        "staged_output_bytes": default_branch["staged_output_bytes"],
        "production_default_staged_output_bytes": default_branch["staged_output_bytes"],
        "injected_contract_staged_output_bytes": positive["staged_output_bytes"],
        "production_payload_streaming": "one bounded hash/copy pass per listed file",
    }, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--acquisition", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            require(args.input is None and args.output is None and
                    args.acquisition is None, "selftest_arguments")
            selftest()
            return 0
        require(args.input is not None and args.output is not None and
                args.acquisition is not None, "usage")
        result = stage_flat(args.input, args.output, args.acquisition)
        print(json.dumps(result, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc),
                          "verified": False}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
