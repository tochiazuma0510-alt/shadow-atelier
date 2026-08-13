# 返書 132 — vN-BIT compact v3 二窓本走

日付: 2026-08-13  
委嘱: `ops/inbox_codex/sol_task_132_mainrun.txt`  
仕様正本: `docs/notes/vnbit_compact_route_v3.md` (`59836eedb8fc315ee3954e5363149a3d2cb8a98b`)  
実行時 HEAD: `4e04f9dd979d3775fc2be66193d8da94d2a1ec16`

## 0. 一行

便 132 の §0–§3 を順に処理した。8 修理候補は NORM-TWIST のちょうど2窓、各 gauge 軌道サイズ4に収縮した。P-vNC3-2 の生値は次のとおり。

```text
epsilon=+ : dim ker(I+theta')=11, |H1|=81
epsilon=- : dim ker(I+theta')=10, |H1|=27
cross-epsilon sum=21
```

SL-RE 後の全射類はそれぞれ80、26。両窓 × 全106類 × 324行、計34,344行を走らせ、全行で障害類は0、生成解は存在した。全類で

```text
|Im R_(N_E,N_W)| = 324
|Im R_(K,M)|     = 972
```

かつ各 t2 で k mod 3 の3値 `{0,1,2}` がすべて実現した。producer と別 heart 基底の checker の不一致は0で、結果は cross-checked（照合済み）。Lean 証明書は作っていないので verified ではない。

`N_E_isolated=UNKNOWN`、`vNB-GAP-1=open` のままであり、有限深度からの型解釈は行っていない。

## 1. 委嘱

### 1.1 C-2′ — NORM-TWIST の二窓

便131の辞書順候補をそのまま採らず、まず τ′ の source-block 符号を `(+,+,+)` に gauge 正規化した。残る固定 block の1ビットを、配列 index 2（3番目の 7×7 block）の実行列と SHA-256 で固定した。

| 窓 | θ′ source-block 符号 | τ′ 符号 | 固定 block B | `B_matrix_sha256` |
|---|---|---|---|---|
| ε=+ | `(-,-,+)` | `(+,+,+)` | +R_S | `fa7796d0afd372982ef29294483f2e1f47b06b54f795ccf2f90dee71cf2cca8f` |
| ε=- | `(+,+,-)` | `(+,+,+)` | -R_S | `ec5586d4dee204d5a9ed7db38d92c0c3d0cbbad7f27f525729b4ea2c296b6a16` |

64組の monomial scalar を悉皆した生値は次のとおり。

| 項目 | 生値 |
|---|---:|
| pure-anchor 解 | 8 |
| End_W(V)× の位数 | 8 |
| 全 gauge stabilizer の位数 | 2 |
| 実効 gauge 群の位数 | 4 |
| 軌道数 | 2 |
| 軌道サイズ | `4,4` |

両窓で pure anchor

```text
((tau')^(-1) theta')^2       = rho(X)
((theta')^(-1) (tau')^2)^2  = rho(Y)
```

が成り立ち、差分 rank はともに0。純部分と外側標識を混同しないよう、cert では ρ(X), ρ(Y) と θ′, τ′ を別行列として保持した。

また θ′²=I、τ′³=I で、全 cocycle 代表について U²=S³=1。従って中心 c=Delta² は標識付き全射の kernel に入る。

無料検査の生値は

```text
rho(X) block signs = (-,+,-)   (+ は1個)
rho(Y) block signs = (+,-,-)   (+ は1個、rho(X) の巡回シフト)
```

である。

C-9 は、P=PSL(2,8) の9点 augmentation heart V7 について次を得た。

```text
P order                                      504
nonzero cyclic submodule dimensions          {7: 2186}
dim_F3 End_P(V7)                              1
V7 absolutely irreducible over F3             true
```

producer の基底と `e_i-e_0 (1<=i<=7)` を使う checker の別基底で同じ数値を再計算した。

### 1.2 P-vNC3-2 の生値

