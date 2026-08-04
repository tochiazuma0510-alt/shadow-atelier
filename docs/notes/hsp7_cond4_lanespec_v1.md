# HS 発火条件 4 — helper 非共有三レーンの発注設計書(v1.1)

- 起草: 実装担当(短命)・2026-08-04(v1)/ 2026-08-04 改版(v1.1・全指摘採択)
- 委嘱: 司令塔(裁定 435「発火条件4の発注設計書を起草せよ」/ falsifier 前哨差戻し「全指摘を採択・v1.1へ改版」)
- 正本参照: `sol/sol_reply_101_math28.md` P101-1(条件1〜6)/ `docs/notes/hs_prop7_translation_v1.md` §5.3 項目2・§8.3.2〜8.3.4・§8.6・§8.7・§9 / `docs/notes/conventions_ledger_v1.md` CV-9 §1.3・CV-13・§2 `conventions_used` / `search/certs/hsp7_cond2_p7_20260804.json`
- **判読書**: `docs/notes/hsp7_cond4_lanespec_falsifier_v1.md`(反証前哨・差戻し・重大9件+要修正10件+軽微5件)。本版はその全指摘を採択し反映する。**改版後は falsifier 再前哨 → 通過後に発注**、の順は不変。
- 本稿は**発注設計書**。実装・実行はしない。

## 変更履歴(v1 → v1.1)

| # | 変更 | 対応する指摘 |
|---|---|---|
| 1 | 認可境界を二段ゲート化(較正走のみ発注・悉皆列挙は別章へ隔離) | R-1 |
| 2 | CV-9 主検問を発注と同時点(§5)に移動、副検問(§7)と分離 | R-2 |
| 3 | cert 骨格に `conventions_used`(cond2 の8欄)・`comparison_target`・`competitor_universe`・`dummy_fixture` を復元 | R-3, R-17 |
| 4 | 交換形式を「x,y の語のみ」に固定(正規形禁止)・Lane P の式に j を復元 | R-4 |
| 5 | ★ **NW-P7 の phantom 引用 W101-1.4 を訂正**。正体は W100-1.4・§8.3.4 で適用済み。family 限定 control(5元中5元 PASS)と S-3 を残置・復帰 | R-5(最重要) |
| 6 | Lane P の継承を stage1-3(構成)のみに限定、stage4_eval.g(ρ/N_ρ 評価)は継承禁止。§2 表と §3 本文を新しい絞りで揃えて書き直し | R-6 |
| 7 | S-8(既存・N vs N₀ 較正失敗)と S-9(新設・Lane S/V 不一致)の比較対象を分離明記。cert 骨格に両方を逐語収載。Lane V の universe に N₀ を追加 | R-7 |
| 8 | Lane V を Lane S の通過集合限定でなく**全候補集合上で独立判定**させ、PASS/FAIL 両側の突合表を作る設計に変更 | R-8 |
| 9 | Lane S/V の実行を stage 資産の無い isolated worktree に固定(自己申告 boolean は補助) | R-9 |
| 10 | Lane S/V に負の較正(𝔥₃ 方向 = must-fail probe)を追加 | R-10 |
| 11 | 較正アンカー参照を二相化(自分の測定値を先に固定 → その後でアンカー cert を開く) | R-11 |
| 12 | 司令塔突合を「手で比較」から「機械合成スクリプト+ハッシュ」に統一、第四の主体の import 禁止表を追加 | R-12 |
| 13 | 各レーンの出力を PASS/FAIL/UNKNOWN の三値に、UNKNOWN の置き場を cert 様式に明記 | R-13 |
| 14 | 計算量予算表(候補数・時間・メモリ・8GB cap・超過時の行き先)を新設。Lane S の通過件数は「予言でない」と明記 | R-14 |
| 15 | 付録 A の family サイズの理由を訂正(族の大きさ = p であって \|𝒳_N\| = p−1 ではない) | R-15 |
| 16 | P 二重実装の独立性評価を正確化(実の独立性は hexagon 評価の簡約 vs full にある) | R-16 |
| 17 | CV-9 分離表の判読可能な軸(生成元記号・交換子規約・向き・j の像・serialization)を明示 | R-17 |
| 18 | CV-13(向き自己検査・外部 anchor 必須)への言及を追加 | R-18 |
| 19 | Lane V の数学的定義出典の節番号を特定 | R-19 |
| 20 | `candidates_in` 自身の digest を cert 骨格に追加 | R-20 |

---

## 0. 位置づけと認可境界(発火条件4とは何か・どこまでを発注するか)

`hs_prop7_translation_v1.md` §8.6 の HS 本走・発火前チェックリスト(5 条):

| # | 条件 | 状態 |
|---|---|---|
| 1 | NW-1 を省略記号なしの verbal subgroup として一意定義 | 履行済(§8.7・紙) |
| 2 | p=7 の構造確認(NW-P3/NW-P5 の標的商での直接確認) | 履行済(裁定435・`hsp7_cond2_p7_20260804.json`) |
| 3 | m=0 finite dummy family を exact group element として構成し、hexagon/charming/SURJ/PENT を**別々に**判定する | 構成は紙で履行済。4判定の分離実装は本稿のレーン割当対象 |
| 4 | 探索・full B₃/N hexagon・K(0,5)/W PENT の三レーンを **helper 非共有**にする | 本稿の主題 |
| 5 | CV-9 判読まで cross-checked と呼ばない | 遵守中 |

### 0.1 ★ 二段ゲート(R-1 対応 — 認可境界の分割)

P101-1 末(逐語): 「条件2が通っても許可されるのは**次段の実装設計まで**であり、shadow 全掃引…は許可しない」。本稿が発注する範囲を、以後この一行で固定する:

> **本 lanespec が発注するのは「レーン構築 + 較正走(NW-P6/P7/P8 + 負例 fixture、条件3の分離判定を含む)」までである。窓 NW(7) 内の悉皆列挙(候補 705,894 対の全数列挙)は「本走」であり、本 lanespec の認可範囲に含まれない。**

