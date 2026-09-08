# Task1132 — Q1450 の公開作業報告 wire を具体化（Luna／公開設計）

rootからの限定委嘱。正式1112のinventory5 handbackと1108/1127最終bindingが最優先であり、本票はv6追加gateを作らない。1127 v2/14位置、P/C current source、実親、全cap、過去票を変更しない。

## 必読・入力範囲

事前登録のbytes/SHAを固定してから読む。公開材料だけを許可する。P/C私的source・raw監査票・私的返信・full runner/driver本文は不読。

- %TEMP%/shadow-atelier-audit163/root-Q1450-adopted-historical-clause-v1.md（6722 / ba94c0ca4341639889ca1166a72e397851bbb3d4f63dc885d05ac0fa518b6622）
- 同 root-Q1450-exact-pairing-citation-lemma-v1.md
- 同 root-current-observable-and-citation-cut-lemma-v1.md
- 同 task1129/public-Q1450-query-result-effect-contract-v2.md（15514 / 888f4e6c690f459c31972869ebd242c604a2970bb3383a0314f31659c3a371f2）
- 同 task1130/public-Q1450-exact-query-result-effect-contract-v1.md（10176 / db94d86cfea59bba5831350d3437b05a723428fbeaa2757d6e359b09a87f31a2）
- 同 task1115/public-type-and-consumer-delta-v3.json、task1121/public-wire-parameter-basis-v2.json。既採択型のscope/名前を確認し、非正文family概要をscopeの代用にしない。
- 既に1131で保持した公開採択限定とown資料は参照可能。現v220/返信163全文は読まなくてよい。

## 目的と固定判断

両公開contractが未閉とする「過去の実作業／今回Pの申告／今回Cの実作業」を混同しない **一つの具体的なversioned公開wire候補** を出す。抽象的な必要事項一覧で止めず、record/field/型/主体/成立条件/reader/旧字段との対応を全定義する。実装はしない。

固定条件:
1. Q1450の数学対象行数と、現在実に完了したrow検査・row-dot・target-dot・引用適用を別々にする。P/Cを別の所有者・別実行ID/source/runtime/queryへ結ぶ。
2. 保存済み歴史start/intake/timing（旧exact10字段等）は改変しない。新wireを既過去recordへ挿入して過去shaを改変しない。候補が現在recordをversion upする場合は原record/readerへの影響を公開contractの射程で列挙する。
3. 現P packetの正しさをCが認証することと、C自身が算術を再実行したことを分離する。Cだけ引用/Pだけ引用/両方直接/両方引用を同じowner規則で表す。相手の件数を自身の行為へ転記しない。
4. 全成功時だけでなく、途中の欠品・拒否・resource停止・target片側到達など、観測できる最小事実を扱う。未知値を0へしない。予定件数や数式上の件数は実測ではない。同cap/同ordinal/同時刻は保証しない。
5. Q1–Q3の過去測定条項の引用元と、今回の同一入力/Γ/TCB/effect適用義務を別にする。完全AcceptedClaim/Γが完成したとしない。global shared helperの全呼出しをcited扱いにしない。
6. source/runtime/実時間等のbindを循環させず、writer/readerの順序とself-referenceの有無を明記。fieldsを増やす理由と消費先を示す。不要な将来機能は足さない。
7. 既public型のnamespaceを無断で流用せず、draftとしてversionとstatusを明示する。値を埋めた偽run receiptではなく、型の定義と紙上scenario表にする。

納品:
- 公開wire draft（JSON/Markdownどちらでもよい。型、全record/field、必要な共通制約）
- 独立したproducer/consumerイベントの順序と、少なくとも上記4成功組合せ＋途中停止/欠品の紙上case表。実数値/実行結果と表示しない。
- 既公開contractとの全字段対応、閉じた設計判断と残る実装/適用義務。現在のintake/hash/sourceを書き換えない。
- 最終入力保全・材料目録・全本文自己読了。
- 返信 sol/luna_reply_1132_r07_Q1450_public_work_report_wire_v1.md。最終行 TASK1132_VERDICT:。
作業は指定返信と%TEMP%/shadow-atelier-audit163/task1132/の新規版だけ。実装、P/C/helper/Python/数学/source実行、自己試験、親/process/Git/GHA/credential操作は0。metadata JSON/本文/bytes/SHAのPS/.NET照合だけを許可。数値主張や費用推定を新たに作らない。