| 窓 | dim ker(I+θ′) | dim ker(I+τ′+τ′²) | dim Z¹(C2*C3,V) | dim B¹ | dim H¹ | \|H¹\| |
|---|---:|---:|---:|---:|---:|---:|
| ε=+ | **11** | 14 | 25 | 21 | 4 | **81** |
| ε=- | **10** | 14 | 24 | 21 | 3 | **27** |

従って強い入口値は `(11,81)`、`(10,27)`、和21。P-vNC3-3 の14も両窓で同じだった。

### 1.3 SL-RE — 両窓の SURJ-LIN

手固定の relator list は用いず、P の504頂点 Cayley graph の正向き X,Y 辺を全て走査した。

| 機械量 | 両窓の生値 |
|---|---:|
| 頂点 | 504 |
| 正向き辺 | 1008 |
| collision 辺 | 505 |
| V=V7^3 上の relation rank | 18 |
| dim Z¹(P,V) | 24 |
| dim B¹(P,V) | 21 |
| dim H¹(P,V) | 3 |
| 外側 `theta',tau'` 不変部分の次元 | 0 |
| \|H¹(bar W,V)\| | 1 |

producer 基底の relation RREF digest は `7c780d3a08b0683fe4d1cb741e57fab90ff54b771c3174813e0e8f67e2a2b2b7`。別基底 checker は relation space を Cayley graph から再生成し、数値欄の不一致0を得た。

SURJ-LIN により inflation 部分は零類だけなので、Γ=C2*C3 の class 0 を除く全類が全射類となる。

| 窓 | \|H¹(Γ,V)\| | \|H¹(bar W,V)\| | 全射類数 |
|---|---:|---:|---:|
| ε=+ | 81 | 1 | **80** |
| ε=- | 27 | 1 | **26** |

checker は供給された全81/27代表が cocycle 条件を満たすこと、商座標が全て異なること、零類が各1個であることも別基底で照合した。

### 1.4 事前登録と34,344行の本走

#### 事前登録境界

`search/certs/vnbit_compact_v3_prereg_20260813.json` に、outcome を開く前に次を凍結した。

```text
windows                         2 (+,-)
surjective classes              80 + 26
roof rows per class             324
total lift rows                 34,344
A shape                         42 x 21
rank(A1)=rank(A2)               mandatory gate
P-vNC3-1 ... P-vNC3-5           v3 values/weak label preserved
inherited image-size set        {324,972}
blind_before_measurement        true
```

最初の本走試行は、outcome を1件も開く前の coefficient-template gate で停止した。原因は、producer が A1,A2 に簡約 F2 式 `f theta(f)` と tau-norm を入れていたことだった。この二式の rank は `10/7`、`11/7` となり、仕様 A-42 の意味とは異なる。正本 (3.3),(3.4) の full B3/N hexagon に直すと全324行で `17=17`、`18=18` となった。lift outcome は0件のまま producer/preflight hash を更新し、prereg を revision 2 として再凍結した。この履歴と `lift_outcomes_opened: 0` は prereg 内に保存している。

#### 障害と生成の独立欄

最終本走の全体分布は次のとおり。

| 窓 | 全射類 | 行数 | rank(A1),rank(A2) | rank(A) | dim ker A | 障害0 | affine 解数 | 生成解数 |
|---|---:|---:|---|---:|---:|---:|---:|---|
| ε=+ | 80 | 25,920 | `(17,17)`（各類で同じ324行） | 17 | 4 | 25,920 | 81/行 | **80/行** |
| ε=- | 26 | 8,424 | `(18,18)`（各類で同じ324行） | 18 | 3 | 8,424 | 27/行 | **27/行: 5,832行、24/行: 2,592行** |

障害類消滅と生成解存在は別欄で計算した。GEN-AFF の block-complement 系を3 simple block ごとに立て、7個の非空 block subset の交叉数を包含排除した。さらに checker は各 affine kernel を実際に全列挙（ε=+ は81元、ε=- は27元）し、各解の3 block complement 条件を直接評価した。

- ε=+: 全80類・全324行で、7個の非空 subset の交叉数は全て1。非生成解が1個、生成解が80個。
- ε=-: 18類では非生成解0、生成解27個。次の8類では7個の非空 subset の交叉数が全て3で、非生成解3個、生成解24個。

