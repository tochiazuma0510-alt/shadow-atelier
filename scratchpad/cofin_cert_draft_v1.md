# COFIN-CERT 草案 v1 — 公平 shell 累積梯子の cofinality と「3 つの cofinal」の層分離

`DIR: 正側(証人型の第一証明物)/ FRAME: B₃-gentle・972 屋根`
**格**: §2–§6 の定理 5 本 = `paper-proof(自前・未監査)`。前件はすべて 2401/2405 の番号つきで pin。§7 の MEAS 訂正 = **確定**(私自身の誤記の撤回)。§8–§9 = 評価。
**著者**: 数学者(Opus 5)/ 2026-08-26。委嘱 = 司令塔(MEAS-N2 の帰結・本丸)。
**読んだ範囲**: `sol/sol_reply_159_iv.md` §21.5–§21.8・§23.11 / `docs/week1-定義ノート.md` §2(settled/isolated/reduction/genuine)・§3 / `scratchpad/d972_idx3_arith_datum_independent_v1.md` §8.2–§8.6・§12.2–§12.3 / `scratchpad/meas_program_draft_v1_1.md` §1・§6。**外部文献の直接参照ゼロ**。

---

## §0 要旨(結論 5 点)

1. **層の不整合は解けた。** MEAS の (P-ISO) と DICHOT の P-i-e は**別の主張**である。P-i-e(= 2401 Prop 3.14+3.15)は**定理**であり、**MEAS が「UNKNOWN」と札を貼ったのは私の誤記 — 撤回する**(§7)。MEAS の Haar は**無条件に立つ**(2401/2405 相対)。
2. MEAS が実際に必要としていたのは別物 = **具体的な鎖の cofinality**。これは §2 の **定理 COFIN-1** で閉じる(Sol §21.5 の公平 shell 梯子について)。証明は短い。
3. さらに **定理 COFIN-2**(合同核版)を提示する — cofinality の証明が**3 行**になり、digest 順序の簿記に依存しない。コストは同等。**証明書としてはこちらを推す。**
4. ★ **定理 DROP-FREE(§5.2)**: **落下(fake 判定)には cofinality も入れ子性も isolated 性も要らない — 窓 1 枚で足りる。** ⟹ **fake 狩りは梯子を登る作業ではなく「最安の窓を大量に撃つ」作業**。梯子の規律が要るのは証人側と測度積の簿記だけ。
5. ★ **定理 DECIDE-972(§6)**: COFIN-1/2 の下で **972 の二択は半決定可能** — fake なら**有限段で必ず証明書が出る**、証人なら出ない。⟹ 梯子を走らせる計画は正しく、かつ**停止するのは fake のときだけ**。

---

## §1 層の分離 — 同じ「cofinal」が 3 つある

| 札 | 主張 | 格 | 典拠 |
|---|---|---|---|
| **(C-1)** 抽象 cofinality | isolated 窓のなす部分 poset $\mathcal I^{\rm iso}\subseteq NFI_{B_3}(PB_3)$ は **cofinal かつ下向き有向** | **定理** | 2401 **Prop 3.14**($N^\diamond$ が isolated・$N^\diamond\subseteq N$)+ **Prop 3.15**(交わりで閉じる) |
| **(C-2)** 鎖の cofinality | **特定の**入れ子鎖 $K_0\supsetneq K_1\supsetneq\cdots$ が $NFI_{B_3}(PB_3)$ で cofinal | **本稿 §2/§3 で定理化** | Sol §21.5 の構成 + M. Hall |
| **(C-3)** 機構の一様性 | その鎖の**全段**で $I_{K_n}=X$(落下しない) | **UNKNOWN・無限量化** | — |

**(C-1) ⟹ (C-2) は成り立たない。** 実例が工房内にある: **Dih×$N_{S4}$ 系の鎖は各段 isolated だが cofinal でない**(`d972_..._v1.md` §12.2-3: $\Lambda_{K_n}=2\mathbb Z^2$ が $n$ に依らず一定 ⟹ $\bigcap K_n\ne1$)。⟹ 「isolated に制限してよい」(C-1)と「この鎖で尽きる」(C-2)は**論理的に独立**。

