# Task1004 — 完成済batchへのresumeの公開契約（root → 994P / 995C / 996監査）

Task997 F10のinvocation開始規則を、完成済の再受付についてだけ明示する。新P/C本文は共有しない。

HEADとresultが両方存在し、全登録入力・portable identity・全保存bytes・全通常完了roster・両者の相互結合が認証された完成packetに対する --resume は、既存resultをそのまま返す読み取り専用の再受付とする。新invocationも新resultも書かず、旧elapsed/counts/実行来歴を新runの値として報告しない。新たなGHA受付と呼出しの実時刻・exit/既存stdout byte一致は外側execution receiptへ保存する。Cは新invocationが増えないことを拒否理由にしないが、完成packetの認証条件は省略しない。

HEADのみ/resultのみ/不完全相互結合はこの分岐に入れない。未完prefixからの通常resumeは従来通り開始時に一度新invocationを書く。resume=falseの既存output受理、source/pin/登録サイズの異なる再受付、破損roster、別runで既存elapsedを新計測とする扱いは認めない。最大1batch/選択k32/親64/rank1450/grade2境界は不変。

これは完成packetを再実行したという算術主張ではない。新数値試験はGHAのみ、rootだけがgit/GHA broker。
