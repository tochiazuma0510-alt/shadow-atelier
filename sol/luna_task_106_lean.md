# Luna 委嘱 106-Lean — F105-6.4 親子実装第 1 束

## 0. 役割・目的

あなたは Luna（Lean 実装増援）。`sol/sol_reply_105_math32.md` F105-6.4 の 8 項目を実装する。順序は厳守する。

1. axiom/checker hygiene
2. Block H TORS-U
3. Block A foundations
4. Block E

T2/Bridge B は quarantine/defer のまま。裸 `Prop` 公理を追加しない。`sorry`、`by exact True.intro`、内容のない placeholder を完成扱いしない。

## 1. build 規律

- 素の `lake build` は禁止。
- `lean/` で `lake build P1` または `lake build +P1.<Module>:olean` の targeted build のみ。
- local receipt は candidate。判定正本は後の GHA。
- Mathlib 依存は既存 policy に沿って隔離し、local で無理に恒常 build しない。

## 2. 要求成果物

1. 全主 theorem inventory を生成し、各 theorem の exact sorted axiom set、正規化 declaration type digest、unexpected axiom/`sorryAx` を fail-closed に判定する checker と AXIOMS manifest/receipt。
2. 四つの bare-T2 `Prop` を import 経路から quarantine。正確な型の Sol 承認前に使わない。二つの `: True` placeholder を inventory から除き、real statement/proof または明示 OPEN にする。
3. TORS-U/B-6tw-lf: character fitting ではなく、有限巡回群の二忠実正則作用と conjugation-induced automorphism を型にする。plain explicit cyclic model の核を先に閉じる。
4. Block A: 実 `G_n` subtype/group、closure/laws、`X in G_n`、cardinality、実 Lambda type と simply-transitive statement。ambient `E_n` の補題を `G_n` の結論と混同しない。
5. Block E: `chiTilde_welldefined` と (3.49) を inventory に含め、`chiTilde_isUnit` の `sorry` を閉じる。未閉鎖なら file-level grade を付けない。
6. T2 はコード追加前に原典 theorem/page、全 hypotheses、domain/codomain、最弱結論、sanity instance の一枚表案だけを返信する。
7. paper-to-Lean statement map と per-theorem receipt、targeted build log を作る。
8. `.github/workflows/lean.yml` は直接変更しない。mathlib cache、sorryAx fail、axiom manifest artifact、targeted jobs を含む **提案版**を `sol/lean_workflow_106_proposal.yml` に起草する。工房承認前に workflow path へ適用しない。

## 3. 六点 delegation envelope

1. **入力**: 現 `lean/`、F105-6.4、Luna 01 receipt、既存 Lean policy。
2. **出力**: Lean source/tests/receipts/manifest、workflow 提案、`sol/luna_reply_106_lean.md`。
3. **禁止**: bare `lake build`、T2 公理追加、Bridge B 着工、`.github/**` 変更、workflow dispatch、git commit/push、credential 読取/出力。
4. **停止条件**: paper statement が不明、Mathlib-only blocker、または targeted build が上限を超える場合は OPEN と exact blocker を報告。
5. **検収**: targeted command、exit code、warning、axiom set/type digest、変更一覧。未証明を verified と呼ばない。
6. **権限**: 実装のみ。paper fidelity/PASS、workflow 承認・push・dispatch は Sol/工房 gate。

## 4. 書込範囲

- `lean/**`
- Lean 用の新規 receipt/manifest（既存規約の場所）
- `sol/lean_workflow_106_proposal.yml`
- `sol/luna_reply_106_lean.md`

`.github/**`、HS、BOTTOM-UP、既存裁定・既存 reply は変更しない。既存版を変える必要がある Lean source は差分を最小化し、user changes を保存する。

## 5. 納品

可能なところまで実装し、各要求を DONE/OPEN/BLOCKED で表にする。`git diff --check` と対象 status を確認。commit/push はしない。
