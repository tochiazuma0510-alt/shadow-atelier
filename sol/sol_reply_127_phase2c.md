# Sol 便 127 返信 — E-1 / Phase 2c 前件ゲート

日付: 2026-08-13

入力: `ops/inbox_codex/sol_task_127_phase2c.txt` 全節

仕様正本: `docs/notes/c1p5_v2_diff_review_v1.md` (指定 commit `73386022`)

## F127-0. 一行結果

E-1 は v2.1 で訂正した。Phase 2c の三前件の生値は

\[
(①,②,③)=(\mathrm{false},\mathrm{true},\mathrm{true}).
\]

候補 $E=\mathrm{PSL}(2,8)\times C_3$ は $|E|=1512$、$E^{\rm ab}=C_3$、$N_E$ isolated、$\theta,\tau$ 不変まで立つ。しかし対角 $C_3$ 写像は **どの正整数 level $l$ でも $G_l$ に降りない**。従って $G_l$ と $E$ の共通非自明商はなく、純商は全 level で直積になる。PH2-VOID′ により事前登録も像測定も行わず、

\[
|\operatorname{Im}R|_{\rm raw}=\texttt{null}\quad(\text{未測定}),qquad\text{状態} = \mathrm{UNKNOWN}
\]

で停止した。

## F127-1. erratum E-1

新規版は `docs/notes/d972_phase2_void_addendum_v2_1.md`。v2 §3 の散文式だけを

\[
\boxed{|GT(K^{(l)})|=2n_0\varphi(n_0),\qquad n_0=l/\gcd(l,2)}
\]

へ訂正した。すなわち $n_0=l$ (奇数 $l$)、$n_0=l/2$ (偶数 $l$)。例として $l=126$ は $2\cdot63\cdot\varphi(63)=4536$。$4(l/2)^3$ は偶数 level の群位数 $|G_l|$ であり shadow count ではない。

旧 v2、旧表、旧 producer/checker/cert は変更していない。旧表 12 行は全て訂正式と一致する。

## F127-2. 候補 $E$ の構成生値

$PB_3=F_2\times\langle c\rangle$ の marking で、対角写像を

\[
\delta(x)=\delta(y)=1,qquad\delta(c)=0\quad(C_3\text{ 加法記法})
\]

とした。標準 $PB_3\twoheadrightarrow P=\mathrm{PSL}(2,8)$ と組み合わせた像の生値は次のとおり。

| 項目 | 生値 |
|---|---:|
| $|P|$ | 504 |
| $|E|$ | 1512 |
| $|[E,E]|$ | 504 |
| $|E^{\rm ab}|$ | 3 |
| $[E,E]=\ker(E\to C_3)$ | true |
| marked $x,y$ が生成する群の位数 | 1512 |

$E$ 自身が split であることは設計どおりである。目的は非完全性であり、$E$ 自身の非分裂性ではない。PSL$(2,8)$ の Schur 乗数を別の拡大探索へ読み替えていない。後段の非積ゲートは、$E$ 自身ではなく $G_l$ と $E$ の純商についてのものとして分離した。

## F127-3. 前件ゲート — 指定順 ①→②→③

### F127-3.1. ① $K^{(l)}\subseteq\ker\delta$

生値:

```text
raw_boolean = false
levels_with_inclusion = []
scope = every positive level, hence no admissible level
```

包含は $\delta$ が $G_l=PB_3/K^{(l)}$ を経由することと同値である。標準 dihedral marking は全 $l>0$ で

\[
xyx=x^{-1}yx^{-1},\qquad yxy=y^{-1}xy^{-1}
\tag{1}
\]

を満たす。任意の $G_l\to C_3$ に (1) を入れると

\[
4\delta(x)=4\delta(y)=0.
\]

$4\equiv1\pmod3$ より $\delta(x)=\delta(y)=0$ しかない。従って対角 assignment $(1,1)$ は全 level で降りない。この全 level 導出に加え、登録 12 level は producer の SymPy permutation group と checker の標準ライブラリ tuple permutations が別々に関係式と Cayley 衝突を再現した。

