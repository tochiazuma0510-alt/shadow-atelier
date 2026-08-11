# ENT-ARITH-TYPE gate v2(裁定 881・R0)— TYPE-IMAGE$^{\rho}$ 五対象様式

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査・**走行ゼロ・紙のみ**)
**前版**: `ent_arith_type_gate_v1.md`(0b507e1)— **四対象様式は本版で置換**(第五対象 $\rho_N$ の欠落 = B117-1)
**規約**: **TYPE-IMAGE$^{\rho}$**(Sol 便 117 P2.2・全面批准形)

> ### ★ 矢印(**唯一の正しい形**)
> $$\boxed{\ \rho_N\ \longmapsto\ A_N=\mathrm{im}\,\rho_N,\qquad \rho_N\ \longmapsto\ \ker\rho_N\ \longmapsto\ L_N\ }$$
> $$\boxed{\ \textbf{✘ }A_N\longmapsto L_N\ \textbf{は}\textbf{ない}\ (\rho_5,\rho_{13}:\ \textbf{同じ像 }C_2\ \textbf{・核体は }\mathbf Q(\sqrt5),\mathbf Q(\sqrt{13})\ \textbf{で別})}$$
> $$\ell\ \textbf{が }L_N/\mathbf Q\ \textbf{で不分岐}\iff\rho_N(I_\ell)=1\qquad(\textbf{標的群の位数の素因子からは読めない})$$

---

## §1 五対象台帳 — $K^{(9)}$

| # | 対象 | 内容 | 格 |
|---|---|---|---|
| **(1)** marked target | $T_9:=GT(K^{(9)})$、模型 $\Theta_9:T_9\xrightarrow{\sim}\mathrm{Aff}(\mathbb Z/9)\times C_2$(位数 108) | **抽象同型型**は U-11 で既知。★ **選んだ marking**($\mathbb Z/9$ 上の $\Delta$-作用が $\chi_9$ か)は**別記帳** | ① 既知 / marking は**要固定** |
| **(2)** arithmetic morphism | $\rho_9:G_\mathbf Q\to T_9$。**source** $=G_\mathbf Q$・**target** $=T_9$・**基点** $=\overrightarrow{01}$(接基点)・**completion** $=$ profinite・**座標** $=$ 定義ノートの $(m,f)$ | ★ **座標と基点は cert に明示が無い** ⟹ **本 gate で固定するのが仕事** | ✘ **未固定** |
| **(3)** embedded image | $A_9:=\rho_9(G_\mathbf Q)\le T_9$。**位数** $\lvert A_9\rvert$・**translation image** $d_9=\lvert C_9$-成分$\rvert\in\{1,3,9\}$・**全射性** $A_9=T_9$? は**三つの独立な主張** | ✘ **すべて UNKNOWN**(上界 $\lvert A_9\rvert\le108$ のみ無条件) | ✘【ENT-GAP-6 K9-ORDER】 |
| **(4)** kernel field | $L_9:=\bar{\mathbf Q}^{\ker\rho_9}$。**ここで初めて** marked 同型 $\mathrm{Gal}(L_9/\mathbf Q)\cong A_9$ を得る | 定義は一意($\ker\rho_9\trianglelefteq G_\mathbf Q$・Galois 対応)。**実体は UNKNOWN** | 定義 ✔ / 実体 ✘ |
| **(5)** local data | $\rho_9(I_\ell)$ と $S_9=\{\ell:\rho_9(I_\ell)\ne1\}$ | ✘ **UNKNOWN**。⚠ **$\lvert T_9\rvert=108=2^2\cdot3^3$ から $S_9\subseteq\{2,3\}$ とは言えない**(v1 の推論は撤回・B116-3) | ✘【ENT-GAP-5 K9-BRIDGE】 |

## §2 五対象台帳 — $N_{S4}$

