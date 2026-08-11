#!/usr/bin/env python3
"""
search/u9bit_extract_v1.py -- U9-BIT-EXTRACT (裁定857/859, docs/notes/u9bit_spec_v1.md §4).

Task (verbatim from the spec, §4 発注 U9-BIT-EXTRACT):
  "registry / ihnec 戦役の cert から次を抽出せよ:
   1. L_9 の定義データ: 定義多項式・判別式・分岐素点、または u_9 の値(Aff(Z/9)部の Kummer
      生成元)と二次捻り d。
   2. L_{S4} の同上(u_{S4} と F_0≅C_9 の生成データ)。
   3. どちらも無ければ即報告(= 本仕様の前件不成立 ⟹「算術側の同定が未了」を §10 の表の
      空欄として確定)。
   ★ これが本仕様の唯一の実質的リスク: 群論側は全て既測だが、算術体の同定が cert にある
   か未確認。"

This script is a SEARCH RECORD of the extraction attempt (not a computation on found data --
there is no computation to perform here, since the required inputs do not exist). It documents
EVERY location searched and the negative result, per this project's discipline against silently
treating "not found" as an assumption rather than a first-class, explicitly reported result.

METHOD: grep/search across docs/notes/*.md (all ihnec-campaign and ENT-related design docs),
search/certs/*.json (all committed certs), and provenance/LEDGER.md, for:
  - u_9, u_{S4} (the Kummer generator symbols themselves)
  - defining polynomial / discriminant / ramified-prime language for L_9 or L_{S4}
  - PARI/GAP number-theory computation markers (polcyclo, nfinit, nfispower, polcompositum)
    in a context tied to K^(9) or N_{S4}

RESULT (raw, no verdict language): u_9 and u_{S4}'s actual arithmetic values (as elements of
Q^*/((Q^*)^9), or equivalently L_9/L_{S4}'s defining polynomials/discriminants) are NOT found
in any committed artifact. What IS found: (a) the ABSTRACT GROUP isomorphism type
Theta_9 = Aff(Z/9) x C2 = GT(K^(9)) (theorem U-11, docs/notes/ihnec_v1.md §C.3, "有限
exhaustive candidate / single lane" per F98-3.8 -- group-theoretic, not the number-field
realization); (b) TWO explicit verbatim statements that u_{S4}'s value has NOT been computed
(docs/notes/surj_s4_v1.md line 16/328, docs/notes/surj_s4_v2.md line 20/268: "u_{S4} の値には
触れていない" / "u_{S4}の値には触れない"); (c) docs/notes/ideas_ent_targets_v1.md line 46's own
disclosure "u_9 実測状態は registry 確認要" (u_9's measurement status requires registry
confirmation -- i.e. not yet confirmed measured at the time that note was written).

No verdict language beyond the raw found/not-found status of each searched item.
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SEARCH_PATTERNS = {
    "u_9_symbol": r"u_9\b",
    "u_S4_symbol": r"u_\{?S4\}?\b|u_\{?\\text\{S4\}\}?",
    "defining_polynomial_ja": r"定義多項式",
    "discriminant_ja": r"判別式",
    "discriminant_en": r"\bdiscriminant\b",
    "ramified_primes_ja": r"分岐素点",
    "pari_polcyclo": r"polcyclo",
    "pari_nfinit": r"nfinit",
    "pari_nfispower": r"nfispower",
    "pari_polcompositum": r"polcompositum",
}

SEARCH_DIRS = [
    REPO_ROOT / "docs" / "notes",
    REPO_ROOT / "docs" / "scout",
    REPO_ROOT / "search" / "certs",
]
SEARCH_FILES = [
    REPO_ROOT / "provenance" / "LEDGER.md",
]


def search_files():
    hits = {key: [] for key in SEARCH_PATTERNS}
    files_scanned = 0
    compiled = {k: re.compile(v) for k, v in SEARCH_PATTERNS.items()}

    all_files = list(SEARCH_FILES)
    for d in SEARCH_DIRS:
        if d.exists():
            all_files.extend(d.rglob("*.md"))
            if d.name == "certs":
                all_files.extend(d.rglob("*.json"))

    seen = set()
    for f in all_files:
        if f in seen or not f.is_file():
            continue
        seen.add(f)
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        files_scanned += 1
        rel = str(f.relative_to(REPO_ROOT)).replace("\\", "/")
        for key, pat in compiled.items():
            matches = list(pat.finditer(text))
            if matches:
                # record line numbers of first few matches (context, not full dump)
                lines_hit = []
                for m in matches[:5]:
                    line_no = text.count("\n", 0, m.start()) + 1
                    lines_hit.append(line_no)
                hits[key].append({"file": rel, "match_count": len(matches), "sample_lines": lines_hit})

    return hits, files_scanned


def main():
    hits, files_scanned = search_files()

    # u_9 and u_S4's ACTUAL VALUE was searched for specifically (not just the symbol appearing
    # in a definitional/planning context) -- disclosed distinction: the symbol MATCHES found
    # above (u_9_symbol, u_S4_symbol) include definitional/planning mentions (e.g. "u_9 の定義",
    # "u_{S4} の測定計画"), NOT necessarily an actual computed rational number. This script does
    # NOT attempt automated semantic classification of "is this hit an actual VALUE vs a
    # DEFINITION/PLAN mention" -- that requires human/mathematician reading (already done by the
    # implementer manually before writing this script; see the module docstring's "RESULT"
    # section for that manual reading's conclusion, reported as prose, not re-derived here).
    u9_files = [h["file"] for h in hits["u_9_symbol"]]
    uS4_files = [h["file"] for h in hits["u_S4_symbol"]]

    extraction_succeeded = False  # per the manual reading documented in this module's docstring

    out = {
        "schema": "shadow-atelier/u9bit_extract_v1",
        "authority": "裁定857/859 -- docs/notes/u9bit_spec_v1.md §4 発注 U9-BIT-EXTRACT",
        "method_note": "grep-style scan of docs/notes/*.md, docs/scout/*.md, search/certs/*.json, "
                       "and provenance/LEDGER.md for u_9/u_S4 symbol mentions and defining-"
                       "polynomial/discriminant/ramified-prime/PARI-number-theory markers tied "
                       "to K^(9)/N_S4. Raw hit locations recorded below; SEMANTIC classification "
                       "(does a hit represent an actual computed VALUE vs a definitional/planning "
                       "mention) was done by manual reading (implementer), reported as prose in "
                       "this module's own docstring, NOT automated here.",
        "files_scanned": files_scanned,
        "search_patterns": list(SEARCH_PATTERNS.keys()),
        "raw_hits": hits,
        "u9_symbol_hit_files": u9_files,
        "uS4_symbol_hit_files": uS4_files,
        "manual_reading_findings": [
            {
                "finding": "theorem U-11 establishes ONLY the abstract group isomorphism type "
                           "Theta_9=Aff(Z/9)xC2=GT(K^(9))=[108,26], via exhaustive GAP search on "
                           "generating-pair data -- NOT a number-field realization (no defining "
                           "polynomial, discriminant, or Kummer generator value).",
                "source": "docs/notes/ihnec_v1.md §C.3 (lines 726-964), status recorded there as "
                          "'有限exhaustive candidate/single lane' per F98-3.8 -- explicitly NOT "
                          "upgraded to cross-checked/verified, and explicitly scoped as "
                          "group-theoretic ('同型型'), not arithmetic.",
            },
            {
                "finding": "u_{S4}'s value is explicitly stated (verbatim, twice, in two "
                           "document versions) to have NOT been computed -- only a measurement "
                           "PLAN exists.",
                "source": "docs/notes/surj_s4_v1.md line 16 ('u_{S4}の値には触れていない...§5は "
                          "測定計画まで') and line 328; docs/notes/surj_s4_v2.md line 20 and 268 "
                          "(near-identical statement).",
            },
            {
                "finding": "u_9's own measurement status is explicitly flagged as unconfirmed "
                           "in the note that proposed this experiment.",
                "source": "docs/notes/ideas_ent_targets_v1.md line 46: "
                          "'u_9 実測状態は registry 確認要' (u_9 measurement status requires "
                          "registry confirmation).",
            },
            {
                "finding": "provenance/LEDGER.md contains ZERO mentions of u_9 or u_S4 "
                           "(searched directly, 0 hits) -- no ruling/session record of either "
                           "value having been computed or reported.",
                "source": "provenance/LEDGER.md (direct grep, this session).",
            },
            {
                "finding": "★ DECISIVE: an entire dedicated planning document for computing "
                           "u_9 exists (docs/notes/u9_extraction_plan_v1.md, 2026-07-28, "
                           "'u_9 抽出の実行計画書 v1 -- 計画のみ・測定なし' = 'execution plan "
                           "ONLY, no measurement'), whose OWN explicit self-constraint (line 8) "
                           "states 'u_9 の値を計算・推定・示唆しない' (does NOT compute/"
                           "estimate/suggest u_9's value). That plan identifies 7 OPEN "
                           "prerequisites (C1,C3,C4,C6,C7,C8,C9 in its §4 checklist) that must "
                           "close BEFORE measurement can even begin, and flags a STRUCTURAL "
                           "risk as the actual rate-limiting step (§5-A): the existing K^(5)-"
                           "style extraction machinery (path A/B, the M-A normal-form pipeline) "
                           "is genus-2-hyperelliptic-specific, and n=9's dessin (degree 18) is "
                           "NOT expected to be genus 2 ('種数2に留まる見込みは薄い') -- meaning "
                           "path B likely does not transfer at all and would need a full "
                           "redesign. u_5 (the n=5 precedent this plan was modeled on) is ALSO "
                           "confirmed unextracted in the same document (§0: 'u_5 はまだ抽出さ"
                           "れていない'). Only u_3 (K^(3)) has an actual extracted value in "
                           "this project (search/week4-u-k3.mjs, u=-4) -- a DIFFERENT window, "
                           "not K^(9) or N_S4.",
                "source": "docs/notes/u9_extraction_plan_v1.md (full document read).",
            },
        ],
        "extraction_succeeded": extraction_succeeded,
        "u9bit_calc_prerequisite_met": extraction_succeeded,
        "no_verdict_note": "raw file-search hits and the manual-reading finding summaries only. "
                           "No judgment on WHAT THIS MEANS for §10's table (that is the "
                           "commander's/mathematician's determination) -- only that the §4 "
                           "extraction task's prerequisite data was not found.",
    }
    out_path = "search/certs/u9bit_extract_v1_20260812.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"files_scanned={files_scanned}")
    print(f"extraction_succeeded={extraction_succeeded}")
    print(f"u9bit_calc_prerequisite_met={extraction_succeeded}")


if __name__ == "__main__":
    main()
