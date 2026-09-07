# Task1082 C — v5 正式 inventory 定数の限定結合

F1. Task1082 を全文読み、root の正式全 inventory 票 7022 B / 64e3f8e6a434be335a88c1dee6efa4aae7b3d669faac28e704aefd0f8e3f4753 と二つの canonical raw の全 bytes/SHA を照合した。旧 C5 の immutable snapshot は変更せず、TEMP/shadow-atelier-audit163/task1082-C 以下へ新しい source と全静的材料を保存した。変更は NEXT_BATCH_INVENTORY の None を正式 exact 五 key 辞書へ置き換えた一箇所だけである。数学本文・関数・main・CLI・四群 selftest は不変。

登録は files=11648 / file_bytes=1308094050 / directories=3525、files_sha256=ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5、directories_sha256=f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64。正式 file 配列は1931889 B、directory 配列は200290 Bで、それぞれ上記 SHA と一致した。これは root の今回の全11648file再hash・全3525dir比較に基づく登録であり、暫定票を正式化したとの主張ではない。

F2. 以下の path は task1082-C を基準とする。

| 納品 | bytes | SHA256 |
|---|---:|---|
| search/check_d972_r07_fixed_lambda_cycle_batch_v5.py | 336193 | 47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73 |
| root-review-checker-v5-bound-v1.py（全 bytes 同一） | 336193 | 47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73 |
| baseline-checker-v5-unbound.py | 335937 | c868aa09a6dd6e94510f996080a8e3e0a7fea1563046486960c7b6a4fca55170 |
| checker-inventory-only-full-diff-v1.txt | 397 | 1d38f1042fa47ffe7462bd3662e50f69e262aa7d212743bc98bdfbd18f01f644 |
| checker-inventory-only-raw-change-v1.json | 1441 | 0ab3dd9ce449efa3e025b5e65e09b306cdcfbb837684d3f37c20da344926c985 |
| checker-current-all-raw-regions-v1.json | 131265 | ce6644d0fff78f69c96a5890b182624ce62eec4178f841b84e54ee757ea47e3d |
| checker-old-loader-and-body-retention-v1.json | 30939 | 182ab9848742a51fb352bcff7a91c8bcd5fc92c89a9de3b7ef6cbe43c042d007 |
| public-checker-final-source-and-ranges-v1.json | 310062 | ff3f33a8b1d02df7fdcbab6d61ef3d603e1a2de70fb456147b4c2e537e4d77b8 |
| material-index-v1.json | 4242 | 3b13c242f777aec360f132d0ad4be71097f0ea03b2c52008885b1eac69c16f50 |

新 source は ASCII、LF4646、CR0、BOMなし、末尾LF、旧版から256 B / 6 LFの追加。全変更 JSON を保存後に再読し、その唯一の old_raw/new_raw の両方向置換が各 source の全 bytes に完全一致することを比較した。逆置換 SHA は元 c868aa09…、順置換 SHA は新47cf2596…である。全 EOF の column0 def/class raw 区切りは140区間のままで、相違は PREAMBLE 一区間だけ。Python parser や AST は用いていない。

F3. 旧4 loader と C4→C5 の20保持 body は全 bytes/SHA を維持する。新旧の同一 raw を比較して、offset は各256 B、LF位置は各6行だけ進むことを保存した。class 内の anchor_metadata は column0 区切りから推測せず、既登録の2463 B実範囲を直接取り直して同SHAへ結んだ。

| loader | 新 C5 offset | bytes | SHA256 |
|---|---:|---:|---|
| anchor_metadata | 42879 | 2463 | ab20e3cbf8f0b0d72a4ffdff93ea09ca71e9b50eec7b5ce3ac9a7aa22d70656e |
| base_pivot_metadata | 50507 | 2403 | 5be807b3382c0c938dc16ac5af4906b85f507e8f16b6844004aceebccc6ec1d7 |
| ThinAnchor | 52910 | 3516 | f4fe4ef5620b7a4e5256d70e15a1c3b4139827d6b6a717ec3e23a02e6ad6e1a9 |
| restore_physical_anchor | 57008 | 14011 | 3178867cb0c359149db73088e11bdee4b19b2e1c0acb9914ee4860044c72a231 |

公開 ranges 票は source 全 pin、全140 current raw 範囲、C4→C5 transition、旧4 loader、20 body の新範囲を含む metadata のみであり、私的 source body を含まない。1079作者/1081監査と root に同 pin を通知した。material-index は自分と本返信を除く12 fileを記録し、正式登録票・正式 canonical二raw・基点・新source二copy・全差分・範囲・保持票・静的編集記録を残す。

F4. 実施した処理は PowerShell/.NET の raw 編集・全file SHA・JSON metadata・静的 byte 範囲比較だけ。途中の静的材料作成では method 範囲を column0 表から引こうとしたため保持票作成が停止し、上記の既登録実範囲による比較へ修正した。研究 source に追加差分はない。P私的 source/票は読まず、source/Python/AST/compile/import/GAP/数学/helper受領実行/Git/GHA/network/credential は全0、新 selftest は全て未実行である。

旧1074 full typed metadata受領は exit1 のまま再実行が必要で、本票はそれを PASS にしない。旧v3空36の root 修復票と正式 inventory 登録を根拠に、今回の定数結合だけを開いた。数学格付けは工房2206の限定7と2209の不変裁定へ依拠し、新 C5 の実親受付・全source・独立照合を省かない。追加の数学矢印、call coverage、第三独立性、verified の成果は作らない。指定新source/全静的材料をこの pin で freezeし、配置・発射はrootの後続工程とする。Task1080の新受領器草案は別範囲で継続する。

AUDIT_1082_VERDICT: C_INVENTORY_CONSTANT_ONLY_BOUND; WHOLE_RAW_BIDIRECTIONAL_IDENTITY_CONFIRMED; OLD_C5_AND_ALL_FUNCTIONS_RETAINED; SOURCE_AND_SELFTEST_EXECUTION_ZERO; FULL_TYPED_PARENT_METADATA_NOT_COMPLETE; NO_NEW_MATHEMATICAL_ASSURANCE.
