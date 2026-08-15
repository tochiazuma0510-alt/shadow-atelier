# 返書 136 — ESCAPE-2（標数 2 の \(C_2\) 障害窓）

- 対象: `ops/inbox_codex/sol_task_136_escape2.txt`
- 実行日: 2026-08-15
- 基準 HEAD: `4f3a835038bb208ac5ad74508019c826b952b95a`
- 到達段: §1–§4 の有限宇宙を完走。producer と helper 非共有 checker は一致
- 数値の格: **cross-checked**。Lean certificate はなく、**verified ではない**
- 判定状態: 数値のみ。`N_E_isolated=UNKNOWN`、`escape2_gap=open`

## 0. 一行と重要な手続注記

選んだ最小の実用的な半単純軌道束は、

\[
 V=E_{12}\oplus E_{23}\oplus E_{13}\cong \mathbf F_2^{12}
\]

である。各 \(E_{ij}\) は \(G_3=C_3^3\rtimes C_2^2\) の 4 次元単純加群で、\(C_3^3\) の指標の支持が座標対 \(\{i,j\}\) にあるもの。生値は

```text
dim V                               12
theta Jordan                        J2^5 + J1^2
dim fixed(theta)                     7
rank(1+theta)                        5
dim H^2(C2,V)                        2
dim fixed(tau)                       4
rank(1+tau+tau^2)                    4
dim H^2(C3,V)                        0
anchor windows                       1
surjective marked classes            7
rows per class                     324
evaluated rows                    2,268
nonzero obstruction rows             0
generation-absent rows               0
checker mismatches                    0
```

したがって、本宇宙では \(H^2(C_2,V)\cong\mathbf F_2^2\) が実在する一方、実障害類は全 2,268 行で零だった。理由は本便では **UNKNOWN** である。

ただし手続上の降格がある。実装試走が preflight freeze より先に全 2,268 結果を開いてしまった。従って後から作った `escape2_prereg_v1.json` は

```text
blind_before_measurement              false
pilot_outcomes_opened_before_freeze   2268
directional_obstruction_prediction    null
status                                procedural downgrade; not prospective
```

と正直に記録した。以下の数値は独立照合済みだが、**prospective な事前登録結果ではない**。この点を遡及的に `blind=true` へ読み替えてはならない。

本便の加群宇宙は、ESCAPE-28 と同じ「単純加群・テンソル・外部作用の軌道束」からなる半単純 lane に限った。非半単純な indecomposable extension の全分類は行っておらず、その方向の最小性は **UNKNOWN** である。

## 1. 入口検査

### 1.1 \(P=\mathrm{PSL}(2,8)\) の単純 \(\mathbf F_2\)-加群棚卸し

Steinberg tensor product と \(\operatorname{Gal}(\mathbf F_8/\mathbf F_2)\) の軌道から、単純 \(\mathbf F_2[P]\)-加群は次の 4 個になる。producer は \(P^1(\mathbf F_8)\) の同じ marked \(s,t\)（生成群位数 504）から全行列を構成し、Node の別実装も \(H^2\) 生値を一致させた。

| 加群 | \(\dim_{\mathbf F_2}\) | \(\theta\) Jordan | \(\dim H^2(C_2,-)\) | \(\dim H^2(C_3,-)\) | \(\dim_{\mathbf F_2}\operatorname{End}_P\) |
|---|---:|---|---:|---:|---:|
| 自明 | 1 | (J_1) | 1 | 0 | 1 |
| 自然 2 次元の 3 Frobenius 捻りの降下 | 6 | \(J_2^3\) | 0 | 0 | 3 (\(\mathbf F_8\)) |
| Steinberg | 8 | \(J_2^4\) | 0 | 0 | 1 |
| 2 因子 tensor の 3 Frobenius 捻りの降下 | 12 | \(J_2^6\) | 0 | 0 | 3 (\(\mathbf F_8\)) |

