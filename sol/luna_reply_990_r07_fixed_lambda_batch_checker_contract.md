# Task990 — 固定 lambda batch の独立 checker 最小移行契約

**F1 — 判定と読取範囲。** 本票は設計のみ。裁定 2153–2154、2155、Task988/990、`docs/notes/cegar_resume64_cv9_reading_v1.md`、v547/v548 を全文読了し、以下に挙げる既存 C の実関数を静的に追跡した。新 P の source・返信989は読んでいない。source/WF/既存返信の編集、ローカル Python/import/AST/数値/GAP、network/Git/credential、新 agent、GHA は実施していない。変更先は本票だけである。

固定 lambda の全 oracle を一度照合し、同じ選定 lambda で複数の raw/source/P1/four-B を独立再生する方式は既存 C に接続できる。ただし **一行追加器と現在状態 serializer の転用は不可**。選定 lambda と batch 後 Separator を分け、依存候補を正規化せず保存する新しい物理消去・状態契約が必要である。共通 wire の確定と実装の許可は root の次委嘱に属する。

実親は run 33990567016/1、artifact 9977040548、64 行追加、rank 1450 / generation 8155、Separator / UNKNOWN_CAP、全 C 64 PASS。裁定2154で工房 cross-checked 限定8条として受理済みであり、grade2 は NOT_DECIDED、full_A0=false、verified=false。最後の HEAD lambda に対する oracle はまだ存在しない。旧 snapshot 63 の q/section/tree をこの最終 lambda の値として使わない。2155 の一回限り cap96 対照と新 batch の実測は別であり、本票はその将来結果を記帳しない。

**F2 — cap96 REST body の静的比較。** `%TEMP%/shadow-atelier-audit163/` の次の二ファイルを実 bytes/SHA と JSON metadata で照合した。

| ファイル | bytes | SHA256 |
|---|---:|---|
| cegar-resume-next-dispatch-parent33990567016-cap128-v2.json | 10005 | f05381734554cfc8a8dd205c70480bb732de6e92aae936c5e78b0bdb6aca6dc5 |
| cegar-resume-next-dispatch-parent33990567016-cap96-v1.json | 10004 | d5ad1f602a9efda6dd214a3875d897a696ecb30fc58f1bdbdf4b9fa57fa6aa1b |

両者の top keys は ref/inputs、inputs は observed_parent/max_appends。ref は `sol/r07-explicit-lift-20260825` の同一文字列、observed_parent も文字列全体が同一。max_appends は両方とも JSON string で、旧 "128"、新 "96"。旧テキスト中の `"max_appends":"128"` を `"max_appends":"96"` へ置換したものと新テキスト全体が完全一致した。従って変更はこの一箇所だけ。986/987 は遡及変更していない。登録 run 33995625884/1 の success は root 観測通知であり、登録 job の true と本数値 skip の記録である。本票は REST 送信・本数値 success を主張しない。

**F3 — 実 C の所在と変更境界。** 次の略号を使う。4 source の bytes/SHA は本便で再照合した。

| 略号 / source | bytes | SHA256 |
|---|---:|---|
| C = search/check_d972_r07_complete_oracle_cegar_continuation_v2.py | 129557 | e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3 |
| O = search/check_d972_r07_section_cochain_oracle_v2.py | 84402 | a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d |
| E = search/check_d972_r07_selected_cycle_materializer_v1.py | 103757 | a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4 |
| L = search/check_d972_r07_actual_root_seed_materializer_v3.py | 64626 | eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701 |

