# Task1072 — metadata 比較の限定コスト点検

**F1　結論と射程。** `Same` の配列／object 内の scalar leaf 二箇所だけで関数呼出しを減らす案を保存した。一回の小さな metadata fixture は 62 件すべてで元と新の受理／拒否・例外メッセージ全文が一致し、両測定データで事前登録した中央値 20% 以上の短縮条件を満たした。したがって限定案を root と別読者へ提出する。実 candidate 全受領の速度は未測定で、前回約 81 分の内訳 profile もない。本票から全受領時間の短縮率を推測しない。基点 1071 をそのまま使う経路は保持され、この案の採否を実受領の前提にしない。

指示書 `sol/luna_task_1072_r07_metadata_comparison_cost_audit.md` は全文読了（3,748 B / `9f6d4d592aca1918115bbb5dbe713f28d5687f13bbba508c9378e8a821333904`）。変更範囲は本返信と `C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/task1072/`（以下 T）のみ。原 1071 の全 raw は CreateNew で保存した。P/C 私的数学本文、source、WF、実入力は変更していない。

**F2　全差分と意味の保持。** 新案 `T/audit-r07-batch-v4-metadata-v4.ps1` は 261,620 B / `a16d8497aafec0cebc6d1c07cc962024ce344854d6d374810e26dc47ce54cb74`、LF 2474 / CR 0 / ASCII / BOM なし / 最終 LF。変更は元 L55–75 の `Same` 1,409 B を新 L55–105 の 3,019 B へ置き換えたものだけである。先行 5,027 B と後続 253,574 B は全 raw 同一。新関数を元関数へ戻した全文は、基点 260,010 B / `accc758ebe41c6c5a239245a62beb961ef1f145bf04f3154c6b34442ec774e44` と完全一致した。全 main、PlainInt、FilePin、JSON 入場、全 parent/source/phase/fixture/inventory/hash/seal/EOF 判定の本文は保持した。

配列と object の各 child を読み、null、string、ValueType の場合に従来と同じ式で直接判定し、失敗時は同じ label を throw する。配列・object の child は引き続き `Same` で全再帰する。Int32/Int64 等の型幅、Bool と数、Single/Double/Decimal、大小文字、null、順序・長さ、object の Ordinal key sort・全 key 集合は従来通り。比較対象の省略、cache、型統一、JSON 文字列同値への変更はない。NaN/Infinity 対照は元 Same の Equals による同値意味を保持する確認であり、別の JSON／finite 入場 gate を緩和するものではない。失敗時の例外メッセージは保持するが、変更された関数内の行番号・call stack の同一性は主張しない。

実 Launch は `34120585268/1`、head `92720e5371164545259c3007cb11e951fa5e1686`、承認 2197 のまま。`Artifact = null` / `ImplementationComplete = false` を保持する。候補 artifact 未登録の静的案で、全受領器の実行・dot-source・Invoke-Expression・ScriptBlock 変換は 0 回である。

**F3　事前登録と唯一の実行。** 12:53:49.0308260Z に範囲・上限を登録し、12:57:32.6355102Z に exact 62 件、入力／script pin、採用検討閾値を追加登録した。その後、PowerShell 5.1.19041.6456 で 13:01:38.4250819Z から一回だけ fixture を実行し、13:01:44.1238206Z に結果票を形成した。比較関数の全文を見える script に保存し、元／新からの相違が関数名とその再帰呼出し名だけであることも全 raw で照合した。script と合成入力の full SHA guard を通して実行した。

22 scalar 対照を配列内／object 内の双方へ置いた 44 件と、空・一要素・順序・nested arrays、object key 順／大小文字／欠品、container 型の左右非対称等 18 件、合計 62 件である。各対照の両実装を一回ずつ呼び、期待した受理／拒否と両者の例外メッセージを比較した。全 62 件が一致した。正しさ比較は 0.3576708 秒、script 本体の stopwatch は 5.6232714 秒、exec 外枠は 6.2609622 秒、exit 0。再実行はしていない。

測定は人工の 512 scalar leaf 配列と 128 metadata record 配列のみで、実 artifact／数学ベクトルを入力にしていない。合成 JSON を独立に二度読み、全配列同士を比較した。各データ・実装の warmup 一回ずつで計 4 回、timed 比較は各 5 round の計 20 回、round ごとに元／新の先行順を交互にした。正しさ比較の入口呼出し 124 回を含め、外側比較呼出しは計 148 回。内部の再帰呼出し数は別途計測していない。事前上限は正しさ 10 秒、測定 25 秒、fixture 全体 40 秒、実行中の一比較による超過猶予 5 秒で、実行は全上限内で終了した。