対照の \(C_3\) 生値は順に

```text
module       dim fixed(tau)   rank norm_tau   dim H2(C3)
trivial             1               1               0
natural-6           0               0               0
Steinberg-8         2               2               0
pair-12             6               6               0
```

である。従って \(P\) の非自明単純因子だけから作る加群は \(C_2\) 上自由である。自由な \(\mathbf F_2[C_2]\)-加群の拡大も自由なので、非自由性を得るには別の組成因子が要る。

自明 1 次元だけは \(H^2(C_2,-)\ne0\) だが、split affine 路では使えない。実際

\[
 \operatorname{Hom}(C_2*C_3,\mathbf F_2)
 \longrightarrow \operatorname{Hom}(\bar W,\mathbf F_2)
\]

は同型で、自明成分の cocycle は全部 \(\bar W\) へ降下する。その成分の関係子平行移動は零になり、GEN-AFF で全生成しない。従って「自然 6 次元 \(\oplus\) 自明 1 次元」等の小さい直和も本 lane では落ちる。

### 1.2 \(G_3\) 側との合成と選択した加群

\(A=C_3^3\triangleleft G_3\) とする。外部作用は既存の規約で

\[
 \theta(n_1,n_2,n_3)=(n_2,n_1,-n_3),\,
 \tau(n_1,n_2,n_3)=(n_3,n_1,n_2).
\]

\(A^\vee\cong\mathbf F_3^3\) の非零指標を支持の大きさで分け、\(\theta,\tau\)-安定化に必要な軌道束を作った。12 次元候補より小さい棚は次の通り。

| 軌道束 | 次元 | \(\theta\) Jordan | \(\dim H^2(C_2,-)\) | SURJ 欄 |
|---|---:|---|---:|---|
| 自明 | 1 | \(J_1\) | 1 | relative \(H^1=0\) |
| \(S_4/V_4\) の単純 \(D\) | 2 | \(J_2\) | 0 | 入口条件なし |
| 1 座標支持の軌道 | 6 | \(J_2^3\) | 0 | 入口条件なし |
| 3 座標支持の軌道 | 8 | \(J_2^4\) | 0 | 入口条件なし |
| **2 座標支持の軌道** | **12** | **\(J_2^5\oplus J_1^2\)** | **2** | **7 全射類** |

2 座標支持の束は

\[
 E_{12}\oplus E_{23}\oplus E_{13},\qquad \dim E_{ij}=4,
\]

である。各 \(E_{ij}\) は、\(C_2^2\) が 4 個の相異なる \(A\)-weight を推移的に動かすため単純。三者は \(A\) への制限が異なるので互いに非同型で、\(\theta,\tau\) は三者を推移的に動かす。

機械 gate は各ブロックで

```text
nonzero cyclic submodule dimension distribution   {4:15}
Hom_W dimension matrix                            [[1,0,0],[0,1,0],[0,0,1]]
End_W(V)                                          F_2^3
End_W(V)^x order                                  1
```

だった。従って、上記半単純軌道束棚の中で \(H^2(C_2,V)\ne0\) と全射類の両方を初めて満たす最小次元は 12 である。

### 1.3 選択加群の生行列値

行列は \(A\)-weight の \(\{\pm a\}\) 6 対を 2 次元 \(\mathbf F_2\) ブロックとして作った。\(C_3\) の行列は

\[
 R=\begin{pmatrix}0&1\\1&1\end{pmatrix},
 J=\begin{pmatrix}0&1\\1&0\end{pmatrix}, JRJ=R^{-1}.
\]

full marked image と pure image の位数は

