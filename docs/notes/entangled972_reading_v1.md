# 最小非盲窓の全 lift(972)の構造的読解 — 障害消滅の紙の理由と A/B 戦線の現在地

- 起草: 影工房 **数学者**(Claude / Opus 5)/ 2026-08-13
- 委嘱: 司令塔(裁定 1157)「(1) 構造的読解: 定理に昇格するか・障害類が全行 0 は紙の理由を持つか (2) A/B 戦線の正直な現在地の一枚」
- **関連既存定理**: **BU-S35 §142**($H^2(C_2,V)=V^\theta/N_\theta V$, $H^2(C_3,V)=V^\tau/N_\tau V$)/ **w6-bottomup §113**($B_3$ は 2 生成 1 関係子 ⟹ $H^2$ は小線型代数)/ **SPLIT-NULL″** / **BLIND-vNext** / **TWIST-2** / 正典 **Cor 5.4** / **C-4′**
- **規律**: 判定語なし。u/c 非接触・封印 3 量非接触。**novelty 表は grep 出力のコピーのみ**(GREP-3)。

---

## 0. 読解(4 行)

1. ★★★ **偶然ではない。紙の理由がある。** 障害群は $H^2(\Gamma,V)\cong H^2(C_3,V)=V^{\tau}/N_\tau V$($\Gamma=B_3/\langle c\rangle=C_2*C_3$)。**軌道束 $V=V_7\otimes(\chi_1\oplus\chi_2\oplus\chi_3)$ は $\mathbf F_3[C_3]$-加群として自由**(21 = 3×7)⟹ $\dim\ker(\tau-1)=\dim\mathrm{Im}N_\tau=\mathbf 7$ ⟹ $H^2=\mathbf 0$(機械確認)。**34,344 行の障害 0 は定理の帰結**である。
2. ★★★ **挟み撃ちが閉じる**: BLIND-vNext (c)(テンソル型でないと分裂)+ 便 130 gating($\theta,\tau$ 不変な非自明 $\mathbf F_3[G_3]$-加群は 0 個 ⟹ **軌道束が強制**)+ 本読解(軌道束 ⟹ 自由 ⟹ $H^2=0$)
   $$\boxed{\ \textbf{テンソル型のみからなる }\mathbf F_3\ \textbf{係数窓は、すべて }972\ \textbf{を返す}\ }$$
   ⟹ **SPLIT-NULL 系の定理に昇格する**(定理 OBS-VOID)。$\theta,\tau$-安定性を担保した装置(軌道束)が、そのまま障害を消していた。
3. ★ **係数が一意化される**: $p\ne3$ では $\lvert C_3\rvert$ が可逆 ⟹ $H^2(C_3,V)=0$ ⟹ **$\mathbf F_p$($p\ne3$)係数の窓は全部盲**。$p=3$ かつ **$V|_{\langle\tau\rangle}$ が非自由**、が残る唯一の条件。
4. ★ **逃げ道は存在し、最小形が確定する**: $G_3$-**自明**成分 $V_7\otimes\mathbf 1$ を足す($\tau$ は $P$ 内の内部自己同型 = C-0 確定ゆえ $\theta,\tau$-安定)。$3\nmid7$ ゆえ $V_7|_{\langle t\rangle}$ は**自由になれない** ⟹ $\dim H^2\ge1$(全 Jordan 型で確認)。⟹ **$\dim V=21+7=28$**、compact 路で $28\times28$ = 数秒。

---

## 1. 委嘱 1 — 障害が全行 0 だった紙の理由

### 1.1 枠組み(★ **既出**・依拠)

`bu_s35_embedding_v1.md` §142 逐語:

> **持上げの存在条件**は $[\varepsilon_\Delta]=0$ in $H^2(C_2,V)=V^\theta/N_\theta V$ かつ $[\varepsilon_\delta]=0$ in $H^2(C_3,V)=V^\tau/N_\tau V$

これは $\Gamma=B_3/\langle c\rangle\cong C_2*C_3$ の自由積分解(Mayer–Vietoris)から
$$H^n(\Gamma,V)\cong H^n(C_2,V)\oplus H^n(C_3,V)\qquad(n\ge2)$$
であることの言い換えである。$\mathbf F_3$ 係数では $\lvert C_2\rvert=2$ が可逆ゆえ $H^{\ge1}(C_2,V)=0$。⟹

