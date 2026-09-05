# Task994 — 固定lambda cycle batch共通契約とP実装 v1（991凍結後）

役: 既存packet_producer。991のsource/WF/返信を完成・凍結してから本便へ進む。
変更可は新 `search/d972_r07_fixed_lambda_cycle_batch_v1.py` と
`sol/luna_reply_994_r07_fixed_lambda_cycle_batch_producer_v1.md` のみ。WFは別便。
新C source/995返信は読まない。rootから届く公開ABI/数学条件/pinだけを受け取る。
ローカルPython/import/AST/数値/GAP/network/git/credentials/新agent禁止。GHAはrootが実行。
sourceを書いて静的に読むことは許可する。既存source/旧返信/旧親を変更しない。

以下C1–C10はrootが定めるP/C共通の数学・wire契約で、Task995/996も同じ部分を読む。
根拠は988 F2–F11とrootの本文F8.63。新P/Cは著者分離、旧自系の保持TCBを明記する。
989/990の名称・partial publication・capの案は、競合する場合には本契約で置換する。

## C1. 範囲・親・新型

prefixは **d972.r07.fixed-lambda-cycle-batch.v1**、一つのselection lambdaで一batchだけ。
Q0/Q2/Delta/全四character/物理48384/source lower96776/物理lower32260/全8059/全54433/2auxは不変。
現実に観測済みの初回親はrun33990567016/1、head c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70、
artifact9977040548/304642285 B/a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792、
旧64/rank1450/gen8155/Separator/UNKNOWN_CAP、工房2154限定8条。親の全output/C成功/同sourceを認証する。
実初回fixtureはこの親。n/rank/genは実HEADから読むが、未来の96結果や任意の親successを補わない。
rootが将来別の実親を選ぶなら、送信前に全tuple/全bytesと範囲を新しく事前登録する。
新batchは別output・別owner/source。旧64と旧owner/source/start/全file/dir/全C dictは読み取り専用。
旧P971/Cv2のsame-owner resumeや旧positive readerへ互換を偽装しない。

## C2. CLI・root入場

元14親の既存引数名を保持: state/delta/seed34/packet/refinement/oracle/e/prepare/p1/task712の各--*-root、
--block-root四件。追加は --continuation-root、--acceptance、--output、--batch-size、--max-seconds、
--max-memory-mib、--resume、--selftest。本走batch-sizeは**32のみ**、max_batches=1、refillなし。
rootの実受付JSONはschema=prefix+.acceptance、topは `schema,parents,anchor,code,runtime,registration`。
parentsは元14＋continuationの実15role、各role/path/実artifact tuple/全files・directories pins。
anchorは実HEAD/result/C/owner/source/start/fixed/全invocation/旧C全prefixのpinsと実n/rank/gen/state/target/lambda。
codeは新P/Cと保持実closure/rawのpath/bytes/SHA、runtimeは実Python/NumPy文字列。
registrationはbatch_size32/max_batches1/selection_policy/partial_policyとP・C各資源上限。全部strict型。
rootが実値を用意する。実ファイルとの全結合/旧実成功C/source/runtime/全履歴/不変を、callerのPASSだけで代用しない。
API/live ZIP認証はworkflow、sourceはその受領証と全bytesを別に照合する。exact公開key/entry ABIは実装中に先に返信へ出しrootへ送る。
Pはmax-seconds5400/max-memory-mib7168、Cは10800/7168を本走の初回枠とし、CLIは実宣言をowner/invocationへ封印する。
旧success suiteは再走しない。新三群canaryは各系統300秒/7168MiBでGHAだけ。

## C3. 元stateのthin受領

元14親からbase行providerを自系で作り、実旧n個のnormalized行を保存physical行として挿入順に結ぶ。
旧oracle/Eを新算術として再生成しない。旧全phase/step/snapshot/HEAD/result/C/source/全親のbytes/EOFは認証する。
同selection lambdaの**全旧行dot0・実旧/現target dot1**は今回直接確認する。元rho2の値1は保存identityによるDERIVED。
old_snapshot_numeric_replays=0とanchor_pairing_rows=実rankを別に保存。元sourceの整数count1をbool扱いしない。

## C4. 固定oracle・選択

