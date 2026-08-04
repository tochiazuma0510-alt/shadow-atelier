# HS 本走(NW(7) 悉皆 705,894 対)— 事前登録票(v1・草案)

- 起草: 実装担当(短命)・2026-08-05
- 委嘱: 司令塔(「HS 本走の事前登録票の起草 — 走らない・便 104 で正式申請するための認可資料」。便 103 F103-1.3「認可資料の準備・事前登録段階へ進むことは可」の履行分)
- 位置づけ: **本票は事前登録の草案であり、認可済みの実行文書ではない。** 走行・列挙・GAP 実行は一切行っていない。本票が確定しても、実行は便 104 で Sol の認可を得てから(`docs/notes/hsp7_cond4_lanespec_v1.md` §10、以下 lanespec §10)。
- 正本参照: lanespec v1.2(`docs/notes/hsp7_cond4_lanespec_v1.md`)§10・`sol/sol_reply_103_math30.md` §1(F103-1.1〜1.3)・`docs/notes/hs_prop7_translation_v1.md`(以下 翻訳ノート)§8.7.3・§8.7.7・§9・`search/certs/hsp7_cond4_summary_v2_addendum_immutref_20260805.json`(不変参照の様式)

---

## 0. 認可境界(不変・lanespec §10 の再確認)

> ★★ lanespec §10 逐語: 「本章は再前哨の審査対象外であり、前哨通過は本章の内容に対するいかなる承認も与えない。」「本節は発注しない。」

本票は lanespec §10 が要求する前提条件 (a)〜(d) のうち、**本走の宇宙・述語・停止規則・解釈規約を紙面で確定する作業**(準備)を行う。(a)「窓内悉皆列挙が P101-1 の言う『shadow 全掃引』に該当するか」の一行確定・(c)「§7 完全性主張の選び直し」は**未確定のまま Sol へ申請文で問う**(司令塔単独では決められないという lanespec §10 の指示どおり)。本票の発効・実行認可は Sol の便 104 回答を待つ。

---

## 1. 宇宙の凍結

### 1.1 対象窓(不変・翻訳ノート §8.7.3 定義 NW(p)、p=7 固定)

- $\mathbf N=\mathcal V(F_2)\times\langle c\rangle$(主標的)、$\mathbf N_0=\mathcal V(F_2)\times\langle c^7\rangle$(control)。$N_{F_2}=\gamma_5(F_2)F_2^{\,7}$。$W=\gamma_5(K(0,5))K(0,5)^{\,7}$。$P=F_2/N_{F_2}$、$Q=K(0,5)/W$。
- 発火条件 2(NW-P1〜P5)により実測確定済み(`search/certs/hsp7_cond2_p7_20260804.json`、翻訳ノート §9.6 で Sol PASS 済): $|P|=7^8=5{,}764{,}801$、$|[P,P]|=7^6=117{,}649$、$N_{\rm ord}=7$、$|\mathcal X_{\mathbf N}|=6$。**これらは NW-P2/P3/P5 の実測値であり、本走はこの値を再登録するのみで再測定しない**(S-7′ が既に閉じている領域を再度不安定化させない)。

### 1.2 候補対の全数(705,894 の導出・機械再計数の手順)

$$
\underbrace{|\mathcal X_{\mathbf N}|}_{6}\ \times\ \underbrace{|[P,P]|}_{117{,}649}\ =\ 705{,}894
$$

