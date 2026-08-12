# R-1 達成宣言(**草案** — Sol 監査前・研究者検分前)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1090
入力 = cert `d2_gate_v1_20260813.json` + `d2_gate_v1_track_20260813.json`(run 31630925950)・`p1d2_r1_canonicalization_v2.md`・`d2gap4_gate_adjudication_v1.md`・falsifier 監査 `fals_p1d2_r1_audit_v1.md`
⚠ **本書は草案です**(発令ではありません)。$u$/$c$ 非接触・**prereg 量($d_9$・$r$)非計算**・封印非接触。

---

# 第 I 部 — §8.3 の正式読解

## §1 分岐判定

`p1d2_r1_canonicalization_v2.md` §8.3 の 5 分岐に対する実測値:

| 量 | 実測 | 予言 | 判定 |
|---|---|---|---|
| $\lvert\mathrm{Mon}(W(P_1))\rvert$ | **324** | **PRED-1**: $\in\{324,972,2916\}$・$\ne419904$ | ★ **的中** |
| $\lvert\mathrm{Mon}(W(P_2))\rvert$ | **419904** | **PRED-2**: $=419904$ | ★ **的中** |
| $W(P_1)$ の三つ組 vs $\lambda_9$($S_{18}$-共役・marked) | **true** | 分岐 (a) の条件 | ★ **該当** |
| $W(P_2)$ の三つ組 vs $\lambda_9$ | **false** | 対照 | ✔ |
| passport($\sigma_0$ 18-cycle・$\sigma_1$ $2^81^2$・blocks [3,9]・transitive) | 一致 | [G-5] 見張り | ✔ |

$$\boxed{\ \textbf{分岐 (a) 該当}\ \Longrightarrow\ W_9=W(P_1).\ \textbf{【CAN-1】【CAN-2】とも不要}\ }$$

★ **予言 2 本の的中は偶然ではありません**: PRED-1/PRED-2 は**数値を見る前に**、exact な組合せ census(GAP・72 本の $\lvert\mathrm{Mon}\rvert$ 分布と resolvent 類の Galois 安定性)から導かれ凍結されました。⟹ **exact な組合せ側が数値側を予言し、数値側が的中させた**という関係が成立しています(§4 の格の議論)。

## §2 技術的 2 点への回答(司令塔の問い)

### 2.1 $\sigma_\infty$ が積関係からの導出であることの扱い — ★ **問題ありません**

$\pi_1(\mathbf P^1\setminus\{0,1,\infty\})$ は $g_0,g_1$ で**自由**であり、$g_\infty=(g_0g_1)^{-1}$ は**関係式による定義**です。被覆は $(\sigma_0,\sigma_1)$ で**完全に決まります**(Riemann 存在定理)。
⟹ $\sigma_\infty$ を導出することは情報の欠落ではなく、**そもそも独立に測るべき量ではありません**。
★ ただし「$\sigma_\infty$ が 18-cycle」は**追跡の健全性検査としては有効**(追跡が壊れていれば $\sigma_0\sigma_1$ の位数が 18 になる理由がない)⟹ cert が導出値と明記したうえで見張りに使っているのは**正しい運用**です。

### 2.2 $S_{18}$-共役(marked)判定の十分性 — ★ **十分です**(使う向きが順方向)

| 向き | 主張 | 成否 |
|---|---|---|
| **順**(本件で使う) | 三つ組が $S_{18}$-共役(marked)⟹ **被覆として同型** | ★ **無条件に正しい**(置換表現の同値 = 被覆の同型) |
| 逆 | 非共役 ⟹ 非同型 | ⚠ Hurwitz 移動(生成系の取り替え)の分だけ注意が要る |

本件が使うのは**順方向のみ**($W(P_1)$ 側)。$W(P_2)$ の棄却は $\lvert\mathrm{Mon}\rvert=419904\ne324$ という**群位数**によるもので、これは Hurwitz 移動でも共役でも不変 ⟹ ★ **より強い不変量で落ちています**。
⚠ **必要条件の確認**: 「marked」= 分岐点のラベル($0,1,\infty$)を対応させた共役であること。cert が marked と明記しているので ✔ ラベルを混ぜた共役だと不足でした。

