# `mb/ninfty-w6-branch-key/v1` — 点ごと branch key と W-6 outer gate(**draft・未発効**)

2026-08-01 起草: ep-keeper(EP 専任係)。**起点は Sol 便97 §3(F97-3.1・P97-3.1・F97-3.2・W97-3.1・P97-3.2・P97-3.3・P97-3.4)。**

> **本稿の格**: **versioned draft。** Sol P97-3.4 が認可したのは「schema と outer gate の versioned draft・二 lane producer の独立 prototype・負例 suite の着工」までである。
> **W-6 は OPEN。** 本稿の実装が green になっても **W-6 closure ではない**。token 一致だけを closure と宣言すること、弱 W6 を代用すること、EP を発効することは**認可されていない**(P97-3.4)。
> **本稿は governing trio(spec v19 / contract v14 / manifest v14)の era には属さない。** 採用時に spec v20 / contract v15 / manifest v15 と payload-era matrix の新 plane を起こす(P97-3.3)。**凍結 R1/R2 の byte は一切触れない。**

---

## 0. no-go(先に確定した否定・F97-3.1)

| # | 条項 |
|---|---|
| **NG-1** | **非自明な Galois 軌道には Galois-equivariant な点番号は存在しない。** 軌道上で推移的に作用する群が各番号を固定できないため。ゆえに「点ごと」と「Galois 不変」を同時に無償では得られない。 |
| **NG-2** | **NF の最小多項式は軌道の正準表現としては正しいが、点ごとの W-6 key には不足する。** 参考案 (beta) の orbit-level W-6 は診断列 `W6-orbit` としてなら置けるが、**W-6 closure とは数えない**。 |
| **NG-3** | 採るのは (alpha) = **点ごとの符号化**。代償として**固定埋込みへの相対性**を負う。これは欠陥ではなく pointwise incidence のために払う**明示的 rigidification** であり、座標・埋込みは digest で束縛する(F97-3.2)。 |

---

## 1. 宇宙の事前登録

**v1 の宇宙は 係数体 $\mathbf Q$、固定標的 $\mathbf P^1_\mu$ に限定する**(P97-3.1)。これ以外(数体係数・別標的座標)は本 schema の対象外であり、**範囲外は silent に広げず MALFORMED とする**。

---

## 2. 符号化(P97-3.1 逐語条項)

| # | 条項 | 逐語根拠(便97 P97-3.1) |
|---|---|---|
| **K-1** | **一度だけ $\overline{\mathbf Q}\subset\mathbf C$ と実軸・虚軸の向きを固定する。** | 「一度だけ $\overline{\mathbf Q}\subset\mathbf C$ と実軸・虚軸の向きを固定する」 |
| **K-2** | 有限 branch point $b$ の最小多項式を $m_b(T)\in\mathbf Z[T]$ とする。**係数は低次順・係数 gcd $=1$・最高次係数 $>0$・$\mathbf Q$ 上既約。**この規約で scalar 倍を除く。 | 「係数は低次順、係数 gcd $=1$、最高次係数 $>0$、$\mathbf Q$ 上既約。この規約で scalar 倍を除く」 |
| **K-3** | $m_b$ の複素根を **exact な辞書式** $z<z' \iff \Re z<\Re z'$ または($\Re z=\Re z'$ かつ $\Im z<\Im z'$)で並べ、$b$ の **0-based rank $k$** を付ける。 | 同上 |
| **K-4** | **数値近似の比較は禁止。** certified root isolation / exact algebraic comparison を使う。**isolation box 自体は key に入れない。** | 「数値近似の比較は禁止し、certified root isolation/exact algebraic comparison を使う。isolation box 自体は key に入れない」 |
| **K-5** | `branch_value` は object でなく、**凍結 Python 辞書の key にできる canonical ASCII string** とする。 | 「`branch_value` は object でなく、凍結 Python 辞書の key にできる canonical ASCII string とする」 |

### 2.1 token 文法

```text
aqp1|mu|I
aqp1|mu|F|a0,a1,...,ad|k
```

| # | 条項 |
|---|---|
| **G-1** | integer は **ASCII 十進**。**空白・`+`・先頭零・`-0` を禁止**する。 |
| **G-2** | `I` は infinity。有限 token では $d\ge1$、$0\le k<d$。 |
| **G-3** | artifact 外枠に **`branch_key_schema_id`・`target_coordinate_id`・その定義 digest を必須**にし、**token prefix と一致**させる。 |
| **G-4** | prefix `aqp1` = target_coordinate_id(標的 $\mathbf P^1$ の固定アフィン座標)、`mu` = 固定した写像の名前。**prefix と外枠 id の不一致は MALFORMED。** |

