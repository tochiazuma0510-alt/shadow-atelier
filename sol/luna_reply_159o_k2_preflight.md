# Luna 便 159o — K2 joint-rung read-only preflight

```text
STATUS = PREFLIGHT_COMPLETE
K2_NAME = NOT_FROZEN
K2_EXECUTION = NOT_RUN
CORRECTED_159N_CANARIES = NOT_RUN / PREDECESSOR_OPEN
RUNG_LADDER = PROVISIONAL_UNFROZEN
VERIFIED = false
```

本便は裁定 1650/1651 の順序を fail-close で適用した read-only 監査である。修正版
pent canary の receipt/verdict は現作業木に存在しないため、K2 を命名・凍結・実行していない。
search/crosscheck code、`sol/sol_reply_159_iv.md`、git、workflow、GHA、es7ops は変更・実行していない。
追加 preregistration file も作っていない。

## 1. 読み込んだ正本と immutable pin

| path | bytes | SHA-256 |
|---|---:|---|
| `AGENTS.md` | 5,418 | `647bed4a9b396521dc427f15246419eaeb69554baeadfdda6950983c33ca6ecf` |
| `ops/inbox_codex/sol_task_159o_ladder_launch.txt` | 2,829 | `aa234d0a4ce138aa3e8c8de24c37a601cc8169a9f75d7d04cfc7f0b6d4e16b84` |
| `ops/express/20260823_fable_sol159n_canary_exec_auth.md` | 1,035 | `2ec0f95f142bc6f2ca98ab76950dc5b93ae6d5507f69d0c623983bcbc5c46b33` |
| `ops/inbox_codex/sol_task_159n_pent_interleave.txt` | 3,359 | `6e15058868b79ff38709d39adb2937fe4518917dff386953aa845f8e0b50c620` |
| `sol/luna_task_159n_pent_canaries.md` | 9,602 | `210f2d2de0001d09fffbdd85e6473c2c4627927b0c17e1211ca2580f5b0ebff5` |
| `sol/sol_reply_159_iv.md` (§§21–22 を含む監査時 snapshot) | 202,810 | `f87d32718026f4a286f15cfb37bb9307a0f297c5191cad8ff532fd80b4fbcd96` |
| `docs/week1-定義ノート.md` | 26,498 | `24db1372fd191659f1f0149cb669870dff470db1f779d3e5f83dba4171501c6c` |

裁定 1651 の優先順は逐語的に

```text
corrected p=2/p=3 Zassenhaus canaries
  -> §22.5 の freeze 4 gates
  -> 159o K2 joint preflight/launch
```

である。したがって本便で閉じられるのは stock と joint の静的 preflight までであり、launch
authority ではない。

## 2. 結論を先に固定する

1. **普通の公平梯子**では、index-2 shell は no-op、index-3 shell の cyclic quotient node
   `16437e...bc37` が最初の strict joint-source candidate である。index 48/162/9072 の named
   stock を先に選ぶことは §21.5 の shell 公平性に反する。
2. `K_Q` と LINS `K_L48A` は exact duplicate である。さらに read-only marked reconstruction
   では `K_1=K^(36) cap N_S4 <= K_Q`、したがって `K_1 cap K_Q=K_1` である。ただし
   rung は source `H` でなく `H^diamond` なので、専用 diamond equality receipt が無い限り
   **candidate 自体を公平列から消してよいとはまだ言わない**。
3. `K_L48B` は `K_Q` の duplicate ではない。F2 kernel は同じだが `c` の像がそれぞれ
   `1` と `-1` で、`c in K_1` かつ `c notin K_L48B`。従って K1 との full PB3 join は中心方向に
   index 2 だけ strict になり得る一方、F2 quotient と row-36 raw-fibre cardinality は増えない。
4. Heisenberg と PGL は plain K1 join では strict であるが、いずれも index-3 shell より後である。
   Heisenberg の `N_0` isolated は別紙の paper-proof があるが、§21.5 が要求する
   `(M cap N_0)^diamond` equality receipt は無い。PGL は B3-stability/core equality までで isolation は
   UNKNOWN。
5. **pent refinement を有限 prefix として挿入しても、以後 ordinary shell 列挙を公平に続ければ
   数学的 cofinality は壊れない。** しかしこれは §21.5 の ordinary ordering からは選ばれない
   **special finite-prefix K2** であり、corrected canary 後の明示的な contract 改訂・再凍結が必要である。
6. `K^(27) cap N_S4` の n=1 結果は別の non-cofinal sniper calibration だけであり、本 stock、K1、
   K2、shell cursor のいずれにも数えない。

従って現時点の正しい終端は

```text
ORDINARY_FAIR_FIRST_STRICT_SOURCE = LINS node 16437e...bc37 (index 3)
SPECIAL_PENT_PREFIX_K2 = CONDITIONAL_DESIGN_ONLY
K2 = UNNAMED / UNFROZEN / NOT_RUN
```

である。

## 3. LINS source の exact pin と公平性監査

### 3.1 LINS provenance

