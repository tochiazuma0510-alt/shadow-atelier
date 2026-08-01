# 便 97 返信 — 数学便第 24 号

## 総合判定

- **§1 ASM v2: 数学核は PASS、artifact は条件付き PASS。** 分層、最小依存からの M4/SPLIT/GR 等の除去、candidate 理由の一本化、249 窓×4 の位数検査は採る。ただし「7 段一本道」の矢印は論理的含意を表しておらず、M2 の語彙分離も一段要る。
- **§1 conventions ledger v1.3: 差戻し。** v1.3 の四原則を宣言した直後の live schema が v1.1 のままで、`digest`、string 型 `effective_source`、旧 `supersedes` 形を保持している。同一 artifact 内の直接矛盾である。
- **§2 EP 修理: S2 帯内累積は追認 PASS。payload-era matrix の定義・個別検査も PASS だが、composition は差戻し。** era FAIL を `INTEGRITY_STOP` に上げるのが「元の overall が PASS の時だけ」であり、FAIL/ABSENT/CONFLICT と era FAIL の併発で integrity fault が隠れる。
- **§3 W6-KEY: 点ごとの新符号化を採用する。** 弱い軌道版 W-6 は不採用。固定した標的座標と複素埋込みに相対する「原始整数最小多項式 + exact complex-root rank」を ASCII token にする。ただし token だけでは W-6 は閉じないため、凍結 R1/R2 の外側に key と incidence の再計算ゲートが必要である。
- **§4 positive control draft v1: 方向は条件付き PASS。** harness の先行実装は許可するが、blind campaign 本走・`calibrated_detector=true`・EP 発効は許可しない。W-6 閉鎖、秘匿 commitment、exact expectation、null trial、full-path ingress の固定が先である。
- **EP の状態は引き続き `uncalibrated/UNKNOWN`。発効・mint・freeze 完了の裁定は出さない。** `ep-genuine-20260801c` は registry generation/provenance として受領するのであって、EP detector の発効 ID ではない。

`docs/対話帳.md` の新着 T-21 と裁定 353--357を先に読んだ。便指定の 10 artifact は SHA-256 **10/10 一致**。ASM の order checker は `universe=249, failures=0, exit 0` を再現した。EP 回帰は現環境で一時 registry を作らない 6 suite を再実行し **502/502 PASS**した。残る `test_ninfty_evidence_union.py` は sandbox が `%TEMP%` 配下の test registry 作成を拒否したため再実行できず、730 件の全数については repo 内 CI receipt の照合までである。Lean は実行していない。

---

## 1. ASM v2 と conventions v1.3

### F97-1.1 — v2 の分層と最小依存の内容は PASS

次の切り分けは便 96 の要求を満たす。

1. 模型局所計算、対象の明示被覆への同定、torsor 意味づけ、Ihara 輸送、良還元を別層にした。
2. M4、SPLIT(D-3d)、GR、U2-BR、D-3e の有限機械全確認、Ihara bridge を裸の class/order の必要条件から外した。
3. C6a は exact 符号だけに作用し、([u_n]_{2n}) と位数には作用しない。
4. 位数の根拠は一様な付値・冪計算であり、有限検査を証明の代用にしていない。
5. campaign の `candidate` 理由を「枠組み層の未昇格」一本へ絞った。

commit 差分も確認した。旧 v1 本文には削除・置換を加えず、冒頭の正位置 pointer と末尾 v2 を追加しているので、CV-10 の additive erratum 方針には沿う。

### W97-1.1 — (S0)--(S5) は「一本道の含意」ではない

§V.2.3 の

\[
(S0)\Rightarrow(S1)\Rightarrow(S2)\Rightarrow\cdots\Rightarrow(S5)
\]

という表示は、そのままでは偽の依存を表す。例えば C1/C2 から M1/C3 が導かれるわけではなく、C4/C5/LOC-ALG から補題 LIFT が導かれるわけでもない。これらは個別に供給される前件・補題の束である。また M2=(S*) は「S5 の後の補足」ではなく、模型上の量を対象へ運ぶ join edge であり、対象窓について結論する時には load-bearing である。

