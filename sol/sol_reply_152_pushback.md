# Sol 便 152 返信 — checkpoint worker v2 完成・GHA 発火指示

受信便 `ops/inbox_codex/sol_task_152_pushback.txt` は先頭から末尾まで読んだ。受信 SHA-256 は

`b310e11e408084d1b120b67c05b0af52614fdfb1f36066e16d89f1248b9a2756`

である。以下、受信便の §1、§2、§3 の順に回答する。

## 1. 資源差し戻しを受理し、checkpoint 可能な worker v2 を実装した

差し戻しは正しい。Linux/GAP runner は blocker ではなかった。真の blocker は、GAP/ACE が一つの extension cell を処理している途中の内部状態を、論理 cursor だけでは復元できないことだった。

これを、Python producer とその全 GAP/ACE 子 process を DMTCP で一括保存する方式に置き換えた。したがって次の六箇所は、後付けの粗い cursor ではなく、heap、stack、open file position を含む process image として lossless に保存される。

1. `canonical_table_relabel`
2. `Aut(H)`
3. extension class
4. marked orbit
5. fp-order の `MTC` / `Size`
6. 972-fiber scan

外部 supervisor は時間切れ時に `dmtcp_command --kcheckpoint` を使い、協調 checkpoint が完了した世代だけを封印する。中途半端な process image、heartbeat、論理 cursor には再開権限も終端権限も与えない。

### 1.1 凍結した実装

| file | SHA-256 |
|---|---|
| `.github/workflows/d972-dovetail-v2.yml` | `9febec70ab87c5cb55920dc7e29acca9818cd706ccc097813b0b615444eb6516` |
| `search/d972_dovetail_worker_v2.g` | `7367780a6c11fa65aeafdf8214065d881141b7461d2d71eadac8db6ea4bd98f0` |
| `search/d972_dovetail_producer_v2.py` | `8bd965efa7c5564478b277a1649dd2dfaa01f022619c99590de95be92bbed5dc` |
| `search/check_d972_dovetail_v2.py` | `46445ae5cbea96c87b3548e1df227fc546d895a0d64f3c0a7fd9c74cf8a6e4b2` |
| `search/d972_dovetail_manifest_v2.json` | `dbee89d8273d286aad3c4fe8861e971e163f9b67ef1c9157f0075a16aa315751` |
| `search/d972_dovetail_state_schema_v2.json` | `85acbb14729ddfec366564b8663cdb085ca21bf329a386fca616bef2c23cae78` |

DMTCP contract SHA-256 は

`673ad777bd5de76077db25cc7744622783218c0323ba428cec1bd790e1234e57`

であり、v2 code/input binding set SHA-256 は

`eacadb0342e9158d2fbc57cdcbf938e8a98adb4c5113f7706a7e2d10e1ace28c`

である。凍結済み v1 数学 worker の実ファイル SHA-256 も期待値も

`323d18de4fadcf4561222995f5b6590bb560cd617048d2e9b54049ae3eea9efd`

に一致する。

### 1.2 再開契約

- 各世代は `.d972-runtime/ckpt/gNNNNNN` に保存し、DMTCP image、restart script、producer state、atomic write 中の `*.tmp`、checker/ledger をすべて列挙して hash 封印する。
- 親 envelope hash を次世代へ結び、最新の有効な predecessor artifact 以外は拒否する。
- source commit、workflow 内容、全 code/input hash、DMTCP/GAP/Python の正確な version、`ImageOS`、architecture、workspace realpath、launch command、allowlist 済み環境を照合する。互換しない再開は fail closed である。
- checkpoint 対象は `env -i` で起動し、credential/token/secret を process image に入れない。`HOME` と `TMPDIR` も campaign 内に隔離する。
- producer/GAP subprocess 自体には wall timeout を置かない。外部 slice 終了だけが協調 checkpoint を要求する。
- 前世代 envelope は restore 後も inflight として保持し、新世代の封印成功または自然完了後にだけ除去する。
- suspended image は常に `UNKNOWN/RESUME` であり、A/B のいずれの権限も持たない。

### 1.3 独立 checker

較正 gate の旧 v1 経路には、production で必ず停止する stale な `case_ok = False` があった。v2 はこれを隠さず置換した。

新 checker は producer/worker の較正 helper を読まず、checker 内で生成した GAP script により、固定した `K9 × PSL(2,8)` base、六 coset marking、Q presentation の全単射を再構成する。その上で式 (3.3)、(3.4)、surjectivity、settlement を literal に再評価し、`k=1` base と split `C2` / 二つの `Q8` diagonal model について、受理された全 `(m,D-index,target,settled)` 行と各 972-vector を保存する。

さらに Python 側で全 8 個の F2 cohomology triple と transvection invariant を独立列挙し、非機械的な唯一の前提 `sol/sol_reply_143_typedfiber.md` §5.4 を SHA-256

`ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a`

で pin する。独立値、producer raw 値、凍結期待値の三者が完全一致しなければ campaign は開始しない。raw row/vector、model label/order、Q relator、target order、生成 script、stdout/stderr も receipt に結合し、PASSED state を書く同じ atomic write の中で再検査する。

### 1.4 A terminal の唯一の条件

候補が見つかっても outer cursor は進めず、その exact shadow の独立再構成が完了するまで保持する。A を出せるのは次の全条件が同時に成立するときだけである。

1. 一つの eligible isolated refinement の 972-fiber を全走査した。
2. outside target に zero fiber がある。
3. producer と独立 checker が同じ candidate canonical digest、shadow、zero fiber を返した。
4. calibration receipt、producer ledger の一意な行、state hash、source/code/DMTCP binding が一致した。
5. pending process envelope が存在しない。
6. v2 postcheck 後に `final-v2-completion.json` が生成された。

これにより便 151 の (2.2) が成立し、指数 3 の二択から `P_M=A_ar`、従って 648 元は全部 A 型と結論できる。v1 が途中で A state を書いた直後に checkpoint された場合も、pending envelope が優先するため A には昇格しない。

この workflow は有限 prefix の all-pass、cap、timeout、nontermination から B を出さない。B は全 isolated refinements にわたる compatible survival という別の全称証明を要するからである。

## 2. Conjecture 5.1 の stale-premise 監査

明示的な監査結果は次のとおりである。

`CONJ51_WORKSHOP_STATUS=FULLY_PROVED_EFFECTIVE_LEAN_ONLY`

`TASK151_STALE_OPEN_PREMISE=NO`

正本 `docs/notes/p1_corpus_index_v1.md` と裁定 550/559/908、さらに ruling 1126 を照合した。当工房における有効な定理は、すべての `n >= 3` について

`Ih_(K^(n)) : G_Q ->> GTSh(K^(n),K^(n)) = GT(K^(n))`

であり、未了なのは Lean 形式化だけである。「一般 n は open」は stale である。

