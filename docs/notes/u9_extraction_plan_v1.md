# $u_9$ 抽出の実行計画書 **v1**(計画のみ・測定なし)

2026-07-28: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱(n=9 照準・裁定 102 の三重収束)。
**状態札**: `candidate / 単系統・未監査`。**commit していない。**
**依拠**: 正典(TB4 導出 v2.5・Rule 1 v1.5・manifest v1.6・BFC v2.15)+ repo 記録(`provenance/CLAIMS.md` W3-16/19/20/21/22/23・`provenance/taint_ledger.md`)+ `sol/sol_reply_73_math.md` Q5.2/Q5.3 + `docs/notes/hfun_functoriality_v1.md`。**外部文献なし。**

> ## ⛔ 本書の自己制約
> **$u_9$ の値を計算・推定・示唆しない。** $n=9$ 窓の dessin データ(置換三つ組・種数・passport)も**測定していない** — それらは本計画の**入力として列挙するだけ**である。曲線・$\lambda$・主係数・平方類・database には一切接触していない。**本書で実行した機械計算は $\Phi_{36}$ の構成のみ**(§2.1・体データであって窓の測定ではない)。

---

## 0. 先に訂正すべき前提 — **$u_5$ はまだ抽出されていない**

委嘱は「$K^{(5)}$ で $u_5$ を抽出した機構」と述べるが、repo の記録はそうなっていない。

| 記録 | 内容 |
|---|---|
| `CLAIMS.md` **W3-16** | 凍結 1 成立。**「解禁 = Model-Builder の個別モデル探索のみ。$u$ 系は Freeze 2 + 発射錠まで封鎖」** |
| `CLAIMS.md` **W3-19** | `non_implications=[… **Freeze 2 未成立**・**N_infty 未再開**]` |
| `CLAIMS.md` **W3-20** | 同上(`Freeze 2 未成立`・`N∞ 未再開`) |
| `provenance/seals/` | 開封済み seal は `seal_PSL_v1.opened.json` のみ($u$ 系の開封記録なし) |

$$ \boxed{\ \text{したがって $K^{(5)}$ にあるのは「\textbf{設計され凍結されたが一度も実行されていない} $u$ 抽出機構」である.}\ } $$

**⇒ 本計画の型が変わる**: $n=9$ は「$n=5$ で成功した手順の移植」**ではない**。**未実行の手順を、より重い窓へ先に適用する**という提案になる。**この差は §4 の前件チェックリストと §5 のリスク評価の両方に効く**ので、冒頭に置く。