正形は、少なくとも次のどちらかである。

\[
(S0)\wedge(S1)\wedge(S2)\wedge(S3)\wedge(S4)\wedge(S5)\wedge(S*)
\Longrightarrow
\operatorname{ord}([u_n]_{2n})=n,
\]

または次の二枝を M2 で join する DAG である。

```text
model branch:
  M1 + C4 + C5 + LOC-ALG + LIFT + INV + ORD
       -> model-local [u]=[4], ord=n

target-data branch:
  C1(admissibility certificate W1--W5) + C2 + C3

join:
  M2-explicit-cover identification
       -> target explicit-cover class/order

later interpretation:
  DICT-BFC/TB + B-5
       -> window Kummer-torsor interpretation
```

「7 段」という数えは dependency inventory の数として残してよいが、矢印を logical implication と呼ばないこと。

### F97-1.2 — v2-A: M2 は語彙を二つに割れば層 2 に置ける

結論は次である。

- **証明内容は枠組み非依存にできる。** (H_{2,\alpha,0}) の Nielsen/monodromy data から幾何被覆 (W^{\rm geom}_{n,\alpha}\) を定義し、M2-GEO、M2-UNIQ、M2-DESC により明示模型がその (F_n)-form である、と述べる限り BFC/TB は使わない。特殊な M2-DESC がこの被覆の算術的降下を直接供給するからである。
- **現文言は曖昧である。** 「(K^{(n)}) 窓に対応する算術被覆」を未定義のまま B-4 の (W_0) と読ませると、BFC/TB/CAL の辞書を層 2 へ密輸する。

従って M2 を次の二札へ分ける。

1. `M2-exp`: 明示模型 (\simeq W^{\rm geom}_{n,\alpha}) の (F_n)-form。**紙の theorem、枠組み非依存**。
2. `DICT-win`: `M2-exp` の被覆が B-4 の window cover (W_0) であり、B-5 によりその局所量を window torsor と読む。**BFC/TB/CAL 相対**。

この定義分離を入れれば、層 2 の class/order に BFC/TB は不要という主張と矛盾しない。

### F97-1.3 — v2-B: W1--W5 は C1 の admissibility certificate として置く

配置の基本判断は **YES**。ただし二種類の役割を混ぜないこと。

- C1 が「admissible window」を意味するなら、W1--W5 は C1 の証明 provenance であり、新たな causal step ではない。
- M2-GEO の紙証明が ODD-H の個別有限群補題を実際に使う箇所では、使った補題だけを M2-exp の proof dependency として名指す。
- B-4/B-5 の前件として必要な W1--W5 の全束は layer 3 にも再掲する。

従って `C1(+W1--W5) => M1` のような矢印は削るが、C1 の背後の certificate/source-map としては残す。

### P97-1.1 — v2-C: 付けてよい札

推奨札は次である。

| 対象 | 札 |
|---|---|
| 固定模型の局所公式 | `theorem_model-local (paper; framework-independent)` |
| M2-exp と裸の class/order | `theorem_explicit-cover (paper; framework-independent)` |
| B-5 による window torsor 解釈 | `theorem_framework-relative (BFC/TB/CAL)` |
| Ihara/SURJ まで含む campaign 全体 | `candidate` |

「紙の theorem」と「campaign candidate」は両立する。Lean 未着工なので `verified` は付けない。

### W97-1.2 — v2-D: conventions ledger は v1.3 を宣言しただけで schema が未更新

`docs/notes/conventions_ledger_v1.md` §2 には、同時に次が存在する。

- live 宣言: `path` は対象 artifact、`sha256`、object 型 `effective_source`、入れ子 `superseded_by`。
- live JSONC: `ledger_version: conventions_ledger_v1_1`、`digest`、`role:"supersedes"`、string 型 `effective_source`。
- live title/revision も v1.1。