| role | path | bytes | SHA-256 |
|---|---|---:|---|
| exact recovered export | `ci/lins_marked_artifacts_32626064970/lins_marked_export/lins_marked_strictness_export_v1_20260823.json` | 51,546,606 | `9fa4fff101d641688b858550e77e3543d7461bc00d149470b81dfdce91fa8324` |
| producer source | `search/lins_marked_strictness_export_v1.g` | 14,064 | `74924dd639470a48d94770578c9ae9b5e22657483461f2063632150948979ec1` |
| execution manifest | `search/certs/lins_marked_strictness_export_manifest_v1_20260823.json` | 5,075 | `c15d7dc422b9b1e3aa5caad7a825210ee31d2e1fc51071de6c936053a0cc3272` |
| earlier census anchor | `search/certs/lins_census_2000_v1_20260811.json` | 3,395,546 | `d0832df8a4e61adff45c5c24c8eba32f5d388f55412907ed5ffdf714b2b4b958` |

Recovered run id は path に固定された `32626064970`。宇宙は一回の
`LowIndexNormalSubgroupsSearch(B3,2000)` が返した identity 以外の 4,265 normal nodes である。
これは全有限指数 subgroup の cofinal 列そのものではなく、§21.5 が明記する「最初の有限 inventory」に
すぎない。また 4,265 maps 全体には producer と helper 非共有の全行 checker は無く、以下の row data は
GAP producer artifact/candidate 層で読む。index-48 選択行だけは後続 checker が独立再生している。

read-only 集計では index `<=48` に 69 normal rows があり、M-join class は

```text
NO_REFINEMENT = 3
PB3_CENTER_ONLY = 3
STRICT_F2 = 63
```

であった。監査用 compact serialization
`index|node_id|F2_ratio|PB3_ratio|source_digest` を index 数値順、次に node-id 順、LF 区切り、末尾 LF
なしで束ねた 9,526 bytes の session-local digest は
`0d6448debb6871c6cde35947ac5f6a6d0ebb61b3b86228e0eeed663aa8ae94ea`。
これは versioned artifact ではなく、claim promotion には使わない。

### 3.2 index-2 shell

export の行は次である。

```text
node_id = 170102fd74f753009cc5bbd7494d27141048a77b553ba42b1af98f398eb8c662
b3_index = 2
canonical_id_words = ["a^-2", "b*a^-1"]
quotient_order / permutation_degree = 2 / 2
sigma1 = sigma2 = (1,2)
x = y = c = 1
F2_image_order / PB3_image_order = 1 / 1
Core_B3(L) = L, core index = 2
M-joint F2_order / PB3_order = 1,469,664 / 1,469,664
M-join ratios = 1 / 1 (NO_REFINEMENT)
source_digest = 7402e6b2fa2d9bb5f4bd344731b5a9bb5fe5996707e48dedfa643e1e4ddec981
```

これは `B3^ab = Z` からも shell 全体を閉じる。index 2 の transitive quotient は C2 のみで、
`sigma1=sigma2=t`、従って `x=y=t^2=1`、`c=t^6=1`。よって `H=M` で K1 join は no-op。
ただし §21.5 の形式上の shell closure には、既受理の M isolation を専用 rung receipt に束縛した
`M^diamond=M` equality/duplicate token がまだ要る。

### 3.3 index-3 shell と最初の strict source

full selected row は次である。

```text
node_id = 16437e56512d99ab2c7ca8328293863fe6b7792504ebd592fa21da9d7952bc37
b3_index = 3
canonical_id_words = ["a^3", "b*a^-1", "b^-1*a"]
quotient_order / permutation_degree = 3 / 3
sigma1 = sigma2 = (1,2,3)
x = y = (1,3,2)
c = 1
F2_image_order / PB3_image_order = 3 / 3
Core_B3(L) = L, core index = 3
M-joint F2_order / PB3_order = 4,408,992 / 4,408,992
M-join ratios = 3 / 3 (STRICT_F2)
source_digest = c6f20bd5c6edc071c48a6ecd10f09e0dcfd0ef232bfa0ee7d3bf4aba45a60158
```

全 index-3 subgroup を normal LINS rows だけで尽くしたとは読んでいない。その代わり transitive
degree-3 image を紙で分類すると C3 または S3 である。C3 branch は上の一意な abelian map。
S3 branch は standard braid-to-S3 map で core は PB3、かつ `M <= PB3` なので `H=M` の no-op。
従って full shell でも strict core-source は上の C3 node が最初である。

K1 側 `G36` は order 23,328、abelianization order 16 なので C3 quotient を持たない。従って
plain marked F2 join は Goursat により

```text
G36 x C3, order 69,984;
with PSL(2,8): F2 quotient order 35,271,936.
```

となる。これは diamond 前の構造値であり、専用 K1-joint receipt/checker は未作成である。

### 3.4 shell 内 ranking の残件

§21.5 の第一 sorting key は raw fibre size ではなく
`exact one-seed candidate count after joining current rung` である。本便で閉じた 48 は raw reduction fibre
の cardinality であり、二 hexagon/charming/onto 後の candidate count ではない。よって source が最初と
分かっても、次の三点なしに `K2` は命名しない。

