# certificate 形状の解釈 v3(裁定 139・便 77 F77-4 の処方を全面反映)

状態: interpretation / candidate — v1/v2 を置換する現行界面(v1/v2 は不変・歴史)。Sol 便 77 F77-4.1 の六点回答と F77-4.2/4.3 の処方を条文化。発効時は認可 receipt が本書の exact digest を束縛する(F77-4 NOTE)。

## 条項
1. **chart_ids**: 非空 opaque string の配列。各 ID は curve_model_digest 内の chart registry または個別 chart digest に解決され、座標環・開集合・遷移写像を一意に指すこと(裸の表示名のみは不可)。
2. **witness field のタグ**: W-1〜W-5 系は per-entry `divisor_object` タグ(値 = ramification_divisor_on_C_ref / branch_divisor_on_P1_ref)。**W-6(pushforward)は divisor_object 複製禁止** — 二 divisor と写像の関係なので **`native_side` タグ**(searcher / checker)で lane ごと 1 entry、各 entry = {native_side, ramification_ref, branch_ref, map_ref, witness_ref}(F77-4.2)。
3. **_ref の意味論**: 参照 = {artifact_id, digest, json_pointer または object_id} の三つ組。inline 併記は任意だが、併記時は canonical digest の一致が必須。**不一致は integrity stop([12] digest-mismatch)— どちらかを黙って優先しない**。
4. **単数形 witness**: total_coverage_and_no_extra_component_witness = divisor_object ごと 2 entry(維持)。pushforward は条項 2 のとおり(2-entry 一律規則は撤回)。
5. **ABSENT と MALFORMED の区別**(F77-4.3): 欄の欠落または明示 `[]` = **ABSENT**(証拠不足 → [25] 系へ)。`null`・非配列・タグ欠落・未知タグ = **MALFORMED**(契約違反)— parse/schema 層で fail-closed 停止・ABSENT へ潰さない。reason code は暫定で validator gate 停止扱い(専用 enum `schema-invalid` の新設は Sol へ諮問中)。digest/inline 不一致のみ既存 [12]。
6. **component_bijection**(F77-4.2): 自己申告の domain/codomain リストを authority にしない。entry = **edge**: {divisor_object, searcher_native_digest, searcher_component_id, checker_native_digest, checker_component_id}。受領側が native artifact から両成分集合を再構成し、各頂点の入次数・出次数 = 1 を検査する。index 使用時は native digest と順序を固定。
7. **W-4 の多重度**(v2 (l) 維持): divisor_object ごと厳密 1 entry・層別は per_overlap_witnesses[] 内の各項(chart_pair・generator_chart_a/b・agree・locus_type)。
8. **multiplicity 欄名**(v2 (j) 維持): searcher_mult / checker_mult。**W-5 欄名**(v2 (k) 維持): searcher_count / checker_count / matched_count / no_extra。

## Sol へ残す諮問
`schema-invalid` reason code の enum 新設(条項 5)・chart registry の最小 schema(条項 1)。
