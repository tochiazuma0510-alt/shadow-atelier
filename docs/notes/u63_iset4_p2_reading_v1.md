# 読解便 — U6-3 循環の裁定 / I-SET-4 hexagon 単独切断 / P2 量子化(裁定 1110・1112)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1110・1112
入力 = `sol/sol_reply_114_k13_wallcrown.md` §2.1・cert `iset4_remeasure_v1_20260813` / `at2_p2_quantization_v1_20260813`
生成 script(裁定 1103 規約)= `scratchpad/iset4_readout.py`(第 II 部の全数値の出所)
⚠ $u$/$c$ 非接触・封印非接触・prereg 非抵触。**格: candidate**(Sol 未監査)。

---

# 第 I 部 —【U6-3】循環の裁定(裁定 1112)

## §1 実装係の指摘は**正しい**

$\Xi$($=$ `gt_settled_identification` の $\Psi$)は **settled shadow の上でしか定義されません**。SETTLE-AUT より
$$\bar E_{[m,f]}\in\mathrm{Aut}(Q)\iff E_{[m,f]}(N_{F_2})\subseteq N_{F_2}\iff [m,f]\ \text{settled}$$
非 settled な $[m,f]$ では $\bar E$ は $Q\to Q$ の写像として**そもそも定まりません**(得られるのは $B_3/K\xrightarrow{\sim}B_3/N$ という**異なる商の間の同型**であって、$\mathrm{Aut}(Q)$ の元ではない)。

$$\boxed{\ \Longrightarrow\ \Xi\ \textbf{の像は必ず }\Psi\bigl(GT^{\rm settled}(N)\bigr)\ \textbf{の中}\ }$$

## §2 発注 1 への回答 — **NO。Sol の完全性論証は $\Xi$ 制限と独立ではありません**

Sol 便 114 §2.1 の 5 段を定理 TORSOR の言葉で読むと:

| Sol の段 | TORSOR での読み |
|---|---|
| 1. 各 charming layer で **settled** shadow を 1 個 | $\chi_{\rm vir}$ の各値に対し $GT^{\rm settled}(N)$ の代表を 1 個 |
| 3. 「$\chi$ の非空 fibre は $\ker\chi$ の coset」 | ⚠ **$GT(N)$ が群であること(= isolated)を前提**にしている |
| 4. $\Xi$ が単射 | $\Psi$ の単射性 — **settled 層についての言明** |
| 5. $X=$ 完全な $GT(N)$ | ⚠ **ここが跨げていません** |