便 151 の推論は、その stale 前件を load-bearing に使っていない。A 車線の有限分類は Conj. 5.1 から独立であり、B 車線の `X_s` 上の像も直接計算されていた。B に昇格できなかった理由は Conj. 5.1 の未証明性ではなく、明示的な非 dihedral isolated refinement

`L = M intersect N_5^cyc`

に対して `X_s` が cofinal でないことだった。

同時に、完全証明済み Conj. 5.1 だけから 972 屋根の B は従わない。Conj. 5.1 の量化域は pure dihedral poset `{K^(n)}` である一方、Cor. 5.4 の B 証明書は `M` 以下の全 isolated refinements、特に上の非 dihedral `L`、にわたる compatible lift を要求するからである。従って

`CONJ51_DOES_NOT_DECIDE_GLOBAL_972_ROOF_A_B`

である。

## 3. 972 屋根 A/B と発火指示

A/B の真理値が二択であることは維持する。しかし Linux/GAP/DMTCP campaign をまだ一度も実行していない現時点で A または B を宣言することは、受信便の不変条件「捏造・過大格付けはしない」に反する。本便は §3 自身が指定した、実装完成直後の発火 handoff である。第三の数学的型を追加する主張ではない。

**この workflow を発火せよ:** `.github/workflows/d972-dovetail-v2.yml`

初回 dispatch は次で固定する。

- ref: 上の六ファイルと各 SHA-256 を含む commit
- `resume_run_id`: 空文字
- `slice_minutes`: `240`

現在の checkout の旧 HEAD は六ファイルを含まないため、その SHA を source commit として使ってはならない。工房で六ファイルを commit した後、その commit を ref にして発火すること。私は commit、push、workflow dispatch を行っていないので、現時点の run ID はない。

workflow は Ubuntu 24.04、job timeout 330 分、slice 240 分で走り、`31 */6 * * *` の schedule が最新の有効 artifact だけを自動再開する。手動再開する場合は `resume_run_id` を空のまま自動選択させるか、最新 run ID と完全一致する値だけを指定する。

発火後の読み方は次のとおりである。

| workflow outcome | 数学的裁定 | 次の動作 |
|---|---|---|
| `A_WITNESS_CROSSCHECKED` かつ有効な `final-v2-completion.json` | **648 は全部 A 型** | terminal receipt を収蔵する |
| `UNKNOWN_RESUME` | A/B 未決。数学的結論なし | 最新 artifact から直ちに継続する |
| `STATE_STOP`、`CALIBRATION_STOP`、互換性/再開失敗 | 証明なし | 原因を修理し、同じ証明義務を再開する |
| B | この A-semidecision workflow は発行しない | 全 isolated refinements の survival 定理が別途必要 |

工房から返してほしい receipt は、run ID、実際の source commit SHA、artifact ID、workflow outcome、A の場合は final seal と terminal witness の hash である。

## 4. 実行前監査と格付け

実行済みのローカル検査は次のとおりである。

- `python -B search/d972_dovetail_producer_v2.py --self-test`: PASS。binding と contract、一時中断、accepted shadow、taskless/null-radices を検査した。
- `python -B search/check_d972_dovetail_v2.py --self-test`: PASS。v1 negative 11 件、envelope hash、親 hash、独立較正 positive、再封印 tamper negative 2 件、partial checkpoint の terminal authority false を検査した。
- JSON parse と canonical contract 再計算: PASS。
- workflow YAML parse: PASS。YAML 中の Python heredoc 11 本も抽出後 compile PASS。
- 六ファイルに対する `git diff --check`: PASS。
- 最終の read-only 敵対的監査: blocker/high finding なし。

ただし、この Windows session のローカル GAP は起動前に `couldn't create signal pipe, Win32 error 5` で停止する。そのため production の POSIX DMTCP restart、生成 GAP 較正、実 972 campaign はまだ走っていない。workflow は発火直後に stateful DMTCP restart smoke と実 GAP worker-v2 smoke を行い、失敗時は campaign に入らず fail closed する。

従って現時点の正確な格付けは「実装候補、静的/self-test PASS」であり、campaign 結果はまだ cross-checked でも Lean verified でもない。A の格付けは上記 Linux workflow の独立 checker と final seal が成功した後に限る。

## 5. 機械可読結論

```text
TASK152_FULL_MAIL_PROCESSED=YES;
RUNNER_BLOCKER=NO;
NONCHECKPOINTABLE_CELL_BLOCKER=CLOSED_BY_DMTCP_WHOLE_PROCESS_V2;
SIX_INTERNAL_STAGES_LOSSLESS_CHECKPOINTED=YES;
INDEPENDENT_CHECKER_V2=IMPLEMENTED;
A_TERMINAL_FAIL_CLOSED=YES;
B_FROM_TIMEOUT_CAP_OR_NONTERMINATION=FORBIDDEN;
CONJ51_WORKSHOP_STATUS=FULLY_PROVED_EFFECTIVE_LEAN_ONLY;
TASK151_STALE_OPEN_PREMISE=NO;
CONJ51_SCOPE=DIHEDRAL_POSET_ONLY;
CONJ51_DOES_NOT_DECIDE_GLOBAL_972_ROOF_A_B;
IMPLEMENTATION=READY_FOR_LINUX_GHA;
WORKFLOW_TO_FIRE=.github/workflows/d972-dovetail-v2.yml;
INITIAL_RESUME_RUN_ID=EMPTY;
INITIAL_SLICE_MINUTES=240;
WORKFLOW_DISPATCH_PERFORMED_BY_SOL=NO;
CURRENT_RUN_ID=NONE;
A_B_TERMINAL=AWAITING_GHA_RECEIPT;
```

## 6. 継続台帳（旧型への逆戻り禁止）

2026-08-17 の直接指示を受け、以後の A/B 判定では次を不変条件とする。

- 「細分が一つもない」路線の正確な証明義務は、細分一般の不存在ではなく、固定した outside shadow を壊す bad refinement の不存在である。
- fake を仮定すれば、指数最小の bad refinement を一段の B4-stable chief factor `K < H <= M`（`H` では survive、`K` では fail）へ圧縮できる。この chief-compression だけは成立している。
- 全 chief factor でその一段の marked/coface/hexagon/pentagon lift を吸収する一様定理は未証明である。従って、旧型でも訂正版でも `NO_BAD_REFINEMENT` はまだ発効していない。
- rho は current rho
  `[-6,-5,-3],[3],[5],[-3,-2,-1],[-5,-4,-1],[1]`
  を正とし、legacy inverse-order rho は使用しない。
- `M=K^(9) intersection N_S4` は B3/PB3 側の named target であり、`M.B4_stable` は型誤りである。B4-normal refinement/core は五つの A.18 coface images から作る別対象として扱う。
- 固定 6/158 object での nonidentity は、semantic/core gate 後に A へ進む一方向の witness になり得る。固定 object の all-pass は全 refinement survival、B、又は Ihara 結論を含意しない。
- B の終端は、訂正版の型で全 bad refinements を排除する一様定理、又は同値な compatible profinite lift の明示構成に限る。有限 prefix/all-pass、timeout、cap は B に格上げしない。

