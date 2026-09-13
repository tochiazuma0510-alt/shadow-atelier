# Task1194 — V11 の具体実装合意（1193 の設計から続行）

宛先: 既存 Pauli/p6_final_binding、Helmholtz/c6_final_binding、Noether/receiver_cost_repair。新agentを作らない。root/Solは数学裁定・別読と唯一のGit/GHA/network broker。研究者の継続実行認可、裁定2302/2306、Task1193に基づく具体実装指示であり、司令塔や研究者の再承認待ちは設けない。

1193の初期設計段階を閉じ、以下の範囲でV11のsourceと公開metadataを実装してよい。120 slotの実snapshot/sidecarと自担当の全ordinary consumer名簿は並行して完成させ、実値を組み込む最終binding前にrootへ渡す。未形成のSHAや実行結果を捏造しない。設計票を全て書き直すことは不要。後着bindingは小さな正逆差分と実pinで足りる。

作業先 R=C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163、T=R/task1194/{P,C,public}/（CreateNew/versioned）。作業ツリーは自担当の `sol/luna_reply_1194_{p,c,public}_r07_v11_f2_f8_implementation.md` と、1193返信の完成追記だけ。P/Cは相手の私有source/diff/fixtureや独立数表を読まない。Noetherは両私有本文を読まない。自担当のsourceを組み立てる有限text/JSON/raw/hash用author helperは、本票で作成・自分の全文確認/pin後の使用を認可する。対象source/receiverのimport・AST・compile・実行・selftestや数学payload再計算は行わない。rootの別読後の本走はGHAで行う。子のGit/network/credentials/codex execは引き続き禁止。

## 固定する実親と宇宙

親は元run34731988156/attempt1/head785bd2d87f2b97452a7f0deb2085afe4e7e56d95、rank2474/gen9179、state_head168d2cf1004ee6ace61fd082dedb21af41ff1047cf3a88482ed8170ad81786f9。candidate10310711557/448498707 B/e5dabd802d8fe6d21ea67169e724e61239b5f1476a76648e981f05910d83d0d7、mirror560455884。timing-only34735785100を親にしない。

D=R/run34731988156-reception-v1。正式票D/root-v10-formal-and-cv9-mathematical-adoption-v1.json1050634/7385f32671c0742cc91df1ffbf1ca2097b3c80ee21f82445aa4863b2ebc8c4a4、formal5 D/root-v10-formal-inventory5-v1.json229/b2ead8b4b63e3ff76caa2ea1e98d6759bb7d38d619b5fa73bc009e108643536aは採用済み。新親header R/task1193/P/batch-anchor-v10-proposed-from-actual-Q-v1.json156207/bb67a1eebd9d4b2850099940eaddf6afcd2b1835cdad7e67daa4173d1edf3820も、root票 R/task1193/root-v10-parent-header-and-cv9-custody-adoption-v1.json253098/802c9bef4dd59793b9b961439c0bf03a9fd57e5381a961db58649cf7edc6e99dで採用した（1de400全文→4c18d2/native0、全36field/791実D3/29model-only/804input前後）。これらをpending扱いして停止しない。

既22 roleの順序を保持してbatch-parent-v10を1件だけ後置。Pは自分の登録表、Cは独立の名前付き8層の和から23親/8層、previous896/total1024、previous ancestry993/final ancestry1121、phase6144/checkpoint6176/invocation8、current acceptance14/start69/intake89/layout16を導く。保存nativeV10の768/896/993、13/64/81/15は変えない。新選定λ2474=e910b7b65d64b1450e2c9b8aad495488e34b643fc0c6f4a01af5b1a78abf4e36のoracleは未計算null。旧λ2346の保存35780/index435/edge847と混ぜない。次のaccepted数は実測まで未知。

宇宙は54432 vertices/108864 edges/54433 chords、合法性5、source_lower96776/physical_lower32260/physical48384/p1_rows8059、characters0..3、元の2値aux domainを保持。k128/max_batches1/no-refill、P5400/outer6000、C10800/outer11400、RSS7168、元selftest全体300/outer360、metadata300/300、job330min/TERM30は不変。C4 raw、P retained raw、P/C著者分離、旧9群と元2child・元absolute deadline・nonproduction親/production子・16optional+2required envを保持する。

