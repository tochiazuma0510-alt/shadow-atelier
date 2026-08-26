# $T$ 測定の設計 v1 — ∞-軌道 pin と IMG 塔の構成手順(implementer 停止解除用)

`DIR: 正側(算術像の上界)/ FRAME: G_dyn 二窓テスト`
**格**: §1 = `paper-proof + 機械裏取り`(紙の幾何 + sympy + GAP)/ §2–§5 = `実装仕様(candidate)`/ §6 = ゲート。
**著者**: 数学者(Opus 5)/ 2026-08-26。前提文書 = `gdyn_definition_draft_v2_1.md` §3・§4。

---

## §0 要旨(先に結論)

1. **implementer の選択 $r'=x$ は誤り。** 反例ではなく**全 24 通りの許容 $(a,b)$ で 0/24 が valid**(GAP 実測)。$r'=y$ も 0/24。**正しい代表は $r=xyx^{-1}$(24/24 valid・模型非依存)。**
2. 正しさの根拠は**幾何の 1 行**: 四面体の 3 回回転軸は「頂点 と 対面の中心」を結ぶ。$t=0$ は頂点(0 の上・$e=3$)、$t=\infty$ は面心(1 の上・$e=3$)で、**両者は同一軸上**。ゆえに $\mathrm{Stab}(\infty)=\mathrm{Stab}(0)=\langle\bar x\rangle$。
3. 塔の構成に **FR は必須ではない**。$\psi_T$ が明示なら、塔は「$12^k$ 点上の置換群の位数」を GAP に聞くだけで済む(level 2 = 144 点)。**FR は独立照合の第二系統**として使う(探索器と照合器の分離)。
4. **測定済みの前提値**(v2 の上界を実測値に置換): $\lvert F_2/N_1^{\rm sym}\rvert=\mathbf{576}$(v2 の「$\le1728$」を確定)・`IdGroup = [576, 8664]`・$x,y,z$ の像は全て位数 6・$\mathrm{Ab}=[3,3]$。**全 $S_3$ 対称化と $C_3$ 対称化は同じ 576**(3 本で足りる)。
5. **fr 2.4.13 は稼働確認済**(`Activity` で加算機の level-3 位数 8 を再現)。

---

## §1 ∞-軌道 pin(委嘱 (a) への回答)

### 1.1 分岐データ(v2 §4.1 の再掲・恒等式は sympy 検算済)

$$T(t)-1=\frac{64\,(t^{3}-1)^{3}}{(t^{6}-20t^{3}-8)^{2}}\qquad\Bigl(\Leftarrow\ t^{3}(t^{3}+8)^{3}-(t^{6}-20t^{3}-8)^{2}=64(t^{3}-1)^{3}\Bigr)$$

| 上 | 点(4/4/6) | $e$ | 幾何 |
|---|---|---|---|
| $0$ | $t=0$、$t^3=-8$ の 3 根 | 3 | **頂点** |
| $1$ | $t^3=1$ の 3 根、$\mathbf{t=\infty}$ | 3 | **面心** |
| $\infty$ | $t^6-20t^3-8$ の 6 根 | 2 | 稜心 |

$T(\infty)=1$(分子分母とも monic 12 次)・$T-1\sim 64/t^3$ ⟹ $e_\infty=3$ ✓。

### 1.2 ★ pin の証明(紙・幾何的モノドロミー追跡)

デック変換群 $=A_4\subset\mathrm{PGL}_2$。**$\sigma(t)=\omega t$($\omega^3=1$)はデック変換**であり、$t=0$ と $t=\infty$ を同時に固定する。頂点・面心の安定化群はいずれも位数 3 ゆえ

$$\boxed{\ \mathrm{Stab}(t=\infty)=\langle\sigma\rangle=\mathrm{Stab}(t=0)\ }$$

