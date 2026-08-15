# 返書 135 — 3 群・3′ 群核の盲目性候補の射程監査

- 対象: `ops/inbox_codex/sol_task_135_blind3grp.txt`
- 実行日: 2026-08-15
- 基準 HEAD: `f43665d4e98902f62c81d495fb723516517d576a`
- 到達段: §4 完了（既存の独立実装・証明書を再利用）
- 全体状態: **UNKNOWN**

## 0. 一行への回答

二つの候補は、いずれも提示された前件だけからは定理化できない。

1. \(Q=PB_3/M\) が非自明な 3 群商を持たない、という補題は正しい。
2. しかし、それが強制するのは「\(Q\) と 3 群 \(U\) の subdirect product が直積になる」ことだけで、一般の拡大

   \[
   1\longrightarrow W_{\rm ker}\longrightarrow PB_3/K\longrightarrow Q\longrightarrow1
   \]

   の作用や拡大類は消さない。ESCAPE-28 自身が、3 群核を持ちながら直積でない \(B_3\)-正規細分を既に与える。
3. 3 群核では \(C_3\) 障害が一般には残る。3′ 群核についても、3 の可逆性から直接消せるのは線型化した \(C_3\) 側であり、2-primary 層の \(C_2\) 障害は残り得る。従って素数条件だけでは、どちらの全射性も従わない。

候補そのものを否定する零 survival 細分は得ていないので、二候補の真偽は **UNKNOWN** のままである。従って冪零核全体についての到達限界定理も本便では立てない。

| 項目 | 本便の裁定 |
|---|---|
| \(Q\) の非自明 3 群商 | 存在しない（紙 + 独立二実装の入力） |
| 3 群核拡大の直積化 | 一般には不成立。ESCAPE-28 が実細分を与える |
| BLIND-3GRP | UNKNOWN |
| BLIND-3PRIME | UNKNOWN |
| 冪零核全体 | 定理化しない |

## 1. 主命題の判定

### 1.1 成立する補題 — \(Q\) は非自明な 3 群商を持たない

便 134 の二つの独立実装は、異なる表現で \(G_9\) を再構成した。

