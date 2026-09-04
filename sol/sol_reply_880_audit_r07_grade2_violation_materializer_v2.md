# Sol Task 880 — grade-two violation materializer v2 狭域敵対監査

## 裁定

**FAIL**。Task869 の F2（actor direction）は修理済みである。一方、F1 は実演 fixture の自己封印境界から production Task554/P1 authority へ昇格しておらず、F3 は accepted v15 の result bytes を要求しても対応する scalar launch を認証しておらず、F4 は current-S の挿入順 pivot transcript を完全 replay していない。したがって一違反 J2 materialization/pivot primitive は受理しない。

## source receipts

| source | bytes | LF | CR | SHA-256 |
|---|---:|---:|---:|---|
| `search/d972_r07_grade2_violation_materializer_v1.py` | 98,247 | 1,677 | 0 | `d76bbc95cb58496856dfa9ea99bebf7e63b477ed168dab1b6f69d95644a9fc1d` |
| `search/check_d972_r07_grade2_violation_materializer_v1.py` | 87,135 | 1,073 | 0 | `875ca7b385e45117bad190813687bfdda4afaa31bbbb655a68b031cd5000c409` |
| `search/d972_r07_grade2_violation_materializer_v2.py` | 177,821 | 3,015 | 0 | `b68133f7021104baa2232f043c0216ead9227c9620139550b7a4426cd2173bef` |
| `search/check_d972_r07_grade2_violation_materializer_v2.py` | 179,767 | 2,559 | 0 | `f5647940ae4dc6b1c3803dd7c46e49802abb2ea72450a6744d67bfb487258394` |
| `search/d972_r07_scalar_degree_pairing_owner_v15.py` | 126,565 | 2,286 | 0 | `76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632` |
| `search/check_d972_r07_scalar_degree_pairing_owner_v15.py` | 141,770 | 2,500 | 0 | `8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662` |

用いた receipt 手順は、各 path について `[IO.File]::ReadAllBytes(...)`、`[Security.Cryptography.SHA256]::HashData(...)`、byte 列中の `0x0a` / `0x0d` の計数である。構文確認は repository 外 pycache で次を実行し、exit 0 を得た。

```powershell
$env:PYTHONPYCACHEPREFIX = Join-Path $env:TEMP 'shadow-atelier-task880-pycache'
python -m py_compile search/d972_r07_grade2_violation_materializer_v2.py search/check_d972_r07_grade2_violation_materializer_v2.py
```

## gate table

| gate | result | 狭域根拠 |
|---|---|---|
| F1 lower/projector reality | **FAIL** | 全 four-block / 96,776-side / 145,152-trit 演算自体は実行するが、accepted public base は固定 16-row・rank `[2,2,2,2]` fixture のみであり、その入力 bytes は production Task554/P1 authority から再構成されない。 |
| F2 actor direction | **PASS** | stored actor tuple は非反転、primal callable traversal は `reversed(actors)`。独立 control の correct SHA、wrong SHA、差分 1,501 を固定し、material row/digest 照合により scalar collision 下でも wrong row を拒否する。 |
| F3 scalar-parent join | **FAIL** | v15 result の exact key/envelope と raw-chain/children/DualPivot digest は照合するが、`launch_sha256` を authenticated v15 launch に結合しない。nonempty prior-pivot replay も欠ける。 |
| F4 current-S authority | **FAIL** | file-backed payload、rank/generation/HEAD、prefix byte comparison、raw/scaled lambda、durable payload 後の単一 HEAD switch はあるが、pivot transcript の raw-origin reduction/normalization replay と externally authenticated current-S provider がない。さらに lead の数値単調増加を要求している。 |
| retained: independent helpers | PASS | producer/checker 間に sibling import はない。 |
| retained: Task712 tables/transposes | PASS | accepted manifest/envelope と forward/adjoint transpose を pin/check する。 |
| retained: raw-q chain + four children | PASS | exact bytes/digests と四 child binding を check する。 |
| retained: forward B / both pairings | PASS | correct reverse action と B、および raw/remainder/scaled physical lambda equations を check する。 |
| retained: packed rows reopen | PASS | 36,288/48,384-trit packed rows を checker が再読する。 |
| retained: no fixture-only accepted terminal | **FAIL** | ordinary public path 自体が固定 fixture universe を要求し、その fixture から terminal を構成できる。 |

## F1 — production authority ではない

Producer の `_fixture_universe` / `validate_base`（約 L425–438, L539–627）と checker の legacy base validation（約 L289–309, L1141–1170）は `fixture=True`、P1 16 rows、旧新 rank `[2,2,2,2]`、Task554 block rank 2 を必須にする。したがって commissioned public boundary は production 8,059-row Task554/P1 adapter ではなく、固定 fixture-only boundary である。

`_lower_reconstruct`（producer 約 L2181–2261、checker 約 L1616–1683）は二つの 96,776-coordinate arrays を実際に読んで全四 character block の reduction/resolution を検査しており、内部に semantic-zero 代用品は見当たらない。しかし `build_lower_parent`（producer 約 L2563–2604）が作れる caller-defined repeated-template fixture とその self-seal が origin になっているため、この実演の算術的非自明性は Task554/P1 provenance を与えない。coherently resealed mutation に対する semantic check が存在しても、未認証の universe 内だけで閉じている。

