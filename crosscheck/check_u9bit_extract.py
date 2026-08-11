#!/usr/bin/env python
# crosscheck/check_u9bit_extract.py
# Independent checker for search/certs/u9bit_extract_v1_20260812.json (U9-BIT-EXTRACT,
# 裁定857/859).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT import search/u9bit_extract_v1.py -- re-implements the
# file-scanning search FROM SCRATCH (own regex patterns, own file enumeration) and independently
# re-verifies the key documentary claims (the specific quoted sentences from surj_s4_v1/v2.md
# and u9_extraction_plan_v1.md) by re-reading those files directly, not trusting the search
# script's manual_reading_findings prose without checking the underlying text is actually there.
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CERT_PATH = REPO_ROOT / "search" / "certs" / "u9bit_extract_v1_20260812.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def main():
    cert = json.load(open(CERT_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/u9bit_extract_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/u9bit_extract_v1")

    if cert.get("extraction_succeeded") is not False:
        fail(f"extraction_succeeded = {cert.get('extraction_succeeded')}, want False")
    else:
        ok("extraction_succeeded = False")

    # (A) independently re-verify the quoted claims by re-reading the source files directly
    # NOTE: exact contiguous-substring matching failed on the first pass because these are
    # LaTeX-in-Markdown documents where "$" math-mode delimiters and "**" bold markers are
    # interleaved with the prose in ways that break naive substring copies (e.g. the actual
    # text is "u_{S4}$ の値には触れていない", with a "$" between the LaTeX symbol and the
    # Japanese text) -- using regex with a bounded gap between the symbol and the key phrase
    # instead, which is robust to markdown-delimiter interleaving while still requiring true
    # textual proximity (not just both substrings appearing anywhere in the file).
    checks = [
        {
            "file": "docs/notes/surj_s4_v1.md",
            "pattern": r"u_\{?S4\}?.{0,15}触れていない",
            "label": "surj_s4_v1.md's 'u_{S4}'s value not touched' statement",
        },
        {
            "file": "docs/notes/surj_s4_v2.md",
            "pattern": r"u_\{?S4\}?.{0,15}触れない",
            "label": "surj_s4_v2.md's 'u_{S4}'s value not touched' statement",
        },
        {
            "file": "docs/notes/u9_extraction_plan_v1.md",
            "pattern": r"u_9.{0,10}計算.{0,5}推定.{0,5}示唆しない",
            "label": "u9_extraction_plan_v1.md's self-constraint against computing u_9",
        },
        {
            "file": "docs/notes/u9_extraction_plan_v1.md",
            "pattern": r"u_5.{0,10}まだ抽出されていない",
            "label": "u9_extraction_plan_v1.md's confirmation that u_5 (the n=5 precedent) is ALSO unextracted",
        },
        {
            "file": "docs/notes/ideas_ent_targets_v1.md",
            "pattern": r"u_9.{0,10}実測状態.{0,10}registry.{0,10}確認要",
            "label": "ideas_ent_targets_v1.md's disclosure that u_9's measurement status needs confirmation",
        },
    ]
    for c in checks:
        p = REPO_ROOT / c["file"]
        if not p.exists():
            fail(f"{c['label']}: file {c['file']} does not exist")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if not re.search(c["pattern"], text):
            fail(f"{c['label']}: expected pattern not found in {c['file']} "
                 f"(independently re-read) -- the cert's claim may be inaccurate")
        else:
            ok(f"{c['label']}: independently confirmed present in {c['file']}")

    # (B) LEDGER zero-hits re-verified independently
    ledger_path = REPO_ROOT / "provenance" / "LEDGER.md"
    ledger_text = ledger_path.read_text(encoding="utf-8", errors="ignore")
    u9_hits = len(re.findall(r"u_9\b", ledger_text))
    uS4_hits = len(re.findall(r"u_\{?S4\}?\b", ledger_text))
    if u9_hits != 0 or uS4_hits != 0:
        fail(f"LEDGER.md independently re-scanned: u_9 hits={u9_hits}, u_S4 hits={uS4_hits} "
             f"(cert claims 0 hits for both)")
    else:
        ok("LEDGER.md independently re-scanned: 0 hits for both u_9 and u_S4 (confirms cert's claim)")

    # (C) files_scanned sanity: independently count md/json files in the same scope
    search_dirs = [REPO_ROOT / "docs" / "notes", REPO_ROOT / "docs" / "scout"]
    certs_dir = REPO_ROOT / "search" / "certs"
    count = 1  # LEDGER.md
    for d in search_dirs:
        if d.exists():
            count += len(list(d.rglob("*.md")))
    if certs_dir.exists():
        count += len(list(certs_dir.rglob("*.md")))
        count += len(list(certs_dir.rglob("*.json")))
    cert_count = cert.get("files_scanned")
    # allow some slack since exact glob semantics/duplicate-path handling can differ slightly
    # between independent implementations -- flag only a LARGE discrepancy (>5%) as suspicious
    if cert_count is None:
        fail("files_scanned missing from cert")
    elif abs(count - cert_count) > max(10, 0.05 * cert_count):
        fail(f"files_scanned sanity: independently counted ~{count} candidate files, "
             f"cert reports {cert_count} -- large discrepancy")
    else:
        ok(f"files_scanned sanity: independently counted ~{count} candidate files, "
           f"cert reports {cert_count} (consistent within tolerance)")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有; the key "
              "documentary claims underlying the negative extraction result were independently "
              "re-read from source, not trusted from the search script's prose alone)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
