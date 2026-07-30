# 出所台帳 (Provenance Ledger)

すべての入力・ソフトウェア・証明書のハッシュと版をここに記録する。追記のみ(過去のエントリは書き換えない)。

## 2026-07-18 — フェーズ 0: 文献入手

arXiv から PDF を取得(`curl -sL https://arxiv.org/pdf/<id>`)。SHA-256:

```
be6afb208b09d79716119fcb479bf74175a1c0ade1fa47d6c9727b01aa2d8f52  papers/2106.06645-gt-shadows-childs-drawings.pdf
4e0a29e19825810eb9db24ebda120a6805c42fee4eb51679d409c5437e0943ab  papers/2401.06870-gt-shadows-gentle-version.pdf
dafa86c0f9e475800067a27dfeaaf7ef38abfdc66a5686579af6c5b9e3a1bcf3  papers/2405.11725-nonabelian-quotients-gt-elementary.pdf
```

- 2106.06645 — Dolgushev–Guay-Paquet–Orr, *The Action of GT-Shadows on Child's Drawings*(実装の入口)
- 2401.06870 — *GT-shadows for the gentle version of GT*(定義の正本)
- 2405.11725 — *Accessing non-abelian quotients of GT via elementary tools*(dihedral 予想の明示)

注意: arXiv の PDF は版更新でハッシュが変わりうる。上記は取得日時点の最新版。取得日: 2026-07-18。

## 2026-07-18 — フェーズ 0: GAP

- GAP **v4.16.0** Windows installer(`gap-4.16.0-x86_64.exe`, 807,634,402 bytes)
- 取得元: https://github.com/gap-system/gap/releases/download/v4.16.0/gap-4.16.0-x86_64.exe
- SHA-256 検証: **一致** — `0e72ae5021d3a9b1303dbe762ed66aa85c9310f4ddc46cb722e51c9db6a7f323`(公式 .sha256 と照合、2026-07-18)
- インストール先: `C:\Program Files\GAP-4.16.0`(Inno Setup、サイレントインストール。`/DIR` 指定は無視された)
- 動作確認: `search/smoke-test.g` PASSED(GAPInfo.Version = 4.16.0 / B₃ の有限表示 / B₃↠S₃ / D16・D6 / 軌道計算)
- 実行方法: プロジェクト直下の `gap.ps1`(`gap.bat` は別窓を開くため自動実行に不向き)

## 2026-07-18 — フェーズ 0: 補助ツール

- poppler **25.07.0**(winget `oschwartz10612.Poppler`)— PDF テキスト抽出・レンダリング。
  - 既知の問題と対処: 同梱バイナリがシステムの古い VC++ ランタイム(14.13)でクラッシュ(0xC0000005)。Edge 同梱の x64 ランタイム DLL(14.50)を poppler の `Library\bin` にコピーして解消。その後システム側も VC++ 14.51 に更新済み。
  - `papers/txt/` のテキスト版はこの poppler で抽出(`pdftotext -layout`)。
- Microsoft VC++ 2015+ x64 Redistributable: 14.13.26020 → **14.51.36247** に更新(winget)。

## 2026-07-18 — Week 1: 定義系のスポット照合(Task #4)

- 抽出ノート 3 本(`docs/notes/`、読解エージェント作)に対する司令塔の独立照合:
  - ページ画像照合 4 か所: 2401.06870 p.10(hexagon (3.3)(3.4)・N_ord/N_F₂)/ 2405.11725 p.13(ψₙ (3.1)・K⁽ⁿ⁾・逆射)/ p.18(Thm 4.3 の (4.12)・𝒳ₙ・ϰ・isolated)/ p.23(Conjecture 5.1 全文)— **すべて一致**。
  - GAP 独立検算: `search/week1-kn-spotcheck.g`(GAP 4.16.0)— |Gₙ| = 4n³/4(n/2)³(n=3..12)・K_ord = lcm(n,2)・K⁽ⁿ⁾=K⁽²ⁿ⁾(n=3,5,7,9,11)— **ALL PASSED**。慣習: Dₙ³ は置換の左作用・rs は「s のち r」で実装(Sol 便 01 で裁定予定)。
- 統合版: `docs/week1-定義ノート.md` v1(状態: Sol 定義ゲート待ち)。

## 2026-07-18 — Week 1: 追加ツール・第三者資源

- **Python 3.13**(winget `Python.Python.3.13`)— 検証器第二系統+パッケージ GT 実行用。
- **Dolgushev パッケージ GT**(B₄ 系の第三者実装・SymPy 製):
  ```
  c3124483cb1464b9010c091011370db091a76561a2af923a38efb6900f645f95  thirdparty/packageGT/PackageGT.zip
  90545f5ea820b41c8bb16c5719c2540d39207f5247a4649fc4d784f1612468f1  thirdparty/packageGT/PackageGT_README.pdf
  ```
  取得元: https://sites.temple.edu/vald/files/2024/05/ (2026-07-18)。thirdparty/ は git 管理外。

## 2026-07-18 — 較正スイート v2: 宇宙の事前登録(Task #5)

計算開始前に対象を固定する(後から広げる場合は新しい版として追記):

- **dihedral 対象**: K⁽ⁿ⁾ = ker(ψₙ)、n ∈ {3,…,16} ∪ {18, 36}(18, 36 は reduction branch suite (q,n) = (36,12), (18,3) の q 側のため)。生成系は 2405.11725 (3.1) の ψₙ(x₁₂)=(r,s,s), ψₙ(x₂₃)=(rs,r,rs), ψₙ(c)=1 に固定。慣習: 置換は左作用、rs は「s のち r」(GAP では s*r)— Sol 便 01 で裁定済み。fixture: z̄ = (r²s, r⁻¹s, r)。
- **control 対象(c ≠ 1)**: N₅ = ker(β₅)、β₅: B₃ → S₃×C₅、σ₁ ↦ ((12), t), σ₂ ↦ ((23), t)(Sol 便 01 提案・採用)。B₃/N₅ の位数 30、PB₃/N₅ ≅ C₅、N_ord = 5、期待 |GT(N₅)| = 4(独立に計算で確認する — 期待値に合わせにいかない)。
- **検証項目**: docs/week1-定義ノート.md §4 の 8 項目(v2)。
- **探索器/検証器**: 探索 = GAP 4.16.0、検証 = node v24(helper 非共有)。証明書は JSON(形式は WP2 で設計し本台帳に追記)。
- **cap(超過時は保留して報告)**: 1 対象の shadow 候補列挙 ≤ 10⁶、GAP 1 スクリプト実行 ≤ 10 分。

## 2026-07-18 — 較正スイート v2: WP1 実行記録

- `search/suite-wp1.g`(GAP 4.16.0・implementer=sonnet 実装・司令塔が再実行で再現確認)— **WP1 ALL PASSED**。
  - 項目 1 完走: n ∈ {3..16, 18, 36} の |Gₙ|・K_ord 全 PASS、doubling K⁽¹³⁾=K⁽²⁶⁾・K⁽¹⁵⁾=K⁽³⁰⁾ PASS。
  - Prop 3.5: **全 256 順序対**で数論式 ⟺ marked factor map が一致(不成立 212 対はすべて fail を返すことも確認)。branch suite 5 対 個別 PASS。
  - N₅ control: |B₃/N₅| = 30、N_ord = 5、**GT(N₅) = {m = 0,1,3,4}(計算値・Sol 予想と一致)**、T(c) = c^{2m+1} 全通過。
  - **新規の観測**: N₅ では raw hexagon (3.3)(3.4) が m = 2 を含む全 m で成立し、m = 2 を落とすのは単元条件と全射性のみ(可換 control では hexagon が実質空回りし、charming 側が制約を担う)。atlas 向けの小データ点として記録。
- **宇宙の補助拡張(透明化)**: doubling 検査のため G₂₆・G₃₀ を一時構成(week1-kn-spotcheck.g の前例と同型の補助であり、研究対象としての登録ではない)。
- 状態: 以上はすべて GAP 単系統 = **candidate**(照合器通過で cross-checked へ)。

## 2026-07-18 — 較正スイート v2: WP2 統合実行記録(二系統照合)

- **探索器**: `search/suite-wp2-explorer.g`(K3..K16+N₅)+ `search/suite-wp2-explorer-q1836.g`(K18, K36 — 10 分 cap 順守の分割)。GAP 4.16.0(-o 2g)。implementer(sonnet/medium)実装・司令塔コードレビュー済み(fixture 釘付け・[ANOMALY] 規律・(4.11) 事前検査を確認)。
- **照合器**: `crosscheck/check.mjs`(node v24・依存ゼロ・GAP 非依存の独立実装)。司令塔コードレビュー(指摘 F1〜F5 修正済み)+司令塔再実行で再現確認。
- **結果: 証明書 17 通(K3..K16, K18, K36, N₅)すべてで照合器の全検査項目 PASS = cross-checked**。
  - shadow 数の実測: |GT(K⁽ⁿ⁾)| が Thm 4.3/4.6 の閉じた式と全 n で一致(2 冪 n=4,8,16: 4/16/64。K18: 108、K36: 216 — 司令塔が指示文に書いた参考値 48 は暗算誤りで、探索器は正しく計算値を報告した)。
  - reduction branch suite 5 対((8,4),(12,4),(9,3),(18,3),(36,12))全射性込みで PASS。LS witness は 3|n の全対象(K3,K6,K9,K12,K15,K18,K36)で (5.1) 両式 PASS(読者委任の m ≡ 2,3 mod 6 含む)。
  - N₅ control: (3.3)(3.4) の c^m 項・T(c)=c^{2m+1}・brute kernel 手続き・charming(f=1)明示検査まで PASS。
- 証明書 SHA-256(先頭 16 桁): `provenance/cert-hashes-wp2.txt`。
- **残ギャップ(達成宣言前に Sol 便 02 で裁定を仰ぐ)**: (a) reduction の関手性 (5.3) は単段 5 対で被覆し、合成鎖(例 K36→K12→K4 vs 直接)は未検証。(b) Thm 4.6 の明示同型 ϱ は独立項目でなく、合成表 ≡ (3.53) 再計算+(4.19)(4.20) 恒等式経由で担保。

## 2026-07-19 — Sol 便 02 の条件閉鎖(Luna 便 02/02b+司令塔統合)

- **Luna 便 02**(gpt-5.6-luna/high・初起動): 照合器の fail-closed 化(仕様 A)・N₅ node 全列挙と T(c) 直接比較(仕様 B)・代表元不変性/θτ 全単射(仕様 D4-5)・ϱ 明示同型+非可換 witness(仕様 E)を実装。GAP はサンドボックス制約(signal pipe 不可)で実行不能 → 正直に UNKNOWN 報告。
- **Luna 便 02b**: global sweep を最適化(source Cayley の一回構築・整数エッジ)し **576 秒 → 3.5 秒**。256/256 対(不成立 212 対の collision 全検出)・doubling 7/7・numeric 16/16 PASS。`--cap` フラグ追加。受理条件を単射性→**井戸定義性**へ修正(商写像の存在条件として正当 — 司令塔追認)。
- **司令塔**: 改修探索器 2 本を再実行(主 687 秒 — **10 分 cap を 14% 超過、次回から分割**。q 側 448 秒)。K36 に K4 直接エントリ・N₅ counts 5/5/4/4 を正規再生成。照合器フル再実行 → **全 verdict 18/18 all_pass(三角形 216/216・GLOBAL ALL PASS)**。証明書ハッシュ再記録(再生成による全対象更新)。
- ops 修理 1 件: `codex exec resume` は --sandbox 非対応(exit 2)— wake から除去(コミット済み)。
- 台帳: C-1 の gate 保留解除・C-1b/C-2 を cross-checked へ再昇格・C-5 条件全閉鎖。

## 2026-07-19 — 探索器 10 分 cap 順守: 決定的 shard 分割(implementer 実装)

- **背景**: search/suite-wp2-explorer.g(n=3..16+N5 一括)が実測 687 秒で cap を 14% 超過(前エントリ記録済み)。今回、決定的 shard 分割で再実行(実装者 = implementer/sonnet)。q 側 search/suite-wp2-explorer-q1836.g(448 秒・K18,K36)は無変更のまま。
- **shard 分割(対象集合の分割のみ、計算内容・出力形式は無変更)**:
  - `search/suite-wp2-shard-a.g`(n=3..12): **205.6 秒**(GAP 内部 193860 ms)。reduction branch suite 3 対((8,4),(12,4),(9,3))もここに含む(全 n が 3..12 に収まるため)。
  - `search/suite-wp2-shard-b.g`(当初案: n=13..16+N5 一括): **897.2 秒(GAP 内部 877922 ms)— cap を大幅超過**。原因観察: n=13(shadows=312, composition_table 最大約 312×312=97344 組)の JSON 文字列組み立てが支配的と推定(処理自体は 267.5 秒、残り約 610 秒が JSON 書き出し側)。このファイルは証拠として無変更のまま残す(生成した K13..K16,N5 は結果的に正しい・ハッシュ一致済み)。
  - 上記を受けさらに分割: `search/suite-wp2-shard-b1.g`(n=13,14)・`search/suite-wp2-shard-b2.g`(n=15,16+N5)。
    - shard-b1(n=13,14): **612.0 秒(GAP 内部 596625 ms)— 10 分 cap をなお超過**。内訳計測(スクリプトに時刻打刻を追加): n=13 ProcessDihedral = 148.1 秒、n=13 の JSON 直列化(composition_table 含む)単独で **437.5 秒**。n=14 側は軽微(ProcessDihedral 8.9 秒、JSON 直列化差分 2.1 秒)。**n=13 単体だけで概算 585.6 秒(GAP 内部)+ GAP 起動オーバーヘッドを要し、対象集合をこれ以上分割しても(n=13 が単一対象のため)cap を安定して満たせない可能性が高い**。根本原因はヘルパー関数 JoinC の文字列連結が `Concatenation` の逐次呼び出し(O(list長²))であることと推定(未確定・司令塔判断待ち)。
    - shard-b2(n=15,16+N5): **243.4 秒**(GAP 内部 231344 ms)— cap 内。
  - **宇宙分担の和の検証**: shard A {3..12} + shard B1 {13,14} + shard B2 {15,16}+N5 + q1836 {18,36} = {3..16,18,36,N5} = 事前登録宇宙(`provenance/LEDGER.md` 2026-07-18 較正スイート v2 エントリ)と exact 一致。宇宙は拡大・縮小していない。
