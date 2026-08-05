# HS NW(7) 主走事前登録 v3（候補非接触・再 gate 束）

- 日付: 2026-08-05
- 状態: **candidate / main run 不認可**。本書は実行 class の物理化であり、候補探索の許可ではない。
- 上書き禁止: v1/v2 と旧 Appendix C は歴史記録として不変。本 v3 が今回の差分正文。
- 根拠: `sol/sol_reply_105_math32.md` F105-2.3/F105-4、`sol/luna_task_106_hs.md`。

## 1. exact universe と意味論

共通の主窓は

$$P=F_2/(\gamma_5(F_2)F_2^7),\qquad D=[P,P],\qquad
\operatorname{Pcgs}(D)=(g_1,\ldots,g_6),$$

`RelativeOrders=[7,7,7,7,7,7]` である。指数ベクトル
$e=(e_1,\ldots,e_6)\in\{0,\ldots,6\}^6$ は
$g_1^{e_1}\cdots g_6^{e_6}$（左から右）の元を表し、$e_1$ を最上位桁とする。

$$f\_index=\sum_{i=1}^6 e_i7^{6-i}\in[0,117648].$$

$X_N=(0,1,2,4,5,6)$（この順）とし、$m\_index$ は 0 始まり位置、

$$pair\_index=m\_index\cdot117649+f\_index\in[0,705893].$$

Lane S/V の exact universe は全 705,894 pair、Lane P は PENT が $m$ 非依存なので全 117,649 f-key である。Lane P の一行は checker が独立に

$$f\_index\longmapsto(f\_index+j\cdot117649)_{j=0}^5$$

を再導出して六つの pair-key へ展開する。GAP の `Elements()`/BFS 順は identity に使わない。

runtime ordered basis は source hash や自己参照的な unit-vector 往復だけでは同定しない。
`hsp7-ordered-pcgs-material/v1` は、権威 source artifact の path/SHA、ambient
`Pcgs(P)` の相対位数、同じ ambient pcgs で測った named $x,y$ と ordered 六
$D$ generator の座標、theta/tau の六像、S→V の逐点 bridge を serialize する。
rank 2/class 4 の本 $P$ では $D=[P,P]$ は可換なので、15 本の pair-commutator
座標は**すべて零が正しい構造データ**である。非零を要求しない一方、ambient 六行は
相異なり非零、theta/tau 行列は $\mathbf F_7$ 上可逆かつ非恒等でなければ STOP とする。

## 2. 三 lane の production 経路

### 2.1 Lane S

`lane_wrapper_S.g` は簡約 (3.10)
$f\theta(f)=1$ と (3.11)
$\tau^2(y^mf)\tau(y^mf)y^mf=1$ を P で評価する。旧 dry stub の
`Hex311(f)` は $m=0$ 専用だったため廃止し、production wrapper 自身が必ず
$y^mf$ を構成する。

### 2.2 Lane V

`lane_wrapper_V.g` は `predicate_lib_laneV_cf.g` の閉形式で N/N0 両窓の full
(3.3)/(3.4) を評価する。語への `PreImagesRepresentative` は候補ごとには行わない。

- Lane-S P から Lane-V P への $x\mapsto x,y\mapsto y$ 写像を構成し、全単射・生成像一致・六 pcgs 生成子の逐点一致を発火前に確認する。
- $A_1,A_2$ は well-defined だけでなく、定義生成元の像が窓全体を生成し、`IsBijective` が両方 true であることを production constructor 内で確認する。
- N/N0 verdict が一件でも異なれば S-8' 型 `INTEGRITY_STOP`。部分成功にしない。

### 2.3 Lane P

`lane_wrapper_P.g` は `predicate_lib_laneP_conv.g` の CONV-P で、P 側 pcgs 指数を Q 側へ送ってから frozen `PENT` を評価する。六生成子の preimage 接続式に加えて、実際の準同型
$D\to\langle\widehat G_1,\ldots,\widehat G_6\rangle$ を構成し、生成像一致と全単射を必須 gate にする。PENT は f-key ごと一回だけで、六 pair-index は cert に実記録する。

## 3. cert / source binding

