# Sol task 368 — A0/v12a code/performance static audit v1

## 0. 裁定と監査境界

**STATIC REJECT**。これは探索結果の裁定ではなく、commit
`2cb97621cdd14bd6af80afb1f68a266cc36cd1ab` の frozen subject に対する静的裁定である。
read-only PowerShell の読取り・SHA-256・ZIP member inspection だけを用い、candidate、
Python、Node、GAP、GHA、git、network、workflow は一切実行していない。従って observed
runtime / RSS / R / V はなく、execution は引き続き `UNEXECUTED`、A0 は `0/1` である。

一意な最初の停止点は producer
`search/d972_r07_history_free_positive_fast_resume_v12a.py:3086 -> 3027-3029`
の `triangular selftest P equation` である。これは task352 で拒否された future-pivot
誤判定が v12a の selftest validator にそのまま残ったものであり、R は構成されない。
さらに、この一箇所を直した仮想経路にも、current dual を用いない selected owner、checker
独立再構成の欠落、miniature mutation owner、二次的 DAG copy、未計上 peak、重複処理、
deadline margin 0、platform boundary 不備が残る。従って一回の v12a
`SELFTEST_BOOTSTRAP` GHA も認可しない。

## 1. Frozen physical identities と P0

全六 owner は委嘱値と一致した。

