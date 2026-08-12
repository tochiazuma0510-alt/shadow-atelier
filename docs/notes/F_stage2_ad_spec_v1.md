# (Ad) 段 2 spec **v1**(便 121 B2・§9.2-5)— 凍結可能形

作成: 数学者(Opus 5)/ 2026-08-12 / 発注 = 司令塔裁定 1045
前提 = 便 121 **B2 = GO**(転進追認・R-1 は留保のまま)。★ **本 spec を versioned freeze してから発火**(B2 第 5 条件)。
⚠ $u$ 非接触・$c$ 未評価。**格: candidate**(Sol 未監査・本 spec)。

---

## §0 ★★ B2 の 5 条件(逐語・本 spec の骨格)

| # | 条件(便 121 B2 逐語) | 本 spec での実装 |
|---|---|---|
| **1** | target は $H_F$、module は Ad、**twist は $i=0$ に固定** | §1 |
| **2** | 段 2 の結論を「**窓が arithmetic に qualification された**」と読まない | §4 非結論行 |
| **3** | **972、非円分供給、K9/K5 bridge へ流用しない** | §4 流用禁止行 |
| **4** | **R-1 は OPEN のまま** claim と cert に明記 | §3 schema `r1_status` |
| **5** | 未凍結の実装を直ちに走らせず、**stage-2 spec と fail-closed 条件を先に versioned freeze** | 本 spec 自体 |

---

## §1 対象の固定(NAME-COLLIDE 行つき)

```
target  : H_F = SL^±(2,691) ×_{C_2} S_3   (位数 1,979,632,080)
module  : Ad = sl_2(F_691)  (3 次元・随伴)
twist   : ★ i = 0 に固定    (i=1 は段 2 の対象外 — 段 1' の予言 dim=0)
coeff   : F_691
NAME-COLLIDE : H_F は pair_h2_design_draft_v1.md §2 の Ḡ と同一対象。|H_F| = |H_6|(位数一致・構造別)。
               P-PH2-4(dim H^2 ≤ 1)は再掲であり本 spec の新規ではない。
```

★ **段 1′ の入力**(凍結済 `F_stage1ad_prereg_v1_1.md`): $\dim H^2(H_F,\mathrm{Ad})=1$・$\dim H^2(H_F,\mathrm{Ad}\otimes\det)=0$(**紙の二導出** — 系統 B の重み計算 + 系統 C の非分裂拡大。⚠ **独立性は段別**)。

---

## §2 段 2 で構成するもの(4 段)

$H^2(H_F,\mathrm{Ad})$ が 1 次元 ⟹ 非零類はスカラー倍を除き一意。段 2 は**その類が実際に何を与えるか**を構成します。

| 段 | 構成 | 判定 |
|---|---|---|
| **S2-1** | **非零 class** $[\mathcal E]\in H^2(H_F,\mathrm{Ad})\setminus\{0\}$ の**明示生成元** | ★ 系統 C の witness($1\to\mathfrak{sl}_2\to SL(2,\mathbf Z/691^2)\to SL(2,691)\to1$)を $H_F$ へ**押し上げる**構成 |
| **S2-2** | **非 split extension** $1\to\mathrm{Ad}\to\mathcal E\to H_F\to1$ | ★ 補元の非存在を**機械で**(小素数で較正 → $p=691$ は安定元法/構造論法) |
| **S2-3** | **braid lift**: $\mathcal E$ が $B_3$(または適切な braid 群商)からの持ち上げを許すか | ⚠ **最も重い段**・失敗しうる |
| **S2-4** | 所要の **surjectivity**($\mathcal E$ への全射性) | ⚠ S2-3 の後 |

⚠ **段 2 は S2-1/S2-2 までを最小成果とし、S2-3/S2-4 は別ゲート**にすることを推奨します(便 121 は 4 つを列挙しているが、S2-3 の失敗が S2-1/S2-2 の成果を巻き込まない設計にすべき)。

---

## §3 cert schema `F_stage2_ad/v1`

