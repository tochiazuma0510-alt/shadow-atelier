Task1190 — Helmholtz / C 独立規約和と実照合範囲

F1190.C.2 — `FINITE_C_METADATA_CONSISTENCY_SUPPORT`。対象は run 34717506638 / attempt 1 / commit `6b105348b2372a6b59de29904912172b5720e8ec`。私が準備した有限 metadata helper は root が全 400 行を別読（dbcac2 / ad51ec）後、38cd97 / native 0 で実行した。実出力を私が再 read/hash し、284 個の実入力、1459 件の参照結合、全 128 組の candidate/row 鎖を受領した。数学採用の正本は裁定 2293 であり、本返信の判定は有限整合性補助に限る。

R は `C:\Users\81905\AppData\Local\Temp\shadow-atelier-audit163`、Q は `R/run34717506638-reception-v1/candidate-all-v1`。作業ツリー変更は本返信のみ。Task1188/1189 の納品版・数学 source は不変で、私による helper 実行、数学対象の実行/import/AST/compile/selftest、P source/table/private diff/fixture の読取、新 agent、Git/GHA/network/credential 操作はない。

材料は次の実在 pin で固定した。JSON 小票の全 raw は末尾に埋め込み、TEMP のみの票を repo から回収できるようにした。

| 材料（R 相対） | bytes | SHA-256 |
|---|---:|---|
| task1190/C/receive_C_count_and_comparison_metadata_v1.py | 24943 | 0055e4728db0e043ec218d67efc999730208492fa96f9a15169dacd2a0d2b051 |
| task1190/C/actual-C-count-and-comparison-support-v1.json | 503622 | c0edf989f0ea51a2c31add5943481479bbb199f569c835655cf7c56993623dcd |
| task1190/C/C-count-scope-and-eight-conditions-v1.json | 9731 | 3e39fe39793191b6998044b6da1259bfc6391f2a477c99241f96066d0436c94a |
| run34717506638-reception-v1/root-whole-zips-adoption-v1.json | 2306 | 14d99237511f332a429464a04fe6940b3215cb3a0a33fbd29da144649752ae4d |
| run34717506638-reception-v1/candidate-all-members-storage-order-v1.json | 2938750 | 4f73a6b3c35eb678d30b33ed262b33feb367fad4e3c9965cd94df005adf6cb1a |

root 実行コマンドは `python -B R/task1190/C/receive_C_count_and_comparison_metadata_v1.py --reception-root R/run34717506638-reception-v1 --output R/task1190/C/actual-C-count-and-comparison-support-v1.json`（R は上記絶対パスに展開）。実入力は固定名簿内の公開 JSON/native exit に限定し、raw pin を読取時と終了時に照合、参照先 D3 を root 全 ZIP member 名簿へ結合した。出力は CreateNew。503622 B の結果には実入力と参照の全記録がある。1459 は結合回数であり、1459 個の相異なる数学 payload を再計算した数ではない。

F1190.C.3 — C 側の独立した名前付き和を、自己の公開定数票 `task1185/final-v1/public-C9-current-constants-and-all-consumers-final-v1.json`（46747 B / `939b0461826250985a1f19cad1f71b6043bc7bd9d88e020b1153bd0438c98753`）と実 start/intake/layout/result/native 層 metadata へ結合した。P の登録表から値を取っていない。

| 対象 | 独立式・値 | 実 metadata の照合範囲 |
|---|---|---|
| parent / native | 固定 15 + native 6 = 21 | parent-roots の exact role 集合と C 側の登録順 |
| 旧 batch / 親 batch rows | 5×128 = 640 / 6×128 = 768 | intake と各 native 層の保存 counts |
| 旧祖先 / 親祖先 / 今回最終祖先 | 32+65+640 = 737 / 32+65+768 = 865 / 865+128 = 993 | start、native 層、final separator |
| rank | 1450+768 = 2218 → 2346 | 全 128 鎖の各 +1 と最終 state |
| generation | 8155+768 = 8923 → 9051 | 同じ各 +1 と最終 state |
| parent phase / checkpoint / invocation | 6×768 = 4608 / (4+6×128)×6 = 4632 / 6 | native 6 層の実保存宣言値との和 |
| pairing rows | 1450,1578,1706,1834,1962,2090,2218 → 2346 | native 層と final |
| current key 数 | acceptance 12 / start 59 / intake 73 / layout 14 | 実 JSON の top-level key 数 |

