# COFIN-CERT 草案 v1.1 — 公平 shell 累積梯子の cofinality と「3 つの cofinal」の層分離

`DIR: 正側(証人型の第一証明物)/ FRAME: B₃-gentle・972 屋根`
**格**: §3–§6 の定理 = `paper-proof(自前)`。**§4.5(Prop 3.15 の工房証明)は原文に証明が無いため必須**。§7 の MEAS 訂正 = 確定。§8 は **v1 から全面差し替え(撤回)**。
**著者**: 数学者(Opus 5)/ 2026-08-26。**v1(sha16 `7700c05461946374`)は改変せず並置。本 v1.1 が v1 を supersede する。**

> ### v1 からの変更(falsifier 審査 + reader 原文照合の反映)
> | # | 内容 | 種別 |
> |---|---|---|
> | **V-1** | **記号の全面統一**: 正典 2401 (1.4)/(3.60) に合わせ **$\mathrm{NFI}_{PB_3}(B_3)$**(v1 は $NFI_{B_3}(PB_3)$ と逆)・**$R_{N,H}:GT(N)\to GT(H)$($N\le H$・source-first)**(v1 は $R_{M,K}$ で target-first)。**CV-9 級の記号衝突として全文書に波及**(§9) | 致命傷・訂正 |
> | **V-2** | DROP-FREE の定理文に **$K\le M$** を明記(v1 は欠落 — $R_{K,M}$ は $K\le M$ でのみ定義) | 致命傷・訂正 |
> | **V-3** | v1 §8-2「閉形式路線は原理的に塞がった」を **撤回**。格を **UNKNOWN** に戻す | 致命傷・撤回 |
> | **V-4** | (C-1)⇏(C-2) の理由づけを差し替え(v1 の「$\Lambda$ 一定 ⟹ $\bigcap K_n\ne1$」は**偽**)。正しくは **COF-Λ の $d=3$ 適用** | 訂正 |
> | **V-5** | DROP-FREE を **[2401] Cor 5.4 の実務系**に降格。$K^\diamond$ 経由の証明を撤去し 3 行に | novelty 降格 |
> | **V-6** | **費用対殺傷力のトレードオフ表**を新設(§9.2)。**配分の決定はしない** | 追加 |
> | **V-7** | **Prop 3.15 の工房証明を収録**(原文は "leave it to the reader" で証明なし・reader 実測) | 追加(必須) |
> | **V-8** | 連結成分の有限性は**正典が直接与える**(§3.2 冒頭・イントロ)⟹ 私の Prop 3.8+M. Hall 補完は**別証**に格下げ | 訂正 |
> | **V-9** | (C-1) の pin を **Prop 3.14 直後の無番号段落**へ精密化(逐語収録) | 精密化 |

---

## §1 正典からの引用(pin・逐語)

すべて `papers/txt/2401.06870-gt-shadows-gentle-version.txt` から。

- **(1.4)**: $\mathrm{NFI}_{PB_3}(B_3):=\{N\trianglelefteq B_3\mid [B_3:N]<\infty,\ N\le PB_3\}$。
- **(1.8) = (3.60)**: $N\le H$ に対し $R_{N,H}:GT(N)\to GT(H)$。**source が第 1 添字**。
- **連結成分の有限性(イントロ・逐語)**: "the connected component $\mathrm{GTSh}^{\rm conn}(N)$ of an object $N\in\mathrm{NFI}_{PB_3}(B_3)$ is **always a finite groupoid**"。
- **(C-1) の所在(Prop 3.14 直後の無番号段落・逐語)**: "the subposet $\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)\subset\mathrm{NFI}_{PB_3}(B_3)$ of isolated objects of GTSh is **cofinal**, i.e., for every $N\in\mathrm{NFI}_{PB_3}(B_3)$, there exists $\tilde N\in\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$ such that $\tilde N\le N$. More precisely, due to **Proposition 3.14**, for every $N$, the intersection of all objects of $\mathrm{GTSh}^{\rm conn}(N)$ is an isolated object $N^\diamond$ of GTSh such that $N^\diamond\le N$."
- **[2401] Cor 5.4(逐語)**: "a GT-shadow $[m,f]\in GT(H)$ is **genuine if and only if** $[m,f]$ belongs to the image of the reduction map $R_{N,H}:GT(N)\to GT(H)$ **for every $N\in\mathrm{NFI}_{PB_3}(B_3)$ such that $N\le H$**"。**fake 版(同段落)**: "$[m,f]$ is **fake if and only if there exists** $N\in\mathrm{NFI}_{PB_3}(B_3)$ such that $N\le H$ and $[m,f]$ does not belong to the image of $R_{N,H}$"。

