# CV-9 仕様同一性判読 — IH-NEC R4a / R4b(|GT(M)|=972・|GT(K⁽⁹⁾)|=108・|GT(N_S4)|=54)v1

- **判読者**: falsifier(反証前哨・opus/max)/ 2026-08-01 / 司令塔委嘱
- **規範**: `docs/notes/conventions_ledger_v1.md` §1.3(CV-9・便 94 F94-5.2 逐条)+ §1.3.9・CV-13(§1 表)+ §3(IF-FIRST)
- **状態札: candidate**(司令塔裁定待ち)。本稿は **CV-9 の三値裁定**であり、数学的正しさの監査ではない(§1.3.4 スコープ制限を遵守)

---

## 0. 判定(先に一枚)

| 対象 | 三値判定 | 一行根拠 |
|---|---|---|
| **\|GT(K⁽⁹⁾)\| = 108** | ★ **同一対象** | 受理式が**逐語同一のソース**・入力 universe が数値まで一致(8748 = 8748)・失敗状態の内訳まで再現 |
| **\|GT(N_S4)\| = 54** | ★ **同一対象** | R4b の S4 アンカーが入力 cert の `hexagon_free_certificate` を **5 欄すべて一致**で再現(3024/2640/330/0/54) |
| **\|GT(M)\| = 972** | ★ **同一対象**(対象の名指しは同一) | 両者とも命題 ROOF(4) の**同じ両辺**を指す。ただし下記【重大-1】 |

> ### ★ 判定に必ず添える 3 つの限定(これを外して引用してはならない)
>
> **【限定 A】972 は「二つの測定の一致」ではない。** R4b は屋根 M で直接悉皆列挙して 972 を**測定**した。R4a は M に一度も触れておらず、因子データに**命題 ROOF(4) を適用して 972 を算出**した(`docs/notes/ihnec_v1.md` 追補 C.4 が自ら明記)。⟹ 一致が支持するのは「**ROOF(4) の独立確認**」であって「独立二測定の合致」ではない。cross-checked の語をこの意味で使うなら、**格の内容を「予測(紙)× 測定(機械)の一致」と書くこと**。
>
> **【限定 B】108 / 54 の独立性は最小である。** R4b の受理式は、R4a の入力 cert を生成した実装の **逐語複製**であり、群の構成コード(`MakeGn`・PSL の marking)も同一ソースの複製である。⟹ **共有された規約誤りは両系統とも検出できない**(CV-13 の射程限定がそのまま適用)。
>
> **【限定 C】本判読は副検問のみの retrofit である。** CV-9-1 の**主検問(計算前)は実施されていない**(制度発足が両系統の設計より後)。さらに CV-9-4 の差戻し事由に該当する仕様変更が凍結後・実測前に 1 件ある(§6)。

---

## 1. 非当事者性の申告(CV-9 §1.3.3)

1. **関与の申告**: 本判読者は (a) R4a の python 実装 (b) R4b の GAP driver (c) 入力証明書 K9.v1 / S4.v2 を生成した GAP スクリプト (d) `docs/notes/ihnec_v1.md` の起草 (e) 裁定 385/387 の一次格付け — **のいずれにも関与していない**。本セッションで初めて全ソースを読んだ。
2. **参照した provenance**: §2 の digest 表がすべて。**本稿の数値は全て機械抽出**(手写しなし)であり、各値に取得元パスを併記した。

---

## 2. 参照した provenance(実測 SHA-256・2026-08-01)