各 wrapper は `hsp7-lane-cert/v3` JSON を**実際に書く**。`would_write` は成功条件でない。必須欄は class ID、run id/attempt、commit、source-bundle/wrapper/predicate/aux/schema の SHA-256、runtime PCGS material と canonical JSON SHA-256、exact range、全 record、UNKNOWN 数、`integrity_ok`、`driver_done=true` である。いずれかの binding が空/`UNSET` なら発火前 STOP。

runner は wrapper の自己申告を信用せず、lane/axis/universe total、class、run id/attempt/commit、五 source binding、range/count、lane 固有 record 型と key 算術、実 record から再集計した UNKNOWN 数、integrity/done をすべて独立照合する。さらに SHARD の**前**に候補非接触の `BASIS_ONLY` を走らせ、live runtime material の canonical fingerprint が frozen lane 値と一致した場合だけ候補 range に入る。collect 側も download 後の cert bytes と receipt の hash/raw/gzip、class/manifest/source/shard/range、pre-shard fingerprint、同じ cert binding を再照合する。class path と file SHA は workflow の二つの freeze sentinel に固定し、receipt 数だけでなく exact unique shard set を要求する。

registered preflight の `run.commit_sha` は ambient HEAD の自己申告ではない。明示
`HSP7_SOURCE_COMMIT_SHA` を必須とし、orchestrator、validator、`gap.ps1`、schema、
全 wrapper/predicate/aux/P5 source の live bytes が `git show <sha>:<path>` と全一致した
場合だけ GAP を起動する。aggregate はその全 file map と orchestrator/validator/GAP
wrapper の path/SHA を保持し、class builder が live bytes と commit bytes を再照合する。

主走 shard では range は非空でなければならない。登録 fixture モードだけは named family を直接作り、range を `[-1,-1]` として main join への混入を `cert_to_join_manifest.py` が拒否する。

## 4. exact shard / workflow

本 v3 では次の一組だけを登録する。runtime の観測で自動 resize しない。

| lane | axis | total | target size | shard 数 | 最終 shard | workflow run | max-parallel |
|---|---:|---:|---:|---:|---:|---:|---:|
| S | pair | 705,894 | 3,678 | 192 | `[702498,705893]` (3,396件) | 1 | 20 |
| V | pair | 705,894 | 54,000 | 14 | `[702000,705893]` (3,894件) | 1 | 20 |
| P | f | 117,649 | 3,678 | 32 | `[114018,117648]` (3,631件) | 1 | 20 |

全て 256 job/run 以下。`shard_manifest_gen.py` v2 はこの三サイズ、60分、max-parallel=20、max-jobs=256 以外を class-v3 manifest として拒絶する。draft workflow は `search/probe/hsp7_mainrun/hsp7_mainrun_workflow_v3.yml`。`.github/workflows/` へは置いておらず、dispatch もしていない。class component は freeze 後に書き換える path/SHA literal 自体を含めず、その二値だけを `UNSET_REQUIRES_FREEZE` へ正規化した workflow template SHA を束縛する。実行時には installed workflow が自身の正規化 SHA と final class path/file SHA の双方を検査するため、class↔workflow の hash fixed-point を作らない。

## 5. timeout / STOP / UNKNOWN

- runtime PCGS `BASIS_ONLY` は **15分**、本 shard は **60分**の hard timeout。前者の失敗・fingerprint 不一致は候補評価 0 の STOP、後者は `HARD_SHARD_TIMEOUT/STOP` receipt とする。GHA job 側は setup/upload/receipt 用余白を含む 90 分。
- GAP nonzero、cert 欠品、range/count 不一致、source/class/digest 不一致、`integrity_ok!=true`、`driver_done!=true` はすべて STOP。部分 cert を完了数へ数えない。
- 現 production predicate は Boolean または fatal error である。fatal error を UNKNOWN に格下げしない。将来 recoverable な第三値を追加する場合だけ、候補ごとに `status=UNKNOWN` と reason を実記録し、checker が未知の型を拒む。これは class change なので再 gate。
- 自動 retry はしない。STOP shard は同一 class/source/range の明示再送だけを許し、旧 receipt を保存する。

## 6. join の独立性

