# 返書 133 — ESCAPE-28 非自由成分つき 28 次元窓

日付: 2026-08-13  
委嘱: `ops/inbox_codex/sol_task_133_escape28.txt`  
仕様正本: `docs/notes/entangled972_reading_v1.md` (`915ca797`) + `docs/notes/vnbit_compact_route_v3.md`  
実行時 HEAD: `45e5789cd597086664cc11c41f711d07eb28b4a1`

## 0. 一行

便133の §0–§3 を順に処理した。28 次元窓では

```text
dim H²(C3,V28) = 2
```

と障害群が実際に生存する。しかし NORM-TWIST の4窓、SURJ-LIN の全3,392類、各324行、計 **1,099,008行**で障害類はすべて0だった。生成解は全行に存在し、別 heart 基底 checker の不一致は0である。従って指定された停止条件

```text
H²≠0 下の全消滅
```

に到達した。ここで停止する。この全消滅の紙の理由は今回の入力定理からは出ず、新しい消滅機構を説明する理論が必要である。有限深度の型認定は行っていない。

## 1. 委嘱

### 1.1 入口検査 — H² と全8 Jordan 型

$H^2(C_3,V)=\ker(\tau-1)/\operatorname{Im}(1+\tau+\tau^2)$ を行列から再計算した。7 次元の全 Jordan 型は次の8通りである。

| Jordan 型 | dim fixed | rank norm | dim H² |
|---|---:|---:|---:|
| `3+3+1` | 3 | 2 | 1 |
| `3+2+2` | 3 | 1 | 2 |
| `3+2+1+1` | 4 | 1 | 3 |
| `3+1+1+1+1` | 5 | 1 | 4 |
| `2+2+2+1` | 4 | 0 | 4 |
| `2+2+1+1+1` | 5 | 0 | 5 |
| `2+1+1+1+1+1` | 6 | 0 | 6 |
| `1+1+1+1+1+1+1` | 7 | 0 | 7 |

実際の $V_7\otimes\mathbf1$ 上の $\tau$ は `3+2+2` である。従って

```text
V21 orbit bundle : Jordan 3^7,       fixed=7, norm rank=7, H²=0
V7  trivial char : Jordan 3+2+2,     fixed=3, norm rank=1, H²=2
V28 total        : Jordan 3^8+2+2,   fixed=10,norm rank=8, H²=2
```

で、命題 ESCAPE-28 の下界 `>=1` を強める生値は **2** だった。全8型の最小値は1、最大値は7で、$3\nmid7$ による入口条件も再現した。

対照の9次元置換ブロック系は

```text
Jordan 3+3+3, fixed=3, norm rank=3, dim H²(C3,V9)=0
```

すなわち $\mathbf F_3[C_3]^3$ として自由である。この行は分類比較用の生値だけであり、この9次元系では OBS-VOID が直ちに働くため後続測定へ進めていない。

### 1.2 28 次元 C-2′ / anchor / NORM-TWIST / C-9

#### pure anchor

4窓すべてで

```text
((tau')^(-1) theta')^2       = rho(X)
((theta')^(-1) (tau')^2)^2  = rho(Y)
```

が成り立ち、両差分 rank は0だった。$\theta'^2=I$、$\tau'^3=I$ も保持される。4ブロックの符号生値は

```text
rho(X): (-,+,-,+)
rho(Y): (+,-,-,+)
```

で、先頭3ブロックは従来の巡回整合、追加ブロックは $G_3$ 自明ゆえ両方 `+` である。

#### gauge と twist 分類器

4つの相異なる $W$-既約成分に対する機械勘定は

```text
End_W(V28)                     = F_3^4
|End_W(V28)^x|                 = 16
共役核                          = 4
実効 gauge 位数                 = 4
pure-anchor scalar 解           = 16
gauge 軌道                       = 4 個、各サイズ 4
H¹(S3,F_2^4): dim Z¹/B¹/H¹      = 4/2/2
|H¹(S3,F_2^4)|                  = 4
```