```text
Core/duplicate coverage for every index-2 and index-3 subgroup class
H^diamond finite-set/equality receipt for node 16437e...bc37
exact row-36 one-seed candidate count + marked quotient order + source digest ordering receipt
```

## 4. bootstrap K1 と row-36 raw fibre

`M=K^(9) cap N_S4` と bootstrap `K1=K^(36) cap N_S4` の exact baseline は次である。

| datum | M | K1 |
|---|---:|---:|
| F2 quotient order | 1,469,664 | 11,757,312 |
| component form | `G9 x PSL(2,8)` | `G36 x PSL(2,8)` |
| `N_ord` | 18 | 36 |
| raw universe `N_ord * |F2 quotient|` | 26,453,952 | 423,263,232 |
| uniform raw fibre over one M target | 1 | 16 |
| GT rows / fibre histogram | 972 / `{1:972}` | 1,944 / `{2:972}` |

証拠は以下である。

| role | path | bytes | SHA-256 |
|---|---|---:|---|
| K36 component cert | `certificates/K36.v1.json` | 727,834 | `feac2a0202e5b78a017272a972e105ac7daf7eb5ca0b4de102b6664b098d8719` |
| K36 independent verdict | `crosscheck/verdicts/K36.v1.verdict.json` | 71,093 | `4436da2643a0577b06761cd310f0032d98fefe67bab10c16f74c534aabb1a92b` |
| K1 producer receipt | `search/certs/b3_gentle_source_census_preflight_v1_20260823.json` | 887,124 | `c30077133305c07ca0e58c9eaa700d42a512a6bbbce96c9c27d161e921e1aaf2` |
| K1 checker verdict | `crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json` | 4,931 | `e308a71323dc429d771d7fb86f507b3c17936716505dd6ca3ee3fbfdeecf7f4e` |

fixed seed は zero-based row 36 のまま変更しない。

```text
key = [0,[[4,0],[5,0],[0,0]],[1,2,3,4,5,6,7,8,9]]
full-row compact digest (99 bytes) = 31d19295b8b5c2f5e36387f6bb63cec508a7b8770e30bfa6d02909b1f16f4cd8
target-key compact digest (43 bytes) = 3940557ee6c0118f2563ff7d19a41059d0fcdd5c7c876bc56c84b4fa9ae242ac
word compact digest (51 bytes) = b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d
```

source artifact は `search/certs/d972_b4_word_key_artifact_v1_20260816.json`、176,474 bytes、
SHA-256 `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9`。

## 5. approved named stock と K1 joint inventory

次表の「individual over M」は既存 crosschecked window、「K1 plain join」は本 preflight の diamond 前の
構造値である。raw fibre は

```text
N_ord(source) * |F2/source_F2| / (18 * 1,469,664)
```

で得た row-36 raw reduction fibre の cardinality。GT survivor 数ではない。

| stock | defining B3 source index | individual over M | K1 plain marked joint | row-36 raw fibre before diamond | isolation/diamond |
|---|---:|---|---|---:|---|
| `K_Q=M cap N_Q` | 48 | component 5,832; full F2 2,939,328; `N_ord=36`; raw 105,815,808; GT fibre 2 | F2/PB3 quotient remains 11,757,312; `K1<=K_Q`, hence source join duplicate | 16 | N_Q normal; isolation and `H^diamond=H` UNKNOWN |
| `K_L48A` | 48 | exact `K_Q` alias | same duplicate | 16 | same unresolved diamond |
| `K_L48B` | 48 | same F2/Q8 data and GT fibre 2; distinct `c=-1` twist | F2 11,757,312; PB3 marked quotient doubles to 23,514,624; strict central index 2 | 16 | `Core_B3(L)=L`; isolation/diamond UNKNOWN |
| `K_H=M cap N_0` | 162 | component 78,732; full F2 39,680,928; `N_ord=18`; raw 714,256,704; GT fibre 3 | `G36 x H3 x PSL`, F2/PB3 317,447,424; `N_ord=36`; raw 11,428,107,264 | 432 | N0 isolated by accepted VERBAL-ISO paper proof; `(M cap N0)^diamond` equality receipt UNKNOWN |
| `K_E=M cap N_E` (PGL) | 9,072 (from `6*1512`) | full F2 2,222,131,968; `N_ord=18`; raw 39,998,375,424; GT fibre 9 | `G36 x PSL x PGammaL(2,8)`, F2 17,777,055,744; `N_ord=36`; raw 639,974,006,784 | 24,192 | B3-stable and `Core_B3(N_E)=N_E`; isolation/diamond UNKNOWN |
| ordinary index-3 C3 row | 3 | M-joint 4,408,992, ratios 3/3; no GT census | `G36 x C3 x PSL`, F2/PB3 35,271,936; `N_ord=36`; raw 1,269,789,696 | 48 | core equality yes; isolation/diamond UNKNOWN |

PGL の B3 index 9,072 は receipt の `N_E <= PB3`、`|PB3/N_E|=1512` と
`[B3:PB3]=6` からの exact inference であり、LINS bound 2,000 外である。

### 5.1 Q8 duplicate の direct marked check

K36 の marked generators と Q8 の `x=i,y=j` を helper 非共有の read-only in-memory BFS で組にして
再構成した値は次である。

