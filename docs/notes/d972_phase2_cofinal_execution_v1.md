# D972 Phase 2 — cofinal 累積交叉と深さ 2 実行票 v1

日付: 2026-08-13 / 対象: \(M=K^{(9)}\cap N_{S4}\) / 格: 紙の構成 + 有限座標計算。

本票は局所 Kummer 量を読まず、封印対象にも触れない。有限深度から全深度側の分岐を認定しない。値が 972 のままなら結論は UNKNOWN のままである。

## 1. 全 isolated refinements の有効列挙

\[
B_3=\langle \sigma_1,\sigma_2\mid
\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle
\]

は有限表示群である。次の手順は \(M\) 以下の有限指数正規部分群を重複込みで列挙する。

1. 有限集合上の乗法表を全列挙し、群公理を満たすもの \(Q\) を残す。
2. \(Q\) の生成対 \((\bar\sigma_1,\bar\sigma_2)\) を全列挙し、braid relation と生成性を有限表で検査する。
3. marked epi \(Q\twoheadrightarrow B_3/M\) で二生成元を標準生成元へ送るものを全列挙する。そのとき合成
   \[
   B_3\twoheadrightarrow Q\twoheadrightarrow B_3/M
   \]
   により \(N:=\ker(B_3\twoheadrightarrow Q)\subseteq M\) である。
4. Reidemeister--Schreier により \(N\) の有限生成系を計算する。有限群 \(Q\) 上で全 charming pair を列挙し、各 \(T_{m,f}\) がその生成系を殺すかを検査する。全 pair で \(\ker T_{m,f}=N\) となるものだけを出力する。

各検査は有限で停止する。逆に任意の isolated \(N\subseteq M\) について、marked quotient \(Q=B_3/N\) と自然な \(Q\twoheadrightarrow B_3/M\) が上の列挙に現れ、isolated の有限検査を通る。従って出力列

\[
N^{[1]},N^{[2]},\ldots
\]

は \(M\) 以下の全 isolated refinements を尽くす。重複は cofinality に影響しない。

## 2. 累積交叉 chain

有限個の先頭項を指定してから上の全列挙を続けても網羅性は変わらない。先頭を

\[
N^{[1]}:=K^{(27)}\cap N_{S4},\qquad
N^{[2]}:=K^{(36)}\cap N_{S4}
\]

とし、

\[
\boxed{L_d:=\bigcap_{i=1}^{d}N^{[i]}}
\]

と置く。2401 Prop. 3.15 を有限回用いると各 \(L_d\) は isolated であり、
\(L_{d+1}\subseteq L_d\subseteq M\)。任意の isolated \(K\subseteq M\) はある
\(N^{[j]}\) として現れるため \(L_j\subseteq K\)。よって \((L_d)\) は全 isolated refinements に対して cofinal である。

先頭二段は

\[
L_1=K^{(27)}\cap N_{S4},\qquad
L_2=K^{(27)}\cap K^{(36)}\cap N_{S4}
=K^{(108)}\cap N_{S4}.
\]

最後の等号は marked product \(G_{27}\times_{\rm marked}G_{36}\) の位数が
\(629856=|G_{108}|\) で、Prop. 3.5 が与える
\(K^{(108)}\subseteq K^{(27)}\cap K^{(36)}\) と合わせて従う。producer は SymPy の置換群 Schreier--Sims でこの位数等式を再計算した。

## 3. reduction の因数分解と包含 (6)

\(L_{d+1}\subseteq L_d\subseteq M\) なので (3.60) の二座標の還元から

\[
\boxed{R_{L_{d+1},M}=R_{L_d,M}\circ R_{L_{d+1},L_d}}.
\]

従って像は単調非増加である。また profinite 射影の錐可換性から、各 \(K\subseteq M\) について

\[
\boxed{
P:=\mathcal{PR}_M(\widehat{GT}_{\rm gen})
\subseteq \operatorname{Im}R_{K,M}
}
\tag{6}
\]

である。実際 \(\mathcal{PR}_M=R_{K,M}\circ\mathcal{PR}_K\) なので直ちに従う。

ある isolated \(K\subseteq M\) で標的元が像から欠けるなら、その \(K=N^{[j]}\) が列挙された時点で \(L_j\subseteq K\) となり、factorization により同じ元は \(\operatorname{Im}R_{L_j,M}\) からも欠ける。従ってこの運転は A 型側の有限証明書を探索する半決定である。停止深度の上界は無く、有限個の 972 から B 型側を認定することはない。

## 4. (3.60) 座標修理

旧 search/d972_phase1_v1.g の候補限定 helper は

\[
m_{\rm fine}\equiv m_{\rm coarse}\pmod{H_{\rm ord}/2}
\]

を使っていた。しかし正典 (3.60) は

\[
R_{N,H}([m,f])=(m+H_{\rm ord}\mathbf Z,\ fH_{F_2})
\]

なので、必要条件は
\(m_{\rm fine}\equiv m_{\rm coarse}\pmod{H_{\rm ord}}\) である。
\(2m+1\) の像だけの一致は \(m\)-座標の一致を代替しない。

本実行では旧 cert を結果の根拠にせず、Thm. 4.3 (4.12) の全座標を厳密な
\(m\bmod H_{\rm ord}\) で再列挙した。深さ 1 の生値は再計算後も同じであった。未実行の GAP producer search/d972_phase2_v1.g にも同じ修理を固定した。

## 5. 実行方法と有限計算

producer は Thm. 4.3 の

\[
\bigl(m,(r^{2k},r^{-2k},r^{\varkappa(m)})\bigr)
\]

を全列挙し、\(4\mid n\) の parity 条件も適用した。次に ROOF の

\[
GT(K^{(n)}\cap N_{S4})\cong
GT(K^{(n)})\times_{(\mathbf Z/18)^\times}GT(N_{S4})
\]

を \(\operatorname{Hol}(\mathbf Z/9)=\mathbf Z/9\rtimes(\mathbf Z/9)^\times\) の座標で有限列挙した。producer は SymPy 置換群で \(G_n\)、marked product、各 roof quotient の位数も独立に測った。checker は SymPy と producer helper を使わず、標準ライブラリだけで \((m,k)\) を再列挙した。

再現コマンド:

    python search/d972_phase2_coord_v1.py --hard-timeout-seconds 900
    python search/check_d972_phase2_coord_v1.py

producer は各段で search/certs/d972_phase2_coord_v1_checkpoint.json を原子的に更新し、内部 watchdog が hard timeout 時に同 checkpoint を hard_timeout として残す。

GAP 版は規約どおり gap.ps1 から二度起動したが、既存 script を含め GAP runtime 自体が couldn't create signal pipe, Win32 error 5 で起動前に停止した。従って GAP 版の出力は本票の測定根拠に含めない。

## 6. 深度と生値

| 深度 | 累積窓 | \(|\operatorname{Im}R_{L_d,M}|\) 生値 |
|---:|---|---:|
| 1 | \(K^{(27)}\cap N_{S4}\) | 972 |
| 2 | \(K^{(108)}\cap N_{S4}\) | 972 |

\(K^{(36)}\cap N_{S4}\) 単独の横断プローブも生値 972 だが、累積窓 \(L_2\) ではないため深度表へ混ぜない。

出力:

- search/certs/d972_phase2_coord_v1_20260813.json
- search/certs/d972_phase2_coord_v1_check_20260813.json
- search/certs/d972_phase2_coord_v1_checkpoint.json

有限深度 2 の後も全深度側の状態は UNKNOWN であり、chain は継続対象である。