| 役 | パス | SHA-256 |
|---|---|---|
| 凍結設計・予言 | `docs/notes/ihnec_v1.md` | `498b24ef9e907b0708c0915c36aa3e2a13bf07e63c753967e920d4731bfe663f` |
| 規範 | `docs/notes/conventions_ledger_v1.md` | `2705ffbbb98eeb3d24fdcf78455b5d33cf140b247c289010fd4bbd99bc38a75b` |
| **R4a 実装** | `scratchpad/ihnec_r4a_run.py` | `f8be65ae5bf1ed2b0a175bb88057e0fb1d36b9c790cd014ce1fa09eb9c88820b` |
| R4a 入力① | `certificates/K9.v1.json` | `ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e` |
| R4a 入力② | `certificates/S4.v2.json` | `c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d` |
| R4a 入力①の生成器 | `search/suite-wp2-explorer.g` | `2baf2adf157364b3a05d6a698da8509979f40bf134e52c97b38be0c099a68495` |
| R4a 入力②の生成器 | `search/week3-psl-S4.g` | `72cc07454d35d1d371d095f5fa6b0c7044bdd8b509d4bfeceaaa482b6479a9f7` |
| 同上・本体 | `search/week3-psl-common.g` | `de5d8d6d107959d7d7b8e40bbe4dcb07a8163a56660877bf2e0ec5b5ccc07a18` |
| **R4b 実装** | `search/probe/wac_v1/ihnec_r4b_run.g` | `5bf6bc551eb7309c0b83adc363c15985973d9cb04e2cde9e7e34fe45c5277aa2` |
| R4b 受理式の原本 | `search/week3-battery-common.g` | `aadf1afa5e1a171d10d0aa1f9657e823cad669b960e08da7b9e7618f2ea4f998` |
| R4b cert(ローカル・全 12 m) | `search/certs/ihnec_r4b_run_20260801.json` | `fdf5fd367cdd00e4aafde4d1ac4ef3708e6f3efd338f7b7945646879e0002fd2` |
| R4b cert(ローカル・m0) | `search/certs/ihnec_r4b_m0_20260801.json` | `c5b35555aa30d4059a1d261693196f90fc912f99a6ba85c6a605d7c30b4d921f` |
| R4b cert(CI・12 本) | `scratchpad/ihnec_r4b/mine-run-ihnec-r4b-roof-20260801-m*/mine/out/ihnec-r4b-roof-20260801/m*/ihnec_r4b_m*_20260801.json` | 12 本の `provenance.script_sha256` は単一値 `5bf6bc55…7aa2`(上の R4b 実装と一致) |
| R4b CI 実行ログ | 同上 `…/ci/out/run.log`(12 本) | run_id `30697198947` |
| 検収 | `mine/reports/ihnec-r4b-20260801_report.md` | `edf25b0537c2164602355134979e247277a7aa33dceebd12b6070ca59be801a5` |
| 計画(事前登録) | `mine/jobs/queue/ihnec-r4b-20260801.json` | `f568805dbab4f02c9044c3c3e915a180b43667fa1633d7c0331d3e45fb07a129` |

**digest 突合の結果**: 追補 C(R4a)が宣言する 3 digest、検収レポートが宣言する `script_sha256`、いずれも**本判読者の再計算と一致**した。出所の連鎖に断裂はない。

---

## 3. 逐条比較(CV-9-1 の 6 項目 × 3 量)

### 3.1 \|GT(K⁽⁹⁾)\| = 108 — **同一対象**

| # | 項目 | **R4a**(`ihnec_r4a_run.py` L20-23 経由・実体は `suite-wp2-explorer.g` L195-241) | **R4b**(`ihnec_r4b_run.g` L126-184) | 判定 |
|---|---|---|---|---|
| ① | 入力 universe | `gn := MakeGn(9)` → `D := DerivedSubgroup(gn.G)` × `Xn := Filtered([0..Nord-1], mm -> Gcd(2*mm+1,Nord)=1)`。cert `counts.raw_candidates = 8748` | `g9 := MakeGn(9)`(**同一ソースの逐語複製**)→ `Elements(DerivedSubgroup(G))` × `CharmingSetOf(18)`。CI 実測 `candidate_total=8748` | ★ **一致**(8748 = 8748・機械値) |
| ② | 比較対象 | 108 という**基数**(`len(K9['shadows'])`) | 108 という**基数**(`resK9.shadow_total`) | ★ 一致 |
| ③ | 同値関係 | (m, f) 組の**同一性**。`shadows` は 1 元 1 行(cert L: 108 行)。R4a は別途 Θ の単射性を 108 点で確認 | (m, f) 組の同一性。`Add(shadows, rec(m,f))` で候補ごとに 1 行 | ★ 一致(いずれも quotient を取らない生の組) |
| ④ | 正規形 (NF) | **無し**(基数のみを比較)。f のラベルは cert 側が `f_word`/`f_triple`、R4b 側は置換元 — **突き合わせていない** | 同左 | ⚠ **NF 不在**(§8【要修正-3】) |
| ⑤ | filter | `hex310 ∧ hex311 ∧ surj`(L224/L228/L234)。加えて `charmPass`(f∈D により恒真)・full hexagon double-check(Q×T モデル・cert `double_check_full_hexagon_fail=0`) | `hex310 ∧ hex311 ∧ surj`(L97/L102/L106)— **上と文字通り同一式** | ★ 一致(R4a 側に double-check が 1 段多いが、これは受理を**狭めない**追加検査) |
| ⑥ | 失敗状態 | cert は `hexagon_pass/charming_pass/surjective_pass` のみ(h10/h11 の内訳なし) | `h10_fail=7776, h11_fail=864, generation_fail=0`(CI run.log) | △ **粒度が非対称**(R4a 入力 cert に h10/h11 欄が無く、内訳の diff ができない) |

