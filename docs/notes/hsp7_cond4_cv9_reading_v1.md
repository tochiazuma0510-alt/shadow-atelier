# HS 発火条件 4 較正走 — CV-9 **副検問**(非当事者判読)v1

- **判読者**: falsifier(反証前哨・非当事者)/ **日付**: 2026-08-04
- **委嘱**: 司令塔(lanespec `docs/notes/hsp7_cond4_lanespec_v1.md` v1.2 §5「仕様凍結→主検問→発注→**副検問**」の最終段 = HS 発火条件 5)
- **判読対象**: 4 cert(laneS / laneV_v2 / laneP / summary)+ 各レーン driver + Lane Σ driver + 生ログ
- **前提として入力に使った文書**: `docs/notes/hsp7_hexagon_arbitration_v1.md`(仲裁書。Prop 3.4 前提充足・Lane V バグ確定・N∩F₂=N₀∩F₂ の構造事実は再導出せず入力として採用)
- **範囲外申告**: 仕様の数学的正しさの監査(Sol/数学者の領分)・実装コードの一般レビュー・代替較正の設計はしない。封印量非接触。

---

## 0. 判定(三値)

# 差戻し

**数値そのものには反証を見つけられなかった**(むしろ二系統の外側から NW-P8 を独立に再現した・§3.1)。差戻しの理由は数値ではなく、**(a) 条件 4 の物理証拠が格付け対象 cert に載っていない・(b) Lane P が lanespec 自身の基準で未較正・(c) c 軸の事前登録が未履行かつ無申告・(d) 「修理後の一致」を隠した格付け文言**の 4 点である。

較正走を **cross-checked と格付けすることはできない**。したがって便 102 で本走認可請求を出す前提は、現状では立たない。

---

## 1. 機械検証済みの事実(判読者が自前で再計算)

| 検査 | 結果 |
|---|---|
| 4 cert のファイル sha256 と Lane Σ の `input_cert_sha256` 宣言 | **全一致**(laneS `f5c53c9f…`, laneV_v2 `7cc7e312…`, laneP `4a41ea6d…`) |
| R-20 連鎖: laneV/laneP の `candidates_in_source_cert_sha256` vs Lane S cert 実測 | **一致**(いずれも `f5c53c9f…`) |
| cert 内に埋め込まれた成果物 digest(log/script/setup/PQ_OUTPUT、計 21 本) | **全て byte-exact 一致** |
| digest 束縛された scratchpad 証拠 5 本(laneS 2 本・laneV 1 本・laneP 2 本) | 本 worktree には**不在**。各レーンの worktree 内に実在し、**宣言 digest と全一致**(§4-M2) |
| Lane S 内蔵の `post_delete_listing` 文字列の sha256 | 宣言値 `f192d5e1…` と一致(末尾改行込み) |
| 各 cert の候補別 verdict と構成 boolean の内部整合(`hex_3_10∧hex_3_11` / `hex_3_3∧hex_3_4`) | **8 行×2 レーンとも整合** |
| Lane Σ driver 生出力 JSON と summary cert の転記 | **全欄一致** |
| ANUPQ バイト一致の主張 | **事実**。laneS(P 側)・**laneV(P 側・cert 未申告)**・laneP(Q 側)の setup/output は cond2 cert の該当 4 digest と完全一致 |
| 3 レーンの h₄/h₃ 語・生成元対応 | **同一**(h₄ = [[[x,y],x],x]·[[[x,y],x],y]⁴·[[[x,y],y],y]、h₃ = [[x,y],x]·[[x,y],y]、Lane P は j(x)=x₁₂=K05fp.1, j(y)=x₂₃=K05fp.4) |
| `codegen_uses_expected_values: false` の実地確認 | 3 レーンとも期待値の計算内埋め込みは**見つからず**(Lane V の hard-code 8 件/f_word 列は事前登録突合の意図された実装) |

---

## 2. 判定事項ごとの裁定

