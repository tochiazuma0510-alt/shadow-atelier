# (Ad) 段 2 — S2-3(braid lift)の**前検査**(裁定 1054・教訓 F-1 の早期適用)

作成: 数学者(Opus 5)/ 2026-08-13 / 対象 = `F_stage2_S1S2_construction_v1.md` の $\tilde H$
⚠ B2 の 5 条件を遵守(target $H_F$ / module $\mathrm{Ad}$ / twist $i=0$ / 窓資格非結論 / 流用禁止 / **R-1 OPEN**)。
⚠ $u$/$c$ 非接触。**格: candidate**(Sol 未監査)。★ **機械走行ゼロ(紙のみ)**。

---

## §0 結論 — **F4 ではありません。既存の未決問題に完全帰着しました**

$$\boxed{\ \textbf{braid lift 可能}\iff \tilde H\ \text{が}(2,3)\text{-生成}\iff H_F\ \text{が}(2,3)\text{-生成}\iff SL^{\pm}(2,691)\ \text{が}(2,3)\text{-生成}\ }$$

★ 最右辺は **私の既存 GAP【W6-GAP-1】**(`w691_scan_gen23_spec_v1.md`)と**同一の問い**です。
⟹ ★★ **発注設計もすでに存在します**(W691-GEN23: 目撃者 1 対で証明・乱択探索・2000 対で打切り ⟹ UNKNOWN)。
⟹ **S2-3 に大予算を投じる前に、秒〜分の既存設計 1 本で決着します**(教訓 F-1 の狙いどおり)。

---

## §1 中心の同定

$\tilde H=\{(A,\sigma)\in SL^\pm(2,\mathbf Z/691^2)\times S_3:\det A=\mathrm{sgn}\sigma\}$。第 1 成分への射影は全射。
⟹ 中心元は $A\in Z(SL^\pm(2,\mathbf Z/691^2))$ かつ $\sigma\in Z(S_3)=\{1\}$。スカラー $\lambda I$ は $\det=\lambda^2\in\{\pm1\}$:
- $\lambda^2=1\Rightarrow\lambda=\pm1$ ✔
- $\lambda^2=-1$ は $-1$ が平方であることを要する。**$691\equiv3\pmod4$ ⟹ $-1$ は非平方剰余** ⟹ ✘

$$\boxed{\ Z(\tilde H)=\{(I,1),(-I,1)\}\cong C_2\ }$$

---

## §2 ★★★ $c$ の像は **1 に強制**される

braid の中心元 $c=\Delta^2$($\Delta=\sigma_1\sigma_2\sigma_1$)⟹ 像 $z\in Z(\tilde H)=\{1,(-I,1)\}$。
$B_3\to S_3$ で $\sigma_i\mapsto$ 互換 ⟹ $\Delta\mapsto$ 互換(3 個の互換の積)⟹ $\mathrm{sgn}=-1$ ⟹ **$\det A_\Delta=-1$**。

$z=(-I,1)$ とすると $A_\Delta^2=-I$ かつ $\det A_\Delta=-1$:
固有値 $\lambda$ は $\lambda^2=-1$、積 $=\det=-1$ ⟹ $\{\lambda,\lambda\}$ 型で $\lambda^2=-1$ ⟹ $A_\Delta=\lambda I$(スカラー)⟹ **$-1$ が平方であることを要する** ⟹ $691\equiv3\pmod4$ で **不可能**。

$$\boxed{\ \Longrightarrow\ z=1\ \Longrightarrow\ c\mapsto1\ \Longrightarrow\ \tilde H\ \textbf{は }B_3/\langle c\rangle=PSL(2,\mathbf Z)=C_2*C_3\ \textbf{の商}\ }$$
$$\boxed{\ \Longrightarrow\ \tilde H\ \textbf{は}(2,3)\textbf{-生成でなければならない}\ }$$

---

## §3 整合検査(必要条件・すべて PASS = 障害なし)

