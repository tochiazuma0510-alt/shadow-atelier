# A0 v19 hot-path 静的監査

## 裁定

**STATIC REJECT（production 起動前に必ず停止）。**

最初の具体的破綻は producer の `search/d972_r07_history_free_positive_fast_resume_v19.py:20-25` にある `_replace_once` である。この関数は常に `source.count(new) == 0` を要求するが、per-pair canary 削除 (`:92-95`, `:96-99`) は `new=b""` を渡す。Python の `bytes.count(b"")` は常に `len(source)+1` なので、最初の `worker-pair-canary` 置換で `SystemExit("v19 worker-pair-canary substitution cardinality")` となり、production 本体へ到達しない。

checker も同じ `_replace_once` と空置換を `crosscheck/check_d972_r07_history_free_positive_fast_resume_v19.py:66-71` で使うため、同様に起動不能である。

修正は空置換専用の一回削除 gate（`old` がちょうど1回、置換後に0回）へ分ければ足りる。本便は「最初の REJECT 点で終了」の指定に従い、残りの hot-path 数学には裁定を出さない。