- **ハッシュ照合(決定性の検証)**: 全 shard 実行後、certificates/*.v1.json 17 件の SHA-256 先頭 16 桁を再計算 → `provenance/cert-hashes-wp2.txt` の記録値と **17/17 一致**(K3..K16, K18, K36, N5)。K18/K36 は今回再生成していない(q1836 は無変更のため既存ファイルのハッシュのみ確認)。差分ゼロ。
- **未解決の懸念(司令塔判断が必要、実装者からの報告)**: shard-b1(n=13,14)は 10 分 cap を超過したまま。n=13 単体の JSON 直列化コストが支配的要因で、これは「対象集合の分割」では原理的に解消できない(n=13 は単一対象であり、これ以上細分化する対象がない)。選択肢の例(実装者は判断せず提示のみ): (a) JoinC を線形時間の実装に置き換える(出力は不変のはずだが「1 バイトも変えない」制約からは逸脱の可能性があるため要承認)、(b) n=13 のみ cap 例外として単独スクリプト化し実測時間を記録した上で許容する、(c) 他の対処。司令塔の裁定を仰ぐ。

## 2026-07-19 — shard-b1 cap 超過の解消: JoinC 線形化(司令塔裁定・選択肢(a)採用)

- **裁定**: 前エントリの未解決懸念(shard-b1(n=13,14)が 612.0 秒でなお 10 分 cap 超過)に対し、司令塔が選択肢(a)を採用。「出力形式を1バイトも変えない」の保護対象は**証明書のバイト列そのもの**であり(ハッシュ照合 17/17 がその判定器)、内部アルゴリズムの効率化は許可されると裁定。cap 例外(選択肢(b))は却下(事前登録 cap を結果後に免除しない — Sol W21 参照)。
- **実装**: `search/suite-wp2-shard-b1.g` のみ、ヘルパー `JoinC` を線形時間実装に置換。
  - 旧実装: `r := strs[1]; for i in [2..Length(strs)] do r := Concatenation(r, sep, strs[i]); od;` — 逐次 `Concatenation` 呼び出しで O(list長²)。
  - 新実装: 区切り記号を挟みながら部品を list へ `Add` し、最後に `Concatenation(parts)` を **1 回だけ**呼ぶ(GAP の `Concatenation` は単一のリスト引数を「リストのリスト」として1回で連結するため O(合計文字数) の線形時間)。生成される文字列は区切り位置・内容とも旧実装と数学的に同一。
  - shard-a/shard-b2/q1836 は cap 内のため今回は無変更(JoinC の統一は将来の別便で扱う)。
- **再実行結果**: `.\gap.ps1 search\suite-wp2-shard-b1.g` — **161.3 秒**(GAP 内部 154297 ms、うち n=13 JSON 直列化 = 672 ms、n=14 JSON 直列化差分 = 31 ms)。旧版の 612.0 秒(うち n=13 JSON 直列化 437547 ms)から劇的に短縮。**10 分 cap 内**。
- **ハッシュ再照合(バイト同一性の確認)**: K13.v1.json / K14.v1.json の SHA-256 先頭16桁を再計算 → 記録値(b9a89b812224ea17 / c90c80b8053a8a91)と **完全一致(2/2 MATCH)**。JoinC の実装変更が出力バイトに一切影響しないことを実測で確認。
- **結論**: 全 shard(shard-a 205.6 秒・shard-b1 161.3 秒・shard-b2 243.4 秒・q1836 448 秒〔既存・無変更〕)が 10 分 cap 内に収まった。宇宙分担(shard A {3..12} + shard B1 {13,14} + shard B2 {15,16}+N5 + q1836 {18,36} = {3..16,18,36,N5})・certificates 17 件の全ハッシュ一致は変わらず有効。

## 2026-07-25 — Week 3: 宇宙の事前登録(L = K⁽³⁾ ∩ N₀)

計算開始前に固定(設計正本: docs/week3-L設計.md):

- **対象**: L = ker(φ_L)、φ_L: PB₃ → G₃ × H₃(x ↦ ((r,s,s), X)、y ↦ ((rs,r,rs), Y)、c ↦ (1,1))。H₃ = 位数 27 Heisenberg(座標 (a,b,e)・積 (a,b,e)(a′,b′,e′) = (a+a′,b+b′,e+e′+ab′) mod 3・X=(1,0,0), Y=(0,1,0))。
- **司令塔導出の構造値(照合対象)**: |Q_L| = 2916(Goursat: 共通商自明)・|B₃:L| = 17496・L_ord = 6・𝒳_L = {0,2,3,5}・|[Q_L,Q_L]| = 81・raw = 324。**L ∉ Dih**(K⁽⁹⁾ との位数一致は H₃ 非可換 3 群商の非存在で分離 — Sol 便 04 監査予定)。
- **計算項目**: GT(L) 完全列挙(counts 全段)・kernel brute 証明書・合成/逆・R_{L,K⁽³⁾} の像と全射判定。**|GT(L)| と像の期待値は事前登録しない(新対象・UNKNOWN から)**。
- **cap**: GAP 1 実行 ≤ 600 秒・node kernel-brute 1 shadow ≤ 120 秒。超過は UNKNOWN+実測報告。
- 台帳規約: L の行は Dih 正解表と別テーブル・三値(genuine/fake/UNKNOWN)・有限深度 PASS から genuine を導かない。

## 2026-07-25 — Week 3 第一撃の実行記録(WP3a/WP3b)

- **WP3a(GAP)**: `search/week3-L-explorer.g` — 全 fixture PASS・列挙 1.16 秒・ANOMALY 0。**|GT(L)| = 36**(324 → 36 → 36 → 36 — hexagon のみが刈る)。**R_{L,K⁽³⁾} 全射**(image 12/12・繊維一様 3)。証明書 `certificates/L01.v1.json`。裁定: 点数 54 は司令塔指示の誤記(正 36 = 9+27)— 実装承認。
- **WP3b(node)**: family="general" 拡張。**実バグ 2 件を発見・修正**: ①Q_L 構成が D₃³ 全体(216)を使用 → Im(ψ₃)(108)に是正(直積の安易な分解の罠)②kernel brute の素朴移植が 17496 点で OOM → 正則作用(推移的+|群| = |点| ⇒ 固定部分群自明)により基点の像のみで追跡する O(N) 版へ(論拠は Sol 便 04 監査対象)。集約 510ms。
- **統合**: L01 verdict 全項目 PASS(kernel 36/36・reduction の全射を独立再計算で追認)。既存 17+global の回帰も全 PASS(挙動不変)。裁定 3 件: f_word からの自前再構成方式(独立性強化・承認)・O(N) brute(承認・要監査)・(4.20) の general 非適用(承認)。
- 台帳: W3-1 を cross-checked へ昇格。**結果の要約: Dih 外の細分 1 段で fake 検出なし — GT(K⁽³⁾) の 12 shadow 全てが survive。**

## 2026-07-25 — Week 3 続: M₅ の宇宙の事前登録(Sol 便 04 P18〜P20 採用)

- **対象**: M₅ = K⁽³⁾ ∩ N₅ = ker(φ_M)、φ_M: PB₃ → G₃ × C₅(x ↦ ((r,s,s), t²), y ↦ ((rs,r,rs), t²), c ↦ ((1,1,1), t))。c が位数 5 で生きる Dih 外細分 — L と直交する中心項機構の本番 survival 試験。
- **事前 fixture(Sol 便 04・司令塔再導出一致)**: |PB₃:M₅| = 540(G₃×C₅ 直積全体 — 共通商自明)・|B₃:M₅| = 3240・M₅_ord = 30・derived = 27・charming 母集合 = |𝒳₃₀|·27 = 16·27 = 432。**期待 |GT(M₅)|・R の像は登録しない(UNKNOWN から)**。
- 判定: R_{M₅,K⁽³⁾} の像を最優先。cap: 単位 600 秒・GAP+checker 集約 10 分(W24: fixture が 1 つでも外れたら列挙へ進まず UNKNOWN)。
- counts 語彙は便 04 P27 を先行適用: 母集合 field 名は raw でなく **pre_hex_charming**(L01 の raw も同義と読み替え・改名は照合器改修と同時)。

## 2026-07-25 — Week 3 続: M₅ 実装での数学的発見(θ/τ の商降下の前提)

- WP3c-a(explorer)が M₅ の fixture 5/5 PASS(540・3240・30・27・432 — 全て事前登録値と一致・2.9 秒)の後、τ の商準同型構成が fail する現象を単離・診断して**独断せず差し戻し**。
- 司令塔裁定(検算済み): 簡約 hexagon の**商内評価の近道**は N_F₂ の θ,τ-不変性 = braid 共役の c-因子の消滅(**c ∈ N**)を暗黙前提にしていた。K⁽ⁿ⁾・L(c ∈ N)では成立、M₅(c ∉ M₅)では不成立 — agent の指標計算 e(τw) = n_x − 2n_y ≢ e(w) mod 5 が正しい。**Prop 3.4 自体は無傷**(元ごとの membership 条件)。対処: θ/τ を自由群の語レベルで適用してから φ_M 評価(設計変更を指示・実装再開)。
- 教訓: falsifier 前哨の軽微指摘(「θτ の商への降下前提を assertion に」)が予言どおり発火し、assertion(hom 構成の fail 検知)が誤列挙の前に停止させた。定義ノート §2 に注意書きを恒久化。

## 2026-07-25 — Week 3: M₅ 実行記録(WP3c 統合)

- **探索器**(語レベル θ/τ 版・4.0 秒・ANOMALY 0): fixture 5/5 事前登録一致(540/3240/30/27/432)+新規防御(EvalWordInQ の BFS 規約一致 540/540)。**|GT(M₅)| = 48**・full hexagon(c̄ 位数 5・c^m 項あり)48/48・**R_{M₅,K⁽³⁾} 全射**(12/12・繊維一様 4)。証明書 M01(SHA-256 a2019d64…)。
- **照合器**(WP3c-b: construction 駆動一般化+F2 改善 4 点適用): M01 verdict **全項目 PASS**・既存 19 verdict 回帰維持・GLOBAL PASS。
- 司令塔観測(candidate・W3-2b): 繊維 4 は m 方向(円分方向)の持ち上げ — L の繊維 3(f 方向・中心 torsor)と対。
- 結果の要約: **c が生きる Dih 外細分でも fake witness なし — K⁽³⁾ の全 12 shadow が survive(2 本目の細分)**。次: J = L∩M₅ の gluing obstruction(Sol P21・A 全射条件成立)。

## 2026-07-25 — 体制改定と Opus 委嘱 01・封印予測プロトコル初適用

- **体制**: 数学者レイヤー新設(Opus 5 = Claude 側数学者・Sol と対等の相互裏取り。司令塔はマネジメント・裁定へ — ユーザー指示・revert 条項つき)。
- **Opus 委嘱 01 成果**(docs/): 命題_中心持ち上げ_v1(定理 A — 完全証明・W23 不要論込み)・命題_円分持ち上げ_v1(定理 B+一般命題 C「直交細分公式」)・week3-J設計_v1(3 因子 Goursat・Φ 単射補題・fixture は Sol P22 と全一致)。第三系統の node 検算つき。**未監査(Sol 便 05 で相互監査)**。
- **封印予測プロトコル(Opus 提案・司令塔採用)**: J の計算結果に対する紙上予測を封印(スクラッチパッド・実装系は読まない規約)し、ハッシュのみ先に記帳。実装完了後に開封して突合 — 一致なら較正 PASS、不一致ならどちらかの誤り(双方に情報)。「発見を期待した予算」でなく「較正としての J」に目的を変更(命題 C の帰結)。
  - **封印ハッシュ(SHA-256)**: `b1da12f5dfc9b31f1380b24b9fb2b798bd25704629716153b4d34cfcdf694fd1`
  - 封印の範囲: 実装レーン(implementer/Luna)に対してのみ。Sol の監査は証明文書を全て読む(監査対象のため)。
- J の実装は **Sol 便 05 の監査通過後**(Opus 提案 1 を採用 — 命題 C が誤りなら設計が変わるため)。

## 2026-07-26 — 外部事象の記録: ヤコビアン予想(n=3)の反例を司令塔が独立検算

- 研究者報告 → scout 実在確認: **2026-07-20・Alpöge(Harvard/Anthropic)+ Claude Fable 5 による n=3 明示反例**(arXiv 未掲載・Tao 他のブログ追認)。F(x,y,z) = (u³z+y²u(4+3xy), y+3xu²z+3xy²(4+3xy), 2x−3x²y−x³z)・u = 1+xy。
- **司令塔の独立検算(docs/scout/検算_jacobian反例.mjs・node 厳密演算)**: det J = −2 恒等(記号計算・単項まで簡約)・3 点 (0,0,−1/4)/(1,−3/2,13/2)/(−1,3/2,13/2) がすべて (−1/4,0,0) へ衝突 — **反例成立を追認**。
- 同時鮮度スイープ: 当工房の主要未解決 3 件への外部進展**なし**(2503.13006 は既知・別系)。戦略含意: G4 バー上方修正(同日裁定)と整合・fake 証明書の「有限・初等検証可能」性は本反例と同じ認識論的形 — 主攻 ① の価値裏付け。

## 2026-07-26 — WO4 完遂・封印 PSL_v1 開封: 7/7 完全一致(CLAIMS W3-6)

- falsifier 条件付き GO(PU-F14 witness 必須化・D7 札 — workorder で実装)→ WO4 実行: **全 7 窓の観測が封印値と一致**(42/32/42/54/110/40/48)。case A settled 100%・**case B settled ちょうど半分**(非 isolated の初観測 — u ≡ ±1 定理と整合)。GAP 合計 <2 秒・check-psl(GF(q) 行列直接構成・P115 遵守)7/7 all_pass。
- **開封**: provenance/seals/seal_PSL_v1.opened.json の SHA-256 再計算 = D696AC9EA7B621A71F83A0182417485E7470FEE6AE6A3376EF419D47B28C141B — **封印時の台帳記録と一致**(予測の事前固定を機械的に証明)。
- D7 遡及: convention_robust は 1a/2a/2b = true・1b/A1/A2/3 = false の一貫パターン(構成型に対応)— D7 の監査は便 11。

## 2026-07-26 — 裁定 10: 独立収束第 4 号(case B 障害機構)・統一定理候補・PU-F14 封印

- **双方向ブラインドの偶然成立**: Opus 委嘱 07 の命題_caseB_settled障害_v1 は Sol 便 10 を読む前に起草(逆も未読)— case B の settled 障害で全論点一致(座 = w・u ≡ ±1・繊維 16/32・20/40・24/48)。**統一定理候補: |GTSh(N,N)| = |N_Aut(⟨w⟩)|**(case A = Hol(ℤ/k)・case B = D_{4k}・case B 恒常非 isolated)— 便 11 で最終相互監査。
- D7(判定式の積規約・(H-a) 鈍感/(H-b′) 敏感)= Opus 新発見・Sol 未監査【GAP-W3 遡及監査は WO4 並行】。PU-F14 は選択肢 (b) 採用(期待値 PS-F14 封印・fixture は出力形式)。Opus 検算スクリプト 36 本を金庫 staging に恒久化(6cc917d)。
- manifest v2_psl(7 窓 10 軌道・19944 点・封印行列と整合)受領 → spec 射影 → falsifier → WO4。

## 2026-07-26 — Lean 工場開通・プロジェクト初の verified(W3-5)

- lean/(plain Lean 4.32.1・Mathlib なし・lake)+.github/workflows/lean.yml(elan → lake build)を設営。ローカル warm 0.8s/RSS 255MB・**CI green**(commit 054db1b)。
- **初の verified**: `Marking.marking_identity` — A₅ marking の s∘X∘s⁻¹ = Y を decide で機械証明。**依存公理 propext のみ・sorry なし**(公理監査込み)。範囲は単一恒等式(誇張しない)。CLAIMS W3-5。
- 次段: 証明書形式(JSON → Lean 命題群)の設計は司令塔+Opus(P87 候補: T2(iii) 捻れ恒等式・E1・A5-Q 生成元等式)。Mathlib は必要が生じた時点で CI 側にのみ導入(ローカル排他は不要になった)。

## 2026-07-26 — 道具の解放完了+正典追加(2008.00066)

- 道具聴取のフォローアップ: **MapClass は GAP 棚に既在**(lins/repsn/twistedconjugacy/wedderga と共に実在確認)— 数学者要望のソフトは全て調達不要で解放済み。Guillot 原文は配達済み。**Lean+Mathlib 工場の設営を implementer に発注**(public 化の主目的 — Actions でのビルド・ローカルは軽量)。
- 正典追加: **arXiv 2008.00066**(What are GT-shadows? — 副線 B₄ 系の定義正本・Phase 0 以来の未入手分)を papers/ へ。SHA-256 = C44EBA890F83C1AC84A44A5B52FD5C6849250B242331D7EAAFF9DD983167FB33。txt 層生成済み。

## 2026-07-26 — PSL 突合成立・封印 PSL_v1(P67 初適用)・裁定 09

- **PSL 独立紙計算の突合**: 重なり(split-inner = case A・4 窓)で Sol(便 09)と Opus(委嘱 06・金庫)が**完全一致**。Opus は外部型 case B を完全分類(Sol は正しく UNKNOWN 申告 — 矛盾なし・相補)。PSL(2,8) に case B 非存在は両者一致。**命題 S は case A で 5/5 成立・case B で 3/3 破れ** — 正しい射程は「split-inner 窓」(3|k は無関係)。case B は **atlas 初の非 isolated 対象の予測**を含む。
- **封印 PSL_v1(P67 六要件・初適用)**: 7 窓の予測(n_m・総数・isolated・群型 Hol(ℤ/k))+構造予測を canonical JSON+128bit nonce で封印。**SHA-256 = D696AC9EA7B621A71F83A0182417485E7470FEE6AE6A3376EF419D47B28C141B**(payload+nonce は金庫 sealed/・金庫 git d851c98)。性格 = 改竄防止 commit(case A 値は sol/ に公開済みゆえ秘匿でなく tamper-evidence — W38 語彙)。
- 裁定 09(sol/裁定_09_psl.md): v_m 恒等式 合格(F2 の訂正込み)・48 一本式/補題 D 合格・E2a は split-inner へ射程修正・語規約 v1 は局所修正後併合(Opus へ v2 差し戻し)。実装は S1(PSL(2,7) A・1008 点)→ A 残り → S2(case B 非 isolated 検証)の順で次 workorder。

## 2026-07-26 — 配達原著の一括取得(規約強化: 引用論文は配達時に取得が既定)

- 研究者指摘 2 件を受け SLA 最終形(要請受領→即出撃→探索完了→**両者同時**配達)と「**覚書+引用論文の原著一式**」を規約化。配達 03/04 の引用 14 本を arXiv から一括取得し papers/delivered/ へ(SHA-256 先頭 16 桁): 0710.1835=EF53BE9ECCF58C5C・1301.2949=FB475EB467E77328・1301.2955=C59A3CCBB5015B5F・1506.01371=D62558D1B60663A5・1811.09526=7F52AD3945972238・2011.12940=F60283B0B406554C・2105.07247=193CC4B18F086C8D・2308.12286=924D986ABC936815・2508.10434=518B0AC317FDE58F・2508.21671=8135119629EDB477・2510.12003=AE029E4E98F4B666・2605.22127=8EBD18F41D40E1D0・2605.23195=07FFF7204EF471B3・math/0304376=5B05A2B6EA43BFC9(再取得は arXiv ID で可・全桁ハッシュはファイルから再計算可)。
- 入手不能: Kawanaka–Matsuyama 1990(Hokkaido Math. J. 19・DOI 10.14492/hokmj/1381517495)— 誌面のみ・書誌で供与。

## 2026-07-26 — P92 完遂: A₅ の窓の完全決定(GT(N_A) = 位数 20 の群・二系統)

- implementer(Opus 答案の読取禁止下)が GAP で settled witness 20/20・(3.53) 合成表 400 マス閉性 100%・単位元/逆元完備を計算、node checker が witness を独立再検証 → **all_pass 8/8**。Opus の単系統計算と合わせ **GT(N_A) が位数 20 の群であることは二系統確定**。位数分布 {1:1, 2:5, 4:10, 5:4} は位数 20 の群のうち **F₂₀ = C₅⋊C₄ を一意特定**(D₂₀/Dic₅/可換型と分布不一致)— 同型の正式宣言は便 09/10 の Sol 監査後。
- 証明書修正一括適用(3.v2 isolated=true・R₇/R₈ fibre 一様 4/6 記入・A2 に R9→N₅ 追加 fibre [5,5,5,5]・schema v2.1 f_word 正式化)・checker 強化(P96)。
- 規約の追加再発見: checker 側 natural+naive が「判定は偶然一致・元は不一致」— witness 検証を prepend に統一(語規約恒久化の必要性をさらに裏書き)。

## 2026-07-26 — 「20 の正体」ブラインド突合成立: 類積係数 5・C₅ torsor・F₂₀ 仮説に独立収束

- **制度としてのブラインド突合・初運用成功**(Opus 成果物 = 金庫・Sol = sol/ 遮断): 両数学者が独立に「20 = 4×5・5 = A₅ の類積係数(Frobenius 指標和・自明指標のみ生存)・繊維 = C₅ torsor(第三の繊維型)・GT(N_A) ≅ F₂₀ = AGL(1,5) 仮説」へ到達。裁定: sol/裁定_08_battery.md。
- Opus の一般化(未監査): **v_m = σ̄₁^{2m+1}**(c ∈ N で一般)— T2-B は「⟨σ̄₁⟩ の生成元の (2,3)-分解」に統一。48 = 8·3·2 の一本式。E4′ の scalar 化は P 完全で閉(【GAP-E2a】部分閉鎖)。語規約追記案(補題 W1: ev_bad(w) = ev(ι(w))⁻¹)。
- F₂₀ 同定は **P92(settled 20/20 の GAP 側計算+合成表)による二系統化が条件**(W63/W64 遵守)。封印予測の初適用を決定: PSL(2,7)/(2,8)/(2,11) の n_m を両数学者が独立紙計算 → 司令塔が P67 六要件で nonce 封印 → 実装。
- 状態: 数値(20/20/48・staged・全射)= cross-checked。構造説明 = 紙上相互収束(監査は便 09)。genuine/arithmetical は未主張。

## 2026-07-26 — バッテリー完走: 全 7 段 all_pass・開封総括

- **観測(blind)= 紙上予測**: 1a 4・1b 24(公式破れ実測)・2a 4・2b 8(H9 較正一致)。**発見値**: A1 = A2 = **20**(補題 A2A1 の全単射が観測成立・staged counts まで一致)・段 3 M₃ = **48**(R→K³ 12/12・R→N₃ 8/8 全射)。**バッテリー全域で fake witness なし**。GAP 合計 <10 秒・7/7 verdict all_pass。
- 規約頑健性: 1a/2a/2b は両規約一致・**1b は非頑健**(natural 12 vs prepend 24)— 二重打ち消し仮説は単一左正則構成のみで成立と確定。crosscheck の genB 対規約バグも検出→修正→全段再照合。**語規約の正本 = prepend(paper 語 "AB" ↔ GAP "B*A")を工房規約として恒久化すること**(定義ノート追記は次回)。
- CLAIMS 更新: W3-3/W3-3b/W3-4 追記。次工程: 結果の両数学者配達(20 と 48 の構造説明の委嘱)・可視化更新・Lean 初弾(Actions 工場)。

## 2026-07-26 — WO2 前半: A₅ 初実測 |GT(N_A)| = 20(発見値)・司令塔裁定の撤回 1 件

- **段 A1(N_A・360 点)all_pass**: 観測 shadow_total = **20**(240 候補 → h10_fail 176 → h11_fail 44 → generation_fail 0)。紙上は「m-full・既知 4 解・総数 UNKNOWN(P59)」だった — **本プロジェクト初の発見値**(GAP+check-v2 二系統一致)。U-F7 も解除済み(両表示一致 PASS・exponent 2 論法)。layer_id は開示制限により BLOCKED(後日司令塔が注記)。
- **A2 で司令塔裁定の誤りが実測反証される**: 司令塔は A2 の語レベル評価を「自然な左→右」と裁定したが、観測 12 ≠ A1 の 20 が**補題 A2A1(集合全単射・監査済み)をトリップワイヤーに作動**。implementer が地の計算(FreeGroup 準同型・独自語コード不使用)で追跡: **paper 語 "AB" ↔ GAP 乗算 "B*A" の反転は一般的規約**であり、Q₈ 型では左正則表現の反転と二重に打ち消されて自然評価が偶然正しく見えていた。A₅(反転一重)では **manifest 事前登録の元規約(M₅ explorer と同一の prepend)が正しい**。**司令塔裁定を撤回**し prepend で再実装を指示。事前登録を走行後の「裁定」で上書きしかけた事例として教材化(W36 の精神: 列挙開始後の規約変更は登録側が勝つ)。
- implementer は矛盾検出時に無断修正せず停止・報告(規律どおり)。WO1 4 段は両規約が一致する型(二重打ち消し)だが、頑健性検査を追加発注。

## 2026-07-26 — WO1 完了: 較正 4 段 all_pass・観測 = 紙上予測(開封)

- blind 運用の implementer(spec 射影のみ・期待値非開示)が観測: **1a = 4・1b = 24・2a = 4・2b = 8**、reduction 全射(1b→K³ 像 12/12・繊維 2 / 2b→N₂ 像 4/4・繊維 2)。**紙上予測(定理 H6/H9・Sol P34/P36)と全一致** — 公式破れ(24 vs 直積公式 48)を実測確認・H9 は反証機会を生還・P40 前件の不成立が実測確定。GAP 合計 374ms・二系統照合 all_pass(check-v2.mjs)。
- 過程の発見 2 件: ①旧 explorer の prepend 語評価は左正則表現の実装反転(照合器へ持ち込み禁止 — 独立性防衛)②手書き collection 公式が結合則を破ることを 128³ 全数検査で検出 → 書き換え系で回避(GAP-E5 の警戒が実地で的中)。
- U-F7(両表示一致)は spec に restricted 定義式がなく BLOCKED — 司令塔が定義式(D₃⁽²⁾ = F₂⁴γ₂²γ₃・D₄⁽²⁾ = F₂⁴γ₂²γ₄)を追給して追検査(定義の供与であり期待値でない)。
- 状態: 4 段は **cross-checked**(二系統一致)へ昇格。CLAIMS 一括更新は WO2(A1/A2/3)完了時。

## 2026-07-26 — 停止ゲート (b)(c) 解除: リポジトリ public 化・GitHub 工場の使用開始

- 研究者承認(同日原文): 「公開設定にしてgithab上で操作してもいいよ。Lean+Mathlib重いからね。」
- 公開先: **https://github.com/tochiazuma0510-alt/shadow-atelier**(public・master・凍結タグ v1.0-g1 込み)。
- 公開除外(gitignore 済みを push 前に確認): papers/(arXiv PDF — 著作権)・ops/codex_activity.log・ops/bin/codex_session_id*.txt。金庫(vault)はリポジトリ外で非公開のまま。
- 主目的: **Lean+Mathlib の重いビルドを GitHub Actions へ**(8GB ローカルの排他制約の回避)。Actions 工場の設営は較正バッテリー完走後の Lean 初弾(T2(iii)・E1・A5-Q)と同時に実施予定。

## 2026-07-26 — 実装ゲート GO(falsifier 差分再確認 PASS)・較正バッテリー発射

- Opus 委嘱 04(G-01〜G-09 反映・manifest v1・比較写像 v2)→ falsifier 監査で **NO-GO(1 重大+3 軽微)**: U-F9 の E_m 値が spec 側に漏れ較正盲検を破壊、ほか型/根拠文/正規形固定。司令塔が外科修正(コミット 6f7ad14)→ **falsifier 差分再確認 PASS・GO**。
- **封印の扱い(バッテリー v1 の正直な記帳)**: 較正 4 段(1a/1b/2a/2b)の期待値は v4 の紙上定理として既に公開・git 履歴にも在中 — 暗号学的秘匿は成立しない。よって本バッテリーの盲検は「**implementer の入力制御**(spec 射影のみ読む・期待値文書の読取禁止)」による **blind 運用**であり、暗号学的封印とは呼ばない(Sol W38 の語彙)。A1/A2 の未知値(gt_count 等)は **P59 により予測自体を作っていない**(封印対象が存在しない)。**P67 六要件の nonce 封印は「次に紙上予測を新規に立てる未知計算」から適用**。
- workorder 1 = 段 1a/1b/2a/2b(商内評価・計 2304 B₃ 点)。workorder 2(A1/A2/3・語レベル含む)は WO1 全 PASS 後。
- 研究者指示(同日): 文献配達は**論文そのもの**+翻訳覚書のセットが既定に(papers/delivered/ 新設・3 本配置)。両数学者へ「他に使いたい道具」の聴取を実施(Opus 回答待ち・Sol は便 08 で)。

## 2026-07-25 — Sol 便 07 受領・裁定 07: 実装ゲート「条件付き GO」(G-01〜G-08)

- 14:34 UTC 受領(exit 0)・git 監査クリーン。裁定: sol/裁定_07_audit.md。
- **合格**: T2 本体(【GAP-E10】閉鎖)・E1・E3(限定版)・E4-E6・比較写像 G1/G2′/G3(【GAP-G1】閉鎖)・A5-Q・Q₈ Φ=0・バッテリー 7 段/25200 点/順序/cap。**要修正 8 点(G-01〜G-08)**: T2-A exact order・E2→E2′ 弱化・`m_missing`/`fake_witness` 分離(F11 — fake は相対概念)・settled の (m,f) witness 化・単一 manifest 統合ほか。
- 訂正: 中心化条件 ⟺ **class ≤ 2 と正確に同値**(F8)・Guillot δ は位数 2(F16)。
- **Sol の数学提供**: F13 行列値 Fourier 公式(成層数の正確式)・F20 A2→A1 全 shadow 集合全単射の紙上証明。文献要請 4 は F13 基準式の scalar 化に絞り直し(P85)。
- 工程: Opus 委嘱 04(修正反映+canonical manifest)→ falsifier 差分確認(P88)→ implementer 発射。状態札: 今便の合格群はすべて「紙上相互監査」(W60)。

## 2026-07-25 — Sol 便 06 受領・裁定 06: H8″/H7′ 不合格・(Q7) は A₅ で存在決着(真の独立収束)

- 13:35 UTC 受領(exit 0)・git 監査クリーン。裁定: sol/裁定_06_audit.md。
- **合格**: H8 本体(狭形)・H9(紙上定理)・H5/H6 本体・H7(補筆条件付)・塔照合・J1′・v2 修文。**不合格**: H8″系戦略結論(【GAP-E2】が本丸の穴 — F2)・H7′(反例 Q₈×_{C₂²}Q₈ — F10)。狩場は **E2 型と Q7 型の二正面**へ再編(W41/W42/W47)。
- **(Q7) 存在決着**: Sol が A₅(k=5)の許容 marking を明示構成(F11)+m-full(F12)。**hunter(要請 2)の GAP 悉皆(A₅ 最小・位数<60 該当なし)と独立収束** — Sol 攻撃中は hunt 報告書 2 本を物理検疫(scratchpad)へ隔離し、活動ログ grep 0 件で**未読を確認**(便 05 の教訓が機能・真の独立)。検疫解除し報告書を docs/scout/ へ復帰。
- A₅ 宇宙の事前登録(P60): PB 指数 60・B₃ 360 点・ord 5・derived 60・母集合 240。M_{A,5} = N_A∩N₅(P61): 1800 点 word-level 較正。**この A₅ は m-full ゆえ Q7 非空 ≠ fake 十分**(W47)。
- 文献配達 02 起草(docs/文献配達_02_guillot定義_E2_kkk.md): §1 Guillot 正確定義(P68 即応 — 検疫圏読解の配当)・§2 E2 文献(Burkhart 非 coprime 不動点・捻れ FS 指標)・§3 (k,k,k) 文献。Opus 委嘱 03 と Sol 便 07 で両者同時配達。
- 封印標準 P67(6 要件)を次の未知計算(|GT(N_A)| 等)から適用。

## 2026-07-25 — Sol 便 05 受領・裁定 05(相互監査 初回転の完了)

- 3 回目の起動(12:13 UTC・exit 0)で sol/sol_reply_05_peer_review.md 受領。git 監査クリーン(変更は返信のみ)。裁定: sol/裁定_05_peer_review.md。
- **判定: 定理 A 合格・定理 B 結論合格(χ の言い回し修正 F5/W31)・命題 C 合格・J 設計合格(kernel 証明書 PB₃ 縮小は F10 の schema 条件付き)。W23 は Sol が原文照合の上で自己撤回(Opus の (3.32) 論拠を承認)。**反証の穴なし。紙上相互監査 PASS ≠ verified(Lean 未接続)。
- 封印プロトコルは F11/P46 で強化裁定(canonical payload+乱数 nonce+計算前 commit)。既存 J 封印は「blind 運用」に再ラベル(暗号学的秘匿とは呼ばない)。
- 狩場案: P32-P36(Q₈/M_Q)は汚染(続報 3)により独立収束と扱わず「第二系統の紙上再計算(一致)」として採用。P37-P43(2-Zassenhaus 塔)は Opus T₄ 塔との照合を委嘱 02 で実施。
- **文献配達 01 実施**(タスク #11): docs/文献配達_01_goursat_guillot.md を起草し Opus(委嘱 02)へ配達・Sol へは便 06 で配達予定。ブラインド局面の終了を確認の上、検疫圏から翻訳して開示(きっかけ: ②常務読み第 1・2 号)。

## 2026-07-25 — ops 障害記録: Sol 便 05 初回起動が OpenAI 503 で失敗

- Codex バックエンドが 503(circuit open + throttled)。WebSocket/HTTPS 両系 5 回再試行の末 turn 失敗(返信なし・exit 1)。
- 扱い: **技術的失敗**(ES7 規律 4 — 数学的 stuck と区別・claim なし)。20 分後に wake で自動再試行(1 回)。再失敗なら間隔を広げ研究者に報告。

### 続報 3(同日): ブラインド工程の汚染を検知 — Sol が Opus 狩場設計を既読(司令塔の工程ミス)

- codex 活動ログ 129101–129120 付近に、Sol のリポジトリ内検索が docs/week3-狩場設計_opus_v1.md の中核(境界定理 H5/H7′・候補一覧・推薦)を表示した記録。11:15–11:22 の走行区間で読了とみられ、セッション transcript に残存(現走行にも引き継がれる)。
- 帰結: **便 05 (e) の Sol 独自狩場案は「独立起草」ではなくなった**(anchoring 済み)。突合(タスク #12)は「ブラインド交差確認」から**「既読前提の第二意見+相互監査」に格下げ** — 両案の収束を独立の裏付けとして扱わない。監査 (a)-(d) は影響なし(監査対象はもともと開示物)。J の封印予測も無傷(封印はハッシュのみ台帳・実装レーン向けで、Sol は監査のため開示済みの設計)。
- 原因: 司令塔が**ブラインド工程の進行中に**片側(Opus)の成果物を共有ツリーへコミットした。検疫圏の設定が docs/scout/(文献)のみで、ブラインド成果物に未適用だった。**Sol の側に非はない**(kickoff (e) の関連資料調査として自然な行動)。
- 再発防止(体制と道具.md に追記): 進行中ブラインド工程の成果物は突合完了まで共有ツリーに置かない(scratchpad か検疫圏で保持)。

### 続報 2(同日 11:15–11:22 UTC): 再ログイン後の wake は成功・約 7 分実走の後 503 再発で turn 失敗

- `codex login` 再認証成功(研究者実施)→ 同一 pinned セッションへの wake 成功・監査の実走を確認(2405 原文のページ画像照合ログ等)。
- 11:21 UTC に WebSocket 5/5 → HTTPS fallback → 5/5 いずれも 503(biscuit_baker circuit open)で turn 失敗(exit 1)・返信なし。**技術的失敗扱い継続(claim なし)**。
- 進行分はセッション transcript に残存 — 次の resume は続きから。対応: **間隔を 35 分に拡大**して再 wake を予約(churn 回避)。以後も失敗なら間隔をさらに拡大し研究者に報告。

### 続報(同日 09:23 UTC): 再試行は 401(認証失効)で失敗 — 自動再試行を停止

- wake 再試行は 503 でなく **401 Unauthorized(token_invalidated / refresh_token_invalidated)**。障害の副作用で Codex のリフレッシュトークンが無効化されたとみられる(exit 1・ログ ops/codex_activity.log)。
- 401 は時間経過で回復しないため**自動再試行を停止**し、研究者に Codex 再ログイン(`codex login`)を依頼。claim なし。
- 再ログイン確認後、同一 pinned セッション(019f9881-…)へ wake を再発射する(sol_task_05_peer_review.txt は不変・監査内容に影響なし)。
- 待機中の並行措置: Claude 側数学者(Opus)に狩場設計 Q1/Q2 の**ブラインド起草**を先行発注(Sol の (e) 回答と独立に起草 → 司令塔が突合)。sol/ 読み取り禁止を指示済み。

## 2026-07-25 — 文献ゲート初運用: scout 予習スイープ(初陣)

- 同日ユーザー裁定の「文献ゲート」(体制と道具.md 新節)に基づく司令塔予習。paper-scout の 4 角度スイープ報告書: docs/scout/scout_20260725_予習スイープ.md(検疫圏 — 数学者読み取り禁止)。
- **URGENT なし**: dihedral 予想(2405.11725 Conj 5.1)への外部進展は 2024-07〜2026-07 窓で確認できず。Semantic Scholar 被引用 0 件(実地確認)— 競合不在。
- **正典の版確認**: 2405.11725 に v2(2026-01-13 改訂)が存在するが、当工房の PDF は入手時(2026-07-18)から **v2**(papers/txt のスタンプ行で確認)。定義ノート・較正データは v2 準拠 — diff リスクなし。
- 司令塔一次読み: Guillot GT(G)(1407.3112 / 1604.04415)は要旨より B₄ 系(pentagon 込み)の可能性高。有限単純群での明示計算の機構は将来の翻訳候補として検疫圏に留置(**降ろしていない** — ゲート通過なし)。
- 残 UNKNOWN(報告書末尾に引き継ぎ): Guillot の関係式実地判定・Yulia's Dream 資料・候補 9/10 実在確認・Dolgushev publist.pdf。
- **②常務読み 第 1 号(同日)**: arXiv 1109.0024 v3(Bauer–Sen–Zvengrowski, Generalized Goursat Lemma)を reader が精密読解 → docs/scout/読解_generalized_goursat.md。**3 因子補題(監査中)への確認定理・反例とも文献に無し** — 監査が引き続き決定打。PDF は方針どおり非コミット(gitignore `papers/`)・SHA-256 = `C2A97D8A4F9BD6EA86B322FA7B57B5B1667B9EF29F860A3965FE237E26D665BB`(docs/scout/papers/1109.0024v3.pdf・arXiv から再取得可)。処置: **留置** — 便 05 決着後に両数学者へ同時降ろしの候補 A(累積型分類 Thm 3.2・profinite 版 Prop 4.2 が翻訳対象)。
- **②常務読み 第 2 号(同日)**: Guillot GT(G) 2 本(arXiv 1407.3112 v3・1604.04415)を reader が精密読解 → docs/scout/読解_guillot_gtg.md。**系統確定: hexagon 階層(逆極限 ĜT₀・pentagon 出現 0 回)の F̂₂-outer「第三変種」**(λ・(m,f)・中心 c なし)。scout 段階の司令塔一次判定「B₄ 系可能性高」は**誤りで訂正**(教訓: 要旨だけで系統判定しない — 上記スイープ記帳の該当部は本行で上書き)。収穫: dihedral 粗塔の fake 実例(Prop 3.1: n 奇の位数 2 元が D₄ₙ で死滅 = 持ち上げテスト式 fake 検出の文献先例・**fake は塔相対的**)/単純因子 menu 定理/両側剰余類+θ 前段フィルタ・packet 法(実装レーン向け)/比較写像 GTSh(N)→GT(G) の予想(読解者発案・小課題候補)。SHA-256 = `416C0A91EF7BBB2EB7B8E615D8D209083232965F1151C3E2832256110806784B`(1407)・`16A2496E4C4929570BBC8D330070DEA92F0A08CB0D1DAD01A2A9DBCEE834CDEA`(1604)。処置: **留置** — 降ろし候補 B。**覚書 docs/scout/降ろし覚書_01_goursat_guillot_v1.md を起草済み**(配達条件: 便 05 決着+ブラインド突合後・両数学者同時)。

## 2026-07-18 — 用語改定(ユーザー指示)

- **「検証(verified)」は Lean(機械証明)に予約**。node/python の独立再計算は「**照合器(cross-checker)**」と呼び、二系統一致の状態は「**cross-checked(照合済み)**」。上のエントリの「検証器/検証 = node」の表記はこの改定で「照合器/照合 = node」と読み替える。ディレクトリ `verifier/` → `crosscheck/` に改名。台帳語彙は CLAIMS.md 冒頭が正。

## 2026-07-26 — A₅ (5,5,5) dessin GAP 二系統化・implementer 実装(P2 発注)

- `search/a5-dessin-crosscheck.g`(GAP 4.16.0・node 実装(`search/week4-a5-dessin-unique.mjs`)非参照・数学的定義から独自再構成)実行、200ms 未満。証明書 `certificates/a5/gap_dessin_crosscheck.json`。
- 任務(a)結果: 全 192・A₅ 型 120・C₅ 型 72・A₅-共役軌道 2(サイズ[60,60])・S₅-共役軌道 1(サイズ[120])・\|C_{S₅}(A₅)\|=1・種数=2(全 120 A₅ 型対で一定)・\|𝒟(v)\|=5 — **node 側期待値と全一致(9/9 PASS)**。
- **不一致 1 件(黙って合わせず報告)**: 発注文の写像 (g0,g1)↦Fix(g1)(g1 の固定点)を字義どおり実装したところ、g1 は位数 5(5-サイクル)ゆえ {1,…,5} 上で常に不動点 0 個 — Fix(g1)=∅ が 𝒟(v) の 5 対すべてで成立。ゆえに写像は {1,…,5} への写像として well-defined でなく、「全単射」判定は **FAIL**(node 側期待値 true と不一致)。⟨v⟩-同変性は両辺恒常的に∅どうしの比較で機械的には PASS するが空虚な成立(vacuous)。詳細と所見は `docs/notes/検算_a5_dessin_gap.md`。司令塔差し戻し事項として記録(FC-6 の (2,3,5) 文脈の Fix(q)(q は位数2)との混同の可能性を指摘・断定はせず)。
- 任務(c′)結果: 4 項目全 PASS — t=1 展開一致・(x+2)(x⁴−2x³+4x²−8x+6) 分解+分離的(gcd(f,f')次数0)・mod 3 因子次数型 [1,1,1,2]・F₂₀(位数20)の cycle type 悉皆に転置型 (2,1,1,1) 不在。
- 実装中の罠: GAP `Concatenation` は単一引数だと「リストのリストの連結」と解釈され文字列(文字のリスト)を渡すとクラッシュする(複数引数なら問題なし)— 証明書 JSON 組み立てで踏み・修正済み。

## 2026-07-26 — A₅ dessin (a).5 発注ミスの訂正・再実行(司令塔裁定・implementer 追補)

- 司令塔裁定: 上記の(a).5 FAIL 報告は implementer の実装ミスではなく**司令塔の発注文の転記ミス**(v2 §3.6 補題 FC-6 は (5,5,5) ではなく (2,3,5) 対の写像だった)。訂正仕様(𝒟(v):={(q,r): q∈2A(位数2・不動点1個), r∈3A(位数3), qrv=1})で `search/a5-dessin-crosscheck.g` に追補・再実行(旧コードは監査痕跡として無変更のまま残置)。
- 「qrv=1」の語順規約は両読み(MAIN: v*r*q=1・NAIVE: q*r*v=1)を並記 — **両規約とも \|𝒟(v)\|=5・well-defined・全単射・⟨v⟩共役で閉じる・⟨v⟩-同変、すべて PASS**。node 側期待値(𝒟(v)=5・全単射/同変=true)と**全一致**。
- 実装中に第二の GAP 罠を検出・修正: ⟨v⟩-同変性検査で「q を v で共役」を素朴に `q^(v^(-1))` と書くと誤り(GAP の `^` は `i^(g*h)=(i^g)^h` の右作用規約で自己完結しており、標準数学の v(i)=i^v と組み合わせて「v q v⁻¹」を再現する正しい GAP 式は `q^v`)。具体例 q=(1,2)(3,4), v=(1,2,3,4,5) で実測確認(`search/debug-equiv-test.g`・削除済み、手順は `docs/notes/検算_a5_dessin_gap.md` に記録)。2026-07-26 WO2 A2「paper "AB" ↔ GAP "B*A" の反転」と同種の罠。
- 証明書 `certificates/a5/gap_dessin_crosscheck.json` の `task_a.item5_corrected` に MAIN/NAIVE 両規約の全数値を記録。`docs/notes/検算_a5_dessin_gap.md` に訂正セクションを追記。

## 2026-07-26 — E2 掃引①r2 項目3・384 系本走査(発射許可後・implementer 実行)

- sol2 一致確認(608 PASS/0 FAIL・規約差ゼロ、`docs/notes/一致確認_E2作用表.md`)を受けた発射許可により、`search/e2-sweep-r2.g` で j=1..6 × m=0..63 の全 384 系を線型段+二次段(F/πB exhaustion・mass check・双対証明書)まで完全実行(elapsed 11094ms・cap 600秒内)。結果: **384/384 POSITIVE(線型段不可解 0・二次段障害 0・cap_exceeded 0)・mass_check 全系 PASS・「F が K 上で恒等的に定数」の現象が全 384 系で観測**(解釈は保留・事実のみ記帳)。証明書 `certificates/e2sweep/sweep_j{1..6}_m{0..63}.json`(384 件、`solution_witness` 型)を `crosscheck/check-e2-action.mjs` が全件独立再検算(GAP コード不読・凍結スペックのみ入力)し **409/409 PASS・0 FAIL・0 SKIP**。証明書一式(401 件、demo/smoke 含む)の連結 SHA-256 = `cdbed977f91be34ec771c0377167ad23f38987c5244cac5b2ab95eb7d888e1a7`、384 本番のみの連結 SHA-256 = `f67aefde75718de1ffb63bc6be0adfeffdb3e7f7f3627f55b37c3359436293e6`。

## 2026-07-26 — 位数 32 全 51 群 (4,4,4)-marked F2-商 悉皆走査(裁定_19 §4 発注・implementer 実行)

- `search/smallgroup32-scan.g`(elapsed 1500ms)で SmallGroup(32,i), i=1..51 の全群につき、G²=1024 対の総当たりで N_i(<a,b>=G かつ ord(a)=ord(b)=ord(ab)=4 を満たす対の数)を算出。G4=⟨(r,s,s),(rs,r,rs)⟩≤D4^3(`week3-M5-explorer.g`の`MakeGn(4)`)は IdSmallGroup(G4)=[32,2] と同定(N_2=384, |Aut|=384, kernels=1 — 裁定_18 の「384/384」と整合)。**結果: N_i>0 は SmallGroup(32,2) だけでなく SmallGroup(32,6)((C2xC2xC2):C4, N_6=192, |Aut|=64, kernels=3)も非零 — 「G4 ただ一つ」の予測は不成立(反例あり)**。独立の別アルゴリズム再計算(`search/smallgroup32-scan-diag.g`、群2・群6のみ)で完全一致確認(社内サニティ、正式照合器ではない)。証明書 `certificates/a5/smallgroup32_scan.json`、詳細 `docs/notes/検算_sg32走査.md`。384/384 の昇格経路(marked bridge 第二証明)はこの形では閉じない。

## 2026-07-26 — SG(32,6) 新窓候補の B₃-許容性判定(裁定19追記・implementer 実行)

- `search/sg32-admissibility.g`(elapsed 172ms)で、SG(32,6) の 3 核候補(N_6=192, Aut-軌道 3 個)につき
  θ: x↦y,y↦x・τ: x↦y,y↦(xy)⁻¹ が核を保つか(marked pair (a,b) の Aut(G)-軌道単位で、変換後の対が同一
  軌道に入るかで判定・核は構成しない・GAP 部分群比較ではなくAut-軌道membership判定)を判定。**結果:
  3 軌道すべて both_admissible=FAIL(軌道1のみ θ=PASS・τ=FAIL、軌道2・3は θ・τ 共に FAIL)— SG(32,6) 由来
  のいずれの核候補も B₃-許容でなく、窓の新候補にはならない**。較正: G4=SmallGroup(32,2)(既知の K̄⁽⁴⁾、
  1軌道)は θ・τ 共に PASS(想定どおり、実装バグなし)。証明書 `certificates/a5/sg32_admissibility.json`、
  詳細 `docs/notes/検算_sg32許容性.md`。

## 2026-07-26 — E2 class-6 二方向掃引: 線型段+fixture 実装(発射は保留・implementer 実行)

- `search/e2c6-sweep.g`(GAP、入力=`crosscheck/agree6_claude.json`のみ・elapsed ~700ms)+ `crosscheck/check-e2c6.mjs`(Node、入力=`crosscheck/agree6_sol2.json`のみ・系統分離)で線型段(Ā_j=15次元, rank15 の (1+θ̄)f=0 & N̄f=−Ē_m)・証明書配管・fixture (ii) class-5 統制(j=2, m=0..63 全可解 PASS)・fixture (iii) mass check(判定基準=解の重複度総和=Π n_i の厳密一致、司令塔補完の基準で class-5 統制系+class-6-shaped 合成系(rhs=0、実ターゲットの m は不使用)双方で PASS)を実装・実行。表転写・d_theta/d_sigma 自己整合の自己検査も全 PASS(GAP側3件・Node側3件)。**64系の本走査(実 m での ob 判定)は未実行**。**ob 抽出層(「(q_θ)₊」の射影定義)は司令塔差し込み(falsifier 計画監査: (A)3⁻¹(1+σ+σ²)平均化射影 vs (B) Ra⊕Rb 単純読取、未批准)により実装保留**— fixture (i)(合成非零で ob≠0 発火)もこれに伴い保留。証明書 `certificates/e2c6/fixture_{ii,iii}_*.json`(5件、fixture専用・ob_a/ob_b は null)、詳細・未解決確認事項は `docs/notes/実装_e2c6掃引.md`。

## 2026-07-26 — E2 class-6 二方向掃引: ob 層批准実装(裁定20)+発射錠・モード錠(implementer 実行)

- 裁定20(委嘱16 Opus・便22 Sol 並列独立導出一致)を受け、`search/e2c6-sweep.g`+`crosscheck/check-e2c6.mjs` を manifest v2 に更新。**ob = [q_θ − 3⁻¹(1+θ)q_N] ∈ C^θ/(1+θ)ker𝒩、j=2 読み出しは ob_a=q_θのu4係数・ob_b=q_θのu2係数**(旧(A)(B)は破棄)を実装。fixture F1(偽陽性検出)・F2(真陽性/ビット脱落検出 2種)・F3(class-5統制 再走)・F4(M2/M3/M5+核enumeration mass check)**全 PASS**(GAP・Node 双方)。実装中に自己発見・修正したバグ2件(前提を満たさない任意ベクトルでM2/M3を検査していた誤り、q_θ/q_Nをmod R=2^{j-1}に還元し忘れていた誤り)は `docs/notes/実装_e2c6掃引.md` に記録。**発射錠**(`search/FIRE_e2c6.auth` の SHA-256 照合、GAP `Exec`+`sha256sum` 経由)を実装・LOCKED 動作確認(認可ファイル不在・ハッシュ不一致の両方で確認、認可ファイルは作成していない)。**ob モード錠**(`ob_mode!="quotient-ratified-v2"` かつ ob 値ありは REJECT)を `check-e2c6.mjs` に実装・偽証明書での REJECT 動作確認済み(試験ファイルは確認後に削除)。証明書 `certificates/e2c6/fixture_{ii,iii,F1,F2a,F2b}_*.json`(8件)。**64系本走査は未実行**(発射錠が閉じているため物理的に不可能)。falsifier 再監査待ち。

## 2026-07-26 — E2 class-6 二方向掃引: 発射前最終バッチ F5/F6+微修正(falsifier②PASS済み・implementer実行)

- 司令塔の発射前最終バッチを実装。**F5(研究者発案・実形合成)**: θ/𝒩 ブロック行列は実物構造のまま、右辺のみ ker(1+θ̄) から決定的疑似乱数で選んだ元の𝒩̄像に置換(実Ē_mは一度も不使用・盲検無傷)。初回の自由疑似乱数rhsでは60 seed中0可解だったため ker(1+θ̄) 経由の構成に自己修正、seed=1,2,3で即全可解(|K|=256/64/128、非自明重複度)・特解復元・mass check全PASS。**F6(falsifier推奨・恒久)**: q_θ=t5+t6/u4/u2 それぞれに非零q_N(F1/F2はq_N=0だった)を組ませた3対でObFromQPairの訂正項(inv3・θ行列積・減算)を非自明実行、obがq_N=0の場合と同値であることを実測(j=2でobがq_Nに依らない証拠化)。微修正2件: F1のGAPコメント出典を「委嘱16§4」に、M2の「override」記述を「Ē_m(0)=0により実系と一致」に訂正。**F1–F6全PASS(GAP・Node双方、証明書14件全PASS、SKIP 0件)**。発射錠は引き続きLOCKED(FIRE_e2c6.auth未作成)。**発射待機・全条件充足**。

## 2026-07-26 — E2 class-6 二方向掃引: 実宇宙本走査(発射・裁定20 ob式・implementer実行)

- 司令塔発行の`search/FIRE_e2c6.auth`(manifest v2 SHA-256一致)により発射錠解錠、`search/e2c6-sweep.g`で j=2・m=0..63 の64系を実行(GAP内部計測elapsed 1234ms・壁時計約5秒、600秒cap内)。発射錠のハッシュ照合コードに大小文字比較バグを発見・修正(auth大文字hex vs sha256sum小文字出力)。**線型段: 可解40系・不可解24系(m=2,4,6,10,12,14,18,20,22,26,28,30,34,36,38,42,44,46,50,52,54,58,60,62 — 汚染申告m=2を含め全系同一手順、特別扱いなし)。可解40系中 ob≠0 は13系、全て(ob_a,ob_b)=(0,1)(m=3,5,11,21,27,35,37,45,51,53,57,59,61)。残り27系は ob=(0,0)**。証明書`certificates/e2c6/sweep_j2_m{0..63}.json`(64件)。`crosscheck/check-e2c6.mjs`(agree6_sol2.json系統、実データ用claim `linear_stage_empty_c6`のNode側再検算ロジックを追加)で全78証明書(fixture 14件+実走査64件)独立再検算 **89 PASS・0 FAIL/REJECT/SKIP**。mass check(実データ版、kernel-enumeration方式M1相当・40系全bijective PASS — 委嘱16の群積によるM8そのものは今回未実装、スコープ注記あり)。実走査64件連結SHA-256=`7a373fa544937c6c01d6f7b92c7cf2f5feab09b4bb878a3259e84b79bb1545a8`、certificates/e2c6/全78件連結SHA-256=`ab4410b8f8d04a6bf61ace7f2c83ea3f5019ff0cc5b95b80540e022aa494faec`。数値の解釈(E15反例候補等)は本記帳では行わない — 機械事実のみ。

- 2026-07-26 セキュリティ処置: sol2 セッション ID ピンが public repo で追跡されていた(総点検 #8)→ git rm --cached 2 件・ローカルピン破棄(次回 sol2 起動時に新規セッションで再生成・旧 ID は resume ハンドルであり資格情報ではないが規律により回転)

## 2026-07-26 — E2 class-6 二方向掃引: M6(L_m全点重複度表)実装+バグ修正(委嘱17優先度変更・implementer実行)

- 委嘱17の発見(m と m+32 は同一系のはずが単一witness評価でob不一致・witness依存性)を受け、司令塔指示によりM6(線型段解集合 L_m の全列挙+ob重複度表)を実装、M8(route G本物群積)より優先。バグ修正: 不可解系証明書に`linear_solvable`フィールドが完全欠落していた(undefined≠false)のを`false`明示に修正、`check-e2c6.mjs`側も`linear_solvable`を厳密`===true`/`===false`で検査するよう堅牢化。
- **M6結果(実データ40可解系全数、GAP内部elapsed 9359ms・壁時計13秒)**: 全40系で ob 重複度表のキー集合は例外なく `{(0,0),(0,1)}` の2値のみ・**全40系で ob=(0,0) の点が存在("all_nonzero"=false、40/40)**。重複度は系ごとに |L_m| のちょうど半分ずつ((0,0):(0,1) = 1:1、|L_m|∈{64,128,256}に応じて32:32/64:64/128:128)。**m/m+32 の4対(3&35, 5&37, 21&53, 27&59)は重複度表が完全一致(IDENTICAL=true、4/4)** — 生成器バグ仮説は再現せず、単一witness評価が原因だったことと整合。
- 証明書: `certificates/e2c6/m6_j2_m{各可解m}.json`(40件、f0・K_generators・K_orders・ob_table 込み)。`crosscheck/check-e2c6.mjs`に`m6_multiplicity_table`claimの独立再検算(L_m全列挙をagree6_sol2.json系統で再構成し重複度表を再現)を追加。
- **両系統検算: 全118証明書(fixture14+実走査64+M6用40)129 PASS・0 FAIL/REJECT/SKIP**。証明書全118件連結SHA-256=`a3c0bd8a10a9e1032790b6bcc427370e32dcf6554498bc504cba1357d49e6d80`。
- M8(route G本物群積)は数学者エージェントによる設計検証のみ実施(collection_tableは[·,x]/[·,y]の交換子表・A はclass2でH(a)H(b)=H(a+b-κ(a,b))という閉形式一発・現行閉形式実装に符号バグ(+κであるべきところ-κ、mod2では消えるがmod4以上では効く)を発見、j≥3で要修正・司令塔裁定案件として記帳)。生成 GAP コード(FromTheLeftCollector版)・node検算スクリプトは数学者エージェントのスクラッチ領域のみに存在、本番スクリプトへの反映はしていない。解釈(なぜob_aが常に0か等)は本記帳では行わない — 機械事実のみ。

## 2026-07-26 -- レベル16双子セル列挙機 v1: 建造+較正①②完了(implementer実行)

- `search/twincell-enum.g`(行列mod L系統を新規実装・BuildMatQuotient/CheckMarkedBijection)+既存MakeGnで4窓(C8/C10/C16/K8)の建造完了。較正①(C8=K^(4)、行列mod8 vs D4^3のmarked factor map全単射)PASS・較正②(C10=N_A、行列mod10で|GT|=20再現)PASS。合成負例(level取り違えL=6)は正しくFAIL判定。標的窓(C16行列mod16・K8=MakeGn(8))はFIRE_twincell.auth未発行のため[LOCKED]、本走査未実施。`crosscheck/check-twincell.mjs`(独立node照合器、新規)で全証明書+較正+負例+自己テスト(証明書改竄検出)all_pass。証明書はcertificates/twincell/、詳細はdocs/notes/実装_双子セル.md。commit未実施。

## 2026-07-26 — E2 class-6: kappa符号バグ修理+F7(route-G本物群積)恒久fixture+mod4再走(j=3前提準備・implementer実行)

- **符号バグ修理**: `search/e2c6-sweep.g`・`crosscheck/check-e2c6.mjs` 両系統で `QThetaFullRaw`/`QNFullRaw` の kappa cocycle 項を `+Kappa` から `-Kappa` に訂正(class-5 実装 `Cs=-kappa` 規約・M8設計検証で確認済みのバグ)。**j=2 本番結果(実走査64件+M6用40件、計104証明書)は全てob値が修理前後でビット単位一致することを確認済み**(mod2では2*kappaの差が恒等的に消えるため、数学的に予見された通り)。
- **F7新設(恒久fixture)**: `kappa_terms`のみから`FromTheLeftCollector`でPcpGroup(21生成子・class2・6個の交換子関係)を構築(`IsConfluent=true`)、θ/σ_m を「昇順Hall順で table[k]^{a_k} を群積」として自己同型に拡張、q_θ/q_N を**本物の群積**(θ(g)g、E_m·σ²(g)σ(g)g)で計算し、符号修理後の閉形式と mod4 で突合。**10ベクトル×(θ1+σ4 m値)=50評価、全50件が mod4 一致・かつ50/50が厳密整数一致**(route-G構築はkappa_termsのみから、closed formとは独立な計算経路)。証明書`certificates/e2c6/fixture_F7_routeG_crosscheck.json`、node側は同ファイルのclosed_form欄をagree6_sol2.json系統で独立再計算し一致確認(群積自体の独立再構築はnode側未実装・GAP限定と明記)。
- **F1/F2/F6/M2/M3のmod4再走**: F1・F2・M2・M3は生の比較でR=2と同型の結果を維持(全PASS)。**F6(ob のq_N非依存性)は生の比較でR=4のとき一部(F6c)が R=2 と異なる値(ob_b: 1→3)を示した — これは実装バグでなく理論的に予見される境界**: 委嘱16 eq 0.3 の Ob≅R[2]a⊕(R/2R)b̄ という構造(b成分はR/2Rの商、Rそのものではない)により、(1+θ)K のu2成分は2R(R=2では自明に0だがR=4では{0,2}と非自明)であるため、q_N補正項がob_bを偶数だけ動かしうる(mod2では消える)。**mod2に還元すればF6c含め全て一致を再確認(F6再読解mod2は全PASS)**。この境界は委嘱16の自己申告(GAP-OB1: 「j≥3用の座標形は未導出」)と正確に整合し、実測で確認された形。**ob読み出し式そのものは今回変更していない**(j=3以降のご裁定・別manifestに委ねる)。
- **発射錠**: j=2用のまま変更なし。64系実走査(j=3相当)は実行していない。

## 2026-07-26 -- 【GAP-18a】K^(3) の 6 点作用と検出器 Lambda への F0 作用(implementer 実行)

- `search/k3-lambda-action.g`(GAP、MakeGn(3) 転用・LatticeSubgroups で位数18部分群18個を悉皆・4共役類 |Lambda|=3,6,3,6 を検出)+ F0={phi_k:k=0,1,2}(Thm4.3 (4.12) m=0 の hexagon-automorphism、GroupHomomorphismByImages+IsBijectiveで機械確認・生成群位数3)。**4共役類すべてでF0のLambda作用は非自明**(|Lambda|=6側: 像36・核3・不動点なしの2個の3-サイクル(委嘱18 sec2.1の主張と一致)/ |Lambda|=3側: 単一3-サイクル・構造的に自動)。発注書「Lambda(3元集合)」と正本委嘱18「Lambda(6元)」の不一致を発見・推測せず4通り全計算+速達箱(`ops/express/20260726_implementer_gap18a-lambda-ambiguity.md`)で確認要請。証明書 `certificates/k3/gap18a.json`(schema k3-lambda-action/v1)・詳細 `docs/notes/検算_18a.md`。commit未実施。

## 2026-07-26 -- レベル16双子セル列挙機 v1: falsifier監査(反証前哨_双子セル.md)の要求4件対応(implementer実行)

- falsifier監査(docs/notes/反証前哨_双子セル.md、PASS保留・要求事項1-4)を受け、司令塔指示により修理。
- **【重大】較正③新設**: K^(8)の既知値|GT|=16(Thm4.3/5.3、2^(2*alpha-2)、alpha=3)をGAP側(calib3Status/calib3KnownValueOk、FIRE unlocked分岐でのみRAN、locked中はstatus="LOCKED"で明示)・node側(check-twincell.mjs、K8_MakeGn8証明書があればcalib3計算、無ければ[LOCKED]と明示しall_pass判定はブロックしない)・calibration_summary.v1.json(calibration_3セクション)の三箇所に登録。既知値が実行コードから断線したまま発射される事態を解消。
- **【要修正】較正②upgrade**: 数値一致(|GT|=20)のみだった較正②に、既存A5置換構成(certificates/A1.v2.json marking、X=(1,3,2,4,5)、Y=(1,3,4,5,2))とのmarked factor map全単射(較正①と同水準、GroupHomomorphismByImages x->x,y->y・IsBijective・shadow対応)を追加。新規証明書`certificates/twincell/C10.a5permutation.v1.json`。あわせてA5-CONV適合テスト(ev(y x^-1)=(1 2 4)、docs/週次定義ノート§1.5.4)をtwincell固有のC10 matrix-mod-10構成に対して(C10-matrix<->A5の語転送経由で)直接実行、GAP側・node側とも新規PASS。
- **【要修正】証明書ハッシュ記載**: `certificates/twincell/`較正分5件+summary計6件(A5置換構成証明書の新規追加込み)のSHA-256:
  - C8.matrix.v1.json = `9a5b958df6cec3d6e786007acd7993411ea8c7ac7604c1578a0625be139f2411`
  - C8.d4cubed.v1.json = `463ad292fffbd1cf7d27d7d9d8122170af021fb090d3b251cdbb5ad0ae7ce89e`
  - C10.matrix.v1.json = `69b617a72572ae09959501a106000c98baa27062703ba904b420facebb44dfb6`
  - C10.a5permutation.v1.json(新規) = `daf5e669648249f2b62b6db7082e4a622866d27efe3573215b5f1467dfd7abd4`
  - C8.matrix.v1.WRONG_LEVEL6_fixture.json = `b73f386985ef97a4e925b6395e89361e625bb69ada99080224fe595d93ad758b`
  - C8.matrix.v1.Ybar_signflip_BONUS.json = `b441a1be9372be2d65ff93798d774f5e6c9e5d9b5c386b9f5cd5d933fee66d7d`
  - calibration_summary.v1.json = `35fd25d4e8f84ed6017dd25d5677d52b11696806e2071a7009d17affe323024d`
  - 上記7件連結SHA-256 = `7b6dbddfac2293e9f01c68a11bffbdf9d1383d8df83bae89812b4a2b4b07e25d`
- **【軽微・対応済み】**: check-twincell.mjsのper-cert出力ラベルに「[self-consistency of this certificate]」注記を追加(負例fixtureのPASS表示が「較正合格」と誤読されるのを防止)。A5-CONV適合テストをtwincell固有構成に対して明示実行(上記)。
- **再実行結果(GAP+node二系統)**: 較正①PASS(matched=4/4)・較正②PASS(数値20+bijection matched=20/20+A5-CONV一致)・較正③はFIRE未解錠のため[LOCKED](既知値16との照合コードは接続済み、発射後に自動実行される)・負例fixture正しくFAIL判定PASS・証明書改竄自己テストPASS。`node crosscheck/check-twincell.mjs`: `check-twincell.mjs overall: all_pass`。
- manifest本文への数値cap・エスカレーション先の明記(falsifier要求4)は司令塔対応事項のため本記帳では未対応。commit未実施。

## 2026-07-26 -- レベル16双子セル列挙機 v1: 発射・標的2窓本走査(FIRE_twincell.auth解錠・implementer実行)

- 司令塔発行`search/FIRE_twincell.auth`(内容=manifest v1現行SHA-256 `CB7EC23F...19D4`)により解錠。実行前に settled/isolated 判定コードが未実装だった欠落を発見・修理(`ComputeSettledIsolated`: 誘導写像 x|->x^u, y|->f^-1 y^u f が G 自身への全単射かを`GroupHomomorphismByImages`+`IsBijective`で判定、較正①②のmarked-factor-map機構の再利用)。修理中に別バグ(`WriteTwincellCert`ラッパーが値を返さない関数に`return`を付けていた"Function Calls: must return a value"エラー)も発見・即修正。
- **𝒞₁₆(行列mod16, Q_16=<Xbar,Ybar><=SL(2,Z/16)/{+-I})機械事実(未知量・予測との突合なし)**: |Q_16|=256・staged counts(排他)= candidate_total=32, h10_fail=0, h11_fail=24, generation_fail=0, shadow_total(=|GT|)=**8**・settled=8/8・**isolated=true**。
- **K^(8)(=MakeGn(8), Im(psi_8)<=D_8^3)機械事実**: |G_8|=256・staged counts= candidate_total=128, h10_fail=64, h11_fail=48, generation_fail=0, shadow_total(=|GT|)=**16**・settled=16/16・isolated=true。**較正③(既知値|GT|=16, Thm4.3/5.3 alpha=3): PASS**(GAP・node二系統とも)。
- **走行時間**: GAP内部計測(Runtime()差分)219ms、外側PowerShell Stopwatch壁時計3017ms(gap.ps.1起動含む)。600秒capに対し十分小さく shard分割等は不要だった。
- **node独立検算(`crosscheck/check-twincell.mjs`)**: settled/isolatedの独立再検証ロジックを新規追加(語のBFS+誘導写像の像サイズ判定、GAPの`GroupHomomorphismByImages`は使わない別実装)。全8証明書(較正分6件+標的2件)self-consistency PASS、較正①②③・負例fixture・証明書改竄自己テストすべてPASS。`check-twincell.mjs overall: all_pass`。
- **証明書SHA-256(`certificates/twincell/`全8件)**:
  - C8.matrix.v1.json = `9a5b958df6cec3d6e786007acd7993411ea8c7ac7604c1578a0625be139f2411`
  - C8.d4cubed.v1.json = `463ad292fffbd1cf7d27d7d9d8122170af021fb090d3b251cdbb5ad0ae7ce89e`
  - C10.matrix.v1.json = `69b617a72572ae09959501a106000c98baa27062703ba904b420facebb44dfb6`
  - C10.a5permutation.v1.json = `daf5e669648249f2b62b6db7082e4a622866d27efe3573215b5f1467dfd7abd4`
  - C8.matrix.v1.WRONG_LEVEL6_fixture.json = `b73f386985ef97a4e925b6395e89361e625bb69ada99080224fe595d93ad758b`
  - C8.matrix.v1.Ybar_signflip_BONUS.json = `b441a1be9372be2d65ff93798d774f5e6c9e5d9b5c386b9f5cd5d933fee66d7d`
  - **C16.matrix.v1.json(新規・標的) = `8ffc7a060b009dc4a3982c835db2630dcc9aba6f11920adbb9390bcd2008767f`**
  - **K8.dncubed.v1.json(新規・標的) = `fec658d830e4aa92bf1e8f9f59c71d3b9c73c2dff0b49e7aa77c2374c3b2c413`**
  - calibration_summary.v1.json = `77ef30aa8e39f42c4ac45429e7e3cfb4d5f643571ee6b93c6a9bc06a5515c670`
  - 上記9件連結SHA-256 = `55fd53374b152db16ed7c2c5d4388ec33513c3ae69c53c81eda273f65e6d3bfc`
- 𝒞₁₆の|GT|=8・settled 8/8・isolated=trueは観測事実として記帳するのみ — 解釈・予測との比較は行っていない(司令塔指示「観測が先」)。commit未実施。

## 2026-07-26 -- レベル16双子セル列挙機 v1: 事後デルタ2件(kernel_certificate生成的化・settled強化)対応(implementer実行)

- falsifier「事後デルタ監査」追記2(docs/notes/反証前哨_双子セル.md)の要求2件に対応。
- **【重大→解消】kernel_certificate を生成的に**: 旧版は`pb3_kernel_index`/`b3_kernel_index`(既存universeフィールドの数値重複)+テキストjustificationのみで、node側は当フィールドを一切参照していなかった(grep 0件)。新版は`generator_images`(N=ker(psi:F2->>Q)を定義する psi(x),psi(y) の実際の生成元像、machine-parseable文字列 -- matrix窓は`"[[a,b],[c,d]]"`・D_n^3窓は`"[[a1,e1],[a2,e2],[a3,e3]]"`・A5窓はGAPサイクル記法)+`verification.generation_verified`(Size(Group(images))=pb3_indexで「部分群でなく完全に claimed group を生成する」ことの確認)を追加。`crosscheck/check-twincell.mjs`に対応する検査ロジック(`parseGeneratorImageMatrix`/`parseGeneratorImageDnTriple`/`parseGapPermString`)を新規実装、8窓全証明書のkernel_certificateを独立に parse・自前構築した(G,X,Y)と突合・generation_verified再計算・pb3/b3_kernel_index再計算。実測: K8証明書のgenerator_images.yを意図的に破壊したclone(`[[9,9],[9,9],[9,9]]`)を作り、`node crosscheck/check-twincell.mjs`が正しく`FAIL -- kernel_certificate.generator_images do NOT match...; kernel_certificate generators only generate a subgroup of size 64, not the full claimed pb3_index=256`を検出することを確認(検出力の実測)。
- **副産物として発見・修理した独立バグ**: `MatCanonL`/`matCanonL`の正準化が「入力を先にmod L還元してから比較する」になっておらず、生の整数リテラル(種生成元Ybarの`-2`)と既に還元済みの同じ元(`L-2`)とで異なる整数キーが計算され、GAP側とnode側が異なる代表元を「正準形」として選びうる不整合があった(kernel_certificate突合を実装して初めて露見しうる潜在バグ)。GAP・node双方で「まずmod L還元してから比較」に統一修理。修理後、generator_images.yは`[[1,0],[14,1]]`(mod16還元済み、旧`[[1,0],[-2,1]]`から変更)のように正しく[0,L)範囲で出力される。
- **【要修正→解消】node側settled再検証を強化**: 旧版はBFS全域木の代表語のみをtargetX/targetYで再評価し、その像集合の濃度が|G|と一致するかだけを見る「弱い」チェックだった(全域木に含まれない非木辺・Cayleyグラフの関係式は一度も検査していなかった)。新版は全要素g∈G×全4生成元方向(x,+-1 / y,+-1)についてF(g*gen)==F(g)*targetGenを悉皆検査する「完全なCayleyグラフ整合性チェック」(falsifierの第三スクリプトと同じ方法論)に格上げ。計算量|G|×4(最大256×4=1024回)で軽量。
- **観測値への影響確認**: 𝒞₁₆=8・K^(8)=16・settled 8/8, 16/16・isolated=trueは**全て不変**(再実行で完全再現、GAP内部219-250ms・壁時計約2.9-3.0秒)。
- **全証明書再生成+両系統再実行結果**: GAP側 較正①②③・負例fixture 全PASS。node側`crosscheck/check-twincell.mjs`: 全8証明書self-consistency PASS(kernel_certificate検査・強化settled検査を含む)、較正①②③・負例fixture・証明書改竄自己テスト全PASS。`check-twincell.mjs overall: all_pass`。
- **証明書SHA-256(`certificates/twincell/` 全9件、kernel_certificate生成的化により全て再生成・ハッシュ変更)**:
  - C8.matrix.v1.json = `34474df387db4fd72ffb997e5370a5e48f0855cc6ccb859fa9f9e983844ef96b`
  - C8.d4cubed.v1.json = `1362c3eea306e49c3004356ae26dd9ac1416c1242102f9ca302c7291eaf1381e`
  - C10.matrix.v1.json = `497087feba27cee174f6f3a3c8db9872190072dfc718d6928093958f22e661f4`
  - C10.a5permutation.v1.json = `69ca1a313f6ebcf2f168bf77e2017d8d0a5a300202fce12885b30684996658ce`
  - C8.matrix.v1.WRONG_LEVEL6_fixture.json = `2c4f56611610df1469c9c1532cdfc92128dc1bf70340eb04c692cb6b2e0a6632`
  - C8.matrix.v1.Ybar_signflip_BONUS.json = `bb0a774b98915e19ed1791958a28c9004d5b5a67ac1b4e04c42d9ae566a7edae`
  - C16.matrix.v1.json = `f1c2c3f044ff4c4933e433572150fb346343a664ab374049860c0e018bf8b91b`
  - K8.dncubed.v1.json = `532ec2b17fb517179ccbb45e789cea9b24e3116e4eed58dde5dd107b7e791a5f`
  - calibration_summary.v1.json = `77ef30aa8e39f42c4ac45429e7e3cfb4d5f643571ee6b93c6a9bc06a5515c670`(不変・kernel_certificate生成的化はcalibration_summaryのスキーマに影響しないため)
  - 上記9件連結SHA-256 = `d41f8ccde32f7c848f17e4e3abbbb1e7bf9626545813a2ceb2fe34d7243f32e8`
- commit未実施。

## 2026-07-26 -- E2 class-6 j=3 ゲート実装(発射保留・implementer実行)

- `docs/manifest_e2c6j3_v1.md`(SHA-256 `aea71b16345a1878ea96152d12a8e8602307b97c0c38c24cfe81c3f5f782005a`)発注に対し、
  `search/e2c6-common-data.g`(共有データ・j=2確定済み`search/e2c6-sweep.g`は不変)・`search/e2c6j3-sweep.g`
  (便24 §F8のみ読取・§F7封印遵守。eq8.1-8.4のλ公式+k_w=0前提+M6型重複度表をλ-shortcut/brute-force二系統実装)・
  `crosscheck/check-e2c6j3.mjs`(agree6_sol2.jsonのみ入力・brute-forceのみで独立再検算)を新設。
  fixture G1-G4 全PASS(GAP側・node側とも)。証明書5件 `certificates/e2c6j3/`。64系本走査は
  `search/FIRE_e2c6j3.auth` 未発行につき未実行(fire lock CLOSED確認済み)。詳細: `docs/notes/実装_j3.md`。
  commit未実施。

## 2026-07-26 -- E2 class-6 j=3 ゲート: falsifier監査(反証前哨_j3.md)対応の修理一式(implementer実行)

- 対応した修理: (1)【重大】RunRealSweepC6J3にk_wガード実走装備(CheckPremiseKw、違反時
  precondition_violated_c6j3で当該m ABORT、λ非適用)+注入違反での単体動作確認(GUARD fixture)。
  (2)便24§F8残り4項のうち3項実装: 不可解系dual witness(G1b、疑似乱数rhsで実際に不可解系を
  発生させ検証)・2×d bit matrix+rank証明書格納(lambda_bit_matrix/lambda_rank)・m→m+32周期性
  fixture(G8、EmBar15/EmC6/W(m)の公開構造データのみ・等号は観測記録に留め合否判定にしない)。
  項目5(中心補正×8・直接群積M8照合)は central extension の具体的構成が未指定のため実装せず
  保留と明記(次便で司令塔/数学者に構成指定を要請)。(3)ObFromQPair(R=4)をnonzero q_Nで実際に
  呼ぶ恒久fixture G7を追加(ob mod2独立性を確認、raw a係数のR=4意味論は未解決のまま明記)。
  (4)search/e2c6-common-data.gとsearch/e2c6-sweep.gの7ブロックのbyte一致を自動検査する
  crosscheck/check-e2c6-common-data-drift.mjsを新設・ALL PASS。(5)発射錠の誤ハッシュ試験
  (前回falsifier監査でタイムアウト)を再試行・今回はLOCKED応答を正常確認(壁時計1秒未満、
  試験用authファイルは削除・不存在確認済み)。
- 実装ノート`docs/notes/実装_j3.md`を「§F8を逐語実装した」という過大申告から
  「実装済み項目の列挙形」へ全面改版(司令塔指示)。
- 全13証明書(GAP側fixture実行+node側crosscheck/check-e2c6j3.mjs)ALL PASS。
  FIRE_e2c6j3.authは作成していない(現在不存在)。commit未実施。

## 2026-07-26 -- E2 class-6 j=3 ゲート: 便24 F8 item 5 実装(設計_F8項目5.md・Opus起草、implementer実行)

- 司令塔小委嘱の設計指定(docs/notes/設計_F8項目5.md)に従い、中心補正×8・直接群積M8との
  mass照合(M8-a torsor律/M8-b fiber実現/M8-c mass恒等式(本体)/M8-d負の統制)を
  search/e2c6j3-sweep.gに実装。G3CExtractは流用不可のため21成分フル判定の新関数
  (G3RouteGQThetaFull21/G3RouteGQNFull21/IsIdentityInCellAj)を新設。
- **符号はM8-aで実測決定**(+で全48検査一致、−は不一致 — 決め打ちせず実測)。
- **自己発見バグ1件**: M8-b初回実装は全ob=0証人に一律kerΛを使っていた(Ξ(g)=0の証人にしか
  正しくない)。証人固有のΛ-ファイバー(-Ξ(g)のコセット)を使うよう修正しPASS。
- **数学的発見**: raw ObFromQPair出力は真のOb=4元群(委嘱16 R[2]a⊕(R/2R)b̄)のクラスとしては
  ob_bをmod2で読む必要があると実測確認(m=0でob=(0,0)と(0,2)は同じ真のクラス — 両方とも
  Λ-ファイバー非空)。G7で「未解決」と記録したR=4座標意味論の一部をM8系列が独立に裏付けた。
- **テスト可能性のスコープ限界(設計の破れではないと判断)**: M8-b/c/dはm=0のみ盲検安全に
  テスト可能(合成系・F5型どちらでもm>0ではq_N(f,m)のσ-不変性〈j=2のM2前提と同型〉が破れ、
  Λ-ファイバー判定が全点で空になることを実測確認 — 「−Ξ(g)∈im(Λ)⟺ob=0」の等式は本物の
  Ē_m(m)アフィン解を前提とするため、実m>0データなしには検証不可)。M8-aは前提を要さない
  恒等式のためm∈{0,1,2,3}全てで妥当にPASS — この対比を根拠に「設計の破れ」でなく
  「盲検制約下のテスト可能性限界」として区別して報告。
- 全14証明書(既存9件+M8c 1件)GAP・node両系統ALL PASS。M8c証明書はf0/K_generators/K_orders
  込みでnode側が完全独立にL_m再列挙+LambdaTable再構築(check-e2c6j3.mjsに追加)。
- 詳細: docs/notes/実装_j3.md 追記節。FIRE_e2c6j3.authは作成していない(現在不存在)。
  commit未実施。

## 2026-07-26 -- E2 class-6 j=3 本走査(発射・FIRE_e2c6j3.auth解錠、implementer実行): 線型段可解20/64(m={0,1,7,9,15,16,17,23,25,31,32,33,39,41,47,48,49,55,57,63})・k_wガード発火0件・重複度表に4種の(ob_a,ob_b)キー出現("0,0"20件・"0,1"20件・"1,0"/"1,1"各8件、全零単独の系は0件)・M8-b/c/d実データ版(m=0,1,7,9,15,16の6系)全PASS(M8-d判定でOR→AND修理を自己発見・全証明書再生成)・GAP側全証明書96件+node独立検算(check-e2c6j3.mjs)全PASS・GAP内部経過35750ms(本走査+M8実データ部分30156ms)・sweep_j3_m*64件連結SHA256=eaca0f396510f2d6e5c13052323405c086578d47839e6af5cb50c49c9ed48941・certificates/e2c6j3/全96件連結SHA256=1add4bf7923454c4474bf244bfd59009bef883bcb2b6840b45ed2af5aa3144a7。封印§F7との照合は実施していない(裁定時に司令塔が行う)。commit未実施。

## 2026-07-28 -- I-1 族窓観測 + I-3 先行手(等号検査)実装(implementer実行)

- 入口条件: search/suite-wp1.g を `.\gap.ps1` 経由で再実行、WP1 ALL PASSED を確認(回帰健全)。
- **I-3 等号検査**(search/mixed-equality-check.g 新設): B3 の (psi_4, psi_3) の像を
  D4^3 x D3^3(21点)内に生成元 x,y から直接構成(c は両写像で単位元に落ちるため寄与なし)。
  |Im(psi_4,psi_3)| = 864 を実測。事前登録済み比較値(provenance/registered/universe_I1_I3.md
  記載の 6912 = 4*12^3)とは**不一致 → 判定 NOT_EQUAL**。ただしこのセッション内で
  MakeGn(12) を参考構成すると |G_12| = 864(WP1 の既知値と一致)であり、imageSize と
  完全一致した。**設計上の疑義として報告**: 6912 は n=12(偶数)に奇数用の式 4n^3 を
  誤って当てはめた値である可能性が高く、n=12 の正しい式(偶数用 4*(n/2)^3)による
  |G_12|=864 と imageSize=864 が厳密一致することは、K^(12) = K^(4) ∩ K^(3) が
  **実は等号として成立している**ことを強く示唆する観測事実である(指数の一致に
  頼らず像そのものを構成した結果としての一致であり、Sol 警告の「指数の偶然一致」の
  トラップには該当しない)。この解釈・登録比較値の訂正要否は司令塔/数学者の判断に委ねる。
  証明書: search/certs/i3_equality_20260728.json。
- **I-1 族窓観測**(search/family-window-survey.g 新設): n in {3,5,7,9,11} の全てで
  較正ゲート |P_n|=4n^3 PASS。列挙述語①[P_n:H]=2n ②自己正規化 ③<X_n>推移的 を
  満たす H を SubgroupsSolvableGroup(Size による事後フィルタ併用・IndexEqual/OrderEqual
  オプションは GAP 4.16.0 で機能しないことを実測確認)+ RightTransversal による
  自己正規化共役類の厳密展開(2n 個)+ 個体ごとの FactorCosetAction 推移性検査で列挙。
  **実測**: n=3→12, n=5→40, n=7→84, n=9→144, n=11→220。**事前登録仮説(該当個数=4n)は
  n=3(12=12)でのみ一致し、n=5,7,9,11(20,28,36,44 との比較)は全て不一致**。実測値は
  2n(n-1) の形(n=3:12, n=5:40, n=7:84, n=9:144, n=11:220 が厳密に一致)に見えるが、
  これは観測記述であり定理主張ではない(解釈は司令塔/数学者へ)。各 n で該当 H は
  複数の P_n-共役類に分かれ(n=3:2類・各6個、n=5:4類・各10個、n=7:6類・各14個、
  n=9:8類・各18個、n=11:10類・各22個)、いずれも「フルサイズ=passing」(自己正規化
  共役類の中で一部だけ通る例はこの5点では観測されず、通るときは全通り)。
  証明書: search/certs/i1_survey_20260728.json。UNKNOWN 該当なし(全 n で較正ゲート PASS)。
- 実行時間: family-window-survey.g 全体で秒単位(n=9 が最重で約4秒)・shard 化不要・
  600秒 cap に対し大幅余裕。
- ハッシュ: search/mixed-equality-check.g = `387b4d98ce43b663471ecdadb5727a49c0e0ca4351a5d6940e8ca4d90a434934`、
  search/family-window-survey.g = `a2a88a7035cbf898a58915dd1ceae10b2f3abe65bd068bc100fa6aa18bdebca7`、
  search/certs/i3_equality_20260728.json = `55235296ab6ab82f8a4c54e4c04b4e63855b81b8a2b1a76fbdbbc61c9858b6cd`、
  search/certs/i1_survey_20260728.json = `2272695979c8d5664d00f4bb4876990d3826bbc9644b46f8e742a58c9cc50a74`。
- 照合器(node/python)未実装 — 両証明書は candidate のまま(cross-checked 昇格は後日)。
- commit未実施。

## 2026-07-28 Actions 工場(壁キャンペーン)
- 煙試験 PASS: run 30370327355(65 秒)。gap-actions/setup-gap@v3.8.0 で GAP **4.16.0** 公式 tarball(sha256 検証つき)をソースビルド・lins **0.9** — ローカルと完全同版。
- 二環境一致: B₃ 正規部分群 指数≤24 = **33 本**(CI smoke)= ローカル probe(wall_probe_20260728.json)。
- workflow: .github/workflows/wall-smoke.yml・証明書は artifact 回収方式。runner = ubuntu-latest(4 vCPU/16GB・public repo 無制限)。

## 2026-07-29 第一撃 W-D-A16-11a
- CI run 30392894007(gap-run)は 30 分 timeout で cancel(真因 = legacy crosscheck の 10¹³ BFS)。修理(JUDGE_SKIP_LEGACY_CROSSCHECK)後**ローカル本走で完走**(数分)。証明書 = search/certs/strike_a16_full_20260729.json。
- 判定: shadow 880(settled 全)・ker χ̃ 位数 88 **非可換**(witness 2 置換)・G_N 導来列 [880,22,1]。scan_mode = xi_restricted・scanned 8,712,000・圧縮 1.2×10⁷。GAP 4.16.0・単系統(witness 独立検算を別途)。

## 2026-07-30 文献ゲート配達(きっかけ = ① 要請駆動: structthm_h2_v1.md §7.3【文献要請】)
- 配達物 = 翻訳覚書 docs/notes/litgate_epsilon_translation_v1.md + 原文 5 本(papers/delivered/):
  - arxiv_2603.24743.pdf (Galindo, Clifford 拡大の分裂 ⟺ 4∤|A|) sha256 eadee8a8b79e61d36b1f03d443fd494406e1a9e8b724b9b28ee2e00c7df63890
  - arxiv_2305.13178.pdf (Korbelář–Tolar, 巡回の場合の初等決定) sha256 583504d03ee08645cef25f38b8d228020d289f08b753e054c9b27ce7dec4893d
  - arxiv_1604.04415.pdf (Guillot, GT₁(PSL(2,q))) sha256 16a2496e4c4929570bbc8d330070dea92f0a08cb0d1dad01a2a9dbcee834cdea
  - arxiv_1407.3112.pdf (Guillot) sha256 416c0a91ef7bbb2eb7b8e615d8d209083232965f1151c3e2832256110806784b
  - arxiv_math_0606374.pdf (Pakianathan–Yalçın) sha256 940d9d3fa40b1bbd509e75a9a2cdf925330ebc19d9f7e30bf5e9f9d662c2af2d
  - Griess 1973 (Pacific J. Math. 48, 403–422) は誌面のみ — 書誌+入手経路注記で代替。
- 一工夫(翻訳)= 型 I の字面不適合の突合(4||Q| でも分裂 ⟹ 方法のみ輸入)・型 II = STR-1.6 の外部検算・本命 = ε 閉形式(【LG-1】【LG-2】)。型 III(Guillot)は同名別物ゲート未架橋のため設問化保留。
- 配達先 = 両数学者(Opus = SendMessage 済・Sol = 便 85 同梱)。scout 報告書は docs/scout/ へ移設(開示済みアーカイブ)。
- **工程反省**: 遠征報告書を金庫 scout でなくリポジトリ(ops/)に直接置かせた(配置図規則 (2)(5) 違反)・初回配達が覚書のみだった(「論文+覚書のセット」既定の違反)。本記帳で是正。以後 hunter/scout の出力先は委嘱時に金庫パスを指定する。

## 2026-07-30 文献ゲート配達 2(きっかけ = ① 要請駆動: surj_d4_t1_v1.md【文献要請】= 半局所 Kummer)
- 配達物 = 翻訳覚書 docs/notes/litgate_semilocal_kummer_v1.md + 原文 6 本(papers/delivered/):
  - arxiv_1301.4429.pdf (Borne–Emsalem–Stix, packet+torsor) sha256 95faad8f8dc971c22a781360ddefe5d5b64bc5316579182be3f68f4f6f105ae3
  - arxiv_0809.0017.pdf (Stix, cuspidal sections) sha256 b456de5edf8dcbd52b5e414d24a87ff942908aac6f06fe2b7f175b32695d21bb
  - arxiv_1507.07208.pdf (Callegaro–Gaiffi–Lochak) sha256 f8ee1666d8b952f3b8419b855183fbe3829fe524c68601e13bb7bd74ec5490fc
  - arxiv_2408.13108.pdf (Dupont–Panzer–Pym) sha256 886997fa9d99b60c50fe3d5c08d88f5fb33916e8ea054b642b18e25bf49bd3b6
  - arxiv_1504.02814.pdf (Sijsling–Voight) sha256 979ac2166c4989901d01334684c8a5192c0b896fa306d5636b2ccd1b1ddd1644
  - arxiv_2506.11310.pdf (O'Dorney) sha256 f1d59eb8d50a1f48214f38e125eb2f0fe764689cbf39265f05418e34c94cbea0
  - Jacobson–Vélez 1990 (manuscripta math. 67, 271–284, DOI 10.1007/BF02568433) は誌面のみ — 書誌+入手経路注記。
- 一工夫 = NORM-U/MARK-U の候補定義対・型 C(束ねない)警戒・新規性警報(層 II は古典既決の疑い — 突合義務)・LG-3/LG-4 設問化。
- 手順 = 金庫 scout 出力 → 配達判断 → docs/scout/ 移設(是正プロトコルの初の完全適用)。配達先 = 両数学者(Opus = SendMessage・Sol = 便 86 同梱)。

## 2026-07-30 r=4 判別窓 C 枝の CI 測定収蔵(裁定 235)
- CI = gap-run.yml run 30494156803(workflow_dispatch・script=search/strike-r4.g・preamble `R4_ONLY_WINDOW:="C";;`・GAP 4.16.0(gap-actions/setup-gap\@v3.8.0)・-o 12g・47 分)。driver 凍結 = commit 207d904(接触遮断仕様 search/_r4_driver_spec.md)。
- 収蔵証明書(artifact `gap-run-out` から司令塔回収・sha256):
  - search/certs/r4_W_E_A20_5x4t0_C_20260730.json = cf8221381267fafd0900865ed560d9b50bd122e9b3806af329ea8b5b49a0e47a
  - search/certs/r4_gate_20260730.json = d580bcb3314a343e5f75d73b463244a6d197ebed5ecbd868ba946d34a444c847
  - search/certs/r4_manifest_C_20260730.json = e9f663776ed2830a06d89644364db898dec368575afe56b91e0f2641e10506dc
- 判定(**裁定 236 — 初版記帳は裁定 235 の誤値転写につき本行で訂正**・突合先 = docs/notes/r4_prediction_v1.md 凍結 fd5aab9): 実測 = |GTSh|=800・|ker χ̃|=**200**・奇部 **25=5²**・2-部 8・IdGroup ker=[200,31]/GTSh=[800,1034]・A≅C₅×C₅・K 直積 test false・Q(C₄)の A 作用非忠実・canonical_id_sha256=d49d2556…(凍結表一致・P-R4-0 PASS)・stage1 all_pass・Ξ 走査 4×112,500,000(上界内)。**NULL-R4 発火((25,8)=形破綻枠)= PRUNE(40)も旧律(1000)も FAIL・核側 s₂ 律は (r=4,t=0) で偽**。P-R4-9(Ξ 埋め込み)・P-R4-10(STR-1.6 判定・ε=0)は PASS。定理 PRUNE-FIX(抽象群側)は無傷。正本 = sol/裁定_236_r4C窓真判定_235撤回.md。
- **B 枝(ε=1・S₂₀)発射記録**: run 30543709450(同 driver・preamble `R4_ONLY_WINDOW:="B";;`・timeout 120 分・2026-07-30 12:42 UTC)。着弾で P-R4-8(ε 依存性)判定へ。

## 2026-07-30 採掘場 mine v0 発足(裁定 237)と受け入れ試験 PASS
- ideas_013(発案係)採用 → implementer 実装(worktree・merge 74bf5d7): mine-job/v1 schema・preflight 3 ゲート(schema/integrity/予言)・統一配車 mine-dispatch.yml(plan push 駆動)・collector 最小・miner 係職務規程。判定ロジック側は無改変。
- 第一号ジョブ = 梯子 13 窓の較正再走(plan: mine/jobs/queue/ladder-recal-20260730.json)。CI run 30547092434(発火 = plan push・GAP 4.16.0・-o 12g・約 15 分)・result.txt: verdict=done・gap_exit=0。
- collector 検収(artifact のみ読取・ログ非参照): **再現照合 13/13 REPRO_MATCH(CI 再走 cert = 収蔵済み cert)・対付け集計 13/13(GAP explorer ⟷ python checker)** → **v0 受け入れ試験 PASS**。レポート = mine/reports/ladder-recal-20260730_report.md。
- v1 残: 窓 shard knob(較正回帰つき)・述語台帳の棚入れ 10〜15 枚・certs メモ化・ジョブ専用 out_dir(分類不能 99 件の解消)。

## 2026-07-30 r=4 判別窓 B 枝の CI 測定収蔵と P-R4-8 判定(裁定 236 追記)
- CI = gap-run.yml run 30543709450(script=search/strike-r4.g 凍結 207d904・preamble `R4_ONLY_WINDOW:="B";;`・GAP 4.16.0・-o 12g・77 分)。
- 収蔵: search/certs/r4_W_E_A20_5x4t0_B_20260730.json = 620c97f5310203781b38e67b85949e6832d05d34489d989aa279f35e4e358236・search/certs/r4_manifest_B_20260730.json = 9cc613955d79d47b42fd1df4a6d3ca070c117454bb939ced870ff3de8332ad84。入口ゲート再通過(実質同一・経過時間欄のみ差 = C run 版を正本のまま維持)。
- 実測(B 枝・ε=1・S₂₀): |GTSh|=2000([2000,931])・|ker χ̃|=500・奇部 125=5³(A≅C₅³=[125,5]・座標 125 本)・2-部 4(S′≅C₂×C₂)・K=[500,53] 直積 test false・χ̃ 像 C₄ 非忠実・dl=2・Ξ 埋め込み PASS(ker=1・像 2000⊆N(60,000)= 11 窓目)・u≡−1 層位数 2 中心化 100(P-R4-10 基準 10 と不一致)・会計 4×112,500,000 上界内。
- **P-R4-8 = FAIL(6 欄全相違)**: 入力(Stab 15000・Syl₂=D₈・B_x=625・N=60,000)は両枝同一を機械確認の上で核・GTSh が全相違 ⟹ **GTSh は窓の E-構造(ε)に依存 — 予想 COARSE(ideas_010 I11-C)反証**(凍結 FAIL 条項どおり・一級)。C=(25,8)/B=(125,4) で t=0 の破れ方は枝依存。撃ち切り完了(唯一の両パリティ族・一回性測定)。正本 = sol/裁定_236 追記。

## 2026-07-30 r=4 A 座標 probe(C 窓)着弾 — A = {(a,a,b,b)} の同定(裁定 236 追記 3)
- mine 経由(plan: mine/jobs/queue/r4-acoords-C-20260730.json)・CI run 30548906952・verdict=done。probe = search/probe/wac_v1/r4_acoords_probe.g(m=0 層のみ再走査・ker=層群の fail-closed 同値 assert つき)。
- 収蔵: search/certs/r4_acoords_C_20260730.json(会計 m=0 走査 112,500,000 上界ちょうど・accepted 200・ker_size 200・同値 check true)。
- **実測**: A(奇部・C₅²)の 25 座標 = **{(a,a,b,b) : a,b∈ℤ/5} 全体**(型集計: diagonal 5・AABB_{12|34} 20・ABAB 0・ABBA 0・other 0)。S=D₈ の共役作用の軌道は size 1/2(a↔b 交換)。
- 司令塔読み(candidate): A = B^{⟨(12),(34)⟩} = **D₈ の可換鏡映部分群の固定空間** — 刈り込みに効いているのは S の可換部分のみ、という「非可換 Syl₂ 境界」仮説(裁定 236 追記 2)の精密化と整合。解釈の確定は数学者(SAT-L1 線)へ。
- 配車の教訓 2 件: ①preamble の GH 式補間で GAP 引用符が食われる欠陥 → plan JSON から python 直接生成へ恒久修理(初回 run 30548585598 は両ジョブ無出力死・result.txt が fail-visible に捕捉)②concurrency 単一グループの pending 1 枠仕様で B 窓 run 30548910493 が後続 push に追い出され cancel → plan 単位グループへ修理。B 窓 probe は再発射。

## 2026-07-30 A 座標 probe B 窓着弾(三重照合成立)+ P-CENT-1 実現探索陰性 + 文献回収(裁定 238 追記 2)
- B 窓 probe(mine・run 30550189874・verdict=done): search/certs/r4_acoords_B_20260730.json = e72df35c758bb063429449d0524e5ebe2831e69ee7e4b7e7f2aa5b8deb9b7b77。A の 125 座標 = {(a,a,c,d)} 全体(diagonal 5・AABB 20・other 100)・[125,5]・会計 112,500,000 上界内。**三重照合**: CI probe = 数学者独立 probe(sat_l1_probe2.g・CI 着弾前測定 = prediction-first)= 仮説 Y 予言。機構 Y(w の 2ℓ-巡回のブロック束ね)確定・X 説反証。
- cent1 実現探索(ローカル・類完備): search/certs/cent1_existence_20260730.json = 68989a887a2898ee4ff9d9704261700a125b5dc43a4a39b11d9460df26a1574b。a₁ 類 4725 全数・適合 50 対の生成群は全て位数 60(A₅ 型)・exists=false — **n=10 判別窓は不存在(陰性・一級)**。判別は n=15 候補へ。probe = search/probe/wac_v1/cent1_existence_search.g。
- 文献回収(剛性/Hurwitz 遠征・配達準備): papers/delivered/ に arxiv_math_0609118.pdf = 4e457fe5475a661d8e3771438c0382cc4542fbddb168562b97221955b7ef4103・arxiv_math_0304376.pdf = 5b05a2b6ea43bfc960d0cc3734f8955db23a48f8234b6947de545545e80551cb・arxiv_1012.5297.pdf = d7801c497f7732396e328c3539168f431e1cc9733f7bab6b142326504740958a(いずれも %PDF 有効)。Hall 1936 一次確認 = DOI 10.1093/qmath/os-7.1.134。覚書(一工夫)起草後に両数学者へ同時配達。

## 2026-07-30 Sol 便 88 返信受領(裁定 239)
- sol/sol_reply_88_math15.md(23:01 着・digest 13 件全一致・Get-FileHash 再計算)。分割 PASS/差戻し: **PRUNE-FIX 定理確定(相互監査 PASS)**・r=4 artifact 検収 PASS・P-R4-8/COARSE FAIL 確定(scope = Stab-only 反証まで)・**司令塔誤判定 2 件の訂正受理(P-R4-7 両枝 PASS・P-R4-10 の ε 解釈撤回 = branch label と H² の ε の混同)**・上包含 Ξ(ker)⊆Pr(H) 位数反証・**(o) 発効 (A) = EP v7 NO-GO 継続**(全置換 probe で PASS 実証・P88-o 5 条件)・SAT-T1 修正版 PASS・**SAT-L1 = Sol 盲検独立反証が Opus と同一診断**(Sol turn 終了 14:01 < sat_l1_v1 commit ⟹ 未読での一致)。blocker 類型に PREDICTION_TO_MEASUREMENT_CONTAMINATION 登録・判定 receipt 機械生成(P88-R4-2)を mine v1.5 要件化。正本 = sol/裁定_239_便88検収.md。

## 2026-07-30 実現探索第二波(cent2/wall1)と文献ゲート配達 3(裁定 240 追記 2)
- **cent2(n=12)= 悉皆陰性**: search/certs/cent2_existence_20260730.json(probe = search/probe/wac_v1/cent2_existence_search.g・a₁ 類 62,370 全数・4.8 秒)。b₁ 型適合 100 対の生成群は全て位数 3840 — S₁₂ 到達ゼロ(TRI 外の第三障害・正体同定は数学者へ)。
- **wall1(n=27)= 乱択保留**: search/certs/wall1_existence_20260730.json(smoke 300,000 試行・hit 0・理論 hit 率 ~1.4×10⁻¹⁰ を cert に申告)。plan は mine/jobs/hold/ へ(徒労 CI を発射しない)。方針転換 = Frobenius 指標和で走査前計数 → Hall/Möbius で生成差引 → 構成的分解。
- 文献ゲート配達 3(きっかけ = ①要請駆動 sat_l1_v1 §9.2 + ②司令塔発 障害解明): 覚書 docs/notes/litgate_rigidity_hurwitz_v1.md + 原文 3 本(papers/delivered/ — arxiv_math_0609118 = 4e457fe5…・arxiv_math_0304376 = 5b05a2b6…・arxiv_1012.5297 = d7801c49… 全ハッシュは本日先行欄)+ 書誌 3 件(Serre・Malle–Matzat・Hall 1936 = DOI 10.1093/qmath/os-7.1.134 一次確認済)。配達先 = Opus(SendMessage)・Sol(便 89 同梱)。scout 報告書は金庫 → 配達完了後に docs/scout/ へ移設予定。

## 2026-07-31 壁(P4)到達 candidate(裁定 241)+ mine v1.5 完成
- **P-WALL-2**(n=24・ℓ=19・w₀=(19,1⁵)・ε=0): 存在を紙で事前確定(不動点なし ⟹ 推移・素数 19>n/2 ⟹ 原始 ⟹ Jordan・指標係数 2280)・witness 実物対(2-opt 山登り)・窓 assert 全通過・**SURV 構成 f_z 2280 個全通過 ⟹ Ξ(ker χ̃) ⊇ C₁₉×S₅(非可解)**・定理 CENT-0(p=s=0 ⟹ CENT 等号定理化)で ker=C(w₀) 確定 ⟹ **GTSh 非可解の初実例 candidate**(Opus 発・Sol 監査待ち・正本 = docs/notes/sat_l1_v1.md §10.6+速達)。W-CENT-B(n=18・9 倍判別)も同梱・162/162。3840 障害の正体 = 2⁵:S₅ 非原始。計数機構(Frobenius+分割 Möbius)11 窓較正・悉皆値厳密再現 — 実現探索は乱択全廃・数秒化。
- mine v1.5 完成(merge e451cee): 判定 receipt 機構(prediction/cert 別入力・恒等式 assert・manifest 束縛必須・fail-closed 負例確認)— **r=4 C/B receipt が Sol F88-2.2 独立判定表と全項一致**(機構の独立再検証)。r=4 driver 欄 12 を 4 段分解・欄 30 改名(P88-R4-1/2 消込)・driver 新 sha = 01783f77fc30991c69be8da65b4419146c8f46b6d960024f708f540ef1b3c81e。

## 2026-07-31 cake_lpr(形式検証済み checker)による遡及三段目検査 = 全 VERIFIED
- workflow = .github/workflows/lrat-recheck.yml(cake_lpr commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa・binary sha256 1822ca1e5d0f925e8f3b73047941a8261bee65eef6ccb0e33bb49f92821a09ca)。CI run 30557427326。
- **n21_transitive(裁定 206 定理 3.1 の n=21 非存在)= s VERIFIED UNSAT**・**n21_m10_depth19(mutant)= s VERIFIED UNSAT**。両者とも CNF/proof の sha256 が収蔵 SHA256SUMS.txt と一致(manifest 束縛検査つき)。
- **fail-closed 負例 = CORRECTLY_REJECTED**(破壊 LRAT は検証されない)。
- ⟹ n=21 非存在の証明経路は **drat-trim × 自前 lrat_check.py × cake_lpr(CakeML で形式検証されたバイナリ)の三系統**で一致。語法は cross-checked(「verified」は Lean 予約のまま)。
- 初回 run 30557129007 は upstream 同梱 sha256 の basis_ffi.c 行 stale(実体 8e30d84f…≠同梱 3fbd8f31…)で fail-closed 停止 → 検証核 cake_lpr.S は一致を確認の上、当該 1 行のみ当方観測値で pin して再走(修理 commit あり)。gate は fail-closed のまま。

## 2026-07-31 標的 T5 決着 — 導来長ちょうど 3 の核の初実例(裁定 242)
- cert: search/certs/dl3_cert_20260731.json = aa75c5d9619b18f4ccdcaa71a8dd8f33cc2f75643f31d03e3d3eaa4d935a16ee(probe = search/probe/wac_v1/dl3_search.g・ローカル完走)。
- 窓 T5-dl3(n=21・ℓ=17・w₀=(17,1⁴)・種数 0・⟨a₁,b₁⟩=A₂₁): 窓 assert 全通過・**C_{S₂₁}(w₀)=408=C₁₇×S₄・導来長 3**・**SURV 408/408 通過**(落ち 0)・Ξ 像 = C(w₀)。CENT-0 適用域(p=s=0)につき等号は定理。
- ⟹ **帯 2 の名指し空白「dl ちょうど 3 の核の実例ゼロ」を消込**(内部標的)。dl 2 ⟷ dl 3(本件)⟷ 非可解(P-WALL-2)が同一パラメータ族の隣接値であることを実物 2 個で確認 = spectrum 予想(ideas_014 H4)の支持データ。
- 効率: ℓ=7,11,13 は Ree 予算+符号パリティで feasible k 空 → 探索起動前に紙で棄却・ℓ=17 初回ハント即ヒット(「計数してから構成」3 例目)。ℓ=19,23 は未走査(正直記載)。
- 残務: cert の f_orientation 欄(hexagon 向き規約)未適用 — wall2/centb と一括で追加。

## 2026-07-31 実験 B(拡大類の初データ)+ f_orientation 欄の適用(裁定 243 工程 2)
- search/certs/extension_class_20260731.json = c5b5238b2587a54992a52266e412857ebc917c2959af8b263c37ffd101d365a8: **r=4 C 枝(800/200/4)= split=true**(既存欄 28_compl_classes_all=5 から抽出・GAP 再走なし)・**B 枝(2000/500/4)= split=true**(同 4)。T5-dl3 / W-CENT-B は **UNKNOWN**(probe が m=0 層のみで全 charming 層の shadow list 未構成 — 一般化は別実装・silent cap でなく明示)。⟹ 構造論の「最後の未知」= 拡大類の最初の実測点は **両枝とも分裂**。
- f_orientation 欄を 3 cert に追加(数値不変・欄追加のみ): wall2 = bdbd750d75e21ae8f9e6b657ed57d4db1568c2671994b1d2bd306e10ff2cc2e2・centb = 794d87253616b79982b0a2df624fc095a17a6fcf3f54464cc68764614c8bb930・dl3 = 8928e063c7fa03b6ff5211b1bfa73436f06bd3b7f0ededfbfd3d43b7ef32787e。**3 本とも値は `mathematician_handwritten`(右共役)**(コード実読で判定 — dl3 のコメント「judge 規約」は式が wall2 と同一という意味で AbstractProd 左共役ではない、と注記)。向き決着により値は向きに依らず不変。

## 2026-07-31 文献ゲート配達 4(P1 線・正種数 Belyi と種数 2 の C₃-被覆)
- きっかけ = ①要請駆動: u_meas_m3_design_v1 §5【文献要請 1・3】(裁定 244 で発注承認)。覚書 = docs/notes/litgate_positive_genus_belyi_v1.md。
- 配達 10 本(papers/delivered/・sha256 は覚書の表が正本): 軸 A = arxiv_1311.2529(Sijsling–Voight・手続きの正本)・arxiv_1311.2081(KMSV・数値経路 = M7 候補)・arxiv_1212.3803・arxiv_1908.10459(single-cycle Belyi = 我々の (9) 成分に最近)/ 軸 B = arxiv_2102.04319・arxiv_2411.17930・arxiv_math_0508174・arxiv_2306.02147(Sophie Germain 型巡回被覆 = 型が最も近い)・arxiv_2503.23041・arxiv_2410.14454(有理捻れ = 篩の実装源)。
- **検疫**: A3 = arxiv_1805.07751(A Database of Belyi Maps)は**配達せず金庫 quarantine へ隔離**(裁定 244 の【文献要請 2】保留対象 = 測定前に引くと汚染)。M3 で候補を自前構成後、M7 の位置で司令塔が解禁。
- 一工夫 = ①我々の設定(次数 9・種数 2・PSL(2,8)・剛・div_∞=9P̄)への落とし込み ②**型 C 警戒**(B1/B5 のフル ℤ₃×ℤ₃ と我々の単一 C₃-被覆は別物 — 束ねない)③要請 1(b)(剛性下の 0 次元化)に直接答える文献は未特定 = 自前規約を凍結する方針を提案。
- scout 報告書 2 本(rigidity_hurwitz・positive_genus_belyi)を金庫 → docs/scout/ へ移設(配達完了に伴う開示)。

## 2026-07-31 窓 B(S4 = PSL(2,8))の SD-c 証明書 — 便 86 NOTE 3 の解消(裁定 244 工程 1)
- cert: search/certs/sdc_twist_S4_window_20260731.json = 24e95d42abb443e85b6ff2cd246599f9ade3382a69cf771cad9a781199892a82(probe = search/probe/wac_v1/sdc_twist_s4_window.g・GF(8) 上のモデルを judge/week3 系を Read せず独立実装)。
- 測定(全 26 assert PASS・all_pass=true): |Bq|=3024=6·504・**|P|=504=PSL(2,8)**・ord_x=ord_y=9・**c_in_N=true(Δ² の実置換計算で実測 — 構築の仮定でない)**・N_ord=9・C_{S₉}(X)=9・N_{S₉}(⟨X⟩)=54=[54,6]・scan_mode=exhaustive_over_P(504 悉皆)・F0_size=9・settled_fail=0・j_values=[0,1,8,4,5,3,2,7,6](全単射)・phi_F0_bijective_onto_inn_X=true。
- **A₁₀ 窓との異同**: C(X)=9・N=54・[54,6]・F0_size=9 は**数値一致**(surj_s4_v2 が指摘した偶然)。異なるのは |Bq|(3024 vs 10886400)・|P|(504 vs 1814400)・ambient(S₉ vs S₁₀)・j 値の並び。⟹ **窓の同定は位数と ambient で行う**(数値一致欄では不可)を教訓として記帳。
- **工程事故と恒久対策**: 初版 cert が JSON parse 不能(GAP の出力整形が `\`+改行を挿入)。原因 = **SizeScreen の列幅上限 4096**(実測確認)を窓 B の長い置換文字列が超過。A₁₀ 窓で効いた SizeScreen 単独では不足。修理 = OutputTextFile + SetPrintFormattingStatus(f,false) で整形自体を無効化。**以後 cert 生成の必須手順に「生成後の json.load 検証」を追加**(実装者へ指示済)。測定ロジックは無関係につき値は不変。

## 2026-07-31 実験 A(裁定 243 工程 1)— 予想 PASSPORT 支持・剛性は等号の必要条件でない・SPIN 否定
- 成果物: docs/notes/passport_experiment_a_v1.md(予言凍結 → 測定 → 判定)・cert = search/certs/expA_passport_20260731.json / expA_passport_batch_20260731.json(f_orientation="judge")・probe = search/probe/wac_v1/expA_{scan,verify,measure,batch,spin}.g + expA_treecheck.py・対話帳 T-18。
- **最小 passport = n=10**(n≤9 は N_gen≤1 と厳密排除)。n=10 に N_gen≥2 が 5 本((9,1)=6・(10)=5・(8,2)=3・(7,3)=3・(6,4)=3)⟹ **剛性の破れは例外でなく常態**。
- **予想 PASSPORT = 支持**: n=10,11 の 7 passport・**24 窓**(21 窓が N_gen≥2 側)で |GTSh|・IdGroup・ker IdGroup・|Ξ(ker)|・N_ord・charming が passport ごとに完全一致。**CENT も 24/24 成立 ⟹ 剛性は等号の必要条件でない**(Sol F88-2.6「E-構造の追加情報」への名指し回答 = 追加情報の正体は w の巡回型)。
- **定理 SAT-RIG (a)(c)(d) の訂正**: n=10・(9,1) で hexagon+全射 54/54 に対し shadow は 9/54(基点軌道のみ)・N_shadow=1 ≠ N_gen=6。犯人は settled 節(T が自己準同型 ⟺ f∈C(ȳ)C(x̄))。**同日 T3 稿が別経路で同一訂正に到達 — 二重発見につき「初」はどちらにも帰属させない**(数学者自身の申告)。
- **N 値の二系統一致(cross-checked)**: Frobenius 指標和+集合分割 Möbius(実験 A)と平面木の Catalan 計数(T3)が (13,1³)=2・(17,1³)=10・(19,1⁵)=1 で完全一致 — **指標理論と組合せ論という別道具**による一致。
- **予想 SPIN(H2)= 否定的**: 2·A₁₀ で対合類 2⁴1² の原像が割れず、持ち上げ不変量が well-defined ですらない。
- **新規性の自己申告**: 梯子の sibling 窓 o2–o6 が本稿の Nielsen 軌道 #2–#6 と permutation 一致 ⟹ **2026-07-30 の梯子キャンペーンが既に「同 passport・別 Nielsen 類の 6 窓が同じ GTSh」を取得していた**。新規部分は 4 点のみ(完全代表系の証明つき同定・CENT-0 外への拡張・n≤9 の厳密排除・F88-2.6 への回答)。

## 2026-07-31 CI 大規模走査 3 本(12 shard)の判定 — 裁定 247
- CI run 30561849635(mine-dispatch・12 shard 全 verdict=done・宇宙は裁定 245 で事前確定)。収蔵 = search/certs/scans/(12 cert・全て JSON 妥当性検証済)。
- **壁族: 非可解核 2 件**(39 レコード中)— P-WALL-2(n=24・ℓ=19・t=5・C₁₉×S₅・2280)と **新規 n=28・ℓ=23・t=5・C₂₃×S₅(2760)**(a₁ = k=14 互換・b₁ = j=9 三巡回・⟨a₁,b₁⟩=A₂₈・braid 成立)。⟹ **P4 は「1 個」から「族」へ**。
- **spectrum: 予想 SPEC の反証ゼロ**(tau 843・C 測定 49)。非可解は上記 2 件のみでいずれも t=5(長さ 1 の巡回 5 本)= 予言どおり。多重度 ≤4 は全て可解。**語法は「(ℓ,1^t)/(ℓ^r,1^t) 型の表+一般型の標本(cap 20/n・truncated 明記)」に限定**(裁定 245)。
- **梯子族: 定理 LAD が 7 系列全てで成立**(ℓ=11..25・上限超え HIT なし)。ただし実際の最大 t は理論上限より小さく、**実効障害が別にある**(新しい問い = t_max(ℓ) の閉形)。**SURV 全数一致 91/91**(HIT 28 件)。
- **司令塔の一次読み取りミスの申告**: cycle_type 欄(GAP スパース表記)を誤読し「SPEC 違反 2 件」と一度読んだ。実物レコードを開いて t=5 を確認し撤回。教訓 = **machine-piped は「機械値を読む」だけでなく「機械値の書式を確かめる」まで**。

## 2026-07-31 文献ゲート配達 5(pentagon = 副線の定義正本・P6 井原への橋)
- きっかけ = ②司令塔発(研究者裁可・井原予想 P6 への直撃路)。遠征 = paper-hunter(金庫 hunt/ 出力 → 配達判断 → docs/scout/ 移設)。覚書 = docs/notes/litgate_pentagon_v1.md。
- 配達: **papers/delivered/arxiv_2008.00066.pdf = c44eba890f83c1ac84a44a5b52fd5c6849250b242331d7eaaff9dd983167fb33**(Dolgushev–Le–Lorenz "What are GT-shadows?"・AGT 24 (2024) 2721–2777・**長らく未入手だった副線の定義正本**)・papers/delivered/arxiv_2106.06645.pdf = be6afb208b09d79716119fcb479bf74175a1c0ade1fa47d6c9727b01aa2d8f52・**papers/delivered/PackageGT.zip = c3124483cb1464b9010c091011370db091a76561a2af923a38efb6900f645f95**(Dolgushev の Python 実装・旧 URL は 308 で死亡・2106.06645 の参考文献 [7] 経由で取得)。Harbater–Schneps 2000 は**未達**(正直申告)。
- **成果の核**: pentagon の明示形(C1 式 (2.20))+ **余面 5 本が PB₃ 生成元上の値だけで決まる**((A.18))⟹ **PB₄/N を 6 置換で持ち、f を語として評価し 5 本の積を比較するだけ = GAP で書ける**(コホモロジー不要)。実装 `PaB.py: def penta()` が同一判定を既に実装・`NotUsed.py` に第二実装(cross-check 可)。
- 実データ(C1 §4): N⁽¹⁹⁾(N_ord=6)= pentagon 満たす f が 216・うち hexagon も 36。N⁽³⁴⁾(N_ord=9)= pentagon 4096・うち hexagon も 243・GT(N⁽³⁴⁾) 位数 486=(ℤ₂×ℤ₃)⋉(ℤ₉×ℤ₉)。
- **同名別物ゲートの対応表を原文で確定**: 本来系 ĜT = B₄/PaB(≤4)・hexagon×2+pentagon・窓は **NFI_{PB₄}(B₄)** / gentle 系 ĜT_gen(工房)= B₃・hexagon のみ・窓は **NFI_{PB₃}(B₃)** / coarse 系 ĜT₀ = pentagon を落としたもの(Guillot が研究)。**窓の圏そのものが違う** ⟹ 橋の第一段は「B₃ 窓から B₄ 窓をどう作るか」であり、ここを飛ばす翻訳は罠。
- 予想外の収穫: **Furusho property(pentagon ⟹ hexagon)の profinite 版は一般には偽**(C1 §4.3・35 例で機械判定・強 11/弱 13)。⟹ hexagon を pentagon で代替はできないが「どの窓で Furusho 性が成り立つか」が新しい問い。

## 2026-07-31 PENT-π 第一実測(裁定 249・司令塔自身が実装)— pentagon は刈る・較正ゲート発動
- 成果物: search/probe/wac_v1/pent_pi_a5.g ほか 4 probe・cert = search/certs/pent_pi_a5_20260731.json(json.load 検証済)。
- **確定測定**: A₅ 窓の π-lift(σ₃↦σ₁・K_π ∈ NFI_{PB₄}(B₄) 正真)で **pentagon (2.20) は A₅ の 60 元中 8 元のみ通す**(rev 辞書・機構は N⁽³⁴⁾ 4096/254016 再現で較正済・**類不変性 60 元×3 変形で違反 0 を実証**)。⟹ 発案係の破綻点 1(潰れ)否定 = **第三の歯は本物**。
- **P-PENT-1 発動 = FAIL で停止**(予言の指示どおり): v4 の「GT(N_A) 20 元全て arithmetical」+算術鎖 ⟹ 20/20 が必要だが、辞書×語順×反転の全 8 組合せで 10/20・live 8 元 < 必要 f ≥10 で構造的に不可能。**未較正部分を「gentle(2401)↔B₄(2008) の (m,f) 径数対応(m 依存 recoding の署名 = per-m [5,0,0,5])」1 箇所に同定** — knob 合わせ禁止・紙上導出を数学者へ委嘱。
- 観察(candidate): readA ラベルで live ⟺ u∈{±1}(平方類)・live 集合は m=0 hexagon 解 5 個を全含。

## 2026-07-31 recoding 恒等の決着と v4 再検分の開始(裁定 250)
- 数学者(docs/notes/pent_recoding_v1.md・紙導出): **gentle(2401)↔B₄(2008) の径数対応は恒等**(hexagon 対の原文突合・c 中心性経由で両辺同一)⟹ PENT-π 実測 10/20 は確定・knob は不在。read A を部分群規準で採択(live = χ̃⁻¹({±1}) 指数 2 部分群・read B は 4∤10 で棄却)。
- 司令塔の lift census(_pent_pi_liftcensus.g): B₄ 関係式を満たす S3 ∈ E は **S1 ただ一つ ⟹ π-lift は最小レベルで唯一(canonical)** — live 8 は lift 選択の artifact でない。
- **含意(candidate・主張未確定)**: live = 「√5 を固定する側」。円分全射性との衝突により **week4 v4 L521「20 全 arithmetical」はこのままでは保持できない** — 最有力仮説 = N_A の dessin は G_{ℚ(√5)}-安定のみ・算術像 = live の 10 個。数学者へ v4 飽和計算の再検分を委嘱(moduli 体の明示計算)・便 90 の最優先積荷へ昇格。pentagon 橋の初仕事が工房自身の旗艦主張の監査になる可能性。

## 2026-07-31 三つ巴の解消(裁定 251)— v4 無罪・pentagon 実測を装置疑いへ降格
- 数学者(docs/notes/a5_arithmetic_recheck_v1.md): **v4 は正しい**(L は rigidification 体・moduli 体は (I1) より ℚ・「20 全 arithmetical」は ℚ 上の主張として正・erratum 不要)。**G_{ℚ(√5)} 仮説は数学者が自己撤回**(R-PENT-1・Chebotarev が逃げ道を塞ぐ)。司令塔の「u≡3 = 非平方類」は **Kummer 助変数と円分座標の型錯誤**(記録)。
- 決定的論証(v4/W3-8 不使用): G_ℚ の pentagon は profinite 恒等式 ⟹ 全 K で成立・χ̃∘Ih は Chebotarev で全射 ⟹ **u∈{2,3} の pentagon-live shadow は存在必須**。実測 0 ⟹ **装置が偽**。⟹ **裁定 249/250 の census 8/60 を「確定測定」から「装置バグ疑い・再較正待ち」へ降格**(本追記が正・過去エントリは非改変)。
- 欠陥候補(優先順): ①f↔f⁻¹ 向き ②K_π 定義(消込済) ③(A.3) 全数検査 ④θ 落ち(φ₂₃₄↝θ — pentagon が hexagon 再言の危険・紙で兆候) ⑤**π-lift 構成段が較正外**(N34 較正は機構のみ)。教訓 = 較正主張には範囲を明記・符合の誘惑に Chebotarev 級の重い定理での即検査。
- 格の教訓(研究者の問いへの回答として記録): v4 = two-mathematician audit PASS(candidate より二段上)vs 攻撃 = candidate — **監査済みが生き残り candidate が倒れた = 梯子の順序どおりの決着**。
