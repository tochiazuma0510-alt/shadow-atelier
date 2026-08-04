# 速達: IMAGE-MU は spec v20 だけでは実装不可 — 欠落 8 件 + 最小改版案(draft)

- **宛先**: 司令塔
- **差出**: ep-keeper(EP 専任係)
- **緊急度**: 今日中(裁定 434 の起票に対する第一報)
- **判定**: **欠落あり(実装せず)**。凍結文書は一切触っていない。W6_CLOSED=false / EP=uncalibrated・UNKNOWN は不動。

---

## 0. 二つの独立した停止理由

**(A) 意味論の欠落**(本文 §1): spec v20 §5.3.5.1 は IMAGE-MU の**意図**を 1 条(W6-P7)と witness の形(W6-P3)で凍結しているが、**再計算の機械**を凍結していない。とくに「curve model **から**」の *curve model がどこから来るか* が全文書のどこにも無い。ここを係が埋めると、**gate に歯が有るか無いかの差**を未裁可のまま作り込むことになる。

**(B) 認可 scope の外**: 便99 F99-5.2 の除外列挙に **`IMAGE-MU=PASS`** が逐語で入っており(発効対象は「W6KEY plane の仕様 bundle と lane B 実装 scope」)、便101 W101-6 item 3 でも「閉じるまで昇格しないもの」に IMAGE-MU が再掲されている。**IMAGE-MU の実装 scope を認可した便は存在しない**(P98-6.2 = trio draft 認可、F99-5.2 = lane B 認可、いずれも別物)。fail-closed の側に倒し、着工前に司令塔判断を仰ぐ。

---

## 1. 欠落箇所(条文 ID つき)