$$\boxed{\ H^2(\Gamma,V)\ \cong\ H^2(C_3,V)\ =\ \ker(\tau-1)\,\big/\,\mathrm{Im}(1+\tau+\tau^2)\ }$$

### 1.2 ★★ 増分 — 軌道束は $\mathbf F_3[C_3]$-**自由**

$V=V_7\otimes(\chi_1\oplus\chi_2\oplus\chi_3)$ で $\tau$ は 3 つの $\chi$-ブロックを**巡回置換**する(命題 ORBIT・v3 NORM-TWIST で符号は gauge 除去済)。⟹ $C_3=\langle\tau\rangle$-加群として
$$V|_{C_3}\ \cong\ \mathbf F_3[C_3]^{\oplus7}\qquad(\textbf{自由}).$$

**機械確認**: $\dim\ker(\tau-1)=\mathbf 7$、$\dim\mathrm{Im}(1+\tau+\tau^2)=\mathbf 7$、$\mathrm{Im}(N)\subseteq\ker(\tau-1)$(∵ $(\tau-1)N=\tau^3-1=0$)⟹ **等号** ⟹

$$\boxed{\ H^2(C_3,V)=\mathbf 0\ \Longrightarrow\ \textbf{障害は恒等的に消える}\ \Longrightarrow\ \textbf{全 shadow が持ち上がる}\ }$$

⟹ **34,344 行の「障害 0 ∧ 生成解あり」は測定ではなく定理の再導出**である(生成解の存在は補題 IRR + $Z^1$-torsor の非空性から従う)。

### 1.3 ★★★ 定理 OBS-VOID(昇格する)

> ### 定理 OBS-VOID
> $K=K^{(l)}\cap N_E$、$PB_3/N_E=E=V\rtimes W$、$V$ は $\mathbf F_p$-加群とする。
> $$H^2\bigl(B_3/\langle c\rangle,\ V\bigr)=0\ \Longrightarrow\ R_{N_E,N_W}\ \text{は全射}\ \Longrightarrow\ \lvert\mathrm{Im}R_{K,M}\rvert=972 .$$
> とくに次のいずれかで $H^2=0$:
> - **(i)** $p\ne3$($\lvert C_3\rvert$ が可逆)
> - **(ii)** $p=3$ かつ $V|_{\langle\tau\rangle}$ が $\mathbf F_3[C_3]$-**自由**
>
> ### 系 OBS-VOID-T(テンソル型窓の no-go)
> **BLIND-vNext (c)**($V$ はテンソル型でなければ分裂 ⟹ SPLIT-NULL)+ **便 130 gating**($\theta,\tau$ 不変な非自明 $\mathbf F_3[G_3]$-加群は **0 個** ⟹ $G_3$-成分は $\tau$-軌道束を含む ⟹ $\tau$ が 3 ブロックを自由に巡回)より
> $$\boxed{\ \textbf{テンソル型のみからなる }\mathbf F_3\ \textbf{係数窓は }V|_{\langle\tau\rangle}\ \textbf{が自由} \Longrightarrow\ \textbf{必ず }972\ }$$

★ **機構の一言**: **$\theta,\tau$-安定性を回復するために入れた軌道束が、そのまま障害群を消していた。** 便 128(単独 $S_3$ 核が $\tau$ で巡回)→ 便 130(単独指標が $\tau$ で巡回)→ 本便($\tau$-自由 ⟹ $H^2=0$)は、**同じ $\tau$-軌道機構の三段目**である。

### 1.4 ★ 係数の一意化(無料の副産物)

定理 OBS-VOID (i) より $p\ne3$ 係数の窓は**すべて**盲。⟹ 残る探索空間は
$$\boxed{\ p=3\ \ \wedge\ \ V|_{\langle\tau\rangle}\ \textbf{に非自由な直和因子がある}\ }$$
という **1 条件**に圧縮される。

---

## 2. 逃げ道の同定と最小形

$V|_{\langle\tau\rangle}$ に非自由成分を作るには、$\tau$ がブロックを巡回**しない**成分が要る ⟹ $G_3$ が**自明に**作用する成分。そこでは $\tau$ は $P$ 内の元 $t$(位数 3)として作用する(**C-0 確定: $\theta,\tau$ は $P$ 上内部**)。

