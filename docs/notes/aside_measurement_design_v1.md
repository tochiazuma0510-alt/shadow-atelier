# A 側(算術像)の相方測定 — 設計 v1(第 2 次 ceremony 用・**設計のみ**)

**状態札: `design only / 走行ゼロ / GAP・python 実行ゼロ / cert 未生成 / 112f 工事と並行 / 封印非接触`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-06
- 委嘱: 司令塔(第 2 次 ceremony 設計への追加・**司令塔発の指摘**)「現行判定表(裁定 656)は $\mathcal S_{12}@691$ の値だけで読むが、**$S=2$ のとき『$\mathcal A$ が落ちた(不均衡)』と『どちらも落ちない(釣り合い)』を区別できない**。$\mathcal A$ 側の相方測定を同じ法 691 で設計せよ」
- 入力正本(すべて既在):
  - `docs/notes/b_type_synthesis_design_v1.md` §0.2・§1.1(SYN-0)・§1.4(SYN-1)・§2.1.2($\mathcal A_\bullet$ の定義・ACDIK 公式)・付録 A-3(母関数)
  - `docs/notes/b_type_synthesis_design_v1_addendum_l4b_grt12.md` §1・§2(**判定表 v1** の正本・素数系列・S-ED-7・禁止文 2)
  - `docs/notes/b_type_synthesis_design_v1_addendum_l4_reflection.md` §1・§3(Ihara–Takao 両形)・§1.1【L4-GAP-1】・§4(depth-graded ≠ weight-graded)
  - `docs/scout/l4_grt_dimension_tables_v1.md`(**$\dim\mathfrak{grt}_w$ の一次資料 pin**: $w=1..12$ で $0,0,1,0,1,0,1,1,1,1,2,2$)
  - `docs/notes/edim_semidirect_model_design_v1.md`(模型 $\mathfrak t=\mathfrak n\rtimes\mathfrak h$・$\dim\mathfrak t_{12}=44{,}555$)
  - `search/edim_run_c12_single_prime.py` / `search/edim_semidirect_v1.py`(`GradedLie`)/ `search/certs/edim_c11_run_v1_20260806.json`
  - `docs/notes/bhunt_l1_bridge_v1.md` §4(ACDIK / $\kappa^*_m$ = **BH 器具**の実体)

> ## 非接触・規律の申告
> **機械ゼロ**(GAP も python も起動していない)。封印 3 量非接触・$\mathrm{Im}\,R$/$d_N$ 非接触。**発火は司令塔**。本票は判定文を書かない(ceremony の「**コードは判定文を書かない**」規律を設計側にも適用)。

---

## 0. 一枚まとめ(6 行)

1. **穴は司令塔の指摘どおり**: 判定表 v1 は $\mathcal S_{12}@691$ の 1 値だけを見て「不均衡」と読むが、**$\mathcal A_{12}@691$ は一度も測っていない**(char 0 の母関数値 $\dim\mathcal A_{12}=2$ を暗黙に流用しているだけ)。
2. ★ **$\sigma_m$ の実現に新装置は要らない**: $\dim\mathfrak{grt}_m=1$($m=3,5,7,9$・一次資料 pin)⟹ **$\sigma_m$ は $\mathcal S_m$ の生成元そのもの**。既存ドライバの出力を使うだけ(§2)。
3. **しかも法 691 のデータは既にある**: 裁定 697 で **$k\le11$ は 3 素数すべて完走**(死んだのは $k=12$ のみ)⟹ $\sigma_3,\sigma_5,\sigma_7,\sigma_9$ の 691 実現は**再走なしで取れる**(cert 化されていないなら軽い再走)。
4. **depth と weight を 2 本の別量として測る**(§3): $\mathcal A^{(2)}_{12}$(深さ 2 先頭項・自由 Lie 環側)と $\mathcal A_{12}$(weight-graded・模型側)。**691 合同は前者の言明であって後者ではない**。
5. **判定表 v2 は $(\mathcal S,\mathcal A)$ の 2×2**(§4)。$\mathcal A\subseteq\mathcal S$ ゆえ **$(S,A)=(1,2)$ は数学的に不可能 = バグ検出セル**。
6. **コストは $\mathcal S_{12}$ よりはるかに軽い**(核を取らず括弧と階数だけ)⟹ **112f のメモリ工事と並行して走らせられる**。

