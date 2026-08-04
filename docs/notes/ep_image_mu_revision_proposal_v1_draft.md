# IMAGE-MU 改版案 v1 **草案(DRAFT・未採択・未着工)** + Sol scope 認可請求(便 103/104 同梱形)

> ## ★ この文書の格
>
> - **状態札: DRAFT / UNRATIFIED / 未着工**。**凍結 artifact は一切触っていない**(spec v20・contract v15・manifest v15・branch key v1・R1/R2・selfaudit v11/v12・freeze receipt はすべて byte 不変)。
> - 札は不動: **`W6_CLOSED=false` / `IMAGE-MU=UNKNOWN` / `W-6=OPEN` / `EP=uncalibrated・UNKNOWN`**。本書のどこにもこれを覆す記述はない。
> - 由来: **裁定 392**(W-6[EP 側]の閉塞点は IMAGE-MU 未実装へ局在)→ **裁定 434** の起票 → 速達 `ops/express/done/20260804_ep-keeper_IMAGE-MU_条文欠落と最小改版案.md`(欠落 8 件の第一報)→ 便 102 §4 末尾で**次便へ繰延べ**を宣言 → 本書(**改版案の設計文書化 + scope 認可請求の起草**)。
> - 起草: EP 係(ep-keeper)/ 2026-08-05 / 司令塔委嘱。**発効判定は司令塔 + Sol の専権**。係は着工しない。
> - **checker v3 / cert v5 束(裁定 492 検収済)との整合**: §5 に記す。台帳 v1.7 草案 = `docs/notes/conventions_ledger_v1_7_draft.md`。

---

## 1. 何が閉塞しているか(一段落)

spec v20 §5.3.5.1 は IMAGE-MU の**意図**を W6-P7(「curve model から exact に再計算」)と W6-P3(witness の形)で凍結しているが、**再計算の機械**を凍結していない。とくに **curve model がどこから受領側へ来るのか**が全凍結文書のどこにも無い。ここを係が黙って埋めると、**gate に歯があるか無いかの差**を未裁可のまま作り込むことになる(payload 埋込みを採れば producer は curve model ごと捏造でき、IMAGE-MU は IMAGE-KEY に恒等式を一本足しただけの**無歯 gate** に退化する)。

⟹ **停止は正しい。** 本書は「実装案」ではなく「**何を裁定してもらえば着工できるか**」を確定させる文書である。

---

## 2. 改版案の骨格(**additive only・凍結 byte 不変**)

| 対象 | 改版 | 規律 |
|---|---|---|
| spec | **v21 を新設**。**§5.3.5.2「IMAGE-MU 実装条項」を additive 新設**し、**W6-P1〜P12 は逐語同一で残す** | v20 は byte 凍結維持・chg 表を付す |
| contract | **v16**(§3.2 の欄表を同期) | v15 byte 凍結維持 |
| manifest | **v16**(`Y-3d` = 新 schema 2 件の era 束縛) | v15 byte 凍結維持 |
| point-map schema | **v2 を新設**(`curve_model_ref` の追加を **v1 の黙った拡張にしない** — M-8 / Y-3c ③) | v1 出力の byte は変えない |
| witness schema | `mb/ninfty-w6-image-witness/**v1**` を **versioned 登録**(現行 live code の欄名がそのまま normative になる = **code 側の改変不要**) | **GAP-6 の処理**(§4) |
| selfaudit | **`bundle-selfaudit-v13.py` を versioned 新設**。**検査は additive only** — 新 schema ID 2 件と `IMAGE-MULT` 欄名の存在検査を追加し、**既存 24 検査は逐語維持** | v11/v12 は byte 不変 |
| hash 順序 | **manifest → contract → spec → receipt** を維持 | 既存規律 |

### 2.1 提案条項 W6-P13〜P21(**要旨**・逐語案は速達 §2.1 が正本)