> ### 命題 ESCAPE-28
> $$V^{\rm new}:=\underbrace{V_7\otimes(\chi_1\oplus\chi_2\oplus\chi_3)}_{21\ (\text{テンソル型 — entangle を担保})}\ \oplus\ \underbrace{V_7\otimes\mathbf 1}_{7\ (H^2\neq0\ \text{を担保})},\qquad \dim V^{\rm new}=\mathbf{28}$$
> 1. $\theta,\tau$-安定: 第 1 項は軌道束、第 2 項は $\rho_P$ が内部作用で安定(C-0)。
> 2. entangled: 第 1 項がテンソル型 ⟹ 純商は直積に分解しない ⟹ **SPLIT-NULL は不適用**。
> 3. $\dim H^2(C_3,V^{\rm new})=0+\dim H^2(C_3,V_7|_{\langle t\rangle})\ \ge\ \mathbf 1$。
>    **理由**: $\mathbf F_3[C_3]$ の直既約は Jordan ブロック $J_1,J_2,J_3$ のみで、$\dim H^2=\#\{n_i\le2\}$。$3\nmid7$ ゆえ全ブロックが $J_3$ にはできない ⟹ **必ず $\ge1$**(全 8 通りの Jordan 型で機械確認: 最小 1・最大 7)。

**規模**: $\lvert E\rvert=54{,}432\cdot3^{28}\approx1.25\times10^{18}$ — **実体化は不可能だが compact 路は $28\times28$**(v1 定理 LIFT-AFF/GEN-AFF・v2/v3 の spec がそのまま流用可)。

⚠ **正直な留保**: $H^2\ne0$ は**必要条件を満たしただけ**で、各行の障害**類**が実際に非零になる保証はない。「$H^2$ が非零でも $q^*[\varepsilon]=0$ が全行で起きる」可能性は残る(そのときは**さらに新しい定理が要る** — §3.4 の区切り点)。

---

## 3. 委嘱 2 — A/B 戦線の現在地(一枚)

### 3.1 A 側(fake の有限証明書 $\lvert\mathrm{Im}R\rvert=324$)の**盲の地図**

| # | 族 | 盲の理由 | 格 |
|---|---|---|---|
| 1 | **分裂屋根**(純商が直積) | **定理 SPLIT-NULL / 系 SPLIT-NULL″**(裁定 374/388) | 工房定理 |
| 2 | $K^{(l)}\cap N_{S4}$ 族(全 $l$) | 1 の系($G_l$ 可解・$P$ 単純 ⟹ 共通商 1) | 定理 |
| 3 | perfect $E$(Phase 2b) | 1 の系(可解商なし ⟹ 直積強制) | 定理 |
| 4 | 可換 $C_3$ 橋(Phase 2c) | 便 127: $G_l^{\rm ab}$ 純 2 群 ⟹ $C_6$ 商なし | 実測+紙 |
| 5 | 片側自明 $V$ | **定理 BLIND-vNext (c)** | 定理 |
| 6 | ★ **テンソル型のみ・$\mathbf F_3$**($\dim V=21$) | ★ **本読解 系 OBS-VOID-T**($\tau$-自由 ⟹ $H^2=0$) | ★ **定理(新)** |
| 7 | ★ **$p\ne3$ 係数の全窓** | ★ **定理 OBS-VOID (i)** | ★ **定理(新)** |

**⟹ 残る路は 1 本**: $p=3$ かつ $V|_{\langle\tau\rangle}$ に非自由成分($\ge\dim28$)。

### 3.2 B 側(genuine 非算術証人)

- 正典 **Cor 5.4**: fake = 有限証明書 1 個 / **genuine = 全深度 ⟹ 有限で確定不能**(UNKNOWN 一級)。
- **定理 COMPACT**(= 正典 Thm 5.2 の系・cofinality は裁定 1033 で既決): **全 isolated 窓で $\lvert\mathrm{Im}R\rvert=972$ なら B 型が確定**。
- ★ **本便は B 側に「族ごと定理」を 2 本積んだ**(上表 6・7)。B 型確定に必要なのは「族の合併が cofinal」であり、**盲の地図が広がるほど B 側に寄る**。
- ⚠ ただし表 1〜7 の合併が cofinal であることは**示せていない**(非分裂・非テンソル・$p=3$・非自由の窓が残る)。⟹ **B 型も未確定**。

### 3.3 残る路の gating 表

