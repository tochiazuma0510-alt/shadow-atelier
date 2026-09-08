# Task1114 — C6 側からの現 run 入力閉包・過去命題引用の独立設計

役割: Luna (既存 packet_checker)。Sol/root が最終裁定と Git/GHA broker を担う。
指定返信: sol/luna_reply_1114_r07_checker_current_closure_independent_design_v1.md。
補助資料は %TEMP%/shadow-atelier-audit163/task1114/ に新規 versioned 保存する。
この指示書と指定返信以外の作業ツリー変更は禁止。旧 C6/1110/追加32票は凍結する。

## 目的と独立性

2227/2228/2229 の冷保存方針について、現 C6 が実際に読む入力と呼出しから、
現在必要な bytes・型・順序・数学検査、過去採用命題の引用へ変更できる候補、
未決前件を区別する限定設計を作る。実装・変換・数学計算はしない。
P 作者の Task1113 が完了しているが、その私的設計表/返信/原 source は読まない。
P の結論を写さず、自分の C6 と既採用公開 wire・司令塔公開裁定から独立に起こす。
共通の論点は下記だけであり、P/C の非公開実装・helper・fixture の交換は0。

## 固定宇宙

- 対象 C6: %TEMP%/shadow-atelier-audit163/task1110/search/check_d972_r07_fixed_lambda_cycle_batch_v6.py
  = 419541 B / SHA256 3996972ccfe8ba9c168b537ac274de96ff69a6fe27fb400e7de6a8e3a19a52ff。
- 自分の凍結1110全資料と task1110-root-followup の32票を使用可。
- 採用済み例: run34161493396/1、head a5b456a973f8a917f3af386d327061a02a0cf900、
  rank1834/gen8539、2224 cross-checked限定7条項。原97は32件5-key+65件6-key、
  batch384は10-keyで各層 local0 と零係数を含む。native contexts を混同しない。
- 現 v6 は18親/k128/no-refill/同caps/計器、未実行。型・loader・source・wire変更0。
  次の実採用数/rank/genは未観測のパラメータ。1962等を結果として固定しない。
- 実データの大規模再hash、数学 source/import/AST/compile、自作数値計算、GHA、
  Git、network、credential操作は禁止。PowerShell/.NET の小 metadata/JSON/raw範囲
  照合だけ可。環境値や token を読んだり記録しない。

## 必要な納品

1. 自分の C6 の全入力経路を、実 caller/関数の raw offset/bytes/SHA/行と結んだ依存票。
   ファイル名だけでなく root/native role、path/schema、読取 key/type、戻り値と次の
   consumer、数値 kernel が実際に使う部分、過去確認だけの部分、運用保全を記す。
   固定の件数に合わせず、登録した全18 role と現候補/診断/出力比較を覆う。
   同一 file の複数用途を許し、最小閉包と未証明のまま呼ばない。
2. active/cold 切替の保守的候補。全 current 行/offer/lead/target/lambda、固定算術資産、
   P1/maps/辞書等の実データを receipt だけで代用しない。削る旧 caller ごとに、
   その検査を代替する具体的採用命題と証拠の依存を明示。cold blob の pin だけでは
   命題が成立しない。必要な閉包が不明なら active 保持または UNKNOWN を記す。
3. CURRENT_REDERIVED / ACCEPTED_CITED / OPEN_PREMISE の三分による将来報告契約。
   1450/1578/1706/1834 の四歴史 pairing、全 literal/reduction/rolling のうち、
   何を今回再演し何を引用へ移すかを per-call で示す。実施しなくなる旧検査の
   flag/count/範囲をそのまま出してはならない。source hash と実実行は別。
4. 元97/各行の word/rho2 前件、逐次 target 符号、全 rolling/native context、
   local0/零/順序、5→3 descriptor と相対 root 解決を守るための反例検問。
   span等式や telescope だけから逐語式・source lower-zero・positive・A0を上げない。
   wrapper/輸送 pin を元 physical head にしない。sr を含む非可換語の段併合禁止。
5. 初回変換の独立監査と各 run の閉包検査を分離した条件付き案。新 TCB、
   採用裁定/元 P-C/source/runtime/実run pin、cold 可用性・完全復元、全file/空dir
   inventory と logical occurrence map、欠品/不正/資源停止の扱いを具体化する。
6. 性能は (H1) blob重複除去、(H2) 過去全再読の引用化、(H3) rank長factor列codec を
   分けて、何が減り何が残るかだけ述べる。walltime改善・保証run数・他方式不可能性
   は未測定。現 v6 の P/C 別計器を混ぜず、欠測を0とせず inclusive を二重加算しない。

## 完了の条件

全納品を一意の source pin に結び、自己照合した全資料目録を作る。
全入力宇宙と未解消点を列挙し、P 設計との一致・独立数学同値性・変換成功・実性能を
先取りしない。Task1111 の原案同値性レビューは別件であり本便で置換しない。
返信末尾は TASK1114_VERDICT: で、設計完了と未裁定を区別して記す。
