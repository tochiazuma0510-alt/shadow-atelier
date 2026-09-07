# Reply1071 — envelope-v3 実launchの限定登録

F1. 新静的版 `%TEMP%/shadow-atelier-audit163/task1071/audit-r07-batch-v4-metadata-v3.ps1` を保存・凍結した。260010 B / SHA256 `accc758ebe41c6c5a239245a62beb961ef1f145bf04f3154c6b34442ec774e44`、LF2444、CR0、ASCII、BOMなし、末尾LF、行末空白0。実launchと発効済み承認2197だけを登録し、ExpectedArtifact=null / ImplementationComplete=falseを保持した。helperは実行していない。ファイル版はv3だが、受領票の既存wire schemaや比較機能は変更していない。

F2. Task1071全文3360 B / `ac9a26f0dc183cca747738e2872a5277185aa7aa9a040e4e6c974247d39c647a` に従った。基点1069全259814 B / `9f9e920b82a0525c41f3eb2aa563a4e5c5d0ba0993deeb7ac16b2a62c9fab826` を `baseline-1069-metadata-v2.ps1` へCreateNew保存。作者1069最終返信10943 B/e6c4dbbf…、独立1070最終返信12801 B/05220a21…の射程を保持し、1070全文を読了した。これら原本を変更していない。

公開追加入力 `registered-producer-body-inheritance-v2.json`（17587 B / `768cbfec35dae2abc80cade25f184c626bef07a8fefb758383a8669e23a0ebed`）と `registered-producer-current-regions-v2.json`（267079 B / `b36818b41ab82ea33e2008e6db921e9cfb4138af472a473b47bbeac2eac063b9`）も新helperと同じdirへCreateNewで全raw複写した。原本の前後hashとコピーhashは一致した。

差分はL10の便名説明、L25の観測済み説明、L27のExpectedLaunch、L28のExpectedApprovalの4行だけ。全関数・main・source/caps/registry/親/比較gateは全raw不変で、完全逆置換は基点259814 bytesへ一致した。新機能や型の緩和は加えていない。

F3. root保存APIを全file pinで認証し、保存runs一覧内の唯一の実run、workflow登録、jobとroot launch票を照合した。新helperに入れたexact5字段は次のとおりである。

| 字段 | 値 | 型 |
| --- | --- | --- |
| run | 34120585268 | Int64、正整数 |
| attempt | 1 | Int32、正整数 |
| head | 92720e5371164545259c3007cb11e951fa5e1686 | string、40桁 |
| workflow | .github/workflows/d972-r07-fixed-lambda-cycle-batch-v4.yml | string |
| workflow_id | 351613185 | Int32、正整数 |

job101737466647、event push、branch `sol/r07-explicit-lift-20260825`、created_at `2026-09-07T12:12:10Z`、実run名 `d972-r07-fixed-lambda-cycle-batch-v4-envelope-v3` を別の記帳に保持する。workflow登録APIのdefault-branch由来nameは旧envelope-v2だが、id/path/state=activeは実runへ一致する。nameを改書きせず、実run名と区別した。

| 保存されたroot/API入力 | bytes | SHA256 |
| --- | ---: | --- |
| v4-envelope-v3-root-launch-v1.json | 2211 | `1ae3842f750e43770ffea9717a93a19bc7ddc46e3a557c802ca5b0d37eebafd7` |
| v4-envelope-v3-runs-initial-v1.json | 525631 | `2d7f5b2c9efb9339c61bf208db85a83fce6e767a6cd9b7367c5e944ccfece160` |
| v4-envelope-v3-workflow-initial-v1.json | 652 | `eb43f402475c2bbe46f5522f153757266b3f4dc83b6495d1cfb8bfb63c593e36` |
| v4-run34120585268-jobs-v1.json | 5220 | `10aa804fd99c1fb95ce97e20173c50e982338c9efec719524220837608d1dc35` |

保存時点ではstep1–8成功、step9進行中、job conclusion=null。それ以降のP/C/全artifact/最終成否は本便で未受領であり、追加API照会や未来値の補完は行っていない。この記帳を現在時刻の最新statusや数学成果へ読み替えない。

F4. 二つの公開expressを全文読了した。2197発効票1771 B / `e24d8e2330c3b56063a9c40740fa66d15ae5925869013625ad5542bb0776c7af` が今回起動の具体承認である。2196は条件付き承認、2198は最終pinの受領、2199は研究者の継続指示を受けたGHA回数制限撤廃と凍結envelope内のnotify-and-go規約であり、起動承認番号へ混ぜない。2198/2199票は1842 B / `cc59df74b783b878d94a693a87f7909d8ebed33489cfb41bec686851a4efc6bb`。Git/GHA/credentialの実行者はrootだけで、今回この子agentは行っていない。

F5. 新TEMP/task1071の比較票は次のとおり。

| 票 | bytes | SHA256 |
| --- | ---: | --- |
| baseline-and-input-copy-pins-v1.json | 1745 | `13dadd43292cc67cd54eb52957d11154e2f486d15033b75a689caf9e8167598e` |
| actual-launch-saved-API-binding-v1.json | 15120 | `03bc656a88ba12d700c6921ad0985fb68191673f5d0d00e0ccb25bd9c7178a49` |
| whole-raw-literal-delta-v1.json | 2955 | `d68b55bc9f7e588516ce1987b976cafd4331ac2f7101933d583d0059cc0ad2c7` |
| whole-raw-literal-delta-v1.txt | 850 | `e5f4a8ae370cfe8cedab9cced0dac5cb2e3b158ae80826078efc56f18080cbbf` |

F6. 今回は保存済みmetadataの型・全pin・raw文字列比較だけを実施した。新旧helper、P/C source、数学、Python/import/AST/compile/GAP、network/Git/GHA/credential、新agentは実行していない。変更したのは指定TEMPと本返信だけ。自作Cの独立算術監査や実candidateの受領PASSではない。

完成candidateの実acquisition/全ZIP/identityが後着した場合だけ、rootが別snapshotでartifact exact4字段とguardの解放を扱う。この版はartifact未形成のため実行不可。実runがFAILなら完成candidate mainへ適用しない。後着を待たず、今回の実launch記帳をこのpinで閉じる。

AUDIT_1071_VERDICT: STATIC_ACTUAL_LAUNCH_BOUND_ARTIFACT_NULL_GUARD_CLOSED
