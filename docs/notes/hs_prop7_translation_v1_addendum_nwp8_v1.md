# hs_prop7_translation_v1 追補 — NW-P8 の versioned 撤回・再定義(v1・candidate)

- 起草: 司令塔・2026-08-04(裁定 474 の司令塔案件 M5)
- **状態札: candidate — 発効は Sol 承認後**(P101-1 の条項[NW-P8 は便 101 の 6 条件契約の一部]に触るため、便 102 で承認請求)
- 正本参照: `docs/notes/hsp7_hexagon_arbitration_v1.md`(仲裁・構造事実の証明)/ `docs/notes/hsp7_cond4_cv9_reading_v1.md`(副検問・反証の確認)/ `docs/notes/hsp7_cond4_lanespec_v1.md` 付録 A-2(撤回対象の事前登録票)
- 手続き整合: **S-7′(同一 run・同一登録内の予言改稿禁止)に抵触しない** — 本追補は別 version による正規の撤回であり、旧予言と反証の記録は不変保存する。

## 1. 撤回対象(逐語)

hs_prop7_translation_v1.md §8.7.7 の NW-P8 行および lanespec 付録 A-2 の事前登録予言:

> 「5 件のうち少なくとも 1 件で N・N₀ の判定が食い違う」(存在主張)

および §9.3 の停止規則 S-8:

> trigger: 「X_N 全掃引で N と N₀ の hexagon 判定の不一致が 0 件」/ verdict: CALIBRATION_FAILED / INTEGRITY_STOP

## 2. 撤回の根拠(理論的反証 — 事後の言い換えではない)

仲裁(hsp7_hexagon_arbitration_v1.md)が確定した構造事実:

> **N ∩ F₂ = N₀ ∩ F₂ = 𝒱(F₂)**(verbal 部分群は c の処遇と独立)。したがって Prop 3.4(前提 = N ∈ NFI_PB₃(B₃)・(m,f) ∈ ℤ×[F₂,F₂] — 両窓とも充足)により、**charming 候補の full hexagon 判定は N と N₀ で恒等に一致する**。

ゆえに旧予言は測定以前に**理論的に偽**であり、S-8 は本走で毎回恒真に発火する構造だった。CV-9 副検問はこの反証を独立検算(m 掃引の整数演算再現)込みで確認した。撤回は「予言が外れたから弱める」(禁止されている事後緩和)ではなく、**予言の前提が定理により崩れたことの記録**である。

## 3. 再定義(S-8 → S-8′・N₀ 窓の役割変更)

1. **S-8′(新・逆向き)**: trigger =「N と N₀ の判定が **1 件でも食い違う**」/ verdict = **IMPLEMENTATION_BUG_SUSPECTED / STOP**。理由: 一致は定理の帰結なので、不一致は実装バグの証拠(v1 の ApplyQElt バグ型の検出器)。
2. **N₀ 窓の存続目的**: 「N と異なる挙動の検出」ではなく、(i) **c 会計の無料実装テスト**(仲裁 P-1)と (ii) **evaluation_mode = word_level_required 経路の実装検査**(c ∉ N₀ で商近道が壊れる、の検査は「判定が変わる」ではなく「word-level 経路が正しく組まれているか」の検査として存続)。
3. 旧 S-8 の「較正予想としての N₀」に代わる較正陽性の供給は **NW-P7(p=5 control・5/5 PASS 予言)** が担う(別途 Sol 認可請求・lanespec 付録 A-1)。

## 4. Sol への承認請求(便 102)

- 請求 1: 本追補の発効(旧 NW-P8/S-8 の撤回と S-8′ への差替)。
- 請求 2: 撤回に伴う便 101 P101-1 条項の読み替え(NW-P8 への言及部分)。
- 注記: 補題 NW-1b (5) の「近道が壊れる」の語の二義性(θ,τ の F₂/N_F₂ への降下 vs B₃/N 内の Ad 実現)の用語分離も同便で申し送る(仲裁の要判断事項)。
