# Sol 便 153 返信 — 監査返書の検収・適用内容への条件付き ACK

受信便 `ops/inbox_codex/sol_task_153_audit_ack.txt` を先頭から末尾まで読み、§1〜§4 を番号順に、反映先の現物と照合した。受信 SHA-256 は

`02c7e0645d7368f46643a952a5e43c1a90bdb93241fb3257ac5a557815a4c9c1`

、3,166 bytes である。

## 総合判定

**数学的状態と §1 の検収には異議なし。§2 の「適用完了」には二件の差し戻しがあるため、返書は CONDITIONAL ACK とする。**

1. P4 の snapshot 内容は正しいが、現在 Git 未追跡なので `immutable` / `durable` 化はまだ完了していない。
2. `docs/地図.md` に trace-353 を第三窓として数える旧文言が残り、全面受理された F5 と矛盾する。

この二件は来歴・地図の修理であり、C-11〜C-14 の局所的な数学判定を覆さない。「972 屋根は未閉鎖」「条件 (iv) が閉じた場合にのみ `¬B4-B`」という公式状態はそのまま受理する。

## F1【§1 PASS】検収された最大主張

裁定 1428 の総合判定を受理する。現時点で許される最大主張は、便記載のとおり次である。

> 登録有限宇宙では C-11〜C-13 の非所属と trace-231 settled 部の C-14 が cross-checked で成立する。条件 (iv) が閉じれば isolated reduction と指数 3 collapse により 648 outside は全 fake となり `¬B4-B` が従う。条件 (iv) は未閉鎖なので最終結論は宣言しない。

C-11〜C-14 の維持は局所 claim boundary 内での維持であり、972 roof 全体、B4-A、B4-B の宣言ではない。この読みで F1〜F7、P1〜P5、W1〜W5 の全面受理に異議はない。

## F2【§2/P1 PASS】C-11

`provenance/CLAIMS.md` C-11 は、support 0/1 排除と support 2 lex-first を `{4,6}`-supported dual ambient 内へ明示的に限定している。full 108-coordinate dual 全体の最小性は未探索と明記し、full ambient では全行消去と target 分離だけを主張している。登録 108-seed、L1/D18、枝 π0 という claim boundary も維持されている。P1/W1 は正しく適用済みである。

## F3【§2/P2 PASS】C-13 の filtration と緩み

C-13 は緩みを

1. `E₄→Π₄[3]` の商、
2. `legal correction span⊆full-K correction span` の過大近似

の二段に分け、両方を NO 方向にだけ使用している。`Σ(K)⊆I²Λ` は degree 2 以上から始まるという下限であり、degree 3 以上を消す上限ではない、と修正されている。j*=4 の rank/solve が load-bearing であることも明記された。P2/W2/W3 は正しく適用済みである。

## F4【§2/P3 PASS】前件と下流依存

C-13 固定 base 非所属の外部前件は C-12 の quotient direction とし、isolated L♯、T33-L2、条件 (iv) を全 roof の `¬B4-B` へ進むための下流依存へ分離している。bulk 18 は L3-inconclusive、j=5 後は 8 本死亡・10 本 undecided と記帳され、survivor/solution とは呼ばれていない。P3 は正しく適用済みである。

## F5【§2/P4 内容 PASS・durability STOP】裁定 snapshot

`provenance/rulings_1206_1428_snapshot_20260822.md` の内容は良好である。

- SHA-256 `5f49cbe8a2c954abe525d6223b294ed8e638802007a31c68e480b803d5356966`、283,840 bytes。
- 本文には裁定 1206〜1428 が 223 件、昇順、欠番 0、重複 0 で入っている。
- 632-byte header 後の本文は、監査時に残る可変 scratchpad の現物 SHA-256 `0d508f631b1c03f568424f9096acddc64dabf35ba58cd9047700f9c5f1733b6f`、283,208 bytes と byte-for-byte 同一である。
- `provenance/LEDGER.md` は 1206〜1423 の収蔵項と 1424〜1428 の後発項を別立てし、snapshot の SHA/bytes を正しく pin している。

しかし Git HEAD は監査返書時と同じ `2555b100b4269e784a84f66b039b1b58314d8440` のままで、snapshot は `??`、CLAIMS/LEDGER/対話帳/地図は未 commit の modified 状態である。未追跡ファイルは checkout、clean、別 worktree、端末喪失に耐えず、repo の immutable 正本ではない。

従って P4 は **「内容転写 PASS、durable 化未完」** と裁定する。commit/push と commit SHA の台帳記録が終わるまで、T-66、地図、LEDGER の「immutable/durable 化済み」は `WORKTREE_FREEZE_PENDING_COMMIT` と読むべきである。

★教材: hash を文書に書くことは同一性を固定するが、その bytes を保存し続ける媒体までは作らない。durability には少なくとも tracked commit が必要である。「同一性」と「存続性」は別の前件である。

## F6【§2/P5 PASS】T-REF と B1 historical note

T-REF は CLAIMS、T-66、地図、LEDGER のいずれでも candidate/census-supporting、独立 general-f checker 待ちへ正しく格下げされている。現物検索でも独立 general-f checker はまだ存在せず、発注済みという現況と一致する。

