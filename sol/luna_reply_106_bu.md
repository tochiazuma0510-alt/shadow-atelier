# Luna 返信 106-BU — BOTTOM-UP freeze blocker 修理束

**実装判定: COMPLETE / AUTHORIZATION APPLIED。Sol 指定の opaque freeze ID `W6-BU-FREEZE2-EXACT17-F106` を物理束へ反映した。S1--S3.5 は将来の workshop-only dispatch に限り eligible、S3.6--S9 は LOCKED。今回いずれの stage も実行していない。**

## 0. 実行境界

- 実行したもの: 既存 17-row census の構造欄読取、versioned 文書作成、schema/manifest/checker/登録 fixture の静的較正、Sol 指定 authorization の反映と再 self-test。
- 実行していないもの: S1--S3.5、S3.6 以降、S9、探索、候補生成、kill、EMPTY、`Im R`、`d_N`、封印量への接触。
- git commit/push、workflow dispatch、credential 読取は行っていない。

## 1. versioned design correction

新規 `docs/notes/w6_bottomup_design_v4_1_addendum.md` を作成した。旧 v4 は不改変。

FREEZE-2 の規範を次の連言へ一意化した。

~~~text
layer = V-cen/S3-inflated
p=2: dim in {2,3,4}
p=3: dim = 2
window_order <= 8000
~~~

exact denominator は既存 census の `/rows` にある 17 `module_id`、stratum は `3+3+6+5=17`。p=2 dim0/1 と p=3 dim0/1/3/4 は cap から推論せず `DIMENSION_OUT_OF_SCOPE/STOP`、許容 dimension の cap 超過は `ORDER_CAP_EXCEEDED/STOP` とした。p=3 dim3/4 の supplemental 28 行は分母に加えない。

さらに `traversed_count`、`accepted_count`、`rejected_count` を別欄にし、

~~~text
traversed_count = accepted_count + rejected_count
~~~

を必須化した。各 traversal は unique id、disposition、source tag を持つ。H1 共役類での lift 潰しを traversal 単位として使うことは禁止した。

## 2. IF-FIRST M-ISO-8 erratum

新規 `docs/notes/iso_r3r4_iffirst_freeze_v1_2_erratum.md` を作成した。旧 IF-FIRST は不改変。

正しい機構を次で固定した。

| 経路 | settled | verdict |
|---|---:|---|
| real | 12/13、witness detail=false | `UNKNOWN(NONSHADOW_IN_DATUM)` |
| M-ISO-8 mutant | 13/13、同じ witness detail=true | `UNKNOWN(NONSHADOW_IN_DATUM)` |

従って verdict は不感であり、M-ISO-8 の kill は **detail-element comparison のみ**。`mutant TRUE != real UNKNOWN`、verdict mismatch、真の `isolated=FALSE` witness という旧読みに対して `MISO8_SEMANTICS_STALE/STOP` を割り当てた。

また、この erratum は過去の再走後の文書なので、欠けていた IF-FIRST の事前性を遡及的に作るものではない、と明記した。

## 3. schema / manifest / source-map の物理化

次を新規作成した。

| artifact | 内容 |
|---|---|
| `search/certs/w6_bu_firing_cert_schema_v1.json` | JSON Schema draft 2020-12。exact p-specific dimensions、cap、17 行、source-map、別 count、M-ISO-8 snapshot、UNKNOWN/STOP、claim 禁止を型にした |
| `search/certs/w6_bu_firing_gate_manifest_v1.json` | freeze authority、exact universe、17 row IDs/order、stratum、source/projection digest、stop/unknown contract、M-ISO-8、claim contract、artifact digest を束縛 |
| `search/probe/w6_bu_s0/check_firing_gate_v1.py` | source から 17 行を再導出し、digest/order/tuple/source-map/count witness/claim を fail-closed 検査 |
| `search/probe/w6_bu_s0/firing_gate_fixtures_v1/` | positive 1 + mutant 14 の物理 fixture |
| `search/certs/w6_bu_firing_gate_fixture_receipt_v1.json` | self-test の固定 receipt |

source-map は次を二重に束縛する。

1. source 全体: `search/certs/h2_census_s4_20260805.json`、SHA-256 `4b8673209d55c46fe1bc01a1e2736df03f296cd7d775df6da98f8f582df73b30`。
2. `/rows` の `(module_id,p,dim,s3_inflated,window_order)` canonical projection: SHA-256 `30a427ea638d8e954056eb3fb71c26a8f3691b3444e23f9f550a79f91f527614`。

checker は source の各 `rows[i]` を cert の `/rows/i` と `FIRING_UNIVERSE_SELECTION` tag へ再構成する。欠落、重複、順序変更、tuple 改変、digest 不一致はすべて STOP。

manifest の authorization は最初に次の pre-authorization 状態で較正した。

~~~json
{"freeze_id": null, "stage_unlock": false}
~~~

このときの manifest SHA-256 は `33554a07f019167ee193dfe09d5c3f67a23d39f70b0c992d91c1aafb8b262726`。これを消さず audit input として保持した上で、Sol 指定により最終 authorization を次へ更新した。

~~~json
{
  "freeze_id": "W6-BU-FREEZE2-EXACT17-F106",
  "stage_unlock": true,
  "authority": "sol/sol_reply_106_math33.md F106-4",
  "pre_authorization_manifest_sha256": "33554a07f019167ee193dfe09d5c3f67a23d39f70b0c992d91c1aafb8b262726",
  "dispatch_scope": "future workshop-only dispatch; no execution in task 106"
}
~~~

