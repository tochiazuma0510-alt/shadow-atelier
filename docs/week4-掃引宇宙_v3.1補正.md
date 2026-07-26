本書は掃引宇宙 v3 の補正 v3.1(便 14 の HOLD 解除要求の逐語版)。実装は v3+作用式追補+本補正を正とする。

## F5. E22 §6 の二次表 — 公式は PASS、postcondition は不足

有限アーベル群
\[
K=\bigoplus_i\langle e_i\rangle,\qquad \operatorname{ord}(e_i)=n_i
\]
上の展開
\[
F\!\left(\sum_i a_ie_i\right)
=\sum_i\left(a_iF(e_i)+\binom{a_i}{2}\pi B(e_i,e_i)\right)
 +\sum_{i<j}a_ia_j\pi B(e_i,e_j)
\]
は正しい。

しかし、現在の唯一の自己検査
\[
n_iF(e_i)+\binom{n_i}{2}\pi B(e_i,e_i)=0 \tag{6.2}
\]
は、\(a_i\) を一周させたときの **\(x=0\) の場合しか検査しない**。一般の
\(x=\sum_{j\ne i}a_je_j\) に対して
\[
F(x+n_ie_i)-F(x)
=
n_iF(e_i)+\binom{n_i}{2}\pi B(e_i,e_i)
 +n_i\pi B(e_i,x)
\]
である。従って (6.2) に加えて、少なくとも次を必須にする。

1. 全 \(i,j\) について
   \[
   n_i\,\pi B(e_i,e_j)=0,\qquad
   n_j\,\pi B(e_i,e_j)=0
   \quad\text{in }\mathrm{Ob}.
   \]
2. checker が \(B(e_i,e_j)\) と \(B(e_j,e_i)\) を別々に群の積から計算し、
   \[
   \pi B(e_i,e_j)=\pi B(e_j,e_i)
   \]
   を検査する。

理論上は \(\pi B\) の双加法性・対称性から自動だが、保存された有限表が本当にその理論を実装していることの **certificate postcondition** としては省けない。特に現在は \(i\le j\) の半分しか保存しないため、対称性を保存値だけで自己正当化してはならない。

この不足は E22′ 本体の反例ではない。`central_lift_obstruction/v2` と掃引 S-4 の修理事項である。

## F12. `U-E2-nm5-r2` の停止規則 — 四点修正後に GO

### F12.1 記号衝突

v3 §4 では既に
\[
C_j=(M_j^{\bar\sigma})^{\bar\theta}
\]
を graded cokernel に使っている。一方、掃引 v3 §1.2 は
\[
C_j=C/2^{j-1}C
\]
を有限中心に使う。同じ作戦文書群で意味が衝突するため、掃引側を
\[
Z_j\quad\text{または}\quad C_j^{\mathrm{cen}}
\]
へ改名する。証明書 schema も同じ語に統一する。

### F12.2 S-3 の重複

§2.1 の「cap の事後引き上げ禁止」と §4 の
\(\mathcal N|_{Z_j}=0\) 再現失敗がともに S-3 である。停止ログが曖昧になるため、全停止規則に一意な ID を振る。

### F12.3 S-4 の補強

F5 のとおり、(6.2) に加えて
\[
n_i\pi B(e_i,e_j)=n_j\pi B(e_i,e_j)=0
\]
および
\[
\pi B(e_i,e_j)=\pi B(e_j,e_i)
\]
を全 \(i,j\) で検査する。一件でも FAIL なら非零終了し、本走査へ進まない。

### F12.4 S-6 の裁定語

\(j=1\) で \(A_1\) がアーベルであることから、直ちに「不可解なら実装バグ」とは言えない。\(P_1\) 自体は class 5 であり得るため、class \(\le4\) の E9′ はそのまま適用できない。class 5 metabelian の全 \(m\) 可解性は E19-b′ の \(c=5\) 適用に対応するが、その数値前提は現在 single-system candidate である。

従って S-6 は、

> \(j=1\) control で不可解が出たら  
> `calibration_mismatch / math_review` として即停止する。独立な E19 \(c=5\)
> witness と照合するまで、実装バグとも数学的反例とも裁定しない。

へ直す。

以上四点を versioned に反映した `r3`、または発射前の同等な凍結 errata があれば、数学面から **GO** を出せる。現行 `r2` 本文のままなら **HOLD** である。cap、二 route の独立性、有限 384 系に限定した読み、\(\mathcal N|_{Z_j}=0\) の停止自体には追加異論はない。

補正反映の確認は falsifier 不要 — 便 14 の原文が正(逐語のため)。
