#!/usr/bin/env python3
"""R07 A4/v6a checker-side physical authority trace.

This checker is written independently from the producer trace module.  It
reopens the accepted task198 owners, reconstructs the seven authority checks,
and makes its own physical clones and event journal.  It is a candidate
tranche only; rows 8--48 are deliberately outside this module.
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


REPO = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-a4-actual-owner-trace/v1"
RECEIPT_FILE = "d972_r07_seven_context_roof_presentation_v1.json"
MANIFEST_FILE = "d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json"
RECEIPT = "ci/in/" + RECEIPT_FILE
MANIFEST = "ci/in/" + MANIFEST_FILE
RECEIPT_SIZE = 31017244
RECEIPT_DIGEST = "82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"
MANIFEST_SIZE = 2722
MANIFEST_DIGEST = "cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"
COORD_WIDTHS = [40, 40, 40, 40, 40, 154, 154, 154, 154, 154]
COORD_DIGEST = "9f9c081e9653d6e141e4d6d231e2d6db9526850b7ccd33c0859d13825f3fa83c"
OCCURRENCE_DIGEST = "040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7"
BLOCKS = ["H1", "H1", "H1", "H2", "H2", "H2", "P1", "P2", "P3", "P5", "P4"]
SIGNS = [1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1]
TEN_INDEX = [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9]

PINNED_FILES: tuple[tuple[str, int, str], ...] = (
    (RECEIPT, RECEIPT_SIZE, RECEIPT_DIGEST),
    (MANIFEST, MANIFEST_SIZE, MANIFEST_DIGEST),
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

CASES = (
    "per_layer_ordinal", "authority_binding", "canonical_input_bytes",
    "resolved_path_traversal", "normal_generation_proof",
    "bridge_typed_occurrence_ledger", "evaluator_abi_canary",
)


class InputRefusal(RuntimeError):
    pass


class NarrowRejection(RuntimeError):
    def __init__(self, validator: str, stage: str, token: str):
        self.validator, self.stage, self.token = validator, stage, token
        super().__init__(token)


class MutationAccepted(RuntimeError):
    pass


class Counter:
    LIMITS = {
        "opened_bytes": 250000000, "temporary_bytes": 250000000,
        "canonical_bytes": 500000000, "opens": 256, "writes": 256,
        "events": 10000, "mutations": 7,
    }

    def __init__(self) -> None:
        self.values = {key: 0 for key in self.LIMITS}

    def add(self, key: str, amount: int = 1) -> None:
        if key not in self.LIMITS or type(amount) is not int or amount < 0:
            raise InputRefusal("checker:meter:registry")
        new_value = self.values[key] + amount
        if new_value > self.LIMITS[key]:
            raise InputRefusal("checker:resource:" + key)
        self.values[key] = new_value

    def reserve(self, key: str, amount: int) -> None:
        if key not in self.LIMITS or type(amount) is not int or amount < 0:
            raise InputRefusal("checker:meter:reserve")
        if self.values[key] + amount > self.LIMITS[key]:
            raise InputRefusal("checker:resource:" + key)

    def export(self) -> dict[str, Any]:
        return {"caps": dict(self.LIMITS), "counts": dict(self.values),
                "measured": "UNEXECUTED"}


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def object_sha(value: Any, meter: Counter | None = None) -> str:
    raw = encode(value)
    if meter is not None:
        meter.add("canonical_bytes", len(raw))
    return sha(raw)


class Journal:
    def __init__(self, meter: Counter):
        self.meter = meter
        self.entries: list[dict[str, Any]] = []
        self.identities: dict[str, dict[str, Any]] = {}
        self.canonical_after: dict[str, str] = {}
        self.terminal_count = 0

    def before(self, validator: str, stage: str, owner: str) -> None:
        self.meter.add("events")
        self.entries.append({"ordinal": len(self.entries) + 1,
                             "validator": validator, "stage": stage,
                             "owner": owner})

    def trace_sha(self) -> str:
        return object_sha(self.entries, self.meter)

    def terminal(self) -> None:
        self.terminal_count += 1


def raw_identity(path: Path, kind: str, content: bytes | None = None) -> dict[str, Any]:
    # Preserve the lexical name for lstat/open; resolving first would follow
    # a symlink before the no-follow flag can reject it.
    resolved = Path(os.path.abspath(path))
    try:
        data = os.lstat(resolved)
    except FileNotFoundError:
        return {"kind": kind, "path": str(resolved), "exists": False,
                "type": "missing", "length": None, "sha": None,
                "dev": None, "ino": None, "nlink": None,
                "single_open_handle": False, "opened_handle_stable": False,
                "pathname_matches_opened_handle": False,
                "substitution_detected": False}
    regular = stat.S_ISREG(data.st_mode)
    return {"kind": kind, "path": str(resolved), "exists": True,
            "type": "regular" if regular else "nonregular",
            "length": int(data.st_size) if regular else None,
            "sha": sha(content) if content is not None else None,
            "dev": int(data.st_dev), "ino": int(data.st_ino),
            "nlink": int(data.st_nlink), "single_open_handle": False,
            "opened_handle_stable": False,
            "pathname_matches_opened_handle": False,
            "substitution_detected": False}


def stable_stat(left: os.stat_result, right: os.stat_result,
                named: os.stat_result) -> bool:
    return all(getattr(left, field) == getattr(right, field) == getattr(named, field)
               for field in ("st_dev", "st_ino", "st_size", "st_mtime_ns"))


class AuthenticatedFiles:
    """Independent one-open POSIX reader; Windows is typed unsupported."""

    def __init__(self, meter: Counter):
        self.meter = meter
        self.memo: dict[str, tuple[bytes, dict[str, Any]]] = {}

    def fetch(self, path: Path, label: str,
              pin: tuple[int, str] | None = None,
              journal: Journal | None = None) -> tuple[bytes, dict[str, Any]]:
        resolved = Path(os.path.abspath(path))
        key = str(resolved)
        if key in self.memo:
            result = self.memo[key]
            if journal is not None:
                journal.identities[label] = result[1]
            return result
        if os.name == "nt":
            raise InputRefusal("checker:windows:one_handle_reparse_unsupported")
        nofollow = getattr(os, "O_NOFOLLOW", 0)
        if nofollow == 0:
            raise InputRefusal("checker:posix:no_follow_unsupported")
        try:
            handle = os.open(resolved, os.O_RDONLY | nofollow)
        except OSError as exc:
            raise InputRefusal("checker:open:" + label) from exc
        try:
            before = os.fstat(handle)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
                raise InputRefusal("checker:physical:file_identity:" + label)
            length = int(before.st_size)
            if length < 0 or length > self.meter.LIMITS["temporary_bytes"]:
                raise InputRefusal("checker:physical:size:" + label)
            self.meter.reserve("opened_bytes", length)
            collected = bytearray()
            while len(collected) < length:
                block = os.read(handle, min(1024 * 1024, length - len(collected)))
                if not block:
                    raise InputRefusal("checker:physical:short_read:" + label)
                collected.extend(block)
            content = bytes(collected)
            after = os.fstat(handle)
            named = os.stat(resolved, follow_symlinks=False)
            if after.st_nlink != 1 or not stable_stat(before, after, named):
                raise InputRefusal("checker:physical:toctou:" + label)
        except OSError as exc:
            raise InputRefusal("checker:read:" + label) from exc
        finally:
            os.close(handle)
        self.meter.add("opened_bytes", len(content))
        self.meter.add("opens")
        identity = raw_identity(resolved, "file", content)
        identity.update(single_open_handle=True, opened_handle_stable=True,
                        pathname_matches_opened_handle=True,
                        substitution_detected=False)
        if pin is not None and (len(content) != pin[0] or sha(content) != pin[1]):
            raise InputRefusal("checker:pin:" + label)
        self.memo[key] = (content, identity)
        if journal is not None:
            journal.identities[label] = identity
        return content, identity


def under(child: Path, parent: Path) -> bool:
    try:
        child.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def admit(path: Path, role: str, local: Path | None, journal: Journal) -> Path:
    journal.before("checker.transport.path_containment", "transport", role + ".path")
    resolved = path.resolve(strict=False)
    registered = (REPO / (RECEIPT if role == "receipt" else MANIFEST)).resolve()
    local_name = {"receipt", "manifest", RECEIPT_FILE, MANIFEST_FILE}
    local_ok = local is not None and under(resolved, local) and resolved.name in local_name
    if (resolved != registered and not local_ok) or path.is_symlink():
        journal.identities[role + ".path"] = raw_identity(path, "path")
        raise NarrowRejection("checker.transport.path_containment", "transport",
                              "checker:path:registered_containment")
    return resolved


def durable_replace(path: Path, data: bytes, workspace: Path, meter: Counter) -> None:
    if os.name == "nt":
        raise InputRefusal("checker:windows:directory_durability_unsupported")
    if not under(path, workspace) or under(path, REPO):
        raise InputRefusal("checker:temporary:containment")
    if len(data) > meter.LIMITS["temporary_bytes"]:
        raise InputRefusal("checker:temporary:size")
    meter.reserve("temporary_bytes", len(data))
    meter.add("temporary_bytes", len(data))
    meter.add("writes")
    fd, name = tempfile.mkstemp(prefix=".checker-trace-", dir=str(workspace))
    staged = Path(name)
    try:
        cursor = 0
        while cursor < len(data):
            cursor += os.write(fd, data[cursor:cursor + 1024 * 1024])
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(staged, path)
    directory = os.open(workspace, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def new_workspace() -> Path:
    value = Path(tempfile.mkdtemp(prefix="d972-r07-a4-checker-"))
    if under(value, REPO):
        shutil.rmtree(value)
        raise InputRefusal("checker:temporary:repository_overlap")
    return value


def parse(raw: bytes, label: str) -> dict[str, Any]:
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputRefusal("checker:json:" + label) from exc
    if not isinstance(result, dict):
        raise InputRefusal("checker:object:" + label)
    return result


def reseal(value: dict[str, Any], meter: Counter) -> bytes:
    body = copy.deepcopy(value)
    body.pop("self_digest_sha256", None)
    first = encode(body)
    meter.add("canonical_bytes", len(first))
    body["self_digest_sha256"] = object_sha(body, meter)
    answer = encode(body)
    meter.add("canonical_bytes", len(answer))
    return answer


def check_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest_sha256")
    body = dict(value)
    body.pop("self_digest_sha256", None)
    if type(claimed) is not str or claimed != sha(encode(body)):
        raise NarrowRejection("checker.transport." + label + ".self_seal", "transport",
                              "checker:transport:self_seal")


def check_manifest(value: dict[str, Any], receipt_path: Path) -> None:
    check_seal(value, "manifest")
    if value.get("schema") != "d972-r07-seven-context-roof-presentation/v1/acceptance-manifest/v3":
        raise NarrowRejection("checker.authority.manifest_schema", "authority",
                              "checker:authority:manifest_schema")
    if value.get("synthetic") is not False or value.get("independent") is not True:
        raise NarrowRejection("checker.authority.manifest_flags", "authority",
                              "checker:authority:manifest_flags")
    if value.get("accepted") is not True:
        raise NarrowRejection("checker.authority.manifest_acceptance", "authority",
                              "checker:authority:manifest_acceptance")
    binding = value.get("receipt")
    if not isinstance(binding, dict) or binding.get("basename") != receipt_path.name:
        raise NarrowRejection("checker.authority.manifest_receipt_binding", "authority",
                              "checker:authority:manifest_receipt_binding")
    if value.get("accepted_receipt_basename") != receipt_path.name:
        raise NarrowRejection("checker.authority.manifest_receipt_binding", "authority",
                              "checker:authority:manifest_receipt_binding")
    if value.get("checker_verdict", {}).get("accepted") is not True:
        raise NarrowRejection("checker.authority.manifest_verdict", "authority",
                              "checker:authority:manifest_verdict")


def check_row_roster(receipt: dict[str, Any]) -> None:
    section = receipt.get("Delta0", {}).get("presentation", {})
    rows = section.get("rows")
    if not isinstance(rows, list) or len(rows) != 6441:
        raise NarrowRejection("checker.authority.row_order", "authority",
                              "checker:authority:row_count")
    for position, item in enumerate(rows):
        if not isinstance(item, dict) or item.get("ordinal") != position + 1:
            raise NarrowRejection("checker.authority.row_order", "authority",
                                  "checker:authority:layer_ordinal")
        wanted = "Gamma_Cayley" if position < 6318 else "action" if position < 6422 else "Q0_lift"
        if item.get("layer") != wanted:
            raise NarrowRejection("checker.authority.row_order", "authority",
                                  "checker:authority:layer_sequence")
    if section.get("row_count") != 6441 or section.get("layer_counts") != {
            "Gamma_Cayley": 6318, "action": 104, "Q0_lift": 19}:
        raise NarrowRejection("checker.authority.row_order", "authority",
                              "checker:authority:layer_sequence")
    if section.get("rows_sha256") != object_sha(rows):
        raise NarrowRejection("checker.authority.row_order", "authority",
                              "checker:authority:row_digest")


def check_generation(receipt: dict[str, Any]) -> None:
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
        raise NarrowRejection("checker.authority.normal_generation", "authority",
                              "checker:authority:normal_generation_proof")


def check_bridge(receipt: dict[str, Any]) -> None:
    bridge = receipt.get("bridge", {})
    records = bridge.get("occurrence_ledger")
    if not isinstance(records, list) or len(records) != 11:
        raise NarrowRejection("checker.authority.bridge_occurrence", "authority",
                              "checker:authority:bridge_occurrence_ledger")
    for index, record in enumerate(records):
        if not isinstance(record, dict) or record.get("ordinal") != index + 1:
            raise NarrowRejection("checker.authority.bridge_occurrence", "authority",
                                  "checker:authority:bridge_occurrence_ledger")
        if record.get("block") != BLOCKS[index] or record.get("factor_sign") != SIGNS[index] or record.get("ten_index") != TEN_INDEX[index]:
            raise NarrowRejection("checker.authority.bridge_occurrence", "authority",
                                  "checker:authority:bridge_occurrence_ledger")
    if bridge.get("occurrence_ledger_sha256") != OCCURRENCE_DIGEST:
        raise NarrowRejection("checker.authority.bridge_occurrence", "authority",
                              "checker:authority:bridge_occurrence_ledger")


def check_coordinates(receipt: dict[str, Any]) -> None:
    evaluator = receipt.get("evaluator", {})
    if evaluator.get("coordinate_widths") != COORD_WIDTHS or evaluator.get("coordinate_ledger_sha256") != COORD_DIGEST:
        raise NarrowRejection("checker.authority.evaluator_abi", "authority",
                              "checker:authority:evaluator_abi_canary")


def check_receipt(raw: bytes, manifest: dict[str, Any], events: Journal) -> dict[str, Any]:
    bind = manifest.get("receipt")
    if not isinstance(bind, dict) or len(raw) != bind.get("bytes") or sha(raw) != bind.get("sha256"):
        raise NarrowRejection("checker.transport.receipt_identity", "transport",
                              "checker:transport:receipt_sha256")
    events.before("checker.transport.receipt_decode", "decode", "receipt.bytes")
    receipt = parse(raw, "receipt")
    check_seal(receipt, "receipt")
    if receipt.get("schema") != "d972-r07-seven-context-roof-presentation/v1" or receipt.get("status") != "COMPLETE":
        raise NarrowRejection("checker.authority.receipt_envelope", "authority",
                              "checker:authority:receipt_envelope")
    events.before("checker.authority.row_order", "authority", "receipt.Delta0.presentation.rows")
    check_row_roster(receipt)
    events.before("checker.authority.normal_generation", "authority",
                  "receipt.Delta0.presentation.normal_generation_proof")
    check_generation(receipt)
    events.before("checker.authority.bridge_occurrence", "authority",
                  "receipt.bridge.occurrence_ledger")
    check_bridge(receipt)
    events.before("checker.authority.evaluator_abi", "authority",
                  "receipt.evaluator.coordinate_widths")
    check_coordinates(receipt)
    return receipt


class Route:
    def __init__(self, manifest: Path, receipt: Path, local: Path | None,
                 receipt_name: str | None = None):
        self.manifest, self.receipt, self.local = manifest, receipt, local
        self.receipt_name = receipt_name


def ordinary(route: Route, files: AuthenticatedFiles, journal: Journal) -> dict[str, Any]:
    journal.before("checker.transport.manifest_path", "transport", "manifest.path")
    manifest_path = admit(route.manifest, "manifest", route.local, journal)
    journal.before("checker.transport.manifest_open", "transport", "manifest.bytes")
    manifest_raw, manifest_id = files.fetch(manifest_path, "manifest", journal=journal)
    if manifest_path == (REPO / MANIFEST).resolve() and (len(manifest_raw) != MANIFEST_SIZE or sha(manifest_raw) != MANIFEST_DIGEST):
        raise NarrowRejection("checker.transport.manifest_identity", "transport",
                              "checker:transport:manifest_sha256")
    journal.before("checker.transport.manifest_decode", "decode", "manifest.bytes")
    manifest = parse(manifest_raw, "manifest")
    journal.canonical_after["manifest"] = sha(encode(manifest))
    journal.before("checker.authority.manifest_acceptance", "authority",
                   "manifest.accepted")
    selected_name = route.receipt_name or route.receipt.name
    check_manifest(manifest, Path(selected_name))
    journal.before("checker.transport.receipt_path", "transport", "receipt.path")
    receipt_path = admit(route.receipt, "receipt", route.local, journal)
    journal.before("checker.transport.receipt_open", "transport", "receipt.bytes")
    journal.before("checker.transport.receipt_identity", "transport",
                   "receipt.identity")
    receipt_raw, receipt_id = files.fetch(receipt_path, "receipt", journal=journal)
    if receipt_path == (REPO / RECEIPT).resolve() and (len(receipt_raw) != RECEIPT_SIZE or sha(receipt_raw) != RECEIPT_DIGEST):
        raise NarrowRejection("checker.transport.receipt_identity", "transport",
                              "checker:transport:receipt_sha256")
    receipt = check_receipt(receipt_raw, manifest, journal)
    journal.canonical_after["receipt"] = sha(encode(receipt))
    return {"manifest": manifest, "receipt": receipt, "manifest_raw": manifest_raw,
            "receipt_raw": receipt_raw, "manifest_id": manifest_id,
            "receipt_id": receipt_id}


def project(identity: dict[str, Any], logical: str, before_canonical: str,
            after_canonical: str) -> dict[str, Any]:
    readable = identity.get("exists") is True and identity.get("sha") is not None
    return {
        "logical_case_path": logical,
        "owner_kind": identity.get("kind"),
        "byte_length": identity.get("length") if readable else "UNREADABLE_AT_REGISTERED_STAGE",
        "content_sha256": identity.get("sha") if readable else "UNREADABLE_AT_REGISTERED_STAGE",
        "link_count": identity.get("nlink") if identity.get("nlink") is not None else "UNREADABLE_AT_REGISTERED_STAGE",
        "symlink_or_reparse": identity.get("type") in ("nonregular", "reparse", "symlink"),
        "logical_link_target": "none" if identity.get("type") in ("regular", "missing") else identity.get("type"),
        "single_open_handle": identity.get("single_open_handle") is True,
        "opened_handle_stable": identity.get("opened_handle_stable") is True,
        "pathname_matches_opened_handle": identity.get("pathname_matches_opened_handle") is True,
        "substitution_detected": identity.get("substitution_detected") is True,
        "canonical_before_sha256": before_canonical,
        "canonical_after_sha256": after_canonical,
    }


def project_trace(before: dict[str, Any], after: dict[str, Any],
                  resealed: list[str], entered: list[str],
                  trace_digest: str, rejection: dict[str, str]) -> dict[str, Any]:
    """Stable v298 projection; host-specific file ids remain local only."""
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


def _same_identity(expected: dict[str, Any], actual: dict[str, Any]) -> bool:
    fields = ("kind", "path", "exists", "type", "length", "sha", "dev", "ino",
              "nlink", "single_open_handle", "opened_handle_stable",
              "pathname_matches_opened_handle", "substitution_detected")
    return all(expected.get(field) == actual.get(field) for field in fields)


def reconfirm_baseline(counter: Counter, manifest_id: dict[str, Any],
                       receipt_id: dict[str, Any]) -> bool:
    """Re-read immutable owners through a fresh one-handle pin verifier."""
    verifier = AuthenticatedFiles(counter)
    _, manifest_now = verifier.fetch(
        REPO / MANIFEST, "baseline_manifest_recheck",
        pin=(MANIFEST_SIZE, MANIFEST_DIGEST))
    _, receipt_now = verifier.fetch(
        REPO / RECEIPT, "baseline_receipt_recheck",
        pin=(RECEIPT_SIZE, RECEIPT_DIGEST))
    if not _same_identity(manifest_id, manifest_now):
        raise InputRefusal("checker:baseline:manifest_identity_changed")
    if not _same_identity(receipt_id, receipt_now):
        raise InputRefusal("checker:baseline:receipt_identity_changed")
    return True


def fixture_row(fixture: dict[str, Any], name: str) -> dict[str, Any]:
    row = fixture.get("checker", {}).get(name)
    if not isinstance(row, dict):
        raise InputRefusal("checker:fixture:missing_expected:" + name)
    required = {"owner", "identity_kind", "ordinary_validator", "stage",
                "first_rejection", "allowed_downstream_reseals", "logical_case_path"}
    if set(row) != required or set(row["first_rejection"]) != {"validator", "stage", "narrow_reason"}:
        raise InputRefusal("checker:fixture:expected_shape:" + name)
    return row


def check_evidence(evidence: dict[str, Any], fixture: dict[str, Any],
                   entered_events: list[dict[str, Any]]) -> None:
    expected = fixture_row(fixture, evidence["id"])
    if evidence["owner"] != expected["owner"] or evidence["identity_kind"] != expected["identity_kind"]:
        raise InputRefusal("checker:fixture:owner_binding:" + evidence["id"])
    if evidence["before_identity"]["logical_case_path"] != expected["logical_case_path"]:
        raise InputRefusal("checker:fixture:logical_case:" + evidence["id"])
    matching_events = [event for event in entered_events
                       if event.get("validator") == expected["ordinary_validator"]
                       and event.get("stage") == expected["stage"]]
    if len(matching_events) != 1:
        raise InputRefusal("checker:fixture:ordinary_event:" + evidence["id"])
    if evidence["first_rejection"] != expected["first_rejection"]:
        raise InputRefusal("checker:fixture:first_rejection:" + evidence["id"])
    if evidence["resealed_nodes"] != expected["allowed_downstream_reseals"]:
        raise InputRefusal("checker:fixture:reseals:" + evidence["id"])
    if evidence["baseline_revalidated"] is not True or evidence["terminal_count"] != 1:
        raise InputRefusal("checker:fixture:evidence_liveness:" + evidence["id"])


def alter_receipt(name: str, receipt: dict[str, Any]) -> None:
    if name == "per_layer_ordinal":
        receipt["Delta0"]["presentation"]["rows"][0]["ordinal"] += 1
    elif name == "normal_generation_proof":
        receipt["Delta0"]["presentation"]["normal_generation_proof"]["Gamma_cayley_edge_count"] += 1
    elif name == "bridge_typed_occurrence_ledger":
        receipt["bridge"]["occurrence_ledger"][0]["block"] = "H1_mutated"
    elif name == "evaluator_abi_canary":
        receipt["evaluator"]["coordinate_widths"][0] += 1
    else:
        raise InputRefusal("checker:mutation:receipt_case")


def run_case(name: str, base: dict[str, Any], fixture: dict[str, Any],
             meter: Counter, workspace: Path, files: AuthenticatedFiles) -> dict[str, Any]:
    meter.add("mutations")
    before_role = "manifest_id" if name == "authority_binding" else "receipt_id"
    observed_role = "manifest" if name == "authority_binding" else "receipt"
    original_manifest = base["route"].manifest
    original_receipt = base["route"].receipt
    manifest_path, receipt_path, local = original_manifest, original_receipt, None
    resealed: list[str] = []
    if name == "authority_binding":
        local = workspace
        changed = copy.deepcopy(base["manifest"])
        changed["accepted"] = False
        manifest_path = workspace / "manifest.json"
        durable_replace(manifest_path, reseal(changed, meter), workspace, meter)
        resealed = ["manifest.self_digest_sha256"]
    elif name == "canonical_input_bytes":
        local = workspace
        altered = bytearray(base["receipt_raw"])
        if not altered:
            raise InputRefusal("checker:mutation:empty_owner")
        altered[-1] ^= 1
        receipt_path = workspace / RECEIPT_FILE
        durable_replace(receipt_path, bytes(altered), workspace, meter)
    elif name == "resolved_path_traversal":
        receipt_path = workspace.parent / (RECEIPT_FILE + ".outside")
    elif name in {"per_layer_ordinal", "normal_generation_proof",
                  "bridge_typed_occurrence_ledger", "evaluator_abi_canary"}:
        local = workspace
        altered_receipt = copy.deepcopy(base["receipt"])
        alter_receipt(name, altered_receipt)
        receipt_path = workspace / RECEIPT_FILE
        receipt_raw = reseal(altered_receipt, meter)
        durable_replace(receipt_path, receipt_raw, workspace, meter)
        altered_manifest = copy.deepcopy(base["manifest"])
        altered_manifest["accepted_receipt_basename"] = receipt_path.name
        altered_manifest["receipt"] = {"basename": receipt_path.name,
                                        "bytes": len(receipt_raw),
                                        "sha256": sha(receipt_raw),
                                        "self_digest_sha256": altered_receipt["self_digest_sha256"]}
        manifest_path = workspace / "manifest.json"
        durable_replace(manifest_path, reseal(altered_manifest, meter), workspace, meter)
        resealed = ["receipt.self_digest_sha256", "manifest.receipt.bytes",
                    "manifest.receipt.sha256", "manifest.receipt.self_digest_sha256",
                    "manifest.self_digest_sha256"]
    else:
        raise InputRefusal("checker:mutation:case")

    journal = Journal(meter)
    route = Route(manifest_path, receipt_path, local,
                  RECEIPT_FILE if name == "resolved_path_traversal" else None)
    try:
        ordinary(route, files, journal)
    except NarrowRejection as failure:
        journal.terminal()
        after = journal.identities.get(observed_role)
        if after is None and name == "resolved_path_traversal":
            after = journal.identities.get("receipt.path", raw_identity(receipt_path, "path"))
        if after is None or base[before_role] == after:
            raise InputRefusal("checker:mutation:identity")
        expected = fixture_row(fixture, name)
        before_canonical = object_sha(base["manifest"] if before_role == "manifest_id" else base["receipt"])
        after_canonical = journal.canonical_after.get(
            observed_role,
            "UNREADABLE_AT_REGISTERED_STAGE")
        first = {"validator": failure.validator,
                 "stage": failure.stage, "narrow_reason": failure.token}
        before_projection = project(base[before_role], expected["logical_case_path"],
                                    before_canonical, before_canonical)
        after_projection = project(after, expected["logical_case_path"],
                                   before_canonical, after_canonical)
        evidence = {
            "id": name, "owner": expected["owner"],
            "identity_kind": expected["identity_kind"],
            "before_identity": before_projection,
            "after_identity": after_projection,
            "resealed_nodes": resealed, "event_trace_digest": journal.trace_sha(),
            "entered_validators": [item["validator"] for item in journal.entries],
            "first_rejection": first,
            "baseline_revalidated": base["baseline_revalidated"],
            "terminal_count": journal.terminal_count,
        }
        evidence["projection"] = project_trace(
            before_projection, after_projection, resealed,
            evidence["entered_validators"], evidence["event_trace_digest"], first)
        check_evidence(evidence, fixture, journal.entries)
        return evidence
    raise MutationAccepted("checker:mutation_accepted:" + name)


def load_fixture(path: Path, reader: AuthenticatedFiles) -> dict[str, Any]:
    raw, _ = reader.fetch(path, "fixture")
    fixture = parse(raw, "fixture")
    if fixture.get("schema") != SCHEMA + "/authority-fixture/v1" or fixture.get("covered_rows") != [1, 2, 3, 4, 5, 6, 7]:
        raise InputRefusal("checker:fixture:scope")
    if (fixture.get("remaining_rows") != list(range(8, 49)) or
            fixture.get("candidate_only") is not True or
            fixture.get("full_a4_selftest") is not False or
            fixture.get("synthetic") is not False):
        raise InputRefusal("checker:fixture:scope")
    if (not isinstance(fixture.get("checker"), dict) or
            set(fixture["checker"]) != set(CASES)):
        raise InputRefusal("checker:fixture:checker_rows")
    if fixture.get("immutable_input_identities") != {
            "task198_receipt": {"bytes": RECEIPT_SIZE, "sha256": RECEIPT_DIGEST,
                                 "self_digest_sha256": "c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f"},
            "task198_manifest": {"bytes": MANIFEST_SIZE, "sha256": MANIFEST_DIGEST,
                                  "self_digest_sha256": "0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684"}}:
        raise InputRefusal("checker:fixture:immutable_inputs")
    return fixture


def run(fixture: dict[str, Any]) -> dict[str, Any]:
    meter = Counter()
    files = AuthenticatedFiles(meter)
    baseline_journal = Journal(meter)
    # Keep receipt/manifest out of this preflight so ordinary entry events
    # precede their actual reads.  The other seven physical pins are checked
    # once and cached for the complete tranche.
    for rel, size, digest in PINNED_FILES[2:]:
        baseline_journal.before("checker.transport.source_pin", "transport", rel)
        files.fetch(REPO / rel, rel, pin=(size, digest), journal=baseline_journal)
    route = Route(REPO / MANIFEST, REPO / RECEIPT, None)
    baseline = ordinary(route, files, baseline_journal)
    baseline["route"] = route
    baseline["manifest"] = baseline["manifest"]
    baseline["receipt"] = baseline["receipt"]
    baseline["manifest_id"] = baseline["manifest_id"]
    baseline["receipt_id"] = baseline["receipt_id"]
    baseline["baseline_revalidated"] = reconfirm_baseline(
        meter, baseline["manifest_id"], baseline["receipt_id"])
    baseline["baseline_event_trace_digest"] = baseline_journal.trace_sha()
    answers: list[dict[str, Any]] = []
    for name in CASES:
        workspace = new_workspace()
        try:
            answers.append(run_case(name, baseline, fixture, meter, workspace, files))
        finally:
            if workspace.exists():
                shutil.rmtree(workspace)
    return {"schema": SCHEMA, "candidate_only": True,
            "covered_rows": [1, 2, 3, 4, 5, 6, 7],
            "remaining_rows": list(range(8, 49)), "full_a4_selftest": False,
            "baseline": {"receipt": project(
                            baseline["receipt_id"], "task198/receipt/baseline",
                            object_sha(baseline["receipt"]), object_sha(baseline["receipt"])),
                         "manifest": project(
                            baseline["manifest_id"], "task198/manifest/baseline",
                            object_sha(baseline["manifest"]), object_sha(baseline["manifest"])),
                         "event_trace_digest": baseline["baseline_event_trace_digest"]},
            "rows": answers, "resource": meter.export()}


def emit(path: Path, value: dict[str, Any], meter: Counter) -> None:
    target = path if path.is_absolute() else REPO / path
    target = target.resolve(strict=False)
    if not under(target, REPO / "ci" / "out"):
        raise InputRefusal("checker:output:containment")
    body = copy.deepcopy(value)
    body["self_digest_sha256"] = object_sha(body, meter)
    raw = encode(body)
    meter.add("canonical_bytes", len(raw))
    target.parent.mkdir(parents=True, exist_ok=True)
    workspace = new_workspace()
    try:
        staged = workspace / "output.json"
        durable_replace(staged, raw, workspace, meter)
        os.replace(staged, target)
        directory = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", default="search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v1_20260829.json")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    if os.name == "nt":
        raise InputRefusal("checker:windows:one_handle_reparse_unsupported")
    meter = Counter()
    reader = AuthenticatedFiles(meter)
    fixture_path = Path(args.fixture)
    if not fixture_path.is_absolute():
        fixture_path = REPO / fixture_path
    fixture = load_fixture(fixture_path.resolve(), reader)
    result = run(fixture)
    if args.output:
        emit(Path(args.output), result, meter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
