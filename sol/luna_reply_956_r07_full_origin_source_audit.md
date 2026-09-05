# Task956 — full-origin refinement の限定ソース監査

監査対象は Tasks954/955 の新しい full-origin consumer と、その実際の受理済み親 JSON への接続。Task953 の第一経路に限定した。数値実行、Python import/構文実行、GAP、network、git、workflow 編集、実装編集は行っていない。workflow と release は root の担当である。

F1. **実際の rank1359 親への接続。** Task950 run33964709359/1 の固定 entry と三つの complete step を静的に照合した。旧 packet instruction は一般の `sha256` seal でなく `rolling_sha256`、step result の `target` は `parent_remainder_sha256 / remainder_sha256 / scalar` だけを持つ plain object である。step manifest の埋込 seal と完全 JSON bytes の SHA は別物であり、両 consumer は後者で前後を接続する。三段目の target scalar は 0、親子 remainder SHA は同一であり、これは正当な target step として受け入れる。producer の受理済み v2 `load_prefix` は保存行・target・metadata を読み付け、旧 offer の再構築・消去を実行しない。checker も旧三段を数値再生しない。両方が現在の lambda を全1359行と受理済み target に直接 pairing する。

F2. **完全 actor と global ActRed。** 旧 offset は `(0,505,1008,1511)`、新 offset は `(2014,3523,5035,6547)`。旧入力 `i=O_a+p` の correction は同じ旧 block の `actor_transitions[p][slot]` に、四つの新 block の `origin_reductions[B_a+44+4p+slot]` を加えたもの。新入力 `i=H_a+p` は同じ新 block の actor transition を使う。新実装はこの式を全 source character の lower と top に一貫して適用する。producer は own v15 の full filtered `_seed_act` を使い、checker は下記の有限27評価を使う。`K_t b_i+T_{2,t}z_i` を作り、homogeneous scalar と lower-to-top scalar を新しい全起源走査に接続してから correction を引く。既存の homogeneous-only generic materializer は呼ばない。

F3. **有限27の独立性と型。** checker は十個の次数≦2 monomial を `F3[C3^3]` の27個の通常群係数へ展開し、実際の六つの tagged actor image による affine 左置換を実行し、十係数を取り出す。展開係数は `prod binom(mu_j,k_j)(-1)^(mu_j-k_j)`、抽出係数は `prod binom(k_j,mu_j)`。受理済み積 `(p,e,k)(p',e',k')=(pp',e+e',sign(e')k+k')` に対し、左 actor の kernel shift は入力 parity `e` による `sign(e)k_actor` となる。source character の transport を用いる Fourier の往復係数は `4=1 mod3` なので1。左置換は augmentation の三乗イデアルを保つため、次数≦2の代表を使うことは正当である。共有8 auxiliary は別成分としてそのまま運ぶ。この手順は `_checker_seed_act` を呼ばず、producer の polynomial multiply/pull を新しい anchor として使わない。accepted group/index inputs は明記された共通前提である。

この anchor は synthetic pure-top の比較だけでなく、**実際に選ばれた canonical input の d0/d1/d2/aux 全部**に適用される。full actor の成分 hash、homogeneous top、lower-to-top、selected scalar、最後の full defect を producer と比較する。追加 canary は次数0のみ・次数1のみの非零入力で、実際の actor2 の kernel translation による top への非零寄与、逆 actor との往復、独立 adjoint scalar を確認する設計である。有限27は actor block の追加 anchor であって、第三の全 pipeline や Lean 証明ではない。

F4. **literal と lower-zero の順序。** `proof_r07_targeted_grade2_direct_relative_literal_compiler_v518.md` §1 の `Act_P(W)=P W P^{-1}`、同 §2 の canonical actor origin に対応して、literal receipt は `t*W*t^-1` を記録する。ActRed の raw event 順を先に保存し、literal 因子の指数を `(3-coefficient)%3` とする。数値上の同類項集約により係数が0となる node も raw event・P1 reference・lift component receipt から消えない。actor 入力の `basis_i` 自身も必ず reference の和集合に入る。受理済み canonical P1 instruction の rolling ancestry、row SHA、literal input SHA に接続する。完全な correction subtraction 後、全 `4*6048+4*18144+8=96776` lower 座標の零を要求し、そこで初めて plain character slice と B を適用する。