同lambdaでq/P1 contraction/8059等式/kappa/score/f/b_aux/tree/tau/J/fit/全residualを一回全EOF。
既定rosterの先頭 min(32,実非零総数) の弦だけを候補にする。全失敗index/edge列と総数を保持。
policyは **CHORD_FIRST_ROSTER_32_THEN_FIRST_AUX**。弦非零ならaux同時非零でも弦batch、弦零なら先頭非零aux一件、
両方全零なら同current lambdaのCOMPLETE_ZERO_CANDIDATE。aux fallbackを実装する（未実装で完全性を称さない）。
固定五basisのtauを行として保存し、各dは `sum_j d[j]*tau_basis[j]=tau_e` を満たす。
各六cycleは選定弦先頭→Jの五本順、係数0を保持。tau零、h_e−sum d*h_J=residual_e=非零を実照合。
旧single witness hashを他候補へ流用しない。全54433を読む前の先頭32打切りは禁止。

## C5. 候補別の実語・source・P1

同selectionに結んだ候補固有のraw/source/primal/P1/four-Bを全数実行する。
既存Eの算術が同じ部分は自系の凍結helperを利用可能、候補viewだけ新型にする。
raw wの普通epsilon/6、三因子順、central sr(omega)=0/1/-1、全六cycle/aux eta、Q0/Q2/Fox/境界/carryを保つ。
同8059 source basis/順のalpha・P1を一度だけ引き、全96776 lower零、全四Bとselection scalarを照合。
mod54/18は普通整数、bool/float不可。候補ごとの可変parts/alpha/sourceはfresh、過去snapshot/親listはdeepcopyかimmutable。
新行v_iのlambda_sel(v_i)=選定非零scalarを確認。次の消去後にも同じ非零を要求する旧one-row wrapperは使わない。

## C6. 実消去と二つの符号

旧全basis＋先採用行を**挿入順**に消去し、全48384のremainderと全係数を保存。
zeroはDEPENDENT、normalized/lead/sigma/target_scalar/newrowはnull、rank/gen/target/physical headは不変。
nonzeroは最初の非零leadで一度monic化し全旧lead零を確認、独立行だけ一行採用。
旧lambda(remainder)=選定scalar−sum_new coefficient*旧lambda(newrow)を実照合し、零でも独立なら採用する。
normalized語は `(P1補正語 · 消去event順の各旧/新語^(-sr(coefficient)))^sr(sigma)`。
数値はtheta=target_before[lead]、target_after=target_before−theta*normalized。
継承positive rootは**correction=元rho2−current remainder**。追加因子は**+sr(theta)**で右へ積む。
theta0/零power/反復Ref/全祖先を落とさない。依存語を自由群identityと呼ばない。
修理/P1後source lower零と、物理消去後のphysical lower零/source-lower NOT_ASSERTEDを区別する。

## C7. 終端と私的進捗

selection lambdaは不変。途中のgrowing spanに対するcurrent lambdaはnullで、Separatorとは呼ばない。
通常は全選定候補のE・依存判定・targetを終えてから、全旧/新rowに直交し初期/最終targetへ1の新lambdaを一回作る。
元rho2への1はDERIVED。新lambdaのoracleは未計算のnull、終端は **BATCH_COMPLETE_CANDIDATE**。
途中で実target全零なら **LINEAR_MEMBERSHIP_CANDIDATE**、lambda/null、未処理selected tailはSKIPPED_AFTER_LINEAR。
oracle全零は行追加前の同lambdaでのみCOMPLETE_ZERO_CANDIDATE。どれもこのsourceだけでgrade2/全11slot/A0/verifiedを宣言しない。
**公開するphysical HEADはfinal SeparatorまたはLinearの完成後だけ**。途中のphase/候補cursorは `progress/HEAD` の
BatchReductionStateとし、公開HEADと別schema/別path。資源停止ではUNKNOWN_RESOURCEとこの私的checkpointを保存する。
未完成finalizerのrankを新accepted physical stateとして公刊しない。初回版はpartial physical flushを行わない。

## C8. 保存配置とwire