> ⚠ **論文タグ義務(二重命名)**: **[2401] Cor 5.4** = genuine 判定条件(上記)。**[2405] Cor 5.4** = 2 冪 dihedral の結果。**別物**。以後、Cor 5.4 は必ず論文タグつきで引用する。

---

## §2 層の分離 — 同じ「cofinal」が 3 つある

| 札 | 主張 | 格 | 典拠 |
|---|---|---|---|
| **(C-1)** 抽象 cofinality | $\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$ は $\mathrm{NFI}_{PB_3}(B_3)$ で **cofinal**($\forall N\ \exists\tilde N\le N$ isolated) | **定理** | **Prop 3.14 直後の無番号段落**(§1 逐語)+ Prop 3.14 |
| **(C-2)** 鎖の cofinality | **特定の**入れ子鎖 $K_0\supsetneq K_1\supsetneq\cdots$ が cofinal | **§3/§4 で定理化** | 本稿 |
| **(C-3)** 機構の一様性 | その鎖の**全段**で $I_{K_n}=X$(落下しない) | **UNKNOWN** | — |

**(C-1) ⟹ (C-2) は成り立たない。** 実例: **Dih×$N_{S4}$ 系の鎖**は各段 isolated だが $\Lambda_{K_n}=2\mathbb Z^2$ が $n$ に依らず一定(`d972` §12.2-3 実測)。

> ### ⚠ V-4:非 cofinal 性の**正しい**理由づけ(v1 の理由は偽)
> **v1 の誤り**: 「cofinal なら $\bigcap K_n=1$ で $\Lambda$ は必ず細る」— **偽**。falsifier の反例:
> $$K_n=\ker(F_2\to Q_8)\cap\bigcap_{i\le n}\ker(F_2\to\mathrm{PSL}(2,p_i))$$
> は $Q_8^{\rm ab}=C_2^2$ と PSL の完全性+Goursat により**全 $n$ で $\Lambda_{K_n}=2\mathbb Z^2$ 一定**、かつ Sanov 部分群の mod $p$ 分離により $\bigcap_nK_n=1$($p=5,7,11,13$ で全射 4/4 数値確認済)。⟹ 「$\bigcap K_n=1$」から「$\Lambda$ が細る」は**出ない**。
> **正しい理由づけ(COF-Λ の $d=3$ 適用)**: §5 の系 COF-Λ より、cofinal なら**ある $n$ で $\Lambda_{K_n}\subseteq3\mathbb Z^2$**。ところが $2\mathbb Z^2\not\subseteq3\mathbb Z^2$($(2,0)$ が反例)。⟹ $\Lambda\equiv2\mathbb Z^2$ の鎖は **cofinal でない**。∎
> **結論(cofinal でない)は不変・理由だけ差し替え。** 同じ非導出が `d972` §12.2-3 の括弧書きにもある ⟹ 同ファイルへ訂正追記(§9.3)。

**MEAS が要るもの**: Haar(M1–M3)= **(C-1) のみ**(定理)。乗法公式 M6 = **(C-2)**。正枝(MEAS-N2)= **(C-2)+(C-3)**。

---

## §3 定理 COFIN-1 — Sol §21.5 の梯子は cofinal

**構成**: $B_3$ の有限指数部分群を index shell 順(同一 index 内は canonical digest 順)に**公平に**列挙し $L_1,L_2,\dots$。
$$H_i:=M\cap\mathrm{Core}_{B_3}(L_i),\qquad J_i:=H_i^{\diamond},\qquad K_0:=M,\quad K_n:=K_{n-1}\cap J_n .$$

> ### 定理 COFIN-1
> 前件: **(F1)** 列挙が公平(各 index shell を有限時間で尽くし欠番なし)/ **(F2)** $M$ は isolated(工房実測・裁定 1133)/ **(F3)** Prop 3.14・**Prop 3.15**(§4.5 の工房証明)/ **(F4)** 連結成分の有限性(正典イントロ・§1 逐語)。
> このとき $\{K_n\}$ は **(i)** 入れ子、**(ii)** 各段 isolated かつ $K_n\in\mathrm{NFI}_{PB_3}(B_3)$、**(iii)** **cofinal**、**(iv)** $\bigcap_nK_n=1$。

