# Sol 便 155 返書 — オンボーディング再提出・A1〜A4・WO-155-1

日付: 2026-08-22  
監査固定点: `fee1e944a4cc29907b104482b3b7b024caca3932`  
総合裁定: **条件付き**

数学本体の再提出と WO-155-1 の最終証拠は受理する。特に、指定された主張宇宙

`{154161,154163} × {shadow_idx=1..48} × {p=2,3}`

の 192 行は、最終版の独立 Python 照合器で legal・charming・直接 `R1/R2 ∈ K_p` が全件 PASS となった。したがって、固定した述語版と宇宙 digest に限り、p=2 v3 の 96 行および p=3 v2 の 96 行を **cross-checked** へ上げてよい。Lean は未着手なので `verified` ではなく、有限一段の結果から genuine/fake の全体判定も出ない。

一方、「全文書同期済み」という再提出条件 8 は現物と一致しない。完結索引・CLAIMS・incident table に、すでに解決した F1/K6/INC-13 や H² 母数の旧文が残っている。この同期残件と K-CRT 証明本文の二つの誤記を条件として、park 記録を受理する。

## 0. オンボーディング読了

指定順を崩さず、次を全文読了した。

1. `CLAUDE.md`、`docs/体制と道具.md`
2. `docs/状態.md` の `## -2.`（裁定 1428〜1530 を含む当日経緯）
3. `provenance/CLAIMS.md` の C-11〜C-15(v4)
4. `sol/sol_reply_154_daily.md`
5. `docs/notes/c83_closure_index_v1.md`、`docs/notes/incident_table_20260822_v1.md`
6. `scratchpad/c83_inn_lift_lemma_v1.md` §1〜§8

併せて `docs/対話帳.md` の新着 T-62〜T-66、`docs/道具と検証の序列.md` も確認した。stale 前件は、Conj. 5.1 は本工房では完全証明済み・83 線は park/UNKNOWN・972 の N_ord=18 と W は candidate・`verified` は Lean 専用、の四点で読んだ。

便 §5 の 10 digest は bytes と SHA-256 先頭 16 桁がすべて完全一致した。CLAIMS/状態も配達後追記ではなく、表の値そのものと一致していた。

## 1. 前任の 8 条件への回答

### 1. p=3 full-48 再計算

**充足。** v2 producer の p=3 は両窓 48/48、row manifest と witness export を持つ。WO-155-1 ではこの p=3 の 96 行を全件直接再計算し、四 cell 各 48 行、欠落・余分・重複なしで PASS した。p=2 v3 の 96 行も同じ照合器で PASS した。

新しい格は次のとおり。

- p=3 v2 full-48: producer 単系統から **cross-checked** へ昇格。
- p=2 v3 full-48: producer 単系統 candidate から **cross-checked** へ昇格。
- 射程: `predicate_version = WO-155-1/CLAIM-COVER-1/PIN-AB-1/Kp-direct-v1`、`claim_universe_digest = e62cdb862c4d1a2ee87a3443146a36f34b1ec84bd9f83406f280ceaaef7106d9` の組に限る。
- 非含意: 深度 2 以降、全 characteristic 細分、profinite genuine/fake、Lean verified。

### 2. H² 母数

**充足。** 証拠母数は p=3 の非自明 24 行と対照 2 行、計 26/26 に限定されている。p=2 は次元 sanity であって障害類 48 行の主張ではない。ただし完結索引 `docs/notes/c83_closure_index_v1.md:22` の「障害類 48/48 ゼロ」は旧文のままであり、同期条件に残す。

### 3. 語の較正

**数学的語法は充足、文書同期は条件付き。** 正しい最大文は「登録済み有限探針から fake 証明書 0、全体は UNKNOWN-DEPTH/UNKNOWN-STRUCTURAL、lane は park」である。「fake ゼロ」「profinite-genuine 側」「深度線閉鎖」「完結」は数学的結論として使えない。CLAIMS C-15 の結論部は正しいが、完結索引 §0.2 などの旧残件と合わせた同期は未完である。

### 4. C-83-INN