```text
|<theta,tau>|        648   (= |B3/K^(3)| model)
|<rho(x),rho(y)>|    108   (= |G3|)
ord rho(x),rho(y)      6,6
theta_matrix_sha256   3534a019f7c5408eb56b1d819589410fdb57a62244d9cefa9ca9657a7472c30a
tau_matrix_sha256     2002346251152ba9d1d1b3ffc4ffb6f53df431c2d5f601f98870e1190c0ca6a7
rho_x_sha256          49b6c09642c15f9ecb1e0bfdc7b24f1ff5549a1e2992cbdd02c9ca2565da510a
rho_y_sha256          c5a3a733a603f3a026a961370e7f0ca880766525d843fb67c5ad026f8f6fe478
```

checker は NumPy 行列を読まず、bit-column 行列から同じ位数 \(648,108\) と \(H^2\) の 6 生値を再構成した。

## 2. compact 路の \(\mathbf F_2\) 移植

### 2.1 名前と宇宙

NAME-COLLIDE を避け、次で固定する。

\[
 N_W=N_{S4}\cap K^{(3)},\quad
 W=PB_3/N_W\cong P\times G_3,\quad
 \bar W=B_3/N_W.
\]

1 個の anchor window と各全射 class に対して、(N_E) を marked affine map の核、

\[
 K=K^{(9)}\cap N_E,\, M=K^{(9)}\cap N_{S4},\,
 W_{\rm ker}=M/K\cong V
\]

とする。\(P\) は \(V\) に自明に作用し、\(G_3\) が三つの 4 次元成分に作用する。

### 2.2 gauge / NORM-TWIST / anchor

\(\mathbf F_3\) 版との主要差分は scalar unit が消えることである。

```text
End_W(V)                        F_2^3
gauge group order                    1
effective gauge order                1
anchor solutions                     1
anchor windows                       1
A1: rho(sigma_1^2)=rho(x)         true
A2: rho(sigma_2^2)=rho(y)         true
```

従って NORM-TWIST で残る符号 bit はなく、唯一の weight-pair 規約を行列 SHA-256 で固定した。

### 2.3 SURJ-LIN

\(\Gamma=C_2*C_3\) 上の cocycle 計算は

```text
dim Z^1(Gamma,V)                 15
dim B^1(Gamma,V)                 12
dim H^1(Gamma,V)                  3
|H^1(Gamma,V)|                    8
H1 basis sha256                  22ecc22b0f37628039d22e25321eb6a1ff91a6c4e4253c2009c17a11ca059a04
```

となった。一方、108 元の (G_3) Cayley graph の全 positive-edge collision から

```text
dim Z^1(G3,V)                    12
dim B^1(G3,V)                    12
dim H^1(G3,V)                     0
relation rref sha256             e281a876a1790c99ea0cc3c8980a8067447168e97a0be2d4cbc5d267fe50d323
```

を得た。\(P\) は perfect かつ \(V\) に自明に作用するので \(H^1(\bar W,V)=0\)。従って 8 class のうち零 class だけが降下し、残る 7 class が全射欄へ入る。独立 checker は各 cocycle を 108 元へ延長できるか collision で直接調べ、flags

```text
[true,false,false,false,false,false,false,false]
```

を得た。

### 2.4 障害の座・full equations・GEN-AFF

\(C_3\) 側は 3 が可逆なので較正どおり \(H^2(C_3,V)=0\)。残る受け皿は

\[
 H^2(C_2,V)=V^\theta/(1+\theta)V\cong\mathbf F_2^2
\]

で、(3.10) の \(\theta\) 側に置いた。

roof は既存の 54 個の \(N_{S4}\) 行と 12 個の \(K^{(3)}\) 行を \(m\bmod3\) で glue した 324 行。各行の \(K^{(9)}\) preimage は 3 個である。charming / target generation gate は既存 cert の pass 行だけから作った。さらに producer と checker はいずれも簡約式だけには依存せず、full (3.3)(3.4) を直接評価した。

全 324 template の生値は一様だった。

```text
A shape                         24 x 12
rank A1 distribution           {9:324}
rank A2 distribution           {9:324}
rank [A1;A2] distribution      {9:324}
dim ker [A1;A2]                 {3:324}
template sha256                2514b6f6dbe46480273b588bfffca590ce5df2144f761b627d26f8d0ae77d941
```

