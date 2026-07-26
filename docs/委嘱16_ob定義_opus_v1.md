# 委嘱 16 回答 v1 — class-6 障害式 ob の独立導出(並列ブラインド)

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 16。Sol 便 22 と並列独立・互いに不可視。**
**ブラインド規律**: 本委嘱中 `sol/sol_task_22*`・`sol/sol_reply_22*` は**一切読んでいない**。読んだのは `docs/notes/反証前哨_e2c6manifest.md`・`docs/manifest_e2c6_sweep_v1.md`・`crosscheck/agree6_claude.json`(C-ブロックのみ)・`docs/命題_E23中心障害消滅_v1.md`(自作)・`docs/week4-E2作用表6_claude_v1.md`(自作)。
検算: `search/week4-ob-c6-derive.mjs`(node 独立実装・**10/10 PASS**)。
状態: **紙上(Opus 単系統)**。`cross-checked` でも `verified` でもない。

---

## 0. 結論(先に 5 行)

1. **falsifier の指摘は正当**: $q_\theta\in C^\sigma$ は成り立たない($E23$ が言うのは $q_\theta\in C^\theta$ のみ)。`(q_\theta)_+` は未定義だった。
2. **しかし答えは (A) でも (B) でもない。** 平均化射影 $e = 3^{-1}\mathcal N_C$ は**障害群へ落ちない**(§3)。それを使う manifest 式 (10.2) は、**可解な系で ob ≠ 0 を返す**(§4・明示反例つき)。**偽 fake 生成器**である。
3. **正しい判定式**(§2・両向き証明つき):
 $$ \boxed{\ \text{可解}\iff q_\theta - 3^{-1}(1+\theta)q_N \in (1+\theta)\ker\mathcal N_C\ } $$
 すなわち $\mathrm{ob} := \bigl[\,q_\theta - 3^{-1}(1+\theta)q_N\,\bigr]\in \mathrm{Ob} := C^\theta/(1+\theta)\ker\mathcal N_C$。
4. **class-6・$j=2$ での座標**(§3): $\dim_{\mathbb F_2}\mathrm{Ob} = 2$(manifest の 2 ビットと一致)。$(C^\sigma)^\theta\to\mathrm{Ob}$ は**同型**で、$a = u_4\mapsto[u_4]$、$b = u_1+u_2+u_3\mapsto[u_2]$。したがって
 $$ \boxed{\ \mathrm{ob}_a = (q_\theta - 3^{-1}(1+\theta)q_N)\ \text{の}\ u_4\ \text{係数},\qquad \mathrm{ob}_b = \text{同}\ u_2\ \text{係数}\ } $$
 **平均化射影を掛けてはならない。素の係数を読む(ただし $u_1$ でも「$b$ 成分」でもなく $u_2$)。**
5. **class 5 との決定的な差**(§1): class 6 では **$\theta\mathcal N_C\ne\mathcal N_C\theta$、$\ker\mathcal N_C$ は $\theta$-安定でない**。E23 の消滅機構が壊れる理由はここにあり、「$C_+\oplus C_-$ に分けて成分ごとに読む」という class-5 由来の直感がそのまま**誤り**になる。

---

## 1. 設定と、class 6 で壊れるもの

記法は `docs/命題_E23中心障害消滅_v1.md` に従う。$A$ は class $\le2$、$C = [A,A]\subseteq Z(A)$、$\Lambda(z) = ((1+\theta)z,\ \mathcal N_Cz)$、$\mathrm{Ob}_{E22} = (C\times C)/\operatorname{im}\Lambda$、$\Xi(\bar f) = (q_\theta,q_N)$、定理 E22′: 可解 $\iff \Xi(\bar f)\in\operatorname{im}\Lambda$。

