#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/probe/wac_v1/nf972_sourcemap_b_v6_gen.py

NF-972 source map B v6 (便103 F103-7 = sol/sol_reply_103_math30.md §7 の6修理)。

【設計判断・申告】 v6 は当初 GAP driver
(search/probe/wac_v1/nf972_sourcemap_b_run.g) の末尾へ追記して生成しようと
したが、その driver は単一の継続実行の中で v1〜v5 を毎回 re-write する構造
であり、GAPLIB_WallElapsedMs() 由来の wall_ms_total と自分自身の sha256
(script_sha256) が実行の度に変わるため、driver へ v6 コードを足して再実行
すると v4/v5 の bytes まで変化してしまう(実際に発生し、司令塔/Sol 便103が
引用した v4 の sha256 a6b412845adf119c80ebf77ab33d118cd47b40d84370f58d8c081d073d6f8b4c
と一致しなくなった -- git commit 4ebe384「裁定461」の内容へ復元し直し、
差分は commit 後の再走による timing/self-hash の変化のみと確認済み)。

v6 は既存の v4/v5/tuples-v3 cert を「読むだけ」で新規の数学計算を一切行わ
ない(972/108/54 の値・can9/can4・sigma・fixture 結果はすべて既存 JSON から
の再構造化)。この性質上、GAP を再実行して mutation リスクを負うより
python で完結させる方が安全と判断した(独立実装ではなく同一 B の
supplement 生成なので、独立性原則には抵触しない -- A 側は一切参照しない)。