**証明.**
**(i)** 定義から。
**(ii)** $\mathrm{Core}_{B_3}(L_i)$ は有限指数の $B_3$-正規部分群、$H_i=M\cap\mathrm{Core}_{B_3}(L_i)\in\mathrm{NFI}_{PB_3}(B_3)$。$\mathrm{GTSh}^{\rm conn}(H_i)$ は**有限**(F4・正典が直接与える)ゆえ $J_i=H_i^\diamond$ は有限個の窓の交わりで、有限指数・$B_3$-正規。Prop 3.14 より $J_i$ は isolated。$K_0=M$ isolated(F2)、**Prop 3.15**(§4.5)と帰納法で全 $K_n$ が isolated。
**(iii)** $N\in\mathrm{NFI}_{PB_3}(B_3)$ を任意に取る。$[B_3:N]<\infty$((1.4) より $N\trianglelefteq B_3$)ゆえ (F1) の公平列挙に現れる: $L_i=N$。$N$ は $B_3$-正規だから $\mathrm{Core}_{B_3}(N)=N$、よって
$$K_i\ \subseteq\ J_i\ =\ (M\cap N)^{\diamond}\ \subseteq\ M\cap N\ \subseteq\ N,$$
(i) より $n\ge i$ でも。
**(iv)** $1\ne w\in PB_3$ を取る。$PB_3$ は剰余有限ゆえ $w\notin N_0$ なる有限指数 $N_0\le PB_3$ がある。$N:=\mathrm{Core}_{B_3}(N_0)$ は有限指数・$B_3$-正規で $N\subseteq N_0$ ⟹ $w\notin N$。(iii) よりある $n$ で $K_n\subseteq N$ ⟹ $w\notin K_n$。∎

> ### ⚠ V-8/[B] 精密化 — Prop 3.14 は cofinality には効かない
> 証明の実質は **(a) 目標窓自身が列挙に現れる(公平性)/ (b) $J_i\subseteq N$($\diamond$ は下がるだけ)/ (c) 累積は単調**。**Prop 3.14 が効くのは (ii)(各段 isolated)であって (iii)(cofinality)ではない。** また $J_i$ の有限指数性 = **梯子の well-defined 性**は連結成分の有限性(F4)から来る。Sol §21.5 の「Prop 3.14 の isolated subposet cofinality により cofinal」という言い回しは**結論は正しいが (C-1) と (C-2) を混ぜている** ⟹ cert の文言はこの書き分けを反映せよ。
> **v1 で私が付けた「Prop 3.8 + M. Hall による連結成分有限性の補完」は不要**(正典が直接与える)。**別証として残すのは可、依拠先は正典**。

---

## §4 定理 COFIN-2(合同核版)と Prop 3.15 の工房証明

### 4.1 定理 COFIN-2

$$\Delta_n:=\bigcap\{\,N\in\mathrm{NFI}_{PB_3}(B_3)\ :\ [PB_3:N]\le n\,\},\qquad K_0:=M,\quad K_n:=K_{n-1}\cap\bigl(M\cap\Delta_n\bigr)^{\diamond}.$$

> **定理 COFIN-2.** $\Delta_n\in\mathrm{NFI}_{PB_3}(B_3)$。$\{K_n\}$ は入れ子・各段 isolated・**cofinal**。
> **証明.** $PB_3$ は**有限生成**($B_3$ が 2 元生成・$[B_3:PB_3]=6$ ⟹ Reidemeister–Schreier で有限生成)ゆえ **M. Hall** により指数 $\le n$ の部分群は有限個 ⟹ $\Delta_n$ は有限交わりで有限指数・$B_3$-正規。$[PB_3:N]=m$ なる $N$ に対し $K_m\subseteq\Delta_m\subseteq N$ ⟹ cofinal。isolated 性は Prop 3.14 + Prop 3.15(§4.5)。∎

### 4.2 比較