| # | 対象 | 内容 | 格 |
|---|---|---|---|
| **(1)** | $T_{S4}:=GT(N_{S4})$(位数 54)・$\mathfrak F_0\cong C_9$・$m$ 像 6 元。窓商は $PB_3/N_{S4}\cong PSL(2,8)$ | ★ **$\mathfrak F_0$ 上の $\Delta$-作用が $\chi_9$ か(marking)は型の水準でも未検証** | ① 既知 / marking ✘ |
| **(2)** | $\rho_{S4}:G_\mathbf Q\to T_{S4}$(同上の 5 データ) | 同上 | ✘ 未固定 |
| **(3)** | $A_{S4}$・$d_{S4}\in\{1,3,9\}$・全射性 | ✘ UNKNOWN(上界 54 のみ) | ✘【ENT-GAP-8 S4-ORDER】 |
| **(4)** | $L_{S4}:=\bar{\mathbf Q}^{\ker\rho_{S4}}$ | 定義一意・実体 UNKNOWN | 定義 ✔ |
| **(5)** | $\rho_{S4}(I_\ell)$・$S_{S4}$ | ✘ UNKNOWN。⚠ **$\lvert PSL(2,8)\rvert=504$ から $S_{S4}\subseteq\{2,3,7\}$ とは言えない** | ✘【ENT-GAP-7 S4-RAM-SUPPORT】 |

## §3 五対象台帳 — $M=K^{(9)}\cap N_{S4}$(**Sol F2 が要求した第三の窓**)

| # | 内容 | 格 |
|---|---|---|
| (1) | $T_M:=GT(M)$、$\lvert T_M\rvert=972$(**実測**) | ✔ |
| (2) | $\rho_M:G_\mathbf Q\to T_M$。$\rho_9=R_{M,K^{(9)}}\circ\rho_M$・$\rho_{S4}=R_{M,N_{S4}}\circ\rho_M$(**関手性 — これは証明済の可換図**) | ★ 関手性 ✔ / $\rho_M$ 自体は未固定 |
| (3) | $A_M=\rho_M(G_\mathbf Q)$。**CRT-INJ** で $A_M\cong A:=R(A_M)\le T_9\times T_{S4}$ | 単射 ✔ / 位数 UNKNOWN |
| (4) | $L_M=\bar{\mathbf Q}^{\ker\rho_M}$。★ **$L_M=L_9L_{S4}$**(合成体)— $\ker\rho_M=\ker\rho_9\cap\ker\rho_{S4}$ より | ★ **証明つき ✔**(本 gate の成果) |
| (5) | $S_M=S_9\cup S_{S4}$ | 定義 ✔ / 実体 ✘ |

> ### ★ §3(4) の帰結(v2 で**証明を明示**)
> $\ker\rho_M=\ker\rho_9\cap\ker\rho_{S4}$(CRT-INJ の中身)⟹ Galois 対応で $L_M=L_9L_{S4}$ ⟹
> $$\boxed{\ \lvert A\rvert=\lvert A_M\rvert=[\,L_9L_{S4}:\mathbf Q\,]\ }$$
> ⚠ **これは $\rho$ から出る**(像からではない)⟹ **TYPE-IMAGE$^{\rho}$ 準拠**。u9bit 仕様 §0 の還元はこの形で**救われる**。

---

## §4 $N_{S4}$ の isolated 判定方針

| 手 | 内容 | 費用 | 判定 |
|---|---|---|---|
| **(I1) 紙** | 定義ノートの isolated 述語($N$ が自分より小さい窓へ真に落ちないこと・正確形は正典 §)を $N_{S4}$ に直接適用 | 紙 | ★ **第一手**。$PB_3/N_{S4}\cong PSL(2,8)$ が**単純**であることが効く見込み(正規部分群が 1 と全体のみ ⟹ 中間窓が作れない) |
| **(I2) cert** | 述語評価器を $N_{S4}$ に走らせる | 中 | (I1) が詰まったとき |
| **(I3) 既存 cert の再読** | ihnec 戦役が $N'\in I$ を仮定していたか | 表読み | ★ **最安・先に見る**(SPLIT-NULL の前件に $N'\in I$ がある) |

> ### ★ 方針(本 gate の裁定)
> $$\boxed{\ \textbf{(I3)}\to\textbf{(I1)}\to\textbf{(I2)}\ \textbf{の順。}\ \textbf{(I3) で }N_{S4}\in I\ \textbf{が前提として使われていたなら、そこで閉じる可能性がある}\ }$$
> ⚠ **genuine / settled は別問題**(isolated とは独立)⟹ 三条件を**別行で**記帳する(TYPE-IMAGE$^\rho$ の (3) が「位数・translation image・全射性は独立な主張」であるのと同型の注意)。

---

## §5 通過条件表(v1 §6 の五対象版)

