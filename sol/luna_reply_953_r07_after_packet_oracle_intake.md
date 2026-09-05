Task953 — fixed44 後の完全 grade2 oracle に向けた限定 intake。v548/v543/v546/v547、v541、関連する v454/Task575・v459・v518/v534、および下記の実装箇所を読んだ。本返信以外の変更、数値実行、ネットワーク、git、credential、追加 agent はない。

F1. **推奨する次の実装は、fresh four-root full-origin scan と一つの正しい actor materializer。** root から run33964709359/1、commit `fff114c41bd8748ad0e708919fe0820335c9cce8` の producer/checker 成功と `ROOT_SEEDS_ZERO` を受領した。報告された現状態は rank1359、generation8064、head `7b7380a7ddb785910347df14f47ba4634cc5fa2fff7c32b722455a824d6cddda`、lambda SHA `60ac649575400e98881c5de5d4ef2c6202d3cf577da1411042104254edb004e2`、candidate9969090590。この実行を私は再実行していない。次 owner はこの受理済み v2 prefix を immutable parent として読む。fixed44 の owner/packet に actor を追加して宇宙を変更する形にはしない。

| 経路 | 既存の具体的資産 | 次に必要な実装 | 零だった場合 |
|---|---|---|---|
| v541 full-origin | corrected actor adjoint、12本の lower blob stream、全8059行と4 actorsの accumulator | 現状態 loader、fresh 全4 roots、全 scalar 配列の封印／独立比較、選択 actor の完全 filtered source 再構成 | root EOF だけでは UNKNOWN。fresh dual closure と全 origin EOF、または下段の完全 cochain が必要 |
| v548 cochain | 同じ affine/Fox/六置換、P1 lower payload/cache、五 carry の公式、v547 literal readout | joint kappa、六置換の Q2 vertex adapter、source edge adjoint、tree/carry 全表、違反 cycle/P1 materializer | 全54433 chord と二つの auxiliary 条件を満たせば、保持した Conn/source premises の下で完全な当該 grade の NONMEMBER |

前者は既に scalar accumulator が全 roster を計算するため、次の候補を具体化する変更が小さい。後者は完全な零判定を与えるが、既存コードへ flag を足すだけの経路ではない。時間比較や非零 outcome の予想はしない。

F2. **再利用する既存系統と変更点。** producer は `search/d972_r07_actual_grade2_root_scalar_batch_v2.py` の `actor_adjoints`、`accumulate_scalars`（806行付近）、P1 batch と lower blob reader。checker は独立の `search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py` の対応する処理を使う。固定 SHA はそれぞれ `3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856` / `e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6`。

現 lambda からの4 roots と4×8059 basis 値には `d972_r07_rank1355_root_seed_scalars_v1.py` / `check_d972_r07_rank1355_root_seed_scalars_v1.py` の `new_roots` / P1 contraction 系統が使えるが、rank1355 固定 state/lambda の受理部分をそのまま呼べない。現 prefix の受理境界は今回の fixed-root-packet-loop v2 と各 checker を正本とする。旧 scalar batch の root pin、character0 固定、seed2 固定 scalar、504/503 という古い orbit 出力は新 owner に持ち込まない。

`accumulate_scalars` は raw seed44、homogeneous actor top と **K_t b の lower 寄与**、global SeedRed/ActRed の全 subtraction を実装している。一方 `_scalar_result` が保存するのは seed scalar と actor lower 配列等で、最終 `actor_values` 全体は保存されず `_scan_accumulated` は first hit で止まる。次版では最終 `seed_values[44]` と `actor_values[8059,4]` の bytes、順序、sha、全長を封印し、checker も全配列を再構成して比較する。4 roots を全て再計算し、零 root の処理も実際の零 bytes に根拠を置く。first hit はその完全配列から固定順序 `seed0..43; basis_i0..8058 × actors(1,-1,2,-2)` で選ぶ。

F3. **そのまま使えない actor consumer を確認した。** `search/d972_r07_grade2_violation_materializer_v2.py` の `_lower_reconstruct`（2181行付近）は、actor direct 側を cached top に homogeneous Task712 T を掛けるだけで作っている。ここには v541 の K_t b がない。seed 側も旧 `seed_source` に依存する。この generic v2 を corrected scalar の後ろへ無変更でつなぐことは不可である。