```text
<(x_G36,i),(y_G36,j)> order = 23,328
projection to G36: order 23,328, kernel 1
projection to Q8: order 8, kernel 2,916
derived order = 1,458
abelianization order = 16
(1,-1) is absent from the F2 graph
```

よって Q8 marking は G36 marking を通じて factor し、両方 `c=1` なので `K1<=K_Q`。
L48B は同じ F2 graph に `(1,-1)` を central generator として加えるため PB3 image だけが 2 倍になる。
この direct check 自体は versioned receipt/checker を持たない一実装の audit なので、台帳昇格には専用 joint
producer/checker が要る。

### 5.2 named-stock evidence pins

| stock | producer/freeze receipt (bytes; SHA-256) | independent verdict (bytes; SHA-256) |
|---|---|---|
| Q8 | `search/certs/b3_gentle_q8_joint_preflight_v1_20260823.json` (1,146,639; `f138aba3e768e314f5f347df7fea9e0980d37878528228848d86b93f7efe0f02`) | `crosscheck/verdicts/b3_q8_source_census_v1_20260823.json` (12,535; `724863b78a0a21554ff74a5ff85e404ddfa2b2752ab55f109d3df67ec1615914`) |
| L48 named rows | `search/certs/lins_index48_two_named_sources_v1_20260823.json` (6,723; `2cb37a75f425850002a0b62a3920dd63681258df26aa90eb786ba442e67a8940`) | row-freeze data is replayed in the next verdict |
| L48 full receipt | `search/certs/lins_index48_two_gate3g_receipt_v1_20260823.json` (11,839,025; `80b9c5fc9cb78ddb0eb1db6dc64e4f9a9d82bf5ceeaead3d89638640b88946b0`) | `crosscheck/verdicts/b3_lins_index48_sources_crosscheck_v1_20260823.json` (47,975; `28da1d0a3bec407c328dcd3bc9714d95e5385943fce31fe08b641cd570cf1f03`) |
| Heisenberg | `search/certs/b3_gentle_heisenberg_joint_preflight_v1_20260823.json` (1,441,029; `c2d013667fab008520c6224dc21bf37c9a2b36afbffa651264b984d219a391fa`) | `crosscheck/verdicts/b3_heisenberg_source_census_v1_20260823.json` (11,496; `0ddbfe3013cf2c1e11d305986651102913fd169fb828be5d31bd56e91f75550e`) |
| PGL | `search/certs/pgl28_independent_window_receipt_v1_20260823.json` (64,765; `04c1232ebc89bb027fa72c0bc1db036e6c13dfbd6712fa761c9520a7849ccdb4`) | `crosscheck/verdicts/pgl28_independent_window_v1_20260823.json` (4,822; `401bdbc7a7b34c49e7217e997e72af4ec7dd6db3eccb09bd1ad8f265bc61e91a`) |

Heisenberg isolation の紙証拠は `docs/notes/auto_settled_check_v1.md`、33,883 bytes、SHA-256
`283145a169d01ed137d0daf1998027aa985e3b80f4f0489f4063b6339bac061e` の §3.4–3.5
(`VERBAL-ISO`)。これは専用 rung diamond receipt の代用ではない。

## 6. 何が今閉じ、何が canary/diamond に依存するか

### 6.1 今閉じられるもの

- exact input/version pins と corrected-canary predecessor が未実行であること。
- K1 baseline quotient/raw cardinality と fixed row-36 digest 束。
- named windows **個別**の M 上の survival/fibre histogram。累積 K1 join へは転用しない。
- Q8/L48A の exact alias、K1 に対する Q8 F2/PB3 duplicate 構造。
- L48B が duplicate ではなく central twist であること。
- index-2 source/core no-refinement と、index-3 shell の earliest strict **source** が full id
  `16437e...bc37` であること。
- diamond 前の plain joint orders と row-36 raw-fibre feasibility table。

### 6.2 corrected p=2/p=3 canary に依存するもの

- `D4_2`, 必要なら `D4_3` の exact PB4/PB3/F2 quotient と Brunnian sensitivity。
- `Ksharp_p=K1 cap D4_p(PB3)` の exact joint quotient/index。
- `(Ksharp_p)^diamond` の isolation/equality/index。characteristic/B3-normal だけでは isolation は出ない。
- instrument full universe と row-36 full raw fibre の producer/checker agreement。
- special pent prefix を採るか、ordinary shell を先にするかという ladder contract の再凍結。

### 6.3 canary と独立に残る ordinary-rung datum

- index-2/3 subgroup/core coverage receipt。
- node `16437e...bc37` の `H^diamond` finite component list/equality。
- K1 と当該 J の exact marked quotient receipt/checker。
- row-36 raw fibre 48 件の deterministic materialization、full gentle predicate、one-seed candidate count、
  coverage digest、mandatory mutants、independent checker。

したがって最初の missing datum は二層に分けて記帳する。

```text
GLOBAL PREDECESSOR:
PENT-INTERLEAVE-CORRECTED-ZASSENHAUS-QUOTIENT-ISOLATION-AND-FULL-ROW36-FIBRE

ORDINARY K2 AFTER PREDECESSOR/MODE FREEZE:
INDEX-SHELL-2-3-CORE-DIAMOND-COVERAGE-AND-K1-JOINT-ROW36-ONE-SEED-COUNT
```

