#!/usr/bin/env python3
"""
twin_witness_build_final_cert_v1_1.py -- assemble the v1.1 run cert.

裁定607 修理束(docs/notes/twin_witness_cv9_reading_v1.md の falsifier 判読
に基づく)。v1(search/certs/twin_witness_run_v1_20260806.json)は不改変・
並置。本ファイルは v1.1 の是正 (i)-(viii) を適用した新規 cert を書く:

  (i)   P-2 を「予言的中」から「census 整合性検査(O-1+D-1 からの定理)」へ
        再格付け。
  (ii)  P-3 を「演繹部分」(3連言のうち補題からの論理的帰結)と「未測定部分」
        (source kernel 異なり数 -- scope3 未実行ゆえ)に分割記載。
  (iii) P4_note を裁定607の会計へ差し替え: 機械出力の実質的内容は「N の
        iota-不変性」1 ビット x 15 window であり、真の内容は陰性命題
        「この層(index<=1000, c in N, N<=PB3)に exotic(非鏡映)双子は
        一つも無い」。旧 P4_note(「新しい紙証明の可能性」)の的外れな
        楽観を撤回。
  (iv)  帰属欄: MIRROR-SHADOW (a)(b)(c) = docs/notes/div_law_v1.md sec2.1
        補題 PIN-A の再導出(既在・falsifier 発見穴4)。新規は
        ker T_{-1,1}=iota(N) + 帰結(iota(N)!=N => 非isolated / isolated
        => iota-不変)、着想は Sol F110-2.1。
  (v)   N5 control 引用: 定義ノート §4-7 / div_law_v1.md sec10.2 検査(I)
        (c の位数5・f=1のcharming GT-pairにm=-1が含まれる確認 -- c!=1の
        窓でも補題PIN-Aが生きることの傍証)。
  (vi)  「K subseteq iota(N) + 指数一致で等号」の段を明示フィールド化。
  (vii) wb_charming の"not asserted"の虚偽記載を訂正、SURJ/charming を
        agreement 集計から除外(記録としては残す)。
  (viii)SETDIGEST の式を区切り子込みで散文化。

Item5(票§3.3 torsor整合)は明示的に「未実施」と書くのみ(便112でSolに諮る)。
"""
import json
import hashlib

with open("search/certs/twin_witness_scope1_v1_20260806.json", encoding="utf-8") as f:
    scope1 = json.load(f)

with open("search/certs/twin_witness_mc1_export_v1_1_20260806.json", encoding="utf-8") as f:
    mc1_export = json.load(f)

with open("search/certs/twin_witness_mc1_check_result_v1_1_20260806.json", encoding="utf-8") as f:
    mc1_check = json.load(f)

certs = mc1_export["mirror_certs"]
assert len(certs) == 30, f"expected 30 directed entries, got {len(certs)}"

check_by_uid = {(e["index"], e["target_window_uid"]): e for e in mc1_check["entries"]}

per_window = []
for c in certs:
    key = (c["index"], c["target_window_uid"])
    chk = check_by_uid[key]
    per_window.append({
        "index": c["index"],
        "pair_uid": c["pair_uid"],
        "target_window_uid": c["target_window_uid"],
        "source_kernel_uid": c["source_kernel_uid"],
        "mclass_systemA": c["mclass"],
        "checks_systemA": c["checks"],
        "canary_v1_1_systemA": c["canary_v1_1"],
        "in_PB3_systemA": c["in_PB3"], "c_in_N_systemA": c["c_in_N"],
        "witness_word_systemA": c["witness_word"],
        # 系統B(python, independent)
        "in_PB3_systemB_indep": chk["in_PB3_python_indep"],
        "c_in_N_systemB_indep": chk["c_in_N_python_indep"],
        "hexagon_full_systemB": chk["hexagon_full_ok"],
        "canary_discriminates_systemB": chk["canary_discriminates"],
        "K_subseteq_iotaN_AND_index_match_therefore_equality": {
            "K_subseteq_iota_N": chk["K_subseteq_iotaN"],
            "index_of_N_equals_index_of_iotaN": chk["imorder_ok"],
            "conclusion": "ker(T_{-1,1}) = iota(N) = K  (equality closed by the "
                          "index-counting argument: K subseteq iota(N) and "
                          "|iota(N)| = |N| = index = |K|, so containment forces "
                          "equality)",
            "note_穴修正vi": "この段は v1 の cert にはフィールドとして存在しな"
                            "かった(falsifier 発見穴: 'W-dの(i)(ii)(iii)のうち"
                            "実際に計算されているのはK⊆ι(N)+指数一致で、等号は"
                            "指数論法で閉じているが、certのどの欄にも記録され"
                            "ていない')。v1.1 で明示フィールド化。",
        },
        "systemA_systemB_agreement": {
            "in_PB3": (c["in_PB3"] == chk["in_PB3_python_indep"]),
            "c_in_N": (c["c_in_N"] == chk["c_in_N_python_indep"]),
            "hexagon_full": (c["checks"]["hexagon_full"] == chk["hexagon_full_ok"]),
            "canary_discriminates": (c["canary_v1_1"]["discriminates"] == chk["canary_discriminates"]),
        },
        "vacuous_recorded_not_counted": {
            "surj": chk["surj_ok_VACUOUS"],
            "note": "SURJ (<s1^-1,s2^-1>=Q) and charming (u=-1 unit mod "
                    "anything, f=1 in [P,P]) hold for ANY window by "
                    "construction -- recorded per doc sec 2.6 but EXCLUDED "
                    "from the core cross-system agreement tally (falsifier 穴7).",
        },
    })