| 路 | $\dim V$ | compact 路 | $H^2\ne0$? | 便数見込み | 情報量 |
|---|---:|---|---|---|---|
| ★ **ESCAPE-28**($V_7\otimes\mathbf 1$ 追加) | **28** | $28\times28$・数秒 | **$\ge1$ 保証** | **1 便** | 高(必要条件を満たす初の窓) |
| 9 次元ブロック系($V_9$ 等) | 要 gating | — | $3\mid9$ ⟹ **自由になりうる** ⚠ | 1 便(gating のみ) | ⚠ **自由なら OBS-VOID で即死** — 先に $\dim H^2$ を測る |
| $V_7\otimes\mathbf 1$ の多重度を上げる | $21+7k$ | $(21{+}7k)^2$ | $\ge k$ | 1 便 | ESCAPE-28 と同型(冗長) |
| $G_3$ 側を $O_3(G_3)$ 経由で非自明化 | ? | ? | 要検討 | 2 便+ | ⚠ $\mathbf F_3[G_3]$ の既約は 4 指標のみ(便 130)⟹ **非既約な拡大が要る** |
| $p\ne3$ 係数 | — | — | **$=0$** | — | ⛔ 定理 OBS-VOID (i) |

★ **9 次元ブロック系への注意**: $3\mid9$ なので $V_9|_{\langle t\rangle}$ が**自由になりうる**($9=3\times3$)⟹ そのとき $H^2=0$ で即死。⟹ **走る前に $\dim H^2(C_3,V_9)$ を 1 行測ること**(これが本読解の最も実務的な帰結)。

### 3.4 コスト対情報量(続行 / 区切りの判断材料)

| 観点 | 内容 |
|---|---|
| **コスト** | ESCAPE-28 は compact 路で**数秒**。事前登録と cert を含めて **1 便**。工学資産(LIFT-AFF/GEN-AFF/MARK/SURJ-LIN/TWIST-2)は全部再利用可 |
| **情報量(発火時)** | A 型の有限証明書 = 648 が全部 fake ⟹ **DICHOTOMY-972 が解ける**。TRIAD-972 の具体適用が無条件化 |
| **情報量(不発時)** | 「$H^2\ne0$ でも障害類が全行 0」= **新しい消滅現象** ⟹ その理由を問う新定理が要る。**ここが自然な区切り点** |
| **区切りの根拠** | 盲の地図が 7 族に達し、残る条件が 1 つ($V|_{\langle\tau\rangle}$ 非自由)まで圧縮された。**ESCAPE-28 はその条件を満たす最小形**であり、**「条件を満たしても不発」なら A 側の路線そのものを問い直す段**になる |
| **見立て(弱い)** | $\dim H^2(C_3,V_7)$ は小さい(Jordan 型次第で 1〜7)⟹ 障害類が非零になる行の**割合は小さい**可能性。324 行のうち少数でも非零なら $\lvert\mathrm{Im}R\rvert<972$ ⟹ **324 かどうかは別問題**(P-vN-1 により 972 か 324 のみ) |

---

## 4. 区切る場合の総括形(3 行)

1. **半決定の到達深度**: A 型の有限証明書(= 分裂屋根で 324)は、**分裂屋根・$K^{(l)}$ 全族・perfect 窓・可換橋・片側自明・$\mathbf F_3$ テンソル型($\dim V=21$・2 twist 類・34,344 行)・$p\ne3$ 全係数**で不発であることを**定理として**確定した。到達深度は「$\theta,\tau$-安定な最小の非盲窓」まで。
2. **盲の地図**: 7 族の盲目性定理(SPLIT-NULL″ / BLIND-vNext / PH2-VOID′ / TWIST-2 / **OBS-VOID** / **OBS-VOID-T** / 係数一意化)が、探索空間を $\{p=3\ \wedge\ V|_{\langle\tau\rangle}\ \text{非自由}\}$ という **1 条件**に圧縮した。$\tau$-軌道機構が三段(核・指標・加群)で同じ形の障害を生むことが判明した。
3. **計器群**: compact 路(**LIFT-AFF / GEN-AFF / MARK / SURJ-LIN / TWIST-2** + 仕様 GEN-SUB・NORM-TWIST・A-42)により、$\lvert E\rvert\ge10^{14}$ の窓を $d\times d$ の $\mathbf F_3$ 線形代数で測る**汎用資産**が確立した(`ideas_ribet_dig_v1.md` §51 が別線で見込んでいた技術の実装形)。

