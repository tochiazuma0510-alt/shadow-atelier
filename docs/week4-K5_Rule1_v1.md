# 凍結 1(Rule 1)候補文書 — $K^{(5)}$ 橋の規約・正規形・抽出手順 v1.3

2026-07-27 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱**。上位文書: `docs/manifest_k5_v1.md` v1.2 §「BRIDGE-IN 構築の独立性」1.・`sol/sol_reply_31_manifest.md` F4.1/F5/F9.3・`sol/裁定_29_ben31.md` 7。姉妹文書: `docs/week4-K5_S5設計_opus_v1.md`。

**v1.1(2026-07-27・便 32 P2/P6 + 裁定 31 の修理)。**
**v1.2(2026-07-27・便 34 F2.3 の blocker R1-T0 修理 — $P_0=\iota(P_\infty)=\infty_-$ の副枝を追加し、M-A を対象宇宙上の total algorithm にする)。**
**v1.3(2026-07-27・便 35 F1.5/F2.2/F5 の修理 — $(N_\infty)$ 排除証明書の撤回と正しい $(0\,\infty)$ 述語の確定。**副枝 $(N_\infty)$ は live**)。**

## v1 → v1.1 差分表

| # | 箇所 | v1 | v1.1 | 出典 |
|---|---|---|---|---|
| D1 | §2.2 **M3** | 「すべての係数を $\mathbb Z$ に入れる」(方法未定義) | 明示の既定手続き(分母 lcm)+ **どの clearing でもよい**ことを明記 | 便 32 F2.2 / P2 |
| D2 | §2.2 **M4** | 「重み付き content が極小」(被 floor 数なし・アルゴリズムでない) | **total algorithm** $\mathrm{wp}$: 重み $w_j$・素数ごとの $k_p=\min_{A_j\ne0}\lfloor v_p(A_j)/w_j\rfloor$・$\tau_+=\prod p^{k_p}$・$A_j\mapsto A_j/\tau_+^{w_j}$。零係数は min から除外、符号単元は M5 へ | 便 32 F2.2 (2.1)(2.2) |
| D3 | **§2.4(新設)** | — | **補題 R1-N1(denominator clearing 非依存性)**・**補題 R1-N2(残余 $=\{\pm1\}$・有限性)**+系(§3.1 の根拠)+計算可能性の注 | 便 32 F2.2「短く証明する」 |
| D4 | §2.3 (M-B) | $y^2=a(x)^2+c_5x^5$ | 符号修理($c_N$ 規約)。**M-B は第一次規則へ昇格しない**・discovery に使うなら sealed automation の別 schema | 便 32 F2.3 / F4.4 |
| D5 | §3.1 | 「有限性の証明義務」(未履行) | 補題 R1-N2 で**両枝とも証明済み**。U-b は fail-closed の札として存続 | 便 32 F2.2 |
| D6 | §4.1 の参考行 | $a(x_0)=0\Rightarrow\operatorname{ord}_{P_0}(\mu)=1$ | **直接証明**($a(x_0)=0\Rightarrow(x-x_0)^2\mid f_5\Rightarrow$ 特異)へ差替え | 便 32 F4.4 末尾 |
| D7 | §5.2 U-2 | 「モデルの単項式順序(固定)」(未定義) | **単項式順序 $(\mathrm{pol},b,a)$ 昇順辞書式**・**ambient $\mathcal A(n)$ の明示**・RREF の対象空間を $L(n_0P_\infty-P_0)$ と明記・存在の証明 | 便 32 F2.1 |
| D8 | §9.1 U-c | 条件のみ(予算値は §11) | **作用行に 600 秒を移記**(同 campaign 内で上限を増やして再分類しない) | 便 32 F2.5 / P6 |
| D9 | §11 論点 1–6 | 未決 | **1–6 すべて決着**(I-b 厳格版採用・M-B 非昇格・R1-C 非緩和・B-ii 独立・U-c 600 秒・文献ゲート 02 PASS) | 便 32 F2.1/F2.3/F2.4/F2.5・裁定 31 |

## v1.1 → v1.2 差分表(便 34 F2.3 の blocker **R1-T0** — $P_0=\iota(P_\infty)=\infty_-$)

> **v1.1 の欠陥(便 34 F2.3・そのまま受け入れる)**: 枝 (N) の六次モデルには無限遠点が $\infty_+,\infty_-$ の**二つ**あり、$P_0=\infty_-=\iota(P_\infty)$ は $P_0\ne P_\infty$ と両立する。したがって §5.1 の根拠にあった
> $$ \text{「}P_0\ne P_\infty\ \text{だから}\ x(P_0)\ \text{は有限」} $$
> は**偽**であり、v1.1 の M-A は対象宇宙上の total algorithm ではなかった。v1.2 は Sol の選択肢 2(副枝の新設)で total 性を回復する。選択肢 1(組合せ的排除証明書)は §11 論点 7 に**任意の補強**として設計だけ置く。

| # | 箇所 | v1.1 | v1.2 | 出典 |
|---|---|---|---|---|
| E1 | §2.2 **M0** | 判定は Weierstrass 性のみ・枝は (W)/(N) の 2 分岐 | **三分岐 (W) / (N$_{\rm aff}$) / (N$_\infty$)**。intrinsic 判定に **補題 R1-M0**($\ell(P_0+P_\infty)=2\iff P_0=\iota(P_\infty)$)を追加。**(N) は親枝として存続**し、$x(P_0)$ に言及しない (N) の全主張は両副枝で verbatim に成立 | 便 34 F2.3 |
| E2 | §2.2 **M1** 枝 (N) | 「$x$-平行移動で $x(P_0)=0$」(無条件) | 副枝 **(N$_{\rm aff}$)** は従来通り。副枝 **(N$_\infty$)** は $x(P_0)=\infty$ ゆえ**適用不能** — 代替の正規化 **$B_5=0$**(depressed form・$e=-B_5/6$ で一意・monic 性と $\infty_\pm$ ラベルを保つ)で平行移動を使い切る | 便 34 F2.3 |
| E3 | §5.1 **U-1** | 「$P_0\ne P_\infty$ だから $x(P_0)$ は有限」(**偽**) | **偽命題を除去**。枝 (W) でのみ「$P_0\ne P_\infty\Rightarrow P_0$ アフィン」が成り立つことを証明し、(N) では $P_0$ 無限遠 $\iff$ (N$_\infty$) と特徴づける。**(N$_\infty$) では $t:=1/x$**(**補題 R1-U∞** で $\operatorname{ord}_{P_0}(1/x)=1$ を証明。**$y/x^3$ は単元**($P_0$ での値 $-1$)ゆえ uniformizer ではない) | 便 34 F2.3 |
| E4 | §5.2 **U-2** | $V=L(n_0P_\infty-P_0)$ をアフィン消滅条件で切る | (N$_\infty$) では $V=\{g\in\mathcal A(n_0):\operatorname{ord}_{\infty_-}(g)\ge1\}$(アフィン条件は消え、$\infty_-$ の局所展開条件に一本化)。$n_0\le5$ の議論と 4. の存在証明は不変 | 便 34 F2.3 |
| E5 | §6.1 **経路 A** | $P_0$ で $x,y$ を $K[[t]]$ に展開(精度 $t^{13}$) | (N$_\infty$) では $x,y$ が $P_0$ で**極**を持つので $(s,w)=(1/x,\,y/x^3)$ チャートで $W=\sqrt F$ を **精度 $s^{23}$**(理由つき)まで持ち上げ、$\lambda=s^{-10}(\tilde A-W\tilde B)$ から $u_{10},\dots,u_{13}=[s^{20}],\dots,[s^{23}]$ を取る | 便 34 F2.3 |
| E6 | §6.2 **経路 B** | (6.1)(6.2) のみ(いずれも **$x_0=x(P_0)$ 有限が前提**) | **B-iii(6.3)を新設**: $u^{(B)}=\hat c/(2a_{10})$($\hat c:=A^2-B^2f$ は**定数**、$a_{10}:=[x^{10}]A$)。**補題 R1-B∞** で $\deg A=10$、$\deg B=7$、$b_7=a_{10}\ne0$、$N(\lambda)\in\mathbb Q^\times$ を証明。**級数を使わない**点は B-i/B-ii と同じ(むしろ弱い仮定) | 便 34 F2.3 |
| E7 | §9.1 U-c / §9.2 | U-c は M0 の Weierstrass 判定のみ | U-c を M0 の**全枝判定**(Weierstrass 性 + $P_0=\iota(P_\infty)$ 判定)へ拡張(予算値は不変)。**I-j 新設**(枝 (N$_\infty$) の構造検査 (N∞-1)–(N∞-4) の破れ = 入力破損) | 便 34 F2.3 |
| E8 | §10-6 | 記録欄「枝 (W)/(N) の別」 | 「枝 (W)/(N$_{\rm aff}$)/(N$_\infty$) の別」+ $\hat c$(N$_\infty$ のみ)を追加(**値は凍結 2 まで空**のまま) | 便 34 F2.3 |
| E9 | §11 | 論点 1–6 決着 | **論点 7 新設**(**補題 R1-N∞-S**: (N$_\infty$) は ordered dessin が底の Möbius 対合 $\lambda\mapsto1/\lambda$ による $(0\,\infty)$-交換で不変であることを**要求する** ⇒ 凍結済み fixture 上の**純組合せ的排除証明書**が可能)。§11.1 に **R-4**(S5 設計 §3.3.4 の分離条件へ **N-0**: $P_0\ne\iota(P_\infty)$ を追記・別便) | 便 34 F2.3 / F3.3 |

## v1.2 → v1.3 差分表(便 35 F1.5 の blocker — **$(N_\infty)$ 排除証明書の撤回**)

> **v1.2 の欠陥(便 35 F1.5・そのまま受け入れる)**: §11 論点 7 は補題 R1-N∞-S 3.(「(N$_\infty$) ならば ordered dessin は $(0\,\infty)$ 交換で不変」)から**組合せ的排除証明書**を作れると書いたが、**置換水準の述語を書き下さなかった**。その空白を埋めた実装は素朴な交換
> $$ g\sigma_0g^{-1}=\sigma_\infty,\quad g\sigma_1g^{-1}=\sigma_1,\quad g\sigma_\infty g^{-1}=\sigma_0 \tag{35.3} $$
> を検査したが、これは $(0\,\infty)$-対称性の必要条件では**ない**。正しい述語は Nielsen 代表 $\beta(x)=z,\ \beta(y)=y,\ \beta(z)=y^{-1}xy$ に対応する**捻れ形 (35.4)** である。**述語が誤りなので `ninf_excluded=true` は撤回する**(仕様の空白は起草者=私の責任 — ★教材 28)。しかも正しい述語の witness は**両 fixture に実在する**(§11 論点 7)ので、対偶による排除は**原理的に使えない**。
>
> $$ \boxed{\ \textbf{副枝 (N}_\infty\textbf{) は排除されていない — live な枝として全工程で扱う。}\ } $$

| # | 箇所 | v1.2 | v1.3 | 出典 |
|---|---|---|---|---|
| F1 | §11 **論点 7** | 「$(0\,\infty)$ 交換で不変 ⇒ 組合せ的**排除**証明書が可能」(置換水準の述語なし。保守判定 $T$ の設計のみ) | **正しい述語 (35.4)** を正本として書き下す。**補題 R1-N∞-W**(解の一意性・$g^2=\sigma_1$・(35.3) の**空虚性**)を新設。**両 fixture の witness (35.5) を記録**(Sol 便 35 (35.5)+数学者の独立再現)。結論を **「対称性条件 PASS・(N$_\infty$) 存否は未決」**に確定し、**排除路線を閉じる** | 便 35 F1.5 / 裁定 36 |
| F2 | §2.2 **M0** | 三分岐判定を規定 | **判定 (2.-1) の実走を義務化**(「排除済みだから省略」を明示的に禁止)。**枝ラベルは三値 enumeration・既定値への fallback を禁止**(未知ラベル ⇒ I-m) | 便 35 F5.1 / F5.2 |
| F3 | §6.2 (N$_\infty$) 封印段 | $u,\hat c,a_{10}$ を封印段 | **$\hat c_\mu:=a^2-f_6p^2$($\mu$ 側の norm 定数)も同段**へ。理由: 補題 R1-N∞-S 2. の $\hat c=1$ と $\hat c=c^2\hat c_\mu^2$ から **(P1) $\iff\hat c_\mu\in K^{\times2}$** が (N$_\infty$) では**単独で**成立する(**I-b∞**) | 本便(S5 設計 v1.2 §3.3.5 と対) |
| F4 | §6.3 独立性の要件 | 1.–4. | **5.(model digest 束縛)**と **6.((N$_\infty$) 用 raw schema: $x_0,y_0$ を持たない)**を追加 | 便 35 F2.2 / F5.2 |
| F5 | §9.2 | I-a〜I-k | **I-l**(raw の model digest が凍結 bundle の expected digest と不一致)・**I-m**(枝ラベルが三値 enumeration 外/既定値へ落とした)を新設。**I-b** に (N$_\infty$) の $\hat c_\mu$ を明記 | 便 35 F2.2 / F5.2 |
| F6 | §10 | 記録 1.–6. | **7.**(fixture ごとの $(0\,\infty)$ witness $g_i$ と (35.4) 充足の記録 — **凍結 2 前でも可視**。$u$ に触れない fixture 事実) | 本便 |
| F7 | §11.1 | R-1〜R-5 | **R-4 を閉**(S5 設計 v1.2・同便)。**R-5 は最優先へ復帰**((N$_\infty$) が live ゆえ)。**R-6/R-7/R-8 新設**(排除証明書の再発行・digest 束縛・枝ラベル fail-closed) | 便 35 F5 / 再申請リスト 1.3.5. |

> **v1.2 の $(N_\infty)$ 機構は一切変更しない(確認)**: M1 (2.-3)(depressed $B_5=0$)・§5.1 U-1 第三行($t=1/x$)・補題 R1-U∞・§5.2.1 の (N$_\infty$) 行($\operatorname{ord}_{\infty_-}(g)\ge1$ 一本)・§6.1 (b) 経路 A∞(A∞-1〜A∞-4)・§6.2 B-iii (6.3)・補題 R1-B∞・構造検査 (N∞-1)–(N∞-4)・I-j・I-k・§10-6 の記録欄は**すべて v1.2 のまま有効**である。v1.3 が変えるのは**排除の可否(§11 論点 7)とその帰結**、および上表 F2–F7 の規則面だけ。**M-A の total 性は v1.2 で既に回復しており、(N$_\infty$) が live であっても Rule 1 は止まらない。**

> **digest 注意(P7)**: 本改訂で canonical serialization が変わる。§10-1 の sha256 は**再取得を要する**(司令塔)。v1.1 の digest `0863b3fd…`・v1.2 の digest `7e3d7e22…` は v1.3 には適用されない。
>
> **起草時点の申告(v1.3 で更新)**: 本改訂の全過程で個別モデル候補・係数・数値近似・database に**一切接していない**。v1.1 で新たに行った機械計算は、**§2.4 の補題を無作為な有理係数ベクトルで確認する検算スクリプト 1 本**(`search/wp-check.mjs`(司令塔が恒久化・再走 11649/0 再現)・整数演算・曲線データを入力に持たない・11649 検査すべて一致)。**v1.2 で新たに行った機械計算は無い**(§6.2 B-iii の補題は二通りの独立な手計算で照合 — §0.4-3)。**v1.3 で新たに行った機械計算は、凍結済み fixture の置換三つ組のみを入力とする (35.4)(35.5) の検算 1 本**(§0.4-4・整数/置換演算のみ・曲線 $\lambda,u,c$ に接触なし)。探索コマンドは依然として一度も実行していない。

---

## 0. この文書の身分と不変条項

### 0.1 身分

本文書は **凍結 1 の候補**である。**受理されるまでは効力を持たず、受理された瞬間に不変となる。**

> **凍結 1 の時点(manifest v1.2・W2)**: 両 dessin のいかなる**個別モデル候補・係数・数値近似にも接する前**、**探索コマンドを一度も実行する前**に完了する。
>
> **起草時点の申告**: 本文書の起草者(Opus)は、起草の全過程で個別モデル候補・係数・数値近似・database に**一切接していない**。用いた計算は §0.4 に列挙したものだけで(v1: 1 本、v1.1: +1 本、**v1.2: 追加なし**、**v1.3: +1 本**)、その入力は凍結済み有限 fixture と無作為な有理数だけである。

### 0.2 不変条項(受理後は一切変更しない)

1. **$a = j_{\rm ns}^{-1}j_{\rm sq} = 1$ は formal invariant であり永久不変**(便 31 F5・裁定 29-2)。橋側の捻れは $b_{\rm sq},b_{\rm ns}$ に、比較指数は $a_{\rm eff}$ に記録する。**$a$ を更新しない。**
2. **$\lambda/t^{10}$ の定数項を 1 に正規化することは禁止**(それが $u$ そのもの)。
3. **規則が一意候補を返さないときは UNKNOWN で止まる**(§9)。規則を後から変えて一意化しない。
4. **漏洩した run は後から同じ規則を hash して救済しない。** 汚染 artifact を隔離し、規則を変えるなら新 version の campaign とする。

### 0.3 本文書が依存していないもの(頑健性の設計)

**したがって本文書の第一次規則(§2 の (M-A))は、`docs/week4-K5_S5設計_opus_v1.md` の命題群に一切依存しない形で書いてある。** S5 設計の結果は §2 の (M-B)(整合検査)と §6 の副経路にのみ現れ、そこが崩れても Rule 1 は生きる。

> **v1.2 で追加した副枝 (N$_\infty$) も同じ設計である**: 補題 R1-M0(Riemann–Roch と種数 2 の超楕円 pencil)・補題 R1-U∞(無限遠チャート)・補題 R1-B∞($\operatorname{div}(\lambda)=10P_0-10P_\infty$ と Vieta)・補題 R1-N∞-S(分岐点集合の $\iota$-不変性)は**いずれも S5 設計に依存しない**。S5 設計側の欠品(N-0)は §11.1 R-4 として別便に送る(Rule 1 の受理条件ではない)。
>
> **(v1.3)** R-4 は `docs/week4-K5_S5設計_opus_v1.md` **v1.2**(同便)で閉じた。**副枝 (N$_\infty$) が live に確定しても、この独立性は変わらない** — 上の四補題はいずれも $\operatorname{div}(\lambda)=10P_0-10P_\infty$ と超楕円幾何だけを使い、$\mu$-分解(命題 S5-2)を使っていない。S5 設計 v1.2 が新設した命題 S5-3∞ は **Rule 1 の受理条件ではなく**、§6.2 の補助経路 B′ と Model-Builder の探索設計にのみ関わる。

