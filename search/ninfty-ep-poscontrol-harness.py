#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-ep-poscontrol-harness.py

The EP full-path positive-control HARNESS -- scaffolding only.

AUTHORISATION BOUNDARY (Sol 便97 P97-4.1, verbatim):
  authorised   : harness schema, catalog schema, non-blind unit fixtures,
                 commit / reveal / adjudication scaffolding.
  NOT authorised: running secret trials, full-path calibration including
                 F-w6, `calibrated_detector = true`, changing EP status.
                 Those require W-6 gate PASS and a re-requested versioned
                 campaign.

This module therefore REFUSES, at run time, to start a blind campaign, and
there is no code path in it that can emit `calibrated_detector: true`. The
existence of the instrument is not the existence of a positive control:
EP stays `uncalibrated/UNKNOWN`.

REPAIRS FROM 便97 W97-4.1, item by item (each has a fixture in
search/test_ninfty_poscontrol.py):
  1. THREE roles, not two (injector / detector / adjudicator).
  2. "blind injection vs absence argument" is NOT an open choice: a
     `calibrated detector` claim requires blind injection; an absence
     argument is a different mathematical result and no substitute.
  3. the commitment is an HMAC over a payload containing a HIGH-ENTROPY
     NONCE -- a bare sha256 of a small option set is dictionary-attackable
     and would leak the injection.
  4. the injector's self-report is not evidence: the adjudicator REPLAYS
     the mutation from the clean base and recomputes the mutated digest.
  5. per-trial EXACT expected vector (stage, primary, sealed and public
     reason vectors, exit code). A range such as "[1]--[5]" is rejected.
  6. null (no-injection) trials are interleaved so false positives are
     measured too, and the injection bit is withheld from the detector.
  7. "full path" = public ingress .. public receipt. A mutation applied to
     an internal function is a unit test and is NOT counted.
  8. data-plane one-lane faults and code-plane tampering are SEPARATE
     families with separately fixed expected codes -- otherwise F-con only
     measures the code-digest gate [12].
  9. an 8-family catalog is coverage of a finite catalog, not a general
     false-negative rate: the claim is scoped to
     `catalog-calibrated under <catalog_digest>`.
 10. a pre-W-6 dry-run receipt (carrying `undetectable_by_construction`)
     is a DIFFERENT schema from a final calibration receipt and the two
     may not be merged.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import secrets

CATALOG_SCHEMA_ID = "mb/ninfty-ep-poscontrol-catalog/v1"
COMMITMENT_SCHEMA_ID = "mb/ninfty-ep-poscontrol-commitment/v1"
DRY_RUN_RECEIPT_SCHEMA_ID = "mb/ninfty-ep-poscontrol-dry-run-receipt/v1"
CALIBRATION_RECEIPT_SCHEMA_ID = "mb/ninfty-ep-poscontrol-calibration-receipt/v1"

# W97-4.1 item 1: THREE roles. The draft v1 table was right and its prose
# said "two"; the prose was the error.
ROLES = ("injector", "detector", "adjudicator")

# W97-4.1 item 7: what "full path" means. A trial that does not traverse
# every one of these is not a full-path trial, whatever it detected.
FULL_PATH_STAGES = (
    "public_ingress",
    "schema_and_digest",
    "registry_resolution",
    "lane_a",
    "lane_b",
    "w6",
    "composition",
    "public_receipt",
)

# W97-4.1 item 8: the data plane and the code plane are different families.
# A fault injected into code is caught by the code-digest gate [12] and
# says nothing about data-plane sensitivity.
PLANES = ("data_plane", "code_plane")

