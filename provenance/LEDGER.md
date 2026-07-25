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