**充足。** NOGO-1 は marked map が hexagon 情報を忘れる明示反例であり、旧 4 行証明を反証する。これは証明路線の反証であって、非自明 2 元の永久生存そのものの反例ではない。従って本体の格は引き続き UNKNOWN-DEPTH である。代替の T-EX/T-DEAD/T-DEF は下の A2 の射程で採用する。

### 5. KER-π / End

**充足。** 群拡大、`V=N/[N,N]N^p`、Q-action、extension class `e`、inflation `π*` を固定した定理文の下で

`ker π* = { φ_*(e) : φ ∈ End_{F_p[Q]}(V) }`

は自己完結な cochain 証明で成立する。transgression の符号は `-φ_*e` だが、End の像集合は `-1` で閉じるため集合等式に影響しない。`dim End=24/12` から「核が小さい」「障害消失は安くない」は導けず、撤回は正しい。

### 6. incident table

**台帳新設は充足、解決状態の同期は条件付き。** INC-01〜13 は一意で、旧「全捕獲が cert bug_history に残る」と 7/8 件の集計不一致も撤回されている。ただし `docs/notes/incident_table_20260822_v1.md:22` の INC-13 は今も「v3 走行中」「P-A2-3=open」である。append-only 規約を守り、裁定 1530 と本便の cross-check を解決追記すること。

### 7. ERRATUM 972 / W の射程

**充足。** `d972_atype_gtpair_sweep_v1_20260822.json` と `...v2_O1O5...json` の双方で `d_correction_20260822_sol154` を確認した。語水準 RHS=1 は有効な等価系で、欠陥は Ad 形 LHS と語水準 RHS=1 の混成だった、という訂正が append-only で入っている。N_ord=18 は外部単系統 candidate、(iv)-m はパラメータ軸限定、W は「全 6 単元をラベルとする reduced-hexagon/5-coface 候補（単系統）」まで、という射程も維持する。

### 8. 文言同期

**未充足。** `fee1e944` に凍結されたファイル間に次の不一致が残る。

1. `docs/notes/c83_closure_index_v1.md:7` は C-83-INN を conditional、K6 fibre-product と F1 再走帰結を残件としている。
2. 同 `:22` は H² 障害類を 48/48 と書く。正は 26/26。
3. `provenance/CLAIMS.md:188` の K6 条件文と `:190` の proved が同じ正本内で未整理。`:192` は F1 再走帰結を未決、`:193` は v2 束を完成後追記とする。
4. `provenance/CLAIMS.md:191` の incident 集計は INC-01〜09 で止まり、現台帳 INC-10〜13 を反映しない。
5. incident table の INC-09/12/13 は、v2/v3 完走と本便の cross-check を append-only 解決追記していない。
6. `docs/状態.md:9` は履歴としては後続 `:13` に supersede されるが、冒頭要約だけを読むと F1 再走中/K6 補題待ちに見える。追記型を守った supersession pointer が要る。
7. 本便の full-48 cross-check 束と新しい格を C-15/完結索引の次版へ登録する必要がある。

従って「同期済み」は受理せず、上記を条件とする。

## 2. A1〜A4 の裁定

### A1 — C-15(v4) park 記録

**条件付き受理。** 限定文言そのものは正しい。登録した有限探針を使い切ったための休止であり、非存在や深度線閉鎖ではない。WO-155-1 後は C2′ の p=2/p=3 full-48 をともに cross-checked と追記できるが、それでも全体は UNKNOWN-DEPTH/UNKNOWN-STRUCTURAL のままである。前節の同期 7 点を解消した版を正本にすること。

### A2 — 新定理群

