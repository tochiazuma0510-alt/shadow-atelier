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

## 2026-07-18 — 用語改定(ユーザー指示)

- **「検証(verified)」は Lean(機械証明)に予約**。node/python の独立再計算は「**照合器(cross-checker)**」と呼び、二系統一致の状態は「**cross-checked(照合済み)**」。上のエントリの「検証器/検証 = node」の表記はこの改定で「照合器/照合 = node」と読み替える。ディレクトリ `verifier/` → `crosscheck/` に改名。台帳語彙は CLAIMS.md 冒頭が正。
