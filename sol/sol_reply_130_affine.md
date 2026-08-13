# 返書 130 — compact 路の C-0/C-1 gate と affine 前段監査

日付: 2026-08-13  
仕様正本: `docs/notes/vnbit_compact_route_v1.md` (commit `5d8055aeca4a91e2861f94ccdd13d24228e46852`) + `docs/notes/vnbit_compact_route_v1_addendum_novelty.md` (commit `492a2eb8049efea785715a4d1fe2e9024ae387ad`)  
実行時 HEAD: `86d13ef8e3beb5db4891b316fda3736dbb33494c`

## 0. 到達点

便 130 の §0、§1.1–§1.4、§2、§3 を順に処理した。到達段は **C-2 と C-3 の標識付き lift 前段**、状態は

```text
UNKNOWN_STOP_MARKED_EPIMORPHISM_UNDEFINED
```

である。

1. C-0: $P=\operatorname{PSL}(2,8)$ 上の $\theta,\tau$ はともに内部作用だった。従って外部作用による $\dim V=63$ の停止分岐には入らない。
2. C-1: 標数3の既約 Brauer 次数は $[1,7,9,9,9]$。7次元既約は **1個**で外部 $C_3$ に固定され、巡回されるのは9次元の3個である。仕様正本 C-1 の「7次元が3個なら巡回」という条件の前件は成立しない。
3. C-2: 一意な7次元 heart と $G_3^{\rm ab}\cong C_2^2$ の3非自明指標の軌道束から、自然な21次元 $W$-加群を行列化した。群型
   \[
   E=V\rtimes W,\qquad |E|=54\,432\cdot3^{21}
   =569\,377\,945\,545\,696
   \]
   は構成できる。
4. C-3: 仕様は群型 $E=V\rtimes W$ を与えるだけで、記号
   \[
   N_E:=\ker(PB_3\twoheadrightarrow E)
   \]
   の矢印、すなわち $x,y$ の $V$-成分を含む標識付き全射を与えていない。自然な zero section の像は $W$ に留まり $E$ へ全射しない。従って単一の $N_E$、定数項 $b_t$、C-3/C-4 の値はまだ定義されない。
5. 指定された停止条件により、task 130 用事前登録、324障害類の測定、生成条件の測定、rigidity 集計は開始していない。測定行数は **0/324**、`raw_image_size=null` である。

以下の数値は producer と、別 heart 基底・別消去法を用いる helper 非共有 checker の二系統で一致した。Lean 証明書は作成していない。

## 1. 委嘱 §1

### 1.1 C-0/C-1 gating

#### C-0: $P$ 上の作用

`search/week3-psl-S4.g` の GF(8) 行列

\[
S=\begin{pmatrix}1&0\\1&1\end{pmatrix},\qquad
T=\begin{pmatrix}4&3\\1&5\end{pmatrix}
\]

から9点置換を独立に再構成した。$w=T^{-1}S$、$X=w^2$、$Y=TXT^{-1}$、$Z=(XY)^{-1}$ とすると、

| 量 | 生値 |
|---|---:|
| $|\langle X,Y\rangle|$ | 504 |
| $\operatorname{ord}(S),\operatorname{ord}(T)$ | 2, 3 |
| $\operatorname{ord}(X),\operatorname{ord}(Y),\operatorname{ord}(Z)$ | 9, 9, 9 |
| $S,T\in\langle X,Y\rangle$ | ともに成立 |
| $SXS^{-1}=Y,\ SYS^{-1}=X$ | ともに成立 |
| $TXT^{-1}=Y,\ TYT^{-1}=Z$ | ともに成立 |

従って

\[
\theta=\operatorname{Ad}(S),\qquad \tau=\operatorname{Ad}(T)
\]

は $P$ 上でともに内部である。これは case A / split-inner という既存分類とも整合する。

#### C-1: 標数3の7次元既約

GAP 4.16.0 同梱 CTblLib の `L2(8)` 標数3 record は、主 block の Brauer tree

```text
[[1,6],[2,3,4,5,6]]
```

と defect-zero block 3個を持つ。ordinary character rows から得る通常指標次数

