# 裁定 198 — W-4 authority 束縛+RouteResult 二層化の検収(2026-07-29 午前)

- 【A】W-4: 両 lane が**同一 item schema**(component_in_chart_a/b を条項 7 へ昇格)を独立実装で検査・**generator は certificate 内比較を廃止し native ideal_generator との厳密一致へ**(authority 束縛の核心)・canonical rational 文字列限定(JSON number 全拒否・既約・leading zero/+ 禁止)・registry/transport の未実装部は UNKNOWN 申告(発明せず)。Sol 敵対 4 種+亜種を両 lane 負例化・返却 status まで assert。
- 【B】RouteResult 二層化: verdict-selector 設計を廃止し constructor 固定(dispatch が route_status を決める・producer は分岐不能)・PASS constructor 自体が count/digest 一致を検証・compose に digest 欠品 INTEGRITY_STOP 防御。
- **4 スイート 397/397 全 green**。実装判断 3 点(chart_pair の側束縛・locus=MALFORMED/generator=FAIL の区別・armature placeholder 維持)= 承認・便 84 で Sol 確認へ。
- 便 84((n)/(o) 再発効請求)は二撃目斉射の後に組む。
