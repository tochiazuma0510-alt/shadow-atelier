# 返書 131 — compact v2 標識作用の入口監査

日付: 2026-08-13  
委嘱: `ops/inbox_codex/sol_task_131_measurement.txt`  
仕様正本: `docs/notes/vnbit_compact_route_v2.md` (指定 commit `0f81f6402614e93298f2549aa7fabbf4982ccafe`)  
実行時 HEAD: `cfc6117546db8d12fa9fdc932b9f0634c8183e68`

## 0. 一行と到達段

便 131 の §0、§1.1–§1.5、§2、§3 を順に処理した。到達段は **SURJ-LIN の直前**であり、機械状態は

```text
stopped_before_SURJ_LIN / marked_pure_anchor_mismatch
```

である。C-4′ に従い isolated 性を入口条件にはしていない。しかし、便 130 から凍結された純部分の作用と v2 の $(U,S)=(\theta,\tau)$ は同じ $B_3$-表現を定めない。したがって、この入力のまま 324 行を開くと指定された $E=V\rtimes W$ とは別の加群を測ることになるため、標識作用の型で停止した。

producer と、別 heart 基底・別消去法・NumPy 非使用の checker は同じ不一致 rank $(14,14)$ を得た。これは **cross-checked（照合済み）**である。Lean 証明書は作っていないので verified ではない。

## 1. 委嘱 §1

### 1.1 標識対の構成

BU-S35 §43/61 と定義正本を逐語的に用いると

\[
\sigma _1=\delta^{-1}\Delta,\qquad
\sigma _2=\Delta^{-1}\delta^2,
\qquad x=\sigma_1^2,\quad y=\sigma_2^2.
\]

従って、列ベクトルへの左作用を用いる便 130 の行列では必ず

\[
R_{\sigma_1}=\tau^{-1}\theta=\tau^2\theta,qquad
R_{\sigma_2}=\theta^{-1}\tau^2=\theta\tau^2
\]

でなければならない。凍結行列に対する生値は次のとおりだった。

| 検査 | 生値 |
|---|---:|
| $\theta^2=I$ | `true` |
| $\tau^3=I$ | `true` |
| $R_{\sigma_1}R_{\sigma_2}=\tau$ | `true` |
| $R_{\sigma_1}R_{\sigma_2}R_{\sigma_1}=\theta$ | `true` |
| braid 語の一致 | `true` |
| $(R_{\sigma_1})^2=\rho(X)$ | `false` |
| $(R_{\sigma_2})^2=\rho(Y)$ | `false` |
| $\operatorname{rank}_{\mathbf F_3}((R_{\sigma_1})^2-\rho(X))$ | **14** |
| $\operatorname{rank}_{\mathbf F_3}((R_{\sigma_2})^2-\rho(Y))$ | **14** |

より具体的には、便 130 の block 順 $(\chi_{10},\chi_{01},\chi_{11})$ で

\[
(R_{\sigma_1})^2=\operatorname{diag}(R_X,R_X,R_X),qquad
\rho(X)=\operatorname{diag}(-R_X,R_X,-R_X),
\]
\[
(R_{\sigma_2})^2=\operatorname{diag}(R_Y,R_Y,R_Y),qquad
\rho(Y)=\operatorname{diag}(R_Y,-R_Y,-R_Y).
\]

差分 rank 14 は、各式で符号が欠けた 7 次元 block が二つあることと一致する。原因は、便 130 の `extended_operator` が外側作用による **block の置換だけ**を入れ、$G_3$ の三つの指標値を実現する monomial scalar factor を入れていないことにある。$U,S$ の $V$-成分 $a,b$ は affine 定数項しか変えず、線形部分のこの不一致を直せない。

従って、現データからは

\[
(U,S)\in\widetilde E^2,qquad U^2=S^3=1,qquad
\langle U,S\rangle=\widetilde E
\]

を **便 130 の $W$-作用を延長する標識対として**構成できていない。`center_in_linear_kernel=true` だけでは純部分 anchor の代用にならない。

#### 修理診断（未採用）

$3\times3$ monomial 部分の source-block scalar を $\{\pm1\}$ で悉皆すると、両 pure anchor を回復する組は **8 個**あった。辞書順先頭は

\[
\theta'=\theta,qquad
\tau'=\tau\,D,qquad
D=\operatorname{diag}(I_7,-I_7,-I_7)
\]

