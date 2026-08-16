# D972 dovetail-v2 calibration failure audit (v1)

## 判定

run `31943735532` の calibration 失敗は再現可能な数学的判定ではなく、
独立 GAP 子プロセスの実行失敗を `UNKNOWN` に落としたものだ。現在の
`31954113424` (head `a422175b3b66b91dfbd54188e5b7688569b6936e`) も、同じ
本命 v2 の step 12 を実行している限り、同じ失敗様式を再び不可視にする。

根本原因は二つある。

1. 本命 v2 は旧 inline calibration を呼ぶ。別 workflow/helper の
   ``d972_calibration_diagnostic_v4.py`` にある fresh/fixed calibration は
   `d972-dovetail-v2.yml` の step 12 に配線されていない。
2. v2 の GAP wrapper は非零終了時に stdout/stderr と生成 script を捨てる。
   したがって実際の GAP のエラー行を観測できず、失敗 receipt も artifact に
   残らない。

これは Norm/KBMAG の既知 bug に依存する失敗ではない。calibration script は
有限 permutation/group、free presentation、homomorphism/bijection checks の
構築であり、該当 block に `Norm`/`KBMAG` 呼出しはない。

## 実行・artifact の事実

read-only `gh run view` と Actions artifact API の結果は次の通り。

| run | head | step 12 | artifact |
|---|---|---|---|
| `31943735532` | `c1a0b91fc25604cd8599da949b7f1e9508c38b54` | 2026-08-16 11:14:46Z--13:44:27Z, failure | `total_count=0` |
| `31954113424` | `a422175b3b66b91dfbd54188e5b7688569b6936e` | 2026-08-16 14:56:53Z から in progress | `total_count=0` (実行中) |

終了 run のログに残ったのは以下だけである。

```text
STATE_STOP independent k=1,2 lossless calibration reconstruction UNKNOWN: GAP failed with exit 1
CALIBRATION_PENDING 2f2f23be0f053b81bffb0e4687c5df16386de24d9a58720dcce4de9608ae82d5
```

`d972-dovetail-v2.yml:566-574` の state upload は
`steps.campaign.outcome == 'success'` 限定である。従って step 12 が失敗すると、
後段に receipt を作れてもこの run からは回収できない。

## 失敗経路と再発理由

本命経路は

```text
d972-dovetail-v2.yml:484-488
  -> d972_dovetail_producer_v2.py:686,712
  -> check_d972_dovetail_v2.py:1101-1140
  -> independently_check_calibration_v2():1144-1158
  -> independent_calibration_gap_script():312-440
```

旧 calibration の疑わしい presentation/base 接続は
`search/check_d972_dovetail_v2.py:438-440` の次である。

```gap
FQ:=FreeGroup(2,"r");; Q:=FQ/MakeRels(FQ,{qrels});;
qg:=GeneratorsOfGroup(Q);;
qToBase:=GroupHomomorphismByImages(Q,BQ,qg,[bs1,bs2]);;
if qToBase=fail or not IsBijective(qToBase) then
  Error("calibration presentation/base mismatch");
fi;
```

ただし、保存された stderr が無いため、ここが今回の exit 1 の正確な GAP
行だとは断定しない。`qToBase`、直前の `Size(BQ)`/presentation checks、または
後続の scan のどれでもあり得る。

wrapper (`search/check_d972_dovetail_v2.py:1110-1138`) は script を tempfile に
書いて `subprocess.run(..., capture_output=True, text=True)` するが、成功時以外
は `completed.stdout`/`completed.stderr` を保存せず、`finally` (`:1130-1134`)
で script を unlink する。その後 `:1135-1137` の generic な
`GAP failed with exit <n>` だけを投げる。さらにこの例外は
`parse_independent_calibration` (`:1155`) より前なので、正常 calibration
receipt に包む機会もない。この構造が run 319437 の opaque failure を生み、
同じ旧経路を使う run 319541 でも再発を予想させる。

## v4 との差と最小修理案