| owner | bytes | SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12a.manifest.v1.json` | 10,058 | `f127bac60d4fb41d984fcfdc57f77a32cc88e32905207009e6758ec913d1d52d` |
| `search/d972_r07_history_free_positive_fast_resume_v12a.py` | 304,762 | `0e938caeb83b4e65440495b0f50952135d4bfca4309aef38f16c00f50d2905cf` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v12a.py` | 237,150 | `b3d95ae7bb7c82878121a5a386e934b425259ef5ea00e80f31d7202d827750a0` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v12a.g` | 24,621 | `816dfb705d38692393cce28675f90e6759065ebb47714ee8ef4c744a54807610` |
| `search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12a_20260829.json` | 22,094 | `6a87bf608bf0a392ff77d3aacbe813a0cc01f54d67bd5d346fb75ee1e7000ffc` |
| `sol/luna_reply_354_r07_a0_v12a_auditable_selftest_bootstrap.md` | 19,508 | `f5c5e33588916193a4d7e30542a8e81feed17efa8ee904633a44c2044e53c715` |

P0 は ASCII 10,058 bytes、CR なし、LF は末尾の一個だけであった。末尾 LF を除く
canonical object から top-level `self_digest_sha256` field を除いた 9,969 bytes の
SHA-256 は
`7c81a9167612300579dac8bb7dd1b5b3f4a48bf08963f00cdc498edc8ecfedf2`
で、P0 claim と一致する。3 source rows と 30 frozen-authority rows は全て exact
path/bytes/SHA と一致した。pre-driver に raw file が無いことは preregistered extraction
境界どおりであり、ZIP は member 一個
`d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json`、uncompressed
86,368,039 bytes、SHA-256
`c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab`
で raw row と一致する。

P0 の R/V prospective rows は四 field とも明示的な
`TO_BE_GENERATED_BY_AUDITED_V12A_SELFTEST` で、`candidate_only=true`、
`production_authorized=false`、`resume_authorized=false`、
`acceptance_preregistration=false` である。P0 physical SHA は driver line 34 だけが pin
し、producer/checker は hard-code しない。constructor graph は driver から R/V への edge
を持たず、R/V field sets に driver identity はない。この部分は acyclic で PASS とする。

## 2. F1 — 一意な literal stop: selftest だけが future pivot を禁じる

ordinary triangular constructor 自体は正しい。producer lines 1313, 1371-1383 は
`seen_pivots` だけを禁止し、checker lines 2755-2766 も chronological
`seen_pivots` を用いる。しかし producer selftest は別実装である。

- `_validate_triangular_subset` lines 2997-3019 は先に **全** 2,896 pivots を
  `pivot_set` に入れる。
- lines 3027-3029 は各 P row に current pivot 以外の `pivot_set` key が一つも無いことを
  要求する。これは future pivot まで禁止する。
- frozen ZIP member を直接読んだ独立照合では column 5 ancestry は一項 `[[5,2]]`、
  raw support は 8、column-6 pivot は column-5 raw row に coefficient 1 で存在する。
  従って P5 ではその future P6 pivot の coefficient は `2*1 mod 3 = 2` である。
- baseline は lines 3083-3087 で mutation 前に同 validator を通る。main は pre-heavy
  process suite (5655-5657)、`build_heavy` (5658) の後、
  `run_real_owner_selftest` (5659-5660) から lines 5401-5404 を通ってここへ来る。

従って heavy work まで消費した後に line 3028 が必ず拒否し、triangular ledger、残る
mutation suites、R publication (5695-5697)、checker、V、artifact sentinel のいずれにも
到達しない。Luna reply354 lines 86-90 は ordinary builder/checker の `seen_pivots` を根拠に
reachability を主張したが、実際に dispatch される producer selftest validator を監査して
いない。この defect 単独で STATIC REJECT である。

## 3. F2/F3 — selected owner と checker independence

### F2. 「actual selected」dual は current search dual ではない

`_producer_correction_selftest_frame` lines 3600-3714 は coordinate/gamma/roster を走査し、
lines 3624-3629 で direct row の最初の `R` key を選び、row coefficient そのものを係数にした
一項 functional `dual={key: coefficient}` を人工的に作る。この functional はその row と
nonzero pairing するよう構成されているだけで、ordinary triangular route が lines
1392-1396 で得た `runtime["initial_dual_private"]` を一度も参照せず、2,896 basis rows の
annihilation、current target remainder、pivot/rank epoch のいずれにも結び付かない。

record lines 3665-3671 に `pivot_hex/rank_before/rank_after` はなく、にもかかわらず
`producer_selected_statement` lines 3758-3760 は `.get` で三 field を取り、全て JSON null
のまま H に入れる。`producer_final_heavy_identity` lines 3777-3811 はこの manufactured
record を `selected_statement` として seal する。これは task351/task353 の
「current dual による actual selected owner」と heavy identity の契約を満たさない。

### F3. checker は transported dual と triangular summary を独立導出しない

checker `validate_correction_provenance` lines 2439-2486 は transported
`active_dual` の self digest、pairing、weighted formula を再計算するが、その dual を
raw target と triangular basis から導出しない。`checker_validate_selected_frame`
lines 2873-2940 も同じ transported record から selected statement/H を組み直すだけである。

checker source には `triangular_certificate`、`initial_dual`、`initial_solution`、
`target_remainder`、`P_equations_independent` の参照が一件もない。
`validate_selftest_v12a` lines 3196-3198 は process owner の dual が support 1,188 で
self-digest と一致することしか見ず、pinned initial-dual digest、target pairing、basis
annihilationを再計算しない。checker triangular validator lines 2711-2769 は transported
2,896 columns から P を再生するが、P0 graph scan lines 3328-3381 で読んだ 86,368,039-byte
raw checkpoint は parseせず捨てるため、transported columns を frozen raw columns と
byte-for-byte bind しない。raw target、remainder、formal solution も再構成しない。

従って V は R の load-bearing triangular/current-dual/selected-owner summaries の独立 checker
ではない。producer helper import が無いことだけではこの欠落を補えない。

到達不能な route 内にも維持可能な部分はある。projected/full Gamma widths はそれぞれ
`5*40+5*154=970` と `40+31*154=4,814` で別 codec/field にされている (producer
2672-2681, 2764-2771)。producer/checker の K0 open-address implementations は coarse hit 後の
retained full-state equality、miss/mismatch の skip、trivial/nontrivial kernel roster、incremental
parent/word replay、selected coordinate build-count 1/release を実装している (producer
2054-2198, 2288-2372, 3525-3595, 5452-5463; checker 2009-2129, 2335-2436,
4407-4418)。しかし query を駆動する dual/epoch 自体が F2 の fabricated owner なので、これら
local mechanisms の存在を ordinary selected route の PASS にはできない。

## 4. F4 — mutation contract は全 case が real owner route ではなく、かつ到達不能

fixture roster は triangular 8、boundary 13、selected-correction 30、positive 7、physical
11、phase 4、phase-positive 2 cases（worker counts は W2/W4）で、producer/checker の名前 roster
は見掛け上一致する。しかし F1 により producer baseline が最初に止まるので、全 ledger の
execution/reachability claim は成立しない。

F1 を仮修理しても次が残る。

- phase suite lines 5216-5374 は小さな合成 `phase-owner-frame` と nested validator
  (5239-5256) を作り、booleans/digests を変更して比較する。実 checkpoint/heavy/correction
  transition を同じ ordinary runtime で起動するものではなく、miniature substitute である。
- boundary suite のコメント lines 4693-4699 自身が、actual owner は一回だけ動かし、mutation
  cases は envelope validation にする、と宣言する。lines 4756-4787 の `blocked/partial/dead/
  survivors/counter` mutations は worker transport/fault を実際に起こさず、lines 4790-4808
  の一回の W4 outcome を clone する。checker lines 3633-3685 も independent outcome を一度
  構成して frame を変えるだけである。
- triangular frame は全 2,896 columns だが producer baseline validator が誤っており、同じ
  ordinary validator route ではない。従って「各 case が real owner を mutate し、ordinary
  validator を呼び、独立 preregistered first reason と比較する」という全称条件を満たさない。
- checker `_validate_contract_ledger` lines 3089-3132 は producer rows を fixture と比較し、
  checker は後で別 ledger を作るが、両者の normalized rows を最後に exact equality 比較しない。
  V はむしろ `producer_ledgers_replayed=false` (4427) を記録する。fixture への二つの局所比較は、
  producer execution ledger と checker observation ledger の exact match の証明ではない。

なお q3 の literal 1..36 gate と `value-1` conversion は producer lines 924-927、積の式
`right[left[i]]` は line 931 に実在する。しかし lines 932-933 が確認するのは積も permutation
であるという入力から自動的に従う性質だけで、期待する physical product/selected state との
比較ではないため、reply354 が第三 gate を lines 907-940 だけに帰した説明は不正確である。
ただし ordinary route は `bytes.translate` により `right[left[i]]` を使って全 Q0 を列挙
(2440-2456)、全 state stream を task176 physical roster に bind (4030-4032) し、checker も
selected physical roster state と比較する (2513-2515)。従ってこの composite third gate 自体は
PASS であり、REJECT 理由には数えない。

## 5. F5 — DAG expansion は bounded iterative でも quadratic memo-copy

`AncestryDAG.expand` lines 226-263 は recursion を stack に置換したが、各 add node で
`answer=dict(memo[left])` (252) とし、完成した full dictionary を全 node の `memo` に残し、
最後にも `dict(...)` (263) を作る。depth `d` の chain で support が毎段一個増える入力なら、
live/copied entries は

`1 + 2 + ... + d = d(d+1)/2 = Theta(d^2)`

となる。node cap と各一個の answer support cap は aggregate memo entries/copies を制限しない。
しかも `FormalReducer.expand` lines 1234-1246 は expansion 完了後に初めて nodes/support counter
を bump する。`AncestryDAG.expand` の default は nodes/entries とも 2,000,000 で nominal product
`4*10^12`、ordinary metered caller は nodes 2,000,000 / per-answer support 4,000,000 でさらに緩い。
少なくとも support が一段一個増える `d=2,000,000` chain だけで
`d(d+1)/2 = 2,000,001,000,000` entries の witness が cap を個別には通る。実 allocation より先に
止める aggregate cap がない。
task353 の no-quadratic-memo-copy 修理は未了である。

## 6. F6 — actual live sets、caps、不要・重複処理

### 6.1 source から得る payload / lifetime 下限

`N=1,469,664` とすると、producer heavy route の packed payload だけで次になる。

- ten Q0 stores: `N*(5*40+5*154) = N*970 = 1,425,574,080` bytes
  (producer 2695-2699, 2734-2743)。
- Q0 permutation roster: `N*36 = 52,907,904` bytes。
- logical parent/letter の packed 下限（checker decoded raw arrays）:
  `4N + N = 7,348,320` bytes。producer の `parents` は実際には Python `list[int]`
  (lines 2412-2415) なのでこれより大きい。
- selected K0 table: E3 は `N*40 + 2^22*4 = 75,563,776` bytes、E4 は
  `N*154 + 2^22*4 = 243,105,472` bytes（producer 5460-5461、checker
  4411-4417）。

これらは bytes payload 下限であり、`qstates` list、`qids` dict、Python int/list/dict、
memberships、old checkpoint DOM、source registry、receipt DOM は含まない。producer
`runtime.update` lines 2734-2743 は Q0 stores/roster/parents/letters/memberships を R serialization
まで保持し、`SourceRegistry` lines 322-398 は raw/modules/JSON DOM を解放しない。checker
`Sources` lines 362-398 と `decode_task176_owners` lines 529-574 は receipt DOM と六 decoded
streams（raw 合計 60,492,663 bytes）を verdict まで保持する。従って phase release は selected
K0 一個の release だけで、主要 live set の phase release ではない。

producer `Meter` の RSS cap は 5.7 GB (lines 407-422)、checker は RSS 5.7 GB / charged
allocation 4.0 GB (checker 130-164) だが、上記 Python object/JSON/clone allocation の多くを
deterministic counter に charge しない。producer `read_physical_once` lines 1062-1083 は
`bytearray(expected_size)` と immutable `bytes` copy を同時に持ちながら checkpoint counter は
一倍しか charge しない。checker `open_physical` lines 922-996 も bytearray、bytes、ASCII str、
DOM を作るが reserve は二倍までで DOM を含まない。

driver artifact reader lines 202-225 は chunk `parts`、joined raw、decoded ASCII、DOM を全て
materializeする。R と V の各 cap を `C=512 MiB` とすると、V 読取り中の raw-byte object
だけでも、既に保持する R raw と V chunks+joined raw により `R+2V` が同時に live である。
cap が許す端点 `R=V=C` ではこれは少なくとも
`3C = 1,610,612,736 bytes (1.5 GiB)` となる。この Python gate には RSS/
allocation cap がなく、さらに R/V DOM が同時に live である。「512 MiB file cap」は peak cap
ではない。

### 6.2 exact duplicated reads と serialization

P0 の 28 `SOURCE_PINS` は合計 17,789,635 bytes、三 source rows は 564,006 bytes、raw は
86,368,039 bytes、archive は 5,001,811 bytes である。

- producer `validate_p0_source_graph` lines 5547-5561 は
  `564,006 + 17,789,635 + 86,368,039 + 5,001,811 = 109,723,491` bytes を読む。
  直後の `SourceRegistry.authenticate` lines 5626-5627 が 17,789,635 bytes を再読し、
  line 5630 が raw 86,368,039 bytes を再読する。従って P0 自身を除いて数学処理前だけで
  `213,881,165` physical-owner bytes を読む。raw は二回、28 owners は二回、三 source owners
  は三回であり、line 5639 の `parsed_once` は「raw read once」を意味しない。
- checker は `validate_p0_checker` lines 3328-3381 と `Sources.authenticate` lines
  4351-4352 で同じ 28 owners を重複読取りする。さらに `validate_selftest_envelope` lines
  3257-3288 は毎回 P0 と三 sources を再読する。ordinary intended path では main 一回、
  physical suite baseline 一回、11 cases の restoration、7 semantic mutants、合計 **20回**。
  `load_fixture_bounded` lines 2806-2810 も七箇所から独立に呼ばれる。R を除く checker の
  source/authentication reads は少なくとも
  `109,733,549 + 17,789,635 + 20*(10,058+564,006) + 7*22,094
   = 139,159,122` bytes である。
- `_triangular_subset_frame` lines 2970-2982 は 2,896 columns を canonicalize/decode して
  deep copy する。その同じ sealed frame（canonical size を `F` とする）を R top-level
  (5678-5679) と `selftest.triangular_owner_frame` (5465-5471, 5690) に二重 serialize するため、
  R は少なくとも `2F` を持つ。checker は baseline と八 mutants を full clone/canonical/
  physical-write する (3555-3567)。
- checker `checker_mutation_trace` lines 3505-3522 は mutant canonical、baseline canonical、
  `write_frame` で再canonical、次に bytearray -> bytes -> ASCII -> DOM と重ね、mutation open には
  meter を渡さない。

### 6.3 不要な Gamma/Q0 processing と unbounded cache

producer lines 2676-2681 は non-load-bearing full Gamma diagnostic を全 243 states について
作る。raw は `243*4,814 = 1,169,802` bytes、さらに lines 2769-2771 で全 row を hex 化して
hash する。一方 load-bearing projected owner は `243*970 = 235,710` bytes であり、選択 state
以外の full diagnostic 242件の group evaluation/hex serialization は不要である。

checker `checker_q0_parent_letter_digest` lines 761-767 は呼出しごとに 1,469,664 Python ints の
parents list と 1,469,664 letters list を作って canonicalize する。selected baseline と最大30
mutation validations が同 validator を通る (3039, 3049-3056) のに cache がなく、同 validator
内でも parent walks (2568-2571) の後 `reconstruct_task176_selected` (2587) が walks を再実行する。

producer Q0 enumeration は known duplicate を lines 2441-2447 で coordinate work 前に skipし、
この点は PASS である。しかし `pc_cache` lines 2431-2463 は cardinality/allocation cap がなく、
enumeration 全体まで保持される。accepted edge ごとに最大 ten keys、静的な insertion-attempt
上限は `10*(N-1)=14,696,630` で、counter/preallocation cap がない。

### 6.4 worker/RSS/accounting

producer pre-heavy `process_selftest` は normal W2/W4 で `2+4=6` children、三 faults ごとに
`3*(2+4)=18`、blocked-send で 1、合計 25 processes を作る (4586-4689)。しかし heavy 構築後の
`producer_boundary_mutations` lines 4790-4798 がさらに W4 を fork するため producer 合計は 29。
main comment lines 5655-5656 の「heavy 後に boundary child は無い」は偽である。checker も
normal/fault/blocked-send で 25 children (1755-1899) を作り、pipeline 合計は 54 processes である。
54 は cumulative spawn count で simultaneous child peak は 4 だが、post-heavy W4 の RSS は
後述の child-inclusive meter に一度も入らない。

producer normal owner は一つにつき八 epochs（五 probes + 三 serial）なので、各 epoch の
EPOCH/RESULT と WINNER/CONTRIBUTORS、最後の STOP/STOPPED を数えると一方向 `17W` frames。
W2+W4 の normal owners だけで sent 102 / received 102 frames となる。ところが producer
lines 4648-4654 と checker lines 1863-1866 が cumulative に加えるのは normal owner だけで、
六 fault owners、blocked-send、post-heavy W4 を足さない。producer `process_restarts` も第二
normal ownerだけを 1 にする (4603)。これは v290 additive/max accounting ではない。

producer `Meter.check` は child PID list を受けられる (443-457) が、source 全 call site は
省略または明示的空 tuple で、`sampled_children_rss_peak_sum` は常に 0 のままである。owner ごとに
fresh `Meter(WALL_SECONDS)` (4600, 4661, 4793) を作るので cumulative allocation/time も reset
される。checker meter は `/proc/self/statm` だけを読む (130-164)。従って advertised 5.7 GB
は worker-inclusive peak cap ではない。

個々の socket frame は producer/checker とも 32 MiB cap と channel deadline を持ち、W は最大4
なので unbounded queue 自体は見当たらない。この local bound は、上記の未集計 cumulative
traffic、post-heavy fork、child RSS 不計測を補わない。

## 7. F7 — deterministic publication、deadline、driver/platform

producer `atomic_json` lines 2801-2878 と checker `exclusive_json` lines 3387-3437 の
exclusive temp create、file fsync、no-replace hard link、parent identity、directory fsync の順序
自体、および driver stale-output/full-line terminal/neutral candidate sentinel は妥当である。
失敗後の stale R/V を driver が受理する明白な経路もない。ただし次のため総合項目は REJECT。

- producer defines structured `InputStop`/`ResourceStop` (181-191) but its top-level handler
  lines 5700-5707 catches neither class。とくに main lines 5649-5653 は `ResourceStop` を再raiseし、
  他の triangular failures を `InputStop` に変換した直後に、どちらも unnormalized traceback として
  escapeする。従って cap/input exit は preregistered typed `UNKNOWN` terminal にならない。
- checker `exclusive_json` は line 3400 で V 全体を canonicalize する前にも後にも
  `MAX_CANDIDATE_BYTES`/allocation bound を適用しない。bounded publication 契約を満たさない。
- checker process fault rows は lines 1827-1832 で OS/socket timing から来る exception class
  `type(exc).__name__` を `fault_reason` として V の process ledger に serialize する。これは
  preregistered deterministic reason ではなく、platform/timing により変わり得る。
- producer/current-dual と checker independence が F2/F3 のとおり偽なので、たとえ bytes が
  canonicalでも R/V の意味論的 deterministic constructor claim は成立しない。

deadline はさらに即時拒否理由である。driver lines 167-174, 190-191, 285 の envelope は

`T_outer - (T_producer + T_checker + T_artifact)`
`= 21,600 - (10,800 + 7,200 + 3,600) = 0 seconds`。

outer timeout 内には raw archive extraction (117-166)、shell startup、terminal gates/log publish
(170-189)、cleanup もあるため strict margin は負になる。producer internal meter と external
timeout は共に10,800秒、checker も共に7,200秒で、typed resource stop/cleanup の margin も 0。
既知の workflow 自体が六時間なので setup/upload と outer 後の raw re-pin/sentinel check
(286-289) の余白もない。envelope は source 上 fit しない。

platform について、実 GHA Ubuntu では固定文字列 `mkdir -p` は動作し shell injection もないが、
driver line 87 の `Exec("mkdir -p ci/out ci/resume")` は GAP native directory API を使うという
既存 portability contract に反する。producer は lines 1682-1684 で Linux/fork を typed reject
する一方、checker は lines 1770, 1870 で `get_context("fork")`、lines 1778, 1869 で AF_UNIX を
typed platform preflight なしに直接要求する。driver 全体も bash/coreutils/Linux-only であり、
P0 に明示的 platform owner はない。従って actual-GHA-only 前提を正式に freeze するか、native
directory construction と checker preflight を入れる必要があり、現状の DRIVER/PLATFORM は
REJECT とする。

## 8. 有限修理境界

次版で同時に閉じるべき load-bearing repair は以下で尽きる。

1. producer selftest P validator を full `pivot_set` ではなく chronological `seen_pivots` にし、
   frozen P5/P6 baseline と八 triangular cases を ordinary route で通す。
2. selected seed を manufactured one-key dual から作らず、actual target reduction の current
   dual、pivot/rank epoch、annihilation、remainder に bind し、その owner を H に入れる。
3. checker は frozen raw checkpoint を一回 parseし、columns/target/P/remainder/formal solution/
   initial-current dual/annihilation/selected epoch を R と独立に再構成する。
4. phase/boundary を含む全 fixture case を miniature envelope でなく actual ordinary owner/
   transport/transition に注入し、producer/checker の exact first reason ledgers を到達可能にして、
   independently generated normalized ledgers の exact equality を明示的に照合する。
5. DAG expansion を shared/streamed sparse accumulation等に替え、aggregate live entries/copies を
   allocation 前に cap して quadratic memo-copy を除く。
6. P0/source/raw/fixture を一回の immutable snapshot registry で共有し、20回の checker
   reauthentication、parent digest/walk、full Gamma 242件、R 内の triangular frame 二重格納と
   full-frame clonesを除く。phaseごとに source DOM、decoded streams、Q0 stores/cacheを解放する。
7. `pc_cache`、JSON DOM/ASCII/canonical buffers、mutation clones、artifact R/V simultaneous live
   setを meter に含め、checker V publication に hard size capを付け、artifactを streamingにする。
8. 全 owner/fault/blocked/post-heavy transition の IPC/STOP/restartを additive、physical gaugesを
   maxで集計し、実 child PIDs の RSS を samplingする。fresh meter reset と exception-class
   serializationを廃止し、`InputStop`/`ResourceStop` を canonical typed `UNKNOWN` に正規化する。
9. producer/checker/artifact/outer/workflow に strict cleanup/setup margin を与える。GAP native
   directory APIを使い、Linux-onlyなら platformをP0に明示してcheckerもtyped preflightする。

970/4,814-byte typing、known-Q0-duplicate early skip、candidate-only false claims、no-replace/fsync
primitive は維持してよい。しかし上記修理後の新 frozen version を再静的監査するまで、v12a
GHA、v12b、production、resume のいずれも禁止する。

AUDIT VERDICT:                         STATIC REJECT
FROZEN PHYSICAL OWNERS:                PASS
P0 / ACYCLIC CONSTRUCTOR GRAPH:        PASS
ORDINARY PRODUCER ROUTE:               REJECT
INDEPENDENT CHECKER ROUTE:             REJECT
ALL PHYSICAL MUTATION SUITES:          REJECT
DETERMINISTIC R/V + ATOMICITY:         REJECT
STATIC CAPS / PERFORMANCE:             REJECT
AVOIDABLE DUPLICATED PROCESSING:       REJECT
DRIVER / PLATFORM BOUNDARY:            REJECT
V12A SELFTEST_BOOTSTRAP GHA:           FORBIDDEN
PRODUCTION / RESUME / V12B:            FORBIDDEN
ACTUAL A0 COMMON + CHECKER:             0/1
LIFT / FAKE / IHARA:                   NONE

TASK368_R07_A0_V12A_CODE_PERFORMANCE_AUDIT_V1