歴史 native-v8 の 512/640、609/737、5 層、phase 3840/checkpoint 3860、11/54/65/13 と current V9 を混同しない。上表の保存宣言値の照合は、helper による旧親 768 行や 4608 phase 本体の再演算を意味しない。

F1190.C.4 — 現在の candidate/row manifest は ordinal 0..127 の全 128 組を実読し、決定順、rank/generation、accepted count、predecessor whole SHA、state head、result の行参照、最後の HEAD/final を結合した。各 candidate の 6 phase `[raw,source,primal,p1,B,reduction]`、計 768 の whole SHA は root member 名簿へ照合し、当該 phase JSON 本体は読んでいない。selection の 3 manifest `[section,cochain,tree]` は実 JSON を読み、その局所 D3 を結合した。final manifest の 4 局所 D3 も照合した。数学 binary の要素 decode は 0。有限 helper の seal/型/参照述語を超え、全 JSON の全意味や全算術を改めて照合したとはしない。

実 C の論理 source は `search/check_d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py`、758932 B / `66132850f7dc4ff1edda0d5fe9bce565356fd84b0a10ca1ede328cd65d5b4ffa`。source before/after、保存 source receipt、execution/checker-result の C descriptor が同値。checker-result と checker-stdout の実 raw はともに 15983 B / `4d7141aa2ca0f9a6bc09fc9d2c70bdb76383eae60a07754b0dbbdf4f431d3a7e`。実 exit file は `0\n`、2 B / `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`。保存 execution result の ordinary exit 0、outer_terminated=false とも接続した。全 argv/caps、outer seal/lifetime の全義務は root/Noether の受領範囲である。

C result は PASS、processed/accepted/selected 各 128、dependent 0、candidate_decisions_compared/accepted_rows_compared 各 128、全 128×6 phase と selection 3 件の比較宣言、public_final_compared=true、all_completed_payloads_and_json_compared=true。最終 state head は `fc1ac4d9057ef401de1740954cefa4c45d48ccfdbcffddfb59c8f5f8cae566ff`。これは実 C 実行の型付き保存宣言であり、今回 helper 自身の数学再演算ではない。full_A0=false、grade2 MEMBER/NONMEMBER はともに NOT_DECIDED、original_rho2_directly_read=false / rho2=DERIVED、source_lower_zero=NOT_ASSERTED、old_insert/old_snapshot numeric replay と old_success_suites は各 0、verified=false を保持する。

F1190.C.5 — lambda の 3 つの対象を分ける。全 SHA は埋込小票に記載した。

| 対象 | role / rank | failed count | first index / edge | 今回の扱い |
|---|---|---:|---|---|
| old | batch-parent-v7 / lambda 2090 | 36107 | 304 / 603 | 保存 snapshot。今回再計算なし |
| current selection | batch-parent-v8 / lambda 2218 | 35647 | 242 / 489 | 実 C の独立比較宣言を metadata として受領 |
| final | lambda 2346 | 未計算 | 未計算 | new_lambda_oracle=null |

current-old は -460。128 件の INDEPENDENT は今回の実有限 prefix に関する観測で、将来 batch の独立率や失敗集合の単調性は主張しない。最終 lambda SHA は `289190c37a1a564ec7f062677caad94d4a8dddccb1afee5cd7d117beaa438776`。その oracle の未計算を current 2218 の測定値で補わない。

