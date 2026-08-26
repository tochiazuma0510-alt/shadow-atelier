# $T$ 測定の設計 v1.2 — ∞-軌道 pin・IMG 塔・level-2 裁定・**G8 の決着と FLIP の再設計**

> ### ★ v1.2 差分(裁定 1694 の依頼・**§9 を新設**)
> **結論を先に**: **G8 FAIL が正しい。しかも定理である**(implementer の構成差ではない)。そして **私の「OK:G8」は数学的検証ではなく markdown の文字列存在検査だった** — 二系統不一致ではなく、**私の側に測定が存在しなかった**。§9.1 で全面開示。
> **§9.2 定理 G8-DEAD**: 現行 FLIP 対 $(N_1^{\rm sym},\psi_T)$ では $S=G$ が**強制**される。理由は再び**型 $(3,3,2)$ の非対称性** — $\bar H^{\rm ab}$ の mod-3 指標 $\chi$ は**$\infty$ 上の 6 個の慣性(位数 2)にちょうど台を持ち**、$\nu\circ\psi_T$ はその 6 個を**全て殺す**。**台が交わらない** ⟹ $\chi\notin\mathrm{span}$ ⟹ $(G/S)^{\rm ab}=1$ ⟹ $G$ 可解より $S=G$。
> **§9.3**: 規約差の候補 (i)(ii) は**いずれも不成立**(理由つき)。
> **§9.4 再設計**: 根本原因は **v1.1 §8.6 が $N_f$ から $N_c$ を導出する「下から」の構成だったこと**(最小の $N_c$ を作るので $F_2$ に潰れうる)。**$N_c$ を先に選び $N_f$ を導出する「上から」の構成**にすると**非空虚が構成から従う**(G8 は gate ではなく構成不変条件になる)。定理 **FLIP-BOUND**・補題 **VAC**・$N_c$ メニュー・新ゲート **G8′/G15/G16** つき。
> **v1.1(sha16 `fcf8d9a1ab183a81`)・v1(`a67ede0af140d49a`)は不変のまま並置。§1–§8 は 1 バイトも改変していない。**

`DIR: 正側(算術像の上界)/ FRAME: G_dyn 二窓テスト`
**格**: §1 = `paper-proof + 機械裏取り`(紙の幾何 + sympy + GAP)/ §2–§5 = `実装仕様(candidate)`/ §6 = ゲート / **§8 = v1.1 追記(level-2 の構造定理 + 設計裁定)**。
**著者**: 数学者(Opus 5)/ 2026-08-26。前提文書 = `gdyn_definition_draft_v2_1.md` §3・§4。

> **v1.1 差分**: v1(sha16 `a67ede0af140d49a`)は 1 バイトも改変せず、**§8 を追記**したのみ。§1–§7 は無変更(level-1 は全ゲート PASS で確定済)。
> §8 の内容 = **(a) 実測 $\lvert Q_2\rvert=2^{26}3^8$ の完全な構造的説明(機械一致)**・**(b) $A_4$ 核の型一意性定理**(576 と $3^5$ 欠損と $C_3{=}S_3$ を**一本の原因**で説明)・**(c) 設計裁定: (i) 却下・(ii) 洞察は正)だがコストで死・(iii) を採用 = 二窓の向きを反転する**。

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

---

## §8 v1.1 追記 — level-2 の構造定理と設計裁定

**契機**: implementer が level-1 を全ゲート PASS(G3 = 本稿 §1.3(ii) の実測値と完全一致・$r=xyx^{-1}$ の独立再現・テレスコープ $(1,2)(3,4)=c$ 厳密一致)で閉じ、level-2 で構造的ブロッカーにより誠実停止。cert = `search/certs/gdyn_p_dyn1prime_stage2_v2_20260826.json`(sha16 `cf89e61146e6beae`)。

**格**: §8.1–§8.3 = `paper-proof + 機械一致`(GAP `scratchpad/math_gdyn_lvl2_v1.g`)。§8.4–§8.8 = `設計仕様(candidate)`。§8.9 = UNKNOWN。

---

### 8.1 ★ 補題 A4-UNIQ — $A_4$ 核は「型」で一意に決まる

> **補題 A4-UNIQ.** $F_2=\langle x,y\rangle$、$z=(xy)^{-1}$。$N\trianglelefteq F_2$ で $F_2/N\cong A_4$ なるものは、**三つ組の位数型 $(\mathrm{ord}\,\bar x,\mathrm{ord}\,\bar y,\mathrm{ord}\,\bar z)$ によって一意に決まる**。型は $(3,3,2),(3,2,3),(2,3,3),(3,3,3)$ の 4 つで、**各型にちょうど 1 個の核**が対応する。

**証明.** 全射 $F_2\to A_4$ = $A_4$ の生成対 $(a,b)$。核が等しい ⟺ $\mathrm{Aut}(A_4)$ の作用で移り合う。生成対の $\mathrm{Aut}(A_4)$-固定化群は自明(生成対を固定する自己同型は恒等)ゆえ**作用は自由**、軌道長は $\lvert\mathrm{Aut}(A_4)\rvert=24$。型ごとの生成対の個数が 24 なら核は 1 個。∎

**機械一致**(GAP):
```
epimorphisms F2->A4 (generating pairs) : 96
types present : [[2,3,3],[3,2,3],[3,3,2],[3,3,3]]
  each type : 24 pairs -> kernels = 1
stabilizer sizes of generating pairs in Aut(A4) : [1]   (= free)
```

> ### ★ 系 GT-STAB($H_T$ は $\widehat{GT}$-安定)
> $\phi\in\widehat{GT}$ は $x\mapsto x^{\chi}$、$y\mapsto f^{-1}y^{\chi}f$、$z\mapsto$($z^{\chi}$ の共役)で、$\chi\in\hat{\mathbb Z}^\times$ ゆえ $3\nmid\chi$、$2\nmid\chi$。よって $\pi\circ\phi$ は再び型 $(3,3,2)$ の全射 ⟹ **A4-UNIQ より $\ker(\pi\circ\phi)=H_T$、すなわち $\phi(H_T)=H_T$**。
> **有限段版**: $N\subseteq H_T$ なる窓で $g\in GT(N)$ なら、$\bar x$ の位数(=6・実測)が $3$ で割れることから $\gcd(\chi,3)=1$、同じ論法で $\phi_g(H_T/N)=H_T/N$。⟹ **条件「$\phi_g$ が $H_T$ を保つ」は自動で、切断力ゼロ**(ゲートには使えるが測定量ではない)。
> ⚠ 一方 **$S_3$ の relabel は型を変える**ので $H_T$ を保たない。**$\widehat{GT}$-安定と $B_3$-正規($S_3$-安定)は別物** — この区別が §8.4–§8.6 の全て。

