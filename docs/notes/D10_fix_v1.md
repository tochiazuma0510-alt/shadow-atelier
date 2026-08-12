# 宣言 **D10^fix**(便 121 §9.2-4 の修理形)

作成: 数学者(Opus 5)/ 2026-08-12 / 発注 = 司令塔裁定 1045
前版 = `sol112_tier2_audit_and_D10_v1.md` §2.2 の C1–C7。**C1 / C2 / C5 を便 121 の修理形へ置換**。
★ **格: candidate / Sol-audited**。⚠ **有限計算核(2,160 点)のみ cross-checked** — ★ **紙包絡へ伝播させません**(新規律・M121-7)。

---

## §0 宣言(標的は不変)

> ## 【D10^fix】$W_9$ には $P_\infty$ が Weierstrass 点となる $k=2$ 平面モデルが存在しない
> 同値に **$2\notin H(P_\infty)$**($P_\infty$ の Weierstrass 半群に 2 が属さない)。
> ⚠ **「$W_9$ は超楕円でない」は従いません**(前版で訂正済・便 121 A13.2 で射程正しいと確認)。

---

## §1 ★★ C1(置換)— trace/norm による integral quadratic model

**✘ 旧 C1**: Newton 三角形の同重み格子点が $(i,j)\mapsto(i+k,j-18)$ で移り合う ⟹ ansatz 完備性。
⚠ **誤り(M121-3)**: 重み $18i+kj$ を保つ**原始格子刻み**は
$$\left(\frac{k}{\gcd(18,k)},\ -\frac{18}{\gcd(18,k)}\right)$$
で、$k=2$ では $(1,-9)$、$k=3$ では $(1,-6)$。⟹ 旧証明はそのままでは使えません。

**★ 新 C1(便 121 A6.1・私が独立に再検証)**:
1. $[K:F_9(w)]=2$($k^*=2$ の仮定)。
2. $t=\lambda_9$ の極は $P_\infty$ のみで、$P_\infty$ は $w=\infty$ 上 ⟹ $t$ は $F_9[w]$ 上 **integral** ⟹ 最小多項式 $t^2-\mathrm{Tr}(t)\,t+\mathrm N(t)=0$ の係数は **$F_9[w]$ に入る**(整閉)。
3. **次数**: $\mathrm{ord}_{P_\infty}(w)=-2$、$\mathrm{ord}_{P_\infty}(t)=-18$ ⟹ $\deg_w\mathrm{Tr}(t)\le18/2=9$、$\deg_w\mathrm N(t)\le36/2=18$。
4. ★ **$t=0$ の全分岐正規化**: $\mathrm{div}(t)=18P_0-18P_\infty$ かつ $\iota(P_\infty)=P_\infty$ ⟹
$$\mathrm{div}\bigl(\mathrm N(t)\bigr)=\mathrm{div}(t\cdot\iota t)=18P_0+18\,\iota(P_0)-36P_\infty=\mathrm{div}(w^{18})$$
⟹ $\mathrm N(t)/w^{18}$ は因子 0 ⟹ **定数** ⟹ $\mathrm N(t)=A\,w^{18}$。

$$\boxed{\ F(t,w)=B\,t^2+t\,P(w)+A\,w^{18},\qquad \deg P\le9\ }$$

★ **Newton の格子文に一切依存しません** ✔(私の独立検証: 4 段すべて追認)

---

## §2 ★ C2(前件追加)— residual 開条件

**✘ 旧 C2**: 完全 $k$ 乗境界($c_9^2=4AB$)**だけ**で $t=\infty$ 上が 1 点 $e=18$。
⚠ **誤り(M121-4)**: 面方程式の重根は**必要条件**にすぎず、Newton–Puiseux の次段で枝が**再分裂しない**ことまでは保証しません。

$$\boxed{\ \textbf{新規律}:\ \textbf{Newton 完全冪}\ \ne\ \textbf{枝一意性 — 別行で記帳する}\ }$$

**★ 新 C2(2 行)**:
| 行 | 条件 | 種別 |
|---|---|---|
| **C2-a** | $c_9^2=4AB$(完全 2 乗境界) | ★ **必要条件** |
| **C2-b** | $e:=\max\{j\le8:\ c_j\ne0\}$ が **偶数**(一般点で $e=8$) | ★ **residual 開条件**(前件として明記) |

⟹ **C2-a ∧ C2-b で「$t=\infty$ 上が 1 点・$e=18$」が十分**。
★ $k=3$ の対応物は $c^{(2)}_5\ne c^{(1)}_{11}$(同じ役割)。⚠ $k\nmid18$ の $k=4,5$ へは**拡張しません**。

---

## §3 ★★ C5(置換)— Tier 2 統一路へ

