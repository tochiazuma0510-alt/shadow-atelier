# 【CP】TRIAD-972 発火の検問 — 公式の正当性・support{2} の読み・格と検証連鎖(裁定 1122)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1122([CP] 最優先)
入力 = cert `search/certs/triad972_r_measurement_v1_20260813.json`・`branchP_and_r_spec_v1.md`(r カード v2)+ §A 追記・`p8_prereg_v3_2.md`
生成 script(裁定 1103 規約)= `scratchpad/triad972_firing_check.py`(本書の全数値の出所)
⚠ $u$/$c$ 非接触。**格: candidate**(Sol 未監査)。★ **QUAR 発動対象**(§6)。

---

## §0 結論 — ★ **A/B 分離**(裁定 1123 の要請)

$$\boxed{\ \textbf{Part A(設問 4 と}\textbf{独立}\textbf{)}:\ \textbf{公式の正当性 — }[a]\ \textbf{の値に依存しない}\ }$$
$$\boxed{\ \textbf{Part B(設問 4 に}\textbf{完全に依存}\textbf{)}:\ \textbf{数値 }648\ \textbf{・P-K9U-1 の判定・UNRAM の反証}\ }$$

**Part A(独立に書ける・§1)**
1. ★ **設問 1 の答え = 公式は正当です。** $[a]=[3]^j$ を**仮定していません**。司令塔が急所とした「$d_9$ は 3-part のみ依存」の **"3-part" は指数 $18=2\cdot9$ の 3-準素部分**であって、**$\mathrm{supp}(a)$ の素数 3 とは別物**です(§1.1)。
2. ★ **$\mathrm{ord}([a])$ は公式の $d_9$ を実体化します**(§1.3)。しかも**測定値に対しては付値論法で証明でき**、**RES-INJ-9 も $\langle[a],[b]\rangle$ 上で直接証明できました**(§1.4)⟹ **前件が 2 本、仮定から定理へ**。
3. ⟹ 残る条件は **T63 鎖の 3 本 (i)(ii)(iii) と既知の前件束 (iv)** に完全集約(§1.5)。

**Part B(設問 4 の決着待ち・§2–§3)**
4. ⚠⚠ ★★★ **発火と予言外れは同一事象です**(§4.4・機械確認):
$$\boxed{\ [a]=3^j\ (\text{P-K9U-1 の予言})\ \Longrightarrow\ r=1\ \Longrightarrow\ \lvert X\setminus A\rvert=972-972=\mathbf 0\ (\textbf{非発火})\ }$$
⟹ **「予言が当たっていたら発火しなかった」**。両者は切り離せず、**設問 4 の決着が発火の生死をそのまま決めます**。
5. ⚠ **$\lvert X\setminus A\rvert=648>0$** ⟹ **QUAR 発火**。格は **candidate(条件つき)**。**Sol ゲート便スキップ不可**(§5・§6)。

$$\boxed{\ \textbf{「反例を得た」とは書きません}\ —\ 648\ \textbf{は}\textbf{個数}\textbf{であって witness の構成ではありません((Q8))}\ }$$

---

## §1 設問 1 — 公式は $[a]=[3]^j$ を仮定しているか ⟹ **していません**

### 1.1 ★★ 急所の解消 — 「3-part」の語の二義性

司令塔が唯一の急所とした一節(`branchP_and_r_spec_v1.md` §A.3)の**文脈**:

> §A.2: 自然な全射 $\mathrm{pr}:\mathbf Q^\times/(\mathbf Q^\times)^{18}\to\mathbf Q^\times/(\mathbf Q^\times)^{9}$ …
> §A.3 表: 「$\mathrm{pr}$ の核 = 位数 2 の部分(**2-part**)」/「$d_9\in\{1,3,9\}$ は **3-part のみ**に依存」

