#!/usr/bin/env python3
"""R07 A4/v6a producer-side physical authority trace.

This is a deliberately small candidate module.  It is independent of the
frozen successor-kernel sources and covers only the first seven authority
owners.  The ordinary route consumes the same physical owner that the
mutation writes; the fixture is consulted only after that route returns.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import stat
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a4-actual-owner-trace/v1"
ROWS = 6441
LAYER_COUNTS = {"Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19}
RECEIPT_NAME = "d972_r07_seven_context_roof_presentation_v1.json"
MANIFEST_NAME = "d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json"
RECEIPT_REL = "ci/in/" + RECEIPT_NAME
MANIFEST_REL = "ci/in/" + MANIFEST_NAME
RECEIPT_BYTES = 31017244
RECEIPT_SHA = "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"
RECEIPT_SELF = "c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f"
MANIFEST_BYTES = 2722
MANIFEST_SHA = "cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"
MANIFEST_SELF = "0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684"

PINS: tuple[tuple[str, int, str], ...] = (
    (RECEIPT_REL, RECEIPT_BYTES, RECEIPT_SHA),
    (MANIFEST_REL, MANIFEST_BYTES, MANIFEST_SHA),
    ("ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt", 81,
     "b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"),
    ("ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt", 95,
     "260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e"),
    ("ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json", 150,
     "ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"),
    ("search/d972_r07_seven_context_roof_presentation_v1.py", 137169,
     "6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"),
    ("crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py", 157253,
     "001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"),
    ("search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g", 20541,
     "6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068"),
)

COORDINATE_WIDTHS = [40, 40, 40, 40, 40, 154, 154, 154, 154, 154]
OCCURRENCE_BLOCKS = ["H1", "H1", "H1", "H2", "H2", "H2", "P1", "P2", "P3", "P5", "P4"]
OCCURRENCE_SIGNS = [1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1]
OCCURRENCE_TEN = [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9]
COORDINATE_LEDGER_SHA = "9f9c081e9653d6e141e4d6d231e2d6db9526850b7ccd33c0859d13825f3fa83c"
OCCURRENCE_LEDGER_SHA = "040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7"

MUTATIONS = (
    "per_layer_ordinal", "authority_binding", "canonical_input_bytes",
    "resolved_path_traversal", "normal_generation_proof",
    "bridge_typed_occurrence_ledger", "evaluator_abi_canary",
)


class InputStop(RuntimeError):
    """Physical input cannot be authenticated or the platform is unsupported."""


class TraceReject(RuntimeError):
    """The ordinary validator's one registered narrow rejection type."""

    def __init__(self, validator: str, stage: str, reason: str):
        self.validator = validator
        self.stage = stage
        self.reason = reason
        super().__init__(reason)


class MutationAccepted(RuntimeError):
    """Raised outside the TraceReject catch when a mutation is accepted."""


class Meter:
    CAPS = {
        "opened_bytes": 250000000, "temporary_bytes": 250000000,
        "canonical_bytes": 500000000, "opens": 256, "writes": 256,
        "events": 10000, "mutations": 7,
    }

    def __init__(self) -> None:
        self.counts = {key: 0 for key in self.CAPS}

    def charge(self, key: str, amount: int = 1) -> None:
        if key not in self.CAPS or type(amount) is not int or amount < 0:
            raise InputStop("producer:meter:registry")
        target = self.counts[key] + amount
        if target > self.CAPS[key]:
            raise InputStop("producer:resource:" + key)
        self.counts[key] = target

    def before_allocation(self, key: str, amount: int) -> None:
        """Reserve a bounded object before any corresponding allocation."""
        if key not in self.CAPS or type(amount) is not int or amount < 0:
            raise InputStop("producer:meter:reserve")
        if self.counts[key] + amount > self.CAPS[key]:
            raise InputStop("producer:resource:" + key)

    def public(self) -> dict[str, Any]:
        return {"caps": dict(self.CAPS), "counts": dict(self.counts),
                "measured": "UNEXECUTED"}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_object(value: Any, meter: Meter | None = None) -> str:
    raw = canonical(value)
    if meter is not None:
        meter.charge("canonical_bytes", len(raw))
    return digest_bytes(raw)


def require(condition: bool, reason: str) -> None:
    if condition is not True:
        raise InputStop(reason)


class EventSink:
    """Events are emitted before the ordinary validator reads its owner."""

    def __init__(self, meter: Meter):
        self.meter = meter
        self.events: list[dict[str, Any]] = []
        self._observed: dict[str, dict[str, Any]] = {}
        self.canonical_after: dict[str, str] = {}
        self.terminal_count = 0

    @property
    def observed(self) -> dict[str, dict[str, Any]]:
        return self._observed

    def enter(self, validator: str, stage: str, owner: str) -> None:
        self.meter.charge("events")
        self.events.append({"ordinal": len(self.events) + 1,
                            "validator": validator, "stage": stage,
                            "owner": owner})

    def digest(self) -> str:
        return digest_object(self.events, self.meter)

    def terminal(self) -> None:
        self.terminal_count += 1


