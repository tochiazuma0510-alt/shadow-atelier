# R-1 達成宣言(**最終確定版** — Sol 監査待ち・研究者検分待ち)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1095(R1-GAP-1 充足 → 最終確定 GO)
**v1 を置換**(`r1_declaration_draft_v1.md`・上書きせず版で残す)。差分 = §6 の cert 差し込み・§7 の格の確定・§9 の R1-GAP-1 閉鎖。
⚠ **本書は発令ではありません**(手続きの鎖 §9 が未完)。$u$/$c$ 非接触・**prereg 量($d_9$・$r$)非計算**・封印非接触。

---

## §0 v1 からの差分(3 点のみ)

| # | v1 | v2 |
|---|---|---|
| 1 | 母集団 census は scratchpad script(cert 未化)【R1-GAP-1】 | ★ **cert 化完了**。司令塔照合で私の fail-closed 突合表と**全行一致**・第 2 レール(sympy)も完全一致 ⟹ **【R1-GAP-1】閉鎖** |
| 2 | 格: 「candidate(厳密)・cert 化待ち」 | ★ **candidate(厳密・2 系統一致・cert 化済・盲第三系統走行中)** |
| 3 | — | 盲 checker F の状況を §9 に明記(resolvent 分割のみ blocked → 定義抜粋を配達済) |

★ **宣言本文(§4)は v1 から一字も変えていません。** cert 着弾は本文の主張を変えず、**根拠の格だけを上げました**。

---

# 第 I 部 — §8.3 の正式読解(v1 §1–§3 を継承)

## §1 分岐判定

| 量 | 実測 | 予言 | 判定 |
|---|---|---|---|
| $\lvert\mathrm{Mon}(W(P_1))\rvert$ | **324** | **PRED-1**: $\in\{324,972,2916\}$ | ★ **的中** |
| $\lvert\mathrm{Mon}(W(P_2))\rvert$ | **419904** | **PRED-2**: $=419904$ | ★ **的中** |
| $W(P_1)$ の三つ組 vs $\lambda_9$($S_{18}$-共役・marked) | **true** | 分岐 (a) の条件 | ★ **該当** |
| $W(P_2)$ の三つ組 vs $\lambda_9$ | **false** | 対照 | ✔ |
| passport / blocks / transitive | 一致 | [G-5] 見張り | ✔ |

$$\boxed{\ \textbf{分岐 (a) 該当}\ \Longrightarrow\ W_9=W(P_1).\ \textbf{【CAN-1】【CAN-2】とも不要}\ }$$

★ **予言 2 本は数値を見る前に凍結**されました。導出は exact な組合せ census(72 本の $\lvert\mathrm{Mon}\rvert$ 分布と resolvent 類の Galois 安定性)であり、**exact 側が数値側を予言し的中させた**関係です。

## §2 技術的 2 点(v1 §2 を継承・要約)

- **$\sigma_\infty$ の導出扱いは問題なし**。$\pi_1(\mathbf P^1\setminus\{0,1,\infty\})$ は $g_0,g_1$ で自由 ⟹ 被覆は $(\sigma_0,\sigma_1)$ で完全に決まる(Riemann 存在定理)。$\sigma_\infty$ は独立に測るべき量ではなく、「18-cycle であること」は追跡の健全性検査として有効。
- **marked $S_{18}$-共役は十分**。使うのは「共役 ⟹ 同型」の**順方向のみ**(無条件に正しい)。$W(P_2)$ の棄却は群位数 $419904\ne324$ による ⟹ 共役でも Hurwitz 移動でも不変な、より強い不変量。

## §3 副産物

- **【D2-GAP-6】=【CAN-2】: 閉鎖(YES)** — 走査を広げず、直接同定によって $\lambda_9$ が split 枝に属することが事後確定。
- **【D2-GAP-7】: 部分閉鎖** — $W(P_1)$ が $\mathbf Q(\zeta_3)$ 上に定義される ⟹ $\lambda_9$ の **moduli 体 $\subseteq\mathbf Q(\zeta_3)$**。
- **【D2-GAP-5】: 閉鎖**(18-cycle 論法)。

---

# 第 II 部 — R-1 達成宣言(最終確定・**Sol 原文承認前**)

## §4 宣言文