である。追加した固定点成分が $H^1(S_3,\mathbf F_2)$ のもう1ビットを与えるため、21次元の2窓は28次元では **4窓**になる。$\tau'$ の4符号を `(+,+,+,+)` に固定し、$\theta'$ の軌道束ビットを `eps`、自明指標ブロックの符号を `eta` とした。

| 窓 | θ′ source-block 符号 | dim ker(I+θ′) | dim ker norm(τ′) | \|H¹(Γ,V)\| |
|---|---|---:|---:|---:|
| `eps=+,eta=+` | `(-,-,+,+)` | 15 | 20 | 2187 |
| `eps=+,eta=-` | `(-,-,+,-)` | 14 | 20 | 729 |
| `eps=-,eta=+` | `(+,+,-,+)` | 14 | 20 | 729 |
| `eps=-,eta=-` | `(+,+,-,-)` | 13 | 20 | 243 |

`eps` の向きは従来どおり

```text
+ : fa7796d0afd372982ef29294483f2e1f47b06b54f795ccf2f90dee71cf2cca8f
- : ec5586d4dee204d5a9ed7db38d92c0c3d0cbbad7f27f525729b4ea2c296b6a16
```

で固定した。同じ2 digest が `eta` の $\pm R_S$ にも現れるため、cert では `B_matrix_sha256` と `trivial_theta_matrix_sha256` を別欄に束縛した。

#### C-9 系

```text
|P|                                      504
V7 の非零 cyclic submodule 次元分布       {7:2186}
dim_F3 End_P(V7)                          1
V7 absolutely irreducible over F3         true
```

さらに $X,Y$ の2作用から全16個の Hom 空間を再計算し、

```text
dim Hom_W(V_i,V_j) = identity 4x4 matrix
```

を得た。従って4成分は対ごとに非同型、`dim End_W(V28)=4`、unit 位数16という gauge 前件と一致する。

### 1.3 28 次元 SURJ-LIN と blind prereg

28次元 $V=A_{21}\oplus B_7$ は $\bar W$-加群として2つの非同型成分を持つ。そのため、既約1成分用の単純な差

```text
|H¹(Gamma,V)| - |H¹(barW,V)|
```

をそのまま使ってはいけない。全射には両成分の translation kernel が必要なので、今回の SURJ-LIN は

```text
(|H¹(Gamma,A)|-|H¹(barW,A)|)
  * (|H¹(Gamma,B)|-|H¹(barW,B)|)
```

となる。inflation 部分は手固定 relator でなく、$P$ の504頂点・正向き1008辺の Cayley collision 系から各 class を明示判定した。

| 成分窓 | \|H¹(Γ)\| | \|H¹(barW)\| | 全射成分類 |
|---|---:|---:|---:|
| orbit `eps=+` | 81 | 1 | 80 |
| orbit `eps=-` | 27 | 1 | 26 |
| trivial `eta=+` | 27 | 3 | 24 |
| trivial `eta=-` | 9 | 1 | 8 |

従って全窓の全射類は

| 窓 | 積 | 全射類 | 324倍した行数 |
|---|---:|---:|---:|
| `eps=+,eta=+` | `80*24` | 1920 | 622,080 |
| `eps=+,eta=-` | `80*8` | 640 | 207,360 |
| `eps=-,eta=+` | `26*24` | 624 | 202,176 |
| `eps=-,eta=-` | `26*8` | 208 | 67,392 |
| 合計 | — | **3,392** | **1,099,008** |

full hexagon の coefficient gate は $56\times28$。324行すべてで `rank(A1)=rank(A2)` となり、窓順に

```text
rank(A1)=rank(A2)=rank(A) : 21,22,22,23
dim ker(A)                 :  7, 6, 6, 5
```

だった。