| | COFIN-1(Sol) | COFIN-2(合同核) |
|---|---|---|
| cofinality の証明 | 公平性の定式化に依存(欠番なしが不変条件) | **構成から自明** |
| 実装コスト | LINS で shell ごと | 同じ LINS 列挙 |
| 1 段の窓の重さ | $J_i$ 1 本 ⟹ 軽い | 指数 $\le n$ の**全部の交わり** ⟹ 重い |
| 証明書の脆さ | 公平性が抜けると cofinality が落ちる | 落ちない |

⟹ **実装は COFIN-1、証明書の文言は COFIN-2 を上界見本として併記**。公平性は cert の不変条件(`shell_index_cursor` 単調・欠番なし)。

### 4.3 ★ V-7 — Prop 3.15 の工房証明(**原文に証明なし**)

> **reader 原文照合**: 2401 の Prop 3.15 は本文に証明がなく "leave it to the reader" とされている。COFIN-1/2 がこれに依拠する以上、工房側で証明を持つ必要がある。

> ### 命題 3.15(isolated の有限交叉閉性)
> $K,L\in\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$ ならば $N:=K\cap L$ も isolated。

**証明.** $[m,f]\in GT(N)$ を任意に取り $S:=\ker(T_{m,f})$ とおく。示すべきは $S=N$(= 全 shadow が settled = $N$ isolated)。
1. $T_{m,f}:PB_3\to PB_3/N$ は**全射**(Def 3.7 の onto 条件・Prop 3.6)ゆえ $[PB_3:S]=[PB_3:N]<\infty$。
2. $N\le K$ より (3.60) の $R_{N,K}:GT(N)\to GT(K)$ が定義され、$R_{N,K}[m,f]=[m,\,fK_{F_2}]$。その構造射は $PB_3\to PB_3/K$、$\sigma_1\mapsto\sigma_1^{2m+1}K$、$\sigma_2\mapsto f^{-1}\sigma_2^{2m+1}fK$ で、これは合成 $\mathrm{pr}_{N\to K}\circ T_{m,f}$ に等しい。ゆえに
$$\ker\bigl(T_{R_{N,K}[m,f]}\bigr)=T_{m,f}^{-1}(K/N)\ \supseteq\ S .$$
3. $K$ は isolated ゆえ左辺は $K$。よって $S\subseteq K$。同様に $S\subseteq L$。⟹ $S\subseteq K\cap L=N$。
4. 1 と 3 より $S\subseteq N$ かつ $[PB_3:S]=[PB_3:N]<\infty$ ⟹ **$S=N$**。∎

**系**: $\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$ は有限交叉で閉じ、(C-1) と合わせて**下向き有向**。⟹ MEAS の M1(有向性)の前件が閉じる。

⚠ **使った前件**: (3.60) の well-defined 性(Prop 3.12)・onto 条件(Def 3.7/Prop 3.6)・isolated の定義(連結成分の対象が 1 個 ⟺ 全 shadow が settled;GTSh は groupoid ゆえ入る射と出る射は逆射で対応)。**いずれも正典。新しい仮定は使っていない。**

---

## §5 系 COF-Λ

> ### 系 COF-Λ
> $\{K_n\}$ が cofinal なら、任意の $d\ge1$ に対しある $n$ で $\Lambda_{K_n}\subseteq d\mathbb Z^2$($\Lambda_K$ = $K_{F_2}$ の $F_2^{\rm ab}=\mathbb Z^2$ における像)。
> **証明.** $V_d:=PB_3^{\,d}[PB_3,PB_3]$ は verbal ⟹ $PB_3$ で特性 ⟹ $B_3$-正規、指数有限 ⟹ $V_d\in\mathrm{NFI}_{PB_3}(B_3)$。cofinality より $K_n\subseteq V_d$ なる $n$ があり、$V_d$ の $F_2^{\rm ab}$ における像は $d\mathbb Z^2$ に含まれる。∎

**用途(§2 の V-4)**: $d=3$ を取れば $\Lambda\equiv2\mathbb Z^2$ の鎖の非 cofinal 性が出る。
**★ COF-Λ が禁じるのは「cofinal ∧ $\Lambda$ 一定」の同時成立のみ**(§8 参照)。

---

## §6 非対称の定理化