**v1.1 での S5 側の監査状態の更新**(便 32 F4):

| S5 側の主張 | 便 32 の判定 | Rule 1 での使われ方 |
|---|---|---|
| 補題 S5-B(唯一のブロック系)・命題 S5-1($\operatorname{ord}=5$)・命題 S5-2($\lambda=c\mu^2$) | **PASS**(紙上証明が通る。有限群部分は cross-checked artifact として受理・**Lean の `verified` ではない**) | §9 I-g(A8 の破れで stop)・§6.2 の補助経路 B′ |
| **命題 S5-3(曲線の二枝正規形)** | **差戻し**(符号・gauge の不整合)→ **S5 設計 v1.1 で修理**。なお**単系統・未監査**(機械照合は受けていない — ★教材 22) | §2.3 (M-B)・§4.1 の参考行のみ。**第一次規則は依存しない** |
| 命題 S5-4((P1) $\iff c\in K^{\times2}$) | **PASS** | §8.5・**§9 I-b**(下記) |

**例外(依存を明示)**: §9 の停止条件 I-b(**$\lambda=c\mu^2$ の $c$ の平方類の漏洩禁止**)は命題 S5-4 に依存する。ただしこれは**禁止を増やす向き**の依存であり、命題 S5-4 が誤りでも安全側に倒れる。S5-4 は便 32 F4.6 で PASS。

### 0.4 起草時に用いた計算

1. `scratchpad/k5_blocks.js`(node・単系統・v1)— 入力は凍結済み有限 fixture($G_5$ の $(v,q)$ 座標と標的 $H$)のみ。
2. `search/wp-check.mjs`(node・単系統・**v1.1 で追加**・司令塔恒久化)— §2.4 の補題 R1-N1/R1-N2 の検算。入力は**無作為な有理係数ベクトル**のみ(BigInt 整数演算・11649 検査すべて一致)。
3. **v1.2 では機械計算を追加していない。** §6.2 の補題 R1-B∞ は (i) $G_+G_-=\hat c\,s^{2M}$ と $G_+(0)=2\tilde A(0)$ による一般証明、(ii) $M=3$ の玩具族 $f_6:=A_3(x)^2-\hat c,\ \lambda:=A_3(x)+y$($A_3$ モニック 3 次・$\hat c\in\mathbb Q^\times$ は**記号のまま**)における冪級数の直接展開($\lambda=\hat c\,s^3/(2\tilde A)+O(s^9)$ ⇒ $u=\hat c/(2a_3)$)、の**二通りの手計算**で照合した。(ii) は**記号族**であって個別モデル候補ではなく、$K^{(5)}$ の dessin データ($\deg=10$・単数値係数)を一切含まない。
4. **v1.3 で追加した計算 1 本**(scratchpad・node・整数/置換演算のみ・リポジトリ外)— §11 論点 7 の (35.4)(35.5) の独立検算。入力は `certificates/k5fixture/K5-{sq,ns}.json` の `perm_triple`(**凍結済み有限 fixture**)のみ。行った検分は (a) $\sigma_0\sigma_1\sigma_\infty=\mathrm{id}$、(b) 補題 R1-N∞-W 2. の 10 候補の悉皆生成、(c) 各候補に対する (35.4) と (35.3) の充足判定、(d) $g^2=\sigma_1$、(e) $[\sigma_0,\sigma_1]\ne1$。**Sol の便 35 とは方法が独立**(Sol は紙上検分、私は $g(0)$ による 10 候補悉皆)。**曲線・$\lambda$・$u$・$c$・数値近似・database には一切接触していない。**

**いずれも曲線・$\lambda$・$u$・数値近似・database に接触なし。**

---

## Q1 → §1. 座標・向き・埋め込みの凍結

### 1.1 底と基点

$$ U := \mathbf P^1_{\mathbb Q}\smallsetminus\{0,1,\infty\},\qquad \text{基点} = \text{接基点}\ \vec{01}. $$

$\mathbf C$ の**標準的向き**(反時計回りが正)を採る。$\gamma_0,\gamma_1,\gamma_\infty\in\pi_1^{\rm top}(U,\vec{01})$ を、それぞれ $0,1,\infty$ を**反時計回り**に一周する単純ループで

$$ \gamma_0\gamma_1\gamma_\infty = 1 \tag{1.1} $$

となるものとする(この順序・この向きが正本)。$\hat F_2 = \pi_1^{\rm geom}(U,\vec{01})$ の位相生成元を $x:=\gamma_0,\ y:=\gamma_1,\ z:=\gamma_\infty$、$xyz=1$。

### 1.2 ordered branch $\leftrightarrow$ $X,Y,Z$

$\pi:\hat F_2\twoheadrightarrow P = G_5$ を D1 (3.6) の marking とする:

$$ \boxed{\ 0\ \leftrightarrow\ X = \pi(x),\qquad 1\ \leftrightarrow\ Y = \pi(y),\qquad \infty\ \leftrightarrow\ Z = \pi(z),\qquad XYZ=1.\ } \tag{1.2} $$

$X = (r,s,s),\ Y = (rs,r,rs),\ Z = (r^2s,r^{-1}s,r)$(D1 §2.1・変更禁止)。

### 1.3 $\Lambda$ 上の作用と合成の向き

$$ \Lambda_i := \{\,gH_ig^{-1}\ :\ g\in G_5\,\},\qquad \tau_i(g)(H') := g\,H'\,g^{-1}\quad(\textbf{左作用}). \tag{1.3} $$

$\tau_i:G_5\to\operatorname{Sym}(\Lambda_i)$ は**準同型**。置換の合成は $(\sigma\rho)(p) := \sigma(\rho(p))$ とする。そこで

$$ \sigma_0 := \tau_i(X),\quad \sigma_1 := \tau_i(Y),\quad \sigma_\infty := \tau_i(Z),\qquad \sigma_0\sigma_1\sigma_\infty = \mathrm{id} \tag{1.4} $$

($XYZ=1$ と $\tau_i$ の準同型性から自動)。

> **第二系統の規約差の扱い**: GAP は $H^g = g^{-1}Hg$(右共役)を使う。**規約を暗黙に吸収してはならない。** 第二系統は「$\tau^{\rm GAP} = \tau\circ(\ )^{-1}$ を使った」ことを**出力に明記**し、突合器はその反転を明示的に適用する。(D1 検算 I4 が「$a$ はこの反転で不変」を確認済だが、それは $a$ についてのみの結果であり、$b_i$ については§7 で改めて記録する。)

### 1.4 $K$ の複素埋め込み(**$b_i$ の一意性の生命線**)

$$ K := \mathbb Q(\zeta_{20}) = \mathbb Q[T]/(\Phi_{20}),\qquad \Phi_{20}(T) = T^8-T^6+T^4-T^2+1 . \tag{1.5} $$

($\Phi_{20}(T)=\Phi_{10}(T^2)$ — $10$ が偶数だから。)

$$ \boxed{\ \iota_\infty: K\hookrightarrow\mathbf C\ \text{を、}\ \zeta_{20}\ \text{が}\ \Phi_{20}\ \text{の根のうち}\ \operatorname{Im}>0\ \text{かつ}\ \operatorname{Re}\ \text{最大のもの}\ \text{に写るものとして固定する}. } \tag{1.6} $$

$\Phi_{20}$ の根は $e^{2\pi ik/20}$($k\in\{1,3,7,9,11,13,17,19\}$)。上半平面にあるのは $k=1,3,7,9$ で、$\operatorname{Re}$ 最大は $k=1$。ゆえに (1.6) は**一意**に $\zeta_{20}=e^{2\pi i/20}$ を指す。

$$ \zeta_{10} := \zeta_{20}^2,\qquad \zeta_5 := \zeta_{20}^4 . \tag{1.7} $$

### 1.5 $\tau_i$ の $\mu_{10}$ 版・Kummer 規約・$j_i$

$$ \iota:\ \mu_{10}\xrightarrow{\ \sim\ }\langle X\rangle,\ \ \zeta_{10}\mapsto X\quad(\textbf{両 dessin 共通}),\qquad \tau_i:\mu_{10}\hookrightarrow\operatorname{Sym}(\Lambda_i),\ \ \tau_i(\zeta_{10}) = \tau_i(X). \tag{1.8} $$

$$ \kappa_w(\gamma) := \frac{\gamma(w^{1/10})}{w^{1/10}}\in\mu_{10}\qquad(\gamma\in G_K,\ w\in K^\times). \tag{1.9} $$

$\mu_{10}\subset K$ ゆえ $\kappa_w$ は**準同型**であり、しかも **$10$ 乗根の取り方に依らない**(二つの根は $\mu_{10}\subset K$ の元だけ違い、$G_K$ 不変)。

$$ j_i:\ \mu_{10}[5]\xrightarrow{\ \sim\ }\mathfrak F_0,\qquad j_i\bigl(\zeta_{10}^{2t}\bigr) = \Phi_{0,-t}\qquad(\text{D1 v1.2 }(6.3)\text{・}i\ \text{に依らない}). \tag{1.10} $$

$$ \boxed{\ a := j_{\rm ns}^{-1}j_{\rm sq} = 1\ \in(\mathbb Z/5)^\times\quad(\textbf{永久不変}).\ } \tag{1.11} $$

### 1.6 $(\mathbb Z/20)^\times\to(\mathbb Z/10)^\times$ の $2:1$ lift(別封印項目)

$\ker\bigl((\mathbb Z/20)^\times\to(\mathbb Z/10)^\times\bigr) = \{1,11\}$(位数 2)。すなわち $\tilde\chi$ の値 8 通りは $\mu_{10}$ 上では 4 通りに潰れる。**この $2:1$ は $b_i$($\varphi(10)=4$ 通り)とは別の項目**であり、混同しない(便 31 F5.1)。付録として凍結記録に別欄で記載する。

---

## Q2 → §2. モデルの同値関係と正規形アルゴリズム

### 2.1 同値関係

$(C,\lambda)$ と $(C',\lambda')$ が同値 $:\iff$ $\mathbb Q$ 上の同型 $\varphi:C\to C'$ で $\lambda'\circ\varphi = \lambda$ となるものが存在する。**$\operatorname{Aut}(C/\mathbf P^1_\lambda)=1$ ゆえ $\varphi$ は存在すれば一意。**

$\lambda$ 側に Möbius の自由度は**ない**: dessin は ordered($0,1,\infty$ が区別されている)なので、$\lambda\mapsto1-\lambda,\ 1/\lambda,\dots$ の 6 元 Möbius 群は**使えない**。$\lambda$ は「$0$-分岐で $0$、$1$-分岐で $1$、$\infty$-分岐で $\infty$」という条件で完全に決まる。

### 2.2 (M-A) 第一次正規形パイプライン(S5 設計に依存しない)

**M0(intrinsic な枝の決定・v1.2 で三分岐化)**: 次の**三つ**を、いずれも**モデルに依らない判定**で決める。

$$ \text{(i)}\ \ P_\infty\ \text{は Weierstrass 点}\ \iff\ \ell(2P_\infty) = 2, \qquad \text{(ii)}\ \ P_0\ \text{についても同様}, $$

$$ \text{(iii)}\ \ \boxed{\ P_0 = \iota(P_\infty)\ \iff\ \ell(P_0+P_\infty) = 2\ }\qquad(\textbf{v1.2 で新設・補題 R1-M0}). \tag{2.-1} $$

以後の枝を

$$ \text{(W)} := \{P_\infty\ \text{Weierstrass}\},\qquad \text{(N)} := \{P_\infty\ \text{非 Weierstrass}\} $$

と書き、さらに **(N) を二つの副枝に分ける**:

$$ \boxed{\ \text{(N}_{\rm aff}\text{)} := \{P_\infty\ \text{非 W}\}\cap\{P_0\ne\iota(P_\infty)\},\qquad \text{(N}_\infty\text{)} := \{P_\infty\ \text{非 W}\}\cap\{P_0=\iota(P_\infty)\}.\ } \tag{2.-2} $$

**全三枝を先に書く**(以下)。**(N) は親枝として存続する** — 以下の (N) についての主張のうち **$x(P_0)$ に言及しないもの**(M2 の重み表、M3/M4、§2.4、§3.1、§3.2、§5.2.0 の ambient $\mathcal A(n)$、§4.1 の (N) 行)は、**両副枝でそのまま成立する**。$x(P_0)$ が入る箇所は M1(下)・§4.2・§5.1・§5.2.1-2.・§6.1・§6.2 だけであり、そこにのみ副枝分けを書く。

> **補題 R1-M0(判定 (2.-1) の正当化と副枝の基本性質).** $C$ を種数 2、$P_0\ne P_\infty$ とする。
> 1. $\ell(P_0+P_\infty)\in\{1,2\}$ であり、$\ \ell(P_0+P_\infty)=2\iff P_0=\iota(P_\infty)$。
> 2. 枝 (W) では $P_0=\iota(P_\infty)$ は**起こらない**。すなわち副枝 (N$_\infty$) は枝 (N) の内部にしか現れない。
> 3. 副枝 (N$_\infty$) では $P_0$ は**非 Weierstrass** である(よって M0 (ii) の出力は自動的に「非」)。
>
> **証明.** 1. $D:=P_0+P_\infty$、$\deg D=2$。Riemann–Roch $\ell(D)-\ell(K-D)=\deg D-g+1=1$ と $\deg(K-D)=0$ より $\ell(K-D)\in\{0,1\}$、かつ $\ell(K-D)=1\iff D\sim K$。$g=2$ では $K$ が唯一の $g^1_2$ であり $|K|=\{P+\iota P: P\in C\}$(超楕円 pencil = $x$ の fiber 全体)。ゆえに $D\sim K$ なら $D\in|K|$ すなわち $\{P_0,P_\infty\}=\{P,\iota P\}$、$P_0\ne P_\infty$ と合わせて $P_0=\iota(P_\infty)$。逆は $D=P_\infty+\iota(P_\infty)\sim K$ で明らか。
> 2. (W) では $\iota(P_\infty)=P_\infty\ne P_0$。
> 3. $\iota(P_0)=\iota^2(P_\infty)=P_\infty\ne P_0$ ゆえ $P_0$ は $\iota$ の不動点でない。$\blacksquare$

> **実装上の同値判定(モデルを得たあとの検査)**: 枝 (N) の六次モデルでは $x^{-1}(\infty)=\{\infty_+,\infty_-\}=\{P_\infty,\iota(P_\infty)\}$(§5.1 補題 R1-U∞)だから、
> $$ \text{(N}_\infty\text{)}\iff x(P_0)=\infty \iff P_0=\infty_- . $$
> intrinsic 判定 (2.-1) と座標判定の**不一致は入力破損** ⇒ **I-k**(§9.2・v1.2 で新設)。**予算超過は U-c**(§9.1・値は不変)。

> **【v1.3・便 35 F5.1/F5.2 の必須規定】M0 の三枝判定は実走で必ず実行する。**
> 1. **判定 (2.-1)($\ell(P_0+P_\infty)$ の計算)を省略してはならない。** とくに「組合せ的証明書で (N$_\infty$) は排除済み」という理由での省略・既定枝への固定を**明示的に禁止**する。**その証明書は撤回された**(§11 論点 7)。判定が予算内に閉じなければ **U-c**(§9.1)であって「(N$_{\rm aff}$) とみなす」ではない。
> 2. **枝ラベルは三値の enumeration** $\{\texttt{W},\ \texttt{N\_aff},\ \texttt{N\_infty}\}$ とし、**既定値へ落とす実装を禁止する**。入出力のどこかで未知ラベル・欠落ラベルが現れたら、既定値に解釈せず **I-m**(§9.2・v1.3 で新設)で停止する(fail-closed)。
>    > (根拠: 便 35 F5.2 — 実装の `loadModel` が `nonWeierstrass` 以外を無条件に `Weierstrass` へ落としていた。**三枝化した規則を二値の既定値付き実装で受けると、live な枝が黙って消える。**)
> 3. 三枝はこの順で**排他かつ網羅**である: (W) $\iff$ $\ell(2P_\infty)=2$;さもなくば (N$_\infty$) $\iff$ $\ell(P_0+P_\infty)=2$;さもなくば (N$_{\rm aff}$)。補題 R1-M0 2. により (W) と (N$_\infty$) は両立しないので、この順序は判定結果に影響しない。

**M1(超楕円モデル)**

- **枝 (W)**: $\deg f = 5$ のモデル $y^2=f_5(x)$ を取り、$P_\infty = \infty$(唯一の無限遠点)とする。$f_5$ は $\mathbb Q$ 上**モニック**にできる($x\mapsto tx,\ y\mapsto sy$ で主係数 $\mapsto s^{-2}t^5\cdot(\text{主係数})$;$t=\mathrm{lc},\ s=\mathrm{lc}^3$ と取れば $\mathrm{lc}\mapsto1$)。次に $x$-平行移動で $\boxed{x(P_0)=0}$(**この枝では $P_0$ は必ずアフィンなので適用可能** — §5.1 補題 R1-U∞ 3.)。
- **枝 (N)**: $\deg f = 6$ のモデル $y^2=f_6(x)$ を取り、$x(P_\infty)=\infty$ とする。$P_\infty\in C(\mathbb Q)$ ゆえ $\mathrm{lc}(f_6)\in\mathbb Q^{\times2}$、$y$-スケールで $f_6$ を**モニック**にできる。$P_\infty = \infty_+$($y\sim+x^3$ の枝)と**定義する**(これが $y\mapsto-y$ を固定する — §4)。**ここで平行移動の使い方が副枝で分かれる**(v1.2):
  - **副枝 (N$_{\rm aff}$)**($P_0\ne\iota(P_\infty)$;$P_0$ はアフィン点で $x(P_0)\in\mathbb Q$): 従来どおり $x$-平行移動で $\boxed{x(P_0)=0}$。
  - **副枝 (N$_\infty$)**($P_0=\iota(P_\infty)=\infty_-$;$x(P_0)=\infty$): **$x$-平行移動による $x(P_0)=0$ は適用不能**($P_0$ は $x$-直線の $\infty$ の上にある)。代わりに、余った平行移動を**係数側**で使い切る:
    $$ \boxed{\ \text{(N}_\infty\text{) の正規化: }\ x\text{-平行移動で}\ B_5 = 0\ \ (\text{depressed form}).\ } \tag{2.-3} $$

> **(2.-3) の一意性と両立性(v1.2).** $f_6 = x^6+\sum_{j\le5}B_jx^j$(モニック)に $x\mapsto x+e$ を施すと $f_6(x+e)$ の $x^5$-係数は $B_5+6e$。標数 0 で $6\in\mathbb Q^\times$ だから $e := -B_5/6\in\mathbb Q$ が**一意**に (2.-3) を実現する。さらに
> - **モニック性を保つ**(最高次係数は平行移動で不変)。
> - **$\infty_\pm$ のラベルを保つ**: $x'=x-e$ とすると $x/x'\to1$($x\to\infty$)ゆえ $y/x'^3 = (y/x^3)(x/x')^3\to y/x^3$ の符号は不変。したがって「$y\sim+x^3$ の枝 $=\infty_+ = P_\infty$」という M1 の定義は平行移動後も同じ点を指す。
> - **M2 の残余群と両立する**: 平行移動は (2.-3) で**完全に使い切られる**($e\ne0$ なら $B_5$ が $6e\ne0$ になる)。残るのは M2 の表の (N) 行そのもの($x\mapsto tx,\ y\mapsto t^3y$)であり、これは $B_5=0$ を保つ($B_5\mapsto B_5/t=0$)。**ゆえに M2–M5 は (N$_{\rm aff}$) と (N$_\infty$) で完全に共通**である。
> - **$A\ne0$(§2.4 の前提)は滑らかさから従う**: $B_0=\cdots=B_5=0$ なら $f_6=x^6$ は平方因子を持ち $C$ が非特異でない。よって係数ベクトルは零でない。
>
> **注(規約の選択について)**: (2.-3) は「代数的に一意・整数演算のみ・$P_0$ の座標を使わない」という三条件を満たす最も単純な規約として採る。**他の規約に後から差し替えない**(§0.2-3)。