\[
[1,7,7,7,7,8,9,9,9]
\]

と合わせると、Brauer 次数は

\[
\boxed{[1,7,9,9,9]}.
\]

なお ordinary table の別欄 $[504,8,9,7,7,7,9,9,9]$ は共役類中心化群位数であり、指標次数として使用していない。producer/checker は character rows の degree-1、degree-7、Galois、degree-8、degree-9 構造を別 parser で確認する。

保存 automorphism `(3,4,5)` は9次元の3位置を巡回し、7次元の位置2を固定する。よって7次元既約の同型類は1個、外部軌道長は1である。

別経路では、9点 permutation module の augmentation heart を $\mathbf F_3$ 上7次元で作った。producer の基底では全2186非零ベクトルの生成部分加群次元がすべて7、checker は $e_i-e_0\ (1\le i\le7)$ という別基底で同じ作用関係を再構成した。

以上から $P$ 側で追加の3軌道束は不要であり、C-0/C-1 由来の次元は63でなく21である。

### 1.2 21次元作用、affine 較正、C-3 停止

#### C-2 の行列作用

\[
H:=\text{7-dimensional augmentation heart},\qquad
V=H\otimes(\chi_{10}\oplus\chi_{01}\oplus\chi_{11})
\]

とした。指標順を $(10),(01),(11)$ とすると、$R_X,R_Y$ を $H$ 上の作用として

\[
\rho(X)=\operatorname{diag}(-R_X,R_X,-R_X),\qquad
\rho(Y)=\operatorname{diag}(R_Y,-R_Y,-R_Y).
\]

$\theta,\tau$ はそれぞれ $R_S,R_T$ と3 block の置換を組み合わせた21次元行列である。機械的に得た関係は次のとおり。

| 関係 | 生値 |
|---|---|
| $\rho(XYZ)=I$ | 成立 |
| $\theta^2=I,\ \tau^3=I$ | 成立 |
| $\theta\rho(X)\theta^{-1}=\rho(Y)$ | 成立 |
| $\theta\rho(Y)\theta^{-1}=\rho(X)$ | 成立 |
| $\tau\rho(X)\tau^{-1}=\rho(Y)$ | 成立 |
| $\tau\rho(Y)\tau^{-1}=\rho(Z)$ | 成立 |

producer の行列 object hash は

```text
rho(X),rho(Y): 7e1eae648dcf38c668537670344d35ab0be9397b58b38b90aabda316a7a98c02
theta,tau:      f25a37729f689838c168c866a52eba517541a32e5e3b2ca736a4bb6cc4104907
```

である。checker は別基底なので byte hash はそれぞれ `74ebc0af...395a5`、`0b0d358a...1031` と異なるが、上の全関係と以下の rank/nullity を独自に再計算した。

#### LIFT-AFF の較正 fixture

$V_0=\mathbf F_3^2$、$C_2$ の作用 $s=\operatorname{diag}(-1,1)$ とし、$f=(v,s)$ に $f^2=1$ を課した。このとき

\[
A=I+s=\begin{pmatrix}0&0\\0&2\end{pmatrix},\qquad b=0.
\]

9個の $v$ を直接展開した値はすべて $Av+b$ と一致し、解は

\[
(0,0),(1,0),(2,0)
\]

の3個だった。これは semidirect product の語展開が affine になることの実装較正であり、未指定の task 130 標識や hexagon の定数項を補うものではない。

#### C-3 で欠けている入力

群型 $E=V\rtimes W$ と $W$-加群 $\rho$ だけからは、$PB_3\twoheadrightarrow E$ は定まらない。標識を $B_3/\langle c\rangle\cong C_2*C_3$ 上で書けば、$\Delta,\delta$ の lift の $V$-成分

\[
a\in\ker(I+\theta),\qquad
b\in\ker(I+\tau+\tau^2)
\]

を選ぶ必要がある。今回の21次元作用では