- $m\in\mathcal X_{\mathbf N}=\{m\bmod 7:\gcd(2m+1,7)=1\}$ の 6 元(翻訳ノート §8.7.3 補題 NW-1b (4))。
- charming $\bar f\in[P,P]$ の全域(翻訳ノート脚注「charming は $[F_2/N_{F_2},F_2/N_{F_2}]$ で列挙 — 罠 #6」)、$|[P,P]|=117{,}649$ 個(全域、部分集合ではない)。
- **機械再計数の手順(発注時に走らせる最初のステップとして事前登録)**: pc presentation で $P$ を構築 → `Size(DerivedSubgroup(P))` で $|[P,P]|$ を実測 → $\mathcal X_{\mathbf N}$ を $\gcd(2m+1,7)=1$ で 0..6 を篩って実測 → 積が $705{,}894$ と一致することを機械確認する。**一致しなければ S-7′(§3)が直ちに発火し、本走は開始しない**(数値 705,894 を紙の予言として先に固定し、実測が一致するかを事前登録された仕様どおり検査する — 罠「指数一致を settled 証明に使わない」への対応として、$|[P,P]|$ の一致は candidate 母集団の確定に使うのみで、genuine 判定の根拠には使わない、§4 参照)。

### 1.3 三レーン+Σ の同一構成(較正済み評価器の versioned 束縛)

本走は較正走(lanespec §1・§6)で発注・cross-checked 格付け済みの **同一 driver コード**を、悉皆列挙用の入力ループで包むのみとする。**判定ロジックを較正走から一切変更しない**(§2 で digest 拘束)。

| レーン | 較正走での cert(発注済・PASS 格付け) | 本走で束縛する driver |
|---|---|---|
| Lane S | `search/certs/hsp7_cond4_laneS_20260804.json` | 同 driver、入力ループのみ悉皆化(13 件 → 705,894 対) |
| Lane V | `search/certs/hsp7_cond4_laneV_v3_20260804.json`(F103-1.2 が pin) | 同上 |
| Lane P | `search/certs/hsp7_cond4_laneP_20260804.json` + `hsp7_cond4_laneP_p5control_20260805.json`(NW-P7 発効済) | 同上 |
| Lane Σ | `search/certs/hsp7_cond4_summary_v2_20260805.json` + addendum | 同一機械合成スクリプト、入力が 3×705,894 件になる分の集計ロジックのみ拡張(新規判定基準の追加は禁止、lanespec §7 D-3①) |

- **digest 列挙(発注時に本票へ追記する空欄)**: 各 driver スクリプトの SHA-256 を本走発注 cert の `frozen_driver_digests` に記録し、較正走 cert の digest と**バイト同一であることを機械確認**してから本走を起動する。不一致なら S-7′ 相当で停止(較正走と異なるコードで本走をしていないことの担保)。

---

## 2. 判定述語の凍結

- **hexagon(簡約 (3.10)(3.11) を $\mathbf N$ で・full (3.3)(3.4) を $\mathbf N_0$ で)**: 翻訳ノート §8.7.4〜§8.7.5(定義 DUM-FIN・補題 DUM-HEX)・定義ノート (3.3)(3.4) 逐語(lanespec §1 ★ R-19 pin)。較正走と**同一 code path**(Lane S/V の driver をそのまま流用、判定関数に手を入れない)。
- **PENT_W**: lanespec §1 Lane P の定義式($\bar\rho^4(\bar f)\bar\rho^3(\bar f)\bar\rho^2(\bar f)\bar\rho(\bar f)\bar f=1$ in $Q$)を逐語で継続。K(0,5) の構成は stage1-2 のみ継承(lanespec §2 表・★司令塔修正済み)。
- **変更ゼロの digest 拘束**: 上記 §1.3 の driver digest 一致確認がこの節の実装形。**較正走と本走で判定述語のコードが 1 バイトでも違えば、それは本票が拘束する「較正済み評価器」ではなくなる** — その場合は本走を始めず、差分を数学者・falsifier へ差し戻す。

---

## 3. 停止規則

較正走の停止規則(lanespec §6・翻訳ノート §9.4)を本走スケールへそのまま拡張する。**新規則は追加しない**(悉皆化に伴い規模のみ変わる)。

```jsonc
"stop_rules_mainrun": {
  "S-6":   { "trigger": "NW-P3 または NW-P5 が偽(再測定時)",
             "verdict": "TARGET_PREMISE_BROKEN / STOP",
             "note": "p=7 本走を止める。p=11,13 への移送判断は司令塔(翻訳ノート §8.7.7)" },
  "S-7'":  { "trigger": "本走冒頭の機械再計数(SS1.2)で |P|,|[P,P]|,N_ord,|X_N| のいずれかが較正走の実測値と不一致",
             "verdict": "PREREGISTRATION_FALSIFIED / INTEGRITY_STOP",
             "note": "即時停止・部分結果は保存・同一run内で予言を書き換えない・別version事前登録から(S-7' 正本、翻訳ノート SS9.1)" },
  "S-9":   { "trigger": "同一窓上で Lane S と Lane V の項目別判定(705,894件のいずれか1件)が食い違う",
             "verdict": "LANE_DISAGREEMENT / INTEGRITY_STOP",
             "note": "多数決・片方優先の自動解決をしない。3レーン全体のcert発行を停止する(lanespec SS6 逐語の悉皆版)" },
  "S-8'":  { "trigger": "NW-P8 の完全形(全 X_N x 全 705,894 候補)で N と N0 の判定不一致が0件",
             "verdict": "CALIBRATION_FAILED / INTEGRITY_STOP",
             "note": "較正走の縮小scope(m-sweepのみ)ではなく本走で初めて評価される完全形。発火は縮小scopeと異なり『完全な不一致0件』という強い事実であり、後から期待値を弱めない(翻訳ノート SS9.3 の完全形)" },
  "S-3":   { "trigger": "NW-P7(p=5 control、既発効)が本走の枠内で再検査され5元中5元PASSでなくなる",
             "verdict": "IMPLEMENTATION_BUG_SUSPECTED / STOP",
             "note": "control が本走スケールのコードでも保たれることの再確認。崩れれば較正走からの digest 不一致を疑う" }
},
"timeout_and_unknown_budget": {
  "per_candidate_timeout": "<発注時に司令塔が具体値を確定・付録Cで事前登録(較正走13件の実測所要時間から外挿)",
  "unknown_recording": "UNKNOWNはPASS/FAILと同格の三値の一つとして705,894件の分布表に記録する(棄却・再試行での握りつぶし禁止)。UNKNOWNの理由(timeout/pc群評価失敗/代表元取り直し要)を候補ごとに併記(lanespec R-13)",
  "unknown_rate_gate": "UNKNOWN率が付録Cの事前登録閾値を超えたら計算資源の問題として一旦停止し司令塔へ報告(数学的停止規則ではなく運用停止)"
},
"prediction_source": { "frozen_at": "<本票 SS1 の digest>", "codegen_uses_expected_values": false }
```

- **S-7′・S-9・S-8′・S-3 は撤回後の逆向き形として、より弱い予言へ書き換えることを恒久的に禁止**(翻訳ノート §9.1〜§9.3 と同型の禁止列挙をそのまま適用)。
- **timeout/UNKNOWN の具体的な閾値(秒数・件数上限)は本票では確定しない**(付録 C・空欄) — 較正走 13 件+NW-P7 5 件の実測所要時間(lanespec §9 予算表「数十秒オーダー」)からの外挿は Sol へ申請前に数学者/miner が実測して埋める。**この空欄が埋まっていない状態では便 104 は発送できない**。

---

## 4. 結果の解釈規約(事前固定)

- **hexagon-PASS ∧ PENT-FAIL の対**: 「**A 型 fake 候補**」として**記録のみ**する。genuine 判定・存在主張は一切しない(裁定文書の警告「PB₃/N を安易に直積分解しない」「GAP の部分群比較でなく marked factor map を使う」を踏まえ、fake/genuine の弁別は別途 Sol ゲートの数学的検討事項とし、本走はラベル付けと分布集計のみ行う)。
- **hexagon-PASS ∧ PENT-PASS の対**: 「候補(candidate)」として記録。**genuine の主張はしない**(較正走の格付け=cross-checked はここまで、Lean verified ではない、を維持)。
- **hexagon-FAIL の対**: PENT 側は評価してもしなくてもよい(§8.3.3 と同型、hexagon 側の非 exact さのみで足りる)。UNKNOWN 込みで 4 区分(PASS/PASS, PASS/FAIL, FAIL/PASS, FAIL/FAIL)+UNKNOWN 絡みの表を作る。
- **全数の分布表の様式(事前登録)**:

  | 区分 | 定義 | 集計欄 |
  |---|---|---|
  | hex-PASS ∧ PENT-PASS | 候補(candidate、genuineではない) | 件数・m別内訳 |
  | hex-PASS ∧ PENT-FAIL | A型fake候補(記録のみ) | 件数・m別内訳 |
  | hex-FAIL | (PENT側は付随情報) | 件数 |
  | いずれかUNKNOWN | 理由別内訳 | 件数・理由(timeout/pc失敗/代表元) |

- **予言は構造量のみ**(事前登録する予言の範囲を明記): 予言してよいのは「候補数の再現」(§1.2 の 705,894 という母集団サイズ、および NW-P6/NW-P5 が既に予言する $t=0$ 一点 PASS のような**構造的**帰結)までであり、**discovery 側(hex-PASS∧PENT-PASS の実件数・A型fake候補の実件数)は予言しない**。これらは本走で初めて測る量であり、事前に数値を書けば「予言 ⇔ 実測」の照合が恒等的に PASS になる事故(翻訳ノート §9.2 の批判)を繰り返すことになる。
- **完全性主張(lanespec §10 (c) の未確定事項)**: 較正走は選択肢(iii)「候補ごとに Lane S と Lane V の判定が二系統で一致する」までしか書かない、と決めていた(lanespec §7)。本走でこれをどこまで拡張するか——「全 705,894 件で Lane S/Lane V が一致した」という主張が「悉皆性(全数を尽くした)の主張」まで含意してよいか——は**本票では選び直さない**。Sol への申請文(§6)でこの一点を問う。

---

## 5. 不変参照(commit/blob/sha256 三つ組で pin)

`search/certs/hsp7_cond4_summary_v2_addendum_immutref_20260805.json` の様式に倣い、依拠する主要 artifact を作業ツリーの可変 path でなく commit 時点の blob で固定する。HEAD commit `f76be7eddbd6c7a098f348d3f02429e756a5d691` 時点で機械確認した値(`git ls-tree` + `git cat-file blob` + `sha256sum`、手写しではない):

| artifact | commit | blob | sha256(全体バイト) |
|---|---|---|---|
| `docs/notes/hsp7_cond4_lanespec_v1.md`(v1.2) | f76be7eddbd6c7a098f348d3f02429e756a5d691 | 88544a6b04b11b84954ae4a3c73b186725c6354a | bd5a9da2fb2454d5bff190cb0ffc364d933b4a4923c3b4f73dc8438e7cb8e188 |
| `sol/sol_reply_103_math30.md` | f76be7eddbd6c7a098f348d3f02429e756a5d691 | fc289331673b5011424a73363820e44a26b2bd55 | 9f6ab0edb2bd68f280f3721647ff7e8a76dce5a47c4df6bdf475ca126419b2be |
| `search/certs/hsp7_cond4_summary_v2_20260805.json` | f76be7eddbd6c7a098f348d3f02429e756a5d691 | f5dba96aa80144555375751b05b759ca1d149b98 | 467e4d41ba704af1aa055698aeb1c71215ecc5906ed9ea1a4b2a98177dc6e0b8 |
| `search/certs/hsp7_cond4_summary_v2_addendum_immutref_20260805.json` | f76be7eddbd6c7a098f348d3f02429e756a5d691 | d8f4969951833b2764a11da858209de71a7a4745 | e71c27c936dd944f7390581e9c2b80b84605984d6e3bc511c9c67bb8240c659a |
| `search/certs/hsp7_cond4_laneP_p5control_20260805.json`(NW-P7 発効・F103-1.1 PASS) | f76be7eddbd6c7a098f348d3f02429e756a5d691 | 3c07e3faed94eb643c940e74750ede3437a86310 | bca2e8cf61302a7307622eca7185b6c3344c53791469b96660a3b97caa77d9ad |

- `search/certs/hsp7_cond4_summary_v2_20260805.json` の sha256(467e4d41...)は addendum が pin した値と一致(§0 の addendum が自ら記録した「本体不改変」の再確認)。
- `sol/sol_reply_102_math29.md` への参照は addendum 自身が pin した三つ組(commit `468287e1c3f12b124da94b2e925936d4854ebfb0` / blob `eca5dc71854123acfaf333bcb3e2d7afc089e041` / sha256 `2ebf7c5e63a41b8989719823527a6f18bb2c5614435bf25a08340080060fa8e7`)をそのまま継承する(本票が新設しない、addendum 経由で再利用)。
- **本票自身も発効(便 104 で versioned 発効)されたら、同じ commit/blob/sha256 三つ組で以後の cert から参照されること**(可変 path 経由の参照を今後発生させない)。

---

## 6. Sol への申請文(便 104 同梱形・実行認可の請求)

### 見出し(便 104 本文にそのまま立てる節構成)

1. **本走認可の請求**: NW(7) 窓内 charming 候補の悉皆列挙(705,894 対、m×[P,P] の全域)+3 レーン+Σ による hexagon/PENT の全数判定の実行認可。認可の根拠として本票(v1)を添付。
2. **F103-1.3 前提の履行報告**: sol_reply_102_math29.md の不変参照(commit/blob/sha256 三つ組)を addendum 経由で固定済み、Sigma v3 相当の source-pin 修理は addendum artifact をもって完了、と申告。
3. **監査点 3(lanespec §10 (a))**: 「窓内悉皆列挙」が P101-1 の言う「shadow 全掃引」に該当するか、一行確定を請う(該当するなら本走はそもそも P101-1 の禁止範囲に触れないかの確認が要る/該当しないなら本票の認可請求が正しい対象であることの確認)。
4. **監査点 4(lanespec §10 (c))**: 完全性主張の選び直し — 本票 §4 末尾の未確定一点(全数一致の主張を「悉皆性の主張」まで含意させてよいか)への裁定を請う。
5. **監査点 5(lanespec §10 (d))**: 較正スイート v2 項目 3(source kernel 証明書=「個数一致・指数一致では不足」)との整合 — 本票 §1.2 の $705{,}894=6\times117{,}649$ という個数一致・指数一致を genuine 判定の根拠に使っていないこと(§4 で候補ラベリングのみに用途を限定していること)の確認を請う。
6. **未確定事項の開示**(発送前に埋めるべき空欄、正直に申告): §3 timeout/UNKNOWN 予算の具体値(付録 C)が未確定。数学者/miner による較正走実測時間からの外挿を待って便 104 本文に確定値を記載する。

---

## 付録 C. timeout/UNKNOWN 予算(空欄・発注前に確定)

| 項目 | 値 |
|---|---|
| 候補1件あたりの timeout | 未確定(較正走13件+NW-P7 5件の実測所要時間から外挿予定) |
| UNKNOWN率の運用停止閾値 | 未確定 |
| 全体の計算時間cap | 未確定(lanespec §9 の GAP `-o 2g` 制約下での見積りが要る) |

以上、本票は草案(v1)。走行・列挙・GAP 実行は行っていない。便 104 発送前に付録 C を埋め、司令塔が §0〜§6 の内容を最終確認すること。