| 既存関数と行 | batch で保持する部分 / 必要な差分 |
|---|---|
| C FixedBundle L144、roots_and_values L216、section L244 | 固定12 blob/P1 index の認証と、各選定 lambda の全4×8059 contraction、kappa 全8059等式を保持。batch 内の候補間で同じ値を使い、次の lambda では全数を新計算する。 |
| C fixed_tree L339、O first_independent_columns L483 | 実 tree/全54433 chord roster、tau、先頭独立5本とその逆行列は lambda 非依存である。固定 source/owner/geometry/hash を照合して再利用できる。 |
| O source_scores L270、raw_edge_cochain L315 | ordinary27 の差分基底、全6 tag、非閉 edge の線形 Fox stencil、shared aux を保持。同一 q/kappa から score/f/b_aux を一度独立再計算する。 |
| C current_tree L358–407 | potential_f、全 chord values/residuals、fit/aux の計算を保持。ただし L378 は aux 優先、L383 は failed[0] 一件。新 selector は全 residual から既定順の先頭32以下を選ぶ別契約にする。旧 witness.json の意味を上書きしない。 |
| E selected_raw_slp L409、raw_materialization L757、ordinary_source L453 | 各 witness ごとの ordered SLP、実6 tag Fox、ordinary27 source、同じ q/kappa/f/b_aux による scalar anchor を保持。raw helper には「先頭失敗弦だけ合法」という前提はなく、実 chord/6 cycles/tau/endpoint/exponent を毎回調べる。 |
| C FixedBundle.primal L298 / corrected L302、E source_correction_record L1044、grouped_forward L1111 | 候補ごとの実 primal/P1 lift、全96776 lower equality、mod54/18、全4 B の和を保持。値を別候補から流用しない。 |
| E one_physical_row L1020–1041 | 分割が必要。L1024 は old_lambda(remainder)=selected、L1029 は各行で fresh Separator を要求する。固定選定 lambda で先採用行まで消去すると前者は一般に偽で、依存行は L.normalize にも渡せない。 |
| C PhysicalState.measure L605 / attach L624 / derived L659 / summary L671 | attach は常に Separator を前提にし、最後に全行/両 target の measure を呼ぶ。新 batch 中間状態は別型にする。immutable metadata の deepcopy 修理は新状態境界にも保持する。 |
| C replay_snapshot L904、dynamic_delta_records L843、step_record L1046、replay_head_prefix L1097、check_actual L1447 | 現状は「一 oracle・一 E・一行・一新 Separator」。新 wrapper の batch/candidate/row cursor と記録へ置き換える。旧 result の remainder_scalar=selected、各行 lambda_rho2、9 phases=一 step を新意味で再使用しない。 |
| L reduce_dense L539、normalize L561、next_target L571、next_separator L710 | 自系統の消去・正規化・target subtraction は保持可能。separator は batch 末尾の全採用行に対して一度構成し、最終ベクトルを全行へ再内積する。 |

特に紙上の F3² で旧 span=0、lambda=(1,0)、v1=(1,0)、v2=(1,1) とすると、各 selected scalar は1だが v2 の先採用行消去後は (0,1) で lambda 値0になる。二行は独立である。v2=2v1 の場合は同じく選定非零でも残余0となる。従って相互独立・消去後 scalar 不変・各候補 rank+1 のいずれも選定条件からは従わない。

**F4 — 一つの固定 oracle と全選定 roster。** batch 開始状態 S0/r0/lambda_sel に対して lambda_sel(S0)=0、lambda_sel(r0)=1 を全旧行の直接内積で確認し、元 rho2 の DERIVED identity/全親列を束縛する。固定 P1/Task554/Task712・Q0/Q2・同じ source であることが前提である。scope は全4 character、P1 8059、source lower 96776、physical 48384、edge 108864、chord 54433、aux 2 のまま。

独立 C が q[a]=B[a]*lambda_sel、chi[i]=sum_a dot(q[a],z_i[a])、kappa(b_i)=chi[i] 全8059、f/b_aux、全 chord 値 h_e と tau_e を作る。固定5本 J について T=(tau_J)^T、a=(h_J)^T T^{-1}、d_e=h_e−a tau_e とする（列/行の向きは C L373–376 と O L499）。全配列の shape/dtype/bytes/SHA/正確な EOF と、実 producer 配列全 bytes の一致を phase manifest ごとに要求する。統計値や PASS リテラルだけを照合の代用にしない。