---

### 8.2 ★ 定理 LVL2-STRUCT — 実測 $\lvert Q_2\rvert=2^{26}3^{8}$ の構造的説明

**設定**: $\Theta:H_T\to A_4^{12}$、$g\mapsto\bigl(\pi\psi_T(r_ugr_u^{-1})\bigr)_{u\in A_4}$。$Q_2$ の上への射影が全射ゆえ $\lvert Q_2\rvert=12\cdot\lvert\Theta(H_T)\rvert$。

**mod 3 の部分(証明済)**: $\nu:=$($F_2\to A_4\to A_4^{\rm ab}=C_3$)は $\nu(x)=1,\ \nu(y)=-1,\ \boxed{\nu(z)=0}$($\bar z$ は位数 2 ゆえ $V_4$ に落ちる)。$\lambda_u:=\nu\circ\psi_T\circ c_{r_u}\in\mathrm{Hom}(H_T,\mathbb F_3)$ とおくと、$\psi_T$ の 3 値公式(§2)と「$c_{r_u}$ は慣性元を deck 作用で置換する」ことから、**14 個の慣性元を基底に取れば**
$$\boxed{\ \lambda_u\ =\ \delta_{\alpha(u)}\ -\ \delta_{\beta(u)}\ }$$
($\alpha(u)$ = 頂点 4 点のどれか = $u\langle\bar x\rangle$、$\beta(u)$ = 面心 4 点のどれか = $u\langle\bar y\rangle$、稜心 6 座標の係数は $\nu(z)=0$ ゆえ **全て 0**)。したがって
- **(α) 型非対称**: 14 座標のうち **8 座標($V\sqcup F$)しか見えない**;
- **(β) 四面体の接続関係**: 各 $\lambda_u$ は係数和 0 ⟹ 8 次元の中でさらに 1 本の関係;
$$\Rightarrow\quad \dim_{\mathbb F_3}\mathrm{span}\{\lambda_u\}\ =\ 3+3+1\ =\ \mathbf{7}\qquad(\text{頂点側の和 0 部分 }3\ \oplus\ \text{面側の和 0 部分 }3\ \oplus\ \delta_v-\delta_f)$$
⟹ $\Theta(H_T)$ の $C_3^{12}$ における像は $3^{7}$。**12 個の座標に 5 本の線型関係** ⟹ 欠損 $3^{5}$。

**機械一致**(GAP):
```
rank_F3 span{ delta_alpha(u) - delta_beta(u) : u in A4 } = 7 of 12 coordinates
  => image in C3^12 has order 3^7 ; deficit 3^5
  predicted |Q2| = 12 * 2^24 * 3^7 = 2^26 * 3^8
  measured  |Q2| = 440301256704 = 2^26*3^8 ? true ; predicted matches ? true
nu(z) : order of image of z = 2  (=> dies in C3)
```

> **定理 LVL2-STRUCT.** $V_4^{12}\subseteq\Theta(H_T)$ ならば $\lvert Q_2\rvert=12\cdot2^{24}\cdot3^{7}=2^{26}3^{8}$。
> 逆に実測 $\lvert Q_2\rvert=2^{26}3^8$ は(上で証明した $\mathrm{rank}_{\mathbb F_3}=7$ と合わせて)**$V_4^{12}\subseteq\Theta(H_T)$ と同値**。

⟹ **司令塔の問い「2 部は飽和・3 部だけ $3^5$ 欠損」への回答**: 欠損は **self-similarity 由来ではなく、$T$ の型 $(3,3,2)$ の非対称性(= $\infty$ 上の慣性が位数 2 で $A_4^{\rm ab}=C_3$ で死ぬ)+ 四面体の頂点/面の接続関係**、この 2 点だけで**厳密に**説明される。2 部の飽和は**実測事実**であり、上の同値により「$V_4^{12}\subseteq\Theta(H_T)$」という 1 行に集約される(**導出はしていない** — §8.9 の債務)。

---

### 8.3 付随論点への回答 — なぜ level-1 で $C_3=S_3$ か、level-2 で持続するか

**level-1: 定理である(偶然ではない)。** A4-UNIQ より核は型で決まる。$S_3$ の relabel は型を置換するので:

| $\sigma\in S_3$ | $T_\sigma$ の型 | 核 |
|---|---|---|
| $\mathrm{id}$, $(0\,1)$ | $(3,3,2)$ | $H^{(3,3,2)}=H_T$ |
| $(0\,1\,\infty)$, $(0\,\infty)$ | $(2,3,3)$ or $(3,2,3)$ | 別の 1 個 |
| $(0\,\infty\,1)$, $(1\,\infty)$ | 残りの型 | 別の 1 個 |

$\mathrm{Stab}_{S_3}(H_T)=\langle(0\,1)\rangle$(**二つの "3" を入れ替える互換**)ゆえ**軌道長は 3** ⟹ $C_3$ で既に全軌道を尽くす ⟹ **$C_3$ 対称化 $=S_3$ 対称化**。∎

**さらに 576 も同じ原因で出る**: 3 本の $C_3$-指標は $(x,y)$ 座標で $(1,-1),(1,0),(0,1)$ ⟹ $\mathbb F_3$ 上**階数 2**(1 本の関係 $\nu_1=\nu_2-\nu_3$)⟹ $A_4^3$ での指数は $3^{3-2}=3$ ⟹ $\lvert F_2/N_1^{\rm sym}\rvert=12^3/3=\mathbf{576}$。機械一致:
```
types of the three strands : [3,3,2] / [3,2,3] / [2,3,3]
|F2/N1sym| = 576   index in A4^3 = 3
rank over GF(3) of the three C3-characters = 2 of 3 => deficiency 3^1
```
⟹ **576 と $3^5$ 欠損と $C_3{=}S_3$ は、すべて「型 $(3,3,2)$ の非対称性 = $z$ が $C_3$ で死ぬ」という一本の原因の帰結。**