---

## 1. 穴の正確な形

判定表 v1(l4b §2)は
> 「$p=691$ で $\dim\mathcal S_{12}=2$ ⟹ **$\mathcal S$ は落ちず $\mathcal A$ だけ落ちる = 不均衡**」

と読む。ここで「$\mathcal A$ だけ落ちる」は**測定ではなく仮定**である。根拠として引かれているのは Ihara–Takao 合同
$$2\{f_3,f_9\}-27\{f_5,f_7\}\equiv0\pmod{691}$$
だが、これは **depth-graded(深さ 2)の言明**であり、**weight-graded の模型 $\mathfrak t_{12}$ 内で $\mathcal A_{12}$ の次元が落ちること**を意味しない(【L4-GAP-1】と §4 の区別が未解消のまま流用されている)。
$$\Longrightarrow\ \boxed{\ \textbf{$S_{12}@691=2$ を「不均衡」と読むには、$\mathcal A_{12}@691$ の実測が要る}\ }$$

---

## 2. 委嘱① — $\sigma_{2i+1}$ の $\mathrm{gr}_k$ での明示実現

### 2.1 ★ 主経路: **$\sigma_m$ = $\mathcal S_m$ の生成元**(新装置ゼロ)

$\dim\mathfrak{grt}_w$($w=1..12$)$=0,0,1,0,1,0,1,1,1,1,2,2$(一次資料 pin・`l4_grt_dimension_tables_v1.md`)。とくに
$$\dim\mathfrak{grt}_3=\dim\mathfrak{grt}_5=\dim\mathfrak{grt}_7=\dim\mathfrak{grt}_9=1$$
⟹ **$\sigma_3,\sigma_5,\sigma_7,\sigma_9$ はスカラー倍を除いて一意**。一方、工房の $\mathcal S_k$ は $k\le11$ で $\mathfrak{grt}_k$ と**次元が一致**(較正済・`edim_c11_run_v1` で $S_{11}=2=\dim\mathfrak{grt}_{11}$)。
$$\Longrightarrow\ \boxed{\ \sigma_m\ (m=3,5,7,9)\ \textbf{の模型内実現} = \mathcal S_m\ \textbf{の(1 次元)解空間の非零ベクトル}\ }$$
⟹ **Ihara 括弧の明示式も、$\kappa^*$ の再構成も要らない。既存 S 側ドライバの副産物である。**

> **【PIN-A-1】**(発火前に取る): 「$\mathcal S_k$ の空間が $\mathfrak{grt}_k$ と**同一視できる**」— 次元一致は較正済だが、**空間としての同定**(模型 $\mathfrak t$ と $\mathfrak{grt}\subset\mathrm{Der}\,\mathrm{Lie}(X,Y)$ の辞書)は工房で明文化されていない。⟹ 同定できないなら、本設計の $\mathcal A$ は「**$\mathcal S_m$ の生成元が張る部分 Lie 環**」と**自前定義**して進む(名前を借りない)。判定表 v2 の意味はそれでも保たれる(下記 §4 の注)。

### 2.2 副経路: **BH 器具(ACDIK / $\kappa^*_m$)は「照合用」に流用可**

`bhunt_l1_bridge_v1.md` §4 の
$$\psi^{\rm ab}_\sigma=\exp\Bigl\{\sum_{m\ge3,\ \rm odd}\frac{\kappa^*_m(\sigma)}{m!}\bigl((X+Y)^m-X^m-Y^m\bigr)\Bigr\}$$
は**アーベル化(深さ 1)**の情報しか持たない ⟹ **$\sigma_m$ の実現そのものには使えない**が、
$$\boxed{\ \textbf{§2.1 で得た }\sigma_m\ \textbf{の「深さ 1 先頭項」が }\mathrm{ad}(X)^{m-1}(Y)\ \textbf{に比例することの照合(第二系統)}\ }$$
には使える。**流用可否の答え: 可(ただし照合用)。**

