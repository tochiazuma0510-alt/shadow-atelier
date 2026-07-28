#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/fixtures/ninfty/gen_native_fixtures.py

Commander directive 115 (EP round-1 packaging fix 2): populate each
cert_pos/neg_0{1,2,3}.json with real searcher_native / checker_native /
native_artifact_digest fields, machine-generated so verifier-b.py's P-3.3
check (native_artifact_digest recomputation) has real content to check.

checker_native content = the ACTUAL, literal output of
search/ninfty-checker.py's run_checker() on the correspondingly-numbered
checker_pos/neg_0N.json curve fixture (not a hand-typed stand-in).

searcher_native content: lane A (searcher, node runtime) is invisible to
this implementer by design (runtime/independence separation, contract
sec.7 C-7 / spec sec.3 lane split) -- there is no real lane-A output this
script can read or generate on lane A's behalf. It is filled with an
explicitly-labeled STAND-IN object (never claimed to be real lane-A
output) whose only purpose is to give P-3.3 something concrete to
recompute a digest over and compare, so the verifier-B code path for
BOTH native slots is exercised end-to-end by the test suite. This is
recorded plainly in the object itself and in the report, not hidden.

Digest scheme matches search/ninfty-verifier-b.py's own
recomputed_digest() exactly: json.dumps(obj, sort_keys=True,
separators=(",", ":")) (default ensure_ascii=True), sha256 hex.

Idempotent: re-running regenerates the same native_a/native_b content and
(since checker.py's output is deterministic) the same digests, as long as
checker.py / the underlying curve fixtures are unchanged.
"""
import hashlib
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SEARCH_DIR = os.path.dirname(os.path.dirname(HERE))


def _load_module(name, relpath):
    path = os.path.join(SEARCH_DIR, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


chk = _load_module("ninfty_checker", "ninfty-checker.py")


def recompute_digest(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


PAIRS = [
    ("cert_pos_01.json", "checker_pos_01.json"),
    ("cert_pos_02.json", "checker_pos_02.json"),
    ("cert_pos_03.json", "checker_pos_03.json"),
    ("cert_neg_01.json", "checker_neg_01.json"),
    ("cert_neg_02.json", "checker_neg_02.json"),
    ("cert_neg_03.json", "checker_neg_03.json"),
]


def build_searcher_stand_in(cert_candidate_ref, cert):
    """
    Explicitly-labeled stand-in for lane A's (searcher, node) native
    output. NEVER claimed to be real lane-A data -- this implementer has
    never read lane A's code or output (operating constraint). Its shape
    mirrors the certificate's own declared pushforward witness so it is
    at least internally plausible for the fixture's own W-6 check, but
    its ONLY real purpose here is to give P-3.3 (native_artifact_digest
    recomputation) something concrete on the searcher_native side.
    """
    # 裁定128: pushforward_compatibility_witness is now a 2-entry array
    # (one entry per divisor_object token), not a single object. Use the
    # first well-formed entry found (toy fixtures duplicate content across
    # both tokens, so any single entry is representative).
    pf_container = cert.get("pushforward_compatibility_witness", [])
    pf = {}
    if isinstance(pf_container, list):
        for entry in pf_container:
            if isinstance(entry, dict) and "ramification_points" in entry:
                pf = entry
                break
    elif isinstance(pf_container, dict):
        pf = pf_container  # pre-裁定128 shape, tolerated for robustness
    return {
        "_stand_in_disclosure": (
            "THIS IS NOT REAL LANE-A (searcher, node runtime) OUTPUT. "
            "Lane A is invisible to this lane-B implementer by design "
            "(contract sec.7 C-7 / spec sec.3 lane split); no such data "
            "was available to generate. This object exists solely so "
            "verifier-b.py's P-3.3 native_artifact_digest check has "
            "concrete content on the searcher_native side to recompute "
            "and compare against for lane-B unit testing."
        ),
        "candidate_ref": cert_candidate_ref,
        "lane": "A (searcher) -- STAND-IN, not authoritative",
        "ramification_divisor_on_C": pf.get("ramification_points", []),
        "branch_divisor_on_P1": pf.get("branch_points", []),
    }


def main():
    for cert_fname, checker_fname in PAIRS:
        cert_path = os.path.join(HERE, cert_fname)
        checker_path = os.path.join(HERE, checker_fname)

        with open(cert_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        with open(checker_path, "r", encoding="utf-8") as f:
            checker_candidate = json.load(f)

        cert = payload["certificate"]

        # checker_native: the ACTUAL run_checker() output on the paired
        # curve fixture -- machine-generated, not hand-typed.
        native_b = chk.run_checker(checker_candidate)
        native_b["_provenance"] = (
            f"literal output of search/ninfty-checker.py run_checker() "
            f"on search/fixtures/ninfty/{checker_fname}"
        )
        digest_b = recompute_digest(native_b)

        # searcher_native: explicitly-labeled stand-in (see docstring).
        native_a = build_searcher_stand_in(cert.get("candidate_ref", cert_fname), cert)
        digest_a = recompute_digest(native_a)

        cert["searcher_native"] = {
            "native_schema_id": "mb/ninfty-stage2-predicate/v18#searcher-native-stand-in",
            "native_schema_digest": "lane-b-stand-in-schema-not-authoritative",
            "ramification_divisor_on_C_ref": "native_a.ramification_divisor_on_C",
            "branch_divisor_on_P1_ref": "native_a.branch_divisor_on_P1",
            "native_artifact_digest": digest_a,
        }
        cert["checker_native"] = {
            "native_schema_id": "search/ninfty-checker.py#run_checker-output/v1",
            "native_schema_digest": chk.sha256_of({"module": "ninfty-checker.py", "function": "run_checker"}),
            "ramification_divisor_on_C_ref": "native_b.rootpart_a / native_b.pushforward_detail",
            "branch_divisor_on_P1_ref": "native_b.pushforward_detail.declared_branch",
            "native_artifact_digest": digest_b,
        }

        payload["native_a"] = native_a
        payload["native_b"] = native_b

        with open(cert_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, indent=2, ensure_ascii=True)
            f.write("\n")

        print(f"{cert_fname}: searcher_native digest={digest_a[:16]}... "
              f"checker_native digest={digest_b[:16]}... (from {checker_fname})")


if __name__ == "__main__":
    main()