## 共通metadataの具体ABI

Noetherの `R/task1193/public/public-V11-canonical-wire-and-history-DAG-design-v2.json`29476/fda7762199bae13145192f391b5ee95972e10f9fea5b52bcb9bf0959d402b6e5（root全文bc5b46）と `public-V11-workflow-CPU-and-reception-boundaries-v1.json`25137/5ab1f4c299d7d2e9e1fcac7c85547d9a02719ddb687f9b7e79e4e98a7e0a7a1c（e47660/d6b244）を以下の明示事項付きで実装する。

F2: keysets/P_timing/C_timing/producer_interface/producer_final_adoption/checker_final_adoptionのexact6を、それぞれ原典全JSONのASCII・sorted・compact・strict finite・末尾LFのcanonical実ファイルとして、registryより先に独立固定する。duplicate keys/nonfinite/ordinary型の混同を拒否。registryの`public_wire_values`（全値）/`public_wire_value_bindings`（canonical D3）/`public_wire_original_provenance`（原典raw D3）は各exact6。原典、登録全値、source採用、実配備canonical、REPORT/public-declarationsの保存copy、before/after全rawを通常comparatorで結ぶ。registryから比較相手を自己生成しただけで独立照合としない。

source-only root採用leafはP/C sourceと既決入力だけを参照し、未来のregistry/driver/WF/全体closureや自己完全SHAを含めない。循環する旧票の黙ったprojectionも使わない。順序は親原典→count/snapshot/sidecar→P→Pをopaque pinしたC→root source-only採用→全6公開canonical→registry→driver→WF→root全体closure。root発行leafの後着中も他の実装を進める。6実データ＋snapshot/sidecarの計8JSONを新しい有限public metadata入力とし、数学raw3やexecutableと別の全input/保存名簿に登録する。

F8: semantic payloadはexact2 `{schema,native_domains}`、8世代v3〜v10を順序固定、各exact4 `{generation,role,namespace,documents}`、各family exact3 `{present,schema,keys}`。共通documentsのexact15名は `acceptance, checker-result, final-manifest, fixed-manifest, head, owner, parent-intake, parent-layout, progress-head, result, selection, selection-start, separator, source, start`。C内部aliasは `checker→checker-result, fixed→fixed-manifest, final_manifest→final-manifest, parent_intake→parent-intake, parent_layout→parent-layout, progress_head→progress-head, selection_start→selection-start`、残8名は同名。この1対1変換をtrusted boundaryで明示し、同義keyをpayloadへ併存させない。Pのcurrent_count_inputs exact8/current_exact_keysの唯一ownerは保持。

Noetherは実ordinary親原典と完全model/member名簿から119実在＋v3 intake不在の全120 slotを独立に結び、別provenance sidecarにrun/role/model/member全D3/schema/root採用を保存する。不在根拠が未完成なら未知をfalseへ変えない。source読取側は入力文書のschemaから期待世代を選ばず、固定callerのrole/generation/familyから選ぶ。original STARTED/DEADLINE確立後に一度だけviewを入場し、未入場参照・再binding・欠品・同数の別キー・不正型を拒否。終了時も同rawを確認。Cは独立のkey数と元実文書を照合し、P数表を数値の源にしない。

## 各担当の実装

Pauli: V10自己sourceからV11の新親入場と通常metadata経路を作る。現在作成中の全8世代ordinary consumer名簿を先に保存し、その列挙範囲を実装へ接続する。V3/V4のretained25に含まれるbodyは保持し、trusted registered rootと実relative memberを結んだ通常full-file read入口でsnapshot入場を行う。旧literalを残す場合は「保持する追加の全値比較」として明示し、置換済みとは書かない。V5〜V9と新V10のauthoritative schema/keysetは共通viewへ移す。4field final-parent countsや36field anchor header、旧partial fixtureへ全HEAD keysetを付加しない。selftest専用clone、global schema/roleの付け替え、dual-schema fallbackを導入しない。自分のcurrent-count-inputs案13234/be2747fe…と最小第10群14例案18147/27a52472…を使い、旧111例の後で元第2production子に接続、writer/子return/保存scopeを実rawで示す。通常41/条件付き74の予定順を実sourceへ結ぶ。fixture本文/case表/production metadata定数/通常reader/child/旧変更のraw増分を重複なく会計する。

