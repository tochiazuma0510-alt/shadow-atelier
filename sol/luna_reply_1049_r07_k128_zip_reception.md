Task1049 — k128 実artifact用 ZIP 受領器の限定移植

**F1. 最終pinと範囲。** Task1049（2077 B / SHA256 `e593546aa259f3f76fcaafbef7d9fa82457e2d896b75e621ed19073c6185d2ce`）と旧受領器全142行を読了し、指定新helperと本返信だけを作成した。新helperは `%TEMP%/shadow-atelier-audit163/extract-k128-v3-artifact.ps1`、**9632 B / SHA256 `1ce4ba4195bb69ce676711779cd57189f2b23240d142871ddf73b9b24a468444` / LF142 / CR0 / BOMなし / ASCII / 末尾LF**。このpinでfreezeする。新helper実行、Python/import/AST/GAP/数学計算・GHA/network/git/credential・新agentは使っていない。旧helper/source/WF/実artifact/旧返信は変更していない。

**F2. 全保持差分。** 基点 `%TEMP%/shadow-atelier-audit163/extract-k64-v2-artifact.ps1` は9632 B / `6de27467c19514bac8185515230ca1fff7d5071edb329ec0c232d3924fced40a` / LF142で、実bytes/SHAを照合した。変更対象は実131行の schema/run と実132行の head/workflow だけである。「末尾3行」のうち、133行の artifact ID/name 引数を変更せず、この2行で指定の移植が完了することをrootへ通知した。attempt=1は同じ値を保持する。

| 字段 | 旧値 | 新登録値 |
|---|---|---|
| schema | `d972.r07.fixed-lambda-cycle-batch.v2.root-acquisition.v1` | `d972.r07.fixed-lambda-cycle-batch.v3.root-acquisition.v1` |
| run / attempt | 34011731149 / 1 | 34023589045 / 1 |
| head | `c2a8a6acd60c0cd859edd2e262cfce074b3acaf1` | `794c5e9f883cb5ff21b2ee087c1d4baa84ac6760` |
| workflow ID | 351332190 | 351445840 |

新二行を旧二行へ逆置換した全source文字列は旧版と完全一致した。全差分を自己読了し、残る140行と全通常処理を保持した。`fc.exe` は長行折返しで表示行番号がずれるため、上の位置は実LF行による。追加修理を要する新所見はなく、新parser/general framework/cleanup/旧file上書きは加えていない。

**F3. 受領規則の保持。** 指定全pathはTEMP配下とし、全ancestorのreparse、既存の展開root/取得票/entry-pin票、展開root内の入力ZIP/取得票を拒否する。入力ZIPは全bytesと小文字64桁SHAをrootの実引数へ照合し、書き換えない。全entry inventoryを先に読み、相対path/空component/dot-dot/末尾dot・space/制御字/Windows予約名、重複・case衝突、fileとancestor directoryの衝突、UNIX/DOSの型、symlink/reparse、destination containmentを確認する。全entry上限1000000、長さoverflowと全展開分＋1 GiBの空き容量を確認してからfresh rootを作る。

通常fileと明示空directoryの両方で実streamをEOFまで読み、宣言長を越える/足りない場合を拒否し、全SHAを保存する。各fileをCreateNewで書き、flush後の実長と全再hashをstream hashへ比較する。末尾では全展開file数を再読し、実directory数・明示directory数を区別して記帳する。`$taskPins.ToArray()` を保持し、ZIP全pinと各entryのpath/type/bytes/SHAを別票へ残す。独立CRCを追加したとはせず、既存 `crc_independently_checked=false` のままである。

これは取得・輸送metadataの受領であり、P/Cの数学再演やartifact内容の意味的合格を与えない。candidate/diagnosticsのいずれも、同じmandatory実artifact引数と同じ受領規則で扱う。未生成のartifact ID/name/ZIP bytes/SHA、全展開数、新受領PASSを予告しない。run/attempt/head/workflowはTask1049がrootから登録した値で、LunaがAPI取得した値ではない。

**F4. 再現CLIの引数。** rootが実APIで完成artifactを観測し、全ZIPを取得した後に以下の7引数へ実値を渡す。ここでは値を埋めず、コマンドを実行しない。

| 引数 | rootが渡す実値 |
|---|---|
| `-ZipPath` | TEMP内の取得済みZIPの絶対path。展開rootの外。 |
| `-ZipBytes` | 取得対象ZIPの実全byte数。正のlong。 |
| `-ZipSha256` | 取得対象ZIPの実SHA256。`sha256:`なし、小文字64桁。 |
| `-ArtifactId` | 完成API tupleの正のartifact ID。 |
| `-ArtifactName` | 同tupleのartifact名。candidate/diagnosticsを実値どおり渡す。 |
| `-RootPath` | 未存在かつreparseのないTEMP内の展開directory。 |
| `-ReceiptPath` | 展開root外の未存在取得票path。さらに同path＋`.all-entry-pins.json`も未存在。 |

```powershell
$zipReceiver = Join-Path $env:TEMP 'shadow-atelier-audit163/extract-k128-v3-artifact.ps1'
if ((Get-FileHash -LiteralPath $zipReceiver -Algorithm SHA256).Hash.ToLowerInvariant() -cne '1ce4ba4195bb69ce676711779cd57189f2b23240d142871ddf73b9b24a468444') { throw 'ZIP receiver pin mismatch' }
# Root defines all seven variables below from the observed artifact and fresh TEMP paths.
& $zipReceiver -ZipPath $actualZipPath -ZipBytes $actualZipBytes -ZipSha256 $actualZipSha256 -ArtifactId $actualArtifactId -ArtifactName $actualArtifactName -RootPath $freshExtractionRoot -ReceiptPath $freshAcquisitionReceipt
```

取得票のexact字段は既存の schema/run/attempt/head/workflow、artifact={id,name}、zip={path,bytes,sha256}、extraction={root,zip_entries,files,directories,uncompressed_file_bytes} を保持する。entry-pin票のschemaは `root-complete-zip-entry-inventory.v1` のまま。rootが本全差分と本票を読んだ後だけ実受領する。新ZIP取得/展開数/実終了値/PASSは本票のfreeze時点で未観測である。

AUDIT_1049_VERDICT: STATIC_ZIP_RECEIVER_READY — 実末尾二行の登録metadataだけを移植し、全142行/全差分/全文逆置換一致を確認。上記新pinでfreeze、実artifact値は未設定、実受領はroot担当で未実行。