### 2.1 事後整合性 — **PASS(1 点の重大な欠落を除く)**
上表のとおり digest 連鎖・conventions_used の相互整合(`ledger_version=conventions_ledger_v1_6` / `f_word_order="paper (W-3)"` / `a5_conv_result` )は成立。**ただし Lane V v2 は §4-M1 の欠落がある。**

### 2.2 「二系統一致」の意味論 — **同一対象(条件は満たされている)**
Lane S は簡約 (3.10)(3.11) を pc 群 P(位数 7⁸)上の直接演算で、Lane V は full (3.3)(3.4) を 12 規則 transversal 状態機械上の σ 語で評価しており、**計算対象も述語も別物**。両者を繋ぐ Prop 3.4 の前提(N ∈ NFI_{PB₃}(B₃)、(m,f) ∈ ℤ×[F₂,F₂])は仲裁書で確定済みで、本較正走の全候補が充足する(h₄ᵗ∈γ₄、h₃∈γ₃、f=1)。生成元対応(x=x₁₂=σ₁², y=x₂₃=σ₂², c=(σ₁σ₂)³)も 3 レーンで一致。**⟹ 「別述語の一致」を cross-checked と読む数学的条件は満たされている。** ただし §4-M5(修理後の一致)により、一致の**証拠力の所在**が変わっている。

### 2.3 ANUPQ バイト一致 — **格の但し書きが要る(格下げは不要)**
バイト一致は「コピーしても一致する」ため**独立性の識別力はゼロ**であり、`傍証` とは呼べない。正しくは**同一対象性の強い証拠**(3 レーンが同じ入力を同じ決定的ツールに与えた)である。独立性の根拠は worktree 物理削除のみに残り、それは実在が確認できた。派生して、Lane V の S-7′ 「own/anchor/LaneS の 3 者一致」は**3 系統の裏取りではない**(Lane V は Lane S と byte 同一の `PQ_OUTPUT_P.g` を読んでいる)。

### 2.4 Lane Σ の独立性 — **トートロジーではない。ただし薄い**
Σ は Lane V の自己申告 `four_way_comparison_table` ではなく両 cert の一次判定配列から再抽出しており、転記誤りは捕まえる。`s9_predicate` は片側欠鍵を `MISSING` で検出する。しかし Σ が自前で再計算しているのは実質「Lane S cert の sha256」と「S-9/S-8 述語の再適用」の 2 つのみで、**値の共有誤りには原理的に無力**(Σ 自身がそう書いていない)。§4-m3/m4 も参照。

### 2.5 較正の十分性 — **不十分(重大 2 件・要修正 2 件)** → §3・§4

### 2.6 総合 — **差戻し**。blocking 条件は §5。

---

## 3. 判読者による独立検算

### 3.1 NW-P8 m 掃引の独立再現(**二系統が存在しない唯一のブロック**)
Lane S の評価器は m 引数を持たず(`Hex311(f) = τ²(f)τ(f)f`)、**構造的に m≠0 を扱えない**。よって NW-P8 の 5 件は Lane V 単独申告であり、N/N₀ 比較は仲裁 (P-1) により理論上必ず一致するので検出力ゼロ。判読者が外部から埋めた:

f=1 のとき (3.10) は恒真、(3.11) は τ:x→y→z→x(z=(xy)⁻¹)より
$$w_m := \tau^2(y^m)\,\tau(y^m)\,y^m = x^m (xy)^{-m} y^m \overset{?}{=} 1 \ \text{in } P .$$
- **m=6**: 指数 7 より x⁶=x⁻¹, (xy)⁻⁶=(xy), y⁶=y⁻¹ ⟹ w₆ = x⁻¹(xy)y⁻¹ = 1 **厳密に成立** ⟹ PASS が強制される。
- **m=1,2,4,5**: UT(5,𝔽₇)(n=5≤p=7 ゆえ class 4・指数 7 ⟹ 任意の 2 元生成部分群は P の商)の 7 組の生成元対で w_m ≠ I を確認 ⟹ P で w_m ≠ 1 ⟹ FAIL。

