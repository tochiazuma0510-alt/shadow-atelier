Task1045 — k128 WF3 の算術試験継承・共有 TCB 票の独立静的監査

**F1. 範囲と現在の判定。** Task1045、公開 Task1035/1040/1041、旧 WF2 全 2314 行、公開 Task1030 の fixture 保存契約、既存独立監査返信1031を全文読了した。Task1045 の「既存独立監査1030」は番号上、1030 が公開保存契約、1031 が独立監査なので、両方を読んだ。変更した作業ツリーは本返信だけである。WF/source を変更せず、P3 私的本文・私的作者票は読んでいない。ローカル Python/import/AST/GAP/数学計算・GHA/network/git/credential・新 agent は使用していない。実施したのは公開 workflow の全文・差分読取、PowerShell による全 file bytes/SHA と raw LF 行領域の metadata 照合だけである。

**最終判定は STATIC_WORKFLOW_PASS、追加必須修理なし。** root が公開配達した登録表の全字段・実 metadata（F7）、WF generator の全完成差分（F8）、作者の最終 freeze 宣言（F9）まで確認した。全静的監査は閉じている。新 GHA と k128 の実結果は未観測であり、本票のPASSに含めない。

**F2. 読了した実 file と全保持比較。** 旧 WF2 は `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml`、166471 B / SHA256 `887c779cfa7f00fb780cc8919e2b34140d05ef598038fe4d71e13a0aefa997d5` / LF2314。新 WF3 の読取 snapshot は `%TEMP%/shadow-atelier-audit163/task1045-wf3-read-snapshot-v1.yml`、180534 B / `b725a5204c75af7bd8caa20c2576e40e494dc7989b3faae28c5b767d850c48b4` / LF2504。同 hash の作業ツリー `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v3.yml` から保存し、その全文の保持部分と全差分を読了した。これは未凍結の読了基点であって最終 pin ではない。

公開文字列の同じ indentation の `def` 境界だけを切り出し、旧67関数中55関数の全文一致、12変更、6追加、除去0を確認した。Python AST や source の実行は使っていない。12変更は `source_mode/live_mode/command/execute/checked_execution/test_gate/post_producer/preservation_mode/coverage_receipt/final_gate/final_mode/main`、6追加は `audit_source_bytes/audit_raw_lines/audit_registered_range/audit_material_observation/audit_material_bindings/audit_mode`。最後の `main` 区間には YAML 実行 tail も含めて比較した。全差分は `%TEMP%/shadow-atelier-audit163/task1045-wf2-to-wf3-read-diff-v1.txt` に読取資料として保存した。`fc.exe` の表示行番号は長行折返しにより実 source 行番号と異なるため、以下の source 位置は実 LF 行による。

**F3. 旧入力・実行・保存契約の保持。** 15 親の固定実 tuple、同旧64/rank1450/gen8155 起点、元 completion 10 entry と resume64 30 entry、旧32/新64 checker prefix・3 invocation・元 int `external_e_attached=1` の結合は全保持である。全 ZIP の bytes/SHA、API run/artifact/期限、safe extraction と全 entry EOF、全親 file/directory、同 runtime/19 retained Python＋新 P/C＋raw3 の24件、GHA 内だけの実行 source AST 記帳、exact six-key acceptance も保持している。私的 P/C source の数学を本票で再監査したとはしない。

新登録は128/1/refill=false、`CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX`、候補 ordinal 0..127、progress sequence ≤771 である。親64の数値を128へ書き換えず、採用数による rank/generation の更新だけを gate する。fresh REPORT と一回だけの通常 P5400秒・C10800秒、7168 MiB、outer6000/11400秒、job330分を保持する。新二群名と公開拒否数 P30/9・C28/8、明示 `--selftest-root` を接続し、旧数学三群は再走0、metadata16 は今回の登録/REPORT への回帰として実行を予定する。全て新実 GHA ではまだ未観測である。

P/C fixture は各 subtree の全 files/directories、hidden tail と空 directory を before/P後/C後で照合する。inner ZIP は全明示 directory と全 file を保存し、再読時に名前・型・bytes/SHA/CRC/EOF を照合する。partial な実在 fixture の ZIP 保存操作が PASS でも、`both_completed_roots_unchanged=false` のまま完成 candidate を拒否する。全 REPORT は増加を許し、除外は `envelope-inventory-before-run.json` と `run-receipt.json` の自己循環回避2件だけ。成功 candidate と always diagnostics は同じ全 REPORT、hidden を含め、新1041の認可どおり retention30日とする。

**F4. 実行前後へ接続した新監査 metadata。** raw source helper（実573–615行）は exact 三字段・全 source pin・checkout containment/ancestor symlink・UTF-8/LF/no BOM/末尾 LF を確認し、1始まり両端包含の LF 行を末尾 LF 込みで切り出す。任意の whitespace 正規化や意味 parser を使わない。新監査票は数学の既存 acceptance へ key を追加せず、`audit-materials-before.json` に二票/登録表/非実行歴史 source copy の full pins と launch/source receipt を結ぶ設計である。