`join_checker.py` v2 は GAP helper、`candidate_key_lib.g`、wrapper を import しない。manifest の radix/width/m-list だけから flat-index と semantic tuple を独立再導出し、Lane-P expansion も独立再導出する。range の exact cover、entry の range 所属、重複/欠落、pcgs/endian、receipt、source/class/digest、`driver_done`、結果三値を fail-closed に検査する。

人工 15 fixture は pair/P の正常完全分割、shard/entry 並べ替え、欠 shard、欠 key、重複、overlap、pcgs/endian、range 外 entry、receipt 欠欄、driver 未完、m 誤り、指数桁の共通 permutation、P expansion 誤りを含む。2026-08-05 の Python 実走は 15/15 期待一致、正常と reorder の canonical hash も一致した。

これとは別に、class/workflow/cert/receipt/cap の binding は candidate 非接触の pure synthetic **71 fixture**（positive 11、tamper-negative 60）で検査し、全期待一致を class manifest に receipt 束縛する。class authorization 二 flag、runtime PCGS の abelian-$D$/ambient/source/action/bridge、S/V/P record 算術と verdict consistency、pre-shard receipt、三 lane cap 合成の改竄を含む。この行列は binding 実装だけを検査し、数学候補の較正ではない。

## 7. exposure / negative result

shard log は per-candidate verdict を job summary へ書かず cert artifact にだけ置く。collect 前の部分分布から IF-FIRST を更新しない。全 PASS/FAIL/UNKNOWN record、STOP receipt、再送前 receipt を保持し、FAIL/UNKNOWN を削除・再試行で丸めない。join 後の claim grade は別の Sol gate であり、本 class は定理・非存在・verified を自動主張しない。

## 8. preflight 状態（正直な停止札）

既存 CF/CONV-P 較正 GHA receipt (`search/certs/hsp7_cf_calib_20260805.json`) と、task 106 の外部代走 commit `849a196` による旧 registered wrapper S=13/V=13/P=8/P5 PASS は歴史的校正として保持する。しかし wrapper/schema/PCGS material が v3 へ変わった後の class を、それら旧 source の receipt だけで閉じない。

最初の ordered-PCGS v2 代走は S/V/P の上流 group/action gate を通過後、15 pair 行に非零を要求した誤った guard で STOP した。これは $D$ の可換性と矛盾する実装 bug で、失敗 aggregate は記録として不変。全15零行と ambient/source/action anchor へ直した v3 では BASIS_ONLY material/fingerprint は三 lane とも得られたが、条件分岐内の top-level 専用 `QUIT;` が parse STOP となり REGISTERED cert は 0。本 v3 FAIL も不変記録とする。

v4 はその三箇所だけを callable `QuitGap(0);` へ直し、出力を新規 `...pcgs_v4_20260806.json` 群へ送った。superseding source commit `a9a653e9a82f4dd93ca9eabec085a03af931b26e` について live/`git show` 22/22 byte 一致を通過後、外部 GAP 4.16 代走で BASIS_ONLY と REGISTERED は三 lane とも exit 0。S=13/V=13/P=8、P5=5、比較8項目は全 true、candidate-universe contact は 0 である。runtime fingerprint は S/P/core が `ff2e40c93bf3b547f34dabb0ab7ee6ea1fa2e46dd67bcca43c59fec5158726d3`、V（S→V bridge 込み）が `eaf54f528795c7831ab4a1b52d4c5e7578f0e93633c2332bfd9428b4b0503889`。

main/production shard cert は意図どおり 0 本であり、**class freeze の前提ではない**。これを前提にすると class 認可前に main run を要求する循環になる。v4 current-source receipt が PASS したので実装側 blocker は閉じ、class draft は `READY_FOR_SOL_FREEZE_REVIEW` へ進む。ただし authorization 四 flag は false のままで、Freeze/本走は Sol と工房の別裁定を要する。

## 9. 再 gate 条件

predicate/wrapper/conversion/schema/checker/source-map/PCGS artifact、semantic key、exact universe/range、shard、timeout/STOP/UNKNOWN、exposure/retention/cap のいずれかが変われば新 class ID を要する。S9、封印隣接量、登録外候補、主走は本書から自動発火しない。