---

## 3. 委嘱② — depth-graded と weight-graded の区別を**測定でどう表すか**

**2 本の別量として測る**(混ぜない)。

| 量 | 舞台 | 定義 | 691 での**予言** | 一般素数での予言 |
|---|---|---|---|---|
| **$\mathcal A^{(2)}_{12}$** | **自由 Lie 環 $\mathrm{Lie}(X,Y)$**(深さ = $Y$-次数が**native**) | $\{f_3,f_9\},\{f_5,f_7\}$ の**深さ 2 成分**が張る空間の次元 | **1**(Ihara–Takao 合同 $2\{f_3,f_9\}-27\{f_5,f_7\}\equiv0$) | **2** |
| **$\mathcal A_{12}$** | **模型 $\mathfrak t_{12}$**(weight-graded・$\dim=44{,}555$) | $[\sigma_3,\sigma_9],[\sigma_5,\sigma_7]\in\mathfrak t_{12}$ が張る空間の次元 | ★ **2(独立のはず)** | **2** |

> ### ★ 設計の核
> $$\boxed{\ \textbf{691 合同は「深さ 2 先頭項の比例」であって「weight 全体の従属」ではない — これを}\ \mathcal A^{(2)}_{12}=1\ \wedge\ \mathcal A_{12}=2\ \textbf{という 2 値で実測する}\ }$$
> - $\mathcal A^{(2)}_{12}=1$ が出れば **pipeline の自己較正**(既知の合同式を再現できた)。**出なければ実装が壊れている**(合同式は文献既知)⟹ STOP。
> - $\mathcal A_{12}=2$ が出れば「$\mathcal A$ は 691 で落ちない」⟹ **判定表 v1 の『不均衡』の読みは崩れる**(§4 の (2,2) セル)。
> - $\mathcal A_{12}=1$ が出れば **初めて**「$\mathcal A$ が落ちる」が実測になる ⟹ v1 の読みが**測定で裏づけられる**。
>
> **どちらに転んでも情報が出る**(§G.8.1 の再発防止規則の適用)。

> **深さ装置の所在についての正直な注記**: 工房には「**depth-graded を窓の言葉に翻訳する装置が無い**」(発案札 5 (J-iii))。本設計はそれを**回避**している — 深さは**自由 Lie 環側でだけ**使い(そこでは $Y$-次数として native)、模型側は weight のみで扱う。⟹ **新装置の建設を要求しない。**

---

## 4. 委嘱③ — **判定表 v2**($\mathcal S$ と $\mathcal A$ の 2×2)

**前提(数学)**: 算術元は hexagon∧pentagon を満たす ⟹ $\mathcal A_k\subseteq\mathcal S_k$ ⟹ $\dim\mathcal A_k\le\dim\mathcal S_k$(**任意の素数で**)。

$$\textbf{判定表 v2}\qquad(p=691\ \text{での実測}\ ;\ \text{一般素数 2 本での}\ (S,A)=(2,2)\ \text{を較正前提とする})$$

| | **$\mathcal A_{12}@691=2$** | **$\mathcal A_{12}@691=1$** |
|---|---|---|
| **$\mathcal S_{12}@691=2$** | **釣り合い**(どちらも落ちない)⟹ **SYN-0 不発火** ⟹ $k^*>12$ へ。**v1 が「不均衡」と読んでいたセル**(要修正) | ★ **不均衡** = $\mathcal S$ は落ちず $\mathcal A$ だけ落ちる ⟹ **SYN-0 発火 = $k^*=12$ candidate** |
| **$\mathcal S_{12}@691=1$** | **数学的に不可能**($\mathcal A\subseteq\mathcal S$ に反する)⟹ **実装バグ確定** ⟹ S-ED-4 | 両方落ちる ⟹ **段差なし** ⟹ $k^*>12$ へ |
| **その他の値** | 想定外 ⟹ バグ疑い ⟹ S-ED-4 | 同左 |