**MEAS が要るもの**:
- §2 の Haar(M1–M3)は **(C-1) だけ**で立つ(有向性・群・準同型・Thm 5.2)。
- §3 の乗法公式 M6($\prod q_i=\lvert X^{\rm st}\rvert/\lvert X\rvert$)は **(C-2)** が要る。
- §6 の正枝(MEAS-N2)は **(C-2)+(C-3)**。

⟹ **不整合ではなく、私が (C-1) の札を (C-2) の場所に貼っていた。**

---

## §2 定理 COFIN-1 — Sol §21.5 の梯子は cofinal

### 2.1 構成(Sol §21.5 の逐語再掲・記号のみ整理)

$B_3$ の有限指数部分群を **index shell** 順(同一 index 内は canonical marked quotient digest 順)に**公平に**列挙して $L_1,L_2,\dots$ とする(shell 飛ばし禁止)。各 $i$ で
$$H_i:=M\cap\mathrm{Core}_{B_3}(L_i),\qquad J_i:=H_i^{\diamond},\qquad K_0:=M,\quad K_n:=K_{n-1}\cap J_n .$$

### 2.2 定理

> ### 定理 COFIN-1
> 前件: **(F1)** 列挙が公平(各 index shell を有限時間で尽くす)/ **(F2)** $M$ は isolated(工房実測・裁定 1133)/ **(F3)** 2401 Prop 3.14・Prop 3.15。
> このとき $\{K_n\}_{n\ge0}$ は
> **(i)** 入れ子($K_n\subseteq K_{n-1}$)、**(ii)** 各段 isolated かつ $K_n\in NFI_{B_3}(PB_3)$、**(iii)** $NFI_{B_3}(PB_3)$ で **cofinal**。
> とくに $\bigcap_n K_n=1$。

**証明.**
**(i)** 定義から。
**(ii)** $L_i$ が $B_3$ の有限指数部分群なら $\mathrm{Core}_{B_3}(L_i)$ は有限指数の $B_3$-正規部分群(有限指数部分群の core は有限指数)。$M\in NFI_{B_3}(PB_3)$ との交わり $H_i$ も同様。$H_i^\diamond$ は $H_i$ の GTSh 連結成分の全対象の交わりで、対象はすべて $NFI_{B_3}(PB_3)$ の元だから交わりも $B_3$-正規。**成分は有限**である: Prop 3.8 より $GTSh(K,N)\ne\emptyset$ なら $K_{\rm ord}=N_{\rm ord}$ で商が同型 ⟹ 成分内の対象は $PB_3$ での指数が等しく、$PB_3$ は有限生成ゆえ(**M. Hall**)所定の有限指数の部分群は有限個。⟹ $J_i$ は有限指数。Prop 3.14 より $J_i$ は isolated。$K_0=M$ は isolated(F2)、Prop 3.15(交わりで閉じる)と帰納法で全 $K_n$ が isolated。
**(iii)** $N\in NFI_{B_3}(PB_3)$ を任意に取る。$[B_3:N]=[B_3:PB_3]\,[PB_3:N]=6[PB_3:N]<\infty$ ゆえ $N$ は $B_3$ の**有限指数部分群**であり、(F1) の公平列挙のどこかに現れる: $L_i=N$。$N$ は $B_3$-正規だから $\mathrm{Core}_{B_3}(N)=N$、よって
$$K_i\ \subseteq\ J_i\ =\ (M\cap N)^{\diamond}\ \subseteq\ M\cap N\ \subseteq\ N .$$
(i) より $n\ge i$ で $K_n\subseteq N$。ゆえに cofinal。最後の $\bigcap_n K_n=1$ は $PB_3$ の剰余有限性(有限指数部分群の交わりが自明)から。$\blacksquare$

**所見**: 証明の実質は 3 行 — **(a) 目標窓自身が列挙に現れる(公平性)/ (b) その段で $J_i\subseteq N$($\diamond$ は下がるだけ)/ (c) 累積は単調**。Sol の「Prop 3.14 の isolated subposet cofinality により cofinal になる」という言い回しは結論として正しいが、**実際に効いているのは Prop 3.14 ではなく公平列挙**である(Prop 3.14 は (ii) の isolated 性にだけ効く)。⟹ **証明書の文言はこの区別を反映させること**(現行の言い回しは (C-1) と (C-2) を混ぜている)。