| 合成データ | 元 Same 中央値（秒） | 新 Same 中央値（秒） | 新／元 | 事前 20% 短縮条件 |
| --- | ---: | ---: | ---: | --- |
| scalar leaf 512 個 | 0.1081056 | 0.0008041 | 0.00743810 | 達成 |
| metadata record 128 件 | 0.5067662 | 0.2300979 | 0.45405139 | 達成 |

小測定の全 20 個の実測値と 62 件の両観測は結果票に保存した。この限定結果は、全 file hash／ZIP／disk 読取／他の PowerShell 処理が占める時間を測っていない。新受領器の全実入力での実走・数学照合・assurance の昇格を意味しない。

**F4　全納品 pin。** 以下は T 内の相対名。全 15 file の bytes/SHA は `final-static-delivery-v1.json` にも固定した。後者自体は 4,321 B / `133ccfc2164092dd4bd08a0530470c8630c29faca77c49f3f7e3316002e2f4ce`。公開 producer metadata 二票は原 1071 から全 raw コピーし、本文・pin を保持した。新 P の数学本文は読んでいない。

| file | bytes | SHA256 |
| --- | ---: | --- |
| audit-r07-batch-v4-metadata-v4.ps1 | 261620 | a16d8497aafec0cebc6d1c07cc962024ce344854d6d374810e26dc47ce54cb74 |
| baseline-1071-metadata-v3.ps1 | 260010 | accc758ebe41c6c5a239245a62beb961ef1f145bf04f3154c6b34442ec774e44 |
| comparison-preregistration-v1.json | 2223 | ecc6e81afdc375667b15c38541156f8c838deb6d8d42fcd4fc06a62c52e5bb16 |
| comparison-preregistration-exact-v1.json | 1108 | 0567f21ab0d31537252c35ccb4b7a4d732e273cf7e225b012b22e2a213d30a20 |
| same-original-v1.txt | 1409 | b2c9cd7561cadfe70653cbe29bcf9be31cc115599a9bbc42d79764cffb899f04 |
| same-candidate-v1.txt | 3019 | 55a6b4b67a7bdb3c6094cbc8211330caf09248ddee13f0fc0432c14bbdbda73a |
| same-function-full-delta-v1.txt | 4481 | ca82b7eb5e637005eeef234518ffa0904f10727d554ed724187043280c8a7477 |
| whole-helper-full-function-diff-v1.txt | 4593 | 199144f405ea0a70b4df11369130da39dd37b9a4ff9a66dfa170edda252fc25f |
| whole-raw-same-substitution-v1.json | 2384 | 6a2c7a6bd4ffa804d565aa8f851f0979f173decc4ee16a896cf811e07116a716 |
| synthetic-comparison-input-v1.json | 30707 | 1ca61b4714843f6abdc378c3b0fb02f685f342100c2c5dde63e9cdf7b46dadb4 |
| same-metadata-fixture-v1.ps1 | 13971 | 12b8f806d5d7a7fad8912fe3c47ed730aa20dc0e4c0972a38edd2541b0c701cb |
| same-metadata-fixture-result-v1.json | 82547 | 9ef4889c4ecc3bf4975c25e9be1dcf645bea6466f0bb577d034c398cff3a997b |
| fixture-execution-observation-v1.json | 1150 | dd79b4d46c95ac0cecdf2010d0e4f3baec4dd4499a7114709d2dc365e0fac52b |
| registered-producer-body-inheritance-v2.json | 17587 | 768cbfec35dae2abc80cade25f184c626bef07a8fefb758383a8669e23a0ebed |
| registered-producer-current-regions-v2.json | 267079 | b36818b41ab82ea33e2008e6db921e9cfb4138af472a473b47bbeac2eac063b9 |

**F5　凍結・未実施。** 本案と上表をこの pin で作者凍結する。root と独立別読の採否前には新 helper を受領に使わない。実 artifact の追加登録は別 snapshot の対象で、原 1071／1069 の凍結値に上書きしない。今回の唯一の実行例外は事前登録した小 PowerShell metadata fixture 一回であり、全受領器、source、数学、Python、AST、compile、import、GAP、Git、GHA、network、credentials の実行・利用は 0、新 agent も起動していない。未解決は全受領時間への寄与と新案の独立別読・root 採否であり、数学上の実成果を追加したものではない。

AUDIT_1072_VERDICT: LOCAL_METADATA_COMPARISON_PASS_PROPOSAL_FROZEN_PENDING_INDEPENDENT_REVIEW; 62/62 SAME_OUTCOMES_AND_MESSAGES; ONE_SMALL_FIXTURE_ONLY; FULL_RECEIVER_NOT_EXECUTED; ARTIFACT_NULL_GUARD_FALSE; ASSURANCE_UNCHANGED.