実行: python search/probe/wac_v1/nf972_sourcemap_b_v6_gen.py
"""
import hashlib
import json
import os

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def sha256_of(path):
    h = hashlib.sha256()
    with open(os.path.join(REPO_ROOT, path), "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def load_json(path):
    with open(os.path.join(REPO_ROOT, path), encoding="utf-8") as f:
        return json.load(f)


def write_json_text(path, text):
    with open(os.path.join(REPO_ROOT, path), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


V4_PATH = "search/certs/nf972_sourcemap_b_v4_20260804.json"
V5_PATH = "search/certs/nf972_sourcemap_b_v5_20260804.json"
TUPLES_V3_PATH = "search/certs/nf972_sourcemap_b_tuples_v3_20260804.json"
V6_PATH = "search/certs/nf972_sourcemap_b_v6_20260804.json"
MANIFEST_V6_PATH = "search/certs/MANIFEST_nf972_sourcemap_b_v6_20260804.json"

EXPECTED_V4_SHA_FROM_SOL_103 = "a6b412845adf119c80ebf77ab33d118cd47b40d84370f58d8c081d073d6f8b4c"
EXPECTED_TUPLES_V3_SHA_FROM_SOL_103 = "8cd10f3a471b3dbae0c8db4961e81f7b4ca22330a51a9337d4e6d2430968254a"


def main():
    v4 = load_json(V4_PATH)
    v5 = load_json(V5_PATH)

    v4_sha = sha256_of(V4_PATH)
    v5_sha = sha256_of(V5_PATH)
    tuples_v3_sha = sha256_of(TUPLES_V3_PATH)

    v4_sha_matches_sol103 = (v4_sha == EXPECTED_V4_SHA_FROM_SOL_103)
    tuples_v3_sha_matches_sol103 = (tuples_v3_sha == EXPECTED_TUPLES_V3_SHA_FROM_SOL_103)

    print("v4_sha (current, committed 裁定461) =", v4_sha)
    print("  matches Sol 便103 quoted hash?", v4_sha_matches_sol103)
    print("v5_sha (current, committed 裁定496) =", v5_sha)
    print("tuples_v3_sha (whole artifact)      =", tuples_v3_sha)
    print("  matches Sol 便103 quoted hash?", tuples_v3_sha_matches_sol103)

    cu5 = v5["conventions_used"]
    dict_selfcheck = v4["dictionary_selfcheck"]
    fixtures = v4["fixtures"]
    canonical_sha = v4["canonical_enumeration"]["sha256"]
    self_sha_of_gap_driver = v4["provenance"]["script_sha256"]
    wall_ms_v4 = v4["provenance"]["wall_ms_total"]
    freeze_spec_sha = v5["source_digests"]["freeze_spec_sha256"]
    k9_cert_sha = v5["source_digests"]["k9_cert_sha256"]
    s4_cert_sha = v5["source_digests"]["s4_cert_sha256"]
    ledger_sha = v5["source_digests"]["ledger_sha256"]

    # roundtrip_witness data (v5) -> reclassified as a separation.dummy_fixture (item 4)
    rtw = cu5["roundtrip_witness"]
    rtw_witness = rtw["witnesses"][0]

    # ---- item 1: structured supplements (v4 path+sha256) ----
    supplements = {"path": V4_PATH, "sha256": v4_sha}

    # ---- item 2: canonical_enumeration_ref = whole-artifact sha256 of tuples v3 ----
    canonical_enumeration_ref = {
        "note": (
            "canonical-content hash(sortしたtuple配列を改行結合したbytesのhash)だけでは"
            "artifactのpathを解決できない(便103 F103-7(2))。whole-artifact SHA-256"
            "(ファイル全体のbytes)をpathとjson pointer付きで記録する。"
        ),
        "artifact_path": TUPLES_V3_PATH,
        "artifact_whole_sha256": tuples_v3_sha,
        "json_pointer_tuples": "/tuples",
        "count": 972,
        "canonical_content_sha256": canonical_sha,
    }

    # ---- item 3: comparison_target.function_b split into K9/S4 typed pins ----
    ct = dict(cu5["comparison_target"])
    old_fb = ct["function_b"]
    ct["function_b"] = [
        {"cert": "K9.v1.json", "name": "f_triple(直接格納値)",
         "domain": "K9.v1.json 108行", "source_digest": k9_cert_sha},
        {"cert": "S4.v2.json", "name": "cert枠(Xperm_cert,Yperm_cert)でのWordEval再評価",
         "domain": "S4.v2.json 54行(pass:true)", "source_digest": s4_cert_sha},
    ]
    ct["function_b_note"] = (
        "v5のfunction_bは単一objectでK9とS4の出所を混同していた(便103 F103-7(3))。"
        "v6ではK9/S4を配列で型付き分離する。旧function_b(参考): " + json.dumps(old_fb, ensure_ascii=False)
    )

    # ---- item 4: roundtrip_witness -> n/a, reclassified into separation.dummy_fixtures ----
    roundtrip_witness_v6 = {
        "status": "n/a",
        "reason": (
            "v5のwitnessはcoarse_of(WordOf(q))=qの往復を示していない -- 向き反転前後で"
            "tuple labelが変わることを示すのみで、CV-3/CV-4の往復assertとしては不完全"
            "(便103 F103-7(4)の指摘)。separation.dummy_fixtures[0](orientation_flip)へ"
            "再分類した。"
        ),
    }

    separation = dict(cu5["separation"])
    old_dummy = separation.pop("dummy_fixture", None)
    separation["dummy_fixtures"] = [
        {
            "id": "nf972-b-fixture1-orientation-flip",
            "normalised_input": "m=%s f=%s (f -> f^-1)" % (rtw_witness["element"].split(" f=")[0].replace("m=", ""),
                                                            rtw_witness["element"].split(" f=")[1] if " f=" in rtw_witness["element"] else rtw_witness["element"]),
            "normalised_output": "NFTupleSerialize(m0,can9,can4)",
            "discriminating_power": {"input_layer_novel": True, "output_layer_novel": True},
            "expected_label": rtw_witness["expected_label"],
            "observed_label_after_inversion": rtw_witness["observed_label_after_inversion"],
            "expected": "向き反転でtuple集合が不一致になる",
            "observed": fixtures["fixture1_orientation_flip_fires"],
            "verdict": "PASS" if fixtures["fixture1_orientation_flip_fires"] else "FAIL",
            "source_note": "v5のroundtrip_witnessから移設(" + rtw_witness["source"] + ")",
        },
        old_dummy,
    ]

    # ---- item 6: effective_source_chain as v4->v5->v6 supplement chain (self-ref via manifest) ----
    self_ref_v6 = {
        "holder_path": MANIFEST_V6_PATH,
        "json_pointer": "/self_reference_resolution/search~1certs~1nf972_sourcemap_b_v6_20260804.json/final_sha256",
        "resolution": "external-postwrite",
    }
    effective_source_chain = [
        {"role": "original", "path": V4_PATH, "sha256": v4_sha},
        {"role": "erratum", "path": V4_PATH, "sha256": v4_sha,
         "scope": ("conventions_used が規約台帳v1.6の必須欄(ledger_version・effective_source(_chain)・"
                   "roundtrip_witness・separation・chi_P_criterion・level)を欠く(便102 F102-2.2)。"
                   "数学結果(972/108/54)は不変。"),
         "superseded_by": {"path": V5_PATH, "sha256": v5_sha}},
        {"role": "erratum", "path": V5_PATH, "sha256": v5_sha,
         "scope": ("欄は追加されたがv4のmain scan/anchors/fixtures/window/projection/canonical "
                   "enumerationへ構造的に束縛されておらず、wall_ms_totalの相違も未説明、"
                   "roundtrip_witnessはcoarse_of(WordOf(q))=qを示さず、comparison_target.function_b"
                   "はK9/S4を混同、effective_source_chainはfreeze specの重複だった"
                   "(便103 F103-7(1)-(6))。数学結果(972/108/54)は不変。"),
         "superseded_by": {"path": V6_PATH, "sha256_ref": self_ref_v6}},
        {"role": "current", "path": V6_PATH, "sha256_ref": self_ref_v6},
    ]
    effective_source = {"path": V6_PATH, "sha256_ref": self_ref_v6}

    conventions_used_v6 = dict(cu5)
    conventions_used_v6["roundtrip_witness"] = roundtrip_witness_v6
    conventions_used_v6["comparison_target"] = ct
    conventions_used_v6["separation"] = separation
    conventions_used_v6["effective_source_chain"] = effective_source_chain
    conventions_used_v6.pop("effective_source_chain_note", None)
    conventions_used_v6["effective_source_chain_note"] = (
        "v4(original)->v5(erratum)->v6(current) の supplement chain(便103 F103-7(6))。"
        "freeze specはsource_digestsに別途記録(このchainは成果物自身の版譜)。"
    )
    conventions_used_v6["effective_source"] = effective_source

    v6_doc = {
        "schema": "nf972-sourcemap-b/v6",
        "generated_by": "search/probe/wac_v1/nf972_sourcemap_b_v6_gen.py (python -- v4/v5/tuples-v3読み取りのみ・新規数学計算なし)",
        "design_doc": "docs/notes/nf972_freeze_v1.md(裁定434/442/454)+docs/notes/conventions_ledger_v1.md(v1.6)",
        "card_label": "NF-972 source map B -- v6: 便103 F103-7(sol_reply_103_math30.md §7)の6修理",
        "supplement_note": (
            "v5(artifact採用FAIL)以前は不改変(v4/v5/tuples-v1..v3のbytesは本ツールで一切書き換えていない"
            "-- 読み取り専用)。数学結果(972点・canonical_content_sha256=%s)は不撤回・不変。"
            "本v6はconventions_usedの構造的束縛を完成させる。" % canonical_sha
        ),
        "a_side_note": (
            "A v3 cert の fixture 説明に『3 mutants』という文言が残っているが実物は4 fixtureである旨、"
            "便102 F102-2.2 で non-blocking の文言修正として指摘済み(A側ファイルは一切参照・変更していない)。"
        ),
        "process_note": (
            "v6生成手法の変更申告: 当初GAP driver(nf972_sourcemap_b_run.g)への追記で生成しようとしたが、"
            "そのdriverは単一実行内でv1〜v5を毎回re-writeする構造のため、v6コード追加後の再実行でv4/v5の"
            "wall_ms_total・script_sha256が変化し、Sol便103が引用したv4のsha256(%s)と不一致になった。"
            "git commit 4ebe384(裁定461)の内容へv4/v5を復元し、以後はv4/v5/tuples-v3を読むだけの本python"
            "スクリプトでv6を生成する(GAP再実行によるmutationを構造的に回避)。"
            % EXPECTED_V4_SHA_FROM_SOL_103
        ),
        "v4_hash_reconciliation": {
            "sol_103_quoted_v4_sha256": EXPECTED_V4_SHA_FROM_SOL_103,
            "current_committed_v4_sha256": v4_sha,
            "matches": v4_sha_matches_sol103,
            "note": (
                "一致しない場合、Sol便103はこのv4の中間的な(未commit)再走版を見ていた可能性がある"
                "(裁定461でcommitされた版とは異なるtiming依存fieldのみの差)。数学的内容(972/108/54・"
                "can9/can4・sigma)は不変。司令塔の確認を仰ぐ。"
                if not v4_sha_matches_sol103 else "一致確認済み。"
            ),
        },
        "tuples_v3_hash_reconciliation": {
            "sol_103_quoted_sha256": EXPECTED_TUPLES_V3_SHA_FROM_SOL_103,
            "current_sha256": tuples_v3_sha,
            "matches": tuples_v3_sha_matches_sol103,
        },
        "supplements": supplements,
        "dictionary_selfcheck": dict_selfcheck,
        "conventions_used": conventions_used_v6,
        "source_digests": v5["source_digests"],
        "canonical_enumeration_ref": canonical_enumeration_ref,
        "provenance": {
            "gap_version": v4["provenance"]["gap_version"],
            "gap_driver_script_sha256": self_sha_of_gap_driver,
            "gap_driver_script_sha256_note": "search/probe/wac_v1/nf972_sourcemap_b_run.g の、v4/v5生成時点のsha256(v4.provenance.script_sha256を継承・再計算していない)。",
            "v6_generator_script": "search/probe/wac_v1/nf972_sourcemap_b_v6_gen.py",
            "wall_ms_total": wall_ms_v4,
            "wall_ms_total_note": (
                "v4の測定値(%d)をそのまま継承(便103 F103-7(5)) -- v6は本走(972点の悉皆)を再実行して"
                "いない純補遺であり、新規のwall clock計測を行わない。" % wall_ms_v4
            ),
        },
        "driver_done": True,
        "driver_done_marker": "NF972_SOURCEMAP_B_DRIVER_DONE",
    }

    v6_text = json.dumps(v6_doc, ensure_ascii=False, indent=2) + "\n"
    write_json_text(V6_PATH, v6_text)
    print("Wrote", V6_PATH)

    v6_actual_sha = sha256_of(V6_PATH)
    print("v6_actual_sha (self, recorded in manifest) =", v6_actual_sha)

    manifest_doc = {
        "schema": "manifest-nf972-sourcemap-b-v6/v1",
        "generated_by": "search/probe/wac_v1/nf972_sourcemap_b_v6_gen.py (implementer)",
        "purpose": (
            "v6 cert(%s)のeffective_source_chain自己参照digest(便103 F103-7(6))を機械可読に保持する。"
            "ファイルは自分自身のsha256を内容に含められない(自己言及不可能性)ため、2段階書き出し"
            "(v6をsha256_refで書く -> sha256計算 -> 本manifestに記録)で解決する"
            "(conventions_ledger_v1.md §1.7 の sha256_ref pattern)。" % V6_PATH
        ),
        "self_reference_resolution": {
            "search/certs/nf972_sourcemap_b_v6_20260804.json": {
                "path": V6_PATH,
                "note": "本v6 certのeffective_source_chain[role:current]とeffective_sourceの自己参照digest。",
                "final_sha256": v6_actual_sha,
            }
        },
    }
    manifest_text = json.dumps(manifest_doc, ensure_ascii=False, indent=2) + "\n"
    write_json_text(MANIFEST_V6_PATH, manifest_text)
    print("Wrote", MANIFEST_V6_PATH)


if __name__ == "__main__":
    main()