本票の selector 案は **chord 優先**を明記する。I は全54433 residual を実 roster 順で走査した非零 index 列の先頭 min(32,非零総数)。edge id と roster index を別字段で保存し、全失敗数・先頭 index・全残差 file hash を記録する。I が非空なら aux が同時非零でも chord batch、I が空で b_aux が非零なら最初の非零 coordinate の一件 fallback、両方全零なら COMPLETE_ZERO_CANDIDATE。aux helper を実装対象から外す場合の代替は UNKNOWN_AUXILIARY_REQUIRED であり、完全零ではない。root はこの優先順位を共通 wire で固定する必要がある。

各 i∈I で beta_i=T^{-1}tau_i、z_i=cycle(e_i)−sum_j beta_ij cycle(e_Jj) を作り、tau(z_i)=0 と h_i−sum_j beta_ij h_Jj=d_i∈{1,2} を個別確認する。witness は「選定弦→同じ5 basis 弦」の6項を係数0も含めて固定順で保持し、eta=(0,0)。この構成は任意の非零 residual に成立し、先頭一本に固有の補題ではない（v548 §5、v547 Theorem4.1）。aux fallback は cycles 空、tau=0、eta がその標準基底、scalar=b_aux[coordinate]。選定 roster と全 witness は raw 計算開始前に封印し、lambda/section/cochain/tree/basis/fit の全 hash と結ぶ。

**F5 — 各 E と符号を含む物理消去。** 各候補について E の実 raw SLP と direct Fox → ordinary27 source u_i → primal の係数 alpha_i → 完全 canonical P1 補正 R(u_i) を独立再生する。raw 正規化は v547 の順序と普通整数 −epsilon_x/6, −epsilon_y/6 を使い、central は sr(omega)（sr(0,1,2)=(0,1,−1)）。P1 exponent は型付き residue54 を全8059行で保持し、18整除後だけ F3 pair にする。actual raw/source scalar の式は

`s_i = f(z_i)+b_aux(eta_i) = sum_a dot(q[a],u_i.d2[a])−dot(kappa,u_i.lower) = sum_a dot(q[a],R(u_i).d2[a]) = dot(lambda_sel,v_i) != 0`、`v_i=sum_a B[a](R(u_i).d2[a])`。

補正後 R(u_i) の全96776 source lower が実 zero であることと primal/P1 全 equality を省略しない。raw u_i の lower 自体は非零でもよい。physical lower zero は v548 §1 の ell=ell1*pi と pi(Ru)=0、および既存の typed lower-zero 行の線形結合から結ぶ。現 E はこの型を使って pure-top B を計算しており、同じ normalized word の full filtered 32260 lower bytes や11 slot を直接再生したとは言わない。physical reduction 後の語へ source-lower zero を新規要求するのも誤りである。

候補 i の到着時に実旧行 P と先採用 normalized 行 N を記録順に消去し、`w_i=v_i−sum_P c_iP P−sum_{j<i,accepted} d_ij N_j` を全48384座標で照合する。全係数、row ID/namespace、row bytes/hash、offer/lead、literal ancestor を保存する。lambda_sel(w_i) は別の測定値であり、s_i と等しいとは要求しない。恒等式 `lambda_sel(w_i)=s_i−sum_j d_ij lambda_sel(N_j)` は保存 scalar の相互照合になる。

- w_i=0: DEPENDENT。正規化行/lead/scale/target_delta は null、rank/generation/target は不変。zero relation の全 recipe と w_i の全 zero bytes は保存する。「物理依存」を「literal word が単位元」と呼ばない。
- w_i!=0: p_i=最初の非零座標、sigma_i=w_i[p_i]^{-1}（F3 では同じ1又は2）、N_i=sigma_i*w_i。N_i[p_i]=1、前座標と全既存 pivot lead の零を実確認して一行だけ採用する。
- target は `t_i=r_before[p_i]`、`r_after=r_before−t_i*N_i`。t_i は plain F3 scalar、s_i や sigma_i とは別。t_i=0 でも独立行の採用は有効で target bytes は不変。受理済 rho2−r0 の旧恒等式へ `r_before−r_after=t_i*N_i` を順に足し、全親列と各 instruction/result/normalized/target hash を結ぶ。

