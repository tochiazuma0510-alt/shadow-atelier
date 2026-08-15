# 返書 141 — ISO-FIBER-ENUM-140 の建造と最初の完全区間

- 対象: ops/inbox_codex/sol_task_141_enum.txt
- 実行日: 2026-08-15
- 入力 SHA-256: 7a93126f464491588256a944d948da8b5f583c9954c3145b8766895b49eeec18
- 着手中に観測した HEAD: ca41953e81a8892bb60516b2721d2cdad6f77a60
- 処理順: §0 → §1 → §2 → §3 → §4
- 証拠格: 紙上の有限群論と、Node producer / helper 非共有 PowerShell checker の有限照合。Lean certificate はない

## 0. 裁定の受領と本便の結論

便 140 への裁定を受領する。CONE-D-140 による自然な \(T_t\) の停止点除去、STRICT-D-140 による ABSORB-BC-139 単独路の閉鎖、便 137 の solver family の再収蔵という三点について異議はない。

本便では ISO-FIBER-ENUM-140 を未着手のまま停止していない。固定商

\[
 Q:=PB_3/M,\qquad M=K^{(9)}\cap N_{S4}
\]

について、全ての整数

\[
 1\le B\le 2{,}939{,}327
\]

を完全性証明書つきで走査した。生値は次のとおりである。

| 生値 | 結果 |
|---|---:|
| \(|Q|\) | 1,469,664 |
| 完走した最大 \(B\) | 2,939,327 \(=2|Q|-1\) |
| marked quotient class | 1 |
| proper refinement class | 0 |
| 唯一の class | \((Q,\pi_M,\mathrm{id}_Q)\)、従って \(L=M\) |
| \(|GT(L)|\) | 972 |
| \(|\operatorname{Im}R_{L,M}|\) | 972 |
| \(GT(M)\) 内の zero fiber | 0 |
| \(GT(M)\setminus A\) 内の zero fiber | 0 |

従って witness 停止は発火しない。一方、この有限完走を B 型の認定には用いない。本便で採る受理出口は EXHAUSTED_TO_B である。

## 1. ISO-FIBER-ENUM-140 の四段

### 1.1 列挙対象の型

段 1 と段 2 を接続するため、marked candidate を

\[
 (E,\phi,\psi),\qquad
 \phi:PB_3\twoheadrightarrow E,\quad
 \psi:E\twoheadrightarrow Q,\quad
 \psi\phi=\pi_M                                      \tag{1.1}
\]

と定め、marked isomorphism で割る。これが便 140 §4.1 で明記した型である。単に抽象群 \(E\) と \(\psi\) だけを列挙しても \(L=\ker\phi\) が定まらないので、(1.1) の compatibility は省略しない。

### 1.2 ORDER-FLOOR-141 と EVENT-GAP-141

> **命題 ORDER-FLOOR-141.** (1.1) を満たす有限群 \(E\) について
> \[
> |E|=|Q|\,|\ker\psi|.
> \]
> 特に \(|E|\) は 1,469,664 の正の倍数である。

これは有限群の準同型定理である。従って候補集合が変化し得る order event は

\[
 |Q|,\ 2|Q|,\ 3|Q|,\ldots                            \tag{1.2}
\]

だけであり、連続する event の間では全ての整数 \(B\) に対する bounded census が同一である。これを EVENT-GAP-141 と呼ぶ。この区間圧縮は sampling ではなく、各整数 \(B\) を覆う完全性証明である。

既存成果物に記録された二通りの位数評価は

\[
 |PB_3/K^{(9)}|\,|PB_3/N_{S4}|
 =2916\cdot504
 =1{,}469{,}664
\]

と、d972 Phase 0 の \(|PB_3/M|=1{,}469{,}664\) で一致した。

### 1.3 prospective prereg と昇順実行

結果 cert より先に、二つの区間を別々に凍結した。

| prereg | SHA-256 | 凍結区間 |
|---|---|---|
| search/certs/iso_fiber_enum_141_prereg_v1_20260815.json | 528725c89c372b1106a09ec5110ecb0621d199d9b6ae45c759758f32d279833a | \(1\le B\le |Q|\) |
| search/certs/iso_fiber_enum_141_prereg_v2_20260815.json | 22e33f6ba14a053b6ed8b0c52e6050b8756fdd4bfbf5df6853472c97022817b0 | \(|Q|<B<2|Q|\) |

昇順走査の生値は次のとおりである。

| \(B\) の区間 | admissible な \(|E|\) | 新規 class | 累積 class |
|---|---:|---:|---:|
| \(1\le B\le1{,}469{,}663\) | なし | 0 | 0 |
| \(B=1{,}469{,}664\) | 1,469,664 | 1 | 1 |
| \(1{,}469{,}665\le B\le2{,}939{,}327\) | 新規なし | 0 | 1 |

したがって 2,939,327 個の各 \(B\) に一ファイルを複製せず、候補集合が一定な二つの event interval を lossless に符号化した。各 \(B\) の漏れはない。

