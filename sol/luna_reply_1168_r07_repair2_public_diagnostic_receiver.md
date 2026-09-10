Task1168 — repair2 公開診断 metadata 受領部品（静的納品）

F1. 現在版は `R/task1168/receive_current_diagnostics_v7_v3.py`、44977 B / `5dbc667b198ba293b9382c8c9bbf719173063fb718ee84641e982ae2dbe04dba`、702 LF、24関数。R は `%TEMP%/shadow-atelier-audit163`。指定署名 `receive_diagnostics(reader, p_contract, c_contract, context)` と既存 `current_metadata_common_v7` の Reader API に接続した。v1/v2 は不変の履歴として保存した。root の全文別読・1161全closure前の実行は行っていない。

F2. context は exact11: progress, selection, decisions, reductions, start, acceptance, invocations, final, producer_result, checker_result, actual_native。progress は指定13800 Bの公開部品の exact14戻り値。decisions は形成済みcandidate manifest配列、reductions は比較済み reduction.json 全配列であり、q+1のrowが先に形成されdecision未形成の場合も含む。invocations は実 `{value,pin}` 配列で pin.file は inventory の output/... 名。final は exact5の typed object/pin/presence。producer_result の非nullは callerの全48項目・closure比較完了を前件とし、保存resultがあるのに完了値が渡されないmain入場は拒否する。

共通公開署名も固定した。

`receive_batch_observation(reader, value, p_contract, context, *, sequence, require_admitted=False, allow_prediction_mismatch=False)`

これは producer_result を参照しない。Noether は自身公開source 14417 B / `9db42889b0f1dbc344ce9b3b0e10b18450fabdebdc922049d2b84c05c14cc1c2` の P result比較末尾に、実committed sequence / require_admitted=True / mismatch=False で接続したと報告した。そのsourceは本著者は再読・実行していない。共通関数は v2→v3 raw同一、offset13472 / 1380 B / `eb7e3850a18dcd9fac6cc6a443c3fdaa94ca698c4c70e876dd6804088c1f208f`。

F3. 旧snapshotは acceptanceだけでは過去startの値を取得できないため、rootが独立発行した公開8-keyを `p_contract['registered_previous_snapshot']` に追加する依存へ確定した。正本は `R/root-v7-old1962-observation-snapshot-v1.json` 2139 B / `4bcd09d6318df50fd36d170753deb7f4ca9bb766d82fa50b4f2501135190ad68` の /observation。root採択票は44899 B / `ad2c94dc23e7e129ac525c8acc691fb6e051838ccdea46f512aba3fc932d5581`。worker側で別pin/leaseへ束縛する。部品は現acceptanceの両親artifactと batch_anchor_v6.selection/old_oracle へ再joinする。P/C private sourceは不要であり開いていない。

F4. P保存診断の全29-keyを受領し、internal seal と whole canonical bytes/SHA を区別する。root/selection/invocation/final/HEAD のnullは後発file存在だけでは埋めない。無HEADならcheckpointと5countは全null。非nullなら実committed歴史HEAD<=qとその実checkpointへjoinし、q+1をcommittedへ入れない。親条件は両true/両nullだけで、未admittedなら後発qによらず未観測。selection/first decision の閾値3/9、実witness/scalar/decisionとのjoin、REJECTEDだけの予測不一致許容を実装した。両診断の新旧は推定せず、双方存在時の診断terminalはnullとする。

F5. C全50-keyの外側型と、各nullable観測・phase prefix・12-key tail・native/partial/terminal優先を接続した。root公開補足 `root-C7-public-assignment-order-supplement-v1.json` 3051 B / `d02d5f7a0dc57a8676d365984d64e93f59599d13a1c8074b4e6732b5e9422b8e` を参照した。Cのcounts/state/progressは現在q由来だけで、FAIL/UNKNOWN時は各fieldを別々にnullableとして照合する。qの存在だけでnonnullを強制しない。selection/rootの観測値は実保存・比較済みfileに条件付きで代入される境界を維持した。

完全比較済みresultがあればそのterminalを用いる。result無しではfinal/HEAD比較済みでも診断が優先し、final/tail観測と REJECTED/UNKNOWN_RESOURCE/null が併存できる。C自身のnative1/FAIL、native3/UNKNOWN_RESOURCEでは成功3flagをfalse、partialをtrueとし、既代入counts/hash/public_final/tailを消さない。native0/PASSの保存partial prefix比較も完全candidateと区別する。未知nativeはNoneのまま。P JSONへ durable_tail/result.partial/checkpoint terminal は追加しない。

F6. この部品のC受領主張は上記の診断projectionである。既存 checker_old_loader_regions の完全な公開certificate、input_preservation の実inventory/host acceptance照合、checker_source.file の実配置identity、全namespace/payload/lease closureは callerに残る。部品でもD3型とroot-public repair2 bytes/SHA、preservation exact9外側・true flagsを確認するが、既存nested本文を照合済みと称さない。返却値に `caller_retained_contract_obligations` を明示した。

F7. 納品材料（task1168内、既存版を上書きしていない）:

| 材料 | bytes | SHA-256 |
| --- | ---: | --- |
| receive_current_diagnostics_v7_v1.py | 7433 | e7bd1b7e422954c1e2f48914f4a329d760cc606ebc30cea32b0b9e62283c02d4 |
| receive_current_diagnostics_v7_v2.py | 21419 | 68e2c2b3cd144f576f60e0950619d64227f25793aa2df658ef0f5d842b0848f0 |
| receive_current_diagnostics_v7_v3.py | 44977 | 5dbc667b198ba293b9382c8c9bbf719173063fb718ee84641e982ae2dbe04dba |
| receiver-static-raw-boundaries-v1.json | 108657 | 32e8ac78dccb54a6a89f54b3d59d281fdd22714576ea598633341e8ebcd07be7 |
| receiver-interface-and-public-coverage-v1.json | 46291 | ef282e1693b18642ed2452aa3285e577f058525a5e692ff7e3a4141538d88b6b |
| author-material-manifest-v1.json | 1242 | 42488b02fade71ae8334987274b8e91e986280d2aab38db797f0c1c3799127ed |

raw票は全sourceの各function coreと全gapを分割し、現在版の全44977 Bを48領域で被覆した。最終占有行は end-exclusive の end-1 を用いた。作成/1→2/2→3の全raw正逆復元が一致した。v1の11関数は全raw同一、v2の共有18関数中17同一。変更共有関数は `_receive_p_diagnostic` のみで、same(set, set)をsorted keysetへ改め、歴史checkpointのcanonical実object照合を加えた。v2のset比較は静的自読で見つけた履歴上の不備であり、その版は実行していない。

F8. 指定公開11入力のfresh bytes/SHAは全一致。旧1150のmetadata helper5 sourceはAPI/raw参照だけで、body転用0。公開coverageはP29/C50の各fieldを重複なく割当て、12-tailと6/8/8/5 observation、16目的枝、依存interfaceを列挙した。これらは静的照合・目的記載であり、fixture/selftest実測ではない。

本便では receiver/P/C source の import・AST・compile・実行・selftest は全0。P/C数学private source参照0、数学再演算0、新agent/Git/GHA/network/credentials/既存PID操作0。metadataのraw/text/JSON/pin作業だけを行った。現runのnative値・artifactは本著者未受領でnullを維持し、数学判断・実PASS・root最終採択を発行しない。

AUDIT_1168_VERDICT: STATIC_PUBLIC_DIAGNOSTIC_SOURCE_READY_NOT_EXECUTED

F9. 公開補足v2後の最終版追記。現在版を v4 に更新した。v1～v3と既存の全納品票は保存したままである。

root は e188b0 で C の全5代入を再読し、公開補足 `R/root-C7-public-assignment-order-supplement-v2.json` 3089 B / `566ce130a91a54272802b89e68debea4ccb603bccbb2e2e6c9f8ea60ee0027b8` を発行した。template はnull、root_records直後は(-1, admitted=False)、saved parent-intake後は(-1, True)、selection/candidate callbackは(min(sequence,q), True)、progress.complete後は(q, True)。従ってFAIL/UNKNOWNで初期FalseやNone/3/9の代表段階を保持するv3の扱いは正しい。computed records.parent_intake と保存parent-intake fileの存在を同一視してはならない。PASSは最後の代入を必ず通るので batch_observation=null は不可能である。

v3にあった「PASS＋null の拒否をsaved parent-intake存在時だけに限定する」余分受入を1条件で修正した。`elif passed and _known_sha(reader, 'output/parent-intake.json') is not None:` を `elif passed:` にした。ほかの観測・失敗枝・共通署名を変更していない。C/P sourceは本著者は引き続き開かず、この公開補足とrootの明示裁定から実装した。

| 追加材料 | bytes | SHA-256 |
| --- | ---: | --- |
| receive_current_diagnostics_v7_v4.py | 44913 | b6cec7a55a9969f31cea1e793b7e16952b673f231ae7ec9403d6fbd6d6e72318 |
| receiver-static-raw-boundaries-v2.json | 19576 | 45f0dbae8cfc9b732d09adc270ed07ae349c457c2699dacc3a9ce699d7284ca8 |
| receiver-interface-and-public-coverage-v2.json | 47894 | 71fbc2b47e59dc6d23f620dec3a25b432650759db53b07d1f794f81d6ec6d000 |
| author-material-manifest-v2.json | 2005 | c87e295250cc5afdffe95891535a0eff6ba67b3e0b87517220dcac1c389a772d |

v3→v4 は offset40249 の64 B削除だけ。前40249 B・後4664 Bを保持し、全raw正逆復元が一致した。702 LF・24関数・48全域を保持し、共有24関数の23はraw同一。変更関数 `_checker_projection` は offset33780 / 8606 B / `ac151fc88703666c5d5b5da5eba46809ef05cd41e503cc2d6045150fd6b7460c`。共通 `receive_batch_observation` の raw/署名は保持し、Noetherへ最終v4 pinを直接共有した。

F10. 最新coverageはv4の全範囲pinと補足v2依存へ更新し、PASS＋null拒否を加えた17目的枝を記載した。最新manifestは9材料342402 Bを束縛する。source実行/import/AST/compile/selftestは依然全0、実native/artifact未受領のnullを維持する。旧判定行は履歴として残し、現在の納品版はv4である。

AUDIT_1168_VERDICT: STATIC_PUBLIC_DIAGNOSTIC_V4_SOURCE_READY_NOT_EXECUTED
