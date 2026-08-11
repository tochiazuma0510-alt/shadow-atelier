#!/usr/bin/env python
# crosscheck/check_s4_iso_i3_extract.py
# Independent checker for search/certs/s4_iso_i3_extract_v1_20260812.json (裁定886).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT import search/s4_iso_i3_extract_v1.py -- independently
# re-reads the SAME source files at the cited line numbers and confirms the quoted/paraphrased
# content is actually present there (not trusting the search script's prose without checking).
import json
import re
import sys
from pathlib import Path

# avoid UnicodeEncodeError on Windows consoles using a non-UTF-8 codepage (cp932) when a
# fail() message happens to embed the source document's own unicode math symbols (e.g. the
# markdown-embedded LaTeX arrow characters) -- reconfigure stdout to UTF-8 defensively.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent
CERT_PATH = REPO_ROOT / "search" / "certs" / "s4_iso_i3_extract_v1_20260812.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def get_line(path, line_no):
    text = (REPO_ROOT / path).read_text(encoding="utf-8", errors="ignore")
    lines = text.split("\n")
    if 1 <= line_no <= len(lines):
        return lines[line_no - 1]
    return None


def main():
    cert = json.load(open(CERT_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/s4_iso_i3_extract_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/s4_iso_i3_extract_v1")

    # (A) F1: SPLIT-NULL's statement at ihnec_v1.md line 374 contains "N'∈I" (independently
    # re-read, checking the KEY textual marker not the full paraphrase)
    line374 = get_line("docs/notes/ihnec_v1.md", 374)
    if line374 is None or "N'\\in I" not in line374:
        fail(f"F1: line 374 of ihnec_v1.md does not contain \"N'\\in I\" -- "
             f"got: {line374!r}")
    else:
        ok("F1: independently confirmed ihnec_v1.md line 374 contains \"N'\\in I\" "
           "(SPLIT-NULL's stated precondition)")

    # (B) F2: lines 319 and 411 contain the (S4-ISO) tag and "UNKNOWN"
    line319 = get_line("docs/notes/ihnec_v1.md", 319)
    line411 = get_line("docs/notes/ihnec_v1.md", 411)
    if line319 is None or "S4-ISO" not in line319 or "UNKNOWN" not in line319:
        fail(f"F2a: line 319 of ihnec_v1.md missing 'S4-ISO' or 'UNKNOWN' marker -- got: {line319!r}")
    else:
        ok("F2a: independently confirmed ihnec_v1.md line 319 contains '(S4-ISO)' and 'UNKNOWN'")
    if line411 is None or "S4-ISO" not in line411 or "UNKNOWN" not in line411:
        fail(f"F2b: line 411 of ihnec_v1.md missing 'S4-ISO' or 'UNKNOWN' marker -- got: {line411!r}")
    else:
        ok("F2b: independently confirmed ihnec_v1.md line 411 contains '(S4-ISO)' and 'UNKNOWN'")

    # (C) F3: surj_s4_v2.md line 78 contains the hardcoded-UNKNOWN claim
    line78 = get_line("docs/notes/surj_s4_v2.md", 78)
    if line78 is None or "isolated" not in line78 or "UNKNOWN" not in line78 or "week3-psl-common.g" not in line78:
        fail(f"F3: line 78 of surj_s4_v2.md missing expected markers -- got: {line78!r}")
    else:
        ok("F3: independently confirmed surj_s4_v2.md line 78 references the hardcoded "
           "'isolated: UNKNOWN' field and week3-psl-common.g")

    # (D) F4: surj_s4_v2.md line 259 contains the two-tier cert-vs-document distinction
    line259 = get_line("docs/notes/surj_s4_v2.md", 259)
    if line259 is None or "UNKNOWN" not in line259 or "true" not in line259:
        fail(f"F4: line 259 of surj_s4_v2.md missing expected markers -- got: {line259!r}")
    else:
        ok("F4: independently confirmed surj_s4_v2.md line 259 documents the "
           "cert-says-UNKNOWN vs table-says-true discrepancy")

    # (E) F5: auto_settled_check_v1.md line 262 explicitly excludes (S4-ISO)/PSL(2,8)
    # (note: source uses LaTeX "\mathrm{PSL}(2,8)" -- match PSL and (2,8) as separate tokens,
    # not a single contiguous substring, since the \mathrm{} macro splits them)
    line262 = get_line("docs/notes/auto_settled_check_v1.md", 262)
    if line262 is None or "PSL" not in line262 or "(2,8)" not in line262 or "S4-ISO" not in line262 or "適用できない" not in line262:
        fail(f"F5: line 262 of auto_settled_check_v1.md missing expected markers -- "
             f"got: {line262!r}")
    else:
        ok("F5: independently confirmed auto_settled_check_v1.md line 262 explicitly "
           "excludes the PSL(2,8)/(S4-ISO) window from the VERBAL-ISO closure route")

    # (F) F6: 裁定219/【SD-a】 traceable in e1_canonical_v1.md
    text_e1 = (REPO_ROOT / "docs/notes/e1_canonical_v1.md").read_text(encoding="utf-8", errors="ignore")
    if not re.search(r"SD-a.{0,20}裁定\s*219|裁定\s*219.{0,20}SD-a", text_e1):
        fail("F6: 【SD-a】/裁定219 co-occurrence not confirmed in e1_canonical_v1.md")
    else:
        ok("F6: independently confirmed 【SD-a】/裁定219 co-occurrence in e1_canonical_v1.md")

    # (G) top-level conclusion consistency: given F2-F5 all point to 'open, not established',
    # n_s4_isolated_established should be False
    if cert.get("n_s4_isolated_established") is not False:
        fail(f"n_s4_isolated_established = {cert.get('n_s4_isolated_established')}, "
             f"expected False given findings F2-F5 (all point to OPEN status)")
    else:
        ok("n_s4_isolated_established = False, consistent with findings F2-F5")

    if cert.get("gate_v2_i3_hypothesis_confirmed") is not True:
        fail("gate_v2_i3_hypothesis_confirmed should be True given F1's direct confirmation")
    else:
        ok("gate_v2_i3_hypothesis_confirmed = True, consistent with F1")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有; all cited "
              "line-level textual claims independently re-read from source and confirmed "
              "present, not trusted from the search script's prose alone)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