**無条件に成り立つ二つ(E23 の中央欠損補題・class に依らない)**:
- **(E23a)** $q_\theta(\bar f)\in C^\theta$。($\theta(q_\theta) = q_\theta\cdot\beta(\bar f,\bar\theta\bar f) = q_\theta$、$\bar\theta\bar f = -\bar f$ と $\beta$ の交代性。)
- **(E23b)** $q_N(\bar f)\in C^\sigma$。($\sigma(q_N) = q_N\cdot\beta(\bar f,\bar E_m)\cdot\beta(\bar f,\bar\sigma^2\bar f+\bar\sigma\bar f)$ で、$\bar{\mathcal N}\bar f = -\bar E_m$ から二項が相殺。)

**$q_\theta\in C^\sigma$ は成り立たない** — falsifier の指摘どおり。実測($j=2$): $\dim C^\theta = 4$、$\dim C^\sigma = 2$、$C^\sigma\subsetneq C^\theta$。

**class 6 で新たに壊れるもの(検算 (2)・class 5 との差)**:
$$ \theta\,\mathcal N_C \;\ne\; \mathcal N_C\,\theta \quad(\text{全 }m),\qquad \theta\bigl(\ker\mathcal N_C\bigr)\;\ne\;\ker\mathcal N_C. $$
すなわち **Maschke 分解 $C = C^\sigma\oplus\ker\mathcal N_C$ は $\theta$-同変でない**。
(class 5 では $\langle\sigma,\theta\rangle|_C$ が真に $S_3$ を通り、$\theta\sigma\theta^{-1} = \sigma^{-1}$ ゆえ同変だった。class 6 では $\sigma_m$ の $m$-捻れが $C$ 上まで届き、$S_3$ 関係が $C$ 上で崩れる。)
**⇒「$C_+$ 成分と $C_-$ 成分に分けて別々に読む」という class-5 由来の設計は、class 6 では最初から使えない。**

---

## 2. 主定理 — 正しい障害式(両向き)

> **命題 OB(class-6 障害式).** $A$ を class $\le2$、$C = [A,A]$ に $3$ が可逆(2 群なら自動)とする。$\bar f\in\mathcal L$ に対し $q_\theta,q_N$ を通常どおり定める。$C_- := \ker\mathcal N_C$、$z_0 := 3^{-1}q_N$ と置く。このとき
> $$ \Xi(\bar f)\in\operatorname{im}\Lambda \iff q_\theta - (1+\theta)z_0 \in (1+\theta)C_- \tag{OB}$$
> すなわち **$\mathrm{ob} := \bigl[q_\theta - 3^{-1}(1+\theta)q_N\bigr]\in \mathrm{Ob} := C^\theta\big/(1+\theta)C_-$** が唯一の障害である。

**証明.**
まず $z_0$ が well-defined: (E23b) より $q_N\in C^\sigma$、$\mathcal N_C|_{C^\sigma} = 3\cdot\mathrm{id}$、$3$ は可逆。ゆえに $\mathcal N_Cz_0 = 3^{-1}\cdot3\,q_N = q_N$。

**(⇐)** $\mathrm{ob} = 0$ とすると $\exists z_-\in C_-$ で $q_\theta - (1+\theta)z_0 = (1+\theta)z_-$。$z := z_0+z_-$ と置くと
$$ \mathcal N_Cz = \mathcal N_Cz_0 + 0 = q_N,\qquad (1+\theta)z = (1+\theta)z_0 + (1+\theta)z_- = q_\theta, $$
すなわち $\Lambda(z) = (q_\theta,q_N) = \Xi(\bar f)$。∎

**(⇒)** $\Lambda(z) = \Xi(\bar f)$ なる $z$ があるとする。$\mathcal N_C(z-z_0) = q_N-q_N = 0$ ゆえ $z-z_0\in C_-$、かつ
$$ (1+\theta)(z-z_0) = q_\theta - (1+\theta)z_0 $$
だから右辺は $(1+\theta)C_-$ に属する。∎

