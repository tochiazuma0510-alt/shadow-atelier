# Sol 便 151 返信 — 972 屋根 A/B 最終監査

## 0. 結論

ops/inbox_codex/sol_task_151_finish.txt を先頭から末尾まで読み、裁定 1202 と A/B 決着要求の双方を処理した。受信便の SHA-256 は
dff557fe619f585fa1dfa6b5966ceb4af09c48b4bd225c7bfac411b340002f8d である。

**要求された A/B の決着証明書は得られなかった。正確な裁定は A_B=UNKNOWN である。**

これは第三の数学的分岐を追加する主張ではない。真値は A/B の二択である。しかし本便で得た最強の有限全数結果と無限族定理のどちらからも、その二択を選ぶ証明は出ない。従って本返信が便 151 の「それ以外は受理しない」という成功条件を満たすとは主張しない。一方、根拠のない A または B を書けば、同じ便の不変条件「捏造・過大格付けはしない」に違反する。後者に従い、決着を装わない。

## 1. 裁定 1202 の履行

「Sol に計算をさせない」という旧文言は停止理由に用いていない。本便では三つの subagent 車線を同時に走らせ、こちらでも既存二実装の fresh rerun、GAP 起動、有限 event の紙上列挙と相互反証を行った。

1. **A 車線**: $M$ 上の $B_3$-安定 relative extension を kernel order 順に分類し、全 reduction fiber を調べた。
2. **B 車線**: 便 150 の restricted thread を敵対的に再監査し、交叉の誤包含を修理した上で、一般の lcm-dihedral chain まで拡張した。
3. **反証車線**: 最初の $k=4$ census「3 event」を反証し、見落としていた twisted $C_4$ event を追加してから全 fiber を再監査した。

実際、最初の $k=4$ 結論は誤っていた。反証を受けて結論を撤回し、4 event に直した。役割境界を理由に途中停止していない。

## 2. A/B の厳密な出口

正本どおり

\[
A_{\rm ar}:=\operatorname{Im}(G_{\mathbf Q}\to GT(M)),\qquad
P_M:=\mathcal{PR}_M(\widehat{GT}_{\rm gen})
\]

と置く。既確定の

\[
|GT(M)|=972,\qquad |A_{\rm ar}|=324,\qquad
A_{\rm ar}\le P_M\le GT(M)
\]

と指数 3 の素数性から

\[
\boxed{P_M=A_{\rm ar}\quad\text{または}\quad P_M=GT(M)}.       \tag{2.1}
\]

従って 648 元は一斉に A 型または一斉に B 型である。値を選ぶために必要な証明書は次のどちらかである。

- **A 証明書**: isolated $L\le M$ と outside 元 $g\in GT(M)\setminus A_{\rm ar}$ で

  \[
  R_{L,M}^{-1}(g)=\varnothing.                                  \tag{2.2}
  \]

  一件あれば $P_M=A_{\rm ar}$ となり、648 元は全部 A 型である。

- **B 証明書**: outside 元一つの全 isolated refinements 上の survival、同値に全 isolated refinements に cofinal な系での compatible inverse-limit lift。一件あれば $P_M=GT(M)$ となり、648 元は全部 B 型である。

Cor. 5.4 はこの全称量化を必要十分条件としている。有限個の all-pass は B 証明書ではない。

## 3. A 車線 — kernel order 7 までの exact event prefix

### 3.1 census

既存 $k=1,2$ を再固定した上で、relative kernel order $k=3,\ldots,7$ を分類した。結果は次のとおりである。

| $k=[M:L]$ | relative kernel / event 数 | reduction の結果 |
|---:|---|---|
| 1 | base 1 | image 972、fiber $1\times972$ |
| 2 | $C_2$ 3 | source size $972,1944,1944$、三つとも image 972、zero 0 |
| 3 | $C_3$ 1 | $|GT(L)|=972$、fiber $1\times972$、zero 0 |
| 4 | $C_4$ 2、fixed $V_4$ 1、natural $V_4$ 1 | **exactly 4 event**、全て isolated、image 972、zero 0 |
| 5 | $C_5$ 1 | $|GT(L)|=3888$、fiber $4\times972$、zero 0 |
| 6 | $C_6$ 3、$S_3$ 0 | source size $972,1944,1944$、全て image 972、zero 0 |
| 7 | $C_7$ 1 | $|GT(L)|=5832$、fiber $6\times972$、zero 0 |

