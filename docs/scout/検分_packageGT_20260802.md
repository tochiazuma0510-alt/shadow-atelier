# 検分書: Dolgushev PackageGT の provenance 検分(IHNEC-L2 第一段)

- 日付: 2026-08-02
- 実施: implementer(司令塔指示。裁定412「再取得でなく既存 archive の検分から」に基づく)
- 対象: `thirdparty/packageGT/PackageGT.zip`(現物・金庫外はこの2ファイルのみ)+ `thirdparty/packageGT/PackageGT_README.pdf`
- 既存使用実績: `search/probe/wac_v1/gt_thirdparty_bootstrap.py`(Windows AUX 罠のブートストラップ)・`search/probe/wac_v1/pent_thirdparty_gt_run.py`(第三実装判別本体)・`search/certs/pent_thirdparty_gt_20260731.json`(裁定275 証明書)が既に存在していた。**本検分は「新規実装」ではなく既存資産の監査+再現確認**である。

## 1. zip の内容目録

`thirdparty/packageGT/PackageGT.zip`(sha256 = `c3124483cb1464b9010c091011370db091a76561a2af923a38efb6900f645f95`、既存収蔵ハッシュと一致)を新設作業場所 `thirdparty/packageGT/extracted/`(`.gitignore` の `thirdparty/` 配下でリポジトリには入らない)へ展開。34 エントリ(うち `__MACOSX/` リソースフォーク3件+ディレクトリエントリ1件を除く実ファイル25本+`.DS_Store`)。`unzip -l` の生出力:

```
Archive:  thirdparty/packageGT/PackageGT.zip
        0  2022-03-17 02:21   PackageGT/
     1715  2021-07-28 03:20   PackageGT/Leila_PB4
      158  2021-07-28 03:20   PackageGT/dde18E29
    18028  2022-03-08 04:20   PackageGT/Aux.py
      142  2022-02-16 06:56   PackageGT/dde14E15
    29478  2021-07-28 03:20   PackageGT/wm_list32_all
     6148  2022-03-17 02:22   PackageGT/.DS_Store
      120  2022-03-17 02:22   __MACOSX/PackageGT/._.DS_Store
     1612  2021-07-28 03:20   PackageGT/wm_list_Leila
      170  2022-02-16 06:56   PackageGT/dde21E15
    19648  2022-02-23 22:56   PackageGT/NotUsed.py
    20426  2021-07-28 03:20   PackageGT/wm_list31_all
     2459  2021-07-28 03:20   PackageGT/E_dde6genus0
      102  2022-02-09 06:36   PackageGT/dde4Many
     3768  2021-07-28 03:20   PackageGT/G_Mighty_Dandy
     9443  2021-07-28 03:20   PackageGT/subGrPB4_org35
    64144  2022-03-08 04:21   PackageGT/PaB.py
      166  2022-02-16 06:56   PackageGT/dde20E8_many
      114  2021-07-28 03:20   PackageGT/dde7E29
      114  2022-02-08 00:54   PackageGT/dde7E28
      176  2022-02-08 00:54   __MACOSX/PackageGT/._dde7E28
     2075  2021-07-28 03:20   PackageGT/E_dde5genus0
      106  2021-07-28 03:20   PackageGT/dde5genus0
   153294  2022-03-17 02:18   PackageGT/README.tex
      333  2022-03-17 02:18   __MACOSX/PackageGT/._README.tex
    75991  2021-07-28 03:20   PackageGT/wm_list_charm35
      146  2021-07-28 03:20   PackageGT/dde15E29
      118  2021-07-28 03:20   PackageGT/dde8E5E19
  6794373  2021-07-28 03:20   PackageGT/Mighty_Dandy_wm_list
      110  2021-07-28 03:20   PackageGT/dde6genus0
   589231  2022-03-17 02:20   PackageGT/README.pdf
      233  2022-03-17 02:20   __MACOSX/PackageGT/._README.pdf
   202872  2021-07-28 03:20   PackageGT/wm_list_all31
      134  2022-02-10 01:01   PackageGT/dde12wheel
```

### 構成の分類

