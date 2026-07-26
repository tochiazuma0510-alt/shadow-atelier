# 検証: `search/e2-sweep-r2.g` の q_θ/q_N 自己導出

2026-07-26 数学者(Opus 5・並列委嘱)。正本: 命題 E22′ v1 / 掃引宇宙 v3+v3.1 / manifest_spec_e2_actions。

## 判定 = **(b) 誤り**。384 系に適用してはならない。

## 1. 何が誤りか(論理の飛躍)

導出は $q_\theta(\bar f)=\theta(s\bar f)\,s\bar f$ の $\theta(s\bar f)$ を $s(\bar\theta\bar f)$ に、$\sigma(s\bar f)$ を $s(\bar\sigma\bar f)$ に、$E_m$ を $s(\bar E_m)$ に**黙って置き換えている**。これは section が $\theta,\sigma$-同変で、かつ $E_m\in s(\bar A)$ であることの仮定であり、証明されていない(そもそも本スクリプトは $A$ を実装していない — $\bar A$ の 10 次元モデルと $C$ の $2\times2$ 行列しか持たない)。正しい恒等式は、$\theta(s\bar u)=s(\bar\theta\bar u)d_\theta(\bar u)$、$\sigma(s\bar u)=s(\bar\sigma\bar u)d_\sigma(\bar u)$、$E_m=s(\bar E_m)e_m$($d_\theta,d_\sigma,e_m\in C$)と置いて

$$q_\theta(\bar f)=\underbrace{c_s(\bar\theta\bar f,\bar f)}_{\text{コードの値}}+\;d_\theta(\bar f),$$
$$q_N(\bar f)=\underbrace{c_s(\bar E_m,\bar\sigma^2\bar f)+c_s(\bar E_m+\bar\sigma^2\bar f,\bar\sigma\bar f)+c_s(\bar E_m+\bar\sigma^2\bar f+\bar\sigma\bar f,\bar f)}_{\text{コードの値}}+\;e_m+d_\sigma(\bar\sigma\bar f)+\sigma\vert_C\bigl(d_\sigma(\bar f)\bigr)+d_\sigma(\bar f).$$

collection の足し上げ(3 項の反復 cocycle)は**正しい**。落ちているのは第二項群である。

## 2. なぜ既存の自己検査で捕まらないか(★ 最重要)

落ちた項は $\bar f_0$ では**定数**、$K$ 上では**準同型**として効く(命題 E22.3 (3.1) を両者が満たすため差は定数+準同型に限られる — 手計算 + GAP 実測)。すなわち $\omega_0$ と $\pi\ell$ をずらす = **判定 $-\omega_0\in F(K)$ を直接ひっくり返す**部分だけが欠けている。(3.1)・(6.2)・v3.1 F12.3 のいずれも**通ってしまう**。実測(GAP・登録 320 系全数、スクリプトは scratchpad):

| 検査 | 結果 |
|---|---|
| (4.1) $B(u,v)-B(v,u)=\Lambda(\beta(u,v))$、$\mathcal N_C=0$、$\operatorname{im}\Lambda=\langle(t_5+t_6,0)\rangle$ | PASS(spec 側は健全) |
| (3.1) を候補式が満たすか(320 系・生成元 640 本) | **違反 0 = 検出力なし** |
| **$K$ の構造(新事実)**: 全 320 系で全生成元が $k_w=0$ かつ $k_p=k_q$ | PASS ⇒ $\beta\vert_{K\times K}=0$、$\pi B\equiv0$ |
| 候補式の $\mathcal Q\vert_K$ | **恒等的に $0$**($c_s(\bar\theta k,k)=k_w(\cdots)=0$) |

⇒ 候補式では**二次段(③)が丸ごと消滅**し、$F=\pi\ell$(準同型)に退化する。(6.2) と F12.3 は**空虚に PASS**。真の $\mathcal Q\vert_K$ は $\beta\vert_K=0$ より準同型だが**零とは限らず**、その値は落とした $d_\theta,d_\sigma$ が全部である。
⇒ そのまま走らせると候補式は **320 系中 216 系を不可解**と報告する。`universal_class5_congruence_obstruction` の見出しが、未証明の零仮定から出る。

## 3. 副次の欠陥

- **P-1**: 使われた $c_s(a,b)=a_w(b_p,b_q)$ は Hall 順序を**降順**に取った section の cocycle。v3 §1.3 の正本(昇順 $s=w^{a_1}p^{a_2}q^{a_3}\cdots$)は $c_s(a,b)=-(a_pb_w)t_5-(a_qb_w)t_6$。定理 E22′ T2(section 独立性)により最終の $\omega$ は変わらないが、証明書の `section_convention` が事実と食い違う。
- **P-2**: ヘッダの「$\operatorname{im}\Lambda=\langle(t_5+t_6,0)\rangle$ を再現することで手計算検証した」は非論理。$\operatorname{im}\Lambda$ は $\theta\vert_C$ と $\mathcal N_C$ だけで決まり、$c_s$ を一切検査しない。
- **無傷**: ITEM 1(スモーク)は線型段のみを使う。`certificates/e2sweep/smoke_negative_c5_m5.json` は本件の影響を受けない。β の「非零ブラケットは $[w,p],[w,q]$ のみ」も正しい。

## 4. 修理の型(実装への発注仕様)

$\bar A_j$ 座標上の $C_j$ 値関数 $d_\theta,d_\sigma:\bar A_j\to C_j$ と定数 $e_m\in C_j$ を**実際に構成**すること。route N = $\gamma_2/\gamma_6$ の Hall collection 多項式(線型部 = $\theta(x_i),\sigma(x_i)$ の $t_5,t_6$ 成分の $2\times10$ 整数行列、二次部 = $\binom{a}{2}$ 型 collection 補正)、route G = $A_j$ の PC presentation 上の**直接の群積**(v3 §4 の指定どおり)。これが【GAP-E22a】の中身そのもの。**発射条件**: v3 §3.3(C)/E22′ §6.3-8 の `independent_recheck`(checker が群の積から $\theta(f)f$ と $E_m\mathcal N(f)$ を再計算)を先に通すこと — 現行モデルには $A_j$ が無いのでこれは実行不可能であり、それが今回の誤りを一発で露見させる唯一の門である。