新しい選択 actor consumer は、指定 basis_i の actual `(b_i,z_i)` を12本の lower payload と、受理済み canonical P1 v9 parent（run33851744070/artifact9931437113）の cache から読む。producer の v15 `_seed_act` と v541 `actor_tag_values`、checker の対応する **full filtered** actor 処理を使い、direct `(A_t b_i, K_t b_i+T_2,t z_i)` を作る。Task554 の選択 `ActRed(i,t)` を旧／新全 block から順序つきで集め、同じ係数で全 lower と top を引く。全96776 lower が零になった後で character slice を選び、B を掛ける。`search/d972_r07_actual_root_seed_materializer_v3.py` / その checker の selected-lift receipt、ordered P1 ancestry、physical insertion、target/新lambda処理は再利用の正本だが、seed-only origin の箇所は actor 用に拡張する必要がある。

raw affine/Fox の正本は producer `d972_r07_targeted_grade2_owner_generated_join_v15.py`（SHA `76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632`）、checker の同名 `check_...v15.py`（SHA `8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662`）。使用対象は raw word/full actor helpers であり、退役した片側 projected direct-seed wrapper ではない。

F4. **v548 の joint kappa は実物から組めるが、lead の読み方を固定する。** 指定 TEMP の `task554-prepare-33677346616-1-pinextract/prepare.1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865.json` を直接読んだ。ファイル本体は top-level `old_blocks` を持ち、`.body` wrapper はない。各 old block は `character, character_index, defect_origin_range, lifted_grade_blob, lower_basis_blob, rank, record`、record は `actor_order, actor_transitions, attempts, character, dag_nodes, queue_exhausted, rank, seed_reductions` を持つ。

old row は width6056 の「owner の6048 d0＋共有8 aux」と width72576 の全4 d1 companion の組。新 row は owner の width18144 d1。最初の old0 DAG node は `pivot=0, lead=6054, origin.projected_seed=1, scale=1` で、lead は共有 aux6 である。full96776行へ d1 を加えた後の最初の非零座標に置き換えると、この元 pivot を失う。

具体的な dual interpolation は、まず新6045行の d1 部分で kappa_d1 を求め、old2014行の値から `kappa_d1(lifted_grade)` を引き、その残差を joint「4 d0＋共有8 aux」の old basis で解けばよい。各段で保存された insertion order と実際の prior-pivot 零条件を使い、数値 lead の昇順を仮定しない。共有 aux を4組に複製しない。最終的に全8059行で

`<kappa,b_i> = sum_a <B_a^*lambda,z_i[a]>`

を照合する。この手順は physical lower rank6705 の multiplier mu を要求しない。Conn の完備性と現 lambda が Conn を殺す premise は残る。

F5. **六置換は同じ legal source の raw-chain adapter を誘導する。ただし実装／受領証は未接続。** 既存 `_SeedContext` の group law は section-left/kernel-right の `(p,e,k)`、積の k 部分は `S(e_right)k_left+k_right`。`_seed_affine_fox` は left-prefix、負 letter は prefix を逆元で進めてから負係数を置く。六置換は `SEED_OO` の固定順で、五つの異なる Nielsen substitutions と identity の重複である。

下降の根拠は A-character transport だけではない。v459 と `scratchpad/a0_v2_words.py` は固定19-relator Q0 presentation の全五置換での endpoint-one を保持する。これらの Nielsen pairs は元の二生成元を回収でき、Q0 の automorphism を与える。`3 O_3(Q0)=3V9` は characteristic なので各 map は同じ Q2 へ下降する。これにより、各 tag j で phi_j:Q2→Q2 を固定し、raw edge `(q,g)` を

`phi_j(q) * J_Q2(phi_j(g))`

へ送る具体式が使える。新 adapter は marked vertex images と全 generator-edge の整合を記録し、異なる tree representative の選択を tag ごとに隠さない。既存 helpers がこの全 vertex map を既に export したとは読めない。

その後に適用する PB3 正規化は、既存 `_seed_qnorm` の全 filtered 式

`(v_x,v_y) -> (-v_x X, v_y-v_x X B, aug(v_x)),  B=(YX)^(-1)`。

