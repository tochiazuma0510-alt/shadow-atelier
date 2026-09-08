# Task1108 / 1109 / 1110 公開追補 — 裁定2227 親別時間計器 v1

宛先: 1108外側作者、1109 P作者、1110独立C作者。元taskの静的実装範囲を、裁定2227の親別時間計器へ延長する。実数学・source import/AST/compile/selftestのローカル実行は0、Git/GHAはrootのみ。共通の本紙と公開serializerだけを共有し、私的P/C body/helperは共有しない。v6は18親/k128/同caps/一batchを保持する。

F1. 観測対象と限界

rootはPの既admitted-parentイベントが全親inventory照合ループの末尾で発火し、三つのnative batch認証callはそのループの後にあることを全文静読した。したがってadmitted-parent間隔だけではnative層の再認証時間を測れない。C側は同じイベントがあると仮定しない。次run一標本の秒からbyte/file/層/候補rankの因果係数を同定したとはしない。

driverだけが出す取得/展開/外側intakeの時間と、P/C内部の親inventory/型解釈/保存metadata/状態復元とpairingの時間を区別する。子stderrへの外側ポーリング到着時刻を、内部処理の正確な開始/終了時刻へ改名しない。

F2. P/Cの最小時間計器（各作者が独立実装）

保持数学kernel/旧loader本体のraw不変を保ち、既に変更対象である通常callerの境界へtime.monotonicによる開始/終了の観測を加える。既P admitted-parentの一呼出にelapsed_seconds/file_bytes等の実観測を足すことは可。同じ公開契約の追加完了イベントを独立helperで作る場合、元の数学値・seal・戻り値・例外・deadline判定を変えない。新たな数値replayや二度目のinventory/JSON全走査を計器のために行わない。

共通公開完了イベントはplain JSON lineとしてstderrへ出す。候補API/出力result/C-result/start/intake/diagnostic等の公開keysetへ計測fieldを混入させない。最低限の情報: schema、side(P/C)、stage、role、ordinal、elapsed_seconds。必要なfiles/file_bytes/rows/recordsは既処理で実観測した値だけを追加し、未観測はnull。各作者はexact keyset・stage列挙・開始/終了のsource位置・inclusive/nested関係・成功時だけ出るかを公開票へ明記し、rootが統一/採択する。

計測すべき境界:
1. 各親の実inventory/受付の一回処理。18 roleの元順序を保持。
2. native batch v3/v4/v5の保存metadata認証caller。役割名・native schemaの意味を保持。
3. 可能なら既callerを包むだけで旧64/各batch状態復元・direct pairingの区間も別記。2と3は同じ仕事と仮定せず、入れ子のinclusive時間を合計しない。旧raw不変を破る必要がある場合は先に公開の具体deltaをrootへ提出し、無断で旧loaderを改変しない。

中断/例外で未完了区間の秒は0や成功値で埋めない。数学例外の原文をloggerが書き換えない。runtime関数を差し替えるmonkeypatchやshared P/C計器helperの共有は禁止。元の計算結果がPASSか否かは従来の完全照合で決め、計器だけで数学を格上げしない。

F3. 1108外側の受領と保存

P/C公開イベント型が固まるまで最終guardは閉じる。既stdout/stderrのraw保存を維持し、実stderr全bytesをpinしてから独立の親時間receiptへparseする。plain lineのsource offset/長さ、元log pin、側、role/native stage、実有限非負秒、欠落/中断/重複/順序違反を記帳し、parseできない行や未完了枝を黙って捨てない（他種の既progress行は別eventとして数を会計する）。失敗/欠落時もreceiptはnon-PASS/partialの事実として残す。source実行の成否や数学receiptを補完しない。

driver自身のlive/transportとintakeのrole別elapsedも、新metadata票として計測してよい。取得/API/ZIP/hash/空dir復元と、P/C側計器との異なる境界を明記する。全新receiptのexact key/type/path/schema/optional/early-nullを公開serializer票、全consumer票、保存rosterへ接続する。timingがn項の原因を確定したというfieldは作らない。

最終driver/WF/P6/C6 pin・raw delta・全consumerと自己読了を更新し、rootの別読後にmarker/nameを2227 notify-and-goで通知する。追加GHAを計器の試験目的で発火させず、許可済み次v6の一runへ同梱する。実装の選択で上記範囲を越える必要があれば、具体設計を公開票でrootへ先に示す。