---

## §3 定理 COFIN-2 — 合同核版(証明 3 行・推奨形)

digest 順序の簿記に依存しない同値な梯子を提案する。

$$\Delta_n:=\bigcap\{\,N\in NFI_{B_3}(PB_3)\ :\ [PB_3:N]\le n\,\},\qquad K_0:=M,\quad K_n:=K_{n-1}\cap\bigl(M\cap\Delta_n\bigr)^{\diamond}.$$

> ### 定理 COFIN-2
> $\Delta_n\in NFI_{B_3}(PB_3)$(有限交わり・M. Hall)。$\{K_n\}$ は入れ子・各段 isolated・**cofinal**。
> **証明.** $[PB_3:N]=m$ なる $N$ に対し $K_m\subseteq\Delta_m\subseteq N$。isolated 性は Prop 3.14+3.15、有限指数は M. Hall。$\blacksquare$

**COFIN-1 との比較**

| | COFIN-1(Sol) | COFIN-2(合同核) |
|---|---|---|
| cofinality の証明 | 公平性の定式化に依存(shell 飛ばし禁止・digest 順の全域性) | **構成から自明**(3 行) |
| 実装コスト | LINS で shell ごとに列挙 | **同じ** LINS 列挙(index $\le n$ を全部使う) |
| 1 段あたりの窓の重さ | $J_i$ 1 本 ⟹ **軽い** | $\Delta_n$ は index $\le n$ の**全部の交わり** ⟹ **重い** |
| 証明書の脆さ | 列挙の公平性が抜けると cofinality が落ちる | 落ちない |

⟹ **推奨**: 実装は COFIN-1(軽い)、**証明書の文言は COFIN-2 を「上界の見本」として併記**し、「COFIN-1 の列挙が公平である限り COFIN-2 と同じ結論」と書く。公平性は**実装の不変条件**として cert に固定する(`shell_index_cursor` が単調・欠番なし)。

---

## §4 系 COF-Λ — cofinal な梯子では「三位一体」は起こりえない

> ### 系 COF-Λ
> $\{K_n\}$ が cofinal なら、任意の $d\ge1$ に対しある $n$ で $\Lambda_{K_n}\subseteq d\mathbb Z^2$。
> ($\Lambda_K$ = $K_{F_2}$ の $F_2^{\rm ab}=\mathbb Z^2$ における像。)
> **証明.** $V_d:=PB_3^{\,d}[PB_3,PB_3]$ は verbal ⟹ $PB_3$ で特性 ⟹ $B_3$-正規、指数有限。cofinality より $K_n\subseteq V_d$ なる $n$ があり、$V_d$ の $F_2^{\rm ab}$ における像は $d\mathbb Z^2$ に含まれる。$\blacksquare$

**帰結(★ 研究計画への含意)**:
- `d972_..._v1.md` §12.2-3 の「$\Lambda_{K_n}=2\mathbb Z^2$ 一定」という配置は、**cofinal な梯子では原理的に不可能**。⟹ **公平 shell 梯子では ★三位一体(閉形式が全段で書けるが何も証明しない)は必ず破れる。**
- ⟹ ある有限段で `RUNG-UNIF` の閉形式 $f=y^\nu x^{-\nu}w_1$ による「無料の持ち上げ」は**必ず使えなくなる**(T-DEAD 型の死)。そこから先の各段は**生の fibre を尽くす**しかない。
- ⚠ **混同禁止**: 閉形式の死は**落下ではない**(機構の限界であって非存在の証明ではない — `d972` §10.4-2)。しかし「梯子が情報を持ち始める点」ではある。
- ⟹ MEAS の $q_1=q_2=1$ が「完全相関 = 新情報ゼロ」だったのは、**まだ $\Lambda$ が細っていない浅い段にいるから**と説明がつく。**深さを増やす動機はここにある**(ただし §5 の非対称は不変)。

---

## §5 非対称の定理化 — 落下側は cofinality も isolated も要らない

