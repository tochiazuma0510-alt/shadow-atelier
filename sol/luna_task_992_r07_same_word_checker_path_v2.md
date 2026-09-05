# Task992 — 同語checkerのv2 source path移行のみ（990完成後）

役: 既存packet_checker。990を完成・凍結してから実行。
変更可は新 `search/check_d972_r07_continuation_same_word_eleven_slots_v2.py` と
`sol/luna_reply_992_r07_same_word_checker_path_v2.md` のみ。新P/WF991のsourceや返信は読まない。
旧C983/986/返信は凍結。ローカルPython/import/AST/数値/GAP/network/git/credentials/新agent禁止。

985の実run33995799635/1でWF受領が停止。原実64のstart.external_e_attachedはboolでなく整数1。
P982:836とWF985:796のis Trueが誤り、P側991がstrict int==1に新P v2で修理する。
C v1は当該誤りを共有していない。C v1:1066のproducer pathがv1に固定されるため、新P v2を正しく受ける
**新C v2へのpath移行だけ**を行う。自分のpath期待もv2にする。producer sourceはpath/wholehash receiptでのみ受ける。

WORD_SCHEMA v1とCのwire schema、保持C9/C4、typed E3/E4、一般LEFT Fox、全11slot、full filtered、freshrho2、
三新canaryと全算術は不変。Pのbool/int修理やhelperをCへ複製しない。必要な変更はsource path/自分識別のみ。
全文diffで算術差分なしを確かめ、実bytes/SHA/行数/CR/BOM/finalLF、CLI・期待canary namesをrootに送る。
rootが991作者へpath/hashだけ渡してWFを仕上げる。GHAはrootが実行、未実行を明記。
最終行 `AUDIT_992_VERDICT:`。
