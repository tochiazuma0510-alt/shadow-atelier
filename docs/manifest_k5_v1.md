# 事前登録 manifest — K⁽⁵⁾ 算術飽和キャンペーン v1.5(2026-07-27・司令塔)

> v1.4 → v1.5(便 38・裁定 39): F8-6 の sealed automation・positive-only 非網羅規則を changelog から **operative な工程節へ転記**+実 K5 Freeze 2 の「同一 bundle から係数ごと読む」不変条件(F1.3)を追加。

> v1.3 → v1.4(便 36 条件 4・裁定 37): **I-b∞ の逐語反映** — whitelist 禁止と即時 integrity stop の双方に「(N_∞) 枝の ĉ_μ(μ の norm 定数)の値・平方類・平方因子・符号」を追加(I-b∞: (N_∞) では (P1) ⟺ ĉ_μ ∈ K^{×2} — ĉ_μ 単独が封印予測を決める)。**μ/Pell ansatz の human-visible な探索は strict I-b∞ を守る sealed automation schema の事前登録なしに禁止**。(N_∞) 探索器が未設計の間は当該枝について「候補なし」と報告してはならず、既設二枝のみの探索は非網羅・全体結論 BRIDGE-UNKNOWN 維持を委嘱文に明記する。
> v1.2 → v1.3(便 32 P1/P3・裁定 31): 結果規則を total transition table 化(UNKNOWN+UNKNOWN 追加・REFUTED 新設 = 便 35 で批准済)・whitelist に Rule 1 I-b と同語の禁止を反映。

> v1.1 → v1.2(便 31 差戻しの全採用・裁定 29): ①fixture 実データ表(付録 A)の実体化を必須化(P1 — **実体化済: docs/manifest_k5_appendixA_v1.md**・K5-sq `a49252af…6716`・K5-ns `0ce28a6d…cd81`・K3-regression `70f2a604…9ed9`(sha256・機械計算)。付録 A 内の新設 tie-break 2 規則(代表 H の辞書式最小・σ₀ ラベル付け)は Sol 検収対象)②凍結 1 の時点を一意化・「または初期」削除(P2)③凍結 2 = 両翼 atomic joint freeze(P3)④formal a = 1 は永久不変・橋側捻れは b_sq/b_ns・比較指数 a_eff(P4 — v1.1 の「a ↦ ab⁻¹ 更新」は誤りとして撤回・裁定 29-2)⑤exact Kummer 証明書型(P5)⑥結果規則表と結果記録の分離(P6)⑦Model-Builder whitelist・u 二経路の独立性要件(P7)⑧即時 integrity stop 条件(P8)⑨S5 紙上 ansatz と Rule 1 要件(P9)。
> v1 → v1.1: falsifier 監査(F1・W1–W3・P1–P2)全採用。

## 宇宙(事前登録・変更禁止)

- 窓: K⁽⁵⁾ = ker ψ₅(= K⁽¹⁰⁾・Prop 3.4 — 独立二例として二重計上禁止)。P = G₅(位数 500)・M = 10・e = 5・𝔉₀ = C₅・K = ℚ(ζ₂₀)。
- 標的: **target_policy = all_two_classes**。Λ_sq(α ∈ {1,4})と Λ_ns(α ∈ {2,3})の二 fixture。標的 dessin: 次数 10・種数 2・ordered (10,2⁴1²,10)・Aut = 1(固定 U 上の ordered dessin の圏)。**結果を見て一方を捨てる = NO-GO**。
- 検出器: degree M = 10(μ₁₀-torsor)。degree 5 detector は SCHEMA-OUT(便 29 W3)。
- **fixture の実体(付録 A・必須)**: dessin ごとに fixture_id / marking_version((X,Y,Z) 正本と作用規約)/ H_generators(G₅ 固定座標での生成元列)/ perm_triple((σ₀,σ₁,σ_∞) ∈ S₁₀³)/ normalization_algorithm(同時共役の正規化と tie-break)/ **sha256(canonical serialization の digest — serialization 規約(UTF-8・改行 LF・配列順序)も付録 A に固定)**/ evidence_ids(node/GAP の検査項目と出力 artifact)を**値として**記載する。K5 finite fixture・K3 regression fixture も同形式で実体化。**付録 A が埋まるまで本 manifest は「凍結済み発射物」ではない**(便 31 F1.2・★教材 19: hash は書かれて初めて seal)。