> **★ 併記すべき既遂**: **$K^{(3)}$ では $u$ が実際に抽出されている**(`search/week4-u-k3.mjs`・16/16 PASS・`manifest_k5_appendixA_v1.md` §2 に $u=-4$、$\mathrm{ord}([u^{-1}]_6)=3$、covariance control $u'=-256/729$)。**$n=9$ の手順的先例として現実に使えるのは $K^{(5)}$ の設計ではなく $K^{(3)}$ の実績のほうである。**

---

## 1. $K^{(5)}$ 機構の $n=9$ への適応 — そのまま使える / 作り直し

$n=9$: $M=2n=18$、$2M=36$、$K_9=\mathbb Q(\zeta_{36})$、dessin 次数 $=[P_9:H_9]=2n=18$。

### 1.1 そのまま使える(窓非依存)

| # | 機構 | 出所 | 根拠 |
|---|---|---|---|
| S1 | **橋 $B_{\rm FC}$ の一般論**(定理 B-3/B-4/B-5/B-6/B-7) | BFC v2.15 | 窓前件 (W1)–(W5) を満たせば窓に依らない |
| S2 | **TB4 系**(TB4-0/1/2/3・TB4-A20・TB4-E・$\hat b_i=b_{\rm op}$) | TB4 v2.5 | 底 $U$ と規約のみ。$M\mid2M$ で足りる(TB4 導出 v2.5 §2.3) |
| S3 | **`Z-norm-seal/v1`(profinite)** | W3-20 | $\zeta_n^{\rm TB2}$ を全 $n$ で確定済 |
| S4 | **較正 (CAL)**($\alpha^{\rm Ih}=\alpha^{\rm std}$) | $A_5$ v4 §1.4 | 窓非依存(補題 C は $A_5$ を使わない) |
| S5 | **二経路独立性の要件**(§6.3)・**受理規則**(§6.4)・**UNKNOWN 停止規律**(§9) | Rule 1 v1.5 | 手続き規約。中身が変わっても枠は再利用 |
| S6 | **二段凍結・役割分離・taint ledger** | W3-16・`taint_ledger.md` | 手続き |
| S7 | **$\Lambda$/marking/$\tau$ の座標規約**(W-1・§1.1–§1.3) | 定義ノート v2・Rule 1 §1 | 窓非依存 |
| S8 | **detector の事前固定と塔** $H^{\rm fun}_9=\langle a_2,a_1a_3,q_2\rangle$ | `hfun_functoriality_v1.md` HF-1/HF-2 | **$n=9$ で (W3)(W4) と $\mathrm{ord}(X)=18$ は証明済**。$9\mid9$、$3\mid9$ の塔も good |

### 1.2 $n$ 依存 — **作り直し**

| # | 項目 | $K^{(5)}$ | $n=9$ | 重さ |
|---|---|---|---|---|
| R1 | **数体** | $K=\mathbb Q(\zeta_{20})$、$\Phi_{20}$、次数 **8** | $K_9=\mathbb Q(\zeta_{36})$、$\Phi_{36}(T)=T^{12}-T^6+1$、次数 **12** | 中(§2) |
| R2 | **dessin データ**(置換三つ組・passport・種数) | 次数 10・$(10,2^41^2,10)$・**種数 2** | 次数 18・$\sigma_0$ は **18-サイクル**(HF-1 より $\mathrm{ord}(X)=18$ かつ単純推移)。$\sigma_1$ の型・種数は **未測定(要計算)** | 中 |
| R3 | **曲線モデルと Belyi 写像** | 種数 2 超楕円 $y^2=f_{5\text{ or }6}(x)$ | **種数不明・超楕円とは限らない** | **重(§5-A)** |
| R4 | **Rule 1 §2 の M-A 正規形パイプライン**(M0 三分岐 (W)/(N$_{\rm aff}$)/(N$_\infty$)・M1–M6) | 種数 2 超楕円**専用** | **そのまま移植できない**(§5-A) | **重** |
| R5 | **経路 B**(Vieta/ノルム・(6.1)(6.2)(6.3)) | $y^2=f$ の構造に全面依存 | **超楕円でなければ消滅** | **重** |
| R6 | **経路 A**(cusp 展開) | Hensel/Newton・精度 $t^{13}$ / $s^{M+14}$ | **原理は移植可**。精度は $\mathrm{ord}_{P_0}\lambda=M=18$ に合わせ $t^{21}$ 相当へ | 中 |
| R7 | **$\mu_M$-torsor / Kummer 判定器** | $10=2\cdot5$ で $w\in K^{\times10}\iff K^{\times2}\wedge K^{\times5}$ | $18=2\cdot9$、$\gcd(2,9)=1$ ⇒ **同型の分解 $w\in K^{\times18}\iff K^{\times2}\wedge K^{\times9}$** が使える | 軽 |
| R8 | **述語** | $(P1)(P2)$・$\mathrm{ord}([v]_{10})\in\{1,5\}$ | **$\mathcal P_{9,3}=[a_9^3\ne1]$**(Sol Q5.3 (5.5))。**素数窓と違い深さが測れる** | 軽(§3) |
| R9 | **window inventory の身分** | `K5 = migrated` | **$n=9$ は inventory に**明示行がない** ⇒ 明示 catch-all により `not_assessed`** | 軽だが必須(§4) |
| R10 | **(W1)(W2)** の供給 | D1 Thm 4.3 等で $K^{(5)}$ について確立 | **$n=9$ の instance は未供給**(§4) | 中 |

> **★ R2 の注意(★教材 T5 の自己適用)**: 「$\sigma_0$ が単一 $2n$-サイクル」は $\mathrm{ord}(X)=2n$(HF-1(b))**かつ** $\langle X\rangle$ が単純推移(HF-1(c))から従う **既証明の帰結**であり、$n=9$ 窓の新規測定ではない。**一方 $\sigma_1$ の型は $\tau$ の非忠実性に依存するので群論計算が要る**($K^{(5)}$ でも $\mathrm{ord}(Y)=10$ に対し $\sigma_1$ の型は $2^41^2$ で位数 2 だった)。**本書では計算しない。**

---

## 2. 計算規模の見積り

### 2.1 数体 $K_9=\mathbb Q(\zeta_{36})$

$$ \Phi_{36}(T)=T^{12}-T^6+1,\qquad [K_9:\mathbb Q]=\varphi(36)=12 . $$
(本書で構成・検算した唯一の量。族パターン $\Phi_{4q}(T)=\Phi_{2q}(T^2)$ も $q=3,5,7,9,11$ で確認 — $\Phi_{36}(T)=\Phi_{18}(T^2)$、$\Phi_{18}(T)=T^6-T^3+1$。正典 Rule 1 (1.5) の「$\Phi_{20}(T)=\Phi_{10}(T^2)$」の族版。)

| 量 | $K^{(5)}$ | $n=9$ | 比 |
|---|---|---|---|
| 体の次数 | 8 | **12** | 1.5× |
| 元 1 個の表現 | $\mathbb Q^8$ | $\mathbb Q^{12}$ | 1.5× |
| 乗算(素朴 $O(d^2)$ + 剰余) | $\sim64$ | $\sim144$ | **2.25×** |
| dessin 次数 | 10 | **18** | 1.8× |
| $\mathrm{ord}_{P_0}\lambda=M$ | 10 | **18** | 1.8× |
| 経路 A の必要精度 | $t^{13}$ / $s^{24}$ | $t^{21}$ 相当 / $s^{M+14}=s^{32}$ | 1.6× |

**⇒ 体・級数の段は $K^{(5)}$ 設計の 2–3 倍程度**で、$8\,$GB 制約では問題にならない見込み。**律速はここではない**(§5-A)。

### 2.2 道具の選定(**実測**: この環境に `pari/gp`・`sage`・`magma` は**存在しない**)

| 用途 | 第一候補 | 理由 | 独立第二系統 |
|---|---|---|---|
| 有限群(窓・$\Lambda$・$\sigma$ 三つ組・(W3)(W4)(W5)) | **GAP 4.16**(`-o 2g`) | $\lvert P_9\rvert=4\cdot9^3=2916$ は軽量。既存の `search/*.g` 群を再利用 | **python**(`search/verify-i1-i3.py` の系統・helper 非共有。W3-22 で実績) |
| 数体 $K_9$ の厳密演算 | **node BigInt** の $\mathbb Q[T]/(\Phi_{36})$ 剰余環(Rule 1 §8.1 の方式をそのまま) | 正典が「浮動小数点を判定に用いない」を規定。実装が軽く監査しやすい | **GAP の native cyclotomics**(`E(36)`)— **実装を共有しない真の第二系統になる** |
| 級数(経路 A) | **node**(切断冪級数・BigInt 有理数) | 既存 `search/u-extract-pathA*.g` の設計を移植 | GAP 側の独立実装 |
| $K_9^{\times18}$ 判定 | $18=2\cdot9$・$\gcd(2,9)=1$ より $K^{\times2}\wedge K^{\times9}$ の 2 本へ分解(Rule 1 §8.2 の同型) | 因数分解は $T^2-w$、$T^9-w$ の $K_9[T]$ 上 | 別実装 |

> **⚠ 第二系統の設計上の利点**: **GAP は円分体を native に扱える**($\mathbb Q(\zeta_{36})$ を `E(36)` で直接)。node 側は $\mathbb Q[T]/(\Phi_{36})$ の剰余環を自前で書く。**両者はデータ構造も算法も共有しないので、Rule 1 §6.3 の「非共有 helper」要件を構造的に満たす。**
> **⚠ RAM**: 8 GB。**GAP は `-o 2g` で運用**(CLAUDE.md)。$\lvert P_9\rvert=2916$・$\Lambda$ の大きさ $18$ なので群論側は余裕。**級数・数体側も 12 次 × 32 項では問題にならない。**律速は R3(モデル探索)であって RAM ではない。

---

## 3. 封印プロトコル設計案(Sol Q5.3 の述語 vector の実装)

### 3.1 述語と出力型

$$ \mathcal P_{9,3}\ :=\ \bigl[\,a_9^{\,3}\ne1\,\bigr],\qquad \mathrm{ord}(a_9)=9\iff\mathcal P_{9,3}\ \text{(Sol (5.5))} $$

```text
predicate_id      = "P_9_3/v1"
predicate         = [ a_9^(9/3) != 1 ]          # 9 の素因数は 3 のみ ⇒ vector は 1 成分
output_domain     = { FULL_p_DEPTH , DEPTH_DROP , UNKNOWN }     # 閉じた三値・既定値禁止
                    #   FULL_p_DEPTH : a_9^3 != 1  (ord = 9)
                    #   DEPTH_DROP   : a_9^3 = 1   (ord ∈ {1,3})
                    #   UNKNOWN      : 予算超過・二経路不一致・前件未閉
never_emitted     = [ class representative, u_9 の値, 係数, 平方類, ord の具体値,
                      DEPTH_DROP 時の 1 か 3 かの別, 中間級数係数, モデル方程式 ]
storage           = SEALED_INTERNAL   # 生値は封印区画にのみ存在し、外へは output_domain の 1 値のみ
```

> **⚠ `DEPTH_DROP` を「$1$ か $3$ か」に細分しない**: 細分すると $a_9$ の位数そのものが漏れ、後続窓の blind 選択を汚染する。**識別力は「$9$ まで上がるか否か」の 1 ビットで足りる**(Sol Q5.4)。
> **⚠ `UNKNOWN` を既定値にしない**: 三値は閉じた enumeration。未知値・欠落は **fail-closed**(Rule 1 v1.3 §F2 の「三値を二値既定値で受けて live な枝が黙って消えた」型の再演を防ぐ)。

### 3.2 役割表(**taint 防止**・`provenance/taint_ledger.md` の様式に接続)

**設計前提(委嘱の指示)**: **司令塔は「$u_5$ 既知者」として扱う。** 実際に taint ledger は、司令塔・Sol・MB 担当 agent が $N_\infty$ 線の封印量($\hat c_\mu$)について `actual knowledge` を持つと記録している。**したがって司令塔を blind 側に置く設計は採れない。**

| 役 | 見てよいもの | 見てはならないもの | recusal |
|---|---|---|---|
| **Model-Builder(新規 agent・taint なし)** | $n=9$ の曲線モデル・$\lambda$・係数・級数 | $K^{(5)}$/$K^{(3)}$ の $u$・$\hat c_\mu$・平方類 | 述語の signer になれない |
| **Extractor A(新規 agent)** | 経路 A の入力と生 $u_9$ | 経路 B の実装・出力 | 同上 |
| **Extractor B(新規 agent)** | 経路 B(または代替第二経路)の入力と生 $u_9$ | 経路 A の実装・出力 | 同上 |
| **Sealer(新規 agent・値を受け取る唯一の合流点)** | 両経路の生 $u_9$・突合・$\mathcal P_{9,3}$ の評価 | — | **以後この線の blind 選択・freeze signer から永久 recusal** |
| **司令塔(Claude・既 taint)** | `output_domain` の 1 値のみ・手続き・digest | 生 $u_9$・係数・平方類・中間量 | **候補順位・blind acceptance の単独裁定から recusal**(既存 ledger の scope を踏襲) |
| **数学者(本稿筆者・Opus 第二インスタンス)** | 前件・証明・schema・`output_domain` の 1 値 | 生 $u_9$・モデル係数 | 前件が閉じるまで測定に関与しない |
| **Sol** | 前件・schema の敵対監査・`output_domain` の 1 値 | 生 $u_9$ | 既存 ledger どおり pre-Freeze-2 の候補選択から recusal |
| **研究者** | **すべて**(最終所有者) | — | — |

**taint ledger への追記様式**(既存 6 欄をそのまま使う):
```text
| artifact/schema | forbidden quantity | 露出時点 | 人物/役割 | 知得の別 | recusal scope | 許容役割 |
| P_9_3/v1        | u_9 の値・a_9 の位数 | (測定時) | Sealer     | actual knowledge | n=9 線の blind selector / freeze signer | 再現・文書化 |
```

### 3.3 発火順序(fail-closed)

```text
1. §4 の前件チェックリストが全項 CLOSED   ── 一つでも OPEN なら発火しない
2. Freeze 1(n=9 版 rule commitment)      ── 規則を値の前にコミット
3. Model-Builder が候補モデルを封印区画へ  ── 司令塔は係数を見ない
4. Extractor A / B が独立に生 u_9 を算出   ── 相互に実装非共有(Rule 1 §6.3)
5. Sealer が突合                           ── 不一致なら即 integrity stop → UNKNOWN
6. Freeze 2(value commitment)             ── b_op 等を u/G_K 観測前に記録
7. Sealer が P_9_3/v1 を評価し 1 値だけ公開
8. 事後 fitting の禁止・値を見てからの規則変更の禁止(Rule 1 §0.2-3・§8.4.3)
```

---

## 4. 前件チェックリスト(測定前に閉じているべき条項)

| # | 条項 | 現在の状態 | 出所 |
|---|---|---|---|
| C1 | **命題 ODD-H の監査**($[P:H]=2n$ かつ推移 ⇒ (1.2) の形・$N_P(H)=H\iff\alpha\ne0$) | **独立監査中**(W3-22 注) | `CLAIMS.md` W3-22 |
| C2 | **$n=9$ の (W3)(W4)** | **CLOSED**(HF-1(a)(c)(d) で直接証明・分類非依存)。W3-22 の GAP/python 二系統も $n=3..11$ で個数 $2n(n-1)$ を再現 | `hfun_functoriality_v1.md`・W3-22 |
| C3 | **$n=9$ の (W5)**($\Lambda$ の $\Phi(\mathfrak F_0)$-安定) | **UNKNOWN**。W3-22 の (W5) regression は**全 20 類 PASS** と記録されるが、それは当該 run の範囲。**$n=9$・$H^{\rm fun}$ での確認が要る** | W3-22 |
| C4 | **$n=9$ の (W1)(W2)** | **未供給**。正典 D1 Thm 4.3 系の $n=9$ instance が要る | R10 |
| C5 | **(CAL)** | **CLOSED**(窓非依存) | $A_5$ v4 §1.4 |
| C6 | **族条項の Sol ゲート**(family Rule 1・(1.7) 族版 $\zeta_M$ 部・$\bar\iota|_{K_q}$) | **OPEN**。便 73 Q3 は I-2 memo を監査したが、**族条項そのものは未提出・未ゲート** | `i2_family_rule1_memo_v2.md` |
| C7 | **(E-iv) の $n=9$ instance**(命名規約 $\tau(\zeta_{18}^{\rm Rule})=\tau(X_9)$) | **OPEN**(I-2 残留・便 73 Q3.3) | 同上 |
| C8 | **window inventory への $n=9$ 行**(`Z-norm-seal/v1` §3) | **未登録 ⇒ 明示 catch-all で `not_assessed`**。migration/compatibility certificate なしに `profinite` を宣言できない | W3-20・`znorm_seal_final_v1.md` |
| C9 | **$B_{\rm FC}$ (5′) の $n=9$ instance** | **OPEN**。BFC は三層供給型で `CURRENT: K5 supplied・K3/A5 pending` — **$n=9$ は層に載っていない** | W3-21 |
| C10 | **A3 framework gate** | **未閉**(全窓共通・文献要請 13(ii)) | W3-19/20/21 の `non_implications` |
| C11 | **$K^{(5)}$ の Freeze 2** | **未成立**。$n=9$ の前件ではないが、**手順の先例が存在しないことの根拠**(§0) | W3-19/20 |

$$ \boxed{\ \text{測定可能条件: C1・C3・C4・C6・C7・C8・C9 が CLOSED。現在 \textbf{7 項が OPEN}。}\ } $$

> **⚠ C10(A3)は $n=9$ で新たに閉じるものではない** — 全窓共通の framework gate であり、$u_9$ 測定の可否とは別線。**「$n=9$ をやれば A3 が閉じる」と読んではならない。**

---

## 5. 破綻リスク

### A. **最大リスク — Rule 1 の M-A パイプラインは種数 2 超楕円専用**(構造的)

Rule 1 v1.5 §2 の正規形(M0 の三分岐 (W)/(N$_{\rm aff}$)/(N$_\infty$)、M1 の $y^2=f_5/f_6$、M2 の重み表、補題 R1-M0/R1-U∞/R1-B∞)と **§6.2 の経路 B 全体**は、**種数 2 の超楕円曲線と $\mathrm{div}(\lambda)=10P_0-10P_\infty$ に全面依存**している。

$n=9$ の dessin は次数 18。**種数は未測定だが、$\sigma_0,\sigma_\infty$ が長いサイクルであることから種数 2 に留まる見込みは薄い**。種数 $\ge3$ または非超楕円なら:

- M-A の正規形アルゴリズムが**存在しない**(新規設計が要る)。
- **経路 B が消滅** ⇒ **二経路独立性(Rule 1 §6.3・受理規則 §6.4)を満たせない** ⇒ 片方だけでは $u$ を採用できない規約により **BRIDGE-UNKNOWN で停止**。

$$ \boxed{\ \textbf{第二経路の再設計が、}n=9\ \textbf{の律速である}(体の次数でも RAM でもない).\ } $$

**緩和案(いずれも未検証・candidate)**: (i) Sol Q6.2 の tower compatibility (6.3) が証明できれば、$d=3$ 段($K^{(3)}$・**$u_3$ は実測済**)との関係が第二経路になりうる — **ただし (6.3) 自体が UNKNOWN で、値から推測して採用してはならない**。(ii) 経路 A を**異なる局所助変数**で二度走らせるのは §6.3 の「非共有 helper」を満たさず**第二経路と数えない**。

### B. モデル探索の重さ

次数 18 の Belyi 写像を $K_9$(12 次体)上で明示的に得る作業は、$K^{(5)}$ の次数 10・8 次体より**質的に重い**。LMFDB 等の外部 database は**文献ゲートの対象**であり、本計画は勝手に使わない。

### C. $u_9$ の退化(Sol Q5.2 の警告)

- **型だけからは $\mathrm{ord}(a_9)=9$ は出ない。** 全分岐指数 $M$・$\lvert\mathfrak F_0\rvert=n$・regular detector という型は上界 $\mathrm{ord}(a_9)\mid9$ を説明するが**下界を与えない**。同じ型に位数 $1,3,9$ の class が共存しうる。
- **`DEPTH_DROP` は十分ありうる帰結であり、失敗ではない** — 型だけの楽観枝を反証する第一級の結果である(Sol Q5.4)。
- **virtual unit / $S$-unit / class-group 障害**: まず divisor の $2n$-可除性を分離し、その後に $S$-unit と class group の障害が現れる。**類数表だけで $a_9$ の order は決まらない**(Q5.2)。$\mathbb Q(\zeta_{36})$ の類数は本書では調べていない(**調べても述語の値は決まらない**ので、事前に見に行く動機がない)。

### D. 手続きリスク

- **§0 の通り $K^{(5)}$ で一度も走っていない手順**なので、$n=9$ で初めて出る実装バグを「数学的発見」と誤読する危険。**Rule 1 §7.4 の integrity quarantine と同じ規律**(実装 → transport → input seal → 紙上前件の順に監査)を $u$ 側にも適用すること。
- **taint の拡大**: Sealer を新規 agent にしても、その報告経路に司令塔が入る以上、**`output_domain` の 1 値以外を報告させない**設計が要る(§3.2)。

---

## 6. まとめ(4 行)

1. **$u_5$ は未抽出。** $n=9$ は「成功手順の移植」ではなく「未実行手順のより重い窓への先行適用」である。**現実の先例は $K^{(3)}$ のみ。**
2. **軽い**: 体($\Phi_{36}=T^{12}-T^6+1$・12 次)・級数・群論・Kummer 判定($18=2\cdot9$ の分解)・道具(GAP + node + python の三点で足り、RAM 8 GB で収まる)。
3. **重い**: **Rule 1 の M-A と経路 B が種数 2 超楕円専用**であり、$n=9$ では**第二経路の再設計が律速**。二経路が立たなければ規約上 BRIDGE-UNKNOWN で停止する。
4. **前件は 7 項が OPEN**(C1・C3・C4・C6・C7・C8・C9)。**測定はそれらが閉じた後**であり、述語は $\mathcal P_{9,3}=[a_9^3\ne1]$ の 1 ビット・出力は三値のみ・`DEPTH_DROP` も第一級の結果。