記号: $X=GT(M)$、$A=\mathrm{Im}(\mathrm{Ih}_M)$、$X^{\rm st}$ = $\widehat{GT}_{\rm gen}$ の $M$ 窓像(= genuine 全体)、$g^\ast$ = row 36 $\in X\setminus A$(c′ 非依存)。前件は DICHOT-972 の P-i-a/b/d・P-ii・P-iii($[X:A]=3$)・P-iv(Cor 5.4)・P-v(Thm 5.2)。

### 5.1 定理 ASYM(二枝の要件表)

| 枝 | 結論 | 必要な前件 | 量化 |
|---|---|---|---|
| **落下** $\exists K:\ g^\ast\notin\mathrm{im}(R_{M,K})$ | $X^{\rm st}=A$ ⟹ **648 は全て fake** | (C-1) のみ。**(C-2) 不要・入れ子不要** | $\exists$(有限で証明可能) |
| **非落下** $\forall K:\ I_K=X$ | $X^{\rm st}=X$ ⟹ **648 は genuine 非算術証人** | (C-1)+**(C-2)**+**(C-3)** | $\forall$(無限・一様定理が要る) |

### 5.2 ★ 定理 DROP-FREE

> **窓 $K\in NFI_{B_3}(PB_3)$ を任意($\mathbf{isolated}$ **でなくてよい**・$M$ の入れ子鎖上でなくてよい)に取る。$g^\ast\notin\mathrm{im}(R_{M,K})$ ならば $X^{\rm st}=A$、すなわち $X\setminus A$ の 648 元はすべて非 genuine(gentle-fake)。**

**証明.** $K^\diamond\subseteq K$ は isolated(Prop 3.14)で、関手性(P-i-d)より $R_{M,K^\diamond}=R_{M,K}\circ R_{K,K^\diamond}$ ⟹ $\mathrm{im}(R_{M,K^\diamond})\subseteq\mathrm{im}(R_{M,K})$。よって $g^\ast\notin\mathrm{im}(R_{M,K^\diamond})$。Thm 5.2(isolated poset 上の極限)より $X^{\rm st}=\bigcap_{L\ \rm isolated}\mathrm{im}(R_{M,L})$ だから $g^\ast\notin X^{\rm st}$。一方 P-i-a/b より各 $\mathrm{im}(R_{M,L})$ は $X$ の部分群、ゆえに $X^{\rm st}$ も部分群で、P-ii より $A\subseteq X^{\rm st}$。$[X:A]=3$ は素数ゆえ $X^{\rm st}\in\{A,X\}$、$g^\ast\notin X^{\rm st}$ から $X^{\rm st}=A$。$\blacksquare$

> ### ★ 実務への含意(戦略の変更提案)
> **fake 狩りに梯子は要らない。** 必要なのは「$g^\ast$ が持ち上がらない窓を 1 枚見つける」ことだけで、その窓は
> - **isolated でなくてよい**($\diamond$ 閉包の計算コストが**丸ごと不要** — Sol の first missing datum `RUNG-LADDER-ISOLATED-JOIN-QUOTIENT...` は落下狩りには不要)、
> - **入れ子でなくてよい**(`OBS-UNIF-1` の 5 窓が非入れ子なのは、落下狩りとしては**欠陥ではない**)、
> - **cofinal 族の一部でなくてよい**(固定素数 Zassenhaus 塔・dihedral 3-冪塔も**使ってよい**)。
> ⟹ **落下狩りの最適戦略は「最安の窓を最大枚数」**。累積梯子の規律は、証人側の簿記と MEAS の測度積のためだけに要る。
> ⚠ ただし**逆向きは非対称**: 非 isolated な $K$ で $g^\ast$ が持ち上がっても $I_K=X$ は言えない(部分群でないので 1 元経済が効かない)。**陽性は isolated 窓でしか記帳できない。**

---

## §6 定理 DECIDE-972 — 972 の二択は半決定可能

> ### 定理 DECIDE-972
> COFIN-1(または COFIN-2)の梯子の下で:
> **(a)** $X^{\rm st}=A$(fake 枝)ならば、**ある有限段 $n_0$ で $I_{K_{n_0}}=A$ が観測される**。
> **(b)** $X^{\rm st}=X$(証人枝)ならば、どの有限段でも $I_{K_n}=X$ で、**有限の証明書は出ない**。
> ⟹ **fake は半決定可能、証人は半決定可能でない**(この手続きの範囲で)。

