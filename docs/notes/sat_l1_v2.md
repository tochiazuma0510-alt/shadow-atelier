# sat_l1 **v2** — Sol 便 90(F90-1)の修理 3 点 + T3-N0 の $t=0$ 補完。**CENT を定理として採択**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-07-31
- 位置づけ: **`docs/notes/sat_l1_v1.md` の修理版・非上書き**(v1 は不変)。本稿は**差分のみ**を正本化する。v1 の本文・表・probe 記録はすべて有効で、下記 4 点だけが v2 で置き換わる。
- 入力: `sol/sol_reply_90_math17.md`(F90-1 全節・F90-2.3)= 司令塔経由で伝達された修理 3 点 + T3-N0 の欠落指摘。**私は便 90 本文を読んでいない**(ブラインド相互監査の規律)。文言の最終突合は司令塔。
- 状態: **CENT = 定理**(Sol 監査 = 条件付き PASS・修理後採択)。**CENT-ORD と $\varepsilon=(-1)^{p+s}$ は系へ昇格**。

---

## 0. 格の更新(v1 → v2)

| 主張 | v1 の格 | **v2(現在)** |
|---|---|---|
| **CENT**: $\ker\widetilde\chi\cong C_{S_n}(w)$ | candidate(11 窓 measured) | **定理**(Sol 監査 PASS・修理 3 点適用後) |
| **CENT-ORD**(閉じた位数公式・奇部 $\ell^{r-p}$) | candidate | **系**(CENT からの直接の帰結) |
| $\varepsilon=(-1)^{p+s}$($\mathrm{sgn}(w)=\mathrm{sgn}(a_1)$) | candidate | **系** |
| 補題 AUT-E | — | **PASS**($\varepsilon=1$ 側も・Sol 判定) |
| XI-INJ | — | **PASS**(修理 2 の一行補筆つき) |
| 補題 SAT-T1 / T3-N0 | 定理(ただし $t=0$ の場合分けが不明瞭) | **定理**($t=0$ を明示的に補完・§4) |
| 定理 SURV / SURV+ | 定理 | **不変**(修理 3 の座標補正後も結論は同一・§3) |
| 壁 P-WALL-2 の一意性系 | — | **無傷**(Sol 判定・T3-N0 の補完に依存しない) |

---

## 1. 修理 1 — $F_{\rm judge}$ と $q=F_{\rm judge}^{-1}$ の分離(XI-C の座標明記)

v1 は $f$ の向きを本文冒頭の注記(2026-07-31 追記)でしか断っていなかった。**v2 では XI-C を座標込みで書く**:

> ### 規約 XI-C(座標の明記)【正本】
> 二つの座標を**記号で区別する**:
> $$f_{\rm hand}\ (\text{本稿 v1 の }f;\ \bar y^{\,f}=f^{-1}\bar yf\ \text{右共役}),\qquad
> F_{\rm judge}\ (\text{judge の }f;\ \text{paper 語 }f^{-1}\bar yf=\text{GAP }f\,\bar y\,f^{-1}\ \text{左共役}),$$
> $$\boxed{\ F_{\rm judge}=q,\qquad q:=f_{\rm hand}^{-1}\ }$$
> 両者は**同一の写像 $T_{0,f}$ を与える**(`hexagon_orientation_ruling_v1.md` §1.4)。$\Xi$ の値 $\alpha$ も同一。
> **定理 SURV は judge 座標で**
> $$F_{\rm judge}(z)\ :=\ a_1\cdot\bigl(a_1^{\,z}\bigr)\qquad\bigl(=f_{\rm hand}(z)^{-1},\ f_{\rm hand}(z)=(a_1^{\,z})a_1\bigr).$$
> **証明書には必ず `f_orientation: "judge" | "handwritten"` を立てる**(混用禁止)。

---

## 2. 修理 2 — XI-INJ′ の一行補筆

v1 §6.2 (b) の自由性は「安定化群 $=C_{S_n}(\langle g,h\rangle)=1$」で済ませていたが、**なぜ $C_{S_n}(\langle g,h\rangle)=1$ か**の一行が抜けていた。補う:

> ### 補題 XI-INJ′【proof・補筆版】
> 生成条件つきの分解 $(g,h)$($\langle g,h\rangle=\langle a_1,b_1\rangle$)に対し
> $$C_{S_n}\bigl(\langle g,h\rangle\bigr)=1 .$$
> **証明.** $\langle a_1,b_1\rangle\in\{A_n,S_n\}$ ゆえ **$A_n\le\langle g,h\rangle$**。$n\ge5$ で $A_n$ は $\{1,\dots,n\}$ 上**推移的**かつ点安定化群 $A_{n-1}$ は自己正規化的だから、$C_{S_n}(A_n)=Z(S_n)=1$($n\ge3$)。$C_{S_n}(\langle g,h\rangle)\subseteq C_{S_n}(A_n)=1$。∎
> **⟹ $C_{S_n}(v)$ の $\mathcal F(v)$ への作用は自由**(v1 §6.2 (b))。**⟹ $\lvert\ker\widetilde\chi\rvert=\lvert C_{S_n}(v)\rvert\cdot N$**(v1 §6.2 (c))。

---

## 3. 修理 3 — $\Xi$ は現実装規約では**反準同型**($\Phi=\Xi^{-1}$ による補正)

**事実**(`strike-r4` の `19_xi_hom_right = true`・`19_xi_hom_left = false`、`norm_embedding` 9 窓も同じ):
$$\Xi\bigl([m_1,f_1]\circ[m_2,f_2]\bigr)=\Xi([m_2,f_2])\cdot\Xi([m_1,f_1]).$$

> ### 訂正 XI-A(v1 §6.1 の言い回しの是正)
> v1 §6.1 は「$z\mapsto\alpha_z$ は準同型(機械確認)」と書いた。**これは正しい**($\alpha_z=z^{a_1}$ で、$z\mapsto z^{a_1}$ は準同型)。誤っていたのは、そこから **$\Xi$ 自体を準同型のように読ませた**点である。正しくは:
> $$\Xi:\ \ker\widetilde\chi\longrightarrow \mathrm{Stab}(\bar x)\quad\text{は\textbf{反}準同型},\qquad
> \boxed{\ \Phi:=\iota\circ\Xi\ (\iota:g\mapsto g^{-1})\ \text{が準同型}\ }$$
> で、$\ker\Phi=\ker\Xi$、$\mathrm{im}\,\Phi=\mathrm{im}\,\Xi$(**部分群としては同一**)。
> **したがって定理 SURV+ の結論**
> $$C_{S_n}(w)\ \subseteq\ \Xi(\ker\widetilde\chi)\ \subseteq\ C_{S_n}(\bar x)$$
> **は不変である**(反準同型の像も部分群であり、$\iota$ で写しても同じ集合)。同様に **定理 CENT-0・壁 P-WALL-2 の非可解性・W-CENT-B の 162 もすべて不変**($\ker\widetilde\chi$ が非可解群を**商にもつ**という言い方は、反準同型でも成立する — 像が部分群だから)。
> **v1 の該当箇所の読み替え**: §6.1 の「$z\mapsto\alpha_z$ は準同型・反準同型?」の欄、§5 系 SURV-2、§10.5.1 定理 SURV+ の全体で、$\Xi$ を**「反準同型 $\Xi$、その補正 $\Phi=\iota\circ\Xi$」**と読む。**位数・構造・包含の主張はすべてそのまま。**

---

## 4. T3-N0 の補完 — $t=0$ を含む全場合分け

v1 §4(補題 SAT-T1)は $r=1,t\le1$ を「残るケース」として一括で扱い、**$t=0$ の扱いが明示的でなかった**。全場合を書き下す。

