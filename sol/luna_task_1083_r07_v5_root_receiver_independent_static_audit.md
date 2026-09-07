# Task1083 — Luna: v5 root metadata受領器の独立静的監査

宛先: packet_producer。1081の最終WF/driver差分監査と返信を最優先で完了した後、本便を続ける。返信は sol/luna_reply_1083_r07_v5_root_receiver_independent_static_audit.md、独自材料は TEMP/shadow-atelier-audit163/task1083 の新fileだけ。新agentは起動しない。rootがGHAの配置・実行・受領を担当する間の限定別読であり、GHA発射に本便完了という追加条件を課さない。

## 権限と入力

Task1080の全文、1074最終受理済みhelper、1079の最終公開serializer/R1/cost/registry、1082の正式whole-inventory登録と公開range、1080作者が固定したimmutable snapshot/全差分を読む。1080のmutable working copyを最終監査済みとしない。P/C私的数値bodyは追加で読まず、raw sourceは公開pin/range比較だけとする。Git/network/credential/Python/GAP/import/AST/compile/source実行は禁止。受領器自体やfixtureも本便では実行しない。ASCII/raw bytes/typed JSON metadataによる静的監査だけを行う。既存親artifactや旧受領器を変更しない。

基点1074は TEMP/shadow-atelier-audit163/task1074/audit-r07-batch-v4-metadata-v5.ps1 = 261800 B / dcccf94a7eb3458d6cf709478a449d3377f86e5b90edfa0a9f011d82122ac411。rootは同一helperの全typed受領v2を15:50:32Zから別sessionで継続中である。初回は旧v3の認証空36dir未復元でexit1。rootが全11437fileの前後SHAを照合して空36だけ復元し、3475dir一致を閉じた。v4も全11648file/1308094050 B/3525dirを新全hashして正式登録済み。2210はこのwhole-inventory登録と長いtyped受領の分離を了承した。未完受領をPASSへ補完せず、旧receiptへの信頼置換やcache最適化も導入しない。

## 監査の要点

1. 旧1074の全raw保持と変更/新規全区間を完全EOF分割で比較する。historical-v4全mainが明示した局所scopeへ移されても、全旧親・全file/dir/ZIP・原64 fixed payload・registry/TCB・全checkpoint/invocation/row/phase・diagnostic/DEPENDENT境界が削除されていないかを読む。旧receipt書出しから値returnへの変更、PowerShell5.1のscopeと空/一要素/nested array、helper出力への余計な値混入を重点にする。
2. v5通常mainへの新reader接続を全て追い、17役/acceptance8key/旧v3と新v4二層/353祖先/theta0/previous v4 start.target/128+128=256を区別する。新batchの採用数は0..128の実観測で、全128独立を仮定しない。型不備/欠品/early failureをnullで完全受理に変えず、normal guardが実観測前に開かないことを確認する。
3. 旧v3/v4両親の早期read-only preflightは全名前・サイズ・保存目録・全dirの欠品を先に捕捉し、親mkdirしない。後続全payload hash/全目録照合を省かない。正式canonical files/dirsの全raw pinは metadataの入力であり、保存PASSを新たな信頼根にしない。
4. WF最終公開契約へ、11行bootstrap SHA/旧WF二archive/旧v4 WFとdriver/新driver・新WF、三registry/全EOF/旧8loader/57body/21Python+3raw、P-C前後/全親保持を接続する。R1は旧 batch-fixed-reference-receipt.json と新 next-batch-fixed-reference-receipt.json の各plain17key、acceptance/always readback/run/final全束縛へ繋ぐ。未形成票の扱いを完全受領へ混同しない。
5. 第四群P28/C15全file・7正負対照/実 observed_error/ledger単一改変を公開型へ結ぶ。旧三群のP17/C16非対称は保持する。synthetic fixtureを実1706算術と宣言せず、共有TCB/call coverage NOT_MEASURED/第三数値独立性なし/verified=falseを残す。
6. cost全15key/8秒欄/6相/全実input pin・field・unit・phase count、17親規模と旧新source文脈を公開契約から読み戻す。P residual/C total/P+C totalを混同しない。負値はsignedのまま、欠品/NaN/Inf/bool/overflowは成功値にしない。作者がmath.fsum用に小さいdouble集計helperを追加する場合は、型/finite/途中overflow/打消し/丸め境界とcallerの意味を独立に別読し、未証明bit一致を主張しない。一般Same/PlainInt/parserの既受理契約へ波及させない。

## 引渡し

required findingは直ちにrootと1080作者へ報告し、修正版は別snapshotと完全差分で受ける。全source/材料pin、旧保持/変更/新規/EOF再構成、全新bodyとmainの読了範囲、未解決項目を返信F#へ明記する。launch/artifactの実pinだけが後着なら本文静的採否と定数pendingを分離してfreezeし、rootが後で一箇所差分を監査できる形にする。本便はmetadata受領器の監査で、新数学矢印・GHA成功・cross-checked/verifiedを先取りしない。最終行は AUDIT_1083_VERDICT: を置く。