### 2.2 現 genuine の例(P97-3.1 逐語)

```text
infinity                         -> aqp1|mu|I
0                                -> aqp1|mu|F|0,1|0
-16*sqrt(5)*i/125                -> aqp1|mu|F|256,0,3125|0
+16*sqrt(5)*i/125                -> aqp1|mu|F|256,0,3125|1
```

$3125T^2+256$ の二根は実部が等しく、**負の虚部が rank 0・正の虚部が rank 1**。ゆえに共役点は分離される。一方 **NF は従来どおり `[256/3125,0,1]` という orbit-level component を保持する。両者を同じ schema にしない。**

### 2.3 v1 の決定可能範囲(fail-closed)

**exact rank / 既約性を決定できない場合は PASS を出さない**(P97-3.2 末尾「exact rank や像を決定できない場合は ABSENT/UNKNOWN」)。v1 実装が exact に決定するのは **$d\le2$**:

- $d=1$: rank $0$、既約は自明。
- $d=2$: 判別式 $D=a_1^2-4a_0a_2$。$D<0$ なら共役対で実部が等しく、**負の虚部が rank 0**。$D>0$ なら実根二つで小さい方が rank 0。$D$ が平方数なら**既約でない**ので拒否。
- $d\ge3$: **UNKNOWN**(float fallback は禁止 — P97-3.2)。

---

## 3. 生成規律 — H-4 を壊さない(F97-3.2 逐語条項)

| # | 条項 |
|---|---|
| **H-1** | lane A は**自身の** curve equation・ideal/locus・写像 $\mu$ から消去・因数分解・exact root rank を導く。 |
| **H-2** | lane B は**自身の** exact algebraic-number 表現から最小多項式と rank を導く。SymPy `srepr` は native provenance として残してよいが **key には使わない**。 |
| **H-3** | **lane A が lane B の token/NF を読むこと、lane B が lane A の ideal normalization を読むことを禁止する。** |
| **H-4′** | **二 producer は common executable canonicalizer を共有しない。**共通なのは本節の数学的 schema だけである。 |
| **H-5** | 既存 NF digest 一致は本符号化が実現可能であることの**予備証拠**にはなるが、**runtime の共通入力・oracle にはしない**。 |

---

## 4. 点ごと map schema `mb/ninfty-w6-point-map/v1`(P97-3.2 逐語)

lane A の registry-pinned map は **aggregate でなく**、少なくとも次の point/component record の配列にする。**frozen core は extra key を無視して同じ配列を加算できる。**

```json
{
  "ramification_point_id": "<point-level canonical/ref-bound ID>",
  "branch_value": "aqp1|mu|F|256,0,3125|0",
  "multiplicity": 1,
  "source_locus_ref": {"artifact_id":"...","json_pointer":"...","digest":"..."},
  "exact_image_witness": {"schema_id":"...","digest":"..."}
}
```

> **P-1(P97-3.2 逐語)**: lane A の現 `x^2+6x+8` は $x=-2,-4$ の orbit/support しか表さず、**各 $x$ 上の $\pm y$ を点として分離しない**。ゆえに**単に NF の branch polynomial を二根へ割り当ててはならない**。curve relation と $\mu(x,y)$ から点を作り、必要なら rational-univariate representation と exact reduction witness で像を証明する。

---

## 5. 凍結 R1/R2 の**外側**の再計算ゲート(W97-3.1 / P97-3.2)

> **W97-3.1 の指摘**: `verify_W6_single` と R2 は dereference した `map_ref` の各 `{branch_value,multiplicity}` を加算して二辞書を比較するだけで、`ramification_ref`/`branch_ref`/`witness_ref` を像 $r\mapsto\mu(r)$ の exact 計算に使わず、**token が本 schema から正しく作られたかも検査しない**。ゆえに producer が任意 token を自己申告し二 map が偶然一致すれば frozen core は PASS し得る。**比較 core の外側に validation が必要。**

各 route が独立に次を行う(P97-3.2 の 6 項目を逐語で実装単位にする)。