従って exact event prefix $k\le7$ には (2.2) の witness がない。以下は分類の荷重箇所である。

### 3.2 $k=3$

$Q_0:=PB_3/M=G_9\times\mathrm{PSL}(2,8)$ とする。$H^1(Q_0,C_3)=H^2(Q_0,C_3)=0$ で、pure extension は $Q_0\times C_3$ に限る。full sign action は

\[
H^1(PB_3,C_3)\cong\mathbf F_3^3
\]

の pair-linking permutation module に sign line がないため marked-generated にならない。従って diagonal $C_3$ kernel が唯一である。二 hexagon と settlement を直接評価すると全 972 target に一意な lift がある。

### 3.3 $k=4$ の敵対的修理

最初の「$C_4$ は一つ、全 event は三つ」という結論は偽だった。$B_3$-不変な $C_2$ characters を

\[
R_0=\operatorname{Hom}_{B_3}(M,C_2)=\langle s,n\rangle\cong\mathbf F_2^2
\]

（$s$ は split、$n,n+s$ は nonsplit）とする。すると

\[
\phi_0(h)=\operatorname{exp}(h)/2\pmod4,\qquad
\phi_1=\phi_0+2n                                               \tag{3.1}
\]

は異なる $C_4$ kernel を与える。もう一つの nonsplit character $n+s$ は $-\phi_1$ を与えるので kernel は同じである。係数写像
$H^2(Q_0,C_4)\to H^2(Q_0,C_2)$ と $R_0/\{\pm1\}$ の計算により、$C_4$ kernel はこの二つで尽きる。

twisted 側の pure small factor は

\[
z^4=1,\quad z\text{ central},\quad
X^2=Y^2=1,\quad [X,Y]=z^2,\quad c=z^3.                         \tag{3.2}
\]

これは exponent $C_8$ factor と nonsplit $Q_8$ factor の central involution を同一視した central product である。各 base target には $m\bmod36$ の二 lift があり、各 $m$ で derived $f$-lift は二つある。その $Q_8$ defect は $1,z^2$ なのでちょうど一つだけが通る。passing map は両 covering factor の automorphism から降りる。従って twisted 側も isolated、

\[
|GT(L_{C_4}^{\rm twist})|=1944,\quad
|\operatorname{Im}R_{L_{C_4}^{\rm twist},M}|=972,\quad
\text{zero fiber}=0.                                           \tag{3.3}
\]

untwisted $C_4$、fixed $V_4$、natural $V_4$ も同じく全 972 を通る。なお両 $C_4$ kernel は $c$ を含まない一方、全 dihedral $K^{(n)}$ は $c$ を含む。従って旧 shortcut $L_{144}\le L_{C_4}$ は不可能であり、(3.2) の直接証明が必要だった。

### 3.4 $k=5,6,7$

- $k=5$: $5\nmid|Q_0|$ による cohomology 消滅と sign line 不在から diagonal $C_5$ 一件。各 base 元の 5 個の CRT lift のうち $u=2m+1\not\equiv0\pmod5$ の 4 個が settled。
- $k=6$: $C_6$ の characteristic $C_2,C_3$ quotients により、三つの $k=2$ event と唯一の $k=3$ event の交叉三件で尽きる。$S_3$ は complete group なので event があれば独立な $PB_3\twoheadrightarrow S_3$ が必要になるが、便 128 の helper-disjoint 36-map census では全 surjection が $G_9\to S_3$ を経由し、$M\le K^{(9)}$ を殺す。従って relative $S_3$ event はない。
- $k=7$: $\operatorname{Aut}(C_7)=C_6$。非自明な三つの quadratic action は outer $S_3$ に一巡回され、$B_3$-fixed でない。trivial action では $\mathrm{PSL}(2,8)$ の perfectness と multiplier 1、さらに $7\nmid|G_9|$ から $H^1=H^2=0$。diagonal kernel 一件だけが残り、7 個の CRT lift 中 6 個が automorphism $t\mapsto t^u$ を与える。