最小修理は、固定 fixture parser を exact accepted production Task554/P1 adapter に置換し、8,059 rows / production segments と provider receipts を pin すること、さらに lower-origin と P1 truncation rows をその authenticated origins/instructions から再構成すること（または別途 accepted provider を exact receipt で結ぶこと）である。現存する four-block replay は保持する。

## F2 — actor direction は修理済み

Producer 約 L2319–2329 と checker 約 L1826–1849 は stored `actors` を保持し、primal map だけを reverse traversal で適用する。control（producer 約 L2264–2290、checker 約 L1693–1713）は `(1,2)` について次を固定する。

- correct row SHA-256: `63a8f0c01693088050ba4751f1898da6bd83663e42e4383dfb907a110f4d8bad`
- wrong-order SHA-256: `42275d9aff5f3c678f6a07a02e13a4da81f8883fe22573bc9686eec6937e26e6`
- differing coordinates: `1501`

Task869 の独立再現値とも一致し、checker は scalar のみでなく complete material row/digest を照合する。F2 の追加修理は不要であり、この実装をそのまま retained とする。

## F3 — v15-shaped bytes と v15 authority は同一でない

`validate_scalar_parent`（producer 約 L1961–2014、checker 約 L1716–1775）は accepted v15 result の exact key set、raw-chain final state、DualPivot、Violation、Task712/P1/relation digests を要求し、named origin まで prefix を再計算する。これは private miniature scalar dialect を排した点では前進である。

しかし `launch_sha256` は key として存在するだけで、authenticated scalar launch の receipt/path と比較されない。fixture builder は v15-shaped result に `launch_sha256 = "0" * 64` を入れて自己封印できる（producer 約 L2853–2875、checker fixture 約 L2420–2438）。accepted v15 owner は actual scalar launch の SHA を result に出し、accepted checker がそれを照合するが、materializer はその launch を join しない。

また materializer 内の DualPivot validation（producer 約 L2115–2178、checker 約 L1542–1606）は nonempty `prior_pivot_coefficients` の場合、ID/lead の形しか見ず、prior dual state から remainder、normalization、next head を replay しない。このため independently resealed pivot/remainder mutation に対する accepted-parent authority がない。

`physical_provider="NOT_READY:authenticated_physical_provider"` と `current_s_provider="NOT_READY:authenticated_current_S_provider"` は accepted scalar-only v15 の正しい literal fields である。ただし Task877/878 が明記した scope-exclusion（provider/materializer は未受理）の sentinel であり、provider authority の肯定証明ではない。これを inert exact-envelope field として照合することは可だが、別供給の current-S/physical parent を正当化する用途には使えない。

最小修理は exact scalar-launch receipt/path を親に加え、accepted v15 checker を実行するか等価な launch-to-result join を行い、`launch_sha256`、prior dual state、nonempty DualPivot replay まで認証すること。NOT_READY fields は負の scope marker のまま扱い、physical/current-S provider は同じ generation/head/lambda に別途 join する。

## F4 — 挿入順 transcript を数値順に置換している

Task535/v536 の current-S 契約は insertion-order normalized rows であり、各新行についてそれ以前の pivot coordinates が 0、lead は unique であればよい。pivot coordinates が数値的に増加する必要はない。ところが v2 は transcript rows と新 pivot に `lead > previous_lead` / `lead > last lead` を要求する（producer 約 L1897, L2423、checker 約 L1335, L1915）。これは有効な insertion-order state を拒絶する semantic broadening である。

さらに separator validation（producer 約 L1889–1941、checker 約 L1323–1385）は各 stored row の非零性と declared lead および metadata/digests を調べるだけで、leading scalar `1`、先行 pivot 座標の 0、各 `raw_origin` と `prior_pivot_coefficients` からの reduction/normalization/scale replay を検査しない。よって duplicate lead rejection や prefix byte equality があっても general nonempty transcript の意味論を認証できない。current-S parent も caller-described/self-sealed で、NOT_READY sentinel はこの欠落を埋めない。

最小修理は numeric monotonicity を除去し、挿入順で unique leads、leading coefficient 1、全 earlier-pivot coordinates 0 を検査し、各 record を authenticated raw origin・prior coefficients・normalization scale から replay すること。そのうえで stable current-S provider/HEAD を exact receipt で pin し、既存の byte-prefix comparison と durable payloads 後の単一 atomic HEAD publication を保持する。

以上は Task869 の F1–F4 と retained gates に限定した裁定であり、production Violation の存在、grade two membership、A0/common/cofinal lift/fake/Ihara のいずれも主張しない。

VERDICT=FAIL
IMPLEMENTATION_ACCEPTED=no
J2_MATERIALIZATION/PIVOT_PRIMITIVE_ACCEPTED=no
ACTUAL_VIOLATION_MATERIALIZED=false
ACTUAL_PHYSICAL_PIVOT_INSERTED=false
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
