# 凍結予言 — $r=4$ 判別窓($\bar x=(5,5,5,5)$・$n=20$)**v1**

**状態札: candidate(裁定前・未 commit・未凍結)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-30
設問: 司令塔委嘱(裁定 231)。**凍結は司令塔が commit で行う** — 本稿は起草のみ。
前提: `docs/notes/pruning_law_v1.md`(PRUNE・系 PRUNE-1)/ `docs/notes/pruning_law_v1_1.md`(撤回記帳・格付け・補題 NORM-E・NORM の二分)/ `search/certs/r4_exhaustive_20260730.json`(実現の悉皆決定)/ `sol/sol_reply_86_math13.md` F86-4.2.2-3
番号系: 本稿の committed 欄は **`P-R4-*`**(`P-STR-*`・`P-A13-*`・`P-I10-*` と衝突しない)

> ## 接触の申告
> 本稿執筆時点で、この 2 窓に judge は一度も向けられていない。$\bar x$ が **$r=4$**($N_{\rm ord}=5$・$t=0$)の窓の GT-shadow 測定値は工房に存在しない。
> 私が見た $r=4$ の情報は `r4_exhaustive_20260730.json` の**実現対の存在と生成群のみ**(shadow は 1 個も見ていない)。
> ## 封印遵守
> 有限群論と初等加群論のみ。分岐データは $\mathsf w:=b_1^{-1}a_1$、$\bar x=\mathsf w^2$。

---

## 0. なぜ $r=4$ が決定打か(1 段落)

$\mathrm{Syl}_2(S_r)$ の $r$ ブロックへの軌道数は $s_2(r)$($r$ の 2 進桁和)であり、$s_2$ は **$r$ について単調でない**。$r=1,2,3$ では $s_2=1,1,2$ で、撤回済の $\ell^{r-1}$ 律($0,1,2$)と $r=2,3$ だけ一致してしまう。**$r=4$ で初めて割れる**: $s_2(4)=1$ ⟹ PRUNE は $\ell^1=5$、$\ell^{r-1}$ は $\ell^3=125$ — **25 倍差**。
機構は $\mathrm{Syl}_2(S_4)=D_8$ が **4 ブロックに推移的**であること。ゆえに $B^S$ は**全対角 $\langle\bar x\rangle$ ちょうど**に潰れる。

> ### 【本窓では機構が周辺群の水準で既に確認できている】
> $\mathrm{Stab}=C_{S_{20}}(\bar x)=C_5\wr S_4$(位数 15000)、$S:=\mathrm{Syl}_2(\mathrm{Stab})\cong D_8$(位数 8)、$B_x=C_5^4$(位数 625)に対し
> $$C_{B_x}(S)=C_5=\langle\bar x\rangle\qquad(\textbf{機械確認・}\lvert\cdot\rvert=5)$$
> — これは**周辺群の計算**であって shadow の測定ではない。予言はこの $C_{B_x}(S)$ が**核の奇部として実現するか**を問う。

---

## 1. 対象 — 2 枝の窓

`r4_exhaustive_20260730.json` の悉皆決定(構造定数先行 + 全非零セル 15/15 の $C_{S_{20}}(\mathsf w_0)$-軌道分解・77,425 解)より、$\bar x=(5^4)$ を与える実現対は **2 セルにのみ**存在する:

| 枝 | $\mathsf w_0$ 型 | $k$ | $j$ | $\mathrm{sign}(\mathsf w_0)$ | $\varepsilon$ | $\langle a_1,b_1\rangle$ | structconst | 軌道数 |
|---|---|---|---|---|---|---|---|---|
| **B** | $(10,5,5)$ | 9 | 6 | $-1$ | **1** | $S_{20}$ | 13,000 | 28 |
| **C** | $(10,10)$ | 8 | 6 | $+1$ | **0** | $A_{20}$ | 20,500 | 118 |

(type-A $\mathsf w_0=(5,5,5,5)$ は $\mathrm{ord}(\mathsf w_0)=5<7$ で双曲性が落ち、実際 $A_{20}/S_{20}$ 解ゼロ ✓ 系 0.4 と整合。)

### 1.1 canonical ID(fail-closed・最初の assert)