- **較正走**(本稿が発注するもの)= dummy family(t=0..6 の7元、NW-P6)+ p=5 control family(5元、NW-P7)+ N/N₀ 較正(NW-P8)+ 𝔥₃ 方向の負例 fixture(R-10)。候補規模は高々数十件、GAP の pc 群構築コストのみ。
- **本走**(本稱の認可範囲外・別章 §10 へ隔離)= P 内の全 charming candidate(6 × 117,649 = 705,894 対)の悉皆列挙とその PENT 判定。

「窓内悉皆列挙 ≠ shadow 全掃引」かどうかの一行確定は**まだ得ていない**(W101-6 は「三レーン cross-check」と「本 shadow 掃引」を別項目として並べており読みが割れる、falsifier R-1 指摘)。本稿は**安全側**に倒し、悉皆列挙を較正走と同じ発注に含めない。§10 に本走の隔離章を置く。

---

## 1. 三レーンの定義(較正走の範囲に限定・R-1)

### Lane S(探索・Search)

- **入力**: 窓定義 NW(7)(`hs_prop7_translation_v1.md` §8.7.3 定義 NW(p) を p=7 で固定)。
- **やること(較正走の範囲)**:
  1. exact pc presentation of P = F₂/(γ₅(F₂)F₂⁷) を**自前で**構築する(stage1-4 のいずれも import しない、§2/§3)。
  2. 簡約 hexagon **(3.10)(3.11)** で、**§0.1 の較正走が要求する候補のみ**を判定する: dummy family(m=0, f̄=h₄ᵗ, t=0..6)・𝔥₃ 方向の負例(m=0, f̄=h₃ᵘ 相当、u は §8.3.3 の代表元、R-10)。**悉皆列挙は行わない**(§10 の本走で扱う)。
- **出力**: 上記候補それぞれについて PASS/FAIL/UNKNOWN(§6 の三値、R-13)。使用した簡約 hexagon の式の逐語。
- **やらないこと**: full B₃/N 上の (3.3)(3.4) は評価しない。K(0,5)/W にも触れない。P 内の全候補列挙(§10 の本走に属する)。

### Lane V(検証・Verify)

- **入力**: 窓定義 NW(7)、および NW(7) の control 窓 N₀(NW-P8 用、§4)。B₃/N・B₃/N₀ を**自前で**組む(Lane S の P オブジェクトを import しない)。Lane S の cert から**候補の値のみ**(m の整数値・x,y の語)を受け取る。
- **やること**:
  1. 較正走と同じ候補集合(dummy family・𝔥₃ 負例)について、**full B₃/N** 上で **(3.3)(3.4)** を評価し独立に再判定する。
  2. ★ **R-8 対応**: Lane S から受け取った候補**だけ**でなく、Lane V 自身が独立に構成した**同じ候補集合の全体**(Lane S の PASS/FAIL 両方の申告を含む)に対して判定を行う。すなわち Lane S が「FAIL」と申告した候補についても Lane V は自分で判定し直す。両者の判定を**候補ごとに突き合わせ**、(PASS,PASS)(FAIL,FAIL)(PASS,FAIL)(FAIL,PASS)の 4 区分すべてを cert に残す。これにより Lane S の false negative(誤って落とした候補)も検出可能になる。
  3. NW-P8(N vs N₀ の full (3.3)(3.4) 判定の食い違い)を担当(§4)。
- **出力**: 候補ごとの PASS/FAIL/UNKNOWN(N・N₀ 両方の窓について)。Lane S との**4区分突合表**(§6)。
- **やらないこと**: K(0,5)/W には触れない。Lane S の中間コードを読まない。

### Lane P(pentagon・PENT)

- **入力**: 窓定義 NW(7)。Lane S/V の cert から候補の値(m の整数値・x,y の語のみ、正規形不可、§2 R-4)。
- **やること**: K(0,5)/W(W = γ₅(K(0,5))K(0,5)⁷)上で
  \[ \mathrm{PENT}_W([m,\bar f]) \iff \bar\rho^4(\bar f)\,\bar\rho^3(\bar f)\,\bar\rho^2(\bar f)\,\bar\rho(\bar f)\,\bar f = 1 \ \text{in}\ Q,\qquad \bar f := j(f)W\in Q \]
  ★ **R-4(b) 対応: j を式に明示復元した**(v1 は `f̄` を P 側・Q 側で使い回す正本の記法をそのまま転記し、j の適用が曖昧だった。cond2 cert の `jh4_word` 規約 — j(x)=x12, j(y)=x23 — をそのまま使う)。
  K(0,5) の構成(B₄ Artin 表示 → PB₄ の RS → Δ₄² での商 → sphere row-product 辞書 → ρ)は**発火条件2の stage1-3 のみを継承**(§2/§3、stage4 は継承禁止 — R-6)。
- **出力**: NW-P6(h₄ᵗ family, t=0..6, 個別 PASS/FAIL/UNKNOWN)・NW-P7(付録A の NW(5) 登録票のもとで p=5 control family, t=0..4)・NW-P8 の PENT 側該当欄(N vs N₀ の PENT 判定、Lane V が担う hexagon 側と対になる)・𝔥₃ 負例(R-10、PENT は FAIL しない可能性がある点に注意 — §8.3.3 は「hexagon が exact でない」だけで PENT の予言は無い。UNKNOWN でよい)。
- **やらないこと**: hexagon 判定はしない。B₃/N 側の (3.3)(3.4) を再評価しない。ρ/N_ρ の評価コードを stage4 から流用しない(R-6 — NW-P6 が cond2 の再実行になり恒真化することを防ぐため、Lane P は N_ρ 評価を**新規に**書く)。

### interface 図(データフローのみ・実装は含まない)

```
        NW(7)/NW(5)/N0 の紙の定義(SS8.7)
           |         |         |
      (各レーンが独自に P/B3N,B3N0/K05W を実装)
           |         |         |
       [Lane S]  [Lane V]  [Lane P]
           |         |         |
   candidates(x,y語のみ) --> Lane V が全候補を独立判定(R-8)
           |                     |
   candidates(x,y語のみ) --------------------> Lane P が PENT 判定
                                               |
                                    第四の主体: 機械合成スクリプト(SS7)
                                               |
                            CV-9 副検問(3cert+集約certの事後整合性確認)
```