### 3.2 \|GT(N_S4)\| = 54 — **同一対象**

| # | 項目 | **R4a**(`ihnec_r4a_run.py` L64-68・実体は `week3-psl-common.g` `RunPSLWindow`) | **R4b**(`ihnec_r4b_run.g` L142-198) | 判定 |
|---|---|---|---|---|
| ① | 入力 universe | `Smat=MakeMatGF8(1,0,1,1)`, `Tmat=MakeMatGF8(4,3,1,5)`, `wPerm := Sperm*Tperm^-1`, `Xperm := wPerm^2`, `Yperm := Sperm^-1*Xperm*Sperm`(L273-277)× charming(9) | **同じ 5 行を逐語複製**(L147-151)× `CharmingSetOf(9)` | ★ **一致**(marking が文字通り同一・cert `marking` 欄とも一致) |
| ② | 比較対象 | 54 という基数 | 54 という基数 | ★ 一致 |
| ③ | 同値関係 | `settled_detail` は `result.shadows`(群元水準)を 1:1 で写す(`week3-psl-common.g` L373-387)⟹ 語の重複による二重計上は原理的に起きない | (m,f) 組の同一性 | ★ 一致 |
| ④ | 正規形 (NF) | 無し(基数のみ) | 無し | ⚠ NF 不在(3.1 ④ と同じ) |
| ⑤ | filter | **二層**: (i) `EnumerateReducedHexagon` の `hex310 ∧ hex311 ∧ surj` → `hexagon_free_certificate.shadow_total=54`;(ii) さらに `settled` = ∃h∈PΓL(2,8): h⁻¹Xh=X^u ∧ h⁻¹Yh=f⁻¹Y^u f → `settled_count=54`。**R4a が `\|GT(N_S4)\|=54` を assert するのは (ii) の値** | (i) のみ(`settled` は計算しない) | ⚠ **仕様は非同一**(R4a の集合 ⊆ R4b の集合)。ただし**本 cert 内で vacuous** — §8【要修正-1】 |
| ⑥ | 失敗状態 | `hexagon_free_certificate = {candidate_total:3024, h10_fail:2640, h11_fail:330, generation_fail:0, shadow_total:54}` | CI run.log: `candidate_total=3024 h10_fail=2640 h11_fail=330 generation_fail=0 shadow_total=54` | ★★ **5 欄すべて一致**(本判読で最も強い副検問 diff) |

### 3.3 \|GT(M)\| = 972 — **同一対象(名指しは同一)/ ただし測定は 1 系統のみ**

凍結仕様(`docs/notes/ihnec_v1.md` §6.3 命題 ROOF(4))は次の**同値**を主張する:

> $[m,f]$($m\in\mathbb Z/18$、$f=(f_9,f_P)$)が $\mathrm{GT}(M)$ に属する $\iff$ $[m\bmod18,f_9]\in\mathrm{GT}(K^{(9)})$ かつ $[m\bmod9,f_P]\in\mathrm{GT}(N_{\rm S4})$

