# (Ad) 段 2 — 最小成果 S2-1 / S2-2 / S2-3 の完了文書(裁定 1057)

作成: 数学者(Opus 5)/ 2026-08-13 / spec = `F_stage2_ad_spec_v1.md`(凍結 `aa49fb520ebfe2f3`)
入力 = `F_stage2_S1S2_construction_v1.md`(S2-1/2)・`F_stage2_S3_precheck_v1.md`(前検査)・cert `s2_3_pre_gen23_v1`(witness)
⚠ **B2 の 5 条件を遵守**。$u$/$c$ 非接触。**格: candidate**(Sol 未監査)。

---

## §0 到達点

| 段 | 内容 | 状態 |
|---|---|---|
| **S2-1** | 非零類 $[\tilde H]\in H^2(H_F,\mathrm{Ad})$ の明示生成元 | ★ **完了**(紙) |
| **S2-2** | 非分裂拡大 $1\to\mathrm{Ad}\to\tilde H\to H_F\to1$ | ★ **完了**(紙) |
| **S2-3** | braid lift($B_3\twoheadrightarrow\tilde H$) | ★ **完了**(紙の同値 + witness 1 対) |
| S2-4 | 所要の surjectivity / 窓適格性 | ⚠ **未** ⟹ §4 で設問を定式化 |

$$\boxed{\ \textbf{(Ad) 線の最小成果 = 「容器あり・拡大あり・braid が乗る」まで到達}\ }$$

---

## §1 S2-1 / S2-2(再掲・要点のみ)

$$\tilde H:=\bigl\{(A,\sigma)\in SL^{\pm}(2,\mathbf Z/691^2)\times S_3\ :\ \det A=\mathrm{sgn}\sigma\bigr\}$$

- **核**: $\det(I+691X)=1+691\,\mathrm{tr}X$ ⟹ $\ker(\tilde H\to H_F)=\{(I+691X,1):\mathrm{tr}X=0\}\cong\mathfrak{sl}_2=\mathrm{Ad}$、作用は共役 ⟹ **twist $i=0$** ✔
- **非分裂**: 補元は $SL(2,\mathbf Z/691^2)$ 内の $\mathfrak{sl}_2$ の補元を与える ⟹ 系統 C(悉皆検算 PASS + $u^p=I+p(u-I)\ne I$ の $p$ 非依存な紙 1 行)に矛盾 ✔
- $\dim H^2(H_F,\mathrm{Ad})=1$(段 1′ の紙の二導出)⟹ ★ $[\tilde H]$ は**生成元** ✔

---

## §2 ★★★ S2-3 — braid 全射の**明示**

### 2.1 同値定理(前検査 §2・§4)
$$\boxed{\ \textbf{braid lift 可能}\iff \tilde H\ (2,3)\text{-生成}\iff H_F\ (2,3)\text{-生成}\iff SL^{\pm}(2,691)\ (2,3)\text{-生成}\ }$$
- **$c\mapsto1$ の強制**: $Z(\tilde H)\cong C_2$、$\Delta\mapsto$ 互換ゆえ $\det A_\Delta=-1$。$z=(-I,1)$ なら $A_\Delta$ はスカラーで $-1$ が平方 ⟹ **$691\equiv3\pmod4$ で不可能** ⟹ **$z=1$**。
- **非分裂 ⟹ 持ち上げが生成**: $\mathfrak{sl}_2$ は既約($p\ge5$)⟹ $\langle\tilde a,\tilde b\rangle\cap\mathfrak{sl}_2\in\{1,\mathfrak{sl}_2\}$。$=1$ は分裂を意味し S2-2 に矛盾 ⟹ **$=\mathfrak{sl}_2$**。

### 2.2 witness(cert `s2_3_pre_gen23_v1`・trial 1)
$$a=\begin{pmatrix}483&28\\59&208\end{pmatrix},\qquad b=\begin{pmatrix}245&158\\69&445\end{pmatrix}\qquad(\bmod\ 691)$$
**私の独立検証**: $\det a=690\equiv-1$ ✔・$a^2=I$ ✔ / $\det b=1$ ✔・$b^3=I$ ✔ / $\lvert\langle a,b\rangle\rvert=659{,}877{,}360=2\cdot691\cdot(691^2-1)=\lvert SL^\pm(2,691)\rvert$ ✔

