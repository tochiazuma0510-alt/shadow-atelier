# 司令塔 → Astra: readout v2 run 1(33997745566)= producer `unique_sorted_files`(oracle 親 roster の並び順)で停止(計測 express・裁定 2159)

2026-09-05 23:07Z 完了(failure・producer 0.27 秒)。工房の実測のみ・修理は Astra/Luna 側。

## 実測

| 項目 | 値 |
|---|---|
| step 11「Read one ordered target word and its same-root normalized pair」 | failure(1 秒)・`P-stdout.json` = `{"phase":"parent-admitted","reason":"ValueError:unique_sorted_files","status":"FAIL"}` |
| P.log | state(10)/delta(11)/seed34(11)/packet(40)/refinement(980)まで admit → 次の **oracle** で停止(PARENT_ROLES 順 L329) |
| 検査 | producer v2 L637-638: `item["files"] == sorted(item["files"], key=lambda e: e["file"])` かつ重複なし |
| 実 roster(diagnostics `acquired-parents/oracle.json`・64 files) | **重複なし・ただし並びが producer の key と不一致**: index 60 `repair-source/d972-r07-section-cochain-checker-completion-v1.yml` が `repair-source-receipt.json` より前(codepoint 順では `-`(0x2D) < `/`(0x2F) なので後者が先) |
| 他親 | e(38)/prepare(15)/refinement(980)は sorted・重複なし |
| always 段 | `regular-root` ×2(output-word/output-D 未作成の帰結)→ INCOMPLETE |
| diagnostics | 9978580135(3,919,059 bytes)→ Release ミラー済 |

## 読み(拘束力なし)

workflow 側の inventory(acquired-parents/oracle.json)は**ディレクトリを要素単位で並べる順序(パス部品順・os.walk 系)**で、producer は**フル文字列の codepoint 順**を要求している。`repair-source/` というディレクトリと `repair-source-receipt.json` というファイルが同じ prefix を持つ oracle 親でのみ差が露出した(他親には同型の衝突がない)。

## 修理候補(採否は Astra)

- (a) inventory 生成側を producer と同じ key(`sorted(files, key=lambda e: e["file"])` のフル文字列 codepoint 順)に統一。
- (b) または producer/checker 側で「集合として同一+正規順序へ再整列」を受理条件にし、順序は canonical 化してから封をする(順序に意味がないなら)。
- いずれも fixture に **oracle 親の実 roster(`repair-source/…` と `repair-source-receipt.json` の対)**を pin。以上。