GEN-AFF は三つの非同型 4 次元成分それぞれについて graph/coboundary 条件を検査した。従って「hexagon 解あり」と「生成解あり」は独立欄である。

## 3. freeze と実行境界

正式な三段のファイル境界自体は作った。

| 段 | outcome opened by that stage | wall | SHA-256 |
|---|---:|---:|---|
| preflight / template gate | 0 | 6.824 s | `d5942eae32b038eaafd3a0bc8a9b67ba78df35b073c4973c98352c4ceefd2a76` |
| versioned freeze | 0 | 6.936 s | `006000c95099c68c39ab18ff7a2e1e3f73fba3ce5616868adeb13b5a76da78d8` |
| producer measurement | 2,268 | 7.371 s | `7daa9cc6ac66683ed9d663bb70e311517c12d6c429aacf7039f11c1ebdc0a29b` |
| independent checker | 2,268 | 112.728 s | `7283a8ba0d0fc1ebcb9203ecc2c8e82499c8c582e3dcc4327f1a1734c41bb2d3` |

freeze した宇宙は

```text
anchor windows                 1
surjective classes             7
rows per class               324
total rows                  2,268
rank gate                    fixed
directional prediction       null
```

で、本走中の拡張・縮小はない。ただし §0 のとおり、これ以前の engineering pilot が同じ 2,268 行を開いたので、freeze の格は prospective ではない。

## 4. 本走の全生値

### 4.1 集計

```text
evaluated rows                         2,268
H2(C2) class distribution              {[0,0]:2268}
H2(C3) class distribution              {[]:2268}
nonzero obstruction row count          0
linear solution count distribution     {8:2268}
generating solution count distribution {6:972, 8:1296}
generation-absent row count             0
zero-survival target count              0
Im R_(N_E,N_W) distribution             {324:7}
Im R_(K,M) distribution                 {972:7}
theta2 count distribution               {3:378}
producer outcome sha256                 1181803675e7f1b4655d155454b8a14a2dc499a51810b09f4760800f094ae482
checker mismatch_count                  0
```

`theta2 count {3:378}` は、7 class × 54 個の (N_{S4}) target の各々で三つの `k_mod3` が全て残った、という生値である。

### 4.2 全 7 class

座標基底は §2.3 の SHA-256 で固定した。

| class position | class index | \(H^1\) 座標 | 非零障害行 | 生成欠損行 | lift 行 | 生成解数分布 | \(|\operatorname{Im}R_{K,M}|\) |
|---:|---:|---|---:|---:|---:|---|---:|
| 0 | 1 | `[0,0,1]` | 0 | 0 | 324 | `{8:324}` | 972 |
| 1 | 2 | `[0,1,0]` | 0 | 0 | 324 | `{6:324}` | 972 |
| 2 | 3 | `[0,1,1]` | 0 | 0 | 324 | `{8:324}` | 972 |
| 3 | 4 | `[1,0,0]` | 0 | 0 | 324 | `{6:324}` | 972 |
| 4 | 5 | `[1,0,1]` | 0 | 0 | 324 | `{8:324}` | 972 |
| 5 | 6 | `[1,1,0]` | 0 | 0 | 324 | `{6:324}` | 972 |
| 6 | 7 | `[1,1,1]` | 0 | 0 | 324 | `{8:324}` | 972 |

### 4.3 最初の行と非零欄

非零障害行は存在しないので、指定された「最初の非零行」は

```text
first_nonzero_obstruction = null
```

である。規約確認用の最初の lift 行は次。

```text
class_position               0
class_index                  1
class_coordinates            [0,0,1]
t_index                      0
t2_index                     0
k3_index                     0
k_mod3                       0
H2_C2_coordinates            [0,0]
H2_C3_coordinates            []
left_null_obstruction        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
linear_solution_count        8
generating_solution_count    8
lift                         true
```

