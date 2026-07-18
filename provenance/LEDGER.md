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