## 五札封印表

| 札 | 内容 |
|---|---|
| **FORMAL-IN** | (0)(1)(2)(3a–d)(6′-i)(6′-ii) の証拠 ID(付録 A・dessin 別行)・命題 K5-1・j_i の定義・**封印値 a = j_ns⁻¹j_sq = 1(formal invariant・永久不変)**。(5′) は `PENDING`(結果は本ファイルでなく結果記録に書く — 下記)。結論との不一致 = proof/record consistency failure |
| **BRIDGE-IN**(凍結 2 で確定・dessin ごと) | 明示 ℚ-モデル式+hash・branch map(0,1,∞ ↦ X,Y,Z の actual conjugator の**完全な置換データ**)・全分岐 cusp・ℚ-有理 uniformizer(式)・局所助変数の式・FC 比較規約の版・**τ 由来一式**(原始根 ζ₁₀ := ζ₂₀² と K 内での表現・向き τ(ζ₁₀)(H′) = XH′X⁻¹・loop の向きと左右作用・Kummer cocycle を γ(s^{1/10})/s^{1/10} と読む規約・ρ₀ 側 generator と j: μ₁₀[5] ≅ 𝔉₀ の対応)・**b_sq, b_ns の機械記録**(下記)。**受理条件: b_sq = b_ns**(不一致は規約不整合として停止・u を開けない) |
| **BRIDGE-FAIL**(= B_FC の真の falsifier) | ①個別橋: BRIDGE-IN 独立成立下で actual G_K-置換と τκ の exact 不一致、または **(P1) の exact な破れ**(前件札が独立に閉じている場合 — (5′) の候補反例)②pairwise: 封印予測 (P2)/(5.5) の exact な破れ(両 BRIDGE-IN 成立時 —「少なくとも一方の (5′) が偽」までを主張し、どちらかは同定しない) |
| **BRIDGE-UNKNOWN** | 明示モデル・actual marking・局所比較・**exact Kummer 証明書**のいずれかを閉じられない — 値を推測せず UNKNOWN(探索失敗は判定でない) |
| **SCHEMA-OUT** | bad H(degree 5 detector)・非 regular・Λ 不安定・ρ₀ 非忠実。将来欄: 8\|n の K⁽ⁿ⁾ 一律(命題 K5-2b・K5e 機械裏取り済・裁定 27) |

- B5 の札は二段を維持: 形式 FAIL(M = 10 合成数)+ primary 分離で迂回 — PASS に塗り替えない。

## 規約捻れの型(v1.2 で全面差替え・裁定 29-2)

- 凍結 1 で決定式を封印: 各 dessin の凍結済み sheet identification c_i と正向き実 local monodromy ℓ_i に対し **c_i ℓ_i c_i⁻¹ = τ_i(ζ₁₀^{b_i})** — τ_i 単射より b_i ∈ (ℤ/10)^×(候補は 1,3,7,9 の 4 つ)は一意。右辺の巡回群に属さなければ actual marking 未閉 = BRIDGE-UNKNOWN。
- **formal invariant a = 1 は永久不変**(有限群側の封印・K5-1 の帰結)。橋側の記録は b_sq, b_ns と **a_eff = b_ns⁻¹ · a · b_sq**(別欄)。(P2) の一般形は [u_ns⁻¹]₁₀ = [u_sq⁻¹]₁₀^{a_eff} — ただし受理条件 b_sq = b_ns の下では a_eff = 1 で完全一致形に戻る。
- (ℤ/20)^× からの lift 2 対 1 は別封印項目として付録 A に記載。

## 封印予測(u 開示前・破れうる形で登録)