| 量 | 次元または位数 |
|---|---:|
| $\ker(I+\theta)$ | 11 |
| $\ker(I+\tau+\tau^2)$ | 14 |
| coboundary map $v\mapsto((\theta-I)v,(\tau-I)v)$ の rank | 21 |
| $V^{\langle\theta,\tau\rangle}$ | 0 |
| $H^1(C_2*C_3,V)$ | 4 |
| $V$-共役を除いた lift 前段の類数 | $3^4=81$ |

この81は **全射 $PB_3\twoheadrightarrow E$ の個数でも、異なる kernel の個数でもない**。各類について pure restriction の全射性、生成する $W$-部分加群、kernel の同一性をまだ調べていない。なお、これは仕様 C-6 の $H^1(W,V)$ ではなく、標識を定義する前段の $H^1(C_2*C_3,V)$ である。

自然な zero cocycle は zero section $PB_3\to W\hookrightarrow E$ を与えるだけで、像は $E$ でない。従って zero cocycle を暗黙に採用しても $N_E$ は得られない。また $x,y,x^u,y^u$ の $V$-成分が未指定なので、LIFT-AFF の定数項 $b_t$ も未定義である。

さらに、仕様 §2 の $A$ は全 vector relation の縦積みとして定義されている。独立な21成分の hexagon が2本なら自然な型は $42\times21$ であり、「各対につき $21\times21$」への縮約には別の従属性証明が要る。GEN-AFF に必要な $W$ の有限表示と関係子列も仕様には無い。

C-3 を再開するために必要な入力順は次である。

1. $B_3/N_W$ の標識付き表示と、$\Delta,\delta$（同値に $x,y$）の $V$-成分を与える。
2. 81 lift 前段類から pure restriction が $E$ へ全射する類を分類する。
3. 全射類が同じ kernel を持つことを示すか、既存の $X,Y$ anchor による正規化で一類を固定する。
4. その kernel を $N_E$ として初めて C-3 の $\theta,\tau$-不変性と C-4 の isolated 性を調べる。
5. $W$ の表示・GEN-AFF 関係子列・$A_t$ の行型を固定してから、事前登録と324行へ進む。

これは BU-S35 で「marked lift の列挙 → 全射類 → kernel 同一性/anchor 正規化」を別段にした理由と同型の欠品である。

### 1.3 事前登録と324障害類

C-3/C-4 より前に測定しないという便の順序に従い、task 130 用の事前登録は作成していない。従って source に既在の予言を測定後に変更する操作も無い。

| 項目 | 生値 |
|---|---|
| task 130 preregistration | 未作成 |
| 凍結値 $\{972,324\}$ | 変更なし |
| $GT(N_W)$ 324行の再形成 | 未到達 |
| $[b_t]\in\operatorname{coker}(A_t)$ | 0/324 |
| obstruction 分布 | 未形成 |
| `generating_solution_exists` | 未形成 |
| $\Theta_2$ の per-$t_2$ 集計 | 未形成 |
| `single_bit_image_size` | `null` |
| `raw_image_size` | `null` |
| rigidity の値 | 無し |

とくに obstruction の消滅だけを lift と同一視していない。再開後の cert には、仕様どおり生成解の存在を独立欄で残す必要がある。

### 1.4 生値・cert・到達段

producer run ID は `vnbit-affine-gate-20260813T051413Z`、checker run ID は `vnbit-affine-check-20260813T051413Z`。両スクリプトは atomic checkpoint と内部120秒 hard-timeout を持ち、最終 checkpoint は `complete=true` である。

checker は producer を import せず、次を別実装した。

- $P$: GF(8) 演算を使わず、監査済み9点置換から閉包を再構成。
- heart: producer と異なる $e_i-e_0$ 基底。
- 線形代数: 別の $\mathbf F_3$ 前進消去と逆行列実装。
- CTblLib: modular/ordinary record を別 parser で読み、block、defect、tree、automorphism、通常指標の行構造から Brauer 次数を再構成。
- raw cert: producer 行列を checker 自身の演算で再評価。

最終 cert は `all_equalities_true=true`。到達段は次で固定した。

| gate | 到達値 |
|---|---|
| C-0 | $P$ 上で $\theta,\tau$ ともに内部 |
| C-1 | 7次元既約1個、外部軌道長1 |
| C-2 | $\dim V=21$、作用行列構成済み |
| C-3 | `null` — 単一の $N_E$ が未定義 |
| C-4 | `null` — 未到達 |
| C-5 | 未到達 |
| C-6 $H^1(W,V)$ | 未測定 |
| 324 lift table | 0行 |