記号: $M$ = 972 窓、$X=GT(M)$、$A=\mathrm{Im}(\mathrm{Ih}_M)$、$X^{\rm st}$ = genuine 全体、$g^\ast$ = row 36 $\in X\setminus A$(c′ 非依存)。前件 = DICHOT-972 の P-i-a/b/d・P-ii・P-iii($[X:A]=3$)・P-iv(**[2401] Cor 5.4**)・P-v(Thm 5.2)。

### 6.1 定理 ASYM

| 枝 | 結論 | 必要な前件 | 量化 |
|---|---|---|---|
| **落下** $\exists K\le M:\ g^\ast\notin\mathrm{im}(R_{K,M})$ | $X^{\rm st}=A$ ⟹ **648 は全て fake** | **(C-1) すら不要**([2401] Cor 5.4 + $M$ isolated) | $\exists$(有限で証明可能) |
| **非落下** $\forall K\le M:\ I_K=X$ | $X^{\rm st}=X$ ⟹ 648 は genuine 非算術証人 | (C-1)+**(C-2)**+**(C-3)** | $\forall$(無限) |

### 6.2 系 DROP-FREE(**V-5: [2401] Cor 5.4 の実務系**)

> **系 DROP-FREE.** $K\in\mathrm{NFI}_{PB_3}(B_3)$ で **$K\le M$**(← V-2)とする。$g^\ast\notin\mathrm{im}\bigl(R_{K,M}:GT(K)\to GT(M)\bigr)$ ならば $X^{\rm st}=A$、すなわち $X\setminus A$ の 648 元はすべて非 genuine(gentle-fake)。
> **$K$ は isolated でなくてよい・入れ子でなくてよい・cofinal 族の一部でなくてよい。**

**証明(3 行).**
1. **[2401] Cor 5.4**(§1 逐語の fake 版)より $g^\ast$ は fake、すなわち非 genuine ⟹ $g^\ast\notin X^{\rm st}$。
2. $M$ は isolated(P-i-a/b + Thm 5.2)ゆえ $X^{\rm st}$ は $X$ の部分群で、P-ii より $A\subseteq X^{\rm st}$。
3. $[X:A]=3$ は素数ゆえ $X^{\rm st}\in\{A,X\}$。$g^\ast\notin X^{\rm st}$ から $X^{\rm st}=A$。∎

> **格 = 「[2401] Cor 5.4 の実務系」(novelty なし)。** Cor 5.4 の fake 版は $N\le H$ の**任意**の窓について述べており、isolated を要求していない。**v1 の $K^\diamond$ 経由の証明は不要 — 撤去した。**
> **含意は残す(価値あり)**: **落下狩りに $\diamond$ 閉包は不要** ⟹ Sol の first missing datum `RUNG-LADDER-ISOLATED-JOIN-QUOTIENT-...` は**落下狩りには不要**。非入れ子・非 isolated の在庫窓がそのまま弾になる。**ただし $K\le M$ は必須**(§9.2 の ⚠)。

### 6.3 補題 MONO(殺傷力の単調性・§9.2 の根拠)

> $K'\le K\le M$ ならば $\mathrm{im}(R_{K',M})\subseteq\mathrm{im}(R_{K,M})$。ゆえに **$K$ で落下すれば $K'$ でも落下する**(逆は不成立)。
> **証明.** 関手性 $R_{K',M}=R_{K,M}\circ R_{K',K}$(P-i-d)。∎

⟹ **殺傷力は窓の細かさについて単調増加**(定理)。コストも単調増加(§9.2)。

---

## §7 定理 DECIDE-972

> COFIN-1(または COFIN-2)の梯子の下で: **(a)** $X^{\rm st}=A$ なら**ある有限段で $I_{K_{n_0}}=A$ が観測される**。**(b)** $X^{\rm st}=X$ なら有限の証明書は出ない。
> ⟹ **fake は半決定可能、証人は(この手続きでは)半決定可能でない**。

**証明.** cofinality より $\bigcap_nI_{K_n}=X^{\rm st}$。$(I_{K_n})$ は有限群 $X$ の部分群の減少列ゆえ有限段で停留し、停留値が $X^{\rm st}$。各段の判定は $g^\ast$ の raw fibre の有限悉皆。∎
**注**: 停留は $[X:A]=3$ と DICHOT (5)(落下高々 1 回)からも直ちに。⟹ **梯子は高々 1 回しか状態を変えない有限状態機械**で、**停止するのは fake のときだけ**。
⚠ **実務上の留保**: 半決定可能性は原理の言明。各段のコストは上に有界でない。

