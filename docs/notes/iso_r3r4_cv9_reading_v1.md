# ISO-GATE route-2 R3/R4 CV-9 仕様同一性判読書 v1(副検問)+ M-ISO-2 計画監査

- **判読者**: falsifier(反証前哨・opus/max)/ 2026-08-05 / 司令塔委嘱(裁定 529)
- **対象**: GAP driver(`iso_gate_r3r4_driver.g`)と Python 第二系統(`r4_second_system.py`)が 3 対象(K⁽³⁾・W-5・M-ISO-2 witness)で全数値一致したことの、cross-checked 格付け直前の判読。
- **種別**: **副検問(CV-9-2)のみ**。**主検問(CV-9-1・IF-FIRST 凍結時・計算前)は本件では実施されていない** — repo 内に本 pair の IF-FIRST 凍結文書は存在せず(`docs/状態.md` の言及のみ)、両実装の `conventions_used` 予定値の事前宣言もない。制度の主眼(無駄な計算が走る前に仕様齟齬を殺す)は本件では働いていない。
- **スコープ**: 任務 1 は「同一対象か」の一点のみ。任務 2(M-ISO-2 計画監査)は司令塔が別途明示委嘱した**計画監査**であり、CV-9 スコープ制限の対象外として §4 に分離した。
- **格付け(cross-checked 付与)は職掌外** — 本書は判読結果のみ。

---

## 0. 非当事者性の申告と provenance

1. **関与の申告**: 判読者は GAP driver・Python 第二系統・r4 データ受け渡し設計・cert のいずれの実装にも**関与していない**。§5.3/5.4 の設計起草にも、裁定 529 の起案にも関与していない。
2. **参照 artifact(本判読時に自分で再計算した SHA-256)**:

| 役割 | path | sha256 |
|---|---|---|
| GAP driver | `search/probe/w6_bu_s0/iso_gate_r3r4_driver.g` | `f1d5789bc53696d0ce191b9068ed0e1bed1ae99e507c10c0457eb0e3837b73b2` |
| Python 第二系統 | `search/probe/w6_bu_s0/r4_second_system.py` | `c98e5088f4f443828f7690235b20a78c31e9a814b3242635b7a7e49af2437870` |
| 受け渡しデータ | `search/probe/w6_bu_s0/r4_input_data.json` | `1f4e66c4cd498f54139472107d49c7a5a49ab7e4bdd69423f8f1541f7db37fb3` |
| 第二系統 出力 | `search/probe/w6_bu_s0/r4_second_system_output.json` | `7e5cc7f8afd31293b32fb2f4c779ba114a9177487d14b8eeb936db1beb196f40` |
| cert | `search/certs/w6_bu_s0_iso_gate_r3r4_20260805.json` | `32e07558cd7e05ada296cae160ac186d1557ad1992a4da1438a27cf2dbad83b8` |
| 共有 helper(参照のみ) | `search/week3-battery-common.g` | `aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998` |
| 仕様 | `docs/notes/w6_bottomup_design_v4.md` | `63438960dcd638e289d1e82c74cc86de4c8757029fa276fa27a03404b1a91c6a` |
| 意味論 | `docs/notes/auto_settled_check_v1.md` | `283145a169d01ed137d0daf1998027aa985e3b80f4f0489f4063b6339bac061e` |
| 規約台帳 | `docs/notes/conventions_ledger_v1.md` | `38b5c977fd2559120d1c9e69e0c14d32335012593d3dc870e6511ef8f53fd958` |

3. **判読者自身の第三実装**(両系統の helper を一切共有しない Python 独立実装。scratchpad 内・対象ファイルは無改変):
   `cv9_probe.py`(BFSWords 規約の逐語複製・witness 同定・hexagon 全段再現)、`cv9_probe2.py`(規約反転不変性・変異体生存判定)。

---

## 1. 三値裁定

# **同一対象 — ただし `verdict` の 1 量のみ「別対象」**