この節は live continuity pin であり、最終 A/B receipt が得られた時点で run ID、commit SHA、artifact hash、独立照合結果とともに終端報告へ統合する。

## 7. 厳密 6/158 の終局裁定（B4 専用）

2026-08-17、B3 路線を保留し、現行 rho と正しい B4 coface/core の型で 6 生成元・158 relator 窓を再裁定した。

- 158 relator は、意味論 bridge が完了した場合に限り、固定商
  `U_M=K(0,5)/<<five A.18 coface images of C_M>>`
  における pentagon defect を扱う。実際の defect は
  `f(x45,x34)^-1 f(x12,x15)^-1 f(x23,x34) f(x45,x51) f(x12,x23)`
  であり、condition (I) を独立再生した後にだけ reverse-rho norm と同一視できる。
- exact 158 all-pass の最大の無条件結論は `LOCAL_U158_PENTAGON_ONLY` である。これは finer B4-normal refinement での恒等式、補正代表の存在、compatible profinite lift、genuine、B4-B のいずれも含意しない。
- 理由は商写像の向きである。`K <= L_M` なら `G/K -> G/L_M` なので、defect が `L_M` に入ることから `K` に入ることは従わない。さらに finer level では旧 f そのものではなく `f*c` という補正代表を許すため、必要なのは hexagon 二式と pentagon 一式を同時に解く correction-lifting equation である。
- 従って 158 all-pass を B4-B 証明路線として使う案は終了する。B4-B の残る本命証明義務は、全 B4-stable chief step でこの補正方程式が解け、解集合の遷移が compatible/onto になること、又は同値な `Out^]_5` の明示 profinite lift である。
- 一方、semantically typed な有限像で 158 norm の nonidentity が得られれば A 側の有限障害になり得る。この一方向の用途のため、GHA direct 6/158 run `31955279723` は継続するが、all-pass を B に格上げしない。

この裁定により、「厳密 158 がそのまま B を証明するか」という問いは **NO** で閉じた。A/B 本体は B4 correction-lifting / `Out^]_5` 路線で継続する。

## 8. 旧 rho-tail 158 の意味論棄却と raw A.18 版への交換

§7 で「意味論 bridge が完了した場合」と留保した点を有限証明書で裁定した。結論は **bridge 不成立** である。従来の

\[
N_\rho=\langle\!\langle R_0,B_0,\rho(B_0),\ldots,\rho^4(B_0)\rangle\!\rangle_{F_6}
\]

と、論文 A.18 を文字どおり入れた

\[
N_{A18}=\langle\!\langle R_0,A_{123},A_{234},A_{12,3,4},A_{1,23,4},A_{1,2,34}\rangle\!\rangle_{F_6}
\]

は同じ正規閉包ではない。

- `search/d972_b4_158_a18_rs_separation_v1.py` は正本 JSON から現行 rho-tail 158 本を再構成し、正則 `C2^5` transversal による 161 Schreier 生成元・5056 relator を作る。
- その exponent quotient over `F3` で、5056 本すべてを消す線形汎関数が、literal A.18 の 140 本中 41 本を消さない。
- 最初の witness は map `12,3,4`、seed row 5 で pairing は `1 mod 3`。従ってこの A.18 relator は `N_A18` に属するが `N_rho` には属さず、`N_A18` は `N_rho` の部分集合ではない。
- producer helper を共有しない `search/check_d972_b4_158_a18_rs_separation_v1.py` が全 5056 current rows と全 140 raw A.18 rows を再構成し、`B4_A18_PRESENTATION_SEPARATED_BY_FINITE_RS_QUOTIENT_CROSSCHECKED` を返した。producer receipt SHA-256 は `7514eee4727e7ca074665bcdd4ba783faaeabcb9ca9b007ef9eed690dffa6001`。
- 既存 GHA run `31956732848` の有限 3-group receipt も別経路で class 2/3 とも 47 本の raw A.18 defect を返し、最初の map/seed は同じであった。

従って旧 rho-tail 158 と、それを使った run の all-pass / defect を B4 A/B の証拠に使用してはならない。§7 の `31955279723` 継続記述はここで撤回し、旧型 run は判定対象から除外する。

交換後の正しい固定対象は、18 K05 relators と五つの literal A.18 images（140 本）からなる raw A.18 presentation、canonical relator digest

`783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305`

である。評価語は condition (I) を仮定しない PENT-FORM' defect

\[
\widetilde D(f)=f(x_{45},x_{34})^{-1}f(x_{12},x_{15})^{-1}
f(x_{23},x_{34})f(x_{45},x_{51})f(x_{12},x_{23})
\]

の 972 本であり、digest は `32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef`。その `C2^5` Schreier relator digest は `db25c0268cdc774ef3205c9c1d1cf62cd013e6daaf73cf959e7972af5b3082bb`、972 defect の Schreier digest は `418e88934210e726de0e7e1f375bac2e6151f465be84f913884c58129217259c` である。

この交換は旧158の型誤りを終端させるが、それ自体は A/B の終端ではない。以後の有限障害探索は `search/d972_b4_u_a18_anupq_v1.g` と独立 checker でこの三つの digest を fail-closed に固定して行う。

### 8.1 GHA handoff

- source commit: `c02288d266f533064c133bb0baeb2612ecfe62d8`
- branch: `sol/d972-dmtcp-provision-v420`
- production run: `31959472442`（raw A.18、p=3、classes 2/3/4、240分 cap）
- producer selftest run: `31959484380`（30分 cap）
- 旧 rho-tail SAT run `31955880120`: 意味論棄却により cancel request 済み

いずれも既存 `.github/workflows/gap-run.yml` を無変更で使用した。production receipt は artifact 回収後に独立 checker で全 presentation relator と全972 defect を再生し、run ID・artifact SHA とともに追記する。

## 9. 再実行禁止路線台帳（記憶圧縮後も有効）

2026-08-17 の研究者による再確認と過去 receipt 監査により、次の族は既実施・否定済みとし、係数体や有限次数を変えただけで再提案・再発火しない。

1. **7進 verbal / Zassenhaus 有限段族**：有限 prefix の all-pass は cofinality を与えず B にならないことを `sol/luna_reply_152_b4_7adic_verbal.md` で監査済み。
2. **一次 twisted Alexander / Fox 有限商族**：`search/d972_b4_u_alexander_v1.py` の F19 走査は 220 個の de-duplicated character すべてで Fox-relator rank `160`、translation nullity `1`、nontrivial defect pairing なし。係数体を F7 に変えた raw-A.18 first-order Fox 案も同族なので中止し、終端路線に算入しない。
3. **有限 p-class / 有限次 Magnus の単な延長**：有限段の all-pass は B ではなく、新しい終端含意がない限り繰り返さない。

