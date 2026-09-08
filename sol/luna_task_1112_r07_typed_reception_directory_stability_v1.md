# Task1112 — typed reception の directory 安定化と失敗 journal

宛先: Luna / packet_bounds_audit。Sol は裁定・独立静読、Luna は TEMP 内の metadata 実装を担当する。1108 の保存済草案を保持し、この受領障害を優先して限定作業する。新 agent、Git、credential、network dispatch は使わない。返信は `sol/luna_reply_1112_r07_typed_reception_directory_stability_v1.md`、最終行 `TASK1112_VERDICT:`。

## 出発点と不変条件

1105 実 child PID13580 は 8203.0273376 秒後 exit1。receiver は 517161 B / `485b28d048ce3265814a532bbd679719e62ee9374cf29170d61b20c4f09b93e6`。`Inventory` の missing-directory は L3455 または L381 で、実 callsite と欠損主体は UNKNOWN。40 mkdir の直後存在と、後続の v3/v4/v5 欠損32/34/36は異なる観測である。既診断票 6201 B / `425367764d90b9b8a059c67f68c4eba0da9de113b2881a2ebd588a66d8dc56fe` と JSON65742 B / `21a75ef146dc931a0c09c6e57e731064dc3c0a17e9df969223b5ca69d1f7bf8f` を引き継ぐ。

全歴史親、全 file/byte/hash、全 ZIP entry/EOF、全 typed key/path/schema、全登録 directory と fixture を保持する。既受領票で本文を省略しない。途中 mkdir で不足を隠して PASS にしない。新 source は別名、旧 source・票は凍結。数学の実行・import・AST・compile・selftestは禁止。以下の小対照は Windows filesystem metadata だけである。

## 今回許可する作業

1. `%TEMP%/shadow-atelier-audit163/task1112/` の新規一意ディレクトリに限り、ASCII PowerShell と必要最小限の Win32 interop による directory handle の小対照を設計・実行する。親 artifact や既存 receiver は変更・起動しない。対照用自作の空 directory だけに非再帰の delete/rename を試し、各操作の絶対 source/destination が一意対照 root 内にあることを直前確認する。成功時・失敗時の Win32 code、時刻、handle 解放を保存する。既存プロセスの停止は禁止。
2. 第一候補は `CreateFileW` の `OPEN_EXISTING` と `FILE_FLAG_BACKUP_SEMANTICS` により directory を開き、read/write sharing を許し delete sharing を与えない非継承 handle を受領期間保持する方法である。desired access の選択、reparse 拒否、取得失敗、親から子への取得順、finally 解放、全件取得を確定してから本受領へ進む条件を明記する。Microsoft 一次資料: [CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)、[RemoveDirectoryW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-removedirectoryw)。文書上、delete sharing を省くと後続 delete-access open を拒否し、delete access は rename にも使う。これは同 OS 上の小対照で確認する仮説であり、実欠損主体の同定ではない。
3. 対照は保持中の通常 read/enumeration、empty child の delete と rename 拒否、ancestor 保持、既に競合 handle がある場合の取得失敗、解放後の正常動作を含める。ディレクトリ handle は file 内容の不変性や全 OS 操作への無条件耐性を保証しない。全内容照合は従来どおり必要。保持方式が実際に成立しなければ UNKNOWN を返し、対照結果だけで親へ適用しない。
4. 対照が成立したら新 TEMP 版の修正案を作る。既認証された空 directory 復元手順を本受領の前に別フェーズとして結び、v3/v4/v5 の全登録 directory と各 root/必要 ancestor を保持してから、同一全 scope の本受領を実行する構成を優先する。親 namespace を実変更する段階は root が別途静読採択して実行する。worker が親の復元、全走査、handle 適用、本受領の再 launch を行うことは今回の許可に含まない。
5. 新診断は Inventory/ZIP の重い読取りの前後に全登録 directory 存在を確認し、入力外の append-only journal に親 role・絶対 base・相対名・呼出 site/callstack・UTC・段階・最初の欠名を残す。完了イベントは成功後のみ。全 scope は保持し、旧判定式を緩めない。失敗時も journal と source pin を回収し、typed PASS とは別票にする。全 source の前後 raw 差分、追加部、変更部、残存全関数/全行範囲の結合票を渡す。
6. 既存 launcher の子を実際に再実行する前に、root の独立静読用に argv、source/full delta、対照の生結果、復元対象の由来と件数、保持範囲、journal/receipt 出力先、例外時の解放と終了契約を提出する。root の静読は既存研究者認可内の内部手順であり、新たな研究者確認は要求しない。

成果の状態は「metadata 小対照済み / 静的採択待ち」で止める。full typed receipt と formal inventory5 は実本受領が完了するまで NULL。1834/8539 の既存 GHA 数学格付けは cross-checked limited7 のまま、verified=false。1108 はこの草案配達後に再開できるよう、未完部分を明記する。
