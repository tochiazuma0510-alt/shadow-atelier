# 定理 UU の機構は gentle 側の全消滅を説明するか — 一点確認 短報

**状態札: 数学者判定・司令塔検分前・Sol 未監査**
判定: Claude 数学者 / 2026-08-19 / 委嘱 = 司令塔(一点確認)
格: paper candidate。機械計算ゼロ。封印非接触。

---

## 0. 裁定

**(a) 不成立。** 仮説の**前提は正しい**($\mathbf F_2[C_2]$, $\mathbf F_3[C_3]$ は局所・$\theta-1$, $\tau-1$ は冪零)が、**結論に至る論法が成立しない**。決定的な理由は 1 行:
> **Nakayama/Neumann は「全射性」と「分裂」を持ち上げるが、「像への包含」は持ち上げない。** $C_tZ\subseteq\operatorname{Im}A_t$ は階数等式 $\operatorname{rank}[A_t\mid C_tZ]=\operatorname{rank}A_t$ であって全射性ではない。

**(b)** 従って COCYCLE-ABSORB-137 / MULTIPLICITY-ABSORB-138 / INDECOMP-ENTRY-138 は系として従わず、**裁定 1159 の「説明定理なし」は閉じない**。
**(c)** 破れの一行: **§1 の反例**($\Lambda=k[s]/(s^3)$, $A=s^2$, $CZ=s$)。
**ただし空振りではない** — 局所性の着眼は正しい方向を指しており、**正しい説明定理の形は Nakayama ではなく「根基フィルトレーションの深さ比較」**である(§3)。そこから**即測定できる検査を 2 本**出す(FC-16 / FC-17)。**FC-16 は既存データの 1 行で終わり、YES なら現象は即座に説明される。**

---

## 1. 決定的な反例(3 行)

$\Lambda=k[s]/(s^3)$(局所・$\mathfrak m=(s)$ 冪零)、$A=s^2$、$CZ=s$($1\times1$ 行列)。
- 剰余体上: $\bar A=0$, $\overline{CZ}=0$ ⟹ $\overline{CZ}\in\operatorname{Im}\bar A$ ✓(mod $\mathfrak m$ の包含は成立)。
- $\Lambda$ 上: $\operatorname{Im}A=s^2\Lambda=\{0,s^2\}$、$s\notin s^2\Lambda$ ⟹ **包含は成立しない**。∎

⟹ 「mod $\mathfrak m$ で包含 ⟹ $\Lambda$ 上で包含」は**偽**。定理 UU が持ち上げたのは $\sigma\mathbf D_3\equiv\mathrm{id}$(**単元性**)であって包含ではない。gentle 側の主張は最初から別の型である。

---

## 2. 仮説の各部の点検

| 主張 | 判定 |
|---|---|
| $\mathbf F_2[C_2]=\mathbf F_2[s]/(s^2)$、$\mathbf F_3[C_3]=\mathbf F_3[s]/(s^3)$ は局所、$s=\theta-1$ / $\tau-1$ は冪零 | **正しい** |
| ノルムが根基の冪: 標数 2 で $N_\theta=1+\theta=s$、標数 3 で $N_\tau=1+\tau+\tau^2=s^2$。従って $Z^1$ の二成分は $\ker s$ と $\ker s^2$、$H^2$ は $\ker s/sV$(resp. $\ker s/s^2V$) | **正しい**(検算済み)。**この構造把握は有用** |
| 「$C_t$ は untwisted 比較の単位摂動」 | **不成立**。UU では augmentation で untwisted 複体が**残る**(T-30 §2 の分裂完全列)。gentle では $\theta\mapsto1$, $\tau\mapsto1$ とすると $N_\theta\mapsto2=0$, $N_\tau\mapsto3=0$ で**cocycle 条件が空虚になりノルムが消える** — 摂動すべき「完全な untwisted 比較」が**存在しない**。twist が摂動ではなく構造そのものである(UU と正反対の領域) |
| 「$C_p$ 方向に制限すれば局所」 | **効かない**。$A_t,C_t$ は roof 行 $t=(m,f)$ と窓作用を含む $\mathbf F_p$-線形写像であり、$\mathbf F_p[C_p]$-線形ではない($\theta,\tau$ は関係式の**中に**現れる作用素)。従って「行列が係数を持つ局所環」が存在しない |
| 「UU が要求した自然性は局所性で不要になる」 | **不成立**。UU で自然性が不要だったのは、$\mathbf D_i$ が**同一の固定行列の係数替え**(GS-S)だったから。gentle の $A_t,C_t$ は roof 行ごとに変わり($T_t$ も行ごとに変わると Sol が明記)、共通の普遍行列が同定されていない |