後者は §21.5 の generic token
`RUNG-LADDER-ISOLATED-JOIN-QUOTIENT-AND-ONE-SEED-FIBRE-UNIVERSE` の最初の shell への具体化である。

## 7. special pent finite-prefix K2 と ordinary fair K2 を混ぜない

### 7.1 ordinary fair K2

§21.5 を変更しない場合、処理順は

```text
bootstrap K1
-> index-2 shell no-op/diamond receipt
-> index-3 S3-core no-op receipts
-> index-3 cyclic C3 source 16437e...bc37
-> its diamond/joint/row36 contract closes
-> only then ordinary K2 is named
```

である。Q8/L48B/Heisenberg/PGL はこの K2 より先には来ない。

### 7.2 special pent finite-prefix K2

corrected canary が有効な `p` と isolated

```text
Jpent = (K1 cap D4_p(PB3))^diamond
```

を crosschecked で供給した場合、司令塔/Sol が §21.5 を明示的に改訂し、これを公平列挙の前へ有限個だけ
挿入できる。その後に index shell 2,3,... を一つも飛ばさず再開すれば、任意の有限指数対象 N に対して
元の公平鎖が eventually `<=N` となる性質を追加交叉が保存するので cofinality は壊れない。

ただしこれは

```text
SPECIAL_PENT_FINITE_PREFIX_RUNG (conditional)
```

であって ordinary fairness が選んだ rung ではない。裁定が明示的に「これを K2 と呼ぶ」と再凍結しない限り、
ordinary K2 と同名にしない。p=2/p=3 の一方または両方を挿す順序も canary 観測前には固定しない。

## 8. phased launch contract

### Phase 0 — predecessor gate (現在ここで STOP)

`sol/luna_task_159n_pent_canaries.md` の producer/checker firewall を守り、corrected canary receipt、manifest、
checker verdict を得る。suggested paths は task §0 にあるが、監査時点では該当 producer/receipt/verdict は
**NOT_PRESENT**、従って command は **NOT_RUN**。旧 W2、single representative、raw Lie kernel だけの結果は
gate を閉じない。

### Phase 1 — mode refreeze

canary verdict を受けて、次の一方を immutable token で選ぶ。

```text
MODE=ORDINARY_FAIR_SHELL_FIRST
MODE=SPECIAL_PENT_FINITE_PREFIX_THEN_FAIR_SHELLS
```

mode 未選択のまま K2 を命名しない。pent mode は selected p、exact Jpent digest、diamond receipt、
fair-shell resume cursor=`index 2` を必須 field とする。

### Phase 2 — selected source の joint/diamond preflight

ordinary mode なら node `16437e...bc37`、special mode なら frozen Jpent について、producer は
parent/source/core/diamond/marked quotient、K1 inclusion、N_ord、row-36 raw cardinalityと順序を pin する。
checker は producer source/helper を読まず receipt/manifest だけから再構成する。既存 named-window scripts は
M-relative の別 predicate/universe なので、そのまま K1-rung checker として再利用しない。

### Phase 3 — venue gate と freeze

固定 prefix benchmark と exact raw count を先に測る。ordinary C3 の pre-diamond raw fibre 48 は local exact
enumeration が十分小さい見込みだが、§21.6 の default は GHA なので、環境測定後に venue receipt で裁定する。
SAT は新 encoder、非共有 semantic checker、controls、DRAT->LRAT replay が揃うまで不採用。
ここまで producer/checker が一致して初めて K2 name、rung digest、fresh v8 lineage を freeze できる。

### Phase 4 — one-seed execution

- positive は一 witness を checker が word-level hexagons/charming/onto/exact reduction まで再生して停止可。
- negative は全 raw fibre、全 reject reason、no omission/duplicate、`CLAIM-COVER-RUNG-1`、独立 checker が必須。
- negative checker agreement 前は `RUNG_FALL_CANDIDATE` を発行しない。
- v7 checkpoint/cargo を rename/resume せず、必要なら fresh v8 のみを使う。

### 現存 evidence の再生 command (launch command ではない)

```powershell
.\gap.ps1 search\lins_marked_strictness_export_v1.g
python -B search/b3_gentle_q8_source_producer_v1.py
python -B crosscheck/check_b3_q8_source_census_v1.py
python -B search/b3_gentle_lins_index48_two_source_producer_v1.py
python -B crosscheck/check_b3_lins_index48_sources_v1.py
python -B search/b3_gentle_heisenberg_source_producer_v1.py
python -B crosscheck/check_b3_heisenberg_source_census_v1.py
python -B search/pgl28_independent_window_producer_v1.py
python -B crosscheck/check_pgl28_independent_window_v1.py
```

これらは既存 individual-window evidence の再生用であり、ordinary/special K2 の missing joint/diamond/fibre
receipt を生成しない。本便では一つも再走していない。新 K2 producer/checker の file/command は未承認・
未作成なので、架空の executable command は pin しない。

## 9. n=1 K27 chain は別 calibration

