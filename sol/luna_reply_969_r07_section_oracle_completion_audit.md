# Task969 — u32 sentinel 修理と保存 oracle 出力の completion 監査

F0. **限定した source/workflow 静的監査 PASS。新 completion 実走は未実施。** Task968/969を全文読み、root指示によりTask967より本便を優先した。完成した修理source、workflow全文、実diagnostic metadata、最終byte/SHAを確認した。本便で変更するのは本返信のみ。ローカル数値、Python/import/AST/GAP、network/git/credentials/dispatch/追加agent、実装変更は行っていない。公開済み959/960/961は凍結したままである。

F1. **実失敗と見落としを確認した。** 元run33975617653/1、head `c57a722224320f9a573cfe84dea6979df5cb5320`、job101331666867は failure。root回収のdiagnostic id9972256636、name `d972-r07-section-cochain-oracle-v1-diagnostics-33975617653-1`、ZIP2271586 bytes / `c66e7477740c8c5e0c0e9e00e613836bf5baacf00f10acf63fad5b23d6cc113a`を前提に、実展開 `%TEMP%/shadow-atelier-section-oracle-run33975617653-diagnostics-a1` の小JSON/bytes/hashを独立に読んだ。live tuple/ZIP取得はrootの証拠であり、本便ではnetworkを実行していない。

実checker-resultはstatus FAIL、candidate false、phase `complete_tree_eof`、reason `OverflowError:Python integer 4294967295 out of bounds for int32`。v1の `geometry_payloads` 573–574行はint32配列に対し `np.where(...,4294967295,...)` を先に評価し、その後でuint32へcastしている。後置castは選択時の型エラーを防げない。`check_actual` 964行のcomplete tree計算の後、965行のpayload辞書構築でこの関数を呼び、968行以降のstage比較loopへは到達していない。log末尾と一致する。全tree計算の終了を全配列一致として扱わない。

Task961の静的監査はこのserializerのNumPy型変換欠陥を見落とした。旧報告を上書きせず、この便で明記する。新v2の修理とGHA上の実production変換canaryが必要であり、既読A–D算術全体の再設計は求めない。

F2. **保存された実entryと出力型。** 下記の全file byte/SHAを本便で照合した。

| file | bytes | SHA256 |
|---|---:|---|
| checker-result.json | 315 | e500b7fa0a5f4387c36d787999f438cea91189b9ea3fd8ec80e0830cb29173e0 |
| source-receipt.json | 2673 | cd9a45a389cafd0cfb3813181c1365b0a66cdd682cc737a1a68f27b438d92934 |
| output/manifest.json | 1430 | 7df077372a51d12cbf95be5f26c94a5e29ef0f6b118f1ed7efb452ba01942639 |
| output/owner.json | 8419 | 6c71fbc405105bd0722924a308594ba41aea6745725ae85d046ff7409998b322 |
| output/start.json | 48377 | 7ff970e54dec57512593f5445fed387075d6602bff31f41b7db9f34bab045a2a |
| output/source.json | 1246 | af1e178d19e4ee427439d102de74a559ed6202ca0a2839212a60748ccfe482ac |
| output/result.json | 13727 | c7f65255443a8901fa1b6fbab69e81bbc811014e1eb527e7f671e2f6343ba312 |
| output/tree/witness.json | 486 | 1c282b82cbf430b3ef492a325c26ac3c7d2bf9146f15aa76c94744f8477620fd |

source-receiptは元producer `4e7546eb…` と旧checker `2db16640…` を含む14 source、二raw data pinsを記録する。output/source.jsonも元producerを保持する。startはrank1385/generation8090、state head `8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61`、lambda `1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1`、target `111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad`で、受理済みcompletion親と一致する。

producerの保存resultはVIOLATION_CANDIDATE/MATERIALIZATION_PENDINGであり、checker未照合の観測である。tree.jsonのaux零、failed chord12、basis[2,3,4,6,11]、residual support36343、witness scalar1を修理checkerの期待値へliteral固定してはならない。新checkerが同じ式から全arrayを計算する必要がある。

実parent.u32とparent-edge.u32は各217728 bytesで、先頭4 bytesは両方 `FF-FF-FF-FF`。hashは順に `d9a3a80fefa1247916c767a4a6d909bbb58d3a3c995857f7f8a9a119b852e1ed` と `a366c1c8de3f3146ec57f1c27db05eb911514e19b0ddc0cb2fee539c21f969be`。これは保存producerの公開little-endian ABIのbyte観測であり、新checker canaryを実行した結果ではない。

F3. **v2 source の限定差分は静的に適合。** `search/check_d972_r07_section_cochain_oracle_v2.py` の読取値は84402 bytes / `a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d`。`rooted_indices_u32`（572行）は非空1次元のsigned int32/int64だけを許可し、root位置0が厳密に−1、非rootが0以上かつupper_bound未満であることをcast前に要求する。正BFSの既存 `positive_tree`（v1:229行）はroot0、signed int32、全頂点到達を実際に作るため、この入力型に接続する。

確認後に `values.astype(np.int64,copy=True)` を作り、そのコピーのrootへ4294967295を代入し、最後に `<u4` へcastする。非rootの誤負値や上限外をwrapせず、元配列を変更しない。`geometry_payloads`（628行）からparentはVERTICES、parent-edgeはEDGESを上限としてこのhelperを実際に呼ぶ。既存 `typed_array` の `<u4` serializer、schema、公開sentinel値は維持される。