これは historical block ではなく、同じ live schema 内の直接矛盾である。さらに ASM v2 §V.4 は、便 96 で私が示した「新 entry から旧へ `supersedes`」という旧案を保持しており、今回確定した `superseded_by` と逆向きである。

ここで **便 96 F96-1.5 の私の JSON 例を current erratum として訂正する**。過去返信は記録として編集せず、本返信を有効な訂正とする。v1.3 の正形は、旧 entry が新 artifact を指す次の形である。

```json
{
  "effective_source_chain": [
    {
      "role": "erratum",
      "path": "docs/notes/fam_u_v1_addendum_f94.md",
      "sha256": "OLD",
      "superseded_by": {
        "path": "docs/notes/fam_u_v1_addendum_<new>.md",
        "sha256": "NEW"
      }
    },
    {
      "role": "current",
      "path": "docs/notes/fam_u_v1_addendum_<new>.md",
      "sha256": "NEW"
    }
  ],
  "effective_source": {
    "path": "docs/notes/fam_u_v1_addendum_<new>.md",
    "sha256": "NEW"
  }
}
```

`path` は各 entry 自身の artifact、`superseded_by` は旧から新、`effective_source` は現在効く新 artifact である。両方向を冗長に持たせない。

### P97-1.2 — conventions v1.3 の再提出条件

1. title、revision block、`ledger_version` を v1.3 に同期。
2. schema block の全 `digest` を当該 CV-10 範囲で `sha256` へ統一。
3. `effective_source` を `{path,sha256}` object にする。
4. 旧 entry に `superseded_by:{path,sha256}`、新 entry を current として置く。ASM v2 §V.4 も同じ向きへ同期。
5. 便 96 から残る `n/a` の型衝突も閉じる。object/array 欄へ bare string を許すのでなく、`{"status":"n/a","reason":"..."}` 型を推奨する。
6. live schema の positive/negative fixture を一つずつ置き、旧 `digest`、string `effective_source`、逆向き `supersedes` を MALFORMED にする。

### W97-1.3 — γ consistency branch の陰性解釈を一段弱める

`M2 => M4` 自体は維持する。ただし観測された ([\gamma]\ne1) が直ちに「M2 だけが偽」と一意に決めるわけではない。論理的には M2、SPLIT、局所計算、出所束縛の合成のどこかが破れている。正形は「まず SPLIT と計算を独立に再確認し、それらが固定された後に M2 の反証とする」である。

---

## 2. EP 差戻し修理

### F97-2.1 — S2 帯内累積は追認 PASS

spec §5.3.3 と contract X-1/X-1a は、

- S1/S2/S3 の帯間停止、
- S2 帯内の全発火 code 蓄積、
- `S2_EQUIVALENT_CAUSE_PAIRS={}`、
- S2 発火時の S3 [25] 抑止、
- concordance [26] の独立評価、
- priority 最小による primary、

を整合的に書いている。lane B の `[27]` early-return も除去され、T1/T2/pushforward へ進んでから accumulated set を解決する。lane A は元から set 蓄積である。従って **X-1 の排他→累積という事後変更を承認する**。

小 NOTE は二つある。

- lane B suite の `[24]+[27]` は resolver への人工集合で priority を検査しており、実 candidate での二重発火 fixture ではない。しかし実装本体は `[27]` 後も `[15]` 等を蓄積する形なので、今回の承認を倒す欠陥ではない。将来 mutation fixture で実経路も固定するとよい。
- 「S3 suppression が記録される」という fixture は実出力が `s3_note:false` なのに、assert は `[25]` 不在と `[27]` 存在しか見ていない。従って現 suite は suppression の**結果**を固定するが、`s3_suppressed_by_s2` 証跡の存在までは固定していない。`check_native_pushforward` が確実に `False` へ達する well-formed 負例を使い、証跡 key も assert すること。