- **コード本体**: `PaB.py`(64144 B、mtime 2022-03-08、主要クラス `Equiv`/`GT_sh`/`Dessin`、生成器 `gener_GT_sh`/`gener_GT_charm`/`gener_GT_pr`/`gener_GT_penta`)、`Aux.py`(18028 B、補助関数群 `cart_pr`/`relB4`/`restr_PB4`/`generB4`/`generB4_A` 等)、`NotUsed.py`(19648 B、README では言及薄いが `PaB.py` の名前空間に依存する補助スクリプト)。
- **事前計算データ**: `subGrPB4_org35`(NFIPB4(B4) の35元、README §4.1.1「How we obtained 35 selected elements」に対応)、`wm_list_charm35`/`wm_list_all31`/`wm_list31_all`/`wm_list32_all`/`wm_list_Leila`/`Mighty_Dandy_wm_list`(6.79 MB、N(34)="Mighty Dandy" の charming shadow 全リスト)、`G_Mighty_Dandy`、`Leila_PB4`。
- **child's drawing 例**: `dde4Many`・`dde5genus0`(+`E_dde5genus0`)・`dde6genus0`(+`E_dde6genus0`)・`dde7E28`・`dde7E29`・`dde8E5E19`・`dde12wheel`・`dde14E15`・`dde15E29`・`dde18E29`・`dde20E8_many`・`dde21E15`。
- **文書**: `README.pdf`(589231 B)・`README.tex`(153294 B)。

### 展開ファイルの sha256(実ファイル25本、`.DS_Store` 除く)

新設展開場所 `thirdparty/packageGT/extracted/PackageGT/` での機械出力(`sha256sum` 生値):

```
62d7f24c502209994663cb79e2f2469c5ab9ac982d1312604722445437fd7144 *./Aux.py
545b02d219f5cd4f7bf415899983e4202a556a905647c3ba2cc06495cc1c6b59 *./E_dde5genus0
ee36f0d9c69c8ae52bbc36c2319ac36ad9cab59cc8728b95a37bf33fd70b6e91 *./E_dde6genus0
b9e2c33056ea37542b77abba94ebe112ead9e1b709fb4113988cdcd03990e9cf *./G_Mighty_Dandy
eb26cedf2258070341b1db7c1fbe8abc002c9e7d4a965024b49f9489b92db9fe *./Leila_PB4
7c5fb01cd3c337831f0467f6f11bdc86e095d3bf2215a5daf05bc711936ae562 *./Mighty_Dandy_wm_list
7f02a1eff47883fbc729f06862c599cb5452a24c86762b7c1b903a925412ff56 *./NotUsed.py
e54c08d3437d0706b4639d7db31f7177c1c82de9c2f820fa7b194fa1c4e378f2 *./PaB.py
90545f5ea820b41c8bb16c5719c2540d39207f5247a4649fc4d784f1612468f1 *./README.pdf
09a4df5c4e473f3195b35430749636b84321dfb27b9f473f9695011b0eca490c *./README.tex
bc8cccc432965cfee47f9fa452c202b172ca6eed7629613c1b71021531c78247 *./dde12wheel
7c837c7138717ac3bebd5856db0537055c87c2e50c4710bce6a4899032aac824 *./dde14E15
fbf51b6e718ac99f80ea0991da7959ebb3e373a377689447c53544a2085655c4 *./dde15E29
82fbf7fb83cdf670fcbce8cb09d68c7b2f46970229533ac037475976ceff44fd *./dde18E29
d9f01be1fc9932cb2846cf1a8ca6caaa6da79a632b77ec803e29e7da486f0efc *./dde20E8_many
afc3dbfc53781b976587506757a67d833a7f7fb75c449917eb483d7dce13943c *./dde21E15
d5bed1e735179c7b3fc0f37e27f253478255fd6b9bbd5d1286766f83dd1e3a67 *./dde4Many
5000981fd8ba9f05c903c59c38535cfeea01a77ea63645de380811046ec347b4 *./dde5genus0
dc9dd8a4b8ac1ccd05617701835d1c33dcd49623b689b26c24e7a860bb69bc8b *./dde6genus0
0b2655da88681b8be05e89683b64296e5096218801a7b6e7de460e66d5ae3537 *./dde7E28
06b76bb0882c42eb3f98d3b83402a25d9a4a0ae8a20fcfce3fd49576f1e4556a *./dde7E29
9533edadc9ef4188da2e22ae1577efe0b4c4d76c0c5dab7cc6b74a5ff0e04634 *./dde8E5E19
98886607af246bc0262f9b10d3cb5a98564d3b2922dd169eddf73045e9d2dd15 *./subGrPB4_org35
96f1c1c93a9fd72c1479bebfb62ec329fd2fe915dbbd66e782f223b5147954ce *./wm_list31_all
25f835a371f23023661190914cec71058d11bd06b1b1a2b01c369759632c7e83 *./wm_list32_all
e1f7841964231c1bf09235015e3baf605dff7654a53ae8894fd0deadd3edf828 *./wm_list_Leila
cb7699708f63f6c70b76cc81cd4628d3fa15efcaa7a6917d5c87ef5088561e5a *./wm_list_all31
9da54386f03c0c74d1d7a7ea12abf5bcb5864599504cd1522a7b773b29a3bd94 *./wm_list_charm35
```

