# Task1194c — V11 metadata canary の期待理由を修理する

宛先: 既存 Noether / receiver_cost_repair。Task1194/1194b の公開 driver/WF 担当を継続する。新 agent を作らない。root は別読と唯一の Git/GHA/network broker。研究者の継続実行認可と裁定2310/2199により、凍結範囲の修理は notify-and-go で再実行する。再承認待ちは設けない。

まず `provenance/rulings_2310_snapshot_20260913.md` と `ops/express/20260913_fable_astra_2310_v11_failclosed_canary_prefix.md` を全文読む。実 run34746915217/1/head200ac2f5885474353a94df4d4b39dbdd4c50c381 は metadata step11 で failure、P/C本走なし。通常 comparator は意図どおり拒否したが `require` が付ける `batch_workflow:` と期待 `wanted` が不一致。step22は下流失敗。root が実ログ/metadata-result の custody を取得する。

作業先は `C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/task1194c/public/` (新規・versioned/CreateNew)。自担当返信は `sol/luna_reply_1194c_public_r07_v11_canary_reason_repair.md`、物理最終行 `AUDIT_1194C_PUBLIC_VERDICT:`。作業ツリーの source/WF を自分で編集しない。P/C私有 source/diff/fixture は読まない。有限 text/JSON/hash 用 author helper は全文自読・pin 後に使用可。対象 driver/P/C の import・AST・compile・実行/selftest、数学再計算、Git/network/credentials/codex execは禁止。

基点は実配備した `search/d972_r07_fixed_lambda_cycle_batch_v11_workflow_driver_v1.py` 63185945 B / fb45024b8f0d0b98e72782444bebe6758242d4231de93205d67222b7c691b8ab、および `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v11.yml` 69995 B / 2b67042d2ee9c9cfd93b69d9cbe614a98912fedea829fc7b803bcd9efa2f8485。基点の全素材/正逆差分/別読票は Task1194 で採用済みであり、その受領をやり直さない。

1. comparator / wanted / 保存側の `v11_saved_public_wire_canaries` / metadata selftest / final join を全て調べ、関連する同じ欠陥を一度で直す。拒否条件を弱めず、exact な理由照合を保持する。裁定2310の F-v11-1 に従い、期待エラー文字列は実 `require()` の書式から導出し、その prefix を別 literal として二重保持しない。通常 comparator の理由名も共有できる最小の方法を選び、期待理由と実理由が全5 canary で一致する自己整合を metadata selftest に接続する。生の拒否を捕まえて自己申告の PASS に変えたり、文字列比較を削除したり、substring/suffix 比較へ弱めたりしない。
2. 旧16 + 新5 の metadata case、同型scalar1個の変異、正例の通常 comparator、copy D3だけ整合、登録全値の不変、保存 fixture/result の正確な再読を保持。元 metadata300/300、旧9群/P/C第10群、元2 child/absolute300、P5400/6000・C10800/11400・RSS7168・job330min/TERM30、23親・rank2474/gen9179・k128/max_batches1/no-refill・C4 raw・著者分離・数学宇宙は一切変更しない。必要 hunk が想定1より多ければ各理由を明記する。
3. P/C source と登録 metadata8本、registry/元の公開契約/親は raw 不変を維持。WF は driver の bytes/SHA pin だけを更新。実 WF path / P WORKFLOW / C CHECKER_WORKFLOW は同じ V11 名を保持し、name=`d972-r07-fixed-lambda-cycle-batch-v11-envelope-v1`、marker=`[r07-fixed-lambda-cycle-batch-v11-envelope-v1-run]` を変えない。修理版の実ファイル候補は TEMP のみ新規保存し、同じ配備 path への更新を root が行う。
4. 完全な raw 正逆差分と全不変区間の EOF 会計、旧/新 source/WF D2、全変更関数/全 caller と関連する5 canary/保存経路の全文、全5理由の静的導出票、凍結 pin 不変票、author helper 自読の証跡を提出。target を実行した静的照合と称さない。root の別読後、pin + 別読票 + marker/name を express へ置き、そのまま修理配置・GHA発射へ進む。

本走結果は未観測として保持し、候補の成立・A0完了・verifiedを宣言しない。
