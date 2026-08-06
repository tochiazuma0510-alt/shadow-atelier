# 便 111c — Lean 実行ターン第 2 波(G2b)委嘱

発: 司令塔 / 2026-08-06 / 宛: Sol(新セッション)。本便は Lean 線専用(数学監査便は 112 として別送予定)。正本参照: AGENTS.md・sol/sol_reply_111_math37.md(あなたの前セッションの 111b 最終返書)。

## F111c-1. 111b 検収裁定(受理)

- merge 候補 `sol/111b-lean-next-wave-v2`(base 818069c・commit b6c1a4f)は工房で照合のうえ **master へ merge 済(ab64cf2)**。局所作業木の同名 4 ファイルはバイト同一を確認して整理した。
- authoritative run `31059473056`(三 job success)を確認。**裁定: B(CyclotomicRam2 討ち取り)= 狭義 verified・C(G2a finite coproducts)= 狭義 verified・A(T2 型契約)= BLOCKED-FOUNDATION を承認**。
- encoding 事故系列の旧 branch(`sol/111b-lean-next-wave` と run 31059242866)は「非 merge のまま保持」で正。削除・改変不要。byte audit preflight が dispatch 前に捕捉した運用は模範として台帳記録済。

## F111c-2. 次波の裁定 = **Bridge G2b(finite-group quotients)**

あなたの提示した二択(T2 foundation 別波 / G2b)のうち **G2b を採る**。理由: T2 の paper-faithful 型の前提は数学者レイヤーの型設計素材が必要で、当方の数学者は現在別戦役(B₄ 定理検分・予言表)に投入中。T2 foundation は素材が揃い次第の別波とする。T2 import・LA/LE 下流のロックは継続。

- 対象: PreGaloisCategory 義務のうち **finite-group quotients**(G2a と同じ same-universe 方式・固定 mathlib)。
- G2a(BridgeBAffineG2FiniteCoproducts.lean)と同じファイル分割様式・命名対称性で `BridgeBAffineG2FiniteGroupQuotients.lean` を新設(あなたの設計裁量で分割変更可・返書に理由明記)。

## F111c-3. 執行様式(111b と同一)

親子方式(子はターン終了で死ぬ — **turn 内 wait 必須**)・Luna 推論 xhigh・broker は GitHub Git Data API(GH_TOKEN は process のみ・ファイル/ログ書き出し禁止)・byte audit preflight・merge 候補 branch 新設(`sol/111c-g2b` 系)・force-push 禁止・workflow ファイル不変更・封印値/blind 値/探索系非接触・GAP/探索/列挙は行わない(必要時は工房代走を express で要請)。委嘱書には素読ゲート(SELF_CONTAINED 判定)を適用。ETA・困りごとは即時 `ops/express/` へ。

## F111c-4. 完了条件と返書

`sol/sol_reply_111c_lean.md` へ: branch/base/tree/commit sha・authoritative run id と job 別 conclusion・changed paths・非接触申告。verified 射程の限定(P1 全体でない等 6 項)は従来どおり遵守 —「P1 全体 verified」等の拡大表現は禁止。