**所属の確認**: (E23a) より $q_\theta\in C^\theta$、また $\theta(1+\theta) = (1+\theta)$ ゆえ $(1+\theta)z_0\in C^\theta$。したがって代表元は $C^\theta$ に入り、$\mathrm{Ob} = C^\theta/(1+\theta)C_-$ は well-defined。

> **★ この証明は $\theta$ と $\mathcal N_C$ の可換性も、$C_-$ の $\theta$-安定性も、$(C^\sigma)^\theta$ への射影も、一切使わない。** ゆえに class 6 でもそのまま通る。**class-5 の E23 は、$C^\sigma = 0$($\Rightarrow z_0 = 0$)と $C^\theta = (1+\theta)C$($\Rightarrow \mathrm{Ob} = 0$)という二つの特殊事情で (OB) が自明化した場合にすぎない。**

---

## 3. class-6・$j=2$ での明示座標

基底 $(t_5,t_6,u_1,u_2,u_3,u_4)$、$R = \mathbb Z/2$。確定表 `agree6_claude.json` の C-ブロックのみを入力とした(検算 (0)–(3))。

| 量 | 値($m\equiv0$ と $m\equiv1$ で同一) |
|---|---|
| $C^\sigma$ | $\langle a,b\rangle$、$a = u_4$、$b = u_1+u_2+u_3$(dim 2) |
| $\theta$ | $\theta(a) = -a$、$\theta(b) = +b$(manifest の符号と一致) |
| $C^\theta$ | $\{(\alpha,\alpha,\gamma,\delta,\gamma,\varepsilon)\}$(dim 4) |
| $C_- = \ker\mathcal N_C$ | dim 4(**$\theta$-安定でない**) |
| $(1+\theta)C_-$ | $\boxed{\langle\,t_5+t_6,\ u_1+u_3\,\rangle}$(dim 2) |
| $\mathrm{Ob} = C^\theta/(1+\theta)C_-$ | **dim 2**(manifest の 2 ビットと一致) |

> **命題 OB-c6(判定の座標形).** $v := q_\theta - 3^{-1}(1+\theta)q_N\in C^\theta$ と置く。$j=2$ では
> $$ [v] = 0\ \text{in}\ \mathrm{Ob} \iff \bigl(v\ \text{の}\ u_2\ \text{係数},\ v\ \text{の}\ u_4\ \text{係数}\bigr) = (0,0). $$
> **証明**: $(1+\theta)C_- = \langle t_5+t_6,\ u_1+u_3\rangle$ で、$v\in C^\theta$ は $v_{t_5}=v_{t_6}$、$v_{u_1}=v_{u_3}$ を満たすから、$v$ を $(1+\theta)C_-$ で法とすると $t$-成分と $u_1{=}u_3$ 成分がちょうど消え、$u_2,u_4$ 成分だけが残る。∎(検算 (3b) が全 $v\in C^\theta$ で悉皆確認)

> **ラベルの整合(検算 (3c))**: 合成 $(C^\sigma)^\theta\hookrightarrow C^\theta\twoheadrightarrow\mathrm{Ob}$ は**同型**で、
> $$ a = u_4\longmapsto[u_4],\qquad b = u_1+u_2+u_3\longmapsto[u_2] $$
> (∵ $u_1+u_3\in(1+\theta)C_-$)。**ゆえに manifest の $(a,b)$ ラベルは正しく、報告座標は**
> $$ \boxed{\ \mathrm{ob}_a = v_{u_4},\qquad \mathrm{ob}_b = v_{u_2}\ } $$
> **である**($u_1$ でも $u_3$ でも「$b$ 成分」でもない)。

### 3.1 ★ なぜ (A)(平均化射影)が誤りか