```
stage           : "S2-1" | "S2-2" | "S2-3" | "S2-4"
target          : "H_F"                       ★ 固定(§1)
module          : "Ad"                        ★ 固定
twist_i         : 0                           ★ 固定(B2 条件 1)
class_nonzero   : bool                        (S2-1)
extension_split : bool                        (S2-2・false が期待)
braid_lift      : true | false | null         (S2-3・null = 未着手)
surjectivity    : true | false | null         (S2-4)
★ r1_status     : "OPEN"                      ★ 必須固定文字列(B2 条件 4)
★ r1_note       : "③→① 非円分算術供給は未証明。段 2 の内部構成の論理前件ではないが、
                   算術 marking を付ける段 4 相当のゲートは OPEN のまま。"
★ no_window_qualification : true              ★ B2 条件 2(結論を窓資格と読まない)
★ no_transfer   : ["972", "non-cyclotomic supply", "K9/K5 bridge"]   ★ B2 条件 3
name_collide_note : "H_F = pair_h2 の Ḡ。|H_F|=|H_6|。P-PH2-4 は再掲"
method          : "stable_elements" | "explicit_cocycle" | "paper_lemma"
calib           : {cal-1..cal-6 の PASS/FAIL}  ★ 段 1' のスイートを継承
tool_version, input_hash, wall_clock_ms, cap_ms
u_touched : false ; c_touched : false
verdict   : null                              ★ 判定語なし(発効は司令塔)
```

---

## §4 fail-closed 条件(凍結対象)

| # | 事象 | 行き先 |
|---|---|---|
| **F1** | 段 1′ の較正スイート(cal-1〜6)が 1 本でも FAIL | ★ **段 2 に入らない**(UNKNOWN + STOP) |
| **F2** | S2-1 で class が 0 と出る | ⚠ **段 1′ の紙の二導出と矛盾** ⟹ 即停止・導出の再検査 |
| **F3** | S2-2 で **split** と出る | ⚠ 同上(非分裂は系統 C の witness そのもの)⟹ 即停止 |
| **F4** | S2-3 の braid lift が**存在しない**と出る | ★ **一級の否定的結果**(異常ではない)⟹ ③ 線は「容器はあるが braid に乗らない」で閉じる |
| **F5** | 壁時計 cap 超過 / メモリ超過 | UNKNOWN + 設計差し戻し(★ 本番値は群を構成しない路で出す) |
| **F6** | `r1_status` が "OPEN" 以外で書かれた cert | ★ **cert 無効**(B2 条件 4 違反) |

**★ 非結論行(必ず claim と cert に書く)**
> 段 2 のいかなる結果も「**窓が arithmetic に qualification された**」ことを意味しない(B2 条件 2)。
> 段 2 の結果を **972 / 非円分供給 / K9・K5 bridge へ流用しない**(B2 条件 3)。
> **R-1 は OPEN**(B2 条件 4)。

---

## §5 ★ 新規律の反映(便 121)

1. **Newton 完全冪 ≠ 枝一意性**(M121-4)⟹ 本 spec には Newton 論法は現れませんが、**同型の注意**を適用: **「必要条件」と「十分条件」を別行で書く**。⟹ §2 の S2-1〜S2-4 は**段の連鎖**であって、前段の成功が後段を含意しません。
2. ★ **有限計算核の格を紙包絡へ自動伝播させない**(M121-7)⟹ §3 の `method` 欄と `calib` 欄で**どこまでが機械でどこからが紙か**を分離。★ **cross-checked は較正($p\le23$)にのみ**。$p=691$ の本番値は **candidate / single-run**(教訓 F-3)。

---

## §6 GAP・記帳

- **【S2-GAP-1】(大)** S2-3(braid lift)の構成法が未設計。⟹ ★ **段 2 の最小成果を S2-1/S2-2 に限る**という私の推奨(§2)は、この GAP を段の外に出す設計です。
- **【S2-GAP-2】(中)** 系統 C の witness($SL(2,\mathbf Z/691^2)$)を $H_F$ へ押し上げる際、$S_3$ 成分の持ち上げが要ります($\det$ が $\mathrm{sgn}$ と両立する形)。⟹ S2-1 の実体。
- **【F-GAP-6】(継続)** $\mathrm{Ad}\otimes\det^i$ の $S_3$-不変部が marking に依存しないか(事前登録項目)。
- **申告**: 走行ゼロ・$u$ 非接触・$c$ 未評価・**未凍結**(凍結執行は司令塔)・**Sol 未監査(本 spec)**・格 = **candidate**。
