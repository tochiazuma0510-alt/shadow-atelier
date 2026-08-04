# NF-972 CV-9 仕様同一性判読書 v1(副検問・格付け直前)

- **判読者**: falsifier(反証前哨・opus/max)/ 2026-08-04 / 司令塔委嘱(裁定 456 後)
- **対象**: 屋根 M = K⁽⁹⁾∩N_{S₄} の |GT(M)| = 972 について、source map A(python・fiber-product)と source map B(GAP・直接悉皆)の NF tuple 集合が第 3 回突合で集合等号したこと。
- **判読の種別**: **副検問(CV-9-2)** — 値の一致後・cross-checked の印の前。主検問(CV-9-1・IF-FIRST 凍結時)は本件では実施されていない(凍結 v1 は裁定 434、CV-9 主検問の制度化は同 2026-08-01 だが本件に主検問の記録はない)。
- **スコープ(§1.3.4 遵守)**: 「**同一対象か**」の一点のみ。仕様の数学的正しさ・実装レビュー・追加テストの発案・計画監査には拡大しない。

---

## 0. 非当事者性の申告(§1.3.3)

1. **関与の申告**: 判読者は本件の**凍結仕様(nf972_freeze_v1.md v1/v1.1/v1.2)の起草に関与していない**。**source map A / B のいずれの実装にも関与していない**。**第 1〜第 3 回突合(一次 grading)にも関与していない**。裁定 434/442/449/454/455/456 のいずれにも起案・裁定として関与していない。
2. **参照した provenance(全て本判読時に自分で再計算した SHA-256)**:

| 役割 | path | sha256 |
|---|---|---|
| 凍結仕様 | `docs/notes/nf972_freeze_v1.md` | `d9fa2d66ee14ecc8da8362b510d0c54894bf0dd42a743db61942ae52158910d1` |
| 規約台帳 | `docs/notes/conventions_ledger_v1.md` | `38b5c977fd2559120d1c9e69e0c14d32335012593d3dc870e6511ef8f53fd958` |
| factor cert K9 | `certificates/K9.v1.json` | `ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e` |
| factor cert S4 | `certificates/S4.v2.json` | `c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d` |
| A 実装 | `search/probe/wac_v1/nf972_sourcemap_a_driver.py` | `eeffc2ddfc58462871801f5809a0fd627066025ba7d6abcfad333a4b995a14b1` |
| A cert | `search/certs/nf972_sourcemap_a_v2_20260804.json` | `33a74c342052b5635e9438bcdf7e36fb0e17b16d23138ab260f296d4c0ece2e1` |
| A tuples | `search/certs/nf972_sourcemap_a_tuples_v2_20260804.json` | `cfa1f3a917e2cd9d21ceaa7f77539633ccb22e8585da8b3248609008d0391801` |
| B 実装 | `search/probe/wac_v1/nf972_sourcemap_b_run.g` | `1f0ce8fb3c451968d1731997457d70033b2d466c39fc1529ee7e1de59d7710d3` |
| B cert | `search/certs/nf972_sourcemap_b_20260804.json` | `bb363303441844ba3c5518345b5b6aa779bd57bb849f407874e6dadcbb03d677` |
| B tuples v3 | `search/certs/nf972_sourcemap_b_tuples_v3_20260804.json` | `8cd10f3a471b3dbae0c8db4961e81f7b4ca22330a51a9337d4e6d2430968254a` |
| 第四者比較器 | `search/probe/wac_v1/nf972_crosscheck3.py` | `f7f81431c034bed9e5524cb6f22bf67cef96c4a322ad023a0f8ee5adc88e405c` |
| 枠定義(参照のみ) | `search/week3-psl-common.g` | `de5d8d6d107959d7d7b8e40bbe4dcb07a8163a56660877bf2e0ec5b5ccc07a18` |
| 枠定義(参照のみ) | `search/week3-battery-common.g` | `aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998` |

**A cert の自己申告 digest は全て実物と一致**(spec_ref・K9・S4・canonical_enumeration・effective_source_chain 4 件)。B cert の `script_sha256` も実物と一致。

---

## 1. 三値裁定

# **PASS(同一対象)**

**ただし** — この PASS は**判読者自身の独立検算によって成立**しており、**両 artifact の自己申告だけでは判定不能だった**。理由は §3【重大 1】(B の義務自己検査が実質トートロジー)と §3【要修正 1】(A の分離 fixture が can₄ 軸を一度も動かさない)である。すなわち **「同一対象」の証拠の一部は判読者が新たに作った**ものであり、既存の cert に元からあったものではない。この事実を格付け文に反映すること。

