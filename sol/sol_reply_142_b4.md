# Sol 便 142 / 142b 統合返信 — B₄ 屋根ビットの型監査と続行在庫

## 0. 結論と射程

本便が対象にするのは

\[
\mathfrak G_{\widehat{GT}}=\operatorname{Im}(\widehat{GT}\to GT(M))
\]

という **pentagon を持つ $\widehat{GT}$ 水準のビット**である。$\widehat{GT}_{\rm gen}$ 水準の DICHOTOMY-972（A 型/B 型）とは別物であり、本書では両者を同一視しない。

便 141 の最終状態は `ENUM_STATUS: EXHAUSTED_TO_B=2939327` であり、`WITNESS_FOUND` ではない。従って発動条件は成立した。

便 142 が指定した **単一の `PENT_W` 経路**には型ゲートの破綻がある。$\tilde{\mathbf N}^{*}=\mathcal V(PB_4)\le L$ 自体は構成でき、$N^{(19)}$ 正対照も正常に動いた。しかし便 142 §3 の中心命題

> 「$GT(M)$ の一元で `PENT_W`-FAIL を示す」

は well-defined でない。`PENT_W` は NW(7) 商の元には定まるが、$GT(M)$ の元には定まらない。同じ $M$-shadow の代表語を変えるだけで `PENT_W`-PASS と FAIL の双方を実現できる。従って、単一代表語の FAIL から $\mathfrak G_{\widehat{GT}}=A_{\rm ar}$ を導くことも、972 元を PASS/FAIL に分類することもできない。

このため `NOT_LIFTABLE` は宣言できない。さらに便 142b §1 の研究者裁定を受け、`LIFTABLE_ALL` と `GATE_FAILED` を**終端札としては撤回**する。型反証 PENT-NODESCENT は残るが、それは次の計器へ進む理由であって作業の終端ではない。現時点の屋根ビットは依然

\[
\mathfrak G_{\widehat{GT}}\in\{A_{\rm ar},GT(M)\}
\]

である。提案された一つの有限証明書の定義域が標的と一致しない、という数学的反証と、在庫全体の尽きたという主張を分ける。便 142b の在庫監査と続行指定は §8 以下に統合した。

## 1. 定理 PENT-NODESCENT — `PENT_W` は $GT(M)$ 上の述語でない

記号の衝突を避け、算術部分群を $A_{\rm ar}$、$\mathrm{PSL}(2,8)$ を $S$、NW(7) の二生成商を $P_7$ と書く。置くものは

\[
M_F=M\cap F_2,\qquad V=\gamma _5(F_2)F_2^7,
\]
\[
H_M:=F_2/M_F\cong PB_3/M\cong G_9\times S,\qquad
P_7:=F_2/V,\quad |P_7|=7^8,\quad |P_7'|=7^6=117{,}649.
\]

最初の直積同定は `docs/notes/triad972_canonical_addendum_v2.md` §2–§3 と、便 141 が引用した D972 データによる。$M$ は中心 $\langle c\rangle$ を含むので $PB_3/M$ と $F_2/M_F$ は同じ marked quotient である。

### 1.1 共通商は自明

$P_7$ の任意の商は 7 群である。一方、$|G_9|=2916=2^2 3^6$ なので $G_9$ は非自明な 7 群商を持たない。非可換単純群 $S=\mathrm{PSL}(2,8)$ から 7 群への準同型も、核の単純性と位数から自明である。従って $H_M=G_9\times S$ と $P_7$ は共通の非自明商を持たない。

Goursat の補題により、二つの自然射の積は全射である:

\[
(\alpha,\beta):F_2\twoheadrightarrow H_M\times P_7.
\tag{1}
\]

同値に

\[
M_FV=F_2,\qquad
F_2/(M_F\cap V)\cong H_M\times P_7.
\tag{2}
\]

特に $M_F$ と $V$ は包含関係にない。

### 1.2 charming 代表元のまま NW residue を任意に変えられる