---

## §8 ★ V-3 — v1 §8-2 の撤回(閉形式路線は **UNKNOWN** に戻す)

> ### 撤回する v1 の記述(逐語)
> 「系 COF-Λ より、cofinal な梯子では $\Lambda$ が必ず細る ⟹ **`RUNG-UNIF` の閉形式は必ず死ぬ**。⟹ **(C-3) を閉形式の一様性で証明する道は原理的に塞がっている**。」
> **⟹ 全面撤回。非導出であった。**

**撤回の理由(falsifier 指摘・2 点)**:

1. **2 自由度の見落とし**。charming 条件は $f N_{F_2}\in[F_2/N_{F_2},F_2/N_{F_2}]$、すなわち $\mathrm{ab}(f)\in\Lambda_K$。閉形式族 $f=f_\nu w=y^{\nu}x^{-\nu}w$ では
$$\mathrm{ab}(f_\nu w)=(-\nu,\nu)+\mathrm{ab}(w)\ \in\ \Lambda_K$$
であり、**$(\nu,w)$ の 2 自由度がある**。$\Lambda_K\subseteq d\mathbb Z^2$ でも $\mathrm{ab}(w)$ を選び直せば満たしうる。`d972` §12.5 が殺したのは **$\nu=2,\ w=1$ に固定した厳密族**だけであって、閉形式路線一般ではない。
2. **範疇違い**。`RUNG-UNIF` は特定塔 $K^{(q_n)}\cap N_{S4}$ についての定理であり、**公平 shell 梯子の上では未定義**。異なる梯子へ結論を移植していた。

**COF-Λ が実際に禁じるもの(正しい射程)**: 「**cofinal かつ $\Lambda$ が一定**」の同時成立のみ(§5)。cofinal 梯子上で閉形式族が生き残るか死ぬかは **UNKNOWN**。

> **格の回復**: **(C-3) を閉形式の一様性で攻める路線は `UNKNOWN`(候補として生きている)。**
> 証明したいなら **falsifier の 2 自由度論点を正面から潰す**必要がある — すなわち「$\Lambda_{K_n}$ が細り続けるとき、$(\nu_n,w_n)$ を段ごとに選び直しても **hexagon (3.10)(3.11) と onto を同時に満たし続けることはできない**」を示すこと。**本稿はこれを証明していない。推測もしない。**

**§8 の帰結として、v1 §8-3「(C-3) への現実的な道は障害の関手性 1 本だけ」も過大 ⟹ 「障害の関手性は**有力な**一路線、閉形式路線も**未決のまま生存**」に訂正。**

---

## §9 MEAS/DICHOT への波及と実務

### 9.1 MEAS への訂正(v1 §7 を維持・V-1 を追加)