| 比較量 | 裁定 | 根拠 |
|---|---|---|
| `\|G\|` | **同一対象** | 両側とも生成元 x,y からの閉包。GAP `Size(Group(x,y))` / Python BFS 閉包。 |
| `N_ord` | **同一対象** | 両側とも `Lcm(Order(x),Order(y))`、charming set も同一述語 `gcd(2m+1,N)=1`。 |
| `shadow_total` | **同一対象** | 列挙域 D=[G,G]・hexagon (3.10)/(3.11)・SURJ の 3 段が逐条一致(§2)。判読者の第三実装も同値(12 / 80)。 |
| `settled_count` / `total` | **同一対象** | `GroupHomomorphismByImages`≠fail ∧ `IsBijective` と、Python の BFS 矛盾検出 ∧ 像位数=\|G\| は同一の数学的事実(§2.4)。 |
| `verdict` | **別対象** | **GAP は 3 変数関数 `ComputeVerdict(shadowSumOk, total, settled)`、Python は 2 変数関数(`shadow_sum_check` gate を持たない)**。差が出る入力(sum-check 不整合)が比較対象の 4 fixture に一度も現れないため一致しているだけ(【重大 2】)。 |
| M-ISO-2 witness の部分群位数 | 同一対象**だが** | 比較しているのは「GAP が dump した置換 f」についての事実のみ。「その f が `f_word` の列挙候補である」という結び目は**設計上 cross-check から除外**されている(【重大 3】)。 |

**この「同一対象」の証拠は、既存 artifact の自己申告ではなく判読者の原典読解と第三実装によって成立している。** 数値一致それ自体には規約同一性を判別する力が**ゼロ**であることを §3【重大 1】で機械的に示した。格付け文はこの事実を反映すること。

---

## 2. 規約の逐条突合(同一対象と裁定した根拠)

### 2.1 `AbstractProd` の反転規約 — Python 側の主張は原典から正しい

`week3-battery-common.g:47-54` の実体:

```gap
AbstractProd := function(list)
  val := list[1]^0;
  for i in [Length(list), Length(list)-1 .. 1] do  val := val * list[i];  od;
```

添字降順ゆえ `AbstractProd([a,b,c]) = c*b*a`(GAP 積順)。Python の module docstring の主張は**原典どおり**。各使用箇所の突合:

| 箇所 | GAP | 実体(GAP 積順) | Python | 判定 |
|---|---|---|---|---|
| z | `AbstractProd([x,y])^-1` | `(y*x)^-1` | `invert(compose(Y,X))` | 一致 |
| (3.10) | `AbstractProd([f,θf])=1` | `θf*f` | `compose(thetaf,f)` | 一致 |
| y^m f | `AbstractProd([y^m,f])` | `f*y^m` | `compose(f,ym)` | 一致 |
| (3.11) | `AbstractProd([τ²,τ,ymf])=1` | `ymf*τ*τ²` | `compose(compose(ymf,t1),t2)` | 一致 |
| genB | `AbstractProd([f^-1,y^u,f])` | `f*y^u*f^-1` | `compose(compose(f,Yu),finv)` | 一致 |

**残存の規約バグは発見できなかった**(実装係が捕った 2 件の外に第 3 の齟齬は見当たらない)。

### 2.2 語規約(裁定 166 prepend)— 修理は正しく、witness は本物

`BFSWords`(:169-189)は `nv := g.gap * cur`(左乗)で語を**末尾に append** ⟹ 語 [w₁..w_k] は積 `w_k*…*w₁` を表す。`EvalWordInQ`(:649-657)は `val := g^e * val` を左から適用 ⟹ 同じく `w_k*…*w₁`。**両者は整合**し、`EvalWordQT`(:192-200、`val := val * g^e`)は整合しない。driver の修理(EvalWordQT→EvalWordInQ)は正しい。

判読者の第三実装で BFSWords を逐語複製し確認:

- `f_word = [y,x,y,x]` の真の BFS 元 = **(7,9,8)** = dump された `f_images` と**一致**。`EvalWordInQ` による再構成も (7,9,8) で**忠実**。
- その (m=0, f=(7,9,8)) は K⁽³⁾ の実列挙中の **h11_fail 候補**であり、`|<x, f y f^-1>| = 36 < 108` も再現。
- ⟹ **witness は捏造ではなく実在の列挙候補**(cert の主張どおり)。

**軽微 1**: driver 内コメント(:290-296)は「EvalWordInQ→(7,8,9)、位数 108」と書くが、これは**修理前の別の語 `[x,y,x,y]`** についての記述で、cert が dump する語 `[y,x,y,x]` の話ではない。判読者は最初これを矛盾と読んだ。**どの語についての記述かを明記されたい**(§2 の再現でどちらも整合することは確認済み)。

### 2.3 列挙域

GAP `D := DerivedSubgroup(G)`、`Dwords` = BFS 順の D の元。Python `derived_subgroup` = 全対の交換子 `g^-1h^-1gh` の閉包。**同一部分群**(判読者の第三実装で |D| = 27(K⁽³⁾)/ 250(W-5))。charming set も同一。

**要修正 1**: `|D|`(GAP の `dwords_count`)は cert にも `r4_input_data.json` にも出力されておらず、Python は計算するが比較しない。**列挙宇宙そのものの大きさが cross-check の対象外**。

### 2.4 theta/tau の「矛盾検出」— 同一の数学的事実

GAP `GroupHomomorphismByImages(G,G,[x,y],[a,b]) = fail` ⟺ 割当 x↦a, y↦b が G の全関係式を満たさない。Python `build_hom_with_check` は Cayley グラフ BFS で像を伝播し、同一の域元に 2 通りの像が来たら False。**両者は「割当が準同型に延びるか」という同一の事実の検査**。`IsBijective` と「像位数 = \|G\|」も有限群上で同値。theta(x↦y,y↦x)・tau(x↦y,y↦z)の割当も同一。**同一対象。**

(Python の `INCOMPLETE: BFS did not cover all of G` 分岐は G=⟨X,Y⟩ ゆえ到達不能な死枝。無害。)

### 2.5 受け渡しデータに「答えを写せる隠れ経路」はあるか

`r4_input_data.json` は生成元 raw dump **だけではない** — GAP の結論 `expected_g_size / expected_n_ord / expected_shadow_total / expected_settled_count / expected_settled_total / expected_verdict / expected_subgroup_size(_lt_g)` を含む。ただしコード読解の結果、**これらは `assert` の右辺と `print` にしか現れず、計算の分岐には一切使われていない**(構造的入力として使われるのは `n_points` と、witness 源を選ぶ `source.startswith("K")` のみ)。**自動的な写しの経路はない。**

**要修正 2**: ただし方式は「先に計算 → GAP の答えに assert」であり、**不一致時は例外で停止 → 出力 JSON が生成されない**。出力の `all_crosschecks_pass: true` は Python リテラルで、成功時にしか書かれない。**出力ファイル単体には識別力がなく**、入力ハッシュも記録されていない。加えて Python の規約選択(反転)は docstring 自身が認めるとおり **R4 突合の不一致を追う過程で GAP 出力に合わせて決定**された。原典読解の結果その選択は客観的に正しい(§2.1)が、**独立性は「別々に作って突合」ではなく「合わせ込み」に近い**。

---

## 3. 発見(重大/要修正/軽微)

### 【重大 1】数値一致は規約同一性を一切判別しない(機械的に実証)

判読者の第三実装で、`AbstractProd` を(a)実際の反転規約、(b)素朴な紙面順、の**両方**で全段を再計算した:

| fixture | 規約 | \|D\| | candidate | h10 | h11 | genfail | shadow | settled |
|---|---|---|---|---|---|---|---|---|
| K⁽³⁾ | 反転(実装) | 27 | 108 | 72 | 24 | 0 | 12 | 12 |
| K⁽³⁾ | 素朴(紙面) | 27 | 108 | 72 | 24 | 0 | 12 | 12 |
| W-5 | 反転(実装) | 250 | 4000 | 3200 | 720 | 0 | 80 | 80 |
| W-5 | 素朴(紙面) | 250 | 4000 | 3200 | 720 | 0 | 80 | 80 |

**全段の値が完全に同一。** ⟹ 仮に GAP が反転規約・Python が素朴規約で走っていても、比較 5 量は全て一致した。**CV-9 が捕らえるべき当の齟齬に対し、本件の観測量は識別力ゼロ**である。同一対象という裁定は数値一致からではなく、判読者の原典読解(§2.1)からのみ出ている。**格付け文で「数値一致が規約同一性を裏づける」と読めてはならない。**

付随して、Python docstring の「D は逆元閉なので集計量は反転に不変」という**未証明の主張は、この 2 fixture については経験的に確認された**(証明ではない)。

### 【重大 2】`verdict` は両側で別の関数 — かつ GAP 側の修理(1)が第二系統に存在しない

- GAP `ComputeVerdict(shadowSumOk, total, settled)`:`shadowSumOk=false → UNKNOWN(CANDIDATE_ENUM_INCONSISTENT)` を最優先。
- Python(`r4_second_system.py:259`):`"TRUE" if settled==total and total>0 else ("UNKNOWN" if total==0 else "FALSE")` — **sum-check gate を持たない**。すなわち**修理前の旧 driver と同じ意味論**。

さらに Python は `candidate_total` も sum-check も計算しない。加えて **`h10_fail` の数え方が両側で違う**(GAP は (f,m) 対ごと=72、Python は f ごと=18。Python 自身が print で認めている)ため、GAP の恒等式 `candidate_total − h10 − h11 − genfail = shadow_total` は Python の帳簿では**そもそも成立しない**(108−18−24−0=66≠12)。

⟹ **verdict の入力集合のうち `shadowSumOk` は第二系統に対応物がなく、cross-check の外**。M-ISO-5 はまさにこの gate を突く変異体だが、これも純スカラー(§4)。

### 【重大 3】settled 述語の**偽側**は、両系統のどの実行経路でも一度も走っていない

実行された 4 fixture の内訳:K⁽³⁾ 12/12、W-5 80/80、N5-control は precondition で settled 未実行、Q3-a は theta/tau fail で settled 未実行。⟹ **`settled = false` を返す分岐(および Python の像位数 < \|G\| 分岐)は、全走行を通じて一度も実行されていない。**

機械的帰結(判読者が確認):`SettledCheckGeneral` の述語を **`settled := true` に固定した変異体は、R3 マトリクス 7 件と R4 突合の全期待値を満たしたまま生存する** —

| 変異体下での結果 | M-ISO-1 | M-ISO-2 | M-ISO-4 | M-ISO-5 | M-ISO-6b |
|---|---|---|---|---|---|
| 出力 | TRUE | FALSE | FALSE | UNKNOWN | UNKNOWN |
| 期待 | TRUE | FALSE | FALSE | UNKNOWN | UNKNOWN |

R4 の Python 側も同じ全 settled fixture 上で 12 / 80 を独立に得るため、**第二系統もこの変異体を殺せない**。M-ISO-7(source-map)は列挙側の汚染しか見ておらず、この変異は検出範囲外。

**すなわち「checker に陰性検出力がある」ことは、本 artifact 群のどの実行によっても示されていない。**

**安価な閉じ方(判読者が数値で確認済み)**: dump 済み witness (m=0, f=(7,9,8)) を実際に settled 検査へ通せばよい。判読者の独立計算では **hom は well-defined に構成され、像位数 36 ≠ 108 ⟹ IsBijective 偽 ⟹ settled=false** となる。両側 1 行ずつの追加で【重大 3】は閉じる。