- **(P1)** ord([u_i⁻¹]₁₀) ∈ {1, 5}(i = sq, ns)。**exact な破れ(位数 2/10)は、前件札が独立に閉じていれば BRIDGE-FAIL 候補・どの前件が壊れたか未確定なら integrity quarantine**(新現象とも記録事故とも断定しない)。
- **(P2・主整合ゲート)** [u_ns⁻¹]₁₀ = [u_sq⁻¹]₁₀ in K^×/K^{×10}(b_sq = b_ns 受理下・生の u 一致は要求しない)。
- 観測列プロトコル(K3 v2 §6 継承): q_*[u] ∈ ⟨[2]⟩ の盲検記録(予測ではない・即時棄却規準あり)。

## exact 判定の証明書型(v1.2・便 31 F2.2/F2.3)

- v_i := u_i⁻¹。**位数 1 の陽性**: 明示 witness c ∈ K^× with c¹⁰ = v_i。**位数 5 の陽性**: c¹⁰ = v_i⁵ **かつ** v_i ∉ K^{×10} の exact obstruction(素イデアル valuation が 10 の倍数でない/単数・1 の冪根成分の exact obstruction/T¹⁰ − v_i の非可解の厳密数体証明書、のいずれか)。**探索失敗のみ = UNKNOWN**(浮動小数点 root search は証明書でない)。
- **(P2) 判定**: r := v_ns / v_sq^{a_eff} について r ∈ K^{×10} の witness(PASS)/ exact obstruction(FAIL)。二経路が同じ代表を返したことだけでは閉じない(W5)。
- **(5′) の量化子**: ∀γ ∈ G_K の恒等。有限個の Frobenius サンプル一致は較正であって PASS の証明でない — PASS は character 恒等の普遍的導出 or Kummer 拡大の厳密同定。FAIL は exact な γ 一つで足りる。

## 結果規則表と結果記録の分離(v1.2・便 31 F1.3/F6.1)

- **manifest は開示後も不変**。結果は別 versioned record `provenance/results_k5.md` に bridge_result_sq / bridge_result_ns ∈ {PASS, FAIL, UNKNOWN}(PASS には ord_i ∈ {5, 1} を付記)・pair_gate ∈ {PASS, FAIL, OPEN}・saturation_result ∈ {PROVED, **REFUTED**, NOT_PROVED} を保存し、凍結 manifest の digest を参照する。**REFUTED は v1.3 で司令塔が追加**(橋が閉じて ord = 1 なら fake shadow の存在 = 飽和の反証であり NOT_PROVED と区別すべき決着 — 便 34 で Sol 確認対象)。
- **結果規則(total transition table・v1.3・便 32 P1)** — 非順序対 {sq, ns} の全状態を尽くす:

| 状態(非順序) | pair_gate | saturation_result | 記録 |
|---|---|---|---|
| PASS(ord5) + PASS(ord5)・(P2)/(6.2) 一致 | PASS | PROVED | 完全決着 |
| PASS(ord5) + PASS(ord5)・(P2) exact 破れ | FAIL | NOT_PROVED | pairwise BRIDGE-FAIL(「少なくとも一方の (5′) が偽」— どちらかは同定しない)・integrity quarantine |
| PASS(ord5) + PASS(ord1) | FAIL | NOT_PROVED | 両橋閉鎖下では矛盾(両者とも Ih 像を計算しているため)⟹ integrity quarantine |
| PASS(ord1) + PASS(ord1)・(P2) 一致 | PASS | **REFUTED** | fake shadow の存在(反証側の決着 — 台帳は W3 三値の fake) |
| PASS(ord5) + FAIL | FAIL | PROVED | 存在型は成立・橋の dessin 非依存性は反証・FAIL 側を捨てない |
| PASS(ord1) + FAIL | FAIL | REFUTED | 同上(反証側) |
| PASS(ord5) + UNKNOWN | OPEN | PROVED | 存在型 witness・(P2) は「未検証」・両翼閉鎖まで campaign OPEN |
| PASS(ord1) + UNKNOWN | OPEN | REFUTED | 反証は片翼で数学的に成立・(P2) 未検証 |
| FAIL + UNKNOWN | FAIL | NOT_PROVED | 個別 bridge falsifier 記録 |
| FAIL + FAIL | FAIL | NOT_PROVED | pairwise falsifier 記録 |
| UNKNOWN + UNKNOWN | OPEN | NOT_PROVED | falsifier なし(便 32 F1.5) |

