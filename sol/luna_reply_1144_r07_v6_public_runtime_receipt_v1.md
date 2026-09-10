Task1144 の公開 metadata 限定受領を完了。実行 run34416548935/1、head `866c87eaec6bca55d2578906c0f338cb34582373` に対する結果は `PASS_BOUNDED_PUBLIC_METADATA_ONLY`。新たな数学判定・CV-9 採択・正式 parent 受領・formal 5 fields の発行ではない。

`receive_public_runtime_v2.py` は native exit 0、tool `2b3209`、4.8253959 秒で終了した。明示登録した 1664 metadata ファイル / 40168797 B を、root 全 member 目録と fresh bytes/SHA で結合。親 payload の再 hash、元 driver/P/C の実行・import/AST、GHA/Git、ディレクトリ復元は行っていない。

実票から、選択128・処理128・新規行128・従属0、rank1962、generation8667、`BATCH_COMPLETE_CANDIDATE` を P/C・HEAD・最終 manifest・run 票間で照合した。acceptance は実9キー・18親の順序と全 tuple、元64段と native v3/v4/v5 の別 schema、親128/256/384行を維持。登録上限は k128/max_batches1/no-refill、P5400/C10800秒、外側6000/11400秒、RSS7168MiB、selftest300/360秒、job330分のまま。

P/C の開始・終了票、raw終了コード `0\n`、stdout/result同一性、stderrの全pinを照合。自己試験の実5群は P の拒否数 `[30,10,6,7,8]`、C は `[28,9,6,7,8]`、既存 metadata 対照16件。旧数学 success suites の再走は0。

cost は全776入力の実JSON値・pin と772 phase manifestを照合し、exact `math.fsum` を再計算した。P1755.57352秒、C2073.026045804秒、合計3828.599565804秒、P残差327.0346219999999秒。誤差許容・丸めによる一致・負残差の clamp は導入していない。timing は43外側区間と、P stderr 674986 B / 10363行 / 26完了イベント、C stderr1186347 B / 17278行 / 31完了イベントを全行照合。到着時刻による内側時間の推定や包含区間の合算はない。

成果物は `%TEMP%/shadow-atelier-audit163/task1144/` 以下。

| ファイル | bytes | SHA256 |
|---|---:|---|
| public-runtime-metadata-contract-v1.json | 55876 | a49450b32c736143e34c9d0e2653ab26b49f111f231a81dd8778efc616bada85 |
| receive_public_runtime_v2.py | 67565 | 37dbc6cb83bac148aca9445e8893707a1ed98d8cb1c5114240fdaeebc7a427fd |
| runtime-receiver-input-contract-v1.json | 4458 | ac7410b02c72b096f9b590800439600f5bcd8a4667e853abbb7c63da24629d3b |
| actual-public-runtime-inputs-v1.json | 608944 | 7ca163f208d5b3ad26d30f050c66c284255855c649ddd0ac06fdaa87a174e928 |
| bounded-public-runtime-reception-v2.json | 1364865 | 32789deeef490b688ee9156ae869f9c8e4510b3a9abff96b03739139f6803729 |
| small-metadata-rejection-controls-v1.json | 4063 | 304bbfb6f1ef511f9f671be0f3ec4b66e9dbeb8081e63f9fa3113d7784427ef8 |
| actual-bounded-reception-handback-v1.json | 6939 | cb1c8f2e4c59cbcb8e21707c531770d60afe05b34da1933a1ea54f3fa1ce5b88 |

拒否対照は重複キー、非有限値、指数overflow、bool-as-int/seconds、unknown/missing keys、型coercion、path/ancestor/casefold異常、実metadataのbyte/SHA不一致など19件が拒否、同一pin等2件が受理。native exit0、tool `6016a7`。Luna側 metadata runtime は Python3.13.14 / Windows10、GHAの登録 runtime は Python3.13.15 / NumPy2.5.1であり、同一runtimeとの主張はしていない。

初回 v1 は source比較票の提示順をcurrent ordinal順と誤って仮定したため exit1 (`24d4a9`)。PASS票を形成していない。原driver R5971–5992 は registry順を保持し、旧156/140区間対応後に追加21/25区間を並べる。v2は旧・current双方のordinal完全被覆と重複なしを照合した。acceptance-receipt は実21キー（短報の23は転記誤り）、source-beforeのschemaも明示照合済み。

`exact_keysets_checked` は `read(shape)` で記帳した82票の表で、追加の手動 `keys()` 対照を全列挙した表ではない。公開wire20種類は契約に登録したが、全JSONを再帰的に網羅したexact-key監査とは称さない。5059個の descriptor は保存REPORT inventoryとの一致のみでpayloadは開いていない。source区間177/165・retention57・old-loader8等は公開結果metadataを照合し、raw source/range採択はrootが担当する。private progress/checkpoint・invocationの意味、vector/pairing/character計算、全fixture/親/元sourceの再走は範囲外として実票に列挙した。

ZIP省略44ディレクトリ（fixture40、拒否control等4）の物理的存在・復元をこの限定票から推定しない。`formal_parent_reception=false`、`root_adoption_established=false`、Luna自身の `candidate/cross_checked/verified=false` を維持する。前の正式v5受領の再走は不要であり、実施していない。

TASK1144_VERDICT: PASS_BOUNDED_PUBLIC_METADATA_ONLY; ACTUAL_EXIT_ZERO; ROOT_MATHEMATICAL_AND_FULL_SCOPE_ADOPTION_SEPARATE
