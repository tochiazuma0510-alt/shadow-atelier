# 予想 EP-DEL の判定 v1 — endpoint $E_P(M)$ は strand-deletion 核に自動で入るか

`DIR: proper 側計器 / FRAME: Sol A7 三 endpoint × 工房 BRUN-DEF`
**委嘱**: 司令塔・裁定 1713 札 3(a)。**判定 = PROVED(filtration 1 段の意味で)/ UNKNOWN(素朴な意味で)。**
**読んだ範囲**: `sol/audit_r07_full_proof_reaudit_and_forward_direction_v220.md` §7(endpoint 鎖・v193→v194 の supersede)・`sol/proof_r07_ordered_nonlinear_residual_double_localization_v252.md` §2 末〜§3(Thm 2.1 の証明末尾・Thm 3.1 DEEP DOUBLE LOCALIZATION)。**v194/v198 の原文は未読**(要旨は v220 §7 経由)。
**著者**: 数学者(Opus 5)/ 2026-08-28。**格 = paper-proof(自前・未監査)。**

---

## 1. 設問の分解

**問**: $M=\sum a_i(U_i-V_i)$ の occurrence が charming 台(commutator words)なら、$E_P(M)$ は 4 本の strand-deletion が誘導する鎖写像 $(d_i)_*$ の核に**自動的に**入るか。

分けるべき 2 つの水準:

| 水準 | 主張 | 状態 |
|---|---|---|
| **(G) 群水準** | $P(F_kc_k)\in B_P=\mathrm{Im}(\mathrm{Brun}_4\to G_P)$ | **既に成立**(Sol v252 (3.3)。**工房の BRUN-DEF を前件に使っている**) |
| **(L) 線型化水準** | $E_P(M)\in\bigcap_i\ker\,(d_i)_*$ | **本設問** |

⟹ 問いは「**(G) が (L) へ降りるか**」である。

---

## 2. 降りる半分(証明できる部分)

### 補題 D-NAT(Fox 微分は strand-deletion に対して自然)
$d_i:P_4\to P_3$ は**生成元を生成元または $1$ に送る**準同型である。Fox 微分の連鎖律
$$\frac{\partial(\varphi w)}{\partial x'_j}=\sum_k \varphi\!\left(\frac{\partial w}{\partial x_k}\right)\cdot\frac{\partial(\varphi x_k)}{\partial x'_j}$$
において $\partial(\varphi x_k)/\partial x'_j\in\{0,1\}$ となるので、連鎖律は**単なる代入**に退化する。ゆえに
$$\boxed{\ (d_i)_*\,\mathrm{Fox}(w)\ =\ \mathrm{Fox}\bigl(d_i(w)\bigr)\ }$$
が**厳密に**成り立つ。∎

### 系 D-BRUN
$w\in\mathrm{Brun}_4=\bigcap_i\ker d_i$ ならば $(d_i)_*\mathrm{Fox}(w)=\mathrm{Fox}(1)=0$、すなわち $\mathrm{Fox}(w)\in\bigcap_i\ker(d_i)_*$。∎

**⟹ もし $E_P(M)$ が「$P(F_kc_k)$ の Fox 鎖」そのものであれば、(G)+D-NAT+D-BRUN で EP-DEL は即座に PROVED。**

---

## 3. 降りない半分(★ 急所は v252 自身が文書化している)

**$E_P(M)$ は $\mathrm{Fox}(P(F_kc_k))$ ではない。**$E_P$ は **11 occurrences を printed order と fixed prefixes/signs で 3 relation block に合成した後の endpoint**(v220 §7・v194)であり、合成は積の Fox 則
$$\mathrm{Fox}(w_1w_2)=\mathrm{Fox}(w_1)+w_1\cdot\mathrm{Fox}(w_2)$$
の **crossed-prefix 項**($w_1\cdot$)を伴う。

> ### ★ v252 の逐語(これが決定的)
> Theorem 2.1 の証明末尾:
> "The crossed-prefix terms in the exact Fox product rule **are not discarded**; equation (2.4) **locates them in the next layer**."
>
> ⟹ **$E_P(M)$ と $\mathrm{Fox}(P(F_kc_k))$ は $\mathcal F^{k+1}$ を法としてしか一致しない。**(v252 の filtration $\mathcal F^k\mathcal C$。)

**⟹ 発案係の警告は正しく、しかも Sol の文書が既にその現象を記録している。**「augmentation filtration と LCS の次数対応が係数拡大で混ざる」という懸念は、ここでは**より具体的に「crossed-prefix 項が 1 層ずれる」**という形で現れる。