| role | path | bytes | SHA-256 |
|---|---|---:|---|
| producer receipt | `search/certs/d972_idx3_s2_m1zero_v1_20260823.json` | 7,975 | `7e857132777730247564bb73cf5e9edd38c76573e8451ec5b8701f36684a90d8` |
| independent verdict | `crosscheck/verdicts/d972_idx3_s2_m1zero_crosscheck_v1_20260823.json` | 2,438 | `0089c577a1372c9686d2e5eaf3aa9058a60a2545f231a9a1971852a5929afeda` |

verdict は separate chain の `K^(27) cap N_S4`、m1=0 branch に対し k'=`2,11,20`、
`nu=50,32,14` の三明示 lift を独立再生し `PASS_CROSSCHECKED`。これは一段で `I_K=X` を示す
positive calibration だが、receipt 自身も tower non-cofinality と m1=18/36 branch NOT_ATTEMPTED を明記する。
従って普通梯子の denominator、candidate ranking、K1/K2、cofinal survival の証拠へ輸入しない。

## 10. 最終 handoff

```text
CAN_CLOSE_NOW:
  evidence pins; K1 baseline; named-window individual facts; Q8/L48A duplicate;
  L48B central distinction; earliest strict source=node 16437e...bc37;
  pre-diamond joint orders/raw-fibre feasibility; separate K27 calibration tag.

CANNOT_CLOSE_NOW:
  corrected p=2/p=3 canaries; freeze four gates; mode refreeze;
  any H^diamond equality for the selected next source;
  exact post-diamond K1 joint; row36 one-seed candidate count;
  K2 name/freeze/execution/result; v8 launch.

FIRST ACTIONABLE HANDOFF:
  complete and independently check sol/luna_task_159n_pent_canaries.md;
  then refreeze ORDINARY versus SPECIAL_PENT_PREFIX;
  then build the selected K1 joint/diamond/row36 receipt and checker.
```

Scoped terminal token:

```text
K2_PREFLIGHT_COMPLETE__CANARY_PREDECESSOR_OPEN__K2_NOT_FROZEN_NOT_RUN
```

---

## Addendum A (2026-08-24) -- Zassenhaus isolation/diamond and exact row-36 raw fibres

This addendum is a narrowly scoped correction to sections 6.2 and 10 above.  It does
not inspect or use any pentagon producer/checker source, does not execute a canary,
and does not assign a rung name.  The status of the full PB4/Brunnian/pentagon
predicate remains unchanged.  What is closed here is the PB3 isolation/diamond
question and the pre-predicate row-36 reduction fibre.

### A.1 Inputs and evidence grade

| input | bytes | SHA-256 / immutable run pin |
|---|---:|---|
| `papers/2401.06870-gt-shadows-gentle-version.pdf` | 500,548 | `4e0a29e19825810eb9db24ebda120a6805c42fee4eb51679d409c5437e0943ab` |
| `certificates/K36.v1.json` | 727,834 | `feac2a0202e5b78a017272a972e105ac7daf7eb5ca0b4de102b6664b098d8719` |
| `crosscheck/verdicts/K36.v1.verdict.json` | 71,093 | `4436da2643a0577b06761cd310f0032d98fefe67bab10c16f74c534aabb1a92b` |
| `search/certs/b3_gentle_source_census_preflight_v1_20260823.json` | 887,124 | `c30077133305c07ca0e58c9eaa700d42a512a6bbbce96c9c27d161e921e1aaf2` |
| `crosscheck/verdicts/b3_gentle_source_census_v1_20260823.json` | 4,931 | `e308a71323dc429d771d7fb86f507b3c17936716505dd6ca3ee3fbfdeecf7f4e` |
| `search/certs/d972_b4_word_key_artifact_v1_20260816.json` | 176,474 | `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9` |
| accepted p=2 F2 stage-0 result | 2,983-byte `run.log` | run `32647100171`, commit `c8e3bc8dd734d788f8ab9f80773c8503f352c0bf`, log SHA-256 `4c4e501f5443379811dc441e54b13dbf7ba8523ed98fd4d5e2f75029b9948b5f` |

The PDF page images were inspected, not merely the extracted text: printed page 13
contains Proposition 3.5 and equation (3.20); printed pages 20--21 contain
Definition 3.13, Proposition 3.14/equations (3.61)--(3.62), and Proposition 3.15.

The isolation argument below is a paper-proof candidate relative to the already
accepted isolation pin for the bootstrap subgroup.  It is not Lean-verified.  The
K36 orders/marking used below are cross-checked inputs.  The new common-quotient
calculation was also replayed in a read-only, in-memory enumeration, but no new
producer/checker receipt was created in this no-code audit; do not relabel this
addendum itself as a new cross-checked certificate.

### A.2 Exact PB3 Zassenhaus subgroups

Write `PB3 = F2 x <c>`, with `F2=<x,y>`, and put

```text
D_p := D_4^(p)(PB3),       Q_p := F2 / D_4^(p)(F2).
```

Lower-central and power subgroups commute with this direct product decomposition,
so the definitions give exactly

