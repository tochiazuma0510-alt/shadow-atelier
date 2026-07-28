#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/certs/assemble_full_witness_cert.py

Standalone assembly step (NOT a lane implementation file). Splices the
independently-generated chart_overlap_witnesses / pushforward_compatibility_witness
content (search/ninfty-witness-gen.py) into the base certificate that lane
A's own real generateCertificate() produces (via
search/certs/gen_full_cert_base.mjs), replacing ONLY those two
still-unmigrated fields. Everything else in the base certificate
(component_bijection, exact_point_equality_witnesses,
distinctness_witnesses, multiplicity_equalities,
total_coverage_and_no_extra_component_witness, all scalar/native fields)
is passed through UNCHANGED -- this file does not compute or alter any of
that content, and does not import ninfty-searcher-v2.mjs, ninfty-verifier-a.mjs,
or ninfty-verifier-b.py.

Usage:
  node search/certs/gen_full_cert_base.mjs > /tmp/base_cert.json
  python search/certs/assemble_full_witness_cert.py /tmp/base_cert.json > search/certs/full_witness_fixture_01.json
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))  # so `import ninfty_witness_gen`-style loading works via importlib below

import importlib.util


def _load_module(name, relpath):
    path = HERE.parent / relpath
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


wgen = _load_module("ninfty_witness_gen", "ninfty-witness-gen.py")


def assemble(base_cert_path, out_path=None):
    with open(base_cert_path, "r", encoding="utf-8") as f:
        base = json.load(f)

    cert = base["certificate"]
    native = base["native"]

    witnesses = wgen.generate()

    cert["chart_overlap_witnesses"] = witnesses["chart_overlap_witnesses"]
    cert["pushforward_compatibility_witness"] = witnesses["pushforward_compatibility_witness"]
    if wgen.CHART_B_ID not in cert.get("chart_ids", []):
        cert["chart_ids"] = list(cert.get("chart_ids", [])) + [wgen.CHART_B_ID]

    # P-3.3 (verifier B) recomputes sha256 over exactly the object that
    # produced native_artifact_digest on the node side (lane A's digestOf()
    # call in buildSearcherNative hashes ONLY {ramification_divisor_on_C_ref,
    # branch_divisor_on_P1_ref} -- NOT the full native object with
    # native_schema_id/native_schema_digest/native_artifact_digest also
    # present). native_a/native_b must therefore be reduced to that same
    # two-key shape for the digest re-check to be meaningful rather than a
    # spurious mismatch.
    native_digest_input = {
        "ramification_divisor_on_C_ref": native["ramification_divisor_on_C_ref"],
        "branch_divisor_on_P1_ref": native["branch_divisor_on_P1_ref"],
    }

    out = {
        "_description": (
            "Full-witness positive certificate (裁定126/127/128): base fields "
            "from lane A's own real generateCertificate() on the genuine Pell "
            "fixture checker_pos_01.json (already flat + divisor_object-tagged "
            "for W-1/W-2/W-2prime/W-3/W-5 per 裁定127/128); chart_overlap_witnesses "
            "(W-4) and pushforward_compatibility_witness (W-6) REPLACED with "
            "independently-generated content from search/ninfty-witness-gen.py "
            "(ideal-equality / reciprocal-chart construction, no Qbar root-finding)."
        ),
        "certificate": cert,
        "native_a": native_digest_input,  # same convention as existing lanea selftest MOCK: searcher_native == checker_native
        "native_b": native_digest_input,
    }

    text = json.dumps(out, indent=2, ensure_ascii=False)
    if out_path:
        Path(out_path).write_text(text, encoding="utf-8")
    else:
        print(text)
    return out


if __name__ == "__main__":
    base_path = sys.argv[1] if len(sys.argv) > 1 else None
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    if not base_path:
        print("usage: assemble_full_witness_cert.py <base_cert.json> [out.json]", file=sys.stderr)
        raise SystemExit(2)
    assemble(base_path, out_path)