> $K^{(9)}$ 窓に付随する次数 18 の Belyi 被覆 $\lambda_9$ の**明示代数モデル**を決定した。
>
> $$W_9:\quad x^2w^3-27\zeta_3\,y\,(w+1)=0\quad\text{over}\quad E:\ y^2+3\zeta_3xy+2y=x^3,\qquad \lambda_9:\ (x,y,w)\longmapsto t=-\frac{y^2}{4}$$
>
> ここで $Q_0=(0,0)$、$Q_\infty=O$、$P_1=(0,-2)=\ominus Q_0$ であり、被覆は $W_9\xrightarrow{3}E\xrightarrow{3}\mathbf P^1_s\xrightarrow{2}\mathbf P^1_t$($s=y/2i$、$t=s^2$)と分解する。
>
> 同定は 2 系統による: **(i) 厳密な組合せ census** — $\lambda_9$ の passport は $\bigl((18),(2^81^2),(18)\bigr)$・$g=4$・$\lvert\mathrm{Mon}\rvert=324$ であり、$E$ を経由する同分岐データの次数 3 被覆は**全 72 本**、その二次分解体による 4 分割のうち $\lambda_9$ の属する類だけが組合せ的に区別される ⟹ Galois 安定 ⟹ 対応する点は $F$-有理 ⟹ $P=P_1$(**仮定なし**)。**(ii) 数値 monodromy**(path-tracking・残差 $\sim10^{-50}$・密度非依存)— $W(P_1)$ の三つ組は $\lambda_9$ の三つ組と $S_{18}$-共役(marked)、$W(P_2)$ は $\lvert\mathrm{Mon}\rvert=419904$ で非共役。**事前登録した 2 予言(PRED-1/PRED-2)はともに的中した。**
>
> モデルの係数はすべて $\mathbf Q(\zeta_3)$ に属し、被覆写像 $\lambda_9$ 全体が $\mathbf Q(\zeta_3)$ 上に定義される。ゆえに **$\lambda_9$ の定義体 $\subseteq\mathbf Q(\zeta_3)$**(したがって moduli 体 $\subseteq\mathbf Q(\zeta_3)$)。
>
> これは **candidate 格**の宣言である。組合せ側は厳密かつ 2 系統一致で証明書化されているが、split 束であること(= $W(P_1)$ であること)の確定は**数値 monodromy 1 系統**に依拠しており、**cross-checked ではない**。**Lean による verified でもない**。

## §5 範囲(★ 言うこと・言わないこと)

**言う**: $\lambda_9$ の明示モデルと定義体 $\subseteq\mathbf Q(\zeta_3)$ / passport・$\lvert\mathrm{Mon}\rvert=324$($\cong D_{18}\times D_{18}=$ T18n140)・ブロック系の一意性 / 母集団 72 本と $P=P_1$ の**無仮定性**。

**言わない**(W-4 / M-4 / M-5 反映)
- ⚠ **走査範囲**: `p1_d2_scan_v2` が走査したのは **split Tschirnhaus 枝の 4 点のみ**で、母集団 72 本のうち**非 split の 68 本は代数的に走査していません**。⟹ 「4 点を尽くしたから」を根拠にしない。**根拠は $W(P_1)$ と $\lambda_9$ の直接同定**(§3)。
- ⚠ 見張り V1–V7 は**判別力ゼロ**。**「4/4 PASS ゆえ確定」とは書かない**。
- ⚠ **「定義体」と「moduli 体」を混同しない**。示したのは定義体($\mathbf Q$ まで降りるかは未決)。
- ⚠ **prereg 量($d_9$・$r$)は本宣言で一切計算していません**。
- ⚠ $\widehat{GT}$・GT-shadow 側の主張は含みません。

## §6 根拠 cert 一覧(★ v2 で確定)

| # | cert | 内容 | 系統 |
|---|---|---|---|
| 1 | `search/certs/d2_gate_v1_20260813.json` + `d2_gate_v1_track_20260813.json`(run 31630925950) | ★ **決定打**: $\lvert\mathrm{Mon}(W(P_1))\rvert=324$・marked $S_{18}$-共役 true / $W(P_2)$ 419904・false。残差 $\sim10^{-50}$・2 密度でビット同一 | 数値 |
| 2 | ★ `search/certs/r1_gap1_population72_v1_20260813.json`<br>`sha256 = 7e24d633e12995f06fafa44af72c2c4f1dbcd4e1e44d01e590e749687eefda36` | ★ **母集団 census の producer cert**: 648→432→**72**・resolvent **[18,18,18,18]**・$\lvert\mathrm{Mon}\rvert$ 分布 **324:3 / 972:9 / 2916:6 / 419904:54**・$\lambda_9$ = **1 本**・**324 類**に帰属・blocks [3,9]・正対照 2 点 | 組合せ(厳密) |
| 3 | ★ 第 2 レール cert `007f2732…`(sympy) | 上と**完全一致**(独立実装) | 組合せ(厳密) |
| 4 | `search/certs/w9_k3_p1_0d_check_v1_20260812.json` | $\lambda_9$ の $\lvert\mathrm{Mon}\rvert=324$・$D=18$・quot 36・deck 1(**標的**) | 組合せ |
| 5 | `search/certs/r13_p1_0_blocks_v1_20260812.json` | ブロック長 $\{9,3\}$・非原始的 | 組合せ |
| 6 | `search/certs/r13_r0_v1_1_20260812.json` | $\lambda_9$ の passport | 組合せ |
| 7 | `search/certs/p1_d2_scan_v2_20260813.json` | 4 点・$c=\zeta_6/2$・$\rho$ | 記号+数値 |
| 8 | `scratchpad/q1081_checks.py`, `q1081_exact.py` | $A_0=-2y/x^2$・$c$・$\rho$ の厳密値 | 記号 |
| 9 | falsifier `scratchpad/fals_p1d2_check.py` 他 | 14 項目の**独立再検算 PASS**(私の script を import せず再構成) | 独立 |