| # | 条文 | 欠けているもの | なぜ実装を止めるか |
|---|---|---|---|
| **GAP-1** ★ | **W6-P7**(「curve model から exact に再計算」) | **curve model の受領側入力経路が未定義。** point-map schema `mb/ninfty-w6-point-map/v1`(branch key 文書 §4)に curve model 欄は無く、受領 route(`R1'`/`R2'`)にも供給口が無い。読みは 3 通りに割れる — (a) payload 埋込み、(b) registry-pinned な独立 artifact の ref、(c) harness が事前登録候補から供給 | **(a) を採ると IMAGE-MU は「witness の内部整合」に退化し、IMAGE-KEY に一本の恒等式を足しただけの無歯 gate になる**(producer は curve model ごと捏造できる)。歯の有無を決める設計判断であり、係の一存にしない |
| **GAP-2** ★ | **W6-P3 / W6-P4** | **無限遠 2 点の μ 再計算規約が無い。** W6-P3 の三段(fibre relation / μ=a(x₀)+p(x₀)y / 像の最小多項式)は**有限点専用**で、無限遠では意味を持たない。現 producer は `orientation: '(Or) div(mu)=5P_0-5P_inf, E-3 branch a5=+p2 => ...'` という**散文文字列**を出しているだけ | **全 12 単位のうち 8 単位(係数 4×2)が無限遠にある。**ここを素通しにすると W6-P4 が禁じた「有限点だけで宣言」の型を IMAGE 欄で再演する。inf_± の canonical ID(固定埋込み K-1 に対する定義)も未凍結 |
| **GAP-3** | **K-3 / W6-P7** | **rank transport 規約が一般形で凍結されていない。** 現 producer は `bSign = sign(p(x₀))·sign(y-rank)` を使うが、spec v20 の該当注記は「$p(x_0)$ は正の有理数なので rank は $y$-root rank と一致する」— **現 genuine fixture についての記述**であって規則ではない | 一般形が無いまま実装すると、gate が fixture 較正になる(=期待値のコード書込み・鉄則 5 違反)か、producer の符号を黙って信じるかの二択になる |
| **GAP-4** | **W6-C1 / W6-C4 / W6-P7** | **multiplicity $m_r$ の再計算が、どの欄の職掌でもない。** W6-C1 の述語は $\sum_{r\mapsto b} m_r = m_{\mathrm{Branch}}(b)$ だが、W6-C4 の「受領側が再集計」は **producer 申告の $m_r$ を足し直す**だけ。現 gate は $m_r$ を「正整数か」型検査するのみ。総和 12($\deg R_\mu = 2g-2+2\deg\mu$)の突合も **producer 側 assert**(`ninfty-w6-pointmap-lanea.mjs` 末尾)にしかない | **IMAGE-MU が語義どおり PASS しても、divisor の係数は producer 申告のまま**で W6-C1 は再計算されていない。closure の論証に穴が残る |
| **GAP-5** | **W6-P4 / COVERAGE** | **ramification support の独立再計算条項が無い。** COVERAGE は producer の `declared_support` に対する被覆を見るだけで、「その $r$ が本当に $\mu$ の分岐点か」は誰も検査しない | curve model が来るなら support も受領側が導ける。この条項が無いと IMAGE-MU だけ強化しても点の取捨は producer 任せ |
| **GAP-6** | **W6-P1 / M-8 / Y-3c** | **witness schema `mb/ninfty-w6-image-witness/v1` が凍結体系に未登録。** 4 本の live code(`ninfty-w6-key-gate-r1p.py` / `-r2p.py` / `-pointmap-lanea.mjs` / `-pointmap-laneb.py`)にのみ存在し、**spec v20・contract v15・manifest v15・branch key 文書 v1 のいずれにも文字列が無い**(branch key 文書 §4 は `"schema_id":"..."` の placeholder のまま) | IMAGE-MU は witness の欄名を検査 interface として使う以上、W6-P1 と同格の versioned 登録が要る。**指摘としては [27] 事件に隣接する型**(番号なき ID の live 混入)だが、現状は draft plane 内の ID 一致検査に閉じており凍結 artifact への混入ではない。**先に報告する** |
| **GAP-7** | **W6-P8** | **IMAGE-MU 固有の status 割当が未定。** ① curve model 不在 → UNKNOWN か ABSENT か(W6-P8 の ABSENT は「独立 **divisor** が供給されなかった」に予約されている)。② 点ごとの $\mu(r)\ne b$ は「well-formed な **divisor** 不一致」ではないので、W6-P8 の逐語では **FAIL に割り当てる根拠が無い** | token 偽造が FAIL(声が大きい)になるか MALFORMED(provenance 扱い)になるかが決まらない。判定に効く曖昧さ |
| **GAP-8** | **W6-P6 / O-1** | **IMAGE-MU における二 route 独立性の具体が無い。** O-1 が別アルゴリズムを課しているのは rank 判定(判別式 vs Sturm)と既約性(平方判定 vs 有理根定理)だけで、**μ の再計算**については何も言っていない | 実装は可能だが「何をもって別実装とするか」を係が決めることになる(H-4 の判定基準に触れる) |

★ = 単独で実装を止める blocker。

---

## 2. 最小改版案(draft・**未採択・Sol ゲート案件**)

**方針**: 凍結 v20 は byte 不変。次版 spec v21 に **§5.3.5.2「IMAGE-MU 実装条項」を additive 新設**し、W6-P1〜P12 は逐語同一で残す。point-map schema は **v2 を新設**(`curve_model_ref` 追加は v1 の黙った拡張にしてはならない — M-8 / Y-3c ③)。witness schema は **v1 を versioned 登録**(現行 code の欄名がそのまま normative になるため、内容は既存と一致 = code 側の改変不要)。contract は v16 で §3.2 の欄表を同期、manifest は v16 で `Y-3d`(新 schema 2 件の era 束縛)。

### 2.1 提案条項