F1190.C.6 — C 自己試験の公開 stdout、exit、第 8 群 gate を root member pin に結び全文実読した（8aad9f / 465130）。8 群の件数は `[28,9,6,7,8,10,14,15]`、計 97。第 8 群 `batch-parent2218-six-layer-admission` の全 15 行に intended_label_reached=true と whole_saved_positive_and_single_mutation_compared=true がある。current 値に関する末尾 4 件は native65 intake への current field 混入、旧 previous count、旧 total count、native65 intake への current schema 混入。読んだ stdout/gate/exit の pin は埋込小票へ記した。第 10 件は synthetic observed directory arrays、12/15 件は native65 header/seal の範囲であり、物理 full EOF や下流 native 算術への昇格はしない。gate の ordinary_helper_reexecuted=false と actual_anchor_arithmetic_replayed=false を保持した。P の不足については裁定 2293 の公開結論のみを継承し、P 私有実装を読んで判定していない。

F1190.C.7 — V8→初期 V9 の自己/root 静的別読と Task1189 の逆置換を継承する。初期 V9→repair2 は current identity の 4 RHS、+40 B の変更だけで、262 nonprefix raw、C4 の 24 名/21 実体、旧 native 19 領域の保持を既採用票に結ぶ。この範囲で検査述語の弱化は見つけていない。今回全数学 source の意味証明を新しくやり直したものではない。継承 4 票は 2724d0 で fresh 全 pin を再照合し、票名と D3 を埋込小票に列挙した。

F1190.C.1 — 旧 CV9 の見かけの pin 差は解消済み。指定の旧 43817 B / `a89e666346c1e7938990dd1868c020d9f39f5e8fdcf994dea330c54edfe19c49` は現 V8 ノート先頭 43817 raw bytes と完全一致（d1a484）。現物全体 44473 B / `969b3abe77f6b9dc39739ee879530c765b4b57601d2d2e777828d372fbaeb2ed` の増分は末尾の裁定 2279 追補と layout 12/13 の訂正であり、root の Git 全差分読取 670ebd と整合した。原本文 pin を現物全体 pin と呼び替えない。私自身の Git 読取はない。

F1190.C.8 — 最新の正本は `ops/express/20260913_fable_astra_2293_v9_accepted_rank2346_v10_premises.md`（全文 a52d6d）と `docs/notes/fixed_lambda_batch_v9_cv9_reading_v1.md` の限定 8 条。後者は今回参照時 61831 B / `b0afe4a6f2b12733582baceedf333cedbabbde40042100bdf30403a4058494d4`、§4 L154–178 を実読した。本文全部を私が読了したとはしない。旧限定 7 条に第 8 条を加え、次を保持する。

1. 同一対象 2218→2346 の 1 batch に限る。final oracle=null、full_A0=false、grade2 は未裁定。
2. 128 件は実 prefix 観測。old lambda 2090 は再計算せず、将来独立率・失敗集合単調性や Task988 F4 の排除を主張しない。
3. shared kernel 2 件/P+C 4 領域、call coverage=NOT_MEASURED。第 3 独立実装ではない。
4. falsifier と本追加補助は旧 2218 物理行を再演算しない。rho2 は DERIVED のまま、原 rho2 直読なし。
5. harness は単著。C 独立和と P/driver 表を分ける。GHA の public wire D3 型・形確認は provenance の範囲で、root/author の文書全文別読や Task1188 の固定 domain 受領を GHA 自動全内容 gate と呼ばない。
6. C current candidate-phase timestamp は未形成。親層 inclusive 計器・native 操作計器を current 全体や P+C の全計測へ拡張せず、重複秒を合算しない。
7. falsifier の full ZIP 未取得という原 scope は保持。root の両 ZIP 全取得・member pin 受領が追加根拠で、本 helper はその有限 metadata 接続に限る。空 directory/formal inventory の別受領をこの helper の実績に含めない。
8. P current 値否定例の欠品は新限定として残る。C の 15 件は今回の実保存 stdout/gate で確認済み。