# The fault families. `plane` is normative: F-con is split so that a
# one-lane DATA fault and a code tamper can never be scored together.
FAULT_FAMILIES = {
    "F-pre": {"plane": "data_plane", "injection_point": "precondition (degree/monic/squarefree/"
                                                        "leading coeff/Pell)"},
    "F-thm": {"plane": "data_plane", "injection_point": "theorem-forced identity (gcd / (Or) / (60.5))"},
    "F-att": {"plane": "data_plane", "injection_point": "E-5 attestation vs derived value"},
    "F-nat": {"plane": "data_plane", "injection_point": "native finite partition / branch count / "
                                                        "harmonicity"},
    "F-w6": {"plane": "data_plane", "injection_point": "ramification -> branch incidence swap"},
    "F-nf": {"plane": "data_plane", "injection_point": "NF N-1..N-5 / total degree / infinity / "
                                                       "non-ramification"},
    "F-reg": {"plane": "data_plane", "injection_point": "registry generation / freeze / four-role / era"},
    "F-con-data": {"plane": "data_plane", "injection_point": "one lane's DATA only (cross-lane "
                                                             "concordance)"},
    "F-con-code": {"plane": "code_plane", "injection_point": "one lane's CODE (tamper) -- expected to be "
                                                             "caught by the code-digest gate, which is a "
                                                             "DIFFERENT claim from data-plane sensitivity"},
}

# W97-4.1 item 2: settled, not open.
BLIND_INJECTION_REQUIRED_NOTE = (
    "a `calibrated detector` claim requires blind injection (便96 裁定, restated in 便97 W97-4.1 item 2). "
    "An absence argument -- 'no natural positive exists' -- is a different mathematical result and is "
    "NOT a substitute. This is not an open design choice and the harness does not offer it as one."
)


class NotAuthorised(RuntimeError):
    """Raised by anything Sol did not authorise (P97-4.1)."""


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def new_nonce():
    """W97-4.1 item 3: high-entropy, so the commitment cannot be inverted by
    enumerating the (small) option set."""
    return secrets.token_hex(32)


def new_key():
    return secrets.token_bytes(32)


# ---------------------------------------------------------------------------
# expected vector -- EXACT, per trial (item 5)
# ---------------------------------------------------------------------------

EXPECTED_VECTOR_FIELDS = ("expected_stage", "expected_primary_reason_code",
                          "expected_sealed_reason_vector", "expected_public_reason_vector",
                          "expected_exit_code")


def validate_expected_vector(vector):
    """(ok, errors). A range, a set, or a 'one of these codes' spec is
    REJECTED: 'expected [1]--[5]' is exactly the weak form item 5 names."""
    errors = []
    if not isinstance(vector, dict):
        return False, ["expected vector is not an object"]
    for field in EXPECTED_VECTOR_FIELDS:
        if field not in vector:
            errors.append(f"{field} is absent -- an unstated expectation is not a satisfied one")
    stage = vector.get("expected_stage")
    if not isinstance(stage, str) or not stage:
        errors.append("expected_stage must be one exact stage name")
    primary = vector.get("expected_primary_reason_code")
    if not isinstance(primary, str) or not primary:
        errors.append("expected_primary_reason_code must be exactly one code, not a range or a set")
    for field in ("expected_sealed_reason_vector", "expected_public_reason_vector"):
        value = vector.get(field)
        if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
            errors.append(f"{field} must be an exact ordered list of codes")
        elif any(("-" in v and v.count("[") > 1) or ".." in v for v in value):
            errors.append(f"{field} contains a RANGE such as '[1]--[5]'; ranges are rejected (item 5)")
    if not isinstance(vector.get("expected_exit_code"), int):
        errors.append("expected_exit_code must be an exact integer")
    return (not errors), errors


# ---------------------------------------------------------------------------
# mutation: declarative, so the adjudicator can REPLAY it (item 4)
# ---------------------------------------------------------------------------

