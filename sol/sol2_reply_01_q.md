# sol2 便 01 — 掃引実装の q 式監査

**判定: (b) 誤り。現状の `QTheta` / `QN` を 384 系へ適用してはならない。**

**根拠:** `search/e2-sweep-r2.g` 188–215 行の式は、(i) 登録された canonical section と異なる section cocycle を用い、さらに (ii) 自己同型および \(E_m\) の section 欠損を落としている。線型条件
\[
(1+\bar\theta)f=0,\qquad \bar E_m+(1+\bar\sigma+\bar\sigma^2)f=0
\]
が保証するのは、対応する積の \(\bar A\)-成分が 0 となり、その積が \(C\) に入ることだけである。中心成分そのものが section cocycle だけになることは保証しない。

**監査範囲外申告:** 指定された 7 ファイルと `docs/所在と能力.md` 以外は読んでいない。384 系の実走査、PC presentation による route G、node/Lean 照合、および E22′ 全体の再監査は行っていない。以下は指定資料中の \(q\) 式に限る紙上監査である。

## 1. `Cs` は登録 section の cocycle ではない

掃引宇宙 v3 §1.3 の section は
\[
s(a)=w^{a_w}p^{a_p}q^{a_q}\cdots
\]
の順である。交換子規約 \([u,v]=u^{-1}v^{-1}uv\)、\(uv=vu[u,v]\)、\(t_5=[w,p]\)、\(t_6=[w,q]\) から、整数 Hall 座標では
\[
\boxed{c_s(a,b)=(-a_p b_w,\,-a_q b_w)}
\tag{1}
\]
となる（有限商では \(C_j\) の法 \(2^{j-1}\) で読む）。

最小の手展開でも、
\[
c_s(w,p)=wp(wp)^{-1}=0,\qquad
c_s(p,w)=pw(wp)^{-1}=-t_5.
\]
一方、実装の
\[
c_s^{\rm code}(a,b)=(a_wb_p,a_wb_q)
\]
はそれぞれ \(t_5,0\) を返す。これは \(p,q\) を \(w\) より前に置く別 section の cocycle であり、登録された canonical section とは一致しない。

また \(\beta\) が決めるのは
\[
c_s(a,b)-c_s(b,a)=\beta(a,b)
\]
という反対称部分だけである。(1) と実装式はどちらもこの差を満たすため、**\(\beta\) だけから実装式を一意に導いた**という論拠は成立しない。

## 2. 正しい \(q\) 式には作用欠損が要る

\(T=\bar\theta\)、\(S=\bar\sigma\)、\(e=\bar E_m\) とし、固定した section に対して
\[
d_\gamma(a):=\gamma(s(a))\,s(\bar\gamma a)^{-1}\in C,\qquad
\varepsilon_m:=E_m\,s(e)^{-1}\in C
\]
と置く。このとき \(a\in\mathcal L\) 上の正しい加法表示は
\[
\boxed{q_\theta(a)=d_\theta(a)+c_s(Ta,a)}
\tag{2}
\]
および
\[
\boxed{\begin{aligned}
q_N(a)={}&\varepsilon_m+d_{\sigma^2}(a)+d_\sigma(a)\\
&+c_s(e,S^2a)+c_s(e+S^2a,Sa)
 +c_s(e+S^2a+Sa,a),
\end{aligned}}
\tag{3}
\]
ただし
\[
d_{\sigma^2}(a)=\sigma_Cd_\sigma(a)+d_\sigma(Sa).
\tag{4}
\]
実装の `QN` にある三つの cocycle の括り方自体は (3) の後半と一致する。しかし、\(\varepsilon_m,d_\sigma,d_{\sigma^2}\) をすべて 0 と無根拠に置いている。`QTheta` も \(d_\theta\) を落としている。

指定された作用 spec が与える \(\bar\theta,\bar\sigma\)、\(\theta|_C,\sigma|_C\)、\(\beta\) だけでは \(d_\theta,d_\sigma,\varepsilon_m\) は決まらない。E22′ §5.4 が「\(\mathcal Q\) は全 10 座標に依存し得る」と警告しているのも、まさにこの Hall collection／作用欠損である。現実装の \(q\) は最初の \(w,p,q\) 座標しか見ないため、この必要情報を表現できない。

## 3. 較正点はこの誤りを検出していない

- \(\mathcal N_C=0\) と \(\operatorname{im}\Lambda=\langle(t_5+t_6,0)\rangle\) の再現は、`ThetaC` / `SigmaC` だけの検査であり、`Cs` や \(q\) の妥当性を検査しない。
- `smoke_negative_c5_m5.json` は、摂動した **線型段**の双対 witness の観測である。生成コードも `QTheta` / `QN` を一度も評価していないので、二次・障害段の較正にはならない。
- 特に \(\mathcal N_C=0\) では \(q_N\) は section 変更で修正できない。したがって (3) の欠落を「section 独立性」や \(\operatorname{im}\Lambda\) で吸収することはできない。

## 結論と修理条件

canonical Hall section に対し、実際の \(A=\gamma_2/\gamma_6\) 上の \(\theta,\sigma,E_m\) を collection して \(d_\theta,d_\sigma,\varepsilon_m\) を導出し、(1)–(4) で \(q_\theta,q_N\) を再実装する必要がある。その後、少なくとも上の二つの cocycle 単体試験と、非可換群積からの
\[
\theta(s(a))s(a),\qquad E_m\sigma^2(s(a))\sigma(s(a))s(a)
\]
の直接一致を通すまで、384 系への E22′ 適用は **HOLD** と裁定する。
