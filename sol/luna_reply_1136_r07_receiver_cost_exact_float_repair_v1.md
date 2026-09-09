# Task1136 返書 — cost の Decimal→binary64 修理

Luna / 2026-09-09。委嘱全文を読み、限定された metadata 修理を完了した。最終案は `review-snapshot-v2` の receiver **cost-v5**。全 receiver の実行・Git/GHA・P/C source の import/実行・vector 読取は行っていない。以下の TEMP 相対名はすべて `%TEMP%/shadow-atelier-audit163/task1136/` 基準。

## F1. 実失敗の原因

旧 R4057 が最初に拒否した項目は `producer_selection`。元 JSON の `11.831757000000001` は `ConvertFrom-Json` により値を保った `System.Decimal` になるが、旧 `CostNumberV5` の `[double]$value` は `4027a9dc0db2702a` へ変換した。実3入力を旧 `CostPartialSumV5` で合計した値と Python `math.fsum` はともに `4027a9dc0db2702b`。旧受領は両辺を double 化した後に厳密比較するため拒否した。

| 項目 | 元 JSON spelling | 旧 cast bits | Python / 最終案 bits |
|---|---|---|---|
| selection aggregate | `11.831757000000001` | `4027a9dc0db2702a` | `4027a9dc0db2702b` |
| candidate phase aggregate | `1411.6453159999999` | `40960e94cdb7ae58` | `40960e94cdb7ae57` |
| checker total input | `2041.4255092800001` | `409fe5b3b8b466fa` | `409fe5b3b8b466fb` |
| checker harness input | `2042.3296421820003` | `409fe9518db85c4c` | `409fe9518db85c4b` |

旧実 comparator の再現では13対象中2拒否。checker total は旧変換の誤りが左右で一致するため拒否せず、harness の時間は独立入力であって P residual の減算項ではない。保存 receipt 自体の不整合、集約順序、配列引数の崩れ、数学的失敗とは判定しない。

初期 `inspect-actual-cost-v1.ps1` の `exact_equal` は Decimal 左辺と Double 右辺の暗黙比較だった。その表示値は旧 receiver の判定再現として使用しない。最終 `bounded-cost-controls-v3.ps1` は実 `SameCostNumberV5` 本文を呼び、この点を明示して supersede した。

## F2. 保存 writer の契約と棄却した案

実保存 `driver.py` は 1145223 B / `f1b50bc529f08ad8654d775e2fce652334dfa8b325d3d2bcc27286aa09cb3f98`。D963 の六 phase 順、D5469–5523 の JSON 読書き、D9011–9100 の cost 照合、D9703–9884 の writer を読んだ。六 phase、selection、phase total、signed residual、P+C は `math.fsum` を使い、D9094 は保存値と再計算値の canonical bytes を比較する。誤差許容・負値 clamp・想定秒数 gate はない。

Decimal の invariant string を `Double.Parse` へ渡す一行案 cost-v4 は棄却した。13集約は通る一方、全776入力の照合で `000047/e/source` の `0.323296` と `000070/e/primal` の `2.397702` が各1 ulpずれた。`review-snapshot-v1` と `bounded-cost-controls-v2.json` の `FAIL_CONTROLS` を保持した。値別例外や項目除外は導入していない。

## F3. 最終 cost-v5

Decimal の符号、96-bit整数係数 N、scale s を `decimal.GetBits` から取り出し、正確な N/10^s を BigInteger で正規化する。整数 `DivRem` の商と余りで最も近い binary64 を選び、ちょうど中点なら偶数仮数を選ぶ。carry 後に exponent/fraction/sign を組み立てる。Decimal の非零値の絶対値は 10^-28 以上、2^96 未満なので、丸め後指数は -94…96 内にあり、正常値領域に収まる。零では符号 bit を維持する。

この説明は Decimal の実値と .NET の整数演算・bit 操作の意味を前提とする。任意 JSON が初めからその Decimal 値へ損失なく読まれること、任意 .NET/Python 版での同一性、一般の `math.fsum` 等価性の証明へ拡張しない。実776入力については元 JSON spelling、実 PS 型・Decimal 表現、旧/新 bits、独立 Python bits をすべて結んだ。

変更は旧 R3875 の前に33行の helper を挿入し、旧 R3877 の変換一行を置換するだけ。`J`、`Same`、`PlainInt`、`CostPartialSumV5`、`SameCostNumberV5`、R3991 の source scalar 型・値比較は不変。R3952/3953、R3991、R4054/4055、sum 入力、比較両辺という全 caller を確認した。R4014 の prior `232.786064` は元と同じ `allowNegative=false` で対照した。