★ **#2 は私の fail-closed 突合表(全 10 行)と全行一致**が司令塔照合で確認済み。⟹ 転記ではなく**再現**として成立。

## §7 格(★ 確定)

$$\boxed{\ \textbf{candidate}\ —\ \textbf{cross-checked ではない・verified ではない}\ }$$

| 部分 | 格 |
|---|---|
| passport・$\lvert\mathrm{Mon}(\lambda_9)\rvert=324$・ブロック一意 | **cross-checked に近い**(cert #4#5#6 + 私の再抽出 + falsifier の GAP 掃引 = 3 系統一致) |
| **母集団 72 本・resolvent 4 分割** | ★ **candidate(厳密・2 系統一致・cert 化済・盲第三系統走行中)** |
| $P=P_1$(**【CAN-1′】**) | **candidate(厳密・数値非依存)**(組合せ census + 紙の Galois 論法) |
| **$W_9=W(P_1)$(split 束)** | ★ **candidate** — ⚠ **数値 monodromy 1 系統**。予言 2 本の的中は強い傍証だが第 2 系統ではない |
| 定義体 $\subseteq\mathbf Q(\zeta_3)$ | **candidate**(上に条件づく) |

> ★ **文言更新枠(1 行・盲第三系統 F の着弾時に司令塔が差し替え)**:
> 「母集団 72 本・resolvent 4 分割」の格 → **F が独立実装で一致すれば「cross-checked(3 系統一致)」へ昇格**。不一致なら**本宣言を保留し §6 #2#3 を再検分**。

**$W_9=W(P_1)$ を cross-checked へ昇格させる条件(1 本で足りる)**:
$$\boxed{\ \text{次数 18 関数体拡大 }\mathbf Q(\zeta_3)(t)[X]/(\deg18)\ \text{の Galois 群を}\textbf{厳密に}\textbf{計算し }\lvert G\rvert=324\ \text{と三つ組を突合}\ }$$
または独立実装による第 2 の path-tracking。⟹ §9【R1-GAP-2】。

## §8 ★ 解錠されるもの

| 行き先 | 理由 | ⚠ 注意 |
|---|---|---|
| **R-2 / R-3** | $\lambda_9$ の厳密モデル確定 ⟹ 還元・分岐の計算が可能に | — |
| **$d_9$ receipt** | モデルが $\mathbf Q(\zeta_3)$ 上 ⟹ 調達先が確定 | ⚠ **prereg 量。本書では計算していません** |
| **$r$ 測定** | 同上 | ⚠ **prereg 量。本書では計算していません** |
| **UNRAM U3-1..3** | 定義体 $\subseteq\mathbf Q(\zeta_3)$ ⟹ 不分岐集合 $S$ の候補が絞れる | ⚠ 悪い還元の集合は別途計算が要る |
| **【D2-GAP-6】【CAN-2】** | ★ 閉鎖 | — |
| **【D2-GAP-7】** | ★ 部分閉鎖($\lambda_9$ の moduli 体 $\subseteq\mathbf Q(\zeta_3)$) | 残る 2 本の軌道構造は未決 |

## §9 未閉鎖項・発令前の条件

- **【R1-GAP-1】★ 閉鎖**(cert #2#3・司令塔照合で全行一致)。
- **【R1-GAP-2】(格の昇格用・任意)** 第 2 系統による次数 18 monodromy の確認 ⟹ $W_9=W(P_1)$ が cross-checked へ。
- **盲第三系統 F の状況**: 母集団数・$\lvert\mathrm{Mon}\rvert$ 分布・$\lambda_9$ 帰属は**自前実装で継続中**。resolvent 分割のみ blocked だったため、**定義のみの抜粋**を配達済(`r1_gap1_resolvent_def_extract_v1.md`・裁定 1096)。⟹ 着弾後に §7 の文言更新枠を適用。
- **手続きの鎖(G1 に倣う・現状)**:
 1. 数学的検収: ⚠ **Sol 監査 未了**(本書が便 122 の筆頭積荷)
 2. 前哨監査: ★ **実施済**(falsifier `fals_p1d2_r1_audit_v1.md`)— B-1/B-2/M-1〜M-5/m-1〜m-9 は v2 系で全件反映済
 3. 盲第三系統: ⚠ **走行中**(F)
 4. 研究者検分: ⚠ **未了**
 5. 凍結 tag: ⚠ **未設定**
$$\boxed{\ \textbf{⟹ 1・4・5 が揃うまで発令しないこと}\ }$$

## §10 記帳

- ★ **v2 の新規部分**: cert #2#3 の差し込み・格の確定(2 系統一致・cert 化済)・文言更新枠の設置・F の状況の明記・【R1-GAP-1】閉鎖。
- ⚠ **宣言本文(§4)は v1 から不変**。cert 着弾は主張を変えず根拠の格だけを上げました。
- **申告**: 紙のみ(本書の機械走行ゼロ)・$u$/$c$ 非接触・**prereg 量非計算**・**Sol 未監査**・**verified ではない**(candidate 格)。