**証明.** cofinality より $\bigcap_n I_{K_n}=X^{\rm st}$。$(I_{K_n})$ は有限群 $X$ の部分群の減少列ゆえ**有限段で停留**する。停留値が $X^{\rm st}$。よって (a): 停留値 $A$ なら有限段で $I_{K_n}=A$。(b): 停留値 $X$ なら全段 $X$。各段の判定は $g^\ast$ の raw fibre の有限悉皆(DICHOT 1 元経済)ゆえ有限計算。$\blacksquare$

**注**: 「有限段で停留」は $[X:A]=3$ と単調性(DICHOT (5): 落下は高々 1 回)からも直ちに従う。⟹ **梯子は高々 1 回しか状態を変えない有限状態機械**であり、走らせる意味は「その 1 回が起きるかを待つ」ことに尽きる。**停止するのは fake のときだけ**。

> ⚠ **実務上の留保**: 半決定可能性は**原理**の言明。各段のコスト($\diamond$ 閉包・raw fibre 悉皆)は上に有界でなく、$n$ とともに爆発しうる。⟹ 「いつか出る」は「実行可能」を意味しない。§5.2 の戦略変更(安い窓を大量に)はこの留保への直接の応答でもある。

---

## §7 MEAS への訂正(確定・私自身の誤記の撤回)

| # | MEAS v1/v1.1 の記述 | 判定 | 訂正 |
|---|---|---|---|
| **X-1** | 「**前件 (P-ISO)**: … **格 = UNKNOWN**(isolated 窓の cofinal 性は当工房で未証明)」(§1) | ❌ **誤り・撤回** | (C-1) は **2401 Prop 3.14+3.15 の定理**であり、DICHOT の前件表 P-i-e に既に pin 済み。「未証明」は事実誤認。**当該行は削除し、典拠を Prop 3.14/3.15 に置換すること。** |
| **X-2** | 「**MEAS 全体がこの前件に載る**」(§7 正直条項 4) | ⚠ **過大** | Haar(M1–M3)が載るのは **(C-1) のみ**で、それは定理。⟹ **MEAS の Haar は無条件に立つ**(2401/2405 相対)。載っていたのは M6 と MEAS-N2 で、それは **(C-2)**。 |
| **X-3** | 「【MEAS-N2】(1) cofinality 証明書 +(2) 一様生存定理 — **UNKNOWN**」「優先度は $K_3$ 測定より (1) の証明が上」(§6) | ⚠ **(1) は本稿で閉じた** | **(1) = COFIN-1/COFIN-2 で証明済**。⟹ **残るは (2) のみ**。**優先度の再逆転**: (1) が閉じた以上、**$K_3$ の測定(= 半決定手続きの前進)が正しい次手**。§6 で私が書いた優先度指定は撤回する。 |
| **X-4** | 台帳 D-8/D-10 の「$q_1=q_2=1$」 | ⚠ **格の精密化** | $q_2$ の $K_2$ は公平 shell 梯子上(Sol §23.11 で shell 2/3 を閉じた後の最初の strict rung)⟹ **COFIN-1 により真に cofinal な鎖の因子**。ただし**非落下は依然として何も証明しない**(§5.1)。なお **cofinality が無い鎖では $\prod q_i$ は $\lvert X^{\rm st}\rvert/\lvert X\rvert$ の**過大評価**にしかならない($X^{\rm st}\subseteq\bigcap_j I_{K_j}$)— この不等号は MEAS v1 に無かった。 |

**⟹ MEAS の Haar が立つために足りないものは、もう無い。**(C-1) が定理、(C-2) が本稿の定理。残る UNKNOWN は **(C-3) 一様生存**ただ 1 本。

---

## §8 残る唯一の穴 — なぜ (C-3) が難しいか(評価・candidate)