> ### 補題 SAT-T1 / T3-N0【定理・完全場合分け】
> $\bar y$ の型を $(\ell^{\,r},1^{\,t})$($\ell$ 奇、$n=\ell r+t$)とする。$\alpha\in S_n$ に対し
> $$\mathcal T_\alpha\ne\varnothing\iff C_{S_n}(\bar y)\,\alpha\cap A_n\ne\varnothing .$$
> $C:=C_{S_n}(\bar y)=(C_\ell\wr S_r)\times S_t$ の**奇置換の有無**で場合分けする:
>
> | 場合 | $C$ は奇置換を含むか | 結論 |
> |---|---|---|
> | **$r\ge2$**(**$t=0$ を含む**) | **含む**: 2 つの $\ell$-ブロックの互換は $\ell$ 個の互換の積で、$\ell$ 奇ゆえ**奇** | $\forall\alpha\in S_n$ で $\mathcal T_\alpha\ne\varnothing$ |
> | **$t\ge2$**(任意の $r$) | **含む**: $S_t$ の互換は奇 | 同上 |
> | **$r=1,\ t=1$** | 含まない($C=C_\ell\times S_1$、$\ell$-巡回は偶) | $\mathcal T_\alpha\ne\varnothing\iff\alpha$ 偶。ただし $H=C_{S_n}(\bar x)=C_\ell\le A_n$ ゆえ**全 $\alpha\in H$ は偶** ⟹ 成立 |
> | **$r=1,\ t=0$**(**補完箇所**) | 含まない($C=C_\ell=\langle\bar y\rangle$、$n=\ell$) | 同上: $H=C_{S_\ell}(\bar x)=\langle\bar x\rangle=C_\ell\le A_\ell$($\ell$ 奇ゆえ $\ell$-巡回は偶)⟹ **全 $\alpha\in H$ は偶** ⟹ $\mathcal T_\alpha\ne\varnothing$ |
>
> **⟹ 本族の全窓・全 $\alpha\in H$ で $\mathcal T_\alpha\ne\varnothing$。**($t=0$ は $r\ge2$ か $r=1$ かで上の 1 行目/4 行目に落ちる。)
> **証明.** $\bar y^{\,f}=\bar y^{\,\alpha}\iff f\in C\alpha$。剰余類 $C\alpha$ が $A_n$ と交わるのは、$\alpha$ が偶であるか $C\not\le A_n$ のとき、かつそのときに限る。各場合の $C$ の奇置換の有無は上表のとおり。∎

**壁 P-WALL-2($r=1,t=5$)への影響**: $t=5\ge2$ ゆえ 2 行目に落ち、**補完箇所とは無関係**。Sol の「壁の一意性系は無傷」と一致。

---

## 5. 昇格した系(CENT が定理になったことの帰結)

> ### 系 CENT-ORD【系】
> $w=(2\ell)^p(\ell)^{r-2p}(2)^s(1)^{t-2s}$ のとき
> $$\lvert\ker\widetilde\chi\rvert=(2\ell)^p\,p!\cdot\ell^{\,r-2p}(r-2p)!\cdot2^s s!\cdot(t-2s)!,\qquad
> \lvert\ker\widetilde\chi\rvert_\ell=\ell^{\,r-p}\ \ (\text{標準域}).$$

> ### 系 EPS【系】
> $$\mathrm{sgn}(w)=\mathrm{sgn}(a_1)=(-1)^{p+s}\quad\Longrightarrow\quad \varepsilon=0\iff p+s\ \text{偶},\qquad\varepsilon=1\iff p+s\ \text{奇}.$$

いずれも v1 §7.5.1 の内容で、CENT の定理化によりそのまま系となる(11/11 窓の照合表は v1 のまま有効)。

---

## 6. v1 で**変わらない**もの(確認)

- 定理 RED / 平行移動公式 / SAT-L1 の反証 / 非可換 $Z^1$ の枠組み(§2・§3)
- 定理 SURV(構成)・SURV+(閉じた式)・**定理 CENT-0**(§10.6.3)
- **壁 P-WALL-2**(n=24・$\Xi(\ker)=C_{19}\times S_5$ 非可解 ⟹ $\mathrm{GTSh}$ 非可解)
- **W-CENT-B**(n=18・162 vs PRUNE 18)
- 定理 TRI・$s=1$ トリックの撤回・計数機構(Frobenius + 巡回集合分割 Möbius)
- probe 1–13 の全出力(**ただし $f$ は $f_{\rm hand}$ 座標**・§1)

---

## 7. 残ギャップ(v2 時点)

- **剛性 $N=1$**(CENT の $\subseteq$ の一般窓版)。**ただし $p=s=0$ 窓では定理 CENT-0 で不要**。
- 【GAP-S1】生成条件の紙上証明(11 窓 machine)。$\ell$ 素数 $\wedge\ t\ge3$ では **補題 HOLE**(`tmax_budget_and_holes_v1` §2.1)で閉じた。
- $m\ne0$ 層の一般公式(candidate・未検証)。
- $\ell=25,t=5$ の $T_{\rm trans}$(クラウド発注済)。