であり、producer/checker の双方で

\[
((\tau')^{-1}\theta')^2=\rho(X),qquad
((\theta')^{-1}(\tau')^2)^2=\rho(Y)
\]

を再現した。ただし v2 はこの scalar factor を凍結しておらず、8 候補の gauge・twist・kernel 同値性も証明していない。この候補を測定入力には使っていない。

再開に必要なのは次の versioned 入力である。

1. $\sigma_1^2\mapsto\rho(X)$、$\sigma_2^2\mapsto\rho(Y)$ を anchor として満たす monomial lift $(\theta',\tau')$ を一つ凍結する。
2. 他の7候補との関係を、少なくとも window kernel を変えない範囲まで記述する。または正規化により一候補だけを定義する。
3. 修正版 C-2 の行列 hash を更新し、C-3′ の必須欄に二つの pure-anchor 等式を追加する。

### 1.2 SURJ-LIN 分類

標識対が凍結 $W$-作用を延長しないため、`Z^1(\bar W,V)` の機械関係列は生成していない。従って

| 項目 | 到達値 |
|---|---:|
| $H^1(C_2*C_3,V)$ の既存前段類 | 81（便 130 の入力値、再解釈なし） |
| $Z^1(\bar W,V)$ | 未計算 |
| $|H^1(\bar W,V)|$ | `null` |
| 全射類数 | `null` |
| class membership | 0/81 |
| 関係子列 digest | 無し |

関係子を手で固定する代替は行っていない。仕様 GEN-SUB の機械出力束縛は、修正版標識を得た再開便で最初から行う必要がある。

### 1.3 事前登録

委嘱順は「SURJ-LIN 分類 → P-vNC2-1〜5 の採録 → 測定」である。前段で停止したため task 131 の事前登録ファイルは作っていない。

- P-vNC2-1 の式 $81-|H^1(\bar W,V)|$: 仕様値のまま、右辺未測定。
- P-vNC2-2 の $\operatorname{rank}(A_1)=\operatorname{rank}(A_2)$: 必須欄として維持したが、展開行がないため値は `null`。
- P-vNC2-3 の集合 $\{972,324\}$: 非接触・変更なし。
- P-vNC2-4、P-vNC2-5: heuristic のまま、結果非接触。
- blind 申告: 324 行の outcome は一件も開いていない。

修正版入力の採択前に後付け prereg を置くと、異なる標識作用に予言を流用することになるため行っていない。

### 1.4 全射類 $\times324$ 行の測定

測定値は次で固定した。

| 項目 | 生値 |
|---|---:|
| 形成した $GT(N_W)$ 行 | 0/324 |
| 測定した全射類 | 0 |
| $42\times21$ の affine 系 | 0 |
| $[b_t]\in\operatorname{coker}(A_t)$ | 0 |
| `generating_solution_exists` | 0 |
| class ごとの分布 | `null` |
| $t_2$ ごとの分布 | `null` |
| $|\operatorname{Im}R_{K,M}|$ | `null` |
| $\Theta_2$ rigidity | `null` |

`A_shape` は仕様どおり `rows=42, cols=21` を保持し、`rank_A1`、`rank_A2`、`rank_A1_equals_rank_A2` はすべて `null` とした。obstruction 消滅と生成解存在を同一視する操作はしていない。

C-4′ は「isolated 未確認でも、**正しく型付けされた**標識作用について測定を続ける」という運用である。今回の停止は isolated 性によるものではない。`N_E_isolated="UNKNOWN"` と `vNB-GAP-1="open"` はそのまま保持した。

### 1.5 生値、cert、到達段

producer run ID は `vnbit-compact-measurement-20260813T054341Z`、checker run ID は `vnbit-compact-measurement-check-20260813T054524Z`。両方とも atomic checkpoint と内部120秒 hard-timeout を持ち、checkpoint は `complete=true` である。

checker は producer を import せず、次を独立に行った。

- 監査済み9点置換 $S,T$ を直書きし、GF(8) helper を共有せず $X,Y$ を再構成。
- heart は $e_i-e_0\ (1\le i\le7)$、$e_8-e_0$ を消去する別基底。
- 有限体消去は標準ライブラリだけの別実装。
- 64 組の monomial scalar を別 loop で悉皆し、8候補と辞書順先頭による両 anchor の回復を再現。
- producer cert の停止段、0行、非接触欄を再照合。

checker の `all_equalities_true=true`。GAP はこの入口等式に不要なので起動していない。

## 2. 終盤勘定の scope pin

本便は gentle $\widehat{GT}_{\rm gen}$ 側の前段だけを対象とする。B 分岐の反証候補昇格には B4 層で **PENT_W-PASS** を検査し、その後 `FAKE-KILL^{B4}/U-10` を適用する必要がある。有限深度の本データから B 型を認定していない。

同文を raw cert の `endgame_scope` と checker cert の `scope` に保存した。

## 3. 規律、novelty 領収書、provenance

### 3.1 規律

- $u,c$: 非接触。
- 封印3量、sealed K5: 非接触。
- 凍結された $\{972,324\}$ と P-vNC2-4/5: 非接触。
- `UNKNOWN`: isolated 性と未到達量を `null`/`UNKNOWN` のまま保存。
- NAME-COLLIDE: $W=PB_3/N_W$ の純作用と $\bar W=B_3/N_W$ の標識作用を分記した。
- relation list の手固定: なし。
- 324 outcome の観測: なし。
- 有限深度からの型認定: なし。
- git commit、push、workflow dispatch: なし。
- 着手前から存在した他便の変更には触れていない。

### 3.2 novelty grep（実行後・task 131 新規物を除外）

仕様 §7 の6系列を `docs/` と `sol/` に対して再走した現在の raw count は順に

```text
Delta/delta marking       6
C2*C3 / PSL(2,Z)         55
OneCocycles / Z^1(W)      0
marked surjection         1
42x21 / dependency        5
H^1(bar W) / surj class   2
```

だった。本便の増分は SURJ-LIN の数値ではなく、**block permutation だけでは pure character anchor を延長しない**という入口不整合と、その monomial scalar 修理候補の機械診断である。

### 3.3 SHA-256

入力:

| 入力 | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_131_measurement.txt` | `bb4833c672a9731bcc4fc92c7528c07cc63550ca1216c34e5e90cadb3defc885` |
| `docs/notes/vnbit_compact_route_v2.md` | `0c449f94657015b3e7240bf718233888a48c921ddd29793d0a873cecca20ada0` |
| `docs/notes/bu_s35_embedding_v1.md` | `dfdb7557972208d4f16907017e9c5c52195859acb9d1eb11013922e83ba87e86` |
| `docs/week1-定義ノート.md` | `24db1372fd191659f1f0149cb669870dff470db1f779d3e5f83dba4171501c6c` |
| `search/certs/vnbit_affine_gate_raw_v1_20260813.json` | `24b78fc1e700223f1be27dabf77e1fed65af6e58c4e28362be7d802f563bb5ee` |

成果物:

| 成果物 | SHA-256 |
|---|---|
| `search/vnbit_compact_measurement_v2.py` | `8a0062f296fd1fa598c50a0683c5ca0cde838cbb879e867e8f12b4b7cb5983e8` |
| `search/certs/vnbit_compact_measurement_raw_v2_20260813.json` | `26dad8a4951a3e847f4df304b2c24b946758d676cd57d56406e6d0c1d7521988` |
| `search/certs/vnbit_compact_measurement_v2_checkpoint.json` | `40e8ec9903c70ab231a03c5897223c7398ab30edc544ba0813a3fb50a82dd60f` |
| `search/check_vnbit_compact_measurement_v2.py` | `f5d97d589588836b221ca4d7833e1c3b6f2a61e18d0beedc90e0068029ecd723` |
| `search/certs/vnbit_compact_measurement_check_v2_20260813.json` | `57e60cc74ed46d572992abf2156633551077a9354694d799c55707083abea7fc` |
| `search/certs/vnbit_compact_measurement_check_v2_checkpoint.json` | `5f1212d8be4e76c630a3f373459b441eaf8200bcd8335664f80c6d5101346de9` |

## 4. 司令塔向け再開 pin

324行への最短再開点は、v2 の前に次を一行追加することである。

```text
C-2′ pure-anchor: ((tau')^-1 theta')^2 = rho(X) and ((theta')^-1 (tau')^2)^2 = rho(Y)
```

その上で monomial scalar の正規化を versioned に凍結し、**SURJ-LIN を再計算してから** P-vNC2-1〜5 を事前登録する。現 cert の8候補は修理設計の候補集合であって、測定結果ではない。