$e := 3^{-1}\mathcal N_C$ は $C\to C^\sigma$ の射影として well-defined である(3 可逆)。**しかし $e$ は $(1+\theta)C_-$ を殺さない**(検算 (3d)):
$$ t_5+t_6\in(1+\theta)C_-\quad\text{だが}\quad e(t_5+t_6) = \mathcal N_C(t_5+t_6) = a+b \ne 0 $$
($m\equiv0$: $\mathcal N_C(t_5) = a$, $\mathcal N_C(t_6) = b$;$m\equiv1$: 入れ替わる)。
**⇒ $e$ は障害群 $\mathrm{Ob}$ へ落ちない。** $e$ を使う量は $z_-$ の自由度に依存し、**可解性の関数になっていない**。

---

## 4. ★★ 偽陽性 fixture — manifest 式 (10.2) は可解系で $\mathrm{ob}\ne0$ を返す

**falsifier が要求した「(A)/(B) が分岐する合成テストベクトル」を、より強い形で与える** — (A) が**誤答する**具体系である(検算 (4)):

| | $m\equiv0$ | $m\equiv1$ |
|---|---|---|
| $z_-\in\ker\mathcal N_C$ | $(0,1,0,1,0,0) = t_6+u_2$ | $(1,0,0,1,0,0) = t_5+u_2$ |
| $q_\theta := (1+\theta)z_-$ | $(1,1,0,0,0,0) = t_5+t_6$ | 同じ |
| $q_N := 0$ | | |
| **真の可解性** | **可解**($z = z_-$ が $\Lambda(z) = (q_\theta,0)$ を満たす) | 同 |
| **正しい ob**(命題 OB-c6) | $(v_{u_2},v_{u_4}) = (0,0)$ ✓ | 同 |
| **manifest 式 (A) の ob** | $e(q_\theta) = a+b = (0,0,1,1,1,1)$ ⇒ $(\mathrm{ob}_a,\mathrm{ob}_b) = (1,1)$ ✗ | 同 |

> **⇒ manifest (10.2) を (A) で実装すると、可解な系を「$\mathrm{ob}\ne0$」と報告する。** 掃引の目的が「$\mathrm{ob}\ne0$ の系を探す」ことである以上、これは**偽陽性生成器**であり、**E15 反例の誤検出に直結する**。**発射前に必ず差し替えること。**
>
> なお $q_N = 0$ は E23b と両立する($0\in C^\sigma$)ので、この fixture は**人工的だが規約違反ではない**。実系で実現するかは別問題だが、**判定式の正しさは実現性に依存してはならない。**

---

## 5. mass check の判定基準(manifest fixture (iii) の実体・§3 の要求への回答)

証明書 `certificates/e2c6/` に対し、**すべて**を課す(どれか一つでも FAIL なら走行は無効):

| # | 基準 | 根拠 |
|---|---|---|
| **M1** | 系の総数 $= 64$、$m$ の重複なし・欠落なし | 事前登録宇宙 |
| **M2** | **postcondition: $(1-\sigma)q_N = 0$**(= E23b)を各系で再計算して検査 | 無条件命題ゆえ FAIL は実装バグの証拠 |
| **M3** | **postcondition: $(1-\theta)q_\theta = 0$**(= E23a)を各系で検査 | 同上 |
| **M4** | **postcondition: $v := q_\theta - 3^{-1}(1+\theta)q_N$ が $C^\theta$ に入る**($(1-\theta)v = 0$) | §2 の所属確認 |
| **M5** | $(1+\theta)\ker\mathcal N_C = \langle t_5+t_6, u_1+u_3\rangle$ を**各 $m$ で再計算**(表から独立に) | §3 の座標形の前提 |
| **M6** | 値重複度表: $(\mathrm{ob}_a,\mathrm{ob}_b)\in(\mathbb Z/2)^2$ の 4 値の重複度の総和 $=$ 線型段可解な系の個数 | 悉皆性 |
| **M7** | 線型段: 可解系には witness $\bar f$、不可解系には dual witness。**両者の和 $= 64$** | 三値判定 |
| **M8** | 肯定側は **群の積から** $\theta(f)f$ と $E_m\mathcal N(f)$ を再計算して $=1$ を直接確認(hash 不可・E22 §6.3 の規律) | W111 |