$$\mathbf Q^\times/(\mathbf Q^\times)^{18}\ \cong\ \bigoplus_p\mathbf Z/18\ \cong\ \underbrace{\bigoplus_p\mathbf Z/2}_{\textbf{2-part}}\ \oplus\ \underbrace{\bigoplus_p\mathbf Z/9}_{\textbf{3-part}}$$

$$\boxed{\ \textbf{「2-part / 3-part」は}\textbf{指数 }18=2\cdot9\ \textbf{の準素分解}\textbf{であって、}\mathrm{supp}(a)\ \textbf{の素数 2 / 3 ではありません}\ }$$

- $\mathrm{pr}$ の核 = $\bigoplus_p\mathbf Z/2$ の部分 ⟹ 「**符号と法 2 の情報**」が落ちる(§A.2 は $[-1]$ が法 9 で自明になることを言っている)。
- $d_9$ は 3 の冪 ⟹ **法 9 の情報だけで決まる** ⟹ 「$\mathrm{pr}$ で落ちる情報は $d_9$ に不要」。

⟹ ★ **測定値 $[a]=2^7$($\mathrm{supp}=\{2\}$)は、この文脈の「2-part」とは何の関係もありません。**「$[a]$ の 3-part が自明」という司令塔の言い方は、正確には「$\mathrm{supp}(a)$ に素数 3 が現れない」ですが、$d_9$ の定義はどの素数が台に現れるかに**依存しません**。

$$\boxed{\ \textbf{⟹ 干渉なし。急所は解消します}\ }$$

### 1.2 公式の導出が実際に使っているもの

$$\lvert A\rvert=12\cdot\frac{d_9\,d_{S4}}{r},\qquad d_9=[L_{9,\rm Aff}:\mathbf Q(\zeta_9)],\ d_{S4}=[L_{S4}:\mathbf Q(\zeta_9)],\ r=\lvert\langle[a]\rangle\cap\langle[b]\rangle\rvert$$

中核は **Kummer 理論の合成次数**です:
$$[L_{9,\rm Aff}\,L_{S4}:\mathbf Q(\zeta_9)]=\bigl\lvert\langle[a],[b]\rangle\bigr\rvert=\frac{\lvert\langle[a]\rangle\rvert\cdot\lvert\langle[b]\rangle\rvert}{\lvert\langle[a]\rangle\cap\langle[b]\rangle\rvert}=\frac{d_9d_{S4}}{r}$$
これは**アーベル群の 2 つの巡回部分群の積公式**で、**台がどの素数かに一切依存しません** ✔

**機械確認**(script): $\langle[a]\rangle=\langle(7,0)\rangle$ 位数 9、$\langle[b]\rangle=\langle(1,6)\rangle$ 位数 9、交わり $\{(0,0),(3,0),(6,0)\}$ ⟹ $r=3$(**cert と一致**)。$\lvert\langle[a],[b]\rangle\rvert=\mathbf{27}=9\cdot9/3$ ✔ しかも $\langle[a],[b]\rangle=\{2^m3^k:k\equiv0\ (3)\}$ と同定できました。

⟹ **公式が使うのは (i) Kummer 理論 (ii) $d_9,d_{S4}$ が $\mathbf Q(\zeta_9)$ 上の Kummer 次数であること (iii) $r$ が類の交わりの位数であること — の 3 つだけ**。$[a]=[3]^j$ は**どこにも入りません**。

### 1.3 ★★ $\mathrm{ord}([a])=9$ は公式の $d_9$ を**実体化します**(付値論法で証明)

司令塔の問い「$\mathrm{ord}([a])=9$ は公式の $d_9$ を実体化するのか、それとも別の量か」への答え:

$$d_9=[\mathbf Q(\zeta_9,a^{1/9}):\mathbf Q(\zeta_9)]=\mathrm{ord}\bigl([a]\ \text{in}\ K^\times/(K^\times)^9\bigr),\qquad K=\mathbf Q(\zeta_9)$$

測定は $\mathbf Q^\times/(\mathbf Q^\times)^9$ での位数 9。両者が一致するか(= RES-INJ-9)が問題ですが、**この $a$ については直接証明できます**:

> **【補題 D9-VAL】** $a=2^7$ とする。$\mathrm{disc}(\mathbf Q(\zeta_9))$ は 3 の冪 ⟹ **2 は $K$ で不分岐**($e=1$)。よって $\mathfrak P\mid2$ で $v_{\mathfrak P}(a)=7$。
> $a=c^9$ なら $9\mid7$(偽)、$a^3=c^9$ なら $9\mid21$(偽)⟹ $\mathrm{ord}_K([a])\ne1,3$ ⟹ $\boxed{\mathrm{ord}_K([a])=9=d_9}$ ∎

**独立の第 2 証明**(次数勘定): $x^9-2$ は Eisenstein ⟹ $[\mathbf Q(2^{1/9}):\mathbf Q]=9$。$[\mathbf Q(\zeta_9):\mathbf Q]=6$、$\gcd(9,6)=3$。$\mathbf Q(\zeta_9)$ の唯一の 3 次部分体は $\mathbf Q(\zeta_9)^+$(**アーベル**)、$\mathbf Q(2^{1/9})$ の唯一の 3 次部分体は $\mathbf Q(2^{1/3})$(**非 Galois**)⟹ 交わりは $\mathbf Q$ ⟹ 合成次数 54 ⟹ $d_9=9$ ✔

$$\boxed{\ \Longrightarrow\ \mathrm{ord}([a])=9\ \textbf{は「別の量」ではなく、公式の }d_9\ \textbf{そのものです}\ }$$
★ **副産物**: $d_9$ については **RES-INJ-9 を前件として要しません**(証明済み)。

### 1.4 ★ RES-INJ-9 が本当に要る場所と、そこでの直接証明

⚠ 公式の $d_9d_{S4}/r$ が**合成次数を与える**には、$\langle[a],[b]\rangle$ 全体が $K^\times/(K^\times)^9$ へ**単射**である必要があります(これが RES-INJ-9 の実効的な内容)。**これも直接証明できました**:

> $\langle[a],[b]\rangle$ の元は $2^m3^{3j}$($m\in\mathbf Z/9$, $j\in\mathbf Z/3$)。$K$ で 9 乗になるには
> (i) 2 は不分岐ゆえ $9\mid m$ ⟹ $m=0$;
> (ii) 残る $3^{3j}$ が 9 乗 $\iff 3^{1/3}$ または $9^{1/3}\in\mathbf Q(\zeta_9)$。$\mathbf Q(\zeta_9)/\mathbf Q$ はアーベル、$\mathbf Q(3^{1/3})/\mathbf Q$ は非 Galois ⟹ **含まれない**。
> ⟹ 核は自明 ⟹ $[L_{9,\rm Aff}L_{S4}:\mathbf Q(\zeta_9)]=27$ ∎

$$\boxed{\ \textbf{⟹ 前件 A4 のうち RES-INJ-9 は、本測定値に対しては}\textbf{仮定でなく定理}\ \textbf{になりました}\ }$$

### 1.5 ⚠ 残る前件(公式のうち私が検証していない部分)

| # | 前件 | 状態 |
|---|---|---|
| **(i)** | $\lvert X\rvert=972$(972 屋根の計数) | ⚠ **T63 鎖に依存・本書では未検証** |
| **(ii)** | 係数 $12$ の出所(円分因子 $\times$ ?) | ⚠ **T63 鎖に依存・本書では未検証** |
| **(iii)** | $A$ が $\lvert A\rvert=12\cdot[\,L_9L_{S4}:\mathbf Q(\zeta_9)\,]$ の形になること | ⚠ **T63 鎖に依存・本書では未検証** |
| **(iv)** | P1–P5(特に P5: $u_0=u_{S4}$)・$i\notin L_{S4}$・R3-GAP-4/5 | ⚠ **既知の条件つき**(r カード [0] A4) |
| (v) | Kummer 積公式と $d_9$ の実体化 | ★ **本書で証明**(§1.2–1.4) |

