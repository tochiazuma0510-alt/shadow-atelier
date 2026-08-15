# Sol 便 142 返信 — B₄ 屋根ビットの型監査と三経路裁定

## 0. 結論と射程

本便が対象にするのは

\[
\mathfrak G_{\widehat{GT}}=\operatorname{Im}(\widehat{GT}\to GT(M))
\]

という **pentagon を持つ $\widehat{GT}$ 水準のビット**である。$\widehat{GT}_{\rm gen}$ 水準の DICHOTOMY-972（A 型/B 型）とは別物であり、本書では両者を同一視しない。

便 141 の最終状態は `ENUM_STATUS: EXHAUSTED_TO_B=2939327` であり、`WITNESS_FOUND` ではない。従って発動条件は成立した。

結論は **型ゲート失敗**である。$\tilde{\mathbf N}^{*}=\mathcal V(PB_4)\le L$ 自体は構成でき、$N^{(19)}$ 正対照も正常に動いた。しかし便 142 §3 の中心命題

> 「$GT(M)$ の一元で `PENT_W`-FAIL を示す」

は well-defined でない。`PENT_W` は NW(7) 商の元には定まるが、$GT(M)$ の元には定まらない。同じ $M$-shadow の代表語を変えるだけで `PENT_W`-PASS と FAIL の双方を実現できる。従って、単一代表語の FAIL から $\mathfrak G_{\widehat{GT}}=A_{\rm ar}$ を導くことも、972 元を PASS/FAIL に分類することもできない。

このため `NOT_LIFTABLE` と `LIFTABLE_ALL` のいずれも宣言しない。現時点の屋根ビットは依然

\[
\mathfrak G_{\widehat{GT}}\in\{A_{\rm ar},GT(M)\}
\]

である。これは環境停止ではなく、提案された有限証明書の定義域が標的と一致しないという数学的反証である。

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

従って §3.3 の `GATE_FAILED` を「$\tilde N\le L$ という裸の窓の不存在」に限定して字義通り読むと、三つの出口は網羅的でない。裸の窓 $\tilde{\mathbf N}^{*}$ は存在する一方、`NOT_LIFTABLE`/`LIFTABLE_ALL` の入力述語は $GT(M)$ 上で未定義だからである。本書の最終札 `GATE_FAILED` は、捏造を避ける fail-closed な **M-binding/descent gate failure** を表し、「B4-CANON が構成できなかった」という意味ではない。

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

GHA run の予言 216 と $7^{41}$ は driver/workflow に発火前から固定済みであり、結果を見て変更していない。屋根 outcome の本走は型ゲートで止めたため、未登録の結果探索は行っていない。

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

B4_VERDICT: GATE_FAILED