本走前に r2 prereg へ、4窓・3,392類・324行・上の rank gate・direct-sum factorisation・outcome UNKNOWN を凍結した。方向付きの障害予言は置いていない。

初回 r1 の本走試行は outcome を1件も開く前の preflight reconstruction hash gate で停止した。原因は `m mod 18` 分布の数値 JSON key が read-back 後に文字列化され、値の差0でも sort 順だけが変わったことだった。JSON 正規化後の比較へ直し、新ファイル r2 を作った。r2 prereg の履歴欄に

```text
lift_outcomes_opened = 0
```

を保存している。r2 preflight の別基底照合も不一致0の後に凍結した。

### 1.4 本走 — 障害と生成の独立欄

LIFT-AFF と GEN-AFF は $A_{21}\oplus B_7$ 上で直和分解する。producer は両成分を別々に全測定し、障害消滅を論理積、affine 解数と生成解数を積として全 Cartesian 行へ展開した。checker は別 heart 基底で full hexagon、roof、成分 inclusion-exclusion、全 Cartesian 展開を作り直した。

成分の生値は次のとおり。

| 成分窓 | 行数 | 非零障害 | 生成解数分布 |
|---|---:|---:|---|
| orbit `eps=+` | 25,920 | 0 | `{80:25920}` |
| orbit `eps=-` | 8,424 | 0 | `{27:5832, 24:2592}` |
| trivial `eta=+` | 7,776 | 0 | `{27:5184, 24:2592}` |
| trivial `eta=-` | 2,592 | 0 | `{8:2592}` |

全行展開後の分布は次のとおり。

| 窓 | 全行 | affine 解数/行 | 生成解数: 行数 | 非零障害行 | 生成解欠如行 |
|---|---:|---:|---|---:|---:|
| `eps=+,eta=+` | 622,080 | 2187 | `2160:414720, 1920:207360` | 0 | 0 |
| `eps=+,eta=-` | 207,360 | 729 | `640:207360` | 0 | 0 |
| `eps=-,eta=+` | 202,176 | 729 | `729:93312, 648:88128, 576:20736` | 0 | 0 |
| `eps=-,eta=-` | 67,392 | 243 | `216:46656, 192:20736` | 0 | 0 |

従って最重要欄は

```text
nonzero_obstruction_rows = []
```

である。非零行の class / t2 生値は存在しない。障害欄とは独立に、生成解数は全1,099,008行で正だった。

全類について roof の324行が持ち上がり、分布は各窓で

```text
|Im R_(N_E,N_W)| = 324
|Im R_(K,M)|     = 972
```

だった。各 class・各54個の t2 で `k mod 3={0,1,2}`、cardinality 3。$\Theta_2$ rigid class は4窓とも0である。

各窓の全行 digest は

```text
eps=+,eta=+  3416698d03627b45bab04c44337dba483f846920b53e91475068619b3b8ffd23
eps=+,eta=-  d53f1c3ceabf217e6bfd6448f9fdcd386b5c46ab1d7b5af1681a443a0f3d2502
eps=-,eta=+  9865d1bfeedd339f86ee737185e4def2ca8feb9467303e0a760b5ae2c3cea925
eps=-,eta=-  875c73b9308018161f50cd0d4b506c182ed11790775e68feb4d014d279c01df0
```

で、producer/checker が4本とも一致した。

### 1.5 生値、cert、到達段

到達段は `escape28_full_campaign_complete`。停止理由は `H²≠0 下の全消滅`。run ID と時間は

```text
preflight          escape28-preflight-20260813T073511Z        52,462 ms
preflight checker  escape28-preflight-check-20260813T073609Z  51,713 ms
main producer      escape28-mainrun-20260813T073814Z          73,457 ms
main checker       escape28-mainrun-check-20260813T073951Z    72,079 ms
```

である。main checker は **1,099,008行**を照合し、不一致0。これは照合済み（cross-checked）であり、Lean 証明書は作っていないので verified ではない。

