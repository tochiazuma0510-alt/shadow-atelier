# Task1187 — 裁定2280のV9操作別計器・Task1184/1185/1186共通追補

宛先: Luna P担当 Pauli / C担当 Helmholtz / public driver担当 Noether。親brokerはrootのみ。数学宇宙・親21・k128/max1/no-refill・caps・C4 raw・P/C著者分離は既委嘱のまま。

## 正本と変更点

`ops/express/20260913_fable_astra_2280_erratum_adopted_instrument_replaced.md` を全文読む。2275の `parent_timing_complete` 新設委嘱は撤回された。V8に存在する受領証は保持し、新設したとの主張をしない。V9への置換要求は native-metadata 内側の「2回目以降の loads / canonical 再直列化 / sha256 / seal+ループ」の4区間である。数学判定の条件は変えない。

既に設計したPの6区間/Cの23区間と読込回数・バイト数は、包含区間および範囲説明として利用できる。これだけで2280を達成したとはしない。全runを再実行して計器を作ることはせず、同じ本走中の元操作を観測する。

## 独立実装と公開契約

P/Cはそれぞれ私有bodyから操作の境界を定義する。非再帰wrapperまたは既に許可された観測位置だけを用い、元の引数・戻り値のidentity・元の例外・元操作1回を保存する。旧数学領域を変更しない。計器の失敗が元の例外を置換したり受入拒否になったりしてはならない。

操作別時間はネストを説明して非重複にする。外側のnative-metadata時間と内側4区間を加算しない。2回目以降の判定単位（role/pathか同一rawか）・初回loads・read/IO・canonical内部・sha内部・seal+loop・未帰属部分を公開票に厳密に記す。読んでいない操作や失敗途中はnull/partialとし、全残差を測定根拠なくseal時間と命名しない。residualを使う場合は引いた区間と残る操作をそのまま列挙する。run間の係数やcap予測を数学gateにはしない。

各担当は短い公開案を先に固定し、元関数保存・caller・測定範囲・重複除去・失敗経路をrootが別読できるraw差分/保持票に結ぶ。公開serializer・型・順序・scopeだけをNoetherへ渡す。P/C相互やdriverへのprivate source共有は禁止。既存の指定返信ファイルに本追補を記録する（新しい返信ファイルは不要）。

Noetherは旧 `parent-timing-receipt.json` と新操作別票を区別して保存する。元stderr全bytes/native exit/source pinと対応付け、未観測を0にしない。P/Cの異なるscopeを強制一致させない。実測票が欠ける場合も診断の欠測として明示し、数学成功を計器の成功と混同しない。

## 閉鎖と発射

対象P/C/driver/WFのローカル実行・import・AST・compile・selftestは行わない。許可された静的metadataの編集/照合のみ。最終4source pins、独立別読票、marker/name、実formal5と派生registry、通常production key拒否の実fixtureを揃え、rootが既認可のnotify-and-goで配置・GHA実行する。今回の追補は受領済みV8の正式受領を再開しない。