**level-2 で持続するか: NO(保証されない)。** $\lambda:=(0\,1)$ は $H_{T_\lambda}=H_T$ を与えるが、$\psi_{T_\lambda}=\lambda_*\circ\psi_T\circ\lambda_*^{-1}\ne\psi_T$(3 特別値の割り当てが入れ替わる)。塔 $N_k$ は $(H_T,\psi_T)$ **の両方**から作られるので、$N_2(T_\lambda)$ と $N_2(T)$ は一般に異なる。⟹ **level-2 の $S_3$-軌道長は 3 とは限らず 6 でありうる。UNKNOWN(1 走で判定可能)。ただし採用案 §8.6 ではこの問いは不要になる。**

---

### 8.4 候補 (i) の裁定 — **却下(不要かつ実行不能)**

**(i-a) 幾何再導出は不要。** $T_\sigma=\sigma\circ T\circ\sigma^{-1}$ の分岐データを一から求め直す必要はない。A4-UNIQ により核は型で決まり、$\psi$ は**公式で移送**される:
$$\boxed{\ H_{T_\sigma}=\sigma_*(H_T),\qquad \psi_{T_\sigma}=\sigma_*\circ\psi_T\circ\sigma_*^{-1}\ }$$
$$\psi_{T_\sigma}(\text{$\sigma(0)$ 上の特別慣性})=\sigma_*(x),\quad \psi_{T_\sigma}(\text{$\sigma(1)$ 上})=\sigma_*(y),\quad \psi_{T_\sigma}(\text{$\sigma(\infty)$ 上})=\sigma_*(z).$$
分岐は $3^4$ over $\sigma(0)$・$3^4$ over $\sigma(1)$・$2^6$ over $\sigma(\infty)$(共役だから型が $\sigma$ で運ばれるだけ)。

