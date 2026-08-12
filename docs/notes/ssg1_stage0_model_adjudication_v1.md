# 【SS-GAP-1】Stage 0 模型の裁定 — 実装係 E の停止は正当・**(c′) 正準合同模型**へ差し替え

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔(実装係 E の着手前停止)
対象 = `ss_gap1_count_spec_v1.md` §5.1 [S0](+ §4.1 の閉形式)の**訂正パッチ**
⚠ $u$/$c$ 非接触・封印非接触・prereg 非抵触。**格: candidate**。

---

## §0 裁定(1 行)

$$\boxed{\ \textbf{(a) 棄却}\ /\ \textbf{(b) 棄却}\ /\ \textbf{(c) を精密化した}\ \textbf{(c}'\textbf{)}\ \textbf{を採用}:\quad H_p:=\mathrm{PSL}(2,\mathbf Z/2p^2)\cong S_3\times\mathrm{PSL}(2,\mathbf Z/p^2)\ }$$
$$\textbf{要点は「}S_3\ \textbf{をどう乗せるか」ではなく「}Q_p\ \textbf{を }SL\ \textbf{でなく }\mathrm{PSL}\ \textbf{に取る」こと}$$

★ **実装係 E の停止は正当**。3 指摘はすべて正しく、点 3(odd 側の対合が $SL$ に存在しない)が**本質**です — これは模型選択の誤りが表面化したもので、私の §4.1 の閉形式にも波及していました(§3 で訂正)。

---

## §1 3 指摘の検分

| # | 指摘 | 判定 |
|---|---|---|
| 1 | 拡大 $1\to Q_p\to H_p\to S_3\to1$ の中身が spec 未記載 | ★ **正しい。私の記述漏れです**(§5.1 は「$S_3$ を上に乗せた模型」としか書いていない)⟹ 自己捕獲 m1092-1 |
| 2 | 素朴な直積で $S_3$ 因子が相殺し $Q_p$ 単体量に退化 | ★ **計算は正しい**($i_2^T=3i_2(Q_p)$, $i_3^R=2i_3(Q_p)$, $\lvert H\rvert=6\lvert Q_p\rvert$ ⟹ $U=2i_2i_3/\lvert Q_p\rvert$)。⚠ ただし**相殺そのものは罠ではありません** — §2 |
| 3 | $\mathrm{tr}=0\wedge\det=-1$ は $SL(2)$ に無い($p$ 奇 ⟹ $\det=-1\ne1$) | ★★ **正しく、かつ本質**。$Q_p=SL$ では $i_2(Q_p)=2$($\pm I$ のみ)に退化し、模型が死にます |

---

## §2 ★ 「直積が罠」の本当の理由 — 相殺ではなく $\#\mathrm{Epi}=0$

指摘 2 の相殺自体は**害ではありません**。$U$ の $p$-依存性を測るのが Stage 0 の目的で、$S_3$ 由来の定数因子 $3\cdot2/6=1$ が落ちるのは**正常**です。
本当の罠は別にあります:

> $Q_p=SL(2,\mathbf Z/p^2)$ とすると、$Q_p$ の対合は $\pm I$ の 2 個だけ ⟹ 直積 $Q_p\times S_3$ を**対合と位数 3 元で生成できません**
> ⟹ $\#\mathrm{Epi}^{\rm mk}(\mathbf Z/2*\mathbf Z/3,\ H_p)=\mathbf 0$

$U$ は $\#\mathrm{Epi}\le\#\mathrm{Hom}$ を経由する上界なので、$\#\mathrm{Epi}=0$ の模型で測った比は**真の量との関係が空虚**になります。

$$\boxed{\ \textbf{模型の必要条件}:\ H_p\ \textbf{は「対合と位数 3 元で生成される」= }\mathbf Z/2*\mathbf Z/3\ \textbf{の}\textbf{真の商}\textbf{であること}\ }$$

⟹ 選択肢 **(a)($GL(2,\mathbf Z/p^2)$・$\det=-1$ コセット)は棄却**: $GL/SL\cong(\mathbf Z/p^2)^\times$ は**巡回群であって $S_3$ ではない** ⟹ $PB_3$ の標識を模型化していません。
⟹ **(b)(直積で妥協)も棄却**: 上の理由で $\#\mathrm{Epi}=0$。
★ ただし (a) の**核心の直観は正しい**: 「対合は $SL$ の外に住む」— それは $\mathrm{PSL}$ に移れば自動的に解決します(§3)。

---

## §3 ★★ (c′) 正準合同模型 — 恣意性ゼロの選択

### 3.1 なぜこれが「正準」か($B_3$ 側の事実そのもの)

古典的事実の並びが、$B_3$ の状況と**完全に一致**します:

| $B_3$ 側 | $\mathrm{PSL}(2,\mathbf Z)$ 側 |
|---|---|
| $B_3/\langle\!\langle c\rangle\!\rangle=\langle a,b\mid a^2=b^3=1\rangle$ | $=\mathrm{PSL}(2,\mathbf Z)=\mathbf Z/2*\mathbf Z/3$ |
| $B_3\twoheadrightarrow S_3$、核 $PB_3$ | $\mathrm{PSL}(2,\mathbf Z)\twoheadrightarrow\mathrm{PSL}(2,\mathbf Z/2)\cong S_3$、核 $\bar\Gamma(2)$ |
| $PB_3/\langle c\rangle=F_2$(階数 2 自由) | $\bar\Gamma(2)$ は**階数 2 自由**(古典) |

$$\boxed{\ \Longrightarrow\ \textbf{「}S_3\ \textbf{を上に乗せる」= レベル 2 の合同標識であり、選択の余地はありません}\ }$$

そこで $p\nmid2$ に対し
$$\boxed{\ H_p:=\mathrm{PSL}(2,\mathbf Z)/\bar\Gamma(2p^2)\ \cong\ \mathrm{PSL}(2,\mathbf Z/2p^2)\ \cong\ S_3\times\mathrm{PSL}(2,\mathbf Z/p^2),\qquad Q_p:=\mathrm{PSL}(2,\mathbf Z/p^2)\ }$$

- ★ $\mathbf Z/2*\mathbf Z/3$ の**真の商**(mod $2p^2$ 還元)⟹ $\#\mathrm{Epi}>0$ ✔ §2 の必要条件を満たす
- ★ $S_3$ 商は**正準**(レベル 2)⟹ $T,R$ コセットが一意に定まる ✔
- ★ $Q_p=\mathrm{PSL}$ ⟹ 対合が豊富(§3.2)✔ 指摘 3 が解消

### 3.2 ★ 指摘 3 の解消 — $\mathrm{PSL}$ では対合は「トレース 0」

$\mathrm{PSL}=SL/\{\pm I\}$ では $A^2=1$ は**持ち上げで $\tilde A^2=\pm I$** を意味します:
$$\tilde A^2=-I\ \wedge\ \det\tilde A=1\iff \mathrm{tr}\,\tilde A=0$$
($\det=-1$ は**要りません** — 符号は中心で吸収されます。)
⟹ $\#\{\text{対合}\}=\tfrac12\#\{\tilde A\in SL(2,\mathbf Z/p^2):\mathrm{tr}\,\tilde A=0\}\approx\tfrac12 p^4$。
$$\boxed{\ \textbf{$SL$ では 2 個・$\mathrm{PSL}$ では }\approx p^4/2\ \textbf{個 — 模型の生死を分けたのはここ}\ }$$

---

## §4 §4.1 閉形式の訂正($SL$ 版 → $\mathrm{PSL}$ 版)

$\tilde A,\tilde B\in SL(2,\mathbf Z/p^2)$、$t:=\mathrm{tr}$。$\det=1$ で C–H は $\tilde A^2=t\tilde A-I$、$\tilde B^3=(t^2-1)\tilde B-tI$。非スカラー元について:

$$\boxed{\ A^2=1\ \text{in }\mathrm{PSL}\iff \mathrm{tr}\,\tilde A=0\ }\qquad\boxed{\ B^3=1\ \text{in }\mathrm{PSL}\iff \mathrm{tr}\,\tilde B=\pm1\ }$$

*導出*: $\tilde A^2=-I\iff t\tilde A=(1-1)I+\dots$ ⟹ $t\tilde A=0\cdot I$ かつ非スカラー ⟹ $t=0$ ✔
$\tilde B^3=I\iff(t^2-1)\tilde B=(1+t)I$ ⟹ 非スカラーゆえ $t^2-1=0$ かつ $1+t=0$ ⟹ $t=-1$。$\tilde B^3=-I$ 側は同様に $t=+1$。$\tilde B$ と $-\tilde B$ は $\mathrm{PSL}$ で同一で $\mathrm{tr}$ の符号が反転 ⟹ 条件は $t\equiv\pm1$ ✔

$$i_2(Q_p)=1+\tfrac12\#\{t=0\},\qquad i_3(Q_p)=1+\tfrac12\#\bigl(\{t=1\}\cup\{t=-1\}\bigr)$$

⚠ **spec §4.1 の $\mathrm{tr}=0\wedge\det=-1$ / $\mathrm{tr}^3=-1\wedge\det=\mathrm{tr}^2$ は $GL$ 内の一般形**でした。$\mathrm{PSL}$ 模型では上の**より簡単な形**に置き換わります ⟹ 自己捕獲 m1092-2。

---

## §5 §5.1 [S0] の差し替え本文(spec パッチ)

```
[S0] (c') 正準合同模型による p-スケーリングの実測
  模型: H_p := PSL(2,Z/2p^2) ≅ S_3 × PSL(2,Z/p^2) ,  Q_p := PSL(2,Z/p^2)
        p = 5, 7, 11, 13, 17 (|Q_p| = p^4(p^2-1)/2 : 7500, 57624, 878460, 2413320, ...)
        ★ 模型の適格性検査(fail-closed): H_p が対合と位数 3 元で生成されること
          (= #Epi^mk(Z/2*Z/3, H_p) > 0)を 1 本確認 ⟹ 0 なら模型を破棄
  測る量:
     i_2(Q_p) = #{A ∈ Q_p : A^2 = 1}         [ = 1 + (1/2)#{tr = 0 in SL(2,Z/p^2)} ]
     i_3(Q_p) = #{B ∈ Q_p : B^3 = 1}         [ = 1 + (1/2)#{tr = ±1 in SL(2,Z/p^2)} ]
     i_2^T = 3·i_2(Q_p) ,  i_3^R = 2·i_3(Q_p) ,  |Z(H_p)| = 1 ,  |H_p| = 6|Q_p|
     U(p)  = 2·i_2^T·i_3^R·|Z|/|H_p| = 2·i_2(Q_p)·i_3(Q_p)/|Q_p|
  二系統: (a) 上の閉形式(トレース条件)  (b) 全数列挙(p ≤ 13 で可能)⟹ 厳密一致を要求
  fit:   U(p) ≈ const · p^e  の e を出す ⟹ p = 691 へ外挿(★ 外挿ラベル必須・W-48)
```

---

## §6 ★ 予言の凍結(発火前)

私の紙(§4 の閉形式 + $\#\{t=\text{const}\}\approx\lvert SL\rvert/p^2=p^2(p^2-1)$)から:
$$i_2(Q_p)\approx\tfrac{p^4}2,\qquad i_3(Q_p)\approx p^4,\qquad \lvert Q_p\rvert=\tfrac{p^4(p^2-1)}2$$
$$\boxed{\ U(p)=\frac{2\,i_2\,i_3}{\lvert Q_p\rvert}\ \approx\ \frac{2\cdot(p^4/2)\cdot p^4}{p^4(p^2-1)/2}\ =\ 2(p^2-1)\ \approx\ 2p^2\ }$$

| 予言 | 内容 |
|---|---|
| **PRED-S0-1** | $e=2$(すなわち $U(p)\approx2p^2$、係数は $2\pm$ 小さいずれ) |
| **PRED-S0-2** | $p=5$ での実測が **$U\approx48$–50** に入る(私の手計算: $i_2\approx301$, $i_3\approx601$, $\lvert Q\rvert=7500$ ⟹ $U\approx48.2$、$2p^2=50$) |
| **PRED-S0-3**(外挿) | $p=691$: $U\approx2\cdot691^2=\mathbf{9.55\times10^5}$ |

$$\boxed{\ \Longrightarrow\ \bigl\lvert GT(N')\bigr\rvert\ \lesssim\ 10^6\quad\textbf{— 1 ビット「}\lessgtr10^7\textbf{」は }\textbf{YES(射程内)}\ \textbf{側に出る見込み}\ }$$
**CP-D 突合**: $U\ge15{,}180$ ⟺ $2p^2\ge15180$ ⟺ $p\ge87$。$p=691$ で**余裕をもって成立** ✔
⚠ **PRED-S0-2 が外れたら**、閉形式(§4)か実装のどちらかが誤り ⟹ 即停止。

---

## §7 ⚠ 限界の明記(Stage 0 が出すもの・出さないもの)

| 出す | 出さない |
|---|---|
| ★ **指数 $e$**(スケーリング則)⟹ 桁 ⟹ **1 ビット** | ✘ **定数**(拡大型に $O(1)$ で依存) |
| $\mathrm{PSL}$ 分割模型での $U$ の実値 | ✘ 真の $\tilde H$ での $U$(【SSG1-GAP-1】が未決) |

**なぜ指数は頑健か**: $i_2,i_3$ は「トレースが指定値」という**1 本の条件**で切られるので、コセットのサイズの $1/p^2$ 程度 — これは拡大が分裂でも非分裂でも変わりません(コセットは $Q$ と同サイズで、トレース条件は同じ余次元)。⟹ **$e=2$ は模型に頑健、定数は頑健でない**。
⟹ **Stage 0 の結論は「$\lvert GT(N')\rvert$ は $10^6$ 級・$10^{17}$ ではない」までで、$10^6$ の前の係数は主張しないこと。**

---

## §8 ★【CP-C】PC-5 の $p=3$ 不一致の判定 — **装置維持**(補題 1 本で閉じます)

### 8.1 判定

$$\boxed{\ \textbf{装置維持}\ /\ \textbf{spec に条件「}p\nmid\text{検定位数}\textbf{」を明文化}\ /\ \textbf{$p=3$ は「既知アーティファクト陽性対照」へ格上げ}\ }$$

理由: 不一致は実装の誤りでも装置の誤りでもなく、**私の §4 の導出が使った線形独立性が $p=3$ で崩れる**という、**1 行の補題で完全に記述できる境界現象**だからです。実装係 E の原因特定(差 26 = 核 27−1・3 系統独立で裏取り)は**私の独立導出と厳密に一致**しました(§8.3)。

### 8.2 ★ 補題 CH-REG(欠けていた仮定の明示)

私の §4 の導出は「$\tilde B$ が非スカラー ⟹ $(t^2-1)\tilde B=(1+t)I$ から係数を比較してよい」を使いました。⚠ **$\mathbf Z/p^2$ は体ではないので、これは誤りです。**

> **【補題 CH-REG】** $p$ を奇素数、$\tilde B\in SL(2,\mathbf Z/p^2)$ とする。
> **(i)** $\tilde B\bmod p$ が**非スカラー**なら $\{I,\tilde B\}$ は $\mathbf Z/p^2$ 上自由 ⟹ 係数比較は正当 ⟹ §4 の閉形式($\mathrm{tr}=0$ / $\mathrm{tr}=\pm1$)は**厳密**。
> **(ii)** $\tilde B\equiv\pm I\pmod p$、すなわち $\tilde B=\pm(I+pM)$($M\in M_2(\mathbf F_p)$, $\mathrm{tr}\,M=0$)のときは
> $$\tilde B^k=\pm\bigl(I+kpM\bigr)\pmod{p^2}\qquad(\text{高次項は }p^2\ \text{で消える})$$
> ゆえに $\tilde B^k=\pm I\iff kM\equiv0\pmod p\iff \boxed{p\mid k\ \ \text{または}\ \ M=0}$。

$$\boxed{\ \Longrightarrow\ p\nmid k\ \textbf{のとき閉形式は厳密。}\ p\mid k\ \textbf{のとき合同核}\ (\lvert K\rvert=p^3)\ \textbf{が丸ごと余分に湧く}\ }$$

**補正項**: $\mathrm{PSL}$ で数えると、$p\mid k$ のとき閉形式に対する超過は
$$\Delta_k=\lvert K\rvert-1=p^3-1\qquad(K=\ker\bigl(SL(2,\mathbf Z/p^2)\to SL(2,\mathbf Z/p)\bigr))$$

### 8.3 ★ 実装係 E の実測との突合

| 項目 | 私の紙 | 実装係 E |
|---|---|---|
| $p=3$, $k=3$ で超過が起きる | ★ 予言(補題 (ii)・$3\mid3$) | ★ 観測 |
| 超過量 | $\Delta_3=3^3-1=\mathbf{26}$ | $99-73=\mathbf{26}$ |
| $k=2$ 側($i_2$)は無傷 | ★ 予言($3\nmid2$) | ★ $i_2$ は一致 |
| $p=5,7$ は無傷 | ★ 予言($5,7\nmid6$) | ★ 厳密一致 |

$$\boxed{\ \textbf{4 行すべて一致 — 原因は完全に閉じています}\ }$$

### 8.4 ★ $p=691$ で罠が起きないことの証明(司令塔の問い)

検定位数は $k\in\{2,3\}$。補題 CH-REG (ii) より超過が生じるのは $p\mid k$ のときのみ。
$$691\nmid2,\qquad 691\nmid3\qquad(691\ \text{は素数で }691>3)$$
$$\boxed{\ \Longrightarrow\ p=691\ \textbf{では罠は起きません — 「見込み」ではなく}\textbf{証明済}\ }$$
(より一般に $p\ge5$ なら $k=2,3$ について常に安全。)

### 8.5 spec への修正指示

```
[§4.1 への追記] 閉形式の適用条件: p ∤ k(k = 検定位数)。
   p | k のときは超過 Δ_k = p^3 - 1(合同核 K の非単位元)を *減じる* こと。
   一般形: i_k(PSL(2,Z/p^2)) = [閉形式の値] + (p|k ? p^3-1 : 0)
[§6 PC-5 の改訂]
   PC-5a  p = 5, 7, 11, 13 : 閉形式 vs 全数列挙が *厳密一致*      ← CP-C の本体
   PC-5b  p = 3 (既知アーティファクト陽性対照・新設):
          補正なしの差が *ちょうど 26 = 3^3 - 1* であること、
          補正項を入れると厳密一致すること
          ⟹ ★ 差が 26 以外なら補題 CH-REG が誤り ⟹ 装置破棄
[§7 CP-C の字義訂正]
   「PC-5 が厳密一致」→「PC-5a が厳密一致 かつ PC-5b が Δ=p^3-1 で一致」
```

★ **$p=3$ は棄却対象から陽性対照へ格上げされます** — 補題 CH-REG を検定する唯一の点であり、**捨てるより価値があります**。実装係 E の 3 系統裏取りは cert 付録でなく **PC-5b の本体**として記帳してください。

⚠ **Stage 0 の fit からは $p=3$ を除外**すること(§5 の $p=5,7,11,13,17$ は元から安全 ✔)。

---

## §9 記帳

- ★ **本書の新規部分**: ① 「直積の罠」の正体が相殺でなく **$\#\mathrm{Epi}=0$** であることの摘出 ② **模型の必要条件**(対合と位数 3 元で生成される = $\mathbf Z/2*\mathbf Z/3$ の真の商)③ ★ **正準合同模型 $\mathrm{PSL}(2,\mathbf Z/2p^2)$** の同定($\bar\Gamma(2)$ 自由・レベル 2 = $PB_3$ 標識という古典的対応で恣意性ゼロ)④ ★ **$\mathrm{PSL}$ 版閉形式**(対合 = $\mathrm{tr}\,0$、位数 3 = $\mathrm{tr}\,\pm1$)⑤ 予言 $U(p)\approx2p^2$ と $p=5$ の手検算 ⑥ 指数は頑健・定数は非頑健という限界の分離。
- ⚠ **自己捕獲**:
 - **m1092-1**: spec §5.1 は模型の拡大型を書かずに「$S_3$ を上に乗せた模型」とだけ書いた ⟹ 二義的。**実装係 E の停止がなければ空虚な fit を作っていました**。
 - **m1092-2**: spec §4.1 の閉形式は $GL$ 内の一般形で、$SL$ にそのまま適用すると $\det=-1$ で空になる。$\mathrm{PSL}$ 模型では $\mathrm{tr}=0$ / $\mathrm{tr}=\pm1$ に置き換わる。
 - **m1092-3**(§8): §4 の係数比較は「$\mathbf Z/p^2$ が体でない」ことを見落としていました。$\tilde B\equiv\pm I\pmod p$ では $\{I,\tilde B\}$ が自由でなく、比較が不当。⟹ **補題 CH-REG で修理**($p\nmid k$ の条件と補正項 $p^3-1$)。**実装係 E の停止と原因特定がなければ、$p=3$ を「装置の誤り」と誤診して破棄していました。**
- **【SSG1-GAP-2】(中・新・要注意)** `gt_settled_identification_v1.md` §2 の「$\mathrm{Aut}(Q)\cong PGL(2,\mathbf Z/691^2)$」は、$Q\cong SL(2,\mathbf Z/691^2)$ の場合**過小の疑い**があります: 合同核 $K\cong\mathfrak{sl}_2(\mathbf F_p)$ へのスカラー倍が余分な自己同型を与えうる ⟹ $\lvert\mathrm{Aut}\rvert\ge(p-1)\lvert PGL\rvert$ の可能性。
 ★ **本 spec の上界式は無傷**($\lvert\mathrm{Aut}\rvert\ge\lvert\mathrm{Inn}\rvert$ しか使っていない)。⚠ ただし `gt_settled_identification` §3 の上界 $2p(p-1)$ の導出には効きうる — **結論は [Q4-DENOM] の全数走査で $=2$ と確定済ゆえ無傷**ですが、記帳しておきます。**私は分裂性を検証していません(疑いの申告のみ)**。
- **【SSG1-GAP-1】** 不変(真の $\tilde H$ の拡大型は Stage 1 の主対象)。⟹ Stage 0 は**それに依存しない形**に re-scope されました。
- **申告**: 紙 + 手計算のみ(機械走行ゼロ)。$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