### 2.3 ★★ braid 対の明示(私が構成・機械検証済)
全単射 $(x,y)\mapsto(u,v)=(xyx,\,xy)$ の**逆**($z=u^2=v^3$):
$$x=v^{-1}u,\qquad y=u^{-1}v^2$$
$u:=a$, $v:=b$($z=1$)を代入して
$$\boxed{\ \sigma_1\ \longmapsto\ x=b^{-1}a=\begin{pmatrix}386&326\\476&658\end{pmatrix},\qquad \sigma_2\ \longmapsto\ y=a\,b^2=\begin{pmatrix}175&337\\156&178\end{pmatrix}\ }$$
★ **braid 関係の機械検証**: $xyx=yxy=\begin{pmatrix}483&28\\59&208\end{pmatrix}=a$ ✔(理論値 $xyx=u$・$yxy=u^{-1}v^3=u^{-1}u^2=u$ と一致)
★ $\det x=\det y=-1$ ⟹ **$S_3$ 成分は互換** ✔

### 2.4 持ち上げの連鎖($\tilde H$ への到達)
1. $SL^\pm(2,691)\to H_F$: $\ker\cong A_3=C_3$。$\alpha=$ 互換($\mathrm{sgn}=\det a=-1$)・$\beta\in A_3\setminus\{1\}$ ⟹ $\langle\alpha,\beta\rangle=S_3$ ⟹ Goursat で $H_F$ 全体(⚠ 共通商の自明性 = **S2-GAP-3**・機械 1 行)
2. $H_F\to\tilde H$: $\ker=\mathfrak{sl}_2$(691-群)。$\gcd(2,691)=\gcd(3,691)=1$ ⟹ **位数保存持ち上げ** ✔ + §2.1 の非分裂論法 ⟹ **生成する** ✔

$$\boxed{\ \Longrightarrow\ B_3\twoheadrightarrow\tilde H\quad(\sigma_1\mapsto\tilde x,\ \sigma_2\mapsto\tilde y),\qquad c\longmapsto1\ }$$

---

## §3 ★ 窓としての姿(副産物)

$N':=\ker(B_3\to\tilde H)$ とおくと:
- $N'\trianglelefteq B_3$・有限指数 ✔
- ★ **$N'\subseteq PB_3$ は自動**: $\sigma_1,\sigma_2$ の $S_3$ 成分が互換で $S_3$ を生成 ⟹ 誘導される $B_3\to S_3$ は標準射影と $\mathrm{Aut}(S_3)=\mathrm{Inn}(S_3)$ の違いのみ ✔
- ★ **$c\in N'$**($z=1$)⟹ $PB_3/N'=F_2/N'_{F_2}$ ⟹
$$\boxed{\ B_3/N'\cong\tilde H,\qquad PB_3/N'\;\cong\;SL(2,\mathbf Z/691^2)\ }$$
- ★ **$c\in N$ 側** ⟹ wcp5d の「$\tau$ が $F_2/N_{F_2}$ に降りない」問題は**起きません**(実測 $c\in N$ の 16/16 が安全)⟹ 下流の列挙器は **(F2) 商規律の分岐が不要** = 設計上の朗報。
- 規模: $\lvert\tilde H\rvert=6\cdot691^4(691^2-1)\approx6.5\times10^{17}$。

---

## §4 ★★ 【S2-GAP-4】窓適格性 — 設問の正確な定式化(**③ 線の次の標的**)