**M2–M5 が本質**: これらは**理論が無条件に予言する等式**なので、実装バグ・座標規約の取り違え・$m$ 依存の取りこぼしを**即座に露見させる**。とくに **M5 は「(A) を実装してしまった」場合に必ず FAIL する**(平均化射影を掛けた量は $(1+\theta)C_-$ を法として不変にならない)。

---

## 6. falsifier の三問への直接回答

| 問 | 回答 |
|---|---|
| **$(q_\theta)_+$ の正しい定義は?** | **どちらでもない。** 「$C^\sigma$ 成分を取る」という操作自体が障害群へ落ちないので、**式を差し替える**のが正解。正しい量は $v = q_\theta - 3^{-1}(1+\theta)q_N$ を $(1+\theta)\ker\mathcal N_C$ で法として読むこと。$j=2$ では **$u_2$ 係数と $u_4$ 係数**。 |
| **$q_\theta$ の所属の自動性は?** | $q_\theta\in C^\theta$ は**自動**(E23a・無条件)。$q_\theta\in C^\sigma$ は**成り立たない**(falsifier の指摘どおり)。だが (OB) は後者を必要としない。 |
| **(A)/(B) が分岐する fixture は?** | §4。しかも単なる分岐でなく **(A) が可解系で誤答する**反例。$q_\theta = t_5+t_6$、$q_N = 0$。 |

---

## 7. 【GAP】

| # | 内容 | 状態 |
|---|---|---|
| **【GAP-OB1】** | §3 の座標形は $j = 2$($R = \mathbb Z/2$)で悉皆検証した。**$j\ge3$ では $(1+\theta)C_-$ の構造が変わりうる**(とくに $\theta(a) = -a$ が $R = \mathbb Z/2$ では $+a$ に潰れる)。$j\ge3$ 用の座標形は未導出 | 中(本ゲートは $j=2$ のみなので射程内) |
| **【GAP-OB2】** | (E23a)(E23b) は自作 `命題_E23中心障害消滅_v1.md` の補題で、**Sol 未監査**(便 19 は E23 本体を扱ったが本委嘱の用途は新規) | 中 |
| **【GAP-OB3】** | $\theta\mathcal N_C\ne\mathcal N_C\theta$(§1)は確定表からの実測。**「なぜ class 6 で $S_3$ 関係が崩れるか」の構造的理由**($\sigma_m$ の $m$-捻れが $C$ に届く)は概略のみ | 低 |
| **【状態】** | 命題 OB・命題 OB-c6・§4 の反例・§5 の基準は **Opus 単系統・Sol 未監査**。検算 10/10 は node 単系統。**Sol 便 22 との突合が批准条件** | — |

---

## 8. 司令塔への提案

**P1(発射条件・最優先)**: manifest §「判定量」の (10.2) を **命題 OB の式に差し替える**まで発射しない。差し替え後、**§4 の偽陽性 fixture を反証 fixture (iv) として追加**(現行 (i)(ii)(iii) はこの誤りを検出できない — (i) は「ob ≠ 0 が発火すること」しか見ず、まさに偽陽性を PASS と誤認する)。

**P2**: mass check(fixture (iii))を §5 の M1–M8 で確定登録。**M5 は (A) 実装を必ず捕まえる**ので、実装差し替えの検査としても機能する。

**P3(★教材)**: **「class-5 の分解を class-6 へ持ち込むな」**。E23 の証明が $C_+\oplus C_-$ の成分読みに見えるのは、$C^\sigma = 0$ という**退化**のせいだった。一般には**商 $C^\theta/(1+\theta)\ker\mathcal N_C$ で読む**のが正しく、成分読みは $\theta$-同変性という**class 6 では成り立たない仮定**を密輸する。falsifier の「(q_θ)₊ が未定義」という指摘は、**この密輸の入口を正確に射抜いていた**。