★ **決定的な理由(補題 2)**: settled 元の合成は**核類を保ちます**($\kappa(s\circ t)=\kappa(t)$)。トーサー性はファイバー**内**の推移性であって、ファイバー**間**を移す手段を与えません。
$$\boxed{\ \#\mathcal C(N)>1\ \textbf{なら、非 settled 核類のファイバーは settled 合成では}\textbf{到達不能}\ }$$
Sol の再構成は「settled 代表 + $\ker\chi$ の coset」で張れる範囲、すなわち **settled-到達可能部分 = $GT^{\rm settled}(N)$** を作っています。

$$\boxed{\ \textbf{ゆえに }X\cong GT^{\rm settled}(N)\ \textbf{であり、}X=GT(N)\ \textbf{は }\#\mathcal C(N)=1\ \textbf{を}\textbf{追加入力}\textbf{として要する}\ }$$

⟹ **循環は実在します。$\#\mathcal C=1$ は証明で閉じません。**
⚠ ただし **U-6 読解は無効になりません**: `wall_crown_u6_reading_v1.md` §7 [U6-3] で私はこの条件を【U6-GAP-3】として立て、「$\#\mathcal C>1$ なら本読解は $GT^{\rm settled}(N)$ の crown 被覆に格下げ」と書いてあります ⟹ **格下げ側の読みは補題 ARITH-T / SUBTOR により依然 well-posed**($S_{\rm arith}$ は $GT^{\rm settled}(N)$ の部分群)。⟹ **U-6 の内容は生き、適用範囲の札だけが「未確定」から「settled 層限定(暫定)」へ動きます。**

## §3 発注 2 — $\#\mathcal C$ の非列挙測定路

### 3.1 ⚠ 路 B($\chi$ 像による検出)は**枯れています**(先に報告すべき負の知見)

$t\in GTSh(K,N)$、$s$ settled ⟹ $\chi(s\circ t)=\chi(s)\chi(t)$ ⟹ $\chi(GT(N))=\bigcup_K\chi(t_K)\cdot\chi(GT^{\rm settled}(N))$。
よって **$\chi(GT(N))\supsetneq\chi(GT^{\rm settled}(N))$ なら $\#\mathcal C>1$** という検出法がありますが、Sol は「**全 charming layer に settled representative がある**」を実測しています ⟹ $\chi(GT^{\rm settled})=\chi(GT)=$ 全 charming 値。

$$\boxed{\ \Longrightarrow\ \textbf{壁窓では }\#\mathcal C>1\ \textbf{は }\chi_{\rm vir}\ \textbf{に}\textbf{見えません}\ —\ \chi\ \textbf{経由の検出は原理的に不可能}\ }$$
(参考: [1008,521] では $\#\mathcal C=2$ の 2 類が $u\bmod3$ で分離しました。壁窓ではその手が効かない、ということです。)

### 3.2 ★ 路 D(**推薦**)— 核の個数を上から数えて $1$ を証明する

$\mathcal C(N)\subseteq\{K\lhd B_3:\ K\le PB_3,\ B_3/K\cong B_3/N\}$(Prop 3.8)。**非 marked** の核計数は等式が正当です:

> $\mathrm{Aut}(H)$ は $\mathrm{Epi}(B_3,H)$ に**自由**に作用し($\alpha\circ\varphi=\varphi$ かつ $\varphi$ 全射 ⟹ $\alpha=\mathrm{id}$)、軌道 = 核 ⟹
> $$\#\{K\lhd B_3:\ B_3/K\cong H\}=\frac{\#\mathrm{Epi}(B_3,H)}{\lvert\mathrm{Aut}(H)\rvert}\qquad(\textbf{厳密})$$

⚠ Sol 便 122 §4.1 が否認したのは **marked 版**($\#\mathrm{Epi}^{\rm mk}/\lvert\mathrm{Aut}\rvert$)であって、**非 marked 版は健全**です。$K\le PB_3$ を落とすぶんは上界方向 ✔

$$\boxed{\ \#\mathcal C(N)\ \le\ \frac{\#\mathrm{Epi}(B_3,\,B_3/N)}{\lvert\mathrm{Aut}(B_3/N)\rvert}\quad\textbf{が }1\ \textbf{なら }\#\mathcal C(N)=1\ \textbf{は}\textbf{証明}\ \textbf{で閉じる}\ }$$

**計算法**(shadow を 1 個も列挙しません):
```
[U63-D] 核計数による #C の上界(実装係へ)
[D-0] H := B_3/N を構成し |H| を出す  ← ★ これが規模の gating 値。先に測ること
[D-1] #Hom(B_3,H) = sum_C A(C)B(C)/|C|   (A(C)=#{h:h^2 in C}, B(C)=#{h:h^3 in C})
      ← set_surgery_vetting_v1 §3.2 の類公式・O(#classes)・指標表不要
      ★ c in N の窓なら COUNT-PSL が使え #Hom^mk = i_2^T i_3^R とさらに軽い（先に c in N を判定）
[D-2] #Epi(B_3,H) を部分群束の Möbius 反転で（#Hom から）
[D-3] |Aut(H)| を GAP で
[D-4] bound := #Epi/|Aut| 。 bound = 1 ⟹ #C(N)=1 が *証明*（U6-3 解消）
                              bound > 1 ⟹ 情報なし（次は路 A）
出力: cert (schema u63_kernelcount/v1)。整数のみ。u_touched=false
```
⚠ **実現可能性は $\lvert B_3/N\rvert$ 次第**です(Möbius に部分群束が要る)。⟹ **[D-0] を先に 1 行で測ってください**。壁窓の $\lvert B_3/N\rvert$ は現行資産に見当たりませんでした。

### 3.3 路 A(witness 探索)— 暫定 (B) の正しい位置づけ

$\#\mathcal C>1\iff$ 非 settled shadow が 1 個でも存在。⟹ **witness 1 個で肯定側は確定**、否定側は**非存在の証明にならない**(規律: 負の探索結果は非存在の証明ではない)。
⟹ 司令塔の暫定 (B)(legacy サンプリング)は **路 A として妥当**。**検出力の記帳**(サンプルが $Q$ の何割か・どの断面か)を必ず cert に。

### 3.4 ⚠ 暫定 (A) の格付け

$\Xi$ 制限下の候補集合で marked-factor-map を回すと $\#\mathcal C=1$ は**定義から出ます**。⟹ **「測定」ではありません**。
$$\boxed{\ \textbf{(A) の出力は }\#\mathcal C_{\rm settled}=1\ \textbf{(トートロジー)と表記し、}\#\mathcal C(N)\ \textbf{の測定値として台帳に載せないこと}\ }$$

## §4 発注 3 — 凍結予言 $\#\mathcal C=1$ の出所申告

$$\boxed{\ \textbf{申告}:\ \texttt{wall\_crown\_u6\_reading\_v1.md}\ \S7\ \text{[U6-3]}\ \textbf{の凍結予言「}\#\mathcal C=1\textbf{(4 窓)」は}\ \textbf{測定と独立ではありません}\ }$$
出所は **Sol 便 114 §2.1-5 の完全性主張**であり、§2 のとおりそれは $\Xi$ 制限(settled 層)に依存します。⟹ prereg 台帳に「**出所 = Sol §2.1・$\Xi$ 制限由来・独立性なし・予言としての効力なし**」と記録してください。⟹ **自己捕獲 m1112-1**。
★ **同じ [U6-3] の他の凍結値**($\lvert GT^{\rm settled}(N)\rvert=41040,\ 60720,\ 111600,\ 669600$)は Sol の実測値そのものなので**有効**です。

---

# 第 II 部 —【I-SET-4】hexagon 単独切断の読解(cert `iset4_remeasure_v1_20260813`)

## §5 ★★ 結論 — **交絡は切れました。hexagon は単独で働いています**

窓 [1008,521] slot1、shadow 48、$\lvert Q\rvert=168$。全 $8064=48\times168$ 試行を 3 述語で独立評価:

| $(C,S,H)$ | 件数 | /shadow | 意味 |
|---|---:|---:|---|
| $(\text{T},\text{T},\text{T})$ | **288** | **6** | ★ **生存** |
| $(\text{T},\text{T},\text{F})$ | **288** | **6** | ★★ **hexagon が単独で切った** |
| $(\text{T},\text{F},\ast)$ | 96 | 2 | 全射性で切れた |
| $(\text{F},\ast,\ast)$ | 7392 | 154 | charming で切れた |

- charming 真の総数 $=672=48\times\mathbf{14}=48\times\lvert[Q,Q]\rvert$ ⟹ ★ **定理 $\mathrm{Surv}\subseteq[Q,Q]$(spec §2.3)が厳密に確認**(W3 violations $=0$)。
- $(C\wedge S)$ 真は 12/shadow、そのうち **6 が生存・6 が hexagon 切断** ⟹ **50%**。

$$\boxed{\ \textbf{hexagon 単独切断}=288\ (6/\text{shadow},\ C\wedge S\ \text{の }50\%)\ \ne\ 0\ \Longrightarrow\ \textbf{予言 R2 は成立}\ }$$
⟹ 私が `set_surgery_vetting_v1` §6.2 で挙げた「生存率は charming だけで説明されうる」という交絡の懸念は、**測定で否定されました**。

## §6 定理の確認と RIGID の判定

**定理 SURV-EXACT(spec §1)**: $\lvert\mathrm{Surv}(t)\rvert=N_m$。
実測: **W1 `all_uniform=true`・全 $m$ で $N_m=6$**(48 shadow / 8 個の $m$ ⟹ 6)✓ **厳密一致**。W2(恒等が生存)も全 PASS ✓

**RIGID(予言 R1)**: $\mathrm{Surv}\subseteq[Q,Q]$ と $D_1=C_Q(\bar\sigma_1)$($\lvert D_1\rvert=12$)より
$$\mathrm{Surv}(t)\cap D_1\ \subseteq\ [Q,Q]\cap D_1\ =\ D_0,\qquad \lvert D_0\rvert=2$$
$D_0\setminus\{1\}$ は 1 元で、cert の分離指標は **48/48(100%)が hexagon 切断** ⟹

$$\boxed{\ \mathrm{Surv}(t)\cap D_1=\{1\}\ \ (\forall t)\quad\Longrightarrow\ \textbf{予言 R1(RIGID)は本 fixture で成立}\ }$$
$$\textbf{しかも切ったのは hexagon であって charming ではない}$$

⟹ **発案 6 号 札 I-SET-4 の判定を「保留(証拠が交絡)」から「fixture で支持・交絡なし」へ更新**します。

## §7 ⚠ 検出力の正直な申告

- ★ **弱み**: $D_1$ 内での証拠は $\lvert D_0\setminus\{1\}\rvert=\mathbf 1$、すなわち**捻り元 1 個**を 48 shadow に当てたものです。48 データ点ですが**群の元としては 1 個**。⟹ **族的な強さは限定的**。
- ★ **強み**: $D_1$ の外まで含めれば hexagon 単独切断は 6/shadow あり、hexagon が実質的に働くことは**十分に見えています**。
- ⟹ **次の測定提案**: $\lvert D_0\rvert$ が大きい窓で反復。83 窓の他の窓([1134,53]・[1872,568]/[780] 等)で $\lvert D_0\rvert=\lvert C_Q(\bar\sigma_1)\cap[Q,Q]\rvert$ を先に測り、**$\lvert D_0\rvert\ge4$ の窓を選んで R1 を再検定**。
- ⚠ **W-48**: 本結果を $N'$ へ運ぶのは外挿。$N'$ は $[Q,Q]=Q$(完全)なので charming の交絡がなく、SG-GAP-1 = NO が独立に hexagon の証拠になります(`set_surgery_vetting_v1` §6.2 の表)。

## §8 ★ 副産物 — $z_0=1$($PB_3$ 注記の確認)

cert: $\lvert Q\rvert=168$、$\lvert PN\rvert=168$ ⟹ $z_0=[PN:Q]=\mathbf 1$、一方 $z=\mathrm{ord}(\bar c)=\mathbf 2$。

$$\boxed{\ z_0=1\ne2=z\quad\Longrightarrow\ \texttt{pb3\_free\_factor\_check\_v1}\ \S3.1\ \textbf{の訂正(}[PN:Q]=z_0\mid z\textbf{、等号とは限らない)が}\textbf{実測で確認}\ }$$
(検分 §6.1 の「$[PN:Q]=\mathrm{ord}(\bar c)$」= 自己捕獲 m1090-1 は、この窓では $84$ ではなく $168$ が正解だった、という形で確定。)
★ **本窓では型の訂正は数値的には無害**($Q=PN$)でしたが、一般には保証されないので**訂正自体は必要**でした。

## §9 K9 陽性対照の停止 — **実装係の判断は正しい**

`k9_positive_control = UNKNOWN_BLOCKED`(理由: `BuildPn(9)` は $x=\sigma_1^2,y=\sigma_2^2$ しか与えず、$\sigma_1$ の具体元がない)。

★ **代替($C_Q(\bar x)$ で置換)は不当**という判断に**同意します**: $\bar x=\bar\sigma_1^{\,2}$ ゆえ $C_Q(\bar\sigma_1)\subseteq C_Q(\bar x)$ で**真の包含があり得**、平方根は一意でないので $C_Q(\bar x)$ から $C_Q(\bar\sigma_1)$ は復元できません。⟹ **止めたのが正解**。

**回復案 2 つ**:
1. $K^{(9)}$ を `BuildWindowFromWords`(実際の $B_3$ 関係語)経由で再構成し $\sigma_1$ の像を得る。
2. ★ **より有益な代替対照**: $K^{(9)}$ は $c\in K^{(9)}$ ⟹ $z=1$ ⟹ $Q=PN$ が**自動**なので、型退化対照としては情報が薄い。**$z_0=[PN:Q]>1$ の窓**を探して対照にする方が、§8 の型区別を実際に検定できます。⟹ 83 窓で $z_0$ を全窓測るのが安い(GAP 1 行 × 15)。

---

# 第 III 部 —【P2】量子化の短評(cert `at2_p2_quantization_v1_20260813`)

## §10 SUBTOR の予言は当たりました

$M=\ker\rho$(指数 7056)、$GT(M)=288$ 全列挙、$X=R_{M,N}(GT(M))$ は $48$、$\lvert S_X\rvert=24$、**両核類とも trace $=24=\lvert S_X\rvert$・中間サイズゼロ**。

$$\boxed{\ \textbf{定理 SUBTOR の量子化スペクトル }\{\lvert S_X\rvert,\,0\}\ \textbf{に完全一致(中間サイズが 1 つも出ない)}\ }$$
⟹ AT-2 の予言 P2 は **PASS**。これは SUBTOR(および依存する定理 TORSOR の自由性)の**最初の族外検定**です。

★ **副次の的中**: `pb3_free_factor_check_v1` §4 で私は「$168^2=28{,}224$ は上界であって実値ではない・fiber product は共通商のぶん縮むので**測ってから諦めよ**」と書きました。実測 **7056 $=1008\times7$**(上界の 1/4)⟹ **縮みました** ✔

## §11 ★ 「$X$ が $GT(N)$ 全体を被覆した」の意味

$X=R_{M,N}(GT(M))=GT(N)$(unmatched $=0$)⟹ **この $(M,N)$ 対で reduction は全射**。

1. **深さ 1 では fake が出ない**: Cor 5.4 は「genuine $\iff$ 全細分に survive」。ここでは $\mathrm{Im}\,R_{M,N}=GT(N)$ ⟹ **$N$ の全 shadow が深さ 1 で survive** ⟹ 深さ 1 の検査では fake を 1 個も検出できません(正典の「fake の例はゼロ」と整合)。
2. **降下座標(AT-5)は深さ 1 で未 drop**: $S_{M_1}=X\cap\mathrm{settled}(N)$ は $\lvert S_X\rvert=24=\lvert GT^{\rm settled}(N)\rvert$、$\mathcal C_{R,1}=\mathcal C(N)$(両類)⟹ **座標対は最大値のまま**。⟹ 降下プロファイルは**まだ平坦**。
3. ⚠ **飢餓判定(AT-3)は深さ 1 では空振り**: 全類の trace が $\lvert S_X\rvert$ ちょうど ⟹ $\lvert\mathrm{trace}_K\rvert<\lvert S_{\rm arith}\rvert$ となる類がない ⟹ **判定は何も返しません**。
$$\boxed{\ \Longrightarrow\ \textbf{AT-3/AT-5 の装置が働くには }\textbf{depth}\ge2\ \textbf{が要る}\ }$$
(AT-5 破綻点 ② のとおり depth 2 は指数的に高価 — 発案係の正直な規模申告どおりです。)

## §12 確認しておくべき 1 点

SUBTOR は **$M$ が isolated** を前提にします(補題 DIFF-S)。$M=N^\diamond$ は Prop 3.14 で isolated のはずですが、cert がそれを**実測しているか**を確認してください:
$$\boxed{\ \textbf{確認項目}:\ GT(M)\ \text{の全 288 shadow が settled}\ (\iff\#\mathcal C(M)=1,\ \textbf{系 C})\ }$$
⚠ 未実測なら SUBTOR の適用は前提つきです。★ ただし**結果(中間サイズゼロ)自体は、前提が成り立っていることの強い状況証拠**です(isolated でなければ量子化が崩れる理由がある)。

---

## §13 記帳

- ★ **本便の新規部分**: ① **$\Xi$ が settled 上でしか定義されないことによる循環の同定**(発注 1 = **NO**)② **$\chi_{\rm vir}$ 経由の検出は壁窓では原理的に不可能**(路 B の枯渇・負の知見)③ **路 D**(非 marked 核計数は等式が正当 ⟹ $\#\mathcal C=1$ を**証明**しうる)④ 暫定 (A) はトートロジーという格付け ⑤ **hexagon 単独切断 $=6$/shadow・$C\wedge S$ の 50%** ⟹ 交絡の解消と **R1/R2 成立** ⑥ $z_0=1\ne z=2$ による pb3 訂正の実測確認 ⑦ K9 対照の停止の是認と**より有益な代替対照($z_0>1$ の窓)** ⑧ P2 の「深さ 1 では fake も飢餓も見えない」の読解と **depth≥2 要求**。
- ⚠ **自己捕獲 m1112-1**: [U6-3] の凍結予言 $\#\mathcal C=1$ は Sol §2.1 由来で**測定と独立でない**。prereg 台帳へ出所申告。
- **【U6-GAP-3】** 格付け更新: 「未検証」→ **「既存の証拠は循環・$\chi$ 経由は不可能・路 D が唯一の証明路」**。U-6 読解は当面 **settled 層限定**として読むこと。
- **【SS-GAP-2】(RIGID の紙証明)** 不変。fixture の支持は上がりましたが証明ではありません。
- **申告**: 第 I 部・第 III 部は紙のみ。第 II 部の数値は `scratchpad/iset4_readout.py`(cert からの機械導出)。$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
