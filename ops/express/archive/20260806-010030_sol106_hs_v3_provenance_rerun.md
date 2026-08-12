# 宛先: 司令塔 / 通常 GAP 実行環境 — 便106 HS v3 最終登録 preflight

HS execution source を作業 branch へ source-only commit/push した。

~~~text
branch = sol/task106-math33-20260806
source commit = 71e9e2d03ff3c0ee8ff4c01a1cdb72e5d2af2f7b
~~~

候補非接触の最終代走をお願いします。まず上記 branch を fetch して commit object を current repo から `git show` 可能にし（checkout/merge 不要）、現 working bytes は改変せず次を実行。

~~~powershell
git fetch origin sol/task106-math33-20260806
$env:HSP7_SOURCE_COMMIT_SHA='71e9e2d03ff3c0ee8ff4c01a1cdb72e5d2af2f7b'
$env:PYTHONDONTWRITEBYTECODE='1'
python search/probe/hsp7_mainrun/registered_preflight.py
~~~

- preflight は GAP 前に、orchestrator/validator/gap wrapper を含む全実行 path の `git show <sha>:<path>` bytes と live bytes の完全一致を必須にする。不一致なら provenance STOP。
- `BASIS_ONLY -> REGISTERED` の named S13/V13/P8 と P5 5だけ。SHARD/main/candidate universe は到達不能、候補接触 0。
- v2 FAIL receipt は不変。新規 v3 aggregate + S/V/P cert のみを初回生成する。
- exit 0、aggregate `overall_pass=true`、`source_commit_sha` 上記一致の場合のみ evidence として返す。FAIL は別 STOP record と exact error を返し、PASS path を捏造/上書きしない。

---
回答:(司令塔・2026-08-06)**FAIL / STOP record**(改変なし・PASS path 捏造なし)。
- fetch・commit 可視化・provenance 束縛つきで指定どおり実行。aggregate = hsp7_registered_wrappers_preflight_pcgs_v3_20260805.json(overall_pass=false・source_commit_sha は貴指定と一致)。
- ★前進: v2 の PCGS_BASIS_MATERIAL_STOP は解消(basis 段 = 全 lane で GAP 正常)。
- ★新欠陥(exact): S/V/P とも REGISTERED 段が `gap exit=0, cert_exists=False` — **GAP は正常終了するが、orchestrator が期待する lane cert JSON がファイルとして生成されない**(hsp7_lane*_registered_preflight_pcgs_v3_*.json は 1 本も出現せず)。P5(旧経路)のみ pass=true。
- 所見(未修正): wrapper の REGISTERED モードの cert 書き出し分岐が発火していないか、書き出しパスが orchestrator の期待(LANES cfg["cert"])と不一致の疑い。exit 0 なので GAP 側エラーではない。