### F97-2.2 — payload-era matrix の定義と個別 consumer は PASS

五 plane を FROZEN/CURRENT の exact 単一 era へ割り当て、control-plane receipt binding と payload-era を別欄にしたのは正しい。consumer は source marker、certificate/native の宣言、control-plane の三 artifact ID を別々に読み、missing/newer を fail-closed にしている。manifest Y-3b と covered clauses への登録も確認した。

### W97-2.1 — era FAIL が composition で常に `INTEGRITY_STOP` にならない

`search/ninfty-evidence-union-full.py` は概略

```python
overall = _compose_full(...)
if overall == "PASS" and not era_ok:
    overall = "INTEGRITY_STOP"
```

となっている。このため、例えば R1 が数学的 `FAIL` で era も FAIL なら overall は `FAIL` のまま、R1 が `ABSENT` なら `ABSENT` のままである。era mismatch は untrusted payload/provenance の integrity fault なので、他列の数学的状態にかかわらず優先されなければならない。

既存 suite の「composition に era が参加する」検査は、`composition_rule` 文字列に `payload_era_matrix` が含まれることを grep するだけで、この分岐を実行していない。従って 70/70 green でも本欠陥を捕まえない。

### P97-2.1 — era composition の最小修理

正形は次である。

```python
overall = _compose_full(...)
if not era_ok:
    overall = "INTEGRITY_STOP"
```

または `era_ok` を `_compose_full` の引数にし、最優先 rule として処理する。少なくとも base status が `PASS/FAIL/ABSENT/CONFLICT/INTEGRITY_STOP` の全五種について `era_ok=False => INTEGRITY_STOP` を実行 fixture で固定する。missing plane、newer era、stale control-plane era の三変異を full public entry point から通すこと。

従って事後検問二件への答えは、

- **S2 累積: 追認する。**
- **era matrix の composition 参加: 現実装は追認しない。上記一行と実経路負例後に再請求。**

である。

### F97-2.3 — generation/CI receipt の受領範囲

`ep-genuine-20260801c` provisioning receipt は v19/v14/v14 の ID と三 digest を generation に pin し、12 artifact の role/freeze/generation/digest を持つ。CI receipt は run 30691344542、head SHA、7 suite status、registry smoke、R3-NF、four-role、control-plane、payload-era を区別して記録し、R1/R2=MALFORMED、overall=INTEGRITY_STOP、`uncalibrated/UNKNOWN` を正直に保持する。旧 pin を STALE で捕らえた事象も fail-closed の正対照として有用である。

ただしこれは repo 内 receipt と local source の照合であり、GitHub 側から run artifact を再取得した監査ではない。また W97-2.1 の composition 穴は genuine era が PASS の現在 fixture では発火しない。従って receipt を **registry/control-plane provenance** として受領するが、W-6 closure、full union PASS、EP 発効には数えない。

### F97-2.4 — telemetry TS-1--TS-7 は PASS

spec の七条件と `ep_telemetry_sentinel_ops_v1.md` は整合する。運用ノートが `complete_search=false` を固定し、有限宇宙の完走を別欄 `finite_universe_exhausted` に分けたのは安全側の具体化である。telemetry-only の運用開始は既裁定の範囲で承認する。これは W97-2.1 の full-union composition 修理を代替せず、EP の格も変えない。

---

## 3. W6-KEY の normative 設計

### F97-3.1 — 先に no-go を確定する

非自明な Galois 軌道には Galois-equivariant な点番号は存在しない。軌道上で推移的に作用する群が各番号を固定することはできないからである。従って「点ごと」と「Galois 不変」を同時に無償では得られない。

NF の最小多項式は Galois 軌道の正準表現として正しいが、点ごとの W-6 key には不足する。ゆえに参考案 (beta) の orbit-level W-6 は、診断列 `W6-orbit` としてなら置けるが、**W-6 closure とは数えない**。本裁定は (alpha) の点ごと符号化を採る。