`ROUTE_EXCLUSION_7ADIC_FIRST_ORDER=PERMANENT;`

`ROUTE_EXCLUSION_TWISTED_ALEXANDER_F7_F19=PERMANENT;`

`NO_COEFFICIENT_FIELD_REBRAND_AS_NEW_ROUTE=YES;`

## 10. B4 対偶の joint-correction 文献ゲート（進行中）

独立 Luna 監査 `sol/luna_reply_152_b4_absorption_literature_v1.md`
（本文 checksum `BC986906A6812DF133BD07C97208C3AF70B57A545C3D418369E0C17AF3145100`）と
原論文ページ画像を照合した。

- Lochak--Schneps--Scheiderer (Invent. Math. 127 (1997), Theorem 2 / Proposition 3,
  pp.573--575) は GT の三関係を非可換 `H^1` の cocycle/coboundary 形にする。
  ただし用いるのは `C2`、`C3`、`C5` に対応する三つの別々の semidirect product と
  別々の補正元 `g,h,k` であり、同一 chief kernel 元による joint correction 定理ではない。
- 同論文 p.574 は、有限商で得る三条件の intersection は真の `GT-hat` 像より大きい
  candidate になり得ること、cofinal tower を降れば有限段で真の像になるが停止段数が
  不明なので algorithmic ではないことを明記する。これは finite all-pass を B に昇格
  できない現象の一次文献上の形である。
- Furusho, *Pentagon and hexagon equations* の characteristic-zero/pro-unipotent 定理は
  finite/profinite chief absorption へ移植できない。同論文 Question 14 (pp.555--556) は
  full profinite の pentagon-to-hexagon 類似を未解決問題として残す。
- 研究者の Desktop 文献リスト中 `LochakSch.pdf` は、universal
  Ptolemy--Teichmuller groupoid を `alpha^4`, `beta^3`, `(alpha beta)^5` と二つの
  commutator relation で提示し、GT 作用が五関係を同時に保つことを証明する。従って
  joint residual の正しい候補器は無根拠な `A5/S5` module ではなく、この groupoid の
  finite-coefficient relation/deformation complex である。ただし presentation completeness
  は complex の exactness/contractibility を含意しない。

従って現時点の厳密な B4 対偶 target は、第一 bad chief step `K < H`、`V=H/K` に対し、
実 A.18 residual がこの typed relation complex の cocycle であり、その class が零であることを
示すことである。abelian `V` では Fox/relation differential、nonabelian `S^t` では
outer-action/pointed obstruction に分ける。補正後の marked onto、charming、isolated の保存も
同じ補題に含める。一般の Gaschutz/Frattini lifting は生成元の onto 保存だけであり、この
joint relation lifting を与えない。

独立型監査 `sol/luna_reply_152_b4_joint_cocycle_audit_v1.md`
（SHA-256 `8D2408DDC8958A93738237C924AA22254745A4AA91A8D55B037C5F424D157DEF`）で、
この target をさらに次の形まで限定した。A.14/A.15 の二残差は PB3 chief fiber、A.13 の
pentagon 残差は PB4 chief fiber にあり、五つの A.18 写像が chief pair `K < H` を保存することを
先に示さない限り同じ係数空間には入らない。正しい一次補正写像は

\[
d_1:C^1_{\rm gen}\longrightarrow
 V_{3,14}\oplus V_{3,15}\oplus V_4
\]

という typed Fox/Jacobian である。第三成分を `N_5 lambda_5` と書けるのは、五 coface の
pentagon derivative との同一性を別途証明した後だけである。さらに obstruction class と呼ぶには
relation syzygy differential `d_2`、`d_2 d_1=0`、実残差の `d_2`-closedness が要る。
従って `p` が 30 と互いに素なら `H^2(A5/S5,V)=0` という通常の averaging は、個別の有限群
cohomology を消すだけで、この typed joint cokernel を消さない。全 chief type を吸収する定理は
依然未成立だが、欠けている写像・exactness はこれで明示された。

### 10.1 compactness / compatibility の訂正

B4 正本の Corollary 3.13（原 PDF p.38 をページ画像で照合）は、charming shadow が genuine
であることと、**全** `K in NFI_PB4(B4), K <= N` で survive することを直接同値にしている。
B3-gentle 正本の Corollary 5.4（pp.28--29）も同型であり、各 fiber を有限非空集合とし、
交差で directed な refinement poset 上の inverse limit が非空であることを compactness から得る。

従って過去便にあった「各有限 fiber の非空性に加えて transition の全射性を別途証明する必要がある」
という要求は過剰であり、ここで撤回する。必要なのは reduction maps の well-definedness と、全 finite
refinement での非空性である。後者を否定する一つの `K` が A、全称的に保証する chief-step absorption
が B になる。これは B の証明義務を正確に狭めるが、有限 prefix の all-pass を全称へ変えるものではない。

### 10.2 A-semidecision GHA repair handoff

- 旧 run `31954113424`（source `a422175b3b66b91dfbd54188e5b7688569b6936e`）は
  `STATE_STOP independent k=1,2 lossless calibration reconstruction UNKNOWN: GAP failed with exit 1`
  で終了した。calibration receipt は
  `5a261115350f1f4cec4e500346b657f65e5dc44f8f2ee4b08d29d3eba69ea858`。
  A/B 結果ではない。
- calibration の旧 ambiguous quotient と opaque GAP exit を checker-only で修理した。
  `python -m py_compile`、checker selftest、failure-receipt fixture、`git diff --check` は PASS。
- repair commit: `d8cc144215921e21a0fa393e0fd0624c7b271eb1`
- pushed branch: `sol/d972-dmtcp-provision-v420`
- repaired workflow dispatch `31962113025` は campaign 前の GAP-worker-v2 smoke で
  `frozen v1 worker digest drift: f9ad3f8f71dc5af3d20dbef66dc6a25c79a50393be55767c0fb9f077d46994e8`
  と fail-closed。原因は commit `0bbbedfe` が `D972Can9` の内部型を flat から 3 組へ直し、
  serializer で再 flatten して外部 key を保存した後、v2 の凍結 SHA binding が旧値のまま
  残ったことにある。gate を外さず、意味保存差分と全 contract digest を Luna が再監査中。
- 再束縛監査後、`worker_v2.g` と `manifest_v2.json` のみを commit
  `d126830d57e93c8e7f9a420b7f40137aa395829e` に限定追加した。新 v1 binding は
  `f9ad3f8f71dc5af3d20dbef66dc6a25c79a50393be55767c0fb9f077d46994e8`、
  canonical v2 contract は
  `1044311458e44b0e7e0639e0bde2e39ad546946b74f09aa85d4dca471085fac1`。
  producer/checker selftest、11 negative cases、calibration tamper cases は PASS。
  DMTCP 再 dispatch は run `31962852940`（workflow YAML 無変更）。