| # | 条件 | 判定 |
|---|---|---|
| (a) | $B_3^{ab}=\mathbf Z$(巡回)⟹ 商の $ab$ は巡回 | $SL(2,\mathbf Z/p^2)$ は完全($p\ge5$)⟹ $[\tilde H,\tilde H]\supseteq SL(2,\mathbf Z/p^2)\supseteq\mathfrak{sl}_2$ ⟹ $\tilde H^{ab}=H_F^{ab}=C_2$ ★ **巡回** ✔ |
| (b) | $PSL(2,\mathbf Z)^{ab}=C_6$ ⟹ $\tilde H^{ab}$ は $C_6$ の商 | $C_2\mid C_6$ ✔ |
| (c) | 位数の整合 | $\lvert\tilde H\rvert/\lvert H_F\rvert=691^3=\lvert\mathfrak{sl}_2\rvert$ ✔($\lvert H_F\rvert=1{,}979{,}632{,}080$ ✔) |

⟹ ★ **紙の必要条件では落ちません**(= F4 の即断はできない)。

---

## §4 ★★★ 非分裂性が効いて **同値**になる

$\mathfrak{sl}_2$ は $H_F$-加群として **既約**($p\ge5$ の随伴表現)⟹ $\mathfrak{sl}_2$ は $\tilde H$ の**極小正規部分群**。

$a,b$($位数 2,3$)が $H_F$ を生成するとする。
1. **位数を保つ持ち上げが存在**: $\gcd(2,691)=\gcd(3,691)=1$ ⟹ 核 $\mathfrak{sl}_2$ は 691-群 ⟹ **互いに素持ち上げ**で位数 2, 3 の元 $\tilde a,\tilde b$ が取れる ✔
2. $\langle\tilde a,\tilde b\rangle\cdot\mathfrak{sl}_2=\tilde H$(像が $H_F$ を生成)。
3. 既約性より $\langle\tilde a,\tilde b\rangle\cap\mathfrak{sl}_2\in\{1,\mathfrak{sl}_2\}$。
4. ★ $=1$ なら $\langle\tilde a,\tilde b\rangle$ は **補元** ⟹ 拡大が**分裂** ⟹ **S2-2(非分裂・§2 で証明済)に矛盾**。

$$\boxed{\ \Longrightarrow\ \langle\tilde a,\tilde b\rangle=\tilde H\quad\Longrightarrow\quad \tilde H\ (2,3)\text{-生成}\iff H_F\ (2,3)\text{-生成}\ }$$

★ **非分裂性が「持ち上げの生成性」を無料で保証する** — S2-2 の副産物です。

---

## §5 $H_F$ から $SL^\pm(2,691)$ への帰着

- **⟹**: $H_F\twoheadrightarrow SL^\pm(2,691)$ ⟹ **必要** ✔
- **⟸**: $\ker(H_F\to SL^\pm)=\{(I,\sigma):\mathrm{sgn}\sigma=1\}\cong A_3=C_3$。$(a,\alpha),(b,\beta)$ で $\alpha=$ 互換($\mathrm{sgn}=\det a=-1$)・$\beta\in A_3$。$\beta\ne1$ なら $\langle\alpha,\beta\rangle=S_3$ ⟹ Goursat で fiber product 全体を生成できる。
 ⚠ **細部**: 共通商が自明であることの確認が要る ⟹ 【S2-GAP-3】(小・機械 1 行で済む)。

$$\boxed{\ \Longrightarrow\ \textbf{決着は }SL^\pm(2,691)\ \textbf{の}(2,3)\text{-生成}\ \textbf{= 既存 GAP W6-GAP-1}\ }$$

★ **私の定理 GEN23-DET は $SL^\pm$ を排除しません**($D=\{\pm1\}$・$\lvert D\rvert=2$ **偶** ⟹ 定理の除外条件に当たらない)⟹ **陽性の見込みは残っています**。

