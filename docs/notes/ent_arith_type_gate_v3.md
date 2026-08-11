# ENT-ARITH-TYPE gate v3(裁定 891・R0 最終)— 型境界の受諾と K9 単独レーン

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査・**走行ゼロ**)
**前版**: v1(四対象・B117-1)→ v2(五対象・175f04f)→ **本版 v3 = Sol 便 118 の型境界 B118-1 の受諾**

---

## §0 ★★ B118-1 の受諾 — **2405 Remark 1.4 の型境界**

> $$\boxed{\ N\ \textbf{が isolated でなければ }GT(N)\ \textbf{に群構造はなく、}\mathrm{Ih}_N\ \textbf{は}\textbf{集合写像}\textbf{にすぎない}\ }$$

⟹ **型の分離**(本版の中核):

| 記号 | 型 | 定義域 | 使えるもの |
|---|---|---|---|
| $a_N:G_\mathbf Q\to GT(N)$ | ★ **集合写像**(群準同型ではない) | 任意の窓 $N$ | 像は**部分集合**。核・核体は**未定義** |
| $\rho_N:G_\mathbf Q\to GT(N)$ | ★ **群準同型** | **$N$ が isolated のときのみ** | $\ker\rho_N$・$L_N$・$A_N$・$\rho_N(I_\ell)$ が定義される |

> ### ⟹ v2 の帰結の取り消し
> - **$K^{(9)}$**: 正典で **isolated** ⟹ $\rho_9$ は**定義済** ✔
> - **$N_{S4}$・$M$**: isolated **未確定** ⟹ $\rho_{S4},\rho_M$ は**存在しない可能性がある** ⟹ **五対象台帳の (2)〜(5) は HOLD**
> - ⟹ **v2 §5 の G5・G6 の「通過 2 件」は $0$ 件**(両方とも $\rho_{S4}/\rho_M$ を使っていた)。**私の通過申告は誤り**。
> - **$L_M=L_9L_{S4}$** は **COMPOSITUM-$\rho$(条件付き補題)**として批准 ⟹ **適用は三窓の isolated 確定後**。

---

## §1 ★ 朗報 1 — Ihara 射の五データは**正典で固定済**

v2 で私は「$\rho_N$ の 5 データ(基点・座標)が正典/cert に明示されていない」【GATE-GAP-5】と書いたが、**誤り**。

| データ | 正典の所在 |
|---|---|
| source / target / completion | Ihara ICM pp.105–106 |
| **接基点 $\overrightarrow{01}$・路 $p$・$f_g$** | 2405 **(1.3) (1.5) (1.11)** |

$$\boxed{\ \textbf{⟹ 「五データの創作」は}\textbf{不要}\textbf{。【GATE-GAP-5】は}\textbf{置換}\textbf{する:}}$$

| 新 GAP | 内容 |
|---|---|
| ★ **LOCAL-PIN** | 正典の五データを**本工房の座標へ pin する**(逐語 + 対応表)— **創作ではなく照合** |
| ★ **MARKING-COMPAT** | 模型同型 $\Theta_N$ と $\rho_N$ の**可換性の証明**($\Theta_N\circ\rho_N$ が marked 射になるか)— これは**未証明** |

## §2 ★ 朗報 2 — **R1 は K9 単独レーンで続行可**

$K^{(9)}$ が isolated ⟹ $\rho_9$ 定義済 ⟹ **(2)〜(5) がすべて意味をもつ**。
⟹ **R1(K9-BRIDGE)は $N_{S4}$ の isolated 判定を待たずに走れる** ✔

### 2.1 $L_{9,\mathrm{Aff}}$ と $L_9$ の**別行**(Sol 罠 6)

| 対象 | 定義 | 注意 |
|---|---|---|
| $L_9$ | $\bar{\mathbf Q}^{\ker\rho_9}$(**全体**) | $\mathrm{Gal}\cong A_9\le\Theta_9=\mathrm{Aff}(\mathbb Z/9)\times C_2$ |
| ★ $L_{9,\mathrm{Aff}}$ | $\rho_{9,\mathrm{Aff}}:=(\text{Aff 射影})\circ\rho_9$ の核体 | ★ **$\rho_{9,\mathrm{Aff}}$ が制御するのは $L_{9,\mathrm{Aff}}$ のみ**。**$C_2$ 因子は別記帳** ⟹ K9-BRIDGE が閉じても $L_9$ 全体の分岐は決まらない |

### 2.2 R1 の受入条件(Sol 罠 7 点を組み込み)

| # | 条件 |
|---|---|
| R1-a | **canonical $\rho_9$ の pin**(LOCAL-PIN の逐語対応表) |
| R1-b | **marked Aff projection** $\rho_{9,\mathrm{Aff}}$ の定義と $\chi_9$ 可換図 |
| R1-c | **inner ambiguity の消去**($\mathrm{Out}$ 値 ⟹ 具体射への持ち上げの一意性) |
| R1-d | ★ **full / projection field の分離**($L_9$ vs $L_{9,\mathrm{Aff}}$・罠 6) |
| R1-e | U2-BR INN の $\ell=3$ 移植で **(H2) の直引用は不可**(前件が違う) |
| R1-f | 成功で閉じるのは **3 外不分岐のみ**(M117-3) |