raw-A.18 finite-image shelf run `31961726889` は packages を含めて起動したが、
`Error, A18 finite D-tilde digest drift` で fail-closed。これは A/B 結果ではない。digest
ロジックと数学データのどちらの drift かを独立監査した結果、source/word/raw-A.18/presentation
の全固定値と独立 Python の 972 行は PASS し、GAP producer の再計算だけが shelf 探索前に
食い違うことを確認した。期待 digest の repin や gate 緩和は行わない。

最初の相違行を採取する versioned 診断三点を commit
`aeb47d4797f40e5a84c63a0c0a79e67ea662faa8` に限定追加し、GHA run `31962716634` を dispatch。
fixture は 972 行、1,142,103 bytes、SHA-256
`aab097b31c2e4a85aab28c6ebb5f3853d7b5b99ef4eb8b331a1faf6626d4bfa6`。
Python 独立再構成は `dtilde_sha256=32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef`
で PASS。GAP はローカル実行していない。

run `31962716634` は row 1 の frozen-fixture contract で直ちに停止した。row 1 は空語で、
Python の canonical JSON は `[]`、SHA-256 は
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`。
GAP では空 list が `IsString([])=true` も満たすため、generic encoder が `IsString` を
`IsList` より先に判定して `[]` を `""` と直列化する。raw relator 群は空語を含まないため
それ以前の digest gates は通り、972 norms の最初の空語でだけ全体 digest がずれた、と
全ログが一致する。数学的な \(\widetilde D\) 語の不一致ではなく canonical serializer の
型曖昧性である。v1 は保存し、signed-word 配列専用 serializer を用いる versioned v2 repair を
Luna が実装中であり、generic gate の緩和や期待値 repin はしない。

## 11. 2026-08-17 早朝の継続台帳（A/B 未決のまま進行中）

### 11.1 規約修正後の Lochak--Schneps 必要条件

paper 積 (AB\leftrightarrow) GAP 積 `B*A` を全積に適用し、
`tau(y)=y^-1*x^-1` を GAP の `X^-1*Y^-1` とした
`search/check_ls_d972_v3.py` は frozen 972 行を全再生して
`PASS_LS_ALL_972` を返した。旧 48-failure は規約負例であり撤回する。
したがって LS 条件から fake witness は得られない。一方、必要条件の全通過は
genuine/B の証明でもない。実装 SHA-256 は
`1e3f373c0ff59c17139c2956a359b9cbce15044e3c028e37e3422f6ad535ae98`、
commit は `bf1a23629ae28a99411543f5af6443d5b2f79e72` である。

### 11.2 raw-A.18 direct (p=2) の有限負結果

versioned producer/checker を commit
`565ee183af983a3d4bf67fd1374e4259055873a5` に限定して push し、GHA run
`31969798235` を実行した。run は success、artifact ID は `9269481348`、
artifact receipt SHA-256 は
`cf849f811b0dc94d73483dd70990b123db569444d4f585dcb11490ac8109114b`、
producer log SHA-256 は
`980f8ebeed03a907d671dcd72004c1523aa6eb92f70358e0023856fc9d6151a2`。

class 1--4 はすべて同じ位数 \(32\) の \(C_2^5\) 商で、158 raw-A.18 relator と
972 個の \(\widetilde D\) 行はすべて恒等元だった。重い汎用 PC checker は使用せず、receipt の
relative orders `[2,2,2,2,2]`、全 power/conjugate relations、六生成元像
(e_1,\ldots,e_5,e_1+\cdots+e_5) を独立に読み、
\(\mathbf F_2^5\) 上で全 158+972 語を再評価して
`C2^5_LINEAR_REPLAY_PASS` を得た。

これは固定 raw presentation の有限 all-pass に過ぎない。`H_A` には typed
`PB4 -> H_A`、B4-stable kernel、induced `N_PB3=M`、補正 fiber、outside-648 label が
ないため terminal B4 A/B へ昇格しない。この STOP 監査の SHA-256 は
`863d2bc70770c361f1f667a2ae7ffe596d813e034346314a262e95a18778c50c`。

### 11.3 K(0,5) / raw-A.18 bridge の最初の破綻点

`d972_b4_marity_phaseb1_direct_v4.g` は full `PB4fp` を作るが、
`Delta_4^2=(s1*s2*s3)^4` を殺した `K05fp` と quotient map を作っていない。
最初の 18 行の一方向評価だけでは raw 158 presentation と K(0,5) の同型、逆 Tietze map、
B4 共役保存、`ker(joint)=M` は従わない。従って direct raw (p)-quotient を typed refinement
として扱う bridge は STOP。監査
`sol/luna_reply_152_a18_k05_pb4_bridge_v1.md` の SHA-256 は
`5cbfdfa5c4a7c2d3e893441e7bd14bc9f3175a3a22f0d95cb2b8c53f6b47126f`。

### 11.4 実行中 GHA

- whole-process DMTCP A-semidecision: run `31962852940`, source
  `d126830d57e93c8e7f9a420b7f40137aa395829e`。step 12 の 240 分 slice が進行中。
  schedule successor `31966124887` は pending であり、重複 dispatch はしない。
- convention-correct Phase-A v3: run `31967434065`, source `170a38ffdfbdfc5fb6a373388aa11bf7c0af3022`、進行中。
- N3 Phase-B1 v2: run `31967437253`,同 source、進行中。
- explicit 20-block direct-v4: run `31969443502`, source
  `bf1a23629ae28a99411543f5af6443d5b2f79e72`、進行中。

いずれも receipt 回収前であり、timeout / finite all-pass / numeric split だけから A/B を出さない。
ローカルの shadow-atelier 関連 GAP/Python process は 0。以後もローカル GAP を並列起動しない。

### 11.5 小位数 relative refinement の再設計

order-8 v1 の raw cursor `Aut(H)^2 * H^158 * H^2` は有限だが天文学的であり、
計算路線として却下した。現在は `Q0=G9 x PSL(2,8)` の直積構造、outer action、
extension class/H2、既知の index 2/4 parents を使い、実際の extension classes のみへ圧縮中。

order-9 C3 v2 は dispatch 前監査で、A.18 triple が paper 順
`[x12,x23,x13]` のまま canonical PB3 generator 順 `[x12,x13,x23]` に渡されていること、
および `N_PB3=intersection phi_i^-1(N)` の kernel equality を検査していないことを検出した。
従って v2 は不採用・未 dispatch。global PB4 character の diagonal C9 と四 deletion を
区別した v3 を再設計中である。

```text
CONTINUATION_20260817_EARLY=RECORDED;
LS_CORRECT_CONVENTION_ALL_972=PASS_NECESSARY_ONLY;
RAW_A18_P2=C2^5_ALLPASS_FINITE_NONTERMINAL;
RAW_A18_TYPED_K05_BRIDGE=STOP;
K8_RAW_CURSOR=REJECTED_ASTRONOMICAL;
K9_V2=REJECTED_BEFORE_DISPATCH;
LOCAL_GAP_PROCESS_COUNT=0;
A_B_TERMINAL=STILL_RUNNING;
```

### 11.6 order 3 / order 8 圧縮案への Sol 差し戻し

Luna の C3 v4 は `S3=C3 semidirect C2` の parity 係数について、`C9 semidirect C2`
由来の carry cocycleを明示し、trivial/parity の作用候補を紙上で縮約した。しかし terminal
cell には採用しない。第一に実装が実際に走査する cocycle domain は `|S3|^3=6^3=216`
triples であり、報告の `18^3` は誤記である。第二に permutation module `F3^3` を
`H1(M,F3)` 全体と同一視した記述は一般に正しくない。必要な完全性は
Hochschild--Serre five-term sequence

```text
0 -> H1(Q,F3) -> H1(B3,F3) -> H1(M,F3)^Q
  -> H2(Q,F3) -> H2(B3,F3)
