# 規約台帳 v1.1(conventions ledger)— 工房の大域規約と cert 宣言欄

- **状態札: candidate**(司令塔検分待ち・**Sol 便 94 §5 で方向承認 + CV-9 の規範文条件を受領**)
- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01 / 司令塔委嘱(研究者発案の制度化)
- **改訂 v1.1**: 2026-08-01・便 94 修文波(裁定 319)。**F94-5.2(CV-9 の規範文)+ P94-5.1(型強化 9 項)を正位置へ編入**。編入前の本ファイルの SHA-256 = `9cde70bdfc4494e6a9180a370bed81a65af3a388c22e8d0f4bf3c5268bed9087`(git 履歴に旧状態あり)。
- **正典との関係**: `docs/week1-定義ノート.md` §1.5.1(規約 W-1〜W-4)+ §1.5.2 補題 W1 が唯一の**ゲート通過済み正本**。本台帳はそれを内包し、以後に発見された規約を同形式で中央化する。**正典と食い違う記述が本台帳にあれば正典が勝つ**。
- 先行文書: `docs/notes/convention_dictionary_W_v1.md`(candidate・(W-\*)(W-^)(W-nf)(W-perm))— 本台帳は同 4 項目を CV-1/CV-2 に吸収する上位集合。**正典への番号付与(W-5/W-6)は v1.1 で決着**(【CL-3】closed・CV-2 一本化)。

> ### v1.1 改訂記録(何をどこへ入れたか)
> **原則: 末尾継ぎ足し禁止 — 生きた正本は論理位置へ**(研究者指示)。
> | 由来 | 内容 | **編入先(正位置)** |
> |---|---|---|
> | **F94-5.2** | CV-9 の規範文(主検問・副検問・三値・差戻し・検問記録) | **§1.3(全面改訂)** |
> | **W94-5.1** | 非当事者性は肩書でなく記録で判定 | **§1.3.3** |
> | **P94-5.1 (1)(2)(3)(4)(5)(9)** | 型強化(多層 character・comparison target・separation・round-trip・coset/action 型・representative/invariant) | **§2 schema(全面改訂)** |
> | **P94-5.1 (6)** | CV-8 に既定値を置かない | **§1 表 CV-8 行 + §2** |
> | **P94-5.1 (7)** | effective source chain(errata 運用) | ★ **§1 表 CV-10(新設)+ §2** |
> | **P94-5.1 (8)** | seal recoverability | ★ **§1 表 CV-11(新設)+ §2** |
> | — | 【CL-3】【CL-4】【CL-5】【CL-6】の閉鎖 | **§5(未閉鎖項)** |
>
> **判断の申告**: (7)(8) は「欄の型強化」ではなく**新しい規約**なので、正位置は §1 の規約表と判断して **CV-10 / CV-11** を新設した(§2 の欄だけに置くと、規約表を読んだ者が存在に気づけない)。**この番号付与は数学者の起草判断であり、司令塔レビューの対象**である。

> **一行**: 今週の計器事故は例外なく「**規約が probe の頭の中にだけあり、文書にも cert にも現れていなかった**」型である。台帳は規約を**外在化**し、cert 欄で**照合可能**にする。

---

## 0. 事故台帳(教材リンク)— 何をこの制度で潰すのか