checker はこの opaque ID、authority、pre-authorization hash、scope、S3.6--S9 lock set を exact equality で検査する。いずれかの改変は `AUTHORIZATION_BINDING_MISMATCH/STOP`。これは本便中の探索開始を意味しない。

## 4. fixture / mutant-negative 検収

再現コマンド:

~~~powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python search/probe/w6_bu_s0/check_firing_gate_v1.py --self-test
~~~

結果: **exit 0、positive 1/1 PASS、mutant 14/14 が指定 STOP、全 15/15 expected match**。

authorization の fail-closed 追加照合では、manifest をメモリ内だけで `freeze_id`、`authority`、`stage_unlock`、`dispatch_scope`、`S3.6` lock の各一箇所を変えた 5 mutant がすべて `AUTHORIZATION_BINDING_MISMATCH/STOP` になった（候補非接触、ファイル非変更）。

| fixture | actual |
|---|---|
| positive exact-17 | PASS |
| p=2 dim0 / dim1 | 各 `DIMENSION_OUT_OF_SCOPE/STOP` |
| p=3 dim0 / dim1 / dim3 / dim4 | 各 `DIMENSION_OUT_OF_SCOPE/STOP` |
| order=8001 | `ORDER_CAP_EXCEEDED/STOP` |
| row missing | `ROWSET_MISSING/STOP` |
| row duplicate | `DUPLICATE_MODULE_ID/STOP` |
| source-map missing | `SOURCE_MAP_MISSING/STOP` |
| accepted count 欄欠落 | `COUNT_ACCOUNTING_MISMATCH/STOP` |
| count witness disposition 不整合 | `COUNT_WITNESS_MISMATCH/STOP` |
| 旧 M-ISO-8 verdict-mismatch 読み | `MISO8_SEMANTICS_STALE/STOP` |
| `isolated_verdict=FALSE` | `CLAIM_OVERREACH/STOP` |

positive の `traversed=19 / accepted=17 / rejected=2` は count anti-alias 用の**合成 schema fixture**であり、探索測定値ではない。19 個すべてに traversal witness があり、17 ACCEPTED + 2 REJECTED を checker が再集計する。

個別 exit-code 検収:

- positive `--check`: exit **0**。
- old M-ISO-8 mutant `--check`: exit **2**、`MISO8_SEMANTICS_STALE/STOP`。
- Python AST parse と schema/manifest/receipt/15 fixture の JSON parse: `AST_OK JSON_OK json_files=18`。

## 5. STOP / UNKNOWN / claim 境界

- artifact/schema/manifest/source/source-map/rowset/count の不整合は STOP。
- 未実行または数学的前件未成立は `UNKNOWN(reason)`。UNKNOWN を FALSE に写さない。
- 本 schema では `isolated_verdict` は `UNKNOWN` のみ。kill、candidate found、EMPTY は boolean false のみ。
- coverage を書ける場合も exact 17-row firing universe 内に限定し、`W \ W_adm` や supplemental inventory へ拡張しない。
- ISO route 2 grade、S3.6 以降、W-5 isolated は本束では昇格しない。

## 6. SHA-256

| path | SHA-256 |
|---|---|
| `docs/notes/w6_bottomup_design_v4_1_addendum.md` | `1d55d01640fffc9649e26589e397e5dfc9aa65518b3e37a88af27c70c5188578` |
| `docs/notes/iso_r3r4_iffirst_freeze_v1_2_erratum.md` | `a684f79dd7924fd5d346dfbfdf02336cbe1cd2942b0059da99b326d07491f9fa` |
| `search/certs/w6_bu_firing_cert_schema_v1.json` | `2f681fdb590e93fbc03132cde6cdb261a6664e7afc2a35e96d7a5deb2facc8eb` |
| pre-authorization manifest（audit input） | `33554a07f019167ee193dfe09d5c3f67a23d39f70b0c992d91c1aafb8b262726` |
| `search/certs/w6_bu_firing_gate_manifest_v1.json`（authorized final） | `2818c0aceb2948750df84f3df5c6a63df12c477bf73681690cb06e7c00a82376` |
| `search/probe/w6_bu_s0/check_firing_gate_v1.py` | `ef44d52c0eeda48a3fd5290b1185bedc39a30121006be9b91051d50ec27246b4` |
| `search/certs/w6_bu_firing_gate_fixture_receipt_v1.json` | `36dcfea73ae5a078d52592455d86f0ed38089fddf3a6990d94b81b93cb5de26f` |
| positive fixture | `9299c3c4e8a17177334d7eae847a6a3576d0b06ba95521ae45ed3b942e6acb04` |
| fixture set（sorted `path sha256\n` 15 行の SHA-256） | `d6644b65a2bc5aeee3a0280a86bb979a0fe6a1b2c8572841b0b91536d1cd6511` |

## 7. 変更一覧・worktree 検収

新規ファイルだけを作成し、既存 artifact は変更していない。

- docs 2
- schema/manifest/receipt 3
- checker 1
- fixture 15
- 本返信 1

対象 path の trailing-whitespace scan は 0 件、対象限定 `git diff --check -- <BU paths>` は exit 0。global `git diff --check` は本委嘱外の既存変更 `search/probe/wac_v1/scan_out.txt:11-15` の trailing whitespace で exit 2 だったため、そのファイルには触れていない。

## 8. 最終状態

Sol の F106-4 authorization を物理化した後の状態は次のとおり。

~~~text
implementation bundle: COMPLETE
FREEZE-2: FROZEN
freeze ID: W6-BU-FREEZE2-EXACT17-F106
S1--S3.5: ELIGIBLE FOR FUTURE WORKSHOP-ONLY DISPATCH (NOT RUN HERE)
S3.6--S9: LOCKED
~~~