---

## 3. それでも残る正しい方向 — 「深さ」による説明

局所性は Nakayama ではなく**フィルトレーション**として効く。$\mathfrak m=(s)$ による根基フィルトレーション $V\supseteq sV\supseteq s^2V\supseteq0$ の下で、COCYCLE-ABSORB が自動になる**十分条件の正しい形**は:

> **(DEPTH)** ある $k$ について $C_t\bigl(Z^1(\Gamma,V)\bigr)\subseteq s^k V$ かつ $s^kV\subseteq\operatorname{Im}A_t$。

これは階数等式を**構造的に**導く(Nakayama を使わない)。しかも標数 $p$ では $C_t$ の各項が $\theta,\tau$ の関係式由来の因子を持つので、$C_t$ が**深さを上げる**($s$ を掛ける)ことは十分あり得る。ESCAPE-28/2 の消滅が「$C_tZ$ が非零なのに常に $\operatorname{Im}A_t$ に入る」という形をしていることは、この型の説明と**整合的**である($C_t=0$ ではないが深い、という Sol の観察そのもの)。

---

## 4. 即測定できる検査 2 本

| 番号 | 検査 | コスト | 効果 |
|---|---|---|---|
| **FC-16** | **全 1,620 template で $\operatorname{coker}A_t=0$ か**(= $A_t$ が全射か)。producer は既に $\operatorname{rank}A_t$ を計算しているので**既存データの 1 行**。 | ほぼ 0 | **YES なら現象は即座に完全説明**($A_t$ 全射 ⟹ 任意の $C_tZ$ が像に入る)。裁定 1159 がその場で閉じる。**最優先** |
| **FC-17** | $s$-フィルトレーションでの深さ: $\min\{k: C_tZ\subseteq s^kV\}$ と $\max\{k: s^kV\subseteq\operatorname{Im}A_t\}$ を全 template で測る($s=\tau-1$ / $\theta-1$) | 小(既存行列に $s$ を掛けるだけ) | (DEPTH) が成立するかを直接判定。成立すれば**説明定理の候補が確定**し、族化(任意 module/roof)の証明目標が「$C_t$ が深さを上げる」という局所的主張に縮む |

**注意**: FC-16 が NO かつ FC-17 が「深さが揃わない」なら、消滅は $A_t$/$C_t$ の**個別の数値的偶然**である可能性が上がり、族定理は期待できない(裁定 1159 の維持)。どちらに転んでも情報になる。

---

## 5. 申告

- 本書は**一点確認**であり、gentle 側の原資料(`sol/sol_reply_137_whyvoid.md` §1.4 の COCYCLE-ABSORB-137、`sol_reply_138_campaign.md`)を読んで判定した。$V_{28}$/$V_{12}$ の具体的な加群構造・標数・$\operatorname{rank}A_t$ の値は**参照していない**(FC-16/17 がまさにそれを測る)。
- §1 の反例と §2 のノルム計算($N_\theta=s$, $N_\tau=s^2$)は手計算で検証済み。
- **UNKNOWN**: FC-16, FC-17。(DEPTH) の成否。裁定 1159 は**閉じない**(本書では)。
- 既在との整合: `sol/luna_reply_152_cocycle_absorb_universal_v1.md:161` が「ordinary $H^2$・Fox 自然性・個別 averaging から普遍 COCYCLE-ABSORB」を **REFUTED** と裁定済み。本書はそれと**同方向**(別機構による独立の否定)であり、覆すものではない。
- **B4-B は宣言していない。**

---

# 追補 v2(2026-08-19)— FC-16 実測(NO)の判定と FC-17/18 の実装仕様

出典: cert `search/certs/cocycle_absorb_137_t_families_v1_20260815.json`(司令塔抽出)。本文 §1–§5 は凍結、以下は追記。

## v2-1. まず自分の型エラーを訂正する