| # | 裁定 | 何が起きたか | 破られた規約 |
|---|---|---|---|
| 1 | **275→278** | 著者パッケージ = 20 に対し我々 3 系統 = 4。真犯人は粗↔精の**語順規約の食い違い**(Psi は語を反転して代入・粗列挙は順方向 ⟹ 同じ精元に $f$ と $f^{-1}$ の二つの粗ラベル)。Sol の独立器も同じ辞書規約を共有していたため検出できなかった | CV-3 / CV-4 |
| 2 | **282→298** | settled = 4/8/8 を構造として報告 → 実体は「ラベル著者側 × 共役我々側」の**混成規約の artifact**。整合規約 $T'$ で 20/20/0 | CV-2 / CV-6 |
| 3 | **306(a)** | $2m+1\equiv1 \pmod{2^a}$ の偽解 $m=2^{a-1}$ が**粗い指標 $\chi_{\rm vir}$ には不可視** | CV-5 |
| 4 | **306(b) 補題 OPP** | 数学者指定の assert 式が 160/240 で偽。正形は $\ell=\tau\circ\rho$($P^{\rm op}$ への準同型)— $\tau$ が**反準同型**であることの未宣言 | CV-6 |
| 5 | **312→313** | $\alpha=2,3$ 不一致。**当初診断「左右規約の取り違え(f/f⁻¹ 族 4 例目)」は裁定 313 で撤回** — 実体は S6 が固定 $\alpha'=1$ 窓とだけ比較していた**比較相手の未宣言**。二実装は一度も食い違っていなかった | CV-7 / CV-8 |
| 6 | **319**(便 94 W94-2.1) | C-β-IND の dummy 自己検査が**識別力ゼロ**。$\alpha=99$ は $\bmod7$ で $1$、$\alpha=5$ は $\pm$ 同値で窓 $[2]$ — **どちらも登録済み宇宙の内側**。さらに条文が要求する「任意の有理関数 $h$ に替える」操作は**実装の入力スキーマに存在しなかった** | CV-9(§1.3.2 識別力)/ CV-10(erratum) |
| 7 | **319**(便 94 F94-4.3) | 初荷 $\alpha$ が **sealed mapping の永続化欠品**で NOT_EXECUTED。数学的陰性ではなく工程 defect | CV-11 |

> **申し送り(訂正)**: 委嘱文の「f/f⁻¹ 族 4 件」のうち **4 件目(裁定 312(c))は裁定 313 で機構主張ごと撤回済み**。確定している f/f⁻¹ 族は #1・#2・#4 の 3 件で、#5 は **comparison_target 欠落**が真因である。この訂正は制度の必要性を弱めない — むしろ「規約違反に見えた事故の一部は**比較相手の未宣言**だった」ことを示し、CV-7 の重みを上げる。

---

## 1. 大域規約(正本候補 CV-1〜CV-12)