$$\boxed{\ \textbf{⟹ 発火は正当。ただし「条件つき」の中身は }(i)(ii)(iii)(iv)\ \textbf{に完全に集約されました}\ }$$
★ **これは進歩です**: 従来 5 本あった不確定要素のうち、**Kummer 側(v)は完全に閉じました**。残るのは **T63 鎖の 3 本と既知の前件束**だけです ⟹ **Sol 監査の照準がここに絞られます**(§5)。

---

## §2 設問 2 — $\mathrm{supp}(a)=\{2\}$ の読み

### 2.1 P-K9U-1 の落ち方

P8 v3.2 の S-1: $L_{9,\rm Aff}=\mathbf Q(\zeta_9,\sqrt[9]{3})\iff$ `support==[3]` **かつ** `order==9`。
測定: `support=[2]`・`order=9` ⟹ **support 条件で不成立** ⟹ **P-K9U-1 は外れ**(§5 (u2) 枝の事前登録どおり)。

★ **凍結の設計が効きました**: v3.2 は「support だけで判定しない(位数 9 の前件も要る)」と修理してありましたが、**今回は support の方で落ちた**ので、修理の有無に関わらず判定は同じでした。⚠ ただし**修理は無駄ではありません** — support が $\{3\}$ で位数 3 だった場合(v3.1 なら誤って的中と判定した)への保険は依然有効です。

### 2.2 得られた体

$\gcd(7,9)=1$ ⟹ $\langle[2^7]\rangle=\langle[2]\rangle$ ⟹
$$\boxed{\ L_{9,\rm Aff}=\mathbf Q\bigl(\zeta_9,\ 2^{7/9}\bigr)=\mathbf Q\bigl(\zeta_9,\ 2^{1/9}\bigr),\qquad [L_{9,\rm Aff}:\mathbf Q]=54\ }$$

### 2.3 ★★ 決定的な帰結 — (K9-UNRAM) の目標は**反証されます**

$x^9-2$ は $\mathbf Q_2$ 上 Eisenstein ⟹ **2 で完全分岐(次数 9)**。よって

$$\boxed{\ L_{9,\rm Aff}\ \textbf{は 2 で分岐する}\ \Longrightarrow\ \textbf{「}S_{9,\rm Aff}\subseteq\{3\}\textbf{」(= 3 の外で不分岐)は}\textbf{偽}\ }$$

⚠ **UNRAM 線の目標そのものが落ちました**。これは `win83_audit_and_unram3_v1.md` II.1 の
> **(K9-UNRAM) の正しい形**: $S_{9,\rm Aff}\subseteq S$ であって $\subseteq\{3\}$ ではない

という私の再設計の警告が**現実になった**形です。★ **さらに**: 同 II.2 の「路 β が当たれば $S\subseteq\{2,3\}$ ⟹ K9-C2 と合わせて $p=2$ は $\mathbf Q(i)$ 由来と分離できる」という筋も**破れます** — 2 の分岐は $C_2$ 因子($\mathbf Q(i)$)由来ではなく **$L_{9,\rm Aff}$ 自身**にあるからです。
⟹ **【UNRAM-GAP-4/5】は、目標が変わったので棚卸しが必要**(新しい正しい目標 = 「$S_{9,\rm Aff}=\{2,3\}$ を確定する」)。

### 2.4 機構の出所(★ candidate・W-50 検疫つき)

「なぜ 2 が order 9 を担うのか」への私の見立て:

$u_9=\lim\lambda_9\,s^{-18}$ の先頭係数は、宣言モデルの構造定数から来ます。$\mathbf Q$-モデルには **2 が構造的に埋まっています**:
- $\rho=27/2$(`u32_global_model_spec_v1.md` §3.1 で私が示したとおり、$\lambda^3=1/2$ が $\mathbf Q$ 上不可能なので **$w$ の有理再スケールでは 2 を消せません**)
- $t=-Y^2/4$(分母 4)
- $\Delta(E)=-216=-2^3\cdot3^3$