Helmholtz: 独立core v2（22300/69dace79…、root d474f4/0c036b）と後着formal bindingを保持し、新8層の通常projection/ancestry/old-current observationを実装する。全8 consumer設計v2（232224/581906c80493baec5df4eb06216918919ef5e4bca5e576423f740fbc3b7db3b3、root 3d8f4b/93fecf/a7bacd/0d95c7）に共通aliasの差分を適用。7旧ordinary入口＋新eighth入口、20 keyset consumer/29 raw site、91旧reader callを同viewへ結ぶ。v3〜v6のrecords入口は全present familyのaggregate、v7〜v10は通常native keysets、acceptanceは各通常header。HEAD7＋selection-lambda5のpartial scopeを拡大しない。元C4の24名/21distinctとnative再構成bodyの全値/型/seal/順序/数学条件を保持し、残101 pattern行を移行済みと呼ばない。最小第10群13例案15429/e077fdf9…を旧117例の後に接続。通常154の予定順、preservation outer exact11/scope第5key registered_public_metadataを実wireへ結び、measurement_scope文字列は別に固定する。

Noether: 自分の公開driver/WFと全input/保存経路を実装する。CPU modelはsource_modeのruntime-observationにnullable stringを1欄だけ追加しcurrent exact5、observed_runtime/EXPECTED_RUNTIMEのexact2と数学gateは保持。/proc/cpuinfoの最大1MiBを一度だけbest-effortに読み、取得失敗はobserver内でnullに限定し元例外/native/statusを隠さない。CPU値・1回再走から因果識別や母集団上界を主張しない。public F2追加5例は元metadata300内で同じ通常comparatorに正例を先に通し、実最終文書のscalar1つを同型変異、copyのD3だけ整合させ登録全値の拒否を確認する設計で保存。旧59 outerを保持し新親live/restoration/intake/nativeの4つを加えた63を実caller順へ結ぶ。元original/saved driver/WFのregular/no-link、実自己hash観測、全before/after SHA名簿を保持し、新8JSONの原本/copyも列挙する。

2307のmath_headは任意の後続具体設計に留め、本便には追加しない。state_headの既定義、chain/sealの数学入力や判定を変えない。費用回帰の更新・外挿も本便に混ぜない。

## 納品と本走

source基点の完全pin、新版全文と全raw正逆差分/不変区間、全関数・caller・型付きwire、旧9群と新最小群のwriter/return、全公開metadata原典とDAG、増分会計を提出。既にroot採用した基点を全受領し直す票は不要。readmeだけで実caller接続を代用しない。sourceや受領器を全書き直さず必要な差分だけにする。rootは全実sourceと完全差分を別読し、source-only leafと最終closureを発行する。

配置候補は `search/d972_r07_fixed_lambda_cycle_batch_v11.py`、`search/check_d972_r07_fixed_lambda_cycle_batch_v11.py`、`search/d972_r07_fixed_lambda_cycle_batch_v11_workflow_driver_v1.py`、`.github/workflows/d972-r07-fixed-lambda-cycle-batch-v11.yml`。metadataは `search/public-metadata-v11/` の宣言6本とhistory2本。name=`d972-r07-fixed-lambda-cycle-batch-v11-envelope-v1`、marker=`[r07-fixed-lambda-cycle-batch-v11-envelope-v1-run]`。rootはP WORKFLOW/C CHECKER_WORKFLOW/物理WF/WF_FILE/期待launchと実GITHUB_WORKFLOW_REFを照合する。最終4source＋8metadata等のpin、別読票、name/markerをexpress通知し、凍結範囲のnotify-and-goで配置・GHA発射する。run回数制限はなく、必要なら同じ認可内で修理再走する。実run id/commit shaはroot返信とv220に記帳する。

返信の物理最終行は担当別 `AUDIT_1194_P_VERDICT:` / `AUDIT_1194_C_VERDICT:` / `AUDIT_1194_PUBLIC_VERDICT:`。現時点でsource採用・本走成功・新oracle・A0の完成を宣言しない。