- 付則: (P1) exact 破れ(ord 2/10)は当該 dessin の bridge_result を確定させる前に integrity quarantine(前件札が独立に閉じていれば BRIDGE-FAIL 候補)。u 二経路不一致は結果を記録せず integrity stop。**「存在型の定理」「橋の普遍性」「全二類整合 campaign」は別出力**(W6)。

## BRIDGE-IN 構築の独立性(v1.1 設置・v1.2 強化)

1. **凍結 1(Rule 1)**: **両 dessin のいかなる個別モデル候補・係数・数値近似にも接する前・探索コマンドを一度も実行する前**に完了する(「初期」条項は削除 — W2)。内容: モデルの同値関係と正規形アルゴリズム・複数候補の全順序と tie-break・y の符号/基底三点/sheet numbering・cusp と uniformizer の決定アルゴリズム(**λ/t¹⁰ の定数項正規化は u を使うため禁止**・P₀ が Weierstrass 点か否かの分岐も先に書く)・「一意に決まらなければ UNKNOWN」規則・**u 二経路の数式・実装版・受理規則**・**b_i の決定式 (5.1)**・exact 数体/Kummer 判定器の版。
2. **凍結 2 = atomic joint freeze**: 両モデル・両 actual marking・両 uniformizer を**一つの bundle として同時に**凍結(★教材 20: 一翼を開く前に両翼を殺す)。片翼しか得られない場合は保存のみ・Extractor 起動は保留(片翼先行は別 manifest の別キャンペーン)。
3. **役割分離**: Model-Builder(A)の出力 **whitelist** — 許可: 明示モデル・Belyi map・分岐 divisor・cusp・uniformizer の式・target triple への exact conjugator(分岐指数 10 や uniformizer 性の証明は許可)。**禁止: λ/t¹⁰ の非零定数項とその同値物(leading coefficient・その valuation/class)、Rule 1 I-b と同語で「c の平方類・平方因子・符号の計算、λ の (c, μ) 対への分離報告」、および **I-b∞ と同語で「ĉ_μ の値・平方類・平方因子・符号の計算」(v1.4)**・それらを候補選択に使うこと**。A は「u 未計算」を申告し全 transcript 保存。**主根拠 = 凍結済み入出力 schema+役割別 access log・grep は補助検査**(W4)。Extractor(B)は凍結 2+発射錠後にのみ起動・規約変更権なし。
4. **u の二経路**(cusp 展開 × Vieta/単数): 非共有 helper・別中間表現・raw 出力の別保存・**一致判定のみを行う第三 checker**。不一致時は平均・符号調整・座標再選択を禁止し即 integrity stop / BRIDGE-UNKNOWN。
5. **hash commitment**: canonical serialization の digest・UTC/JST timestamp・commit ID・凍結対象の全ファイル一覧・**発射錠 FIRE_k5bridge.auth はこの digest 組に束縛(一回性・別 artifact へ再利用不可)**。

## S5 の紙上 ansatz(v1.2・便 31 F9 採録)

- Riemann–Hurwitz: 2g−2 = −20+(9+4+9) = 2・g = 2。divisor 恒等式を係数 ansatz より先に使う: (λ) = 10P₀ − 10P_∞・(λ−1) = 2Q₁+…+2Q₄+R₁+R₂−10P_∞・(dλ) = 9P₀+Q₁+…+Q₄−11P_∞。
- **紙上フィルタ**: [P₀−P_∞] ∈ J(C)(ℚ)[10] で **ord ∈ {5, 10}**(位数 1 は不可能・位数 2 は超楕円対合が λ を固定して Aut = 1 に反する)。
- **λ ∈ ℚ(x) と仮定してはならない**: 超楕円対合が deck 変換になり Aut = 1 に反する。**λ = A(x) + B(x)y, B ≠ 0** を許す(★教材 21)。二 dessin は同一曲線とは限らない — 「同時」は共同凍結の意味であり同一 ansatz の強制ではない。
- 凍結 2 に入れる受理物は exact のみ: 曲線方程式と Belyi map・divisor 恒等式・種数/分岐型・monodromy 群と exact conjugator・Aut(C/P¹) = 1・P₀/P_∞ と uniformizer。**数値近似や database label は discovery 用であり証拠でない**。