$$\boxed{\ \textbf{⟹ 分岐 (a) の読解は成立。R-1 は無条件形で宣言できます}\ }$$

## §3 ★ 副産物 —【D2-GAP-6】の閉鎖

`p1d2_r1_canonicalization_v2.md` §4.2 で私が摘出した穴(代数走査は **72 本中 4 本**しか見ていない)は、**走査を広げることなく閉鎖されました**: $W(P_1)$ が $\lambda_9$ と直接同定されたので、$\lambda_9$ が split 枝に属することが**事後的に確定**したためです。
$$\boxed{\ \textbf{【D2-GAP-6】= 【CAN-2】: 閉鎖(YES — }\lambda_9\ \textbf{の Tschirnhaus 束は split)}\ }$$
★ **【D2-GAP-7】も部分閉鎖**: $W(P_1)$ は $\mathbf Q(\zeta_3)$ 上に定義されるので $\mathrm{Gal}(\bar{\mathbf Q}/\mathbf Q(\zeta_3))$-安定 ⟹ $\lambda_9$ の**moduli 体 $\subseteq\mathbf Q(\zeta_3)$**、残る 2 本は Galois 安定な 2 元集合。

---

# 第 II 部 — R-1 達成宣言(草案本文)

## §4 宣言文(草案・**Sol 原文承認前**)

> $K^{(9)}$ 窓に付随する次数 18 の Belyi 被覆 $\lambda_9$ の**明示代数モデル**を決定した。
>
> $$W_9:\quad x^2w^3-27\zeta_3\,y\,(w+1)=0\quad\text{over}\quad E:\ y^2+3\zeta_3xy+2y=x^3,\qquad \lambda_9:\ (x,y,w)\longmapsto t=-\frac{y^2}{4}$$
>
> ここで $Q_0=(0,0)$、$Q_\infty=O$、$P_1=(0,-2)=\ominus Q_0$ であり、被覆は $W_9\xrightarrow{3}E\xrightarrow{3}\mathbf P^1_s\xrightarrow{2}\mathbf P^1_t$($s=y/2i$、$t=s^2$)と分解する。
>
> 同定は 2 系統による: **(i) 厳密な組合せ census**(GAP)— $\lambda_9$ の passport は $\bigl((18),(2^81^2),(18)\bigr)$・$g=4$・$\lvert\mathrm{Mon}\rvert=324$ であり、$E$ を経由する同分岐データの次数 3 被覆は**全 72 本**、その二次分解体による 4 分割のうち $\lambda_9$ の属する類だけが組合せ的に区別される ⟹ Galois 安定 ⟹ 対応する点は $F$-有理 ⟹ $P=P_1$(**仮定なし**)。**(ii) 数値 monodromy**(path-tracking・残差 $\sim10^{-50}$・密度非依存)— $W(P_1)$ の三つ組は $\lambda_9$ の三つ組と $S_{18}$-共役(marked)、$W(P_2)$ は $\lvert\mathrm{Mon}\rvert=419904$ で非共役。**事前登録した 2 予言(PRED-1/PRED-2)はともに的中した。**
>
> モデルの係数はすべて $\mathbf Q(\zeta_3)$ に属し、被覆写像 $\lambda_9$ 全体が $\mathbf Q(\zeta_3)$ 上に定義される。ゆえに **$\lambda_9$ の定義体 $\subseteq\mathbf Q(\zeta_3)$**(したがって moduli 体 $\subseteq\mathbf Q(\zeta_3)$)。
>
> これは **candidate 格**の宣言である。組合せ側は厳密だが、split 束であること(= $W(P_1)$ であること)の確定は**数値 monodromy 1 系統**に依拠しており、**cross-checked ではない**。**Lean による verified でもない**。

## §5 範囲(★ 言うこと・言わないこと)

**言う**
- $\lambda_9$ の**明示モデル**と、その**定義体が $\mathbf Q(\zeta_3)$ に収まる**こと。
- $\lambda_9$ の passport・$\lvert\mathrm{Mon}\rvert=324$($\cong D_{18}\times D_{18}=$ T18n140)・ブロック系の一意性。
- 母集団が 72 本であること、および $P=P_1$ が**仮定なしに**決まること。