| gate | 条項 | v1 実装状態 |
|---|---|---|
| **KEY** | token grammar・原始化・既約性・root rank・coordinate/schema digest を**再計算**。 | **実装済**($d\le2$ で exact・$d\ge3$ は UNKNOWN) |
| **COVERAGE** | ramification support の**全点を一度ずつ覆い**、重複・欠落がないことを確認。 | **実装済** |
| **IMAGE** | 各点で $\mu(r)=b$ を **exact に確認**し、multiplicity の型を確認。 | **部分実装**: token ↔ exact image datum の再計算(`IMAGE-KEY`)は実装済。$\mu(r)=b$ 本体(`IMAGE-MU`)は curve model 側の witness が要るため **v1 は UNKNOWN 固定**。ここが W-6 の残り穴である。 |
| **AGGREGATE** | lane A の per-point pushforward を**受領側が集計**し、lane B の独立 branch divisor map と比較可能な形にする。 | **実装済** |
| **INDEPENDENCE** | 二 producer と二 receiver route の dependency closure を照合し、**共通 math helper / 片側出力の読込みを禁止**。 | **実装済**(構造検査) |
| **最終比較** | 上記 PASS 後に**のみ**、既存 R1/R2 の辞書 equality を W-6 の最終比較として使う。 | **未到達**(IMAGE-MU が UNKNOWN のため) |

| # | 条項 |
|---|---|
| **O-1** | **二 receiver route も key/image の共通実装を共有してはならない。**(P97-3.2 逐語)本稿の実装は `search/ninfty-w6-key-gate-r1p.py` と `search/ninfty-w6-key-gate-r2p.py` の**二本**であり、**互いを import せず・共通 helper module を持たない**。rank 判定は前者が判別式、後者が **Sturm 列 + 有理区間二分**、既約性は前者が平方数判定、後者が**有理根定理**という**別アルゴリズム**である。 |
| **O-2** | schema/provenance 不正は **MALFORMED/INTEGRITY_STOP**、exact rank や像を決定できない場合は **ABSENT/UNKNOWN**、**well-formed な divisor 不一致だけを W-6 FAIL** とする。 |
| **O-3** | **orbit key や float への fallback は禁止。** |

---

## 6. version/era と必須 fixture(P97-3.3)

> **P97-3.3 逐語**: 「この追加は v18 payload schema の黙った拡張ではない。新しい key schema、point-map schema、spec/contract/manifest、payload-era matrix の plane を versioned に起こす。凍結 core に新 payload を嘘の v18 として読ませてはならない。既存 façade が型上受け取れない場合は core byte をコピー改変せず、versioned adapter/route `R1'/R2'` を新設する。」

| # | 条項 | 状態 |
|---|---|---|
| **V-1** | 新 key schema `mb/ninfty-w6-branch-key/v1`・point-map schema `mb/ninfty-w6-point-map/v1` を versioned に起こす。 | **本稿で起票** |
| **V-2** | spec v20 / contract v15 / manifest v15 と payload-era matrix の新 plane(`w6_key_route`)。 | **未着手 — 司令塔検問 + Sol ゲート待ち**(意味論の新設は係の職掌外) |
| **V-3** | 凍結 core に新 payload を v18 として読ませない。**versioned adapter/route `R1'/R2'` を新設**(core byte はコピー改変しない)。 | **本稿の二 gate module が `R1'`/`R2'` の receiver 側** |

### 6.1 必須 fixture(P97-3.3 の 7 項目)

| # | fixture | 実装 |
|---|---|---|
| 1 | genuine 四点 $(0,\infty,\pm16\sqrt5 i/125)$ の**両 lane token 一致** | `test_ninfty_w6key.py` §2 |
| 2 | rational polynomial の **scalar 倍・分母表現が同じ token へ正規化**される正例 | §3 |
| 3 | **係数 1,2 の共役二点 incidence swap: NF PASS・pointwise W-6 FAIL** | §4 |
| 4 | **root rank の片側 swap・token 改竄・wrong coordinate digest** | §5 |
| 5 | ramification point の**重複・欠落** | §6 |
| 6 | **float 近似だけ・非既約 polynomial・範囲外 rank** を fail-closed | §7 |
| 7 | **lane A が lane B token を読む / 共通 canonicalizer を使う H-4 負例** | §8 |

> **注意(P97-3.3 末尾・逐語)**: 「W-6 が等置するのは pushforward divisor であり、あらゆる labelled incidence graph そのものではない。**等しい multiplicity をもつ二点の交換で pushforward divisor が変わらない場合、それを W-6 が分離しないのは正しい**。★負例は 1,2 のように交換で branch-wise multiplicity が変わるものを使う。」— §4 の負例は **multiplicity 1,2** を使い、**multiplicity が等しい交換は「分離しないのが正しい」正例**として別に張る。

---

## 7. 出所

- Sol 便97 §3(`sol/sol_reply_97_math24.md`)。
- governing spec `docs/week4-NInfty_stage2_spec_v19.md` §5.3.5(W-6 option (a)・`UNKNOWN W6-KEY`)。
- 実装: `search/ninfty-w6-key-gate-r1p.py`・`search/ninfty-w6-key-gate-r2p.py`・`search/test_ninfty_w6key.py`。