**✘ 旧 C5**: 層 $(0,9)$ 空を「車線 B の Gröbner × 手計算の二経路」で全域証明。
⚠ **誤り(M121-5)**: $U_\pm=(w^9+1)\pm S_1$ を**一般に互いに素**とした点。共通根 $q$ は $q^9=-1$ ∧ $S_1(q)=0$ を満たし、$q^2\mid Q$ は $Q=(w-a)(w-b)g^2$ と**両立**します。しかも $R_2(q)=-4\ne0$ なので、私の $R_1,R_2$ 互いに素論法($c_0\ne0$ 由来)は**この locus を排除しません**。
$$\boxed{\ \Longrightarrow\ \textbf{車線 B は }\textbf{coprime sublocus だけを覆う}\ }$$
★ 私は独立に確認しました($Q(q)=0$・$(q^9-1)^2=4$ ⟹ $R_2(q)=-4$)✔ **Sol の指摘は正しい**。

**★ 新 C5**: 層 $(0,9)$ 空の根拠は **Tier 2 の統一的な判別式因子列挙**(cert `r13_p1_tier2_v2_20260812.json` + 独立 checker)。4 既約因子の profile は $(6,9)$ または $(8,7)$ のみで、$(0,9)$ は現れない。
⟹ **「車線 B の Gröbner × 手計算で全域 cross-check」とは書きません**。⚠ 車線 B を定理証明として残すなら、**共通因子 locus だけ**を非当事者 falsifier へ回すこと(便 121 B4)。

---

## §4 修理後の条件表

| # | 条件 | 状態 |
|---|---|---|
| **C1** | trace/norm による integral quadratic model ⟹ $F=Bt^2+tP(w)+Aw^{18}$、$\deg P\le9$ | ★ **置換済**(§1) |
| **C2-a** | $c_9^2=4AB$ | ★ 必要条件(§2) |
| **C2-b** | $e=\max\{j\le8:c_j\ne0\}$ が偶数 | ★ **新設・前件明記**(§2) |
| **C3** | 5 層分割の完備性($o_1$ 偶・$o_2$ 奇・$o_1+o_2=9$) | 不変 |
| **C4** | $\operatorname{disc}(R_1)\cdot\operatorname{disc}(R_2)=0$ が全層で必要(**積**) | 不変 |
| **C5** | 層 $(0,9)$ 空 = **Tier 2 統一因子分類**(車線 B は coprime sublocus 限定) | ★ **置換済**(§3) |
| **C6** | 2,160 候補が全て genus 7 | ★ **cross-checked**(producer / 独立 checker 一致) |
| **C7** | $g(C_2)=1$ ⟹ $\operatorname{ord}(P_0-P_\infty)=9$・$P_0$ 非 Weierstrass | 不変(単一実測依存) |

$$\boxed{\ \textbf{D10}^{\rm fix}\ \textbf{の格} = \textbf{candidate / Sol-audited}\ }$$
$$\boxed{\ \textbf{新規律}:\ \textbf{有限計算核(C6)の cross-checked を紙包絡(C1--C5,C7)へ}\textbf{伝播させない}\ }$$

---

## §5 ★ 教訓行(M121-3〜5・7)

| 札 | 教訓 |
|---|---|
| **M121-3** | ★ **Newton 格子の原始刻みは $\gcd$ で割る**。$(k,-18)$ は $\gcd(18,k)>1$ のとき原始でない ⟹ 「同値な格子点は高々 2 個」という数え上げが崩れる。**格子論法を使う前に原始刻みを計算せよ**。 |
| **M121-4** | ★ **面方程式の重根は「境界の $k$ 根の一致」までしか言わない**。**枝の一意性(1 点 $e=18$)は residual 段の条件**。⟹ **必要条件と十分条件を別行で書く**。 |
| **M121-5** | ★ **「一般に互いに素」は genericity の仮定であって定理ではない**。共通因子 locus を**明示的に排除する論法**がなければ、その sublocus は未被覆。⟹ **coprimality を使うときは locus を書き出せ**。 |
| **M121-7** | ★ **有限計算核の格を紙包絡へ自動伝播させない**。cert が cross-checked でも、その cert を使う**定理全体**は紙の前件を含むので **candidate** に留まる。 |

⟹ ★ **私自身への適用**: M121-3/4/5 はいずれも**私の起草**(`w9_structure_and_ansatz_v1` §4 / `w9_k2_diagnosis_v1` §2 / `w9_laneB_elimination_v1` §2)。⟹ **暫定札としてそのまま受け入れ**、案 B により Sol 採番(M121-3/4/5)を正とします。

---

## §6 GAP

- **【D10-GAP-3】(中・新)** 車線 B の **coprime sublocus の外**(共通根 $q$ をもつ locus)は、Tier 2 統一路で覆われている**はず**ですが、その被覆の明示照合は未了 ⟹ falsifier 回付候補(便 121 B4)。
- **【D10-GAP-1/2】(継続)** $a=b=0$ chart / profile の既約因子ごとの一定性 ⟹ cert 注記。
- **申告**: 走行ゼロ・$u$ 非接触・**Sol-audited(便 121)**・**verified ではない**。