### 1.1 「同一対象」の正確な意味(誤読防止)

A と B は**同一の写像を同一の universe に適用してはいない**。凍結仕様 §2 の設計どおり:

- **A の universe** = K9 cert 108 行 × S4 cert 54 行(互換 m mod 9)の fiber-product = **予測 route**。
- **B の universe** = 屋根 M の直接悉皆(m ∈ Mcharm 12 値 × D(GM) 367416 元 × hexagon 判定)= **実測 route**。

裁定に係る「同一対象」とは **両者が写す先の像集合(NF tuple 集合)が同一対象である**ことであり、「同一写像」ではない。格付け文で「二実装が同じ計算をした」と書かないこと。

---

## 2. 判読の焦点 5 点に対する所見(全て実物で確認)

### 焦点 1: 三成分は同じ数学的対象か

**m₀**: 両側とも **mod 18**(M_ord = Lcm(Ord(XM),Ord(YM)) = 18・K9 の N_ord = 18)。charming set は両側とも同一の 12 値 `{0,2,3,5,6,8,9,11,12,14,15,17}`(実 artifact から確認)。S4 側は m mod 9 でのみ参照。**一致**。

**can₉**: 両側とも D₉³ の (a,ε) 三つ組・成分順固定。A は K9 cert の `f_triple` を**そのまま複写**(A 側に計算はない)。B は自構成 `MakeDn(9)` の r,s で `r^a·s^ε` 正規形へ分解し、**集合水準で K9 cert と逐語一致**を script 内で fail-closed 検査済み(`dictK9OK`)。
判読者の独立検算 — K9 cert の 108 行集合は、**a ↦ k·a mod 9 の 6 通りの単位倍のうち k=1 でのみ不変**(k=2,4,5,7,8 は全て集合を変える)。よって回転生成元 r の取り方は**剛的に pin されており**、B の恒等辞書は無内容ではない。**一致**。

**can₄**: 両側とも「S4.v2.json の `marking`(S=[[1,0],[1,1]], T=[[4,3],[1,5]])から X:=w², Y:=S⁻¹XS(w:=S·T⁻¹)で作った 9 点置換表現上の one-line」。
- **P¹(F₈) 点列挙規約の同一性を code 水準で確認**: A の python `gf8_add/gf8_carryless_mul/gf8_reduce/gf8_inv/mat_to_perm_gf8` は `search/week3-psl-common.g` の `XorInt/GF8CarrylessMul/GF8Reduce/GF8Inv/MatToPermGF8` の**逐語再現**(index 1 = ∞、index 2+x for x∈GF(8)、a₀+2a₁+4a₂ 符号化、x³+x+1)。X,Y 構成も同 L273-277 の GAP ネイティブ形と同一。
- **判読者の独立第三評価**: A/B いずれのコードも import せず、GAP ソースの規約だけから GF(8)・MatToPermGF8・AbstractProd を書き下ろし、S4.v2.json の 54 f_word を評価 → **B の (m₀ mod 9, can₄) 射影 54 件と完全一致**。
**一致**。

### 焦点 2: 乗算規約(f/f⁻¹ 事故族)

- GAP `AbstractProd(list)`: `val:=id; for i in [k,k-1..1] do val:=val*list[i]; od`(全項反転)。A の python `abstract_prod` は**同一の反復順・同一の合成向き**(`perm_compose(p,q)` は GAP `p*q` = i^(p*q)=(i^p)^q)で、**逐語再現**。空語は両側とも恒等。
- **A5-CONV fixture は両側 PASS だが「実質同一の検査」ではない**: A の A5-CONV は S5 の別生成元での**方向 fixture**、B の conv fixture は Xperm,Yperm/g9.x,g9.y の**非可換性を使った方向 fixture**。どちらも方向を pin するが、A の A5-CONV は A の GF(8)/点列挙 pipeline を**一切通らない**(S5 の巡回置換直書き)。
- **代替として判読者が識別力を実測**: 反転規約を捨てた誤規約(非反転)で S4 の 54 語を評価すると、B の 54 射影との**対称差 96/108**。すなわち**この接合部は規約に対して鋭敏**であり、A=B の一致は規約盲目ではない。**一致・かつ識別力あり**。

### 焦点 3: 第四者比較器の正規化