### 1.4 段 1 — BOUNDARY-MARK-141

> **命題 BOUNDARY-MARK-141.** \(|E|\le|Q|\) で (1.1) を満たす marked candidate は、marked isomorphism を除いて
> \[
> (E,\phi,\psi)=(Q,\pi_M,\mathrm{id}_Q)
> \]
> の一つだけである。

**証明.** ORDER-FLOOR-141 により候補があれば \(|E|=|Q|\)。従って \(\psi\) は同位数有限群間の全射なので同型であり、compatibility から

\[
 \phi=\psi^{-1}\pi_M
\]

が強制される。\(\psi\) 自身で canonical triple へ marked-isomorphic になるので、重複も未収録 class もない。∎

さらに \(|Q|<B<2|Q|\) では、新しい正の倍数がないため同じ一 class だけである。SmallGroups の不使用は候補取り落としではなく、この位数証明による全排除である。

包含記号を反射的な \(L\le M\) と読むとこの一件は base row である。strict refinement \(L<M\) だけを数える規約でも、当該範囲の候補数は 0 となり、以下の zero-witness 結論と完走上界は変わらない。

### 1.5 段 2 — \(B_3\)-安定性

唯一の candidate では

\[
 L=\ker\phi=\ker\pi_M=M.
\]

\(K^{(9)}\) と \(N_{S4}\) はともに \(B_3\)-安定な finite-index normal subgroup であり、交叉 \(M\) も \(B_3\)-安定である。従って段 2 は PASS である。proper refinement はこの到達範囲に存在しない。

### 1.6 段 3 — isolated certificate と settled 全数

isolated 性は二経路で確認した。