これは四面体の 3 回軸が「頂点 ↔ 対面中心」を貫くという事実そのもの。慣性の正規化 $\varphi_*(\gamma_0)=x^{3}$(点 $t=0$ を基点シートに置く)により $\mathrm{Stab}(0)=\langle\bar x\rangle$、同様に $\varphi_*(\gamma_1)=y^{3}$ により $\mathrm{Stab}(1)=\langle\bar y\rangle$。よって

> **pin(不変形・規約非依存)**: $\varphi_*(\gamma_\infty)=r\,y^{3}\,r^{-1}$ における $r$ は
> $$\bar r\,\langle\bar y\rangle\,\bar r^{-1}=\langle\bar x\rangle$$
> を満たす元であり、そのような $\bar r$ は**ちょうど 3 個**($\langle\bar x\rangle$ の左剰余類 = $\langle\bar y\rangle$ の右剰余類)。3 個はいずれも同じ元 $ry^3r^{-1}$ を与えるので**選択は無害**。
> そして $\psi_T(r\,y^3\,r^{-1})=z$。

### 1.3 機械裏取り(2 系統)

**(i) sympy**(`scratchpad`・整数係数有理式):
```
sigma: t->w*t          deck? True
tau1 : t->(t+2)/(t-1)  deck? True        # 1 <-> inf, 0 <-> -2, w <-> w^2 を交換する対合
rho  : t->-2/t         deck? False       # ただし T(-2/t) = 1 - T(t)  (0 と 1 の繊維を交換する外側対称)
identity  N - D - 64(t^3-1)^3 = 0
```
$\tau_1$ が $1\leftrightarrow\infty$ を交換する**対合**であることは、$\infty$ と $1$ が同じ $A_4$-軌道(面心 4 点)に属することの独立確認。

**(ii) GAP**(`scratchpad/math_gdyn_tpin_v3.g`・全 24 通りの許容 $(a,b)$ を悉皆):
```
pairs = 24
UNIV r=aba^-1 valid : 24 / 24  (invalid 0)
UNIV r=x     valid  : 0 / 24
UNIV r=y     valid  : 0 / 24
model a=(2,3,4) b=(1,2,3) z=(1,2)(3,4)
rho_a cycles = 4 x 3   rho_b cycles = 4 x 3   rho_z cycles = 6 x 2   ra*rb*rz = id : true
Euler: 4+4-12+6 = 2
orbit of sheet 1  under rho_b (= point t=1)   : [1,5,7]
orbit of sheet r0 under rho_b (= point t=inf) : [10,11,12]   disjoint : true
```

### 1.4 判定と却下理由

