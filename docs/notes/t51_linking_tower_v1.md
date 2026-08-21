# linking tower $\{L_n\}$ 一括降下の紙上判定 — T-51 回答

**状態札: 数学者判定・司令塔検分前・Sol 未監査**
判定: Claude 数学者 / 2026-08-19 / 委嘱 = 司令塔(Sol `ops/express/20260819_sol_fable_t51_total_linking_tower.md`)
入力: 157dq run 32197397734(修正済 Def 2.9 gate・candidate 124 の $L\to L'=L\cap K_1$ 一 chief descent 成立・CV-9 は falsifier 並行中)。
格: paper candidate。**計算追加なし・紙上判定のみ**。封印非接触。語法: exponent = 冪指数 / index = 指数。
記号: $\ell:PB_4\to\mathbf Z$ = 全リンク数、$K_n=H\cap\ell^{-1}(6\cdot3^n\mathbf Z)$、$L=H\cap\ker\rho_{A_5}$、$L_n=L\cap K_n$。

---

## 0. 一行裁定

**Q1: YES — ただし前件を 1 箇所訂正する。** 「完全 vs 巡回 3-冪」の共通商論法は三水準で成立し $n$ に一様 ✓。**しかし「整数 linking 厳密 0」は hexagon 残差には不十分**である:必要なのは **$PB_3^{ab}=\mathbf Z^3$ での像がゼロ**(五 coface のうち三つの $\ell$-重みベクトルが**行列式 1**で独立なため)。pentagon 残差には $\ell=0$ で足りる。
**Q2: 登録してよい。** 補題 **LT-1**(§2)として、訂正済み前件つきで起草した。
**Q3: 射程限定で足りる。** $\bigcap_nL_n=L\cap\ker\ell$ は**開でない**ので塔は非 cofinal ✓。T33-L10 / T-50 ④ とは**衝突しない** — 逆極限が $\widehat{GT}$ でなく thin 商である旨の一文を §3.3 に用意した。
**Q4: 依存関係は 3 段。** $\ell$ の $B_4$-不変性(⟹ $K_n$ が $B_4$-normal)は無条件 ✓、$\ell(H)\subseteq6\mathbf Z$ は $H\le N_4(3)$ から ✓、**等号(全射性)だけが要 witness**。ただし**等号が崩れても補題は $c=\ell(H)$ の生成元で成立**するので障害にならない。
**Q5: $PB_4^{ab}$ の $B_4$-不変汎函数は $\ell$ ただ一つ(階数 1)。** 太らせるには冪零商へ上がるしかなく、条件は「残差が $\ker\psi$ に**厳密に**入る」— 157dq の残差語から直接測れる。

---

## 1. Q1 — 三水準の確認と、1 箇所の訂正

### 1.1 群論の核は $n$ に一様に成立(訂正なし)

**補題 LT-0.** $G_1$ が非自明 3-群商を持たず $G_2$ が 3-群なら共通非自明商はない(T-49 GL-1)。
**三水準の確認**:
- **$PB_4$**: $H/L\cong A_5^4$ は完全 ⟹ 全商が完全 ⟹ 3-群商なし。$H/K_n\cong C_{3^n}$ は 3-群 ✓。
- **$PB_3$**: $(L\cap K_n)_{PB_3}=L_{PB_3}\cap(K_n)_{PB_3}$(逆像は交叉と可換)。$H_{PB_3}/L_{PB_3}\hookrightarrow(H/L)^5$(核は $H_{PB_3}\cap\bigcap_j\varphi_j^{-1}(L)=L_{PB_3}$)⟹ **合成因子は $A_5$ のみ** ⟹ 3-群商なし ✓。$H_{PB_3}/(K_n)_{PB_3}\hookrightarrow(C_{3^n})^5$ ⟹ 3-群 ✓。
- **$F_2$**: 同じ埋め込み論法 ✓。
⟹ 各水準で Goursat:$L_\bullet(K_n)_\bullet=H_\bullet$、$H_\bullet/(L_n)_\bullet\cong H_\bullet/L_\bullet\times H_\bullet/(K_n)_\bullet$ ✓。**$n$ に一様**(変わるのは $C_{3^n}$ が 3-群であることだけ)✓。
> **記法の注意(非障害)**: Sol の「$A_5\times C_5^r$」は $H_{PB_3}/L_{PB_3}$ **ではあり得ない**($(A_5^4)^5$ の部分群なので合成因子は $A_5$ のみ・$C_5$ は現れない)。別の対象($PB_3/L_{PB_3}$ 等)を指しているはずである。**結論はどちらでも同じ**(いずれも 3-群商を持たない)ので障害ではないが、出所を一行明記されたい。

### 1.2 onto ゲートも一様に継承(T-49 と同じ Goursat 論法)

$U=\langle x^u,\ f^{-1}y^uf\rangle\le F_2/(L_n)_{F_2}\cong G_1\times G_2$ は両成分へ全射、共通非自明商が自明 ⟹ Goursat により $U=G_1\times G_2$ ✓。**$n$ に一様** ✓。

### 1.3 ★ 訂正 — 「整数 linking 厳密 0」は hexagon 残差には不十分

**残差が全 $n$ で $L_n$ に入る条件**を型ごとに書く。
- **pentagon 残差** $w_3\in H\le PB_4$: 条件は $\ell(w_3)\equiv0\bmod6\cdot3^n\ (\forall n)\iff\boxed{\ell(w_3)=0}$ ✓ — **Sol の言明どおりで十分**。
- **hexagon 残差** $w_1,w_2\in H_{PB_3}\le PB_3$: 条件は $w_i\in(K_n)_{PB_3}=\bigcap_j\varphi_j^{-1}(K_n)$、すなわち**五 coface すべてについて** $\ell\bigl(\varphi_j(w_i)\bigr)\equiv0\bmod6\cdot3^n$。$\forall n$ ⟹ $\ell(\varphi_j(w_i))=0$(五本すべて)。
 (A.18) から $\ell\circ\varphi_j$ を $PB_3^{ab}=\mathbf Z^3$($x_{12},x_{23},x_{13}$ 座標)上の汎函数として読むと
$$\varphi_{123}:(1,1,1),\quad \varphi_{234}:(1,1,1),\quad \varphi_{12,3,4}:(2,1,2),\quad \varphi_{1,23,4}:(2,2,1),\quad \varphi_{1,2,34}:(1,2,2).$$
うち三本の行列式は
$$\det\begin{pmatrix}1&1&1\\2&1&2\\2&2&1\end{pmatrix}=-3+2+2=\mathbf 1$$
で**ユニモジュラー** ⟹ $\mathbf Z$ 上でも
$$\boxed{\ \ell(\varphi_j(w))=0\ (\forall j)\iff w\ \text{の}\ PB_3^{ab}\ \text{での像がゼロ}\ }$$
⟹ **必要なのは「$\ell(w)=a+b+c=0$」という 1 本の条件ではなく、$(a,b,c)=(0,0,0)$ という 3 本の条件**である。
> **⟹ Sol の主張「整数 linking 厳密 0 ⟹ 全 $n$ で働く」は、hexagon 残差については前件不足。** 正しい前件は **$w_1,w_2$ が $[PB_3,PB_3]$ に入る(= $PB_3^{ab}$ で消える)**こと。**これは 157dq の残差語から直接読める安価な検査**であり、$m=0$・charming($f\in[F_2,F_2]$)という状況では**成立する見込みが高い**が、**成立を仮定してはならない** ⟹ **FC-32**。
> (なお $\ell(w)=0$ は 3 条件の 1 次結合なので、Sol の観測は必要条件としては正しい。)

### 1.4 CRT($m$ 座標)は全 $n$ で通る — T-49 FC-29 への回答

$(L_n)_{PB_2}=L_{PB_2}\cap(K_n)_{PB_2}$ ⟹ $(L_n)_{\rm ord}=\operatorname{lcm}\bigl(L_{\rm ord},(K_n)_{\rm ord}\bigr)$。CRT の両立条件は $\gcd\bigl(L_{\rm ord},(K_n)_{\rm ord}\bigr)=H_{\rm ord}$。Sol の値 $L_{\rm ord}=90=2\cdot3^2\cdot5$、$(K_n)_{\rm ord}=18\cdot3^{n-1}=2\cdot3^{n+1}$ で
$$\gcd(90,\ 2\cdot3^{n+1})=2\cdot3^{\min(2,n+1)}=18=H_{\rm ord}\qquad(\forall n\ge1)\ ✓$$
⟹ **T-49 で私が最重要として挙げた FC-29 は、この塔では全 $n$ で充足される** ✓。$L_{\rm ord}/H_{\rm ord}=5$(Sol の「PB2 $C_5$」)がまさにこれを担っている ✓ — 役割が確定した。
**friendly**: $m=0$ ⟹ $u=1$ ⟹ $\gcd(1,(L_n)_{\rm ord})=1$ が全 $n$ で自明 ✓(Sol の $\gcd$ 計算より強い理由)。

### 1.5 Q1 の裁定

> **YES(訂正つき)。** §1.1–1.2 の共通商・Goursat・onto は $n$ に一様に成立、§1.4 の CRT も全 $n$ で成立。**唯一の訂正は §1.3** — hexagon 残差の前件を「$\ell=0$」から「$PB_3^{ab}$ で消える」へ強める必要がある。

---

## 2. Q2 — 補題 LT-1 の起草(登録可)

> ### 補題 **LT-1**(Linking Tower Descent・versioned)
> **前件**
> **(P1)** $\ell:PB_4\to\mathbf Z$ は全リンク数。$PB_4^{ab}=\mathbf Z^6$ 上 $B_4$ は 6 本の $x_{ij}$ を置換するので $\ell$ は $B_4$-不変 ⟹ $K_n:=H\cap\ell^{-1}(c\cdot3^n\mathbf Z)$ は $B_4$-normal 開部分群($c$ は $\ell(H)$ の正の生成元;本件は $c=6$・FC-33)。$H/K_n\cong C_{3^n}$(**$B_4$-自明作用**)、$[K_n:K_{n+1}]=3$。
> **(P2)** $L\le H$ は $B_4$-normal で $H/L$ は**非自明 3-群商を持たない**(本件 $A_5^4$・完全ゆえ充足)。
> **(P3)** $(m,f)$ は $L$ における charming shadow の literal 代表(157dq)。
> **(P4)** ★ **acceptance 残差の消滅**: pentagon 残差 $w_3$ は $\ell(w_3)=0$、hexagon 残差 $w_1,w_2$ は **$PB_3^{ab}$ での像がゼロ**(⟺ 五 coface すべてで $\ell\circ\varphi_j$ が消える;三本で足りる)。
> **(P5)** $\gcd\bigl(L_{\rm ord},(K_n)_{\rm ord}\bigr)=H_{\rm ord}$($\forall n$)。
>
> **結論**
> **同一の literal 対 $(m,f)$ が、全ての $n\ge1$ について $L_n=L\cap K_n$ の charming shadow である。** 従って T48-1 により
> $$\forall n,\ \forall\ \text{isolated }H'\ \text{with}\ L_n\le H'\le M:\quad I_{H'}=X .$$
>
> **使用ゲートと根拠**
> | ゲート | 根拠 |
> |---|---|
> | hexagon ×2 | (P4) の $PB_3^{ab}$ 消滅 ⟹ $w_i\in(K_n)_{PB_3}$ ∀$n$、かつ $w_i\in L_{PB_3}$(P3)⟹ $w_i\in(L_n)_{PB_3}$ |
> | pentagon | (P4) の $\ell(w_3)=0$ ⟹ $w_3\in K_n$ ∀$n$、かつ $\in L$ ⟹ $\in L_n$ |
> | friendly | $u=2m+1$ が $\gcd(u,(L_n)_{\rm ord})=1$。$m=0$ なら自明 |
> | charming(交換子代表) | $[G_1\times G_2,\cdot]=[G_1,\cdot]\times[G_2,\cdot]$ と $[F_2/N,F_2/N]=[F_2,F_2]N/N$ ⟹ 自動 |
> | onto($T^{F_2},T^{PB_3},T^{PB_2}$) | Goursat + (P2)(§1.2)⟹ 自動 |
> | settlement / isolated | **不要**(T-34 軽量化・FV-5)。$L_n$ の isolated 性は主張しない |
>
> **射程(必ず併記)**: $\bigcap_nL_n=L\cap\ker\ell$ は**開でない** ⟹ $\{L_n\}$ は **cofinal でない**。本補題は **full-$\Phi$ 層の代替でも B4-B への一歩でもない**。位置づけは**出口②(witness 安定化)の実例**である。

**登録形式の提案**: `SR/T` 番号系に **LT-1** として登録し、**LT-0**(共通商補題 = T-49 GL-1 の再掲)を補助補題として併記。T-49 の GL-2/GL-3 は $\Phi_3$ 版、LT-1 は linking 版で、**同一の骨格の 2 実例**であることを索引に明記されたい。

---

## 3. Q3 — 射程限定の十分性と L10 / T-50 ④ との整合

### 3.1 非 cofinal 性の確認

$\bigcap_nK_n=H\cap\ker\ell$。$\ell(H)=c\mathbf Z\cong\mathbf Z$ は無限なので $H\cap\ker\ell$ は $H$ で**無限指数**、すなわち**開でない** ⟹ 任意の開部分群の下に入るわけがなく、$\{L_n\}$ は $NFI$ に **cofinal でない** ✓。

### 3.2 T33-L10 との関係 — 衝突しない

T33-L10 は「単一 literal 対が **cofinal** 族の全段で shadow ⟹ $2m+1=\pm1$」。本件は (a) 族が非 cofinal、(b) しかも $m=0$ ⟹ $u=1=+1$ で**結論と整合**。⟹ **矛盾は生じない**。L10 は $u=\pm1$ を禁じておらず、$u\ne\pm1$ を禁じている。

### 3.3 T-50 ④(離散 GT 元の過大主張)との整合 — 一文の形

私の T-50 ④ 警告は「**cofinal** 族の全段で同一 literal 対が通れば離散 $\widehat{GT}$ 元という異常主張になる」だった。本件はその前件(cofinality)を満たさない。Sol の求める一文:

> **$\varprojlim_n\mathrm{ML}(L_n)$ は非 cofinal な部分系上の逆極限であり、2008 Thm 3.8 の $\widehat{GT}\cong\varprojlim(\mathrm{ML})$(全 isolated poset 上)とは異なる。従って本補題が与えるのは $\widehat{GT}$ の元ではなく、linking 方向にのみ完備化した thin 商の元であり、離散 $\widehat{GT}$ 元の主張には**一切**なっていない。**

**自己点検(T-50 ④ の「$f$ の段変動記録」との整合)**: T-50 ④ で私は「段ごとに $f$ が変わることを明示記録せよ」と要求した。**LT-1 では $f$ は変わらない**(同一語)。これは矛盾ではなく、**警告の発火条件が cofinality だったから**である。⟹ 記録の形を次に改める:
> **警告 T-50④′(改)**: 「同一 literal 対が通る段の族」が **cofinal になった瞬間に**警報。非 cofinal 族での定数語は正常(LT-1 が実例)。⟹ 今後は「$f$ が変わったか」ではなく「**族が cofinal になっていないか**」を監視項目とする。

⟹ **Q3 の裁定: 射程限定で十分。** ただし上の一文と警告の改訂を LT-1 の登録に添えること。

---

## 4. Q4 — $\ell(H)=6\mathbf Z$ の依存関係(一行×3)

1. **$\ell$ の $B_4$-不変性**: $PB_4^{ab}=\mathbf Z^6$ は 6 本の $x_{ij}$ 上の $S_4$-置換加群、$\ell$ = 座標和 ⟹ 不変 ✓。**無条件・追加入力不要**。これが $K_n$ の $B_4$-normal 性を与える。
2. **$\ell(H)\subseteq6\mathbf Z$**: $H\le N_4(3)$ なら $H$ の元は 3 乗の(共役の)積 ⟹ $\ell\in3\mathbf Z$ ✓。2-部分は $H\le M$ 側から来る。⟹ **包含は紙で出る**。
3. **等号(= $\ell(H)$ がちょうど $6\mathbf Z$)**: $\ell(h)=6$ なる $h\in H$ の**明示 witness が要る**。引用された gate(H9 8×6 $\mathbf F_2$ rank 5・kernel $\langle111111\rangle$・$\Pi4_{ab}=I_6$ mod 3)は **mod 3 / mod 2 の情報**であり、$\mathbf Z$ 上の像の生成元を直接は与えない。⟹ **FC-33**。
> **非障害である理由**: $\ell(H)=c\mathbf Z$ なる $c$ が何であれ、$K_n:=H\cap\ell^{-1}(c\cdot3^n\mathbf Z)$ とすれば $H/K_n\cong C_{3^n}$ ✓ で LT-1 はそのまま成立する(P1 を $c$ で書いた理由)。⟹ **$c=6$ の確認は記述の正確性の問題であって、補題の成否ではない。**

---

## 5. Q5 — thin 方向を太らせる次の一手(方向のみ)

**まず限界を確定する**: $PB_4^{ab}\otimes\mathbf Q$ は 6 辺上の $S_4$-置換加群で、$S_4$ は 6 辺に推移的 ⟹ **不変部分空間は 1 次元** ⟹ **$B_4$-不変な線型汎函数は $\ell$ のスカラー倍のみ**。⟹ **可換 1 次の方向にこれ以上の余地はない。**

**⟹ 太らせるには次の 2 方向しかない**:
1. **同じ機構の一般形へ**: LT-1 の実質は「**残差が $\ker\psi$ に厳密に入る**」ことだけである。従って
 > 任意の $B_4$-不変準同型 $\psi:PB_4\to A$($A$ は torsion-free または residually-$p$ 可換)について、acceptance 残差が **$\ker\psi$ に厳密に**入るなら、同一 literal 対は塔 $\{H\cap\psi^{-1}(p^nA)\}$ の全段へ降下する。
 ⟹ **次の候補は冪零商**:$PB_4/\gamma_3(PB_4)$ 等の $B_4$-不変商への $\psi$。条件は 157dq の残差語から**直接測れる**(§1.3 と同型の検査)。
2. **可換方向でない安定化**: $H/L$ 側(完全群方向)に同種の塔を作る。ただし $A_5^4$ は完全なので「3-冪塔」の相手にならず、別の共通商論法が要る。
**⚠ 重要な制限**: どの方向を足しても、$\psi$ たちの核の共通部分が開にならない限り **cofinal にはならない**。⟹ 太らせても出口②(witness 安定化)の範囲を出ない可能性が高い。**cofinal 化には可換・冪零方向だけでは足りない**(T33-L7:非可解商への到達が不可避)。

---

## 6. 新規の有限検査

| 番号 | 検査 | 重要度 |
|---|---|---|
| **FC-32** | candidate 124 の hexagon 残差 $w_1,w_2$ が **$PB_3^{ab}=\mathbf Z^3$ で消える**か(= 三本の $\ell\circ\varphi_j$ がすべて 0)。$\ell(w_i)=0$ だけでは不十分 | **最重要**(LT-1 の (P4)・唯一の訂正箇所) |
| **FC-33** | $\ell(H)$ の正の生成元 $c$(Sol は $c=6$)。$\ell(h)=c$ なる $h\in H$ の明示 | 中(非障害・記述の正確性) |

(T-49 の FC-29 は §1.4 で全 $n$ 充足を確認済 ⟹ **本塔については閉じた**。FC-30/31 は 157dq 側で継続。)

---

## 7. 自己点検(敵対的)

- **「$n$ に一様」の根拠が本当に $n$ 非依存か** ✓ §1.1 は「$C_{3^n}$ が 3-群」しか使わず、§1.4 の $\gcd$ は $n\ge1$ で定数 18 ✓。
- **$\ell\circ\varphi_j$ の係数を (A.18) から直接読んだか** ✓ 五本すべて表から書き下し、三本の行列式 1 を手計算 ✓。
- **pentagon と hexagon で条件が違うことを見落としていないか** ✓ §1.3 が本判定の主要な訂正。
- **T-49 の FC-29 を再確認したか** ✓ §1.4 で全 $n$ 充足を確認、$C_5$ の役割も確定。
- **T-50 ④ との整合** ✓ §3.3 で警告の発火条件を cofinality に改訂(自己訂正)。
- **禁止短路** ✓ centerless/Schreier・$K(5)$ 単連結性・strict deletion-kernel・ambient exponent-3 quotient・$A$ 正規性 — 未使用。
- **一様吸収を主張していないか** ✓ LT-1 は非 cofinal な特定塔への降下のみ。T-48 §2 の崩壊定理と無矛盾。

---

## 8. 申告

- **計算追加なし**(委嘱どおり紙上のみ)。手計算で検証: 三水準の共通商・Goursat・onto、$\ell\circ\varphi_j$ の五係数ベクトルと行列式 1、$\gcd(90,2\cdot3^{n+1})=18$、$(L_n)_{\rm ord}=\operatorname{lcm}$、非 cofinal 性。
- **157dq の CV-9 判読は未了**。本書は witness の literal 成立を前提として受け取っている。
- **UNKNOWN**: FC-32(LT-1 の (P4))、FC-33。$C_5$ の出所(記法・非障害)。
- **LT-1 は非 cofinal 塔への降下であり、一様吸収でも B4-B でもない。B4-B は宣言していない。**