| 最終材料 | bytes | SHA-256 |
|---|---:|---|
| `review-snapshot-v2/receiver/root-review-receiver-v5-directory-stability-cost-v5.ps1` | 527244 | `d4ca12668c334c4668f02f4aae795ab85fbd4c5d0ced9cee39d29d809a28199d` |
| `review-snapshot-v2/root-directory-stability-broker-cost-v5.ps1` | 18559 | `9533acd02b95d89ba5dd71a40c4ed724fcb050c90f5397ea7c14ae0c84fddd42` |
| `review-snapshot-v2/proposal-runtime-closure-v1.json` | 3905 | `9cd6f268be52a67a4a1728a3d3acaba80cc16a301e13847e5704c1e88feaf310` |
| `cost-decimal-binary64-helper-v1.ps1` | 2739 | `20da16c397c3e27b052eff2de5d93337968bbfc5dcb1a888dafc68702c02dd1a` |
| `cost-metadata-helpers-repair-v2.ps1` | 8542 | `e354be1fcfe8b6b1cdba97af362acbaeead101404c1fcd3cd2c6217686dda2ab` |

14 runtime のうち receiver 以外13は raw bytes 同一。broker は receiver 名の2置換だけ。root activation flag は変更しなかった。親、caps、batch/no-refill、C4、著者分離、全ファイル/ZIP/hash/typed/directory-lease/finally の gate は保持した。

## F4. 限定対照と保持票

`bounded-cost-controls-v3.json` = 2714859 B / `1a4f6fbf2e3f1183322bd00fded1d601e48de685eb22a15e42f51eb535085a86`、結果 `PASS_REGISTERED_METADATA_CONTROLS_ONLY`。実776入力と13集約/残差の Python bits 差0、実 comparator の拒否0。numeric 27例（必須24＋明示した limit probe 3）、sum 17例、比較8例、変造17例を記録した。

null と零、bool/string/nonfinite、負 duration と正当な負 residual、空/単一/複数入力、相殺、中点の偶数丸め、Decimal 最小単位/最大値、signed zero を分離した。1 ulp変造13件と入力変更・欠落・残差符号変更4件はすべて拒否。負 residual の実対照値 -8 を保持し、±0 の数値比較は元契約どおり同一視する。3 limit probe が通ったことは一般 decoder の保証ではない。

実行は `bounded-cost-controls-v3.ps1 -TaskRoot <task1136>`。新しい出力を作る仕様なので、既存結果の上書きを目的とした再実行はしない。実 native host exit0 は tool chunk `4d0b6f`、所要6.6227758秒、PowerShell `5.1.19041.6456` / framework `4.0.30319.42000`。Python oracle は project source を import せず、子 process の環境を空にして必要な非秘密キーだけを渡した。

観測した追加 native TCB は `System.Numerics, Version=4.0.0.0`、`C:/WINDOWS/Microsoft.Net/assembly/GAC_MSIL/System.Numerics/v4.0_4.0.0.0__b77a5c561934e089/System.Numerics.dll`、133976 B / `bda8cbe437f30610d84980aeb3a048341cb215b24a588217de7fc99765a618c9`。これは実環境の来歴であり、一般的な platform 保証ではない。

`final-author-handback-v1.json` = 21922 B / `10a3024017a4d81f0780935f3edad36aade2f49702a9460d5158974b389d2064`。最終時点で初期6＋named1563＋template/library3 の各登録 pin を順に再照合し、すべて不変。named1563 は driver1、runtime14、cost source776、manifest772。再帰的 parent scan・parent 書換えは0。source 全文の順逆 raw 結合と実変更 byte ranges、14/13、実行来歴を同票に収蔵した。

receiver の byte offset は旧433157に2739 B挿入、旧433377の27 Bを新436116の87 Bへ置換。broker は旧6164/9866の57 B名を新6164/9864の55 B名へ置換。残りの prefix/middle/suffix は物理 EOF まで完全一致する。

## F5. handoff の境界

root は別読票 `root-task1136-source-and-controls-review-v1.json` により source/controls を採択し、同じ v5 を新 session で全受領へ起動したと通知した。私自身は全 receiver を起動していない。起動済みなので、root の指示に従い新しい承認案・追加試験は形成しない。未実行の整形用 `form-final-metadata-handback-v1.ps1` は来歴として残す。

小対照は全受領の代替ではない。typed receipt、formal inventory5、全受領の最終 PASS はこの返書で主張しない。A0 数学結果、v6 本走結果、verified の昇格もない。

TASK1136_VERDICT: 条件付き GO — cost-only 修理と限定 metadata 対照・保持票は完了。全受領の結末は root の実票に従う。