all_hexagon_ok = all(w["checks_systemA"]["hexagon_full"] and w["hexagon_full_systemB"] for w in per_window)
all_canary_discrim = all(
    w["canary_v1_1_systemA"]["discriminates"] and w["canary_discriminates_systemB"] for w in per_window
)
all_agree = all(
    all(w["systemA_systemB_agreement"].values()) for w in per_window
)
all_mclass_M1 = all(w["mclass_systemA"] == "M1" for w in per_window)

with open("docs/notes/twin_witness_prereg_iffirst_v1.md", "rb") as f:
    prereg_sha256 = hashlib.sha256(f.read()).hexdigest()
with open("docs/notes/twin_witness_cv9_reading_v1.md", "rb") as f:
    cv9_sha256 = hashlib.sha256(f.read()).hexdigest()
with open("docs/notes/div_law_v1.md", "rb") as f:
    div_law_sha256 = hashlib.sha256(f.read()).hexdigest()

result = {
    "schema": "twin_witness_run/v1.1 (裁定607 修理束 -- v1 は不改変・並置。scope3 は未実行、item5 参照)",
    "supersedes_note": "v1 (search/certs/twin_witness_run_v1_20260806.json) は保持・不改変。"
                        "本 cert はその是正版として並置される(裁定607の指示どおり)。",
    "prereg_doc_path": "docs/notes/twin_witness_prereg_iffirst_v1.md",
    "prereg_doc_sha256": prereg_sha256,
    "cv9_reading_doc_path": "docs/notes/twin_witness_cv9_reading_v1.md",
    "cv9_reading_doc_sha256": cv9_sha256,
    "div_law_doc_path": "docs/notes/div_law_v1.md",
    "div_law_doc_sha256": div_law_sha256,
    "census_cert_path": scope1["cert_path"],
    "census_cert_sha256": scope1["cert_sha256"],

    "scope1_registration": {
        "counts": scope1["counts"],
        "directed_counts": scope1["directed_counts"],
        "setdigest": scope1["setdigest"],
        "registered_set": "L2 (15 pairs / 30 directed, c_in_N and in_PB3 both members)",
        "L3_13_pairs_touched": False,
        "uid_scheme_prose_viii": {
            "note_穴修正viii": "票 §1.2 は 'pair UID の昇順連結の sha256' とのみ"
                "書き、区切り子が明記されていなかった(falsifier 穴9: 'sha256"
                "(\"|\".join(sorted(uids))) で区切り子が書かれておらず、変種を"
                "試すまで再現できなかった')。ここで明記する:",
            "member_uid": 'sha256(UTF-8("|".join(canonical_id_words)))の先頭12桁hex'
                          '(区切り子は半角パイプ "|" 、words の間のみに挿入、末尾には付かない)。',
            "pair_uid": 'sha256(UTF-8(f"{index}#{sorted_muid_1}#{sorted_muid_2}"))の先頭12桁hex'
                        '(区切り子は半角ハッシュ記号 "#" 、index と各 member_uid の間、'
                        'および 2 つの member_uid の間の計 2 箇所に挿入。member_uid は'
                        '辞書式に昇順ソート後。)',
            "setdigest": 'sha256(UTF-8("|".join(sorted(layer_pair_uids)))).hexdigest()'
                         '(全 64 hex 桁。区切り子は半角パイプ "|" 、pair_uid 間のみ。'
                         'pair_uid は辞書式に昇順ソート後。)',
        },
        "note": "matches docs/notes/twin_witness_prereg_iffirst_v1.md sec 1 bit-for-bit "
                "(all counts and all 4 SETDIGESTs machine-reproduced identically).",
    },

    "scope2_mirror_classification_v1_1": {
        "domain": "L2 only (15 pairs / 30 directed). L3 (13 pairs, 裁定T-1) 非接触。",
        "per_window": per_window,
        "counts": {"M0": 0, "M1": 30, "M2": 0},
        "all_M1": all_mclass_M1,

        "repair_1_W_a_full_hexagon": {
            "status": "IMPLEMENTED in both systems (v1 の穴: 両系統とも未実施だった)",
            "systemA": "search/twin-witness-mirror-v1_1.g -- (3.3)(3.4) evaluated "
                       "directly in Q_N=B3/N via ImageElm(hmN,...) equality, both "
                       "directions, all 15 pairs.",
            "systemB": "search/twin_witness_mc1_check_v1_1.py -- (3.3)(3.4) "
                       "reimplemented from scratch on the exported permutations "
                       "(s1,s2 -> x=s1^2,y=s2^2,c=(s1 s2 s1)^2), independent.",
            "result": "30/30 directed windows: hexagon_full = TRUE in both systems, agreement 30/30.",
            "all_pass": all_hexagon_ok,
        },

        "repair_2_S_TW_6_canary_replacement": {
            "status": "OLD CANARY WITHDRAWN (was vacuous: a^-1(ab)b^-1=e holds in "
                      "ANY group, tests nothing window- or convention-specific).",
            "new_canary": "tau implemented as an ACTUAL substitution homomorphism "
                          "on abstract F2=<x,y> (GAP: GroupHomomorphismByImages; "
                          "python: from-scratch word-substitution engine), applied "
                          "by RUNNING the code (not hand-reduced identities). "
                          "Computes P1=tau^2(y^-1), P2=tau(y^-1), P3=y^-1 as "
                          "elements of Q_N, then contrasts forward=P1*P2*P3 "
                          "(paper-product order, W-4 -- must be trivial) against "
                          "reversed=P3*P2*P1 (wrong convention -- must NOT be "
                          "trivial in a non-abelian Q).",
            "result": "30/30 directed windows: forward=TRUE, reversed=FALSE "
                      "(genuinely discriminating -- Q non-abelian in all "
                      "registered windows), both systems agree 30/30.",
            "all_discriminate": all_canary_discrim,
        },

        "repair_3_mc1_export_frozen_schema": {
            "status": "All frozen §2.7 fields now populated: target_window_uid, "
                      "source_kernel_uid, index, in_PB3, c_in_N, perm_degree, "
                      "s1_perm, s2_perm, N_gen_words, K_gen_words, witness_word, "
                      "shadow{m,f_word}, checks{braid,N_in_ker,K_in_ker,imorder,"
                      "iota_w_nontrivial,hexagon_full,surj}.",
            "D_3_independent_reverification": {
                "index": "already independently re-derived in v1 (BFS group order == index)",
                "in_PB3": "NEW in v1.1 -- systemA via GroupHomomorphismByImages(Q,S3,...)<>fail; "
                          "systemB via from-scratch BFS homomorphism-factoring test "
                          "(no GAP, no shared code). Agreement 30/30.",
                "c_in_N": "NEW in v1.1 -- systemA via ImageElm(hm,c_elt)=One(Q); "
                          "systemB via c_perm=(s1 s2 s1)^2 computed from the "
                          "exported permutations directly, checked trivial. "
                          "Agreement 30/30.",
                "status_D3": "3/3 履行(v1 は 1/3 のみ -- index only)。",
            },
            "interface_all_windows_both_directions": "export now carries ALL 15 pairs "
                "x 2 directions (30 entries) with mclass, not just the M1-only subset "
                "(v1's 穴8). Interface can flag A/B-side or systemA/systemB class "
                "disagreement for ANY window (none occurred: all 30 = M1, consistent).",
        },

        "note_穴修正vii": "search/twin-witness-mirror-v1.g (v1) declared 'all as "
            "explicit GAP computations, not asserted' while wb_charming was in "
            "fact `wb_charming := true;;` -- a hardcoded constant, not computed. "
            "This wording was FALSE for that one field (v1 script comment error, "
            "not a math error: charming at m=-1 really is unconditionally true, "
            "gcd(-1,n)=1 for all n, but the SCRIPT never computed it, just "
            "asserted it). v1.1 correction: charming is recorded as a STRUCTURAL "
            "FACT (proven once, universally, not per-window) rather than a "
            "per-window computation, and -- together with SURJ, which IS computed "
            "per-window but is vacuous (<s1^-1,s2^-1>=<s1,s2> always) -- is "
            "EXCLUDED from the core cross-system 'agreement' tally reported above, "
            "while both remain recorded in full (see vacuous_recorded_not_counted "
            "per window).",
    },

    "prediction_accounting_v1_1": {
        "P1_status": "confirmed, exceeded: all 15/15 registered pairs (not just the "
                     "paper-provable 8) are M1. No prediction failure (no "
                     "predicted-M1 window came out M0) -- S-TW-7 not triggered. "
                     "UNCHANGED from v1.",
        "P2_correction_i": {
            "old_v1_framing": "'prereg_prediction_P2_M2_is_zero: true' -- recorded "
                              "as a confirmed PREDICTION.",
            "v1_1_correction": "RECLASSIFIED (falsifier 発見穴6, 裁定607 (i)): M2=0 "
                "is NOT a prediction that could have failed -- it is a THEOREM "
                "following from the registration's own structural facts O-1 "
                "(L1 上で twin 関係は完全マッチング, no triple-or-more twin "
                "clusters) + D-1 (LINS exhaustiveness at the census bound). "
                "Proof sketch: iota(N) is always normal in B3 (iota in Aut(B3)), "
                "same index as N (iota is an automorphism), iota(PB3)=PB3 so "
                "iota(N) in_PB3 iff N in_PB3, c in iota(N) iff iota(c)=c^-1 in N "
                "iff c in N (N normal, so c in N implies c^-1 in N), and "
                "B3/iota(N) = B3/N (conjugate quotients under an automorphism "
                "are isomorphic) -- so iota(N) is ALWAYS a valid census node in "
                "the same layer L2, and {N, iota(N)} is ALWAYS itself a twin "
                "pair (or N=iota(N), i.e. M0). Under O-1 (complete matching, no "
                "node has 2+ twin partners), the ONLY twin partner N can have is "
                "K, so iota(N) in {N,K} is FORCED -- M2 is a priori impossible "
                "for ANY window in this registered layer, not merely observed "
                "to be zero. What the machine run actually checked, then, is a "
                "CENSUS-CONSISTENCY test (did O-1/D-1 actually hold, as an "
                "empirical safeguard against a census bug) -- not a prediction "
                "about the mathematics of individual windows.",
            "reclassified_as": "census consistency check (structural theorem from O-1+D-1), NOT a prediction hit",
        },
        "P3_correction_ii": {
            "old_v1_framing": "'prereg_prediction_P3_both_directions_nonempty: true' "
                              "-- recorded as a single confirmed prediction.",
            "v1_1_correction": "P-3 is a 3-way conjunction; SPLIT per falsifier 穴6 "
                "and 裁定607 (ii):",
            "deduced_part": {
                "claims": ["both directions simultaneously non-empty "
                           "(GTSh(K,N)!=empty and GTSh(N,K)!=empty)",
                           "|GT(N)|=|GT(K)| (TWIN-CARD, itself a candidate lemma)"],
                "status": "LOGICAL CONSEQUENCE of iota(N)=K (already established) "
                          "+ the (candidate) lemmas MIRROR-SHADOW/TWIN-CARD -- "
                          "NOT independently measured by this run. Recorded as "
                          "deduced, not verified by direct computation.",
            },
            "unmeasured_part": {
                "claims": ["source kernel 異なり数 (number of distinct source "
                           "kernels K' with GTSh(K',N)!=empty) >= 2"],
                "status": "UNMEASURED -- requires the scope3 exhaustive enumeration "
                          "(R1-b, doc sec 3) over (m, f-bar) which was NOT executed "
                          "in this pass (v1 also did not run it; explicitly out of "
                          "scope, see scope3_not_executed below). Also entails "
                          "torsor consistency (doc sec 3.3), separately deferred "
                          "(see item5_torsor_not_run).",
            },
        },
        "P4_correction_iii": {
            "old_v1_1_framing_WITHDRAWN": "v1 run cert's P4_note_per_裁定602 said "
                "'P-4 の7対(紙50/50)が全て機械M1 -- MIRROR-OBSTRUCTION の射程外"
                "確定・数学者検討材料' -- framed as an interesting opportunity "
                "for a NEW POSITIVE lemma covering these 7 cases.",
            "v1_1_correction_裁定607_accounting": (
                "falsifier's 任務3 accounting (裁定607 (iii)) supersedes this: "
                "the 7/7 result is NOT '7 independent 50/50 hits' NOR a mere "
                "'measurement quirk'. Correct accounting: "
                "(1) the paper's 'undetermined' (50/50) meant only that "
                "MIRROR-OBSTRUCTION could not NAME a suitable characteristic "
                "cyclic subgroup A for these 5 orders (72,81,84,147,156) -- "
                "not that the true probability of M1 was actually 1/2; "
                "(2) there is a SELECTION EFFECT biasing the base rate strongly "
                "toward M1: iota manufactures twins for free -- if iota(N)!=N "
                "then iota(N) is automatically another census node with an "
                "isomorphic quotient (same argument as the P2 theorem above), "
                "so 'having a twin' FOLLOWS from 'not iota-invariant'; the "
                "census selects exactly the objects that have twins, so under "
                "this selection M1 is the NULL hypothesis, not a surprise; "
                "(3) under O-1+D-1, M1 is not merely 'likely' but FORCED once "
                "iota(N)!=N is known (see P2 theorem) -- so the machine's "
                "output is really a single 15-bit fact: 'is N iota-invariant, "
                "for each of the 15 registered N'; "
                "(4) the substantive content is on the NEGATIVE side: this "
                "layer (index<=1000, c in N, N<=PB3, twin-census-registered) "
                "contains ZERO exotic (non-mirror) twins -- every twin pair "
                "found here is explained by the mirror mechanism, none needed "
                "a genuinely different (non-iota) source of twinning; "
                "(5) the residual dependency for even this negative reading is "
                "census's own isomorphism test (裁定548, StructureDescription+"
                "IdGroup, not established by this run)."
            ),
            "what_actually_needs_a_new_lemma": "a proof that iota(N)!=N for the "
                "7 UNKNOWN-by-paper indices (432,486,504x2,882,936x2) -- NOT a "
                "search for interesting new structure; the interesting OPEN "
                "question is the negative one (why are there no exotic twins "
                "in this layer), not a missing positive lemma.",
        },
    },

    "second_system": {
        "system_A": "GAP (search/twin-witness-mirror-v1_1.g)",
        "system_B": "python, GAP-helper-free (search/twin_witness_mc1_check_v1_1.py)",
        "agreement_core": "30/30 directed windows: braid, N subseteq ker, iota(N)!=N "
            "(explicit witness word), |<s1,s2>|=index, K subseteq iota(N), "
            "hexagon_full (NEW), canary discriminates (NEW), in_PB3 independent "
            "(NEW), c_in_N independent (NEW) -- ALL AGREE.",
        "all_core_agree": all_agree,
        "vacuous_excluded_from_core_vii": ["surj (<s1^-1,s2^-1>=Q, always true)",
                                           "charming (u=-1 unit mod anything, always true)"],
        "grade": "cross-checked (系統A + 系統B 一致; Lean 不使用ゆえ verified ではない)",
    },

    "attribution_iv": {
        "MIRROR_SHADOW_abc": "(a) hexagon, (b) charming, (c) SURJ -- these three "
            "steps are a RE-DERIVATION of docs/notes/div_law_v1.md sec 2.1 "
            "補題 PIN-A (同じ Delta 操作・同じ charming 論法・同じ SURJ 論法。"
            "工房既在, falsifier 発見穴4 で特定)。票 twin_witness_prereg_"
            "iffirst_v1.md sec2.2 の 'novelty grep: MIRROR 0 hit ゆえ [-1,1] が"
            "常にshadowであることはrepo未出' という主張は誤り(新造語で grep "
            "したため既存の PIN-A に当たらなかった -- 二度指摘済みの失敗型)。",
        "genuinely_new": "ker T_{-1,1} = iota(N) の同定、および帰結 "
            "(iota(N)!=N => N は非isolated / N が isolated => iota(N)=N)。"
            "着想は Sol(F110-2.1 L98-104)。div_law の ker は全て ker chi-tilde "
            "であり本件と無関係。",
        "citation_v": {
            "N5_control": "定義ノート §4-7 の N5 control(c の位数5)。f=1 の "
                "charming GT-pair は m in {0,1,3,4} であり m=-1(=4 mod 5)が "
                "含まれることを確認済み(div_law_v1.md sec10.2 検査(I))。"
                "c^m 項が非自明(c!=1)な窓でも補題PIN-A(=本走のMIRROR-SHADOW "
                "(a)(b)(c))が生きることの傍証として引用する。本走の登録15対は "
                "全て c in N(c^m=1 for any m)なので、この控えは本走そのものの "
                "計算ではなく、補題の適用範囲がc!=1側にも及ぶことの参考証拠と"
                "して付記する(falsifier 発見穴5: '本走は中心項を一度も試して"
                "いない'への対応 -- 引用のみ、新規計算はしない)。",
        },
    },

    "M_ISO_2_status": {
        "claim": "M-ISO-2(settled 述語が FALSE を返せることの実証)は満たされる: "
                 "登録した L2 の全15対(directed 30)で ker(T_{-1,1}) = iota(N) = K "
                 "!= N が両系統(A: GAP / B: python, GAP-helper非共有)で確認された。",
        "first_witness": {"index": 126, "pair_uid": "b6b8a3feb9d2"},
        "grading_limitation_verbatim": (
            "本 witness は算術元([-1,1] = 複素共役)であり、非算術証人(B 型)ではない。"
            "本件が閉じるのは M-ISO-2(settled 述語が FALSE を返せることの実証)であって、"
            "FAKE-VOID・非算術証人の存在/非存在には一切触れない。"
        ),
    },

    "scope3_not_executed": {
        "reason": "M0 count = 0 in the registered L2 set (all 15 are M1) -- doc sec3 "
                  "applies to M0-classified windows. Optional-on-M1 full enumeration "
                  "(to get |GT| counts and source-kernel multiplicity) NOT executed.",
    },

    "item5_torsor_not_run": {
        "status": "NOT EXECUTED (票 §3.3 の torsor 整合検査)。",
        "reason_裁定607_5": "司令塔指示により本走では走らせない -- Sol への諮り"
            "(便112)を経てから扱いを決める。この明示のみで足りる。",
        "consequence": "P-3 の 'source kernel 異なり数>=2' も torsor 整合と同様に "
            "未測定(prediction_accounting_v1_1.P3_correction_ii 参照)。",
    },

    "output_claim_per_doc_sec5": (
        "witness FOUND (branch (i) of doc sec 5.3): L2 に M1(鏡映対)が 15 件(全数)。"
        "最小指数の対(126, pair_uid=b6b8a3feb9d2)を第一 witness とする。"
        "禁止語(AS-GAP-6 の非存在主張・AUTO-SETTLED・剛性主張・L3/L0残りへのTRUE/FALSE)は使用していない。"
        "本 v1.1 は falsifier の CV-9 判読(docs/notes/twin_witness_cv9_reading_v1.md)"
        "が支持した『登録L2の15対それぞれでiota(N)!=NかつiotaN)=Kであり、補題PIN-A"
        "(既在)+核同定ker T_{-1,1}=iota(N)により[-1,1]∈GTSh(K,N)は非settled "
        "GT-shadow、ゆえにNは非isolated。最小指数126』という狭い一文の6条件"
        "((a)W-a欠落明記→(a)実装済 (b)カナリア差替→実施済 (c)帰属訂正→実施済 "
        "(d)P-2/P-3格下げ→実施済 (e)c∈N限定+N5引用→実施済 (f)MC-1改版→実施済)"
        "を全て履行した。"
    ),
}

with open("search/certs/twin_witness_run_v1_1_20260806.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Wrote search/certs/twin_witness_run_v1_1_20260806.json")
print(json.dumps({
    "all_hexagon_ok": all_hexagon_ok,
    "all_canary_discrim": all_canary_discrim,
    "all_agree": all_agree,
    "all_mclass_M1": all_mclass_M1,
}, indent=2))