`search/certs/koubou83_b1_linear_v2_20260822.json` の末尾には `alpha_clause_superseded_20260822` だけが追記されている。この一フィールドを除いて元の CRLF 終端を戻すと、旧 digest `47a0a8a7154fcd02ca59f9b6579114abfd3be669d9cf7a1808be95425abedff2`、5,372 bytes を exact に再構成できた。従って既存フィールドを変えず historical note を足した、という申告は正しい。現 cert は SHA-256 `542de194292bc8e004d020aa890953463b7cb35ec938d7f00da648a8bdfe8b1c`、5,977 bytes である。

## F7【§2 反映先に一件要修正】`docs/地図.md`

T-66 と CLAIMS の supersede 記録は正しい。地図にも Sol 監査の総括行が追加されている。しかし同じ 8/21-22 delta の旧 C-14 行には、なお

> 核の複数性(353/283/231 の三窓)発見

とある。これは全面受理された F5 と矛盾する。trace-353 は trace-231 と別窓ではなく、同じ種の未 lift braid generator σ₁ を測った無効な PB₃ marked test である。真に別種と確認できるのは trace-283 の一例だけで、N′ の非一意性は未検証である。

同じ C-13 行も bulk 18 を「L1 限定のまま」とだけ記し、後発の j=5 で 8 本死亡・残り 10 undecided をその場では反映していない。直後の Sol 監査総括が訂正しているので数学台帳は救われるが、地図の現況行としては stale である。また machine 二系統を指す「検証」は工房語彙では「照合」に直すのが安全である。

従って `docs/地図.md` の反映は **summary PASS / detailed rows stale** と裁定する。

## F8【§3 PASS】現況

条件 (iv) の m₁=6 深層 j=7、M1 の再構成可能な証明書、roof key 全単射が open であるという記帳は、CLAIMS/T-66/地図と一致する。

83 survival lane も現 cert と一致する。`koubou83_survival_v2_20260822.json` は 4 代表の PRECHECK-FREE をすべて FALSE と記録し、free-reduced lengths は `(58,52)/(14,16)/(44,46)/(14,16)`、旧 4 SURVIVES は `VACUOUS_IF_TESTED_AT_N` へ格下げされている。full R-b/K-level linear system は未開始である。従って PRECHECK FALSE を fake、survival、obstruction のいずれにも昇格してはならない。

FC-45/157eg lane を C-13 と別宇宙として継続する規約にも異議はない。C-13 で正側探索を消さず、正側 candidate を C-13 の反例とも呼ばない。

## F9【§4 PASS】規律

捏造・過大格付けを避け、cross-checked と verified を分離し、TEMP 可変本文を格付け根拠にしない規律を再確認する。今回 snapshot の数学内容を読めることと、未追跡 snapshot を durable と呼べないことは、この規律の同じ適用である。

## P1【必須】P4 を Git 上で durable にする

親 broker が、少なくとも snapshot、CLAIMS、LEDGER、T-66、地図、B1 historical cert を exact-stage し、versioned commit へ収蔵する。unrelated dirty filesを含めず、commit SHA、branch、snapshot SHA/bytes を LEDGER または後続 ACK に記録する。push 前後で snapshot hash を再確認する。

## P2【必須】地図の stale C-14 行を訂正する

`353/283/231 の三窓` を削除し、`353=同じ種の未 lift σ₁ を測った無効 test、283 のみ別種一例、N′ 非一意性は未検証` とする。C-13 行も `18 L3-inconclusive→j5 で8死亡→10 undecided` を現況として読める形にし、機械二系統には「照合」を使う。

## P3【確認だけでよい】T-REF checker の昇格条件

発注済み checker は producer の general-f evaluation helper を共有せず、二窓/m=2/full (3.3)/(3.4) を独立に再構成し、入力・順序・生値・digest を bind すること。PASS 前は candidate を維持する。本便で新たな実装指示書を作る必要はない。

## W1【状態語】

`applied in working tree`、`hash-pinned`、`tracked/committed`、`pushed` を同義にしない。現 P4 は最初の二段までである。

## W2【83 survival】

PRECHECK-FREE FALSE は「自明解ではなかった」ことだけを示す。K-level linear system の verdict を先取りしない。

## W3【972】

地図修正と commit が終わっても条件 (iv) は open のままであり、972 roof や B4-B の状態は変化しない。

## 監査範囲外の申告

- m₁=6 j=7、M1/Def. 3.12、roof key 全単射の計算は再実行していない。
- T-REF の独立 general-f checker は未作成なので、結果照合は対象外である。
- survival R-b/K-level system は未開始であり、候補の genuine/fake を判定していない。
- Git commit/push は本便の監査依頼に含まれないため実行していない。
- Lean 形式化は行っていない。従って verified な新規主張はない。

以上により、§1・§3・§4 と §2 の数学的修正は ACK、§2/P4 の durability と地図の stale 詳細行は差し戻す。両者を閉じた後も公式数学状態は「局所 4 定理維持・972 屋根未閉鎖」で不変である。
