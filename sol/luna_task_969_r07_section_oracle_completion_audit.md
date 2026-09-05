# Task969 — u32 sentinel 修理と checker-only completion の限定監査

役: Luna read-only監査。Task967より本便を優先し、完了後967へ戻る。
変更可は `sol/luna_reply_969_r07_section_oracle_completion_audit.md` のみ。
ローカル数値/Python import/AST/GAP/network/git/credential/dispatch/追加agent禁止。
Task968全文と実diagnostic小JSON/bytes/hashを読む。公刊961は上書きしない。

実run33975617653/1はchecker geometry_payloadsのroot sentinel変換でFAIL。
np.whereの選択前にPython4294967295をint32へcastしようとする型エラーを
sourceの到達順と照合する。complete_tree_eof後だが比較loop前であり、未照合。

監査点:
- 新v2だけが修正され、旧v1/producer output/source/P1/数式は不変。
- int32のroot -1からu32maxへ明示変換、非root/index範囲と誤負値を拒否し、入力配列を
  変更しない。little-endian serializerの正規ABIを維持。実helperの限定canaryがGHAで
  rootの ff ff ff ff と末端index、誤負値/上限/型を試す。旧成功suite再走なし。
- 固定13親/元failure、diagnostic ZIP/実entry pins、全保存output前後不変、元source
  receiptを新checker's source receiptと分離、旧FAIL/newPASSを分離する。
- 新checker一回だけで、producer0/旧suite0。全A–D算術再計算と全stage/top配列比較が
  PASSを必要条件とし、新candidateは不変確認後だけ。未照合witness値をliteral期待値に
  しない。完了前/資源停止からcompletezero/非零受理を作らない。
- 最終source/workflow diff/hash/markerとroot broker限定。旧F-fo-1および新ordinary27の
  保持TCB/2131限定と新CV9 gateを維持する。

v1に追加の実blockerが見つかれば具体的に作者/rootへ伝え、必要な差分だけを監査する。
既読A–D全sourceを理由なく最初から再監査せず、今回の変換・到達順・保存物・workflow
差分に集中する。最終行 `AUDIT_969_VERDICT:`、verified=false。