**R4b は左辺の基数を測り、R4a は右辺の基数を数える。** これが両系統の関係の正確な形である。

| # | 項目 | **R4a**(L71-83) | **R4b**(L216-294) | 判定 |
|---|---|---|---|---|
| ① | 入力 universe | **M に触れない**。`ck9`(K9 cert の m 別度数)と `c4`(S4 cert の m 別度数)のみ | $G_M=\langle X_M,Y_M\rangle$、$X_M=x_9\oplus X_P$・$Y_M=y_9\oplus Y_P$(27+9=36 点 block-diagonal)。実測 `\|PB3/M\|=1469664`・`derived_order=367416`・`candidate_total=4408992` | △ **層が違う**(因子 vs 屋根)— 名指す対象は同一だが universe は別物 |
| ② | 比較対象 | `GTM = sum(ck9[m]*c4[m%9] for m in k9m)`(= ROOF(4) 右辺) | `resM.shadow_total`(= ROOF(4) 左辺) | ★ 同一対象を**別の辺**から |
| ③ | 同値関係 | 因子側の (m,f) 組の同一性 | 屋根の (m,f) 組の同一性 | ★ 一致(ROOF(4) の下で) |
| ④ | 正規形 (NF) | 無し | 無し | ⚠ NF 不在 |
| ⑤ | filter | **ROOF(4) の適用そのもの**(m の charming 条件は $\mathcal X_9$=charming(18)、S4 側は $m\bmod9$) | `hex310 ∧ hex311 ∧ surj` を屋根で直接。m は `CharmingSetOf(18)` | ★ m-universe は一致(両者とも {0,2,3,5,6,8,9,11,12,14,15,17}) |
| ⑥ | 失敗状態 | 無し(算術のみ・`fails` リストは assert 用) | `h10_fail=4346784, h11_fail=61236, generation_fail=0`・`shadow_accounting_balances=true` | — |

#### 3.3.1 本判読者による独立検算(整数のみ・R4b 自身の数値だけを使用)

R4b の cert / run.log の値だけから、屋根の走査が直積として分解しているかを検算した(node・整数演算):

| 検算 | 式 | 結果 |
|---|---|---|
| 導来部分群 | 729 × 504 = 367,416 | ✔ `scan.derived_order` と一致 |
| 候補数 | 367,416 × 12 = 4,408,992 | ✔ `scan.candidate_total` と一致 |
| **(3.10) 通過数の積** | K9 単体 81/m × S4 単体 64/m = **5,184** vs 屋根 367,416−362,232 = **5,184** | ✔ 一致 |
| **shadow 数の積** | K9 単体 9/m × S4 単体 9/m = **81** vs 屋根 **81**/m | ✔ 一致 |
| CI 総和 | 12 shard の `scan.shadow_total` の総和 | ✔ **972**(cert 12 本から機械集計) |
| ローカル ↔ CI | ローカル全 12m 走 `h10_fail=4346784, h11_fail=61236, shadow=972` = CI 各 shard 値 ×12 | ✔ 完全一致 |
| 受理率 | 972 / 4,408,992 = 1/4,536 | ✔ **「何にでも当たる試験」ではない**(§8【軽微-2】) |

> **意味**: (3.10)/(3.11) は成分ごとに分解するので上 2 行は自動に近い。**自動でないのは生成条件**(部分直積が真部分群になりうる = Goursat 段)であり、屋根で `generation_fail=0` かつ因子側も 0 が出たことが **ROOF(4) の非自明部分の実測**にあたる。⟹ R4b の「独立確認」は**空虚ではない**。

---

## 4. 向き規約の突合(CV-13・本工房で 4 度事故化した点)

**結論: 向き規約は両系統で一致している。ただし一致の理由は「同じコードを共有しているから」であり、正典忠実性の証拠にはならない。**