```text
D_2 = (F2^4 gamma_2(F2)^2 gamma_4(F2)) x <c^4>,
D_3 = (F2^9 gamma_2(F2)^3 gamma_4(F2)) x <c^9>.
```

In particular, unlike the earlier `VERBAL-ISO` lemma, these subgroups do not contain
`c`.  That lemma's `c in N` shortcut must not be invoked.  The correct argument is
at PB3 level.

Each `D_p` is fully invariant in PB3: lower-central terms and verbal power
subgroups are preserved by every endomorphism, and so is their product.  It is
finite-index and characteristic in PB3, hence normal under B3 conjugation and an
object of `NFI_PB3(B3)`.

### A.3 PB3-VERBAL-ISO lemma and application

**Lemma (PB3-VERBAL-ISO).**  If `V` is a fully invariant finite-index subgroup of
PB3 and is normal in B3, then `V` is isolated in the gentle-shadow groupoid.

**Proof.**  Take an arbitrary shadow `[m,f] in GT(V)` and set `u=2m+1`.  Equations
(3.20) and (3.41), together with `PB3=F2 x <c>`, show that its PB3 restriction is
the quotient of the genuine PB3 endomorphism

```text
Phi_(m,f): w c^k |-> E_(m,f)(w) c^(u k),
E_(m,f)(x)=x^u,  E_(m,f)(y)=f^(-1)y^u f.
```

Full invariance gives `Phi_(m,f)(V) <= V`, hence
`V <= ker(T_(m,f)|PB3)`.  A shadow is onto by definition (Proposition 3.6), so
Proposition 3.8/first isomorphism gives

```text
[PB3 : ker(T_(m,f)|PB3)] = |PB3/V| = [PB3:V].
```

Finite-index inclusion therefore forces equality.  Equation (3.32) identifies
this PB3 kernel with the B3 kernel, so the shadow is settled.  The shadow was
arbitrary; Definition 3.13 gives isolation.  QED.

Apply the lemma to `D_2` and `D_3`: both are isolated.  The bootstrap subgroup

```text
K1 = K^(36) cap N_S4
```

is already isolated relative to the accepted K36 theorem/certificate and the
settled-54 S4 kernel audit, using Proposition 3.15 once.  Therefore Proposition
3.15, now applied to `K1` and `D_p`, gives for both `p=2,3`

```text
H_p := K1 cap D_p  is isolated.
```

Consequently its connected component has one object.  Proposition 3.14 therefore
specializes to the exact finite-component/diamond statement

```text
Ob(GTSh_conn(H_p)) = {H_p},
H_p^diamond = intersection({H_p}) = H_p.              (p=2,3)
```

There is no missing component census and no index growth on passing to diamond.
The earlier statement that characteristic/B3-normality alone did not prove
isolation remains true in general; the newly used premise is the strictly stronger
**full invariance in PB3**.

### A.4 Exact marked joint quotients

Let

```text
A = F2/(K1 cap F2) = G36 x PSL(2,8),       |A|=11,757,312,
B = F2/(M  cap F2) = G9  x PSL(2,8),       |B|= 1,469,664.
```

The PSL factor has no nontrivial p-group quotient, so every common quotient of
`A` and the p-group `Q_p` comes from `G36`.

The class-3 Hall normal forms give

```text
Q_2: x^a y^b [y,x]^e [[y,x],x]^d [[y,x],y]^h,
     0<=a,b<4 and 0<=e,d,h<2,                    |Q_2|=4^2*2^3=128;

Q_3: x^a y^b [y,x]^e [[y,x],x]^d [[y,x],y]^h,
     0<=a,b<9 and 0<=e,d,h<3,                    |Q_3|=9^2*3^3=2,187.
```

For p=2 the maximal common marked quotient is exact.  In the frozen realization

```text
G36 = <X=(r,s,s), Y=(rs,r,rs)> <= D_36^3,
```

the elements

```text
X^4=(r^4,1,1),  Y^4=(1,r^4,1),  (XY)^4=(1,1,r^(-4))
```

generate `P=(<r^4>)^3 ~= C9^3`, of order 729.  This is normal in the ambient
`D_36^3`, hence in G36.  Since `|G36|=23,328`,

```text
C_2 := G36/P,                  |C_2|=32.
```

It embeds in `(D_36/<r^4>)^3`, a direct product of order-8 dihedral groups.  Thus
`C_2` has exponent at most 4 and class at most 2; its derived subgroup has exponent
at most 2.  Hence `F2^4 gamma_2(F2)^2 gamma_4(F2)` is killed by the marked map and
`Q_2 ->> C_2`.  Conversely, any common quotient of G36 and the 2-group Q2 is a
2-group and must kill the normal 3-group P, so it factors through C2.  Therefore
`C_2` is the maximal common marked quotient, not merely a lower bound.

For p=3, the cross-checked values `|G36|=23,328` and
`|G36'|=1,458` give `|G36^ab|=16`.  A nontrivial finite 3-group has nontrivial
abelianization, so G36 has no nontrivial 3-group quotient.  Thus the maximal common
quotient `C_3` is trivial.

It follows by Goursat that the F2 quotient of `H_p=H_p^diamond` is