| 候補 $\bar r$ | 判定 | 理由 |
|---|---|---|
| $\bar r=\bar x$(implementer の $r'=x$) | ❌ **不可** | $\bar x\langle\bar y\rangle\bar x^{-1}=\langle\bar y\rangle$ となるのは $\bar y\in\langle\bar x\rangle$ のときだけだが、$\bar x\bar y$ が位数 2 ゆえ $\langle\bar x\rangle\ne\langle\bar y\rangle$。**規約をどう取っても救えない**(0/24) |
| $\bar r=\bar y$ | ❌ 不可 | 同上(0/24)。$\bar r=\bar y$ は点 $t=1$ 自身を指す |
| $\bar r=\bar x\bar y\bar x^{-1}$ | ✅ **正解** | 24/24。具体語 **$r=xyx^{-1}$** |

⟹ **$\psi_T$ の第 3 の値は $\ \psi_T\bigl(xyx^{-1}\cdot y^{3}\cdot xy^{-1}x^{-1}\bigr)=z$。**

---

## §2 $\psi_T$ の完全な明示(実装可能形)

$H_T=\ker(\pi:F_2\twoheadrightarrow A_4)$、$\pi(x)=a,\pi(y)=b$、$a,b$ 位数 3・$ab$ 位数 2。$H_T$ は自由・階数 $12(2-1)+1=13$。

**14 個の慣性元**(シート = $A_4$ の元、右乗法作用 $\rho_g$):
- $0$ の上(4 個): $\rho_a$ の 4 軌道 $u\langle a\rangle$ に対し $\ \iota_u:=r_u\,x^{3}\,r_u^{-1}$
- $1$ の上(4 個): $\rho_b$ の 4 軌道 $u\langle b\rangle$ に対し $\ \jmath_u:=r_u\,y^{3}\,r_u^{-1}$
- $\infty$ の上(6 個): $\rho_z$ の 6 軌道に対し $\ \kappa_u:=r_u\,z^{2}\,r_u^{-1}$($z=(xy)^{-1}$)

($r_u$ = Cayley グラフの全域木から得る横断系、$r_1=1$。$4+4+6=14$、$\rho_a\rho_b\rho_z=1$ は GAP 実測 ✓。)

> ### $\psi_T$ の定義(3 値 + 11 個の死)
> $$\psi_T(\iota_1)=\psi_T(x^3)=x,\qquad \psi_T(\jmath_1)=\psi_T(y^3)=y,\qquad \psi_T(\jmath_{r_0})=z\ \ (r_0=xyx^{-1}),$$
> $$\psi_T(\text{他の 11 個})=1 .$$
> **実装形(基底問題を回避)**: $K:=\langle\langle\text{他の 11 個}\rangle\rangle_{H_T}$ と置き、$\psi_T$ を
> $$H_T\ \twoheadrightarrow\ H_T/K\ \xrightarrow{\ \cong\ }\ F_2$$
> と定義する。右の同型は 3 特別元の像を $x,y,z$ に送ることで pin される。

**なぜこの形か**: 14 個の慣性元は $H_T$ を生成するが、**自由基底ではない**(1 本の関係「適当な順序の積 $=1$」がある)。順序は dessin の平面埋め込みに依存するので、生成元ごとに値を代入する定義は**規約事故を呼ぶ**。商で定義すれば順序の情報は不要 — 幾何由来なので整合性は自動、機械側は §6 の G2 で検査するだけでよい。

---

## §3 塔の構成(委嘱 (b) への回答・規約を固定する)

### 3.1 ★ 規約の固定(W-1 型事故の予防)

**右剰余類** $H_Tr_u$ を使う。$g\in F_2$ に対し $H_Tr_ug=H_Tr_{u\pi(g)}$ ゆえ $r_u\,g\,r_{u\pi(g)}^{-1}\in H_T$。切片を

$$\boxed{\ g|_u\ :=\ \psi_T\bigl(r_u\,g\,r_{u\pi(g)}^{-1}\bigr)\ }$$

と定める。**$g\in N_1=H_T$(正規)なら $\pi(g)=1$ なので $g|_u=\psi_T(r_u\,g\,r_u^{-1})$。**

> ⚠ **v2 §3.1 の訂正**: v2 は $\psi_\varphi(r^{-1}gr)$ と書いたが、右剰余類代表系を使う上式では **$\psi_\varphi(r\,g\,r^{-1})$** が正しい($r^{-1}gr$ は左剰余類規約に対応)。**どちらかに固定して cert に明記すること。**混在は W-1 と同型の事故になる。

### 3.2 塔

$$N_1:=H_T,\qquad N_{k+1}:=\{\,g\in N_1\ :\ g|_u\in N_k\ (\forall u)\,\},\qquad Q_k:=F_2/N_k .$$

**$\psi_T(N_{k+1}\cap H_T)\subseteq N_k$ は $u=1$ を取れば構成から自動** ⟹ v2 §3 の二窓性は無料(DYN-NOGO と矛盾しない = 標的が粗い)。

**実装は wreath 積を作らずに置換で行う**:
$$\Phi_k:\ F_2\ \longrightarrow\ \mathrm{Sym}(12^{k}),\qquad Q_k=\mathrm{im}\,\Phi_k,\quad N_k=\ker\Phi_k .$$
$\Phi_{k}$ は $g\mapsto(\text{level-}k\ \text{の頂点置換})$。GAP は 2 生成の置換群の位数を level 2(144 点)・level 3(1728 点)で瞬時に出す。

> ⚠ **GAP API の罠(実測)**: `WreathProduct(A4, A4)` は **$12^5=248{,}832$** を返す(上の $A_4$ の**自然 4 点作用**を使うため)。本件で要るのは**正則 12 点作用**の $A_4\wr_{12}A_4$($12^{13}$)。⟹ **wreath 積は作らない。置換表現を直接組む**のが正解。

### 3.3 $S_3$ 対称化(**実測済**)

$N^{\rm sym}_k:=\bigcap_{\alpha\in S_3}\alpha(N_k)$。$\theta:x\mapsto y,\ y\mapsto y^{-1}x^{-1}$(= $x\to y\to z\to x$)、$\omega:x\leftrightarrow y$。

```
|F2/N1sym(full S3)| = 576      IdGroup = [576, 8664]   Ab = [3,3]
|F2/N1sym(C3 only)| = 576      orders of x,y,z images = [6,6,6]
```
⟹ **$C_3$ 対称化で既に $S_3$-安定**(3 本の核の交わりで足りる)。v2 §3.3 の「$\le1728$」は**確定値 576** に置き換える。$x,y,z$ が全て位数 6 になるのは対称化の健全性の徴候(各座標で $(3,3,2)$ の lcm)。

---

## §4 GAP 手順(数コマンド粒度)

```gap
# --- 0. 窓 N1sym (実測済・再現用) ---
A := AlternatingGroup(4);;
a := (2,3,4);; b := (1,2,3);;                      # ab = (1,2)(3,4) 位数 2
F := FreeGroup("x","y");; x := F.1;; y := F.2;;
h1 := GroupHomomorphismByImages(F,A,[x,y],[a,b]);;
th := GroupHomomorphismByImages(F,F,[x,y],[y, y^-1*x^-1]);;
homs := [ h1, th*h1, (th*th)*h1 ];;                # GAP: f*g = 「f を先に」
# 直積への対角像を取ると |Q| = 576

# --- 1. H = ker pi の自由基底 ---
Fp := F/[];;  Hp := PreImage(..., ...);;           # または AugmentedCosetTableInWholeGroup
#   目的: 13 本の Schreier 生成元(自由基底)と、横断系 r_u(全域木・r_1=1)

# --- 2. 14 個の慣性元を語として構成 ---
#   rho_a の 4 軌道 -> r_u x^3 r_u^-1 ,  rho_b の 4 軌道 -> r_u y^3 r_u^-1 ,
#   rho_z の 6 軌道 -> r_u z^2 r_u^-1     (z := (x*y)^-1)

# --- 3. psi の構成 ---
K   := NormalClosure(H, [11 個の非特別慣性元]);;
Hb  := H/K;;                                        # 階数 2 の自由群であることを G2 で検査
psi := Hb -> F  (x^3 |-> x, y^3 |-> y, (xyx^-1) y^3 (xyx^-1)^-1 |-> z)

# --- 4. level-2 置換表現 ---
#   頂点 = A4 x A4 の 144 点。 g の作用: (u,v) |-> (u*pi(g),  v*pi(g|_u))
act2 := function(g) ... end;;
Q2 := Group(act2(x), act2(y));;   Print(Size(Q2));   # <= 12^13、これが未測定の量
```

**この 4 段の中で数学的判断が要るのは段 3 の 3 値だけ**で、それは §1–§2 で確定した。残りは機械的。

---

## §5 FR 経由(独立照合の第二系統)

`fr 2.4.13` 稼働確認済(加算機 $a=\langle1,a\rangle\sigma$ で `Activity` level 1/2/3 = $(1,2)$ / $(1,3,2,4)$ / $(1,5,3,7,2,6,4,8)$、level-3 群位数 8 ✓)。

```gap
LoadPackage("fr");;
# trans[i] = アルファベット 12 文字上の切片語(整数リスト表現)、out[i] = 12 点の置換
M := FRMachine( [ transX, transY ], [ permX, permY ] );;
gx := FRElement(M,1);; gy := FRElement(M,2);;
Size(Group(Activity(gx,2), Activity(gy,2)));      # = |Q2|
```
`permX = rho_a`(4 個の 3 サイクル)・`permY = rho_b`。**`transX`/`transY` は §3.1 の $g|_u$ そのもの** ⟹ FR は「同じ入力を別実装で回す」照合器になる。
**$T$ の有理式から `IMGMachine(T)` を直接呼ぶ経路は浮動小数複素数を使う** ⟹ **第一系統にはしない**(数値 Thurston アルゴリズムは失敗し得る)。成功したら第三の照合として採用。

---

## §6 検証ゲート(どの経路でも必ず通す)

| # | ゲート | 期待値 | 効用 |
|---|---|---|---|
| **G1** | $\lvert Q_1\rvert$、$\rho_a,\rho_b,\rho_z$ の型 | 12、$3^4$/$3^4$/$2^6$、$\rho_a\rho_b\rho_z=1$ | 単葉性・モノドロミーの健全性 |
| **G2** | $H_T/K$ が階数 2 の自由群、3 特別元の像が生成 | $\mathrm{Ab}=\mathbb Z^2$・Tietze で自由 | **$\psi_T$ の well-defined 性**(§2 の定義の唯一の穴) |
| **G3** | ★ **pin**: $\infty$ の $\rho_b$-軌道の安定化群 $=\langle a\rangle$ | true | **規約非依存**。どんな構成でもこれで自己検査できる |
| **G4** | $\psi_T$ が慣性元を 3+11 に分ける | 3 個が $x,y,z$・11 個が 1 | 定義の忠実な実装 |
| **G5** | $\lvert F_2/N_1^{\rm sym}\rvert$ | **576**(`IdGroup [576,8664]`) | 既知値との突合(本稿で実測済) |
| **G6** | 陽性対照 $z^2$: $\mathrm{DYN}_{z^2}(\mathcal W_k)=GT(\mathcal W_k)$ | 全通過 | 外れたら実装バグ(v2 §3.2) |
| **G7** | 破壊対照: $\psi$ を別 $\varphi$ のものに差し替え | 判定が変わる | 判定器が本当に $\psi$ を見ている証拠 |

**G3 が最重要**: 本稿の pin は不変形で書いてあるので、実装がどの規約(左/右剰余類、$rgr^{-1}$/$r^{-1}gr$)を採っても**同じ 1 行で検査できる**。

---

## §7 コスト・出力仕様・未決

- **level 1**: 窓 576(実測)。$GT(N_1^{\rm sym})$ の列挙コストは既存計器のスケール則から実装側で見積もれ。
- **level 2**: 144 点の置換群 ⟹ **位数計算は秒**。$\lvert Q_2\rvert$ は**現在未測定の量**で、v2 の「$\le12^{13}$」は粗い上界のまま。**測ってから語ること**(推測で埋めない)。
- **出力仕様**: cert に必須 — ①採用した剰余類規約($rgr^{-1}$ か $r^{-1}gr$ か)②$r_0$ の具体語 ③G1–G5 の実測値 ④$\lvert Q_2\rvert$ ⑤$\lvert\mathrm{DYN}_T(N_1^{\rm sym})\rvert$ と $\lvert GT(N_1^{\rm sym})\rvert$ の対。
- **未決(推測で埋めていない)**: ① $O$ 側の同じ pin(面心 $\leftrightarrow$ 頂点の対応が $S_4$ でどうなるか)は未実施 ② $\psi_{z^2}$ の降下 $\psi(\mathcal W_{k+1}\cap H)\subseteq\mathcal W_k$ は依然要機械確認 ③ $Q_2$ 未測定 ④ $GT(N_1^{\rm sym})$ の列挙可能性は未評価。