1. **構造路.** 正典 Thm 4.3 により \(K^{(9)}\) は isolated。search/certs/d972_h1_ns4_v1_20260813.json は \(N_{S4}\) の 54 / 54 shadow で kernel trivial、\(\#\mathcal C(N_{S4})=1\) を記録する。命題 INT により
   \[
   M=K^{(9)}\cap N_{S4}
   \]
   は isolated。
2. **直接全数路.** search/d972_phase0_v1.g は \(M\) の全候補を走査して 972 shadow を得た後、全 972 個について誘導 endomorphism を構成して \(972^2\) 個の composition table を閉じた。各 shadow は既に source-generation を通過しており、well-defined な有限全射 endomorphism は automorphism なので全 972 個が settled である。search/d972_phase1_v1.g の別再走も shadow 数 972 を与えた。

従って段 3 の生値は

\[
 |GT(M)|=|GT^{\mathrm{settled}}(M)|=972,\qquad
 \#\{\text{unsettled shadow}\}=0.                  \tag{1.3}
\]

である。

### 1.7 段 4 — reduction image

唯一の行は \(L=M\) なので

\[
 R_{L,M}=R_{M,M}=\mathrm{id}_{GT(M)}.
\]

従って判定語を入れない生値は

\[
 |\operatorname{Im}R_{M,M}|=972,\qquad
 \{\,|R_{M,M}^{-1}(g)|:g\in GT(M)\,\}=\{1\}.       \tag{1.4}
\]

全 972 元で zero fiber は 0、従って既知の 324 元部分集合 \(A\) の外の 648 元でも zero fiber は 0 である。witness 行はない。

### 1.8 producer / 独立 checker

| 成果物 | SHA-256 | 生値 |
|---|---|---|
| search/certs/iso_fiber_enum_141_v1_20260815.json | 4d1ffe562f2a98381358bd576d71c2b8d21d075bc404e798f73770a636c4f811 | \(B\le|Q|\)、class 1、image 972、zero fiber 0 |
| crosscheck/verdicts/iso_fiber_enum_141_check_v1_20260815.json | c9bbca94238a01f337dadd7d6a3b3aa1e82beffbac7f6c939597f26f88dce5cc | 独立位数積・INT 路、failure 0 |
| search/certs/iso_fiber_enum_141_v2_20260815.json | cd4a30b4132aaad143faeb015593866c03cd511e58d6cea89917e5e33ffddc8c | 継続 1,469,663 個の \(B\)、新規 event 0 |
| crosscheck/verdicts/iso_fiber_enum_141_check_v2_20260815.json | be2f651dab6e950b895a5ac9c4e4fcedef0ce8cf19b96ff103c5e5c2c7fdfc7c | next-multiple 独立計算、failure 0 |

producer は Node で public cert の値と event interval を処理した。checker は producer helper を import せず PowerShell の整数演算を使い、\(2916\cdot504\)、次の倍数、境界の marked 一意性、INT の前件、恒等 reduction を別順序で照合した。

陽性対照は二種である。

- \(|E|=|Q|-1\) および \(2|Q|-1\) を「全射候補」として注入し、非零 remainder により拒否。
- 恒等 image から一元を削った偽値 971 を注入し、codomain 972 との不一致を検出。

検出数は全 3 件、未検出 0 件である。

### 1.9 次の order event

新しい candidate が初めて現れ得る次の一点は

\[
 B=2|Q|=2{,}939{,}328.                              \tag{1.5}
\]

このとき \(|\ker\psi|=2\)。位数 2 の正規部分群への共役作用は自明なので、次に列挙すべき対象は \(Q\) の central \(C_2\)-extensions と、\(\pi_M\) を持ち上げる surjective \(PB_3\)-marking の orbit である。その後に \(B_3\)-安定性、isolated 性、reduction image を同じ gate 順で検査する。

これは BLOCKED の申告ではなく、今回の完全区間の直後にある最初の未処理 event の型指定である。

### 1.10 §1.3 の並行路

CHIEF-COFINAL-140 / REL-VANISH-140 / GEN-NONCOVER-140 / CHAR-LIFT-140 へは移らなかった。§1 の bounded enumeration 自体が停止していなかったためであり、優先度規則どおりである。

## 2. 資源の使用

GAP / GHA / SmallGroups は本到達範囲では発火していない。理由は環境でも計算量でもなく、ORDER-FLOOR-141 が抽象群を開く前に全候補を完全分類したためである。SmallGroups が初めて意味を持ち得るのは (1.5) の central \(C_2\)-extension event からである。

checkpoint は v1 と v2 に分け、既成結果を上書きせず、各 continuation の prereg SHA と親 cert SHA を固定した。

## 3. 規律

### 3.1 prospective / raw-verdict separation

- v1 prereg を v1 producer より先に、v2 prereg を continuation producer より先に作成した。
- prereg には候補宇宙、停止則、出力欄、陽性対照を固定した。
- 唯一の base row の image 972 は既開示値なので、新規 prospective discovery とは呼ばない。今回 prospective に固定した増分は bounded universe、完全性規則、停止則、および新規 proper candidate の件数である。
- cert は order、件数、fiber 数だけを持ち、A/B 判定と ENUM_STATUS を入れていない。
- 本文 §1.3–1.8 を生値欄とし、ENUM_STATUS は最終行に隔離する。

### 3.2 novelty receipt

初稿前に

    rg -n -S "ORDER-FLOOR-141|BOUNDARY-MARK-141|EVENT-GAP-141" \
      docs sol search crosscheck provenance ops \
      --glob '!sol_task_141_enum.txt' --glob '!sol_reply_141_enum.md'
    NO_PREEXISTING_HITS

を得た。これは名前の未出だけを示し、準同型定理や marked quotient の数学的優先権を主張しない。

### 3.3 provenance

| 既存入力 | SHA-256 |
|---|---|
| search/certs/d972_phase0_v1_20260813.json | dbd34c59638363762cee1eb77720625704935e50a269528df0f88daeaf3841fe |
| search/certs/d972_h1_ns4_v1_20260813.json | a100893d151b4f4885bab8d950d09fc9d7b875d5651481ae9496f6edc93c8292 |
| search/certs/d972_phase1_v1_20260813.json | b41c99684af7096af9b609077d2953ccd9b572d86b92ee871ff5e08cf291bb23 |
| search/d972_phase0_v1.g | 95dd7b45fef229cf54ae31c365701be64bb4abf569db7e5e7946d59750075783 |
| search/d972_h1_ns4_v1.g | 38fda9322d494f75e5eb382fee21777391aba4201b42349f6d4b760ffc525ab0 |
| search/d972_phase1_v1.g | a0796707cf43e9bc5f2bf4670299db2d6afe3b616ca13610f280e964e4b0f966 |

本便で作成したものは、指定返書、二つの prereg、二つの raw producer cert、二つの独立 checker cert の計 7 ファイルである。他の dirty / untracked file は変更していない。.git は read-only とし、commit、push、workflow dispatch は行っていない。

### 3.4 noncontact / NAME-COLLIDE

- sealed three quantities: opened = false
- \(u\): opened = false
- \(c\): opened = false
- sealed K5: opened = false
- NAME-COLLIDE: 本書の \(E\) は finite marked quotient、\(Q=PB_3/M\)、\(L=\ker\phi\)。便 140 の relative cokernel \(D_{L/K,t}\) や dihedral 群の記号とは別物である

## 4. 終盤勘定

本便の有限悉皆は、proper isolated refinement を一件も含まない最初の order interval を完全に閉じたものであり、族定理ではない。zero fiber がないため出口 II は発火せず、有限深度の 972 から B 型も認定しない。972 屋根の A/B は未決のままである。

endgame_scope は gentle side only。B₄ の PENT_W-PASS、FAKE-KILL\(^{B_4}\)、U-10 は全て NOT_RUN であり、本便の範囲外である。

次の具体的対象は (1.5) の kernel-\(C_2\) marked extension census であるが、今回受理条件として指定された bounded completeness は \(B=2{,}939{,}327\) まで成立した。

ENUM_STATUS: EXHAUSTED_TO_B=2939327