この $k=3,\ldots,7$ 分類は紙上証明候補であり、完全な relative-extension engine による独立 census でも Lean でもない。$k=6$ の $S_3$ 非存在に使った有限 36-map census のみ既存二実装照合済みである。従って global に cross-checked や verified へ上げない。

### 3.5 fresh machine rerun

Phase 2b の非分裂 $C_2^6$ 窓を repository 外の一時 directory で producer/checker とも再走した。

| 項目 | fresh 値 |
|---|---|
| producer | source shadows 432、settled 432、source roof shadows 7776、raw image 972 |
| independent checker | all_checks_true=true、direct well-defined/bijective $432/432$、raw image 972 |
| fresh producer SHA-256 | a7bbb3aac861cd051e3db001830f823ef5d7aebe61b744605b889a0668d860a2 |
| fresh checker SHA-256 | a5ca5759b359b0e771c99a1bed253bfdaaa3e5f3fc6000c38148feadc6e413f5 |

既収蔵の最初の非可換 Magnus cutoff-5 window も producer/checker が fiber $16\times972$、zero 0 で一致している（cert 2b79438f7bfe574103bfcf6e30d9c873aa358dec7d254c98088a7003b5a25df3、checker 8006d83db4fca54cf735b92d4a3b236af9c26cef105e14d6eccfcd6b7824c3f5）。どちらも有限窓の陰性結果であり、B へは昇格させない。

## 4. B 車線 — 便 150 の修理と cofinality の反例

### 4.1 便 150 の誤包含

便 150 で暗黙に使った $L_{144}\le K_2$ は偽である。$c\in L_{144}$ だが、split $c$-parity factor のため $c\notin K_2$ である。従って便 150 の $H_r\cap L_{144}$ の処理はそのままでは成立しない。

### 4.2 修理された無限 all-972 chain

\[
n_s:=\operatorname{lcm}(36,1,\ldots,s),\qquad
D_s:=K^{(n_s)}\cap N_{S4},\qquad
X_s:=D_s\cap W\cap K_2.                                       \tag{4.1}
\]

と置く。$D_s$ と非中央 $C_2^6$ window $W$ の相対 modules は、$\mathrm{PSL}(2,8)$ が自明に作用する成分と非自明既約成分に分離する。従って fiber product は

\[
PB_3/(D_s\cap W)\cong G_{n_s}\times E
\]

となり、$E$ の perfectness により charming 条件も componentwise に貼れる。残る split $c$-parity factor は一意 lift である。よって

\[
\boxed{\operatorname{Im}R_{X_s,M}=GT(M)\quad\text{for every }s} \tag{4.2}
\]

であり、transition も全射である。これは便 150 の最初の非中央交叉停止点を越える。さらに $(X_s)$ は全 dihedral refinements $M\cap K^{(q)}$ に対して cofinal である。

### 4.3 しかし global cofinal ではない

各 $X_s$ は $c^2$ を含む。一方、$N_5^{\rm cyc}:=\ker\beta_5$ を既存の cyclic $c$-survival control（$PB_3/N_5^{\rm cyc}\cong C_5,\ c\mapsto t$）とし、

\[
L:=M\cap N_5^{\rm cyc}
\]

と置く。$M,N_5^{\rm cyc}$ は isolated なので $L$ も isolated である。しかし

\[
c^2\notin L,\qquad c^2\in X_s\quad(\forall s),\qquad
\therefore X_s\nleq L.                                        \tag{4.3}
\]

従って $(X_s)$ は全 isolated refinements に cofinal ではない。これは抽象的な注意ではなく、明示的 isolated counterexample である。

便 150 の「genuine outside $g_\star$」という語は過大だった。正しくは「outside target に対する restricted $X_s$-thread」である。(4.2) は強い無限族定理だが、Cor. 5.4 の全細分量化を満たさないため B 証明書ではない。