def _stat_identity(path: Path, kind: str, raw: bytes | None = None) -> dict[str, Any]:
    # Keep the lexical pathname for lstat/open identity; resolving here
    # would follow a symlink before O_NOFOLLOW had a chance to reject it.
    resolved = Path(os.path.abspath(path))
    try:
        info = os.lstat(resolved)
    except FileNotFoundError:
        return {"identity_kind": kind, "path": str(resolved), "exists": False,
                "type": "missing", "bytes": None, "sha256": None,
                "device": None, "inode": None, "nlink": None,
                "single_open_handle": False, "opened_handle_stable": False,
                "pathname_matches_opened_handle": False,
                "substitution_detected": False}
    regular = stat.S_ISREG(info.st_mode)
    return {"identity_kind": kind, "path": str(resolved), "exists": True,
            "type": "regular" if regular else "nonregular",
            "bytes": int(info.st_size) if regular else None,
            "sha256": digest_bytes(raw) if raw is not None else None,
            "device": int(info.st_dev), "inode": int(info.st_ino),
            "nlink": int(info.st_nlink), "single_open_handle": False,
            "opened_handle_stable": False,
            "pathname_matches_opened_handle": False,
            "substitution_detected": False}


def _same_open_identity(before: os.stat_result, after: os.stat_result,
                        pathname: os.stat_result) -> bool:
    fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns")
    return all(getattr(before, field) == getattr(after, field) ==
               getattr(pathname, field) for field in fields)


class PhysicalStore:
    """One-handle POSIX reader with no-follow and post-read identity checks."""

    def __init__(self, meter: Meter):
        self.meter = meter
        self.cache: dict[str, tuple[bytes, dict[str, Any]]] = {}

    def read(self, path: Path, role: str, *, expected: tuple[int, str] | None = None,
             owner_kind: str = "file", session: EventSink | None = None) -> tuple[bytes, dict[str, Any]]:
        resolved = Path(os.path.abspath(path))
        key = str(resolved)
        if key in self.cache:
            cached = self.cache[key]
            if session is not None:
                session.observed[role] = cached[1]
            return cached
        if os.name == "nt":
            raise InputStop("producer:windows:one_handle_reparse_unsupported")
        nofollow = getattr(os, "O_NOFOLLOW", 0)
        if nofollow == 0:
            raise InputStop("producer:posix:no_follow_unsupported")
        try:
            fd = os.open(resolved, os.O_RDONLY | nofollow)
        except OSError as exc:
            raise InputStop("producer:open:" + role) from exc
        try:
            opened = os.fstat(fd)
            if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1:
                raise InputStop("producer:physical:file_identity:" + role)
            size = int(opened.st_size)
            if size < 0 or size > self.meter.CAPS["temporary_bytes"]:
                raise InputStop("producer:physical:size:" + role)
            self.meter.before_allocation("opened_bytes", size)
            chunks = bytearray()
            remaining = size
            while remaining:
                part = os.read(fd, min(1024 * 1024, remaining))
                if not part:
                    raise InputStop("producer:physical:short_read:" + role)
                chunks.extend(part)
                remaining -= len(part)
            raw = bytes(chunks)
            after = os.fstat(fd)
            pathname = os.stat(resolved, follow_symlinks=False)
            if after.st_nlink != 1 or not _same_open_identity(opened, after, pathname):
                raise InputStop("producer:physical:toctou:" + role)
        except OSError as exc:
            raise InputStop("producer:read:" + role) from exc
        finally:
            os.close(fd)
        self.meter.charge("opened_bytes", len(raw))
        self.meter.charge("opens")
        identity = _stat_identity(resolved, owner_kind, raw)
        identity["single_open_handle"] = True
        identity["opened_handle_stable"] = True
        identity["pathname_matches_opened_handle"] = True
        identity["substitution_detected"] = False
        if expected is not None and (len(raw) != expected[0] or
                                     digest_bytes(raw) != expected[1]):
            raise InputStop("producer:pin:" + role)
        self.cache[key] = (raw, identity)
        if session is not None:
            session.observed[role] = identity
        return raw, identity

    def clear_local(self) -> None:
        # Only local temporary paths are ever removed from this cache.
        self.cache = {key: value for key, value in self.cache.items()
                      if str(ROOT) in key and "\\Temp\\" not in key}


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def resolve_owner(path: Path, role: str, *, local_root: Path | None,
                  session: EventSink) -> Path:
    session.enter("producer.transport.path_containment", "transport", role + ".path")
    resolved = path.resolve(strict=False)
    expected = (ROOT / (RECEIPT_REL if role == "receipt" else MANIFEST_REL)).resolve()
    is_registered = resolved == expected
    is_local = (local_root is not None and _inside(resolved, local_root)
                and resolved.name in ("receipt.json", "manifest.json",
                                      RECEIPT_NAME, MANIFEST_NAME))
    if (not is_registered and not is_local) or path.is_symlink():
        session.observed[role + ".path"] = _stat_identity(path, "path")
        raise TraceReject("producer.transport.path_containment", "transport",
                          "producer:path:registered_containment")
    return resolved