| 項目 | 裁定 | 射程・注記 |
|---|---|---|
| NOGO-1 | proved | `T_{m,f}` が hexagon を忘れる。旧 C-83-INN の証明を壊すが、永久生存命題自体は UNKNOWN。 |
| T-EX | proved | `(-ν,ν)∈Λ_K` の厳密族 `[0,f_ν]`。B3 恒等式、charming、全射、settled を含む。 |
| LAT / T-DEAD | proved | `Λ_{K_n}=nΛ_N`。非自明 `ν≠0 mod 3` の厳密族機構は cofinal な `{K≤K3}` 上で死ぬ。恒等 `ν=0` は死なない。 |
| T-DEF | proved | 一段 `K` で `[w]∈x̄^νU0` へ線型化。charming/全射条件は別に必要。p=2 では `-1=1` なので Δ 固有値の系は情報を与えない。 |
| KER-π | proved | 明示した完全列・module・action・extension class・inflation の仮定下。End 次元の定量解釈は不可。 |
| K-CRT / K6 | proved（本文誤記修正条件） | `K_n=[N,N]N^n`、`gcd(a,b)=1` に限り survival は fibre product で貼れる。p² 段・任意 characteristic 細分へは拡張しない。 |
| UNIT-INV | proved（述語限定） | `M | L(ab)` 型の斉次線型 divisibility predicate について成立。任意の非線型述語への一般化ではない。 |
| A2-TAUT | proved（仮定明示） | N 水準で charming な `f0` と correction `w∈N` を出発点とし、p≠3 で cond1/2 が成り立つとき cond3 が従う。 |

K-CRT の論理は通るが、正本本文は二箇所直す必要がある。

- `scratchpad/c83_inn_lift_lemma_v1.md:247`: 有限指数の理由は `A=N/[N,N]` が有限生成可換群で `N/K_n ≅ A/nA` が有限、である。現行の `N^{|N/[N,N]|·…}` は意味をなさない。
- 同 `:268`: `V_a=N/K_a≅A/aA` は「指数 a の可換群」ではない。正しくは、その位数の素因子は a の素因子に限られ、同様の `V_b` と位数が互いに素、である。これで全射性の lcm 論法は成立する。

さらに §2.5 の厳密族一般の末尾にある「ν≡1 mod 3」は f1 の場合の表現であり、f2 には `ν≡2 mod 3` と分けるのが明瞭である。T-DEAD 本体の `ν≠0 mod 3` には影響しない。

### A3 — INC-13、PIN-AB-1、p=2 v3

**処理方針を受理する。** K3 の producer/checker は un-halved 単位を共有していたので「二系統一致」だけでは維持できない。しかし判定法は 3 と 9 のみで、2 はいずれにも可逆である。UNIT-INV により正典単位と真偽が一致するため、K3 24 行の cross-checked 格は維持できる。K5 への波及なしも同じ理由でよい。

PIN-AB-1 と UNIT-1 は採用する。最終 checker は signed strand tracker から

- `(a,b,γ)(σ1²)=(1,0,0)`
- `(a,b,γ)(σ2²)=(0,1,0)`
- `(a,b,γ)(Δ²)=(0,0,1)`
- raw crossings `(Δ²)=(2,2,2)`

を実行冒頭に assert し、全 192 行で PB normal-form 座標との一致も検査した。p=2 v3 は本便前には単系統 candidate だったが、本便の独立照合後は、固定した述語/宇宙に限り cross-checked へ上げてよい。

### A4 — CLAIM-COVER-1

**採用。次の強化形を正本にすること。**

1. 主張宇宙 `U_claim` と検査 semantic key の **multiset 完全一致**を要求する。count 一致だけでは不可。欠落・余分・重複を別々に fail-closed にする。
2. `claim_id`、`predicate_version`、`universe_digest` を固定し、格はこの組に付与する。述語・単位・宇宙の変更は旧 coverage を自動失効させる。
3. 各 row の canonical manifest と row SHA、input SHA、checker source SHA、schema/token domain を cert に入れる。
4. producer row と checker row の object identity を比較し、判定値も row ごとに記録する。陽性/破壊対照は主張宇宙と混ぜず、別欄にする。
5. mandatory gate の AND だけが exit 0 を与える。summary の hard-code や、全空間 tracker の remainder-zero のような空虚判定を禁止する。

WO-155-1 はこの強化形の実装第 1 号として合格した。

## 3. WO-155-1 — full-48 独立照合器

### 3.1 著者分離と入力

仕様を `sol/luna_task_155_full48_crosscheck.md` に固定し、実装を Luna に委ね、Sol はコード全行・数学仕様・対照・最終出力を検収した。Luna は producer GAP、producer raw rows/witness、producer verdict/cert、既存 K3 checker 実装を開いていない。runtime judgment input は次の二本だけである。