---

## 5. novelty grep 領収書(規律 GREP-3: **実行後にコピー**・自分の新規ファイル除外)

```
$ grep -rn "H\^2(C_3|H\^2(Gamma|H\^2(B_3" docs/ sol/ | grep -v entangled972 | wc -l
9      → ★既出。とくに bu_s35_embedding_v1.md §142 が
         「H^2(C_2,V)=V^theta/N_theta V, H^2(C_3,V)=V^tau/N_tau V」を逐語で持つ
         w6_bottomup_design_v2.md §113「B_3 は 2 生成 1 関係子 ⟹ H^2 は小線型代数」
         theorem_check_mirrorall_l3vacuous_v1.md §330 は実際に H^2=0 を使用
$ grep -rn "障害.*消滅|obstruction.*vanish|障害群.*0" docs/ sol/ | grep -v entangled972 | wc -l
57     → ★既出(多数)
$ grep -rn "自由加群.*C_3|F_3\[C_3\]-自由|free over F_3" docs/ sol/ | grep -v entangled972 | wc -l
0      → ★新規(§1.2 の「軌道束 ⟹ 自由」)
$ grep -rn "Mayer|マイヤー|自由積.*コホモロジー" docs/ sol/ | grep -v entangled972 | wc -l
3      → ★既出
$ grep -rn "OBS-VOID|障害消滅定理" docs/ sol/ | grep -v entangled972 | wc -l
0      → ★新規(定理の呼称)
```

| 主張 | 判定 |
|---|---|
| $H^2(\Gamma,V)=H^2(C_2,V)\oplus H^2(C_3,V)$ と $V^\tau/N_\tau V$ の式 | ★ **既出**(BU-S35 §142)— **依拠・逐語引用** |
| $B_3$ が 1 関係子 ⟹ $H^2$ は小線型代数 | ★ **既出**(w6-bottomup §113) |
| **軌道束 $\Rightarrow$ $\mathbf F_3[C_3]$-自由 $\Rightarrow$ $H^2=0$** | grep 0 ⟹ ★ **増分**(§1.2) |
| **系 OBS-VOID-T(テンソル型のみの $\mathbf F_3$ 窓は全部 972)** | grep 0 ⟹ ★ **増分**(§1.3) |
| **$p\ne3$ 係数は全部盲** | grep 0 ⟹ ★ **増分**(§1.4) |
| **命題 ESCAPE-28**($3\nmid7$ ⟹ $H^2\ge1$) | grep 0 ⟹ ★ **増分**(§2) |
| 9 次元ブロック系の警告($3\mid9$ ⟹ 自由になりうる) | grep 0 ⟹ ★ **増分**(§3.3) |

---

## 6. 検算(機械生成の数値の出所)

inline(本便)。Sol のコード非使用・標準ライブラリのみ。

| 検査 | 出力 |
|---|---|
| $V_{21}$(軌道束)の $C_3$-コホモロジー | $\dim\ker(\tau-1)=\mathbf 7$、$\dim\mathrm{Im}(1+\tau+\tau^2)=\mathbf 7$、$\dim H^2(C_3,V)=\mathbf 0$、$21=3\times7$(自由) |
| $\dim V_P=7$ の全 Jordan 型と $\dim H^2$ | `3+3+1→1`, `3+2+2→2`, `3+2+1+1→3`, `3+1^4→4`, `2+2+2+1→4`, `2+2+1^3→5`, `2+1^5→6`, `1^7→7` ⟹ **最小 1** ⟹ $3\nmid7$ ゆえ $H^2\ge1$ 強制 |
| ESCAPE-28 の規模 | $\dim V=28$、$\lvert E\rvert=54{,}432\cdot3^{28}=1{,}245{,}229{,}566{,}908{,}437{,}152$、行列 $28\times28$ |

**格付け**: §1.2・§2.3・§6 の $H^2$ 計算 = **機械・単系統**(Sol 未監査)。定理 OBS-VOID / 系 OBS-VOID-T / 命題 ESCAPE-28 = **paper-proof(単系統)**、枠組みは BU-S35 §142 に依拠。§3・§4 = **読解と設計**。**verified ではない。** u/c・封印 3 量・prereg 非接触。