この全消滅を一般定理へ拡張しない。少なくとも、(p=3) 側の 28 次元例に加え、(p=2) 側の本 12 次元例でも「障害群は非零だが、測った実障害写像の像は零」という生値になった。消滅の紙の理由、非半単純加群への射程、各 (N_E) の isolated 性はいずれも **UNKNOWN** である。

## 5. 終盤欄

```text
endgame_scope = gentle side only; no finite-depth type adjudication
PENT_W                                      NOT_RUN
FAKE-KILL^{B4}/U-10                         NOT_RUN
required elevation order                    PENT_W-PASS, then FAKE-KILL^{B4}/U-10
```

本便の有限深度値から型の認定は行っていない。

## 6. 独立照合・再現・成果物

producer は NumPy と既存 compact engine の行列 helper を再利用した。checker はそれらを import せず、純 Python の bit-column 行列で次を独立に行った。

1. 12 次元 weight-pair 表現、位数 648/108、(H^2) を再構成。
2. 8 cocycle class の (G_3) への descent を 108 元の collision で検査。
3. 7×324 行の各々で (2^{12}=4,096) 個の (f)-平行移動を直接評価。
4. 各解について三つの 4 次元成分の coboundary 条件を総当りし、生成解を数えた。

checker の最終値は

```text
agreement                       true
mismatch_count                  0
group_orders                    {full:648, pure:108}
descent_census                  {classes:8, descends:1, surjective:7}
solution_count_distribution     {8:2268}
generation_distribution         {6:972,8:1296}
Im R_(K,M) distribution         {972:7}
```

だった。両 lane は source cert だけを共有し、線型 template helper と outcome helper は共有していない。

成果物は契約に従い repo 外

```text
%TEMP%\shadow-atelier-escape2-136\
```

に置いた。

| artifact | bytes | SHA-256 |
|---|---:|---|
| `escape2_producer_v1.py` | 26,821 | `3bf3c92fe66f2a121753a092135e2155e1878660bd411f88311abaff43b24996` |
| `escape2_checker_v1.py` | 17,083 | `c7fcbfb4b3bafd3504420158827f4dd6c5d42a9c4433cc271e3d3bdc62529383` |
| `escape2_preflight_v1.json` | 8,429 | `d5942eae32b038eaafd3a0bc8a9b67ba78df35b073c4973c98352c4ceefd2a76` |
| `escape2_prereg_v1.json` | 773 | `006000c95099c68c39ab18ff7a2e1e3f73fba3ce5616868adeb13b5a76da78d8` |
| `escape2_mainrun_v1.json` | 6,520 | `7daa9cc6ac66683ed9d663bb70e311517c12d6c429aacf7039f11c1ebdc0a29b` |
| `escape2_checker_v1.json` | 3,875 | `7283a8ba0d0fc1ebcb9203ecc2c8e82499c8c582e3dcc4327f1a1734c41bb2d3` |

checkpoint は全て `complete=true`。hard-timeout は各 lane 180 秒で、producer 7.371 秒、checker 112.728 秒だった。

再実行時は、archive した二スクリプトを一時的に repo の `scratchpad/` 直下へ同じ内容で置く（スクリプトは `ROOT=parents[1]` を用いる）。出力先は repo 外のままにする。

