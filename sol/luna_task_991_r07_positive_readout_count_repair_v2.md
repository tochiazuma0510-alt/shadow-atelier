# Task991 — 実startのcount型修理・同語PとWF v2（989完成後に優先）

役: 既存packet_producer。989を完成・凍結してから本便へ進む。
変更可は新 `search/d972_r07_continuation_positive_word_readout_v2.py`、
新 `.github/workflows/d972-r07-continuation-positive-word-readout-v2.yml`、
`sol/luna_reply_991_r07_positive_readout_count_repair_v2.md` のみ。
旧P982/WF985/返信は凍結。新C v2のsourceは読まない（rootがABI/pinを渡す）。
ローカルPython/import/AST/数値/GAP/network/git/credentials/新agentは禁止。GHAはrootのみ。

実失敗: 985 run33995799635/1、head920780033b3aaa519a898e8b6b1d29fe67a04cd1。
source/runtimeと十六live/wholeZIPはPASS、acceptで `positive_word_workflow:original-start-not-renamed`。
P/D/canary未実行。alwaysも前段不足で `always-preservation-incomplete`、diagnostics upload成功、candidateなし。
診断9978026066=244085 B/e6565d625f42e9e3202a1faedc271ff07c5c6cfee9cc38558f879155312522b4。
rootが回収中。原実64親のoutput/start.jsonは54707 B/87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b。
実字段は rank1386/generation8091/completed_steps0、external_e_attached=整数1、external_e_numerically_replayed=false。
P v1:836とWF v1:796が `external_e_attached is True` と誤読した。boolを受け入れる弱い==1へは直さず、
**type is int（bool拒否）かつ==1** に結ぶ。原startやP971/Cv2は変更しない。

修理範囲:
1. P v1を新v2へ版管理し、productionのstart header入場をstrict count=1へ修理する。
   算術/SLP/同語/signed/全13出力/WORD_SCHEMA v1/その他receipt wire型は不変。
2. source入場のproducer/checker pathをP v2/C v2へ接続する。Task992でC側はpath migrationだけ行う。
   v2の実source bytes/SHAをrootから渡すまでは最終WF pinを凍結しない。新P/Cの中身を交差読取しない。
3. 実start header型を使う最小canaryをproduction helperに直結する。整数1 PASSとtrue/1.0/"1"/0/2を拒否。
   必要なら既存P新三群に一群追加。WFの期待群数/名前も厳密一致。旧数値suiteの再走は追加しない。
4. WF v1を新v2へ。実十六親/実64/全30pinと現source/math/resource/inputを保持し、name/marker/自身WF保存をv2へ。
   workflow markerは `[r07-continuation-positive-word-readout-v2-run]`。
5. alwaysの実診断を読み、accept失敗時も取得済みlive全親/source/部分receiptsを記録できる順序へ最小修理。
   実前後が揃わないものはINCOMPLETEのまま、原エラーを隠さず、成功candidate条件を緩めない。
   rootから実diagnostic rootと全小JSONを渡すので保存境界はそれから確定する。
6. 他の実start/small receiptのbool/int混同をPとWFで静的検索し、同種なら実型の根拠付きで修理。

原失敗を保存した上でroot/993が最終差分と実入力を独立監査し、GHAで新canary/本P/Dを行う。
未実行試験のPASSや修理後成功を先取りしない。最終bytes/SHA/全差分/CLIと未実行を報告。
最終行 `AUDIT_991_VERDICT:`。
