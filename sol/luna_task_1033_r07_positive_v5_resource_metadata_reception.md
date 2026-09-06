# Task1033 — positive WF5 の公開資源 metadata 受領照合を準備

宛先: 既存 packet_producer。Sol は GHA の本 P を監視中で、artifact 到着前に公開 resource ABI の受領照合だけを準備する。変更可は新 `sol/luna_reply_1033_r07_positive_v5_resource_metadata_reception.md` と `%TEMP%/shadow-atelier-audit163/audit-r07-positive-v5-resource-metadata.ps1`（ASCII only）だけ。公開済み source/WF/票と他の作業ツリーは変更しない。ローカル Python/import/AST/数学/GAP/network/git/credential/新 agent は禁止。root が全文静読してから metadata 操作だけを行う。

対象は実 run34009883488/attempt1、head a590fa9a70322145f1c0688a8f14d2c9640b1bf3、workflow351315722/job101423728128。03:49:33Z から本 P が実行中、04:58:00Z API でも継続、本 D は pending。全親16・実旧64・inventory20・path12・P/D 各新三群と公開 D 型8の工程は success だが、実 payload/計測はまだ未回収である。artifact ID/ZIP pin/実 terminal/語量/資源値は予測しない。

正本は凍結 WF5 `.github/workflows/d972-r07-continuation-positive-word-readout-v5.yml`（180687 B / a840cebcd0ba3f15ff2c31c13b0a09bacd140cb4c8e756466baafd052df8e436）、公開返信1022、公開 Task1024。P 私的 source は自分の既読範囲内だが、D 私的 source/票/fixture の事前閲覧は禁止。公開実 artifact が到着した後の実受領はこの禁止と区別する。旧 TEMP `audit-positive-readout-v4-metadata.ps1` は旧 receipt の参考に限り、MemoryError/exit3/旧実語量/旧 group 数を新期待値へ移さない。新一般 JSON parser や数値 canonicalizer を作らず、PowerShell/.NET の読み取りと既存型別 metadata 比較の範囲にする。

今回の helper は全数学 envelope の代替ではなく、**公開資源 receipt と telemetry の局所 metadata 照合**を担当する。root の完全取得 root と新 ReceiptPath を引数にし、実際に形成された各 P/D main/selftest session の開始/終了/index/cache/telemetry/paths の全対応を読む。全 regular file の実 bytes/SHA を結び、全 JSONL 行を末尾まで読み、行数/単調 sample/elapsed/公開 exact keyset と scalar 型を照合する。未完了 session には完成 index/result を捏造せず、PASS_RESOURCE_METADATA、INCOMPLETE_RESOURCE_METADATA、FAIL_RESOURCE_METADATA を区別する。未形成 D や partial index は、実境界に応じて明示する。ローカルで word grammar/群作用/線形代数を再演しない。

1022/1024 の実 ABI に従い、P selftest top の old_full_suites_run/paths/paths_receipt/reference_source と D top を混同しない。fixture binding の producer basename と main の full binding を区別する。session_sha256 は start file 全 SHA、binary SHA は全 header 含む bytes、index seal と file SHA は別である。telemetry 最終 sample の cache/index_states と result の対応、未形成 cache/indices の null、各 purpose の exact keys、int と bool の区別、finite/nonnegative/monotone float を保持する。fsync/IO/scratch は自分の sample/result 書込みより前の実測なので、書込後量との偽の完全一致を要求しない。普通整数の budget 六字段・型 canary 八件も実 payload から読めるようにする。

計測は実 elapsed/outer wall、ru_maxrss KiB と peak bytes、VmRSS/VmHWM、read/write/fsync、cache payload と Python object overhead、scratch/line/disk-floor を区別して受領票にまとめる。7168 MiB/64 MiB/16 GiB は登録枠であり実 peak ではない。語 nodes/edges/refs は実 metadata の値として読み、未観測の全語完成/全11slot/80644/正語成功を主張しない。全 envelope・全16親/source・全保全の最終合流は root の別受領作業であり、この局所票だけで合格にしない。

取得後の root に空き容量が足りない可能性があるため、準備時点では全展開を仮定して実行しない。全 ZIP 保持・全 stream 読取りを root が先に行い、実展開 root を供給できるか判断する。helper が展開前提なら明記する。新 helper/返信を全文行数/bytes/SHA とともに凍結し、未実行と報告する。candidate/cross_checked/verified/math_replay はすべて false、正式 CV-9 と Lean は別判定。最終行 `AUDIT_1033_VERDICT:`。