**照合結果**: `PaB.py`・`NotUsed.py`・`Aux.py`・`subGrPB4_org35`・`wm_list_charm35`・`wm_list_all31` の6件は既存証明書 `search/certs/pent_thirdparty_gt_20260731.json` の `file_hashes` と全一致。`README.pdf` は `thirdparty/packageGT/PackageGT_README.pdf` の収蔵ハッシュ(`90545f5e…`)とも一致。さらに `diff` で `search/thirdparty/PackageGT/`(2026-07-31 裁定275 で使われた既存展開先)と本検分の新規展開先 `thirdparty/packageGT/extracted/PackageGT/` を突合した結果、差分は `AuxSafe.py`(ブートストラップ専用の複製ファイルで zip には含まれない)のみ — **zip 本体・2026-07-18 収蔵物・2026-07-31 使用物の3者が完全に同一物であることを確認**。

## 2. README の要点(pdftotext 抽出、`scratchpad/packageGT_provenance/README_pdftotext_20260802.txt`)

- タイトル: "Documentation for the package GT"、著者 V. A. Dolgushev(Temple University, Department of Mathematics, vald@temple.edu)。
- Contributors(§謝辞): Chelsea Zackey, Aidan Lorenz, Khanh Le, V.A.D. — **正式版数の明記なし**(pip パッケージではなくスクリプト集。バージョンの代理指標は mtime: `PaB.py` 2022-03-08、`README.pdf`/`.tex` 2022-03-17〜18)。
- 冒頭Abstract: 「GT-shadows は GTSh というグルーポイドを成し child's drawing に作用する」— **pentagon+hexagon の両方を扱う本来系**(§1.1「The poset NFIPB4(B4) and the groupoid of GT-shadows」)。
- §7 Testing: 著者自身の間接テスト方式が列挙されている(`isNormB4`・`test_cyclotomic`・`test_relPB4`・`test_generWF2`/`test_generWComm`・`test_conj_braid_rel`・`test_dessin`・compose の結合律/単位律のランダムサンプリング検定)— 著者側の内部較正手続きであり、本検分はこれとは独立(照合器分離を維持)。
- 依存: `sympy.combinatorics`(`Permutation`・`PermutationGroup`・`SymmetricGroup`・`AlternatingGroup`・`DihedralGroup`・`CyclicGroup`)+ 標準ライブラリ(`itertools`・`math`・`pickle`・`random`・`operator`)のみ。README 中に Python バージョン要求の明記は見当たらず(2021-2022年当時の記述で、暗黙に Python 3 系・0-indexed 前提〈`Just as C, Python starts counting at 0`〉)。

## 3. 実行可能性(python 3.13 環境)

- 環境: `Python 3.13.14`(`C:\Users\81905\AppData\Local\Programs\Python\Python313\python.exe`)、`sympy 1.14.0`。
- `Aux.py` は Windows 予約デバイス名 `AUX` に抵触し native Windows Python では**いかなるファイル名でも import 不能**(既知の技術的罠、`gt_thirdparty_bootstrap.py` docstring に詳述済み)。回避策は既存ブートストラップ(`AuxSafe.py` という bash 側で複製した同一内容ファイルを `sys.modules["Aux"]` へ直接注入)で、`PaB.py`/`Aux.py` 自体は1バイトも改変していない。
- 上記ブートストラップ経由で `import` は**正常に通ることを再確認**(下記4節の再実行が実質的な実行可能性の証跡)。追加の依存不足なし(sympy 以外はすべて標準ライブラリ)。

## 4. 既知例較正の再現(裁定275 第三実装判別の再実行)

`search/probe/wac_v1/pent_thirdparty_gt_run.py` を無変更のまま、2026-08-02 に再実行(`echo no | python313 pent_thirdparty_gt_run.py`)。生成物 `scratchpad/packageGT_provenance/OUT_pent_thirdparty_gt_full_rerun_20260802.json` と既存証明書 `search/certs/pent_thirdparty_gt_20260731.json` の機械比較(`json` 突合、丸めなし):