---

## 4. 判定

> ### 予想 EP-DEL の判定
> **(i) $\ \mathcal F^{k+1}$ を法として PROVED**:
> $$E_P(M)\ \in\ \bigcap_{i=1}^{4}\ker\,(d_i)_*\ \ \pmod{\mathcal F^{k+1}}.$$
> **証明.** $F_kc_k$ は commutator word(v252 (3.1))⟹ **BRUN-DEF** より $P(F_kc_k)\in B_P$(v252 (3.3))⟹ $\mathrm{Fox}(P(F_kc_k))\in\bigcap\ker(d_i)_*$(D-NAT + D-BRUN)。$E_P(M)\equiv\mathrm{Fox}(P(F_kc_k))\pmod{\mathcal F^{k+1}}$(v252 (2.4) の crossed-prefix 局所化)。∎
>
> **(ii) 素朴な意味(on the nose)では UNKNOWN。**障害は**ただ一点** — crossed-prefix 項が $\ker(d_i)_*$ に入るか。

**⟹ 「自動的に入るか」への答えは「**先頭層は自動・次層は未決**」。**

---

## 5. 実務的帰結(配達判断の材料)

### 5.1 A7 は 2 本にはならない。が、$E_P$ の検査は **1 層縮む**。

v220 (7.1) は $E_{H1}=E_{H2}=E_P=0$ を**厳密に**要求する。判定 (i) より

$$E_P(M)\ \text{の}\ \mathcal F^{k}/\mathcal F^{k+1}\ \text{成分は自動的に}\ \ker(d_i)_*\ \text{に入る}$$

ので、**$E_P=0$ の検査は「先頭層 = 0」から「次層 $\mathcal F^{k+1}$ 成分 = 0」へ落ちる**。
⟹ **A7 の endpoint は 3 本のまま**だが、**$E_P$ の 1 本だけ検査次数が 1 段上がる(= 探索空間が 1 層小さくなる)**。「実質 2 本」という期待は**過大**。

### 5.2 昇格に必要な補題(これを潰せば PROVED)

> ### 補題 CP-BRUN(未証明・これが唯一の欠落)
> v194 の block 合成で生じる **crossed-prefix 補正項が $\bigcap_i\ker(d_i)_*$ に入る**。
> **十分条件の候補**: 合成の各 prefix $w_1$ が **$d_i$ で 1 に落ちる**か、あるいは補正項 $w_1\cdot\mathrm{Fox}(w_2)$ の $w_2$ が Brunnian であること。
> **なぜ非自明か**: $M$ は「Brunnian 語の積」ではなく「**総和が関係語になる符号つき occurrence の線型結合**」である。個々の occurrence は Brunnian でなくてよい ⟹ 補正項を個別に殺す根拠が現状ない。

### 5.3 v252 §3 との整合(一言)

v252 Thm 3.1 の $B_P\cap R_S(G_P)$ は**群水準の局所化**であり、**本判定はその線型化版**である。両者は矛盾しない:
- v252: 「残差は $B_P\cap R_S(G_P)$ に入る」(**群**)。
- 本稿: 「その事実の Fox 線型化は endpoint の**先頭層**にのみ降りる」(**鎖**)。
⟹ **語 residual 版(v252)の方が強く、鎖版(A7 の $E_P$)へ降ろすときに 1 層失う。**この「1 層の損失」が v252 が "stronger and safer than asking whether the raw additive Fox chain is group-like" と書いた内容の、deletion 側での対応物である。

---

## 6. UNKNOWN・債務

1. **補題 CP-BRUN**(§5.2)— 未証明。**これが EP-DEL の全て。**
2. **v194/v198 の原文未読** — 合成の prefix/sign の具体形を見ていない。CP-BRUN の十分条件が実際に満たされるかは**原文を読めば決まる可能性がある**(Sol 側に照会するのが最短)。
3. $\mathcal F^k$ が augmentation filtration か LCS filtration か、および係数環($\mathbb F_3[E_4]$ 等)での両者のずれ — v252 は $\mathcal F^k\mathcal C$ としか書いておらず、**本稿はどちらでも成り立つ形で書いた**(D-NAT は係数環に依らない)。ただし **CP-BRUN の判定には filtration の同定が要る**。
4. **BRUN-DEF 自体の格**: `paper-proof`(工房・falsifier 照合済)であって Lean 未形式化。本判定はその上に乗る。