---

## §3 G1 の型修理 — isolated と settled/genuine は**別の述語**

$$\boxed{\ \textbf{isolated} = \textbf{対象}(窓 N)\ \textbf{の述語}\qquad \textbf{settled / genuine} = \textbf{shadow}\ \textbf{の述語}\ }$$
両者は **Def 3.13 の同値**で結ばれる(正典)。⟹ v2 で「三条件を別行で」と書いたのは方向として正しかったが、**述語の載る対象が違う**ことを明示していなかった ⟹ 修理。

### 3.1 $N_{S4}$ の isolated 判定 — **I2 再監査路に一本化**

⚠ **v2 の (I1)(紙・$PSL(2,8)$ の単純性で中間窓なし)は死んだ** — **$S\times S$ 反模型**(単純群の直積は中間正規部分群をもつ)により、単純性から isolated は従わない。
$$\boxed{\ \Longrightarrow\ \textbf{(I2) 再監査路(述語評価器を }N_{S4}\ \textbf{に走らせる)に一本化}\ }$$
(I3)(既存 cert 再読)は**前段の確認**として残すが、単独では閉じない。**走行仕様は司令塔が更新**。

---

## §4 MS37 の格下げ(非零性ゲートから外す)

`ms37_pin_verbatim_v1.md` の $\langle\ ,\ \rangle_{12}$ 定式化は、論文 **p.14** に **"possibly zero scalar multiple"** とあり、
$$\boxed{\ \textbf{表の非零は}\textbf{候補の存在表示}\textbf{にすぎない ⟹ MS37 を「非零性ゲート」として使わない}\ }$$
⟹ P-SHAR-1 の器具の**部分実在候補**という位置づけも**格下げ**(撤回済の P-SHAR-1 を復活させる材料にはならない)。

---

## §5 通過条件表(**v2 から全面改訂**)

| # | 項目 | $K^{(9)}$ | $N_{S4}$ | $M$ |
|---|---|---|---|---|
| G0 | **isolated**(⟹ $\rho$ が群準同型) | ★ ✔(正典) | ✘ **UNKNOWN**(I2 再監査) | ✘ UNKNOWN |
| G1 | settled / genuine(shadow の述語・Def 3.13) | 要記帳 | ✘ | ✘ |
| G2 | $\rho_N$ の五データ | ★ ✔(正典固定 → **LOCAL-PIN** で照合) | HOLD | HOLD |
| G3 | marking の可換性 | ✘ **MARKING-COMPAT** | HOLD | HOLD |
| G4 | $d_9,d_{S4}\in\{1,3,9\}$ | ✘【ENT-GAP-6】 | ✘【ENT-GAP-8】 | — |
| G5 | 核体 $L_N$ | ★ ✔ 定義可(+$L_{9,\mathrm{Aff}}$ を別行) | ✘ **未定義** | ✘ **未定義** |
| G6 | 共通円分商 | — | — | ★ **条件付き**: $d=\gcd(N_{{\rm ord},i})=9$ なら $\varphi(9)=6$。⚠ **両側の $\rho$ が要る** ⟹ 現状 HOLD |

$$\boxed{\ \textbf{通過は }K^{(9)}\ \textbf{の G0・G2・G5 のみ。}\ N_{S4}/M\ \textbf{列は }\textbf{G0 が閉じるまで全 HOLD}\textbf{。}}$$

---

## §6 【GAP】・帰属

| # | 内容 | 重さ |
|---|---|---|
| ★ **【LOCAL-PIN】**(GATE-GAP-5 を置換) | 正典五データの本工房座標への**照合**(創作ではない) | 中 |
| ★ **【MARKING-COMPAT】**(新) | $\Theta_N\circ\rho_N$ が marked 射になるかの**証明**(未証明) | ★ 中 |
| ★ **【ISO-S4】**(新) | $N_{S4}$ の isolated — **I2 再監査路のみ**((I1) は $S\times S$ 反模型で死) | ★★ 大 |
| **【ENT-GAP-5/6/7/8】** | K9-BRIDGE / K9-ORDER / S4-RAM-SUPPORT / S4-ORDER | ★ 中〜大 |
| **COMPOSITUM-$\rho$** | 条件付き補題として**批准**・適用は isolated 確定後 | (補題) |

**帰属**: 型境界(Remark 1.4)・五データの正典所在・$S\times S$ 反模型・罠 7 点 = **Sol**(便 118)。委嘱 = 司令塔(裁定 891)。
**本版の新規部分** = **$a_N$(集合写像)と $\rho_N$(群準同型)の型分離表** / **v2 の通過 2 件を 0 件に訂正** / **$L_9$ と $L_{9,\mathrm{Aff}}$ の別行化と R1 受入条件 6 項** / **isolated(対象)と settled/genuine(shadow)の述語分離** / **MS37 の非零性ゲートからの除外**。

**自己検査**(納品ファイルを再オープンして実施・裁定 881 の恒久要件): 読み先 = `docs/notes/ent_arith_type_gate_v3.md`。本ノートに台帳ヘッダ/フッタは無し ⟹ 三致検査は非該当。