```
charming_total MATCH 20 | 20
friendly_pr_total MATCH 100 | 100
gtsh_total MATCH 100 | 100
penta_comm_total MATCH 16 | 16
charming_per_m MATCH {'0': 5, '1': 5, '3': 5, '4': 5} | {'0': 5, '1': 5, '3': 5, '4': 5}
friendly_pr_per_m MATCH {'0': 25, '1': 25, '3': 25, '4': 25} | {'0': 25, '1': 25, '3': 25, '4': 25}
gtsh_per_m MATCH {'0': 25, '1': 25, '3': 25, '4': 25} | {'0': 25, '1': 25, '3': 25, '4': 25}
charming_distinct_words MATCH 10 | 10
window_invariants match: True
window_transfer_checks match: True
calibration N19 match: True 216 216
calibration N34 match: True
file_hashes match: True
```

**再現確認: 全項目一致(fail-closed・差分ゼロ)。** 裁定275 の「K_π 窓で charming = 20・per-m {0,1,3,4}=[5,5,5,5]」は machine-piped で再現された。

## 5. 正典同定(pin)

README §末尾 参考文献より:

- `[4] V. A. Dolgushev, The Action of GT-Shadows on Child's Drawings, https://arxiv.org/abs/2106.06645`
- `[5] V. A. Dolgushev, K.Q. Le and A.A. Lorenz, What are GT-shadows? https://arxiv.org/abs/2008.00066`

README本文は "In this documentation, we will freely use the terminology and notational conventions from [5]" と明記(§1、行420相当)。`PaB.py` は `penta()`(pentagon 関係式・508行目)・`hexa1()`/`hexa2()`(hexagon 関係式・537/557行目)を実装し、生成器 `gener_GT_sh`/`gener_GT_charm`/`gener_GT_pr`/`gener_GT_penta` はいずれも `penta(...)` を必須の起点条件として使う(§4.2「The class GT_sh」対応箇所)。

**pin: PackageGT は arXiv:2008.00066(定義正本)+ arXiv:2106.06645(child's drawing への作用)の**B₄ ベース本来系**(pentagon あり)を実装したもの — CLAUDE.md の「副線」に該当し、2401.06870/2405.11725 の B₃ ベース gentle 系(pentagon なし・主線)とは同名別物(2405 Remark 1.2 と整合)である。**この対応は既に裁定275 の運用でも前提とされていたが、README の一次引用箇所(`arXiv:2008.00066`本文中「terminology and conventions from [5]」の明記)と `penta()` 関数の実在によって本検分で直接裏付けられた。

## 未監査残項

1. `README.tex` と `README.pdf` の内容差分は未確認(pdftotext のみ抽出。数式のズレ等がある可能性はゼロではない)。
2. `Mighty_Dandy_wm_list`(6.79 MB)・`wm_list_all31`・`wm_list32_all` 等の事前計算データファイルの**内容フォーマット**(README §6「Descriptions of storage files」に説明あり)を実際にロードして中身の整合性を検査してはいない(今回はファイル存在+sha256+`PaB.py` の `load_now` 経由の暗黙ロード成功のみ確認)。
3. §7 Testing に列挙された著者自身のテスト群(`test_cyclotomic`・`test_generWF2`・`test_generWComm` 等)を**本検分側で独立に再実行してはいない**(裁定275 の N19 再計算〈216件、既に本検分でも再現一致確認済み〉のみが著者関数の独立再計算に相当)。
4. `dde*`/`E_dde*` の child's drawing 例ファイル群(degree 4〜21 相当)は今回内容未検査(存在・ハッシュ照合のみ)。
5. `NotUsed.py` の用途(README に明記なし、ファイル名からして著者が「使っていない」と位置づけたコードの可能性)は未解明。
6. 正確な python バージョン要求(README に明記なし)は今回 3.13 での動作確認一点のみ。3.7〜3.12 系での動作は未検証(現行環境が3.13のみのため対象外)。

## 収蔵物

- 新設展開先: `thirdparty/packageGT/extracted/PackageGT/`(`.gitignore` の `thirdparty/` によりリポジトリ外挙動・ローカルのみ)。
- README テキスト抽出: `scratchpad/packageGT_provenance/README_pdftotext_20260802.txt`
- 再実行 raw 出力: `scratchpad/packageGT_provenance/OUT_pent_thirdparty_gt_full_rerun_20260802.json`
- 較正スクリプトは**新設なし**: 既存の `search/probe/wac_v1/gt_thirdparty_bootstrap.py`(ブートストラップ)+ `search/probe/wac_v1/pent_thirdparty_gt_run.py`(較正+本番実行)をそのまま再実行して再現確認した。
