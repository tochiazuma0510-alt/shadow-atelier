# Luna reply 345 — task343 A4/v5 bidirectional DAG repair

判定は `BLOCKED / UNEXECUTED` です。指示書 Section 1–11 と v285/v286/v288/v290/v292 の境界を静的に読み、許可された5ファイルだけを更新しました。Python/Node/GAP/GHA/workflow/git/network は実行していません。従って下記の実行時メータは測定値ではなく、実行禁止を表す `UNEXECUTED` です。

## 許可された成果物と物理値

以下が今回の4 machine/fixture files の最終物理値です（SHA-256 は作業ツリーからの読み取り値）。driver 自身は in-file SHA 自己参照を作らず、固定外部 commit/run owner に束縛するアシクリックな設計にしました。

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v5.py` | 218912 | `e78537a5e5dcb7b897cf7398bea2f72d467d881c534d1118a9f0e93a99a0e0ac` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v5.py` | 258659 | `49fead3263aba57a9058b9c0b2ed0f893cf45287ec18e772a0068a6ccd7ab3a5` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v5.g` | 13360 | `2099bab7ae7de8d3e31fb15380283bebbf33ecc886895602a43e11209fbe0676` |
| `search/certs/d972_r07_word_independent_successor_kernel_selftest_v5_20260829.json` | 5026 | `696386deb6b093abac2748ae6a7adc0c72aa9e9b8b2da8f065da6f75ac5d626f` |

`D345Pins` (driver 31–39) は producer/checker/fixture の上記 bytes/SHA を exact pin します。D345Driver の自己 pin は除去し、reply と外部 immutable commit/run がその物理値を束縛します。driver は task198 の receipt、acceptance manifest、producer/checker attestation、verdict に加え、producer/checker/GAP の3 physical source を pin し、task176 receipt/manifest/producer/checker source/physical checker result/recovery-v1/recovery-v2 も pin します。

## Section 3/4 — authority と A4 bridge

producer の `AuthorityAdapter` は `search/..._v5.py:608–1015`、checker の独立 `Authority` は `check_..._v5.py:590–1060` です。checker は producer module、producer trie、producer arithmetic instance、echelon、row states、node ids、transcript、digest を import しません。producer は stdlib と自前の affine/Fox/ledger/DAG を使い、checker は stdlib と checker-local `CheckerArithmetic`、right-associated `SuffixDAG`、checker-local sparse/Fox recurrence を使います。共有は pinned public group/quotient primitive の意味だけです。

両 adapter は task198 の receipt/manifest/attestation/verdict と物理 producer/checker/GAP source、task176 の受理 receipt/manifest/両 source/physical checker result/recovery-v1/v2、Q3/E4 identity を `read_once` で検査します。task176 result は physical `757` bytes、SHA `e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5`、self `e9d42ea064e7caaa9a333f7e2a8aec42f709bf1565e9fc9a8950ef92e18ce473` に束縛し、recovery-v1 の b34f 転記は superseded として拒否します。recovery-v2 は `2690` bytes、SHA `67dd555f6e0f943d0161ef2f2c8124b4cc31c9167846b45b43fd2001f5fbba3f`、self `e95b4e7781a14cffd07d445141f20c942861168d201f2ce62879a0ddf3a45026`、accepted receipt self は物理 b34b、`mathematical_grade_change=false` と検査します。

`read_once` は producer `528`、checker `559` から lstat→O_NOFOLLOW open→fstat/read/fstat→pathname identity/nlink 再検査までを一つの opened handle で行います。POSIX で no-follow/identity が使えない場合は typed input stop にします。Windows は現実に同一 CreateFileW handle から FileAttributeTagInfo/FileIdInfo/ReadFile/recheck を実装していないため、別 probe と `os.open` を同一 handle と偽らず `windows_same_handle_identity_unavailable` の typed `UNKNOWN_INPUT` に fail closed します。path は `exact_path`/`output_path`/`checkpoint_input`（producer 499/519、checker 534/550）で repository-relative、ci/in または ci/out containment、traversal、symlink/reparse を検査し、main の `output`/`checkpoint_arg`/`resume_arg` は解決済み absolute owner を保持します。

adapter は literal row ordinal を 6,318 `Gamma_Cayley`、104 `action`、19 `Q0_lift` の連続 global order として検査します。canonical array framing (`[`, comma、`]`) を whole rows と seven chunks (`1024,2048,3072,4096,5120,6144,6441`) に一巡で与えます。receipt の normal-generation proof、row/bridge/typed-coordinate/ABI owners、forbidden flags を declared digest のみでなく literal owner から再計算します。bridge は producer `bridge_trace_from_states` (1068)、checker reverse `checker_bridge_trace` (1640) の各 row assembly 内で ten→eleven→delete/regroup seven→flatten、左右 inverse、11 occurrence fields、10 spellings/state blobs、per-row digest を融合します。DAG 完了後の 6,441 語 flat re-evaluation は追加しません。

actual evaluator canary roster は次の8個だけです：`nonsplit_y_y_section_cocycle, source_2_2, x, x_action_y, x_inverse, xy, xy_section_cocycle, y`。`y_inverse` は要求しません。actor cache の signed 40 entries と actual inverse-word calculation で missing inverse を導出し、producer `ForwardDAG` (1130–1190) と checker `SuffixDAG` (1170–1220) が ten states を cache/replay します。

## Section 5 — forward/reverse row route

producer `primitive_inventory`/`replay_ancestry` (1191/1242) は authenticated 288 primitive words、literal 114,458 letters を authority phase で reduced/alphabet-check し、row route では `tuple(row["word"])` との一回の linear literal comparison と登録 primitive/inverse lookup のみ行います。checker は同じ stored literal に対して自前の reverse suffix recurrence と checker-local substitute/Fox collector を使います。row assembly は producer `build_kernel` (2203) と checker counterpart (約2280) で 6,441 rows を一回だけ構成し、`row_piece_products` を structural 19,408、`typed_context_products` を 10×piece として別 charge します。

固定静的数は `ROWS=6441`、split `6318/104/19`、10 contexts、65 tagged families、288 primitive words、15,970 producer prefix edges/159,700 edge states、26,136 checker suffix edges/261,360 edge states、stored row letters 5,475,488 です。Forward/Suffix new node では node、edge、10 edge-state products、sparse work を高価な state 計算前に reserve します。DAG constructors は canonical key/cache hit を先に調べ、materialize は iterative postorder stack、pre-expansion cap、reduced length `<=` stored upper bound で行います。conjugate は false intermediate product ledger を intern せず、prefix action を直接反映します。

## Section 6/7 — mixed B/K, dual, discrepancy, queue, action

`LiveBasis`/checker `Basis` (producer 1368、checker 約1350) は append-only pivot order と chronological insertion events を保持します。各 combined pivot は formal `(Q,C)`、`C=Psi(Q)+Σ C_l K_l` を持ち、late-B が既存 K で減る場合も event relation を展開して pure-B row と mixed row を分離します。restore は `boundary_row` を入力に再 insert し、event の combined row/detail、raw identity、formal、K row/pivot/rank/raw coefficients を時系列に再導出して saved roster と一致させます。

dual pullback は checker `dual_pullback` (約1458) の inverse elimination order を使い、noncommuting MaxPivot canary (1496) で wrong order と correct order が違うことを要求します。active registry は B/K insertion 時の incremental support であり、毎 query の全 combined-row scan は行いません。correlation は pre-indexed `(context,component)` matching pairs を一回 reserve/bulk-bump し、65-family の actual translated key、`t=g*h^-1; t*h=g`、full accumulator、selected lexicographic column、strict rank rise を normal route で再計算します。

`action_column` は producer 2068、checker 2128 で独立実装し、MEMBER は final K-only `c`、ZERO/rank-rise は `c+s^{-1}e_new`（F3 では `c+s e_new`）を返します。inner support も final labels の subset、非零 F3 coefficient、exact key set として `validate_action_matrix` (2055/2115) が検査します。queue は signed order `1,-1,2,-2`、parent/action/query/event digest、partial matrix、rank-rise owner を検査し、accepted K queue は chronological bijection です。Word/ledger DAG node ledger は translated conjugate action と一致させ、accepted item ごとに `node.ledger == discrepancy` を要求します。

K item は `accept_k` (2006/2038) で `candidate_word,candidate_E,Q,c,s,word_formula,E_formula,ancestry,replay` を一つの owner recurrence から作り、同じ ten states/row を discrepancy、rho、q に再利用します。`public_k_roster` (2464/2087) は process-local `word_node/candidate_node` を receipt から除き、literal recurrence owners を strict field roster として比較します。rho0 は各 context の `element_blob(state.a).hex()` 全体、rho1 は ten Fox components の flattened row と exact normalized row、q は actual `h2_word` です。

`build_anchor` (2146、checker h2/anchor 約2202–2272) は supplied anchor/base_pairs を信頼せず、各 `q(k_i)=z0^a_i` を再計算し、least nonzero `j`、`e=a_j^-1`、powered word、全 adapted rows、discrepancy、rho0/rho1/q を replay します。change matrix は star column `e e_j`、tilde column `e_i-a_i e e_j`、inverse old-j `a_j e_star`、old-i `e_tilde_i+a_i e_star` とし、T*Tinv と Tinv*T の双方を要求します。全 a_i=0 は v247 の exact typed `anchor:all_q_exponents_zero:UNKNOWN_INPUT` です。

## Section 8/10 — checkpoint, resource, terminal, driver

checkpoint payload/state/counter/next-state canary は producer 2640–2970、checker counterpart に同じ field roster を持たせています。保存対象は chronological raw B/L rosters、formal/echelon events、active registry、topological DAG、oracle/query/event/action/dual prefixes、row/bridge digest prefixes、chunk cursor、queue phase、typed semantic/restore/host/peak maps です。restore は saved state を直接再構築し、completed rows/actions の prefix replay はしません。`chunk_start=last_end+1` を要求し、action cursor には exact four-action records、terminal/query relation、matrix column recurrence、event-chain digest を要求します。prefrontier checkpoint は Authority 完了直後に物理 sealed file として作成し、resume 後も geometric queue milestones/terminal frontier で atomic replace します。

Meter は semantic completed additive、restore-validation additive、host current/history、peak max を別 map にし、`checkpoint_current_bytes` は object cap、`checkpoint_total_bytes` は additive work、`checkpoint_peak_bytes` は peak と分離します。hot `bump` は target counter/cap の O(1) 更新、host wall/RSS sample は batch/phase 境界です。producer 固有 prefix nodes/edges/state products と checker suffix counters を typed registry で分け、shared caps と semantic/host/peak/restore map を checker が exact validate します。normal/terminal serialization は final physical length、canonicalization、serialized work、final write を bounded fixed point 内で record し、terminal transport は reserved channel を使います。atomic writer は flush/fsync/replace 後の POSIX parent-directory fsync（Windows は機能不可時 fail closed）を担います。

driver (1–139) は明示的 input/output/checkpoint/resume、14400 秒/8,000,000,000 RSS、producer→checker の serial route、outer `timeout 14520s` transport reserve、exact-one terminal line、status token equality、nonempty sealed verdict、last sentinel を要求します。fresh mode では v1–v5 receipt/verdict/log/sh/ok と checkpoints の stale owner を拒否し、RESUME では checkpoints を required input として保持します。HARD_STOP は mathematical terminal にせず stop/exit 2、typed UNKNOWN_INPUT/UNKNOWN_RESOURCE は checker を必ず呼ぶ設計です。

## Section 9 — first exact blocker (正直な停止点)

ここが最初の未充足 owner/API です。fixture の mutation roster は 48 件で `synthetic:false` ですが、`expected_rejections` は現在 `{"producer":{},"checker":{}}` だけです（fixture SHA は上表の `696386...`）。producer `selftest_certificate` (3328、expected registry check 約3335)、checker (3297/3302) は、各 side の map が48名の完全 key setで、各 entry が exact `{normal_validator, first_rejection}` であることを先に要求します。そのため SELFTEST は route construction/実行より先に `selftest:expected_rejection_registry` / `checker:selftest_expected_rejection_registry` で narrow fail-closed します。これは任意の Reject を受理する回避策ではなく、exact first reason が未提供であることを明示する安全な停止です。

さらに、現行48 route の多くは in-memory slot mutation であり、物理 authority bytes/path/no-follow、row/chunk/bridge/ABI transport、checkpoint resume、atomic/stale/sentinel、physical input TOCTOU の ordinary transport test をまだ実装していません。candidate/prior/translation sparse owner は nonempty precondition に依存し、実行前にその形状を証明する fixture owner もありません。従って `reached_normal_validator:true` を fixture name/stage だけで主張せず、before/after canonical digest、exact validator、exact first reason の48×producer/checker registryを完成するまでは IMPLEMENTED としません。A4 物理 owner についても同理由で、実行せずに PASS/A4 completion を宣言していません。

## 実行・測定・結論

実行は禁止されていたため、SELFTEST/PRODUCTION/RESUME、positive、typed terminal、Linux/Windows transport、checkpoint recovery、resource cap、bridge/DAG arithmetic の runtime result はすべて `UNEXECUTED` です。静的 source は producer forward/checker reverse の row 1、row 6319、後続 rows、B/K queue、matrix、ordered roster、v280 route、UNKNOWN_INPUT/UNKNOWN_RESOURCE/checkpoint/hard-stop の各入口を持ちますが、§9 exact physical owner gateのため positive acceptanceを完了扱いにはしません。reply 自体は測定値をゼロに置き換えず、実行禁止を明記します。

IMPLEMENTATION:                  BLOCKED
SELFTEST / PRODUCTION:           UNEXECUTED
AUTHORITY-V2 INPUT:              A4 1/3 only
ACTUAL POSITIVE BRANCH:          BLOCKED
ACTUAL A4:                       remains 1/3 at most before execution
LIFT / FAKE / IHARA:             NONE