| # | 問い | 型 | 何を測れば閉じるか |
|---|---|---|---|
| **(Q1)** | $N'\subseteq PB_3$ か | 群論 | ★ **自動・閉鎖済**(§3) |
| **(Q2)** | $N'$ が $\mathrm{NFI}_{PB_3}(B_3)$ の対象($B_3$ 正規・有限指数・$PB_3$ 内)か | 群論 | ★ **自動・閉鎖済**(§3) |
| **(Q3)** | $N'$ が **isolated** か(⟹ $GT(N')$ が群・$\rho_{N'}$ が群準同型) | 群論 | ⚠ **測定が要る**。★ **census 装置は回りません**($\lvert\tilde H\rvert\approx6.5\times10^{17}$ ⟹ shadow の完全列挙は不可能)⟹ **§4.1 の crown 路** |
| **(Q4)** | $A_{N'}=\mathrm{im}\,\rho_{N'}$ が $GT(N')$ を覆うか(= 全射性) | ★ **算術** | SURG バッテリー(crown 検定)+ receipt。⚠ **SURG-A6 の代金は不変** |
| **(Q5)** | $\mathrm{Ad}$ 層の拡大類が $G_\mathbf Q$ 側で実現されるか | ★ **算術**(R-1 の中身) | ⚠ **OPEN**。札 I-CEX-4 の「第 0 要求(両者を同じ空間に置く写像)」が未構成 |

$$\boxed{\ \textbf{測れば閉じるのは (Q3) のみ。(Q4)(Q5) は算術で、(Q5) は }R\text{-}1\ \textbf{そのもの}\ }$$

### 4.1 ★ (Q3) の実行仕様(crown 路 — 巨大群に触らない)
```
=== [S2-4-Q3] N' の isolated 判定(crown 路)===
⚠ 直接列挙は不可(|B_3/N'| ≈ 6.5×10^17)⟹ 以下の順で「触らずに」判定する

[Q3-a] settled の紙側条件(便 121 A7.1 逐語の再利用):
   π∘T_{m,f} = π ⟹ ker T ⊂ PB_3 ⟹ 「PB_3/N' 上の well_defined ∧ kernel_trivial」= settled
   ⟹ ★ 判定は PB_3/N' ≅ SL(2,Z/691^2) の *内部* で閉じる(B_3 全体を作らない)
[Q3-b] ★ crown 分解(SB-1)を適用:
   X := GT(N')。X/Φ(X) 上で極大の共役類ごとに 1 ビット検定
   ⟹ ★ 巨大な X を構成せず、X/Φ の crown census だけで済む
   ⚠ 前提: X = GT(N') 自体の構成が必要 ⟹ ★ これが律速【S2-GAP-5】
[Q3-c] 代替(理論路): SL(2,Z/p^2) 型の窓について settled/isolated を *族として* 決める補題を探す
   ⟹ 私の推薦: ★ こちらを先に(機械路は規模で詰む見込みが高い)
出力: cert (schema s2_4_q3/v1)。u_touched=false
```

### 4.2 ★ ③ 線の次の標的宣言(私の推薦)
$$\boxed{\ \textbf{次の標的} = \textbf{(Q3) — }SL(2,\mathbf Z/691^2)\ \textbf{型の窓の isolated 性を}\textbf{族として}\textbf{決める補題}\ }$$
理由: (Q4)(Q5) は算術で **R-1 が OPEN のまま**(B2 条件 4)。⟹ **群論で閉じられる最後の一段が (Q3)** です。

---

## §5 ★ 非結論行(claim と cert に必ず書く・B2 条件 2/3/4)

> 1. 本結果は「**窓が arithmetic に qualification された**」ことを**意味しない**(B2 条件 2)。到達したのは **群論的な容器・拡大・braid 全射**までです。
> 2. **972 / 非円分供給 / K9・K5 bridge へ流用しない**(B2 条件 3)。
> 3. **R-1 は OPEN**(B2 条件 4)— ③→① 非円分算術供給は未証明。
> 4. ★ **$G_\mathbf Q$ 側の実在については何も言っていません**。$\tilde H$ は braid 側の対象であり、「$G_\mathbf Q$ がこの拡大を実現するか」(= (Q5) = R-1)は**未着手**です。
> 5. ⚠ **格は candidate**。cross-checked は witness の再現(GHA)にのみ及び、**紙の同値定理には及びません**(有限計算核の格を紙包絡へ伝播させない・M121-7)。

---

## §6 cert 記入(schema `F_stage2_ad/v1`)

```
stage : "S2-1"/"S2-2"/"S2-3"(いずれも PASS)
target : "H_F" ; module : "Ad" ; twist_i : 0
class_nonzero : true ; extension_split : false ; braid_lift : true
braid_pair : { sigma_1 : [[386,326],[476,658]], sigma_2 : [[175,337],[156,178]] }   ★ mod 691
braid_relation_verified : true      ★ xyx = yxy = [[483,28],[59,208]]
c_image : "1"                       ★ z=1(p ≡ 3 mod 4 からの強制)
window_shape : { "B_3/N'" : "H~", "PB_3/N'" : "SL(2,Z/691^2)", "c_in_N" : true }
surjectivity : null                 (S2-4 未着手)
★ r1_status : "OPEN"
★ no_window_qualification : true
★ no_transfer : ["972","non-cyclotomic supply","K9/K5 bridge"]
method : "paper_lemma + witness"   ; grade : "candidate"
u_touched : false ; c_touched : false ; verdict : null
```

## §7 GAP

- **【S2-GAP-3】(小)** §2.4-1 の Goursat 細部(共通商の自明性)⟹ 機械 1 行。
- **【S2-GAP-4】★ 定式化完了**(§4)⟹ 実体は **(Q3)**。
- **【S2-GAP-5】(中・新)** $GT(N')$ の構成が (Q3) の律速。⟹ ★ **crown 路(SB-1)でも $X$ 自体は要る** ⟹ 族補題(§4.1 [Q3-c])を推薦。
- **【W6-GAP-1】★ 閉鎖**(witness により $SL^\pm(2,691)$ は $(2,3)$-生成)。
- **申告**: 私の側は機械走行ゼロ(検証は python 行列演算のみ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**。