(1) を導来部分群へ制限すると

\[
(\alpha,\beta)([F_2,F_2])=H_M'\times P_7'.
\]

従って任意の $q\in P_7'$ に対し $(1,q)$ の逆像を $[F_2,F_2]$ 内に取れる。その逆像は $\ker\alpha=M_F$ にも属するから

\[
\boxed{\ \beta(M_F\cap[F_2,F_2])=P_7'.\ }
\tag{3}
\]

$M$-shadow の charming 代表語を $f\in[F_2,F_2]$ とする。任意の $q\in P_7'$ に対し、(3) から

\[
\beta(h)=\beta(f)^{-1}q,\qquad h\in M_F\cap[F_2,F_2]
\]

を選べる。すると $f$ と $fh$ は同じ $M_F$-coset、従って同じ $M$-shadow を表す一方、$fh$ の NW residue はちょうど $q$ である。

これは word-level の自由度だけではない。$M_{\rm ord}=18$、NW(7) の $N_{\rm ord}=7$ なので、任意の二つの $m$-class は中国剰余定理で同時に持ち上がる。(2) 上では hexagon は成分ごとに成立し、二因子に共通非自明商がないため二つの全射成分を持つ $T_{m,f}$ の像も Goursat により直積全体である。従って **各 $g\in GT(M)$ と 294 個の各 NW(7) shadow は、共通細分 $M\cap\mathbf N$ 上で compatible** である。内訳は各 $g$ について `PENT_W`-PASS の有限 B3 common-refinement 42 個、FAIL の有限 B3 common-refinement 252 個となる。これは $\widehat{GT}$ lift の存在主張ではない。

`PENT_W` は $q=1$ では PASS し、BIT-252 の $q_*$ では FAIL する。従って **各 $M$-shadow は PASS 代表元と FAIL 代表元の双方を持つ**。特に BIT-252 の FAIL shadow の $m$-class を $m_*$ とし、$\mu\equiv0\pmod {18}$、$\mu\equiv m_*\pmod7$ を選べば、恒等 shadow $[0,1]_M$ についてさえ、ある $h\in M_F\cap[F_2,F_2]$ が

\[
[\mu,h]_M=[0,1]_M,\qquad [\mu,\beta(h)]_{\mathbf N}\in GT(\mathbf N),\qquad \mathrm{PENT}_W(\beta(h))=\mathrm{FAIL}
\]

を満たす。単一代表語を使う規則なら、$\widehat{GT}$ から来ることが自明な恒等元まで「非持上げ」と誤判定する。これは提案された規則に対する陰性対照である。

### 1.3 B4-DIR の正しい型

B4-DIR は、**同じ NW(7) residue を固定した** $B_4$ 窓 $\tilde N\le L$ において

\[
\mathrm{PENT}_W\text{-FAIL}\Longrightarrow (2.20)\text{-FAIL}
\]

をいう。これは NW shadow の有限非持上げ証明書であり、互いに比較不能な商 $M$ の coset へ FAIL を押し下げる定理ではない。HSP-SOUND、PENT-NORM、PENT-FORM/PENT-FORM′ のいずれも、この欠けた比較射を供給しない。

従って便 142 §3 の

\[
\text{「$GT(M)$ の一元でも `PENT_W`-FAIL」}
\]

は型不正である。正しい陰性証明書は、$M$ へ reduce する一つの細かい $B_4$ 窓で、対象 $M$-shadow の **全 reduction fiber** が空または (2.20)-FAIL であることを示す必要がある。一つの選択 lift の FAIL では足りない。

## 2. 必須窓ゲート

B4-CANON により

\[
\tilde{\mathbf N}^{*}=\mathcal V(PB_4)=\gamma _5(PB_4)PB_4^7\le L,\qquad
|PB_4/\tilde{\mathbf N}^{*}|=7^{41},\qquad
\tilde{\mathbf N}^{*}_{PB_3}=\mathbf N_0
\]

は成立する。したがって「$W$ 感度を持つ窓が存在しない」のではない。しかし

\[
\mathbf N_0\cap F_2=V,\qquad M\cap F_2=M_F,\qquad M_FV=F_2
\]

なので $\mathbf N_0$ と $M$ は比較不能である。ゆえに $\tilde{\mathbf N}^{*}$ から $M$ への reduction map はない。$\tilde{\mathbf N}^{*}$ 上の (2.20) 評価器へ、便 141 の 972 coset の代表語をそのまま入力する操作は quotient map ではなく任意の section であり、§1.2 の反例を受ける。

抽象的には

\[
C_M:=\bigcap_{i=1}^4p_i^{-1}(M),\qquad
\tilde K:=C_M\cap\tilde{\mathbf N}^{*}\le L
\tag{4}
\]

を作れる。$\tilde K_{PB_3}\le M$ なので、これは今後の **typed な**候補窓である。ただし $C_M$ 側の追加条件を含む全 fiber の charming・hexagon・SURJ・(2.20) を列挙した成果物は存在しない。NW residue 一個を選ぶだけでは (4) の fiber 全体を調べたことにならない。

従って旧 §3.3 の `GATE_FAILED` を「$\tilde N\le L$ という裸の窓の不存在」に限定して字義通り読むと、三つの出口は網羅的でない。裸の窓 $\tilde{\mathbf N}^{*}$ は存在する一方、`NOT_LIFTABLE`/`LIFTABLE_ALL` の入力述語は $GT(M)$ 上で未定義だからである。便 142b により `GATE_FAILED` は終端札から削除する。残す正確な中間結論は **M-binding/descent が無いので、この一経路は A/B を判定しない**という PENT-NODESCENT だけである。

## 3. 指定三経路を全て試した結果

| 経路 | 実行したこと | 停止点 | 次に必要な有限品 |
|---|---|---|---|
| 紙路 | $H_M$ と $P_7$ の共通商を Goursat で監査し、(3) を導いた | `PENT_W` は $GT(M)$ 上へ降下せず、恒等 shadow にも FAIL 代表元がある | (4) の reduction fiber 全体を拘束する新しい entanglement 定理。単一代表語・canonical word は代用品にならない |
| 機械路 | 既存 `p1_build_R.g` と `b4-cal.yml` を GHA 発火し、$\tilde{\mathbf N}^{*}$ と $N^{(19)}$ 計器を再走した | $R_7=PB_4/\mathcal V(PB_4)$ は W 商だけで、$M$ 入力を受ける map がない。`DirectFactorsOfGroup` の成否はこの型欠落を直さない | producer で (4) を構成し、648 個の外側 coset ごとに **全** lift を列挙。独立 checker は marked quotient、reduction、fiber 完備性、hexagon/SURJ/(2.20) を helper 非共有で再構成 |
| 較正移植路 | `cal_b4_n19_pentagon.g` の GHA 正対照と、Dolgushev らの Package GT による独立 Python 再計算を実行 | 評価器は正常だが、その入力型は NW/B4 quotient の元である。$M$ の任意代表語への適用は section 依存 | `search/probe/b4_m972_v1/m972_b4_fiber.g` 型の producer と `crosscheck/check_b4_m972_fiber.py` 型の独立 checker。入力は $M$ の marked quotient、五余面、$R_7$、(4)、972 shadow の coset ID |

ここで提案した二つのファイル名は必要品の仕様名であり、本便では実装していない。Sol の役割境界上、型が閉じる前に探索器を新造して数を出すことはしない。

## 4. 陽性対照・GHA・独立照合

### 4.1 新規 GHA run

- workflow: `.github/workflows/b4-cal.yml`
- event: `workflow_dispatch`
- run id: **31883177663**
- head SHA: **38077214814f52fd8d85d4704e6ed6c16a45e267**
- workflow conclusion: success
- `anupq_smoke`: success
- `cal_b4`: success（fail-closed marker gate）
- `p1_build_R`: wrapper job success。ただし raw GAP は $|R_7|=44567640326363195900190045974568007=7^{41}$、`B4-EXQ-1: true`、$|Z(R_7)|=3909821048582988049$ まで印字した後、`DirectFactorsOfGroup` で 6 GB 上限に達した。`P1_PASS/P1_FAIL` marker は未到達で、B4-EXQ-2 は UNKNOWN
- 発火前から凍結されていた予言: $N^{(19)}$ pentagon-pass $=216$、B4-EXQ-1 $|R_7|=7^{41}$

ローカル `gap.ps1` は GAP 起動時の Windows signal-pipe error 5 で走らなかったが、そこで停止せず GHA を発火した。従って本判定はローカル環境を理由にしていない。

### 4.2 $N^{(19)}$ の独立正対照

GHA の GAP producer は、`cal_b4_n19_pentagon.g` 内の二方式で pentagon-pass **216 / 216** を再現し、job の fail-closed gate を通過した。さらに

```powershell
$answer = 'no'; $answer | python search\probe\wac_v1\pent_thirdparty_gt_run.py
```

を実行し、Dolgushev–Le–Lorenz–Zackey の Package GT 自身の `penta/hexa1/hexa2/generWF2` から独立に

```text
N19 ind4                         216
N19 indF2                       7776
N19 pentagon f-count             216
N19 f with some hexagon m         36
N19 total (m,f) hexagon pairs     72
```

を得た。GAP 計器と third-party Python は pentagon-pass 216 で一致したので、この陽性対照は **照合済み**である（Lean certificate はなく `verified` とは呼ばない）。Python が一時生成した root 直下の JSON は値と SHA-256 を読んだ後、作業契約に従い削除した。第三者 run の一時 JSON SHA-256 は `f71ae870ab56b14f177802249666280f5c111bc40ec14aa9c3b28a8296349e29` である。

この正対照が示すのは **評価器が壊れていないこと**であり、$GT(M)$ への比較射が存在することではない。

## 5. raw と verdict の分離

### raw

1. $|GT(M)|=972$、$|A_{\rm ar}|=324$、指数 3。
2. $H_M\cong G_9\times\mathrm{PSL}(2,8)$、$P_7$ は 7 群。
3. $M_FV=F_2$、かつ $\beta(M_F\cap F_2')=P_7'$。
4. 各 $M$-shadow は NW(7) の 294 shadows 全てと有限 B3 共通細分上で compatible であり、内訳は PASS 42 / FAIL 252（genuine lift の計数ではない）。
5. $\tilde{\mathbf N}^{*}\le L$、$|PB_4/\tilde{\mathbf N}^{*}|=7^{41}$、ただし $\tilde{\mathbf N}^{*}_{PB_3}=\mathbf N_0$ と $M$ は比較不能。
6. $N^{(19)}$ pentagon-pass 216 は GAP/Package GT で照合済み。

### verdict

- `PENT_W`-FAIL の有限証明書性は **NW shadow に対して有効**。
- `PENT_W`-FAIL は **$M$-shadow の代表元不変な述語ではない**。
- 外側 648 元の一つを非持上げとする typed witness は本便で 0 件。
- 972 元を `PENT_W`-PASS とする typed enumeration も本便で 0 件。
- 従って $\mathfrak G_{\widehat{GT}}=A_{\rm ar}$ も $GT(M)$ も導かない。

`LIFTABLE_ALL` 分岐に入っていないため、FAKE-KILL$^{B_4}$ の前件表は発火しない。本便が新たに充足した前件は IH-S / GEN$^{B_4}$ / PR$^{B_4}$ / CHM$^{B_4}$ のいずれにもない。有限窓 PASS は GEN$^{B_4}$ を含意しない。

## 6. $\widehat{GT}$ と $\widehat{GT}_{\rm gen}$ の分離

もし typed な (2.20)-FAIL fiber 証明書が得られれば、それが閉じるのは **$\widehat{GT}$ 水準**であり、井原予想へ渡す際に (U-10) を要しない。この点は便 142 §4 の通りである。

しかし本便で見つかったのはその証明書ではなく、証明書候補が $GT(M)$ 上へ降下しないという反証である。従って

- $\widehat{GT}$ 屋根ビット: **未決のまま**（本書の直接対象）
- $\widehat{GT}_{\rm gen}$ の A/B ビット: **別問題であり、本便から変化なし**

である。両者を混ぜて FAKE-KILL を発火しない。

## 7. 規律・provenance

### 7.1 prospective / noncontact / NAME-COLLIDE

GHA run の予言 216 と $7^{41}$ は driver/workflow に発火前から固定済みであり、結果を見て変更していない。便 142 の単一経路では屋根 outcome を測らず、便 142b では既存成果物に対する在庫監査だけを行った。未登録の outcome 探索は行っていない。

- sealed three quantities: opened = false
- $u$: opened = false
- $c$: opened = false
- sealed K5: opened = false
- NAME-COLLIDE: $A_{\rm ar}$ は算術部分群、$S$ は $\mathrm{PSL}(2,8)$、$P_7$ は NW(7) 二生成商、$R_7$ は $PB_4/\mathcal V(PB_4)$。既存の $P,Q,R,A$ と混同しない

### 7.2 novelty grep 領収書

新規性は主張しない。着手時 grep は次の通り。

```text
PENT_W.*代表元|代表元.*PENT_W       0 files
M_F.*PENT_W|PENT_W.*M_F             0 files
B4_VERDICT                           2 files
共通非自明商|Goursat               101 files
```

最後の 101 files が示す通り Goursat 機構自体は既在である。本書の役割は、その既在機構を便 142 の比較型へ適用して fail-closed に裁定することだけである。

### 7.3 入力 SHA-256

| 入力 | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_142_b4.txt` | `eec95626db1e06c02d5c01d15ec478367246b296bf70366214f0b1cb07c5e78d` |
| `sol/sol_reply_141_enum.md` | `1f9f390552b945c56587cb96270b04bd8f6a1f67ddd361b1b9f2ffbf2a98587e` |
| `docs/notes/b4_direct_adjudication_feasibility_v1_2.md` | `7d1f882da75fce8fddaa2303afb8fb0515231771a15984d61718175c35bee990` |
| `docs/notes/triad972_canonical_addendum_v2.md` | `5dc660dd0023bf9b1986cefa65ec9947ad5b3b366f210933dbe09ac2544c7659` |
| `search/probe/b4_cal_v1/cal_b4_n19_pentagon.g` | `023f8187aad8ccfb0cce3d861c8f720a064ed55875832f6980f9d2ced1d4d517` |
| `search/probe/wac_v1/pent_thirdparty_gt_run.py` | `d5ece6af4baee4afbfdbfdb8e9d3dbdb7481231a9a29fb6df5b85b02af1797e9` |
| `search/probe/b4_cal_v1/p1_build_R.g` | `9a97767fc81b134477f72bf13b1def05a8afb1f77071493822f04e7a9c145998` |
| `search/certs/cal_b4_integrated_v2_20260806.json` | `71b6fa73b99c4afafc624df844bda61d654248908bc813a4651864d603d44f1b` |

本便では commit / push を行っていない。`.git` は read-only とし、外部状態の変更は上記 workflow dispatch 1 回だけである。有限悉皆 $N^{(19)}$ と、本件特有の quotient 定理を族定理とは呼ばない。

## 8. 便 142b の受領と終端規則の差し替え

- 追補入力: `ops/inbox_codex/sol_task_142b_noexit.txt`
- SHA-256: `3d6227903fa4cb0d66692e6575ad72e1dd222a0a701e074e572237ce4859375b`
- 処理順: §0 → §1 → §2 → §3 → §4 → §5

研究者裁定を字義通り受領する。本書で受理終端になり得るのは、次のいずれかを伴う 972 屋根の A/B 決着だけである。

1. $GT(M)\setminus A_{\rm ar}$ の一元について、有資格な isolated 細分の reduction fiber が空である。
2. cofinal な isolated 細分族について reduction が全射であることを族定理で示す。

便 142 の PENT-NODESCENT、有限窓での全通過、窓の不発見、局所的な 972 全射はどれもこの二条件ではない。従って本追補では `SETTLED_A`、`SETTLED_B`、`NOT_LIFTABLE` のどれも書かない。また、以下に未消化在庫があるので「不可能」「もう手がない」とも申告しない。

## 9. 在庫 1–8 の逐項監査

| # | 状態 | 実行済みの生値・紙結論 | 未消化部分 |
|---:|---|---|---|
| 1 | **未消化** | GHA run `31883177663` で $R_7=PB_4/\mathcal V(PB_4)$、$|R_7|=7^{41}$、$|Z(R_7)|=7^{22}$、B4-EXQ-1=`true` まで到達 | `DirectFactorsOfGroup` の 6 GB 死より前へ分岐し、自然射 $PB_4\twoheadrightarrow R_7$ と五余面を保持して full (2.20) を直接評価する工程は未実行 |
| 2 | **未消化** | `cal_b4_n19_pentagon.g` は $N^{(19)}$ で C-1–C-6e を通し、pentagon 216 を二方式で一致させた | $M$ は $B_3$ 窓であり、そのまま `PaB.py` / (2.20) の target にはならない。移植先を (4) の $\tilde K=C_M\cap\tilde{\mathbf N}^{*}$ と型付けし、全 reduction fiber を走査する移植は未実行 |
| 3 | **未消化** | Prop 3.3、CORE-4、B4-MONO の紙機構は存在する | $\tilde K$ から source kernels を全数作り、Prop 3.3 の交叉で isolated 化し、$GT(M)\setminus A_{\rm ar}$ の 648 元ごとに survival を測る工程は未実行 |
| 4 | **未消化** | 正しい母集団は `[192,1489]` と `[192,1490]` の各 2 epi、計 4 窓。各群で B4 全射三つ組 768、$|\operatorname{Aut}G|=384$、2 軌道、$\psi(PB_4)\cong Q_8$、$\operatorname{ord}(\psi(\sigma_i))=8$、$\Delta_4^2$ の kernel bit は 384/384 | $N_{PB_3}$、$N_{\rm ord}$、charming/hexagon/SURJ、pentagon、source kernel、settledness は全て未評価 |
| 5 | **消化** | Package GT 本体の `penta/hexa1/hexa2/generWF2` をローカル checkout から実行。$N^{(19)}$ で `ind4=216`, `indF2=7776`, pentagon $f=216$, hexagon を持つ $f=36$, $(m,f)=72$。GAP 側の 216 と一致 | これは C-8 の第三者**較正**を消化したもの。項目 1–4 の $M$/新窓評価を代行したとは数えない |
| 6 | **消化** | MIRROR-SHADOW-B4 は紙で成立し、FIXED-B4 により $\tilde{\mathbf N}^{*}$ と $\tilde{\mathbf N}_{\rm core}$ は $\iota$-固定。下記 §9.2 により 4 個の $Q_8$ 窓も固定 | 現用 6 窓に distinct mirror partner はなく、この線から非持上げ元は出ない |
| 7 | **未消化** | ISO-FIBER-ENUM は $1\le B\le2|Q|-1=2{,}939{,}327$ を完走。class 1（$L=M$）、image 972、zero fiber 0 | event $B=2|Q|=2{,}939{,}328$ の central $C_2$ extensions、surjective marked orbit、$B_3$-安定性、isolatedness、reduction image は未実行。その後の kernel order $3,4,\ldots$ も未実行 |
| 8 | **未消化** | 四命題の入力・量化・出力は便 140 §4.2 で定式化済み。STRICT-D-140 は ABSORB-BC 単独では REL-VANISH を導けない抽象反モデルを与える | `CHIEF-COFINAL-140` / `REL-VANISH-140` / `GEN-NONCOVER-140` / `CHAR-LIFT-140` の同一 cofinal family 上での証明は 0 本 |

### 9.1 項目 4 の母集団訂正

追補本文の「1492/1494 も $Q_8$ 商」という読みは、修復 cert と独立第二系統に反する。`search/certs/b4_r0_probe_v2_p2fix_20260806.json` では 1492/1494 の実際の epi image は `[8,5]\cong C_2^3` で可換、`is_window=false` である。P2 の abstract normal-subgroup census に $Q_8$ が存在することと、具体的 epi の $\psi(PB_4)$ が $Q_8$ であることを同一視してはならない。

従って評価対象は

\[
(1489,\mathrm{epi} 1),(1489,\mathrm{epi} 2),
(1490,\mathrm{epi} 1),(1490,\mathrm{epi} 2)
\]

の四つに固定する。候補発見自体は GAP cert と、生 Cayley 表から GAP の判定 helper を共有せず再構成した Python 系で一致している。しかし `scope_declaration.gtshadow_predicates=false` なので、存在確認を shadow/pentagon 評価へ昇格させない。

### 9.2 項目 6 の消化 — Q8 四窓も鏡映固定

$\psi:B_4\twoheadrightarrow G$ を四窓の一つとし、$N=\ker\psi$ とする。$\psi\circ\iota$ も同じ $G$ への全射であり、

\[
\Delta_4^2\in\ker(\psi\circ\iota)
\iff \iota(\Delta_4^2)=\Delta_4^{-2}\in\ker\psi
\iff \Delta_4^2\in\ker\psi .
\]

独立第二系統の全数表では、1489 と 1490 のそれぞれについて全射 768 本がこの bit で 384/384 に分かれ、各片がちょうど一つの $\operatorname{Aut}(G)$ 軌道である。従って $\psi\circ\iota=\alpha\circ\psi$ となる $\alpha\in\operatorname{Aut}(G)$ があり、

\[
\iota(N)=\ker(\psi\circ\iota)=\ker(\alpha\circ\psi)=N.
\]

よって四窓も全て $\iota$-固定である。これは orbit の有限全数照合と紙の一行を組み合わせた結論であり、Lean certificate はない。MIRROR-SHADOW-B4 の $[-1,1]$ は各窓で settled となるため、distinct twin を供給しない。これをもって項目 6 を消化する。

## 10. 未消化項目の障害名・独立経路・発火要求

### 10.1 B4 側（1–4）

1. **`R-EPIMORPHISM-142B`（項目 1）**: 現 driver は `Pq` 後の abstract pc group $R_7$ だけを使い、full pentagon に必要な五つの marked coface map を保存していない。`DirectFactorsOfGroup` は判定に不要なので外す。GHA 用 producer は 117,649 個の $P_7'$ 元について direct (2.20)、$\tilde D$、`PENT_W` を別欄で出し、層 $S_0/S_1/S_2$ の分母と通過数を保存する。独立路は 41 座標の pc presentation・collector relations・五余面の生成元像を lossless export し、独立 Python pc collector で再評価する。既存の `PENT_W` / $\tilde D$ 集計は別 invariant の照合に回す。
2. **`M-ARITY-142B`（項目 2）**: $M$ は arity 3、(2.20) は arity 4 なので、移植先は裸の $M$ でなく $\tilde K=C_M\cap\tilde{\mathbf N}^{*}$ でなければならない。producer は 972 target IDs と $\tilde K\to M$ の全 fiber を列挙する。checker は marked quotient、五余面、fiber 完備性、hexagon、SURJ、pentagonを helper 非共有で再構成する。
3. **`PROP33-SOURCE-ENUM-142B`（項目 3）**: Prop 3.3 の交叉は、連結成分の source objects を列挙して初めて有限レシピになる。各 source kernel、交叉前後の index、isolated certificate、648 外側元の fiber 分布を出す。独立路は CORE-4 の四 forgetful maps を生成元上で再構成して kernel equality を照合する。
4. **`R0-GTSHADOW-142B`（項目 4）**: 既存 cert に必要なのは四 epi の generator images の lossless export。各窓について `(ind4,ind3,indF2,N_ord)`、pentagon $f$ 数、full hexagon $(m,f)$ 数、charming shadow 数、source-kernel orbit、settled 数を GAP と Package GT の二経路で出す。1492/1494 を $Q_8$ 窓として混入させる run は fail-closed とする。

### 10.2 B3 側（7–8）

5. **`C2-MARKED-EVENT-142B`（項目 7）**: $Q=G_9\times\mathrm{PSL}(2,8)$ の central $C_2$ extension classes を extension-over-$Q$ 同型で列挙し、各 class の $PB_3$ marking lifts を base map 固定 automorphism で orbit 化する。各 orbitに対して $B_3$-安定性、isolatedness、$|GT(L)|$、$|\operatorname{Im}R_{L,M}|$、zero-fiber IDs を順に出す。主路は GAP の cohomology/extension presentation、独立路は normalized 2-cocycle と Cayley closure の自前 checker とする。kernel order 3 以後は event ごとの versioned checkpoint を要する。
6. **`COFINAL-FOUR-142B`（項目 8）**: `CHIEF-COFINAL` は単に $\mathcal U=\mathcal I_M$ と置く循環的な形では計算族を供給しない。restricted かつ enumerable な同一族 $\mathcal U$、各 chief step の relative complex、relation affine space、proper-submodule bad loci、charming representative の compatibility map を明示し、その上で四命題を同時に証明する必要がある。反対向きの実例が出た段は項目 7 の zero-fiber 候補へ戻す。

これらは環境を理由にした停止申告ではなく、GHA / PackageGT / SmallGroups に渡す入力・出力の型指定である。本追補では新規 workflow dispatch は行っていない。次便での優先発火は、最小有限宇宙を持つ項目 4、その後に項目 7 の $C_2$ event、並行して項目 1–3 の typed $\tilde K$ 建造とする。

## 11. provenance と最終勘定

| 入力 | SHA-256 |
|---|---|
| `search/certs/b4_r0_probe_v2_p2fix_20260806.json` | `eb62d2bb1a884dd36e525e55f2580df8215279a311717b0f903f7f276e09a024` |
| `docs/notes/b4r0v2_second_system_verification_v1.md` | `3912a295152e1dcb51f34678349f824b9c697bd60cb8d19d5a3ad9f9f312b75a` |
| `docs/notes/b4_mirror_transfer_design_v1.md` | `3f898e6ba1f98f77280f3fadaade5fd2a3f064652cb8bfde1b8d9a4fc2212c28` |
| `search/certs/iso_fiber_enum_141_v2_20260815.json` | `cd4a30b4132aaad143faeb015593866c03cd511e58d6cea89917e5e33ffddc8c` |
| `sol/sol_reply_140_finish.md` | `3463fe6ca0d876b2b512a270e907c32ea82afa6183848c92de63fee8a0ba0da2` |
| `sol/sol_reply_141_enum.md` | `1f9f390552b945c56587cb96270b04bd8f6a1f67ddd361b1b9f2ffbf2a98587e` |

- 消化済み: **5, 6**
- 未消化: **1, 2, 3, 4, 7, 8**
- outside-$A_{\rm ar}$ の有資格 zero fiber: **0 件**
- cofinal 全射族定理: **0 本**
- A/B 決着: **未成立**
- `GATE_FAILED` / `LIFTABLE_ALL`: **終端札として撤回済み**
- 便 142b での変更対象: この統合返信のみ。commit / push / workflow dispatch なし

B4_VERDICT: INVENTORY_5_6