**M2(残余群・重み)**: M1 のあと残る座標変換と、それが係数に与える**重み**を次で固定する。

| 枝 | 係数の並び | 残余変換 | 係数の変換則 | 重み $w_j$ |
|---|---|---|---|---|
| **(W)** | $f_5 = x^5+\sum_{j=0}^{4}A_jx^j$ | $x\mapsto\tau^2x,\ y\mapsto\tau^5y$($\tau\in\mathbb Q^\times$) | $A_j\mapsto A_j/\tau^{2(5-j)}$ | $w_j := 2(5-j)\in\{10,8,6,4,2\}$ |
| **(N)** | $f_6 = x^6+\sum_{j=0}^{5}B_jx^j$ | $x\mapsto tx,\ y\mapsto t^3y$($t\in\mathbb Q^\times$) | $B_j\mapsto B_j/t^{6-j}$ | $w_j := 6-j\in\{6,5,4,3,2,1\}$ |

以下、両枝を統一して**係数ベクトル** $A = (A_j)_{j\in J}$($J$ は**主係数を除く**添字集合)、群作用を

$$ (\sigma\cdot A)_j\ :=\ A_j/\sigma^{w_j}\qquad(\sigma\in\mathbb Q^\times) \tag{2.0} $$

と書く(枝 (W) では $\sigma=\tau$、枝 (N) では $\sigma=t$)。**主係数の重みは $w=0$** なので M2 は主係数を動かさない — これが M1 のモニック性が M2 で保たれる理由であり、同時に主係数を $J$ から**除かねばならない**理由である($w_j$ で割るため $w_j\ge1$ が要る)。枝 (W) では群の元は $\alpha=\tau^2\in\mathbb Q^{\times2}$ であり、$w_j$ が偶数なので $\sigma^{w_j}=(\sigma^2)^{(5-j)}$、すなわち (2.0) は常に**実在する群元**の作用である。

**M3(整数化・どの clearing でもよい)**: 任意の $\sigma_3\in\mathbb Q_{>0}$ で $A\mapsto\sigma_3\cdot A$ とし、全係数を $\mathbb Z$ に入れる。

> **既定手続き(実装が迷わないため)**: $A_j$ の分母の最小公倍数を $D$ とし $\sigma_3 := 1/D$ を取る。$w_j\ge1$ ゆえ $v_p(A_j)+w_jv_p(D)\ \ge\ v_p(A_j)+v_p(D)\ \ge\ 0$ で必ず整数化する。**これは過剰 clearing でよい** — M4 が同じだけ戻す(補題 R1-N1)。

**M4(weighted-primitive 正規化・total algorithm)**: 入力は M3 の出力(零ベクトルでない整数ベクトル)。ただし以下は**任意の有理係数ベクトルに対して定義される**(それが R1-N1 の内容)。

1. $S(A) := \{\,p\ \text{素数}\ :\ \exists j\in J,\ A_j\ne0,\ v_p(A_j)\ne0\,\}$ — $A_j$ の分子・分母の素因数分解から決まる**有限集合**。
2. 各素数 $p$ について
   $$ k_p(A)\ :=\ \min_{\substack{j\in J\\ A_j\ne 0}}\ \left\lfloor\frac{v_p(A_j)}{w_j}\right\rfloor\qquad(\textbf{零係数は min から除外}). \tag{2.1} $$
   $p\notin S(A)$ なら $k_p(A)=0$。
3. $\displaystyle \tau_+(A)\ :=\ \prod_{p\in S(A)}p^{\,k_p(A)}\ \in\ \mathbb Q_{>0}$。
4. **出力** $\ \mathrm{wp}(A)\ :=\ \tau_+(A)\cdot A$、すなわち
   $$ \boxed{\ A_j\ \longmapsto\ A_j\big/\tau_+(A)^{\,w_j}\ }\qquad(j\in J). \tag{2.2} $$
5. **符号単元 $\sigma=-1$ は M4 で扱わない** — M5(§3.2)へ回す。

$\mathrm{wp}(A)$ は**整数ベクトルであり、かつ weighted primitive**($\forall p:\ k_p(\mathrm{wp}(A))=0$)である(§2.4)。具体形は、枝 (W) が便 32 (2.1)、枝 (N) が便 32 (2.2) と一致する。

> **計算可能性と凍結記録**: $S(A)$ と $(k_p(A))_{p\in S(A)}$ は **値として**凍結記録に載せる(再現に因数分解の再実行を要求しない)。$v_p$ は整数演算のみ。**浮動小数点を使わない。**

**M5(全順序で一意化)**: §3。

**M6(一意性の検査)**: M5 が一意な候補を返さなければ **UNKNOWN 停止**(§9 U-a/U-b)。

### 2.3 (M-B) 整合検査(規則ではない・**第一次規則へ昇格しない**)

S5 設計の命題 S5-3(v1.1 で符号修理済み・$c_N$ 規約)が正しければ、枝 (W) のモデルは

$$ y^2\ =\ a(x)^2-c_N\,x^5\qquad(\deg a\le2),\qquad\text{gauge を統一すれば}\ c_N=-1\ \text{で}\quad y^2 = a(x)^2+x^5 $$

の形に一致するはずである($x_0=0$ は M1 で既に固定済。符号は `docs/week4-K5_S5設計_opus_v1.md` v1.1 §3.3 の $N=\mu\mu^\iota=a^2-b^2f=c_N(x-x_0)^5$ 規約に統一した — v1 の $+c_5$ は誤り。便 32 F4.4)。**一致しない場合でも Rule 1 は M-A に従う**(M-B は自己整合の警報にすぎない)。不一致は §11 に記録し、S5 設計の命題を疑う。

> **【裁定 31 / 便 32 F2.3】M-B を第一次規則へ昇格しない。** 理由は監査の順序ではなく **I-b 厳格版との両立不能**である: M-B を通常の Model-Builder 探索規則にすると、solver は $\lambda=c\mu^2$ の $c$ を明示変数として扱う。これは §9 I-b(**$c$ の平方類・平方因子・符号を凍結 2 前に計算・報告・選択に使うことの禁止**)と同時には運用できない。
>
> **M-B / $\mu$-正規形を discovery engine に使うなら**、全候補列挙・M-A canonicalization・両翼共同 freeze までを**人間から隔離した sealed automation** として、**別 schema に事前登録**すること(本 v1 の範囲外)。v1 では **M-A を正本**、**M-B を凍結 2 後の整合検査**に留める。

### 2.4 M3–M4 の正当化(便 32 F2.2 の要求)

記号は §2.2 の通り($J$・$w_j\ge1$・作用 (2.0)・$k_p$ (2.1)・$\mathrm{wp}$ (2.2))。$A\ne0$ とする。

> **補題 R1-N1(denominator clearing 非依存性).** 任意の $\sigma\in\mathbb Q_{>0}$ に対し
> $$ \boxed{\ \mathrm{wp}(\sigma\cdot A)\ =\ \mathrm{wp}(A).\ } $$

**証明.** $A_j\ne0$ なら $(\sigma\cdot A)_j\ne0$ でありその逆も真だから、(2.1) の min を取る添字集合 $\{j: A_j\ne0\}$ は $\sigma$ 作用で**不変**である。各 $j$ につき $v_p((\sigma\cdot A)_j) = v_p(A_j)-w_j\,v_p(\sigma)$、そして $v_p(\sigma)\in\mathbb Z$ なので floor の外へ出せる:

$$ \left\lfloor\frac{v_p((\sigma\cdot A)_j)}{w_j}\right\rfloor = \left\lfloor\frac{v_p(A_j)}{w_j}-v_p(\sigma)\right\rfloor = \left\lfloor\frac{v_p(A_j)}{w_j}\right\rfloor-v_p(\sigma). $$

min を取って $k_p(\sigma\cdot A) = k_p(A)-v_p(\sigma)$(全素数で)、すなわち正の有理数として $\tau_+(\sigma\cdot A) = \tau_+(A)/\sigma$。よって

$$ \mathrm{wp}(\sigma\cdot A)_j\ =\ \frac{A_j/\sigma^{w_j}}{\bigl(\tau_+(A)/\sigma\bigr)^{w_j}}\ =\ \frac{A_j}{\tau_+(A)^{w_j}}\ =\ \mathrm{wp}(A)_j. \qquad\blacksquare $$

**系 R1-N1a.** M3 でどれだけ余分に denominator を clear しても、M4 の出力は同一である。すなわち **$\mathrm{M4}\circ\mathrm{M3}$ は M3 の選択に依らず、元の有理係数ベクトル $A$ の関数 $\mathrm{wp}(A)$ である。** とくに $\mathrm{wp}$ は M2 の**正部分** $\mathbb Q_{>0}$ の軌道上の定数であり、$k_p(\mathrm{wp}(A))=k_p(A)-k_p(A)=0$ から $\mathrm{wp}\circ\mathrm{wp}=\mathrm{wp}$(冪等)。また $k_p(\mathrm{wp}(A))=0\ (\forall p)$ は $\mathrm{wp}(A)$ の**整数性**も含む(下記の同値による)。

> **補題 R1-N2(残余は符号単元のみ ⇒ 有限性).** $A$ を整数かつ weighted primitive(すなわち $\forall p:\ k_p(A)=0$)とする。$\sigma\in\mathbb Q^\times$ に対し
> $$ \sigma\cdot A\ \text{が再び整数かつ weighted primitive}\quad\Longleftrightarrow\quad \sigma=\pm1. $$

**証明.** まず $w_j\ge1>0$ より、任意の有理係数ベクトル $B$ について

$$ B\ \text{が整数}\ \iff\ \forall p,j:\ v_p(B_j)\ge0\ \iff\ \forall p:\ k_p(B)\ge0 $$

(⇐ は $\lfloor v_p(B_j)/w_j\rfloor\ge k_p(B)\ge0\Rightarrow v_p(B_j)\ge0$)。R1-N1 の計算より $k_p(\sigma\cdot A) = k_p(A)-v_p(\sigma) = -v_p(\sigma)$。したがって

- 整数性 $\iff\forall p:\ -v_p(\sigma)\ge0$、
- weighted primitive $\iff\forall p:\ -v_p(\sigma)=0$。

後者は $\forall p:v_p(\sigma)=0$、すなわち $\sigma=\pm1$。逆に $\sigma=\pm1$ なら $v_p(\sigma)=0$ で両条件を保つ。$\blacksquare$

**系 R1-N2a(§3.1 の有限性).** M1 正規形の一つの同値類内では、候補は M2 群 $\cong\mathbb Q^\times$ の**一軌道**である。M3+M4 を経た候補集合はその軌道のうち「整数かつ weighted primitive」なもの全体であり、R1-N2 によりそれは $\{\pm1\}\cdot\mathrm{wp}(A)$、すなわち**高々 2 個**。**有限性は証明された。** さらに

- 枝 (W): $w_j$ が偶数ゆえ $(-1)\cdot A = A$ ⇒ **係数ベクトルは 1 個**($\sigma=-1$ は $y\mapsto-y$ としてのみ効き、§4.1 で処理)。
- 枝 (N): $((-1)\cdot B)_j = B_j/(-1)^{6-j} = (-1)^jB_j$ ⇒ **係数ベクトルは高々 2 個**(§3.2 の tie-break が受け持つ)。

> **検算(単系統・整数演算)**: `search/wp-check.mjs`(node・BigInt 有理数・司令塔再走で 11649/0 再現)。無作為な有理係数ベクトル 400 組 × 2 枝に対し、(i) 無作為な $\sigma\in\mathbb Q_{>0}$ 6 通りでの R1-N1、(ii) 既定手続き($\sigma_3=1/\mathrm{lcm}$)での整数化と wp 一致、(iii) 出力の整数性・weighted primitivity・冪等性、(iv) $\sigma\ne\pm1$ での安定化の破れと $\sigma=-1$ での保存 — **計 11649 検査すべて一致・失敗 0**。符号作用も $(W)$ で不変・$(N)$ で $(-1)^j$ を確認。**入力は無作為な有理数のみで、曲線・$\lambda$・$u$ のデータを含まない。**

---

## Q3 → §3. 全順序と tie-break

### 3.1 有限性(**証明済み** — v1.1)

$$ \boxed{\text{M4 のあと残る候補集合が\textbf{有限}であることを、最小化の前に証明する。}} $$

有限でない(または有限性を証明できない)なら最小元は存在しないかもしれないので、**即 UNKNOWN 停止**(U-b)。

**この義務は v1.1 で履行された。** §2.4 の**補題 R1-N2**(残余 $=\{\pm1\}$)と**系 R1-N2a** により:

- 枝 (W): $\tau\mapsto-\tau$ は $A_j\mapsto A_j/(-1)^{2(5-j)} = A_j$ で係数に作用しない(作用は $y\mapsto-y$ のみ — §4 へ回る)。M3+M4 のあと $\tau\in\{\pm1\}$ ゆえ**候補は 1 個**。
- 枝 (N): $t\mapsto-t$ は $B_j\mapsto(-1)^{j}B_j$ で**係数を実際に動かす**。M3+M4 のあと $t\in\{\pm1\}$ ゆえ**候補は 2 個** ⇒ tie-break が要る(§3.2)。

**U-b は札として存続する**(fail-closed)。v1 では「有限性が未証明だから U-b が発火しうる」状態だったが、v1.1 以降は M1 が想定した正規形に**入らなかった**場合(例: $\deg f\notin\{5,6\}$、主係数がモニックにならない、$J$ の重みが (2.0) と異なる)にのみ発火する。**v1.2 の副枝 (N$_\infty$) はこの点を変えない** — M2 の残余群も重みも (N) 行のままだから、R1-N2 とその系はそのまま適用される($B_5=0$ は零成分として (2.1) の min から除かれるだけ)。**R1-N2 の前提($w_j\ge1$ の重み付き $\mathbb Q^\times$-作用・一軌道)が成り立たない入力を受け取ったら、規則を延長せずに U-b で止める。**

### 3.2 全順序

$\mathbb Z$ に全順序
$$ 0\ \prec\ -1\ \prec\ 1\ \prec\ -2\ \prec\ 2\ \prec\ -3\ \prec\ \cdots\qquad(\text{絶対値優先・同値なら負が先}) $$
を入れる。モデルの鍵を

$$ \kappa(\text{model}) := \Bigl(\ \lvert\operatorname{disc}\rvert,\ \ (\text{係数ベクトルを高次から低次へ並べたもの})\ \Bigr) $$

とし、第一成分は通常の $\mathbb Z_{\ge0}$ の順、第二成分は $\prec$ の**辞書式**で比較する。**最小のものを取る。**

- 枝 (N) の 2 候補は $\operatorname{disc}$ が等しいので第二成分で決まる。$b_j\mapsto(-1)^jb_j$ ゆえ、$(b_5,b_3,b_1)$ のうち**最初の非零成分が正**になる方を取る。すべて零なら $f_6$ は偶関数で $t\mapsto-t$ が真の自己同型 ⇒ **候補は 1 個**(曖昧さ消滅)。
  - **(v1.2) 副枝 (N$_\infty$) では M1 (2.-3) により $b_5=0$** なので、この規則は実質 $(b_3,b_1)$ の最初の非零成分で決まる。**規則の文言は変更しない**(零成分を飛ばすのは元の規則の内容である)。$b_5=b_3=b_1=0$ の場合の扱いも上の通り。

### 3.3 「最小係数」型のアルゴリズムを名指しで禁止する

> **禁止**: 「reduction algorithm が返した最小モデル」「CAS の `reduce`/`minimize` の出力」を**アルゴリズム名と版を書かずに**採用すること。それは数学的不変量ではない。
> **許可**: §3.2 のように**純粋に算術的な全順序**を書き下し、任意の実装が再現できる形にすること。外部アルゴリズムを使う場合は、その出力を §3.2 の順序で**再検証**する(出力が最小でなければ、順序に従って修正する)。

---

## Q4 → §4. $y\mapsto-y$・Möbius・sheet numbering の tie-break