**v1 からの実質的変更**: v1 は左上セル(**$S=2$ かつ $A=2$**)を「不均衡」と読んでいた。v2 では左上は**釣り合い**であり、**不均衡は右上のみ**。⟹ **「$S_{12}@691=2$」だけでは SYN-0 は発火しない。**

**付帯規律(v1 から逐語継承)**:
- **S-ED-7**: 691 で差が出たら **677・701** で対照し「691 だけが特異」を確認してから段差と呼ぶ。**$\mathcal A$ 側にも同じ手続きを適用**($\mathcal A_{12}@677,701$ も測る)。
- **禁止文 2 件**(v1): 「char 0 で釣り合ったから $k=12$ は空」/「691 で落ちる」を**測る前に**書くこと。**v2 で 1 件追加**: 「**$\mathcal A_{12}@691$ を測らずに『不均衡』と書くこと**」。
- **コードは判定文を書かない**(生値 + RAW_FACT のみ)。判定表の適用は司令塔。

> **【PIN-A-1】が取れなかった場合の読み**: $\mathcal A$ を「$\mathcal S_m\ (m=3,5,7,9)$ の生成元が張る部分 Lie 環」と自前定義すると、$\mathcal A\subseteq\mathcal S$ は**定義から自動**(生成元も括弧も $\mathcal S$ の中)⟹ **表の不可能セルは保たれる** ✓。ただし「$\mathcal A$ = 算術像」という**解釈**は $\mathfrak{grt}$ 同定に条件つき ⟹ 結論文では「$\mathcal S$ の $\sigma$-生成部分」と書く。

---

## 5. 実測指示書 **ASIDE-1**(数学者 → 実装係・設計のみ)

**素数**: $\{2147483647,\ 998244353,\ 691\}$(+ S-ED-7 用に $677,701$ を**別 dispatch**)。

```
# 段 A: sigma の取得(k<=11 は既走 — cert 化されていなければ軽い再走)
for m in [3,5,7,9]:
    S_m := 既存ドライバの解空間(dim=1 を assert; 落ちたら STOP)
    sigma_m := S_m の非零ベクトル (正規化: 先頭項の係数を 1 に)
# 段 B: 模型内の括弧と階数(= weight-graded の A)
v1 := bracket(sigma_3, sigma_9);   v2 := bracket(sigma_5, sigma_7)   # in t_12 (dim 44,555)
A12 := rank_Fp([v1, v2])                                            # 期待 2
# 段 C: 深さ 2 先頭項(= depth-graded の A)  ※自由 Lie 環側で完結
f_m := ad(X)^(m-1)(Y)                                               # 深さ1 先頭項
d2  := 深さ2成分( ihara_bracket(f_3,f_9) ), 深さ2成分( ihara_bracket(f_5,f_7) )
A12_depth2 := rank_Fp(d2)                                           # 期待: 一般素数 2 / 691 は 1
# 段 D: 照合(第二系統・BH 器具)
assert sigma_m の深さ1先頭項 ∝ ad(X)^(m-1)(Y)                        # ACDIK/κ* 由来の形と一致
```
**出力 cert** `search/certs/aside1_<date>.json`: 素数ごとに `A12`, `A12_depth2`, `sigma_norm_ok`, `bracket_dims`, `rank_certificate`(pivot 列)。**判定文は書かない。**

**コスト見積り**: 段 B は $\mathfrak t_{12}$($\dim=44{,}555$)の**ベクトル 2 本の括弧と階数**のみ ⟹ **$\mathcal S_{12}$ の核計算(16GB 壁の原因)とは桁違いに軽い** ⟹ **112f 工事の完了を待たずに走れる**。段 C は自由 Lie 環の低次元計算 ⟹ 秒。

**カナリア**: (a) $\dim S_m=1$($m=3,5,7,9$・全素数)。(b) 一般素数で $A_{12}=2$ **かつ** $A^{(2)}_{12}=2$。(c) **691 で $A^{(2)}_{12}=1$**(既知合同の再現 — **落ちたら実装 STOP**)。(d) $\mathcal A\subseteq\mathcal S$: $v_1,v_2$ が $H_{12}\cap\ker(\nu_{12}\circ j)$ に入ること(**$\mathcal S_{12}$ が計算できたときのみ**・後段の突合)。

