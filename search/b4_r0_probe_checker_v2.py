#!/usr/bin/env python3
"""
b4_r0_probe_checker_v2.py -- independent (GAP-free) consistency checker for
search/certs/b4_r0_probe_v2_p2fix_20260806.json (裁定673 repair run; prior
cert search/certs/b4_r0_probe_v2_20260806.json is checked only by this
script's history -- see git log for the version that pointed at it), per
docs/notes/b4_r0_probe_prereg_iffirst_v2.md.

Per the prereg's own 【R0v2-GAP-1】, R0 v2 is single-system by design (GAP
only); a second group-theory system is triggered ONLY if a non-abelian
window is found, as a separate follow-up task. This script therefore does
NOT recompute any group theory (no SmallGroups reconstruction, no
GQuotients). What it DOES independently re-verify, without importing the
GAP driver or trusting the cert's self-report, is:

  - prereg_doc_sha256 matches an independently-recomputed sha256 of
    docs/notes/b4_r0_probe_prereg_iffirst_v2.md (S-R0-1'..9' anchor)
  - prereg_erratum_sha256 matches an independently-recomputed sha256 of
    docs/notes/b4_r0_probe_prereg_iffirst_v2_1_erratum.md (v2.1 erratum:
    v2's body is byte-for-byte unchanged; the erratum corrects ONE frozen
    constant v2 got wrong -- nr_small_groups_192 10494 -> 1543, a
    digit-swap misremembering of the order-512 group count. S-R0-1'
    threshold only; nothing else in driver behavior changes)
  - driver_self_sha256 matches an independently-recomputed sha256 of
    search/probe/b4_r0_probe_v2/r0_probe_v2_driver.g
  - nr_small_groups_192 == 1543 (S-R0-1', corrected per v2.1 erratum)
  - sanity.index_B4_PB4 == 24 (S-R0-2')
  - stage_caps_ms == {P1:600000, P2:600000, P3:1200000} and
    wall_cap_ms == 2400000 (frozen constants)
  - p1_passed_count == len(p1_passed); p2_passed_count == len(p2_passed)
  - every p2_passed id appears in p1_passed (P2 only runs on P1 survivors)
  - windows_count == len(nonabelian_windows)
  - every nonabelian_windows entry has Q_order==8 and Q_is_abelian==False,
    and its smallgroup_id appears in p2_passed (P4 only fires on P3 which
    only runs on P2 survivors)
  - filter_soundness_spotcheck: p1_rejected_sampled / p2_rejected_sampled
    each have min(20, actual rejected-pool size) entries -- NOT a hard 20,
    since the P2-rejected pool can genuinely be smaller than 20 when P1
    passes few groups (this run: pool size 8, corrected from the prior
    checker's naive hard-20 assertion, itself a false-positive discovered
    in the run-3 report). all_clear is True iff no sampled entry has
    window_found=True, and no sampled id overlaps p1_passed / p2_passed
    respectively (S-R0-7' input integrity)
  - verdict is consistent with cap_hit / windows_count / spotcheck all_clear
    per the prereg SS6 table (S-R0-4', S-R0-7', S-R0-8')
  - output contains none of the SS5.2 forbidden phrases
  - scope_declaration all False (S-R0-6')
  - untested_ids non-empty only for stages where cap_hit is True (PARTIAL
    discipline, S-R0-8': never NOT_FOUND when a stage was capped)
  - REPAIR-ITEM-B invariant (裁定673): every p1_passed id has EXACTLY ONE
    disposition -- present in p2_passed XOR p2_rejected XOR untested_ids.P2
    (no silent drops). p2_rejected_count == len(p2_rejected).
    p2_disposition_complete's own self-report is independently
    recomputed and compared, not merely echoed.
"""
import hashlib
import json
import sys

CERT_PATH = "search/certs/b4_r0_probe_v2_p2fix_20260806.json"
PREREG_PATH = "docs/notes/b4_r0_probe_prereg_iffirst_v2.md"
ERRATUM_PATH = "docs/notes/b4_r0_probe_prereg_iffirst_v2_1_erratum.md"
DRIVER_PATH = "search/probe/b4_r0_probe_v2/r0_probe_v2_driver.g"