GAP wrapper は

```powershell
.\gap.ps1 search\g3bridge_moddim_v1.g
```

で起動を試みたが、script 読込前に signal pipe を作れず Win32 error 5 で終了した。この失敗を GAP の計算値には数えていない。producer/checker は同梱 CTblLib 原データと標準ライブラリによる再構成を使用した。

再現コマンド:

```powershell
python search/vnbit_affine_gate_v1.py
python search/check_vnbit_affine_gate_v1.py
```

## 2. 終盤勘定の scope pin

本測定の位置は gentle $\widehat{GT}_{\rm gen}$ 側の A/B 分岐である。**gentle-genuine 側の反証候補を昇格させるには B₄ 層で PENT_W-PASS を検査し、その後 `FAKE-KILL^{B₄}/U-10` を適用する必要があり、有限深度データだけでは昇格させない。もう一方の分岐は gentle 内で完結する。**

同文を raw cert の `endgame_scope` と checker cert の `scope` に記録した。

## 3. 規律・非接触

- $u,c$: 非接触。
- 封印3量、sealed K5: 非接触。
- 凍結された $\{972,324\}$: 変更なし。
- 324測定前の outcome 観測: なし。測定自体を開始していない。
- $PB_3/N$ と $B_3/N$: pure quotient と marked $C_2*C_3$ lift を分記した。
- 有限深度から B 型を認定する操作: なし。
- `UNKNOWN`: C-3 の未定義入力を隠さず停止値として保存。
- git commit、push、workflow dispatch: なし。

## 4. provenance と成果物 SHA-256

仕様・入力:

| 入力 | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_130_affine.txt` | `40f7702a42d12a3a53bf85cb33aa2a41444333839ee0aa60551994ecd13c6469` |
| `docs/notes/vnbit_compact_route_v1.md` | `c8451f3694f76863c2a6b4dbfde221a9962bc9a2e07ea3d500ec9aa91630b8ab` |
| `docs/notes/vnbit_compact_route_v1_addendum_novelty.md` | `24d4e00f8d3d4f0b6e651ef75b94341a3aed9371b900c1a696c4b54d5c2f87e8` |
| `search/week3-psl-S4.g` | `72cc07454d35d1d371d095f5fa6b0c7044bdd8b509d4bfeceaaa482b6479a9f7` |
| CTblLib `ctbline1.tbl` | `1fa08fa503184536cd1e671c275aaf8c9a4ab1278a372cc85d2eb71292c00e78` |
| CTblLib `ctoline1.tbl` | `8937d8828f7c7719e357585fd1529dcff2152f5111d15fed79e62782c7d0a9b4` |

成果物:

| 成果物 | SHA-256 |
|---|---|
| `search/vnbit_affine_gate_v1.py` | `533e33d7c50f627d909b6f276f85d3bf9b1c6f030809a3d5567e809cbb9c5ef1` |
| `search/certs/vnbit_affine_gate_raw_v1_20260813.json` | `24b78fc1e700223f1be27dabf77e1fed65af6e58c4e28362be7d802f563bb5ee` |
| `search/certs/vnbit_affine_gate_v1_checkpoint.json` | `261c62aacd519407143b5597c81b6b350e2fdb913ce0bcc24f20f6e787e4dc02` |
| `search/check_vnbit_affine_gate_v1.py` | `5401aab89253ad9cf872f104e0b15b77901fcab89c939567784a287e7fcd3490` |
| `search/certs/vnbit_affine_gate_check_v1_20260813.json` | `e62d1d91e24ad27de60ee5c44f752bbada6fe736daa12afab1f50b1d91ba29d5` |
| `search/certs/vnbit_affine_gate_check_v1_checkpoint.json` | `a210bd1f8ed84f518805526e18a8b678923c90caba0e6a5f03163a01f11d65bc` |

作業木には着手前から他便の変更が多数存在したため、それらには触れていない。