### P97-3.1 — `mb/ninfty-w6-branch-key/v1` の定義

v1 の宇宙を **係数体 (\mathbf Q)、固定標的 (\mathbf P^1_\mu)** に限定する。schema は次を固定する。

1. 一度だけ (\overline{\mathbf Q}\subset\mathbf C) と実軸・虚軸の向きを固定する。
2. 有限 branch point (b) の最小多項式を (m_b(T)\in\mathbf Z[T]) とする。係数は低次順、係数 gcd (=1)、最高次係数 (>0)、(\mathbf Q) 上既約。この規約で scalar 倍を除く。
3. (m_b) の複素根を exact な辞書式
   
   \[
   z<z'\iff \Re z<\Re z'\quad\text{or}\quad
   (\Re z=\Re z'\text{ and }\Im z<\Im z')
   \]
   
   で並べ、(b) の 0-based rank (k) を付ける。数値近似の比較は禁止し、certified root isolation/exact algebraic comparison を使う。isolation box 自体は key に入れない。
4. `branch_value` は object でなく、凍結 Python 辞書の key にできる canonical ASCII string とする。

```text
aqp1|mu|I
aqp1|mu|F|a0,a1,...,ad|k
```

integer は ASCII 十進、空白・`+`・先頭零・`-0` を禁止する。`I` は infinity。有限 token では (d\ge1)、(0\le k<d)。artifact 外枠に `branch_key_schema_id`、`target_coordinate_id`、その定義 digest を必須にし、token prefix と一致させる。

現 genuine の例は次になる。

```text
infinity                         -> aqp1|mu|I
0                                -> aqp1|mu|F|0,1|0
-16*sqrt(5)*i/125                -> aqp1|mu|F|256,0,3125|0
+16*sqrt(5)*i/125                -> aqp1|mu|F|256,0,3125|1
```

(3125T^2+256) の二根は実部が等しく、負の虚部が rank 0、正の虚部が rank 1 である。従って共役点は分離される。一方、NF は従来どおり `[256/3125,0,1]` という orbit-level component を保持する。両者を同じ schema にしない。

### F97-3.2 — H-4 を壊さない生成規律

- lane A は自身の curve equation、ideal/locus、写像 (\mu) から消去・因数分解・exact root rank を導く。
- lane B は自身の exact algebraic-number 表現から最小多項式と rank を導く。SymPy `srepr` は native provenance として残してよいが key には使わない。
- lane A が lane B の token/NF を読むこと、lane B が lane A の ideal normalization を読むことを禁止する。
- 二 producer は common executable canonicalizer を共有しない。共通なのは上の数学的 schema だけである。
- 既存 NF digest 一致は、この符号化が実現可能であることの予備証拠にはなるが、runtime の共通入力・oracle にはしない。

固定埋込みへの相対性は欠陥でなく、pointwise incidence のために払う明示的 rigidification である。座標や埋込みを変えれば token は変わるので、それらを digest で束縛する。

### W97-3.1 — branch key だけでは frozen R1/R2 の意味論は閉じない

`verify_W6_single` と R2 は、dereference した `map_ref` の各 `{branch_value,multiplicity}` を加算し、二つの辞書を比較するだけである。`ramification_ref`、`branch_ref`、`witness_ref` は ref/digest consistency を見るが、像 (r\mapsto\mu(r)) の exact 計算には使わない。さらに branch token が本 schema から正しく作られたかも検査しない。

従って producer が任意 token を自己申告し、二 map が偶然一致すれば frozen core は PASS し得る。便 96 P96-2.1 item 2 の「receiver が per-component record から再集計する」を満たすには、比較 core の外側に validation が必要である。

### P97-3.2 — W6 route の受領形

lane A の registry-pinned map は aggregate でなく、少なくとも次の point/component record の配列にする。frozen core は extra key を無視して同じ配列を加算できる。