| # | 項目 | 対象 | 状態 |
|---|---|---|---|
| G1 | $N_{S4}$・$M$ の isolated / genuine / settled | (前提) | ✘ UNKNOWN(§4 の方針) |
| G2 | $\rho_9,\rho_{S4}$ の**5 データ固定**(source/target/基点/completion/座標) | (2) | ✘ **本 gate の仕事・未了** |
| G3 | marking($\Delta$-作用 $=\chi_9$)の型水準での検証 | (1) | ✘ UNKNOWN(両窓) |
| G4 | $d_9,d_{S4}\in\{1,3,9\}$ | (3) | ✘【ENT-GAP-6/8】 |
| G5 | $L_N$ の定義 | (4) | ★ ✔(§1–3)+ **$L_M=L_9L_{S4}$ を証明**(§3) |
| G6 | 共通円分商の構成 | (2)+(3) | ★ ✔ $\lvert Q_A\rvert\ge\varphi(d)$($\chi_{\rm cyc}$ 全射ゆえ**像に依存しない**) |
| G7 | $S_9,S_{S4}$ | (5) | ✘【ENT-GAP-5/7】 |

$$\boxed{\ \textbf{7 項中通過 2(G5・G6)。}\ \textbf{G2 は「本 gate で決めるべきこと」で、未了は起草者の宿題。}}$$

---

## §6 【GAP】・帰属・novelty

| # | 内容 | 重さ |
|---|---|---|
| ★ **【GATE-GAP-5】**(新) | **$\rho_N$ の 5 データ(基点・座標)が正典/cert に明示されていない** — TYPE-IMAGE$^\rho$ (2) の空欄 | ★★ 大 |
| **【GATE-GAP-1】** | ①→③ の橋(算術全射性)— v1 から継続(番号は $\rho$ 様式で (1)→(3) と読み替え) | ★★ 最大 |
| **【GATE-GAP-2】** | marking の型水準での未検証(両窓) | ★ 中 |
| **【GATE-GAP-3】** | ORDER の観測量(O2 Frobenius 標本)未整備 — 律速 | ★★ 大 |
| **【ENT-GAP-5/6/7/8】** | K9-BRIDGE / K9-ORDER / S4-RAM-SUPPORT / S4-ORDER(v1.4.6 §8) | ★ 中〜大 |

**帰属**: TYPE-IMAGE$^\rho$ の五対象様式・$\rho_5/\rho_{13}$ 反例 = **Sol**(便 117 P2.2)。四対象版の型事故 = 起草者(B117-1)。委嘱 = 司令塔(裁定 881)。
**本版の新規部分** = **五対象台帳 3 窓分**($M$ を第三窓として追加)/ ★ **$L_M=L_9L_{S4}$ の証明**($\ker\rho_M=\ker\rho_9\cap\ker\rho_{S4}$ から・u9bit 仕様 §0 の還元を $\rho$ 様式で救う)/ **§4 の isolated 判定方針 (I3)→(I1)→(I2)**($PSL(2,8)$ の単純性が (I1) で効く見込み)/ **【GATE-GAP-5】($\rho$ の 5 データが未明示)の摘発**。

**novelty grep**: `GATE-GAP-5` `L_M=L_9L_{S4}` = 0 hit(本版初出)。

---

## §7 三致 checker の恒久要件(裁定 881・**手順の欠陥の修正**)

> ⚠ **前版の失敗**: 私の checker は**納品ファイルの当該行ではなく、メモリ上の生成文字列**を読んでいた ⟹ 「三致確認済」の申告が実ファイルと乖離(7 巡目)。
> $$\boxed{\ \textbf{恒久要件}:\ \textbf{checker は}\textbf{納品対象ファイルを再オープンして当該行そのもの}\textbf{を読む。読み先パスを cert に明記する。}}$$
> **実装**: ①`io.open(納品パス)` で**書き込み後に再読**する ②ヘッダの**加法式**と表の**行数**とフッタの**数値**の三つを同じ読み込みから取る ③checker の出力に**読み先の絶対パスと行番号**を含める。
> **本版はこの手順で自己検査した**(§8)。

## §8 自己検査(本ファイルを再オープンして実施)

本ノートには台帳ヘッダ/フッタが無いため三致検査は非該当。**適用したのは「納品ファイルを再オープンして読む」手順のみ**(§7 ①③)。