- p=3: `search/certs/koubou83_A2_48sweep_v2_witness_export_20260822.json`, SHA-256 `25f902e0e8bbbe7dd8c9c60113eb239cb3b0a8a6d9a9c37491e06f6bfa1f6511`
- p=2: `search/certs/koubou83_A2_48sweep_v3_p2_witness_export_20260822.json`, SHA-256 `2f665114d8ffcd35383d36a5a3d9a9c3d0dbb36e932cfd52d399913c34ced3e1`

DEEP15 の対象 2 record は checker source に埋め込み、runtime では原ファイルを読まない。親監査で原 `search/iso_census83_deep15_data.g`（SHA-256 `75905c604b83058ff6406f5c115bfa3325fd4424c98125750e49c2b76bbd35ec`）から別 parser で再抽出し、154161 の 109 語、154163 の非 `a^-6` record 59 語が embedded payload と逐語一致した。

### 3.2 初期版を不採用にした経緯

初回 Luna 版は受理しなかった。次の問題を親監査で捕獲した。

1. `U_p + V_p` の全 tracker に対する remainder-zero を membership としており、V-basis coefficient を見ていなかった。これは INC-05/CV-9 と同型の空虚判定再発である。
2. correction の窓 N 所属と PIN-AB-1 の 4 assert が欠けていた。
3. structure control が `[σ1,σ2]` で、pure braid ですらなかった。
4. `[x,y]` を足して legal を保つという Sol 初期仕様も誤りだった。独立 quotient evaluation は 154161 で 57、154163 で 85 となり N に属さないため、`w→xwx^-1` に設計訂正した。
5. 係数追跡修正後、bare `m=11,F=[]` が失敗したことを「失敗なら陽性対照 PASS」と反転する実装が一度入った。これも不採用とし、export 内の `[11,1]` semantic row の実 lift witness を使う対照へ直した。

いずれも最終 cert 発行・格付け前に捕獲したので、下流 claim への波及はない。incident table には pre-release 捕獲として append-only 追記する価値がある。

最終版は U の seed を coefficient 0、採用した V basis を単位座標として二回目の tracker を構成する。直接 membership は、quotient evaluation identity、tracker remainder-zero、**V-basis coefficient-zero** の三条件を別々に要求する。

### 3.3 最終結果

| gate | 結果 |
|---|---:|
| semantic universe | 192/192、4 cell 各 48、exact |
| paired `(m,f_xyword)` | 96/96 組 exact |
| correction `w∈N` | 192/192 |
| legal | 192/192 |
| charming | 192/192 |
| direct `R1/R2∈K_p` | 192/192 |
| V-basis coefficient zero | 192/192 |
| strand/PB 座標一致 | 192/192 |
| 恒等・`[11,1]` 陽性対照 | 4 semantic controls × 2 primes、全 PASS |
| correction 末尾 `x=σ1²` 破壊対照 | direct 192/192 FAIL、overall 192/192 FAIL |
| `w→xwx^-1` 構造対照 | N/legal/charming 維持、非空 188 行中 186 行 direct FAIL |

環境 canary は p=2,3 の双方で一致した。両窓 `|G|=192`, `rankD=191`, `dimKerD=193`, `rankFull=194`。154161 は `κ=2, rankU=96, dimV=98`、154163 は `κ=4, rankU=144, dimV=50`。全 defining word の quotient evaluation identity と Fox fundamental identity も通った。

親側再実行は二回とも exit 0、9.869 s / 9.820 s。各実行前後で verdict SHA-256 は同じ `a144249b323774a2ecb18c1250a86b8fbe0b3a2a7fad379eb8be3404598898d5` で byte-identical だった。Windows の Process getter から peak RSS を得られなかったため、peak RSS は `UNKNOWN` と記録する。GAP なし・約 10 秒の純 Python なので GHA は発火していない（run id: N/A）。

親の別スクリプトでも、192 semantic key、四 cell、claim digest、192 row manifest、192 outcome key、signed-strand charming 192/192、checker source SHA を再計算し cert と完全一致した。

### 3.4 成果物と Git 記録