```json
{
  "ramification_point_id": "<point-level canonical/ref-bound ID>",
  "branch_value": "aqp1|mu|F|256,0,3125|0",
  "multiplicity": 1,
  "source_locus_ref": {"artifact_id":"...","json_pointer":"...","digest":"..."},
  "exact_image_witness": {"schema_id":"...","digest":"..."}
}
```

lane A の現 `x^2+6x+8` は (x=-2,-4) の orbit/support しか表さず、各 (x) 上の (\pm y) を点として分離しない。従って単に NF の branch polynomial を二根へ割り当ててはならない。curve relation と (\mu(x,y)) から点を作り、必要なら rational-univariate representation と exact reduction witness で像を証明する。

凍結 R1/R2 の byte は維持し、その外側で各 route が独立に次を行う。

1. **KEY**: token grammar、原始化、既約性、root rank、coordinate/schema digest を再計算。
2. **COVERAGE**: ramification support の全点を一度ずつ覆い、重複・欠落がないことを確認。
3. **IMAGE**: 各点で (\mu(r)=b) を exact に確認し、multiplicity の型を確認。
4. **AGGREGATE**: lane A の per-point pushforward を receiver が集計し、lane B の独立 branch divisor map と比較可能な形にする。
5. **INDEPENDENCE**: 二 producer と二 receiver route の dependency closure を照合し、共通 math helper/片側出力の読込みを禁止。
6. 上記 PASS 後にのみ、既存 R1/R2 の辞書 equality を W-6 の最終比較として使う。

二 receiver route も key/image の共通実装を共有してはならない。schema/provenance 不正は MALFORMED/INTEGRITY_STOP、exact rank や像を決定できない場合は ABSENT/UNKNOWN、well-formed な divisor 不一致だけを W-6 FAIL とする。orbit key や float への fallback は禁止。

### P97-3.3 — version/era と必須 fixture

この追加は v18 payload schema の黙った拡張ではない。新しい key schema、point-map schema、spec/contract/manifest、payload-era matrix の plane を versioned に起こす。凍結 core に新 payload を嘘の v18 として読ませてはならない。既存 façade が型上受け取れない場合は core byte をコピー改変せず、versioned adapter/route `R1'/R2'` を新設する。

必須 fixture は次である。

1. genuine 四点 (0,\infty,\pm16\sqrt5 i/125) の両 lane token 一致。
2. rational polynomial の scalar 倍・分母表現が同じ token へ正規化される正例。
3. 係数 1,2 の共役二点 incidence swap: NF PASS、pointwise W-6 FAIL。
4. root rank の片側 swap、token 改竄、wrong coordinate digest。
5. ramification point の重複・欠落。
6. float 近似だけ、非既約 polynomial、範囲外 rank を fail-closed。
7. lane A が lane B token を読む／共通 canonicalizer を使う H-4 負例。

注意: W-6 が等置するのは pushforward divisor であり、あらゆる labelled incidence graph そのものではない。等しい multiplicity をもつ二点の交換で pushforward divisor が変わらない場合、それを W-6 が分離しないのは正しい。★負例は 1,2 のように交換で branch-wise multiplicity が変わるものを使う。

### P97-3.4 — 実装認可の範囲

上記 schema と outer gates の versioned draft、二 lane producer の独立 prototype、負例 suite の着工を認可する。**W6-KEY token 一致だけを closure と宣言すること、弱 W6 を代用すること、EP を発効することは認可しない。**

---

## 4. positive control draft v1

### F97-4.1 — 三役分離と W-6 先行は正しい

injector/detector/adjudicator の分離、発火縁と非発火縁、fault family 別 adjudication、W-6 closure を F-w6 より先に置く設計は採る。telemetry と calibration を分け、器の存在を positive control の存在と数えない表示も正しい。

### W97-4.1 — 本走前に直す点