`nf972_crosscheck3.py` は A 側に `a%9, e%2`、B 側に `v%9, v%2` を掛ける。判読者が**正規化を一切掛けずに**両集合を突合した結果 **972/972 で集合等号が成立**(a の実値域は両側とも 0..8、ε は**両側とも全行 0**、m₀ は 12 値のみ)。よって **mod は情報を潰していない(可逆・無害)**。m₀ には mod を掛けていないので法の軸も潰れていない。**問題なし**。
ただし §3【軽微 1】参照(射影 assert の論理的冗長)。

### 焦点 4: 分離 fixture は両側で同じ変異か

| 仕様 §4 | A の実装 | B の実装 | 同一か |
|---|---|---|---|
| ① 向き反転(f↦f⁻¹) | `can9` の a ↦ −a mod 9(**can₄ は不動**) | 実 f ↦ f⁻¹(can₉・can₄ 双方が動く) | **部分的にのみ同一** |
| ② 片側 generator swap | `can9` の成分順 (1,2,3)→(3,2,1)(**q₉ 側**) | 屋根 GM2 を再構築し **q₄ 側** X↔Y を入替えて再悉皆 | **別の変異** |
| ③ m の法の誤り | m₀ = m mod 9 | m₀ = m mod 9 | **同一** |

仕様 §4-2 は「q₉ **or** q₄」と書いているので**文言上はどちらも適法**。しかし発火の意味は同一ではない(§3【要修正 1】)。

### 焦点 5: 972/108/54 は期待値ハードコードで通過を作っていないか

- **A**: 全 `chk()` は**計算値と期待値の突合**であり、生成には使っていない(`BASELINE_LIST` は fiber-product の実列挙)。ただし `len(BASELINE_LIST)==972` は入力件数 108×9 から**代数的に自明**で、独立情報を持たない。
- **B**: `Length(resM.shadows) <> 972 → Error` は **fail-closed gate**(fail-open ではない)。ただし帰結として **B の cert は shadow_total ≠ 972 では存在し得ない** — cert の 972 は「観測の記録」であると同時に「cert 存在の前提」である。cert の不在 ≠ 走行の不在。格付け文で「B が独立に 972 を観測した」と書くなら、走行ログ側の証拠を併記すること。
- **「重複 0」は両側とも自動**: B の NF は (m,f) の可逆な再符号化(f ∈ GM ≤ Sym(27)×Sym(9) は 2 ブロック制限で決まる)なので単射は構成上自明。A も rectangle 構成から自明。**§3-1 の「重複 0」は検査ではない**。

---

## 3. 所見(タグ + 根拠)

### 【重大 1】B の「非トートロジー形」義務自己検査は実質トートロジーである(仕様 v1.2 §7-6 未履行・cert の自己記述が偽)

仕様 v1.2 §7-6 は「σ(P_B(f)) = P_cert枠(f) を、**cert 枠評価(右辺)と自表現評価+σ(左辺)の別経路突合**で確認」を義務づける。実物:

- B は `Smat := MakeMatGF8(1,0,1,1)`・`Tmat := MakeMatGF8(4,3,1,5)` を**ハードコード**し、cert 枠も**同じ関数で同じ行列**から再構成する。実測値: `xperm_cert_equals_xperm = true`・`yperm_cert_equals_yperm = true`・`sigma_gap_repr = "()"`。
- 従って自己検査 `lhs := sigma*WordEval(w,Xperm,Yperm)*sigma^-1` と `rhs := WordEval(w,Xperm_cert,Yperm_cert)` は**同一関数・同一引数の同一式**。`rows_pass 54/54` は **WordEval にどんな規約バグがあっても 54/54 になる**。
- B v3 tuples の cert 注記は「**非トートロジー形(v1.2 §7-6)**」と自称するが**偽**。これは事故台帳 #6(裁定 319・識別力ゼロの dummy)および裁定 454 が潰したはずのトートロジーの**同一ワークストリーム内 2 回目の再発**である。
- **傍証**: `nf972_sourcemap_b_tuples_20260804.json`(v1)・`_v2_`・`_v3_` の `tuples` 配列は**逐語同一**、canonical sha も 3 版とも `932a0f36bc7a3ca81cb5dcc285d5f9c0d85d17bbff0d64f05c5e7dccdccc8db8`。**σ 機構は全て no-op**であり、第 2 回→第 3 回の実質的な修理は **100% A 側**(witness 誤用 → f_word 評価)だった。

**判読上の扱い**: B の枠が cert 枠と一致するという**事実自体は真**(判読者が marking 値と構成規約を突合して確認)。真であるのは**構成上の定義**によってであって、この自己検査によってではない。よって「同一対象」の裁定は覆らないが、**当該 flag(`dictionary_selfcheck.all_54_pass` / `rows_pass 54/54`)を証拠として引用してはならない**。