```

と `H1(Q,F3)=H2(Q,F3)=0` の exact pin から、B3-stable character が exponent character
一本であることを導く形で証明しなければならない。さらに五 coface kernel equality、semantic
`M`、outside ledger、972 fibre は未接続である。これらを修正した v5 を継続委嘱した。

order-8 v3 は `G9=(C9^3) semidirect V4` 側について五つの order-8 group の action と
cohomology raw cells を有限化し、総数 8208 を得た。しかしこれは full
`Q=B3/M=(G9 x PSL(2,8)) semidirect S3` の relative-extension universe ではない。
PSL(2,8) 因子を split-centralizing で除けても、残る S3 側の braid lifts、G9-action との
conjugation compatibility、square-inner relations、braid defect を列挙する必要がある。
従って 8208 を完全 task universe として dispatch せず、full-Q radices を閉じる v4 を
差し戻した。

DMTCP calibration については、raw `FQ/<q_relators>` の完全 presentation は exhaustive
enumeration の完全性には関係するが、A の十分条件である「一つの実在 finite refinement の
zero fibre」には不要であると整理した。修理案は、independent calibration と個別 candidate
checker の双方を explicit permutation group `BQ` に直結し、candidate finite group `P -> BQ`
の onto、kernel order、marked images、`|P|=k|BQ|` を直接検査する。q-relators が不完全なら
候補を見落とすだけであり、この direct gate を通った zero fibreから false A は生じない。
Luna に実際の v2 本線へこの fail-closed repair を実装させている。

```text
K9_C3_V4=RETURNED_FOR_H1_AND_COCOUNT_REPAIR;
K8_V3=G9_SIDE_ONLY_FULL_Q_S3_RADIX_MISSING;
DMTCP_REPAIR_TARGET=DIRECT_EXPLICIT_BQ_CANDIDATE_VALIDATION;
LOCAL_GAP_PROCESS_COUNT=0;
A_B_TERMINAL=STILL_RUNNING;
```

### 11.7 DMTCP run の実結果と C3 圧縮案の差し戻し

run `31962852940` は 2026-08-16 20:38:29 UTC に failure で終了した。数学的な
cell には到達していない。step 12 の決定行は

```text
STATE_STOP independent k=1,2 lossless calibration reconstruction UNKNOWN:
GAP failed with exit 1; stage=calibration.gap.execute;
stderr_tail="Error, the coset enumeration has defined more than 4096000 cosets ..."
```

であり、要求した 240 分 slice の checkpoint 時刻より前に、独立 calibration が GAP の
`CosetTableDefaultMaxLimit=4096000` で fail-closed した。artifact は 0 件であるため、再開可能な
世代も A/B receipt も無い。scheduled successor `31966124887` も artifact を拾えず新規起動へ
回った後、Ubuntu mirror で `Package 'dmtcp' has no installation candidate` となり provisioning
段で failure。これは別 source `59aa890e...` の旧 workflow であり、数学結果ではない。

現在は workflow YAML を変更せず、checker が明示 permutation group `BQ` から exact marked
presentation を独立再構成して producer の relator list を束縛するか、少なくとも terminal 前の
exactness gate へ移す versioned repair を Luna に委嘱した。単に coset 上限を外して無制限化する
repair は採用しない。

一方、指数 3 の相対 refinement を LHS cohomology で一 cell へ圧縮する C3 v1 は、紙上では

\[
H^2(Q,\mathbf F_3)=0,\qquad H^2(Q,\mathbf F_3^{\rm sign})\cong\mathbf F_3
\]

および permutation module \(\mathbf F_3^3\) の唯一の安定直線
\(\langle(1,1,1)\rangle\) と整合する。しかし独立監査は BLOCKER とした。producer/checker が
cohomology と marked-orbit completeness を再計算せず hard-code し、972-vector の
`image_size/fiber_counts/zero_indices` 相互矛盾も拒否できないためである。さらに semantic
\(M=K^{(9)}\cap N_{S4}\) の kernel binding と outside-648 gate が receipt に無い。
従って C3 v1 は commit/dispatch せず、A/B 証拠に数えない。

```text
RUN_31962852940=STATE_STOP_COSET_LIMIT_NO_ARTIFACT;
RUN_31966124887=PROVISIONING_FAIL_NO_ARTIFACT;
C3_COMPRESSED_V1=BLOCKED_NOT_DISPATCHED;
LOCAL_GAP_PROCESS_COUNT=0;
A_B_TERMINAL=STILL_RUNNING;
```

### 11.8 semantic M-export の長時間再投入

Phase-A v3 run `31967434065` は 2026-08-16 20:53:57 UTC、指定した 90 分の
job timeout で cancellation となった。startup/load warning より後の証明 receipt は出ず、
artifact は 0 件である。従ってこれは `M` の kernel equality の肯定・否定でも A/B 結果でもない。
source `170a38ffdfbdfc5fb6a373388aa11bf7c0af3022` から現 HEAD
`565ee183af983a3d4bf67fd1374e4259055873a5` まで、producer と checker を含む当該三ファイルに
差分がないことを確認し、workflow YAML を変更せず timeout 360 分で run `31972043453` を
再 dispatch した。branch は `sol/d972-dmtcp-provision-v420` である。

同時に、長時間部分が `IsomorphismFpGroupByGenerators(PB3sub,pb3Marks)` である可能性が高いため、
既知の `PB3 ≅ F2 × Z` の marked presentation を明示し、subgroup-presentation 計算を避ける
versioned v4 の設計も Luna に要求した。v3 の長時間化と v4 の高速化は互いを代用せず、いずれも
semantic `M=K^(9) ∩ N_S4` の exact kernel binding を terminal gate として保持する。

```text
RUN_31967434065=CANCELLED_90M_NO_ARTIFACT;
RUN_31972043453=DISPATCHED_360M_HEAD_565ee183;
LOCAL_GAP_PROCESS_COUNT=0;
A_B_TERMINAL=STILL_RUNNING;
```

## 12. 2026-08-17 06:40 JST 一時停止・完全引継ぎ凍結

研究者指示「一旦終わってよい」により、ここで新規探索・Luna 実装・dispatch を停止した。
実行中だった Luna 三本は interrupt 済み。既存 GHA 三本は artifact 回収可能性を残すため
cancel していない。ローカル GAP/DMTCP process は 0 である。

### 12.1 終端状態

```text
D972_B4_A_WITNESS_COUNT=0;
D972_B4_B_WITNESS_COUNT=0;
D972_B3_GENTLE_A_WITNESS_COUNT=0;
D972_B3_GENTLE_B_WITNESS_COUNT=0;
A_B_TERMINAL=UNKNOWN;
IHARA_COUNTEREXAMPLE_CLAIMED=NO;
```

したがって、この便は研究成果の終端報告ではなく、再開時に同じ型誤り・有限窓の過大解釈・
GAP 規約事故を繰り返さないための handoff である。研究者が認める A/B 決着はまだ得ていない。

### 12.2 以後も固定する数学的契約

1. 屋根は
   \(M=K^{(9)}\cap N_{S4}\)、\(|PB_3/M|=1,469,664=2916\cdot504\)、
   \(|B_3/M|=8,817,984\)。有限 target は \(|X|=|GT^\heartsuit(M)|=972\)、
   算術像 \(A\) は 324、指数は 3。index-3 dichotomy を使う場合、一本の terminal outside
   zero-fibre が全 648 を fake とする A、一本の genuine outside element が全 648 を genuine
   とする B へ進む。
2. B4-B なら \(\widehat{GT}\) の M-像が算術像を真に越えるので、そのまま井原予想の反例へ進む。
   B3-gentle-B だけでは full B4/\(\widehat{GT}\) との同一性 bridge が別途必要である。
3. genuine の compactness に transition surjectivity は不要。全 finite refinement で fiber が
   非空、reduction が total/functorial、refinement poset が directed なら有限交差性から inverse
   limit は非空になる。B 側の核心は「全 finite refinement の非空性」である。
4. fake を仮定すれば最小指数 failure を一段の B4-stable chief extension
   \(1\to V=H/K\to E_K\to E_H\to1\) に圧縮できる。abelian chief layer の正しい一次問題は

   \[
   d_1:C^1_{\rm gen}\longrightarrow V_{3,14}\oplus V_{3,15}\oplus V_4,
   \]

   で、同一 correction が二 hexagon と literal A.18 pentagon を同時に消すか、すなわち実 defect
   が \(\operatorname{Im}d_1\) に入るかである。第三成分を根拠なく \(N_5\lambda_5\) と置かない。
   typed coface maps、syzygy/closedness、onto、charming、settlement、nonabelian \(S^r\) layer が
   未閉鎖。個別 averaging、Schur--Zassenhaus、Gaschuetz/Frattini だけでは joint correction は出ない。
5. 「本当の158」は旧 rho-tail ではない。正しい固定対象は六生成元で、K(0,5) prefix 18本と
   五つの **literal A.18** coface image \(5\times28=140\) 本を合わせた raw-A.18 158本である。
   relator digest は
   `783d7d80f472fbf6abc8a2f58454048de361e95774c76ce1c511982bb44eb305`、
   972本の \(\widetilde D\) digest は
   `32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef`。
   semantically typed finite quotientでの nonidentity は A の一方向 witness になり得るが、
   fixed-158 all-pass は `LOCAL_U158_PENTAGON_ONLY` であり B ではない。
6. paper 積は現実装の GAP permutation 積と逆順になるため、全積を `PaperProd` で評価する。
   \(\tau(y)=y^{-1}x^{-1}\) は GAP 側 `X^-1*Y^-1`。Artin bridge の paper word
   \(x_{13}=s_2s_1^2s_2^{-1}\) も raw GAP conjugate と混ぜない。

### 12.3 恒久棄却・再実行禁止

- **7進 verbal/Zassenhaus 有限段族**：事前登録窓 705,894 候補から hexagon 通過294、
  pentagon 通過42まで得たが terminal outside witness は0。42 all-pass は cofinality を持たず B
  ではない。`ROUTE_EXCLUSION_7ADIC_FIRST_ORDER=PERMANENT`。
- **旧 rho-tail 158**：literal A.18 normal closure と有限 RS quotient で分離済み。旧 run の
  all-pass/defect は B4 A/B に使用禁止。
- **一次 twisted Alexander/Fox の係数体替え**：F19 全220 characterで非自明 pairing 0。
  F7 への改名再走査も禁止。
- **有限 p-class/Magnus 深度の単純延長**：新しい terminal implication がない all-pass prefix を
  B にしない。
- **Lochak--Schneps 必要条件だけの再走査**：paper/GAP 規約修正後は frozen 972/972 PASS。
  必要条件通過なので A witness でなく、十分条件でもない。
- **raw-A.18 p=2 の C2^5 shelf**：class 1--4、158+972 語は全恒等。typed PB4/M bridge がなく
  nonterminal。単純な深度追加を新路線と数えない。

### 12.4 GHA の live handoff（停止時点）

2026-08-17 06:40 JST に `gh run view` で確認した。

| run | source | step | artifact | 扱い |
|---:|---|---|---:|---|
| `31967437253` | `170a38ffdfbdfc5fb6a373388aa11bf7c0af3022` | N3 Phase-B1 v2 GAP、in progress | 0 | 完了後のみ receipt 回収 |
| `31969443502` | `bf1a23629ae28a99411543f5af6443d5b2f79e72` | explicit 20-block direct-v4 GAP、in progress | 0 | 完了後のみ receipt 回収 |
| `31972043453` | `565ee183af983a3d4bf67fd1374e4259055873a5` | semantic-M export、360分、in progress | 0 | exact M receipt候補 |

いずれも現時点では A/B evidence 0。完了・timeout・failure のいずれでも、artifact を一意な
TEMP directoryへ downloadし、SHA-256 を取り、対応する独立 checkerを通すまで数学結果としない。

### 12.5 DMTCP/direct-BQ repair（静的 PASS、GHA 未実行）

旧 run `31962852940` は independent `FQ/<q_relators>` Todd--Coxeter が 4,096,000 coset capで
停止し artifact 0。修理は巨大 quotient 構成を捨て、明示 permutation
`BQ`（order 8,817,984）へ q-relators を一方向評価し、候補ごとに有限
`P -> BQ` の onto、kernel order、marked images、braid、generation、\(|P|=k|BQ|\) を直接検査する。
候補の実在有限 extension を直接検査するので、q-relator list の不完全性は候補を落とし得ても
false A を作らない。

最新の未 commit 静的 bundle:

| file | SHA-256 |
|---|---|
| `search/check_d972_dovetail_v1.py` | `f2dd2f2dcfd9a1d1e18a0362a795871bf384789e2afff97bc5c1b8c91f33bb8d` |
| `search/check_d972_dovetail_v2.py` | `ddfe0a0725f4281df3ce488e8c541dce5d890dda6a7634ce438c31db88dcd7c4` |
| `search/d972_dovetail_manifest_v1.json` | `c477896001f55038b58a262f540804eb44fca883eb73f2dd543c446db6d745a2` |
| `search/d972_dovetail_manifest_v2.json` | `e3214710442d7a6755939c001b76993eb3899fa5e727503c6edf304690527455` |
| `search/d972_dovetail_producer_v2.py` | `080a39ec5fe8174fbd2721d484bd263f4e0c691327188c2bdb429febe7735c16` |
| `search/d972_dovetail_state_schema_v1.json` | `945ca3b20ac6f9efe5199756567569b73b3d768932dd60fed3fbcc0f120443c1` |
| `search/check_d972_semantic_m_v1.py` | `e71fff79af4301faa6ab230a2c9c96bd1fb00de7e37196ab06d36218df2c4330` |
| `search/d972_semantic_m_manifest_v1.json` | `7cbceac3353d266c31e4b9c986231143bd8a576c3e8120f84afb9307f9042f8a` |

詳細は `sol/luna_reply_152_dmtcp_calibration_repair_v4.md` と
`sol/luna_reply_152_semantic_m_bq_v1.md`。semantic-M は GAP 生 markerで
\(|K9|=2916,|PSL(2,8)|=504,|M|=1,469,664,|BQ|=8,817,984,|\ker\epsilon|=1,469,664\)
と両 component projection、Artin/central bridge、paper orientation canaryを実測する設計。
raw marker、q-relator/target/script/stdout digest、self-hashを state/final-A seal に束縛する。

停止直前に親が実行した `py_compile` と semantic/v1/v2/producer-v2/v3 の全 selftest は exit 0、
`git diff --check` も clean。ただし **local GAP 未実行、GHA raw marker 0** なので実測証明書ではない。
再開者は sourceを再監査後、workflow YAMLを変えず既存 DMTCP workflowを fresh dispatchする。

### 12.6 order-8 / order-9 relative lanes

**k=8 v4 は production 不採用。** split action prefilter は五つの order-8 kernelで652 actions、
64 liftsずつ、計41,728 cells
（C8 256、C4xC2 512、C2^3 36,352、D8 512、Q8 4,096）まで圧縮した。しかし
`search/d972_k8_extension_v4.g` と checker は BQ の二生成元 fp relator list にも「158本」を
要求している。158は raw-A.18 六生成元 presentation の型であり、BQ fp presentation の本数では
ない。この型混同は未修正なので、v4を commit/dispatch/terminal evidence に使わない。
詳細は `sol/luna_reply_152_k8_extension_v4.md`。再開時は BQ q-relators を「非空の実際の
二生成元 list＋digest＋明示 BQ 一方向評価」に直し、raw-A.18 158は pentagon層だけで使う。

**k=9 C9 v6 は有限 bridge の partial。** 六 radix `1,2,4,5,7,8` について明示
`P -> BQ`、kernel order 9、pure kernel order 9、五 A.18 finite kernel checkを実装し、v5 の
`rows[ri][4]` 範囲外バグを修正した。Python selftestは PASS。だが
`b4_normality/isolated/settled=UNKNOWN`、`semantic_M_binding_exact=false`、
`outside_648_identified=false` なので terminal A/B は禁止。GHA未実行。
詳細は `sol/luna_reply_152_k9_relative_hunt_v6.md` と v6 producer/checker/manifest。

### 12.7 B4-B 本命の再開点

有限 A 探索に配分が寄りすぎたことを停止前に認めた。B4-B を再開するなら、新しい有限窓を
増やすのではなく次の二択に集中する。

1. **minimal-bad-chief joint correction**：literal A.18 cofaceを含む typed relation complexを
   構成し、全 abelian irreducible chief moduleで defect classが \(\operatorname{Im}d_1\) に入る
   theoremを証明する。p=2,3,5 と非半単純性、generation/settlementを別 gateにし、最後に
   nonabelian \(S^r\) の transported intersectionを閉じる。
2. **直接 global outside element**：\(\widehat{GT}\to GT(M)\) の像に一本の outside elementを
   明示する。K9因子と PSL(2,8)因子への個別 surjectivityだけでは足りず、Goursat common
   quotient/compatibilityを実際に壊す global elementまたは独立性定理が必要。有限 roof の
   972/972 や arithmetic 648 の存在をその elementと取り違えない。

現存文献監査では ordinary group cohomology、個別 Fox naturality、Furusho の characteristic-zero
pentagon-to-hexagon、Lochak--Schneps の別補正元三本、Frattini/projectivityのいずれもこの joint
theoremを供給しなかった。これは B4-B が否定されたという意味ではなく、現在の本当の theorem
blocker である。

### 12.8 作業ツリーと再開手順

- branch: `sol/d972-dmtcp-provision-v420`
- handoff bundle commit: `d408f454827c7ae29cff61443bfbbf3212ea3c04`。direct-BQ/semantic-M
  static bundle、k9 v6 fail-closed partial、各 Luna report のみを exact-stage した。既知の型誤りが
  残る k8 v4、workflow YAML、無関係な dirty files は含めていない。
- handoff ledger commit: `f128b89772a623b29851ee158b404c8c0fffac5a`。
  `origin/sol/d972-dmtcp-provision-v420` へ `565ee183..f128b897` を push 済み。
- HEAD before handoff bundle: `565ee183af983a3d4bf67fd1374e4259055873a5`
- 本節作成時、上の direct-BQ/semantic bundle、k8 v4、k9 v6、各 Luna report、及び本返信は
  modified/untracked。巨大な既存 dirty tree があるため `git add -A`、reset、checkout、clean は禁止。
- commitする場合は採用 bundleを path exact-stage し、k8 v4 は既知の型誤りを直すまで除外する。
- GHA三本をまず pollし、完了 artifactを回収・独立照合する。artifact 0なら結果なしとして閉じる。
- ローカルで複数 GAPを起動しない。停止時 process count は0。
- A/Bが出たときだけ terminal sealを作る。B4-Bなら直ちに井原反例の紙証明、独立監査 package、
  PDFへ進む。

```text
HANDOFF_FREEZE_20260817_0640_JST=COMPLETE;
HANDOFF_BUNDLE_COMMIT=d408f454827c7ae29cff61443bfbbf3212ea3c04;
HANDOFF_LEDGER_COMMIT=f128b89772a623b29851ee158b404c8c0fffac5a;
HANDOFF_BRANCH_PUSHED=sol/d972-dmtcp-provision-v420;
SUBAGENTS_INTERRUPTED=3;
LIVE_GHA_RUNS_RETAINED=31967437253,31969443502,31972043453;
LOCAL_GAP_PROCESS_COUNT=0;
PERMANENT_EXCLUSIONS_RECORDED=YES;
TRUE_RAW_A18_158_DISTINGUISHED_FROM_7ADIC_AND_BQ_FP_RELATORS=YES;
A_B_TERMINAL=UNKNOWN;
```
