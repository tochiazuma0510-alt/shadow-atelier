# R-1 達成宣言(**発令版** — 残は研究者検分と凍結 tag のみ)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1109(Sol 便 122 検収 → v4 起草)
**v3 を置換**(`r1_declaration_draft_v3.md`・上書きせず版で残す)。差分は §0 の 4 点のみ。
根拠 = `sol/sol_reply_122_r1_line3.md` §1(B1)・§2(B2)
⚠ **本書はまだ発令ではありません**(§9 の 4・5 が未了)。$u$/$c$ 非接触・**prereg 量($d_9$・$r$)非計算**・封印非接触。

---

## §0 v3 からの差分(Sol 便 122 §1.2 の必須訂正 3 点 + 司令塔指示 1 点)

| # | v3 | v4 |
|---|---|---|
| 1 | §6 #3「第 2 レール cert(sympy)・**独立実装**」 | ★ **「同一実装者による異言語第二レール。独立性は主張しない」**(cert 自身の `same implementer ... NOT a blind independent checker` 申告と整合) |
| 2 | §7「母集団 72・resolvent 4 分割 = candidate(2 系統一致・cert 化済)」/【R1-GAP-3】未閉 | ★ **cross-checked(3 code path)**・**【R1-GAP-3】= CLOSED**。⚠ **CAN-1′ と $W_9=W(P_1)$ へ格は自動伝播させない** |
| 3 | §7「昇格条件 = 関数体 Galois 群を厳密計算し $\lvert G\rvert=324$ と三つ組を突合」 | ★ **Sol の固定文言へ差し替え**(§7.2)。位数・passport・抽象同型だけでは**不合格**。**【R1-GAP-2】は昇格条件であって発令の前件ではない** |
| 4 | (B4 = ③ 線の訂正) | ★ **本宣言に該当箇所なし**(R-1 は $\lambda_9$/$W_9$ の言明で、$\lvert GT(N')\rvert$・$U_{\rm split}$ には触れていません)⟹ 訂正は `ss_gap1_count_spec_v1_addendum_b4.md` に分離 |

★ **宣言文(§4)は v3 から不変**です。訂正はすべて**根拠の記述と格の欄**に対するもので、主張は動いていません。

---

# 第 I 部 — §8.3 の正式読解(v1–v3 を継承)

## §1 分岐判定

| 量 | 実測 | 予言 | 判定 |
|---|---|---|---|
| $\lvert\mathrm{Mon}(W(P_1))\rvert$ | **324** | **PRED-1**: $\in\{324,972,2916\}$ | ★ **的中** |
| $\lvert\mathrm{Mon}(W(P_2))\rvert$ | **419904** | **PRED-2**: $=419904$ | ★ **的中** |
| $W(P_1)$ の三つ組 vs $\lambda_9$($S_{18}$-共役・marked) | **true** | 分岐 (a) の条件 | ★ **該当** |
| $W(P_2)$ の三つ組 vs $\lambda_9$ | **false** | 対照 | ✔ |
| passport / blocks / transitive | 一致 | [G-5] 見張り | ✔ |

$$\boxed{\ \textbf{分岐 (a) 該当}\ \Longrightarrow\ W_9=W(P_1).\ \textbf{【CAN-1】【CAN-2】とも不要}\ }$$

★ 予言 2 本は**数値を見る前に**凍結され、導出は exact な組合せ census でした。

## §2 技術的 2 点(要約)

- **$\sigma_\infty$ の導出扱いは問題なし**。$\pi_1(\mathbf P^1\setminus\{0,1,\infty\})$ は $g_0,g_1$ で自由 ⟹ 被覆は $(\sigma_0,\sigma_1)$ で完全に決まる。
- **marked $S_{18}$-共役は十分**。使うのは「共役 ⟹ 同型」の**順方向のみ**。$W(P_2)$ の棄却は群位数による(共役でも Hurwitz 移動でも不変)。

## §3 副産物

**【D2-GAP-6】=【CAN-2】: 閉鎖(YES)** / **【D2-GAP-7】: 部分閉鎖**($\lambda_9$ の moduli 体 $\subseteq\mathbf Q(\zeta_3)$)/ **【D2-GAP-5】: 閉鎖**。

---

# 第 II 部 — R-1 達成宣言(**Sol 監査 = 条件つき PASS 済**)

## §4 宣言文(v3 から不変)

> $K^{(9)}$ 窓に付随する次数 18 の Belyi 被覆 $\lambda_9$ の**明示代数モデル**を決定した。
>
> $$W_9:\quad x^2w^3-27\zeta_3\,y\,(w+1)=0\quad\text{over}\quad E:\ y^2+3\zeta_3xy+2y=x^3,\qquad \lambda_9:\ (x,y,w)\longmapsto t=-\frac{y^2}{4}$$
>
> ここで $Q_0=(0,0)$、$Q_\infty=O$、$P_1=(0,-2)=\ominus Q_0$ であり、被覆は $W_9\xrightarrow{3}E\xrightarrow{3}\mathbf P^1_s\xrightarrow{2}\mathbf P^1_t$($s=y/2i$、$t=s^2$)と分解する。
>
> 同定は 2 系統による: **(i) 厳密な組合せ census** — $\lambda_9$ の passport は $\bigl((18),(2^81^2),(18)\bigr)$・$g=4$・$\lvert\mathrm{Mon}\rvert=324$ である。**この passport をもち、かつ(一意に定まる)サイズ 3 のブロック系による次数 6 商が $E\to\mathbf P^1_t$(次数 6 の Nielsen 類 #1)に同型な被覆の全体**(以下 $\mathfrak M$・厳密な定義は §5.1)**は 72 本**であり、その二次分解体による 4 分割のうち $\lambda_9$ の属する類だけが組合せ的に区別される ⟹ Galois 安定 ⟹ 対応する点は $F$-有理 ⟹ $P=P_1$(**仮定なし**)。**(ii) 数値 monodromy**(path-tracking・残差 $\sim10^{-50}$・密度非依存)— $W(P_1)$ の三つ組は $\lambda_9$ の三つ組と $S_{18}$-共役(marked)、$W(P_2)$ は $\lvert\mathrm{Mon}\rvert=419904$ で非共役。**事前登録した 2 予言(PRED-1/PRED-2)はともに的中した。**
>
> モデルの係数はすべて $\mathbf Q(\zeta_3)$ に属し、被覆写像 $\lambda_9$ 全体が $\mathbf Q(\zeta_3)$ 上に定義される。ゆえに **$\lambda_9$ の定義体 $\subseteq\mathbf Q(\zeta_3)$**(したがって moduli 体 $\subseteq\mathbf Q(\zeta_3)$)。
>
> これは **candidate 格**の宣言である。組合せ側の母集団と resolvent 分割は 3 つの code path で一致し cross-checked であるが、split 束であること(= $W(P_1)$ であること)の確定は**数値 monodromy 1 系統**に依拠しており、**その部分は cross-checked ではない**。**Lean による verified でもない。**

## §5 範囲(★ 言うこと・言わないこと)

**言う**: $\lambda_9$ の明示モデルと定義体 $\subseteq\mathbf Q(\zeta_3)$ / passport・$\lvert\mathrm{Mon}\rvert=324$($\cong D_{18}\times D_{18}=$ T18n140)・ブロック系の一意性 / **母集団 $\mathfrak M$ が 72 本**であることと $P=P_1$ の**無仮定性**。

**言わない**(W-4 / M-4 / M-5 反映)
- ⚠ **走査範囲**: `p1_d2_scan_v2` が走査したのは **split Tschirnhaus 枝の 4 点のみ**で、$\mathfrak M$ の 72 本のうち**非 split の 68 本は代数的に走査していません**。**根拠は $W(P_1)$ と $\lambda_9$ の直接同定**(§3)。
- ⚠ 見張り V1–V7 は**判別力ゼロ**。**「4/4 PASS ゆえ確定」とは書かない**。
- ⚠ **「定義体」と「moduli 体」を混同しない**。示したのは定義体($\mathbf Q$ まで降りるかは未決)。
- ⚠ **prereg 量($d_9$・$r$)は本宣言で一切計算していません**。
- ⚠ $\widehat{GT}$・GT-shadow 側の主張は含みません。
- ⚠ ★ **§4 (i) の「Galois 安定 ⟹ $F$-有理 ⟹ $P=P_1$」という紙の対応を、verified と呼んではいけません**(Sol §1.1)。

### 5.1 母集団 $\mathfrak M$ の定義(Sol の独立再計算の仕様)

$\mathbf F:=\pi_1(\mathbf P^1\setminus\{0,1,\infty\})=\langle g_0,g_1\rangle$(自由)。被覆 = 推移的有限 $\mathbf F$-集合。

> **【定義 POP】** $\mathfrak M$ := 次数 18 の連結被覆 $X$ の同型類のうち:
> **(C1)** passport が $\bigl((18),(2^81^2),(18)\bigr)$ — $g_0,g_\infty$ が 18-巡回、$g_1$ が型 $2^81^2$ の対合。
> **(C2)** $g_0$ が 18-巡回ゆえ**一意に定まる**サイズ 3 のブロック系による次数 6 商が、**次数 6 の Nielsen 類 #1**(monodromy 位数 **36**・サイズ 3 のブロック系・deck 群自明)に同型。
> $$\boxed{\ \lvert\mathfrak M\rvert=72\ }$$

⚠ **(C2) が本質的**: (C1) 単独では $\approx1.9\times10^6$ 類(大半が $\lvert\mathrm{Mon}\rvert=18!$)。
★ **Sol は別正規化($324\to216\to72$;producer は $648\to432\to72$)でこれを再現**しました(§6 #4)。

> **【補題 POP】** (C1)+(C2) を満たす $X$ について、次数 3 の部分被覆の分岐は**自動的に**決まる: $t=0,\infty$ 上の各 1 点で全分岐 / $t=1$ 上の $e=2$ の 2 点で不分岐 / $e=1$ の 2 点で単純分岐。

*証明*: $g_0$ 18-巡回 ⟹ $t=0,\infty$ 上は各 1 点 $e=18$ ⟹ 全分岐。$e=2$ の点で $(2,1)$ だと $e=4$ の点が生じ $g_1$ が対合であることに矛盾 ⟹ 不分岐。$g_1$ の固定点はちょうど 2 個で $e=2$ の点の上には来ない ⟹ $e=1$ の 2 点が 1 個ずつ供給 ⟹ 各々 $(2,1)$ ∎

## §6 根拠 cert 一覧(★ v4 で #3 を訂正)

| # | cert | 内容 | 系統 |
|---|---|---|---|
| 1 | `search/certs/d2_gate_v1_20260813.json` + `d2_gate_v1_track_20260813.json`(run 31630925950) | ★ **決定打**: $\lvert\mathrm{Mon}(W(P_1))\rvert=324$・marked $S_{18}$-共役 true / $W(P_2)$ 419904・false。残差 $\sim10^{-50}$・2 密度でビット同一 | 数値 |
| 2 | `search/certs/r1_gap1_population72_v1_20260813.json`<br>`sha256 = 7e24d633e12995f06fafa44af72c2c4f1dbcd4e1e44d01e590e749687eefda36` | **母集団 census の producer cert**: 648→432→**72**・resolvent **[18,18,18,18]**・$\lvert\mathrm{Mon}\rvert$ 分布 **324:3 / 972:9 / 2916:6 / 419904:54**・$\lambda_9$ = **1 本**・**324 類**に帰属 | 組合せ(厳密)・**code path 1** |
| **3** | 第 2 レール cert `007f2732…`(sympy) | 上と完全一致。⚠ ★ **同一実装者による異言語第二レール。独立性は主張しない**(cert 自身が `same implementer ... NOT a blind independent checker` と申告) | 組合せ(厳密)・**code path 2** |
| **4** | ★ **Sol 便 122 §2**(`sol_reply_122_r1_line3.md` の再現 script) | ★ **独立実装・独立正規化**($324\to216\to72$)。cover 類 **72**・gauge 軌道 $\{3:72\}$・resolvent **[18,18,18,18]**・monodromy 分布 **{324:3, 972:9, 2916:6, 419904:54}**・joint 分布(3 行 $\{419904:18\}$ / 1 行 $\{324:3,972:9,2916:6\}$)。**producer と実装者・正規化・helper を共有しない** | 組合せ(厳密)・**code path 3** |
| 5 | `search/certs/w9_k3_p1_0d_check_v1_20260812.json` | $\lambda_9$ の $\lvert\mathrm{Mon}\rvert=324$・$D=18$・quot 36・deck 1(**標的**) | 組合せ |
| 6 | `search/certs/r13_p1_0_blocks_v1_20260812.json` | ブロック長 $\{9,3\}$・非原始的 | 組合せ |
| 7 | `search/certs/r13_r0_v1_1_20260812.json` | $\lambda_9$ の passport | 組合せ |
| 8 | `search/certs/p1_d2_scan_v2_20260813.json` | 4 点・$c=\zeta_6/2$・$\rho$ | 記号+数値 |
| 9 | `scratchpad/q1081_checks.py`, `q1081_exact.py` | $A_0=-2y/x^2$・$c$・$\rho$ の厳密値 | 記号 |
| 10 | falsifier `scratchpad/fals_p1d2_check.py` 他 | 14 項目の**独立再検算 PASS** | 独立 |

## §7 格(★ v4 で確定)

$$\boxed{\ \textbf{宣言全体 = candidate}\ —\ \textbf{Lean verified ではない}\ }$$

| 部分 | 格 |
|---|---|
| passport・$\lvert\mathrm{Mon}(\lambda_9)\rvert=324$・ブロック一意 | **cross-checked に近い**(cert #5#6#7 + 私の再抽出 + falsifier の GAP 掃引) |
| ★ **母集団 $\mathfrak M$ = 72 本・resolvent 4 分割** | ★★ **cross-checked(3 code path)** — producer / 異言語第二レール / **Sol の独立実装・独立正規化**。⟹ **【R1-GAP-3】= CLOSED** |
| $P=P_1$(**【CAN-1′】**) | ⚠ **candidate**(厳密・数値非依存)。★ **上の cross-checked は有限計算の前提に対するものであり、Galois 同変な紙の対応にはここから格が伝播しません**(Sol §1.2-2) |
| **$W_9=W(P_1)$(split 束)** | ⚠ **candidate** — **数値 monodromy 1 系統**。★ **母集団の cross-checked は伝播しません**。母集団内に $\lvert\mathrm{Mon}\rvert=324$ の被覆が **3 本**あるため、位数だけでは同定できません |
| 定義体 $\subseteq\mathbf Q(\zeta_3)$ | **candidate**(上に条件づく) |

### 7.1 ⚠ 格の非伝播(Sol 指定・明文化)

$$\boxed{\ \textbf{cross-checked なのは「母集団 72 と resolvent 4 分割」という}\textbf{有限計算}\textbf{のみ}\ }$$
- **【CAN-1′】**($\lambda_9$ の resolvent $=P_1$ の類)は、その有限計算の上に **Galois 同変性という紙の推論**を載せたものです ⟹ **candidate 据え置き**。
- **$W_9=W(P_1)$** はさらに数値 1 系統に依存します ⟹ **candidate 据え置き**。

### 7.2 ★【R1-GAP-2】exact 成功条件(Sol 便 122 §1.2-3 の固定文言)

> $W_9=W(P_1)$ を **cross-checked** へ上げるための exact レールの成功条件:
> 1. 対象は算術 Galois 群の位数だけでなく、**定数体を分離した幾何 monodromy**。
> 2. $t=0,1,\infty$ の **marked inertia 生成元を exact に取り出し**、$\lambda_9$ の三つ組と **同時 $S_{18}$-共役**を示す。
> 3. **既約性・分離性・次数 18・余分な消去因子がないこと**を証明書に含める。
> 4. ★ **群位数 324、passport、抽象群同型だけでは不合格**(母集団に 324 の被覆が 3 本あるため)。

$$\boxed{\ \textbf{【R1-GAP-2】は}\textbf{昇格条件}\textbf{であって、candidate 宣言の}\textbf{論理的前件ではない}\ }\quad(\text{Sol }\S1.2)$$

## §8 ★ 解錠されるもの

| 行き先 | 理由 | ⚠ 注意 |
|---|---|---|
| **R-2 / R-3** | $\lambda_9$ の厳密モデル確定 ⟹ 還元・分岐の計算が可能に | — |
| **$d_9$ receipt** | モデルが $\mathbf Q(\zeta_3)$ 上 ⟹ 調達先が確定 | ⚠ **prereg 量。本書では計算していません** |
| **$r$ 測定** | 同上 | ⚠ **prereg 量。本書では計算していません** |
| **UNRAM U3-1..3** | 定義体 $\subseteq\mathbf Q(\zeta_3)$ ⟹ 不分岐集合 $S$ の候補が絞れる | ⚠ 悪い還元の集合は別途計算が要る |
| **【D2-GAP-5/6】【CAN-2】** | ★ 閉鎖 | — |
| **【D2-GAP-7】** | ★ 部分閉鎖 | 残る 2 本の軌道構造は未決 |
| **【R1-GAP-3】** | ★ **CLOSED**(Sol B2) | — |

## §9 発令の適法性(手続きの鎖)

1. **前哨監査**: ★ **実施済**(falsifier `fals_p1d2_r1_audit_v1.md`)— B-1/B-2/M-1〜M-5/m-1〜m-9 は v2 系で全件反映。
2. **数学的検収(Sol)**: ★ **済**(便 122 §1)— 必須訂正 3 点を本 v4 で反映。Sol の判定:
 > 「上の文言修正、研究者検分、凍結 tag が揃えば candidate 宣言は**発令可**である」
3. **独立第三系統**: ★ **済**(便 122 §2・【R1-GAP-3】CLOSED)。工房内盲線は店じまい(裁定 1097)。
4. **研究者検分**: ⚠ **未了**
5. **凍結 tag**: ⚠ **未設定**

$$\boxed{\ \textbf{⟹ 発令残は 4・5 のみ}\ }$$

## §10 記帳

- ★ **v4 の新規部分**: ① §6 #3 の証拠記述の訂正(独立性を主張しない)② §6 に **code path 3(Sol 独立実装)** を追加 ③ §7 の格を **cross-checked(3 code path)** へ・**【R1-GAP-3】CLOSED** ④ **§7.1 格の非伝播の明文化**(Sol 指定)⑤ **§7.2 R1-GAP-2 の exact 成功条件を Sol の固定文言で採録**+「昇格条件であって前件でない」の明記 ⑥ §5 に「紙の対応を verified と呼ばない」の一行。
- ⚠ **自己捕獲 m1109-1**: v2/v3 で第 2 レールを「独立実装」と書いていました。cert 自身が独立性を否認しており、**cert を読めば分かる誤記**でした。⟹ 証拠欄の形容は cert の自己申告に合わせる。
- **B4(③ 線)の訂正は本宣言に該当箇所なし** ⟹ `ss_gap1_count_spec_v1_addendum_b4.md` に分離。
- **申告**: 紙のみ(本書の機械走行ゼロ)・$u$/$c$ 非接触・**prereg 量非計算**・**Sol 監査済(条件つき PASS・訂正反映済)**・**verified ではない**(candidate 格)。