Lane 間を流れるのは**候補の値(m の整数値・f を x,y の語で表した文字列)のみ**。★ **R-4(a) 対応: 「正規形」の選択肢を削除した**(v1 は「語または正規形」としていたが、ANUPQ の pcgs は presentation・生成元順序に依存し、独立再構築された P では正規形が解釈不能になる。交換形式は抽象生成元 x, y の語に一意固定)。GAP オブジェクト・中間関数・helper モジュールは一切流れない。

---

## 2. import 禁止境界(何を読んでよい/いけないか・R-6/R-9)

| 対象 | Lane S | Lane V | Lane P |
|---|---|---|---|
| `docs/notes/hs_prop7_translation_v1.md`(定義・紙の証明) | ○ 読む(定義の一次典拠) | ○ 読む | ○ 読む |
| `sol/sol_reply_101_math28.md`・`sol/sol_reply_100_math27.md`(W100-1.4 の正本) | ○ 読む | ○ 読む | ○ 読む |
| 他レーンの driver スクリプト本体 | ✗ 禁止 | ✗ 禁止 | ✗ 禁止 |
| 他レーンの GAP セッション内オブジェクト・中間表現 | ✗ 禁止 | ✗ 禁止 | ✗ 禁止 |
| 他レーンの cert(候補の値のみ) | (該当なし) | ○ Lane S の cert から `(m, x-y語)` の値を読む(判定関数は読まない) | ○ Lane S/V の cert から候補値を読む |
| `search/probe/hsp7_gap_v1/stage1_pb4.g`(B₄/PB₄構築)・`stage2_k05.g`(K(0,5)構築・辞書・fail-closedアンカー) | ✗ 禁止 | ✗ 禁止 | ○ **継承可**(§3) |
| ★ `search/probe/hsp7_gap_v1/stage3_gen_setup.g`(バッチ setup 生成の**コード**) | ✗ 禁止 | ✗ 禁止 | ✗ 禁止(付録Bの**手順の文章記述**のみ共有可、コードは読まない — Lane P も含め全レーン不可) |
| ★ `search/probe/hsp7_gap_v1/stage4_eval.g`(ρ/N_ρ/RhoPow/jh4 の評価コード) | ✗ 禁止 | ✗ 禁止 | ★ **✗ 禁止(R-6 — v1 は Lane P に○としていたが誤り)**。NW-P6/NW-P7 の判定コードは Lane P が新規に書く。継承してよいのは K(0,5) の**構成**(stage1-3)までで、**評価**(stage4)は継承しない — さもなくば NW-P6 が cond2 の再実行になり恒真になる(falsifier R-6) |
| `search/probe/hsp7_v1/*.py`(Lie環側 python 検算) | ✗ 禁止 | ✗ 禁止 | ✗ 禁止(群側と Lie環側は別建て) |
| GAP 共通 utility(`gap.ps1` 等の出力整形 prelude) | ○ 可 | ○ 可 | ○ 可 |
| ANUPQ SetupFile バッチ**手順**(付録Bの文章記述のみ、コード非接触) | ○ 可 | ○ 可 | ○ 可 |

### ★ R-9 対応: import 禁止の物理化(自己申告から実行環境隔離へ)

v1 は `imports_forbidden_check` という**自己申告 boolean**のみで、`.g` ファイルには「読んだ」痕跡が残らないため検証不能だった(台帳 CV-13 の教訓: 「規約メモでは止まらない、止まるのは実行時 assert のみ」)。以後:

- **Lane S・Lane V は `search/probe/hsp7_gap_v1/` が物理的に存在しない作業ディレクトリ(git worktree、または新規クローン)で実行する。** これを発注条件に明記する — 実装インスタンスは `Agent` の `isolation: "worktree"` を使い、`search/probe/hsp7_gap_v1/` を含む親ブランチから分岐させず、当該ディレクトリを含まないクリーンな worktree を割り当てる(あるいは委嘱プロンプトで当該パスへの `Read`/`Grep` を明示禁止し、cert にその制約が守られたかの実行痕跡 — bash 履歴・tool-call ログ — を添付させる)。
- 自己申告 boolean(`imports_forbidden_check`)は**補助情報**として残すが、判定の根拠にはしない。判定根拠は「そのファイルが存在しない環境で完走した」という物理事実、および発注プロンプト・tool-call ログの digest 束縛(§7)。
- Lane P は継承対象(stage1-3)のみを含む縮小 worktree(または通常の作業ディレクトリだが `stage4_eval.g` を削除したコピー)で実行する。

---

## 3. 既存 stage1-4 資産の継承先 — **Lane P に stage1-3 のみ限定継承(R-6)**

### 継承してよいもの

`search/probe/hsp7_gap_v1/stage1_pb4.g`(B₄/PB₄ 構築・index確認・RS)・`stage2_k05.g`(K(0,5) 構築・sphere row-product 辞書・fail-closed アンカー)。この2本は「K(0,5) という**対象の構成**」であり、判定ロジックを含まない。

### ★ 継承してはいけないもの(v1 からの訂正・R-6)

`stage4_eval.g` は**継承しない**。実物には `rhoQ := GroupHomomorphismByImages(...)`・`RhoPow`・`jh4`・`N_rho_jh4` の評価一式が入っており、これをそのまま使うと NW-P6/NW-P7 が「cond2 と同一コードの再実行」になって**恒真**になる(§8.10 の紙の議論どおり: γ₄(Q) は初等アーベルで j(h₄ᵗ)=j(h₄)ᵗ、N_ρ(j(h₄ᵗ)) = N_ρ(j(h₄))ᵗ が代数的に従うので、cond2 が既に出した `N_rho_jh4 ≠ 1` から「t=0 のみ PASS」は紙で出る — これ自体は正しい数学だが、**同じコードを再実行して確認しても新しい検証情報は増えない**)。Lane P は ρ の適用・N_ρ の評価・h₄ᵗ の生成をすべて**新規に**書く(K(0,5) の presentation という対象だけを stage1-3 から継承する)。

`stage3_gen_setup.g` の**コード**も継承しない(SetupFile のコマンド列生成は Lane P が自分の presentation から自分で行う)。ANUPQ バッチの**手順**(付録B)のみ共有。

### 理由(継承範囲を stage1-3 に絞った上での妥当性)