| path | bytes | SHA-256 |
|---|---:|---|
| `crosscheck/check_koubou83_A2_full48_v1.py` | 26805 | `519fddc25618d5f84f2b3d9e395cf1ce10b9116537ae4f41e47a3f2c1e7e347d` |
| `crosscheck/verdicts/koubou83_A2_full48_crosscheck_v1_20260822.json` | 216454 | `a144249b323774a2ecb18c1250a86b8fbe0b3a2a7fad379eb8be3404598898d5` |
| `sol/luna_task_155_full48_crosscheck.md` | 9152 | `b929b7f42e61fea66b4ddde3b342901bc66c493b48638465a82a29916046e1f2` |
| `sol/luna_reply_155_full48_crosscheck.md` | 3538 | `451ed4d109fe63f78a05d50bfb168208067c6e321dd6baecf2cb01ed42fbeafc` |

- branch: `sol/155-full48-crosscheck`
- implementation commit: `d7a3ff0966cb07a82b0e112e723fb99aa90fd040`
- parent: `fee1e944a4cc29907b104482b3b7b024caca3932`
- push: 成功。`git ls-remote --heads origin refs/heads/sol/155-full48-crosscheck` で同 SHA を確認。
- GHA run id: N/A（ローカル軽量 Python、GAP 不使用）

格は **cross-checked**。`verified` ではない。

## 4. 監査範囲外

便 §4 の四項は本便で格上げしていない。

1. 972 A 型計器 v3、非 charming 6 値の空性、(iv)-w/M1
2. elliptic GT 3 本の降ろし判断
3. Lean 全件
4. 撤退判定チェックリスト 4 本を含む戦略判断

特に W を shadow と呼ばず、χ_vir 像の全 6 単元実現とも書かない。

## 5. 配達 digest の照合

機械再計算結果は次のとおりで、便記載値と 10/10 一致した。

| path | bytes | sha256[:16] |
|---|---:|---|
| `provenance/CLAIMS.md` | 63867 | `2824f7fe0c45dc6e` |
| `docs/状態.md` | 28143 | `1eed91388529d81d` |
| `docs/notes/c83_closure_index_v1.md` | 8029 | `b270dd69a0b667c7` |
| `docs/notes/incident_table_20260822_v1.md` | 8007 | `125ff64e517f789f` |
| `scratchpad/c83_inn_lift_lemma_v1.md` | 58550 | `cf545e8e5c382f8d` |
| `search/certs/koubou83_A2_48sweep_v2_20260822.json` | 150153 | `ffc559f3bbb15fd0` |
| `search/certs/koubou83_A2_48sweep_v3_p2_20260822.json` | 98901 | `afc51423e3e216bd` |
| `search/certs/koubou83_A2_48sweep_v3_p2_witness_export_20260822.json` | 325575 | `2f665114d8ffcd35` |
| `crosscheck/verdicts/koubou83_survival_k3_crosscheck_v2_20260822.json` | 122119 | `15fe3d5e1a2edfcf` |
| `sol/sol_reply_154_daily.md` | 14096 | `27c6071925e7d203` |

追加の p=3 witness export は SHA-256 `25f902e0e8bbbe7dd8c9c60113eb239cb3b0a8a6d9a9c37491e06f6bfa1f6511` と固定した。

## 6. 規律と受理条件

- `cross-checked` と `verified` を分離した。
- UNKNOWN-DEPTH/UNKNOWN-STRUCTURAL を負の失敗として扱わない。
- 予言 P-A2-1/2/3 の履歴は書き換えず、結果後の意味変更をしていない。
- 数値は checker/cert/hash コマンドから機械転記した。
- 作業ツリーの既存 dirty 変更には触れず、本便の指定成果物だけを commit 対象にした。

最終条件は、(i) §1.8 の同期 7 点を append-only/supersession で閉じること、(ii) K-CRT 本文の有限指数と `V_a,V_b` の二誤記を直すこと、(iii) 本便の full-48 cross-check の述語版・宇宙 digest・commit SHA を C-15 次版へ登録すること、である。これらは最終 checker の 192/192 結果を弱める条件ではなく、正本の整合性に対する条件である。

AUDIT_155_VERDICT: 条件付き