normalized 行の word recipe は `(U_i · prior_factor_1^sr(−c_1) · ...)^sr(sigma_i)`。U_i は raw word に記録順 P1 因子を内部 scale 一回ずつ適用した語であり、物理因子は実消去順、外側 scale は一回である。係数の residue と普通整数 exponent、物理和と非可換積の順序を混同しない。最終 target の正負を判別するため、全 accepted 行の subtraction identity を実 bytes から比較する。

**継承する positive root は残余 r_i の語ではなく correction C_i=元rho2−r_i を表す語である。** 従って新 batch でも `CorrectionWord_after = CorrectionWord_before · NormalizedWord_i^sr(t_i)` と **正の係数 +sr(t_i)** で順に延長する。数値残余は `r_after=r_before−t_i*N_i`、correction の値は `C_after−C_before=t_i*N_i` であり、同じ恒等式の両側である。採用行で t_i=0 の零冪参照も recipe から脱落させない。sr(−t_i) は残余自体の語を更新するなら現れる符号であり、現 positive correction root に使ってはならない。正の同語 root と数値 target をこの定義で明示的に結ぶ（root の公開数学指示、Task988 (988.8)–(988.9) と同じ区別。新 P source/989 は未読）。

**F6 — 新しい状態型と batch 末尾。** 最小の型を次のように分ける。

| 型 | lambda と保証 |
|---|---|
| FrozenSelection | batch 開始時 S0/r0 の Separator として認証済みの lambda_sel。選定 snapshot/全 oracle/roster に固定され、候補の途中で更新しない。 |
| BatchInProgress | 実消去・target identity を終えた採用行 prefix。現在 rank/target/row head は進むが current_lambda=null、current_separator_checked=false。selection_lambda は別字段で残す。 |
| Separator | batch 又は部分 batch の閉じた境界で新 span 全体を殺す lambda_after を実構成し、最終 target に1を与える。 |
| LinearMembershipCandidate | 実 target bytes 全零。current_lambda/direct_pairing/lambda_rho2 は null。target の親 identity 列は別の無条件字段として残る。 |

batch の採用数 A>0、残余 target r_A!=0 なら、L.next_separator の逆順 pivot solve を全採用行へ適用する。既存 API の最後の一行引数を使う場合は「旧行＋先採用 A−1 行」と「最後の N_A」を渡せる。構成後 lambda_after を旧全行＋新全 A 行へ直接内積し全零、lambda_after(r_A)=lambda_after(r0)=1 を確認する。各中間 target も telescoping identity から同じ値1であり、保存する場合は同じ最終 lambda の測定と明記する。元 rho2 に対する値1は旧 DERIVED identity と新 A 個の subtraction identity から導く。新旧両 lambda の hash・作用対象・直接測定/DERIVED の別を保存する。A=0 なら変更のない開始状態の lambda がそのまま有効であり、存在しない「最後の行」は作らない。

新残余が途中で零になったら、正しい Linear 型で止めてよい。選定済みの未処理候補は SKIPPED_AFTER_LINEAR と残し、全選定候補の E を再生したとは言わない。COMPLETE_ZERO_CANDIDATE は、**その時点の現在 Separator** に対して全8059/54433/2の oracle が完結している場合だけである。行を追加した後の古い固定 oracle は、この条件を満たさない。batch 終了時の新 lambda の全 oracle をまだ計算していなければ、結果は BATCH_APPLIED（grade2 未判定）又は適切な UNKNOWN とし、NONMEMBER に昇格しない。全弦零でも aux 非零、選定上限32、資源上限、target 非零は、それぞれ別の理由を保存する。