本文 §3 の (DEPTH) を「$C_t(Z^1)\subseteq s^kV$ かつ $s^kV\subseteq\operatorname{Im}A_t$」と書いたのは**型が誤り**である。実測表のとおり $A_t$ は $42\times21$ / $14\times7$ / $24\times12$、すなわち
$$A_t:\ V\ (\dim 21/7/12)\ \longrightarrow\ W_{\rm def}\ (\dim 42/14/24)$$
で、$\operatorname{Im}A_t$ は**始域 $V$ ではなく終域(欠損空間)$W_{\rm def}$ の部分空間**である($\dim W_{\rm def}=2\dim V$ = 二 hexagon 分)。⟹ **(DEPTH) はフィルトレーションを $W_{\rm def}$ 上で取らねばならない**:
$$\textbf{(DEPTH')}\qquad \operatorname{Im}\bigl(C_t|_{Z^1}\bigr)\ \subseteq\ s^kW_{\rm def}\ \subseteq\ \operatorname{Im}A_t .$$

## v2-2. 実測データの判定

**(1) FC-16 = NO を受領。** $\operatorname{rank}A_t=17<21$ 等で $A_t$ は全射でない ⟹ 「$A_t$ 全射だから自明」という最軽量の説明は**消えた**。

**(2) 定数 rank は「roof 行が単元で効く」ことの指紋である(仮説の残骸が生き残る).**
108 個の $A_t$ がすべて相異なるのに $\operatorname{rank}A_t$ が全 324 行で完全に定数、という現象は数値的偶然としては不自然である。最も自然な構造的説明は
$$A_t\;=\;U_t\,A_0\,W_t\qquad(U_t,W_t\ \text{可逆})$$
すなわち**roof 行が可逆作用素(単元)としてのみ効く**こと。これは司令塔の元仮説「$C_t$ は単元摂動」の**正しい残骸**であり、データはこの弱形を支持する。(ただし §1 の反例により、単元性から包含は出ない — 支持されるのは機構の一部であって結論ではない。)

**(3) 境界一致は (DEPTH') より「不変部分空間」を示唆する.**
- trivial_character:+ の 240 行と support_two_orbit の 108 行で $\operatorname{rank}C_tZ=\operatorname{rank}A_t$。COCYCLE-ABSORB-137 の包含と合わせると、そこでは $\operatorname{Im}(C_tZ)=\operatorname{Im}A_t$ が**厳密に等号**。
- 一方 orbit_bundle:± では $\max\operatorname{rank}C_tZ=16<17,18$ で**常に真に小さい**。
- ⟹ (DEPTH') が成り立つなら、境界一致行では $s^kW_{\rm def}$ が $\operatorname{Im}(C_tZ)$ と $\operatorname{Im}A_t$ に挟まれて**両者と一致**せねばならない。すなわち **(DEPTH') は「$\operatorname{Im}A_t$ がフィルトレーション段そのもの」という強い予言を出す** — 検証可能だが、余裕(slack)がゼロなので苦しい。
- **より素直な説明候補**: $\operatorname{Im}A_t$ が **$t$ に依存しない固定部分空間 $\mathcal I$** であり、$C_t(Z^1)\subseteq\mathcal I$ が全 $t$ で成り立つ。これなら (i) 定数 rank ✓ (ii) 324 行の全通過が族あたり 1 条件に縮む ✓ (iii) 全族で $\operatorname{rank}C_tZ\le\operatorname{rank}A_t$ という数値パターン ✓ (iv) support_two_orbit の「12/24 しか相異ならない」縮退 ✓ をすべて同時に説明する。
- ⟹ **判定: データは (DEPTH') より「不変部分空間 $\mathcal I$」機構を強く示唆する。** 従って **FC-18 を FC-17 より優先**する。

## v2-3. FC-18(新規・最優先)— implementer 向け仕様

**目的**: $\operatorname{Im}A_t$ が $t$ に依らないか、そして $\operatorname{Im}(C_tZ)\subseteq\mathcal I$ が族あたり 1 条件に縮むかを決定する。
**入力**: 既存 producer の $A_t$($42\times21$ 等)と $C_tZ$。新規計算なし。
**手順**(族ごと・全 324 行):
1. 各 $A_t$ の**列空間**の正準表現を作る:$A_t^{\mathsf T}$ を RREF し、pivot 行集合と正準基底行列 $B_t$ を得る(体は族の `field` に従う:3 or 2)。
2. $\{B_t\}_{t}$ が全行で一致するか判定。**一致 ⟹ $\mathcal I$ 確定**。
3. 一致しない場合、$\mathcal I_\cap:=\bigcap_t\operatorname{Im}A_t$ と $\mathcal I_\Sigma:=\sum_t\operatorname{Im}A_t$ の次元を報告(どの程度動くかの定量化)。
4. $\mathcal I$(または $\mathcal I_\cap$)に対し $\operatorname{Im}(C_tZ)\subseteq\mathcal I_\cap$ を全行で判定。
**出力**: 族 × {`image_constant: bool`, `dim I_cap`, `dim I_sum`, `CZ_in_I_cap_rows`}。
**判定の意味**: 2 が YES なら**説明定理の骨格が確定**(あとは $\mathcal I$ を構造的に同定するだけ)。NO かつ 3 で $\dim\mathcal I_\cap$ が小さいなら、消滅は行ごとの事情であり族定理は期待薄 ⟹ 裁定 1159 維持。

## v2-4. FC-17 改(条件付き)— implementer 向け仕様

**Step 0(退化検査・必須・これだけでも先に走らせる).**
$s$ 作用行列の**出所は新規入力ではない**: producer は $Z^1=\ker(1+\rho(\theta))\oplus\ker(1+\rho(\tau)+\rho(\tau)^2)$ を作るために $\rho(\theta),\rho(\tau)$ を**既に持っている**(escape28 / escape2 の preflight で marked 作用として構成済み)。そこから
$$s_\tau:=\rho(\tau)-I\ (\text{field }3\ \text{の 4 族}),\qquad s_\theta:=\rho(\theta)-I\ (\text{field }2\ \text{の support\_two\_orbit})$$
を作り、**$\operatorname{rank}(s)$ を報告**する。
- **$\operatorname{rank}(s)=0$ なら局所フィルトレーションは自明**($V$ は $\mathbf F_p[C_p]$ 上自明加群)⟹ **(DEPTH') は空虚・その場で FC-17 を打ち切り、FC-18 のみ続行**。これが司令塔の懸念(trivial_character で $\tau$ 自明 ⟹ $s=0$)への処方である。
- **懸念は実在する**が現時点では**確定していない**。次元算術で検算できる: 標数 3 では $\mathbf F_3[C_2]$ は半単純なので $\ker(1+\theta)=V^{\theta=-1}$、$\mathbf F_3[C_3]$ は局所で $\ker(1+\tau+\tau^2)=\ker s_\tau^2$。よって
 $$\dim Z=\dim V^{\theta=-1}+\bigl(\dim V-\operatorname{rank}s_\tau^2\bigr).$$
 trivial_character:+($\dim V=7$, $\dim Z=10$)は $(\dim V^{\theta=-1},\operatorname{rank}s_\tau^2)=(3,0)$ で整合するが $(4,1)$ でも整合するので**$\tau$ 自明とは断定できない**。⟹ Step 0 の実測が必要。
 (標数 2 の族では役割が逆転: $\mathbf F_2[C_2]$ が局所で $\ker(1+\theta)=\ker s_\theta$、$\mathbf F_2[C_3]$ は半単純。)
**Step 1(終域の作用・条件付き).** (DEPTH') は $W_{\rm def}$ 上のフィルトレーションを要する。producer が $W_{\rm def}$ 上の $\theta,\tau$ 作用を保持しているか確認し、**保持していなければ「target action not carried」と報告して FC-18 へ回す**(欠損空間は二 hexagon の残差の直和なので作用は原理的に定まるが、実装が持っていない可能性が高い)。
**Step 2(測定).** 族 × 行ごとに $\dim\operatorname{Im}A_t$、$\dim\operatorname{Im}(C_tZ)$、$\dim s^kW_{\rm def}$($k=0,1,2,3$)を出し、**$\operatorname{Im}A_t=s^kW_{\rm def}$ なる $k$ が存在するか**を判定(v2-2 (3) の予言の直接検証)。

## v2-5. 優先順位と申告

**FC-18(Step 1–4)→ FC-17 Step 0 → 必要なら FC-17 Step 1–2。** FC-18 は既存行列だけで完結し、YES なら裁定 1159 の「説明定理なし」を閉じる骨格が出る。
- 本追補で新たに手計算検証したのは:型エラー(v2-1)、$\dim Z$ の次元算術(v2-4 Step 0)、境界一致から (DEPTH') が出す予言(v2-2 (3))。
- **UNKNOWN**: FC-17/18 の結果。$\mathcal I$ の構造的同定。裁定 1159 は**依然閉じない**。
- 本文 §0 の裁定「(a) 不成立」は**維持**(FC-16 = NO はそれを覆さない)。変わったのは**次の一手の指定**である。

---

# 追補 v3(2026-08-19)— FC-18 = NO と FC-17 Step 0 の判定

出典: cert `search/certs/fc18_imAt_constancy_v1_20260819.json`(1,620/1,620 ハッシュ一致・恒等式 $A_tT_t+C_tZ\equiv0$ 全行成立)。v1 本文・追補 v2 は凍結、以下は追記。

## v3-0 一行裁定

**$\mathcal I$ 固定仮説は死亡。私の「$A_t=U_tA_0W_t$(単元活動)」も、司令塔の「$(A_t,C_t)$ 同変」も、いずれも既報の数値だけで決着する — 前者は真だが内容ゼロ、後者は反証。加えて (DEPTH′) も次元勘定で反証。⟹ 幾何(部分空間)側の説明線は全滅し、残るのは witness $T_t$ の規則性ただ一本(FC-19)。同時に、FC-17 Step 0 の 3 数から 5 族の加群構造が完全に決まり、$H^2$ の 2 つの実測値を再現した。**

## v3-1 【自己訂正】「定数 rank は単元活動の指紋」は誤り(内容ゼロ)

追補 v2 §v2-2(2) で「108 個の $A_t$ が相異なるのに rank が定数 ⟹ $A_t=U_tA_0W_t$」と書いたが、**体上の行列の $GL\times GL$-同値類は rank だけで完全分類される**。従って
> 「全 $A_t$ が $U_tA_0W_t$ の形」$\iff$「$\operatorname{rank}A_t$ が定数」
であり、**両者は同一の言明**である。既知の事実を言い換えただけで、包含 $\mathcal C_t\subseteq\mathcal A_t$ の説明力は**ゼロ**。撤回する。

## v3-2 司令塔の同変性仮説は既報数値で**反証**される(新規計算不要)

**補題(必要十分).** 包含 $\mathcal C_t\subseteq\mathcal A_t$ が全 $t$ で成り立つとき、次は同値:
1. $\exists U_t\in GL(W_{\rm def}),V_t\in GL(V),S_t\in GL(Z)$: $A_t=U_tA_{t_0}V_t$ **かつ** $C_tZ=U_t(C_{t_0}Z)S_t$(= 司令塔の同変性);
2. $\operatorname{rank}A_t$ と $\operatorname{rank}(C_tZ)$ が**ともに** $t$ に依らず定数。
*証明.* (1)⟹(2) 自明。(2)⟹(1): 入れ子対 $(\mathcal A_t,\mathcal C_t)$ は $GL(W_{\rm def})$ の**旗**であり、$GL$ は与えられた次元型の旗に推移的に作用する ⟹ $U_t\mathcal A_{t_0}=\mathcal A_t$, $U_t\mathcal C_{t_0}=\mathcal C_t$ なる $U_t$ が取れ、$V_t,S_t$ は基底の取り替えで得る。∎

⟹ **判定は既報の「max rank $C_tZ$」欄で終わっている**: trivial_character:+ は $\operatorname{rank}C_tZ=4$ が 240 行・残り 84 行は $<4$、すなわち**$\operatorname{rank}(C_tZ)$ は $t$ に依存する**。⟹ 条件 2 が破れる ⟹ **同変性仮説は反証**。
**⟹ FC-19 を「拡大行列 $[A_t\mid C_tZ]$ の $GL$-同値類比較」や「$(\mathcal A_t,\mathcal C_t)$ の相対位置不変量」として実装してはならない** — それらは次元対だけの不変量であり、答えは既に出ている。

## v3-3 FC-17 Step 0 の 3 数から加群構造が完全に決まった(本追補の実質)

$s^3=0$(char 3, $\tau^3=1$)/ $s^2=0$(char 2, $\theta^2=1$)と Jordan 型の標準計算($\#$blocks$=\dim-\operatorname{rank}s$ 等):

| family | $(\dim,\operatorname{rank}s,\operatorname{rank}s^2)$ | 加群構造 | $H^2$ |
|---|---|---|---|
| orbit_bundle | $(21,14,7)$ | $\;\mathbf F_3[C_3]^{\oplus7}$ — **自由!** | $H^{*>0}=0$ |
| trivial_character | $(7,4,1)$ | $\;\mathbf F_3[C_3]\oplus J_2^{\oplus2}$($J_2=k[C_3]/s^2$) | $\dim\ker s-\dim s^2V=3-1=\mathbf 2$ |
| support_two_orbit | $(12,5,0)$ | $\;\mathbf F_2[C_2]^{\oplus5}\oplus\mathbf F_2^{\oplus2}$ | $\dim\ker s-\dim sV=7-5=\mathbf 2$ |

**検証**: $21+7=28$ ⟹ $V_{28}=V_{21}\oplus V_7$(orbit_bundle ⊕ trivial_character)。自由加群は $H^{*>0}=0$ なので
$$H^2(C_3,V_{28})=0\oplus2=\mathbf 2\quad✓,\qquad H^2(C_2,V_{12})=\mathbf 2\quad✓$$
— **戦役が引用してきた 2 つの実測値を独立に再現した。**

**構造的含意(新規)**: **ESCAPE-28 の $H^2$ 障害は全て trivial_character 成分 $V_7$ に住み、orbit_bundle 成分 $V_{21}$ は $\mathbf F_3[C_3]$ 上自由=コホモロジー的に自明**である。⟹ orbit_bundle 族での消滅は「$\tau$ 方向のコホモロジー的障害がそもそも無い」ことで**部分的に説明され得る**(ただし当該障害は $\operatorname{coker}A_t$ であって $H^2$ そのものではないので、直結は要証明)。**これは 1159 に向けた最初の構造的手掛かりである。**

## v3-4 (DEPTH′) も次元勘定で反証される

(DEPTH′) は $\dim\mathcal C_t\le\dim s^kW_{\rm def}\le\dim\mathcal A_t$ なる $k$ の存在を要求する。$W_{\rm def}\cong V^{\oplus2}$(二 hexagon 残差)と仮定すると:
- **orbit_bundle:+**: 必要な窓は $[16,17]$。$\dim s^kW=42,28,14,0$ ⟹ 窓に入る $k$ **なし** ✗
- **orbit_bundle:−**: 窓 $[16,18]$ ⟹ 同じく**なし** ✗
- **support_two_orbit**: 窓 $[9,9]$。$\dim s^kW=24,10,0$ ⟹ **なし** ✗
⟹ **(DEPTH′) は 5 族中少なくとも 3 族で反証**。
**前件**: $W_{\rm def}\cong V^{\oplus2}$($C_p$-加群として)。これは 1 行で確認できるが、仮に構造が違っても $\dim s^kW$ が $\{16,17\}$ や $\{9\}$ にちょうど嵌まる必要があり、窓は極めて狭い。⟹ **FC-17 Step 1–2(終域フィルトレーションの実測)に implementer 時間を使う価値は無い。**

## v3-5 (a) FC-19 の最終述語 — witness $T_t$ の規則性(implementer 向け)

幾何側が全滅したので、説明は **cert が既に持っている witness $T_t$** に求めるしかない($A_tT_t+C_tZ\equiv0$ が包含の証人)。

> **FC-19(witness regularity).** 族ごと・全 324 行。新規の数学入力なし(既存 $A_t,C_t,Z$ から再計算可)。
> **正準化**: $T_t$ は $\ker A_t$ の分だけ不定。**固定列順の RREF 後退代入で自由変数を 0 に置いた解** $T_t^{\rm can}$ を正準代表とする(producer と同じ RREF 規約を明記して固定すること)。
> **測定**:
> - **(R1)** $\operatorname{rank}T_t^{\rm can}$ は $t$ に依らず定数か。
> - **(R2)** $T_t^{\rm can}$ は $t\mapsto A_t$ のファイバー(サイズ 3/6/27)上で定数か(= $T$ が $A$ のみの関数か)。
> - **(R3) ★中核**: $d_{\rm aff}:=\dim_{\mathbf F_p}\operatorname{span}\{T_t^{\rm can}-T_{t_0}^{\rm can}\ :\ t\}$ を報告。
> - **(R4)** (R3) が小さいときのみ: 324 行の群構造に対する $T_{tt'}$ と $(T_t,T_{t'})$ の関係(準同型/crossed hom 型)を探索。
> **判定**: $d_{\rm aff}$ が小さい(数個)⟹ **$T_t=\Phi(t)$ の閉形式が射程内**であり、その $\Phi$ こそが説明定理。$d_{\rm aff}$ がほぼ最大 ⟹ 消滅は行ごとの事情 ⟹ **裁定 1159 維持**。
> **出力**: 族 × {`rank_T_const: bool`, `T_const_on_A_fibres: bool`, `d_aff: int`, `dim_T_space: int`}。

## v3-6 (b) ファイバーサイズ 3 / 6 / 27 の解釈(断定なし・検査可能な予言つき)

$324=2^2\cdot3^4$。ファイバー 3, 6, 27 ⟹ 像 108$=2^2 3^3$, 54$=2\cdot3^3$, 12$=2^2\cdot3$。3-部分の潰れは $3^1,3^1,3^3$、2-部分は $1,2,1$。
**最有力の解釈**: $t\mapsto A_t$ は $t$ の**当該族の加群への作用**を通してのみ依存し、ファイバーはその作用の核の剰余類である。
> **予言 FC-20(検査可能)**: ファイバーは**部分群の剰余類**をなす(324 行の群構造に対して)。かつファイバー $=\ker\bigl(t\mapsto\rho_{\rm fam}(t)\bigr)$($\rho_{\rm fam}$ = roof 元の $V_{\rm fam}$ への誘導作用)。
> 検査は既存データで可能(ファイバー分割が剰余類分割かを判定し、$\rho_{\rm fam}$ の核と突合)。**YES なら $A_t$ の $t$-依存性が $\rho_{\rm fam}$ に還元され、(R3) の $d_{\rm aff}$ が小さいことの理由になり得る。**
支持材料: support_two_orbit のファイバーが $27=3^3$ と大きいのは、char 2 の族なので roof の 3-部分が加群作用にほとんど効かない、という読みと整合的(断定はしない)。

## v3-7 (c) 優先順位の裁定と 1159 の見通し

| 線 | 裁定 |
|---|---|
| 同変性(FC-19 を幾何で実装する案) | **不要**。v3-2 で既報数値により反証済み |
| (DEPTH′) / FC-17 Step 1–2 | **不要**。v3-4 で次元勘定により反証済み |
| **FC-19(witness $T_t$ の規則性)** | **唯一の生存線・最優先**。既存データのみ・新規数学入力なし |
| FC-20(ファイバーの剰余類性) | FC-19 と同時に走らせられる安価な補助 |

**1159 の見通し(一行)**: 説明定理があるとすれば、それは**部分空間の幾何ではなく witness $T_t$ の閉形式** $T_t=\Phi(t)$ であり、その存否は FC-19 の $d_{\rm aff}$ 一つで決まる。加えて v3-3 の「$V_{21}$ 自由 ⟹ $H^{*>0}=0$」は、少なくとも orbit_bundle 族については**構造的理由が実在する**ことを示しており、説明定理の第一歩はそこにある可能性が高い。

## v3-8 申告(追補分)

- 手計算で検証: Jordan 型の 3 族分(v3-3)、$21+7=28$ と $H^2$ 2 値の再現、v3-2 の必要十分補題、v3-4 の次元窓、v3-1 の $GL\times GL$-分類。
- **自己訂正 1 件**: 追補 v2 §v2-2(2) の「定数 rank = 単元活動の指紋」を撤回(内容ゼロ)。
- **前件**: v3-4 は $W_{\rm def}\cong V^{\oplus2}$ を仮定(1 行で確認可)。v3-3 は $s$ の冪零次数($\tau^3=1,\theta^2=1$)のみ使用。
- **UNKNOWN**: FC-19 / FC-20 の結果。$\operatorname{coker}A_t$ と $H^2$ の関係。裁定 1159 は**依然閉じない**。
- 本文 §0 の裁定「(a) 不成立」は維持。**B4-B は宣言していない。**
