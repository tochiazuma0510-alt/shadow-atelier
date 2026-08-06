# 実験 E-DIM5/6 — **走行前の予想値宣言(IF-FIRST・単独コミット)**

**状態札: `IF-FIRST 凍結 / 実験は 1 行も走らせていない / 本ファイルのコミット後にのみ走らせる / 封印非接触`**

- 起草: 影工房 数学者(Claude / Opus 5)・2026-08-06
- 委嘱: 司令塔 **裁定 640**(「実験 E-DIM5/6 を実行せよ。IF-FIRST: 実行前に予想値を 1 行宣言してから走らせよ」)
- 対象: `docs/notes/b_type_synthesis_design_v1.md` §3.1 の実験 E-DIM5/6。本ファイルは同ノートの versioned addendum(本体は 1 バイトも改変しない)。

---

## 1. 測る量(述語の凍結)

$L_k:=\mathrm{gr}_k(F_2)\otimes\mathbb Q=\mathrm{Lie}_k(x,y)$($\dim=2,1,2,3,6,9$ for $k=1..6$)、$\mathfrak t_k:=\mathrm{gr}_k(K(0,5))\otimes\mathbb Q$($\dim=5,4,10,21,54,125$)。

$$H_k:=\ker(1+\theta)\cap\ker(1+\tau+\tau^2)\subseteq L_k\qquad(\textbf{hexagon 斉次解空間}),$$
$$\boxed{\ \mathcal S_k:=H_k\cap\ker\bigl(\nu_k\circ j\bigr),\qquad \nu_k=\sum_{i=0}^{4}\rho^i,\quad j:x\mapsto T_1,\ y\mapsto T_2\ }$$

$\theta:x\leftrightarrow y$、$\tau:x\mapsto y,\ y\mapsto-x-y$、$\rho:T_i\mapsto T_{i+3\ (\mathrm{mod}\ 5)}$。

**較正(先に通す)**: $\dim\mathfrak t_k=5,4,10,21,54,125$ / $\dim H_3=\dim H_4=1$ / $\dim\mathcal S_3=1$ / $\dim\mathcal S_4=0$。**1 つでも外れたら実装バグとして停止し、$k=5,6$ の値を報告しない。**

---

## 2. ★ 予想値(**1 行**)

> $$\boxed{\ \dim H_5=2,\quad \boxed{\dim\mathcal S_5=1},\qquad \dim H_6=3,\quad \boxed{\dim\mathcal S_6=0}\ }$$

**根拠**: $\dim\mathcal A_5=1$($\sigma_5$)・$\dim\mathcal A_6=0$(偶数次に生成元なし)であり、$\mathcal A_k\subseteq\mathcal S_k$(HSP-SOUND)。**古典的知見では低次数で両者は一致する**(`b_type_synthesis_design_v1.md` §4・要文献確認 L-4)。ゆえに一致側に賭ける。$\dim H_k$ は $\dim L_k$ のおよそ $1/3$($\theta$ で約半分・$\tau$ で更に絞る)からの**値からの推測**であり、賭けの本体ではない。

**採点**: $\mathcal S_5,\mathcal S_6$ の 2 値のみを採点対象とする。$H_5,H_6$ は参考(外れても停止事由でない)。

---

## 3. ★ 判定文の規律(**どちらに転んでも UNKNOWN 規律** — 裁定 640 の明示指示)

| 実測 | 書いてよい文 | ★ 書いてはならない文 |
|---|---|---|
| $\dim\mathcal S_5=1,\ \dim\mathcal S_6=0$(予想どおり) | 「$k^*\ge7$(斉次水準)」 | 「class 5,6 の窓に B 型は無い」— **$k^*$ の上限は未知**。「$k^*=12$」も**言えない**(§4 の古典的知見は未確認) |
| $\dim\mathcal S_5>1$ | 「斉次水準で $\dim\mathcal S_5>\dim\mathcal A_5$ — **$k^*=5$ の candidate**」 | 「class 5 窓に B 型が存在する」— ★ **命題 SYN-0 は candidate(単系統・Sol 未監査)**。断定は便 113 の監査後 |
| $\dim\mathcal S_6\ge1$ | 「斉次水準で $\dim\mathcal S_6>\dim\mathcal A_6$ — **$k^*=6$ の candidate**」 | 同上。**さらに下記 ⚠ の非斉次留保を必ず添える** |

> ### ⚠ 非斉次留保(**$k=6$ に固有・先に書いておく**)
> $m\equiv0$ 層では深さ 5 まで hexagon は**斉次**($F_2=0$ ゆえ BCH 補正が次数 6 以上)。しかし**深さ 6 では $\tfrac12\sum_{i<j}[\tau^jF_3,\tau^iF_3]$ 型の非斉次項が初めて効く**($\theta$ 側は $\theta\mathfrak h_3=-\mathfrak h_3$ で消えるが、$\tau$ 側は $\tau\mathfrak h_3=-u_1\ne\pm\mathfrak h_3$ ゆえ消えない)。
> ⟹ **本実験が測るのは斉次(associated graded)水準の $\dim\mathcal S_6$ であり、真の解集合は「空 or $\dim\mathcal S_6$ 次元のトーサー」である。**
> ⟹ $\dim\mathcal S_6\ge1$ が出ても、**非斉次可解性が別途要る**(可解でなければ層は空 = 逆に $\mathcal S$ 側が小さくなる)。**「$k^*=6$」は candidate の中でもさらに条件つき**であることを判定文に必ず書く。
> ⟹ $\dim\mathcal S_5$ には**この留保は不要**(深さ 5 は斉次)。

**停止規則 S-ED-1**: 較正 4 項のいずれかが外れたら `CALIBRATION_FAIL / STOP`・$k=5,6$ の値を報告しない。
**停止規則 S-ED-2**: 本予想値を走行後に改稿したら `S-7′ 抵触 / STOP`。
**停止規則 S-ED-3**: 有理数厳密でなく素数法で計算した場合、**素数 2 本以上での一致**を報告に明記する(単一素数の結果を「厳密」と書かない)。

---

**本ファイルのコミット時点で、実験は 1 行も走っていない。**