## 5. 計算資源と GHA 要求

ローカル GAP は worker を読む前に次の状態で停止し、出力を一つも作らなかった。

    fatal error - couldn't create signal pipe, Win32 error 5
    exit = -1073741502

一方、現行 dovetail v1 自身も completeness receipt に
workflow_resumable:false / BLOCKED_NONCHECKPOINTABLE_EXTENSION_CELL と明記し、fp-order、automorphism、shadow scan の cell 内 cursor を永続化できない。現 SHA の workflow を発火しても数学的 candidate enumeration は進まないため、無意味な dispatch は行っていない。

工房への具体的資源要求は次である。

1. Linux GAP runner 上で動く relative-extension worker v2。
2. canonical_table_relabel、Aut(H)、extension class、marked orbit、fp-order、972-fiber scan の**各内部 cursor**を lossless に checkpoint できること。
3. producer と helper 非共有 checker が、isolatedness、source size、972-vector、zero-key set を独立再計算すること。
4. 最初の eligible zero fiber でだけ A terminal。有限 cap / nontermination / all-pass prefix を B と読まないこと。

これは A の半決定器に必要な実装要求である。A が偽なら停止保証はなく、計算資源を無制限にしても、その nontermination は B の有限証明にはならない。B には (4.3) をも越える cofinal family theorem、または outside 元の明示的な global profinite lift が別途必要である。

## 6. 最終会計

- eligible な zero-fiber certificate: **0 件**。
- 全 isolated refinements に cofinal な all-pass / compatible outside thread: **0 件**。
- exact event prefix: $k\le7$ は全 event all-pass（紙上候補。global cross-check ではない）。
- 無限族: dihedral subsystem では all-972 compatible thread を構成したが、(4.3) により global noncofinal。
- explicit genuine non-arithmetic profinite element outside $A_{\rm ar}$: **未構成**。

よって A を書けば (2.2) を捏造し、B を書けば (4.3) を無視した finite/subsystem-to-global の過大格付けになる。本便で手を尽くして得た正直な最終値は

\[
\boxed{\texttt{A\_B=UNKNOWN}.}
\]

## provenance / operational

- 作業時 HEAD: ea009bd8fc4229b5dd779f027feb4fd60adbd0a7。
- 便 150 SHA-256: 8626f990bbf253d8e21e44f9a0ac777a76d3a4111c507fca37471264e4956bd0。
- 現行 dovetail producer / worker / checker SHA-256:
  1243f3646fc05cc9ea9f5bf00ff92c0c6c6d82b4ae6b81c57a4fcab874638ac0 /
  323d18de4fadcf4561222995f5b6590bb560cd617048d2e9b54049ae3eea9efd /
  d2e398ebdc4333a04b726cf8fa68b76e1815c6d15a1db4e14b53fcd3511388a0。
- commit、push、workflow dispatch は行っていない。従って run id / commit SHA の新規記録はない。
- fresh rerun の出力は repository 外の一時 directory に置き、作業木へ収蔵していない。
- 本便で変更した repository file は指定返信 sol/sol_reply_151_finish.md だけである。
- Lean certificate はない。global decision は cross-checked=false, verified=false。

    FINAL:
    TASK151_FULL_MAIL_PROCESSED;
    RULING1202_APPLIED_SUBAGENTS_AND_COMPUTATION_USED;
    KERNEL_ORDER_1_THROUGH_7_ALLPASS_PAPER_CANDIDATE;
    NO_ELIGIBLE_ZERO_FIBER_CERTIFICATE;
    DIHEDRAL_SUBSYSTEM_COMPATIBLE_THREAD_ONLY;
    NO_GLOBAL_COFINAL_SURVIVAL_CERTIFICATE;
    A_NOT_PROVED;
    B_NOT_PROVED;
    A_B_UNKNOWN;
    NO_FABRICATION;
    GLOBAL_CROSS_CHECKED_FALSE;
    VERIFIED_FALSE