1. K(0,5) の構成は Lane P 固有の対象であり、Lane S/V はそもそも必要としない。
2. P 自体の構築は Lane S・Lane P 双方が要るが、**司令塔裁定によりこれは各レーンが独立著者で再構築する要件**である(単なる許容ではなく要求)。Lane S は stage1-4 のいずれも import せず P をゼロから構築する。突合は共有 helper なしの数値アンカー(位数・LCS 層・アーベル化)で司令塔集約 cert(§7)にて行う。
3. ★ **R-16 対応(独立性評価の正確化)**: P の二重実装(Lane S と Lane P 側の stage1)が買う独立性は限定的である — どちらも 2 生成自由群の class4/exponent7 の p-quotient であり、同じ `pq.exe` を同じ ANUPQ 経路(付録B)で叩く。実質的な自由度は生成元の記号・pcgs の並びだけで、そこはむしろ R-4 の交換形式問題の原因側になる。**実の独立性は hexagon 評価そのもの(Lane S: 簡約 (3.10)(3.11) / Lane V: full (3.3)(3.4))にある**。CV-9 の主論拠は P の二重構築ではなくこちらに据える(§8 で修正)。
4. 発火条件2で fail-closed アンカー(K(0,5)^ab=Z⁵・ρ well-defined・ρ⁵=id・ρ≠id)を全 PASS しているため、Lane P が K(0,5) をゼロから作り直すコストは検証価値に見合わない。辞書の精読照合は Sol ゲート案件(発火条件2 cert の状態表参照、本稿の範囲外)。
5. ★ **較正アンカーとしての cond2 cert の使用範囲・読み順(R-11)**: 各レーンは `hsp7_cond2_p7_20260804.json` の既知値(|P|=7⁸・LCS 層 [2,1,2,3]・|[P,P]|=7⁶ 等)を**突合欄限定**で参照してよいが、**二相化する**: (相1) 自分の測定値を出力し SHA-256 を cert に固定する → (相2) **その後で**アンカー cert を開いて突合欄を埋める。この順序をレーンの driver コード自体にコメントで明記し、「測定 → digest固定 → アンカー参照」の順が守られたことを cert 内の timestamp/digest で示す。生成コード(P をどう作るか・候補をどう列挙するか)には一切接触させない。

---

## 4. NW-P6/P7/P8・S-6/S-7′/S-8/S-9・DUM-1/p family・負例 の担当割り当て

### 4.1 NW-P6/P7/P8

| 項目 | 担当レーン | 内容(★ = v1.1 での訂正) |
|---|---|---|
| **NW-P6**(h₄ᵗ family, t=0..6, PENT PASS はちょうど 1 個 = t=0) | **Lane P**(判定コードは新規、§3) | 定理 DUM-1/p (d) は K(0,5)/W 側の値そのものの主張。★ **R-6 系の位置づけ**: cond2 が既に `N_rho_jh4 ≠ 1` を出しているため、NW-P6 は代数的にはそこから従う系であり「新しい数学的情報を測る」ものではない。Lane P にとっての価値は「**cond2 と非共有の独立実装**が同じ結論(t=0 のみ PASS)を出すことの確認」= **コード整合性の較正**である。cert にこの格付けを明記すること(「新規の数学的発見」と書かない) |
| **NW-P7**(p=5 control) | **Lane P**(別宇宙 NW(5)、付録A) | ★★ **R-5 対応・最重要訂正**: v1 は根拠として「W101-1.4」を引用したが、**この便101番号は実在しない**(司令塔の誤引用・LEDGER裁定435に伝播したため司令塔がerratumを出す — 実装担当の非ではない)。正しい出典は **W100-1.4**(便100)であり、`hs_prop7_translation_v1.md` §8.3.4 が**既に正しく適用済み**。撤回されたのは「p=5 窓一般の情報量はゼロ」「**全候補** control として全 hexagon shadow が 100% PASS」という一般化のみ。**§8.3.2 の m=0 dummy family に限れば P-HSP-5(family 5元中5元 = 全PASS)は有効な control として残置されている**。よって NW-P7 の予言は正本どおり: 「**h₄ᵗ family(t=0..4)は 5 元すべてが PENT PASS する**(ν₄(j𝔥₄) ≡ 0 mod 5 の直接帰結)」。「𝔥₄-座標の fiber 内分離が死ぬ」という言い換えはこの正しい予言の**説明**であって別の弱い予言ではない — 両者は同じ主張(付録A で訂正) |
| **NW-P8**(N vs N₀・c の有無で判定が食い違う m の存在) | **Lane V**(hexagon 側)+ **Lane P**(PENT 側、対応する欄があれば) | N₀(c ∉ N₀)は簡約 hexagon の近道が壊れる窓であり、full B₃/N₀ 上の (3.3)(3.4) 評価が必要(NW-1b (5) 注)。**Lane V の universe 欄に N₀ を追加**(§6、R-7)。★ NW-P8 は **S-8 の比較対象そのもの**(下記 4.2) |

### 4.2 ★ S-6/S-7′/S-8/S-9 の整流(R-7)

v1 は S-8(既存・裁定433 鋳造)を計画から欠落させ、代わりに新設 S-9 の比較対象を曖昧にしたまま「S-8」と誤記した箇所も残っていた(falsifier R-7 実物指摘)。以後、**S-8 と S-9 は別の比較対象を持つ別の規則**として明記する:

| 規則 | 出典 | 比較対象 | 発火条件 | 担当 |
|---|---|---|---|---|
| **S-6** | `hs_prop7_translation_v1.md` §8.7.7 | NW-P3(h₄≠1 in P)・NW-P5(ν₄(jh₄)≠0 in Q) | いずれかが偽 → INTEGRITY_STOP | 発火条件2で既評価済(不変)。条件4では Lane P が NW-P6 の family 版を再評価するたびに同型チェックを都度入れる |
| **S-7′** | 便101 W101-1.1(裁定・S-7 差戻し後の正形) | NW-P2 型の全予言(NW-P6/P7/P8 含む) | いずれかの等号が破れる → `PREREGISTRATION_FALSIFIED/INTEGRITY_STOP`。同 run 内で予言を書き換えない | 全レーン共通。各レーンの cert に自レーンの予言との突合欄を持たせ、不一致が出たら該当レーンのみ停止(他レーンへ伝播させない) |
| **S-8**(既存・正本 §9.3・裁定433) | 数学者鋳造 | ★ **N vs N₀**(𝒳_N 全体での hexagon 判定) | **不一致が 0 件なら** `CALIBRATION_FAILED/INTEGRITY_STOP`(= N と N₀ で判定が食い違う m が**存在しなければならない**、NW-P8 の直接実装) | **Lane V**(N/N₀ 両方の hexagon 判定を持つのは Lane V だけなので、S-8 は Lane V の cert 内で判定する) |
| **S-9**(新設・本稿 v1 提案・司令塔裁定で正式採用) | 本稿 | ★ **同一窓 N 上の Lane S vs Lane V の項目別判定**(N₀ 側は比較対象に含めない — S-8 と競合させない) | **候補が1件でも食い違えば**(集合差または判定ビット不一致、下記で確定) `LANE_DISAGREEMENT` として保留・3レーン全体の cert 発行を停止・人手切り分けまで前進しない | 第四の主体(§7)が判定。「食い違い」の定義: ★ **判定ビットの一致**(候補 (m, x-y語) のキーで Lane S/V それぞれの PASS/FAIL/UNKNOWN を突き合わせ、キーごとに一致するかどうかを見る。R-8 により Lane V は Lane S の全申告に対して判定するので、キー集合自体の差異=Lane S の候補漏れも UNKNOWN 側で検出できる) |

S-8(N vs N₀ の**不一致がゼロなら失敗**)と S-9(Lane S/V の**不一致があれば失敗**)は比較対象が異なるため(前者は N と N₀ という**別の窓**、後者は同じ窓 N 上の**別レーン**)、同一データ上で逆向きに発火することはない。ただし両者とも Lane V の cert に関わるため、Lane V の cert は「N 列・N₀ 列」と「Lane S との突合欄」を明確に分けて持つこと(§6)。

### 4.3 DUM-1/p family の分離判定(条件3)

| 判定 | 担当 | 備考 |
|---|---|---|
| hexagon | **Lane S**(簡約形)+ **Lane V**(full形、R-8 により全候補) | |
| charming | **Lane S** | 候補生成の前提条件 |
| SURJ | **Lane V** | full B₃/N 上の T_{m,f} で判定。系 H8′ により全候補で自動 PASS が期待値 = **識別力ゼロ**(§8.7.6 の申し送り厳守・S-7′ 型の突合に使わない・cert に明記) |
| PENT | **Lane P** | |

### 4.4 ★ 負の較正(R-10)

`hs_prop7_translation_v1.md` §8.3.3 の自己捕獲: **𝔥₃ 方向(u₁+u₂ に対応する語 h₃)は有限窓で exact な hexagon 解ではなく、γ₄ 剰余が残る**。これを Lane S・Lane V 双方の**負例 fixture**として同梱する: h₃ᵘ(u は §8.3.3 の代表元)の family について、Lane S/V は「簡約/full hexagon が exact に成立するとは限らない(mod γ₄ でのみ成立)」ことを検出できるかを検査する。現行の dummy family(t=0..6 の h₄ᵗ)は補題 DUM-HEX により**全 7 元が exact に hexagon を満たす**ため、Lane S/V の較正入力が「全部 PASS」のみになり FAIL を返せるかの検査が無かった(裁定319 C-β-IND と同型の事故、falsifier R-10)。𝔥₃ 方向はこれを埋める**唯一の正本内既知 FAIL 材料**である。

---

## 5. ★ CV-9 主検問の位置(R-2/R-3 — 新設セクション)

台帳 §1.3.1(便94 F94-5.2 逐条): 「(CV-9-1) 主検問(計算前): IF-FIRST 凍結時に、非当事者が二系統の仕様同一性を判読する」「(CV-9-4) 差戻し: 主検問後に仕様または normalizer が変われば、副検問で救済せず主検問へ差し戻す」。v1 は CV-9 を「3 cert 完成後」(§7 相当・副検問のみ)にしか置いておらず、**主検問が計画に存在しなかった**(falsifier R-2、条件5が原理的に閉じない指摘)。

### 5.1 手順(発注と同時に実施)

1. **仕様凍結**: 3 レーンの発注プロンプトを書く時点で、各レーンの `conventions_used` **予定値**(§6 の8欄+新設欄)を本 lanespec に確定して書き出す(本稿の §1・§4 が既にその内容)。この時点で「凍結」とみなす。
2. **主検問**: falsifier が**計算実行前に**、3 レーンの仕様(本 lanespec の該当節)を読み、「Lane S の hexagon 定義」「Lane V の hexagon 定義」「Lane P の PENT 定義」が**同一の対象**(NW(7) の GT-shadow・PENT_W)を指しているか、生成元記号・向き(θ/τ/ρ)・j の像・交換子規約が食い違っていないかを判読する。判定は「同一対象/別対象/判定不能」の三値(CV-9 の裁定型)。
3. **発注**: 主検問 PASS(同一対象と判定)を得てから、3レーン(worktree隔離済み、§2)を並行発注する。
4. **副検問**: 3 cert 完成後、§7 の機械合成スクリプトが作った集約 cert を falsifier が再度読み、実測結果が仕様どおりに得られたか(数値の整合・stop rule の発火有無)を確認する。
5. **差戻し規律**: 主検問後、発注プロンプトや `conventions_used` の予定値に変更が生じた場合(たとえば実装中に生成元の向きを変えた等)は、**副検問で救済せず主検問へ差し戻す**(CV-9-4 逐語)。

---

## 6. 各レーンの cert 様式(R-3/R-7/R-13/R-17/R-19/R-20)

各レーンの cert は独立ファイル。命名:

- `search/certs/hsp7_cond4_laneS_p7_YYYYMMDD.json`
- `search/certs/hsp7_cond4_laneV_p7_YYYYMMDD.json`(N・N₀ 両方を含む)
- `search/certs/hsp7_cond4_laneP_p7_YYYYMMDD.json`(NW(7) 側)
- `search/certs/hsp7_cond4_laneP_p5control_YYYYMMDD.json`(付録A の NW(5) 側、別ファイル)