F5. **動的全起源走査。** 各状態の lambda から四つ全部の `q_a=B_a^*lambda` と四 actor child を作る。各 character の順序は seed0..43、次に basis_i0..8058 の actor `(1,-1,2,-2)`。四 character 合計129120個の seed/actor scalar 全配列と P1/lower scalar 配列を seal し、checker は first-hit prefix だけでなく全部を再計算して比較する。非零 root は毎回判定し、零 root では配列の零を記録する。P1 cache は一 scan 一 pass の buffered packed contraction、8059行の full decoded lift matrix は作らない。producer の lower 読込は active root ごとに5 body/12 blob、checker は active root をまとめて5 body/12 blob。checker の自分の I/O receipt はこの差を producer の宣言値と区別している。旧 JSON body を次の新 body と同時に保持しない。

F6. **主張の境界。** 旧固定44の `ROOT_SEEDS_ZERO` は集合が現 physical span に含まれるという意味ではなく、lambda が変われば seed の再出現はあり得る。新しい `ROOT_ORIGINS_ZERO` でも current dual closure とその全起源試験は未実行であり、grade2 NONMEMBER は導かない。cap32 は運用上の上限で、全 physical image の次元上界ではない。source-only の12092や過去の504を新しい停止根拠にしていない。MEMBER_CANDIDATE に到達しても新しい literal 全 word replay、他 grade、PB4/full A0 完成は別のままである。`cross_checked=false; verified=false` を保つ。

F7. **新しい physical/target/separator。** producer の `append_step` は selected `q(d)=lambda(Bd)` が非零であることを直接確認し、既存の挿入順で physical 消去し、未使用 lead の normalized row を一つ加える。target は `r'=r-r[lead]*normalized` であり、receipt の `parent_remainder-child_remainder=target.scalar*normalized` と符号が一致する。checker は own physical arithmetic で同じ payload を再構築する。新しい lambda は挿入順の逆向きに構成し、**構成終了後の同じ lambda** で全旧行と新行を再走査し、親 target と新 target の両方への値1を確認する。DERIVED rho2 は base・seed30・seed34・packet-step1/2/3 の六つの受理済み target identity と、新しい target step 数を明記する。original rho2 の新しい直接読込とは主張しない。

F8. **保存と実際の再開の接続。** scan と step は全 payload・manifest の書込、同期、directory publication を終えてから HEAD を進める。step の publication と HEAD 更新の間に cooperative resource stop を挟まない。HEAD は owner/source/runtime/start/P1 index/packet と state head、complete step manifest、current scan manifest を固定する。再開は保存済み scan 全配列・選択・materialization ancestry・normalized row・target の seal/metadata を読み、完了済みの full scan や insertion arithmetic をやり直さない。current scan は pivot 追加で必ず無効になり、cap 判定より先に新しい現状態の full scan を保存する。途中 resource stop なら complete prefix を保った UNKNOWN_RESOURCE とし、初期化中の停止は別 diagnostic に残す。HEAD 外の pending/orphan/numbered tails はデータに数えない。checker は受理済み rank1359 から**新しい committed scan と step だけ**を再生し、全 payload と terminal HEAD を比較する。

F9. **focused canary の静的確認。** 実際の parent JSON layout の正例と拒否例に加え、producer は full filtered production helper の lower-to-top 非零寄与を使い、homogeneous-only consumer では一致しないことを要求する。durable fixture は実際の `append_step / load_prefix / load_scan` を通し、active character が1から3へ変わること、最後の cap 後の scan、scan/step が HEAD より先に存在すること、保存 bytes の再利用、再 seal した wrong owner の拒否、full scalar array 後端の改変拒否を確認する設計である。checker は次数0・1の有限27 canary と全配列後端の比較を持つ。これらは今回この agent では実行していない。新しい actual GHA cap1→same-output resume cap32→checker の数値結果は、この判定時点では未実行である。

F10. **最終ソース限定判定。** 下記の全ソースと retained helper の今回の呼出箇所を読んだ範囲で、新しい full-origin consumer を妨げる数学上／source 上の必須修正はない。root の runtime gate に進めてよい。workflow/source-release 運用の独立確認は root の担当で、この返信は GHA 成功や今回の数値照合済み判定を代行しない。root から裁定2125による upstream の限定照合済み受理を受けたが、それを新実装の実行結果に繰り上げない。

| 対象 | bytes | SHA256 |
|---|---:|---|
| `search/d972_r07_full_origin_refinement_v1.py` | 97806 | `d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa` |
| `search/check_d972_r07_full_origin_refinement_v1.py` | 75083 | `1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2` |

この判定はこの bytes に限定する。以後の変更には、その差分の再確認が必要である。今回は指定返信だけを作成し、v220 は root の更新に委ねた。

AUDIT_956_VERDICT: PASS_STATIC_SOURCE