右側の X/XB 積も実際の affine group で行い、その結果の `prod_m(1+u_m)^k_m` の degree0/1/2 と全 Fourier weights `chi_transport[j][a](e)` を取る。これは六 tag、二 Fox components、三 d1／六 d2 monomials を同じ raw edge に結ぶ。Task712 homogeneous map だけから source の lower/mixed 項を推測しない。

aux0..5 は各 tag の上記 augmentation、aux6..7 は独立に渡す `eta=nu=epsilon/18 mod3`。mod3 edge augmentation から18で割った nu を復元してはならない。D=ker(tau)×F3² の同じ `(z,eta)` を全 tag に使う。この実装で `f=sum_a q_a Psi2[a]-kappa Psi1`、`b_aux` を作る。v459 の `c_x=r_x^9,c_y=r_y^9` は全 occurrence の Q2 Fox が零で nu が e_x/e_y なので、型の接続後の auxiliary test は共有末尾2座標を直接拘束する。

F6. **carry/tree と literal readout の最小 consumer。** carry は v546 の rotation-left `v=S(e)k` に変換してから計算する。既存 marked k_X=(1,0,0)、k_Y=(1,1,1) はこの変換前の値であり、そのまま v546 の rotation-left generator 値へ代入しない。五 rows は三つの整数 carry と二つの普通の exponent augmentation。全Q2 vertex、2本の正 generator edge、固定 tree、全54433 chord、独立な五つの tau columns と全 EOF を同じ marking に封印する。108864 edge 値と54433 chord 比較は有限の配列サイズであり、実行時間の約束ではない。

失敗した chord は高々六つの fundamental cycles の線形結合になる。tree paths、cycle の固定 factor 順序、signed coefficients から Schreier word w を作り、v547 の

`w (r_x^3)^(-epsilon_x(w)/6) (r_y^3)^(-epsilon_y(w)/6) [r_x,r_y]^omega(w)`

を同順序で SLP 化する。整数 exponent と omega は product/inverse の SLP 規則で読む。epsilon/6 は整数であり mod3 の逆数ではない。`scratchpad/a0_v2_words.json` の19-relator roster（canonical roster SHA `dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a`）と v459 の固定 r_x/r_y が入力になる。新27-element endpoint table は不要。auxiliary 違反なら先に c_x/c_y を使う。

選択 word の complete P1 truncation を実際の8059行で reduction し、その canonical lift SLP を同じ係数・順序で引き、全 lower-zero と物理値を照合する。この selected-cycle/SLP consumer は読んだ現行 packet/root-seed 系統にはない。現在の `literal_reference` / `literal_word_dag` は v518 に渡す ancestry recipe で、任意の cycle を受ける実装ではない。normalized exponent pair や同一 word の十一 physical slot replay を済ませた出力とも区別する。

F7. **次便の最小完了条件。** full-origin の非零は、同じ現 lambda/owner に対する complete filtered defect、全96776 lower零、raw scalar と physical pairing の一致、現 prefix への独立な pivot 挿入、target 更新、新 lambda の全行／両 target pairing、ordered literal ancestry まで結合して初めて一つの rank rise とする。選択 actor がなければ全4 current root EOF を保存するが、その時点では完全 NONMEMBER としない。

完全な negative には、fresh4-root dual closure の全 actor reductions/FIFO/EOF と各 accepted raw dual の全32280 origins 零、または v548 の authenticated source adapter・8059 kappa等式・二 auxiliary零・全54433 chord identity が必要。旧504 orbit は現 lambda の上限／証明書にならない。positive target remainder零なら、保存した target/pivot係数を v518 の一つの ordered word へ read out し、当該 grade の要求する直接 replay を別途完結させる。

新しい原データの欠品はこの intake では確認していない。route2 に欠けるのは上記の実際の adapter/consumer とその receipt であり、走行済み fixed44 に新入力を要求する理由ではない。root が次 full-origin owner を固定し、fresh current-state loading・全 scalar-array比較・corrected selected-actor materialization の三点を一便で実装することを推奨する。

AUDIT_953_VERDICT: INTAKE_COMPLETE — proceed with fresh full-origin v541 scan plus full-filtered actor materializer; legacy generic materializer_v2 is not a valid unchanged consumer; complete cochain remains a concrete but unimplemented alternative; grade2 undecided.