**言わない**(★ W-4 = 走査範囲の明示 / M-4 / M-5 反映)
- ⚠ **代数走査の範囲**: `p1_d2_scan_v2` が走査したのは **split Tschirnhaus 枝**($\mathcal E\cong\mathcal O(P)\oplus\mathcal O(2P)$)内の **4 点のみ**であり、母集団 72 本のうち**非 split の 68 本は代数的には走査していません**。⟹ 「4 点を尽くしたから」を根拠にしてはいけません。**根拠は $W(P_1)$ と $\lambda_9$ の直接同定**です(§3)。
- ⚠ **見張り V1–V7 は判別力ゼロ**(恒等式・空虚)。**「4/4 PASS ゆえ確定」とは書かない**(監査 M-4)。
- ⚠ **「定義体」と「moduli 体」を混同しない**(監査 B-2)。示したのは「モデルが $\mathbf Q(\zeta_3)$ 上に書ける」= 定義体。moduli 体 $\subseteq$ 定義体。$\mathbf Q$ まで降りるかは**未決**。
- ⚠ **prereg 量($d_9$・$r$)は本宣言で一切計算していません**。
- ⚠ **$\widehat{GT}$・GT-shadow 側の主張は含みません**($\lambda_9$ は $K^{(9)}$ 窓の幾何的対象としてのみ扱った)。

## §6 根拠 cert 一覧

| # | cert / 資産 | 内容 | 系統 |
|---|---|---|---|
| 1 | `search/certs/d2_gate_v1_20260813.json` + `d2_gate_v1_track_20260813.json`(run 31630925950) | ★ **本決定打**: $\lvert\mathrm{Mon}(W(P_1))\rvert=324$・$S_{18}$-共役 true / $W(P_2)$ 419904・false。残差 $\sim10^{-50}$・2 密度でビット同一 | 数値 |
| 2 | `search/certs/w9_k3_p1_0d_check_v1_20260812.json` | $\lambda_9$ の $\lvert\mathrm{Mon}\rvert=324$・$D=18$・quot 36・deck 1(**標的**) | 組合せ |
| 3 | `search/certs/r13_p1_0_blocks_v1_20260812.json` | ブロック長 $\{9,3\}$・非原始的・非自明ブロック系 2 本 | 組合せ |
| 4 | `search/certs/r13_r0_v1_1_20260812.json` | $\lambda_9$ の passport | 組合せ |
| 5 | `search/certs/p1_d2_scan_v2_20260813.json` | 4 点・$c=\zeta_6/2$・$\rho$ の実測 | 記号+数値 |
| 6 | `scratchpad/lambda9_passport.g`, `d2gap4_census.g`, `d2gap4_census2.g`, `d2gap4_census3.g`, `deg3_census_over_E.py` | ★ **母集団 72 本・$\lvert\mathrm{Mon}\rvert$ 分布・resolvent 4 分割**(2 系統独立) | 組合せ(厳密) |
| 7 | `scratchpad/q1081_checks.py`, `q1081_exact.py` | $A_0=-2y/x^2$・$c$・$\rho$ の厳密値 | 記号 |
| 8 | falsifier `scratchpad/fals_p1d2_check.py` 他 | ★ 14 項目の**独立再検算 PASS**(数学者の script を import せず再構成) | 独立 |

⚠ **発令前の必須整備**: **#6 は scratchpad の script であり cert 化されていません**。母集団 72 本と resolvent 分割は宣言の骨格なので、**cert(schema `d2_census/v1`)へ昇格させること**。⟹ §9【R1-GAP-1】。

## §7 格(★ 明記)

$$\boxed{\ \textbf{candidate}\ —\ \textbf{cross-checked ではない・verified ではない}\ }$$