**F7 — 旧64行を固定した最小移行。** 提案は **受理済み continuation を読み取り専用親とする別 batch delta/overlay** である。旧 output/HEAD、source.json、owner.json、start.json、fixed/、全64 steps/snapshots、invocations、diagnostic を一切改名・再封印・上書きしない。新 owner は数学的 scope と accepted_owner_sha256 を参照する別 schema の記録、新 source は新 P/C の executable/import/raw/runtime と責任範囲を記帳する。旧 owner/source と byte 同一であるという偽装はせず、旧 frozen P971 の --resume に新 batch schema を読ませない。

新 checker 名の案は `search/check_d972_r07_fixed_lambda_batch_v1.py`、外側 schema prefix は `d972.r07.fixed-lambda-batch.v1`。これは未作成の名称案であり hash は未定。既存 C/O/E/L を自系統の凍結依存として保持し、新しい selector/state/serializer だけを自分で著述する。新 P の helper を import・コピーしない。内側 E v1 の raw/source/primal/P1 データは意味が同じ部分だけ保持できるが、新 physical-result/selection/checkpoint は新 schema にする。

提案 CLI は旧 C と同じ14親引数（state/delta/seed34/packet/refinement/oracle/e/prepare/p1/task712 各 --*-root、--block-root 四件）に、`--continuation-root ACCEPTED_ARTIFACT_ROOT --acceptance ACTUAL_PIN_JSON --candidate-root NEW_OUTPUT --output CHECKER_REPORT --max-seconds SEC --max-memory-mib MIB` を加える形。acceptance は root が実観測から作る親 tuple・全 file/dir roster・旧 full C receipt・HEAD/owner/source/start/fixed/target-history/runtime と、新 run の事前登録（candidate_limit=32、max_batches、absolute max_total_appends、resource ceilings）を明示的に分ける。ceilings は正整数/有限値で型確認し、候補中の self-declared limit だけで宇宙を決めない。最小の初回登録は max_batches=1 とし、次 batch は明示の登録に従う。parent が未来の96になったとの仮定は置かない。

出力の案は root に acceptance.json / owner.json / source.json / start.json / HEAD / result.json、`batches/000000/selection.json` と section/cochain/tree の完全 payload、`candidates/000000/` 以下の各 E phases/decision/依存又は採用 receipt、accepted rows の別 index、closure/checkpoint/invocation receipts。selection は開始 row head と lambda/target/fixed/P1 を参照し、candidate は selection digest/ordinal/edge/前 decision を参照する。採用 row instruction は old physical state_head から新 schema の rolling chain を延ばすが、batch/候補の進捗 hash とは区別する。全 file は exact roster、canonical JSON は sorted compact ASCII＋LF、inner seal と full-file SHA は別、packed3/u8/u32le の型・範囲・EOF は現契約を保持する。

counter は最低でも `anchor_continuation_rows=64`、`accepted_rows_since_anchor`、`total_continuation_rows=64+accepted_rows_since_anchor`、`rank=1450+accepted_rows_since_anchor`、`generation=8155+accepted_rows_since_anchor`、completed_batches、selected_candidates、processed_candidates、dependent_candidates、pending_candidates を分離する。依存候補は candidate cursor を進めるが rank/generation/physical row head を進めない。absolute row cap は total_continuation_rows に掛け、batch を32行と数えたり resume で0へ戻したりしない。候補 ordinal/attempt は generation と別にする。

既存 positive consumer 982/983 がこの新 schema を読めるとは主張しない。新 target-history の ordered ancestry は将来の同語 adapter が読めるよう完全に保存するが、本票はその追加実装も11-slot replayも実施しない。

**F8 — 中断・部分採用・全保存。** 全選定 roster を封印してから、候補を順に処理する。一候補の raw/source/primal/P1/B/物理消去と全比較を完了し、独立なら row/target/instruction、依存なら zero remainder/全 reductions/unchanged-target を完全保存してから、decision manifest → checkpoint → HEAD の順に公開する。物理採用がない候補の完了も耐久 cursor に含める。旧 prefix と全未処理 selected witness は残す。