| 層 | 実体 | 出所 |
|---|---|---|
| 積の向き | `AbstractProd([a,b,…])` は **紙の $ab\cdots$ を GAP の $\cdots b\,a$ に反転**して評価(`week3-battery-common.g` L47-54) | CV-1 と整合 |
| (3.10) | `AbstractProd([f, thetaf]) = 1`(= 紙 $f\,\theta(f)=1$) | R4a 入力生成器・R4b とも**同一文字列** |
| (3.11) | `AbstractProd([tau2ymf, tauymf, ymf]) = 1`(= 紙 $\tau^2(w)\tau(w)w=1$) | 同上 |
| 生成条件 | `genA := x^u`, `genB := AbstractProd([f^-1, y^u, f])` | 同上 |
| PSL 窓の宣言 | `S4.v2.json` `convention_note` = 「XYZ=1 checked as GAP Z*Y*X=1 (full 3-term reversal, paper's word AB=GAP's B*A applied to all 3 factors)」 | 上の反転規約と**整合** |
| R4b の cert 宣言 | `conventions_used.perm_composition = "gap_native_right_action"` + `reduced_hexagon_predicate` に式を明記 | 宣言と実装が一致(本判読者が突合) |

> ### ★ CV-13 射程限定の直接適用(§1 表 CV-13・便 98 F98-4.5)
> CV-13 は **internal orientation gate であって canonical-fidelity gate ではない**。本件では受理式が**両系統で同一のソーステキスト**であるため、内部整合は自明に成り立つ一方、**一様な鏡像(共有された向き誤り)はこの対で原理的に検出できない**。
> CV-13 が義務づける「**外部 anchor(既知集合との集合等号)または独立 source-map route の併置**」は、**本対には存在しない**。R4b の 108/54 アンカーは同一述語・同一窓の再走であり、外部 anchor ではない。
> ⟹ **「向きが正典と一致する」と書いてはならない**(CV-13 の明文)。書けるのは「**両系統で向きは同一**」までである。

---

## 5. 独立性の評価(cross-checked の前提)

| 軸 | 108 | 54 | 972 |
|---|---|---|---|
| **受理式の実装** | ✗ 逐語複製(`suite-wp2-explorer.g` L224-234 ≡ `ihnec_r4b_run.g` L97-106) | ✗ 逐語複製(`EnumerateReducedHexagon` ≡ `ScanRoofHexagon`) | △ R4a は受理式を**持たない**(算術のみ)・R4b のみが実装 |
| **群の構成コード** | ✗ `MakeGn` が両ファイルに逐語複製 | ✗ marking 5 行が逐語複製 | ✗ 因子の構成は上に同じ(屋根の block-diagonal 埋め込みのみ R4b 固有) |
| **言語・処理系** | ✗ 両方 GAP 4.16.0 | ✗ 両方 GAP 4.16.0 | ○ python(R4a)vs GAP(R4b) |
| **入力の共有** | ○ R4b は cert を読まない(driver L25-29 の宣言を本判読者がソースで確認) | ○ 同左 | ○ 同左 |
| **列挙戦略** | ○ BFS+word 辞書 vs `Elements(DerivedSubgroup(G))` 直接列挙 | ○ 同左 | ○ 同左 |
| **著者** | ○ R4a = 数学者(Opus 5)/ R4b = implementer(driver ヘッダ「実装係」)/ CI 発車 = miner | ○ 同左 | ○ 同左 |
| **環境** | ○ ローカル Windows vs CI ubuntu(run 30697198947) | ○ 同左 | ○ 同左 |
| **GAP のバージョン** | ✗ 両環境とも `4.16.0`(cert `provenance.gap_version` を 12 本+ローカルで機械確認) | ✗ 同左 | ✗ 同左 |

**総評**:
- **972**: 独立性は**実在する**(入力非共有・別言語・別著者・別環境)。ただし独立性の**型**が「二測定」ではなく「予測 × 測定」(限定 A)。
- **108 / 54**: 独立性は**列挙戦略・環境・実行時刻のみ**。受理式と窓構成は同一ソースの複製であり、**規約誤り・数式誤りに対する検出力はゼロ**。買えているのは「BFS 辞書実装の bug」「Windows 固有の bug」「一過性の実行事故」の排除まで。

---

## 6. IF-FIRST 順序の確認(CV-9-1 / CV-9-4 / §3)