### 【重大 2 の手前・要修正 1】A の分離 fixture 3 種は can₄ 軸を一度も動かさない(CV-9-5 の識別力束縛が can₄ について未充足)

A の F1 = `flip_can9`、F2 = `swap_can9_13`、F3 = `wrong_modulus_m0` — **3 つとも can₄ を不動のまま**にする。すなわち A の登録済み competitor universe は、**v1.2 修理の対象そのものである can₄ 軸に対して識別力ゼロ**。A cert の `cv1_cv2_scope_note` は「S4 側(can4)…は A5-CONV fixture で識別力を実証済み」と書くが、A5-CONV は **S5 の別群・別生成元の方向 fixture** であり、A の `mat_to_perm_gf8` / X:=w² / Y:=S⁻¹XS pipeline を通らない。その pipeline の防御は `ord_S/ord_T/ord_w/ord_X` の 4 個の位数一致のみで、**位数は共役不変 = 点ラベル付け替えに盲目**である。

**判読者による代替実証**(これがなければ can₄ 軸は判定不能だった): 誤規約評価との対称差 96/108(§2 焦点 2)+ 独立第三評価 54/54 一致(§2 焦点 1)。**識別力は存在するが、それを示したのは cert ではない。**

### 【要修正 2】B cert が §3-3 の必須 3 点のうち 2 点を欠く

凍結仕様 §3-3 = 「cert に conventions_used(v1_6)・**出所 digest**・**DRIVER_DONE**」。
- `conventions_ver: "v1_6"` ✓
- **出所 digest: `script_sha256` のみ。凍結仕様の digest なし・入力(K9.v1.json / S4.v2.json)の digest なし・`effective_source_chain` なし** ✗
- **`driver_done` 欄が cert JSON に存在しない**(標準出力に `NF972_SOURCEMAP_B_DRIVER_DONE` を印字するのみ)✗
- 規約台帳 §2 の `conventions_used` schema に対し、B は自由文 4 欄のみ(`comparison_target`・`separation`・`chi_P_criterion`・`roundtrip_witness`・`effective_source_chain`・`level` を欠く)。§2 は「新規 cert から適用」なので本 cert に適用される。
- **stale な欄名**: `q4_projection_matches_s4_cert_witness_verbatim_after_sigma` — **裁定 454 で廃止された「witness 逐語照合」基準**の名を残したまま、値は別物(σ 別経路突合の結果)を入れている。欄名が撤回済み基準を主張している。

（A cert 側は §3-3 の 3 点・§2 schema ともほぼ充足。ただし **`comparison_target`(CV-7・§2 必須型)は A にも無い**。）

### 【要修正 3】第四者比較の結果が cert 化されていない(CV-9-5 の「検問記録の束縛」未成立)

`nf972_crosscheck3.py` は cert を出力しない裸の script で、結果は LEDGER の散文にのみ存在する。CV-9-5 が要求する「**両 source / spec digest・target・competitor universe・識別力を持つ dummy fixture**」を束縛した記録が**どこにも無い**。格付け前に比較 cert を鋳造すること(必要な digest は §0 の表で全て提供済み)。

### 【軽微 1】比較器の射影 assert は論理的に冗長

`crosscheck3.py` L22-23 の 2 本の射影一致 assert は L21 の `SA == SB` から**論理的に従う**。「射影も一致した」を**独立した証拠として数えない**こと。加えて L23 は `(m₀ mod 18, can₄)` = 108 対を見ており、仕様 §3-2 が要求する **q₄ 射影 54** を検査していない(54 の検査は A・B が各自の cert 内で行っている)。

### 【軽微 2】pin されない規約自由度 2 件(集合水準の主張は影響を受けないが、再利用時の注意)

1. **ε ≡ 0**: 972 件・108 件のいずれも**全成分 ε = 0**(D₉ の交換子部分群 = 回転部分群 ⟨r⟩ による構造的帰結・B が script 冒頭で自己申告済み)。よって凍結仕様 §1 の「ε ∈ {0,1}」の**半分は一度も試されていない**。`r^a s^ε` と `s^ε r^a` の順序規約・反射 s の取り方は本データでは**原理的に判別不能**。
2. **ブロック 1↔2 の転置**: K9 cert の 108 行集合は**ブロック順 (1,0,2) の入替に対して不変**(判読者が実測。他の 4 通りの非自明置換は全て集合を変える)。A も同じ null を自 cert に正直に記録済み。よって B のブロック順規約は**この転置を除いてのみ pin されている**。像集合は不変なので**集合水準の主張は無傷**だが、「per-element の対応が一意に決まる」とは言えない。