### 【要修正 1】列挙宇宙 `|D|` / `candidate_total` が cross-check の対象外(§2.3)

### 【要修正 2】第二系統の出力に識別力・provenance がない(§2.5)。加えて出力 JSON と module docstring が自身のパスを `scratchpad/r4_second_system.py` と誤記(実体は `search/probe/w6_bu_s0/`)。

### 【要修正 3】CV-3(規約台帳)が要求する層ごとの向き宣言が、両 cert に存在しない

規約台帳 `conventions_ledger_v1.md` **CV-3**:「語の評価向きは層ごとに宣言し、突き合わせる層の間で一致させる」。本件では GAP cert が `group_side` / `enumeration_domain` を宣言する一方、**積・語の評価向き(AbstractProd 反転・BFSWords prepend)はどちらの cert にも宣言されていない**。第二系統 cert は `group_side` / `enumeration_domain` すら持たない。⟹ **副検問の機械 diff が原理的に実行できない**。本判読が全て手作業になった直接の原因。**両 cert に `conventions_used`(積順・語順・列挙域・group side)を追加されたい。**

### 【軽微 1】driver コメントの語の取り違え(§2.2)

### 【軽微 2】CV-6(反準同型・逆順の積)と `AbstractProd` 反転の関係が未整理

Python docstring 自身が「紙面の `f^-1 y^u f` ではなく実際は `f y^u f^-1`」と記す。**両系統が同じ物を計算していること(=CV-9 の問い)は成立**するが、**それが正典の物かは本 cross-check の射程外**であり、【重大 1】より数値からは永久に分からない。**Sol / 数学者の領分として司令塔へ返す**(判読者はこれ以上展開しない)。

---

## 4. 任務 2: M-ISO-2 構成の計画監査

### 4.1 混入 witness は checker の実経路を通っているか — **通っていない**

GAP(:337-345)・Python(:329-336)とも、実際の処理は:

```
mIso2ShadowsTotal := realShadowsTotal + 1;   # 13
mIso2SettledCount := realSettledCount;       # 12
mIso2Verdict := ComputeVerdict(true, 13, 12) # -> "FALSE"
```

**witness は shadow リストに入らず、`SettledCheckGeneral` に渡されず、hexagon にも SURJ にも settled にも触れない。** 混入は checker の**下流・カウンタ層**で行われている。「手前の自明な位置で落ちている」のではなく、**checker を一度も通らずに終端比較器だけが動いている**。Python 側に至っては `run_fixture` の verdict 関数すら使わず、`"FALSE" if 12 < 13 else "TRUE"` を別途書いた**恒真式**であり、cross-check としての情報量はゼロ。

なお §5.3 の事前登録は M-ISO-4 を「1 個の shadow を non-settled に**差し替え**」、M-ISO-5 を「列挙から shadow を 1 個**落とす**」と**データ/経路層の変異**として書いている。実装は 5 件(M-ISO-2/3/4/5/6b)すべてを**スカラー層の変異**に置換した。7 件中 5 件が、10 行の純関数 `ComputeVerdict` のみを叩いている。

### 4.2 内部矛盾:M-ISO-2 は自らが追加した修理(1)を手で迂回している

K⁽³⁾ の実測は `candidate_total=108, h10=72, h11=24, genfail=0` ⟹ `108−72−24−0 = 12`。混入後の `shadow_total=13` に対し sum-check は **12≠13 で false**。すなわち**この datum が実際に生じたなら、修理(1)により verdict は FALSE ではなく UNKNOWN(CANDIDATE_ENUM_INCONSISTENT)になる**。M-ISO-2 が FALSE を出すのは、`ComputeVerdict` の第 1 引数に `true` を**手で渡して sum-check を迂回している**からのみである。