canonical 文字列 $=$ `<ID>|n=<n>|ell=<ell>|r=<r>|t=<t>|a1=<perm>|b1=<perm>|S1=<perm>|S2=<perm>`(GAP 印字形・UTF-8)。**I10-1 の spec と同一書式**。

| 窓 | SHA-256 |
|---|---|
| `W-E-A20-5x4t0-B` | `093b8b32d239de2a363b170b692e3f72ab3e9433d403e1587d54fef2eb54b586` |
| `W-E-A20-5x4t0-C` | `d49d2556efa837b5f811072c42b06271ffab900f7240319ad87c000041ccdb84` |

**canonical 対の選択規則(LID-1 準拠)**: 凍結証明書 `r4_exhaustive_20260730.json`(それ自体が hash される)の該当セルの `orbit_reps` 配列で、`eq_S20`(B 枝)/ `eq_A20`(C 枝)が最初に `true` になる代表。**同一性は序数ではなく literal な置換語 + 上の SHA** が担う(裁定 171 の処方)。

### 1.2 `W-E-A20-5x4t0-B`($\varepsilon=1$・ファイバー積・$S_{20}$)

```gap
a1 := ( 1,15)( 3,14)( 4, 5)( 6,13)( 7,20)( 8, 9)(10,19)(11,18)(12,16);;   # 2^9 1^2   k=9
b1 := ( 1,14, 2)( 3,13, 5)( 6,12,20)( 7,19, 9)(10,18,15)(11,17,16);;      # 3^6 1^2   j=6
## w := b1^-1*a1 = (1..10)(11..15)(16..20)   ord 10 ;  xbar = w^2 = (5,5,5,5)  ord 5
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15)(16,17,18,19,20)(21,22);;
JUDGE_S2_IMG := ( 1,18,16, 6, 3)( 2,14, 5, 4,13,20, 9, 8,19,15)( 7,12,17,11,10)(22,23);;
JUDGE_ID := "W-E-A20-5x4t0-B";;   ## degree(E) = 23
```

### 1.3 `W-E-A20-5x4t0-C`($\varepsilon=0$・直積・$A_{20}$)

```gap
a1 := ( 1,14)( 2,15)( 3,10)( 5, 9)( 6, 7)(12,19)(13,16)(17,18);;          # 2^8 1^4   k=8
b1 := ( 1,13,15)( 2,14,10)( 3, 9, 4)( 5, 8, 7)(11,20,19)(12,18,16);;      # 3^6 1^2   j=6
## w := b1^-1*a1 = (1..10)(11..20)   ord 10 ;  xbar = w^2 = (5,5,5,5)  ord 5
JUDGE_S1_IMG := ( 1, 2, 3, 4, 5, 6, 7, 8, 9,10)(11,12,13,14,15,16,17,18,19,20)(21,22);;
JUDGE_S2_IMG := ( 1, 2,13,18,17,12,20,11,19,16)( 3,14,15,10, 4, 9, 7, 6, 8, 5)(22,23);;
JUDGE_ID := "W-E-A20-5x4t0-C";;   ## degree(E) = 23
```

### 1.4 窓 assert(両窓・機械確認済・`r4_window.g`)

| 項目 | B 枝 | C 枝 |
|---|---|---|
| $a_1^2=b_1^3=1$ | ✓ | ✓ |
| $\langle a_1,b_1\rangle$ | $S_{20}$($2.43\times10^{18}=20!$)✓ | $A_{20}$($1.22\times10^{18}=20!/2$)✓ |
| $\mathsf w$ 型 / $\mathrm{ord}$ | $(10,5,5)$ / **10** | $(10,10)$ / **10** |
| $\bar x=\mathsf w^2$ 型 / $\mathrm{ord}$ | $(5,5,5,5)$ / **5** | $(5,5,5,5)$ / **5** |
| braid $s_1s_2s_1=s_2s_1s_2$ | **true** | **true** |
| $c=(s_1s_2)^3$ | **$=1$**(**$c\in N$**) | **$=1$** |
| $\mathrm{ord}(s_1)$ | 10 | 10 |
| $\lvert E\rvert=[B_3:N]$ | $7{,}298{,}706{,}024{,}529{,}920{,}000=6\lvert A_{20}\rvert$ ✓ | 同左 ✓ |
| $P=\langle\bar x,\bar y\rangle$ | $\lvert P\rvert=\lvert A_{20}\rvert$ ✓ | ✓ |
| $\mathrm{ord}(\bar x),\mathrm{ord}(\bar y),\mathrm{ord}(\bar c)$ | $5,5,1$ ⟹ $N_{\rm ord}=5$ | 同左 |
| $[P,P]=P$(charming の $f$ 条件が空虚) | ✓ | ✓ |
| charming $m$ / $c_m$ | $\{0,1,3,4\}$ / $4=\varphi(10)$ | 同左 |

> ### 【実装上の必須注意】B 枝は $\varepsilon=1$ = **ファイバー積**
> $\mathrm{sign}(a_1)=-1$、$\mathrm{sign}(b_1)=+1$。$E=S_3\times_{C_2}S_{20}\subsetneq S_3\times S_{20}$。
> **`E = DirectProduct(S3,S20)` と比較する assert を書いてはならない**(`wac_tail8_v1.md` §3.3【assert の訂正】と同型の事故)。正しい assert は $\lvert E\rvert=6\lvert A_{20}\rvert$・$\lvert P\rvert=\lvert A_{20}\rvert$・$E=\langle a_1(21,23),\,b_1(21,23,22)\rangle$。
> C 枝は $\varepsilon=0$ で $E=A_{20}\times S_3$(直積)。**同じ driver で両方を扱うので、この 1 行の分岐を落とさないこと。**

### 1.5 周辺群と予算(両枝で完全に同一)

| 項目 | 値 |
|---|---|
| $\mathrm{Stab}_{\mathrm{Aut}(P)}(\bar x)=C_{S_{20}}(\bar x)$ | $C_5\wr S_4=C_5\times((C_5^3){:}S_4)$、**15,000** |
| $C_P(\bar y)$ | **7,500** |
| $N_{S_{20}}(\langle\bar x\rangle)$ | **60,000** |
| $S:=\mathrm{Syl}_2(\mathrm{Stab})$ | $\boldsymbol{D_8}$、位数 **8** |
| $B_x$($\bar x$ の 4 巡回が生成) | $C_5^4$、**625**。$\bar x=$ 全対角 ✓ |
| **$C_{B_x}(S)$** | $\boldsymbol{C_5=\langle\bar x\rangle}$、**5**($D_8$ が 4 ブロックに推移的) |
| $Q\le(\mathbf Z/5)^\times$ | $\le C_4$。**$Q_2$ は常に巡回(階数 1)** |
| **$\Xi$ 走査数** $=c_m\lvert C_P(\bar y)\rvert\lvert\mathrm{Stab}\rvert$ | $4\times7500\times15000=\mathbf{450{,}000{,}000}$ |
| 素の経路 $c_m\lvert[P,P]\rvert$ | $4.87\times10^{18}$(**不能** — 較正ゲートは張れない) |

**2 窓合計 $\Xi=9\times10^8$。** A19-13t6($5.3\times10^8$)と同オーダー。

---

## 2. パリティ会計(裁定 209 の恒久項目)

補題 1.2(`i10_1_prediction_v1.md` §1.2)より、$\bar x=(\ell^r,1^t)$ 型では $\mathsf w$ の $\ell$-部は「$p$ 個の $2\ell$-巡回 + $(r-2p)$ 個の $\ell$-巡回」、$\mathrm{sign}(\mathsf w)=(-1)^{p+m_2}$、$k\equiv p+m_2\pmod2$。

| 窓 | $p$ | $m_2$ | $k$ | $\mathrm{sign}(a_1)$ | $\mathrm{sign}(\mathsf w)=(-1)^{p+m_2}$ | 一致 | $\varepsilon$ | $\langle a_1,b_1\rangle$ | $E$ |
|---|---|---|---|---|---|---|---|---|---|
| B | 1 | 0 | 9 | $-1$ | $-1$ | ✓ | 1 | $S_{20}$ | ファイバー積 |
| C | 2 | 0 | 8 | $+1$ | $+1$ | ✓ | 0 | $A_{20}$ | 直積 |

**両パリティ枝が同時に実在する初の族**(梯子は $t$ ごとに片枝のみ、I10-1 は $t=0$ ゆえ両窓とも奇枝)。これが §3.4 の「$\varepsilon$ 依存性」欄を可能にする。

**Ree 台帳(両枝とも等号・種数 0)**

| 窓 | $c(a_1)+c(b_1)+c(\mathsf w)$ | $n+2$ | 種数 |
|---|---|---|---|
| B | $11+8+3=22$ | 22 | **0** |
| C | $12+8+2=22$ | 22 | **0** |

$p=2$ 枝は最小型では余裕 2($10+8+2=20$)だが、**実現しているのは $k=8$ の等号配置**である(悉皆の結果)。$k=10$ セル(type-C, $k=10$)は $A_{20}/S_{20}$ 解ゼロ。

---

## 3. committed 欄(`P-R4-0` … `P-R4-11`)

### 3.0 判別表(先出し)

$S':=$ 実測される $\Xi(\ker\widetilde\chi)$ の 2-部、$B=C_5^4$ とする。**「$\ker=C_B(S')\times S'$」という形**を仮定すると、$S'\le\mathrm{Syl}_2(S_4)=D_8$ の共役類ごとに値が決まる:

| $S'$($4$ ブロックへの作用) | ブロック軌道数 | $\lvert C_B(S')\rvert$ | $\lvert S'\rvert$ | $\lvert\ker\rvert$ |
|---|---|---|---|---|
| **$D_8$(推移)** | 1 | **5** | 8 | **40** ← **PRUNE** |
| $C_4$(推移) | 1 | 5 | 4 | 20 |
| $V_4=\langle(12)(34),(13)(24)\rangle$(推移) | 1 | 5 | 4 | 20 |
| $\langle(12),(34)\rangle$ | 2 | 25 | 4 | 100 |
| $\langle(12)(34)\rangle$ | 2 | 25 | 2 | 50 |
| $\langle(12)\rangle$ | 3 | 125 | 2 | 250 |
| $1$ | 4 | 625 | 1 | 625 |

> ### 重要(形そのものの反証条件)
> 撤回済 $\ell^{r-1}$ 律の予言(奇部 $125$・2-部 $8$・$\lvert\ker\rvert=1000$)は、**上の表のどの行にも無い**。
> 理由: 奇部 $125$ はブロック軌道数 3 を要し、そのような $S'\le S_4$ は位数 $\le2$ しかない。ゆえに $(125,8)$ は **$\ker=C_B(S')\times S'$ という形そのものを壊す**。

### 3.1 committed 欄

> ### P-R4-0(窓同定・fail-closed)
> $$\boxed{\ \text{canonical ID SHA-256 が §1.1 の表と一致し、§1.4 の窓 assert が全項 PASS}\ }$$
> **FAIL なら以降を撃たない。** B 枝のファイバー積 assert(§1.4 の注意)を含む。

> ### P-R4-1(**主判別**・核の位数)
> $$\boxed{\ \lvert\ker\widetilde\chi\rvert=\mathbf{40}\quad(\text{B 枝・C 枝とも})\ }$$
> PRUNE: $\lvert C_{B}(S)\rvert\cdot\lvert S\rvert=5\times8=40$。
> 撤回済 $\ell^{r-1}$ 律なら **1000**。**25 倍差。**

> ### P-R4-2(奇部 — $s_2$ 律の直接測定)
> $$\boxed{\ \lvert\ker\widetilde\chi\rvert\ \text{の奇部}=\mathbf 5=\ell^{\,s_2(4)}=\ell^1\ }$$
> **これが $s_2$ 律の非単調性の署名**: $r=3$ で $\ell^2=25$ だったものが $r=4$ で $\ell^1=5$ へ**下がる**。単調な律($\ell^{r-1}$ でも $\ell^{r}$ でも $\ell^{\lceil r/2\rceil}$ でも)はこの下降を出せない。

> ### P-R4-3(2-部 = Stab 律)
> $$\boxed{\ \lvert\ker\widetilde\chi\rvert\ \text{の}\ 2\text{-部}=\mathbf 8,\quad \mathrm{Syl}_2(\Xi(\ker))\cong D_8\ }$$
> $r\le3$ では 2-部は $1,2,2$(および尾部由来の $D_8$)だったので、**$r$ 由来で初めて $D_8$ が出る**。

> ### P-R4-4(奇部の同定 — $\langle\bar x\rangle$ ちょうどか)
> $$\boxed{\ \Xi(\ker)\ \text{の奇部}=\langle\bar x\rangle\ (\text{全対角})\ \text{であり、}B_x\ \text{の座標ベクトルは}\ (a,a,a,a)\ \text{型}\ }$$
> $r=2,3$ では $B^\tau=\{v_1=v_2\}$ 型(対角を含むが真に大きい)だった。$r=4$ では **$D_8$ 推移性により全対角ちょうどに潰れる**。座標で確認する(v1 §2 と同じ読み方)。

> ### P-R4-5(核の構造の名指し)
> $$\boxed{\ \ker\widetilde\chi\cong C_5\times D_8,\qquad \mathrm{IdGroup}=[40,10]\ }$$

> ### P-R4-6($\mathrm{GTSh}$ の形・STR-2 の一般化)
> $$\boxed{\ \mathrm{GTSh}(N,N)\cong S\times\bigl(C_{B}(S)\rtimes Q\bigr)=D_8\times\mathrm{Hol}(\mathbf Z/5),\quad\lvert\cdot\rvert=\mathbf{160},\ \mathrm{IdGroup}=[160,207],\ \mathrm{dl}=2\ }$$
> ($\mathrm{Hol}(\mathbf Z/5)=C_5{:}C_4$、`IdGroup [20,3]`。)撤回済 $\ell^{r-1}$ 律なら $\lvert\mathrm{GTSh}\rvert=4000$。

> ### P-R4-7($\widetilde\chi$ の全射性)
> $$\boxed{\ \lvert Q\rvert=\varphi(5)=\mathbf 4,\ Q\cong C_4\ \text{が}\ \langle\bar x\rangle\ \text{に忠実}\ }$$

> ### P-R4-8(**$\varepsilon$ 依存性** — 両枝で同じか違うか)
> $$\boxed{\ \text{B 枝と C 枝で }\lvert\ker\rvert,\ \text{奇部},\ 2\text{-部},\ \lvert\mathrm{GTSh}\rvert,\ \mathrm{IdGroup}\ \text{がすべて一致する}\ }$$
> **根拠**: PRUNE の入力($\mathrm{Stab}$・$S$・$C_B(S)$・$Q$)は §1.5 のとおり**両枝で完全に同一**。$\varepsilon$($E$ が直積かファイバー積か)は入力に現れない。
> **FAIL の意味(一級)**: $\varepsilon$ が GTSh に効くなら、PRUNE は $(\mathrm{Stab},S)$ だけの関数ではなく**窓の $E$-構造にも依存する**ことになり、予想 COARSE(`ideas_010` I11-C)も同時に反証される。**両パリティ枝が同時に実在する初の族なので、この欄はここでしか測れない。**

> ### P-R4-9(NORM の埋め込み — `norm_embedding` 様式)
> $$\boxed{\ \Xi:\mathrm{GTSh}\to N_{S_{20}}(\langle\bar x\rangle)\ \text{が}\ \ker\Xi=1,\ \text{像が}\ N\ (\text{位数 }60{,}000)\ \text{の部分群}\ }$$
> 既存 9 窓で PASS(`search/certs/norm_embedding_20260731.json`)。**$\Xi$ は反準同型**(合成規約)なので $\Xi'=\iota\circ\Xi$ で判定すること。
> 補題 NORM-E により $m=0$ 層だけの検査で足りる(コスト $1/c_m=1/4$)。

> ### P-R4-10($\varepsilon$-bit / 系 STR-1.6 の安価判定)
> $Q\le(\mathbf Z/5)^\times\cong C_4$ ゆえ **$Q_2$ は巡回(階数 1)**。したがって
> **委嘱 3 の「交差ビット欄」は発火しない** — `_probe_epsilon_bits_v2` の転用は**不要**。
> 代わりに 系 STR-1.6(`structthm_h2_v1.md` §7.1)が使える:
> $$\boxed{\ 2m+1\equiv-1\ (\mathrm{mod}\ 5)\ \text{の層に、位数 2 かつ }S\ \text{を中心化する shadow が ちょうど }2\ell=\mathbf{10}\ \text{個}\ }$$
> これ 1 本で $\varepsilon=0$(直積)が決まる(補群クラスの全列挙が不要)。$f\ne1$ も走査すること(W4 §7.2)。
> **交差ビット欄が要る条件の明示**: 将来 $N_{\rm ord}$ が $(\mathbf Z/N)^\times$ の $\mathrm{Syl}_2$ が非巡回になる値($N=15,16,20,24,\dots$)の $r\ge2$ 窓を撃つときに `_probe_epsilon_bits_v2` を転用する。$N_{\rm ord}=5$ の本窓では不要。

> ### P-R4-11(形そのものの検査)
> $$\boxed{\ (\text{奇部},\ 2\text{-部})\ \text{の対が §3.0 の表のいずれかの行に一致する}\ }$$
> すなわち $\ker=C_B(S')\times S'$ の形が保たれる($S'$ は実測 2-部)。
> **FAIL(例: $(125,8)$)なら PRUNE だけでなく「$C_B(S')\times S'$ という形」自体が壊れる**(§3.0 の注)。

**committed 欄の総数 = 12(`P-R4-0` … `P-R4-11`)。**

---

## 4. NULL 枠(事前登録)

> ### NULL-R4
> $$\boxed{\ (\text{奇部},\ 2\text{-部})\ \text{が}\ (5,8)\ \text{でない}\ }$$

**発火時の解釈(凍結時点で固定)**:

| 実測 $(\text{奇部},2\text{-部})$ | $\lvert\ker\rvert$ | 解釈 |
|---|---|---|
| $(5,8)$ | 40 | **PRUNE 的中**。$s_2$ 律の非単調性が実証され、$\ell^{r-1}$ は完全に死ぬ |
| $(125,8)$ | 1000 | **$\ell^{r-1}$ 律が復活**するが、同時に $C_B(S')\times S'$ の形が壊れる(§3.0)。**両立しない 2 つのことが同時に起きる**ので、形と律の両方を建て直す |
| **$(25,\ast)$** | — | **$s_2$ の修正が要る**。$25=\ell^2$ はブロック軌道数 2 ⟹ $S'$ は非推移($\lvert S'\rvert\le4$)。ゆえに **2-部も同時に $\le4$ に落ちているはず**。もし $(25,8)$ なら形が壊れ、$(25,4)$ か $(25,2)$ なら**形は生きて Stab 律(2-部 $=\mathrm{Syl}_2(\mathrm{Stab})$)が死ぬ**。この二択の判別が本欄の主目的。$s_2$ の後継候補は「$\mathrm{Syl}_2(\mathrm{Stab})$ ではなく**実際に作用する 2-群** $S'$ の軌道数」となり、$S'$ の同定が新しい問いになる |
| $(5,4)$ or $(5,2)$ | 20 / 10 | 奇部は PRUNE どおりだが **Stab 律が死ぬ**($S'\subsetneq\mathrm{Syl}_2$)。形は生存 |
| $(625,1)$ | 625 | $S$ が $B$ に自明作用 = 刈り込みが起きていない。**PRUNE の機構全体の反証** |
| $(1,\ast)$ | — | 奇部が消える。$r=1,2,3$ の全データと矛盾するので、**測定または窓同定の事故を先に疑う**(P-R4-0 を再検査) |
| 上記以外 | — | 形も律も無い。$\Xi(\ker)$ の $B_x$-座標(P-R4-4 の欄)を最優先で読み、部分加群の型から立て直す |

**$\varepsilon$ 依存性の NULL**: B 枝と C 枝で値が割れた場合(P-R4-8 FAIL)は、上のどの行に落ちても**別枠で記帳**する。PRUNE の関数依存性($(\mathrm{Stab},S)$ のみ)が偽になる初の証拠であり、予想 COARSE の反証を兼ねる。

---

## 5. 撃ち順(凍結時点で固定)

| 順 | 窓 | $\Xi$ | 目的 | 通過条件 |
|---|---|---|---|---|
| **1** | `W-E-A20-5x4t0-C`($\varepsilon=0$・直積) | $4.5\times10^8$ | **P-R4-1〜7**(主判別)。直積なので $E$ 構成が単純で事故が少ない | P-R4-0 PASS |
| 2 | `W-E-A20-5x4t0-B`($\varepsilon=1$・ファイバー積) | $4.5\times10^8$ | **P-R4-8**($\varepsilon$ 依存性)+ 主判別の独立再現 | — |

**根拠**: (i) 主判別は 1 窓で出る。C 枝を先にするのは、ファイバー積 assert の事故型(§1.4)を主判別の経路から外すため。(ii) B 枝は主判別の**独立再現**を兼ねる — 同じ $(\mathrm{Stab},S)$ から同じ答が出るかどうかが P-R4-8。
**シャード**: $m$(4 層)× $\alpha\in\mathrm{Stab}$(15,000)で 1 シャード 7,500 候補。600 秒 cap に収まる。fail-closed は実測 $\lvert\mathcal C_m\rvert$ と上界 $7500\times15000$ の併記。

---

## 6. 測定スペック

**driver へ渡してよいのは以下の左半分(欄名と計算内容)のみ。**

```text
0.  canonical_id                = SHA-256(canonical 文字列)      # §1.1 と一致しなければ Error
1.  eps_branch                  = "eps0_direct" | "eps1_fibre"   # E の構成の分岐フラグ
2.  group_order                 = |GTSh(N,N)|
3.  ker_size                    = |ker chi~|
4.  ker_odd_part_order          = ker_size の奇部分
5.  ker_2_part_order            = ker_size の 2 部分
6.  ker_odd_part_primes         = 奇部分の素因子の集合
7.  K_struct                    = StructureDescription(ker chi~)
7b. K_idgroup                   = IdGroup(ker chi~)
8.  K_is_direct_product         = ker = A x S の内部直積か
9.  A_order, A_idgroup          = O_{2'}(ker chi~)
10. S2_struct, S2_order         = Syl_2(ker chi~)
11. Stab_order, Syl2_Stab_struct= |Stab_Aut(P)(xbar)|, Syl_2(Stab) の構造
12. A_coords_in_Bx              = Xi(ker) の奇部の B_x = C_5^4 座標ベクトル全列挙
                                   （B_x は xbar の 4 巡回が生成。各元を (v1,v2,v3,v4) mod 5 で）
13. S2_block_action             = Syl_2(Xi(ker)) の 4 ブロックへの置換像と軌道分割
14. chi_image_order, Q_struct   = |Q|, Q の不変因子
15. gtsh_idgroup                = IdGroup(GTSh)（圏外なら StructureDescription + 導来列位数）
16. derived_length_G            = dl(GTSh)
17. xbar_normalizer_order       = |N_{S_20}(<xbar>)|
18. xi_map_alpha_well_defined   = 全 shadow で alpha が一意（norm_embedding.g 様式）
19. xi_hom_left / xi_hom_right  = 準同型規約の判定
20. xi_kernel_trivial           = 相異なる alpha の個数 == shadow 総数
21. xi_image_order, xi_image_in_normalizer
22. u_minus1_involutions        = 2m+1 ≡ -1 (mod 5) の層で ord=2 かつ [.,Syl_2(ker)]=1 の
                                   shadow 個数（f ≠ 1 も走査）
23. xi_count_measured / xi_count_bound                            # 23a > 23b で Error
```

**判定表(司令塔用・driver には渡さない)**

| 欄 | PASS 条件 |
|---|---|
| P-R4-0 | 欄 0 一致 + 窓 assert 全項 |
| P-R4-1 | 欄 3 $=40$(両枝) |
| P-R4-2 | 欄 4 $=5$ |
| P-R4-3 | 欄 5 $=8$ かつ 欄 10 $\cong D_8$ |
| P-R4-4 | 欄 12 が $(a,a,a,a)$ 型 5 本 |
| P-R4-5 | 欄 7b $=[40,10]$ |
| P-R4-6 | 欄 15 $=[160,207]$ かつ 欄 2 $=160$ かつ 欄 16 $=2$ |
| P-R4-7 | 欄 14 $=4$・$Q\cong C_4$ |
| P-R4-8 | B 枝と C 枝で 欄 2,3,4,5,7b,15 が全一致 |
| P-R4-9 | 欄 20 true・欄 21 が $N$(60,000)の部分群・$\lvert$像$\rvert=$ 欄 2 |
| P-R4-10 | 欄 22 $=10$ |
| P-R4-11 | (欄 4, 欄 5) が §3.0 の表のいずれかの行 |
| NULL-R4 | — |

---

## 7. 自己監査

| # | リスク | 判定 |
|---|---|---|
| R-1 | PRUNE 自体が candidate | ○ **明示**。`pruning_law_v1_1.md` §2 のとおり飽和($\supseteq$)は未証明。本予言は candidate の**外挿**であって定理の適用ではない |
| R-2 | $C_{B_x}(S)=C_5$ は測定ではないのでは | ○ **周辺群の計算**として機械確認済(`r4_window.g`)。予言しているのは「それが核の奇部として**実現する**か」であって、$C_{B_x}(S)$ の値そのものではない |
| R-3 | $r=4$ の 1 点で $s_2$ 律が確定するか | △ **しない**。$s_2$ と一致する他の関数(例: $\mathrm{Syl}_2(S_r)$ の軌道数そのもの)は区別できない — もっとも $s_2(r)=$ 軌道数は**定理**なので、区別すべき対抗仮説は「単調な律」だけ。$r=4$ はそれを落とす |
| R-4 | 較正ゲートが張れない | △ **明示**。素の経路が $4.9\times10^{18}$ で不能。**judge の $\Xi$-制限実装の健全性は本窓では検証できない** — 既存の較正ゲート(`W-E-A10-9t1`・`W-E-A10-5x2t0`)の PASS に依存する。**両ゲートの回帰を先に通してから撃つこと** |
| R-5 | 悉皆証明書への依存 | △ 実現対の存在は `r4_exhaustive_20260730.json`(構造定数先行 + 15/15 セル完全列挙)に依存。私は窓 assert を独立に再計算したが、**「他に実現セルが無い」という悉皆性は再検査していない** |
| R-6 | 両枝が同じ答を出すという予言の根拠 | △ 「入力が同じだから」は PRUNE の**関数形の仮定**に依存する。P-R4-8 はその仮定そのものの検査であり、循環ではないが**予言としては弱い** |
| R-7 | 接触遮断 | ○ shadow は 1 個も見ていない(§0) |
| R-8 | $\varepsilon$-bit 欄の省略 | ○ $Q_2$ が巡回(階数 1)であることは $(\mathbf Z/5)^\times\cong C_4$ から**無条件**。委嘱 3 の条件節が発火しないことの根拠は算術のみ |

---

## 8. 未閉鎖項

* 【R4-a】凍結手続き: 司令塔の commit で凍結。凍結前に driver を起動しない。
* 【R4-b】測定発注は凍結後。judge は $\Xi$-制限実装版(v1.3 以降)。**既存 2 較正ゲートの回帰 PASS を入口条件にする**(R-4)。
* 【R4-c】兄弟軌道: B 枝 28 軌道・C 枝 118 軌道のうち $S_{20}/A_{20}$ を出すものは複数ある。`P-A13-12` と同型の**軌道非依存性**は本稿では問わない(canonical 1 対のみ対象)。必要なら追試枠。
* 【R4-d】$r=5$($s_2=2$)は $\Xi\approx2.8\times10^{11}$ で不能。**$s_2$ 律の次の検証点は $r=8$($s_2=1$)だが予算は絶望的** — $r=4$ が事実上唯一の判別点であることを記帳しておく。

---

---

> # ⛔ 接触遮断の注意書き
>
> **本ファイルは測定 driver の実行エージェント(implementer / falsifier / CI ジョブ)に読ませてはならない。**
>
> - driver へ渡してよいのは **§1 の窓同定情報(canonical ID・生成対・judge preamble・$\Xi$ 上界・§1.4 のファイバー積注意)と §6 の欄定義(左半分のみ)**。
> - **§0 の機構説明・§3 の committed 欄と判別表・§4 NULL 枠・§5 の目的欄・§6 判定表・§7 は渡さない。**
> - §6 のコード欄の右側コメントも削ってから渡すこと。とくに `# §1.1 と一致しなければ Error` 以外の説明は不要。
> - 判定は測定完了・証明書ハッシュ確定後に司令塔が本ファイルと突き合わせて行う。
> - 番号系は `P-STR-*`・`P-A13-*`・`P-I10-*` と分離済み(本稿は `P-R4-*` のみ)。
