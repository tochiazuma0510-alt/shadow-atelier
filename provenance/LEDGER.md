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

## 2026-07-18 — 用語改定(ユーザー指示)

- **「検証(verified)」は Lean(機械証明)に予約**。node/python の独立再計算は「**照合器(cross-checker)**」と呼び、二系統一致の状態は「**cross-checked(照合済み)**」。上のエントリの「検証器/検証 = node」の表記はこの改定で「照合器/照合 = node」と読み替える。ディレクトリ `verifier/` → `crosscheck/` に改名。台帳語彙は CLAIMS.md 冒頭が正。