1. **正側は井原と同値**(`d972` §8.6-3 の再確認): 標的は $A$ の**外側**ゆえ算術は定義上一切供給できない。$X^{\rm st}=X$ の証明 = 「genuine かつ非算術」の構成 = 井原予想の反例構成。**無料の帰納は無い。**
2. **★ 本稿が付け加える悪い知らせ**: 系 COF-Λ より、cofinal な梯子では $\Lambda$ が必ず細る ⟹ **`RUNG-UNIF` の閉形式は必ず死ぬ**。⟹ **(C-3) を閉形式の一様性で証明する道は原理的に塞がっている**。(C-3) を狙うなら、閉形式ではなく**障害の消滅の関手性**(`d972` §8.6-4 の ①②③)しかない。
3. ⟹ **(C-3) への現実的な道は 1 本だけ**: 各段の持ち上げ障害 $H^2(Q_n,V_n)$ の**消滅が段を跨いで伝播する**補題(= 83 線の【文献要請 L-1】と同一の欠落補題。`d972` §8.6-4 で統合を具申済)。
4. **prior**: BIT-252 = VERDICT A(落下が実際に観測された姉妹窓)⟹ 非落下側への事前確率は低い。**総合 UNKNOWN・資源は落下側**(§5.2)。

### 【文献要請 COF-L1】(既出 L-1 と統合の再具申)
- **困難**: 副有限塔 $Q_{n+1}\twoheadrightarrow Q_n$ の各段で、群拡大の持ち上げ障害類 $\mathrm{ob}_n\in H^2(Q_n,V_n)$ が消えることが分かっているとき、**それが全段で消えること**(= 逆極限での持ち上げの存在)を有限段のデータから結論する一般補題。
- **欲しい結果の型**: 「$\varprojlim^1$ の消滅条件」「障害の関手性 $H^2(Q_n,V_n)\to H^2(Q_{n+1},V_{n+1})$ の自然性と、それによる伝播」「pro-$p$ でない(全素数混在の)塔での版」。Iwasawa 塔・変形空間・Galois 表現の持ち上げ(Ramakrishna 型)に類例がありそう。
- **83 線の L-1 と同一の欠落**。統合発注を具申。

---

## §9 実務への含意(4 点)・未決

1. **落下狩りの再設計(§5.2)**: $\diamond$ 閉包・入れ子・cofinal をすべて外し、**安い窓を大量に $g^\ast$ に当てる**。既存在庫(LINS 4,265 行・固定素数 Zassenhaus・dihedral 塔・5 named windows の細分)がそのまま弾になる。**Sol の first missing datum は落下狩りには不要**。
2. **累積梯子は証人側と測度台帳のためだけに維持**。COFIN-1 の公平性は **cert の不変条件**(`shell_index_cursor` 単調・欠番なし)として固定する。
3. **$K_3$ の測定は正しい次手**(X-3)。ただし期待値は非対称: $q_3=1/3$ で完結、$q_3=1$ で情報ゼロ。
4. **深さの意味づけが変わった**: 系 COF-Λ により、深く登れば必ず「閉形式が効かない段」に到達する ⟹ **梯子は treadmill ではない**。ただしそこで得られるのは「情報のある測定」であって「証人の証明」ではない。

**未決・債務(推測で埋めていない)**
- (C-3) 一様生存定理 — **UNKNOWN**(§8)。
- 「公平列挙」の形式化: COFIN-1 (F1) は「各 shell を有限時間で尽くす」まで。**実装が本当に欠番なしかは cert 側の検査事項**で、本稿は証明していない。
- $M$ の isolated 性(F2)は**工房実測**(裁定 1133)であって論文の定理ではない — 前件として明記が要る。
- Prop 3.14 の $N^\diamond$ の**連結成分の有限性**は本稿で Prop 3.8 + M. Hall から補ったが、**論文が同じ論法を使っているかは未照合**(定義ノート §2 の記述は結論のみ)。⟹ **原文の Prop 3.14 の証明を 1 度 pdftocairo で確認すること**を具申(私は本稿で原文画像を見ていない)。
- COF-Λ の $V_d=PB_3^d[PB_3,PB_3]$ が $NFI_{B_3}(PB_3)$ に入ることは verbal ⟹ 特性から従うが、$PB_3\cong F_2\times\mathbb Z$ の分解と $B_3$ 作用の相性は**本稿では 1 行で済ませた**。要 1 回の確認。