```text
class_index / quotient_coordinates
 5  (1,2,0)     7  (2,1,0)     9  (0,0,2)    14  (1,2,2)
16  (2,1,2)    18  (0,0,1)    23  (1,2,1)    25  (2,1,1)
```

いずれも生成解数は正なので、全34,344行の `lifts` は `true` となった。

#### 窓・類・t2 分布

| 窓 | class ごとの \|Im R_(N_E,N_W)\| 分布 | class ごとの \|Im R_(K,M)\| 分布 |
|---|---|---|
| ε=+ | `{324: 80}` | `{972: 80}` |
| ε=- | `{324: 26}` | `{972: 26}` |

各 class、各 t2 in GT(N_S4)（54個）について同じ生値だった。

```text
lifted N_W rows over each t2     6
k mod 3 values realized          [0,1,2]
cardinality                      3
```

従って Θ2 の cardinality distribution は

```text
epsilon=+ : {3: 4320} = 80 classes x 54 t2
epsilon=- : {3: 1404} = 26 classes x 54 t2
```

で、rigid class 数は両窓とも0。二窓の像サイズは同じであり、弱い P-vNC3-5 の見立てと同じ生値になった。凍結済みの `|GT(N_W)|=324`、K9 の各対応行の preimage 数3、組立 `|GT(M)|=972` も保持された。

C-4′ の scope は変えていない。中間像の生値324を isolated な窓の型情報へ読み替えておらず、`N_E_isolated=UNKNOWN` のままである。最終の K→M 像サイズは972だが、これについても本便では型認定を行わない。

### 1.5 生値、cert、到達段

到達段は `two_window_measurement_complete`。producer run ID は `vnbit-compact-mainrun-20260813T062104Z`（checkpoint elapsed 340,205 ms）、main checker run ID は `vnbit-compact-mainrun-check-20260813T063523Z`（335,419 ms）、preflight checker run ID は `vnbit-compact-preflight-check-20260813T064213Z`（7,616 ms）。

再現コマンドは次の4本。

```powershell
python -B search/vnbit_compact_mainrun_v3.py --mode preflight
python -B search/vnbit_compact_mainrun_v3.py --mode measure --hard-timeout-seconds 900
python -B search/check_vnbit_compact_mainrun_v3.py --hard-timeout-seconds 900
python -B search/check_vnbit_compact_preflight_v3.py --hard-timeout-seconds 180
```

全 runner は atomic checkpoint と hard timeout を持つ。main checker は producer を import せず、別 heart 基底、独立 roof 再構成、full (3.3)/(3.4) 展開、affine kernel 全列挙を用いた。preflight checker は同じ別基底 primitive を明示依存として使うが producer は import せず、C-9、gauge、Cayley relation、両 cocycle 商を再構成した。main 34,344行と preflight 数値欄はいずれも不一致0。

## 2. 終盤勘定の scope pin

本便は gentle GT-hat-gen 側の測定だけを扱う。B 分岐の反証候補へ昇格させるには、B4 層の **PENT_W-PASS** を先に通し、その後 `FAKE-KILL^{B4}/U-10` を適用する必要がある。この pin は raw cert の `endgame_scope` に保存した。有限深度の本データから B 型を認定していない。

## 3. 規律、novelty、provenance

### 3.1 規律

- u,c: 非接触。
- 封印3量、sealed K5: 非接触。
- isolated 性: `UNKNOWN`、`vNB-GAP-1=open`。
- NAME-COLLIDE: W=PB3/N_W、bar W=B3/N_W、tilde E=B3/N_E を分記した。
- PB3 の X,Y と B3 の Delta,delta,sigma1,sigma2 を別名で保持した。
- SL-RE の relation は手固定せず、Cayley graph の全 collision から生成した。
- 障害消滅と生成解存在を別欄にした。
- 有限深度からの B 型認定、git commit、push、workflow dispatch は行っていない。
- 着手前から存在した dirty worktree の他便変更には触れていない。本便で追加したのは下記の task-specific scripts/certs と本返書だけである。