| 実装 | \(G_9\) の表現 | \(\lvert G_9\rvert\) | \(\lvert G_9'\rvert\) | 可換化 |
|---|---|---:|---:|---|
| producer | \(D_9^3\) の dihedral triple | 2,916 | 729 | \(C_2^2\) |
| checker | 27 点置換群 | 2,916 | 729 | \(C_2^2\) |

checker 側でも \(G_9/G_9'\) の位数は 4 で、標識 \(x,y\) の二つの異なる非自明剰余類はいずれも位数 2 なので \(C_4\) ではなく \(C_2^2\) である。`S4.v2.json` は \(\operatorname{PSL}(2,8)\) の位数と導来群位数をともに 504 と記録する。従って

\[
Q^{\rm ab}
 \cong G_9^{\rm ab}\times\operatorname{PSL}(2,8)^{\rm ab}
 \cong C_2^2.
\]

ここから司令塔の粗い論証は次のように完成する。非自明有限 3 群 \(H\) は指数 3 の極大部分群を持つので \(H^{\rm ab}\ne1\)。もし \(Q\twoheadrightarrow H\) なら、可換化して \(C_2^2\twoheadrightarrow H^{\rm ab}\) を得る。しかし左辺の商で 3 群であるものは自明群だけであり矛盾する。従って

\[
\boxed{Q\text{ は非自明な有限 3 群商を持たない}.}
\]

同じ理由で、3 群 \(U\) と \(Q\) は非自明な共通商を持たない。従って \(S\le Q\times U\) が両因子へ全射する subdirect product なら、Goursat により \(S=Q\times U\) となる。これは便 134 型の「独立な追加商との fiber product」には正しく適用できる。

### 1.2 最大の隙間 — 商不存在は拡大を直積にしない

一般の拡大 \(E\twoheadrightarrow Q\) には \(E\to W_{\rm ker}\) という第二の全射はない。従って上の Goursat 論法を適用できない。最小の抽象模型だけでも、非自明指標

\[
\chi:Q\twoheadrightarrow C_2\hookrightarrow\operatorname{Aut}(C_3)
\]

を取り \(E=C_3\rtimes_\chi Q\) とすれば、核は \(C_3\) だが共役作用が非自明なので \(C_3\times Q\) ではない。\(Q\) に 3 群商がないこととは両立する。

さらに工房内には、抽象模型ではなく条件を満たす実細分が既にある。便 133 の記法で

\[
\begin{aligned}
P&=\operatorname{PSL}(2,8),\\
N_W&=N_{S4}\cap K^{(3)},\qquad PB_3/N_W\cong P\times G_3,\\
E_{28}&=V_{28}\rtimes(P\times G_3),\qquad V_{28}\cong\mathbf F_3^{28},\\
N_E&=\ker(PB_3\twoheadrightarrow E_{28}),\\
K_{28}&=K^{(9)}\cap N_E,\qquad M=K^{(9)}\cap N_{S4}
\end{aligned}
\]

とする。一つを完全に固定するなら、`escape28_mainrun_raw_v1_20260813.json` の

```text
window_id                    eps=+,eta=+
class_position               0
orbit class / coordinates    1 / [0,0,0,2]
trivial class / coordinates  3 / [0,1,0]
```

を選べばよい。この標識付き全射の核 \(N_E\) は \(B_3\)-正規・有限指数であり、従って \(K_{28}\subseteq M\) も同様である。純商は

\[
PB_3/K_{28}\cong
G_9\times_{G_3}\bigl(V_{28}\rtimes(P\times G_3)\bigr)
\]

で、\(PB_3/M\cong G_9\times P\) への核は

\[
W_{\rm ker}=M/K_{28}\cong V_{28}\cong C_3^{28}.
\]

\(G_9\times P\) の \(V_{28}\) への作用は非自明なので、この純商は \(Q\times V_{28}\) ではない。これは「3 群核なら商不存在によって直積へ潰れる」という段を、実際の \(B_3\)-正規細分の中で否定する。作用の非自明性は主に \(P\) の 7 次元表現と \(G_3^{\rm ab}=C_2^2\) の指標から来ており、提案された \(G_9'\) の非自明作用型ではない。その型の構成は未達として残る。なお `N_E_isolated=UNKNOWN` はこの構成・核同定には不要で、有限深度の型解釈にだけ関係する。

### 1.3 候補 BLIND-3GRP

まず相対核が初等可換 \(V\) の場合でも、持ち上げ障害の自然な受け皿は

\[
H^2(C_2*C_3,V)
 \cong H^2(C_2,V)\oplus H^2(C_3,V).
\]

標数 3 では \(2\) が可逆なので第 1 項は消えるが、

\[
H^2(C_3,V)=V^\tau/(1+\tau+\tau^2)V
\]

は一般には消えない。ESCAPE-28 では実際に

```text
dim V28                         28
dim fixed(tau)                  10
rank(1+tau+tau^2)                8
dim H^2(C3,V28)                  2
```

である。従って「核が 3 群」という前件だけから、障害群の消滅も、全 shadow の実障害類の消滅も導けない。非可換 3 群へ進めば、さらに非可換コホモロジーと生成条件が必要になる。

本便で確定できる裁定は次である。

- 直積化による証明: 不成立。
- 一般の 3 群核に対するコホモロジー消滅: 不成立。
- 候補の結論そのもの: 零 survival の実細分がないため **UNKNOWN**。

成立する弱形は既存のものに留まる。すなわち、LIFT-AFF / GEN-AFF の適用範囲で、各初等可換層の実障害が消え、かつ生成解が存在する場合にはその層を持ち上げられる。標数 3 で \(V|_{C_3}\) が自由なら \(H^2(C_3,V)=0\) となる OBS-VOID-T はこの弱形の一例である。

### 1.4 候補 BLIND-3PRIME

線型な初等可換層では、「3 が可逆」は \(C_3\) 側だけを処理する。初等可換 \(p\)-核でさえ、素数だけから得られる無条件の消滅域は

\[
p\nmid6
\]

である。このとき \(C_2,C_3\) の両方で averaging が使える。一方 \(p=2\) では、たとえば自明な \(C_2\)-作用を持つ \(V=\mathbf F_2\) に対して

\[
H^2(C_2,V)=V^{C_2}/(1+\theta)V=V/0\cong\mathbf F_2
\]

となる。従って \(p\ne3\) だけでは足りない。これは対話帳 T-28 の「生き残る場所は 2-primary と 3-primary」という訂正、および便 134 が 2 群核で二つの hexagon を実際に検査する必要があったことと整合する。

従って族 7 の安全な読みは次である。

1. 主前件 \(H^2(C_2*C_3,V)=0\) を直接確認した窓には OBS-VOID を使える。
2. 素数だけで自動化するなら \(p\nmid6\)。
3. \(p=2\) を含めて「\(p\ne3\)」と書くには、\(C_2\) 障害が別理由で 0 になる前件が要る。

従って `entangled972_reading_v1.md` §1.3–1.4 の「\(p\ne3\) 係数の全窓」という略記は、その掲載証明だけでは \(p=2\) を覆わない。\(p\nmid6\) に狭めるか、窓ごとの \(H^2(C_2,V)=0\) を追加する必要がある。

一般の非可換 3′ 群核はこの線型定理の射程外であり、SURJ も別途必要である。便 134 の位数 2,048 の一窓で全 972 元が持ち上がったことは整合する生値だが、全 3′ 群核への量化は支えない。この候補も結論は **UNKNOWN** とする。

## 2. ESCAPE-28 との接続

BLIND-3GRP は立たなかったので、便 133 の全消滅をその系として説明することはできない。むしろ ESCAPE-28 は次の二点を同時に示す。

1. \(W_{\rm ker}\cong C_3^{28}\) かつ純商は直積でない。従って枝 (b) の直積化説明には使えない。
2. \(\lvert H^2(C_3,V_{28})\rvert=3^2\) なので、既存の \(H^2=0\) 説明にも入らない。

それでも既存の本走では、4 窓・3,392 全射類・各 324 行、計 1,099,008 行について

```text
nonzero_obstruction_row_count   0
generation_absent_row_count     0
Im R_(K,M) distribution         {972: 3392}
checker mismatch_count          0
```

だった。上で固定した `class_position=0` についても \(\lvert\operatorname{Im}R_{K_{28},M}\rvert=972\) である。従ってこれは候補と整合する一例ではあるが、候補の証明ではない。

残る紙の問いは明確である。各 shadow から \(H^2(C_3,V_{28})\cong\mathbf F_3^2\) へ送る**実障害写像の像がなぜ 0 なのか**を、この特定の標識付き拡大について示す必要がある。\(Q\) の 3 群商不存在はこの写像を制御しないため、便 133 の全消滅の説明は依然として開いている。

便 134 の `d972_survival_noncomm_v1.py` は明示的な \(U_5\) fiber 用で、\(3^{28}\) の compact semidirect 窓を直接表現しない。本件では同じ対象を既に全数処理した `escape28_mainrun_v1.py` と独立 checker の再利用が正しいため、新たな 1,099,008 行走査は行っていない。この構成が否定するのは直積化の段であり、候補の全射結論ではないので、新しい零 survival 候補を得た扱いにはしていない。

## 3. 冪零核への到達限界

二候補が成立していないので、「冪零核の細分は全部盲」という命題は本便からは得られない。

さらに論理上の注意が一つある。仮に二候補が**固定した基底 \(M\) 上だけ**で成っても、混合素数の冪零核へは直ちに合成できない。\(W_{\rm ker}=M/K\) が冪零なら

\[
W_{\rm ker}=W_3\times W_{3'},
\]

で、両 Hall 部分群は characteristic である。\(L/K=W_3\) と置けば \(L\trianglelefteq B_3\) かつ

\[
L/K\cong W_3,\qquad M/L\cong W_{3'}.
\]

しかし合成

\[
GT(K)\longrightarrow GT(L)\longrightarrow GT(M)
\]

の第一段には、基底を \(L\) に替えた 3 群核定理が必要である。従って冪零核命題が従うのは、二つの主張を**全ての中間 \(B_3\)-正規有限指数対に対して base-change 安定な形**で証明した場合に限る。その強い前件の下なら二段の全射を合成できる。

現状はその前件を持たない。冪零核を越えて可解核・一般核へは何も拡張せず、すべて UNKNOWN に残す。

## 4. 機械確認・再現・格

### 4.1 \(Q^{\rm ab}\) と 3 群商

新しい実装・cert は作らず、便 134 で凍結済みの二つの監査関数 `audit_g9()` / `independent_g9_audit()` だけを `python -B` で再実行した。二系統は helper を共有せず、前者が dihedral triple、後者が 27 点置換を使う。現在の実行でも

```text
producer  order=2916  derived_order=729  abelianization=[2,2]
checker   order=2916  derived_order=729  abelianization=[2,2]
agreement true
```

となった（Python 起動込み wall 約 0.4 秒）。凍結済み checker cert の `agreement=true` とも一致する。PSL 因子の perfectness は `S4.v2.json` の `derived_order=504` を用いた。

再現する場合は、repo 内の既存 cert を上書きしないよう出力先を一時領域に取る。

```powershell
$blind135Tmp = Join-Path $env:TEMP 'shadow-atelier-blind3grp-135'
New-Item -ItemType Directory -Force -Path $blind135Tmp | Out-Null
python search/d972_survival_noncomm_v1.py --output (Join-Path $blind135Tmp 'producer.json') --checkpoint (Join-Path $blind135Tmp 'producer.checkpoint.json') --hard-timeout-seconds 120
python crosscheck/check_d972_survival_noncomm_v1.py --producer (Join-Path $blind135Tmp 'producer.json') --output (Join-Path $blind135Tmp 'checker.json') --checkpoint (Join-Path $blind135Tmp 'checker.checkpoint.json') --hard-timeout-seconds 120
```

群論的な「非自明有限 3 群の可換化は非自明」という段は上の紙の証明であり、探索の不在を非存在証明に読み替えてはいない。

### 4.2 再利用した証明書

| artifact | SHA-256 |
|---|---|
| `sol/sol_reply_133_escape28.md` | `c31b93797b36630c1d039a23d4ac0aa96709d55c339afa05f7701f8cc4888a1a` |
| `sol/sol_reply_134_survival.md` | `2148194eaff935a7cd00199eb5fe5399a2bc3b31f81da0b141b538da35bc339a` |
| `search/d972_survival_noncomm_v1.py` | `5686cd3d88cac6de6a904c36aa34fee5e07885158135de2e7f55824b16b5e8e3` |
| `crosscheck/check_d972_survival_noncomm_v1.py` | `bdcafe90ffe2dc3a331e966e34b02058653096f559253b756f81ff3d2f495bfd` |
| `search/certs/d972_survival_noncomm_v1_20260815.json` | `2b79438f7bfe574103bfcf6e30d9c873aa358dec7d254c98088a7003b5a25df3` |
| `crosscheck/verdicts/d972_survival_noncomm_v1_20260815.json` | `8006d83db4fca54cf735b92d4a3b236af9c26cef105e14d6eccfcd6b7824c3f5` |
| `search/escape28_mainrun_v1.py` | `2acdbdd17c30f28ea3709cf6f44ee47dd81e9868a8ae64b364926f3c4e1ea6b8` |
| `search/check_escape28_mainrun_v1.py` | `aa371e68fd24151f5225eb9ddd4a3a45d7e8172e1a301ae1aa8e2250c8615975` |
| `search/certs/escape28_preflight_v1r2_20260813.json` | `50b614660db17a560d2e4ef8fc954dcf23705765cb2d2721d28fe19d15f4ce45` |
| `search/certs/escape28_mainrun_raw_v1_20260813.json` | `5f0718e4c6a6227aa75126b7a8059077b682e4273100eee7775621cdaa34eb50` |
| `search/certs/escape28_mainrun_check_v1_20260813.json` | `dfa755c3f9009b15d285481a7b09069b104578016585637df037e2c310ce6a5d` |
| `certificates/K9.v1.json` | `ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e` |
| `certificates/S4.v2.json` | `c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d` |

数値部分の格は既存 producer と独立 checker の一致による **cross-checked**。本便の主増分は紙の射程監査であり、Lean certificate はない。

## 5. 終盤勘定

本便は gentle 側の構造監査だけである。再利用した raw cert の `endgame_scope` は、B4 層の `PENT_W-PASS` を先に要求し、その後に指定された B4/U-10 鎖へ進む順序を保持している。本便では零 survival がなく、昇格操作は行っていない。

## 6. 規律・novelty receipt

- 核は \(W_{\rm ker}\)、既存の \(W=PB_3/N_W\)、\(\bar W=B_3/N_W\) と分記した。
- 封印 3 量、`u/c`、sealed payload は非接触。
- 有限深度からの型認定は行っていない。
- `.git` は read-only。commit、push、workflow dispatch は行っていない。
- 新規の producer/cert は作らず、凍結済み二系統を hash 固定で再利用した。

受信時 HEAD `f43665d4e98902f62c81d495fb723516517d576a` を corpus に固定し、`git grep` で `docs/` と `sol/` を対象に採った行ヒット数は次の通り。作業中に裁定 1164 の後続記帳が入ったため、現在の worktree を使うと本便自身の結論を prior art として数える循環が生じる。この固定によりそれを除外した。

```text
Q の非自明 3 群商不存在                 3
p\nmid6 / p∤6                            34
ESCAPE-28 と C3^28 核の同一行            0
冪零核と base-change の同一行            0
H^2(C2,F2) の同一行変種                  5
```

商不存在と `p\nmid6` 自体は既出である。本便の増分は、ESCAPE-28 をその商不存在から直積化できない実細分として位置づけたことと、固定基底版の二候補から冪零核命題へ移る際の base-change 前件を分離したことである。grep 0 は数学的新規性の証明には用いない。