`serialization_selftest`（589行）は同じhelperから同じtyped_arrayまでを呼ぶ。parent/edge双方についてint32のroot−1、0、最後の有効index、little-endian `FF FF FF FF`、入力不変を照合する。非root−1/−2、誤root、parent/edge上限、巨大int64、float、unsignedの先回りwrap、bool、2次元、空配列、plain list、非整数boundを拒否する。専用 `--serialization-selftest` は他modeと排他、parent不要であり、旧selftestを呼ばない。これらは本便ではsourceを読んだだけで、実canaryはGHAで行う。

whole-sourceのテキスト比較も行った。新header、helper/canary挿入、二つの呼出し変更、専用CLIだけをメモリ内で旧形へ戻すと、旧v1の80740文字と全文一致した。これはsource文字列/正規表現の比較であり、Python/AST/数値実行ではない。旧v1の80740 bytes / `2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967` とproducerの73290 bytes / `4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb`も再hashし、不変を確認した。A–D算術、solver、owner/start/result、selectionに変更はない。

F4. **完成workflowの13親、保存物、新旧receiptを確認した。** 新workflowは同じsol branch、marker `[r07-section-cochain-checker-completion-v1-run]`。旧12 artifactsに今回のfailure diagnosticを加え、repository/run/attempt/head/workflow、artifact ID/name/size/digest/expiryをlive認証する。元oracle runのconclusionはfailureを要求する。追加diagnostic ZIPは実bytes/hashを照合してから展開し、重複entry、絶対/上位path、symlink、展開先外を拒否する。旧12親の型・pinsは継承しており、新たな算術を実行して受理し直すものではない。

original14-source receiptを元順序・canonical bytesで再構成して実2673-byte receiptと一致させ、新v2を加えた15-source/runtime/workflow/launch receiptは `repair-source-receipt.json` へ分ける。output/source.jsonと元source-receiptは変更せず、新source/workflowのコピーも `repair-source/` へ分ける。旧FAILとlogは `previous-checker-result.json` / `previous-checker.log` に保持し、新checker-resultの不存在から開始する。

保存outputは本便のfilesystem/byte監査でも **44 files、4 directories、5361492 bytes、reparseなし**だった。39個のmanifest列挙payload全部、4 stage manifests、top manifestのhashは一致した。workflowはコピー前後の全file length/hashと全output directory/file rosterをbaselineへ記録し、実checker後にもoriginとcompletionの両方をそのbaselineに対して照合する。新しい余剰file/空directoryも許可しない。元receiptや保持したcanary/logのbytesもこの不変照合に含まれる。外部checkerが元outputを書き換えたとの仮定で差分を受け入れる条件はない。

実行順は専用15-case serialization canary→新v2 checker一回である。旧metadata/旧成功canary、producer、cap/resumeを呼ばない。新checkerはcheckpointを持たないため全A–Dを再計算するが、元runで未完だった全stage/topのbyte比較を完了させるための一回である。内部1800秒、外40分、job60分。Python3.13.15/NumPy2.5.1に加え、元outputのfull Python version文字列とも一致させる。

最終gateはserialization/actual-checker両stepのsuccess、exit0、修理checker SHA、全8059 section等式・54433 chord・2 aux・全stage arrays flag、owner/start/result/manifestと各stage hash、rank/generation/state head/DERIVED rho2/direct pairing、元producer terminal/materializationとの一致を要求する。保存witnessのscalar/failed chordを数値literalの正解にしていない。PASS時だけ `completion-run-receipt` にcomplete A–D/full comparisonを記録し、candidate uploadもcheckerと不変gate成功後に限る。未完はINCOMPLETE receiptと失敗になり、diagnosticsはalwaysで保持する。元FAILや資源停止から非零/complete-zeroの受理を作らない。

F5. **最終固定値と判定範囲。** 作者から完成source/workflowの申告を受け、次の実bytes/hashを本便で確認した。両方LFのみ、BOMなし、最終LFあり。workflowのrepaired-checker byte/SHAはこのsourceと一致する。

| file | bytes | SHA256 | LF / CR |
|---|---:|---|---:|
| search/check_d972_r07_section_cochain_oracle_v2.py | 84402 | a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d | 1272 / 0 |
| .github/workflows/d972-r07-section-cochain-checker-completion-v1.yml | 44679 | b439c24229523daec90570f527a72a5bdc5c32f475fd3a1ad0361922a0cb60e8 | 704 / 0 |

この固定差分に未解消blockerはない。実装・workflowを実行したとのPASSではなく、新completion run/artifact、全配列一致、工房CV9はまだ未観測である。親裁定2131の七限定、旧F-fo-1の履歴、新ordinary27とdense対packed算術の保持TCB、source/P1/Conn前提は変更しない。新sourceの修理は旧origin scanの独立性欠如を遡及閉鎖しない。raw witnessの物理materialization、grade2 terminal、Task958同一語positive gate、full A0、Lean verifiedはpendingのまま。rootがrelease/GHAを担当し、本便の完了後は許可済みTask967へ戻る。

AUDIT_969_VERDICT: STATIC_SOURCE_WORKFLOW_PASS — u32-only repair and exact saved-output completion gates confirmed at final hashes; new full-array GHA/CV9 and materialization pending; historical F-fo-1 and parent2131 limits retained; verified=false.