| $l$ | $|G_l|$ | $|[G_l,G_l]|$ | $|G_l^{\rm ab}|$ | 包含生値 |
|---:|---:|---:|---:|:---:|
| 9 | 2916 | 729 | 4 | false |
| 27 | 78732 | 19683 | 4 | false |
| 36 | 23328 | 1458 | 16 | false |
| 45 | 364500 | 91125 | 4 | false |
| 54 | 78732 | 19683 | 4 | false |
| 63 | 1000188 | 250047 | 4 | false |
| 72 | 186624 | 11664 | 16 | false |
| 81 | 2125764 | 531441 | 4 | false |
| 108 | 629856 | 39366 | 16 | false |
| 126 | 1000188 | 250047 | 4 | false |
| 135 | 9841500 | 2460375 | 4 | false |
| 162 | 2125764 | 531441 | 4 | false |

### F127-3.2. ② $N_E$ isolated

生値:

| 列挙段 | 生値 |
|---|---:|
| $[E,E]$ 候補 | 504 |
| charming $m\bmod9$ | $\{0,2,3,5,6,8\}$ |
| raw candidate | 3024 |
| (3.10) 除外 | 2640 |
| (3.11) 除外 | 330 |
| generation 除外 | 0 |
| shadow | 54 |
| direct endomorphism well-defined | 54/54 |
| direct endomorphism image size | 1512 (全 54 件) |
| settled | 54/54 |
| `N_E_isolated` | true |

54 件の各 marked image を $E$ の 1512 元 Cayley graph 全体へ直接延長し、well-defined かつ bijective であることを調べた。producer/checker は helper を共有していない。

### F127-3.3. ③ $\theta,\tau$ 不変性

$z=(xy)^{-1}$、$\theta:(x,y)\mapsto(y,x)$、$\tau:(x,y)\mapsto(y,z)$ とした。

| 項目 | 生値 |
|---|:---:|
| $\theta$ well-defined / bijective | true / true |
| $\tau$ well-defined / bijective | true / true |
| $(\delta(x),\delta(y),\delta(z))$ | $(1,1,1)$ |
| $\delta\circ\theta=\delta$ on all 1512 elements | true |
| $\delta\circ\tau=\delta$ on all 1512 elements | true |
| raw_boolean | true |

PSL marking と対角成分を組み合わせた $N_E$ は両作用で不変となった。

## F127-4. PH2-VOID′ 非積ゲート

要求された二つの生値は逆方向になった。

```text
E_nonperfect = true
E_abelianization_is_C3 = true
G_l_has_C3_quotient = false
nontrivial_common_quotient_exists = false
requested_nonproduct_raw_boolean = false
pure_quotient_direct_product_raw_boolean = true
PH2_VOID_prime_applies = true
```

理由は前件①と同じで、$G_l$ の可換化には 3-part がない。さらに $G_l$ は可解なので $P$ を商に持たない。$E=P\times C_3$ の非自明単純商候補は $P$ または $C_3$ だが、どちらも $G_l$ の商にならない。従って Goursat の共通商は自明で、全 $l>0$ について

\[
PB_3/(K^{(l)}\cap N_E)\cong G_l\times(P\times C_3),
\qquad
|PB_3/(K^{(l)}\cap N_E)|=1512\cdot4\bigl(l/\gcd(l,2)\bigr)^3.
\]

候補 $E$ が非完全であることだけでは非積性は従わず、その $C_3$ が実際に $G_l$ と共通商である必要があった。この候補ではその前件が空になる。

## F127-5. 事前登録・測定境界

非積ゲートが false なので、レビュー仕様に従いその場で停止した。