共通骨格(★ = v1.1 で復元・新設した欄):

```
{
  "schema": "hsp7-cond4-lane{S|V|P}/v1.1",
  "DRIVER_DONE": true,
  "lane": "S" | "V" | "P",
  "generated_by": [...このレーン専用 driver scripts...],
  "imports_declared": [...読んだファイルの網羅リスト...],
  "imports_forbidden_check": {"other_lane_scripts_referenced": false, "other_lane_gap_objects_referenced": false,
                                "note": "補助情報。判定根拠は実行環境隔離(worktree)の事実そのもの(SS2 R-9)"},
  "execution_isolation": {"worktree_path_or_clone_id": "...", "stage_assets_present": false},
  "universe": {
     "note": "...",
     "prime": 7, "class_bound": 4, "exponent": 7,
     "windows": ["N"]   <- ★ Lane V のみ ["N", "N0"] (R-7)。付録A(p=5)は別 universe block
  },
  "conventions_used": {                          <- ★ R-3: cond2 の8欄を復元 + 新設欄(R-17)
     "ledger_version": "...",
     "commutator_convention": "Comm(a,b):=a^-1 b^-1 a b, 左正規化の向き明記",
     "b3_b4_presentation": "...", "pb_n_generator_formula": "...",
     "sphere_row_relation": "... (Lane P のみ)", "K05_eq_PB4_mod_center": "... (Lane P のみ)",
     "generator_symbols_and_order": "...",         <- 新設(R-17)
     "theta_tau_rho_orientation": "...",           <- 新設(R-17)
     "j_image": "j(x)=x12, j(y)=x23 (Lane P のみ)", <- 新設(R-4b/R-17)
     "serialization": "candidates は x,y の語のみ、正規形不可 (R-4a)"
  },
  "comparison_target": "S-9: Lane {S,V} の同一窓 N 上の項目別判定 | S-8: N vs N0 (Lane V 内部)",  <- 新設(R-3/R-7)
  "competitor_universe": "候補は SS0.1 の較正走の範囲(dummy family t=0..6, p=5 control t=0..4, 負例h3) に限定。悉皆列挙は含まない(SS10参照)",  <- 新設(R-3)
  "dummy_fixture": {"positive": "h4^t family (DUM-HEX, 全t exact hexagon PASS)",
                     "negative": "h3^u family (SS8.3.3, exact hexaogn ではない, mod gamma4でのみ成立) -- R-10"},  <- 新設(R-3/R-10)
  "candidates_in": [...他レーンから受け取った値のみ(x,y語)...],
  "candidates_in_source_cert_sha256": "...",
  "candidates_in_own_digest_sha256": "...",        <- ★ 新設(R-20: 自分が実際に読み込んだ値列そのものの digest)
  "calibration_anchor_usage": {"phase1_own_measurement_digest": "...", "phase2_anchor_cert_opened_after": true},  <- 新設(R-11)
  "lane_specific_results": {
     "...": "PASS/FAIL/UNKNOWN の三値で格納(R-13)。UNKNOWN の理由(timeout/評価失敗/代表元取り直し要)を併記"
  },
  "compute_budget": {"candidate_count_planned": "...", "wall_time_cap_s": "...", "mem_cap_gb": 2,
                      "overflow_action": "UNKNOWN として記録・打ち切り、cert に明記"},  <- 新設(R-14)
  "stop_rules": {
     "S6": {"fired": false, "note": "..."},
     "S7prime": {"fired": false, "note": "..."},
     "S8": {"fired": "n/a (Lane V only)", "comparison_target": "N vs N0", "note": "..."},
     "S9": {"fired": "n/a (集約 cert 側で判定, SS7)", "comparison_target": "same-window Lane S vs Lane V"}
  },
  "cross_checked_status": {"status": "n/a", "reason": "single lane; 3レーン揃って主検問PASS+副検問後に格上げ"},
  "provenance": {...}
}
```

**Lane S 固有**: `lane_specific_results.candidate_count_note` に「この件数は事前登録された予言ではなく探索結果である」と明記すること(R-14 — NW-P1〜P8 のどれも Lane S の件数を予言していない。較正走の範囲では候補は dummy family + 負例 fixture のみで数十件、悉皆列挙の 705,894 対は §10 の本走まで扱わない)。

---

## 7. 司令塔突合の手順 — 機械合成へ統一(R-8/R-12)

v1 は「3 cert を並べて手で比較」(§1 図)と「機械的に合成」(§5.2-4 相当)が同一文書内で矛盾していた(falsifier R-12)。以後、**突合は必ずスクリプト成果物とする**:

1. **突合スクリプトの著者・独立性**: 突合を行うスクリプト(以下「Lane Σ」)は 3 レーンのいずれの driver とも別著者で書く(3 レーン + Lane Σ = 4 者)。Lane Σ 自身の import 禁止表: 3 レーンの cert(JSON、値のみ)は読んでよいが、3 レーンの driver コードは読まない。
2. Lane Σ は 3 cert(+ Lane V の N₀ 内訳)を入力に、次を機械的に合成する:
   - Lane S vs Lane V の**候補ごと4区分表**(PASS/PASS, FAIL/FAIL, PASS/FAIL, FAIL/PASS)→ S-9 の判定はここから機械的に導出(3列目・4列目が1件でもあれば `LANE_DISAGREEMENT`)。
   - Lane V の N vs N₀ の不一致件数 → S-8 の判定(0件なら `CALIBRATION_FAILED`)。
   - Lane P の NW-P6/P7 の PASS/FAIL 一覧 → NW-P2 型予言との突合。
3. 出力は `search/certs/hsp7_cond4_summary_YYYYMMDD.json`(判定を新たに行わない、3 cert の値を転記・突合するだけの文書、SHA-256 を全入力 cert に対して束縛)。
4. **R-8 完全性主張の扱い**: 現行設計(Lane V が Lane S の全申告[PASS/FAIL]に対して独立判定する、§1)で支えられるのは「Lane S の判定は Lane V と一致する(候補ごとに)」までである。「これが窓 N の shadow の**全部**である」という完全性主張は、較正走の範囲(dummy family + 負例)では**そもそも主張しない**(全部という言葉が意味を持つのは §10 の本走のみ)。**選択肢 (iii) を採用**: 完全性主張を降ろし「Lane S の判定(候補ごと)は Lane V と二系統で一致する」までを cert に書く。本走(§10)を発注する際に改めて (i)(ii) のいずれかを選ぶこと。
5. 集約 cert を falsifier へ提出し**副検問**(§5 手順4)を受ける。ここで初めて「cross-checked」を名乗れる。