def atomic_owner(path: Path, raw: bytes, workspace: Path, meter: Meter) -> None:
    if os.name == "nt":
        raise InputStop("producer:windows:directory_durability_unsupported")
    if not _inside(path, workspace) or _inside(path, ROOT):
        raise InputStop("producer:temporary:containment")
    if len(raw) > meter.CAPS["temporary_bytes"]:
        raise InputStop("producer:temporary:size")
    meter.before_allocation("temporary_bytes", len(raw))
    meter.charge("temporary_bytes", len(raw))
    meter.charge("writes")
    fd, temporary = tempfile.mkstemp(prefix=".producer-trace-", dir=str(workspace))
    temporary_path = Path(temporary)
    try:
        offset = 0
        while offset < len(raw):
            offset += os.write(fd, raw[offset:offset + 1024 * 1024])
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(temporary_path, path)
    directory_fd = os.open(workspace, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def make_workspace() -> Path:
    location = Path(tempfile.mkdtemp(prefix="d972-r07-a4-producer-"))
    if _inside(location, ROOT):
        shutil.rmtree(location)
        raise InputStop("producer:temporary:repository_overlap")
    return location


def seal_json(value: dict[str, Any], meter: Meter) -> bytes:
    body = copy.deepcopy(value)
    body.pop("self_digest_sha256", None)
    raw_body = canonical(body)
    meter.charge("canonical_bytes", len(raw_body))
    body["self_digest_sha256"] = digest_object(body, meter)
    result = canonical(body)
    meter.charge("canonical_bytes", len(result))
    return result


def parse_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputStop("producer:json:" + label) from exc
    if not isinstance(value, dict):
        raise InputStop("producer:object:" + label)
    return value


def validate_self_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256")
    body = dict(value)
    body.pop("self_digest_sha256", None)
    if type(claimed) is not str or claimed != digest_bytes(canonical(body)):
        raise TraceReject("producer.transport." + label + ".self_seal", "transport",
                          "producer:transport:self_seal")


def validate_manifest(value: dict[str, Any], selected_receipt: Path) -> None:
    validate_self_seal(value, "manifest")
    if value.get("schema") != "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3":
        raise TraceReject("producer.authority.manifest_schema", "authority",
                          "producer:authority:manifest_schema")
    if value.get("synthetic") is not False or value.get("independent") is not True:
        raise TraceReject("producer.authority.manifest_flags", "authority",
                          "producer:authority:manifest_flags")
    if value.get("accepted") is not True:
        raise TraceReject("producer.authority.manifest_acceptance", "authority",
                          "producer:authority:manifest_acceptance")
    receipt = value.get("receipt")
    if not isinstance(receipt, dict) or receipt.get("basename") != selected_receipt.name:
        raise TraceReject("producer.authority.manifest_receipt_binding", "authority",
                          "producer:authority:manifest_receipt_binding")
    if value.get("accepted_receipt_basename") != selected_receipt.name:
        raise TraceReject("producer.authority.manifest_receipt_binding", "authority",
                          "producer:authority:manifest_receipt_binding")
    if value.get("checker_verdict", {}).get("accepted") is not True:
        raise TraceReject("producer.authority.manifest_verdict", "authority",
                          "producer:authority:manifest_verdict")


def validate_rows(receipt: dict[str, Any]) -> None:
    presentation = receipt.get("Delta0", {}).get("presentation", {})
    rows = presentation.get("rows")
    if not isinstance(rows, list) or len(rows) != ROWS:
        raise TraceReject("producer.authority.row_order", "authority",
                          "producer:authority:row_count")
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or row.get("ordinal") != index + 1:
            raise TraceReject("producer.authority.row_order", "authority",
                              "producer:authority:layer_ordinal")
        expected_layer = ("Gamma_Cayley" if index < 6318 else
                          "action" if index < 6422 else "Q0_lift")
        if row.get("layer") != expected_layer:
            raise TraceReject("producer.authority.row_order", "authority",
                              "producer:authority:layer_sequence")
    if presentation.get("row_count") != ROWS or presentation.get("layer_counts") != LAYER_COUNTS:
        raise TraceReject("producer.authority.row_order", "authority",
                          "producer:authority:layer_sequence")
    if presentation.get("rows_sha256") != digest_object(rows):
        raise TraceReject("producer.authority.row_order", "authority",
                          "producer:authority:row_digest")


def validate_generation(receipt: dict[str, Any]) -> None:
    proof = receipt.get("Delta0", {}).get("presentation", {}).get("normal_generation_proof")
    expected = {
        "Gamma_cayley_edge_count": 6318, "Gamma_cayley_state_count": 243,
        "Q0_defect_normal_closure_order": 243, "Q0_lift_count": 19,
        "all_record_generator_closure_order": 243,
        "marked_action_loop_count": 104, "normal_closure_exact": True,
        "presentation_quotient_order_upper_bound": 357128352,
        "selected_gamma_closure_order": 243,
        "selected_gamma_records": [1, 3, 6, 9],
        "surjective_marked_image_order": 357128352,
        "upper_bound_equals_image_order": True,
    }
    if not isinstance(proof, dict) or any(proof.get(key) != value for key, value in expected.items()):
        raise TraceReject("producer.authority.normal_generation", "authority",
                          "producer:authority:normal_generation_proof")


def validate_bridge(receipt: dict[str, Any]) -> None:
    bridge = receipt.get("bridge", {})
    ledger = bridge.get("occurrence_ledger")
    if not isinstance(ledger, list) or len(ledger) != 11:
        raise TraceReject("producer.authority.bridge_occurrence", "authority",
                          "producer:authority:bridge_occurrence_ledger")
    for index, row in enumerate(ledger):
        if not isinstance(row, dict) or row.get("ordinal") != index + 1:
            raise TraceReject("producer.authority.bridge_occurrence", "authority",
                              "producer:authority:bridge_occurrence_ledger")
        if row.get("block") != OCCURRENCE_BLOCKS[index]:
            raise TraceReject("producer.authority.bridge_occurrence", "authority",
                              "producer:authority:bridge_occurrence_ledger")
        if row.get("factor_sign") != OCCURRENCE_SIGNS[index] or row.get("ten_index") != OCCURRENCE_TEN[index]:
            raise TraceReject("producer.authority.bridge_occurrence", "authority",
                              "producer:authority:bridge_occurrence_ledger")
    if bridge.get("occurrence_ledger_sha256") != OCCURRENCE_LEDGER_SHA:
        raise TraceReject("producer.authority.bridge_occurrence", "authority",
                          "producer:authority:bridge_occurrence_ledger")


def validate_abi(receipt: dict[str, Any]) -> None:
    evaluator = receipt.get("evaluator", {})
    if evaluator.get("coordinate_widths") != COORDINATE_WIDTHS:
        raise TraceReject("producer.authority.evaluator_abi", "authority",
                          "producer:authority:evaluator_abi_canary")
    if evaluator.get("coordinate_ledger_sha256") != COORDINATE_LEDGER_SHA:
        raise TraceReject("producer.authority.evaluator_abi", "authority",
                          "producer:authority:evaluator_abi_canary")


def validate_receipt(raw: bytes, manifest: dict[str, Any], *, selected: Path,
                     events: EventSink) -> dict[str, Any]:
    binding = manifest.get("receipt")
    if not isinstance(binding, dict) or len(raw) != binding.get("bytes") or digest_bytes(raw) != binding.get("sha256"):
        raise TraceReject("producer.transport.receipt_identity", "transport",
                          "producer:transport:receipt_sha256")
    events.enter("producer.transport.receipt_decode", "decode", "receipt.bytes")
    receipt = parse_json(raw, "receipt")
    # The physical clone is canonical JSON.  This is the stable content
    # projection; raw path/inode/mtime remain internal to the reader.
    events.canonical_after["receipt"] = digest_bytes(canonical(receipt))
    validate_self_seal(receipt, "receipt")
    if receipt.get("schema") != "d972-r07-seven-context-roof-presentation/v1" or receipt.get("status") != "COMPLETE":
        raise TraceReject("producer.authority.receipt_envelope", "authority",
                          "producer:authority:receipt_envelope")
    events.enter("producer.authority.row_order", "authority", "receipt.Delta0.presentation.rows")
    validate_rows(receipt)
    events.enter("producer.authority.normal_generation", "authority",
                 "receipt.Delta0.presentation.normal_generation_proof")
    validate_generation(receipt)
    events.enter("producer.authority.bridge_occurrence", "authority",
                 "receipt.bridge.occurrence_ledger")
    validate_bridge(receipt)
    events.enter("producer.authority.evaluator_abi", "authority",
                 "receipt.evaluator.coordinate_widths")
    validate_abi(receipt)
    return receipt


class Paths:
    def __init__(self, manifest: Path, receipt: Path, local_root: Path | None,
                 receipt_name: str | None = None):
        self.manifest, self.receipt, self.local_root = manifest, receipt, local_root
        self.receipt_name = receipt_name


def ordinary_route(paths: Paths, store: PhysicalStore, events: EventSink) -> dict[str, Any]:
    events.enter("producer.transport.manifest_path", "transport", "manifest.path")
    manifest_path = resolve_owner(paths.manifest, "manifest", local_root=paths.local_root,
                                  session=events)
    events.enter("producer.transport.manifest_open", "transport", "manifest.bytes")
    manifest_raw, manifest_identity = store.read(manifest_path, "manifest", session=events)
    if manifest_path == (ROOT / MANIFEST_REL).resolve() and (
            len(manifest_raw) != MANIFEST_BYTES or digest_bytes(manifest_raw) != MANIFEST_SHA):
        raise TraceReject("producer.transport.manifest_identity", "transport",
                          "producer:transport:manifest_sha256")
    events.enter("producer.transport.manifest_decode", "decode", "manifest.bytes")
    manifest = parse_json(manifest_raw, "manifest")
    events.canonical_after["manifest"] = digest_bytes(canonical(manifest))
    events.enter("producer.authority.manifest_acceptance", "authority",
                 "manifest.accepted")
    selected_name = paths.receipt_name or paths.receipt.name
    validate_manifest(manifest, Path(selected_name))
    events.enter("producer.transport.receipt_path", "transport", "receipt.path")
    receipt_path = resolve_owner(paths.receipt, "receipt", local_root=paths.local_root,
                                 session=events)
    events.enter("producer.transport.receipt_open", "transport", "receipt.bytes")
    events.enter("producer.transport.receipt_identity", "transport", "receipt.identity")
    receipt_raw, receipt_identity = store.read(receipt_path, "receipt", session=events)
    if receipt_path == (ROOT / RECEIPT_REL).resolve() and (
            len(receipt_raw) != RECEIPT_BYTES or digest_bytes(receipt_raw) != RECEIPT_SHA):
        raise TraceReject("producer.transport.receipt_identity", "transport",
                          "producer:transport:receipt_sha256")
    receipt = validate_receipt(receipt_raw, manifest, selected=receipt_path, events=events)
    return {"manifest": manifest, "receipt": receipt, "manifest_identity": manifest_identity,
            "receipt_identity": receipt_identity, "manifest_raw": manifest_raw,
            "receipt_raw": receipt_raw, "observed": dict(events.observed)}


def authenticate_sources(store: PhysicalStore, events: EventSink | None = None) -> None:
    # Receipt and manifest are opened by ordinary_route after their entry
    # events.  Reading them here would make the baseline cache bypass the
    # required event-before-owner-read boundary.
    for relative, size, expected_sha in PINS[2:]:
        if events is not None:
            events.enter("producer.transport.source_pin", "transport", relative)
        raw, _ = store.read(ROOT / relative, relative, expected=(size, expected_sha),
                            session=events)
        if len(raw) != size or digest_bytes(raw) != expected_sha:
            raise InputStop("producer:pin:" + relative)


def load_fixture(path: Path, store: PhysicalStore) -> dict[str, Any]:
    raw, _ = store.read(path, "fixture")
    fixture = parse_json(raw, "fixture")
    if fixture.get("schema") != SCHEMA + "/authority-fixture/v1" or fixture.get("covered_rows") != [1, 2, 3, 4, 5, 6, 7]:
        raise InputStop("producer:fixture:shape")
    if (fixture.get("remaining_rows") != list(range(8, 49)) or
            fixture.get("candidate_only") is not True or
            fixture.get("full_a4_selftest") is not False or
            fixture.get("synthetic") is not False):
        raise InputStop("producer:fixture:scope")
    if (not isinstance(fixture.get("producer"), dict) or
            set(fixture["producer"]) != set(MUTATIONS)):
        raise InputStop("producer:fixture:producer_rows")
    if fixture.get("immutable_input_identities") != {
            "task198_receipt": {"bytes": RECEIPT_BYTES, "sha256": RECEIPT_SHA,
                                 "self_digest_sha256": RECEIPT_SELF},
            "task198_manifest": {"bytes": MANIFEST_BYTES, "sha256": MANIFEST_SHA,
                                  "self_digest_sha256": MANIFEST_SELF}}:
        raise InputStop("producer:fixture:immutable_inputs")
    return fixture


def _update_manifest(manifest: dict[str, Any], receipt_name: str,
                     receipt_raw: bytes, receipt: dict[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(manifest)
    answer["accepted_receipt_basename"] = receipt_name
    answer["receipt"] = {"basename": receipt_name, "bytes": len(receipt_raw),
                         "sha256": digest_bytes(receipt_raw),
                         "self_digest_sha256": receipt["self_digest_sha256"]}
    return answer


def _mutate_ordinal(receipt: dict[str, Any]) -> None:
    receipt["Delta0"]["presentation"]["rows"][0]["ordinal"] += 1


def _mutate_generation(receipt: dict[str, Any]) -> None:
    receipt["Delta0"]["presentation"]["normal_generation_proof"]["Gamma_cayley_edge_count"] += 1


def _mutate_bridge(receipt: dict[str, Any]) -> None:
    receipt["bridge"]["occurrence_ledger"][0]["block"] = "H1_mutated"


def _mutate_abi(receipt: dict[str, Any]) -> None:
    receipt["evaluator"]["coordinate_widths"][0] += 1


def _flip_bytes(raw: bytes) -> bytes:
    if not raw:
        raise InputStop("producer:mutation:empty_owner")
    answer = bytearray(raw)
    answer[-1] ^= 1
    return bytes(answer)


def _mutate_manifest(manifest: dict[str, Any]) -> None:
    manifest["accepted"] = False


def _sealed_document(value: dict[str, Any], meter: Meter) -> bytes:
    return seal_json(value, meter)


def path_identity(path: Path, kind: str) -> dict[str, Any]:
    return _stat_identity(path, kind)


def _same_identity(expected: dict[str, Any], actual: dict[str, Any]) -> bool:
    fields = ("identity_kind", "path", "exists", "type", "bytes", "sha256", "device",
              "inode", "nlink", "single_open_handle", "opened_handle_stable",
              "pathname_matches_opened_handle", "substitution_detected")
    return all(expected.get(field) == actual.get(field) for field in fields)


def reconfirm_baseline(meter: Meter, manifest_identity: dict[str, Any],
                       receipt_identity: dict[str, Any]) -> bool:
    """Re-read both immutable owners through fresh one-handle pin checks."""
    verifier = PhysicalStore(meter)
    _, manifest_now = verifier.read(
        ROOT / MANIFEST_REL, "baseline_manifest_recheck",
        expected=(MANIFEST_BYTES, MANIFEST_SHA))
    _, receipt_now = verifier.read(
        ROOT / RECEIPT_REL, "baseline_receipt_recheck",
        expected=(RECEIPT_BYTES, RECEIPT_SHA))
    if not _same_identity(manifest_identity, manifest_now):
        raise InputStop("producer:baseline:manifest_identity_changed")
    if not _same_identity(receipt_identity, receipt_now):
        raise InputStop("producer:baseline:receipt_identity_changed")
    return True


def project_identity(raw: dict[str, Any], logical_case: str,
                     canonical_before: str, canonical_after: str) -> dict[str, Any]:
    """Drop host-specific inode/mtime/temp-path data from load-bearing evidence."""
    readable = raw.get("exists") is True and raw.get("sha256") is not None
    return {
        "logical_case_path": logical_case,
        "owner_kind": raw.get("identity_kind"),
        "byte_length": raw.get("bytes") if readable else "UNREADABLE_AT_REGISTERED_STAGE",
        "content_sha256": raw.get("sha256") if readable else "UNREADABLE_AT_REGISTERED_STAGE",
        "link_count": raw.get("nlink") if raw.get("nlink") is not None else "UNREADABLE_AT_REGISTERED_STAGE",
        "symlink_or_reparse": raw.get("type") in ("symlink", "reparse", "nonregular"),
        "logical_link_target": "none" if raw.get("type") in ("regular", "missing") else raw.get("type"),
        "single_open_handle": raw.get("single_open_handle") is True,
        "opened_handle_stable": raw.get("opened_handle_stable") is True,
        "pathname_matches_opened_handle": raw.get("pathname_matches_opened_handle") is True,
        "substitution_detected": raw.get("substitution_detected") is True,
        "canonical_before_sha256": canonical_before,
        "canonical_after_sha256": canonical_after,
    }


def project_trace(before: dict[str, Any], after: dict[str, Any],
                  resealed: list[str], entered: list[str],
                  trace_digest: str, rejection: dict[str, str]) -> dict[str, Any]:
    """Stable v298 projection; raw host identity stays private to this run."""
    return {
        "logical_case_path": before["logical_case_path"],
        "owner_kind": before["owner_kind"],
        "byte_length": after["byte_length"],
        "content_sha256": after["content_sha256"],
        "link_count_before": before["link_count"],
        "link_count_after": after["link_count"],
        "symlink_or_reparse": before["symlink_or_reparse"] or after["symlink_or_reparse"],
        "logical_link_target": after["logical_link_target"],
        "single_open_handle": after["single_open_handle"],
        "opened_handle_stable": after["opened_handle_stable"],
        "pathname_matches_opened_handle": after["pathname_matches_opened_handle"],
        "substitution_detected": after["substitution_detected"],
        "canonical_before_sha256": before["canonical_before_sha256"],
        "canonical_after_sha256": after["canonical_after_sha256"],
        "resealed_logical_nodes": list(resealed),
        "entered_validators": list(entered),
        "event_trace_digest": trace_digest,
        "first_typed_rejection": dict(rejection),
    }


def expected_entry(fixture: dict[str, Any], name: str) -> dict[str, Any]:
    expected = fixture.get("producer", {}).get(name)
    if not isinstance(expected, dict):
        raise InputStop("producer:fixture:missing_expected:" + name)
    required = {"owner", "identity_kind", "logical_case_path",
                "ordinary_validator", "stage", "first_rejection",
                "allowed_downstream_reseals"}
    if set(expected) != required or set(expected["first_rejection"]) != {"validator", "stage", "narrow_reason"}:
        raise InputStop("producer:fixture:expected_shape:" + name)
    return expected


def compare_evidence(evidence: dict[str, Any], fixture: dict[str, Any],
                     entered_events: list[dict[str, Any]]) -> None:
    expected = expected_entry(fixture, evidence["id"])
    if evidence["owner"] != expected["owner"] or evidence["identity_kind"] != expected["identity_kind"]:
        raise InputStop("producer:fixture:owner_binding:" + evidence["id"])
    if evidence["before_identity"]["logical_case_path"] != expected["logical_case_path"]:
        raise InputStop("producer:fixture:logical_case:" + evidence["id"])
    matching_events = [event for event in entered_events
                       if event.get("validator") == expected["ordinary_validator"]
                       and event.get("stage") == expected["stage"]]
    if len(matching_events) != 1:
        raise InputStop("producer:fixture:ordinary_event:" + evidence["id"])
    if evidence["first_rejection"] != expected["first_rejection"]:
        raise InputStop("producer:fixture:first_rejection:" + evidence["id"])
    if evidence["resealed_nodes"] != expected["allowed_downstream_reseals"]:
        raise InputStop("producer:fixture:reseals:" + evidence["id"])
    if evidence["baseline_revalidated"] is not True or evidence["terminal_count"] != 1:
        raise InputStop("producer:fixture:evidence_liveness:" + evidence["id"])


def run_mutation(name: str, baseline: dict[str, Any], fixture: dict[str, Any],
                 meter: Meter, workspace: Path, store: PhysicalStore) -> dict[str, Any]:
    meter.charge("mutations")
    original_paths: Paths = baseline["paths"]
    before_role = "manifest" if name == "authority_binding" else "receipt"
    before_identity = baseline["manifest_identity"] if before_role == "manifest" else baseline["receipt_identity"]
    local_root: Path | None = None
    manifest_path = original_paths.manifest
    receipt_path = original_paths.receipt
    resealed: list[str] = []
    if name == "authority_binding":
        local_root = workspace
        changed = copy.deepcopy(baseline["manifest"])
        _mutate_manifest(changed)
        manifest_path = workspace / "manifest.json"
        atomic_owner(manifest_path, _sealed_document(changed, meter), workspace, meter)
        resealed = ["manifest.self_digest_sha256"]
    elif name == "canonical_input_bytes":
        local_root = workspace
        receipt_path = workspace / RECEIPT_NAME
        atomic_owner(receipt_path, _flip_bytes(baseline["receipt_raw"]), workspace, meter)
    elif name == "resolved_path_traversal":
        # No file is created for this path owner; the ordinary resolver must
        # reject the real lexical path before any read/allocation.
        receipt_path = (workspace.parent / (RECEIPT_NAME + ".outside"))
    elif name in {"per_layer_ordinal", "normal_generation_proof",
                  "bridge_typed_occurrence_ledger", "evaluator_abi_canary"}:
        local_root = workspace
        changed = copy.deepcopy(baseline["receipt"])
        if name == "per_layer_ordinal":
            _mutate_ordinal(changed)
        elif name == "normal_generation_proof":
            _mutate_generation(changed)
        elif name == "bridge_typed_occurrence_ledger":
            _mutate_bridge(changed)
        else:
            _mutate_abi(changed)
        receipt_path = workspace / RECEIPT_NAME
        receipt_raw = _sealed_document(changed, meter)
        atomic_owner(receipt_path, receipt_raw, workspace, meter)
        changed_manifest = _update_manifest(baseline["manifest"], receipt_path.name,
                                             receipt_raw, changed)
        manifest_path = workspace / "manifest.json"
        atomic_owner(manifest_path, _sealed_document(changed_manifest, meter), workspace, meter)
        resealed = ["receipt.self_digest_sha256", "manifest.receipt.bytes",
                    "manifest.receipt.sha256", "manifest.receipt.self_digest_sha256",
                    "manifest.self_digest_sha256"]
    else:
        raise InputStop("producer:mutation:unknown:" + name)

    paths = Paths(manifest_path, receipt_path, local_root,
                  RECEIPT_NAME if name == "resolved_path_traversal" else None)
    events = EventSink(meter)
    events._observed = {}
    try:
        ordinary_route(paths, store, events)
    except TraceReject as rejection:
        events.terminal()
        observed = dict(events.observed)
        after_identity = observed.get(before_role)
        if after_identity is None and name == "resolved_path_traversal":
            after_identity = observed.get("receipt.path", path_identity(receipt_path, "path"))
        if after_identity is None:
            raise InputStop("producer:mutation:missing_after_identity:" + name)
        if before_identity == after_identity:
            raise InputStop("producer:mutation:owner_unchanged:" + name)
        entered = [event["validator"] for event in events.events]
        logical_case = expected_entry(fixture, name).get("logical_case_path", name)
        canonical_before = digest_bytes(canonical(baseline[before_role]))
        canonical_after = events.canonical_after.get(
            before_role, "UNREADABLE_AT_REGISTERED_STAGE")
        first = {"validator": rejection.validator,
                 "stage": rejection.stage, "narrow_reason": rejection.reason}
        before_projection = project_identity(before_identity, logical_case,
                                             canonical_before, canonical_before)
        after_projection = project_identity(after_identity, logical_case,
                                            canonical_before, canonical_after)
        evidence = {
            "id": name, "owner": expected_entry(fixture, name)["owner"],
            "identity_kind": expected_entry(fixture, name)["identity_kind"],
            "before_identity": before_projection,
            "after_identity": after_projection,
            "resealed_nodes": resealed, "event_trace_digest": events.digest(),
            "entered_validators": entered,
            "first_rejection": first,
            "baseline_revalidated": baseline["baseline_revalidated"],
            "terminal_count": events.terminal_count,
        }
        evidence["projection"] = project_trace(before_projection, after_projection,
                                                resealed, entered,
                                                evidence["event_trace_digest"], first)
        compare_evidence(evidence, fixture, events.events)
        return evidence
    # This is deliberately outside the narrow rejection catch.
    raise MutationAccepted("producer:mutation_accepted:" + name)


def execute(fixture: dict[str, Any]) -> dict[str, Any]:
    meter = Meter()
    store = PhysicalStore(meter)
    baseline_events = EventSink(meter)
    baseline_events._observed = {}
    authenticate_sources(store, baseline_events)
    baseline_paths = Paths(ROOT / MANIFEST_REL, ROOT / RECEIPT_REL, None)
    baseline_run = ordinary_route(baseline_paths, store, baseline_events)
    baseline = dict(baseline_run)
    baseline["paths"] = baseline_paths
    baseline["manifest"] = baseline_run["manifest"]
    baseline["receipt"] = baseline_run["receipt"]
    baseline["manifest_raw"] = baseline_run["manifest_raw"]
    baseline["receipt_raw"] = baseline_run["receipt_raw"]
    baseline["manifest_identity"] = baseline_run["manifest_identity"]
    baseline["receipt_identity"] = baseline_run["receipt_identity"]
    baseline["baseline_revalidated"] = reconfirm_baseline(
        meter, baseline["manifest_identity"], baseline["receipt_identity"])
    baseline["baseline_event_trace_digest"] = baseline_events.digest()
    records: list[dict[str, Any]] = []
    for name in MUTATIONS:
        workspace = make_workspace()
        try:
            records.append(run_mutation(name, baseline, fixture, meter, workspace, store))
        finally:
            if workspace.exists():
                shutil.rmtree(workspace)
    return {"schema": SCHEMA, "candidate_only": True, "covered_rows": [1, 2, 3, 4, 5, 6, 7],
            "remaining_rows": list(range(8, 49)), "full_a4_selftest": False,
            "baseline": {"receipt": project_identity(
                            baseline["receipt_identity"],
                            "task198/receipt/baseline",
                            digest_bytes(canonical(baseline["receipt"])),
                            digest_bytes(canonical(baseline["receipt"]))),
                         "manifest": project_identity(
                            baseline["manifest_identity"],
                            "task198/manifest/baseline",
                            digest_bytes(canonical(baseline["manifest"])),
                            digest_bytes(canonical(baseline["manifest"]))),
                         "event_trace_digest": baseline["baseline_event_trace_digest"]},
            "rows": records, "resource": meter.public()}


def write_sealed_output(path: Path, value: dict[str, Any], meter: Meter) -> None:
    if path.is_absolute():
        resolved = path.resolve(strict=False)
    else:
        resolved = (ROOT / path).resolve(strict=False)
    if not _inside(resolved, ROOT / "ci" / "out"):
        raise InputStop("producer:output:containment")
    body = copy.deepcopy(value)
    body["self_digest_sha256"] = digest_object(body, meter)
    raw = canonical(body)
    meter.charge("canonical_bytes", len(raw))
    output_root = resolved.parent
    output_root.mkdir(parents=True, exist_ok=True)
    workspace = make_workspace()
    try:
        staged = workspace / "output.json"
        atomic_owner(staged, raw, workspace, meter)
        os.replace(staged, resolved)
        directory_fd = os.open(output_root, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", default="search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v1_20260829.json")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    if os.name == "nt":
        raise InputStop("producer:windows:one_handle_reparse_unsupported")
    meter = Meter()
    fixture_store = PhysicalStore(meter)
    fixture_path = Path(args.fixture)
    if not fixture_path.is_absolute():
        fixture_path = ROOT / fixture_path
    fixture = load_fixture(fixture_path.resolve(), fixture_store)
    result = execute(fixture)
    if args.output:
        write_sealed_output(Path(args.output), result, meter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