def _pointer_parts(pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError(f"not a JSON pointer: {pointer!r}")
    return [p.replace("~1", "/").replace("~0", "~") for p in pointer[1:].split("/")]


def apply_mutation(base_artifact, mutation):
    """Deterministically apply one declarative mutation and return the new
    artifact. Pure: `base_artifact` is not modified."""
    if not isinstance(mutation, dict) or mutation.get("op") not in ("set", "delete"):
        raise ValueError("mutation must be {'op': 'set'|'delete', 'json_pointer': ..., ...}")
    out = json.loads(canonical(base_artifact))
    parts = _pointer_parts(mutation["json_pointer"])
    node = out
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    last = parts[-1]
    if mutation["op"] == "set":
        if isinstance(node, list):
            node[int(last)] = mutation["value"]
        else:
            node[last] = mutation["value"]
    else:
        if isinstance(node, list):
            del node[int(last)]
        else:
            del node[last]
    return out


def replay_and_verify(base_artifact, mutation, claimed_mutated_digest):
    """W97-4.1 item 4: the injector's word is not evidence. The adjudicator
    re-applies the mutation to the clean base and recomputes the digest.
    (ok, recomputed_digest, reason)."""
    try:
        mutated = apply_mutation(base_artifact, mutation)
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        return False, None, f"the declared mutation does not replay against the clean base: {exc}"
    recomputed = sha256_of(mutated)
    if recomputed != claimed_mutated_digest:
        return False, recomputed, ("the replayed mutation does not reproduce the committed mutated "
                                   "artifact digest -- the injector's self-report is contradicted")
    if recomputed == sha256_of(base_artifact):
        return False, recomputed, "the 'mutation' left the artifact unchanged: nothing was injected"
    return True, recomputed, "replayed from the clean base and digest-matched"


# ---------------------------------------------------------------------------
# commitment (item 3 + P97-4.1's exact binding list)
# ---------------------------------------------------------------------------

COMMITMENT_FIELDS = ("campaign_id", "trial_id", "catalog_digest", "base_artifact_digest",
                     "mutation_id", "mutation_parameters", "mutated_artifact_digest",
                     "exact_expected_vector", "null_or_injected", "nonce")


def seal_commitment(payload, key):
    """HMAC_K(canonical({...the exact P97-4.1 field list...})).
    Every field is REQUIRED: a commitment that omits one binds less than it
    claims to."""
    missing = [f for f in COMMITMENT_FIELDS if f not in payload]
    if missing:
        raise ValueError(f"commitment payload is missing required fields: {missing}")
    if payload.get("null_or_injected") not in ("null", "injected"):
        raise ValueError("null_or_injected must be exactly 'null' or 'injected' (item 6)")
    if not isinstance(payload.get("nonce"), str) or len(payload["nonce"]) < 32:
        raise ValueError("the nonce must be a high-entropy string (item 3): a small-option-set digest "
                         "is dictionary-attackable and would leak the injection")
    if payload["null_or_injected"] == "injected":
        ok, errors = validate_expected_vector(payload.get("exact_expected_vector"))
        if not ok:
            raise ValueError(f"exact_expected_vector is not exact: {errors}")
    body = {f: payload[f] for f in COMMITMENT_FIELDS}
    return {"schema_id": COMMITMENT_SCHEMA_ID,
            "commitment": hmac.new(key, canonical(body).encode("utf-8"), hashlib.sha256).hexdigest(),
            "bound_fields": list(COMMITMENT_FIELDS),
            "note": ("the sealed values themselves never appear here, and are never written to a public "
                     "surface even after adjudication (P97-4.1)")}


def verify_commitment(payload, key, sealed):
    return hmac.compare_digest(seal_commitment(payload, key)["commitment"], sealed.get("commitment", ""))


def detector_view(trial):
    """W97-4.1 item 6: the detector must not see the injection bit, the
    expected vector, the mutation, or the trial's position in the order."""
    hidden = {"null_or_injected", "exact_expected_vector", "mutation_id", "mutation_parameters",
              "base_artifact_digest", "nonce", "order_index"}
    return {k: v for k, v in trial.items() if k not in hidden}


# ---------------------------------------------------------------------------
# full-path accounting (item 7) and scope (item 9)
# ---------------------------------------------------------------------------

def is_full_path(traversed_stages):
    """A unit-level mutation of an internal function is a unit test. Only a
    trial that entered at the public ingress and came out at the public
    receipt counts as a full-path trial."""
    if not isinstance(traversed_stages, (list, tuple)):
        return False, ["traversed stages were not recorded -- an unrecorded path is not a full path"]
    missing = [s for s in FULL_PATH_STAGES if s not in traversed_stages]
    return (not missing), missing


def calibration_scope(catalog_digest):
    """W97-4.1 item 9: never 'the detector's false-negative rate'."""
    return (f"catalog-calibrated under {catalog_digest} -- coverage of a FINITE catalog, not a general "
            "false-negative rate. A general rate would require a pre-registered sampling distribution "
            "and trial count.")


# ---------------------------------------------------------------------------
# catalog / receipts
# ---------------------------------------------------------------------------

def build_catalog(entries):
    """entries: [{'mutation_id', 'family', 'json_pointer', 'op', 'value'?}]."""
    errors = []
    for entry in entries:
        family = entry.get("family")
        if family not in FAULT_FAMILIES:
            errors.append(f"unknown fault family {family!r}")
        elif FAULT_FAMILIES[family]["plane"] not in PLANES:
            errors.append(f"family {family!r} declares no plane")
    catalog = {"schema_id": CATALOG_SCHEMA_ID, "families": FAULT_FAMILIES,
               "planes": list(PLANES), "entries": sorted(entries, key=canonical), "errors": errors}
    catalog["catalog_digest"] = sha256_of({k: v for k, v in catalog.items() if k != "catalog_digest"})
    return catalog


def dry_run_receipt(catalog_digest, trials, undetectable_by_construction):
    """W97-4.1 item 10: a PRE-W-6 dry run. Its own schema id, its own field
    for the families that cannot be detected yet, and an explicit statement
    that it may not be merged into a calibration receipt."""
    return {
        "schema_id": DRY_RUN_RECEIPT_SCHEMA_ID,
        "catalog_digest": catalog_digest,
        "trials": trials,
        "undetectable_by_construction": sorted(undetectable_by_construction),
        "blind": False,
        "is_calibration": False,
        "calibrated_detector": False,
        "ep_status": "uncalibrated/UNKNOWN",
        "merge_rule": ("this dry-run receipt may NOT be merged into, or reported as, a final full-path "
                       "calibration receipt (schema " + CALIBRATION_RECEIPT_SCHEMA_ID + "). The families "
                       "listed as undetectable_by_construction are excluded from every sensitivity "
                       "claim, and a run that excludes any family is not 'full-path calibration'."),
        "w6_note": ("W-6 is OPEN, so F-w6 trials would measure 'that route does not exist', not "
                    "'the detector is insensitive' (draft v1 section 4)."),
    }


def run_blind_campaign(*_args, **_kwargs):
    """NOT AUTHORISED (P97-4.1). Kept as an explicit refusal so that the
    absence of a blind run is a property of the code, not of anyone's
    restraint."""
    raise NotAuthorised(
        "a secret/blind trial run, full-path calibration including F-w6, `calibrated_detector = true` "
        "and any EP status change are NOT authorised (Sol 便97 P97-4.1). They require W-6 gate PASS and "
        "a re-requested versioned campaign. " + BLIND_INJECTION_REQUIRED_NOTE)


def harness_status():
    """What this instrument is allowed to say about EP -- and it is not much."""
    return {
        "roles": list(ROLES),
        "blind_campaign_authorised": False,
        "calibrated_detector": False,
        "ep_status": "uncalibrated/UNKNOWN",
        "note": ("the existence of the harness is not the existence of a positive control (draft v1 "
                 "standing note; 便97 F97-4.1 approves the separation of telemetry from calibration)"),
        "blind_injection_required": BLIND_INJECTION_REQUIRED_NOTE,
    }