**⟹ (FAIL, FAIL, FAIL, FAIL, PASS) を Lane V と独立に再現。一致。** 併せて判明: NW-P8 は「m ≡ 0 または −1 (mod N_ord) ⟺ PASS」の確認に過ぎず(TOY 窓の m=2 PASS も同じ規則の帰結)、非自明な発見を含まない。検算: `scratchpad/msweep_check.py` 相当(整数演算のみ・GAP 非依存・レーン成果物非依存)。

### 3.2 h₃ の (3.10) PASS(Lane S 逸脱申告 3)
θ は gr₃ 上で 𝔥₃ = u₁+u₂ を −(u₂+u₁) に送る(θ(u₁)=−u₂, θ(u₂)=−u₁)ため γ₃/γ₄ では消える。P で厳密に 1 になるか(γ₄ 成分の消滅)は独立には確かめていない — Lane S の実測を反証も追認もできていない。**負例としての機能は (3.11)=FAIL で立っているので judgement には影響しない。**

---

## 4. 所見

### 【重大】M1. Lane V v2 cert に条件 4 の物理証拠が無い
v2 には **`execution_isolation` ブロックが存在しない**(D-2 が「判定根拠は自己申告 boolean ではなく物理事実」と明記した当の欄)。併せて `imports_declared`・`imports_forbidden_check`・`candidates_in_own_digest_sha256`・`compute_budget` も無い(あるのは `imports_declared_addendum` のみ)。v1 にはすべて在る。しかし **Lane Σ は「v1 は読んでいない」と明記して集約している** ⟹ 格付け対象の束は、二系統一致の検証側を担う cert について helper 非共有の裏取りを**一切含んでいない**。条件 4 そのものが主題なので、これは形式不備ではなく中身の欠落。
*(証拠は実在する: v1 の `post_delete_listing_sha256=4fcb20e7…` は worktree 内の実ファイルと一致した。閉じ方は**cert 修文**で足りる。)*

### 【重大】M2. Lane P に非自明な PASS が一つも無い ⟹ lanespec 自身の基準で未較正
Lane P の全 13 件は: NW-P6 で PASS = t=0(f=1)のみ・t=1..6 FAIL、h₃ FAIL、NW-P8 側 5 件は f̄=1 の自明 PASS。**「PENT_W(f)=true ⟺ f が自明」という誤実装は Lane P の 13 件すべてを完全に再現する。** これは lanespec 付録 A-1 が自ら書いた識別力条件(「NW-P7 だけが非自明な PENT PASS を含む事前登録予言」「PENT PASS⟺入力が自明という誤実装では NW-P7 の 5 元中 5 元 PASS を再現できない」)に文字どおり該当し、その NW-P7 は C-6 順序ゲート未発効で走っていない。
緩和材料は ρ の well-defined/bijective/位数 5/非恒等という構造チェックのみで、これらは **N_ρ の積式を一度も検査しない**。
付随: 候補が全て γ₄(Q)(γ₅(Q)=1 ゆえ中心・初等アーベル)に落ちるため **N_ρ の積順序規約も一度も試験されていない**。Lane S は同型の事実を自分で開示したが(`word_order_robustness_note`)、Lane P は前例(cond2)への依拠で済ませており、この非試験性を申告していない。本走では f が一般の charming 元に及び中心性が効かなくなるため、この規約は生きた争点になる。