root: owner.json/source.json/start.json/parent-layout.json、fixed/manifest.json。
selection/start.json、selection/{section,cochain,tree}/、selection/selection.json。
candidates/000000/{witness.json,oracle-view.json,e/{raw,source,primal,p1,B},reduction/}、candidate manifest。
accepted rowsは `rows/000000/` から0始まり（**新rowのlocal offset**）。旧/新global row ID・generation・offer ordinalと区別。
final/manifest.json・final/lambda.bin/target-remainder.bin・final/separator.json（Linearならlambda fileなしとtyped null）、公開HEAD/result.json。
progress/HEAD/checkpoints/、invocations/、全pending diagnostics。候補数・処理数・依存数・採用数・旧n・累積nを分ける。
rank=anchor_rank+accepted_new_rows、generationも同増分、全行追加上限48384。非空batch完走なら採用≥1。
内部E payload名/dtype/shapeは既存L registered_phase_roster/E_ROSTERと同じ部分を保持し、外側manifestだけ新型。
全JSONはsorted compact ASCII+LF、inner sha除外sealと全file hashを区別。u8 trit0..2/packed4 trit base3 byte0..80/u32leを保つ。
各file descriptorはexact `file,bytes,sha256`、binaryはさらにdtype/shape。各phaseはowner/start/selection/候補ordinal/前phaseへ結ぶ。
各行/候補のrolling chainはそれぞれ別schema。physical instructionは直前physical headとnormalized/literal/target全hashへ結ぶ。
構造上まだ未確定の小keyは作者が**公開ABI表だけ**をrootへ先送りする。rootが両者へ同じ追補を配達してからfreezeする。
相手のsource/アルゴリズムの読取りでABIを合わせてはならない。

## C9. 中断/再開

完了payload→manifest→候補decision→checkpoint/progress HEADをdurable publication。builderを二重実行・二重採用しない。
公開physical HEADはfinal一取引の最後。協調停止をpublication列途中へ挟まない。
resumeは同親/owner/source/runtime/k/selection/完了prefix全hash、旧HEAD外tailは直後の登録phase/candidateだけ完全認証して回復。
穴/飛び番号/別snapshot/無根拠extraは拒否。明示pending名は診断として全保存しordinary countへ数えない。
P停止exit3/UNKNOWN_RESOURCE、型算術不一致exit1。Cは新committed private prefixも全算術比較し、partialと完了を別に出す。
CのPASSは照合完了範囲だけで、公開physical HEAD未完成ならcandidate=false/partial=trueを維持。

## C10. 全比較/計測/試験

Cは独自の全oracleと各E/全消去/依存/全target符号/最終dotを実配列・全JSONと比較。
未処理候補は測定null、旧受理はthin anchor、実新third実装と呼ばない。全文output/親/code前後不変。
全失敗residual数/先頭index/全列、q四台、kappa tag/aux、score/aux、raw修理前omega/普通epsilon/中央指数/SLP長、
selection/final lambda四台、候補ごと各phase秒/RSS/I/O測定の区別、全selected/processed/dependent/accepted/target係数を保存。
final lambdaのoracle未計算で失敗数改善を捏造しない。実時間/採用32/速度比は予言しない。
新三群canaryを本番helperへ直結: (1)全roster/先頭32/末尾違反/aux-only/全零/別snapshot拒否、
(2)依存・旧lambda残差0の独立・sigma2・theta非零の両符号・実Linear/Separator・packed EOF拒否、
(3)完成/依存/publication前後停止・深いalias・hole/別親/cap reset/完全reseal改竄拒否。
合成fixtureを実Omega/実rank1450の成果と称さない。数値とASTはGHAのみ。旧suiteを再走しない。

## C11. P著者への実装境界

Pは既存自系L/O/E/M/Fを保持依存として利用できる。旧sourceを変更せず新wrapper/selector/消去/記録を自分で著述する。
行別のone_physical_row/fresh separator wrapperは使わず、選定immutableと消去stateを分離。
一候補ずつ大きい配列を解放し、全54433×48384行列・全8059 dense cache・32候補phase常駐を作らない。
旧n thin loader、selection、各E、消去、finalizer、durable復元の公開API/CLI/serialized keyを最初に返信へ記す。
C1–C10に疑義/型衝突があればsourceを実装しながらrootへ具体的なABI差分だけ送る。
最終全source/依存closure/raw bytes/SHA、全差分/未実行を報告。最終行 `AUDIT_994_VERDICT:`。