| # | 記述 | 判定 | 訂正 |
|---|---|---|---|
| **X-1** | 「(P-ISO) = UNKNOWN」 | ❌ 撤回 | (C-1) は定理(§1 の逐語 pin) |
| **X-2** | 「MEAS 全体がこの前件に載る」 | ⚠ 過大 | Haar は **(C-1) のみ**で立つ |
| **X-3** | 「MEAS-N2 (1) は UNKNOWN」「優先度は $K_3$ 測定より (1) が上」 | ⚠ (1) は閉じた | 残るは **(2)** のみ。優先度指定は撤回 |
| **X-4** | 非 cofinal 鎖の $\prod q_i$ | ⚠ 精密化 | $X^{\rm st}\subseteq\bigcap_jI_{K_j}$ ⟹ **過大評価** |
| **★ X-5(新)** | **$R$ の添字順と $\mathrm{NFI}$ の添字** | ❌ **致命傷** | MEAS §1 の $R_{K,N}:GT(N)\to GT(K)$($K\subseteq N$)は**写像の向きと包含が矛盾**。M1(1) の $\bigcap_{M\supseteq'N}$ は**粗窓を走っており量化子が逆**(genuine 判定は細窓が担う)。**source-first に統一**し、cert に `reduction_index_order: "source_first"` を固定 |

### 9.2 ★ V-6 費用対殺傷力(トレードオフ表)— **配分の決定はしない**

**X-3(「$K_3$ が正しい次手」)と v1 §9-1(「安い窓を大量に」)の資源矛盾を明示する。**

**DROP-FREE(§6.2)の下で、$K_3$ に落下側の特権はゼロ。** $K_3$ の残る価値は **$\prod q_i$ の簿記(証人側・MEAS の測度積)のみ**。

- **非リフト証明のコスト** ≈ raw 候補 fibre
$$\#\mathrm{fib}(K)\ =\ \frac{K_{\rm ord}}{M_{\rm ord}}\ \cdot\ [\,M_{F_2}:K_{F_2}\,]\qquad(K\le M)$$
(各候補に hexagon (3.10)(3.11)・charming・onto を判定)。既知の実測点: $K_2$ で **48**(うち valid lift 2)。
- **殺傷力**: 補題 MONO により**細かいほど落ちやすい(単調・定理)**。粗い(安い)窓は落ちにくい。

| 選択肢 | コスト | 殺傷力 | 副次価値 | 実績 |
|---|---|---|---|---|
| **在庫の安い窓を大量に**($K=L\cap M$、$L$ = LINS/Zassenhaus/dihedral 在庫) | 小(fibre 小)・$\diamond$ 閉包**不要** | **低**(MONO の下端) | なし | 5 窓 + $K_2$ = **落下 0** |
| **公平梯子を深く**($K_3,K_4,\dots$) | 大($\diamond$ 閉包 + fibre 増大) | **高**(MONO の上端) | $\prod q_i$ 簿記・(C-2) の実現 | $q_1=q_2=1$ |
| **深い非梯子窓**(在庫を深く取る) | 中 | 高 | なし(簿記に載らない) | 未試行 |

> ⚠ **必須の断り**: どの窓も **$K\le M$**(972 窓の細分)でなければ $R_{K,M}$ が定義されない。在庫窓 $L$ は**そのままでは使えず** $K:=L\cap M$ として使う(交わりを取ると指数が上がる ⟹ コスト欄はその後の値で見積もること)。
> ⚠ 「安い窓ほど落ちにくい」は MONO(定理)の帰結だが、**どの深さで落ちるかの予測は UNKNOWN**。上表の「殺傷力」は順序関係のみで、**確率的な見込みではない**。
> **★ 配分の決定は本稿では行わない。**研究者との選定会議の入力とする。

### 9.3 DICHOT(`d972_idx3_arith_datum_independent_v1.md`)への訂正

- **§12.2-3 の括弧書き**「(cofinal なら $\bigcap K_n=1$ で $\Lambda$ は必ず細る)」は **V-4 と同じ非導出** ⟹ 同ファイルへ訂正追記(§15)。**結論(cofinal でない)は不変**、理由を COF-Λ($d=3$)へ差し替え。
- §12.3 の「(4a) は 1 段で有効」は **[2401] Cor 5.4 の直接の帰結**として既に正しい(DROP-FREE と同内容)。**本稿の DROP-FREE はこれの再発見であり、novelty はない**(V-5)。

---

## §10 未決・債務(推測で埋めていない)

1. **(C-3) 一様生存 — UNKNOWN**。閉形式路線も障害関手性路線も**どちらも生存**(§8)。
2. **公平列挙の欠番なし性**は cert 側の検査事項。本稿は証明していない。
3. **$M$ の isolated 性**(F2)は工房実測(裁定 1133)であって論文の定理ではない。
4. **§4.5 の Prop 3.15 証明は未監査**(原文に証明が無いため工房証明が正本になる ⟹ Sol/falsifier の監査を要請)。
5. **COF-Λ の $V_d=PB_3^d[PB_3,PB_3]$ が $\mathrm{NFI}_{PB_3}(B_3)$ に入る**ことは verbal ⟹ 特性から従うが、$PB_3\cong F_2\times\mathbb Z$ の分解と $B_3$ 作用の相性は 1 行で済ませた。**要 1 回の確認**。
6. **【文献要請 COF-L1】**(既出 L-1 と統合の再具申)— 副有限塔の各段で持ち上げ障害 $\mathrm{ob}_n\in H^2(Q_n,V_n)$ が消えるとき、**全段で消えること**を有限段データから結論する一般補題。型: $\varprojlim^1$ の消滅条件・障害の関手性・全素数混在塔での版。**83 線の L-1 と同一の欠落。**