### 【軽微 3】972 の集合等号が実際に買っているもの(格の過大評価を防ぐため)

判読者の実測: **B の 972 は各 m で完全な rectangle**(12 の m 全てで n=81・|can₉|=9・|can₄|=9)。A は構成上 rectangle。よって

> 集合等号 ⟺ (m 集合一致) ∧ (各 m の can₉ fiber 一致) ∧ (各 m の can₄ fiber 一致)

であり、can₉ fiber の一致は **B が script 内で既に K9 cert と突合済み**の項目の再掲。したがって第 3 回突合が新たに確立したのは実質 **(i) B の屋根像が m ごとに完全な直積(= 屋根の生成条件が Goursat 障害なく分解する)** と **(ii) B の屋根 q₄ 像が S4 cert の shadow 集合と一致する** の 2 点である。これは十分に非自明だが、「独立 2 系統が 972 点を各々別々に計算して全て一致した」という読み方は**強すぎる**。

---

## 4. 判読者が実行した独立検算(再現手順)

いずれも A/B のコードを import せず、GAP ソース(`week3-psl-common.g` の GF8*/MatToPermGF8、`week3-battery-common.g` の AbstractProd)の規約のみから python で書き下ろした。

1. **接合部の第三評価**: S4.v2.json の `marking` → S,T 置換 → w=S·T⁻¹ → X=w², Y=S⁻¹XS → `settled_detail` 54 行の f_word を AbstractProd 評価 → **B の (m₀ mod 9, can₄) 射影 54 件と完全一致**。
2. **規約識別力の実測**: 同じ評価を**非反転(誤)規約**で行うと B との**対称差 96**(集合サイズは同じ 54)。
3. **正規化の無害性**: mod を一切掛けずに A/B を突合 → **972/972 集合等号**。値域: a ∈ 0..8、ε ∈ {0}、m₀ = 12 値。
4. **can₉ 座標の剛性**: K9 cert 108 行集合は a↦k·a(k=2,4,5,7,8)・ブロック順 (0,2,1)/(1,2,0)/(2,0,1)/(2,1,0)・a↦−a の**全てで変化**。不変なのは **k=1 と ブロック順 (1,0,2) のみ**。
5. **universe の同一性**: S4.v2.json の `settled_detail` 54 行(m, f_word)は `generation_detail` の `pass:true` 54 行と**集合としても順序としても同一**。A の入力 universe に drift なし。
6. **B の 3 版の同一性**: `_b_tuples_`(v1)・`_v2_`・`_v3_` の tuples 配列は逐語同一・canonical sha も同一。
7. **A の python が GAP の逐語再現であること**の code 突合(GF8Add/CarrylessMul/Reduce/Inv・MatToPermGF8・AbstractProd・X,Y 構成)。

---

## 5. 格付けへの勧告(判読者の意見・採否は司令塔)

- **CV-9 三値 = PASS**(§1)。CV-9-3 の「PASS 以外では上げない」条件は満たす。
- ただし **CV-9-5(検問記録の束縛)は現状 未充足**。格付け前に最低限:
  1. 【重大 1】B cert / v3 tuples の「非トートロジー形」自称の**訂正 erratum**(CV-10 形)。当該 flag を証拠から外す。
  2. 【要修正 3】比較 cert の鋳造(A/B/比較器/凍結仕様の digest + comparison_target + competitor universe + 本判読書の digest を束縛)。
  3. 【要修正 2】B cert の出所 digest・`driver_done`・stale 欄名の補修(再走不要 — 追補 cert で可)。
  4. 【要修正 1】can₄ 軸を動かす分離 fixture を A 側へ 1 本追加(例: X↔Y 入替・点ラベル π による共役)。**判読者は §4-2 でその識別力を実測済み**なので、追加は記録の完備化であって数学の再確認ではない。
- **格の文言案**: 「**集合水準 cross-checked 候補**(予測 route × 実測 route の像集合一致・CV-9 副検問 PASS・記録束縛は §5 の 4 件を条件とする)」。**verified とは書かない**(Lean 予約)。**「二系統が 972 点を独立に計算して一致」とは書かない**(§3【軽微 3】)。
- **主検問(CV-9-1)の欠落**: 本件には IF-FIRST 時点の主検問記録が無い。今回の事故列(第 1 回 9/972・第 2 回 A=54/54 vs B=1/54)は、まさに主検問が殺すはずだった仕様齟齬である。**次案件から主検問を先に置く**ことを制度として推奨(本判読書の射程外・司令塔判断)。