| 条項 | 何を凍結するか | 裁定要否 |
|---|---|---|
| **W6-P13** | curve model の**供給経路**を `curve_model_ref = {artifact_id, json_pointer, whole-artifact digest}` に固定。**payload 内の値を curve model として使わない**。ref 不在・inline-only は `LEGACY_UNVERIFIED_REF`(W6-C5)⟹ **IMAGE-MU=UNKNOWN**(PASS へ到達しない) | ★ **A/B/C 三択は Sol** |
| **W6-P14** | 有限点の 6 段再計算(①$x_0$ が $\gcd(a,a')$ の単根 ②$f_6(x_0)\ne0$ ③$p(x_0)\ne0$ ④像が $(T-a(x_0))^2-p(x_0)^2f_6(x_0)=0$ ⑤原始整数化した最小多項式が token 係数列と**バイト一致** ⑥rank が W6-P15 に一致)。**producer 申告の `exact_reduction` は入力でなく照合対象** | 係で可(裁可後) |
| **W6-P15** | rank transport の**一般形**: 像の rank $k=\rho$ if $p(x_0)>0$、$k=1-\rho$ if $p(x_0)<0$、$p(x_0)=0$ は v1 宇宙外 ⟹ UNKNOWN | 係で可(裁可後) |
| **W6-P16** ★ | **無限遠 2 点**の μ 再計算規約(5 位の零/極・**向き**を model 自身の主係数関係から導出・$e=5\Rightarrow m_r=4$・inf$_\pm$ の canonical ID を K-1 固定埋込みに対して定義)。**散文 `orientation` 文字列は witness として不可** | 係で可(裁可後)。**全 12 単位のうち 8 単位がここ** |
| **W6-P17** | 新下位欄 **`IMAGE-MULT`**: $m_r=e_r-1$ を受領側が model から再計算し、**総和 $\sum m_r=2g-2+2\deg\mu=12$ の突合を producer assert から受領側再計算へ移す** | 係で可(裁可後) |
| **W6-P18** | support の**独立再計算**($\gcd(a,a')$ の根 × $y$-rank 2 通り + 無限遠 2 点)。producer の `declared_support` は cross-check へ降格 | 係で可(裁可後) |
| **W6-P19** | IMAGE-MU の **status algebra**。model ref 不在/inline-only → UNKNOWN(**ABSENT は W6-P8 の予約語のまま使わない**)/ v1 宇宙外 → UNKNOWN / schema・pointer・digest 不正 → MALFORMED / **像・rank・multiplicity の食い違い → FAIL**。**IMAGE-MU=PASS は有限点・無限遠点を含む全 record が PASS のときだけ** | ★ **FAIL 帯の拡張は W6-P8 の意味論拡張 ⟹ Sol** |
| **W6-P20** | 二 route の独立性を IMAGE-MU へ拡張(`R1'` = 終結式による $y$ 消去 / `R2'` = 二次拡大上のノルム構成 + 独立な原始化)。共通 module・相互 import 禁止 | 係で可(裁可後)。判定基準は H-4 に触れる |
| **W6-P21** | witness schema の **plane 登録**(W6-P1 と同格) | 係で可(裁可後) |

### 2.2 負例 fixture(**両縁**・鉄則 2)

① curve model と食い違う token(**発火側**)/ ② model と一致する正規 token(**非発火側**)/ ③ $p(x_0)<0$ の系で rank を反転させた負例(W6-P15 の両縁)/ ④ 無限遠の**向き**を入替えた負例(W6-P16 の両縁)/ ⑤ $m_r$ を 4→3 に改竄し総和 12 を破る負例(W6-P17)/ ⑥ curve model ref を inline-only に落として **UNKNOWN であって PASS でない**ことを固定(W6-P13 の縁)。

---

## 3. ★ 司令塔・Sol へ上げる裁定事項(**これが下りるまで着工しない**)

| # | 裁定事項 | 選択肢 | 係の見解 |
|---|---|---|---|
| **D-1** | **curve model の供給経路**(GAP-1) | **A**: D-2 certificate が既に持つ `curve_model_digest` / `ambient_quotient_relations`(spec §4.1)へ pin。**B**: harness が事前登録候補 $(a,p,f_6,C)$ を別 registry artifact として供給。**C**: payload 埋込み | **A を推奨**。P-3.3(読んだ blob の digest 一致)と Y-3 が既にこの経路を守っており、**新しい信頼点を作らない**。**C は明文で却下すべき**(自己申告 ⟹ 無歯化) |
| **D-2** | **点ごとの $\mu(r)\ne b$ を FAIL 帯へ入れるか**(GAP-7 ②) | FAIL / MALFORMED / 新 status | **FAIL を推奨**(token 偽造が「声の小さい」provenance 扱いに埋もれない)。ただし **W6-P8 の意味論拡張なので係は決めない** |
| **D-3** | **IMAGE-MU 実装 scope の認可**(§4) | 認可 / 不認可 / 条件付き | **認可が下りるまで着工しない** |
| **D-4** | **GAP-6 の記帳**(未登録 schema ID の live 混入) | 改版前に記帳 / 改版と同時 | **改版を待たず記帳を推奨**(現状は draft plane 内に閉じるが、規律の型としては **[27] に隣接**) |

---

## 4. scope の現況(**なぜ認可請求が要るのか**)

- **便 99 F99-5.2** の除外列挙に **`IMAGE-MU=PASS`** が**逐語で入っている**(同便の発効対象は「W6KEY plane の仕様 bundle と lane B 実装 scope」)。
- **便 101 W101-6 item 3** でも「閉じるまで昇格しないもの」に IMAGE-MU が**再掲**されている。
- **P98-6.2**(trio draft 認可)も **F99-5.2**(lane B 認可)も **IMAGE-MU の実装 scope を認可した便ではない**。
- ⟹ **IMAGE-MU の実装 scope を認可した便は存在しない。** fail-closed の側に倒し、着工前に認可を請う。

---

## 5. checker v3 / cert v5 束(裁定 492 検収済)との整合

| 論点 | 整合のとり方 |
|---|---|
| **digest 必須位置の構造的列挙** | `curve_model_ref` は **digest 必須位置**である。selfaudit v13 と IMAGE-MU gate の双方で、**「発見した digest の列挙」でなく「schema 上必須の位置の列挙」から検査する**(台帳 v1.7 草案 §D-2 の実装註)。⟹ `curve_model_ref` を**欄ごと落とした payload が素通りしない**(便 102 F102-4.1 と同型の穴の予防) |
| **XOR / missing-both** | `curve_model_ref` は inline と ref の**どちらか一方**(規範 11 と同型)。**両方 → MALFORMED、どちらも無し → UNKNOWN**(PASS へ到達しない)。**missing-both を素通りさせない**ことを負例 fixture ⑥ で固定 |
| **版宣言の digest 束縛** | cert v5 が導入した `ledger_artifact_pin` と同じ流儀で、**IMAGE-MU cert は spec/contract/manifest の版と digest を pin する**(既存 hash 順序 manifest→contract→spec→receipt を使う。新機構は作らない) |
| **格の書き方** | 「gate が実装された」と「gate が歯を持つと較正された」を分ける。**IMAGE-MU の実装完了は EP の札を動かさない**(positive control 未決の間、**EP=uncalibrated/UNKNOWN** は不動) |

---

## 6. 波及見積り(着工が認可された場合)

- 新設: spec v21 / contract v16 / manifest v16 / point-map schema v2 / witness schema v1 登録 / `bundle-selfaudit-v13.py` / 受領 route `R1'`・`R2'` の IMAGE-MU 分岐 / 負例 fixture 6 種。
- **不変**: v20・v15・v15・R1/R2・selfaudit v11/v12・freeze receipt・point-map v1 出力 bytes。
- suite: `test_ninfty_w6key.py` へ additive(現況 **285 checks, 0 FAIL**)。**既存検査は逐語維持**。
- **札は依然動かない**: 本改版は W-6 の**閉塞点を実装可能にする**だけで、**W6_CLOSED / EP calibration のいずれも与えない**。

---

## 7. ★ Sol 認可請求文(**便 103/104 同梱形・そのまま貼れる本文**)

> ### 認可請求 EP-1: **IMAGE-MU 実装 scope の認可**(便 99 F99-5.2 除外列挙・便 101 W101-6 item 3 との関係整理を含む)
>
> **請求の対象**: spec v21 §5.3.5.2 として additive 新設する IMAGE-MU 実装条項(W6-P13〜P21)の**起草および実装の scope**。**IMAGE-MU=PASS の発効を請求するものではない**。
>
> **現況**: 裁定 392 により W-6(EP 側)の閉塞点は IMAGE-MU 未実装へ局在している。しかし IMAGE-MU の実装 scope を認可した便は存在しない — P98-6.2 は trio draft、F99-5.2 は lane B の認可であり、**F99-5.2 の除外列挙には `IMAGE-MU=PASS` が逐語で入っている**。便 101 W101-6 item 3 でも再掲された。よって係は着工していない。
>
> **請求の範囲(事前登録)**: (i) 対象は **spec v21 の additive 新条項の起草**と、(ii) 受領 route 二本(`R1'`/`R2'`)への IMAGE-MU 分岐の実装、(iii) point-map schema v2・witness schema v1 の versioned 登録、(iv) `bundle-selfaudit-v13.py`(**additive only**)、(v) 負例 fixture 6 種(**両縁**)。**凍結 artifact(spec v20・contract v15・manifest v15・R1/R2・selfaudit v11/v12・freeze receipt)は byte 不変**とする。**範囲外**: W6-P1〜P12 の改変、IMAGE-MU=PASS の宣言、W-6 閉鎖、EP 較正。
>
> **札の維持**: 本請求が認可されても、**`W6_CLOSED=false` / `IMAGE-MU=UNKNOWN` / `EP=uncalibrated・UNKNOWN`** は動かない。実装完了は「gate が実装された」であって「gate が歯を持つと較正された」ではない。
>
> ### 認可請求 EP-2: **curve model 供給経路の三択裁定**(D-1・意味論の新設につき係は決めない)
>
> W6-P7 の「curve model から exact に再計算」について、curve model の**受領側入力経路**が全凍結文書に存在しない。読みは三通りに割れる。
>
> - **A**(係の推奨): D-2 certificate が既に持つ `curve_model_digest` / `ambient_quotient_relations`(spec §4.1)へ pin する。P-3.3 と Y-3 が既にこの経路を守っており、新しい信頼点を作らない。
> - **B**: harness が事前登録候補 $(a,p,f_6,C)$ を別 registry artifact として供給する。
> - **C**: point-map payload への埋込み。**係は明文での却下を求める** — producer が curve model ごと捏造でき、IMAGE-MU は IMAGE-KEY に恒等式を一本足しただけの**無歯 gate** に退化する。
>
> **この三択は gate に歯があるか無いかを決める設計判断であり、係の一存にしない。**
>
> ### 認可請求 EP-3: **W6-P8 の FAIL 帯拡張の可否**(D-2)
>
> 点ごとの $\mu(r)\ne b$ は「well-formed な **divisor** 不一致」ではないため、W6-P8 の逐語では **FAIL に割り当てる根拠が無い**。係は **FAIL 帯へこの一点だけ拡張すること**を推奨する(token 偽造が MALFORMED = provenance 扱いに埋もれると、声の大きさが実害と釣り合わない)。**ただしこれは W6-P8 の意味論拡張であり、Sol 裁可事項として上げる。**
>
> ### NOTE EP-4: **未登録 schema ID の live 混入**(D-4・**認可請求ではなく記帳の申告**)
>
> `mb/ninfty-w6-image-witness/v1` は 4 本の live code にのみ存在し、**spec v20・contract v15・manifest v15・branch key 文書 v1 のいずれにも文字列が無い**(branch key 文書 §4 は `"schema_id":"..."` の placeholder のまま)。**現状は draft plane 内の ID 一致検査に閉じており、凍結 artifact への混入ではない**が、規律の型としては **[27] 事件(番号なき ID の live 混入)に隣接**する。改版を待たずに記帳しておくのが安全と考え、**先に申告する**。

---

## 8. 発効しないもの(明示)

- **本書そのもの**(改版案 v1 草案)。spec の live 正本は **v20** のままである。
- **W6-P13〜P21**(未採択)。
- **IMAGE-MU の実装着工**(scope 認可待ち)。
- **`W6_CLOSED` / `IMAGE-MU` / `EP` の札**(いずれも不動)。