再現コマンドは次の4本。

```powershell
python -B search/escape28_mainrun_v1.py --mode preflight --preflight-output search/certs/escape28_preflight_v1r2_20260813.json --checkpoint search/certs/escape28_preflight_v1r2_checkpoint.json --hard-timeout-seconds 600
python -B search/check_escape28_mainrun_v1.py --mode preflight --preflight search/certs/escape28_preflight_v1r2_20260813.json --output search/certs/escape28_preflight_check_v1r2_20260813.json --checkpoint search/certs/escape28_preflight_check_v1r2_checkpoint.json --hard-timeout-seconds 900
python -B search/escape28_mainrun_v1.py --mode measure --preflight-output search/certs/escape28_preflight_v1r2_20260813.json --prereg search/certs/escape28_prereg_v1r2_20260813.json --output search/certs/escape28_mainrun_raw_v1_20260813.json --checkpoint search/certs/escape28_mainrun_v1_checkpoint.json --hard-timeout-seconds 900
python -B search/check_escape28_mainrun_v1.py --mode measure --preflight search/certs/escape28_preflight_v1r2_20260813.json --input search/certs/escape28_mainrun_raw_v1_20260813.json --output search/certs/escape28_mainrun_check_v1_20260813.json --checkpoint search/certs/escape28_mainrun_check_v1_checkpoint.json --hard-timeout-seconds 900
```

全 runner は atomic checkpoint と hard timeout を持つ。

## 2. 終盤勘定の pin

本便は gentle 側測定だけである。B 分岐の反証候補へ昇格させるには、B4 層の **PENT_W-PASS** を先に通し、その後 `FAKE-KILL^{B4}/U-10` を適用する必要がある。この `endgame_scope` は raw cert に保存した。

今回の有限深度データには型語を付していない。`N_E_isolated=UNKNOWN`、`escape28_gap=open` のままであり、C-4′ の isolatedness 前件を越えた解釈もしていない。

## 3. 規律、provenance、hash

### 3.1 規律

- `u`, `c`: 非接触。
- 封印3量、sealed K5: 非接触。
- blind 境界: r1 停止時も outcome 0件。r2 prereg 後にのみ本走。
- NAME-COLLIDE: $W=PB_3/N_W$、$\bar W=B_3/N_W$、$\widetilde E=B_3/N_E$ を分記。純生成元 $X,Y$ と $B_3$ の $\Delta,\delta,\sigma_1,\sigma_2$ を分離した。
- SURJ-LIN: 28次元の可約直和を明示し、2成分の全射条件を積で扱った。
- 障害消滅と生成解存在は別欄・別 digest 入力にした。
- `nonzero_obstruction_rows=[]` を見て指定どおり停止し、次の探索・理論仮定へ進んでいない。
- git commit、push、workflow dispatch は行っていない。着手前からの巨大な dirty worktree には触れていない。

実行後、今回の新規ファイル名を除いた raw grep count は

```text
H^2/H² と「全消滅」の同一行変種        0
ESCAPE-28                               9
F_3^4 / End_W(V) dimension 4 変種       1
```

だった。名称 ESCAPE-28 と一般の End 勘定は既出。本便の増分は、凍結した最小窓で得た **H²非零かつ全1,099,008障害類0** という機械生値であり、説明定理はまだない。

### 3.2 入力 SHA-256