- **W6-P13(curve model の供給・★要裁定)**: 受領 route は curve model($a,p,f_6,C$ と ambient 関係 $y^2=f_6(x)$)を **`curve_model_ref` = {artifact_id, json_pointer, whole-artifact digest}** で受け取る。**point-map payload 内の値を curve model として使ってはならない。** ref 不在・inline-only は `LEGACY_UNVERIFIED_REF`(W6-C5)とし **IMAGE-MU = UNKNOWN**(PASS に到達しない)。
  - **選択肢 A(係の推奨)**: D-2 certificate が既に持つ `curve_model_digest` / `ambient_quotient_relations`(spec §4.1)へ pin する。P-3.3(読んだ blob の digest 一致)と Y-3 が既にこの経路を守っているので、新しい信頼点を作らない。
  - **選択肢 B**: harness が事前登録候補 $(a,p,f_6,C)$ を別 registry artifact として供給。
  - **選択肢 C(明文で却下すべき)**: payload 埋込み。自己申告になり gate が無歯化する。
  - **この三択は Sol へ**。係は決めない。
- **W6-P14(有限点の再計算)**: 受領側は model と record の $(x_0,\ y\text{-rank})$ だけを入力に、独立に次を再計算する — ① $x_0$ が $\gcd(a,a')$ の単根(=$a$ の二重根)であること、② $f_6(x_0)\ne0$、③ $p(x_0)\ne0$、④ 像が $(T-a(x_0))^2 - p(x_0)^2 f_6(x_0)=0$ を満たすこと、⑤ 原始整数化した最小多項式が record の token の係数列と**バイト一致**、⑥ rank が W6-P15 に一致。**`exact_image_witness.exact_reduction` の申告値は入力ではなく照合対象**である(不一致は FAIL)。$p(x_0)^2f_6(x_0)$ が有理平方の場合は像が有理数に退化し、二点は**次数 1 の別 token 二つ**を持つ — この分岐も条文に置く。
- **W6-P15(rank transport・一般形)**: $y$-root rank $\rho\in\{0,1\}$ に対し $y=s\sqrt{f_6(x_0)}$($s=-1$ が $\rho=0$、K-3 を $y^2-f_6(x_0)$ に適用)。$a(x_0),p(x_0)\in\mathbf Q$ ゆえ、有理数による平行移動は $(\Re,\Im)$ 辞書順を保存し、$p(x_0)>0$ の scaling は順序を保存・$p(x_0)<0$ は反転する($f_6(x_0)>0$ の実根対でも $f_6(x_0)<0$ の純虚根対でも同様)。ゆえに **像の rank $k=\rho$ if $p(x_0)>0$、$k=1-\rho$ if $p(x_0)<0$**。$p(x_0)=0$ は二点が像を共有する縮退で **v1 宇宙外 → UNKNOWN**。
- **W6-P16(無限遠点・★最大の穴)**: 受領側は model から exact に ① $\mu$ が一方の無限遠点で 5 位の零、他方で 5 位の極を持つこと、② **どちらが 0 に落ちるか**(向き)を model 自身の data(E-3 分岐 $a_5=+p_2$ 等の主係数関係)から、③ $e=5$ ゆえ $m_r=4$ を再計算する。inf$_\pm$ の canonical ID は **K-1 の固定埋込みに対して**定義する($y/x^3$ の符号分岐等)。**散文 `orientation` 文字列は witness として不可。**
- **W6-P17(multiplicity 再計算・新下位欄 `IMAGE-MULT`)**: $m_r=e_r-1$ を受領側が model から再計算する($a$ の二重根で $e_r=2$、無限遠で $e_r=5$)。**総和 $\sum m_r = 2g-2+2\deg\mu = 12$ の突合を producer 側 assert から受領側再計算へ移す。** これ無しでは IMAGE-MU が PASS でも W6-C1 は再計算されない。
- **W6-P18(support の独立再計算)**: 受領側は model から ramification support を自ら導き($\gcd(a,a')$ の根 × $y$-rank 2 通り + 無限遠 2 点)、record 集合との**厳密一致**を要求する。producer の `declared_support` は cross-check に降格し、参照系にしない。
- **W6-P19(IMAGE-MU の status algebra)**: curve model ref 不在/inline-only → **UNKNOWN**(ABSENT は W6-P8 の予約語のまま使わない)。v1 宇宙外(係数体 $\ne\mathbf Q$・$d\ge3$・$p(x_0)=0$)→ **UNKNOWN**。schema/pointer/digest 不正 → **MALFORMED**。**model から再計算した像・rank・multiplicity が record と食い違う → FAIL**(W6-P8 の FAIL 帯をこの一点だけ「点ごとの像不一致」へ拡張する — **これは W6-P8 の意味論拡張なので Sol 裁可事項**)。**IMAGE-MU = PASS は、有限点・無限遠点を含む全 record が PASS のときだけ**(部分被覆で PASS を出さない)。
- **W6-P20(二 route の独立性を IMAGE-MU へ拡張)**: 二 route は $\mu$ の再計算を**別アルゴリズム**で行う(例: `R1'` = $\{y^2-f_6(x_0),\ T-a(x_0)-p(x_0)y\}$ からの $y$ 消去/終結式、`R2'` = 二次拡大上のノルム構成 + 独立な原始化)。共通 module・相互 import は禁止(現状の O-1 と同じ規律)。
- **W6-P21(witness schema の登録)**: `mb/ninfty-w6-image-witness/v1` を W6-P1 と同格で plane に登録し、欄名(`datum` / `exact_reduction.{fibre_relation, map_evaluation, image_relation, square_relation}` と無限遠用の後継欄)を normative 化する。

### 2.2 改版に伴う波及(見積り)

- spec v21(§5.3.5.2 additive 新設・chg 表・v20 byte 凍結維持)・contract v16(§3.2 欄表同期)・manifest v16(`Y-3d`)。**hash 順序 manifest → contract → spec → receipt を維持。**
- `bundle-selfaudit-v13.py` を versioned 新設(v11/v12 は byte 不変)。検査は additive のみ — `IMAGE-MULT` 欄名・新 schema ID 2 件の存在検査を追加、既存 24 検査は逐語維持。
- point-map schema v2 への移行は producer 二本の versioned 追記(v1 出力の byte は変えない)。
- 負例 fixture(両縁): ① curve model と食い違う token(発火側)・② model と一致する正規 token(非発火側)、③ rank を $p(x_0)<0$ の系で反転させた負例(GAP-3 の両縁)、④ 無限遠の向きを入替えた負例(GAP-2 の両縁)、⑤ $m_r$ を 4→3 に改竄し総和 12 を破る負例(GAP-4)、⑥ curve model ref を inline-only に落として **UNKNOWN であって PASS でない**ことを固定。

---

## 3. 現状の機械的確認(本作業で走らせたもの)

```
$ python search/test_ninfty_w6key.py
285 checks, 0 FAIL
```

- 凍結境界に触れた箇所: **無し**(読み取りのみ。spec v19/v20・contract v15・manifest v15・R1/R2・selfaudit v11/v12・freeze receipt はいずれも未変更)。
- 札の状態は不動: `W6_CLOSED=false` / `IMAGE-MU=UNKNOWN` / `W-6 = OPEN` / `EP = uncalibrated・UNKNOWN`。本速達のどこにも逆を書いていない。
- 裁定 424 の申し送り(v12 束縛と consumer required map の v11→v12 同一 move)には触れていない。

## 4. 司令塔への求め

1. **GAP-1 の三択(A/B/C)** と **GAP-7 ②(点ごと像不一致を FAIL 帯に入れるか)** を便 102 の Sol ゲート案件へ。意味論の新設なので係は決めない。
2. **IMAGE-MU 実装 scope の認可**(便99 F99-5.2 除外列挙・便101 W101-6 との関係整理)。認可が下りるまで着工しない。
3. **GAP-6(未登録 schema ID の live 混入)** は改版を待たずに記帳しておくのが安全と考える(現状は draft plane 内に閉じているが、規律上の型としては [27] に隣接)。
