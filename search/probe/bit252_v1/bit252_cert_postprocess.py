#!/usr/bin/env python3
"""
bit252_cert_postprocess.py -- fills the GAP-side raw cert's metadata
placeholders (run id, prereg doc sha256, commit sha) with real values,
matching the pattern in search/probe/hsp7_ci_calib/parse_and_compare.py.
GAP itself has no access to the GitHub Actions run context.
"""
import argparse
import hashlib
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-cert", required=True)
    ap.add_argument("--prereg-doc", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--run-attempt", required=True)
    ap.add_argument("--commit-sha", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.raw_cert, encoding="utf-8") as f:
        cert = json.load(f)

    with open(args.prereg_doc, "rb") as f:
        prereg_sha256 = hashlib.sha256(f.read()).hexdigest()

    cert.pop("run_id_PLACEHOLDER", None)
    cert.pop("prereg_doc_sha256_PLACEHOLDER", None)
    cert.pop("commit_sha_PLACEHOLDER", None)

    cert["run_id"] = args.run_id
    cert["run_attempt"] = args.run_attempt
    cert["prereg_doc_path"] = args.prereg_doc
    cert["prereg_doc_sha256"] = prereg_sha256
    cert["commit_sha"] = args.commit_sha

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(cert, f, ensure_ascii=False, indent=2)

    print(f"Wrote {args.out}")
    print(f"prereg_doc_sha256 = {prereg_sha256}")
    print(f"run_id = {args.run_id}  run_attempt = {args.run_attempt}  commit_sha = {args.commit_sha}")


if __name__ == "__main__":
    main()