### 【重大】M3. c(中心因子)経路の較正が 1 セル + 事前登録の未履行が無申告
- 恒久 fixture(TOY)は **c ↦ 1 を構成上「要求」する**(`statemachine_lib.g` L405-407: `if Cg <> One(...) then return rec(ok := false, reason := "c is not trivial in this TOY window …")`)⟹ **TOY は c 会計に対して識別力ゼロ**。
- 実走で φ(c)≠1 なのは N₀ 窓のみ。N₀ が使われたのは NW-P8 の 5 セルだけで、うち 4 件は FAIL/FAIL(c 成分の一致は問われない)⟹ **c 会計を生かして検査しているセルは m=6 の 1 点のみ**。
- しかも仲裁 §5.4 項目 5 の事前登録は「**主標的 N・control N₀ の両方で** h₄ᵗ(t=0..6)全 PASS・h₃ FAIL」だが、`driver_step4_evaluate_v2.g` は 8 候補を **N 窓のみ**(`chatMain := Identity(P)`)で評価している。cert は `prediction_source.frozen_at` にその事前登録を引用しながら、未評価であることを `not_evaluated` として申告していない。
- 無害ではない: v1 のバグは「c は中心なので c 成分の会計だけ健全に見えた」型であり、**c 軸が盲点だった系譜そのもの**。8 候補を N₀ でも回せば生きた検査セルが 1 → 8 に増える。実行コストは秒オーダー。
- 緩和材料(実在する): ApplyGen 自体の c 経路は selftest の control 型インスタンス G₃×C₅(3240 点)で braid 関係 0 fail が確認されている。ただし braid 関係の成立は必要条件であって (3.3)(3.4) の c 指数会計の十分検査ではない。

### 【重大】M4. 「修理後の一致」が格付け文言から落ちている
時系列は v1 が S-9 発火(mismatch=6)→ 仲裁 → 修理 → v2 で mismatch=0。すなわち **S/V の一致は「独立二系統が偶然一致した」のではなく「一方を他方に合うまで直した」結果**である。緩和は本物(バグの構造的同定・修理 A は調整ノブでなく経路の廃止・独立 literal オラクル・期待値は Lane S でなく紙から)。しかしその帰結として、**一致の証拠力は「一致そのもの」ではなく TOY literal オラクルと紙の予言(DUM-HEX + 数学者の独立 Lie 検算)に移っている**。そして TOY は c 非自明経路も負例も持たない(M3・m1)。
にもかかわらず summary の `completeness_claim` (iii) と Lane V の `cross_checked_status.reason` にはこの但し書きが無い。**この状態で cross-checked を無条件に名乗るのは過剰。**

### 【重大】M5. NW-P8 の事前登録予言は反証されており、その撤回が正本に伝播していない
lanespec §4.2/付録 A-2 の予言は「5 件のうち少なくとも 1 件で N・N₀ の判定が食い違う」。実測 0 件。仲裁 (P-1) は「N∩F₂ = N₀∩F₂ = 𝒱(F₂) ゆえ charming f では理論上必ず一致する」= **予言が最初から偽だった**ことを示す(数学的には仲裁が正しい)。手続きとしてこれは**事前登録の反証**であり、cert は S-8 の解釈を「情報不足」→「理論的に予言された一致」へ事後に書き換えている。S-7′ の note が禁じる「後から期待値を弱めない」型に触れる。
波及先は較正走の外: 正本 `hs_prop7_translation_v1.md` §8.7.7 の NW-P8 行と §9.3 の S-8。放置すると **本走で S-8 は charming 候補に対して恒真に発火し、毎回「解釈で回避」する運用**になる。versioned な撤回・再定義が要る(司令塔案件)。

### 【要修正】m1. 恒久 fixture(TOY)に負例が無い
6 セルすべてが literal=PASS/PASS。⟹ **「常に PASS を返す評価器」は TOY ゲートを 6/6 で通過する**。TOY は実走を許可するゲートとして使われている(`driver_step4_evaluate_v2.g` L17-21)ので、ゲート側に分離条件が無いのは設計上の穴。実走側に負例(h₃・m∈{1,2,4,5})があるので今回の評価器が定数 PASS でないことは別途分かるが、それは「ゲートが効いた」ことにはならない。
関連(こちらは欠陥ではない): 等式判定は反自己同型で不変なので、**全体一貫した語順反転は原理的に検出不能**。検出すべきは*不整合な*反転であり、それは literal 突合が担う — この論理が cert のどこにも書かれていないため、A5-CONV/TOY の守備範囲が読み手に誤解される。