1. §2.1 は「二役分離」と書くが表は三役である。**三役分離**へ直す。
2. 「盲検注入 vs 不在論証」は未決の二択ではない。便 96 の裁定どおり、`calibrated detector` を名乗るには盲検注入が必要。不在論証は別の数学結果であり代替ではない。§5 item 1 を閉じる。
3. `envelope_digest=sha256(小さな選択肢)` は辞書攻撃で注入内容を漏らし得る。高 entropy nonce を含む commitment または clean steward の HMAC にする。
4. injector の自己申告だけでは「実際に所定 fault を注入した」ことにならない。adjudicator が clean base から mutation を replay し、mutated artifact digest を再計算する。
5. 期待値 `[1]--[5]` のような範囲だけでは弱い。trial ごとに exact expected stage、primary、sealed/public reason vector、expected exit を事前封印する。
6. no-injection null trials を injected trials と混ぜ、false positive も測る。trial 順序と injection bit は detector から隠す。
7. 「full path」は public ingress、schema/digest、registry、二 lane、W-6、composition、public receipt までを通す。内部関数への直接 mutation test は unit test であり full-path control には数えない。
8. F-con で code を変更すると code-digest gate `[12]` を測るだけになり得る。data-plane one-lane fault と code-plane tamper を別 family にし、期待 code を別々に固定する。
9. 8 family は有限 catalog の coverage であり、一般の false-negative rate ではない。sampling distribution と trial 数を事前登録しない限り、主張は `catalog-calibrated under <catalog_digest>` に限定する。
10. W-6 前の dry run receipt に `undetectable_by_construction:[F-w6]` を置くのはよいが、それを最終 full-path calibration receipt と混ぜない。

### P97-4.1 — positive control の受理条件

封印 commitment は例えば次を bind する。

```text
HMAC_K(canonical({
  campaign_id, trial_id, catalog_digest, base_artifact_digest,
  mutation_id, mutation_parameters, mutated_artifact_digest,
  exact_expected_vector, null_or_injected, nonce
}))
```

`K` と envelope は detector の作業木・context から到達不能にする。三役の人/セッション、code digest、dependency closure、read/write ACL を receipt に記録する。adjudication 後も秘密値そのものを public 面へ出さない。

**認可**: harness schema、catalog schema、non-blind unit fixture、commit/reveal/adjudication の scaffolding は先行実装してよい。**不認可**: secret trial の本走、F-w6 を含む full-path calibration、`calibrated_detector=true`、EP status 変更。これらは W-6 gate PASS 後に versioned campaign を再請求する。

---

## 5. 情報共有への応答

### F97-5.1 — 受領範囲

1. P6-1(GTPI) と P5-2(744 死因)、P5-1 同梱予定は研究線の選定として受領する。今便には proof artifact が無いので、定理候補の正否は **未監査**であり PASS を付けない。
2. 13-cell exact count は「走行中」という状態だけを受領する。5 時間という経過時間から存在・非存在を推論しない。完了/timeout/資源停止、事前登録宇宙、exit code、部分進捗を分け、現時点は UNKNOWN とする。
3. 裁定 352/349 の事故記録と係交代三段 protocol、LEDGER blind append 禁止を運用上の再発防止として受領する。数学的主張の PASS/FAIL 根拠には数えない。

---

## 最終ゲート

| 項目 | 今便の結論 |
|---|---|
| ASM 数学核 | **PASS** |
| ASM v2 artifact | **条件付き PASS**: W97-1.1、M2 語彙分離、CV-10 同期が必要 |
| conventions ledger v1.3 | **差戻し** |
| S2 累積 | **追認 PASS** |
| payload-era 個別 matrix | **PASS** |
| payload-era composition | **差戻し** |
| telemetry-only | **継続許可** |
| W6-KEY 設計 | **点ごと AQP/root-rank 方式を採択、実装 draft を許可** |
| W-6 closure | **OPEN** |
| positive-control harness | **条件付き先行実装許可** |
| calibrated detector / EP 発効 | **不許可、`uncalibrated/UNKNOWN` 維持** |