| 事象 | 時点 | 判定 |
|---|---|---|
| 予言 P-IHN-1〜7 の凍結(`ihnec_v1.md` §6.5・検算 script digest `edf61813…9309`) | 実測前 | ★ **prediction-first は守られている**(本判読で最も健全な点) |
| R4a/R4b の役割分担と独立性要求(§6.6 注 1)の文書化 | 実測前 | ✔ |
| **CV-9-1 主検問(非当事者が 6 項目を照合)** | — | ✗ **未実施**(CV-9 制度は裁定 316/318 = 本件設計より後) |
| **仕様変更①**: R4a が「GAP 新規悉皆走査」→「既存 cert を入力とする独立実装」へ(追補 C.1・**自主申告あり**) | 凍結後・R4b 実測前 | ⚠ **CV-9-4 の差戻し事由に該当**。この変更が「二測定」を「予測 × 測定」に変えた(限定 A の発生源) |
| **仕様変更②**: R4b が「BFS+word 辞書の流用」→「`Elements(D)` 直接列挙」へ(driver L11-23・**自主申告あり**) | 凍結後・実測前 | ○ **受理式は不変**(本判読者がソースで逐語一致を確認)。列挙戦略のみ ⟹ 実害なし |
| CV-9 判読(本稿) | 両実測の**後** | ⚠ **副検問のみの retrofit** |

> **CV-9-4 の字義**: 「主検問後に仕様または normalizer が変われば、副検問で救済せず主検問へ差し戻す。」 本件は主検問が存在しないため「差し戻す先」が無い。**司令塔裁定事項**として §8【重大-1】に挙げる。
> なお**両方の仕様変更は当事者が自主申告している**(追補 C.1・driver ヘッダ)。隠蔽ではない — 制度が無かっただけである。

---

## 7. CV-9-5(検問記録の束縛)の充足状況

| 要求 | 状況 |
|---|---|
| 両 source / spec digest | ✔ §2 に全 digest。**ただし R4a 側に cert artifact が存在しない**(出力は `ihnec_v1.md` 追補 C の地の文のみ)⟹ CV-9-2 の「二 artifact の機械 diff」は**片側しか artifact が無い**(§8【要修正-2】) |
| target | ✔ 972 / 108 / 54 と明示 |
| competitor universe | ✗ **未登録**。「972 でない値と区別できるか」の分離条件(CV-7 §1.2)が両系統ともに無い |
| **識別力を持つ dummy fixture** | ✗ **両系統ともに不在**。R4b の `anchors`(108/54)は**既知値ゲート**であって dummy fixture ではない(期待値がソースに直書きされ、不一致なら `Error` で停止 ⟹ **不一致は cert として残らない**) |

---

## 8. 発見した齟齬・懸念(全列挙 — 潰す義務は負わない)

### 【重大-1】972 の格の型が「二測定の一致」ではない
- **根拠**: `ihnec_r4a_run.py` L74 `GTM=sum(ck9[m]*c4[m%9] …)` は命題 ROOF(4) の右辺そのもの。`ihnec_v1.md` 追補 C.4 が「**命題 ROOF(4) は確認していない。972 は ROOF(4) を使って因子データから組み立てた値である**」と自ら明記している。
- **含意**: 便 99 の請求文「R4a(組立)× R4b(直接悉皆列挙)」を読んだ者が「二つの独立測定が一致した」と受け取る余地がある。**格の内容を「紙の予測 × 機械の測定」と明記すれば齟齬は消える**(値の訂正は不要)。
- **付記(擁護側)**: この構図は設計どおりである(§6.6 注 1・追補 C.4)。**欠陥ではなく、格の言い方の問題**。