---

## 6. IF-FIRST 予言(**各行に「偽ならどう変わるか」**)

| # | 予言 | 偽なら測定値はどう変わるか |
|---|---|---|
| **P-A-1** | $A^{(2)}_{12}@691=1$、一般素数で $2$ | 691 でも 2 ⟹ **合同式の実装が誤り**(文献既知の式を再現できていない)⟹ STOP |
| **P-A-2** ★本命 | **$A_{12}@691=2$**(weight-graded では落ちない) | $1$ が出る ⟹ **判定表 v1 の読みが実測で裏づけられる**(深さの縮退が weight まで伝播している)⟹ 【L4-GAP-1】が**測定で解消**される方向 |
| **P-A-3** | $A_{12}@677=A_{12}@701=2$(S-ED-7 対照) | 677/701 でも落ちる ⟹ **691 の特異性ではない** ⟹ 段差と呼べない |
| **P-A-4** | $\dim S_m=1$($m=3,5,7,9$)が全素数で成立 | 落ちる ⟹ $\sigma_m$ の一意性(=$\dim\mathfrak{grt}_m=1$)と模型の対応が崩れる ⟹ 【PIN-A-1】へ差し戻し |

**★ 予言 P-A-2 の重み**: 真なら **判定表 v1 の左上セルの読みが誤りだった**ことが確定し、**$k^*=12$ candidate は取り下げ**になる(SYN-0 は $S>A$ を要求するが $S=A=2$ なら不発火)。偽なら **$k^*=12$ が実測で支持**される。**どちらでも第 2 次 ceremony の結論が変わる** ⟹ **A 側測定は S 側と同格の本命測定**である。

---

## 7. 停止規則・格・【GAP】

| # | trigger | verdict |
|---|---|---|
| **S-AS-1** | $\dim S_m\ne1$($m=3,5,7,9$) | `SIGMA_NONUNIQUE / STOP` |
| **S-AS-2** | 一般素数で $A_{12}\ne2$ または $A^{(2)}_{12}\ne2$ | `CALIBRATION_FAIL / STOP`(**691 の値を報告する前に止める**) |
| **S-AS-3** | 691 で $A^{(2)}_{12}\ne1$ | `CONGRUENCE_NOT_REPRODUCED / STOP` |
| **S-AS-4** | $A_{12}>S_{12}$(同一素数で) | `IMPOSSIBLE_CELL / STOP`(数学的に不可能 ⟹ バグ) |
| **S-AS-5** | 出力に判定文(「不均衡」「SYN-0」「$k^*$」「段差」)が現れた | `VERDICT_IN_CODE / STOP`(ceremony 規律) |
| **S-AS-6** | 本票に無い量(封印量・$\mathrm{Im}\,R$・深さ $\ge3$ の合同式経路)を計算した | `SCOPE_CREEP / STOP`(【BSY-GAP-1】: 合同式経路は深さ $\ge4$ 使用禁止) |

| # | 【GAP】 |
|---|---|
| **【PIN-A-1】** | $\mathcal S_k\leftrightarrow\mathfrak{grt}_k$ の**空間としての同定**(次元一致は較正済)。取れなければ $\mathcal A$ は自前定義で進む(§4 の注) |
| **【A-GAP-1】** | Ihara 括弧 $\{,\}$ の深さ 2 成分の**符号・正規化**(合同式の係数 $2,-27$ は正規化依存)。**段 C は既知合同の再現をカナリアにしているので、係数の取り違えはそこで露見する** |
| **【A-GAP-2】** | 「$\mathcal A$ = 算術像」の解釈は **Deligne–Ihara 自由性【BSY-GAP-3】に依存しない**(本測定は生成元 4 個の括弧 2 本の階数を見るだけで、自由性を仮定しない)✓ — **これは本設計の利点**として記録 |

**格**: 本測定の出力は **candidate / single-system**。$A_{12}$ の値は**生値**であり、判定表 v2 の適用(= 「不均衡」の宣言)は**司令塔の裁定事項**。