### 【要修正】m2. Lane V の 0 手目 A5-CONV が v2 の新コード経路を覆っていない
v2 は評価経路を全面置換した(`LetterRepAssocWord` → σ 文字列展開 → ApplyGen)のに、`a5_conv_result` は "correct (v1 から不変、再検証不要)" として再実行されておらず、v2 の唯一のゲートは TOY である。A5-CONV は置換の右作用規約を突くテストであり、**Lane S の driver 自身が「W-1 反転は置換/右作用表現に固有」と書いている**とおり、v2 が新設した語順面(自由群 letter rep の順序)には一度も触れていない。lanespec §0.2 の運用文言(各レーンの driver は最初に A5-CONV を走らせる)にも形式上反する。

### 【要修正】m3. `prediction_source.frozen_at` が digest でない
lanespec §6 は `"frozen_at": "<本ノート該当節のdigest>"` を要求しているが、3 レーンとも**節名の文字列**を書いている。参照先文書は可変なので、「予言を後から書き換えていない」ことが検証不能。**本件で実際に効いている**: Lane V の `frozen_at` は、争点の測定値が出た**後**に書かれた仲裁書 §5.4 項目 5 を事前登録として引用している(実質は非当事者の数学者が理論から導いた予言なので中身は健全だが、形式はこの規律が防ぐべき当のもの)。

### 【要修正】m4. R-20 と S-8 述語の検査に穴
- Lane V に `candidates_in_own_digest_sha256` が無い(v1 は note のみ、v2 は欄ごと消失)。Lane Σ の R-20 検査は `candidates_in_source_cert_sha256` しか見ないので、この欠落を捕まえていない。*(実質は Lane V が driver 内で Lane S cert を機械 text-scan して候補列を突合しているので中身は担保されている — 欄の不備。)*
- Lane Σ の自己較正 fixture は `s9_predicate` のみを検査。**`s8_predicate` は無検査**で、しかも極性が反転している(`fired = (mismatch == 0)`)= 符号ミスが最も起きる型。読んだ限り実装は正しい。
- Lane Σ は両レーンの候補集合を **lanespec §6 C-5 の事前登録リストと突合していない**(件数 8 を報告するだけ)。両レーンが同じ鍵を落とした場合に無力。

### 【要修正】m5. Lane V が自分で `cross_checked_status.status = "cross-checked"` と名乗っている
lanespec §7 手順 6 は「(副検問を)経てここで初めて cross-checked を名乗れる」。Lane S・Lane P は正しく `"n/a"`。Lane V v2 のみ `status` が `"cross-checked"` で、**同じ欄の `reason` 本文が「副検問を経て初めて名乗れる(本 cert はその前段)」と自己矛盾している**。機械 diff で捕まる型の規約ズレ。

### 【軽微】m6. 証拠ファイルが本 worktree に merge されていない
digest 束縛された 5 本(`scratchpad/laneS_post_delete_listing.txt`, `laneS_own_measurement_phase1.txt`, `laneV_post_delete_listing.txt`, `laneP_own_measurement.txt`, `laneP_candidates_in.txt`)が本 worktree に無い。各レーン worktree 内に実在し digest は全一致したので**証拠鎖は健全**だが、`.claude/worktrees/` は git 管理外の一時領域であり、消えれば cert が検証不能になる。

### 【軽微】m7. 範囲縮小が集約 cert に記録されていない
Lane S は司令塔の本発注で候補を 8 件(lanespec C-5 の 13 件の真部分集合)に縮小され、それを deviations 4 で正直に開示している。しかし **summary cert にはこの縮小の記載が無い**(`candidate_count: 8` のみ)ので、summary だけを読む者は lanespec の事前登録リストと突合できない。同様に、NW-P8 の 5 件が「二系統性の無い単独申告」であることも summary で格が区別されていない。

### 【軽微】m8. §8.6 条件 3 の 4 判定分離のうち charming と SURJ は数値評価が無い
本較正走が評価したのは hexagon と PENT のみ。正本は §8.3.2 で紙の分離を済ませたとしているので較正走の欠落ではないが、「5 条全閉」を宣言する際に**条件 3 は紙で閉じている**旨を明記しないと、後から「数値でも 4 判定を分離した」と読まれる。