`audit_material_bindings`（実746–783行）は before の exact fields、二票の seal/fullfile pin、登録表、歴史 source 原本/全 copy inventory、false assurance を再読する。歴史 source 名は現在の24実行/raw closureと disjoint にし、copy の file roster と全 original source pin を一致させる。`live_mode` の前、全 execution の開始と `checked_execution`、P後の入力票、always保全、C後の入力一致、最終 gate と run receipt へ同じ metadata を渡している。歴史 source が途中までしか保存できない場合も個別の acquired receipt/copy と partial inventory を残し、完成 before がなければ INCOMPLETE とする。最終 REPORT 両 upload に追加二票/登録表/履歴 copy が含まれる。完成済み比較/実行の gate を弱める変更はない。

F2の初回 snapshot の `audit_mode`（当時実785–787行）は登録表未受理を明示拒否する placeholder だった。その後の公開登録表と generation の全完成差分はF7/F8で別に読了し、この未完境界を閉じた。

**F5. 歴史試験と shared TCB の境界。** 公開1040の歴史 run34004423047/1、head `81a1b22975308ae0ac628f97da447a008a1d087e`、artifact9980697123、ZIP94677901 B / `d21f9e0b93b070327b4ef02e975dc377a8020e7f8aa7553a720d97d690ed85f0`、旧 P 票2409 B / `1bfb8b4404d1d24e481dd139b6b84136ef21e8e79b1fd3548607a66b45d1c238`、旧 C 票1725 B / `2c8005f98883a711bece270552fa5f39f85755a8d06a27f0cf6c1b3fc257cdce` は新公開定数に一致する。旧三群の名前/順序、歴史拒否数 P7/6/26・C2/3/14、`old_mathematical_suites_rerun=0`、`historical_payload_reacquired_in_this_run=false` を保持する。歴史 PASS と今回の実再走を同じ状態にしない。

shared 二 kernel/四 source の public full pins と raw LF 範囲を metadata だけ独立に照合した。`vectorized_projection_chunk` の P342–357 は1011 B / `b68bbb5af24240a8758fffa0902323727e0a22838f1acdaede8e1d1c867a5199`、C269–284 は1020 B / `6e785bdf5b4fb8b2010b3645462ffaff8d84e2ff2e2c134eafa0425c18b4beaf`。`sparse_adjoint` の P/C192–203 は各670 B / `4b75584298a67005d5af61bd972d8dfe5069b65f1dd5d32bdeb345bf2eadbd39`。これらは whole source と宣言範囲の実 bytes の記録であり、呼出し回数の測定ではない。新票の `current_run_call_coverage=NOT_MEASURED`、`kernel_third_independence_claimed=false` を確認した。歴史/current の near-clone 由来を残し、C全 body 同一や現在 sparse helper の実走を推論しない。

**F6. 現 pin と実未実行。** 公開 WF の24 source/raw descriptorを全件実 bytes/SHAで照合し、全24一致した。P3 は `search/d972_r07_fixed_lambda_cycle_batch_v3.py`、209926 B / `a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8`。C3 は `search/check_d972_r07_fixed_lambda_cycle_batch_v3.py`、178914 B / `1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7`。P 私的本文は表示せず full hash と公開登録領域の bytes 一致だけを扱った。

root から k64 の受領 metadata v2 `PASS_METADATA_ONLY` の通知を受けているが、本監査でその全票を読んだ、または k128 を実行したとはしない。新128独立・rank1578・新λ oracle の結果は未観測である。新 oracle=null、grade2 MEMBER/NONMEMBER は両 `NOT_DECIDED`、full A0=false、verified=false を保持する。

**F7. root 公開後の登録表全件照合。** `%TEMP%/shadow-atelier-audit163/k128-sources-and-inheritance-registry-v1.json`、76867 B / `9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38` / 全878行を SHA guard 後に全文読了した。root はその全文と1042最終票を読了して限定静的 PASS を受理したと配達しており、私的1042本文を取得する必要はない。registry は public source metadata/region/disposition の正本として扱い、私的 P 数学本文を表示・解釈していない。

全6 source の bytes/SHA、LF数、CR0、BOMなし、末尾 LF を実 bytes と比較した。全60範囲も登録された1始まり両端包含の raw LF byte segment の size/SHAに一致した。9 unchanged group（P2・C7）の各3版は hash比較に加えて全raw byte列を比較し、一致した。2 literal groupは各3版の実raw列を公開 `raw_utf8` のUTF-8 bytesへ比較し、一致した。残る9 reviewed-change groupは公開 disposition/reasonを保持する。これら三分類の範囲を source ごとに整列すると、先頭1から末尾LFまで gap/overlapなしで全bytesを覆う。P各版5範囲、C各版15範囲であり、未登録の source 行を黙って除く余地はない。

