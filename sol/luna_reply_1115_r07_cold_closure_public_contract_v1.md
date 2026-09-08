# Task1115 返信 — 冷保存の公開 exact 契約候補

F0. 公開設計を完成・凍結した。namespace は `shadow-atelier.r07.cold-closure.proposed.v1`。実出力schemaや実装採択ではない。Task1115全文6105/5ae5a24956858e1b9a7fdae22ec430df0c7e78993c6d281c8a884585ae1d746c、凍結1111、2230正本／速達を全文読了し、rootの途中精密化を結合した。P/C私的設計・source・返信と1116/1117材料は読んでいない。

F1. 全資料は `%TEMP%/shadow-atelier-audit163/task1115/`。目録 `final-public-material-manifest-v1.json` = **3484 B / 4463d8cf91f31605e8a09c5ff5157faebac937ccb92501841dcc1f6fdf48ba5b**。下記6材料466088 Bを全raw再読・pin照合して固定した。目録自身と本返信は自己hash循環を避けて目録の外側に置く。

| 材料 | bytes | SHA-256 |
|---|---:|---|
| public-contract-v1.md | 28233 | d9c8f1608009c6fd67ea6bc98fe434ffd0604a8853371a5c07a6ab1bf76e6251 |
| public-type-table-v1.tsv | 76544 | fd573cbeeef064ecf160e21f5801ec3a0555ac9d19614701a82b7df7fa48b546 |
| public-consumer-obligations-v1.tsv | 242655 | 77c8c76829eec07158ffa23b35b76402183d1aaa4db784d43de55f7b67ed47c0 |
| public-consumer-families-v1.json | 13562 | 053f36a1d31e34b412d55f4e7971f84c68ce7472c35744ad79c4f57e5163d905 |
| obligations-and-counterexamples-v1.md | 20332 | 5c469008fa510e545bf1f05d5b1519882dd674f8f172488bb7a319b89677007f |
| author-self-review-and-open-parameters-v1.json | 84762 | 9b3afbf7682a397316e142bf3b2f49bdfb5f4bdd4e6abbeab7c9a7c980e9b7b5 |

F2. 型表は72 record alternatives／489字段、consumer表は17意味reader＋全字段共通C00、506行（17字段の複数用途を重複列挙）。全key/type/nullable/order/root-referenceと、今回raw読取／引用pin読取を分けるread_scopeを記載した。公開型名の未定義・未対応字段・重複key・type/null/order/ref/述語のconsumer転記差は0。これは公開wireの全字段対応であり、P/C実装の全内部usepointを独立監査したとの意味ではない。

F3. 0-basedは新wrapper位置だけ。元native candidate/local/index値と文法は元rawのまま、明示写像へ結ぶ。`global_row_position=1450+o_i+j`／`ancestor_position=97+o_i+j`をrank/countと分離し、実a_i/p_i/u_i、採用0層、未完候補と完成prefixを区別。元97 mixed shape、零、順序、整数指数、native multi-row更新、有限typed DAG／Γ／foreign root／各rolling familyのbodyと除外字段を保持する。old64を含め一律17-key／sha字段／現schemaへのcastは課さない。

F4. 現P6/C6のplain/packed SHA・scalar結合と、将来課す各explicit transitionの数値差分／全中間target再計算は別。元8059／元97のΓも別に残し、既実施の再計算や現source欠陥へ読み替えない。追加費用は未測定。異なる歴史λの問いはACCEPTED_CITED候補、最新親λの全行・二targetと新候補／新λはCURRENT_REDERIVED、元word/rho2/lower-zero/positive/A0はOPEN_PREMISEを保持する。引用には具体採択条項・元P/C/source/runtime/入力閉包／限定が必要で、cold pinだけでは足りない。

F5. 全旧ordinary file/dir/空dirの復元写像とactive/coldの論理／物理目録を分離した。現在必要な同一fileの用途が一つでもあればwhole fileをactiveに残す。最初のP変換と独立Cは全原物→全出力→全復元・全EOF／raw一致を実照合する将来義務。各runのAは全cold raw再hash、Bは既全復元票＋immutable世代／全object存在・長さ等に依存する未採択TCB。Bはcurrent_full_cold_rehashをtrueにせず、旧全tree不変旗も偽昇格しない。欠品UNKNOWN_INPUT_MISSING／評価不能OPEN／不正REJECTEDを区別する。

F6. coreには先行可用性規約だけを置き、Bの既全復元票は後続ExecutionBindingへ束縛する。新core／実acceptanceは外側のwhole-raw sealで別形成し、将来票への自己hash循環／wrapperをnative hにすることを禁止。今の新出力は元native schema・実contextのまま扱い、未形成artifactや次回変換coreを先取りしない。正例P0–P7とN01–N23の紙上反例familyを保存し、単一意味変異／必要reseal／目的の通常reader到達を要求した。早期hash拒否と後段意味拒否は別採点で、実fixture／目的拒否／変換成功は全0。

F7. root未裁定は、実変換元と条項、native公開catalog全束縛、P/Cの各用途・動的alias・変更global・内部閉包とTCB、Vの引用移行／包含根拠、Bのprovider／世代／安定性／採択、H1任意共有、実converter source/runtime／通常callable・拒否型、具体配置／実inventory／実a_i/p_i/u_iの8群。必要性未確定fileはactive、H3は非採用。起動時復元や前後hash一致だけでは途中改変・後の外部削除を防いだとは言わず、同じ認証済みbytesを使う条件を公開義務にした。削除主体は観測なしに推測しない。

F8. 自己再読とmetadata表の整合照合を完了。1111／1108の返信、1111独立性票、1108 immutable v2 driver/WF/registryの6保護入力は全実bytes/SHAが凍結pinと一致。納品材料はCR0/BOMなし/finalLF/行末空白0。新source・数学・Python/AST/import/compile/selftest・Git/GHA/network/credential・実parent/process操作・新agentは0。v6 18親/k128/同caps／計器／格付けを変更せず、WF既契約はbytes<500000のまま、1115を新たな発射待ち条件や各試行の新ユーザー承認要件にしない。実可用性・最小閉包・変換成功・速度は未立証、verified=false。

TASK1115_VERDICT: PUBLIC_CONTRACT_PROPOSAL_COMPLETE_RUNTIME_UNEXECUTED_ROOT_CHOICES_OPEN