| 部分 | 格 | 理由 |
|---|---|---|
| passport・$\lvert\mathrm{Mon}(\lambda_9)\rvert=324$・ブロック一意 | **cross-checked に近い** | cert 2 本(#2#3)+ 私の再抽出 + falsifier の GAP 掃引 = 3 系統一致 |
| 母集団 72 本・resolvent 4 分割 | **candidate(厳密)** | 2 系統(python 曲面群 / GAP 誘導表現)一致。cert 化待ち |
| $P=P_1$(**【CAN-1′】**) | **candidate(厳密・数値非依存)** | 組合せ census + 紙の Galois 論法 |
| **$W_9=W(P_1)$(split 束)** | ★ **candidate** | ⚠ **数値 monodromy 1 系統**。予言 2 本の的中は強い傍証だが第 2 系統ではない |
| 定義体 $\subseteq\mathbf Q(\zeta_3)$ | **candidate** | 上に条件づく。$t=-y^2/4$ の導出は記号(ゲージ不変量 2 本一致) |

**cross-checked への昇格条件(1 本で足りる)**:
$$\boxed{\ \text{次数 18 関数体拡大 }\mathbf Q(\zeta_3)(t)[X]/(\deg18)\ \text{の Galois 群を}\textbf{厳密に}\textbf{計算し }\lvert G\rvert=324\ \text{と三つ組を突合}\ }$$
または独立実装による第 2 の path-tracking。⟹ §9【R1-GAP-2】。

## §8 ★ 解錠されるもの

| 行き先 | 解錠される理由 | ⚠ 注意 |
|---|---|---|
| **R-2 / R-3** | $\lambda_9$ の**厳密モデル**が確定 ⟹ 還元・分岐の計算が可能になった | — |
| **$d_9$ receipt** | モデルが $\mathbf Q(\zeta_3)$ 上 ⟹ receipt の調達先が確定 | ⚠ **prereg 量。本書では計算していません** |
| **$r$ 測定** | 同上 | ⚠ **prereg 量。本書では計算していません** |
| **UNRAM U3-1..3** | 定義体 $\subseteq\mathbf Q(\zeta_3)$ ⟹ 不分岐集合 $S$ の候補が絞れる | ⚠ 「定義体 $\subseteq\mathbf Q(\zeta_3)$」は**モデルの係数体**の主張。悪い還元の集合は別途計算が要る |
| **【D2-GAP-6】【CAN-2】** | ★ **閉鎖**(§3) | — |
| **【D2-GAP-7】** | ★ **部分閉鎖**($\lambda_9$ の moduli 体 $\subseteq\mathbf Q(\zeta_3)$) | 残る 2 本の軌道構造は未決 |

## §9 未閉鎖項・発令前の条件

- **【R1-GAP-1】(必須)** 母集団 census(72 本・$\lvert\mathrm{Mon}\rvert$ 分布・resolvent 4 分割)の **cert 化**。現状は scratchpad script。
- **【R1-GAP-2】(格の昇格用・任意)** 第 2 系統による次数 18 monodromy の確認 ⟹ cross-checked へ。
- **【D2-GAP-5】** 閉鎖済(18-cycle 論法)。**【D2-GAP-1/2/3】** 既設・GAP-2 閉鎖済。
- **手続きの鎖(G1 に倣う・現状)**:
 1. 数学的検収: ⚠ **Sol 監査 未了**(便 122 で発送予定)
 2. 前哨監査: ★ **実施済**(falsifier `fals_p1d2_r1_audit_v1.md`)— 指摘 B-1/B-2/M-1〜M-5/m-1〜m-9 は v2 で全件反映済
 3. 研究者検分: ⚠ **未了**
 4. 凍結 tag: ⚠ **未設定**
$$\boxed{\ \textbf{⟹ 現時点では「草案」。1・3・4 が揃うまで発令しないこと}\ }$$

## §10 記帳

- ★ **本書の新規部分**: ① §8.3 分岐 (a) の正式読解 ② $\sigma_\infty$ 導出と marked 共役の十分性の論証(順方向のみ使用・$W(P_2)$ は群位数という強い不変量で落ちている)③ **【D2-GAP-6】の「走査せずに閉鎖」**(直接同定による事後確定)④ **【D2-GAP-7】の部分閉鎖**(moduli 体 $\subseteq\mathbf Q(\zeta_3)$)⑤ 宣言文の草案と格の層別 ⑥ W-4 に基づく走査範囲の明示(4/72 と、それが根拠でないこと)。
- **申告**: 紙のみ(本書の機械走行ゼロ)・$u$/$c$ 非接触・**prereg 量非計算**・**Sol 未監査**・**verified ではない**(candidate 格)。