M-ISO-5(12→11)は同型の摂動に対し正しく UNKNOWN を要求している。**同じ種類の摂動に対し M-ISO-2 と M-ISO-5 が矛盾する帳簿処理をしている。**

**安価な修理**: witness を「h11_fail バケツから shadow バケツへ移す」形(`h11_fail: 24→23`, `shadow_total: 12→13`)で構成すれば `108−72−23−0 = 13` と整合し、sum-check を迂回せずに FALSE が出る。しかもその構成は「hexagon フィルタが誤って非 shadow を通した場合に settled 検査が捕まえるか」という**意味のある変異**になり、【重大 3】も同時に閉じる。

### 4.3 M-ISO-3(constant-TRUE)の kill 証拠として 12+1 は十分か — **部分的にのみ十分**

- `ComputeVerdict` 内の constant-TRUE:**殺せる**(M-ISO-2 は実際に `ComputeVerdict` を呼ぶので、常時 TRUE 化すれば `mIso2Ok` が落ちる)。
- `SettledCheckGeneral` 内の constant-TRUE(`settled := true`):**殺せない**(【重大 3】の表で実証)。
- 列挙器内の constant-TRUE:M-ISO-7 の source-map で**テキスト的にのみ**カバー。挙動としては未カバー。

なお M-ISO-3 自体は `constantTrueMutantVerdict := "TRUE"` というリテラルと実 verdict の文字列比較であり、変異体を走らせてはいない。`ComputeVerdict` 由来の感度は持つが、それ以上ではない。

### 4.4 「h11-fail 候補は定義上そもそも shadow でない」ことは陰性 fixture の意味を弱めるか — **弱める**

witness (m=0, f=(7,9,8)) は判読者の再現で **h11_fail 段**の候補、すなわち hexagon (3.11) を満たさず**定義上 GT-shadow ではない**。したがって混入後の datum「K⁽³⁾ の shadow が 13 個」は**数学的に存在し得ない対象**である。

**この fixture が検査しているものの特定(一文)**:

> **M-ISO-2 が検査しているのは「報告された shadow 件数と settled 件数が食い違うとき終端比較器 `ComputeVerdict` が TRUE を返さない」という配管の性質だけであり、shadow 性・hexagon・SURJ・settled 述語のいずれにも触れていない。**

⟹ cert の `m_iso2_construction_note` の一文 —

> "This is the campaign's first isolated=FALSE instance and is registered here as a permanent negative fixture"

は**是正されたい**。isolated=FALSE となる**対象(marked datum)は存在しない**(cert の `search_appendix` 自身が 5 族の探索で自然な例を見つけられなかったと正直に記録している)。ここにあるのは整数 2 個 (13,12) である。これを「初の isolated=FALSE 事例」として恒久 fixture 登録すると、将来の読者が数学的対象と誤読する。**「終端比較器の配管 fixture」として登録すべき**。

---

## 5. 判読の限界(正直な申告)

- 本判読は **K⁽³⁾ と W-5 の 2 fixture・K⁽³⁾ の witness 1 件**を第三実装で再現した範囲での読解。W-5 の witness 経路・N5-control / Q3-a の内部は再現していない。
- **§2 の逐条突合で「残存する規約不一致」は発見できなかった**。これは不在の証明ではない — 特に【重大 1】より、**この観測量の組では規約齟齬は原理的に検出できない**ので、「見つからなかった」の情報量は小さい。
- 数学的正しさ(反転規約が正典 (3.10)/(3.11) の意味かどうか、settled ⟸ hexagon+SURJ+有限性 という cert 記載の仮説)は**判読していない**(Sol / 数学者の領分・§1.3.4 スコープ制限)。【軽微 2】として 1 行で司令塔へ返す。
- 封印 3 量・Im R・705,894 宇宙は**非接触**。W-5 の `iso_gate_state` は **UNKNOWN のまま**であり本判読は触れていない。対象ファイルは**読み取りのみ・無改変**。