### 4.1 $y\mapsto-y$

$y\mapsto-y$ は超楕円対合 $\iota$ の座標表示である。**印付きデータ $(C,P_0,P_\infty,\lambda)$ に対しては、多くの場合そもそも自由度でない。**

| 状況 | $y\mapsto-y$ の効果 | 規則 |
|---|---|---|
| 枝 (N)($P_\infty$ 非 Weierstrass) | $\infty_+\leftrightarrow\infty_-$ を入れ替える | **$P_\infty = \infty_+$ の定義(M1)で固定済**。自由度なし(**副枝 (N$_\infty$) では同時に $P_0=\infty_-$ と $P_\infty$ を入れ替えるので、なおさら自由度でない** — v1.2) |
| 枝 (W) かつ $y(P_0)\ne0$ | $P_0 = (0,y_0)\mapsto(0,-y_0)$ — **別の点** | **$y(P_0)$ が正になる符号**を取る($y_0\in\mathbb Q^\times$ なので判定可能)。自由度なし |
| 枝 (W) かつ $y(P_0)=0$($P_0$ も Weierstrass) | $P_0,P_\infty$ をともに固定し、$\lambda\mapsto\lambda\circ\iota\ne\lambda$ | **真の 2 択**。下記 |

**$P_0$ も Weierstrass の場合の規則**: $\iota$ は印付き被覆の同型 $(C,\lambda\circ\iota)\xrightarrow{\sim}(C,\lambda)$ を与えるので、**§5 の uniformizer 規則が $\iota$-同変である限り $u$ は同じ**($t=y\mapsto-y$ で $u\mapsto u\cdot(-1)^{10}=u$)。ゆえに数学的曖昧さはない。再現性のためだけに tie-break を置く:
$$ \lambda = A(x)+B(x)y\ \text{と書いたとき、}\ B\ \text{の係数ベクトルが §3.2 の順序で小さい方の}\ \lambda\ \text{を取る}. $$

> **S5 設計 §3.3 の帰結(参考・依存しない)**: 枝 (W) では $P_0$ は自動的に非 Weierstrass になる。**直接証明**(便 32 F4.4 末尾の形・v1.1 で差替え): 命題 S5-3 の正規形 $b_0^2f_5 = a(x)^2-c_N(x-x_0)^5$($b_0\in\mathbb Q^\times$)で $a(x_0)=0$ とすると $(x-x_0)\mid a$、ゆえに $(x-x_0)^2\mid a^2$ かつ $(x-x_0)^2\mid(x-x_0)^5$ で $(x-x_0)^2\mid f_5$。**$f_5$ が $x_0$ で二重根をもつので $C:y^2=f_5$ は滑らかでない** — 種数 2 の非特異曲線という前提に反する。ゆえに $a(x_0)\ne0$、すなわち $y(P_0)=-a(x_0)/b_0\ne0$ で $P_0$ は非 Weierstrass。∎(S5 設計 v1.1 補題 S5-W) したがってこの行は**枝 (N) でのみ発火する見込み**である。ただし Rule 1 は S5 設計に依存しないので、両方書いておく。
>
> **(v1.2 の絞り込み)**: さらに副枝 (N$_\infty$) では $P_0=\iota(P_\infty)$ が $\iota$ の不動点でない(補題 R1-M0 3.)ので $P_0$ は非 Weierstrass。**「$P_0$ も Weierstrass」の場合が発火しうるのは副枝 (N$_{\rm aff}$) だけ**である(S5 設計に依存しない結論)。

### 4.2 Möbius

- **底 $\mathbf P^1_\lambda$**: 自由度**なし**(§2.1)。
- **源の $x$-直線**: $x(P_\infty)=\infty$ を課した時点で残るのは affine 変換 $x\mapsto tx+e$ のみであり、それを M1 と M2–M5 で**使い切っている**。追加の Möbius は使わない。
  - 枝 (W) / 副枝 (N$_{\rm aff}$): 平行移動 $e$ は $x(P_0)=0$ が、スケール $t$ は M2–M5 が使い切る。
  - **副枝 (N$_\infty$)(v1.2)**: $P_0$ も $x=\infty$ の上にあるので $e$ に条件を与えない。代わりに **$B_5=0$**(M1 (2.-3))が $e$ を使い切る。スケール $t$ は従来どおり M2–M5。**自由度の数(1+1)は両副枝で同じ**である。

### 4.3 sheet numbering

> **補題 R1-U.** $\operatorname{Aut}(W_0/U)=1$ ゆえ
> $$ C_{S_{10}}\bigl(\operatorname{Mon}\bigr)\ \cong\ N_{\operatorname{Mon}}(\text{点安定化群})/(\text{点安定化群})\ =\ N_{G_5}(H)/H\ =\ 1 . $$
> したがって、幾何 fiber $\operatorname{Fib}_{\vec{01}}(W_0)$ と $\Lambda_i$ の間の、monodromy を intertwine する全単射 $c_i$ は **ちょうど一つ**。

$$ \Longrightarrow\qquad \boxed{\text{sheet numbering に tie-break は不要。}\ c_i\ \text{は一意である。}} \tag{4.1} $$

**もし実装が 2 個以上の intertwiner を返したら**、それは補題 R1-U に反するので**入力が壊れている** ⇒ **integrity stop**(§9 I-f)。UNKNOWN ではない。

---

## Q5 → §5. $u$ を使わない uniformizer 決定アルゴリズム

### 5.0 底側の局所助変数は選択の対象ではない

$\lambda=0$ における底の局所助変数は **$\lambda$ 自身**である($0,1,\infty$ が印付きなので $\lambda$ に自由度がない — §2.1)。**選ぶのは源の $P_0$ における $t$ だけ。**

### 5.1 Rule U-1(実務規則・超楕円座標)

$$ \boxed{\ t := \begin{cases} x - x(P_0)\ (= x,\ \text{M1 で}\ x(P_0)=0) & P_0\ \text{アフィンかつ}\ f(x(P_0))\ne0\quad(P_0\ \text{非 Weierstrass}) \\[2pt] y & P_0\ \text{アフィンかつ}\ f(x(P_0))=0\quad(P_0\ \text{Weierstrass}) \\[2pt] 1/x & P_0 = \infty_-\quad(\textbf{副枝 (N}_\infty\textbf{)}\ \text{— v1.2 で新設}) \end{cases}\ } \tag{5.1} $$

**根拠(v1.2 で修理)**:

- **アフィンの二行**(枝 (W) と副枝 (N$_{\rm aff}$)): $P_0$ 非 Weierstrass なら $\operatorname{ord}_{P_0}(x-x_0)=1$;Weierstrass なら $\operatorname{ord}_{P_0}(x-x_0)=2$ かつ $\operatorname{ord}_{P_0}(y)=1$。
- **第三行**(副枝 (N$_\infty$)): 補題 R1-U∞ 2.。
- **場合分けの網羅性**: 補題 R1-U∞ 3./4.(「$P_0$ がアフィンか無限遠か」は M0 の判定 (2.-1) で**先に決まっている**)。

> **【v1.1 の誤り・便 34 F2.3 で指摘・撤回】** v1.1 の根拠行にあった
> $$ \text{「}P_0\ne P_\infty\ \text{ゆえ}\ x(P_0)\ \text{は有限で、無限遠の場合分けは不要」} $$
> は**枝 (N) では偽**である。六次モデルの無限遠点は $\infty_+,\infty_-$ の二つあり、$P_0=\infty_-=\iota(P_\infty)$ は $P_0\ne P_\infty$ と両立するからである。この文は削除し、下の補題 R1-U∞ 3./4. で置き換える。**この誤りは枝 (W) でのみ真であった主張を枝 (N) へ不当に一般化したものである。**

> **補題 R1-U∞($\infty_\pm$ の局所構造と uniformizer).**
> **1.(枝 (N) の無限遠チャート)** M1 の正規化モデル($f_6$ モニック・$P_\infty=\infty_+$)で
> $$ s := 1/x,\qquad w := y/x^3\ (=ys^3) $$
> と置くと、$C$ の $x=\infty$ の近傍はアフィン曲線
> $$ w^2 = F(s) := s^6f_6(1/s) = 1 + B_5s + B_4s^2 + B_3s^3 + B_2s^4 + B_1s^5 + B_0s^6\ \in\mathbb Q[s] \tag{5.1a} $$
> で与えられ、$\boxed{F(0)=1\ne0}$。したがって $x^{-1}(\infty)$ は**相異なる二点**
> $$ \infty_+ = (s,w)=(0,+1) = P_\infty,\qquad \infty_- = (s,w)=(0,-1) = \iota(P_\infty) $$
> から成り、$x$ は $\infty$ の上で**不分岐**。両点で
> $$ \operatorname{ord}_{\infty_\pm}(s) = 1,\qquad \operatorname{ord}_{\infty_\pm}(w) = 0,\qquad \operatorname{ord}_{\infty_\pm}(x) = -1,\qquad \operatorname{ord}_{\infty_\pm}(y) = -3 . $$
> **2.($P_0=\infty_-$ での uniformizer)** $\boxed{t := 1/x = s\ \text{は}\ P_0=\infty_-\ \text{の uniformizer}}$($\operatorname{ord}_{P_0}(1/x)=1$)であり、$\mathbb Q$-有理。他方
> $$ \boxed{\ y/x^3 = w\ \text{は}\ P_0\ \text{で単元}(\text{値}\ -1)\ \text{であって uniformizer ではない}.\ } $$
> **3.(枝 (W) では $P_0$ は必ずアフィン)** $\deg f=5$ のモデルでは $x^{-1}(\infty)$ は**一点** $P_\infty$(分岐指数 2 の Weierstrass 点)だから、$P_0\ne P_\infty$ ならば $P_0$ はアフィン点であり $x(P_0)\in\mathbb Q$。
> **4.(枝 (N) での正しい場合分け)** 枝 (N) では
> $$ P_0\ \text{が無限遠}\iff P_0\in\{\infty_+,\infty_-\}\iff P_0=\infty_-=\iota(P_\infty)\iff \textbf{副枝 (N}_\infty\textbf{)} $$
> ($P_0\ne P_\infty=\infty_+$ による)。すなわち**アフィン/無限遠の二択は M0 の (2.-1) と完全に一致する。**
>
> **証明.** 1. $f_6$ がモニックだから $F(s)=s^6f_6(1/s)$ は $\mathbb Q[s]$ の元で $F(0)=\mathrm{lc}(f_6)=1$。$(s,w)$ は $x\ne0$ 上のアフィンチャートを与え($x=1/s,\ y=w/s^3$)、方程式 $y^2=f_6(x)$ は両辺に $s^6$ を掛けて (5.1a) になる。$F(0)=1\ne0$ ゆえ $s=0$ 上の点は $w=\pm1$ の二点で、$\partial(w^2-F)/\partial w = 2w = \pm2\ne0$ だから $s$ は両点で局所助変数(陰関数定理/完備局所環 $\mathbb Q[[s]]$ 上で $w$ が一意に解ける)。よって $\operatorname{ord}_{\infty_\pm}(s)=1$。$w(\infty_\pm)=\pm1\ne0$ から $\operatorname{ord}(w)=0$、$x=1/s$ と $y=w/s^3$ から残りの二式。$\infty_+$($y\sim+x^3$ すなわち $w\to+1$)が M1 の定義で $P_\infty$、$\iota:(x,y)\mapsto(x,-y)$ が $(s,w)\mapsto(s,-w)$ ゆえ $\iota(\infty_+)=\infty_-$。
> 2. 1. より直ちに従う($1/x=s$)。$1/x\in\mathbb Q(C)$ は $\mathbb Q$-有理。
> 3. $y^2=f_5(x)$ の無限遠を $s=1/x,\ v=y/x^3$ で見ると $v^2 = s\,F_5(s)$、$F_5(s):=s^5f_5(1/s)$、$F_5(0)=\mathrm{lc}(f_5)\ne0$。ゆえに $s=0$ 上の点は $v=0$ の**一点のみ**で、そこで $\operatorname{ord}(v)=1,\ \operatorname{ord}(s)=2$、すなわち分岐指数 2(Weierstrass 点)。よって $x^{-1}(\infty)=\{P_\infty\}$。
> 4. 1. と $P_0\ne P_\infty$ から。$\blacksquare$

**$t$ は $\mathbb Q$-有理**である(三つの場合すべて)。したがって §5.4 の観測 R1-C(Kummer class の uniformizer 非依存性)は副枝 (N$_\infty$) でもそのまま適用される。

> **注(なぜ $1/x$ であって $y/x^4$ ではないか)**: $y/x^4=ws$ も $\operatorname{ord}_{P_0}=1$ をもつので uniformizer である。**規則は最も単純な $1/x$ を正本として固定する**(§0.2-3: 後から一意化のために規則を変えない)。生の $u$ は $t$ の取り方に依存するので、**経路 A と経路 B は必ずこの同じ $t=1/x$ を使う**(§6・R1-C は $[u]_{10}$ の不変性しか与えない)。

### 5.2 Rule U-2(モデル非依存の仕様・Riemann–Roch)

U-1 は超楕円座標に依存する。モデル非依存の仕様を併記し、**両者が一致することを検査する**(U-3)。U-2 は**検査路**であって launch blocker ではない(便 32 F2.1)が、再現可能でなければ検査にならないので、v1.1 で ambient と単項式順序を値として固定する。

#### 5.2.0 ambient と単項式順序(v1.1 で明記・便 32 F2.1)

$C$ のアフィン座標環を $R := \mathbb Q[x,y]/(y^2-f(x))$ とする。$R$ の $\mathbb Q$-基底は単項式 $x^ay^b$($a\in\mathbb Z_{\ge0},\ b\in\{0,1\}$)。$P_\infty$ での極位数を $\operatorname{pol}(x^ay^b) := -\operatorname{ord}_{P_\infty}(x^ay^b)$ と書く。

| 枝 | $\operatorname{ord}_{P_\infty}(x),\ \operatorname{ord}_{P_\infty}(y)$ | $\operatorname{pol}(x^ay^b)$ | ambient $\mathcal A(n)$ | 同値 |
|---|---|---|---|---|
| **(W)** | $-2,\ -5$ | $2a+5b$ | $\operatorname{span}_{\mathbb Q}\{x^ay^b:\ b\in\{0,1\},\ 2a+5b\le n\}$ | $=L(nP_\infty)$ |
| **(N)** | $-1,\ -3$ | $a+3b$ | $\operatorname{span}_{\mathbb Q}\{x^ay^b:\ b\in\{0,1\},\ a+3b\le n\}$ | $=L(n\infty_++n\infty_-)$($\dim=2n-1$、$n\ge3$) |

枝 (N) では $x^ay^b$ は $\infty_+$ と $\infty_-$ の**両方**に極をもつので $\mathcal A(n)\ne L(nP_\infty)$ である。この場合

$$ L(n P_\infty)\ =\ L(n\infty_+)\ =\ \{\,g\in\mathcal A(n)\ :\ \operatorname{ord}_{\infty_-}(g)\ge0\,\} $$

は $\mathcal A(n)$ の**線型部分空間**($\infty_-$ での局所展開の主要部が消える、という $\mathbb Q$-線型条件)であり、局所展開は厳密に(冪級数の切断で)計算する。