⟹ ★ **仮説 SUPP2**: $v_3(u_9)\equiv0\pmod9$(27 の冪が 9 乗に吸収される)かつ $v_2(u_9)\equiv2\pmod9$(⟹ $v_2(a)=-2\equiv7$)。

$$\boxed{\ \textbf{検証法(安い)}:\ \textbf{cert に }v_2(u_9),v_3(u_9)\ \textbf{を記録し、上の合同が成り立つか見る}\ }$$
⚠ **W-50 検疫**: 「モデルに 2 がある」と「$a$ の台が $\{2\}$」の一致は**現時点では観察**であり、機構の証明ではありません。★ **上の合同の実測が通って初めて機構と呼べます**。私は**ここで止めます**。

---

## §3 設問 3 — $\lvert X\setminus A\rvert=648$ の意味

### 3.1 数の再導出(機械)

$$\lvert A\rvert=12\cdot\frac{9\cdot9}{3}=12\cdot27=324,\qquad \lvert X\setminus A\rvert=972-324=\mathbf{648},\qquad \frac{\lvert A\rvert}{\lvert X\rvert}=\frac13$$

★ **独立の整合**: `ideas_surg_boost_v1.md` §65 が「指数 3 なら 648・指数 9 なら 864」と**先に**書いていました。私の $r$ 依存表と**完全一致**:

| $r$ | $\lvert A\rvert$ | $\lvert X\setminus A\rvert$ |
|---:|---:|---:|
| 1 | 972 | **0**(非発火・唯一の枝) |
| **3** | **324** | ★ **648** |
| 9 | 108 | 864 |

⟹ **発案係の予測表と測定が一致**(別経路の整合 1 本)。

### 3.2 意味(★ 過剰主張を避けた形)

$$\boxed{\ \textbf{972 屋根 }M=K^{(9)}\cap N_{S4}\ \textbf{において、算術像に入らない shadow が }\mathbf{648}\ \textbf{個ある(条件つき)}\ }$$

- ★ **これは「非算術 shadow の存在」の初の肯定的証拠**(工房史上)。従来はすべて UNKNOWN か陰性でした。
- ⚠ **witness ではありません**((Q8))。個数が出ただけで、**具体的な $[m,f]$ は 1 個も名指しできていません**。
- ⚠ **条件つき**: §1.5 の (i)(ii)(iii)(iv)。特に **972 と 12 の出所(T63 鎖)は私は検証していません**。
- ⚠ **型境界**: これは $M$ **屋根**の話で、$K^{(9)}$ 単独や $N_{S4}$ 単独の言明ではありません。**(r4) の射程 = 972 屋根に限る**(P8 v3.2 S-4)。

### 3.3 格の指定(私の推薦)

| 対象 | 推薦する格 |
|---|---|
| $r=3$・$\langle[a],[b]\rangle=27$・Kummer 積公式 | ★ **cross-checked に近い**(cert + 私の独立再導出 + $[b]$ の三重独立導出) |
| $d_9=9$・RES-INJ-9 on $\langle[a],[b]\rangle$ | ★ **candidate(証明つき)**(§1.3–1.4・紙 2 本 + 機械) |
| $L_{9,\rm Aff}=\mathbf Q(\zeta_9,2^{1/9})$・2 で分岐 | ★ **candidate(証明つき)** |
| **$\lvert X\setminus A\rvert=648$** | ⚠ **candidate(条件つき)** — T63 鎖 (i)(ii)(iii) と前件 (iv) に懸かる |
| 「非算術 shadow が存在する」 | ⚠ **candidate(条件つき)・verified でも cross-checked でもない** |

---

## §4 ★★ 設問 4 — ゲージ不変性(裁定 1123・研究者起点)

### 4.1 (i) uniformizer の取り替えについては **証明できます**

> **【補題 GAUGE-18】** $s,s'$ を $P_0$ の **$F$-有理 uniformizer** とする。$c_1:=\lim_{s\to0}(s'/s)\in F^\times$ とおくと $s'^{18}=c_1^{18}s^{18}(1+O(s))$ ゆえ
> $$u_9'=\lim\lambda_9\,s'^{-18}=u_9\cdot c_1^{-18}$$
> ⟹ $[u_9]\in F^\times/(F^\times)^{18}$ は **uniformizer の取り替えで不変**。したがって $[a]\in F^\times/(F^\times)^{9}$ も不変。∎

$$\boxed{\ \textbf{⟹ uniformizer 由来のゲージ自由度は}\textbf{ゼロ}\ }$$
★ 私が `u32_global_model_spec_v1.md` §4 で出した 2 本($s=w$ と $s'=X/w^2$)は**同じ $[a]$ を出すはず** ⟹ **T63-UNIF-INV はまさにこれを検定します**。⚠ 前提は「両方が $F$-有理」— 有理でない uniformizer を使うと $c_1\notin F^\times$ で保証が消えます(spec [U-4](W-c) がその見張り)。

### 4.2 (ii) 残る唯一のゲージ = **$\lambda_9$ の Belyi 正規化**

$t\mapsto\alpha t$($\alpha$ 定数)で $u_9\mapsto\alpha u_9$ ⟹ $[a]\mapsto[a]\cdot[\alpha]^{-1}$。**これが唯一のゲージ自由度**です。

★ **しかし $\alpha$ は自由ではなく、Belyi 条件で固定されます**: 分岐値が**ちょうど** $\{0,1,\infty\}$ であること。検証可能な形は
$$\boxed{\ t(B_1)=t(B_2)=1\ }$$
$t=-Y^2/4$、$B_i$ は $Y=\pm2i$ ⟹ $t=-(-4)/4=1$ ✔ — **私が独立に検算済**(`r2r3_model_invariants.py` 系)。

$$\boxed{\ \Longrightarrow\ \textbf{spec の }t\ \textbf{は正しく正規化されており、定数の自由度は残っていません}\ }$$

⚠ **重要な区別**: 経路の定数($\rho=27/2$・Chart 1 の先頭係数 2・$\lambda_9$ 先頭係数 $-1/16$)は **$u_9$ の正しい値の一部**であって「ずれ」ではありません。ずれになるのは **spec と違う $t$ を使ったときだけ**です。

### 4.3 (iii) 単数混入の具体形と guard

| 単数 | $[\cdot]$ 法 9 | 危険度 |
|---|---|---|
| $\pm1$ | $-1=(-1)^9$ ⟹ **自明** | ✔ 無害 |
| $\zeta_3,\zeta_6,\zeta_{12}$ | $\mathbf Q(\zeta_3)^\times/(\cdot)^9$ で**非自明**($b^9=\zeta_3$ の解は 27 乗根 ⟹ $\mathbf Q(\zeta_3)$ 外) | ⚠ **危険** |

⚠ **$\zeta_3$-モデルで計算すると混入しえます**($A_0^{(\zeta_3)}=\zeta_3^2A_0^{(\mathbf Q)}$ 等)。混入すれば $[u_9]$ は $\mathbf Q^\times$ に**降りなくなり**、**DESC-9 の (D-ii) 有理性検査が fail-closed guard として働きます**。

$$\boxed{\ \textbf{推薦: }\mathbf Q\textbf{-モデル(}E_{\mathbf Q},W_{\mathbf Q},t=-Y^2/4\textbf{)で計算すれば }\zeta\ \textbf{混入は}\textbf{構造的に起きません}\ }$$

### 4.4 ★★★ (iv) どのずれなら観測を説明するか — **感度表**(機械・script)

| 仮定した $[a]$ | $\mathrm{ord}$ | $r$ | $\lvert X\setminus A\rvert$ |
|---|---:|---:|---:|
| **観測** $2^7$ | 9 | **3** | **648** |
| **P-K9U-1** $3^1$ / $3^2$ / $3^4$ | 9 | **1** | ★ **0(非発火)** |
| 2 冪ずれ $2^1$ / $2^4$ | 9 | 3 | 648(**不変**) |
| 混合 $2^7\cdot3^3$ | 9 | 3 | 648(**不変**) |
| 混合 $2^1\cdot3^6$ | 9 | 9 | **864** |

**読み**:
- ★ **純 2 冪のずれは 3-part を動かしません** ⟹ 「真の $[a]$ が $3^j$ なのに $2^k$ を掛けて $2^7$ に見えた」は **不可能**(3-part が残るはず)⟹ **研究者の懸念の最も素直な形は否定されます**。
- ⚠ **生きている唯一のバグ仮説は「混合 $2^a3^b$ の定数ずれ」**です。経路の定数はすべて $\pm2^a3^b$ 型なので、原理的には起こりえます。
- ★ ただし §4.2 のとおり、その定数は **Belyi 正規化で固定**され、その正規化は**検算可能で私は検算済**です。⟹ **spec どおりに実装されていれば、ずれはありません**。
- ★★ **発火の頑健性**: 2 冪方向のずれに対し **648 は不変**でした ⟹ 発火の結論は「$[a]$ の 2-part の**存在**」に依存し、その**指数の値**には依存しません。

### 4.5 第三系統への具体的要請(5 点)

```
1. Belyi 正規化の fail-closed :  t(B_1) = t(B_2) = 1 を厳密に確認
2. GAUGE-18 の実測          :  s = w と s' = X/w^2 の 2 本で [a] が一致するか
3. u_9 を *厳密元* として報告 :  単数因子(±1, zeta_k)込みで。類だけにしない
4. DESC-9 (D-ii) の実行有無と結果を明記(有理性検査が通ったか)
5. ★ Q-モデルで計算する      :  zeta 混入を構造的に排除(u32_global_model_spec §0)
```

### 4.6 ⚠ 私の判定(紙側)

$$\boxed{\ \textbf{(i) は証明済(補題 GAUGE-18)。(ii) の「正しいゲージ」は }t\ \textbf{の Belyi 正規化が固定し、それは検算済}\ }$$
⟹ **紙の側にゲージの穴は見つかりませんでした**。⚠ ただし**実装が spec どおりかは私には検証できません** — そこは第三系統の職掌です。
⚠⚠ **そして §0-4 のとおり、$[a]$ が動けば発火そのものが消えます**($3^j$ なら 0)⟹ **第三系統の結果が出るまで、Part B は一切流通させないでください**。

---

## §4′ 検証連鎖の設計(定理候補級)

```
[V-1] T63 鎖の再検分(★ 最優先・私は未検証)
      (a) |X| = 972 の出所と導出
      (b) 係数 12 の出所
      (c) |A| = 12 * [L_9 L_S4 : Q(zeta_9)] の導出
      ⟹ この 3 本が閉じれば 648 は「前件 (iv) のみに条件づく」まで上がる
[V-2] 前件 (iv) の状態転記(主張せず状態を写す)
      P5(u_0 = u_S4)・i not in L_S4・R3-GAP-4/5
[V-3] 機構 SUPP2 の検定(安い): cert に v_2(u_9), v_3(u_9) を追記
      ⟹ v_3 = 0 mod 9 かつ v_2 = 2 mod 9 なら機構が実体化
[V-4] UNRAM 線の棚卸し: 目標を「S_{9,Aff} ⊆ {3}」から「S_{9,Aff} = {2,3} の確定」へ
      ⟹ U3-3 の再設計(【UNRAM-GAP-4/5】の射程も変わる)
[V-0] ★ 最優先: [a] の第三系統再導出(§4.5 の 5 点)
      ⟹ [a] が動けば r も 648 も動く。Part B は全てこれ待ち
[V-5] Sol ゲート便(便 124 筆頭・スキップ不可)
      監査対象: §1 の公式正当性・§1.3/1.4 の 2 補題・§4 のゲージ論・§3.2 の書き方・格
```

---

## §5 QUAR 発動(r カード v2 [4]・8 要件)

$\lvert X\setminus A\rvert=648>0$ ⟹ **発火**。

| # | 要件 | 状態 |
|---|---|---|
| **Q1** | 即時隔離・流通禁止 | ⟹ **司令塔へ要請**(本書と cert を隔離枠へ) |
| **Q2** | 前件 A1–A4 の再検査 | ★ **A1 充足**($[a]$ が類として出た)/**A4 の RES-INJ-9 は §1.4 で証明**/残 = §1.5 (i)–(iv) |
| **Q3** | falsifier 独立判読 | ⟹ **要請**(特に §1.1 の語の二義性と §1.3 の付値論法) |
| **Q4** | Sol 監査請求 | ⟹ **便 124 筆頭・スキップ不可** |
| **Q5** | 研究者報告 | ⟹ **要請** |
| **Q6** | 三値の出所を各々明記 | $d_9=9$(R-3 出力 → §1.3 で証明)/$d_{S4}=9$(S4-RECON・前件 P5)/$r=3$(本書 §1.2 で再導出) |
| **Q7** | 型境界検問 | ★ **本書 §1.1 がまさにそれ**(法 9/18・「2-part」の二義性)。窓の取り違えなし(972 屋根限定・§3.2) |
| **Q8** | 「反例を得た」と書かない | ★ **遵守**(§0・§3.2) |

---

## §6 記帳

- ★ **本書の新規部分**: ① ★★ **「2-part/3-part」の語の二義性の解消**(指数 18 の準素分解 vs 台の素数)⟹ 急所が消える ② 公式が使うのは Kummer 積公式のみで台に依存しないことの明示 ③ ★ **補題 D9-VAL**($d_9=9$ を付値で証明・RES-INJ-9 不要)+ 次数勘定による独立第 2 証明 ④ ★ **RES-INJ-9 を $\langle[a],[b]\rangle$ 上で直接証明**(前件が定理になった)⑤ 残る条件の (i)–(iv) への完全集約 ⑥ ★★ **(K9-UNRAM) の目標の反証**($L_{9,\rm Aff}$ は 2 で分岐)⑦ 仮説 SUPP2 と安い検定法(W-50 検疫つき)⑧ 発案係の 648/864 予測表との一致 ⑨ 検証連鎖と QUAR 発動。
- **【r-GAP-1】** ⟹ 本測定では **DESC-9 が不要**でした($u_9$ が $\mathbf Q$ 上・§`r2_r3_unram_execution_spec_v1` §6 の予告どおり)。
- **【UNRAM-GAP-4/5】** ⟹ **目標変更により棚卸しが必要**(§2.3)。
- ⚠ **私が検証していないもの**: $\lvert X\rvert=972$・係数 12・$\lvert A\rvert$ の形(T63 鎖)。**これらは Sol 監査の主対象にしてください**。
- ★ **設問 4 の新規部分**: ⑩ **補題 GAUGE-18**(uniformizer 取り替えでの類の不変性・3 行)⑪ 唯一のゲージ = $\lambda_9$ の Belyi 正規化で、それは $t(B_i)=1$ で**検算可能・検算済** ⑫ $\zeta$ 単数混入の危険と **$\mathbf Q$-モデル推奨**(構造的排除)⑬ ★★ **感度表** — 純 2 冪ずれでは観測を説明できない/648 は 2 冪方向に**不変** ⑭ ★★★ **発火と予言外れが同一事象**($[a]=3^j$ なら $r=1$・非発火)。
- **申告**: python(`scratchpad/triad972_firing_check.py`・整数演算のみ)+ 紙。本書の全数値は機械生成(裁定 1103 規約)。$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