| source ID | bytes | LF | 分割数 | 全 SHA256 |
|---|---:|---:|---:|---|
| P1 | 213861 | 3463 | 5 | `229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591` |
| P2 | 208805 | 3420 | 5 | `6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e` |
| P3 | 209926 | 3434 | 5 | `a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8` |
| C1 | 181828 | 2680 | 15 | `7a4289506ce78b0ea562c63c9fb0841179a5bac10bc08165b211ed83982d292f` |
| C2 | 177544 | 2675 | 15 | `4ada8490ef931e639159b2c3522510b6fc2da82551daa9a7aa3f1a1970d0ca90` |
| C3 | 178914 | 2695 | 15 | `1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7` |

公開 shared TCB 4範囲も F5 の先行実測と全一致した。P/Cいずれも不変領域は別登録の BATCH_SIZE に依存するので、各 k の出力同一性を意味しない。P workflow literal と C selector docstring を正規化で消すことはせず、別の実 pin と理由として残す。Cの admission extraction/ordinal/row/count/invocation gates/canary/CLI は変更領域として認証し、旧三算術群の歴史 PASS をその新 helper 全体の実試験と呼ばない。現 registry に追加必須 finding はない。WFへの最終接続はF8で確認した。

**F8. 登録表接続後の WF 全追加差分。** 作者から完成 block の通知を受けた WF3 は283886 B / `6224c2bad40e7a95291b92aa8cb3d5088bc41969287c2262d0c4249058bcab1f` / LF3601。読取 snapshot は `%TEMP%/shadow-atelier-audit163/task1045-wf3-read-snapshot-v2.yml`。F2の初稿から70関数を全文保持し、`source_mode/audit_material_bindings/audit_mode` の3変更、`public_audit_registry/capture_audit_source_versions/compare_audit_regions/compare_audit_shared_kernels` の4追加、除去0を確認した。関数外の追加は登録表 pin と原文 byte literal、先頭コメントの現状態への更新である。全 generator/consumer を読了し、前稿からの実行・保全 tail は全保持を確認した。

WFの `br'''...'''` から YAML 共通10空白だけを除いた literal原文は、root公開登録表の76867 B / `9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38` に全bytes一致した。これは Python literalの評価ではなく公開ASCII文字列の比較で、登録表本文の正規化はしていない。`public_audit_registry` はこの全bytes pinを先に確認し、current P3/C3 の実行pin、同旧64/1450/8155、24 source/raw、15親、新二群と128/1/refill=false、歴史試験の実run/artifact/旧票pin、4kernelを公開定数へ結ぶ。

`capture_audit_source_versions` は全6 sourceの実LF/EOLと全pinを照合し、非実行4sourceだけを `audit-history-sources/search/` に全bytes保存、各 acquired receiptを形成する。`compare_audit_regions` は全60 descriptorの実raw bytes/SHA、同側の三版、9不変領域の全bytes比較、2literalの原文比較、9変更領域の限定dispositionを実行する。sourceごとの全LF範囲を連続に結んで gap/overlap・末尾欠損を拒否する。`compare_audit_shared_kernels` は4kernelの whole sourceを現在の retained closureへ結び、全raw範囲と sparse 両側の同一bytesを比較する。これらは source metadata の照合で、数学 source の import/AST/呼出しを行わない。

`audit_mode` は original registry bytesをREPORTへ保存後に再hashし、全比較を完了してから二票とbeforeを形成し、直後に `audit_material_bindings()` を通す。二票には登録表原文の全意味字段と実range比較結果、current code/launch/source-receipt、historical source全pinを含める。before consumerも固定原文との全bytes一致を追加し、F4の実行前/P後/C後/always/最終gateへ接続する。旧数学三群の再走なし、歴史artifact本体の再取得なし、C全body同一の主張なし、call coverage未測定という境界は維持している。この完成版に追加必須findingはない。

**F9. 最終freeze。** 作者は `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v3.yml` を **283886 B / SHA256 `6224c2bad40e7a95291b92aa8cb3d5088bc41969287c2262d0c4249058bcab1f` / LF3601 / CR0 / BOMなし / ASCII / 末尾LF / 行末空白0** でfreezeしたと通知した。F8の全読了版から変更なしである。rootも同WFと作者返信1041を全文読了した旨を配達しており、本監査は作者私的票を追加取得せず公開WF・公開registry・実pinだけで閉じる。既存旧WF2、source、旧返信は本監査で変更していない。本返信も最終票としてfreezeする。公開commit/push/初回GHAはrootだけが行い、その実run/commitは未発生として本票に架空値を置かない。

AUDIT_1045_VERDICT: STATIC_WORKFLOW_PASS — 最終 WF3 全本文の保持・全差分、root公開 Task1042 全登録表、実60範囲/6source partition/4kernelと二票の生成・全保全接続に追加必須修理なし。作者freeze受領、静的監査を完了。新 GHA / k128結果 / 新canary実PASS は未観測。
