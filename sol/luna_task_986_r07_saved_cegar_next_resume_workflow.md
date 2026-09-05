# Task986 — 同owner保存CEGARの次runを、観測済みpinだけで再開するGHA

役: Luna実装。Task983 source/返信の最終接続とfreezeを先に完了し、その後に本便を実装する。
変更可は `.github/workflows/d972-r07-complete-oracle-cegar-resume-next-v1.yml` と
`sol/luna_reply_986_r07_saved_cegar_next_resume_workflow.md` のみ。公刊source/workflow/返書は不変。
ローカルPython/import/AST/数値/GAP/network/git/credential/新agentは禁止。実行とGitHubはroot brokerのみ。
既存980 workflow/981監査/975・976・979の境界を使う。P971とC継続v2の算術を変更・共有しない。

## 目的と起動前件

WO-162-1のCEGARをactual grade2結論まで続けるため、同じ凍結P/Cを別runnerで再開する。
現在run33990567016/1（launch c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70）は全C実行中。
まだsuccess/after-count/terminal/artifactは未観測なので、その値を作らない。
最初の再開はrootが実artifactを回収し全C成功と継続可能なUNKNOWN_CAP/UNKNOWN_RESOURCEを読んだ後。
COMPLETE_ZEROやLINEAR_MEMBERSHIP候補なら該当976/975経路へ進み、本workflowは発火させない。
CV9は事後判読であり、計算実行の事前許可にしない。正式受理rank/候補rankは別の値を保つ。

次の各runでworkflowを書き換えずに済むよう、workflow_dispatchの一つのJSON文字列入力
`observed_parent`（必須）と普通整数文字列`max_appends`（必須）を使う。初期の数値capはrootが
実親を読んだ上で決める。既定の未来parent/成功pinは置かず、pushでは数値jobを起動しない。
入力JSONは固定env経由でjson.loadsし、shell/script本文へ直接式展開しない。
caller-provided成功文字列だけでは認証せず、全live API/実ZIP/body/既存owner/sourceと照合する。
公開reply986でexact入力schemaと再現dispatch JSONを明記し、全入力を新artifactへ保存する。

## 同一親・同一producerの契約

rootの観測pin JSONはrun/attempt/head/workflow/artifact id/name/ZIP bytes/SHA・実entry一覧・実current
count/rank/gen/kind/terminal/state_head/owner/source/start/full HEAD/hash・実旧invocation一覧を含む。
作成時点で欠ける実値はpendingと表示する。受理可能な親workflowは公刊completion-v1、resume64-v1、
本resume-next-v1の三つのみ。同repo 1312092366、同作業branch、実success、正しいcandidate名を要求する。
rootが手渡す初回の実pinへの接続は別に最終監査する。

元14親の全run/head/artifact/size/digest/Task554 accepted failureは980から厳密に継承する。
第15親が直前の完全candidate全体。旧completion等がその中に入る場合、保存済み全file/dirを保持し
来歴を認証する。過去親を未観測のlive成功と扱わない。全rootは相互非包含、安全ZIP exact type/path/EOF。
15 live API repository/head_repository/run/attempt/head/workflow/conclusion/artifact name/id/bytes/digest/expiryと
実ZIP全hashを要求し、元source20/raw3/Python全文3.13.15/NumPy2.5.1も980と同じ実pinに固定する。
固定P971=126940 B/67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c、
C v2=129557 B/e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3。

beforeの実countをnとし、元startはrank1386/gen8091/count0固定。before rank=1386+n/gen=8091+nを
親HEAD/result/checker/full-prefix各実receiptへ結ぶ。元owner/source/start/fixedと20source/rawは不変。
全outputを新mutable siblingへcopyし、before全file/dirを記帳、HEAD/resultの旧実bytesをbefore/へ保存。
許可する旧file変化はHEAD/resultのみ。他の全旧file/dir、旧step/snapshot/phase/pending/checkpointは
親Cが認証した入力をそのまま保つ。全旧invocation UUID/hashも保存する。

## 一回P・全C・保存

Pを一回だけ `--resume --max-appends M --max-seconds 5400`、outer100minで走らせる。
Mはnより大きい絶対累積cap。現在の固定48384物理次元とstart1386の範囲内へ制限し、bool/負値/非整数を拒否。
追加append数はafter-count minus nの実差、rank上昇は同実値から記帳し、cap達成と決めつけない。
旧invocationすべて不変、新invocationちょうど一件、新UUID・before n/HEAD/hash/source/runtimeを結ぶ。
afterの実kind/terminal/coherent HEAD/current checkpointを読む。未知/資源終端の全partial/pendingも保持する。

C v2をstartから全after-prefixに一回、internal10800s/outer190minで実行する。全8059/54433/二aux/
96776/four B/current lambda/HEAD/各phaseと32に限らない全snapshot/step/現在checkpointを照合する。
新Cのsteps[:n]/snapshots[:n]は親Cの全dictへ厳密に一致、旧全invocationの数と実hashも一致。
数学算術が変わらないこのdriverに旧成功suiteの再走を足さない。新metadata境界canaryが必要なら
新JSON/型/コピーの実経路だけを小さく試し、その目的を記帳する。ローカルでは実行しない。
job330min/7GiB、旧owner内の同P/runtimeを維持。時間・反復数の成功予測は書かない。

alwaysで元15親/保存old output/20source/raw/WF/入力JSONの全bytes/hashとdirectory rosterの前後不変を
比較し、保存receiptを作る。旧completion/失敗run/現在runの来歴を混ぜない。新run/source/current親と
全after結果・親C prefix・新invocation・保存を最終receiptへ結び、全gate成功のみcandidate upload。
always diagnosticは全output/途中file/hidden/pending/ログ/exit/実秒/入力/元source/WF/親intakeを残す。
retention30日。新artifactに元14親の巨大payloadを重複格納する必要はない。

CV9用に、可能なら新driverで全after-prefixのcoverageを機械生成する。既存completionのq/κ/score/aux
bytes scopeを継承し、2149指定の修理前wのωとcentral指数全列・lambdaのcharacter別台・failed_chord/
basis実値を追加する。legality.omega定数を修理前ωと取り違えない。このdriverの測定はP/Cの第三算術と
呼ばず、sourceや旧数値を再演したとも言わない。現q零と作用素恒等零、fixed scopeと情報性を分ける。

candidate=true/cross_checked=false/verified=false。MEMBER/NONMEMBER/side/fullA0の未完境界を維持。
最終source全文と正確なschemaをレビュー可能にし、bytes/SHA/LF/CR/BOM/finalLFを返信へ。
最終行 `AUDIT_986_VERDICT:`。985の同一語consumerは別job・別owner出力であり本再開の前件にはしない。
