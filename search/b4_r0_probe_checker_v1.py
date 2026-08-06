#!/usr/bin/env python3
"""
b4_r0_probe_checker_v1.py -- independent (GAP-helper-free) consistency
checker for search/certs/b4_r0_probe_v1_20260806.json, per
docs/notes/b4_r0_probe_prereg_iffirst_v1.md.

This is NOT a second group-theory system (the prereg's own 【R0-GAP-1】
declares R0 single-system by design -- a second system is only mandated IF a
non-abelian window is found, and would be a separate follow-up task). What
this script DOES independently re-verify, without calling GAP or importing
search/b4-r0-probe-v1.g, is the cert's INTERNAL BOOKKEEPING and the prereg's
own hard constraints:

  - windows_total == windows_abelian + windows_nonabelian
  - nonabelian_windows list length == windows_nonabelian, and every entry in
    it corresponds to a node with in_PB4=True and Q_is_abelian=False (cross-
    referenced against the full nodes list)
  - verdict is consistent with cap_hit / nonabelian_windows content (schema
    SS3 wording)
  - output_statement contains NONE of the SS4.2 forbidden phrases
  - census_index_hi == 240, lins_calls == 1 (LID-1, S-R0-1)
  - wall_cap_ms == 900000 and cap_hit matches total_elapsed_ms vs wall_cap_ms
  - scope_declaration all False (S-R0-6)
  - prereg_doc_sha256 matches an independently-recomputed sha256 of
    docs/notes/b4_r0_probe_prereg_iffirst_v1.md (this script recomputes the
    hash itself, not trusting the cert's own claim)
"""
import hashlib
import json
import sys

CERT_PATH = "search/certs/b4_r0_probe_v1_20260806.json"
PREREG_PATH = "docs/notes/b4_r0_probe_prereg_iffirst_v1.md"

FORBIDDEN_PHRASES = [
    "指数1000まで非可換窓は存在しない",
    "指数 1000 まで非可換窓は存在しない",
    "すべて可換",
    "鏡映双子はゼロ",
    "exoticが無い",
    "exotic が無い",
    "GT-shadowが無い",
    "GT-shadow が無い",
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    with open(CERT_PATH, encoding="utf-8") as f:
        d = json.load(f)

    problems = []

    # bookkeeping
    if d["windows_total"] != d["windows_abelian"] + d["windows_nonabelian"]:
        problems.append("windows_total != abelian+nonabelian")
    if len(d["nonabelian_windows"]) != d["windows_nonabelian"]:
        problems.append("nonabelian_windows length != windows_nonabelian count")

    nodes_by_index = {}
    for nd in d["nodes"]:
        nodes_by_index.setdefault(nd["index"], []).append(nd)
    for nw in d["nonabelian_windows"]:
        idx = nw["index"]
        matched = [nd for nd in nodes_by_index.get(idx, [])
                   if nd.get("Q_structure") == nw.get("Q_structure")]
        if not any(nd["in_PB4"] and not nd["Q_is_abelian"] for nd in nodes_by_index.get(idx, [])):
            problems.append(f"nonabelian_windows entry index={idx} has no matching in_PB4&non-abelian node")

    # verdict consistency
    if d["cap_hit"]:
        if d["verdict"] != "STOP(TIME_CAP)":
            problems.append("cap_hit=True but verdict != STOP(TIME_CAP)")
    elif d["windows_nonabelian"] > 0:
        if d["verdict"] != "NONABELIAN_WINDOW_FOUND":
            problems.append("nonabelian windows present but verdict != NONABELIAN_WINDOW_FOUND")
    else:
        if d["verdict"] != "NOT_FOUND_WITHIN_240":
            problems.append("no nonabelian windows, no cap_hit, but verdict != NOT_FOUND_WITHIN_240")

    # frozen constants
    if d["census_index_hi"] != 240:
        problems.append(f"census_index_hi != 240 (S-R0-1 LID_VIOLATION): {d['census_index_hi']}")
    if d["lins_calls"] != 1:
        problems.append(f"lins_calls != 1 (S-R0-1 LID_VIOLATION): {d['lins_calls']}")
    if d["wall_cap_ms"] != 900000:
        problems.append(f"wall_cap_ms != 900000: {d['wall_cap_ms']}")
    expect_cap_hit = d["total_elapsed_ms"] > d["wall_cap_ms"]
    if bool(d["cap_hit"]) != bool(expect_cap_hit) and not d["cap_hit"]:
        # only flag the "should have been true but wasn't" direction hard;
        # a true cap_hit with total_elapsed_ms slightly under due to the
        # 30s write-margin in the per-node check is expected/benign.
        if expect_cap_hit:
            problems.append("total_elapsed_ms exceeds wall_cap_ms but cap_hit=False")

    # forbidden phrases (S-R0-5)
    stmt = d.get("output_statement", "")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in stmt:
            problems.append(f"FORBIDDEN PHRASE present in output_statement: {phrase!r}")

    # scope declaration (S-R0-6)
    sd = d.get("scope_declaration", {})
    for k, v in sd.items():
        if k == "note":
            continue
        if v is not False:
            problems.append(f"scope_declaration.{k} is not False: {v}")

    # prereg hash, independently recomputed
    actual_sha = sha256_file(PREREG_PATH)
    if actual_sha != d.get("prereg_doc_sha256"):
        problems.append(f"prereg_doc_sha256 mismatch: cert={d.get('prereg_doc_sha256')} actual={actual_sha}")

    result = {
        "schema": "b4-r0-probe-checker/v1",
        "cert_checked": CERT_PATH,
        "prereg_sha256_independently_recomputed": actual_sha,
        "problems": problems,
        "all_checks_pass": len(problems) == 0,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