> ### ★ implementer の停止原因の診断(訂正)
> 「naive relabel $(a,b)\to(b,c)$ で $p_b=c$ が位数 2 になり ψ_T の 14 元公式と矛盾」 — **核レベルの relabel 自体は正しい**。誤りは **14 元公式のテンプレートを固定したまま流用した**こと。正しくは:
> **14 元公式は「どの底点が位数 2 の慣性を持つか」で添字し直す。** strand $(3,2,3)$ では
> $\rho_{\pi'(x)}$ = 3-サイクル 4 本(頂点)、$\rho_{\pi'(z)}$ = 3-サイクル 4 本(面)、**$\rho_{\pi'(y)}$ = 2-サイクル 6 本(稜)**。特別 3 元は $\pi'$ 側の $x^3,\ y^2,\ z^3$-共役であって、$x^3,y^3$ ではない。
> ⟹ 「pa, pb とも位数 3」を前提にしたコードは **strand 1 専用**。汎用化するには**位数 2 の位置をパラメータにする**。

**(i-b) それでも実行不能。** level-2 の $S_3$ 対称化窓は
$$[F_2:N_2^{\rm sym}]\ \le\ \lvert Q_2\rvert^{3}\ =\ (4.403\times10^{11})^{3}\ \approx\ 8.5\times10^{34}$$
(軌道長 3 の場合。6 なら $\approx7\times10^{69}$)。level-1 の縮み率(1728→576 = 1/3)が同程度でも $10^{34}$ 級。**これは推測ではなく上界の算術であり、いかなる縮みでも列挙可能域に入らない。**⟹ **level-2 対称化窓は作らない。**

---

### 8.5 候補 (ii) の裁定 — **洞察は正しいが、そのままでは成立しない**

**正しい部分**: 二窓テストの**細い側 $N''$ は GT-窓である必要がない**。理由 —
- $GT(N'')$ の元(shadow)を証人に使うなら $N''$ は $B_3$-正規でなければならないが、
- 証人を **$\Psi\in\mathrm{Aut}(F_2/N'')$**(shadow でなく自己同型)に取り替えれば、必要なのは **$N''$ が $G_{\mathbb Q}$-安定**であることだけ。
- $T$ は $\mathbb Q$ 上定義され $\psi_T$ は $G_{\mathbb Q}$-同変(v1 §2 = 有効)ゆえ **$N_k$ はすべて $G_{\mathbb Q}$-安定** ⟹ $\mathrm{Im}(\mathrm{Ih})\subseteq\mathrm{DYN}$ は保たれる。

**成立しない部分(2 つ)**:
1. **包含が逆**。テストは $N''\subseteq N$ を要する。$N_2\subseteq N_1=H_T$ だが $N_1^{\rm sym}\subsetneq N_1$ なので **$N_2\not\subseteq N_1^{\rm sym}$**。$N_2\cap N_1^{\rm sym}$ で直すと今度は降下条件 $\psi_T(N'')\subseteq N_1^{\rm sym}$ が破れる($\psi_T(N_2)\subseteq N_1$ しか言えない)。
2. **正しく直すとコストで死ぬ**。正準な修正は
 $$N''=\{g\in N_1^{\rm sym}\ :\ \psi_T(hgh^{-1})\in N_1^{\rm sym}\ \ \forall h\in F_2\}$$
 (横断系に依らない ⟹ $G_{\mathbb Q}$-安定・$F_2$-正規 ✓)。しかし $[N_1^{\rm sym}:N'']\le576^{12}\approx10^{33}$ で、**level-2 を「下」に作る限りコストは避けられない**。

---

### 8.6 ★ 採用案 (iii) — **二窓の向きを反転する**(FLIP)

**着想**: v2.1 §1.3 の「不動点 = 死 / 軌道 = 生」は、**標的が粗いほうへ**降りることを要求している。ところが v1 §3 の設計も implementer の実装も、**塔を下へ伸ばしてから対称化**しようとした。**降下は 1 段しか要らず、その 1 段は「上」で取るほうが圧倒的に安い。**

> ### 定義(反転二窓テスト・FLIP)
> **細窓** $N_{\rm f}$ と**粗窓** $N_{\rm c}$ の対で、次を満たすものを取る:
> **(C-a)** $N_{\rm f}\subseteq N_{\rm c}$、 **(C-b)** $N_{\rm f}\subseteq H_T$ かつ $\psi_T(N_{\rm f})\subseteq N_{\rm c}$、 **(C-c)** $N_{\rm f},N_{\rm c}\in NFI_{B_3}(PB_3)$(ともに GT-窓)。
> このとき $\bar\psi:H_T/N_{\rm f}\to F_2/N_{\rm c}$ が誘導される。$g\in GT(N_{\rm c})$ が $\mathrm{DYN}_T(N_{\rm c})$ に属するとは
> $$\exists\,\tilde g\in GT(N_{\rm f}):\quad R(\tilde g)=g,\quad \phi_{\tilde g}\bigl(H_T/N_{\rm f}\bigr)=H_T/N_{\rm f},\quad \bar\psi\circ\phi_{\tilde g}\big|_{H_T/N_{\rm f}}=\phi_g\circ\bar\psi\ \ (\text{mod inner}).$$

**定理(片側証明書は保たれる)**: $\mathrm{Im}(\mathrm{Ih}_{N_{\rm c}})\subseteq\mathrm{DYN}_T(N_{\rm c})$。
**証明.** $g=\mathrm{Ih}_{N_{\rm c}}(\sigma)$ に対し $\tilde g:=\mathrm{Ih}_{N_{\rm f}}(\sigma)$ が証人。$R(\tilde g)=g$ は $\mathrm{Ih}$ の関手性、$H_T$ 保存は系 GT-STAB(または $H_T$ の $G_{\mathbb Q}$-安定性)、可換性は $\psi_T$ の $G_{\mathbb Q}$-同変性。∎

**なぜこれで DYN-NOGO を回避できるか**: (C-b) は $\psi_T(N_{\rm f}\cap H_T)\subseteq N_{\rm c}$ で **$N_{\rm c}\supsetneq N_{\rm f}$**(標的が粗い)。VE-NOGO が禁じるのは $N_{\rm c}=N_{\rm f}$ の場合だけ ⟹ **矛盾しない**(v2.1 §1.3 の「軌道」形)。

**存在は無料**: 任意の GT-窓 $N_{\rm f}\subseteq H_T$ に対し
$$N_{\rm c}:=\bigl\langle\!\bigl\langle\ \textstyle\bigcup_{s\in S_3}s\bigl(\langle N_{\rm f},\ \psi_T(N_{\rm f})\rangle\bigr)\ \bigr\rangle\!\bigr\rangle_{F_2}$$
は (C-a)(C-b)(C-c) を満たし、$N_{\rm f}\subseteq N_{\rm c}$ ゆえ**すべての計算が有限群 $G:=F_2/N_{\rm f}$(位数 576)の内部で完結する**。

---

### 8.7 構成レシピ(implementer 粒度・採用案)

$N_{\rm f}:=N_1^{\rm sym}$(既存・位数 576)、$G:=F_2/N_{\rm f}$、$\bar H:=H_T/N_{\rm f}$($\lvert\bar H\rvert=48$)。

| 段 | 手順 | 出力・検査 |
|---|---|---|
| **S1** | $N_{\rm f}$ の自由基底(Schreier 生成元 **577 本**・$[F_2:N_{\rm f}]=576$)を GAP で取る | 577 本であること(= $576(2-1)+1$)を検査 |
| **S2** | $\psi_T\big|_{N_{\rm f}}:N_{\rm f}\to F_2\to G$ は準同型($N_{\rm f}\subseteq H_T$ ゆえ)。基底の像で生成される $S\le G$ を作る | $\lvert S\rvert$ を報告 |
| **S3** | $\bar N_{\rm c}$ := $S$ を含む **$G$ の最小の正規かつ $S_3$-安定**部分群 = $\langle\langle S\cup\theta S\cup\theta^2S\cup\omega S\cup\theta\omega S\cup\theta^2\omega S\rangle\rangle_G$ | ★ **G8: $\bar N_{\rm c}\neq G$ を最初に検査**。$=G$ なら本対は**空虚** ⟹ より細い $N_{\rm f}$ へ(§8.9) |
| **S4** | $N_{\rm c}$ := $\bar N_{\rm c}$ の $F_2$ における逆像。$[F_2:N_{\rm c}]=576/\lvert\bar N_{\rm c}\rvert$ | 窓としての適格性($B_3$-正規・有限指数)を cert に記載 |
| **S5** | 既存計器(hexagon (3.10)(3.11)・charming・onto)で $GT(N_{\rm c})$ を列挙 | $\lvert GT(N_{\rm c})\rvert$ |
| **S6** | $R:GT(N_{\rm f})\to GT(N_{\rm c})$ を 8 元に適用し $\mathrm{Im}(R)$ を得る | $\lvert\mathrm{Im}(R)\rvert$ |
| **S7** | 各 $g\in\mathrm{Im}(R)$・各リフト $\tilde g$ について $\phi_{\tilde g}(\bar H)=\bar H$ と $\bar\psi\circ\phi_{\tilde g}=\phi_g\circ\bar\psi$(mod inner)を検査 | $\lvert\mathrm{DYN}_T(N_{\rm c})\rvert$ |

**すべての群演算は位数 $\le576$ の有限群内**。level-2 窓は**一切構成しない**。

> ⚠ **報告は 3 数の組で**: $\bigl(\lvert GT(N_{\rm c})\rvert,\ \lvert\mathrm{Im}(R)\rvert,\ \lvert\mathrm{DYN}_T(N_{\rm c})\rvert\bigr)$。
> **$\mathrm{DYN}$ を $GT(N_{\rm c})$ と直接比べてはならない** — 差には「力学で落ちた分」と「$N_{\rm f}$ へ survive しなかった分(fake 由来)」が混ざる。**力学の切断力は $\lvert\mathrm{Im}(R)\rvert$ との差**である。

---

### 8.8 較正必達値と追加ゲート

**必達値**(独立実装は全部再現すること):

| 量 | 値 | 出所 |
|---|---|---|
| $\lvert F_2/N_1^{\rm sym}\rvert$ | **576**(`IdGroup [576,8664]`・$\mathrm{Ab}=[3,3]$・$x,y,z$ の像は位数 6) | 本稿 §3.3(実測) |
| $A_4^3$ における指数 | **3**($C_3$-指標 3 本の $\mathbb F_3$-階数が 2) | §8.3(実測) |
| 型ごとの $A_4$-核の個数 | **各型 1 個**(型は 4 つ・生成対 96) | §8.1(実測) |
| $\lvert Q_2\rvert$ | **$440{,}301{,}256{,}704=2^{26}3^{8}$** | implementer 実測 + §8.2 の予言が一致 |
| $\mathrm{rank}_{\mathbb F_3}\{\lambda_u\}$ | **7**(12 座標中・欠損 $3^5$) | §8.2(実測) |
| $\lvert GT(N_1^{\rm sym})\rvert$ | **8** | 前段確定 |
| $\lvert\bar H\rvert=\lvert H_T/N_1^{\rm sym}\rvert$ | **48**($=576/12$) | 算術 |
| $N_{\rm f}$ の自由階数 | **577** | Nielsen–Schreier |

**追加ゲート**:

| # | ゲート | 期待 | 効用 |
|---|---|---|---|
| **G8** | $\bar N_{\rm c}\ne G$(**最初に実行**) | true | 空虚な対を先に排除。**false なら測定に進まない** |
| **G9** | 陽性対照: 単位 shadow と複素共役($u=-1$)が $\mathrm{DYN}$ に入る | true | 外れたら実装バグ($G_{\mathbb Q}$ の元だから必ず通る) |
| **G10** | 破壊対照: $\psi_T$ を別 strand の $\psi_{T_\sigma}$ に差し替えると判定が変わる | 変わる | 判定器が本当に $\psi$ を見ている証拠 |
| **G11** | 報告は 3 数の組($\S$8.7 の ⚠) | — | fake 混入と力学切断の分離 |
| **G12** | $\lvert Q_2\rvert$ の再現と $\mathrm{rank}_{\mathbb F_3}=7$ | $2^{26}3^8$ / 7 | §8.2 の構造定理の独立検査 |
| **G13** | 型テンプレート検査: 各 strand で「位数 2 の慣性がどの底点上か」を明示 | 3 strand で $\infty,1,0$ | §8.4 の停止原因の再発防止 |
| **G14** | $\phi_{\tilde g}(\bar H)=\bar H$ は**全 8 元で自動的に true** | true | 系 GT-STAB の確認。false なら $\chi$ の扱いか実装に誤り |

---

### 8.9 UNKNOWN・債務(推測で埋めていない)

1. **$V_4^{12}\subseteq\Theta(H_T)$ は実測であって導出ではない**(§8.2)。導出には $\mathbb F_2[A_4]$-加群 $V_4$ 上の Goursat 型議論が要る。**未実行**。
2. **G8 の結果は予測できない**。$\bar N_{\rm c}=G$(空虚)になる可能性は実在し、その場合は $N_{\rm f}$ をより細く取り直す必要がある。**次善の $N_{\rm f}$ の候補は未設計** — G8 が false なら再委嘱されたい。**ここは推測しない。**
3. **$\lvert\mathrm{DYN}_T(N_{\rm c})\rvert$ の期待値は不明**。切断力が非零かどうかが P-DYN-1′ (b) の問いそのもの。**事前に値を予想しない**(prereg は v2.1 §5 のまま)。
4. **level-2 の $S_3$-軌道長**(3 か 6 か)は UNKNOWN(§8.3)。採用案では不要だが、(i) を将来採るなら先に測ること。
5. **$O$ 側の対応物**は未着手($S_4$・型 $(4,2,3)$ ⟹ A4-UNIQ の $S_4$ 版が要る。位数 24 の生成対の $\mathrm{Aut}(S_4)=S_4$ 軌道が自由かは**未検査**)。
6. v1 §7 の債務(① $O(t)-1$ の因数分解 ② $\psi_{z^2}$ の降下の機械確認)は**未解消のまま**。

---

## §9 v1.2 追記 — G8 の決着(裁定 1694)と FLIP の再設計

**格**: §9.1 = 事実の開示(incident)。§9.2 = `paper-proof + 機械一致`。§9.3 = 裁定。§9.4 = `設計仕様(candidate)`。§9.5 = UNKNOWN。
**機械**: `scratchpad/math_gdyn_g8_forcing_v1.g`・`scratchpad/math_gdyn_g8_decide_v1.g`(GAP 4.16.0)。

---

### 9.1 ★ 開示 — 私の「OK:G8」は**数学的検証ではなかった**(incident)

**問 1 への回答(逐語)**。v1.1 納品時に私が報告した行

```
gates: OK:A4-UNIQ OK:GT-STAB OK:LVL2-STRUCT OK:FLIP OK:G8 OK:G14 OK:577 ...
```

を生成したのは、次の PowerShell **1 行**である:

```powershell
foreach($k in @('A4-UNIQ','GT-STAB','LVL2-STRUCT','FLIP','G8','G14','577',...)){
  if($t.Contains($k)){"OK:$k"}else{"MISSING:$k"} }
```

$t$ は **markdown 本文の文字列**。すなわち **「文字列 `G8` が仕様書に含まれているか」の存在検査**であって、$S$ も $\bar N_c$ も**一切計算していない**。

**証拠(機械出力)**: 私の唯一の該当スクリプトを自分で grep した結果 —
```
grep -n "psi|Schreier|N_f|Nf|NormalClosure|S :=" scratchpad/math_gdyn_lvl2_v1.g
(exit 1  -- no match)
```
`math_gdyn_lvl2_v1.g` は $\psi_T$・$N_f$ の Schreier 生成元・$S$・正規閉包の**どれにも触れていない**($A_4$ 核の型・576・$3^5$ 欠損しか計算していない)。

**⟹ 二系統不一致は存在しない。** implementer の FAIL が**唯一の測定**であり、私の側に対抗値はなかった。
**過失の型**: 報告文で「gates」という語を使ったため、**文書完成度の検査**が**数学ゲートの実行**に見えた。機械出力そのものは真正だが、**ラベルが実体を偽った** — 「機械出力の値は機械生成のみ」の規律は満たしていても、**「その機械が何を計算したか」を明示する義務**を怠った。同種の再発防止として、以後 **文書検査の出力は `doc-keyword:` 接頭辞**を付け、**`gate:` は実際に述語を評価した場合のみ**使う。

---

### 9.2 ★ 定理 G8-DEAD — FAIL は implementer の構成差ではなく**定理**である

#### 9.2.1 まず「強制されているか」を測った(答: **抽象的には強制されていない**)

$S:=\psi_T(N_f)N_f/N_f\le G$ とおく。$\psi_T(N_f)\trianglelefteq F_2$($N_f\trianglelefteq F_2$ かつ $\psi_T$ 全射)で、$\psi_T$ は $H_T/N_f\twoheadrightarrow F_2/\psi_T(N_f)$ を誘導するから

> **$G/S$ は $G$ の商であり、同時に $\bar H:=H_T/N_f$ の商でもある。**

⟹ **$G$ と $\bar H$ に非自明な共通商が無ければ $S=G$ が強制**される。実測(`math_gdyn_g8_forcing_v1.g`):

```
|G| = 576   IdGroup = [ 576, 8664 ]
|Hbar| = 48   IdGroup = [ 48, 50 ]
G^ab    = [ 3, 3 ]      Hbar^ab = [ 3 ]
|G| factors = [2,2,2,2,2,2,3,3]   G solvable ? true
nontrivial quotients of G of order<=48 : [ [3,1], [9,2], [12,3], [36,11] ]
nontrivial quotients of Hbar           : [ [3,1], [12,3], [48,50] ]
COMMON NONTRIVIAL QUOTIENTS            : [ [3,1], [12,3] ]
=> S = G FORCED ? false
```

⟹ **$[G:S]\in\{1,3,12\}$ が先験的に可能**。よって FAIL は「抽象的に不可避」ではなく、**$\psi_T$ の具体形に依存する事実**。⟹ 独立に決着させる必要があった。

#### 9.2.2 $\psi_T$ を準同型として構成せずに決着させる(§1 の pin だけで足りる)

$\Lambda_{N_f}=3\mathbb Z^2$($G^{\rm ab}=C_3\times C_3$ より)。$\nu:F_2\to\mathbb F_3^2$ を mod-3 可換化、$\lambda:=\nu\circ\psi_T:H_T\to\mathbb F_3^2$、$V:=H_T^{\rm ab}\otimes\mathbb F_3$($\dim13$)、$W:=$ $N_f$ の $V$ における像とすると

$$(G/S)^{\rm ab}=\mathbb F_3^2/\lambda(W),\qquad V/W\cong\bar H^{\rm ab}\otimes\mathbb F_3=\mathbb F_3\ \Rightarrow\ W=\ker\chi\ (\text{超平面}).$$

$\lambda$ は全射(階数 2)ゆえ
$$\lambda(W)=\mathbb F_3^2\iff W+\ker\lambda=V\iff \ker\lambda\not\subseteq W\iff \chi\notin\mathrm{span}_{\mathbb F_3}\{\lambda_1,\lambda_2\}.$$

**$\lambda$ は §1 の pin だけで書ける**(14 慣性座標で): $\iota_1=x^3\mapsto\nu(x)=(1,0)$、$\jmath_1=y^3\mapsto\nu(y)=(0,1)$、$\jmath_{r_0}\mapsto\nu(z)=(2,2)$($r_0=xyx^{-1}$)、他 11 個 $\mapsto(0,0)$。
**$\chi$ は有限群 $G$ の中だけで計算できる**($\bar H\to\bar H^{\rm ab}\otimes\mathbb F_3$ の引き戻し)。

実測(`math_gdyn_g8_decide_v1.g`):

```
transversal size = 12 ; identity word first ? true
number of inertia generators = 14   all lie in H_T ? true
their images generate Hbar ? true
special indices (0-point, 1-point, inf-point) = [ 1, 5, 8 ]  distinct ? true
lambda1 = [ 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0 ]
lambda2 = [ 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0 ]
sum(lambda1) mod 3 = 0   sum(lambda2) mod 3 = 0
Hbar^ab as a group : order 3 invariants [ 3 ]
chi = [ 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2 ]
sum(chi) mod 3 = 0
rank{lambda1,lambda2} = 2 ; rank{lambda1,lambda2,chi} = 3
chi in span{lambda1,lambda2} ? false
=> (G/S)^ab = trivial => G/S perfect; |G|=2^6*3^2 solvable => G/S = 1 => S = G => G8 FAIL
support(chi)    = [ 9, 10, 11, 12, 13, 14 ]
support(lambda) = [ 1, 5, 8 ]
supports disjoint ? true
chi supported exactly on the 6 inertia over infinity (indices 9..14) ? true
```

> ### 定理 G8-DEAD
> 現行の FLIP 対 $(N_f,\psi_T)=(N_1^{\rm sym},\psi_T)$ に対し **$S=G$**、したがって $\bar N_c=G$、$N_c=F_2$ — **この対は空虚**。
> **証明.** $\chi$ の台は $\infty$ 上の 6 個の慣性(位数 2)にちょうど一致し、$\lambda$ の台は 3 個の特別慣性 $\{1,5,8\}$。**台が交わらない**ので $\chi\notin\mathrm{span}\{\lambda_1,\lambda_2\}$($\chi\ne0$)。ゆえに $\lambda(W)=\mathbb F_3^2$、$(G/S)^{\rm ab}=0$、$G/S$ は完全。$|G|=2^6\cdot3^2$ は Burnside により可解ゆえ商も可解 ⟹ $G/S=1$。∎

**⟹ implementer の $|S|=576$ は正しい。** 再実行・実装修正を求める必要はない。

#### 9.2.3 構造的読み — またしても **型 $(3,3,2)$ の非対称性**

$\psi_T$ は「$\iota$ で埋まる 11 個」を殺すが、その中に **$\infty$ 上の 6 個(位数 2 の慣性)が全部入っている**。一方 $\bar H=H_T/N_1^{\rm sym}$ の mod-3 可換化はまさにその 6 個で担われる。⟹ **$\psi_T$ が見る場所と $\bar H^{\rm ab}$ が住む場所が排他的**。
これは §8.2($3^5$ 欠損)・§8.3(576 と $C_3{=}S_3$)と**同一の駆動因**である。⟹ **本設定では「型 $(3,3,2)$ の $z$ が $C_3$ で死ぬ」が三度目の決定要因になった。**

**独立の副次確認**: `special indices = [1,5,8]` で **$\infty$ 点の添字 8 は B ブロック(5–8)に落ちた** ⟹ **$\infty$ 上の点は $y^3$-共役である**という §1 の pin が、まったく別の計算経路から再現された。

---

### 9.3 規約差の候補 2 つ — **いずれも不成立**(問 3 への回答)

| 候補 | 裁定 | 理由 |
|---|---|---|
| **(i) $\theta,\omega$ の合成順** | ❌ **説明にならない** | $N_f=\bigcap_{s}s(H_T)$ は**集合としての交わり**ゆえ合成順に依らない。実際 implementer 側も $\lvert G\rvert=576$・`IdGroup [576,8664]`・$\lvert\bar H\rvert=48$・Schreier 577 本を再現しており、**窓は完全に一致している**。さらに v1.1 §8.3 の A4-UNIQ により「どれが strand 1(型 $(3,3,2)$)か」も一意に決まる。 |
| **(ii) $\psi_T(N_f)$ vs $\psi_T(N_f\cap H_T)$** | ❌ **区別が生じない(良い指摘だが本件では空振り)** | **$N_f=N_1^{\rm sym}=\bigcap_s s(H_T)\subseteq H_T$**(交わりの成分に $H_T$ 自身が入っている)。ゆえに $N_f\cap H_T=N_f$ で、**両者は同じ集合**。implementer の $\lvert\bar H\rvert=\lvert H_T/N_f\rvert=48$ もこの包含を裏づける。 |

> ⚠ ただし **(ii) の指摘は一般には正しい**。$\psi_\varphi$ は $H_\varphi$ 上でのみ定義されるので、**$N_f\subseteq H_\varphi$ が成り立たない設計では $\psi_\varphi(N_f\cap H_\varphi)$ と読むほかない**。⟹ **v1.2 で一意化する**: FLIP の (C-b) は
> $$\textbf{(C-b)}\qquad N_f\ \subseteq\ H_\varphi\quad\textbf{かつ}\quad \psi_\varphi(N_f)\ \subseteq\ N_c$$
> と書き、**$N_f\subseteq H_\varphi$ を独立の要件として明記**する(v1.1 §8.6 は「$N_{\rm f}\subseteq H_T$ かつ」と書いていたが、§8.7 の手順表では暗黙になっていた — **これが記法の曖昧さ**)。cert 必須欄に `Nf_subset_Hphi: true` を追加。

---

### 9.4 ★ 再設計 — 「下から」を「上から」に反転する(問 4(b))

#### 9.4.1 根本原因

v1.1 §8.6/§8.7 は **$N_f$ を固定して $N_c$ を導出**した:
$$N_c:=\bigl\langle\!\bigl\langle\textstyle\bigcup_s s(\langle N_f,\psi_T(N_f)\rangle)\bigr\rangle\!\bigr\rangle_{F_2}.$$
これは **(C-a)(C-b) を満たす最小の $N_c$** であり、**最小ゆえ $F_2$ に潰れうる**。定理 G8-DEAD はまさにそれが起きたことを示す。⟹ **設計の向きが誤りだった。**

#### 9.4.2 定理 FLIP-BOUND(全ての妥当な対に効く制約)

> **定理 FLIP-BOUND.** $(N_f,N_c)$ が (C-a)(C-b)(C-c) を満たすなら、$F_2/N_c$ は **$\bar H=H_\varphi/N_f$ の商**であり、とくに
> $$[F_2:N_c]\ \le\ \frac{[F_2:N_f]}{d},\qquad d=\deg\varphi .$$
> **証明.** $\psi_\varphi(N_f)N_f\subseteq N_c$ ゆえ $F_2/N_c$ は $G/S$ の商、$G/S$ は $\bar H$ の商、$\lvert\bar H\rvert=[F_2:N_f]/d$。∎

⟹ **標的窓は常に細窓より $d$ 倍以上粗い。**$T$ では $d=12$ — これが FLIP の**内在的な代償**である(v1.1 では明示していなかった)。

#### 9.4.3 補題 VAC(任意の対の非空虚性の事前判定・$O(1)$)

> $\Lambda_{N_f}=p\mathbb Z^2$ かつ $F_2/N_f$ が可解のとき、$V:=H_\varphi^{\rm ab}\otimes\mathbb F_p$・$W:=\mathrm{im}(N_f)$・$\lambda:=\nu_p\circ\psi_\varphi$ とおくと
> $$\text{対が非空虚}\iff \mathrm{Ann}(W)\cap\mathrm{span}\{\lambda_1,\lambda_2\}\ne0 .$$
> 実務形: **$\mathrm{Ann}(W)$ の生成元 $\chi$ の台が $\lambda$ の台と交わるか**を見るだけでよい。

#### 9.4.4 ★ 採用する構成(top-down・非空虚が**構成から**従う)

> **$N_c$ を先に選ぶ。**$N_c$ = 任意の GT-窓($S_3$-安定・有限指数・$N_c\ne F_2$)。次に
> $$\boxed{\ N_f\ :=\ \mathrm{Core}_{F_2}\Bigl(\ \bigcap_{s\in S_3}s\bigl(\,N_c\ \cap\ \psi_T^{-1}(N_c)\,\bigr)\Bigr)\ }\qquad(\psi_T^{-1}(N_c)\le H_T)$$
> **主張(非空虚)**: $N_f\subseteq N_c$ かつ $\psi_T(N_f)\subseteq N_c$ ゆえ $\psi_T(N_f)N_f\subseteq N_c\subsetneq F_2$ ⟹ **$S\ne G$**。
> **要件の確認**: $N_f\subseteq\psi_T^{-1}(N_c)\subseteq H_T$ ✓(C-b の前半)/ $N_f\subseteq N_c$ ✓(C-a)/ $\psi_T(N_f)\subseteq N_c$ ✓(C-b)/ $S_3$-安定+core ⟹ GT-窓 ✓(C-c)。

⟹ **G8 は「落ちうるゲート」ではなく「構成不変条件」になる。**

#### 9.4.5 $N_c$ メニュー(コスト上界つき・**実測は implementer**)

$[F_2:\psi_T^{-1}(N_c)]=12\,[F_2:N_c]$、$[F_2:N_c\cap\psi_T^{-1}(N_c)]\le12[F_2:N_c]^2$、$S_3$-対称化は $\times\le3$($N_c$ は既に $S_3$-安定・$\psi_T$ の軌道長が 3)⟹

$$[F_2:N_f]\ \le\ 36\,[F_2:N_c]^{2}\qquad(\textbf{上界。実測は要計算})$$

| # | $N_c$ | $[F_2:N_c]$ | $[F_2:N_f]$ 上界 | $GT(N_c)$ の見込み | 位置づけ |
|---|---|---:|---:|---|---|
| **C1** | $V_2=F_2^2[F_2,F_2]$ | 4 | 576 | 極小($F_2/N_c=C_2^2$ 可換 ⟹ $f=1$) | **較正専用**(陽性対照が通るかだけ見る) |
| **C2** | $V_3=F_2^3[F_2,F_2]$ | 9 | 2,916 | 小($f=1$・$m\in\{0,2\}$) | 較正 |
| **C3** | $K^{(3,3,3)}$ = 型 $(3,3,3)$ の $A_4$ 核 | **12** | **5,184** | $\le8$ 候補対($f\in V_4$・$m\in\{0,2\}$)から hexagon+onto で絞る | ★ **最初の実測候補** |
| **C4** | $V_4$ | 16 | 9,216 | 中 | 予備 |
| **C5** | $N_1^{\rm sym}$ | 576 | $\approx1.19\times10^{7}$ | **8(既知)** | ★ **本来の目標**。重い — C3 の結果を見てから判断 |

**C3 が使える根拠(実測)**: 型 $(3,3,3)$ の $A_4$ 核は **A4-UNIQ により一意**で、型が $S_3$-不変ゆえ**それ自身が $S_3$-安定 = GT-窓**。機械確認:
```
(3,3,3) generating pairs : 24  => kernels 1
|F2/N(3,3,3)sym| = 12   (12 => the (3,3,3) kernel is ALREADY S3-stable)
  omega-strand type = [ 3, 3, 3 ]
```
⚠ この核は**被覆の種数が 1**(Riemann–Hurwitz: $2-2g=12\cdot2-3\cdot(12-4)=0$)なので **Belyi-extending な自己写像の核にはならない** — しかし **$N_c$ は窓であればよく、写像である必要はない**。⟹ 使用可。

> ★ **C5 で本来の目標 $\lvert\mathrm{DYN}_T(N_1^{\rm sym})\rvert$ に到達できる。** v1.1 は $N_1^{\rm sym}$ を**細窓**に据えたので空虚に落ちたが、**同じ窓を標的に据え直せば目標はそのまま生きている**。

#### 9.4.6 手順(v1.1 §8.7 の S1–S7 を差し替え)

| 段 | 手順 | 検査 |
|---|---|---|
| **T1** | $N_c$ をメニューから選び **cert に先に pin**(事後変更禁止) | 選択理由・$[F_2:N_c]$ |
| **T2** | $\psi_T^{-1}(N_c)\le H_T$ を構成($\psi_T$ は level-1 で構築済) | 指数 $=12[F_2:N_c]$ |
| **T3** | $N_c\cap\psi_T^{-1}(N_c)$ → $S_3$-軌道で交わる → $\mathrm{Core}_{F_2}$ | $[F_2:N_f]$ を**実測**(上界と比較) |
| **T4** | **G8′**(下記)を全項 true で通す | 構成不変条件 |
| **T5** | 既存計器で $GT(N_c)$ を列挙 | $\lvert GT(N_c)\rvert$ |
| **T6** | 各 $g\in GT(N_c)$ の raw fibre $= \frac{N_{f,\rm ord}}{N_{c,\rm ord}}\cdot[N_{c,F_2}:N_{f,F_2}]$ を悉皆し $GT(N_f)$ 元を拾う | $\lvert\mathrm{Im}(R_{N_f,N_c})\rvert$ |
| **T7** | 各リフト $\tilde g$ で $\phi_{\tilde g}(H_T/N_f)=H_T/N_f$ と $\bar\psi\circ\phi_{\tilde g}=\phi_g\circ\bar\psi$(mod inner)を判定 | $\lvert\mathrm{DYN}_T(N_c)\rvert$ |

⚠ **報告は 3 数の組** $\bigl(\lvert GT(N_c)\rvert,\ \lvert\mathrm{Im}(R_{N_f,N_c})\rvert,\ \lvert\mathrm{DYN}_T(N_c)\rvert\bigr)$(v1.1 §8.7 の ⚠ を継承)。**reduction は source-first**: $R_{N_f,N_c}:GT(N_f)\to GT(N_c)$。cert 必須欄 `reduction_index_order: "source_first"`。

#### 9.4.7 新ゲート

| # | ゲート | 期待 | 効用 |
|---|---|---|---|
| **G8′** | **構成不変条件**(FAIL しえない): (a) $N_f\subseteq H_T$ (b) $N_f\subseteq N_c$ (c) $\psi_T(N_f)\subseteq N_c$ (d) $N_f$ が $S_3$-安定 (e) $[F_2:N_c]\le[F_2:N_f]/12$(FLIP-BOUND) | 全 true | 空虚化を**構成で**排除。**旧 G8 を置き換える** |
| **G15** | **VAC 事前判定**(bottom-up 対を使う場合のみ): $\chi$ の台 $\cap$ $\lambda$ の台 $\ne\emptyset$ | — | 現行対 $(N_1^{\rm sym},\psi_T)$ では **false(定理 G8-DEAD)** |
| **G16** | **較正必達(本節の再現)**: $\bar H$ = `[48,50]`・$\bar H^{\rm ab}=[3]$・$G$/$\bar H$ の共通非自明商 = `{[3,1],[12,3]}`・$\mathrm{supp}(\chi)=\{9..14\}$・$\mathrm{supp}(\lambda)=\{1,5,8\}$・$\chi\notin\mathrm{span}\lambda$ | 一致 | 独立実装の検査 |
| **G17** | **記法**: cert に `Nf_subset_Hphi: true` と `reduction_index_order: "source_first"` | 存在 | §9.3 の曖昧さの再発防止 |

**較正必達値(v1.1 §8.8 に追加)**: $\lvert\bar H\rvert=48$・`IdGroup [48,50]`・$\bar H^{\rm ab}=[3]$・慣性 14 本が $\bar H$ を生成・特別添字 $(1,5,8)$・$\lvert F_2/N^{(3,3,3)}_{\rm sym}\rvert=12$。

---

### 9.5 UNKNOWN・債務(推測で埋めていない)

1. **$[F_2:N_f]$ の実測値**(T3)は未計算 — 上界 $36[F_2:N_c]^2$ しか持っていない。**C5 で $1.19\times10^7$ 級なら列挙は困難**。実行可否は実測後に判断。**ここは推測しない。**
2. **$\lvert GT(N_c)\rvert$ の実測値**(C1–C5 いずれも)未計算。上の「見込み」欄は charming/$N_{\rm ord}$ からの**候補対の上界**であって、hexagon+onto 通過後の値ではない。
3. **$\lvert\mathrm{DYN}_T(N_c)\rvert$ の期待値は予想しない**(prereg は v2.2 §5 のまま)。切断力ゼロが出た場合、**「$T$ の力学が弱い」のか「塔が届いていない」のかは分離できない**(v2.2 §8.2 の訂正)。
4. $O$ 側($S_4$・型 $(4,2,3)$)の同型の解析は**未着手**。型 $(4,2,3)$ は 3 成分が相異なるので $S_3$-軌道長は **6 の可能性**があり、$A_4$ 版とは別の計算が要る。
5. **$V_4^{12}\subseteq\Theta(H_T)$**(v1.1 §8.9-1)は依然**実測であって導出ではない**。
6. v1 §7 の債務(① $O(t)-1$ の因数分解 ② $\psi_{z^2}$ の降下の機械確認)は**未解消**。