資源停止で現候補が途中なら、最後の完成 candidate/phase までを HEAD の意味とし、未完成 bytes は明示型の diagnostic。既に完成した採用行を失わず、新 Separator が未完成なら BatchInProgress/current_lambda=null の UNKNOWN_RESOURCE にする。全32選定を破棄して別 lambda で引き直すことは resume ではない。再開は同一 selection digest/旧 anchor/新 owner/source/runtime と実 cursor を認証して、同じ lambda_sel の残りを続ける。old cap を越えて追加するには新 invocation の絶対上限を明示する。cap 停止時も計算済みの範囲を正しく残し、未評価候補の依存性や完全零を推測しない。

HEAD 外の完成 payload を回収するなら、許すのは直後の一つの連続 phase/candidate とその完全な親 hash/型/EOF が閉じる場合だけ。任意の先行番号・hole・別 selection・別 row predecessor を「orphanだから無視してPASS」としない。atomic pending 名は明示 grammar で診断として保存し、regular decision/invocation の件数には含めない。producer の durable保存だけで C の arithmetic accepted にはせず、新 C は新 batch の全 committed prefix を自系統で再生してから対応 cursor を進める。

全 start/selection/DERIVED parent/pairing/closure の export は deepcopy 又は immutable bytes とし、後の append で過去 seal が変わらない。C v2 L659–675 の修理を旧データ参照の浅いコピーで再導入しない。資源切れは exit3/UNKNOWN_RESOURCE、型・算術不一致は exit1/FAIL、全 committed data の比較終了は exit0/PASS と producer terminal の別字段で示す。PASS でも partial batch や未計算 oracle を全完了とは書かない。

**F9 — 重複を除く条件と最小 canary。** 旧64の全数 numerical replay を新 batch checker で省ける条件は、root が採用した実 success tuple/ZIP と safe extraction、旧 C v2 source/runtime pin、全64 steps/snapshots の full-array PASS receipt、現在 HEAD/result/target/lambda/全親列、全旧 output files/dirs の bytes/hash/EOF を正確に照合し、前後不変を残すことである。単に rank=1450 や status=PASS という字段だけでは足りない。現在の実64親はこの受理ルートの候補として既に存在する。

新しい thin anchor loader は、元14親の base/pivots と保存 normalized 行を actual row reader へ結び、現1450行の lambda_sel 内積と current target を新たに直接確認する。旧 oracle/raw/source を再生成せず、旧 target identity は受理済み列として明示する。`old_snapshot_numeric_replays=0` と `anchor_pairing_rows=1450` を別々に報告する。C.check_actual L1472 の旧全 replay 呼出しを単にスキップする改変や、P-only receipt による入場は認めない。旧 C の照合結果が FAIL/UNKNOWN、又は証明書の欠品、別 source、別 owner/HEAD、改変があれば入場拒否とし、必要な旧照合は root の別委嘱で行う。producer terminal の UNKNOWN_CAP/UNKNOWN_RESOURCE と、C 自身の未完照合は区別する。

新 batch 内は一つの FixedBundle と一つの q/kappa/f/tree を使い、各 E は順次処理して大きい raw/source 配列を次候補へ持ち越さない。固定12 blob、P1 index、geometry/carry の source 認証は一度でも、候補が使う row/phase の実 bytes/hash/EOF を外さない。次 lambda の contraction/section/cochain/tree は再計算する。新 batch の過去 committed 部分まで数字を省略する追加の accepted-checkpoint 制度は、本票では導入しない。

必要な新 canary は以下の三群に限る（未実装・未実行、実装後 GHA のみ）。旧成功 suite の重複再走を要求しない。

