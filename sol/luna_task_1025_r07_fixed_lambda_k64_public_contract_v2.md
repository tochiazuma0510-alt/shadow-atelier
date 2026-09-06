# Task1025 — 固定lambda k64 batch v2 の公開共通契約

工房2173と返信163 F8.89の合意を実装へ固定する。rootが旧共通994 C1–C10、公開997（R1優先）/1000/1001/1002/1003/1004/1011、実k32全成果とP静的設計1023を読了して著作した。相手の私的設計票やsourceを読む許可ではない。

## 登録と変更範囲

新prefixはd972.r07.fixed-lambda-cycle-batch.v2。新sourceは search/d972_r07_fixed_lambda_cycle_batch_v2.py と search/check_d972_r07_fixed_lambda_cycle_batch_v2.py、新WFは .github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml。旧全source/旧票/旧親は不変。
固定登録はbatch_size=64、max_batches=1、selection_policy=CHORD_FIRST_ROSTER_64_THEN_FIRST_AUX、partial_policy=PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY、refill=false。全整数はbool/floatを拒否する。初回GHAはfresh P一回・C全新payload一回、resume/自動再試行なし。128は64の実結果後に別登録する。
親はrun33990567016/1・旧64/rank1450/gen8155、head c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70、artifact9977040548、ZIP304642285 B / a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792。元14とcontinuationの15親の全tuple/全file/全dir/全history/実旧C64を保持する。別k32/run34004423047やcontrol96のrank1482を初期状態へ入れず、旧packetを新sourceでresumeしない。
P5400秒/C10800秒・各7168 MiB、外側6000/11400秒。exact実Python/NumPy/runtime全文、保持Python19＋新P/C二本＋raw3の全24fileを1002の全pinへ結ぶ。旧batch v1自体を新計算helperとしてimportせず、新二sourceの実pin確定後だけ新codeへ置換する。

## 数学と公開wire

同じ固定lambdaで全54433弦・2aux・全four-character・全8059を走査する。非零弦m>0なら既定roster先頭min(64,m)、弦零なら先頭非零aux一件、全部零なら同current lambdaのCOMPLETE_ZERO_CANDIDATE。全failed列/残差全表は選択上限で切らない。依存候補の補充はしない。
候補別raw/source/primal/P1/全B、普通整数signed指数、mod54、全六cycle/零係数/全Ref/祖先、物理48384/source lower96776/物理lower32260、挿入順消去と全係数を保持する。数値targetの負号とliteral correctionの正号を変えない。新算術最適化・並列化・旧snapshot数値再演・候補ごとのSeparator生成を混ぜない。
全旧行dot0と両target dot1を今回直接読み、rho2 DERIVEDを維持する。共有TCB/F-fo-1/F-flb-1と163 F8.89の限定を継承し、二保持kernelの独立性を新sourceから主張しない。
公開997以降のkey/suffix/型/配置/全sealとfullfile hashの区別を保持し、新batch外側prefixだけv2へ移す。旧親schema・旧inner数値phase schema・旧artifact名は改名しない。nonce32hex/int32/uint32/歴史before32等の無関係な32は変更しない。
new candidate/row local ordinalは0..63、各countは全rosterと整合させる。rank=1450+accepted、generation=8155+accepted。private相sequenceは既存式3+6*i+p、p=1..6で上限387。64採用/rank1514や独立率は予告しない。
one-phase durable tail、bootstrap invocation、全保存/diagnostic型、同v2内の厳密resume、完成read-only resumeの無書込みを維持する。初回WFはそれらの自動再開を行わない。途中private stateを公開physical HEADへ昇格しない。
新lambda oracleはnull、grade2二字段はNOT_DECIDED、full_A0=false、verified=false。P/C既存のcandidate/cross_checked各字段の限定意味を保持し、工房CV-9の正式受理とは分ける。LinearだけNEW_BATCH_SAME_WORD_ADAPTER_PENDING、その他NOT_APPLICABLE。A0 actual0/1・階段1/6の台帳は新数値結果まで不変。

## 新二群だけのselftest

P/Cとも新 --selftest は二群だけへ接続する。名前と順は k64-version-registration-and-types、k64-full-roster-cutoff-and-restoration。各300秒/7168 MiB・外側360秒。旧三群はrun34004423047/1の保存実績として認証し、全再走しない。変更のない係数/target/packed等の旧成功suiteをここから呼ばない。
第一群は通常登録/schema/保存scope/新source bindingへ結ぶ。新64/1の正対照と、旧v1/schema/policy32/旧owner、k=32/33/63/65/128、64.0/文字列/true、max_batches=2/true/1.0、refill=true/0の拒否を、可能なものは完全resealして目的のgateへ届かせる。ordinal/row63・sequence387の受付、ordinal/row64・sequence388の拒否、直後一phaseと二phase先の区別、strict count0 bootstrapと新ownerの一件再rootを小metadataで結ぶ。無関係な旧全履歴・大物理spanを再走しない。
第二群は通常の全長roster選択と保存readerに接続する。synthetic非零弦数m=32/33/63/64/65で保存failed数m、選定数32/33/63/64/64を要求し、各caseの最後の非零を全弦末尾へ置く。非自明な五basis係数・全六cycle・零係数を含める。弦非零とaux非零が同時にあるcase、弦零/aux非零、全部零も含める。
65失敗時の過剰65witness、先頭32打切り、末尾全表欠損、64番目のindex/係数改竄、選定尾部順序改竄を保存readerへ通す。単なるmin式の写しを自己試験としない。P/Cは自系の別helper/fixtureを使い、相手の実装を読まない。実fixtureの拒否名/件数は作者票で公開し、事前に機械PASSを作らない。

新selftest top bodyは旧型 status/tests/fixture_scope/production_interfaces_used/old_success_suites/actual_anchor_arithmetic_replayed/candidate/cross_checked/verified、prefixだけv2。testsは二要素で各exact {name,status,rejected_cases}。status PASS、非空str/list、old_success_suites=普通整数0、actual_anchor_arithmetic_replayed=false、三assurance全false。
対照fixtureを後から点検できるよう、両CLIに **--selftest-root** を追加する。この引数はselftest時だけ必須、通常実行では拒否する。新WFからREPORT/selftest-fixtures/P又はCの絶対pathを渡す。TEMP又はRUNNER_TEMP内・regular既存parent・symlinkなし・まだ存在しないrootを作る。source/数学親/actual outputをselftestへ渡さず、同rootの再利用を拒否する。終了時にfixtureを削除しない。自己試験topに架空のsource別名や余分なreceiptを増やさず、実rootは外側command/全inventoryへ結び、全診断へ保存する。
Pの --batch-size は64、Cは既存の固定定数型を保ち、不要な同名CLIを増やさない。自己試験で計算した小値を実Omega/実rank1450の成果と呼ばない。

## 実装・監査・計測の境界

著者は自系v1全pinを基点に最小差分を作り、旧sourceは変更しない。新自系source/指定返信だけ変更可。ローカルPython/import/AST/数値/GAP/network/git/credentials/追加agentは禁止。rootだけが公開/実行brokerであり、全新source/全差分/公開CLI・型/新WF/別監査を閉じてからGHAへ進む。
候補相の秒/プロセス累積RSS/I/O、P全とC全、全selection/processed/dependent/accepted/skipped、保存量は実出力で分ける。約94%は旧primal+P1/候補六相の比で、P全では約76%。新速度/採用率/資源天井は未観測。source freeze時は全bytes/SHA/LF・新二群実interface・未実行を報告する。