```powershell
$escape2Tmp = Join-Path $env:TEMP 'shadow-atelier-escape2-136-rerun'
New-Item -ItemType Directory -Force -Path $escape2Tmp | Out-Null

# archive scripts を scratchpad/_escape2_producer_v1.py / _escape2_checker_v1.py に一時配置後
python -B scratchpad/_escape2_producer_v1.py --mode preflight --preflight (Join-Path $escape2Tmp 'preflight.json') --prereg (Join-Path $escape2Tmp 'prereg.json') --output (Join-Path $escape2Tmp 'main.json') --checkpoint (Join-Path $escape2Tmp 'preflight.checkpoint.json') --hard-timeout-seconds 180
python -B scratchpad/_escape2_producer_v1.py --mode freeze --preflight (Join-Path $escape2Tmp 'preflight.json') --prereg (Join-Path $escape2Tmp 'prereg.json') --output (Join-Path $escape2Tmp 'main.json') --checkpoint (Join-Path $escape2Tmp 'freeze.checkpoint.json') --hard-timeout-seconds 180
python -B scratchpad/_escape2_producer_v1.py --mode measure --preflight (Join-Path $escape2Tmp 'preflight.json') --prereg (Join-Path $escape2Tmp 'prereg.json') --output (Join-Path $escape2Tmp 'main.json') --checkpoint (Join-Path $escape2Tmp 'measure.checkpoint.json') --hard-timeout-seconds 180
python -B scratchpad/_escape2_checker_v1.py --preflight (Join-Path $escape2Tmp 'preflight.json') --producer (Join-Path $escape2Tmp 'main.json') --output (Join-Path $escape2Tmp 'checker.json') --checkpoint (Join-Path $escape2Tmp 'checker.checkpoint.json') --hard-timeout-seconds 180
```

入力 SHA-256 は次。

| input | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_136_escape2.txt` | `d7da562456c0a2b00f65e0788e09e56027d2c336627b108b38d29df560d02c08` |
| `docs/notes/vnbit_compact_route_v3.md` | `ff9febbcb47142cbc1716b326b4ca5684a2a57ca1639a44142d697aefe2e6432` |
| `docs/notes/entangled972_reading_v1.md` | `0a439e48b8df64b0472402125abe887b026a637633db7953942e6688a897887a` |
| `search/vnbit_compact_mainrun_v3.py` | `4ba20a286e9616c9363a9e8187fb4c35d04e11a6dbc4610c17d3879e5c47eb9a` |
| `search/escape28_mainrun_v1.py` | `2acdbdd17c30f28ea3709cf6f44ee47dd81e9868a8ae64b364926f3c4e1ea6b8` |
| `certificates/S4.v2.json` | `c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d` |
| `certificates/K3.v1.json` | `d7cd44ea6d71e341e3e1a6164ce03540e92c50d405113ad1d3dc26972b1e8171` |
| `certificates/K9.v1.json` | `ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e` |

## 7. novelty / noncontact / FINDING

実行後、返書自身と受信便を除いて固定文字列 grep を行った。

```text
"2 座標支持"     0
"二座標支持"     0
"support-two"     0
"J_2^5"           0
"H2_C2_dimension" 0   (非 JSON 文書)
```

これは語の未出だけを示し、数学的優先権の証明ではない。

封印欄は producer / checker とも

```text
u                       false (not opened)
c                       false (not opened)
sealed_three_quantities false (not opened)
sealed_K5               false (not opened)
```

である。作業ツリーに残した新規ファイルは本返書だけで、git commit / push / workflow dispatch は行っていない。

| # | 生値・未閉鎖 |
|---|---|
| F1 | 半単純軌道束 lane の最小実用候補は \(V=E_{12}\oplus E_{23}\oplus E_{13}\)、\(\dim V=12\)、\(\dim H^2(C_2,V)=2\)、\(\dim H^2(C_3,V)=0\)。 |
| F2 | anchor window 1、全射 class 7、全 2,268 行で非零障害 0、生成欠損 0、\(|\operatorname{Im}R_{K,M}|=972\) が 7/7。checker mismatch 0。 |
| F3 | 実障害写像が零になる紙の理由は **UNKNOWN**。一般の \(p=2\) 加群や非半単純 extension へ量化しない。 |
| F4 | `N_E_isolated=UNKNOWN`。有限深度値から型語へ移さない。 |
| F5 | prereg は pilot 後で **非 prospective**。数値の cross-check と事前登録の格を混同しない。 |