$$ \boxed{\ \textbf{単項式順序(固定)}:\quad x^ay^b\ \prec\ x^{a'}y^{b'}\ :\Longleftrightarrow\ \bigl(\operatorname{pol},\,b,\,a\bigr)\ <_{\rm lex}\ \bigl(\operatorname{pol}',\,b',\,a'\bigr)\quad(\text{三成分とも昇順}).\ } \tag{5.2} $$

- 枝 (W) では $\operatorname{pol}=2a+5b$ が $b=0$ で偶数・$b=1$ で奇数($\ge5$)ゆえ**すべて相異なる**。第一成分だけで順序が確定し、tie-break $(b,a)$ は発火しない。
- 枝 (N) では $\operatorname{pol}=a+3b$ が同値になりうる(例: $x^3$ と $y$ はともに $3$)ので $(b,a)$ が実際に効く。(5.2) は $x^3\prec y$ を意味する。

$\mathcal A(n)$ の単項式を (5.2) の昇順に並べた列を $(m_1\prec\cdots\prec m_N)$ とし、$g=\sum c_{a,b}x^ay^b\in\mathcal A(n)$ の **ambient coefficient vector** を

$$ \operatorname{vec}(g)\ :=\ \bigl(c_{m_1},\,c_{m_2},\,\dots,\,c_{m_N}\bigr)\ \in\ \mathbb Q^N \tag{5.3} $$

と定める。**RREF はこの $\operatorname{vec}$ を行に並べた行列に対し、列を $m_1,\dots,m_N$ の順(左端が $m_1$)として取る**(pivot は最左優先)。RREF は部分空間と列順序だけで決まるので**一意**である。

#### 5.2.1 手順

1. $n_0 := \min\{\,n\ge1\ :\ \ell(nP_\infty-P_0) > \ell(nP_\infty-2P_0)\,\}$ を計算する(有限:$n\ge5$ なら $\deg(nP_\infty-2P_0)=n-2\ge3=2g-1$ で両者非特殊、$\ell$ は $n-2$ と $n-3$ で必ず相異なる。ゆえに $n_0\le5$)。
2. **対象空間**を $V := L(n_0P_\infty-P_0)\subseteq\mathcal A(n_0)$ とする(v1.1 修理: v1 は $L(n_0P_\infty)$ と書いていたが、それでは 4. の存在が保証されない)。$V$ は $\mathcal A(n_0)$ 内の線型条件で切り出す。**切り出す条件は枝によって次のとおり**(v1.2 で副枝を明示):

   | 枝 | $V=L(n_0P_\infty-P_0)$ を切り出す線型条件 |
   |---|---|
   | **(W)** | $g(P_0)=0$($P_0$ アフィン。$\mathcal A(n_0)=L(n_0P_\infty)$ なので他に条件なし) |
   | **(N$_{\rm aff}$)** | $g(P_0)=0$($P_0$ アフィン)**かつ** $\operatorname{ord}_{\infty_-}(g)\ge0$($\infty_-$ での正則性) |
   | **(N$_\infty$)** | $\boxed{\operatorname{ord}_{\infty_-}(g)\ge1}$ の**一本のみ**($P_0=\infty_-$ なので「$\infty_-$ での正則性」と「$P_0$ での消滅」が一本の位数条件に融合する。**アフィン条件は存在しない**) |

   いずれも $\infty_-$ における局所展開(補題 R1-U∞ 1. のチャート $(s,w)$、$w=-W$)の**切断係数に対する $\mathbb Q$-線型条件**であり、厳密に計算する(浮動小数点を使わない)。$L(n_0P_\infty-P_0)\subseteq\mathcal A(n_0)$ は (N$_\infty$) でも成立する($\operatorname{ord}_{\infty_-}\ge1\ge-n_0$)。
3. $V$ の任意の生成系の $\operatorname{vec}$ を行に並べ、(5.3) の列順序で **reduced row echelon form**(一意)を取る。得られた行を pivot 列の添字の昇順に $g_1,\dots,g_r$ と番号づける。
4. $\operatorname{ord}_{P_0}(g_i)=1$ を満たす $i$ のうち **最小のもの**を取り、$t_0 := g_i$ とする。
   **存在**: $\ell(n_0P_\infty-P_0)>\ell(n_0P_\infty-2P_0)$ なので、$V$ の**どの**基底にも $\operatorname{ord}_{P_0}=1$ の元が少なくとも一つある(全て $\operatorname{ord}_{P_0}\ge2$ なら $V\subseteq L(n_0P_\infty-2P_0)$ となり次元が矛盾)。存在しない出力が返ったら**入力破損 ⇒ integrity stop**(§9 I-e)。
   **(v1.2)** 副枝 (N$_\infty$) では $\operatorname{ord}_{P_0}=\operatorname{ord}_{\infty_-}$ を 2. と同じ $(s,w)$ 展開から読む(新しい機構は不要)。1. の $n_0\le5$ の証明と上の存在証明は $P_0,P_\infty$ が相異なる点であることしか使っていないので、**両副枝で verbatim に成立する**。
5. $\boxed{t := t_0}$ — **再スケールしない。**

> **禁止(明示)**: $\lambda/t^{10}$ の定数項が $1$ になるように $t$ をスケールすること、および $\lambda$ の局所展開から計算した任意の量で $t$ をスケールすること。**それが $u$ である。**

### 5.3 Rule U-3(整合検査)

U-1 の $t$ と U-2 の $t_0$ は $t_0 = \varepsilon\,t\,(1+O(t))$、$\varepsilon\in\mathbb Q^\times$ を満たすはずである。$\varepsilon$ を記録する。**$\varepsilon\notin\mathbb Q^\times$、または一方が uniformizer でない ⇒ integrity stop**(§9 I-e)。

> **(v1.2) 副枝 (N$_\infty$) での注意**: この副枝では U-1 の $t=1/x$ は**どの $\mathcal A(n)$ にも属さない**($1/x$ は $x=0$ の上の二点に極をもつ)。したがって $t$ と $t_0$ は関数として別物であり、$t_0/t$ を多項式環の中で比較することはできない。**U-3 は両者を $P_0$ の局所助変数として比較する規則である** — すなわち $\operatorname{ord}_{P_0}(t)=\operatorname{ord}_{P_0}(t_0)=1$ を確認し、$\varepsilon := \lim_{P\to P_0}(t_0/t)\in\mathbb Q^\times$ を $(s,w)$ 展開の主要係数として読む。$\mathbb Q$-有理な二つの uniformizer だから $\varepsilon\in\mathbb Q^\times$ は自動であり、破れは入力破損(I-e)。**正本が U-1 であることも不変**。

**正本は U-1** とする(実装が単純で監査しやすい)。U-2 は仕様と検査。

### 5.4 ★ なぜ規則を緩めないか(緩めてよい理由があるのに)

> **観測 R1-C.** $t,t'$ がともに $K$-有理な $P_0$ の uniformizer なら $t' = ct(1+O(t))$、$c\in K^\times$、したがって $u\mapsto uc^{-10}$。ゆえに
> $$ \boxed{\ [u]_{10}\in K^\times/K^{\times10}\ \text{は}\ K\text{-有理 uniformizer の取り方に依らない}.\ } $$

すなわち**封印予測 (P1)(P2) は uniformizer の選択に影響されない**(manifest の covariance control 2 と同じ内容)。

**それでも §5 の規則を緩めない理由は二つ**:
1. **生の $u$** は二経路突合(§6)の対象であり、経路間で同じ $t$ を使わなければ比較にならない。
2. 「$K$-有理」という条件自体が規則を要する。アルゴリズムが非有理な $t$ を返せば類も動く。

---

## §6. $u$ の二経路(数式・実装版・受理規則)

$$ \lambda\ =\ u\,t^{10}\,\bigl(1+O(t)\bigr)\quad\text{at }P_0,\qquad u\in K^\times\ (\text{実は}\ \mathbb Q^\times). $$

### 6.1 経路 A(cusp 展開)

**(a) $P_0$ がアフィンの場合(枝 (W)・副枝 (N$_{\rm aff}$))**

1. モデルの定義方程式を $P_0$ で Hensel/Newton 持ち上げし、$K[[t]]$ の中で $x,y$ の展開を精度 $t^{13}$ まで**厳密に**求める。
2. $\lambda = A(x)+B(x)y$ に代入し、$\lambda = \sum_{k\ge10}u_kt^k$ を得る。
3. $\boxed{u^{(A)} := u_{10}}$。$u_{10},\dots,u_{13}$ を**生出力として別保存**する。
4. 検査: $u_k = 0$($k<10$)を厳密に確認。破れたら integrity stop。

**(b) 副枝 (N$_\infty$)($P_0=\infty_-$・$t=1/x$)— v1.2 で新設**

この副枝では $x,y$ が $P_0$ で**極**をもつので、$x,y$ を $K[[t]]$ の中で展開することはできない($x=1/s\notin\mathbb Q[[s]]$)。展開の場を補題 R1-U∞ 1. の $(s,w)$ チャートへ移す。**用いる局所助変数は U-1 と同じ $t=s=1/x$**(経路 B と共通 — §5.1 の注)。

- **A∞-1**: $W\in\mathbb Q[[s]]$ を $W^2=F(s)$((5.1a))かつ $W(0)=+1$ で Newton/Hensel 持ち上げにより厳密に求める($F(0)=1$ ゆえ一意)。**精度は $W \bmod s^{M+14}$**(下の $M$;$M=10$ なら $s^{23}$ の係数まで)。
- **A∞-2**: $M := \max(\deg A,\ \deg B+3)$ を**計算し**(仮定しない)、$\tilde A(s) := s^MA(1/s)$、$\tilde B(s) := s^{M-3}B(1/s)\in\mathbb Q[s]$ と置く。$P_0=\infty_-$ の枝は $w=-W$ だから
  $$ \lambda\ =\ s^{-M}\bigl(\tilde A(s)-W(s)\tilde B(s)\bigr)\ =:\ s^{-M}G_-(s). $$
- **A∞-3**: $\boxed{u^{(A)} := [s^{M+10}]\,G_-}$。$u_{10},\dots,u_{13} = [s^{M+10}],\dots,[s^{M+13}]\,G_-$ を**生出力として別保存**する。
- **A∞-4**: 検査: $[s^k]G_-=0$($k<M+10$)を厳密に確認(= $\operatorname{ord}_{P_0}\lambda=10$)。破れたら integrity stop。あわせて $M$ の実測値を生出力に記録する(補題 R1-B∞ 1. は $M=10$ を予言する — **経路 A はそれを仮定せず、独立に観測して突合に供する**)。

> **精度 $M+14$ の根拠**: $\operatorname{ord}_s\tilde B\ge0$ ゆえ $[s^k]G_-$ は $W$ の $s^{\le k}$ の係数だけに依存する。$u_{13}=[s^{M+13}]G_-$ に必要かつ十分なのは $W\bmod s^{M+14}$。アフィン枝の「精度 $t^{13}$」($t^{10}$ の 3 次先まで)と同じ情報量である。

**中間表現**: $K[[t]]$(切断冪級数;副枝 (N$_\infty$) では $\mathbb Q[[s]]$ の切断と $\lambda\in\mathbb Q((s))$)。

### 6.2 経路 B(Vieta / ノルム・**級数を使わない**)

$\lambda^\iota := \lambda\circ\iota = A(x)-B(x)y$、$N(\lambda) := \lambda\lambda^\iota = A^2-B^2f\in\mathbb Q[x]$ と置く($\lambda$ は $C$ のアフィン部分で正則だから $A,B\in\mathbb Q[x]$)。$\operatorname{div}(\lambda) = 10P_0-10P_\infty$ に $\iota$ を施して

$$ \operatorname{div}\bigl(N(\lambda)\bigr)\ =\ 10P_0+10\,\iota(P_0)-10P_\infty-10\,\iota(P_\infty). \tag{6.0} $$

**(6.0) の右辺は副枝によって形が変わる**(v1.2 で明示 — v1.1 はアフィンの場合しか書いていなかった):

| 枝 | (6.0) の帰結 | 適用する式 |
|---|---|---|
| **(W)**・**(N$_{\rm aff}$)**($P_0$ アフィン) | $N(\lambda)$ の $x_0:=x(P_0)$ における零位数は $10$ であり $\hat c := \bigl[N(\lambda)/(x-x_0)^{10}\bigr]_{x=x_0}\ne0$ | **B-i / B-ii** |
| **(N$_\infty$)**($P_0=\infty_-=\iota(P_\infty)$) | $\iota(P_0)=P_\infty,\ \iota(P_\infty)=P_0$ ゆえ $\operatorname{div}(N(\lambda))=0$、すなわち $N(\lambda)$ は**定数** $\hat c\in\mathbb Q^\times$。**$x_0$ は存在せず「零位数 10」も起こらない** | **B-iii(新設)** |

- **B-i($P_0$ がアフィンかつ非 Weierstrass・$t=x-x_0$)**: $\iota P_0\ne P_0$ かつ $\lambda^{-1}(0)=\{P_0\}$ ゆえ $\lambda^\iota(P_0)\ne0$(**$\iota P_0$ が $P_\infty$ でないこと、すなわち副枝 (N$_\infty$) でないことを使っている** — v1.2 で明示)。したがって
  $$ \boxed{\ u^{(B)}\ =\ \frac{\hat c}{\lambda^\iota(P_0)}\ =\ \frac{\hat c}{A(x_0)-B(x_0)\,y_0}\ }\qquad(y_0:=y(P_0)). \tag{6.1} $$
- **B-ii($P_0$ Weierstrass・$t=y$;この場合 $P_0$ は自動的にアフィン — 補題 R1-U∞ 1. より $\infty_\pm$ は Weierstrass 点でない)**: $\lambda+\lambda^\iota = 2A(x)$ で、$\lambda = ut^{10}+u_{11}t^{11}+\cdots$, $\lambda^\iota = \lambda(-t)$ ゆえ $\lambda+\lambda^\iota = 2ut^{10}+O(t^{12})$。他方 $y^2=f(x)$ と $f(x_0)=0$ から $x-x_0 = y^2/f'(x_0)+O(y^4)$。ゆえに $A(x) = \alpha(x-x_0)^5+O((x-x_0)^6)$ と書けば
  $$ \boxed{\ u^{(B)}\ =\ \frac{\alpha}{f'(x_0)^5},\qquad \alpha := \bigl[(x-x_0)^5\bigr]A(x)\ =\ \frac{A^{(5)}(x_0)}{120}.\ } \tag{6.2} $$

- **B-iii(副枝 (N$_\infty$): $P_0=\infty_-$・$t=1/x$)— v1.2 で新設**: この副枝では $\lambda^\iota$ は $P_0$ で **10 位の極**をもつので (6.1) の分母 $\lambda^\iota(P_0)$ は定義されない。$N(\lambda)$ が定数になる代わりに、$\iota(P_0)=P_\infty$ での主要係数が分母の役を果たす:

  $$ \boxed{\ u^{(B)}\ =\ \frac{\hat c}{2\,a_{10}},\qquad \hat c := A^2-B^2f_6\ \in\mathbb Q^\times\ (\textbf{定数}),\qquad a_{10} := [x^{10}]\,A(x)\ \ne 0.\ } \tag{6.3} $$

  **(6.3) は多項式の係数抽出と一回の多項式恒等式検査だけで計算される**(評価も Taylor 展開も不要 — B-i/B-ii より弱い機構)。

> **補題 R1-B∞(副枝 (N$_\infty$) の構造と $u$).** M1 の正規化モデル($f_6$ モニック・$P_\infty=\infty_+$・$P_0=\infty_-$)で $\lambda = A(x)+B(x)y$、$a_j:=[x^j]A,\ b_j:=[x^j]B$ とし、$s=1/x$、$W\in\mathbb Q[[s]]$ を $W^2=F,\ W(0)=1$、$M:=\max(\deg A,\deg B+3)$、$\tilde A:=s^MA(1/s)$、$\tilde B:=s^{M-3}B(1/s)\in\mathbb Q[s]$、$G_\pm := \tilde A\pm W\tilde B$ と置く。$\operatorname{div}(\lambda)=10P_0-10P_\infty$ の下で:
> 1. $\boxed{M=10}$、すなわち $\deg A = 10$ かつ $\deg B = 7$。さらに $\boxed{b_7 = a_{10}\ne0}$。
> 2. $\boxed{N(\lambda) = A^2-B^2f_6 = \hat c\in\mathbb Q^\times}$(**定数**)。
> 3. $t=1/x$ に関して $\lambda = u\,t^{10}(1+O(t))$ が成り立ち、$\boxed{u = \hat c/(2a_{10})}$。
>
> **証明.** 補題 R1-U∞ 1. のチャートで $x=1/s,\ y=w/s^3$ だから
> $$ \lambda\ =\ A(1/s)+B(1/s)\,\frac{w}{s^3}\ =\ s^{-M}\bigl(\tilde A(s)+w\,\tilde B(s)\bigr), $$
> ここで $\infty_+$ では $w=W$、$\infty_-$ では $w=-W$($w^2=F$ の二つの根)。$M$ の定義から $(\tilde A(0),\tilde B(0))\ne(0,0)$ であり、$\tilde A(0)=a_M$($\deg A=M$ のとき、さもなくば $0$)、$\tilde B(0)=b_{M-3}$(同様)。
>
> **1.** $\operatorname{ord}_{\infty_-}(\lambda)=+10$ は $\operatorname{ord}_s G_- = M+10>0$ を意味するから $G_-(0)=\tilde A(0)-W(0)\tilde B(0)=\tilde A(0)-\tilde B(0)=0$、すなわち $\tilde A(0)=\tilde B(0)$。もし両方 $0$ なら $M$ の定義に反するので $\tilde A(0)=\tilde B(0)\ne0$、ゆえに $\deg A=M$ かつ $\deg B+3=M$ で $a_M=b_{M-3}\ne0$。すると標数 $0$ で $G_+(0)=\tilde A(0)+\tilde B(0)=2a_M\ne0$、すなわち $\operatorname{ord}_sG_+=0$。他方 $\operatorname{ord}_{\infty_+}(\lambda)=-10$ は $\operatorname{ord}_sG_+ - M = -10$ を与えるから $M=10$。
> **2.** $G_+G_- = \tilde A^2-W^2\tilde B^2 = \tilde A^2-F\tilde B^2 = s^{20}\bigl(A(1/s)^2-f_6(1/s)B(1/s)^2\bigr) = s^{20}\,N(1/s)$、$N:=N(\lambda)\in\mathbb Q[x]$。左辺の $\operatorname{ord}_s$ は $0+(M+10)=20$。$N=\sum_{k}n_kx^k$ と書けば $s^{20}N(1/s)=\sum_kn_ks^{20-k}$ の $\operatorname{ord}_s$ は $20-\deg N$。ゆえに $\deg N=0$、$N=\hat c$ は定数で、$\operatorname{ord}_s$ がちょうど $20$ だから $\hat c\ne0$。
> **3.** 2. より $G_- = \hat c\,s^{20}/G_+$、よって
> $$ \frac{\lambda}{s^{10}}\ =\ \frac{G_-}{s^{20}}\ =\ \frac{\hat c}{G_+}\ \xrightarrow[\ s\to0\ ]{}\ \frac{\hat c}{G_+(0)}\ =\ \frac{\hat c}{2a_{10}} . $$
> $s=t$ ゆえこれが $u$。$\blacksquare$
>
> **【級数を使っていないことの確認】** 証明の中では $W$ を**書き下していない**($W(0)=1$ という一点の値しか使っていない)。(6.3) の右辺は $A,B,f_6$ の係数から**有限回の有理数演算**で得られる。したがって B-iii は経路 A(Newton/Hensel 級数)と原理的に独立である(§6.3 の要件 1./2. を満たす)。

> **(N$_\infty$) の構造検査(fail-closed・すべて厳密な多項式演算)**:
> - **(N∞-1)** $\deg A = 10$ かつ $\deg B = 7$;
> - **(N∞-2)** $b_7 = a_{10}\ne0$;
> - **(N∞-3)** $A^2-B^2f_6$ が**定数** $\hat c\ne0$(次数 $\ge1$ の係数がすべて $0$);
> - **(N∞-4)** $\boxed{\hat c=1}$(**補題 R1-N∞-S** — §11 論点 7)。前提の $\sigma_1\ne\mathrm{id}$ は**本 campaign では自動**である: $\sigma_1=\mathrm{id}$ なら $\operatorname{Mon}=\langle\sigma_0\rangle$ は巡回群で $10$ 点上に推移的、ゆえに正則作用で点安定化群 $H=1$、すると $N_{\operatorname{Mon}}(H)/H=\operatorname{Mon}\ne1$ となり §4.3 **補題 R1-U**($\operatorname{Aut}(W_0/U)=1$)に矛盾する。
>
> **いずれかが破れたら入力破損 ⇒ integrity stop(§9 I-j)。**
>
> > **【重要・I-b との関係(v1.2)】** 補題 R1-B∞ 3. により、この副枝では
> > $$ u\ =\ \frac{\hat c}{2a_{10}}\ \overset{(\text{N∞-4})}{=}\ \frac{1}{2a_{10}} $$
> > すなわち **$u$ は $\lambda$ の係数一つ($a_{10}=[x^{10}]A$)の一行の関数**である。したがって **(N∞-2)(N∞-3)(N∞-4) は事実上 $u$ の計算と同値**であり、「$u$ を開ける前の安全な事前検査」として扱ってはならない。
> > - 凍結 2 前に人間へ見せてよいのは **(N∞-1)(次数のみ)** だけ。
> > - **(N∞-2)–(N∞-4) は $u$ と同じ封印段で、同じ access control の下で走らせる。** $\hat c$ と $a_{10}$ の値は §10-6 の記録欄(凍結 2 まで空)に入る。
> > - これは §11-1 の但し書き(full Belyi map を許す以上、担保は語彙 grep でなく **access control と total selection rule の二重**である)の、副枝 (N$_\infty$) における具体化である。**M-A の正規化規則は $u$ にも $a_{10}$ にも依存しないので、選択自由度ゼロという前件は保たれている。**
> >
> > **【v1.3 で追加・I-b∞: $\mu$ 側の norm 定数 $\hat c_\mu$ も同じ封印段】** 副枝 (N$_\infty$) が live に確定した以上、この枝の**漏洩経路をすべて閉じる**必要がある。$\lambda=c\mu^2$(命題 S5-2)と (N$_\infty$) の norm 恒等式(S5 設計 v1.2 命題 S5-3∞)から
> > $$ \hat c_\mu\ :=\ a^2-f_6p^2\ \in\mathbb Q^\times\ (\textbf{定数}),\qquad \hat c\ =\ c^2\hat c_\mu^{\,2},\qquad a_{10}=2ca_5^2,\qquad u\ =\ c\Bigl(\frac{\hat c_\mu}{2a_5}\Bigr)^{2} $$
> > (**$\mu=a(x)+p(x)y$、$a_5:=[x^5]a$**)。ここで補題 R1-N∞-S 2. の $\hat c=1$ を使うと $c=\pm\hat c_\mu^{-1}$、したがって $-1=i^2\in K^{\times2}$($K=\mathbb Q(\zeta_{20})$)ゆえ
> > $$ \boxed{\ \text{(N}_\infty\text{) では}\quad \text{(P1)}\ \iff\ c\in K^{\times2}\ \iff\ \hat c_\mu\in K^{\times2}\ \iff\ \operatorname{sqfree}(\hat c_\mu)\in\{1,-1,5,-5\}.\ } $$
> > すなわち **$\hat c_\mu$ 単独で封印予測 (P1) が完全に決まる**。他の二枝ではこうならない((N$_{\rm aff}$)/(W) では $\hat c=c^2c_N^2$ だが $\hat c=1$ の定理がないので、$c_N$ 単独では (P1) は決まらない)。**この非対称は $\hat c=1$(補題 R1-N∞-S 2.)が (N$_\infty$) だけで成り立つことから生じる。**
> > - よって **§9 I-b の禁止対象に $\hat c_\mu$(および $\mu$ の norm 定数と同値な任意の量)を明記する**(§9.2 I-b)。
> > - **$\hat c_\mu$ は $u,\hat c,a_{10}$ と同じ封印段・同じ access control** に置く。凍結 2 前に人間へ見せない。
> > - これは新しい禁止ではなく、**strict I-b(「$\lambda$ を $(c,\mu)$ の対に分離して報告することの禁止」)の (N$_\infty$) における具体化**である。ただし $\hat c_\mu$ は「$c$ でも $\mu$ の係数でもない第三の量」の顔をして通りうるので、**逐語で書く**(S5 設計 §6.2 ★教材候補 2 の形: 禁止リストは量の出自でなく「封印予測のどのビットを決めるか」で書く)。

**中間表現**: $\mathbb Q[x]$(多項式・評価・Taylor 係数;B-iii は係数抽出のみ)。**冪級数を使わない。**

> **補助経路 B′(S5 設計に依存・任意)**: 命題 S5-2 が成立するなら $\lambda=c\mu^2$、$\mu = v t^5(1+\cdots)$ で $u = cv^2$、かつ $\mu\mu^\iota = c_N(x-x_0)^5$(**v1.1: 記号を $c_N$ に統一** — S5 設計 v1.1 §3.3.0)から、$P_0$ 非 Weierstrass・$t=x-x_0$ の場合に $v = c_N/\mu^\iota(P_0)$(級数不要)。**B′ は第三経路であって B の代用ではない。** 用いる場合は独立な札で記録する。
>
> **【v1.2 の適用範囲】B′ の上式は $x_0=x(P_0)$ が有限であること(枝 (W)・副枝 (N$_{\rm aff}$))を前提とする。** 副枝 (N$_\infty$) では $\mu\mu^\iota$ も定数になり(補題 R1-B∞ 2. の $\lambda$ を $\mu$ に置き換えた議論;$\operatorname{div}\mu=5P_0-5P_\infty$ ならば $\deg A_\mu=5,\ \deg B_\mu=2$)、上式は書き換えを要する。**B′ は任意の第三経路なので、v1.2 では (N$_\infty$) 版を書き下さない** — この副枝で B′ を使いたければ、S5 設計側の (N$_\infty$) 対応(§11.1 R-4)を待って別便で追加する。それまで (N$_\infty$) で B′ を走らせてはならない。
>
> **【v1.3・B′∞】R-4 が閉じた**(S5 設計 v1.2 §3.3.5 命題 S5-3∞)ので、(N$_\infty$) 版を書ける: $\mu=a(x)+p(x)y$、$\hat c_\mu:=a^2-f_6p^2\in\mathbb Q^\times$(定数)、$a_5:=[x^5]a\ (=[x^2]p\ne0)$ とすると $t=1/x$ に関して
> $$ \mu=v\,t^5(1+O(t)),\qquad v=\frac{\hat c_\mu}{2a_5},\qquad \boxed{u^{(B')}=c\,v^2=\frac{c\,\hat c_\mu^{\,2}}{4a_5^{\,2}}}\quad(\text{B-iii と同型の議論;}\ \deg=10\to5). $$
> **付随する強い整合検査**(いずれも封印段): $a_{10}=2ca_5^2$、$b_7=a_{10}$、$\hat c=c^2\hat c_\mu^2$、および補題 R1-N∞-S 2. の $\hat c=1$ との合成 $c^2\hat c_\mu^2=1$。**ただし B′ は依然として任意の第三経路であり、$(c,\mu)$ 分離を要するので strict I-b の下で凍結 2 前は走らせない**(上の v1.1 運用制限は不変)。$\hat c_\mu$ の扱いは §6.2 の **I-b∞** に従う。
>
> **【v1.1 の運用制限】B′ は $\lambda$ を $(c,\mu)$ に分離した形を要求するので、§9 I-b 厳格版の下では凍結 2 より前に走らせてはならない。** 凍結 2 のあとの独立な裏取りとしてのみ使う。

### 6.3 独立性の要件(manifest v1.2 §4 の実体化)

1. **非共有 helper**: 経路 A の級数モジュールと経路 B の多項式モジュールは、**共通の関数・共通のデータ構造を一切共有しない**。共有してよいのは数体 $K$ の元の表現(§8)だけで、それも**別実装を推奨**。
2. **別中間表現**: $K[[t]]$ vs $\mathbb Q[x]$(上記)。
3. **raw 出力の別保存**: `u_pathA.json` / `u_pathB.json`(それぞれ生の中間量も含む)。
4. **第三の checker**: 二つの生出力**だけ**を読み、$u^{(A)} = u^{(B)}$ を $K$ の中で厳密に判定する小さな独立プログラム。**それ以外の計算をしない。**
5. **model digest の束縛(v1.3・便 35 F2.2)**: 両経路の driver は、モデルの係数を**手転記せず**、凍結 bundle の canonical model JSON を読み、その **canonical digest を入力として束縛**する。第三 checker は (i) 二 raw の `model_digest` の相互一致、(ii) **凍結 bundle 側の expected digest との一致**、の**両方**を fail-closed に検査する。
   > **根拠**: digest を二 raw の echo field から自己生成するだけでは、**二 driver が同じ誤転記をすれば checker は ACCEPT する**(便 35 F2.2)。「二系統一致」は同じ入力を仮定した上でしか意味を持たない。破れは **I-l**(§9.2)。
6. **(N$_\infty$) 用 raw schema(v1.3・便 35 F5.2)**: 副枝 (N$_\infty$) では $x_0,y_0$ が**存在しない**。したがって cusp raw は $x_0,y_0$ を必須 field に持つ schema を**流用してはならない**(欠落を $0$ 等の既定値で埋めると I-k/I-j が発火せずに通る)。(N$_\infty$) 用に、$x_0,y_0$ を持たず代わりに $M$ の実測値・$\hat c$・$a_{10}$・$b_7$ を持つ**別 schema** を用意し、schema 名を枝ラベルと突合する(不一致は **I-m**)。

### 6.4 受理規則

| 結果 | 処置 |
|---|---|
| $u^{(A)} = u^{(B)}$($K$ 内の厳密等号) | **受理**。$u := u^{(A)}$ を凍結記録へ |
| 不一致 | **即 integrity stop / BRIDGE-UNKNOWN**。**平均・符号調整・座標再選択を禁止**。数学的結論を一切宣言しない |
| 一方が計算不能(予算超過・分岐未対応) | **二経路不成立** ⇒ BRIDGE-UNKNOWN(§9 U-e)。片方だけで $u$ を採用しない |

---

## §7. $b_i$ の決定式と受理条件

### 7.1 定義

- $\ell_i$ := **正の向きの実 local monodromy**。すなわち、$P_0$ における惰性群($\cong\mu_{10}$、全分岐)の生成元で、(1.6) の埋め込みの下で $\lambda$ の周りを**反時計回り**に一周する $\gamma_0$ に対応するもの。
- $c_i$ := §4.3 の**一意**な intertwiner $\operatorname{Fib}_{\vec{01}}(W_0^{(i)})\xrightarrow{\sim}\Lambda_i$。

$$ \boxed{\ c_i\,\ell_i\,c_i^{-1}\ =\ \tau_i\bigl(\zeta_{10}^{\,b_i}\bigr),\qquad b_i\in(\mathbb Z/10)^\times = \{1,3,7,9\}.\ } \tag{7.1} $$

$\tau_i$ は単射なので、右辺が $\tau_i(\langle\zeta_{10}\rangle)$ に属せば $b_i$ は**一意**。

$$ \text{属さない}\ \Longrightarrow\ \text{actual marking が閉じていない}\ \Longrightarrow\ \textbf{BRIDGE-UNKNOWN}\ (\S9\ \text{U-f}). $$

### 7.2 比較指数

$$ \boxed{\ a_{\rm eff}\ =\ [b_{\rm ns}]^{-1}\,a\,[b_{\rm sq}],\qquad a = 1\ \text{(永久不変)}\ } \tag{7.2} $$

($[b_i]$ は $\mu_{10}[5]$ への制限。$(\mathbb Z/10)^\times\to(\mathbb Z/5)^\times$ は全単射ゆえ lift の曖昧さはない。)

### 7.3 受理条件(**厳格運用**)

$$ \boxed{\ b_{\rm sq} = b_{\rm ns}\ }\quad\Longrightarrow\quad a_{\rm eff} = a = 1\quad\Longrightarrow\quad \text{(P2) は完全一致形}\ [u_{\rm ns}^{-1}]_{10} = [u_{\rm sq}^{-1}]_{10}. $$

$$ b_{\rm sq}\ne b_{\rm ns}\ \Longrightarrow\ \textbf{規約不整合として停止・}u\ \textbf{を開けない}\ (\S9\ \text{I-d}). $$

### 7.4 事前の見込みと、それを仮定しない規律

§1.2–§1.3 の規約の下では $\sigma_0 = \tau_i(X)$ が定義であり、$c_i$ が一意な intertwiner であることから **$b_i = 1$ が期待される**。しかし

> $b_i = 1$ を**仮定してはならない**。必ず (7.1) を**計算して記録**する。

$b_i\ne1$ が出る現実的な原因は (a) 実装内の向きの反転(§1.3 の GAP 規約差の吸収漏れ)、(b) 埋め込み (1.6) と異なる原始根の使用、(c) 惰性生成元の取り方の反転である。**いずれも「発見」ではなく規約の記録事項**であり、$a$ を更新して吸収してはならない(裁定 29-2)。

---

## §8. exact 数体・Kummer 判定器の仕様

### 8.1 数体

$$ K = \mathbb Q[T]/(T^8-T^6+T^4-T^2+1),\qquad \zeta_{20} := \bar T,\qquad \text{埋め込みは }(1.6). $$

すべての演算は**厳密**(有理数係数の多項式剰余環)。**浮動小数点を判定に用いない。**

### 8.2 $K^{\times10}$ 判定の骨(算術的単純化)

$\mu_{10}\subset K$ であり $10 = 2\cdot5$、$\gcd(2,5)=1$ なので

$$ \boxed{\ w\in K^{\times10}\ \iff\ w\in K^{\times2}\ \textbf{かつ}\ w\in K^{\times5}.\ } \tag{8.1} $$

($\Leftarrow$: $w=p^2=q^5$ なら $w = w^5(w^2)^{-2} = p^{10}q^{-20} = (p/q^2)^{10}$。)

したがって判定は **$T^2-w$ と $T^5-w$ の $K[T]$ における厳密な因数分解**に帰着する(根の存在判定)。**「根が見つからなかった」ではなく「因数分解の結果、一次因子がない」**という証明書を出す。

### 8.3 証明書型($v_i := u_i^{-1}$)

| 判定 | 陽性証明書 | 陰性(obstruction) |
|---|---|---|
| $\operatorname{ord}([v]_{10}) = 1$ | 明示 $c\in K^\times$ with $c^{10}=v$ | — |
| $\operatorname{ord}([v]_{10}) = 5$ | 明示 $c$ with $c^{10}=v^5$ **かつ** $v\notin K^{\times10}$ の exact obstruction | 下記メニューのいずれか |
| **(P2)** | $r := v_{\rm ns}/v_{\rm sq}^{\,a_{\rm eff}}$ について $c^{10}=r$ の明示 witness | $r\notin K^{\times10}$ の exact obstruction |

**obstruction メニュー(いずれか一つで足りる)**

- (O-a) 素イデアル $\mathfrak p$ で $v_{\mathfrak p}(v)\not\equiv0\pmod{10}$($(v)$ のイデアル分解を厳密に取る)。**最も安価で最も強い。**
- (O-b) $T^2-v$ が $K[T]$ で既約(2-part の障害)。
- (O-c) $T^5-v$ が $K[T]$ で既約(5-part の障害)。

**探索失敗しか無い場合は UNKNOWN**(§9 U-e)。浮動小数点の root search は証明書にならない。

### 8.4 (5′) の量化子

$$ \rho_i(\operatorname{Ih}(\gamma)) = \tau_i(\kappa_i(\gamma))\qquad(\forall\gamma\in G_K). $$

**有限個の Frobenius サンプル一致は較正であって PASS の証明ではない。** PASS は character 恒等の普遍的導出、または同値な Kummer 拡大の厳密同定を要する。**FAIL は exact な $\gamma$ 一つで足りる。**

### 8.5 (P1) の補助証明書(**S5 設計 命題 S5-4 に依存・凍結 2 後にのみ使用可**)

$\lambda = c\mu^2$($c\in\mathbb Q^\times$)なら
$$ \text{(P1)}\ \iff\ c\in K^{\times2}\ \iff\ \operatorname{sqfree}(c)\in\{1,-1,5,-5\} $$
($K=\mathbb Q(\zeta_{20})$ の二次部分体は $\mathbb Q(i),\mathbb Q(\sqrt5),\mathbb Q(\sqrt{-5})$)。

> **★ この事実は同時に漏洩経路である。** §9 I-b を参照。**$\operatorname{sqfree}(c)$ の計算は凍結 2 より前は禁止**であり、凍結 2 のあとに (P1) の**独立な第二証明書**としてのみ用いてよい。

### 8.6 版の固定

凍結記録に: 数体演算ライブラリ名 + 版 + commit、因数分解アルゴリズム名、イデアル分解アルゴリズム名、経路 A/B の実装 commit、第三 checker の commit。

---

## Q6 → §9. 停止条件

### 9.1 UNKNOWN 停止(札であって失敗ではない)

| # | 条件 |
|---|---|
| **U-a** | §2 のパイプラインが 2 個以上の候補を返し、§3.2 の全順序でも同点 |
| **U-b** | §3.1 の**有限性が証明できない**(残余群の軌道が無限かもしれない) |
| **U-c** | M0 の**枝判定**($P_\infty$/$P_0$ の Weierstrass 性、**および $P_0=\iota(P_\infty)$ 判定 (2.-1)** — v1.2 で追加)が、事前登録した計算予算内に閉じない。**予算 = M0 の一判定ジョブにつき wall-clock 600 秒**(**予算値は v1.2 でも不変**。判定が三つになったので、ジョブ数が増えるだけで一ジョブの上限は同じ)(v1.1 で §11 から本行へ移記・便 32 F2.5)。**timeout は U-c**(FAIL でも「非 Weierstrass」でもない)。**同 campaign 内で上限を増やして再分類しない** — 上限を変えるなら新 version の campaign |
| **U-d** | 明示モデルそのものが得られない(撤退条件 2026-08-10 / 8 委嘱とは別枠の即時札) |
| **U-e** | exact Kummer 証明書が得られない(探索失敗のみ)/ $u$ の一方の経路が計算不能 |
| **U-f** | $b_i$ が $\tau_i(\langle\zeta_{10}\rangle)$ に属さない(actual marking 未閉) |

**UNKNOWN で止まったら、規則を変えて一意化しない。** 規則を変えるなら**新 version の campaign** とする。

### 9.2 即時 integrity stop(救済不可)

| # | 条件 |
|---|---|
| **I-a** | 凍結 1 前に個別モデル候補・係数・数値近似に接触した |
| **I-b** | 凍結 2 前に $u$ **または同値な leading class** が漏れた。**同値物には $\lambda=c\mu^2$ の $c$ の平方類・平方因子・符号を含む**(命題 S5-4)。$\lambda$ を「$c$ と $\mu$ の対」に分離して報告することも禁止。**(v1.3・I-b∞)** 副枝 (N$_\infty$) では**さらに $\hat c_\mu=a^2-f_6p^2$($\mu$ の norm 定数)の値・平方類・平方因子・符号**、および $\hat c$・$a_{10}$・$b_7$・$a_5$ を含む(§6.2 の I-b∞: $\hat c=1$ ゆえ **$\hat c_\mu$ 単独で (P1) が決まる**) |
| **I-c** | $u$ 二経路の不一致(§6.4) |
| **I-d** | $b_{\rm sq}\ne b_{\rm ns}$(§7.3) |
| **I-e** | モデル検査二系統の不一致 / U-3 の $\varepsilon\notin\mathbb Q^\times$ |
| **I-f** | intertwiner $c_i$ が一意でない(補題 R1-U に反する ⇒ 入力破損) |
| **I-g** | S5 設計の受理物 A8($\operatorname{ord}[P_0-P_\infty]=5$)が破れる |
| **I-h** | hash・serialization・発射錠の対象が一致しない / 両翼共同凍結前に片翼の $u$ を開けた |
| **I-i** | exact Kummer 証明書なしに PASS/FAIL を宣言した |
| **I-j**(v1.2) | 副枝 (N$_\infty$) の構造検査 **(N∞-1)–(N∞-4)**(§6.2 B-iii)のいずれかが破れる。すなわち $\deg A\ne10$ / $\deg B\ne7$ / $b_7\ne a_{10}$ / $a_{10}=0$ / $A^2-B^2f_6$ が非定数または $0$ / ($\sigma_1\ne\mathrm{id}$ なのに)$\hat c\ne1$。**いずれも $\operatorname{div}(\lambda)=10P_0-10P_\infty$ と入力モデルの矛盾を意味する** ⇒ 入力破損 |
| **I-k**(v1.2) | M0 の intrinsic 判定 (2.-1) と座標判定($x(P_0)=\infty$)が食い違う(I-e の特例として明示) |
| **I-l**(v1.3) | raw の `model_digest` が**凍結 bundle の expected model digest** と一致しない、または二 raw の間で一致しない(§6.3-5)。**二 raw の自己生成 digest が一致するだけでは閉じない** — 同じ誤転記は同じ digest を生む(便 35 F2.2) |
| **I-m**(v1.3) | 枝ラベルが三値 enumeration $\{\texttt{W},\texttt{N\_aff},\texttt{N\_infty}\}$ に属さない / 欠落している / **未知ラベルを既定値へ落とした**(§2.2 M0 の v1.3 規定)。raw schema 名と枝ラベルの不整合も同じ(§6.3-6)。**「知らない枝は Weierstrass」型の暗黙 fallback は入力破損として扱う**(便 35 F5.2) |

### 9.3 Model-Builder(A)の入出力 schema(凍結 1 の一部)

**許可される出力**: 明示モデル $C/\mathbb Q$、Belyi 写像 $\lambda$(**完全な式として**)、分岐 divisor、cusp $P_0,P_\infty$、uniformizer $t$ の式、target triple への exact conjugator、分岐指数 10 の証明、$t$ が uniformizer であることの証明、$\operatorname{Aut}(C/\mathbf P^1)=1$ の証明、**および (7.1) による $b_i$ の計算と記録**(【司令塔修正 C1】: $b_i$ は $u$ に接触しない置換計算であり、BRIDGE-IN 組立ての一部として Model-Builder が計算・記録する。所有者の空白を残さないための明示)。

**禁止される計算**: $\lambda/t^{10}$ の非零定数項およびその同値物(leading coefficient・その valuation・その Kummer class)、**$c$ の平方類・平方因子・符号**、そしてそれらを**候補選択に使うこと**。

**A は「$u$ 未計算」および「$\operatorname{sqfree}(c)$ 未計算」を申告し、全 transcript を保存する。** 主根拠は本 schema と役割別 access log であり、**grep は補助検査**にすぎない(W4)。

---

## §10. 凍結記録に載せるもの

1. 本文書の **canonical serialization**(UTF-8・改行 LF・末尾改行あり・BOM なし)と **sha256**。
2. UTC/JST timestamp、commit ID、凍結対象の全ファイル一覧。
3. §8.6 の実装版一覧。
4. §1.6 の $(\mathbb Z/20)^\times\to(\mathbb Z/10)^\times$ の $2:1$ lift の記載(別欄)。
5. 発射錠 `FIRE_k5bridge.auth` が束縛する digest 組(**一回性・別 artifact へ再利用不可**)。
6. **記録欄(値は凍結 2 まで空)**: $b_{\rm sq}$, $b_{\rm ns}$, $a_{\rm eff}$, $\varepsilon$(U-3)、**枝 (W)/(N$_{\rm aff}$)/(N$_\infty$) の別**(v1.2)、$P_0$ の Weierstrass 性、**$M=\max(\deg A,\deg B+3)$ の実測値と $\hat c$(いずれも副枝 (N$_\infty$) のみ・v1.2)**、**$\hat c_\mu$(副枝 (N$_\infty$) で B′∞ を使う場合のみ・v1.3・I-b∞ の封印対象)**。**$a=1$ の欄は不変値として先に埋める。**
7. **(v1.3)$(0\,\infty)$-対称性 witness の記録(凍結 2 前でも可視)**: 各 fixture $i\in\{\rm sq,ns\}$ について、(35.4) を満たす $g_i\in S_{10}$ の**存否・値・一意性**、および $g_i^2=\sigma_{1,i}$ の成否(§11 論点 7 の (35.5))。**これは凍結済み fixture の置換データだけから決まる有限事実**であり、モデル・$\lambda$・$u$・$c$ に一切依存しないので、$u$ の封印段の外に置いてよい。**「排除された」ではなく「対称性条件は充足・(N$_\infty$) の存否は未決」という結論の形で記録すること。**

---

## §11. 論点(**v1.1 で 1–6 すべて決着** — 便 32 / 裁定 31)

1. **§9 I-b(命題 S5-4 由来の漏洩禁止)を採るか。** → **【決着・I-b 厳格版を採用】**(便 32 F2.3・裁定 31)。凍結 2 前は (i) $c$ の平方類・平方因子・符号を**計算しない**、(ii) $\lambda$ を $(c,\mu)$ の対として**報告しない**、(iii) それらを**候補選択に使わない**。代案(「分解形の報告は許し access log で担保」)は**採らない**。
   > **採用理由の補足(裁定 30 の但し書きつき)**: 「漏洩実害 = 可視性 × 選択自由度」という分析は原理として正しいが、**「選択自由度ゼロ」は正規化が total, executable, pre-frozen であるときにだけ成立する**(便 32 F2.3・★教材 23)。v1 は M4 が未定義でその前件が立っていなかった。**v1.1 の §2.2 M4 + §2.4 の R1-N1/N2 が前件を初めて成立させる**が、それでも I-b の緩和には使わない — 便 32 W4 の通り、full Belyi map を許す以上 $c$ の平方類は原理的に導出可能であり、担保は語彙 grep でなく **access control と total selection rule** の二重である。親 manifest 側にも同語で反映される(P3・司令塔)。
2. **§2 (M-A) と (M-B) の分離**は過剰か。 → **【決着・分離を維持。M-B は第一次規則へ昇格しない】**(便 32 F2.3・裁定 31)。理由は「S5 設計が未監査だから」ではなく、**M-B が strict I-b と両立しないから**である(solver が $c$ を明示変数として扱う)。監査が通っても自動昇格はしない。**M-B / $\mu$-正規形を discovery engine に使うなら、$c$ を凍結 2 前に人間へ見せない sealed automation を別 schema として事前登録する**(§2.3 の枠内)。v1.1 では M-A が正本、M-B は凍結 2 後の整合検査。
3. **§5.4 の観測 R1-C** を規則の緩和に使わないという判断でよいか。 → **【決着・承認】**(便 32 F2.1)。「R1-C は Kummer class の covariance を示すだけであり、生の $u$ の二経路比較に使う $t$ を曖昧にしてよい理由にはならない」。
4. **§6.2 B-ii の式 (6.2)** を経路 A と独立と認めてよいか。 → **【決着・独立と認定】**(便 32 F2.4)。B-ii は曲線上の Hensel/Newton 級数を作らず $\mathbb Q[x]$ 内の Taylor 係数と一点評価だけを使うため、§6.3(非共有 helper・raw 中間量の別保存)が実装でも守られる限り独立経路。**「多項式の Taylor 係数」という語だけを理由に級数経路と同一視しない。** B′ は第三経路であり B の代替にしない(現規定どおり)。
5. ~~U-c の計算予算の具体値を凍結 1 に書き込むべきか~~ → **【決着・§9.1 U-c の作用行へ移記済(v1.1・D8)】**(便 32 F2.5)。値 = M0 の一判定ジョブにつき wall-clock 600 秒。**論点欄に予算値を置かない**(未決パラメータに見えるため)。委嘱全体の cap は従来どおり委嘱ごと。
6. **【文献要請・充足】** §8.2 の $K^{\times10}$ 判定 → **`docs/文献ゲート_02_power_residue.md` が仕様 provenance として PASS**(便 32 F2.5)。$\zeta_2,\zeta_5\in K$ のもとで平方・五乗判定へ分解する exact Kummer 仕様と、valuation obstruction / binomial factorization の数学的出所は閉じた。
   > **ただし二つの留保(便 32 F2.5・そのまま採録)**: (i) Sol は Cohen/Roblot の一次 PDF と定理番号を独立照合していない。(ii) **文献は executable certificate checker ではない。** 凍結 1 の最終 bundle には §8.6 が要求する library 名・版・commit、アルゴリズム名、経路 A/B と第三 checker の commit を**値として**埋めること(P6 後半・実装別便)。

7. **【v1.2 新設・v1.3 で決着(否定的決着)】副枝 (N$_\infty$) の存否を、凍結済み fixture 上の組合せ的証明書で閉じるか。** 便 34 F2.3 は二つの選択肢を示した。**v1.2 は選択肢 2(副枝の追加)を採り、M-A の total 性はこれで回復した。** 選択肢 1(exact な排除証明書)は**任意の補強**として設計だけ置いた — **launch blocker ではない**(証明書が得られなくても M-A は total)。

   $$ \boxed{\ \textbf{v1.3 の決着: 選択肢 1 は使えない。両 fixture が必要条件を満たすので、対偶による排除は不可能である。}\ } $$

   **したがって副枝 (N$_\infty$) は live** であり、以後「排除済み」を前提にした省略・既定枝への固定を一切してはならない(§2.2 M0 の v1.3 規定・§9.2 I-m)。**この決着は Rule 1 の受理を妨げない**(M-A は v1.2 で既に total)。影響を受けるのは (i) 実装の網羅性(§11.1 R-5 が最優先へ復帰)と (ii) S5 設計の探索 ansatz(R-4 — S5 設計 v1.2 で閉)だけである。

   > **補題 R1-N∞-S(副枝 (N$_\infty$) が要求する dessin の対称性).** $P_0=\iota(P_\infty)$ と仮定する。$m(z):=\hat c/z$ と置く。
   > 1. $\lambda\lambda^\iota=\hat c\in\mathbb Q^\times$(補題 R1-B∞ 2.)、すなわち $\lambda\circ\iota = m\circ\lambda$。**$\iota$ は底の Möbius 変換 $m$ を覆う $C$ の自己同型**である。
   > 2. **$\lambda$ が $1$ の上で分岐する($\sigma_1\ne\mathrm{id}$)ならば $\hat c=1$**、したがって $m(z)=1/z$ は $\{0,1,\infty\}$ を保ち、$0\leftrightarrow\infty$ を交換し $1$ を固定する。
   > 3. ゆえに $\iota$ は**被覆の同型 $(C,\lambda)\xrightarrow{\ \sim\ }(C,1/\lambda)$** を与える。すなわち **ordered dessin は $S_3$-作用の元「$(0\,\infty)$ 交換」で不変**でなければならない。
   > 4. さらに $\iota$ の不動点(6 個の Weierstrass 点)は $\lambda$ で $\operatorname{Fix}(m)=\{+1,-1\}$ へ写る。
   >
   > **証明.** 1. は補題 R1-B∞ 2.。2.: $R:=\{\lambda\ \text{の分岐点}\}=\{P_0,P_\infty\}\cup S$、$S:=\lambda^{-1}(1)\cap R$ と置く。$\iota$ は同型だから $\operatorname{ram}(\lambda\circ\iota)=\iota(R)$;他方 $\lambda\circ\iota=m\circ\lambda$ で $m$ は $\mathbf P^1$ の同型だから $\operatorname{ram}(m\circ\lambda)=\operatorname{ram}(\lambda)=R$。ゆえに $\iota(R)=R$。$\sigma_1\ne\mathrm{id}$ なら $S\ne\emptyset$ で、$Q\in S$ に対し $\iota(Q)\in R$ かつ $\lambda(\iota(Q))=\hat c/\lambda(Q)=\hat c$。$\lambda(R)\subseteq\{0,1,\infty\}$ で $\hat c$ は有限非零だから $\hat c=1$。3. は 2. の言い換え。4.: $\iota(P)=P$ なら $\lambda(P)=1/\lambda(P)$。$\blacksquare$
   >
   > **補足($\sigma_1\ne\mathrm{id}$ は本 campaign では仮定でなく定理)**: $\sigma_1=\mathrm{id}$ なら $\operatorname{Mon}=\langle\sigma_0\rangle$ が巡回群として $10$ 点上に推移的に作用するので正則作用となり点安定化群 $H=1$、ゆえに $N_{\operatorname{Mon}}(H)/H=\operatorname{Mon}\ne1$ となって §4.3 補題 R1-U($\operatorname{Aut}(W_0/U)=1$)に矛盾する。**したがって 2.–4. は本 campaign では無条件に成立する。**

   **【論点 7-A】$(0\,\infty)$-対称性の正しい置換水準の述語(v1.3・便 35 F1.5)**

   > **式番号の規約(本論点のみ)**: 追跡を容易にするため、**便 35 の式番号 $(35.x)$ をそのまま引き継ぐ**(`sol/sol_reply_35_freeze1r4.md` F1.5)。本文書の他節の式番号体系とは独立である。

   > **【v1.2 の欠陥・撤回】** v1.2 の「証明書の設計」欄は、$T:=\{(\tau_0,\tau_1,\tau_\infty):\tau_0\tau_1\tau_\infty=\mathrm{id},\ \tau_i\in\mathrm{Cl}(\cdot)\}$ を使う**保守的判定**しか書かず、**正本となる置換水準の述語を書き下さなかった**。その空白を埋めた実装は素朴な交換 (35.3)($g\sigma_0g^{-1}=\sigma_\infty,\ g\sigma_1g^{-1}=\sigma_1,\ g\sigma_\infty g^{-1}=\sigma_0$)を検査し、両 fixture で `false` を得て `ninf_excluded=true` を出した。**この判定は数学的に無効であり、撤回する。** 仕様の空白は起草者(私)の責任である。
   >
   > **★教材 28(自認)**: **「必要条件がある」と書くだけでは仕様にならない。** 幾何の必要条件を組合せ的証明書に落とすときは、**置換水準の述語そのものを正本に書き下す**まで仕様は未完成である。書かなければ、埋めるのは実装であり、実装は最も自然に見える(そして誤った)対称形を選ぶ。

   **正しい述語.** §1.1 の正本関係 $xyz=1$ の下で、向きを保つ $(0\,\infty)$-交換を表す $\operatorname{Out}(\hat F_2)$ の代表は
   $$ \beta(x)=z,\qquad \beta(y)=y,\qquad \beta(z)=y^{-1}xy \tag{35.1} $$
   である。実際 $\beta(x)\beta(y)\beta(z)=z\,y\,y^{-1}xy=zxy=1$($xyz=1$ の巡回)で関係式を保ち、peripheral 類を $[x]\leftrightarrow[z]$、$[y]\mapsto[y]$ と移し、$\beta^2=\operatorname{Inn}(y^{-1})$ ゆえ outer 位数は 2。基点への経路を変えた別代表は inner だけ異なり、simultaneous conjugacy に吸収される(3 点穴あき球面の写像類群は $S_3$ で、pure 部分は自明 — $\beta$ は $[y]$ を固定し $[x],[z]$ を交換する向き保存類として**一意**)。

   $\pi:\hat F_2\to\operatorname{Sym}(\Lambda_i)$、$(\sigma_0,\sigma_1,\sigma_\infty)=(\pi x,\pi y,\pi z)$ に対し、被覆が $\beta$-捻りと同型 $\iff$ $\exists g:\ g\,\pi(w)\,g^{-1}=\pi(\beta(w))\ (\forall w)$。生成元に書き下すと

   $$ \boxed{\ g\sigma_0g^{-1}=\sigma_\infty,\qquad g\sigma_1g^{-1}=\sigma_1,\qquad g\sigma_\infty g^{-1}=\sigma_1^{-1}\sigma_0\sigma_1\ } \tag{35.4} $$

   **これが正本である。** §10-7 の記録欄はこの述語で書く。

   > **補題 R1-N∞-W((35.4) の構造・v1.3 で新設).** $\sigma_0\sigma_1\sigma_\infty=\mathrm{id}$、$\operatorname{Mon}=\langle\sigma_0,\sigma_1\rangle$ は $\Lambda_i$ 上推移的、$C_{S_{10}}(\operatorname{Mon})=1$(§4.3 補題 R1-U)とする。
   > 1. **(35.4) の第三式は第一・第二式から自動**である。ゆえに (35.4) $\iff$ $g\sigma_0g^{-1}=\sigma_\infty\ \wedge\ g\sigma_1g^{-1}=\sigma_1$。
   > 2. $\sigma_0$ は $10$-巡回だから、$g\sigma_0g^{-1}=\sigma_\infty$ を満たす $g$ は $g(0)$ の値で**完全に決まり、ちょうど 10 通り**。したがって (35.4) の判定は **10 候補の悉皆**で閉じる($10!$ の走査は不要)。
   > 3. **解 $g$ は存在すれば一意**であり、そのとき $\boxed{g^2=\sigma_1}$。
   > 4. **素朴述語 (35.3) は (35.4) $\wedge\ [\sigma_0,\sigma_1]=1$ と同値**であり、本 campaign の仮定の下で **$[\sigma_0,\sigma_1]\ne1$ が定理**である。すなわち **(35.3) は恒真に偽** — dessin が何であれ `false` を返す**空虚な検査**であった。
   >
   > **証明.** 1. 第一・第二式より $g\sigma_\infty g^{-1}=g(\sigma_1^{-1}\sigma_0^{-1})g^{-1}=\sigma_1^{-1}\sigma_\infty^{-1}$。他方 $\sigma_0\sigma_1\sigma_\infty=\mathrm{id}$ から $\sigma_\infty^{-1}=\sigma_0\sigma_1$、ゆえに $\sigma_1^{-1}\sigma_\infty^{-1}=\sigma_1^{-1}\sigma_0\sigma_1$。
   > 2. $g\sigma_0=\sigma_\infty g$ を $p\mapsto\sigma_0(p)$ に沿って反復すると $g(\sigma_0^k(0))=\sigma_\infty^k(g(0))$。$\sigma_0$ が $10$-巡回ゆえ $\{\sigma_0^k(0)\}=\Lambda_i$ で $g$ は $g(0)$ から一意に定まり、$\sigma_\infty$ も $10$-巡回ゆえ得られる写像は常に全単射。
   > 3. $g,g'$ が二解なら $g^{-1}g'$ は $\sigma_0$ と $\sigma_1$ の双方と可換、すなわち $\operatorname{Mon}$ を中心化するので $=1$。次に $\pi\circ\beta^2=\operatorname{Inn}(\sigma_1^{-1})\circ\pi$ と (35.4) を二度使うと $g^2\pi(w)g^{-2}=\sigma_1^{-1}\pi(w)\sigma_1$、ゆえに $\sigma_1g^2\in C_{S_{10}}(\operatorname{Mon})=1$、$g^2=\sigma_1^{-1}=\sigma_1$($\sigma_1$ は型 $2^41^2$ の対合)。
   > 4. (35.3) は (35.4) に $g\sigma_\infty g^{-1}=\sigma_0$ を足したもの。1. よりこれは $\sigma_1^{-1}\sigma_0\sigma_1=\sigma_0$、すなわち $[\sigma_0,\sigma_1]=1$ と同値。もし $[\sigma_0,\sigma_1]=1$ なら $\operatorname{Mon}$ は可換かつ推移的ゆえ**正則**、したがって $C_{S_{10}}(\operatorname{Mon})\cong\operatorname{Mon}\ne1$ となり補題 R1-U に矛盾する。$\blacksquare$

   > **★教材 29(便 35 ★教材 27 の強化)**: cross-check は述語の妥当性を上げないだけでなく、**述語が恒真に偽なら、二系統一致は「二つの実装が同じ空虚な質問に正しく答えた」ことしか意味しない。** 判定述語を採用する前に、**その述語が充足可能でありうるか**(本件では $[\sigma_0,\sigma_1]=1$ が campaign の仮定と両立するか)を先に確かめる。**空虚な検査は、負の結果を出し続けることで最も長く生き延びる。**

   **【論点 7-B】両 fixture の witness と結論**

   凍結済み fixture の置換三つ組($\sigma_0$ は $10$-巡回)に対し、補題 R1-N∞-W 2. の 10 候補を悉皆すると **(35.4) の解は各 fixture でちょうど一つ**存在する。one-line・0-indexed で

   $$ g_{\rm sq}=[1,0,3,8,5,6,7,4,9,2],\qquad g_{\rm ns}=[6,3,2,7,8,1,4,5,0,9] \tag{35.5} $$

   いずれも $\boxed{g_i^2=\sigma_{1,i}}$((35.6))を満たし、補題 R1-N∞-W 3. と整合する。素朴述語 (35.3) の解は両 fixture で存在しない(補題 R1-N∞-W 4. の通り、これは dessin に依らない)。

   > **出所と状態札**: (35.5) の初出は **Sol 便 35 (35.5)**(`sol/sol_reply_35_freeze1r4.md` F1.5・紙上検分)。**数学者側で独立に再現した**(§0.4-4: 入力は `certificates/k5fixture/K5-{sq,ns}.json` の `perm_triple` のみ、方法は $g(0)$ による 10 候補悉皆、実装は Sol と非共有)。**二つの独立導出が一致 = cross-checked。`verified`(Lean)ではない。**
   > 参考記録(幾何的解釈を付けない生データ): $g_{\rm sq}$ の巡回型は $4+4+2$、$g_{\rm ns}$ は $4+4+1+1$。**$\operatorname{Fix}(g_i)$ を「$\iota$ の不動点数」と読んではならない** — $m$ が底の基点を動かすので $g_i$ は $\iota$ と基点復帰経路の合成であり、$\operatorname{Fix}$ に直接の幾何的意味はない。

   $$ \boxed{\ \textbf{結論: 両 fixture で補題 R1-N}\infty\textbf{-S 3. の必要条件は充足される。ゆえに対偶による (N}_\infty\textbf{) の排除は不可能。存否は UNKNOWN。}\ } $$

   **ここから「(N$_\infty$) が発火する」とまでは言えない**(必要条件が満たされただけである)。**規則面の帰結は「(N$_\infty$) を live 枝として全工程で扱う」の一点**に尽きる。

   **【論点 7-C】残る鋭化の余地 — launch blocker ではない**

   排除路線は 3. では閉じたが、補題 R1-N∞-S 4.(**$\iota$ の 6 個の不動点が $\operatorname{Fix}(m)=\{\pm1\}$ へ写る**)からの必要条件はまだ使い切っていない。**現時点では UNKNOWN**であり、閉じる義務も予算も置かない。閉じたい者のための定式化だけ残す:

   - $\iota$ は $\lambda^{-1}(1)$(6 点・分岐指数 $2,2,2,2,1,1$)を保ち、その上での不動点は Weierstrass 点である。$g_i$ が $\sigma_1$ の巡回に誘導する置換($g_i$ は $\sigma_1$ を中心化するので巡回を置換する)と、$\lambda^{-1}(-1)$(10 点・不分岐)への作用の不動点数の和が **ちょうど 6** でなければならない。**この「和 = 6」を $g_i$ から純組合せ的に読む正しい規約**(基点復帰経路の寄与の扱い)は本 v1.3 では確定していない。
   - **安価な不変量は無力(v1.2 の観察は不変)**: $\sigma_0,\sigma_\infty$ はともに $10$-巡回なので巡回型は自動一致、$\operatorname{sgn}(\sigma_1)=+1$ も関係式から自動。**巡回型・パリティ水準の検査に予算を割かないこと。**
   - **v1.2 の保守的判定 $T$ は (35.4) に置き換えられた**(超越されたので、以後 $T$ は使わない)。$T$ 自体は健全な**十分条件**だったが、(35.4) の witness が実在する以上 $T$ も「判定不能」を返す。

### 11.1 v1.3 時点で残る未充足項目(凍結 1 受理の前提)

| # | 項目 | 担当 | 状態 |
|---|---|---|---|
| R-1 | §8.6/§10-3 の実装版・commit・checker ID を**値として**記入 | 実装(P6 後半) | **未**(便 35 F4: 版表・付録 A・本節の自己申告が現物と食い違う。**実 commit を値として埋め、全修理後に再 hash**) |
| R-2 | 本文書 + 付録 A の新 digest 再取得と再提出 | 司令塔(P7) | **未**(**v1.3 で serialization が三たび変わる**) |
| R-3 | 親 manifest 側の whitelist/stop に I-b と同語を反映 | 司令塔(P1+P3) | **実体は閉(便 37 F4.1・裁定 38・2026-07-27・Sol 検分済み)**。`docs/manifest_k5_v1.md` **v1.4** の whitelist(§3)・即時 stop 行はいずれも「$\hat c_\mu$ の値・平方類・平方因子・符号」の四語を逐語列挙する(Sol 便37 F4.1 が「R-3 の実体部分は閉じた」と判定)。**残る留保**: $\mu$/Pell の sealed automation・(N$_\infty$) 探索器未設計中の非開示規則が変更記録の一段落にしかなく、operative 節(Model-Builder 委嘱・S5 工程節)への転記が探索解禁版までの宿題として残る(便37 F4.2・単独では本条件を FAIL にしない)。 |
| R-4(v1.2) | S5 設計 §3.3.4 の分離条件表に **N-0: $P_0\ne\iota(P_\infty)$** を追記し、(3.3) の $x_0$ 有限前提を明示し、**(N$_\infty$) の stratum を total な分岐表に入れる**(便 34 F3.3・便 35 F5.1) | 数学者 | **閉(2026-07-27)** — `docs/week4-K5_S5設計_opus_v1.md` **v1.2** §3.3.4 の N-0 と §3.3.5(命題 S5-3∞・(3.3∞)・total 分岐表)。**Rule 1 の受理条件ではない** |
| R-5(v1.2) | 実装側: 経路 A/B/第三 checker を副枝 (N$_\infty$)(§6.1 (b) A∞-1〜A∞-4・§6.2 B-iii・構造検査 (N∞-1)–(N∞-4)・(N$_\infty$) 用 raw schema §6.3-6)へ拡張 | 実装 | **production 較正済み(便 36 F3.2/F6-1・裁定 37 条件 1・2026-07-27)**。schema v2 へ更新(三値 branch label `N_infty`・`M`(旧 `n` を置換)・`model_digest`・`expected_model_digest`)。`search/u-extract-pathA.g` の `ExtractPathA_Ninf` に (N∞-1)–(N∞-4) の fail-closed 検査(deg A=M・deg B=M-3・$b_{M-3}=a_M\ne0$・$A^2-B^2f$=定数=1・必要級数長 $\ge 2M+4$)と `gcd(f,f')` が単元であることの exact 検査(GAP 側 `PolyGcdIsUnit`・node 側は独立実装の Euclid 互除法)を追加。**Sol 提供の exact synthetic fixture**($p=x^2+1$・$a=1+x(x^2+1)^2$・$f=x^6+2x^4+x^2+2x$・$\lambda=\mu^2$ で $\deg A=10$・$\deg B=7$・$b_7=a_{10}=2$・$\hat c=1$)で `search/u-extract-pathA-ninf-production-driver.g` + `crosscheck/u-extract-pathB-ninf-production-driver.mjs` + `crosscheck/u-compare-ninf.mjs`(第三 checker・R-7 の expected digest 束縛も同時実装)を実行し、$u^{(A)}=u^{(B)}=1/4$・`result:"ACCEPT"`・digest 一致を確認(実行ログは本裁定対応の便報告に原文記載)。旧 M=3 玩具は `search/u-extract-pathA-ninf-toy-driver.g`/`crosscheck/u-extract-pathB-ninf-toy-driver.mjs` として**同一ライブラリの unit test**に位置づけ直し(schema v2・chat=1 の passing fixture に更新)、旧 chat=2 入力での fail-closed 停止は `crosscheck/check-r5-r8-ninf-fail-closed.mjs`(11/11 PASS)で確認。詳細 `docs/week4-K5_Rule1_impl_versions.md` §9.3 |
| **R-6**(v1.3) | `ninf-exclusion*.json` の `ninf_excluded=true` を**撤回**し、**(35.4) 述語**で証明書を再発行する。結論は「**対称性条件 PASS・witness (35.5) を記録・(N$_\infty$) の存否は未決**」。補題 R1-N∞-W 2. により **10 候補の悉皆**でよい($10!$ 走査は不要)。撤回の事実自体も証明書に残す | 実装(数学者の検分必須) | **実装済(便 36・v3・裁定 37 で数学 PASS・文言修理済み・2026-07-27)**。`search/k5-ninf-exclusion.g`/`crosscheck/check-k5-ninf.mjs` を司令塔中継の補題 R1-N∞-W 仕様どおりに実装: 判定述語は (35.4) の E1・E2 のみ(第三式は **E1+E2** から自動 ⇒ 冗長確認として記録 — 便 36 F1.2 の文言修理: 「E1 だけから」ではない)、$\sigma_0$ が単一 10-サイクルであることを使う **10 候補の悉皆**(g(0)=c、$10!$/$3628800$ 通りの総当りは不要)。定理由来の自己検査は「解は**高々一つ**」(R1-N∞-W が実際に証明する範囲・便 36 F1.2 の文言修理)を integrity stop 条件とし、**0 survivors は理論に反しないため fixture corruption 扱いしない**(>1 のみ integrity stop)。$g^2=\sigma_1$ (35.6) は survivor が実在する場合の理論由来の self-check。$\sigma_0\sigma_1\ne\sigma_1\sigma_0$ の直接計算により旧述語 (35.3) が E1 のもとで恒真に充足不能であることも証明書内で自己完結的に示した。両 fixture で witness (35.5) と一致(GAP/node とも 20/20 PASS・cross-check 11/11 PASS、文言修理後も再実行して同結果を確認)。結論札は「排除されず・対称性充足・(N$_\infty$) の存否は UNKNOWN・witness は cross-checked」。旧証明書は `certificates/k5pipeline/retracted/`(撤回理由・(35.3)⇔(35.4)∧可換性の説明は同ディレクトリ `NOTE.md`) |
| **R-7**(v1.3) | §6.3-5: raw の `model_digest` を**凍結 bundle の expected digest に束縛**し、第三 checker で fail-closed に検査(**I-l**) | 実装 | **閉(便 37 F2/裁定 38 条件 1・2026-07-27)**。旧実装は `crosscheck/u-compare-ninf.mjs`/`u-compare.mjs` が raw 二本の**自己申告** `expected_model_digest` 同士を比較するだけであり、「二 driver が同じ誤転記をすれば ACCEPT する」攻撃(Sol 便37 F2)を防げなかった。修理版は両 checker とも**第三の独立引数**(bundle ファイル)を必須化した: (N$_\infty$) 副枝は `crosscheck/build-frozen-bundles.mjs`(pathA/pathB のどちらのコードとも独立な第三実装)が生成する `certificates/k5pipeline/{toy-ninf-M3,prod-ninf-M10}-bundle.json`(schema `k5pipeline/frozen-bundle/v1`)、主枝(W/N$_{\rm aff}$)は凍結済み model-spec ファイル自身(`certificates/k5fixture/K3-regression-model.json`・`bridge_mode: "calibration_pre_bridge"` を明記)を bundle 引数として渡す。checker は (i) raw から再構成した canonical model string が bundle の canonical model string と**逐語一致**すること、(ii) bundle 自身の canonical string から取り直した sha256 が bundle の `expected_model_digest` と一致すること(bundle 自己整合)、(iii) production/calibration モードでは `expected_model_digest` の欠落を必ず INTEGRITY_STOP にすること、を検査する。raw 内の自己申告 `expected_model_digest` は参考記録に格下げし、判定根拠には使わない。攻撃再現の adversarial 較正 `crosscheck/check-r7-bundle-attack.mjs`(二 raw に同一の誤転記+相互整合する誤 digest を仕込んでも、正しい bundle と照合すると INTEGRITY_STOP になることを確認・5/5 PASS)で閉を確認。 |
| **R-8**(v1.3) | §2.2 M0 / §6.3-6 / §9.2 **I-m**: 枝ラベルを三値 enumeration とし、**未知ラベルの既定値 fallback を禁止**(fail-closed) | 実装 | **閉(便 37 F3/裁定 38 条件 2・2026-07-27)**。便 36 時点の修理は無条件 Weierstrass fallback バグを除去したが、`branchP0` という**単一 field** に大域枝(M0 の三値 $\{{\tt W},{\tt N\_aff},{\tt N\_infty}\}$)と局所 $P_0$ の Weierstrass 性を混在させており、Sol 便37 F3 の指摘どおり型が正本と異なっていた。本便で二軸に分離: 大域 field `branch`(main-path raw では $\{{\tt W},{\tt N\_aff}\}$、$N_\infty$ raw では常に `"N_infty"`)と局所 field `P0_type`($\{{\tt Weierstrass},{\tt nonWeierstrass}\}$)。整合規則も fail-closed に実装: `branch='W'` は `P0_type='nonWeierstrass'` を要求(S5-W 補題・SS4.1「v1.2 の絞り込み」)、`branch='N_aff'` のみ両値を許す、$N_\infty$ raw の `P0_type` は与えられれば `'nonWeierstrass'` のみ許す(補題 R1-M0 3.)。schema 名(`u-pathA/v3`・`u-pathB/v3`・`u-pathA-ninf/v2`・`u-pathB-ninf/v2`)と枝ラベルの突合も第三 checker に追加。`crosscheck/check-r5-r8-ninf-fail-closed.mjs` で `branch='W'`+`P0_type='Weierstrass'` の拒否・`branch='N_aff'`+`P0_type='Weierstrass'` の受理などを含め 18/18 PASS。 |

> **本節の運用注(便 35 F4)**: 凍結物は task や裁定の説明文でなく、**hash された本文が正本**である。したがって本表の「未」は、実際に閉じたときに**本文で**更新し、その後に再 hash する。**「別便で閉じた」という外部説明で本表を上書きしない。**
>
> **Rule 1 の受理条件ではない項目**: R-4(閉)。**受理条件である項目**: R-1・R-2・R-3・R-5・R-6・R-7・R-8。

**現状(2026-07-27・便 37/裁定 38 修理反映後)**: R-3(実体は閉・Sol 検分済み)・R-4(閉)・R-5(production 較正済み)・R-6(数学 PASS・文言修理済み)・**R-7(閉・bundle 束縛へ修理)**・**R-8(閉・branch/P0_type 分離へ修理)**。**R-1・R-2 はなお未着手**(実 commit ID の値記入・全修理後の再 hash・本文書自身の再提出 -- これは実装担当ではなく司令塔の作業。commit 後に司令塔が本節・実装版表・付録 A の commit ID 欄を最終確認し、値として記入する)。

**R-1・R-2 が閉じ、かつ本文書の再 hash(R-2)が済むまで、凍結 1 は受理されず、個別モデル探索コマンドは実行しない。**

> **v1.3 の射程外(本文書が判定しないもの)**: 便 35 の blocker 4(第三 covariance の再実装 — $b_i,\tau_i,\rho_0,j_i$・actual local monodromy・$G_K$ 上の Kummer character・formal $a=1$ を同一 artifact 内で検査する)は**親 manifest 側の control** であり、Rule 1 の条項ではない(Rule 1 §8.4 は (5′) の量化子の規律だけを定める)。裁定 36 の配分どおり実装別便で閉じる。