| ID | 宣言(工房標準) | 格 | 事故 |
|---|---|---|---|
| **CV-1** | **置換・語の合成順序**。GAP native は**右作用** $i^{\,p*q}=(i^{p})^{q}$。工房標準(paper)は**左作用** $(AB)\cdot i=A\cdot(B\cdot i)$。ゆえに $\boxed{\text{paper 語 }AB\ \leftrightarrow\ \text{GAP }\texttt{q*p}\ \text{型}}$。**時間語(先に掛ける/後で掛ける)を正本に置かない** | **正典 W-1** | 裁定 109(F10)・`i24-u3-recheck`(自己捕獲) |
| **CV-2** | **作用の側・共役・剰余類の側**。GAP `X^g` $=g^{-1}Xg$(GAP 積)は CV-1 を 2 回通して**紙面の $\mathrm{inn}(g)(X)=gXg^{-1}$ そのもの** — $g$ を反転しない。剰余類の側は共役規約から**導出**される: $\bar y^{f}=f^{-1}\bar y f$ の下では $\bar y^{f}=\bar y^{f_0}\iff f\in C(\bar y)f_0$ = **左**剰余類 | candidate | SGN-ĉ・S2 / `pruning_law_v2` §6.3 の右剰余類 → `sat_l1_v1` §3.1 で左へ訂正(草稿内自己捕獲・cert 未汚染) |
| **CV-3** | **語の評価向き(層ごとに宣言)**。正典 W-2(prepend)は**紙面由来の語**の評価手続。GAP 内部で生成・保存された語(`PreImagesRepresentative` の出力等)には別途 `Rev` の要否があり、**同一対象にラベルを付ける二つの層は同じ向きでなければならない**。向きは「正しい向きが一つある」のではなく「**層ごとに宣言し、突き合わせる層の間で一致させる**」ものである | candidate | 裁定 278/280 |
| **CV-4** | **粗ラベル写像 coarse_of**。正本 = `coarse_of(w) := MappedWord(w,[gx,gy,gc],[xb,yb,()])`(**forward・`Rev` を掛けない**)。fiber ラベルは合成 `coarse_of ∘ WordOf`、`WordOf(q) := Rev(PreImagesRepresentative(epiP,q))`。**`Rev` は `WordOf` 側に 1 個だけ**置く(Psi が反準同型であることの帰結・裁定 278)— `coarse_of` 側に二重に掛けない | candidate(裁定 280 で発効) | 裁定 278/280 |
| **CV-5** | **$\chi$ の水準**。$\chi_N([m,f]):=2m+1 \bmod N_{\rm ord}$ は**粗い射影**(定義ノートの $\chi_{\rm vir}$・**$m$ を復元しない**)。$\tilde\chi_N([m,f]):=2m+1 \bmod 2N_{\rm ord}$ が**忠実**($\mathcal X_N\leftrightarrow(\mathbb Z/2N_{\rm ord})^\times$)。**指標から $m$ を復元する箇所では $\tilde\chi_N$ を使う**。$N$ が isolated のときに限り $\tilde\chi_N$ は群準同型 | **定理**(命題_円分持ち上げ_v2 補題 B4) | 裁定 306(a)・一斉点検 = 裁定 307 |
| **CV-6** | **反準同型の扱い(補題 OPP)**。写像が反準同型なら**終域を $P^{\rm op}$ と型付けて宣言する**。$\tau(g):=\hat c(g)^{-1}$ は生成元を固定する反自己同型で、正典の合成則 (3.53) $f_{12}=f_1E_{m_1,f_1}(f_2)$ は $\tau$-座標で $\boxed{g_{12}=\Phi'_{m_1,g_1}(g_2)\cdot g_1}$ と**逆順の積**になる。**素朴座標で準同型形の恒等式を assert してはならない** | **定理 + 機械 9600 対** | 裁定 306(b)・裁定 280(「redMap 準同型の近道」= 旧バグと代数的に同一) |
| **CV-7** | **比較相手の明示(comparison_target)**。二実装の照合は「**何と何を**」比べるかを、パラメータの**関数として**宣言する。固定既定値(例: $\alpha'=1$)との比較を「対応窓との比較」と呼ばない。**合格形には分離条件を含める**: 一致だけの試験は「何にでも当たる試験」でありうる | 手続き(裁定 313 で必須欄化) | 裁定 312/313 |
| **CV-8** | **判定基準の粒度(chi_P_criterion)**。$\chi_P$ の階層 $7\subset14\subset42$ のうち、厳密一致(7)と**完全共役類(14)は同答**、「同じ直線」(42)は**完全 fail-open**(3 窓全一致)。許容値 = `exact` / `conjugacy_class`、**`line` は禁止値**。★ **既定値は置かない**(P94-5.1(6)): **完全共役類は不変形**、**exact element は generator / orientation を固定した場合にのみ許す** — どちらを使ったかを cert が**必ず明示**する | 手続き(裁定 312(b) + **便 94 P94-5.1(6)**) | 裁定 310(fail-open の実地発見)・312(b) |
| **CV-9** | **仕様同一性判読(二検問・三値・差戻し)**。二系統一致を cross-checked と格付けする前に、**どちらの実装も書いていない者**が両側の仕様を判読し **PASS / FAIL / UNKNOWN** を裁定する。**規範文の正本は §1.3**(便 94 F94-5.2 逐条) | 手続き(裁定 316/318 + **便 94 F94-5.2**) | 裁定 312(a) stub の True・裁定 313 comparison_target 未宣言・裁定 319 識別力ゼロの dummy |
| **CV-10** | ★ **有効出所連鎖(effective source chain)**。文書・cert・定理を引用するときは **original / supersedes / errata・addenda** と各 digest を連鎖として記録し、**「その主張の現在有効な出所」が一意に定まる**ようにする。旧正本の冒頭には後継への誘導を置く。**旧証明だけを引用させない** | 手続き(**便 94 P94-5.1(7)**・新設) | U2 の旧 cyclotomic-lift 本文(W94-1.1)・`c_beta_ind_dummy_h_selfcheck` の撤回(W94-2.1) |
| **CV-11** | ★ **封印 fixture の回収可能性(seal recoverability)**。封印・退避する fixture は **ID・digest・金庫参照・復元 preflight の結果**を残す。**「封印した」だけでは回収可能性の記録にならない** | 手続き(**便 94 P94-5.1(8)**・新設) | 初荷 $\alpha$ の sealed mapping 喪失 ⟹ NOT_EXECUTED(F94-4.3) |
| **CV-12** | ★ **派生表の機械生成則**。定義・閉形から導出可能な表は機械生成(生成スクリプト+SHA-256 併記)か定義との機械照合つきのみ・手展開禁止(詳細 = §1.4) | 手続き(裁定 323/324・研究者発案) | δ(n) 早見表の定義乖離(裁定 322) |

### 1.1 CV-3/CV-4 の運用判定(唯一の合否)— 往復 assert

規約の正否を地の文で議論しない。**操作的判定はただ一つ**:

> **往復 assert**: 精元 $q$ に対し `coarse_of(WordOf(q))` が、粗列挙側が同じ $q$ に付けるラベルと一致すること。
> **証人は自己逆元でない粗 $f$ を取ること**(裁定 278 の指紋 = 生存 4 行がちょうど自己逆元の粗 $f$ 2 種 × 2 $m$ だった。**自己逆元の証人はこの罠を原理的に検出できない** — 既存 unit test 3 元が全滅した理由)。
> ★ **記録の型**(v1.1・P94-5.1(4)): 証人は「自己逆でない**具体例**・**期待 label**・**出所**」の三つ組で記録する(`roundtrip_witness`・§2)。**一例で足りない小宇宙では全列挙(`mode: "exhaustive"`)を優先する** — 宇宙が小さいのに標本で済ませる理由は通常ない。

### 1.2 CV-7 の合格形(分離つき)— C-β S6 の型

> **(a) 一致**: model$(\alpha)$ は**対応する**抽象窓 $H_{2,\alpha,0}$ と共役。
> **(b) 分離**: $\alpha'\neq\alpha$ の全窓と**非共役**。
> 合格形 = $3\times3$ の**単位行列**。(a) のみは fail-open になりうる(実例 = CV-8 の「直線」基準)。

---

### 1.3 CV-9 仕様同一性判読(規範文・**便 94 F94-5.2 の条文で固定**)

> **起源**: 司令塔追記 2026-08-01・裁定 316/318・研究者発案。**v1.1 で Sol F94-5.2 の規範文をそのまま採用**(「CV-9 は次の規範文なら PASS とする」)。以下 §1.3.1 の 5 条は **Sol 指定の逐条**である。

**宣言**: 新発明量の二系統一致を cross-checked と格付けする前に、**どちらの実装も書いていない者**(既定 = falsifier(opus/max)・代替 = 第三数学者インスタンス)が両側の仕様を判読し、**「同一対象 / 別対象 / 判定不能」を三値で裁定する**。

#### 1.3.1 規範文(5 条・F94-5.2 逐条)

> **(CV-9-1) 主検問(計算前)**: **IF-FIRST 凍結時**に、非当事者が二系統の
> ① **入力 universe** ② **比較対象** ③ **同値関係** ④ **正規形(NF)** ⑤ **filter** ⑥ **失敗状態**
> を照合する。目的 = 無駄な計算の前に仕様齟齬を殺すこと。
>
> **(CV-9-2) 副検問(格付け直前)**: **cross-checked 格付けの直前**に、**凍結宣言と実際の二 artifact の diff** を照合する(大半は機械 diff)。実装中のズレ(stub 型)の網。
>
> **(CV-9-3) 三値**: 判定は **PASS / FAIL / UNKNOWN**。**PASS 以外では cross-checked に上げない。**
>
> **(CV-9-4) 差戻し**: **主検問後に仕様または normalizer が変われば、副検問で救済せず主検問へ差し戻す。**
>
> **(CV-9-5) 検問記録の束縛**: 記録には **両 source / spec digest**、**target**、**competitor universe**、**識別力を持つ dummy fixture** を束縛する。

#### 1.3.2 「識別力を持つ dummy fixture」の要件(CV-9-5 の操作化)

dummy は **raw label ではなく、仕様が採用する同値関係を通した後**に既存 fixture と異なることを **machine-check** せねばならない(Sol ★教材 1)。**二層の正規化**(入力層 = datum、出力層 = 判定対象)を各々明示し、**各層の外に出る dummy を 1 個以上**含めること。

- **先例(実装形)**: `docs/notes/u7_fire_log_v1_addendum_grade.md` §4.2.6.5–§4.2.6.7(C-β の二層正規化と DUM-1〜DUM-5)。
- **反例(識別力ゼロ)**: `u7_cbeta_final_20260801.json` の `c_beta_ind_dummy_h_selfcheck` — $\alpha=99\equiv1$、$\alpha=5\sim[2]$ で**両方とも登録済み宇宙の内側**(裁定 319 で証拠から撤回)。

#### 1.3.3 非当事者性の判定(W94-5.1)

**model label(opus/max 等)や担当名で CV-9 PASS にしてはならない。** 判定は次の**記録**による:

1. 当該**仕様・実装・一次 grading に関与していない**こと(関与の有無を明示的に申告)。
2. **参照した provenance**(読んだ source / cert / 凍結文書とその digest)の列挙。

#### 1.3.4 スコープ制限と格

**スコープ**: 判読は「**同一対象か**」の一点のみ — 仕様の数学的監査・実装レビュー・追加テスト発案・計画監査への拡大は**禁止**(気づきは 1 行で司令塔へ・展開判断は司令塔)。原則 1 走・三値 + 根拠数行。
**格**: 主検問をすり抜けた仕様齟齬の最終防衛は従来どおり外部アンカー・Sol・Lean(§4 の射程宣言は CV-9 にも適用)。

**事故**: stub の True(裁定 312(a) — 仕様相違でも値が偶然一致し比較の瞬間には誰も気づけない型)・comparison_target 未宣言(裁定 313)・識別力ゼロの dummy(裁定 319 / W94-2.1)。

### 1.4 CV-12 派生表の機械生成則(司令塔追記 2026-08-01・研究者発案・裁定 324 で CV-10 衝突を改番)

**宣言**: 定義・閉形から導出可能な表(早見表・数値表・対応表)を文書に載せる場合、**機械生成**(生成スクリプトのパス+SHA-256 を表の直下に併記)か、**定義との機械照合**(checker スクリプト+照合結果)のいずれかを必須とする。人手展開の派生表は禁止。既存文書の手展開表は発見次第 erratum(定義側が正)。

**施行三点(v1.2・Sol 便 95 F95-3.3 で確定)**: CV-12 の履行は次の三点を**一束**にする — ①定義から表を生成する script ②script/input/output の digest ③文書 build 時に表と定義を再照合し不一致を fail-closed にする check。①だけ(生成したが照合が回らない)は不履行。

**格**: machine-piped 規律(cert の値の手写し禁止)の文書内派生物への拡張。同一文書内に定義と展開が併存する冗長表現は、機械照合がない限り「二重管理の事故源」とみなす。

**事故**: tmax_budget_and_holes_v1.md の δ(n) 早見表が同ノートの代数定義と 6 剰余類で不一致(裁定 322・CI 実測は定義側と整合)。照合スクリプトは定義から直接計算していたため 86/86 は無傷 — 表は機械に読まれない「飾り」として腐り、読む者だけを騙す位置にいた(stub 事件と同じ派生物ドリフト族)。

## 2. cert 必須ブロック `conventions_used`(schema)

**適用**: 新規 cert から。**既存 cert への遡及は不要**(⟹ 本欄の不在は旧 cert について何の情報も与えない・【CL-2】)。

**型付けの原則(v1.1・P94-5.1)**: **boolean と自由文だけの欄は弱い。** 「宣言した」ことが「機械で突き合わせられる」ことを意味するように、**比較・分離・多層・出所・封印**の各欄は**構造化して束縛する**。

**"n/a" の型(v1.2・F95-3.3)**: 全型で "n/a" を許すなら、将来の JSON schema では各 field を文字列との union にするか、型つき `{status:"n/a", reason:...}` に統一する — object/array 欄へ bare string を入れて schema が壊れる事故を防ぐ。

**CV-10 出所連鎖の schema 統一(v1.3・裁定 354・ASM v2 §V.4.3 の未同期 4 点を確定)**: 新規 cert/ノートから適用(遡及不要)。①`path` は**リポジトリ root 相対で参照対象 artifact 自身**を指す(生成 script や親文書ではない)②ハッシュのキー名は **`sha256`**(Sol 語彙に統一・`digest` は不使用)③`effective_source` は**文字列でなく object** `{path, sha256}` ④supersede 関係は入れ子欄 **`superseded_by: {path, sha256}`** で機械可読に持つ(散文の「失効」注記は人間用の副)。混在は機械照合を壊すため、以後この 4 点が正。

```jsonc
"conventions_used": {
  "ledger_version": "conventions_ledger_v1_1",

  // ---- CV-1 / CV-2: 合成順序・作用の側 ----
  "perm_composition":  "gap_native_right" | "paper_left",   // CV-1
  "conjugation":       "gap_caret_g_inv_X_g" | "paper_inn_g_X_g_inv", // CV-2
  "coset_object":      "left_coset_gH" | "right_coset_Hg",  // CV-2 / P94-5.1(5) 型分離
  "action_side":       "OnLeft" | "OnRight",                // CV-2 / P94-5.1(5) 自由文で代用しない
  "coset_side_derivation": "<共役規約からの導出を一文で>",   // CV-2(導出であって独立選択ではない)

  // ---- CV-3 / CV-4: 語の向きと粗ラベル ----
  "word_eval": [                                            // CV-3: 層ごとに 1 entry
    { "layer": "psi", "direction": "reversed", "word_source": "internal_gap" },
    { "layer": "coarse_enumeration", "direction": "forward", "word_source": "internal_gap" }
  ],
  "coarse_of":         "MappedWord_forward_no_rev",         // CV-4
  "word_of":           "Rev(PreImagesRepresentative)",      // CV-4(Rev の置き場所)

  // ---- §1.1: 往復 assert(P94-5.1(4) 型強化)----
  "roundtrip_witness": {                                    // 一例だけで足りない小宇宙では全列挙を優先
    "mode":            "exhaustive" | "sampled",
    "witnesses":       [ { "element": "<具体例>", "is_self_inverse": false,
                           "expected_label": "<期待値>", "source": "<出所+digest>" } ],
    "result":          true
  },

  // ---- CV-5: 多層 character(P94-5.1(1) 型強化: 単一 enum を廃止)----
  "characters": [                                           // 配列。層ごとに 1 entry
    { "layer": "chi_vir", "purpose": "coarse_projection", "modulus": "N_ord",
      "faithful": false, "source": "<定義ノート §/式番号>" },
    { "layer": "chi_tilde_N", "purpose": "recover_m", "modulus": "2*N_ord",
      "faithful": true,  "source": "<同上>" }
  ],

  // ---- CV-6: 反準同型 ----
  "opposite":          { "map": "tau", "antihomomorphism": true, "codomain": "P^op" },

  // ---- CV-7: 比較相手(P94-5.1(2) 型強化: prose だけでは不可)----
  "comparison_target": {
    "as_function_of":  "<パラメータの関数として一文で>",      // 裁定 313
    "function_a":      { "name": "<関数/実装>", "domain": "<定義域>", "source_digest": "<sha256>" },
    "function_b":      { "name": "<関数/実装>", "domain": "<定義域>", "source_digest": "<sha256>" },
    "normalization_digest": "<NF 仕様の sha256>"
  },

  // ---- §1.2: 分離条件(P94-5.1(3) 型強化: included=true では不可)----
  "separation": {
    "included":            true,
    "competitor_universe": [ "<比較対象の全列挙>" ],
    "result":              { "matrix": "<比較行列>" } | { "result_digest": "<sha256>" },
    "forbidden_values":    { "handling": "MALFORMED" | "reject_with_reason", "list": [ "line" ] },
    "dummy_fixture":       {                                // CV-9-5 / §1.3.2
      "id": "<ID>", "normalised_input": "<入力層の正規化値>",
      "normalised_output": "<出力層の正規化値>",
      "discriminating_power": { "input_layer_novel": true, "output_layer_novel": true },
      "expected": "<事前登録の期待値>", "observed": "<実測>", "verdict": "PASS"
    }
  },

  // ---- CV-8: 判定粒度(P94-5.1(6): 既定値なし)----
  "chi_P_criterion": {
    "value":   "exact" | "conjugacy_class",                 // "line" は禁止値・既定値は置かない
    "justification": "<conjugacy_class = 不変形 / exact = generator・orientation を固定した場合のみ>",
    "generator_fixed":   true | "n/a",                      // value=="exact" のとき必須
    "orientation_fixed": true | "n/a"                       // 同上
  },

  // ---- P94-5.1(9): 代表元と不変量の分離 ----
  "representative_vs_invariant": {
    "exact_representative": { "value": "<値>", "depends_on":
        { "model_id": "<sha256>", "uniformizer_id": "<記号>", "orientation": "<向き>",
          "lift": "<整数持上げ等>" } },
    "invariants":           { "class": "<類>", "order": "<位数>" }   // これらは上記に依存しない
  },

  // ---- CV-10: 有効出所連鎖(P94-5.1(7))----
  "effective_source_chain": [
    { "role": "original",  "path": "<path>", "digest": "<sha256>" },
    { "role": "supersedes","path": "<path>", "digest": "<sha256>" },
    { "role": "erratum",   "path": "<path>", "digest": "<sha256>", "scope": "<何を撤回/訂正したか>" }
  ],
  "effective_source": "<この cert の主張が現在依拠する出所(上の連鎖の末端)>",

  // ---- CV-11: 封印回収可能性(P94-5.1(8))----
  "seal_recoverability": [
    { "fixture_id": "<ID>", "digest": "<sha256>", "vault_reference": "<金庫内の参照子>",
      "restore_preflight": "PASS" | "FAIL" | "NOT_RUN", "checked_utc": "<ISO8601>" }
  ],

  // ---- 水準 ----
  "level":             "PB3" | "PB4"                        // 水準の混同禁止(p93 追補 §3.3)
}
```

**規範**:
1. 該当しない欄は**省略でなく `"n/a"`** と書く(欠品と非該当を区別する)。
2. `chi_P_criterion.value: "line"` を含む cert は **MALFORMED**。**`chi_P_criterion` を省略した cert も MALFORMED**(既定値を置かないため・P94-5.1(6))。
3. `roundtrip_witness` に自己逆元の witness しか無いものは**証拠として無効**(§1.1)。小宇宙では `mode: "exhaustive"` を優先する。
4. 二実装照合の cert では `comparison_target` の欠落を **MALFORMED** とする(裁定 313)。**prose のみ(`as_function_of` だけ)で `function_a/b` と digest を欠くものも MALFORMED**(P94-5.1(2))。
5. `separation.included: true` だけで `competitor_universe` と結果(行列 or digest)を欠くものは **MALFORMED**(P94-5.1(3))。
6. **cross-checked を主張する cert** は `effective_source_chain`(CV-10)と、封印物を使うなら `seal_recoverability`(CV-11)を**必須**とする。
7. **`representative_vs_invariant` の混記を禁止**: 代表元の値を不変量の欄に書いた cert は **MALFORMED**(格の過大表示の直接原因・CV-7 の記法規律)。

---

## 3. 手順則 **IF-FIRST**(interface first)

> **二実装が突き合う場面では、実装の前に比較インターフェースを凍結する。**

1. **凍結対象** = ①比較する対象 ②**正規形(NF)** ③合否等式の一覧 ④合格形(**分離条件を含む**・§1.2) ⑤両側の `conventions_used` 宣言。
2. **生比較の禁止**。先例 = EP の **NF 方式**(裁定 311): 生 field 比較を禁じ、正規形 NF(4 欄)を spec §4.1 に凍結、各 lane が**独立に** NF を計算し NF 同士を 5 等式(N-1〜N-5)で比較。
3. **独立性は壊れない**。「**NF は形式契約であって共有実装ではない**」(`lanea_native_semantics_v1.md` §4)。逆に共有 helper 実装を配ると独立性偽装になる(裁定 305 (a) 禁止・sol75 精神)。
4. **条項は両側へ同時に降ろす**(裁定 311 C-5)。片側耳打ちは独立性違反。
5. **合格形の先例** = C-β の **S6 二条件**(裁定 313・§1.2)。
6. **順序**: インターフェース凍結 → 各側実装 → 照合。**不一致が出てから機構を推測しない** — 先に両側の入出力仕様を突き合わせる(裁定 313 ★教材)。

---

## 4. 限界(射程宣言)

- **完全仕様ではない**。**未発明の概念の規約は事前列挙できない** — 本台帳は「**既知規約の中央化 + 初接触時の即文書化**」であって、これを満たせば規約事故が起きないという主張では**ない**。
- **宣言は正しさを含意しない**。`conventions_used` が全欄埋まった cert は「規約が**監査可能**」なだけで「規約が**正しい**」ことは意味しない。裁定 278 では**両層とも内部的には整合**していた — 台帳が買うのは「二つの宣言を 1 回の diff で突き合わせられる」ことだけである。
- **格の差**。CV-1 のみゲート通過済み正典、CV-5/CV-6 は定理、残りは candidate または手続き。**candidate 項目を「工房が証明した」と引用しない**。
- **規約は取り決めであって定理ではない**(CV-1/CV-2/CV-4)。台帳はどれが数学的に正しいかを決めない — **一貫性**だけを要求する。
- **遡及なし**ゆえ、旧 cert の規約は本台帳では保証されない。
- ★ **事故台帳(§0)は悉皆調査ではない**(旧【CL-5】をここへ移設・**恒久の射程宣言**)。§0 は「今週分 + grep で確認した既知例」であり、同型の未発見事故がありうる(`convention_dictionary_W_v1` 【WDICT-3】と同じ留保)。**§0 の件数を「工房で起きた規約事故の総数」として引用してはならない。** これは調査すれば閉じる種類の項目ではなく(非存在の証明になる)、**常に付す留保**である。

---

## 5. 未閉鎖項(v1.1 で更新)

| # | 状態 | 内容 |
|---|---|---|
| **【CL-1】** | ★ **格下げ(部分閉鎖)** | 本稿は **candidate** のまま。ただし **Sol 便 94 F94-5.1 で CV-1〜8 の方向は承認**され、**F94-5.2 の CV-9 規範文は v1.1 §1.3.1 に逐条で採用**、**P94-5.1 の 9 項は §1.3/§1 表/§2 に編入済**。⟹ 残るのは**司令塔検分**と**次便での条件履行確認**のみ。正典としての引用は引き続き不可 |
| **【CL-2】** | **未閉鎖(先鋭化)** | `conventions_used` の**遡及なし**。v1.1 で問いを絞る: 遡及の価値があるのは「**cross-checked 以上の格を主張している既存 cert**」に限られる(それ以外は遡及しても格が変わらない)。⟹ 決めるべきは「その集合を列挙して CV-10 の `effective_source_chain` だけ後付けするか」の一点。**司令塔裁定待ち** |
| **【CL-3】** | ★ **CLOSED(v1.1)** | 正典 §1.5.1 へ **W-5/W-6 を追記しない**。(W-^)(W-nf) は **CV-2 に一本化**する。**理由**: (i) 正典はゲート通過済みの凍結面であり、candidate 由来の番号を足すと「ゲートを通った番号」と「通っていない番号」が同じ体系に混在する、(ii) 番号体系の二重化それ自体が新しい事故源(【CL-3】原文の懸念)、(iii) v1.1 で台帳が**生きた正本**として機能する体裁が整ったので、追記先を台帳に一本化できる。**⟹ 正典は凍結・台帳が増える、という一方向を規約とする。**(数学者の起草判断 — 司令塔レビュー対象) |
| **【CL-4】** | ★ **CLOSED(CV-6 へ吸収)** | `Rev` の置き場所の必然性は、**CV-6(反準同型の型付け)の特例**として説明が閉じる: $\Psi$ が反準同型であることは「精 → 粗のラベル経路上に**順序反転がちょうど 1 個**必要」を意味し、`Rev` はその反転を置く**境界の指定**である(2 個置けば打ち消し、0 個なら型が合わない)。**移植条件**も同時に定まる: 別の窓へ移植してよいのは、**その窓の $\Psi$ が再び反準同型であることを cert の `opposite` 欄で宣言・検査した場合に限る**。⟹ 「どこに置くか」は規約、「1 個必要」は定理(CV-6)、「移植可否」は検査可能な条件 |
| **【CL-5】** | ★ **CLOSED(§4 へ移設)** | 悉皆調査していないという留保は**閉じる種類の未閉鎖項ではない**(閉じるには非存在証明が要る)。⟹ **恒久の射程宣言**として §4 へ移設した |
| **【CL-6】** | ★ **CLOSED(P94-5.1(6))** | CV-8 の **既定値は置かない**。`conjugacy_class` は不変形、`exact` は **generator / orientation を固定した場合にのみ**許す。既存 cert(`u7_cbeta_final_20260801.json` の `"exact"`)は裁定 312(b) の「同答」により**実害なし**だが、v1.1 以後は `chi_P_criterion.justification` と `generator_fixed` / `orientation_fixed` の記入が必須 |

### 5.1 v1.1 で新たに開いた項

| # | 内容 |
|---|---|
| **【CL-7】** | **CV-10 / CV-11 の番号付与**は数学者の起草判断(§0 冒頭の改訂記録参照)。「型強化を新規約として立てる」境界は一般には自明でない — 司令塔が別配置(例: §2 の欄のみ)を選ぶなら差し替える |
| **【CL-8】** | **schema の実装コスト**。v1.1 の `conventions_used` は v1 より欄が増えた。**全欄必須にすると小さな probe cert が書けなくなる** — 「cross-checked を主張する cert は全欄必須 / 単系統の探索 cert は縮約版」という**二層適用**が要るかもしれない。未検討 |