### 3.2 novelty grep（実行後・`vnbit_compact` を含む行を除外）

`docs/` と `sol/` に対する現在の raw line count は次のとおり。

```text
monomial                                      120
gauge class/orbit variants                      1
Clifford / Schur-End_W variants                19
H1(S3) / Shapiro variants                      18
twist class variants                            0
pure anchor variants                            1
```

一般の monomial/Clifford/Schur/Shapiro は既出。個別の TWIST-2、SWAP-7、NORM-TWIST と本二窓への適用が v3 の増分、pure-anchor の既出1行は便131である。

### 3.3 SHA-256

入力:

| 入力 | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_132_mainrun.txt` | `e4bc70fff7103af2b829a55144db37fafa25d2d2f8f6d7eeaecee72af003bd1e` |
| `docs/notes/vnbit_compact_route_v3.md` | `ff9febbcb47142cbc1716b326b4ca5684a2a57ca1639a44142d697aefe2e6432` |
| `docs/notes/bu_s35_embedding_v1.md` | `dfdb7557972208d4f16907017e9c5c52195859acb9d1eb11013922e83ba87e86` |
| `docs/week1-定義ノート.md` | `24db1372fd191659f1f0149cb669870dff470db1f779d3e5f83dba4171501c6c` |
| `search/certs/vnbit_affine_gate_raw_v1_20260813.json` | `24b78fc1e700223f1be27dabf77e1fed65af6e58c4e28362be7d802f563bb5ee` |
| `certificates/S4.v2.json` | `c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d` |
| `certificates/K3.v1.json` | `d7cd44ea6d71e341e3e1a6164ce03540e92c50d405113ad1d3dc26972b1e8171` |
| `certificates/K9.v1.json` | `ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e` |

成果物:

| 成果物 | SHA-256 |
|---|---|
| `search/vnbit_compact_mainrun_v3.py` | `4ba20a286e9616c9363a9e8187fb4c35d04e11a6dbc4610c17d3879e5c47eb9a` |
| `search/certs/vnbit_compact_preflight_v3_20260813.json` | `f6eb203473632b242f9ca6de32319e5ef906ca733198aaec9bffa08480762ead` |
| `search/certs/vnbit_compact_v3_prereg_20260813.json` | `a6e357656b719830f2ee1055cdb339c75b256fe936c36e047e72f7ab599cf046` |
| `search/certs/vnbit_compact_mainrun_raw_v3_20260813.json` | `0f4ee4dd905e3e66bb3367c7a77ce935157deb7cc63dfef540b7503142d6728b` |
| `search/certs/vnbit_compact_mainrun_v3_checkpoint.json` | `78e666e2496e35732d3061ab2a43ccd3bbc5261c785b77aeac9dd9bc6da782fb` |
| `search/check_vnbit_compact_mainrun_v3.py` | `52c47c908ddbcb9aa06fba15269e263c4e7d7a574a5047443e300ac40029d33e` |
| `search/certs/vnbit_compact_mainrun_check_v3_20260813.json` | `18a61e2159d2478f917b8851d155e7cd3a9f6b85f68ee05b8d00fc2ae13fbb6c` |
| `search/certs/vnbit_compact_mainrun_check_v3_checkpoint.json` | `62cc4ef9cb8ab5c8e7ea7e64fae59d5b6370a216f197fbd22ad85999ec38e8ef` |
| `search/check_vnbit_compact_preflight_v3.py` | `330891bba957d7686b8b0a857f6d5cf8e9ddbb57a0aa664b2ea9bf6744e5d1ab` |
| `search/certs/vnbit_compact_preflight_check_v3_20260813.json` | `bd250f65fb2919f08ef5a55e79f49104708ea4879bb8d1b04585227898d5e2fb` |
| `search/certs/vnbit_compact_preflight_check_v3_checkpoint.json` | `92eb5e188b395d20935fb72db2df6a92ea68e2322be989b15caea985e2ac9df6` |

git は read-only 運用とし、run ID / commit SHA を伴う外部操作は無い。成果物の凍結は工房側へ委ねる。