### 【要修正-1】54 の根拠が両系統で別述語(R4a = settled / R4b = shadow)
- **根拠**: R4a は `chk(S4['settled_count']==54,"|GT(N_S4)|=54")`(L66)。`settled` は `week3-psl-common.g` L373-387 の「∃h∈PΓL(2,8) が $T_{m,f}$ を実現する」witness 探索であり、R4b の `shadow_total`(hexagon+生成条件)より**真に強い条件**。
- **本件では vacuous**: `S4.v2.json` 内で `hexagon_free_certificate.shadow_total = 54`・`generation_pass_count = 54`・`settled_count = 54`・`settled_detail` 54 行が**全て `settled: true`** — 本判読者が機械確認済み。⟹ 両者は**同一集合**。
- **正確な記帳の提案**: 「R4a の 54 = settled 数、R4b の 54 = shadow 数、両者一致は `S4.v2.json` 内で機械確認」と書く。
- **付随の吉報**: 972 の組立に使う `c4` は `settled_detail` の**全行**を数えており(L65)、これは shadow 集合そのもの ⟹ **972 の組立側には settled 非対称は入っていない**。

### 【要修正-2】R4a に cert artifact が無い(副検問が非対称)
- R4a の出力は stdout → `ihnec_v1.md` 追補 C の表。`conventions_used` ブロックが**どこにも存在しない**。⟹ CV-9-2 の機械 diff が構造的にできない。script digest はあるので**出所は追える**が、規約宣言の突合は人手になる(本稿がそれを代行した)。

### 【要修正-3】NF(正規形)を凍結していない — 一致は「基数の一致」のみ
- 両系統が突き合わせているのは **108 / 54 / 972 という整数**だけで、**shadow 集合そのものの照合はしていない**。R4a の f ラベルは `f_word` / `f_triple`、R4b は置換元 — **写像が定義されていない**。
- ⟹ 原理的には「別の 972 元集合」が両側で出ていても検出できない。IF-FIRST §3.2「生比較の禁止/NF 方式」の要求を満たしていない。
- **緩和材料**: R4b の m 別内訳(全 m で 81)と R4a の m 別内訳(9×9)が一致し、`reduction_images_this_shard` が 12/6 の m 像を全被覆している ⟹ **m 水準までは集合として照合されている**。未照合なのは各 m-fiber 内部(81 元)の中身。

### 【要修正-4】R4b cert の `conventions_used` が台帳 §2 の字義に照らして MALFORMED
- `"comparison_target": "n/a(単系統GAP探索。二実装照合ではない)"` は **object 欄への bare string** ⟹ **規範 8 違反**(`{status:"n/a", reason:…}` が正形)。
- `chi_P_criterion` が**欠落** ⟹ **規範 2**(省略した cert も MALFORMED)。他に `roundtrip_witness` / `separation` / `effective_source_chain` / `level` 等も不在(規範 1 は「省略でなく `"n/a"`」を要求)。
- **情状**: 台帳自身の【CL-8】が「全欄必須にすると小さな probe cert が書けない / 二層適用が要るかもしれない・**未検討**」と開いており、本 cert はまさにその未決部分に落ちている。cert は `cross_checked_status: n/a` を自ら宣言しており**格を偽っていない**。⟹ 「cert を直す」より「**台帳 §2 の二層適用を裁定する**」ほうが筋。

### 【要修正-5】識別力を持つ dummy fixture が両系統に無い(CV-9-5 未充足)
- R4b のアンカーは**期待値直書き + 不一致で `Error` 停止**(L179-198)。したがって「**不一致な cert は生成されえない**」— 12/12 の一致は 12 回の独立試行ではなく、**同一の決定的計算の 12 回反復**である(各 shard が同じ K9/S4 アンカーを毎回再計算している)。
- 陽性統制としては機能するが、**陰性統制(落ちるべき fixture が落ちる)は未登録**。

### 【軽微-1】「二環境」は OS 層のみ — GAP は両環境とも 4.16.0
- 12 本の CI cert と ローカル cert の `provenance.gap_version` は全て `4.16.0`(機械確認)。⟹ **GAP 実装固有のバグは二環境化で排除できていない**。「二環境」の語は OS/toolchain 層を指すと明記するのが正確。