```text
J_2 = A x_(C_2) Q_2,             |J_2|=|A|*128/32=47,029,248;
J_3 = A x Q_3,                   |J_3|=|A|*2,187=25,713,241,344.
```

Because `K1` contains `c`,

```text
H_2 = (H_2 cap F2) x <c^4>,
H_3 = (H_3 cap F2) x <c^9>.
```

The marked x and y already have order 36 in the G36 coordinate; their Q2/Q3
orders are 4/9, and c has order 4/9.  Therefore `(H_p)_ord=36` for both primes.

| p | `|Q_p|` | `|C_p|` | `|F2/(H_p cap F2)|` | `|PB3/H_p|` | raw universe `36*|F2/...|` |
|---:|---:|---:|---:|---:|---:|
| 2 | 128 | 32 | 47,029,248 | 188,116,992 | 1,693,052,928 |
| 3 | 2,187 | 1 | 25,713,241,344 | 231,419,172,096 | 925,676,688,384 |

The central factors 4 and 9 belong to the PB3 quotient column.  They must **not**
be multiplied into the raw `(m,f)` universe a second time; the raw universe uses
`N_ord` and the F2 quotient only.

### A.5 Complete row-36 raw-fibre contract

The fixed zero-based row 36 remains

```text
row = [0,[0,[[4,0],[5,0],[0,0]],[1,2,3,4,5,6,7,8,9]],
       [-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]]
key = [0,[[4,0],[5,0],[0,0]],[1,2,3,4,5,6,7,8,9]]
full-row digest   = 31d19295b8b5c2f5e36387f6bb63cec508a7b8770e30bfa6d02909b1f16f4cd8
target-key digest = 3940557ee6c0118f2563ff7d19a41059d0fcdd5c7c876bc56c84b4fa9ae242ac
word digest       = b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d
```

Let `rho:J_p -> B` be reduction and let `j_*` be the evaluation of the archived
signed word in the marked quotient Jp.  It reduces to the frozen target element.
The complete raw fibre is the single kernel coset

```text
Fibre_p(row36) = {(m, j_* z) : m in {0,18}, z in Z_p=ker(rho)}.
```

This is an equality, not a sampling rule.  Indeed, `Z/36 -> Z/18` has the two
lifts 0 and 18, and every group-map fibre is one coset of its kernel.

Put `L=ker(G36 -> G9)`, so `|L|=8`.  Write
`alpha:G36->C_2` and `beta:Q_2->C_2` for the quotient maps above.  Then the kernels
have small coordinate descriptions which avoid enumerating either enormous Jp:

```text
Z_2 = {(l,1,q) : l in L, q in Q_2, alpha(l)=beta(q)}.
      For each of 8 l there are |ker(beta)|=128/32=4 q; hence |Z_2|=32.

Z_3 = L x {1_PSL} x Q_3; hence |Z_3|=8*2,187=17,496.
```

Therefore the exact complete raw counts after diamond are

```text
p=2: 2*32     = 64,
p=3: 2*17,496 = 34,992.
```

These also follow from the uniform index formula

```text
|Fibre_p| = (36/18) * (|J_p|/|B|) = 16*|Q_p|/|C_p|.
```

Deterministic materialization, with no full-Jp BFS, is:

1. Enumerate the 23,328 frozen G36 triples, reduce coordinates modulo 9, and keep
   the 8 elements of L.  Sort them by the frozen triple integer code.
2. Enumerate Qp by the Hall exponent vector `(a,b,e,d,h)` in lexicographic order.
3. For p=2 retain exactly `alpha(l)=beta(q)`; for p=3 retain every pair `(l,q)`.
4. Order first by `m=0,18`, then by the L code, then by the Hall vector.  Emit the
   coordinate element `(m,j_* z)` and hash the canonical compact serialization.
5. Assert counts 64/34,992, no duplicate coordinate pair, exact reduction to the
   frozen key for every row, and no omitted `(l,q)` satisfying the displayed rule.

This closes complete **raw reduction coverage**.  It does not assert that any raw
element satisfies hexagons, charming, onto, or the PB4 predicate.

### A.6 Exact remaining artifact boundary

There is no remaining mathematical diamond datum for p=2 or p=3.  The first
missing immutable execution datum is now narrower:

```text
MARKED-QP-COLLECTOR-AND-JOINT-KERNEL-MATERIALIZATION-RECEIPT
```

For p=2 it must pin the marked pc epimorphism/collector for Q2 (the accepted stage-0
run pinned only order/class), the maps `alpha,beta`, all 32 Z2 coordinate rows, and
the resulting 64 raw rows.  For p=3 it must first independently reconstruct the
2,187-element marked Hall quotient, then pin all 17,496 Z3 coordinates and 34,992
raw rows.  An independent checker must rebuild the Hall multiplication and G36/G9
reductions without importing producer helpers.

A later PB4/coface evaluator and full-predicate receipt are separate downstream
data.  They are not consequences of isolation or raw-fibre coverage and remain
UNKNOWN here.

Scoped addendum token:

```text
ZASSENHAUS_PB3_ISOLATION_DIAMOND_CLOSED_PAPER__ROW36_RAW_COUNTS_64_34992__FULL_PB4_PREDICATE_UNKNOWN
```