1. **実 selector/receipt の全数境界。** 整合する5本 basis/tau と全54433 shape の fixture で33個の違反から既定先頭32を選び、後方の違反も全失敗数へ数える。32/33取り違え、roster index/edge id取り違え、witness の basis 又は順序変更、末尾欠落/余分byte、別 lambda の完全 reseal を拒否する。chord+aux 同時非零、aux-only、完全零を別に通して新優先規則を判別する。
2. **実 batch 消去/target/closure。** 紙上期待値は旧 span=0、r0=(1,0,1)、lambda_sel=(1,0,0)、候補 v1=(2,0,0), v2=(1,1,0), v3=(1,2,0)。採用は2行、依存1件、sigma1=2、target scalar は1,0、r_after=(0,0,1)、lambda_after=(0,0,1)。v2 の残余 scalar は0でも独立であり、旧一行 API の偽 gate を判別する。続く v4=(1,0,1) で実 target 零/Linear/null lambda の型へ移る。数値 target の −t と correction root の +sr(t) の両 identity を結び、逆符号、scale 二重適用、依存をrank+1、selection lambda を current とする変異を拒否する。これは合成 fixture の期待値であり、実rank1450の outcomeではない。
3. **実 immutable/state/再開境界。** 最初の採用後・依存完了後・Separator 保存前の各停止点で serialize→resume を実関数から通し、同一 selection と completed cursor、絶対row cap、全 hash の安定を確認する。深い parent/pairing mutation、完成前 HEAD、飛び番号、違う親/source、cap counter の reset を完全 reseal 後も拒否する。未完は diagnostic、Linear 後の未処理は明示型、旧64の受理と新 arithmetic の完了を混同しない。

比較後の receipt は各 batch の lambda hash、全失敗数/先頭 roster index、全 selected/accepted/dependent list、各 target scalar/scale、全4 root の台、P/C 各 phase 秒を束縛する。次 lambda の oracle がないときに失敗数の改善を記入しない。時間は測定値であり、採用数32・速度改善・収束を予言しない。最初の実 nonzero 候補を完走すれば旧 span 外なので少なくとも1行進むが、停止前には保証せず、上限は `A <= min(32,48384-rank_before)`。全失敗集合や先頭 index の次 lambda での単調性も保証しない。

**F10 — 独立性と最終境界。** 新 source の著者を P/C で分けること、入口/出力を相互 import しないこと、静的差分や将来 AST 類似度を調べることは工程上の証拠であり、深い算術独立性の証明ではない。本便は AST を実行していない。C の ordinary27 差分基底、RawSLP、grouped B と packed P1 contraction を保持する予定だが、新 P の手法は未読なので新対の独立性を未監査とする。継承 TCB の read_task712_envelope / word/context / transport / PSL / B decode、旧 sparse_adjoint/vectorized_projection_chunk の clone 系譜、canonical P1/Conn、元 target/DERIVED rho2 の受理前提は残る。2154の歴史的限定を新設計で遡及閉鎖しない。

4 character 全 scope を計算することと、各 character が実際に informative なことは別である。受理済64の q1–3/aux が零でも今後の省略規則にはしない。v548 の完全零判定には Conn と同一 source/section を保持する。正の Linear 候補は同語 readout/必要な11 typed slotsを経る別経路であり、この batch の source lower-zero だけで MEMBER/full A0 を宣言しない。現 PB4-dropped grade の6成分と残り5 P endpoint receiptsの境界も変更しない。

本票の新規成果は cap96 body の一箇所一致確認と、C の既存関数に即した設計契約である。実装 source/CLI/WF/canary/新 batch の P/C 実走/CV9 はすべて未実施。Task988 の数学裁定と root の共通 wire 指示を受けてから、別委嘱の versioned source を作る。旧 986/987/source は凍結のまま。

判定: CAP96_BODY_ONLY_LIMIT_DELTA_PASS / STATIC_DESIGN_READY_WITH_NEW_BATCH_TYPES。実装・新 batch の算術結果を認定する票ではない。

AUDIT_990_VERDICT:
