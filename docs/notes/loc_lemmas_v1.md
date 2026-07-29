# LOC 3 段補題 v1(candidate)— M-1P の証明経路と、その破れ箇所の名指し

作成: 数学者(Opus 5)・2026-07-30(レーン A-2)
委嘱: 司令塔(発案係 I11-A `ideas/ideas_011_i10_followup.md` 第二部を踏まえて)
正本の関係: `docs/notes/epsilon_mechanism_v2.md`(M-1P/M-1c)・`docs/notes/structthm_h2_v2.md`(STR-1 v2)
新規計算: `search/_probe_loc_lemmas.g`(+ driver `_a16.g`/`_a20.g`)・`search/_probe_loc_diag.g` / 証明書 `search/certs/.loc_W-D-A{16,20}-*.json`
凍結済み予言(P-EPS-5′ 等)非接触・封印量非接触。**状態札: candidate**

---

## 0. 結論(3 段の成否)

| 段 | 主張 | 判定 | 根拠 |
|---|---|---|---|
| **LOC-1** | 中心化 $\iff$ $T_{(m,f)}\vert_S=\mathrm{id}$ | **FAIL(同値は偽)** | A16: 中心化 220 個 vs $T\vert_S=\mathrm{id}$ **4 個**;A20: 240 vs **2**。逆向き($T\vert_S=\mathrm{id}\Rightarrow$中心化)は両窓で反例 0 だが**未証明** |
| **LOC-2** | 中心化 shadow の冪の $K$-成分は $C_K(S)=A\times Z(S)$ | **PASS** | 2 行で証明(§3)+実測 22/22・30/30 |
| **LOC-3** | $u=-1$ 層で $\mathrm{pr}_{Z(S)}(\mathcal N_2)=1$ | **結論は成立・提案機構は反証** | 結論 22/22・30/30。しかし提案の根拠「$D=T\circ\tilde\theta$ が $S$ 上自明」は **0/22・0/30 で全滅** |

> **一行要約**: **鎖は LOC-1 で切れる**。LOC-2 は無傷。LOC-3 の結論は正しいが、I11-A が用意した理由(D の $S$-自明性)は**実測で完全に否定**された。切れ目の正体は §2.3 で特定できた — **$\Sigma_S$ が $C_{P_N}(x)$ に入らないこと**。

---

## 1. 設定と道具

shadow の合成則(`kerchi-judge.g` `GroupOfShadows` 逐語):
$$(m_1,f_1)(m_2,f_2)=\bigl(m_1\!\circ\!m_2,\ f_1\cdot T_{(m_1,f_1)}(f_2)\bigr),\qquad
T_{(m,f)}:\ x\mapsto x^{u},\ y\mapsto f^{-1}y^{u}f\ \ (u=2m+1).$$
settled 条件により $T_{(m,f)}\in\mathrm{Aut}(P_N)$ で、$T_{gh}=T_gT_h$(v2 §3.2 で証明済)。すなわち
$$T:\ G\longrightarrow \mathrm{Aut}(P_N)\quad\text{は準同型}.$$
$K=\{(0,g)\}$、$S=\mathrm{Syl}_2(K)$、$A=O(K)$、$\Sigma_S:=\{\sigma:(0,\sigma)\in S\}\subseteq P_N$、$z$ = $Z(S)$ の生成元。
$\tilde\theta(g)=\Delta g\Delta^{-1}$($\Delta=s_1s_2s_1$)は $x\leftrightarrow y$ の入れ替えで**対合**。θ-公理は $f\cdot\tilde\theta(f)=1$。

> **型の罠(I11-A の警告を正式化)**: $f$ は一般に $K$ の元ではない($m\ne0$ の shadow の第 2 成分だから $(0,f)$ は shadow とは限らない)。ゆえに **$\mathrm{pr}_{Z(S)}(f)$ や $\mathrm{pr}_{Z(S)}(D(f))$ は無意味**。射影は $K$ の元、すなわち $\mathcal N\in C_K(S)=A\times\langle z\rangle$ に落としてからしか取れない。本ノートは全ての射影をこの型で書く。

---

## 2. 【LOC-1】中心化の真の条件 — 同値は**偽**

### 2.1 補題 LOC-0(中心化の正確な形・証明)

> **補題 LOC-0.** $h=(m,f)$、$s=(0,\sigma)$ とすると
> $$[h,s]=1\iff f\cdot T_h(\sigma)=\sigma\cdot T_{(0,\sigma)}(f),\qquad T_{(0,\sigma)}:x\mapsto x,\ y\mapsto\sigma^{-1}y\sigma .$$

**証明**: $hs=(m\!\circ\!0,\ f\,T_h(\sigma))=(m,\ f\,T_h(\sigma))$、$sh=(0\!\circ\!m,\ \sigma\,T_{(0,\sigma)}(f))=(m,\ \sigma\,T_{(0,\sigma)}(f))$。shadow は座標で決まるので第 2 成分の一致が同値条件。$\square$

**I11-A が想定した式との差**: 「$[h,s]=1\iff T_h(\sigma)=\sigma$」は**右辺の $T_{(0,\sigma)}(f)$ を落とした形**であり、一般には成り立たない。

### 2.2 いつ退化するか(分水嶺)

$T_{(0,\sigma)}$ は $x\mapsto x$、$y\mapsto\sigma^{-1}y\sigma$。一方 $\mathrm{conj}_\sigma$ は $x\mapsto\sigma^{-1}x\sigma$、$y\mapsto\sigma^{-1}y\sigma$。ゆえに
$$T_{(0,\sigma)}=\mathrm{conj}_\sigma\iff \sigma\in C_{P_N}(x).$$
このとき LOC-0 の右辺は $\sigma\cdot\sigma^{-1}f\sigma=f\sigma$ となり、条件は $f\,T_h(\sigma)=f\sigma$ すなわち $T_h(\sigma)=\sigma$ に退化する。

> **補題 LOC-1′(修正版・証明つき).** $\Sigma_S\subseteq C_{P_N}(x)$ ならば
> $$h\ \text{が}\ S\ \text{を中心化}\iff T_h\vert_{\Sigma_S}=\mathrm{id}.$$

### 2.3 実測 — 前件は最大限に破れている(**切れ目の同定**)

`search/_probe_loc_diag.g`(A16):
$$\lvert\Sigma_S\rvert=8,\qquad \lvert\Sigma_S\cap C_{P_N}(x)\rvert=\mathbf 1\ (=\{1\}\ \text{のみ}),\qquad \lvert\Sigma_S\cap C_{P_N}(y)\rvert=1 .$$
**単位元以外の $\Sigma_S$ の元はどれも $x$ を中心化しない。** ゆえに LOC-1′ の前件は成り立たず、LOC-1 は同値として偽。

`search/_probe_loc_lemmas.g`(全 shadow 走査):

| 窓 | shadow 総数 | #中心化 | #$T\vert_S=\mathrm{id}$ | #両方 | #中心化 $\wedge$ $T\vert_S\ne\mathrm{id}$ | #$T\vert_S=\mathrm{id}$ $\wedge$ 非中心化 |
|---|---|---|---|---|---|---|
| A16 | 880 | 220 | **4** | 4 | **216** | **0** |
| A20 | 960 | 240 | **2** | 2 | **238** | **0** |

> **判定**: $T\vert_S=\mathrm{id}$ は中心化より**真に強い**(A16 で 4 vs 220)。
> 一方 **$T\vert_S=\mathrm{id}\Rightarrow$ 中心化** は両窓で反例 0。ただしこれは LOC-0 から形式的には出ない($T_h(\sigma)=\sigma$ を代入しても $T_{(0,\sigma)}(f)=\sigma^{-1}f\sigma$ が別途必要)。**【GAP-LOC-1】未証明の実測事実**として登録する。

---

## 3. 【LOC-2】封じ込め — **PASS**

> **補題 LOC-2(証明).** (H1) $K=A\times S$ の下、$h$ が $S$ を中心化し $n=\mathrm{ord}(\tilde\chi(h))$ とすると
> $$h^{\,n}\in C_K(S)=C_{A\times S}(S)=A\times Z(S).$$

**証明**: $\tilde\chi(h^n)=u^n=1$ より $h^n\in K$。$h$ が $S$ を中心化するから $h^n$ も中心化する。よって $h^n\in C_K(S)$。$K=A\times S$ と $[A,S]=1$ から $C_K(S)=A\times C_S(S)=A\times Z(S)$。$\square$

**実測確認**: $\lvert C_K(S)\rvert=22=\lvert A\rvert\lvert Z(S)\rvert$(A16)・$30$(A20)、いずれも一致。$u=-1$ 層の中心化 shadow の $h^2$ は **22/22・30/30 が $C_K(S)$ に入る**。

> これで **$P(u)\in\{0,1\}$ の枠が固定**され、残る中身はちょうど 1 ビット。I11-A の見立てどおり、この段は形式的で無傷である。

---

## 4. 【LOC-3】z-成分の消去 — 結論は成立・**提案機構は反証**

### 4.1 余境界形は正しい(証明+検算)

$u=-1$($n=2$)のとき $h^2=(1,\ \mathcal N_2)$、$\mathcal N_2=f\cdot T_h(f)$。$D:=T_h\circ\tilde\theta$ とおくと $\tilde\theta^2=\mathrm{id}$ より $D(\tilde\theta(f))=T_h(f)$、θ-公理 $\tilde\theta(f)=f^{-1}$ を代入して

$$\boxed{\ \mathcal N_2=f\cdot D(f)^{-1}\ }\qquad(D\text{-余境界形}).$$

**検算**: A16 で 22/22、A20 で 30/30 が厳密一致(`N2_coboundary_form_ok`)。**この式は正しい**。

### 4.2 提案された理由は**全滅**

I11-A は「LOC-1 により $D$ は $S$(とくに $\langle z\rangle$)に自明に作用する」を根拠に据えていた。実測:

| 窓 | $u=-1$ 中心化 shadow | $D\vert_S=\mathrm{id}$ | $D\vert_S\ne\mathrm{id}$ | $\mathrm{pr}_{Z(S)}(\mathcal N_2)\ne1$ の個数 |
|---|---|---|---|---|
| A16 | 22 | **0** | **22** | **0** |
| A20 | 30 | **0** | **30** | **0** |

- **$D$ は一例も $S$ 上自明でない**。根拠は完全に否定された(LOC-1 が偽なのだから当然の帰結でもある)。
- それでも**結論 $\mathrm{pr}_{Z(S)}(\mathcal N_2)=1$ は全例で成立**。つまり「正しい結論・誤った理由」。

### 4.3 生き残る部分と、生き残らない部分

- **生き残る**: $\tilde\theta$ は $\Sigma_S$ を**集合として保ち**(A16 実測 true)、**$Z(S)$ を各点固定する**(実測 true;$Z(S)$ が $S$ の特性部分群で位数 2 だから自動でもある)。ゆえに $D$ も $z$ を固定する。I11-A の括弧書き「とくに $\langle z\rangle$」だけは**真**である。
- **生き残らない**: それだけでは $\mathrm{pr}_{Z(S)}(\mathcal N_2)=1$ は出ない。$\mathrm{pr}_{Z(S)}$ は**元 $\mathcal N_2$ の $K$-分解**についての射影であって、$D$ の $z$ 上の作用とは別物である(§1 の型の罠)。**この一段の飛躍が現在の空白**。
- **構造的規則性(新観察)**: $D\vert_{\Sigma_S}$ は 22 個の shadow に対し **2 型しか取らない**(A16)。代表は $\tilde\theta\vert_{\Sigma_S}$ と同じ置換 $(4,5)$(8 点中 6 点固定の対合)。すなわち **$D\vert_S$ はほぼ定値**であり、$h$ にほとんど依らない。

> **【GAP-LOC-3】** $\mathcal N_2=f\,D(f)^{-1}$(両因子とも $K$ の外)から、$K$ における $Z(S)$-成分の消滅を導く一段が無い。ここが M-1P の証明の真の壁である。

---

## 5. A10 型標本との突合(何を殺し、何については沈黙か)

`W-E-A10-9t1`($u=7$ 層、$\mathcal N\in A\setminus\{1\}$、$\mathrm{ord}_G=9$ vs 商位数 3)。

| 段 | A10 での状態 |
|---|---|
| LOC-1 | **空虚**。$S_{\rm order}=1$ ゆえ $\Sigma_S=\{1\}$、両辺とも自明に真 |
| LOC-2 | **空虚に真**。$C_K(S)=K=A$ |
| LOC-3 | **空虚**。$Z(S)=1$ ゆえ $\mathrm{pr}_{Z(S)}$ は**自明な写像**、$\varepsilon\in H^2(Q;1)=0$ |

> **重要な帰結**: A10 は「$\mathcal N=1$ という強すぎる形」を殺す型標本としては有効だが、**LOC-3 については何も語らない**($z$ が存在しないので消すべきものが無い)。
> ゆえに **A10 を LOC-3 の反例探索の場に使ってはならない**。LOC-3 の型標本になり得るのは $S\ne1$ かつ $Z(S)\cong C_2$ の窓 — 手近では**梯子 $t=4$ 窓 `W-E-A13-9t4`**(S が $D_8$ 型と期待され、しかも $N_{\rm ord}=9$ で **(H2) が破れる** = STR-1 v2 §3 の H2′ 経路が要る領域)。**次の測定の第一候補として推す**。

---

## 6. 破れ箇所 = P-EPS-5′ 点火機構の候補名指し

委嘱の設計どおり、切れ目がそのまま点火候補になる。3 つ挙げ、優先順を付ける。

> **【IGN-1】$\Sigma_S$ と $C_{P_N}(x)$ の乖離**(切れ目そのもの)
> LOC-1 を殺しているのはこれ(A16: 8 中 1 のみが $x$ を中心化)。$S$ が大きくなれば $\Sigma_S$ も大きくなり、乖離は**拡大方向**と予想される。$\Rightarrow$ tail-8 では LOC-1 型の道具はさらに使えない。
> **測定**: 新窓ごとに $\lvert\Sigma_S\cap C_{P_N}(x)\rvert/\lvert\Sigma_S\rvert$ を 1 欄追加(費用ゼロ)。

> **【IGN-2】$D\vert_S$ の型数**(一様性の源)
> A16 では 22 個に対し 2 型しかない。この「ほぼ定値」性が層内一様性(v2 §1.6)の背後にある可能性が高い。型数が増える窓では、層内で $P$-ビットが割れる(= 一様性が壊れる)ことがありうる。
> **測定**: 層別に $D\vert_{\Sigma_S}$ の相異なる型数を出す(本ノートの probe に実装済)。

> **【IGN-3・最有力】$\tilde\theta\vert_{Z(S)}$ の非自明化**
> 現在 $Z(S)\cong C_2$ は特性部分群ゆえ $\tilde\theta$ は $z$ を**必ず**固定する。これは「$Z(S)$ が位数 2」に完全に依存した恩恵である。
> **$Z(S)$ が非巡回になる窓では $\tilde\theta$ が $Z(S)$ 上で非自明に作用しうる** — その瞬間、上の「自動的な恩恵」が消える。
> 該当窓は **`W-D-A19-13t6`($S=\mathrm{Syl}_2(S_6)\cong D_8\times C_2$、$Z(S)\cong C_2^2$)**。裁定 214 で「$Z(S)=C_2^2$ の較正 pilot」と位置づけられた窓に、**本ノートは具体的な測定標的を与える**: $\tilde\theta\vert_{Z(S)}$ が自明か否か。
> **自明でなければ**、それが P-EPS-5′ の点火機構の第一候補として名指しできる。**自明なら**、恩恵は $Z(S)$ の形に依らない可能性が上がり、tail-8 側の予言は「0」に傾く。**どちらでも領土**。

---

## 7. M-1c(交差ビット)側の同型分解

同じ 3 段が引ける。$h_i=(m_i,f_i)$($i=1,2$)を $S$ を中心化する shadow とする。

- **LOC-1c** = LOC-1 と同一(中心化の条件は片方ずつ)。よって**同じ理由で同値は偽**。
- **LOC-2c(PASS・証明)**: $Q$ がアーベルなら $\tilde\chi([h_1,h_2])=1$ ゆえ $[h_1,h_2]\in K$。両者が $S$ を中心化するから $[h_1,h_2]\in C_K(S)=A\times Z(S)$。$\square$
 (三窓・梯子とも $Q$ はアーベル。非アーベル $Q$ の窓では**この段から崩れる** — 注意点として登録。)
- **LOC-3c(open)**: $h_1h_2$ と $h_2h_1$ は同じ $u$-成分 $u_1u_2$ を持ち、第 2 成分はそれぞれ
 $$f_1\,T_{h_1}(f_2)\qquad\text{と}\qquad f_2\,T_{h_2}(f_1).$$
 よって交差ビットは **この 2 語の食い違いの $Z(S)$-成分**:
 $$c(h_1,h_2)=\mathrm{pr}_{Z(S)}\Bigl(\bigl(f_1T_{h_1}(f_2)\bigr)\cdot\bigl(f_2T_{h_2}(f_1)\bigr)^{-1}\ \text{に対応する}\ K\ \text{の元}\Bigr).$$
 LOC-3 の $\mathcal N_2=f\,D(f)^{-1}$ が**単項の余境界形**だったのに対し、こちらは**双線型な非対称項**である。

> **方針(I11-A に同意)**: LOC-3 が通っていない以上、**LOC-3c を単独で攻めるのは早い**。ただし LOC-2c は独立に証明できたので、**「交差ビットは $A\times Z(S)$ の中の 1 ビット」という枠は既に固定された** — これは v2 §7 の測定契約(項目 3)を紙の側から正当化する。
> **測定先行**: $\pi(N)\ge2$ の新窓(E-2 系)で $c(a_i,a_j)$ を実測するのが正しい順序。**現行 `_probe_epsilon_bits.g` は交差ビット欄を持たない**(v2 §8)ので、その追加が前提。

---

## 8. 次の一手(優先順)

1. **`W-D-A19-13t6` で $\tilde\theta\vert_{Z(S)}$ を測る**(IGN-3)。$Z(S)=C_2^2$ の pilot に明確な標的を与える。費用: 窓 1 個の LOC probe。
2. **`W-E-A13-9t4`(梯子 $t=4$)で LOC-1/2/3 を測る**。$S\ne1$ かつ $Z(S)\cong C_2$ の第 4 標本で、しかも (H2) 破れ領域。A10 では空虚だった 3 段が初めて内容を持つ。
3. `_probe_epsilon_bits.g` に**交差ビット欄**を追加(v2 §8 の宿題・LOC-2c が枠を保証済)。
4. 【GAP-LOC-1】($T\vert_S=\mathrm{id}\Rightarrow$ 中心化)と【GAP-LOC-3】(余境界形から $Z(S)$-成分消滅へ)は**紙の宿題**として残す。

---

## 9. 出所・格付け

- スクリプト: `search/_probe_loc_lemmas.g`(+ `_probe_loc_a16.g` / `_probe_loc_a20.g`)・`search/_probe_loc_diag.g`
- 証明書: `search/certs/.loc_W-D-A16-11a.json`・`search/certs/.loc_W-D-A20-15a.json`
- 入力 shadow 集合は既存 `search/certs/.w62_shadows_*.g` を再利用(走査は再実行していない)。規律: 1 窓 1 プロセス・`-o 2g`。
- **格付け**: 補題 LOC-0・LOC-1′・LOC-2・LOC-2c・§4.1 の余境界形は**証明済**(初等・自己完結)。§2.3・§4.2・§4.3 の表は **GAP 単系統の実測**(cross-checked ではない)。§6 の IGN-1〜3 は **candidate(未証明の点火候補)**。§5 の A10 空虚性は証明書の値($S_{\rm order}=1$)からの直接帰結。
- A20 側の `loc_diag`(Σ_S と $C_{P_N}(x)$ の交わり・$D\vert_S$ の型数)は**未測定** — A16 単窓の観察である。