`search/d972_calibration_diagnostic_v4.py:73-100` の `FIXED_QTOBASE` は、
free generators から normal subgroup と natural quotient を明示的に作り、
各 relator の base image、generator image、order/surjectivity/bijection を
段階的に検査する。`run_frozen_base_presentation` (`:258-312`) は bounded
stdout/stderr と SHA/byte 数を receipt に保持する。これは診断としての最小の
意味修理候補だが、v4 workflow は本命 v2 step 12 の呼出し先ではない。

workflow をこの監査では変更しない。次に必要な versioned 修理は、次のどちらか
である。

* 本命 v2 の calibration block を v4 の固定 block と同じ explicit quotient
  construction に置換する。
* 置換前に、失敗を常に独立 receipt にする。少なくとも generated script の
  SHA-256/bytes、実行 mode と安全な argv、return code、stdout/stderr の
  bytes/SHA、bounded tail (例えば各 4096 bytes)、stage marker を
  `checker-out-dir` に atomic write し、正常 receipt と同じ frozen manifest/
  ルート digest に bind する。失敗時は依然 `UNKNOWN`/`STATE_STOP` とし、
  `finally` で script を消す前に receipt を確定する。

後者だけでも次 run で正確な GAP 行を特定できる。前者だけで診断情報を残さ
なければ、別の後続行で落ちた場合に再び同じ opaque exit 1 になる。逆に診断
receipt を足しても A/B への昇格は起こしてはならない。

別 workflow の fresh v4 を試す場合は、`target_keys` の source fix を含む
最新 commit（`7bee3bec` 以降）を使うこと。a422 時点の fresh helper は
`canonical_target_keys` の source が後に修正された履歴があるため、a422 の
古い helper をそのまま「修理済み」と扱わない。

## 結論

`31943735532` と進行中の `31954113424` は、972 の A/B、あるいは calibration
数学の失敗を決着していない。確定しているのは「旧 v2 inline GAP lane が exit
1 を返し、wrapper/workflow が原因証拠を破棄して UNKNOWN にした」ことだけで
ある。GAP stderr/script SHA を保存した versioned diagnostic を先に入れ、
その receipt で exact failing stage を特定してから、v4 の explicit quotient
修理を本命 lane に統合するのが最短の安全な次手である。

監査は read-only `gh`/静的ソース確認のみで実施し、ローカル GAP、重い計算、
workflow変更、commit/push/dispatch は行っていない。

## Versioned 修理 (実装済み)

上記の最小修理を `search/check_d972_dovetail_v2.py` に実装した。workflow YAML、
producer、worker は変更していない。

* `independent_calibration_gap_script()` の旧
  `Q:=FQ/MakeRels(...); qg:=GeneratorsOfGroup(Q)` block を、
  `FQgens` の固定順、`NormalClosure`/`NaturalHomomorphismByNormalSubgroup`、
  relator の `freeToBase` identity、quotient/base order、surjectivity、
  bijectivity を含む explicit block に置換した。生成 script に旧 block や
  `{qrels}` placeholder が残らないことを self-test で拒否する。
* v2 の `--out-dir` を adapter に渡し、非零 GAP 終了（および command/select
  error）の前に `d972-independent-calibration-failure-v1.json` を
  `atomic_json` で保存する。receipt は schema/status/stage/purpose、return
  code、safe argv、script bytes/SHA-256、stdout/stderr bytes/SHA-256、各
  bounded 4096-byte tail、tail truncation、receipt SHA-256 を含む。
* 失敗時の `STATE_STOP` に stage、receipt path、stdout/stderr tail も含めるため、
  workflow が失敗 artifact を upload しない場合でも Actions log から exact
  GAP stage/error を追跡できる。失敗は引き続き UNKNOWN であり、A/B へ昇格しない。

静的/self-test 結果:

```text
python -m py_compile search/check_d972_dovetail_v2.py       PASS
python search/check_d972_dovetail_v2.py --self-test          PASS
mocked nonzero subprocess receipt fixture                   PASS
git diff --check -- search/check_d972_dovetail_v2.py         PASS
```

実装後 checker SHA-256 は
`63C04A6B980F1597601F8319DA129BE0D3F124E67833D04FF7E768043C1BB77B`。
ローカル GAP/重計算、commit/push/dispatch は行っていない。