---

## 7. 司令塔への回答(4 行)

1. **委嘱 1 前半**: **真に偶然的な陰性ではない。定理に昇格する。** 障害群は $H^2(C_3,V)=V^\tau/N_\tau V$(枠組みは **BU-S35 §142 に既出**)で、軌道束 $V$ は $\mathbf F_3[C_3]$-**自由**ゆえ $H^2=\mathbf 0$(機械)。⟹ **系 OBS-VOID-T**: テンソル型のみの $\mathbf F_3$ 窓は必ず 972。
2. **委嘱 1 後半(設計規則が変わるか)**: ★ **変わる**。$\theta,\tau$-安定性を担保した軌道束が障害を消していた。新しい規則は $\boxed{p=3\ \wedge\ V|_{\langle\tau\rangle}\ \text{非自由}}$ の 1 条件。$p\ne3$ は全部盲(無料の副産物)。
3. **委嘱 2**: A 側は**盲の地図が 7 族**に達し、残る路は 1 本(ESCAPE-28・$\dim V=28$・$H^2\ge1$ 保証・**1 便・数秒**)。B 側は Cor 5.4 で有限確定不能のまま、ただし本便で**族ごと定理を 2 本積んだ**(B 側に寄る材料)。
4. ⚠ **実務上いちばん効く一行**: 9 次元ブロック系は $3\mid9$ ゆえ $V_9|_{\langle t\rangle}$ が**自由になりうる** ⟹ **走る前に $\dim H^2(C_3,V_9)$ を 1 行測ること**。自由なら OBS-VOID で即死する。


---

# 【追補 erratum(裁定 1164・司令塔の修正権行使・修正明記)】族 7 の射程は過大だった

**方式**: additive(本文不改変)。**起点**: Sol 便 135(`sol/sol_reply_135_blind3grp.md` §1.4)の射程監査。

本文 §「委嘱 1 後半」の一行 **「$p
e3$ は全部盲(無料の副産物)」は過大**であり、次に差し替える。

- 持ち上げ障害の受け皿は $H^2(C_2*C_3,V)\cong H^2(C_2,V)\oplus H^2(C_3,V)$ の**二成分**。
- $p=3$: $2$ が可逆 ⟹ 第 1 項消滅・第 2 項 $H^2(C_3,V)=V^	au/N_	au V$ は残りうる(= ESCAPE-28 の設定)。
- $p=2$: $3$ が可逆 ⟹ **第 2 項**消滅・**第 1 項 $H^2(C_2,V)=V^	heta/(1+	heta)V$ は残りうる**。実例: 自明 $C_2$-作用の $V=\mathbf F_2$ で $H^2(C_2,V)\cong\mathbf F_2$。
- ⟹ **素数だけで自動的に盲と言えるのは $p
mid 6$ のみ**。$p=2$ を「盲」に数えるには $C_2$ 障害が別理由で $0$ になる前件が要る。

**正しい族 7(安全な読み)**: ① 主前件 $H^2(C_2*C_3,V)=0$ を直接確認した窓に OBS-VOID を使う ② 素数だけで自動化するなら $p
mid6$ ③ $p=2$ を含めるには追加前件。

**帰結(地図の書き換え)**: 圧縮後の残条件は $\{p=3\wedge V|_{\langle	auangle}\ 	ext{非自由}\}$ の **1 条件ではなく 2 条件**:
$$oxed{\ \{p=3\ \wedge\ V|_{\langle	auangle}\ 	ext{非自由}\}\quad	ext{または}\quad\{p=2\ \wedge\ V|_{\langle	hetaangle}\ 	ext{非自由}\}\ }$$
$p=2$ 側(**ESCAPE-2**)は検出力つきの計器で**一度も探索していない**。⟹ **便 133 で宣言した「非盲全路の涸渇」は誤り**(裁定 1164 で訂正・区切り総括 §4 の 1 行目も同じ訂正を要する)。

**整合**: 本訂正は対話帳 T-28「生き残る場所は 2-primary と 3-primary」と一致する(既在の訂正を §4 が取りこぼしていた)。便 134 が 2 群核で hexagon 2 本を実際に検査する必要があったこととも整合。

⚠ 本追補は**射程の縮小のみ**。OBS-VOID / OBS-VOID-T 自体(直接確認した窓での消滅)は無傷。