| 入力 | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_133_escape28.txt` | `944088d5e618ba6f5557b7bbfe6d50b32b92b1a3d523310c92a95d3dcc32c021` |
| `docs/notes/entangled972_reading_v1.md` | `2ea6a8a3d7b7f9858cc54ec0026a4939e736d4cc6899efd044bbd2d9c47130f6` |
| `docs/notes/vnbit_compact_route_v3.md` | `ff9febbcb47142cbc1716b326b4ca5684a2a57ca1639a44142d697aefe2e6432` |
| `search/vnbit_compact_mainrun_v3.py` | `4ba20a286e9616c9363a9e8187fb4c35d04e11a6dbc4610c17d3879e5c47eb9a` |
| `search/check_vnbit_compact_mainrun_v3.py` | `52c47c908ddbcb9aa06fba15269e263c4e7d7a574a5047443e300ac40029d33e` |
| `search/certs/vnbit_affine_gate_raw_v1_20260813.json` | `24b78fc1e700223f1be27dabf77e1fed65af6e58c4e28362be7d802f563bb5ee` |
| `certificates/S4.v2.json` | `c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d` |
| `certificates/K3.v1.json` | `d7cd44ea6d71e341e3e1a6164ce03540e92c50d405113ad1d3dc26972b1e8171` |
| `certificates/K9.v1.json` | `ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e` |

### 3.3 成果物 SHA-256 — active r2 / main

| 成果物 | SHA-256 |
|---|---|
| `search/escape28_mainrun_v1.py` | `2acdbdd17c30f28ea3709cf6f44ee47dd81e9868a8ae64b364926f3c4e1ea6b8` |
| `search/check_escape28_mainrun_v1.py` | `aa371e68fd24151f5225eb9ddd4a3a45d7e8172e1a301ae1aa8e2250c8615975` |
| `search/certs/escape28_preflight_v1r2_20260813.json` | `50b614660db17a560d2e4ef8fc954dcf23705765cb2d2721d28fe19d15f4ce45` |
| `search/certs/escape28_preflight_v1r2_checkpoint.json` | `c3dcf0d0c6c489b08d01f3a4961df2d21ff3bf77bc1fe4d9e5f03ac33e057d37` |
| `search/certs/escape28_preflight_check_v1r2_20260813.json` | `a5bec9872e7235f1792e6ed5a9f95f1bb59074c906acd52eb888258b3a6dd0f0` |
| `search/certs/escape28_preflight_check_v1r2_checkpoint.json` | `43537181758e6810e8dd285759f375f713333f754e0b8671f3e3f0e045b155c7` |
| `search/certs/escape28_prereg_v1r2_20260813.json` | `286a1cf2115ad76fa9940105868482ab22ffe19f4c872007dc54d57337fd69f9` |
| `search/certs/escape28_mainrun_raw_v1_20260813.json` | `5f0718e4c6a6227aa75126b7a8059077b682e4273100eee7775621cdaa34eb50` |
| `search/certs/escape28_mainrun_v1_checkpoint.json` | `f2df443f4918965c5832db3d31459711c47312152c77a5ebb95b0ac8b568070a` |
| `search/certs/escape28_mainrun_check_v1_20260813.json` | `dfa755c3f9009b15d285481a7b09069b104578016585637df037e2c310ce6a5d` |
| `search/certs/escape28_mainrun_check_v1_checkpoint.json` | `d713513c53afc0bae7b973f20de23098800fb879f0e6cf236bc1c22c1ed96728` |

### 3.4 r1 の zero-outcome 履歴 SHA-256

| 履歴成果物 | SHA-256 |
|---|---|
| `search/certs/escape28_preflight_v1_20260813.json` | `5eb683035dd70cb5b25e5e5f965d6f0497ffc49636e7e809fefffe9e34807ab6` |
| `search/certs/escape28_preflight_check_v1_20260813.json` | `c2cb325bb28f48d97f5f20341acf45adc1d3f485472e7875f5a1dcf0b40d1527` |
| `search/certs/escape28_preflight_check_v1_checkpoint.json` | `62d188224427dbfa9bdae3e4bf5aae0929f697cd9909f73fdc4e44a6905bc050` |
| `search/certs/escape28_prereg_v1_20260813.json` | `dd246246ddb278b1f7ad54d06bea4fc7361ca1753603b4455c1e99b06499e692` |

git は read-only 運用とした。成果物の凍結は工房側へ委ねる。