---

## 8. CV-9 判読に耐える独立性 — 著者・helper・規約の分離表(R-16/R-17/R-18/R-19)

| | Lane S | Lane V | Lane P |
|---|---|---|---|
| **起草者** | 新規インスタンス#1(worktree隔離、§2) | 新規インスタンス#2(#1とも#3とも別、worktree隔離) | 新規インスタンス#3、または発火条件2インスタンスの続き(stage1-3限定継承のみ許容される唯一のレーン) |
| **数学的定義の出典** | §8.7(簡約hexagon (3.10)(3.11)) | ★ **`hs_prop7_translation_v1.md` §2.2 前半 + 定義ノート該当節(3.3)(3.4)**(v1は「定義ノート(3.3)(3.4)」とだけ書きファイル名・節番号未特定だった。R-19対応: full hexagonの一次典拠を §2.2 として明記し、次版で正確な式番号の再確認をLane V起草者に委ねる) | §1.2-1.3(PENT-NORM)・§8.7.3(sphere row-product辞書) |
| **GAP構築** | Lane S独自(Pのみ) | Lane V独自(B₃/N・B₃/N₀) | stage1-3継承(K(0,5)のみ)。stage4は継承禁止(§2/§3) |
| **停止規則の実装者** | driver内(S-7′部分) | driver内(S-7′部分+S-8) | driver内(S-7′部分) |
| **falsifier提出物** | driver+cert+run log+imports_declared+worktree隔離の実行痕跡 | 同左 | 同左 |

### ★ R-17: 判読可能な軸として宣言する `conventions_used` の項目

「実装スタイルが意図的に異なっていることが望ましい」(v1)は判読者が判定できる述語ではなかった。以後、宣言可能な軸を固定する: **①生成元記号と順序 ②交換子規約(`Comm(a,b)=a⁻¹b⁻¹ab` か左右逆か) ③左正規化交換子の向き ④θ/τ/ρ の向き(どちらを先に適用するか) ⑤j の像(x↦?, y↦?) ⑥serialization(x,y語のみ)**。§6 の cert 骨格 `conventions_used` に欄を持たせ、レーンごとに値を書かせる(cond2 cert が既にこの一部を持っている)。

### ★ R-16: P二重実装の独立性評価の正確化

P の二重構築(Lane S・Lane P 側の stage1)が買う独立性は限定的(§3 理由3で既述)。**CV-9 の主論拠は hexagon 評価そのもの(簡約 vs full)に据える**。

### ★ R-18: CV-13(向き自己検査)への言及

台帳 CV-13 は新規 probe の必須テンプレであり、「生成器と受理器が同じ誤った向きを共有すれば**一様な鏡像は素通りする**」「⟹ **外部 anchor または独立 source-map route を必ず併置**」を課す。**本稿の3レーンは全て同じ一次資料(`hs_prop7_translation_v1.md`)から θ/τ/ρ の向きを取っている**ため、3レーン一致は CV-13 の言う「外部 anchor」にはならない(一様な向き誤りがあれば3レーンとも同じ誤りを共有し、一致してしまう)。**外部 anchor 候補**: cond2 cert の `N_rho_jh4_is_identity=false` という**独立に得られた既存の機械値**(stage4、Lane Pの継承外だが「既に出ている値」として突合に使える、§3理由5の較正アンカーと同じ位置づけ)。CV-13 の要求を満たすには、3レーン一致に加えてこの外部値との整合も確認すること。falsifier への申し送り事項とする。

**CV-9判読で falsifier が確認すべき核心**(不変・v1から継承):
1. 3レーンのdriverが実際に別セッションで書かれ、相互import無し(worktree隔離の事実で裏取り)。
2. `imports_declared`が§2禁止表と矛盾しない。
3. 3レーンの判定が独立導出でありながら一致することが「同じ間違いの3回コピー」でないこと(CV-13対応の外部anchor確認を含む)。

---

## 9. 計算量予算・撤退条件(R-14 — 新設)

較正走の範囲(§0.1)での予算:

| 量 | 値/見積り | 効く先 | cap/撤退 |
|---|---|---|---|
| \|P\| | 5,764,801 = 7⁸ | Lane S/V の pc群構築 | GAP `-o 2g`(8GB機・既定cap)。超過なら UNKNOWN として記録・打ち切り |
| 較正走の候補数 | dummy family 7 + p=5 control 5 + 負例(h₃ family、代表元の個数は要 Lane S 起草時点で確定・目安 数元) | Lane S/V/P の判定ループ | 数十件、時間 cap 目安 600秒(gap.ps1既定の重い探索と同オーダー未満のはず) |
| \|Q\| | 7⁴⁰ ≈ 6.37×10³² | Lane P の pc群構築(stage1-3継承) | cond2 で既に完走実績あり(pq batch, 数十ms) |
| ★ **Lane S の候補件数(悉皆列挙時)** | 705,894(6×117,649) | **本走(§10)のみ**、較正走では発生しない | 較正走の発注には含めない。本走を別途発注する際に改めて予算化すること |

★ **R-14 明記事項**: NW-P1〜P8 のどれも Lane S の候補件数を予言していない。較正走の範囲では候補は事前に確定した少数(dummy+control+負例)なのでこの問題は生じないが、**本走(§10)を発注する際は、Lane P のコストが Lane S の通過件数に比例するにもかかわらずその大きさが事前登録されていないことに注意** — 本走発注時に別途この cap を設計すること。

---

## 10. ★ 認可外・別章隔離: 「本走」(R-1)

本節は**発注しない**。将来 P101-1 の認可拡大(司令塔/Sol)を得てから、別の lanespec 改版で発注すること。