### 【軽微-2】分離条件の代替材料はある(反証できなかった点の正直な報告)
- 受理率 972/4,408,992 = **1/4,536**、K9 単体 108/8,748 = 1/81、S4 単体 54/3,024 = 1/56。**「何にでも当たる試験」ではないことは実測で示されている**。CV-7 §1.2 が要求する形式的な分離条件(競合 universe に対する非一致)ではないが、識別力ゼロの疑いは**この観点からは立たなかった**。

### 【軽微-3】屋根 M の実現には両系統に共有された前提がある
- $G_M := \langle x_9\oplus X_P,\ y_9\oplus Y_P\rangle$ が $PB_3/(K^{(9)}\cap N_{\rm S4})$ であるためには、**二つの窓の marking $(x,y)$ が同じ $PB_3$ 生成対の像である**ことが要る。この前提は R4b の実装にも命題 ROOF にも**共通**で、本対では**反証不能**。$|G_M|=1{,}469{,}664$ の実測はこの前提の下でのみ ROOF(1) の確認になる。(数学的当否は Sol/数学者の領分・本判読は指摘のみ)

### 【軽微-4】検収レポートの語法 1 箇所
- `mine/reports/ihnec-r4b-20260801_report.md` L58 に「charming_set_m の**18 元中 12 元**」とあるが、charming set は **12 元**であり 18 は法($M_{\rm ord}$)である。12 shard は charming set の**全体**を覆う(cert `charming_set_m` と `shard.target_ms` の和が一致することを機械確認)。⟹ **数値ではなく語法の誤り**。「$\mathbb Z/18$ の 18 剰余類のうち charming な 12 元」が正。

### 【軽微-5】CI shard cert の置き場
- 12 本の cert は `scratchpad/ihnec_r4b/…`(git 未追跡)にのみ存在する。GHA artifact は失効しうるので、**格上げの根拠にするなら永続位置へ移すか digest を LEDGER に固定する**のが安全(CV-11 の精神)。CI 側の `ci/out/` には cert JSON が含まれず run.log のみ — 数値は log からも取れるが、正式 artifact は `mine/out/` 側にある。

---

## 9. 射程限定(この判読が言っていること・言っていないこと)

**本判読の対象は 3 つの整数のみ**: |GT(M)| = 972、|GT(K⁽⁹⁾)| = 108、|GT(N_S4)| = 54。

**対象外(明示)**:
- **U-11(合成表 11,664 対・$\mathrm{GT}(K^{(9)})\cong\mathrm{Aff}(\mathbb Z/9)\times C_2$)は本判読の射程外**。R4b は合成表を一切作っていない(`ihnec_r4b_run.g` に積の検査は存在しない — 本判読者がソース全体を確認)。⟹ **U-11 は R4a 単系統のまま**であり、「有限 exhaustive candidate / single lane」の記帳(便 98 F98-3.8)を**据え置くのが正しい**。裁定 389 の分離請求方針を本判読は支持する。
- P-IHN-1/2/3(比較不能・|PB₃/M|=1,469,664・M_ord=18)は R4b **単系統**(R4a は「射程外・未測定」と自認)⟹ これらに二経路の格は付かない。
- P-IHN-7 後半($\mathrm{GT}(M)$ の抽象型)は**どちらの系統も測っていない**。
- 命題 ROOF・定理 SPLIT-NULL・(S4-ISO) 等の**数学的当否**(§1.3.4 によりスコープ外)。
- 実装コードの品質レビュー・追加テストの発案(同上)。

---

## 10. 判読の限界(§4 射程宣言に準じる)

1. **PASS は正しさを含意しない**。本判読が言えるのは「二系統は同じ対象を指している」までで、**その対象の測り方が正典に忠実か**は言えない(§4「宣言は正しさを含意しない」・CV-13 射程限定)。
2. **共有ソースは同一性を強め、独立性を弱める**。本件の同一性判定が高い確度で下せた理由そのもの(逐語複製)が、独立性を削っている。この二律背反は本判読では解消できない。
3. **主検問を代替しない**。本稿は事後の副検問であり、CV-9-1 が意図した「無駄な計算の前に仕様齟齬を殺す」効果は本件では得られていない(得られたのは記録の整備のみ)。
4. 本判読は **1 走**で完結し、調査を自己拡大していない(§1.3.4)。