| 欄 | 生値 |
|---|---|
| preregistration created | false |
| frozen spectrum | null |
| blind declaration | null |
| measurement authorized | false |
| measurement performed | false |
| reduction image set formed | false |
| $|\operatorname{Im}R|$ raw | null (未測定) |
| status | UNKNOWN |
| finite-depth B type recognition | false |

したがって 324/972 のいずれかを Phase 2c の観測値として記帳していない。

## F127-6. 任意 target-54 helper

今後の直積族 gating 用の算術 fixture を producer cert に含めた。

\[
\text{roof raw}=18\cdot\text{target internal image count},qquad
18\mapsto324,quad54\mapsto972.
\]

`implemented_as_formula_fixture_only=true`、`used_for_phase2c_measurement=false`。Phase 2c の reduction image は形成していない。

## F127-7. producer/checker 生出力と再現

producer:

```json
{"E_abelianization_order": 3, "E_order": 1512, "antecedent_raw": [false, true, true], "pure_quotient_direct_product": true, "raw_image_size": null, "run_id": "d972-phase2c-preflight-20260813T025841Z", "shadow_count_for_isolatedness": 54, "status": "UNKNOWN"}
```

helper 非共有 checker:

```json
{"E_order": 1512, "all_checks_true": true, "derived_order": 504, "pure_quotient_direct_product": true, "raw_image_size": null, "settled_count": 54, "shadow_count": 54, "status": "UNKNOWN"}
```

再現コマンド:

```powershell
python search/d972_phase2c_preflight_v1.py --hard-timeout-seconds 900
python search/check_d972_phase2c_preflight_v1.py --hard-timeout-seconds 900
```

両方に atomic checkpoint と hard-timeout を実装した。producer は SymPy、checker は Python 標準ライブラリの tuple permutations のみを使い、checker は producer を import していない。格は producer/checker 二系統一致の cross-checked candidate であり、Lean 証明書は本便の射程外である。

## F127-8. 成果物と SHA-256

| path | SHA-256 |
|---|---|
| `docs/notes/d972_phase2_void_addendum_v2_1.md` | `4e9c77a1fdb2d61a10e9fe2716ad0e154c5aa12ad4fd11cb10cde6ac58a2cd9d` |
| `docs/notes/d972_phase2c_preflight_report_v1.md` | `eb560ae40c2deacc4d0aefa2d4488ae334ddc347d9427a1e1168e2d8475ea2e5` |
| `search/d972_phase2c_preflight_v1.py` | `5ddc17c60a31c12d09ea964465b1db0fc916aa3003c926c780d2adb4a657d590` |
| `search/check_d972_phase2c_preflight_v1.py` | `b489ec534d1a61e909e1263d07a84c21834d67206eef8ac6e3d5e2b8eeed9f10` |
| `search/certs/d972_phase2c_preflight_v1_20260813.json` | `dce4d838fa87cb65d7786d4ca4890cbcd46df86ecd3ae886049ecb95c5929096` |
| `search/certs/d972_phase2c_preflight_v1_check_20260813.json` | `dca4a80f2285e99a8131cf76fa71f095560e0800f46231cdd06880c09d084303` |
| `search/certs/d972_phase2c_preflight_v1_checkpoint.json` | `8adcd922d6cdda0368c56ae7e631f541df207a71b2ab75beeeacc3982adbd0d6` |
| `search/certs/d972_phase2c_preflight_v1_check_checkpoint.json` | `b1dc9c8f76e56f609ac4ac914f1dc7755f7d8382f14ca07db2a76183c2704691` |

## F127-9. 境界・git

- u/c 非接触、封印 K5 非接触、既存事前登録量の変更なし、宇宙拡張なし。
- 有限深度から B 型を認定していない。
- 既存 `d972_phase2_void_addendum_v2.md`、旧表、旧 cert に diff はない。
- git は read-only 運用。HEAD `ff1aaadd90f2b213aeeeaf8a8bc98245bf70a886`、branch `master`。commit / push / workflow dispatch は行っていない。
- 本便の新規成果物と本返信以外の既存 dirty worktree は変更していない。