## 較正三層(発射前必須)

1. **K5 finite fixture**: 二類・passport・normalizer・regularity・K5-1・ρ₀(𝔉₀) = τ(μ₁₀[5])— 代表・置換三つ組・ρ_i・j_i・a = 1・証拠 ID・digest を付録 A に一表固定。
2. **K3 regression fixture**: 既知データ一体(モデル・branch・exact conjugator・cusp/uniformizer・その正規化での u = −4・ord = 3・τ/ρ₀/j の向き)を付録 A に実体化し、pipeline が**モデルから raw 再計算**で既知 class を再現。u = −4 は二者一致(厳密 blind independence は主張しない)— **回帰専用・「独立二経路の新証拠」へ札を上げない**。u′ = −256/729 は covariance control。
3. **covariance controls**: X ↦ X⁻¹(class 反転・位数/体不変)・s ↦ cs(u ↦ uc⁻¹⁰・class 不変)・τ ↦ τ∘[d]+Kummer character 逆冪(同時変換で (5′) 不変 — b_i と同じ型で実装し **formal a を書き換えない**)。

## 工程と発射条件

- **現在許可されている工程(便 31)**: S5 の紙上設計と凍結 1(Rule 1)文書の起草まで。**個別モデル探索は修正版凍結 1 の受理後・u 抽出は両翼共同凍結 2+発射錠後に限る**。
- 発射条件: ①付録 A 実体化+較正三層 PASS ②falsifier 計画監査(v1.1 で PASS・v1.2 差分は Sol 差分検収に含める)③Sol ゲート(差分検収)④FIRE_k5bridge.auth(digest 束縛・一回性)。
- **(v1.5・operative)** S5 探索の許容範囲: **既設二枝((W)/(N_aff))のみの positive-only 探索は非網羅**であり、委嘱文に「(N_∞) 枝は未探索・全体結論は BRIDGE-UNKNOWN 維持」を明記する。(N_∞) 探索器が S5 設計 §3.3.6 で「未設計」の間、当該枝について「候補なし」と報告してはならない。**μ/Pell ansatz を用いる探索は、strict I-b∞ を守る sealed automation schema の事前登録なしに人間可視で走らせてはならない**。実 K5 の Freeze 2 では両 driver が**同一 atomic frozen bundle の canonical model JSON を係数ごと読む**(digest のみ読取り+係数別転記の運用は禁止 — 便 38 F1.3)。
- 算術全射性の宣言は (4d)(5′)+exact Kummer 証明書の閉鎖まで禁止。

## 即時 integrity stop(期限を待たない・v1.2)

凍結 1 前の個別候補接触/凍結 2 前の u または同値 leading class の漏洩(**同値物は I-b・I-b∞ と逐語同一: c および ĉ_μ の値・平方類・平方因子・符号・(c,μ) 分離報告** — v1.4)/hash・serialization・発射錠対象の不一致/両翼共同凍結前の片翼 u 開示/モデル検査二系統の不一致/u 二経路の不一致/b_i が一意に決まらない・受理規約 b_sq = b_ns の破れ/K3 regression・covariance control の失敗/exact Kummer 証明書なしの PASS/FAIL 宣言。**漏洩 run は後から同じ規則を hash して救済しない** — 汚染 artifact を隔離し、規則を変えるなら新 version の campaign とする。

## 撤退条件(先に書く)

明示 genus-2 モデル(二 dessin とも)が **暦日 2026-08-10 まで、または S5 実装委嘱 8 回のいずれか早い方**(委嘱 = 委嘱 ID を付した 1 発注・失敗/timeout/再走も 1 回に数える・片翼のみ取得も「両翼未閉鎖」として期限発火)で得られない場合、BRIDGE-UNKNOWN のまま**保留**し、資源を奇数族の別窓・Lean・論文線へ移す。