- **対象**: NW(7) の窓 P 内の全 charming candidate(6 × 117,649 = 705,894 対)の悉皆列挙 + 3レーンでの hexagon/PENT の全数判定。
- **現状**: `hs_prop7_translation_v1.md` §7.1 格付け表・P101-1 末尾の「shadow 全掃引は許可しない」に照らし未認可。
- **前提条件**(発注前に要確定): (a) 「窓内悉皆列挙」が P101-1 の言う「shadow全掃引」に該当するか一行確定(W101-6 の読みの割れを解消、司令塔/Sol)。(b) §9 の計算量予算を本走の規模(70万対)向けに再設計。(c) §7 の完全性主張の扱いを (i)(ii)(iii) から選び直す(較正走では (iii) を採用したが、本走は完全性そのものが目的なので (i) か (ii) が必要になる可能性が高い)。

---

## 付録 A. NW(5) 事前登録票(草案・NW-P7 用・★ R-5/R-15 で訂正)

★ **本票は草案であり、Lane P が NW-P7 に着手する前に司令塔/数学者の確認を要する。**

★★ **v1 からの訂正(R-5・最重要)**: v1 は「W101-1.4」という実在しない便101項目を根拠に、NW-P7 の予言を「𝔥₄-座標の fiber 内分離が死ぬ」という弱い形に書き換え、かつこれを既に撤回済みの P-HSP-5 と混同していた。**正しい出典は便100 W100-1.4 であり、`hs_prop7_translation_v1.md` §8.3.4 が既に正しく適用している**: 撤回されたのは「全候補 control(全 hexagon shadow が 100% PASS)」のみで、**§8.3.2 の m=0 dummy family に限った control(family 5元中5元 = 全PASS)と停止規則 S-3 は残置・有効**である。以下、この訂正を反映した登録票。

| 項目 | 内容 |
|---|---|
| **宇宙ID** | NW(5)(NW(7)とは別version。S-7′の「別version事前登録から開始する」規律に基づく新規登録) |
| **窓対** | 定義NW(p)をp=5, e=1で固定。N=𝒱(F₂)×⟨c⟩, N₀=𝒱(F₂)×⟨c⁵⟩ |
| **窓の役割** | control専用。discovery標的ではない(篩条件「標数5を排除せよ」はdiscovery標的としてのp=5を禁じるものであり、NW(7)のcontrolとしてのp=5を禁じるものではない) |
| ★ **対象family(訂正)** | h₄ᵗ(t=0..4)。★ **族の大きさ = ord(h₄) = p = 5 であって、\|𝒳_N\|=p−1=4 ではない**(v1はdummy familyが m=0固定・𝒳_N非関与であるにもかかわらず「𝒳_Nの元は4個」と誤った理由づけをしていた。正しい理由: dummy familyはm=0に固定された1パラメータ族 t∈{0,...,p−1}で、その大きさは ord(h₄)=p。NW-P6[p=7側]の「t=0..6=7元」と対称的に、NW-P7[p=5側]は「t=0..4=5元」— どちらも規則は「族の大きさ=p」) |
| ★★ **予言(訂正・正本どおり復帰)** | **「h₄ᵗ family(t=0..4)は5元すべてがPENT PASSする」**(ν₄(j𝔥₄)≡0 mod 5 の直接帰結、§8.3.4「PENT ⟺ tν₄(𝔥₄)=0 が全tで真になる」の正文どおり)。「𝔥₄-座標のfiber内分離が死ぬ」はこの予言の**説明**であり、両者は同じ主張 — 弱い言い換えとして扱わない |
| ★ **停止規則(復帰)** | S-6/S-7′に加え、★ **S-3を計画に復帰**: 「p=5 control(family限定)が5元中5元PASSにならなければ実装バグと判定して本走[較正走]を止める」(§8.3.4逐語の family限定読み替え版)。NW(7)側でS-6/S-7′/S-3が発火していてもNW(5)側の走を自動停止しない(宇宙が違うので伝播させない、逆も同様) |
| **cert命名** | `search/certs/hsp7_cond4_laneP_p5control_YYYYMMDD.json`(NW(7)のLane P certとは別ファイル) |
| **NW-P7の較正上の意味(R-5帰結3の反映)** | ★ **事前登録された予言のうち非自明なPENT PASSを含むのはNW-P7だけ**(NW-P6のPASSはt=0=恒等元の1点のみ)。NW-P7を残すことで、Lane PのPENT判定器が「PASSを正しく出せるか」を検査するfixtureが確保される(「PENT PASS ⟺ 入力が自明」という誤実装ではNW-P7の5元中5元PASSを再現できない ⟹ 識別力を持つ) |
| **未決事項** | (a) NW(5)のP/Qのexact pc presentationをp=7と同じ手順で再構築するか、p=7で構築したK(0,5)のpresentation(pに依存しない)を再利用しp-quotientだけp=5で取り直すか — 後者が自然(Lane P内部の話でLane S/Vとの非共有原則には抵触しない)。(b) 本登録票の発効は司令塔/Solの追認を要する。 |

---

## 付録 B. 環境ノート(全レーン共有可・裁定432/435・falsifier確認済み=裏口として機能しない)

ANUPQ の対話 iostream(`InputOutputLocalProcess` 経由の `PqStart`/`Pq`)はこの Windows/Cygwin GAP 4.16.0 環境で `Error, failed to find any more of line (iostream dead?)` により機能しない(pq.exe 単体は健全・DLL PATH も正しい・パイプのバッファリングが疑われるが未確定)。回避策として、ANUPQ 純正の `SetupFile` オプション(`Pq(G : ..., SetupFile := path)`)でコマンド列をファイルへ書き出し、`pq -i -k -g < setupfile > log` の一方向 stdin リダイレクトで pq.exe を実行し、出力 `PQ_OUTPUT`(GAP 形式2)を `Read()` でそのまま読み込む。この手順は ANUPQ 自身が生成・読解するものであり自作プロトコルではない。全レーンがこの**手順**を使ってよい(環境事実であり判定ロジックではないため helper 非共有の対象外)。**各レーンは自分の窓定義から自分で setup file を生成すること**(生成済みファイルの使い回しは禁止・`stage3_gen_setup.g` の**コード自体**も読まない、§2)。

---

以上、実装・実行は行っていない。改版版は falsifier 再前哨へ提出し、通過後に司令塔が3レーン(+Lane Σ)を発注する。