FORBIDDEN_PHRASES = [
    "指数1000まで非可換窓は存在しない",
    "指数 1000 まで非可換窓は存在しない",
    "[PB_4:\\widetilde N]\\le41",
    "41 の窓はすべて可換",
    "鏡映双子はゼロ",
    "ι-固定である",
    "GT-shadow",
    "settled",
    "isolated",
    "genuine",
    "指数 192 の正規部分群を悉皆列挙した",
    "正規部分群を悉皆列挙した",
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

    # --- STOP-shaped certs (P0/library-guard failures) short-circuit most
    # downstream checks; handle them narrowly and return early.
    verdict = d.get("verdict", "")
    if verdict.startswith("STOP("):
        # only the sanity/library fields and grade/forbidden-phrase checks apply
        if "sanity" in d and d["sanity"].get("index_B4_PB4") == 24 and "PRESENTATION_BROKEN" in verdict:
            problems.append("verdict=STOP(PRESENTATION_BROKEN) but sanity.index_B4_PB4==24 (should have passed P0)")
        actual_sha = sha256_file(PREREG_PATH)
        actual_erratum_sha = sha256_file(ERRATUM_PATH)
        result = {
            "schema": "b4-r0-probe-checker/v2",
            "cert_checked": CERT_PATH,
            "prereg_sha256_independently_recomputed": actual_sha,
            "prereg_erratum_sha256_independently_recomputed": actual_erratum_sha,
            "note": "cert is a STOP-shaped early exit; only minimal checks applied",
            "problems": problems,
            "all_checks_pass": len(problems) == 0,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1 if problems else 0)

    # --- hashes, independently recomputed ---
    actual_prereg_sha = sha256_file(PREREG_PATH)
    if actual_prereg_sha != d.get("prereg_doc_sha256"):
        problems.append(
            f"prereg_doc_sha256 mismatch: cert={d.get('prereg_doc_sha256')} actual={actual_prereg_sha}"
        )
    actual_erratum_sha = sha256_file(ERRATUM_PATH)
    if actual_erratum_sha != d.get("prereg_erratum_sha256"):
        problems.append(
            f"prereg_erratum_sha256 mismatch: cert={d.get('prereg_erratum_sha256')} actual={actual_erratum_sha}"
        )
    actual_driver_sha = sha256_file(DRIVER_PATH)
    if actual_driver_sha != d.get("driver_self_sha256"):
        problems.append(
            f"driver_self_sha256 mismatch: cert={d.get('driver_self_sha256')} actual={actual_driver_sha}"
        )

    # --- frozen constants (S-R0-1', corrected 10494 -> 1543 per v2.1 erratum) ---
    if d.get("nr_small_groups_192") != 1543:
        problems.append(f"nr_small_groups_192 != 1543 (S-R0-1' LIBRARY_MISMATCH, v2.1 erratum value): {d.get('nr_small_groups_192')}")

    # --- P0 sanity (S-R0-2') ---
    if d.get("sanity", {}).get("index_B4_PB4") != 24:
        problems.append(f"sanity.index_B4_PB4 != 24 (S-R0-2' PRESENTATION_BROKEN): {d.get('sanity')}")

    # --- caps (frozen SS3.5) ---
    if d.get("wall_cap_ms") != 2400000:
        problems.append(f"wall_cap_ms != 2400000: {d.get('wall_cap_ms')}")
    sc = d.get("stage_caps_ms", {})
    if sc.get("P1") != 600000 or sc.get("P2") != 600000 or sc.get("P3") != 1200000:
        problems.append(f"stage_caps_ms mismatch (expect P1:600000,P2:600000,P3:1200000): {sc}")

    # --- bookkeeping ---
    p1_passed = d.get("p1_passed", [])
    p2_passed = d.get("p2_passed", [])
    p2_rejected = d.get("p2_rejected", [])
    if d.get("p1_passed_count") != len(p1_passed):
        problems.append("p1_passed_count != len(p1_passed)")
    if d.get("p2_passed_count") != len(p2_passed):
        problems.append("p2_passed_count != len(p2_passed)")
    if d.get("p2_rejected_count") != len(p2_rejected):
        problems.append("p2_rejected_count != len(p2_rejected)")

    p1_ids = {r["id"] for r in p1_passed}
    p2_ids = {r["id"] for r in p2_passed}
    p2_rejected_ids = {r["id"] for r in p2_rejected}
    for r in p2_passed:
        if r["id"] not in p1_ids:
            problems.append(f"p2_passed id={r['id']} not in p1_passed (P2 must only run on P1 survivors)")
    for r in p2_rejected:
        if r["id"] not in p1_ids:
            problems.append(f"p2_rejected id={r['id']} not in p1_passed (P2 must only run on P1 survivors)")
        if not r.get("reason"):
            problems.append(f"p2_rejected id={r['id']} has no reason code")

    # --- REPAIR-ITEM-B (裁定673): every P1-survivor gets EXACTLY ONE
    # disposition (p2_passed XOR p2_rejected XOR untested.P2) -- no silent
    # drops. Independently recomputed (not just echoing p2_disposition_complete).
    p2_untested_ids = set(d.get("untested_ids", {}).get("P2", []))
    overlap_passed_rejected = p2_ids & p2_rejected_ids
    if overlap_passed_rejected:
        problems.append(f"ids in BOTH p2_passed and p2_rejected: {sorted(overlap_passed_rejected)}")
    overlap_passed_untested = p2_ids & p2_untested_ids
    if overlap_passed_untested:
        problems.append(f"ids in BOTH p2_passed and untested_ids.P2: {sorted(overlap_passed_untested)}")
    overlap_rejected_untested = p2_rejected_ids & p2_untested_ids
    if overlap_rejected_untested:
        problems.append(f"ids in BOTH p2_rejected and untested_ids.P2: {sorted(overlap_rejected_untested)}")
    covered = p2_ids | p2_rejected_ids | p2_untested_ids
    missing = p1_ids - covered
    if missing:
        problems.append(f"REPAIR-ITEM-B violation: p1_passed ids with NO disposition (silent drop): {sorted(missing)}")
    expected_disposition_complete = (len(p2_ids) + len(p2_rejected_ids) + len(p2_untested_ids) == len(p1_ids)) and not missing
    if bool(d.get("p2_disposition_complete")) != expected_disposition_complete:
        problems.append(
            f"p2_disposition_complete self-report ({d.get('p2_disposition_complete')}) != independently recomputed ({expected_disposition_complete})"
        )

    nonab = d.get("nonabelian_windows", [])
    if d.get("windows_count") != len(nonab):
        problems.append("windows_count != len(nonabelian_windows)")
    for w in nonab:
        if w.get("Q_order") != 8:
            problems.append(f"nonabelian_windows entry smallgroup_id={w.get('smallgroup_id')} has Q_order != 8: {w.get('Q_order')}")
        if w.get("Q_is_abelian") is not False:
            problems.append(f"nonabelian_windows entry smallgroup_id={w.get('smallgroup_id')} has Q_is_abelian != False")
        if w.get("smallgroup_id") not in p2_ids:
            problems.append(f"nonabelian_windows entry smallgroup_id={w.get('smallgroup_id')} not in p2_passed")

    # --- filter soundness spot-check (S-R0-7' input) ---
    # Sample sizes are min(20, actual rejected-pool size), NOT a hard 20 --
    # a hard-20 assertion is a checker bug when the pool itself is smaller
    # than 20 (this run: P2-rejected pool = p1_passed(12) - p2_passed(4) -
    # untested(0) = 8, discovered as a false positive in the run-3 report
    # and fixed here per 司令塔 instruction).
    spot = d.get("filter_soundness_spotcheck", {})
    p1_sample = spot.get("p1_rejected_sampled", [])
    p2_sample = spot.get("p2_rejected_sampled", [])
    # P1-rejected pool size: total tested in P1 (nr_small_groups_192, or up
    # to the P1 cap boundary) minus p1_passed.
    p1_untested = d.get("untested_ids", {}).get("P1", [])
    p1_tested_total = d.get("nr_small_groups_192", 0) - len(p1_untested)
    expected_p1_sample_len = min(20, max(0, p1_tested_total - len(p1_ids)))
    if len(p1_sample) != expected_p1_sample_len:
        problems.append(
            f"filter_soundness_spotcheck.p1_rejected_sampled length {len(p1_sample)} != expected min(20,pool)={expected_p1_sample_len}"
        )
    expected_p2_sample_len = min(20, len(p2_rejected_ids))
    if len(p2_sample) != expected_p2_sample_len:
        problems.append(
            f"filter_soundness_spotcheck.p2_rejected_sampled length {len(p2_sample)} != expected min(20,pool)={expected_p2_sample_len}"
        )
    for s in p1_sample:
        if s["id"] in p1_ids:
            problems.append(f"filter_soundness_spotcheck p1 sample id={s['id']} is actually in p1_passed (sampling pool contamination)")
    for s in p2_sample:
        if s["id"] in p2_ids:
            problems.append(f"filter_soundness_spotcheck p2 sample id={s['id']} is actually in p2_passed (sampling pool contamination)")
    spot_all_clear_expected = all(not s.get("window_found") for s in p1_sample) and \
        all(not s.get("window_found") for s in p2_sample)
    if bool(spot.get("all_clear")) != spot_all_clear_expected:
        problems.append("filter_soundness_spotcheck.all_clear inconsistent with sampled window_found values")
    if not spot_all_clear_expected:
        problems.append("FILTER_UNSOUND: a spot-checked rejected group produced a window (S-R0-7')")

    # --- cap_hit / untested_ids / verdict consistency (SS6 table) ---
    cap_hit = d.get("cap_hit", {})
    untested = d.get("untested_ids", {})
    any_cap_hit = any(cap_hit.get(k) for k in ("P1", "P2", "P3"))
    for stage in ("P1", "P2", "P3"):
        hit = cap_hit.get(stage)
        ids = untested.get(stage, [])
        if hit and len(ids) == 0:
            problems.append(f"cap_hit.{stage}=True but untested_ids.{stage} is empty")
        if not hit and len(ids) != 0:
            problems.append(f"cap_hit.{stage}=False but untested_ids.{stage} is non-empty")

    filter_unsound = not spot_all_clear_expected
    if filter_unsound:
        expect_verdict = "STOP(FILTER_UNSOUND)"
    elif any_cap_hit:
        expect_verdict = "UNKNOWN(partial)"
    elif len(nonab) > 0:
        expect_verdict = "NONABELIAN_WINDOW_FOUND"
    else:
        expect_verdict = "NOT_FOUND_AT_192"
    if verdict != expect_verdict:
        problems.append(f"verdict={verdict!r} but expected {expect_verdict!r} per SS6 table")
    if any_cap_hit and verdict == "NOT_FOUND_AT_192":
        problems.append("S-R0-8' violation: a stage was capped but verdict claims NOT_FOUND_AT_192")

    # --- forbidden phrases (S-R0-5') ---
    blob = json.dumps(d, ensure_ascii=False)
    for phrase in FORBIDDEN_PHRASES:
        if phrase in blob:
            problems.append(f"FORBIDDEN PHRASE present in cert: {phrase!r}")

    # --- scope declaration (S-R0-6') ---
    sd = d.get("scope_declaration", {})
    for k, v in sd.items():
        if v is not False:
            problems.append(f"scope_declaration.{k} is not False: {v}")

    result = {
        "schema": "b4-r0-probe-checker/v2",
        "cert_checked": CERT_PATH,
        "prereg_sha256_independently_recomputed": actual_prereg_sha,
        "prereg_erratum_sha256_independently_recomputed": actual_erratum_sha,
        "driver_sha256_independently_recomputed": actual_driver_sha,
        "problems": problems,
        "all_checks_pass": len(problems) == 0,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