---

## §6 ★ 副産物 — $c\in N'$ 側

$z=1$ ⟹ $B_3/N'\cong\tilde H$ なる窓があれば **$c\in N'$**。
⟹ ★ **wcp5d の「$\tau$ が $F_2/N_{F_2}$ に降りない」問題は起きません**($c\in N$ 側は実測 16/16 安全)⟹ 下流の列挙器は **(F2) 商規律の分岐が不要**になります。⟹ **設計上の朗報**。

---

## §7 次の一手(実装係へ直結・既存設計の再利用)

```
=== [S2-3-PRE] SL^±(2,691) の (2,3)-生成 目撃者探索 ===
根拠: docs/notes/F_stage2_S3_precheck_v1.md §5 / 設計 = w691_scan_gen23_spec_v1.md §3(既存・そのまま使える)
対象: H_2 = SL^±(2,691) = {det = ±1}
手順(既存設計の逐語):
  1. 候補生成(乱択・探索のみ): a = g·diag(1,-1)·g^{-1}(a^2=I・det a=-1 が構成から保証)
                               b = 位数 3 の元(det b=1・SL(2,691) 内)
  2. Size(<a,b>) = |H_2| = 659,877,360 か判定(nice monomorphism / Schreier–Sims で秒)
  3. ★ 陽性が 1 対出た時点で証明終了 ⟹ ★ braid lift の必要条件クリア
  4. 2000 対で打切り ⟹ UNKNOWN(「生成でない」とは書かない)
★ 陽性なら: S2-3 へ進んでよい(ただし §8 の残条件つき)
★ 打切りなら: Dickson 極大部分群排除で陰性主張を試みる(既存設計 §3 末尾)
u_touched=false ; c_touched=false ; prereg 非抵触(純群論)
```

---

## §8 ⚠ 残る条件(**(2,3)-生成だけでは braid lift 完了ではない**)

$(2,3)$-生成 $\Rightarrow$ $PSL(2,\mathbf Z)\twoheadrightarrow\tilde H$ ⟹ $B_3\twoheadrightarrow\tilde H$($c\mapsto1$)✔
⟹ ★ **これで braid lift 自体は完了**します(全射 $B_3\to\tilde H$ の存在)。
⚠ **ただし S2-4(所要の surjectivity)は別**: 窓の枠組みで要るのは「$B_3\to\tilde H$ が**特定の $N'$ を核とする**」ことや、$\rho$ 側との整合であって、**単なる全射の存在ではありません** ⟹ 【S2-GAP-4】。
⚠ ★ **B2 条件 2 の再掲**: いかなる結果も「**窓が arithmetic に qualification された**」ことを意味しません。**R-1 は OPEN**。

---

## §9 GAP・記帳

- **【S2-GAP-1】★ 縮小**: S2-3 は「$SL^\pm(2,691)$ の $(2,3)$-生成」1 点に帰着(既存設計あり)。
- **【S2-GAP-3】(小・新)** §5 ⟸ 向きの Goursat 細部(共通商の自明性)⟹ 機械 1 行。
- **【S2-GAP-4】(中・新)** braid lift の存在と「窓としての適格性」は別 ⟹ S2-4 の内容。
- **【W6-GAP-1】** = 本前検査の律速。⟹ ★ **優先度が上がりました**(段 2 のクリティカルパス)。
- ★ **本ノートの新規部分**: ① $Z(\tilde H)\cong C_2$ の同定 ② ★ **$p\equiv3\pmod4$ から $c\mapsto1$ が強制**されること ③ ★★ **非分裂性が持ち上げの生成性を無料で保証**し、$(2,3)$-生成が **同値**になること ④ **W6-GAP-1 への完全帰着**と既存設計の再利用 ⑤ 副産物 $c\in N'$。
- **申告**: 機械走行ゼロ(紙のみ・数値検算は sympy の legendre_symbol と位数計算のみ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