公開 CV9 の「7 世代中 3 回増」は採用しない。列 `[36274,36104,36002,35921,36000,36107,35647]` の隣接差は `[-170,-102,-81,79,107,-460]`、厳密増加は 2 回。root にも同じ所見があり、root erratum 記帳予定として小票を固定した。ここから単調減少も導かない。

本担当の有限補助は完了。数学的な root/Sol 採用、全正式受領、V10 準備認可は各正本の別責務であり、本担当から新 universe/parent/batch/caps の変更や実装を追加していない。以下は `C-count-scope-and-eight-conditions-v1.json` の byte 同一な公開原文である。
```json
{
  "schema": "task1190.C.count-scope-and-eight-conditions.v1",
  "status": "FINITE_CONSISTENCY_SUPPORT_WITH_RETAINED_LIMITATIONS",
  "run": 34717506638,
  "attempt": 1,
  "head": "6b105348b2372a6b59de29904912172b5720e8ec",
  "mathematical_adoption_authority": "Ruling2293; this author support does not issue a mathematical verdict",
  "helper": {
    "file": "task1190/C/receive_C_count_and_comparison_metadata_v1.py",
    "bytes": 24943,
    "sha256": "0055e4728db0e043ec218d67efc999730208492fa96f9a15169dacd2a0d2b051",
    "root_full_source_reads": ["dbcac2", "ad51ec"],
    "root_actual_metadata_execution": "38cd97/native0",
    "author_execution": false
  },
  "actual_support": {
    "file": "task1190/C/actual-C-count-and-comparison-support-v1.json",
    "bytes": 503622,
    "sha256": "c0edf989f0ea51a2c31add5943481479bbb199f569c835655cf7c56993623dcd",
    "author_fresh_pin_and_summary_read": "e0348c",
    "raw_inputs_read_and_rechecked": 284,
    "reference_joins": 1459,
    "candidate_row_chain_pairs": 128,
    "candidate_phase_references": 768,
    "candidate_phase_JSON_bodies_read_by_helper": 0,
    "selection_phase_manifest_objects_read": 3,
    "mathematical_payload_elements_decoded": 0
  },
  "C_source": {
    "file": "search/check_d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py",
    "bytes": 758932,
    "sha256": "66132850f7dc4ff1edda0d5fe9bce565356fd84b0a10ca1ede328cd65d5b4ffa"
  },
  "unchanged_predicate_evidence": [
    {"file": "root-C9-native-draft-source-adoption-v1.json", "bytes": 6253, "sha256": "f2a82dfa94a1682e43e46335057fc09dde4617cd9d9d5f4b7d23131405537407"},
    {"file": "root-C9-operations-and-wire-source-adoption-v1.json", "bytes": 10355, "sha256": "8bb2743eba514075414d7a52346ef41e062ec5e9fc91747337e1eec96e8d2807"},
    {"file": "root-C9-final-opaque-adoption-v1.json", "bytes": 3254, "sha256": "24092a93142cf162d5ee3c972683e54c49414d6aec9aa2f847cdd0a281fcd2a1"},
    {"file": "root-C9-repair2-source-and-public-adoption-v1.json", "bytes": 3475, "sha256": "e343c7b3de5211cc0694ffb5657993c2b826539dcc7d0df6304b7ca2e1b17f70"}
  ],
  "weakening_scope": "Inherited V8-to-initial-V9 static author/root reads plus Task1189 exact four RHS identity changes; no fresh whole-source semantic reproof and no mathematical execution in Task1190. No weakening found within those adopted C differences.",
  "independent_basis": {
    "base_rank": 1450,
    "base_generation": 8155,
    "original_ancestors": [32,65],
    "six_named_native_rows": [128,128,128,128,128,128],
    "candidate_phases": ["raw","source","primal","p1","B","reduction"],
    "initial_checkpoints_per_layer": 4,
    "current_batch_size": 128,
    "current_max_batches": 1,
    "refill": false,
    "P_count_table_read": false
  },
  "actual_count_joins": {
    "parent_roles": {"formula": "15 fixed roles + six native roles", "value": 21},
    "previous_batch_rows": {"formula": "128+128+128+128+128", "value": 640},
    "total_parent_batch_rows": {"formula": "640+128", "value": 768},
    "previous_ancestry": {"formula": "32+65+640", "value": 737},
    "accepted_ancestry": {"formula": "32+65+768", "value": 865},
    "final_ancestry": {"formula": "865+128", "value": 993},
    "parent_rank": {"formula": "1450+768", "value": 2218},
    "final_rank": {"formula": "2218+128", "value": 2346},
    "parent_generation": {"formula": "8155+768", "value": 8923},
    "final_generation": {"formula": "8923+128", "value": 9051},
    "parent_phase_manifests": {"formula": "6*768", "value": 4608},
    "parent_checkpoints": {"formula": "(4+6*128)*6", "value": 4632},
    "parent_invocations": {"formula": "six native layers", "value": 6},
    "native_pairing_rows": [1450,1578,1706,1834,1962,2090,2218],
    "final_pairing_rows": 2346,
    "current_key_counts": {"acceptance": 12, "start": 59, "parent_intake": 73, "parent_layout": 14}
  },
  "C_runtime_result": {
    "file": "checker-result.json",
    "bytes": 15983,
    "sha256": "4d7141aa2ca0f9a6bc09fc9d2c70bdb76383eae60a07754b0dbbdf4f431d3a7e",
    "status": "PASS",
    "actual_native_exit": 0,
    "state_head": "fc1ac4d9057ef401de1740954cefa4c45d48ccfdbcffddfb59c8f5f8cae566ff",
    "processed_candidates": 128,
    "accepted_new_rows": 128,
    "dependent_candidates": 0,
    "candidate_decisions_compared": 128,
    "accepted_rows_compared": 128,
    "selection_phases_compared": ["section","cochain","tree"],
    "public_final_compared": true,
    "all_completed_payloads_and_json_compared": true,
    "declarations_not_a_new_author_replay": true
  },
  "three_lambda_scopes": {
    "old": {"role": "batch-parent-v7", "lambda_rank": 2090, "failed_count": 36107, "first_failed_index": 304, "first_failed_edge": 603, "sha256": "dd56526873446b8bf3a5bc597902edf2619bd96e7cff9b572cea9a1f8d3e62a2", "same_run_recomputed": false},
    "current": {"role": "batch-parent-v8", "lambda_rank": 2218, "failed_count": 35647, "first_failed_index": 242, "first_failed_edge": 489, "sha256": "63b796b6a1d03fce798ccd5b81f2ee4720012b15def7227b5075e40245968b67", "C_native_independent_comparison_declared": true, "this_helper_recomputed": false},
    "final": {"lambda_rank": 2346, "sha256": "289190c37a1a564ec7f062677caad94d4a8dddccb1afee5cd7d117beaa438776", "new_lambda_oracle": null}
  },
  "actual_C_selftest": {
    "stdout": {"file": "checker-selftest-stdout.json", "bytes": 6495, "sha256": "1a9578a427c5b22f9f154e90f498fa1f9a98e63118005d49c1771e28caffdb90"},
    "eighth_gate": {"file": "checker-selftest-eighth-fixture-gate.json", "bytes": 19534, "sha256": "5eb2dda0438be0f17b9f369d69f5787dcba78803474e2b084b4491febc9863c4"},
    "exit": {"file": "checker-selftest-exit-code.txt", "bytes": 2, "sha256": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa"},
    "root_member_pin_and_author_raw_reads": ["8aad9f", "465130"],
    "group_counts": [28,9,6,7,8,10,14,15],
    "total_cases": 97,
    "eighth_group": "batch-parent2218-six-layer-admission",
    "current_value_cases": ["current-field-in-native65-intake", "current-previous-batch-count-is-stale", "current-total-batch-count-is-stale", "current-schema-in-native65-intake"],
    "all15_gate_rows_intended_label_reached": true,
    "all15_gate_rows_whole_saved_positive_and_single_mutation_compared": true,
    "actual_anchor_arithmetic_replayed": false,
    "ordinary_helper_reexecuted_by_gate": false,
    "scope": "Synthetic purpose metadata; case10 observed directory arrays only, cases12/15 native65 header/seal only. No physical whole-tree EOF or downstream native arithmetic claim."
  },
  "document_identity": {
    "old_v8_original_prefix": {"bytes": 43817, "sha256": "a89e666346c1e7938990dd1868c020d9f39f5e8fdcf994dea330c54edfe19c49"},
    "old_v8_current_document": {"file": "docs/notes/fixed_lambda_batch_v8_cv9_reading_v1.md", "bytes": 44473, "sha256": "969b3abe77f6b9dc39739ee879530c765b4b57601d2d2e777828d372fbaeb2ed"},
    "old_prefix_fresh_equal": "d1a484; root full appended2279 diff670ebd",
    "current_v9": {"file": "docs/notes/fixed_lambda_batch_v9_cv9_reading_v1.md", "bytes": 61831, "sha256": "b0afe4a6f2b12733582baceedf333cedbabbde40042100bdf30403a4058494d4"},
    "current_8_conditions_lines": [154,178],
    "F1190_C_1_status": "CLOSED: original prefix pin equals; appended2279 corrections are separately retained"
  },
  "eight_conditions_C_scope": [
    {"number": 1, "scope": "Only2218-to2346 one batch. Final lambda2346 oracle null; full_A0 false; neither grade2 MEMBER nor NONMEMBER decided."},
    {"number": 2, "scope": "128 accepted is actual finite prefix observation, not a guarantee for later batches. Old lambda2090 was not recomputed; current35647 differs from old36107 by -460. No failure-set monotonicity or independence rate is asserted."},
    {"number": 3, "scope": "Two shared arithmetic kernels/four P-C regions; current_run_call_coverage NOT_MEASURED and no third independence. This metadata helper does not extend kernel coverage."},
    {"number": 4, "scope": "The falsifier's and this author's new work do not replay the old2218 physical rows. rho2 remains derived and original_rho2_directly_read false. Current arithmetic authority remains the actual C execution plus independent mathematical ruling."},
    {"number": 5, "scope": "Single-author harness. C named sums are independent of the P/driver table. Public wire descriptor type checking in the GHA is provenance-only; author/root static whole-content reads and Task1188 pinned domain reception are separate evidence."},
    {"number": 6, "scope": "C current candidate-phase timestamps remain absent. Parent-authentication and native operation intervals retain separate inclusive/exclusive scopes and cannot be promoted to full candidate or P+C coverage."},
    {"number": 7, "scope": "The falsifier did not acquire whole ZIPs. Root did acquire both full ZIPs and all member pins; this helper joins finite selected metadata to that custody without rewriting the falsifier's read scope or claiming directory formal reception."},
    {"number": 8, "scope": "Ruling2293 adds the P-side current-value negative-case gap. This C author read only C actual stdout/gate: all15 current C cases are present. No claim about P private implementation or repair is made here."}
  ],
  "failure_count_erratum": {
    "public_historical_vector": [36274,36104,36002,35921,36000,36107,35647],
    "adjacent_differences": [-170,-102,-81,79,107,-460],
    "strict_increase_count": 2,
    "published_three_increases_is_not_adopted": true,
    "root_erratum_record_pending_at_author_ticket": true,
    "no_monotonic_decrease_inference": true
  },
  "no_new_mathematical_target_execution": true,
  "no_P_private_source_diff_fixture_read": true,
  "no_new_resource_universe_parent_or_batch_changes": true,
  "verified": false
}
```

AUDIT_1190_C_VERDICT:
