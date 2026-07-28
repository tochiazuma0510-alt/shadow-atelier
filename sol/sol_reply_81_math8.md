# 便 81 返信 — 第一撃・等号反例・追補 (n)/(o) 監査

## 0. 総合判定

**総合判定: FAIL（部分採択）。**

ただし主菜については明確に切り分ける。

- **KERNEL-NONABELIAN 第一号は採択する。** `W-D-A16-11a` の二つの
  \(m=0\) shadow が核内で非可換であることは、GAP judge とコード非共有の
  Python/SymPy 構成的 witness が一致しており、工房語彙で
  **cross-checked** に上げてよい。
- `W-A-B3idx162-s1` は
  \[
  G_N\cong C_6,\qquad \operatorname{Im}\widetilde\chi\cong C_2,\qquad
  \ker\widetilde\chi\cong C_3,\qquad [G_N,G_N]=1
  \]
  を独立 Todd–Coxeter レーンが再構成した。これは **TYPE-L の等号第二反例を
  cross-checked で確定**する。
- I24-P1 v2 の係数 \(+4\) assert、追補 (n) について便 80 で指定した五例、
  normalizer の六修理は実装され、申告されたテスト総数も再現した。

一方、現 bundle 全体の封緘と EP v7 発射を止める blocker は次の四点である。

1. Ree 不等式自体は正しいが、逆設計文書が掲げる「初等証明」の推論は成立しない。
2. \(\Xi\)-制限は isotropy の正例集合を完全列挙できる一方、制限外の
   pre-settled 候補を数えない。従って A16 証明書の
   `settled_total_evaluated=880` / `settled_all_pass=true` は、judge v1.2 が
   定義した意味では偽である。
3. equality v2.2 には、撤回済み KE-P\(^{\prime}\) をなお生かす旧文、
   `abs_PN` の型混同、独立レーンの状態札の旧記述が残る。
4. 追補 (n) は指定五例を閉じたが、lane A が W-4 の重複 entry を ABSENT に
   落とし、retired key 併存を受理し、壊れた内側 entry では crash/通常 FAIL に
   なる。追補 (o) v2 もまだ全状態に対する一意な合成関数になっていない。

「verified」は Lean 証明に予約する。本便で verified へ上げる主張はない。

### digest 照合

依頼に列挙された 11 blob はすべて SHA-256 が一致した。

| artifact | SHA-256 |
|---|---|
| `docs/notes/wac_reverse_design_v1.md` | `ab52c4a05c313a5b7a542cb900e6e75389f347e8811f67203d8e60a50875ea93` |
| `search/certs/strike_a16_full_20260729.json` | `3d35594306b1109c572652a606f2dcbdd6c12a2312482b4e93d634d89fc016bb` |
| `search/strike-a16.g` | `b0aa188c256a6fbfefdf866b1db5254078dd13b8263e769c4c1f971671b520bb` |
| `search/strike-witness-recheck.py` | `9a6abbc8cdbbefb3b2445f2b2e57b377b386eb90715240c0280f6cc26e0ef83b` |
| `search/certs/strike_a16_witness_recheck_20260729.json` | `2dc4d245e5e763822b3fca5472517f500060d3a50d105c65af56ded3cf96e4b3` |
| `search/kep-cx-recheck.py` | `96bb566b3535fdcf8f79333324d95261543b2ed3ce9bf14189ada6fecb17b1a8` |
| `search/certs/kep_counterexample_idx162s1_20260729.json` | `fee6e1b4e50d60a0890ceeba6ea5173139821e1283bcb945086f2965ff63962e` |
| `docs/notes/kerchi_equality_v2.md` | `e7eb3518cec889f87919604733389edb403148de9965e62bf50258238b337c53` |
| `docs/notes/cert_shape_interpretation_addendum_o_v2.md` | `aca55bfe41327397bb2edf0b3aff5170c803e4ca8efdde81f86e95a4d1de0a60` |
| `search/certs/i24p1_measurement_v2_20260729.json` | `085c130f9016ee2e34aa564676d18e168eea3d61926e243e120e25e8bb7f5bc3` |
| `search/certs/kerchi_judge_v13_calibration_20260729.json` | `580a04233156b56a277467c65c893964cb4bd0a8572edd06ad334f8efec9781e` |

---

## 1. 第一撃 `W-D-A16-11a`

### F81-1.1 — 逆設計 §0–§1: PASS

補題 0.1、補題 0.2、命題 0.3、系 0.4 は紙上で整合している。

- \(c\in N\) の有限窓と \(C_2*C_3\cong PSL_2(\mathbf Z)\) の有限商の対応は
  正しい。
- 命題 0.3 の Goursat 使用も正しい。完全群 \(G\) の商は完全である一方、
  \(S_3\) の非自明商に完全群はないので、両射影に全射な部分直積の共通商は
  自明である。
- \(F_2\) の像が \(G\times1\) 全体になる指数論法、および
  \(P=\langle s_1^2,s_2^2\rangle\cong G\) も正しい。
- \(C_{S_n}(x)=\prod_\ell(C_\ell\wr S_{m_\ell})\) より、\(A_n\) 標的で
  Hol 必要条件を生きるには同じ長さの巡回が五本以上必要、という補題 1.1
  も正しい。

### F81-1.2 — Ree 不等式: 主張 PASS、掲げた初等証明 FAIL

補題 2.1 の
\[
c(a')+c(b')+c(u')\le n+2
\]
は正しい。推移的な積 1 の三置換から得る Riemann–Hurwitz、または同値な
dessin の Euler 標数で従う。

しかし 103 行目の初等証明は、そのままでは成立しない。そこで示しているのは

1. 互換の総数 \(L=\sum_\sigma(n-c(\sigma))\) のグラフが連結なので
   \(L\ge n-1\)、
2. 積が恒等なので \(L\) は偶数、

までである。これだけから出るのは「\(n-1\) 以上の最小偶数」であり、
\(L\ge2(n-1)\) ではない。

初等証明を残すなら、次の一段を実際に書けば修理できる。互換を左から掛けた
途中積の巡回数を追うと、一回ごとに巡回数は \(1\) 増減する。恒等から始まり
恒等で終わるので merge 回数と split 回数は等しい。一方、累積互換グラフを
連結にする少なくとも \(n-1\) 本は、その時点で異なる連結成分を結ぶ
merge である。従って merge \(\ge n-1\)、ゆえに
\[
L=2\,\#\mathrm{merge}\ge2(n-1).
\]
この補足を書くか、Riemann–Hurwitz を正式に引用するまで、
「文献要請なし・上の初等論法で自足」は差戻しとする。

### F81-1.3 — 定理 2.2 の \(A_{13}\) 否決: 条件付き PASS

Ree 補題を正しく供給すれば証明は通る。

- \(E/\langle\bar c\rangle\) の \(A_{13}\) への共役作用像は
  \(\operatorname{Inn}(A_{13})=A_{13}\) を含むため 13 点上推移的。
- Ree から \(c(u')\le3\)。
- \(x=u'^2\) に同長巡回を五本作るには、\(u'\) の三巡回成分すべてが
  長さ \(2L\) であるか、二つが \(2L\)、一つが \(L\) でなければならず、
  それぞれ \(13=6L\)、\(13=5L\) を要求して不可能である。

従って「\(P_N\cong A_{13}\) の窓は Hol 必要条件を生きない」
「監査 §7.3 の七巡回標的は持ち上がらない」は正しい。

ただし表題と注の「\(A_{13}\) は \(B_3\)-窓に持ち上がらない」は強すぎる。
証明は \(P_N\cong A_{13}\) の窓そのものの不存在を示していない。
示したのは、**仮にその窓があっても \(x,y\) の二中心化群は可解であり、
壁標的にはならない**ことである。回答札は

> \(A_{13}\) の壁適格な持ち上げ = NO

と書くべきで、「\(A_{13}\) 商の存在 = NO」と読める表現は避けること。

### F81-1.4 — 定理 2.3 と \(n=16\): 条件付き PASS（計算候補札）

`enum2.g` と `a15c.g` の完全性の組み方は妥当である。特に \(n=15\) は、
固定した \(u'\) に対する \(C_{S_{15}}(u')\)-軌道を集め、その総数が構造定数
72 / 120 に達した時点で全解を覆うので、ランダム探索を「NOT FOUND」の
根拠にしているのではない。

ただし次の状態札が必要である。

- \(n=12,15\) は GAP 4.16.0 一系統であり、同じ GAP 内の構造定数と列挙の
  一致は強い内部相互監査だが、cross-checked ではない。
- `enum2.g` の明示範囲は \(n=9,\ldots,16\) である。定理が \(n\le15\)
  と書くなら \(n=7,8\) を本文で消す必要がある。これは容易である。
  \(n=7\) では五不動点を除く二点上で \(\operatorname{ord}(x)\ge3\) は不可能。
  \(n=8\) では唯一の候補 \(x=(3)(1^5)\) に対し、\(u'^2=x\) なら
  \(c(u')\ge1+\lceil5/2\rceil=4\) だが、Ree 上界は
  \(4+2\cdot2+2-8=2\) で矛盾する。
- 従って定理 2.3 は「紙上補題 + GAP 完全列挙による theorem candidate」
  であり、純紙上定理や verified としては記録しない。

\(n=16\) の明示生成対、\(E=A_{16}\times S_3\)、19 点表示、指数、
\(N_{\rm ord}=11\)、中心化群 \(C_{11}\times A_5\) と
\(C_{11}\times S_5\) は整合する。Python witness も
\(|A_{16}|=10{,}461{,}394{,}944{,}000\)、braid、\(c=1\) を別系統で再計算
しており、存在標本としては十分である。

### F81-1.5 — \(\Xi\)-制限: 正例の完全性 PASS、settled 会計 FAIL

命題 3.1 は正しい。settled shadow なら \(T_{m,f}\) は \(P_N\) 上に
\[
x\longmapsto x^{2m+1},\qquad
y\longmapsto f^{-1}y^{2m+1}f
\]
という自己同型を誘導するので、候補 \(f\) は
\(\operatorname{Stab}_{\operatorname{Aut}(P)}(x)\) と
\(C_P(y^{2m+1})\) から作る有限個の coset に必ず入る。従って
\(\Xi\) 内を尽くし、各候補へ従来の (F2)、generation、Bq-settled を
再適用すれば、**実際の isotropy shadow の正例集合を漏れなく列挙できる**。

しかし v1.3 は同時に、v1.2 の settled counter の意味を壊している。
三つの旧 (F2) 条件を通った全候補を \(\mathcal H\)、\(\Xi\) 必要条件を
通る候補を \(\mathcal X\)、settled shadow 集合を \(\mathcal S\) とすると
\[
\mathcal S\subseteq\mathcal H\cap\mathcal X.
\]
Xi scan が示したのは
\[
\lvert\mathcal H\cap\mathcal X\rvert=880,\qquad
\text{その 880 件がすべて settled}
\]
である。従って \(\lvert\mathcal S\rvert=880\) はよい。一方
\(\mathcal H\setminus\mathcal X\) は一件も列挙していない。そこに候補があれば
命題 3.1 の対偶により必ず **unsettled** だが、その個数は未測定である。

従って現 JSON の

```text
settled_fail_count       = 0
settled_total_evaluated  = 880
settled_all_pass         = true
```

を、judge 113–120 行の定義
「旧 (F2) 三条件を通った全候補が settled だった」と読むことはできない。
この三欄から isolated 相当を読んではならない。正しい schema は例えば

```text
isotropy_complete_by_xi_prop31 = true
xi_f2_candidates_evaluated    = 880
xi_settled_pass_count         = 880
xi_settled_fail_count         = 0
pre_xi_f2_candidate_count     = UNKNOWN
pre_xi_settled_fail_count     = UNKNOWN
isolation_status              = UNKNOWN
```

である。`legacy_candidate_count` は
\(|[P,P]|\times\#m\) という raw loop 予算であって
\(|\mathcal H|\) ではない。したがって \(1.2\times10^7\) は
**scan-space 圧縮率**としては正しいが、settled 判定母集団の圧縮率とは
呼ばないこと。

なお `chi_image_order=10=\varphi(22)` は、得られた正例集合上で像を直接
数えているので、isolation を使わず **観測された全射**と判定できる。
`chi_surjective_assert=true` の値自体は正しいが、
`c_in_N` を isolated proxy とする説明から切り離し、
`chi_image_full_observed=true` として記録すべきである。
A16 本走の `crosscheck_vs_EnumerateReducedHexagon` は `null` であり、
小窓の calibration は実装回帰であって 880 元集合の独立再列挙ではない。

### F81-1.6 — KERNEL-NONABELIAN 第一号: cross-checked PASS

独立 witness の論理鎖は十分である。

1. 両 \(f\) について charming、(F2) の二 hexagon 条件、generation を
   SymPy が再計算している。
2. 各 \(f\) について
   \[
   Hs_1H^{-1}=s_1,\qquad
   Hs_2H^{-1}=f^{-1}s_2f
   \]
   を満たす \(H\in C_{\operatorname{Sym}(19)}(s_1)\) を具体的に発見した。
   よって \(T_{0,f}\) は \(B_3/N=\langle s_1,s_2\rangle\) 上の
   \(\operatorname{Ad}(H)\) そのものであり、P-level proxy でなく
   full Bq-settled である。
3. \(x,y\) が \(P=A_{16}\) を生成するので、\(P\) 上の実現子 \(h_1,h_2\) は
   \(E_{0,f_i}\) を一意に定める。
4. (3.53) の二順序
   \(f_1E_{0,f_1}(f_2)\) と \(f_2E_{0,f_2}(f_1)\) が異なる。

従って二元は \(\ker\widetilde\chi\) 内で非可換であり、
**KERNEL-NONABELIAN 第一号**は cross-checked で確定する。

証明書の小修理は二点ある。現在の `witness_valid` は P-level proxy と
非可換性だけを論理積にし、`bq_settled_constructive.f1/f2.H_found` を
含めていない。今回は `all_asserts_pass=true` に Bq 二 assert が入るため
結論は変わらないが、将来の fail-open を防ぐため `witness_valid` 自体にも
二つの `H_found` を入れること。また `f2_conditions.*.settled_note` に残る
「full Bq は未検査」という旧文を現 scope note と一致させること。

### F81-1.7 — 880/88/22 と「第三機構」: 条件付き PASS

次の数値は GAP 単系統である。

\[
|G_N|=880,\quad |\ker\widetilde\chi|=88,\quad
|\operatorname{Im}\widetilde\chi|=10,\quad
|[G_N,G_N]|=22,\quad G_N''=1.
\]

従って単系統 candidate としては
\[
\ker\widetilde\chi\supsetneq[G_N,G_N],\qquad
[\ker\widetilde\chi:[G_N,G_N]]=4
\]
であり、等号反例になる。これは「等号第三反例候補」として受領するが、
独立 witness が確定したのは核の非可換性までであり、位数 88/22 と
導来列までは cross-check していない。

受領数値からはさらに
\[
[G_N,G_N]\cong C_{22},\qquad
G_N/[G_N,G_N]\ \text{は位数 }40\text{ の可換群},\qquad
\ker\widetilde\chi/[G_N,G_N]\ \text{は位数 }4
\]
と読める。核は位数 \(88=2^3\cdot11\) なので Burnside の
\(p^aq^b\) 定理だけでも可解であり、非可換 witness と
\(G_N''=1\) を合わせれば核自身の可解長は 2 である。

ここで **「A16 = 非可換核機構」という命名はまだ早い**。核が非可換である
ことは、なぜ位数 4 の商
\(\ker\widetilde\chi/[G_N,G_N]\) が残るかを説明しない。
これは第三の **標本**ではあるが、第三の **機構**は
\(C_4\) か \(C_2^2\) か、T-B の transgression/coinvariant のどこが残したかを
決めて初めて成立する。

「hexagon が何を殺したか」について現時点で安全に言えるのは次である。
Hol 上界の
\[
C_P(y)\cong C_{11}\times A_5,\qquad
\operatorname{Stab}_{\operatorname{Aut}(P)}(x)\cong C_{11}\times S_5
\]
は 3,5-primary と非可解 \(A_5\) 成分を許すが、実際の核は
\(\{2,11\}\)-群の位数 88 に縮み、5-primary は \(\chi\) の像側にしか
現れない。従って非可解 ambient factor は実際には全く実現されなかった。
ただしこれを hexagon 単独の効果と断定するには、\(\Xi\)、charming、
(F2)-1、(F2)-2、generation、settled の各段階別 survivor count が要る。

以上より「この窓でも非 metabelian 壁は立った」は、GAP 単系統の
metabelian 観測として PASS。「Hol 必要条件を生きたことは陽性判定でない」
という逆設計文書自身の注意も正しい。

---

## 2. 等号第二反例と equality v2.2

### F81-2.1 — `idx162-s1`: cross-checked PASS

独立レーンは GAP の表や helper を読まず、29 個の再構成語と braid relator
から SymPy Todd–Coxeter で位数 162 の商を作り直している。そこから

- \(P_N=\langle x,y\rangle\) の位数 27、\([P_N,P_N]\) の位数 3、
- 全 6 shadow と Bq-relator による settled、
- (3.53) の Cayley 表、
- \(G_N\) の位数 6 と可換性、
- 核位数 3、像位数 2、全射性

を再計算した。GAP v5 と 13 項目が一致しており、
\[
\boxed{\ker\widetilde\chi=C_3\ne1=[G_N,G_N]}
\]
は cross-checked の等号反例である。

機構 B2 も正しい。\(Q_N=C_2\) は巡回なので
\(\Lambda^2Q_N=0\)。さらに \(G_N=C_6\) は可換なので共役作用は自明で、
\[
(\ker\widetilde\chi^{\rm ab})_{Q_N}=C_3.
\]
従って T-B は \(C_3\) 全体を coker に残す。これは \(L\) の重み 2 生存とは
別機構である。

P80-A の provenance については NOTE が残る。29 語は同じ quotient を
再構成するには十分だが、同じ \(N\) に一意な canonical UID ではない。
証明書冒頭の `canonical_id_words (LID-1 run-independent identity)` と
`window_uid="W-A-B3idx162-s1"` は P80-C 未実装のままである。
`v5_source_canonical_id_words` は `v5_source_reconstruction_generators` へ改名し、
恒久 UID は generator-labelled Cayley table digest にすること。
また Todd–Coxeter 後に table completeness を明示 assert すると capsule が
さらに閉じる。これらは今回の数学的 cross-check を無効にはしない。

### F81-2.2 — equality v2.2: FAIL（内容の核は採択）

採択できる修理は次である。

- 補題 \(\chi\)-DEG の対象を
  \(P_N=F_2/N_{F_2}\) に直したこと。
- F2-source と B3-settled の間を BRIDGE として open に戻したこと。
- KE-P、KE-P\(^{\prime}\) をともに撤回したこと。
- idx162 を B2、\(L\) を重み 2 と分離したこと。
- KE-j を retrospective heuristic に格下げしたこと。
- v5 の分類個数 `EQUAL 62 / TYPE-0 3 / TYPE-L 1` 自体。

しかし v2.2 完成 claim は次の差分を消すまで認めない。

1. §3.2 はなお「生き残るのは §11 の全射ゲート版 KE-P\(^{\prime}\) のみ」
   と書き、143 行付近も KE-P の篩用途を現在形で残す。§11.1 でも撤回札の
   直後に「篩としての用途は保たれる」「依然未証明」と書く。
   歴史節として残すなら全段落を明示的な「v2.1 時点の失効記録」へ囲むこと。
2. §12.2 は idx162 を「独立レーン進行中・第二反例候補」、
   §12.5 KE-m も「進行中」とする。現在は cross-checked 第二反例である。
3. §11.4(c) の「この窓では \(|P_N|\) は証明書に出ていない」は偽である。
   `abs_PN` は judge の \(P_N=F_2/N_{F_2}\) の位数であり、idx126 では 21。
   一方、§12.3 表と KE-j は `abs_PN` を一般に \(|PB_3/N|\) と表示する。
   v5 の 66 行中 10 行では
   \[
   \texttt{abs\_PN}\ne \texttt{abs\_Bq}/6,
   \]
   なので一般には同じ欄ではない。PB quotient が必要なら
   `abs_Bq/6` を別型で導出すること。今回の四表示行では偶然一致しているだけである。
4. §12.2 の「v5 66 窓中 TYPE-L \(\ge2\)」は、同節の census
   `TYPE-L 1` と衝突する。正しくは「v5 に 1、別 universe の atlas に \(L\)」
   であり、同じ母集団の個数に足さない。
5. §12.3 の表題「非 EQUAL の全行」は、その直下に
   `idx6-s1 = TYPE-0(等号・自明)` を含む。表題は
   「非 default 分類の全行」または「TYPE-0/TYPE-L 全行」とすること。

従って equality 文書は v2.3 の小差分再提出を求める。idx162 の反例確定や
B2 機構そのものを差し戻しているのではない。

また便の「反例 3 個・機構 3 種」は、次のように限定すべきである。

> substantive 標本は \(L\)、idx162、A16 の三つ。機構同定済みは前二つ。
> A16 は \(\ker/[G,G]\) の位数 4 まで観測した第三標本で、機構は未同定。

TYPE-0 の idx126 兄弟は別会計にする方針でよいが、数学的にはもちろん等号を
破る標本である。「反例」という裸の語を使うときは TYPE-0 を除いた個数なのか
明記すること。

---

## 3. 手続き監査 — FAIL / NOTE 二段

### FAIL

#### F81-3.1 — 追補 (n) の「完遂」は未達

申告された回帰はすべて再現した。

```text
node search/ninfty-selftest-lanea.mjs              61/61
python search/test_ninfty_laneB.py                 173/173
python search/test_ninfty_legacy_normalizer.py      51/51
```

便 80 の五つの lane A probe、および normalizer の六修理は閉じている。
しかし accepted universe を一段外から当てると、まだ三つ fail-closed 残差がある。

1. v3 条項 7 は W-4 を divisor object ごと厳密 1 entry とするが、lane A は
   `e.length === 1 ? e[0] : undefined` とし、0 件 **または複数件**を
   `ABSENT` にする。lane B は複数件を正しく MALFORMED にする。
2. lane A の `classifyChartOverlapEntry` は retired
   `per_overlap_witnesses` の併存を見ない。直接 probe では
   canonical ABSENT + retired key が `ABSENT`、canonical PRESENT と
   retired key が矛盾しても `PASS` になった。normalizer と lane B が
   ambiguous として拒否する規則に反する。
3. PRESENT の内側 entry schema を検査しない。直接 probe の結果は

   ```text
   {status:PRESENT, entries:[null]}  -> TypeError を throw
   {status:PRESENT, entries:[{}]}    -> FAIL
   ```

   である。前者は crash、後者は schema MALFORMED を算術 FAIL に潰している。

修理は lane A にも「外側の一意性」「retired key 不在」「内側 entry の必須欄と
型」を一つの schema gate として置き、いずれも top-level MALFORMED へ
上げること。上の四ケース（重複、retired 併存、内側 null、内側欠品）を
end-to-end regression に加えるまで、追補 (n) 発効は FAIL とする。

#### F81-3.2 — 追補 (o) v2 はなお proposal、EP v7 発射不可

二経路と基本合成表の方向は正しい。しかし全入力に対する一意な関数として
まだ不足がある。

- 表の `MALFORMED | 任意` は R1 が MALFORMED の向きしか字面上覆わない。
  他行では明示した「逆も」がこの行にはないため、
  `R1=PASS, R2=MALFORMED` 等の結果が未定義である。
- 「両経路併存時は同じ claim/object を digest で束縛」という原則はあるが、
  claim digest 不一致の遷移が PASS/PASS にしか書かれていない。
  FAIL/FAIL、FAIL/PASS、FAIL/ABSENT で異なる claim を混ぜてもよいのかが
  表だけでは決まらない。非 ABSENT が二本あるなら、status を合成する前に
  claim digest 一致を要求し、不一致は常に CONFLICT とすべきである。
- 「各 route に全五欄必須」は ABSENT/MALFORMED にも同じ shape を要求する
  読みになる。PASS は全域 count/coverage を要し、FAIL は反例 locus、
  ABSENT は受領側が導出した欠品 mask、MALFORMED は schema error を持つ、
  という status 別必須欄を定義すべきである。
- `checked_domain_count` が何と一致すれば「全点」なのかが未束縛である。
  expected domain は native divisor/map digest から受領側が導出し、
  `coverage_digest` はその canonical domain の digest と一致することを
  PASS 条件に入れる必要がある。
- `route_status` も producer 入力欄ではなく、受領 verifier が上記検査から
  生成する出力欄であることを明記すること。

最小の全関数は次で足りる。

1. 各 route を receiver が ABSENT/MALFORMED/PASS/FAIL に分類。
2. どちらかが MALFORMED なら向きによらず INTEGRITY_STOP。
3. 非 ABSENT が二本なら claim digest を比較し、不一致なら CONFLICT。
4. PASS/FAIL が衝突すれば CONFLICT。
5. 残りは FAIL が一つでもあれば FAIL、PASS が一つでもあれば PASS、
   両方 ABSENT のみ ABSENT。

これを v3 に明記するまで `(o) v2` は発効させず、EP v7 の最終 record を
発射しないこと。

### NOTE

#### N81-3.1 — I24-P1 v2: PASS

`node search/i24p1-u-h3.mjs` を再走し 17/17、終了コード 0 を確認した。
検査 (9a) は order 6、(9b) は係数 \(+4\) を別々に assert している。
\[
t=4x^6+O(x^7),\qquad
\frac{t}{1+t}=4x^6+O(x^7)
\]
なので凍結予言の **回帰 HIT** という呼称も正しい。P80-B の observable、
uniformizer、cusp、normalization、prediction digest も certificate に入った。

provenance 上の小 NOTE として、現在の Node script 自体は JSON を生成せず、
certificate は raw output を転記した別 blob である。今回は私の再走が
17 行と一致したので受領できるが、恒久版では runner が stdout digest と
exit code を含む receipt を直接生成するか、`generated_by` を
`transcribed_from_run` と分けるとよい。

#### N81-3.2 — judge v1.3 較正: 部分 PASS

三行の一致は真であり、D1-p5 と W-C-\(N5{\rm cong}\) が同じ窓であることも
正直に申告されている。従って実質二窓で、legacy と Xi の **採択 shadow 集合**
が一致した較正として PASS。

ただし二窓とも legacy `settled_fail_count=0` であり、F81-1.5 の会計事故を
検出できない。negative fixture として `idx126-s2` または `s3`
（legacy は 6 pass + 6 settled fail）を入れるべきである。期待値は

- actual isotropy shadow 集合は legacy/Xi で同じ 6、
- legacy pre-Xi settled fail は 6、
- Xi はその 6 fail を検索前に除くので、同じ counter 名で「0」と比較しない、

である。この fixture を入れると、正例集合の完全性と isolation 会計を
別欄にする必要が機械的に露出する。

P80-C が v1.4 待ちであるとの申告は正しい。従って現 v1.3 を canonical UID
実装済みとは扱わない。

#### N81-3.3 — legacy normalizer: 指定修理は PASS

完全 canonical 判定、`entries`-without-status 拒否、旧新配列併存拒否、
legacy schema ID、retired key 除去、in-place 非変更はコードと 51/51 で
確認した。F81-3.1 は normalizer のこの部分を差し戻すものではなく、
normalizer を通さず raw canonical input を読む lane A の残差である。

---

## 4. ★教材

1. **必要条件による prefilter は正例集合を完全にできても、負例会計を保存しない。**
   \(\mathcal S\subseteq\mathcal X\) は isotropy の漏れなしを保証するが、
   \(\mathcal H\setminus\mathcal X\) の settled failure 数は与えない。
2. **定理が正しくても、掲げた証明が正しいとは限らない。**
   「連結だから \(n-1\)、偶数だから \(2(n-1)\)」には、merge/split の
   釣合いという本質的一段が抜けていた。
3. **局所 witness の cross-check と全群 census の cross-check を分ける。**
   A16 の二元非可換性は二系統だが、880/88/22 と導来列はまだ GAP 一系統である。
4. **撤回札を付けただけでは旧命題は死なない。**
   後続 bullet が「用途は保たれる」と現在形で残れば、文書は二つの裁定を同時に
   発行してしまう。
5. **テスト件数は accepted universe の証明ではない。**
   61/61 は指定五例を閉じたが、重複 entry、retired key、壊れた内側 entry は
   なお別分岐に残っていた。
6. **状態合成表は対称かつ全域でなければ fail-closed ではない。**
   `MALFORMED | 任意` の片向き省略や、FAIL/FAIL の claim 不一致未定義を
   prose の善意で補ってはならない。
7. **新しい標本と新しい機構を同一視しない。**
   A16 の指数 4 coker は第三標本だが、非可換核という事実だけではその coker の
   発生源を説明していない。

---

## 5. 共同設計者発案（常設）

### P81-A — `A16-kernel-structure/v1`

次工程は単なる SmallGroup 名当てでなく、次を一 capsule にする。

```text
G_order / K_order / Gprime_order
Kprime_order / Z(K)_order
K/Gprime = C4 | C2xC2
G/Gprime の不変因子
Sylow-11 の作用と補群
Im(Xi) / ker(Xi)
T-B transgression image / coinvariant / coker
```

受領数値だけで \(G'\cong C_{22}\)、\(|K/G'|=4\) までは決まっている。
ここから \(C_4\) 対 \(C_2^2\) と T-B map を決めれば、A16 を初めて
「第三機構」と命名できる。

### P81-B — `A16-filter-ledger/v1`

「hexagon が何を殺すか」を答えるため、各 charming \(m\) について

```text
Xi raw
f in [P,P]
F2-inversion
R_tau
generation
Bq-settled
final shadow
```

の survivor count と集合 digest を記録する。これにより \(A_5/S_5\) の
3,5-primary がどの歯で消えたかを、Hol 上界との比較として可視化できる。
`settled_*` は pre-Xi と post-Xi を別 namespace にする。

### P81-C — Ree proof capsule

逆設計文書の補題 2.1 を、Riemann–Hurwitz 版と
「identity transposition word の merge/split」版の二証明で一枚にする。
また \(n=7,8\) の二行消去を加え、定理 2.3 の紙上範囲を実際の
`enum2.g` の \(9..16\) と接続する。

### P81-D — equality v2.3 delta

全文を書き直さず、次だけを差分 gate にする。

1. KE-P 系の旧現在形を historical block へ封じる。
2. idx162 を cross-checked に更新。
3. `abs_PN` と `abs_Bq/6` を別型にする。
4. TYPE census の母集団と表題を修正。
5. A16 は specimen、mechanism open とする。

### P81-E — `evidence-union/fail-closed-v2`

追補 (o) を W-6 専用 prose から独立させ、二 route の順序を swap しても
同じ結果になること、全 \(4\times4=16\) status pair に値があることを
table-driven test にする。claim mismatch と MALFORMED は status 合成より
先に処理し、coverage completeness は各 route の PASS gate に置く。

### P81-F — canonical marked-quotient UID

idx162 の 29 語は `reconstruction_generators` として保存し、別に
\((B_3/N;\bar\sigma_1,\bar\sigma_2)\) の shortlex labelled Cayley table を
canonical serialize した digest を `window_uid` にする。同じ normal subgroup
を別生成集合で書いた fixture を二つ用意し、同じ UID になることを回帰にする。

---

## 6. 監査範囲・実行記録

- turn 冒頭で対話帳を T-17 まで読み、本便向け新着がないことを確認した。
- `ops/inbox_codex/sol_task_81_math8.txt` は §0 から末尾の返信様式まで全文を
  読んだ。§1–§3 を監査し、§4 の予告は指定どおり監査対象外とした。
- 上記 11 digest を `Get-FileHash -Algorithm SHA256` で照合した。
- lane A 61/61、lane B 173/173、normalizer 51/51、I24 17/17 を再走した。
  lane A にはさらに retired key 併存と malformed inner-entry の直接 probe を
  投入した。
- A16 full GAP run、v5 66 窓の GAP 再採掘、n=15 の GAP 全列挙は再走していない。
  source と受領 JSON の相互監査である。A16/idx162 の Python script は
  実行すると指定外 certificate を書き換えるため再走せず、source 全文と
  現 certificate を監査した。
- `wall_miner_v5_20260729.json` は read-only 抽出で 66 行の TYPE census、
  `abs_PN != abs_Bq/6` が 10 行、idx126 の 6/12 settled を確認した。
- 本便で変更したのは本返信だけである。既存の無関係な dirty files には
  触れていない。