### 【所見・肯定】
3 レーンとも `deviations_and_open_questions` で自分に不利な事実を自己申告している(Lane S: R-11 順序瑕疵・h₃ の (3.10) 想定外 PASS・候補範囲縮小/Lane P: 同型の順序瑕疵・NW-P8 側の自明性・worktree の提供経路差/Lane V: 旧 evaluator 残置・NW-P8 全再計算)。**隠蔽の兆候は見つからなかった。** M2/M3 の穴は、隠されていたのではなく「気付かれていなかった」型である。

---

## 5. 差戻しの blocking 条件(この 4 つが閉じるまで cross-checked を名乗れない)

| # | 条件 | 閉じ方の重さ |
|---|---|---|
| **B-1** | Lane V の cert に `execution_isolation`(post_delete_listing + digest)・`imports_declared`・`imports_forbidden_check`・`candidates_in_own_digest_sha256` を載せる。証拠は worktree 内に実在し判読者が digest 一致を確認済み | **cert 修文のみ**(再走不要) |
| **B-2** | 事前登録どおり **8 候補を N₀ 窓でも評価**する(仲裁 §5.4 項目 5)。実行できないなら cert に `not_evaluated` を明記し、c 会計の較正が m=6 の 1 セルのみである旨を格の但し書きとして書く | **秒オーダーの再走**(Lane V) |
| **B-3** | Lane P の分離条件を立てる — すなわち**非自明な PENT PASS を含む予言を 1 つ通す**。lanespec 自身の設計では NW-P7(付録 A-1 の versioned 発効が必要)。発効が Sol 認可待ちなら、Lane P の格を「未較正(PENT PASS⟺自明 の誤実装を排除できていない)」として cert と summary に明記する | **司令塔/Sol 判断**(発効 or 格の明記) |
| **B-4** | 格付け文言の訂正: (i) Lane V は修理後の再走であり一致の証拠力は TOY literal オラクルと紙の予言に由来する旨、(ii) ANUPQ バイト一致は独立性ではなく同一対象性の証拠である旨、(iii) Lane V の `cross_checked_status.status` を `"n/a"` に戻す、(iv) NW-P8 の 5 件は二系統性を持たない単独申告である旨 | **cert 修文のみ** |

**別枠(較正走の外・司令塔案件)**: M5 の NW-P8 予言の versioned 撤回と S-8 の再定義。これを片付けずに本走へ行くと S-8 は毎回恒真に発火する。

---

## 6. 反証できなかった範囲(正直な申告)

- 8 候補の判定値そのもの(Lane S 7 PASS+1 FAIL / Lane V 同)には穴を見つけられなかった。h₄ᵗ の全 PASS は DUM-HEX + 数学者の独立 Lie 検算 + Lane V の三重アンカーがあり、判読者はこれを覆す材料を持たない。
- NW-P8 の N 列は外部から独立に再現でき、**一致した**(§3.1)。
- h₃ の (3.10) が P で厳密に 1 になるか(Lane S 逸脱申告 3)は独立には確かめていない。商への写像では PASS 側は証明できないため。判定への影響は無い。
- 「3 レーンが本当に別セッションで書かれたか」は worktree の物理痕跡と時刻で裏取りしたが、**Lane V については格付け対象 cert にその痕跡が載っていない**(B-1)。
- Lane P の K(0,5) 構成(stage1-2 継承)と Q の pc 構築は cond2 と byte 同一であり、**構築層は独立再計算になっていない**(評価層のみが独立)。Lane P cert の「同一量の独立再計算」はこの限定つきで読むべきだが、限定は書かれていない。
- 本判読は cert・driver・ログの読解と小さな独立検算に基づく。**実装コードの網羅的レビューは行っていない**(職掌外)。ここで PASS を出せなかったことは、逆に「他の穴が無い」ことの保証ではない。

---

**使用ソフト**: Python 3(標準ライブラリのみ・整数演算)/ sha256sum。**GAP 不使用**(レーンの計算を再実行していない = 非当事者性の維持)。
