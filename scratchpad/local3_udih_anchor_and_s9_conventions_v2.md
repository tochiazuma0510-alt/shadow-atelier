# LOCAL-3 規約台帳 v2 — S4 側正規化の解消・D-6 判定・EP-DEL 実験仕様

`DIR: 972 の 1 ビット(c′)/ FRAME: B₃-gentle・IDX3`
**委嘱**: 司令塔・裁定 1717(c) の ①②③④(裁定 1719/1720 の falsifier 所見を反映)。
**v1(sha16 `55af94e165e4095d`)は改変せず並置。本 v2 が v1 を supersede する。**
**格**: §1 = `paper-proof + 機械裏取り`(決定的)。§2 = 台帳更新(確定)。§3 = 裁定。§4 = 実装仕様(candidate)。
**著者**: 数学者(Opus 5)/ 2026-08-28。**規約 (R-1)(R-2) 準拠。**

> ### v2 の変更(訂正表)
> | # | 内容 | 種別 |
> |---|---|---|
> | **W-1** | **① S4 側正規化を解消**(候補 (ii) が成立 — 正規化因子は完全立方)。SELECT の格上限を「S4 側正規化相対」から**解除** | ★ 前進 |
> | **W-2** | 私の根拠を訂正: **$u_{S4}=u_0$ の健全な根拠は producer code L118/L120 + $T=1/t$ 代数**(falsifier)。v1 §A.4 の「正本 §7.2 の語法」は**偶然正解**であって根拠にならない | ⚠ 訂正 |
> | **W-3** | **② 正本 d972 へ訂正伝播済**(§7.3.3 予言表に ⚠⚠ + 訂正表・§7.3.2 に sgn 配線罠・§7.3.5 の最大文更新・**§7.3.6 新設**) | ⚠ R-1 履行 |
> | **W-4** | **D-10(cert 同名異値)を台帳に新設** | 追加 |
> | **W-5** | **③ D-6 は閉じない**(1 行の理由つき) | 裁定 |
> | **W-6** | **④ $E_4$ は非可換の見込み ⟹ (C-β) は abelian 経路では閉じない。ただし正しい問いは「$d_i\circ\rho_o$ の像が可換か」**(より弱く、1 行で測れる) | ★ 鋭化 |

---

# §1 ★ ① S4 側正規化の解消

## 1.1 falsifier 所見(受諾)

規約 D の「両窓同一レシピ」は**不成立だった**: 二面体側は 3 点 Möbius 完全正規化済みだが、**S4 側はモデル所与の $t$ に $u_0=-1/\lim(t\,s^9)$ を当てただけ**。しかも $3^3$ 分岐点対は
$$\tau_{1,2}=\tfrac32\pm\tfrac32\sqrt{-3},\qquad \tau_1+\tau_2=3,\quad\tau_1\tau_2=9,\quad\text{min.\ poly }x^2-3x+9$$
で **ℚ 上共役な無理数対** ⟹ $(\infty,\tau_1,\tau_2)\to(0,1,\infty)$ は ℚ-有理でない。**私の v1 は S4 側の正規化を検査していなかった** — 受諾する。

## 1.2 裁定: **候補 (ii) を採用**($c'$ は残余自由度に不変・証明つき)

index-9 cusp は $t=\infty$ 上。3 点正規化は $\mu(w)=\dfrac{\tau_k-\tau_j}{w-\tau_j}$、$t'=\mu\circ t$。cusp 近傍で

$$u_{S4}^{\rm norm}=\lim_{s\to0}\frac{t'}{s^9}=\frac{\tau_k-\tau_j}{\Lambda},\qquad \Lambda=\lim_{s\to0}t\,s^9=-\frac1{u_0}.$$

$\lambda:=\sqrt{-3}$、$\lambda^2=-3$ より

$$\boxed{\ \pm3\sqrt{-3}=\pm3\lambda=\mp\lambda^3=(\mp\lambda)^3\ \ \text{— 完全立方}\ }$$

$-1=(-1)^3$ も立方。ゆえに $\mathbb Q(\zeta_3)^\times/(\mathbb Q(\zeta_3)^\times)^3$ で

$$[u_{S4}^{\rm norm}]_3=\bigl[\text{cube}\bigr]\cdot[-u_0]_3=[u_0]_3 .$$

⟹ **3 点正規化を完全に実行しても $c'$ は変わらない。$u_{S4}=u_0$ を使ってよい。**
$\tau_j\leftrightarrow\tau_k$ の入替も符号 $-1$ だけ ⟹ 無害。**二面体側と同じ性質**(§A.2 v1: $\pm2^{-7}$ が同一類)。

## 1.3 機械確認(`gate:` — `scratchpad/math_s4norm_v1.py`)

```
gate: (-sqrt(-3))^3 == 3*sqrt(-3) ?  True
      tau1+tau2 = 3 ; tau1*tau2 = 9 ; tau2-tau1 = -3*sqrt(-3)
gate: p in {19,37,73,163,181,199,271,373}   (109/127/307/397 は判別力条件で degenerate)
      cube(3*sqrt(-3) mod p) == 1                       : 8/8
      c'(u_S4 = u0)  ==  c'(u_S4 = normalised)          : 8/8      [ すべて c' = +1 ]
gate: falsifier 感度検査の再現
      p=19,37,73,163 :  c'(u_dih=2^-7) = 1 ;  c'(u_dih=2^-8) = 2 ;  flipped: True
```

> ⚠ **$2^{-8}$ の正体**: $\mu(w)=1/w$ は $\infty\to0$、$1\to1$ を送るが **$-1\mapsto-1\ne\infty$** ⟹ **3 点正規化になっていない**。⟹ **falsifier の感度検査は「3 点正規化こそが値を pin する」ことの確認**であって、私の $2^{-7}$ を否定するものではない。**$2^{-7}$ が完全正規化の値。**

## 1.4 格の更新

- SELECT の上限: ~~candidate(S4 側正規化相対)~~ ⟹ **candidate(正規化解消済・census ラベル **D-6** 相対)**。
- **$c'=+1$**: 根拠は **(i) falsifier の producer code L118/L120 明示宣言 + $T=1/t$ 代数($u_{S4}=u_0$)** と **(ii) 本節の正規化不変性** の二本立て。
- ⚠ **W-2**: v1 §A.4 で私が挙げた「正本 §7.2 の語法($u(s):=(t/s^9)(P_0)$ と呼んでいる)」は**根拠として不健全**(自分のノートの語法は producer の実装規約ではない)。**結論は維持されたが根拠は差し替える。**

---

# §2 ② 修理 3 点(R-1: 同ターンで本文に打った)

| # | 対象 | 実施 |
|---|---|---|
| **(a)** | 正本 `d972_..._v1.md` **§7.3.3 の予言表が stale**($\beta$ アンカー前提で $c'$ 列が真逆・⚠ なし = R-1 違反) | **⚠⚠ ブロック + 訂正表**を挿入し、旧表を打消線で歴史記録化。**falsifier 判読($u_{S4}=u_0$)と §7.3.6 の正規化不変性も併記** |
| **(b)** | **§7.3.2 の sgn 配線罠** | S4 行に ⚠⚠ コメントを挿入: 規約 D の正解は $u_{S4}=u_0$ なので **u0inv 基準なら sgn = −1**。cert 見出しが `input_u0_inverse` を第一級で出すため**素直実装は逆ビット**。併せて `Sanc := cube(u_dih)`(β を使わない)行を追加 |
| **(c)** | **ds4 cert の同名異値** | 台帳 **D-10** に新設(下記) |
| 追加 | §7.3.5 の最大文 | 打消線 + **§7.3.6 新設**(S4 側正規化の解消・機械出力つき) |

---

# §3 規約台帳 v2(v1 §B の D-1〜D-9 を継承・更新分のみ)

| # | 項目 | 宣言(v2) | 決定者 | 状態 |
|---|---|---|---|---|
| **D-1** | 規約 D | v1 のまま。**追加**: 「両窓とも**3 点 Möbius 完全正規化**を行う。S4 側の因子 $\tau_k-\tau_j=\pm3\sqrt{-3}$ は完全立方ゆえ mod 3 で無害(§1.2)」 | 数学者(確定) | **更新** |
| **D-2** | アンカー | $S_{\rm anc}=\mathrm{cube}(u_{\rm dih})$、$u_{\rm dih}=\pm2^{-7}$。**$\beta$ 不使用**。cert 必須欄 `anchor_source:"u_dih"` | 数学者(確定) | 不変 |
| **D-5** | $u_{S4}$ の同定 | **$u_{S4}=u_0$(= cert の `u0_inverse` の逆数)。**根拠 = producer code L118/L120 + $T=1/t$ 代数(falsifier 判読・裁定 1719) | **cert-reading(閉)** | ★ **閉じた** |
| **D-6** | census ラベル写像 | **未確定**(§4 の裁定) | census-reading | **fail-closed 継続** |
| **★ D-10(新設)** | **cert 同名異値** | `ds4_receipt_v1_20260812.json` 内に **`/input_u0_inverse` が符号違いで 2 箇所**(`-1423828125/256` と `/d2_ord_computation/input_u0_inverse = 1423828125/256`)。**符号は 9 乗類・3 乗類では無害**($-1$ は立方)だが、**同名異値は実装が取り違える** ⟹ **cert は絶対値と符号を別欄に分離し、参照キーを 1 つに正規化すること** | cert-reading(要修理) | **警告** |
| **★ D-11(新設)** | **sgn 配線** | 実装は `u_S4` を**直接**(`u0` として)持ち、`u0inv` からの符号反転に依存しない。cert に `u_S4_value` と `u_S4_source_line` を記録 | 数学者(確定) | 追加 |

**破壊対照の追加**: **DC-8(正規化不変性)** — $u_{S4}$ に $3\sqrt{-3}$ を掛けて再走し **$c'$ が不変**であること。変われば mod 3 還元か $\sqrt{-3}$ の実装に誤り。

---

# §4 ③ D-6 の正式確認 — **閉じない**

**事実**: 札 7 で 5 集合 × 2 ハッシュ = **10/10 が Sol pin と一致**(implementer v2 cert)。

**裁定**: これは **roster の同一性**(どの 2 集合か)を閉じるが、**ラベル写像 $c'\mapsto\{$NN-09, NN-12$\}$ は閉じない。**

> ### 残るもの(1 行)
> **NN-09 / NN-12 のどちらが $A_{c'}\cap X^0=\ker(\Psi-c'\mathcal K_3)|_{X^0}$ の $c'=+1$ 側として構成されたか、その定義式が pin に含まれているか — 元集合の一致だけでは向きは決まらない。**

**なぜ元集合から向きが取れないか(ORIENT (e) の帰結・正本 §7.1)**: $A_+\cap A_-$ は位数 108、$\lvert A_\pm\rvert=324$ ゆえ対称差は 432 key で**そのすべてが $\mathcal K_3\ne0$ 側**。⟹ **対称差に $\varepsilon$-不変に強制される key は 1 個も存在せず、census から無料の 1 ビットは原理的に取れない。**⟹ **ハッシュ一致は(何個一致しても)向きを与えない。**

> ### ⚠⚠ **v2 の当該文を訂正する**(2026-08-28・裁定 1726・falsifier D-6 ハント)
> **旧(誤り)**: 「pin(または **census producer**)に各 roster の定義式を文字列として記録すること」。
> **なぜ誤りか**: falsifier 実測(census producer L706-713・機械 12/12)により **ラベル NN-jj は辞書式順位で符号意味論をまったく持たない**。⟹ **census には符号データがそもそも存在しない**ので、census 側に「定義式を書け」と要求すると、**後付けで 50/50 のどちらかを選ぶ行為を制度化してしまう**。**宛先が誤っていた。**
> **新(正)— 宛先は算術 marking レーン**:
> $$\boxed{\ \textbf{要求先}=\textbf{joint marked Frobenius row}\ (\S 7)\ \text{— census ではない。}\ }$$
> **具体的な D972 key を 1 本測り、2 つの 324-key roster への所属を直接照合する。**これなら「どちらが $c'=+1$ 側か」を**知る必要がない**(名前を経由せず、集合の所属だけで決まる)。
> ⟹ **`conclusion_pending_D6` は解除しない**が、**閉じ手は census 側の記録ではなく §7 の測定**である。

~~**閉じるための最小要求(1 行)**: pin(または census producer)に **各 roster の定義式**…**数値の一致では代替できない。**~~ ⟹ **上のブロックで置換(宛先差替)。**

---

# §5 ④ EP-DEL — $E_3/E_4$ の可換性と ミニ evaluator 仕様

## 5.1 (a) $E_4$ の可換性 — **非可換の見込み。しかし問いを鋭化すべき。**

**在庫から読めた構造**(`sol/luna_task_157da_b345_q3_chief.md` l.123,126・`luna_reply_157da` l.92・`luna_reply_162_..._v1.md` l.164):
$$E_4=PB_4/K_4,\qquad E_4=Q_4\times_{C_4}P_4=Q_4\times\Pi_4[3],\qquad V=\Pi_4[3],\qquad \lvert Q_4^{\rm ab}\rvert=32 .$$
$\Pi_4[3]$ は工房 C-13 の対象で「**radical filtration・$j^\ast=4$・FC-37 = Jennings 次数 3**」(状態.md)⟹ **Jennings 次数 3 は下 3-中心列が次数 3 に届くこと = 類 $\ge2$ = 非可換**。
⟹ **$E_4$ は非可換の見込み(格 = `candidate`・`IsAbelian(E_4)` の 1 行実測は未実行)。**

> ### ★ しかし (C-β) に必要なのは $E_4$ の可換性ではない
> (C-β) の各項は $\bigl(d_i\rho_o(U_j)-d_i\rho_o(V_j)\bigr)$。**$U_j,V_j$ は charming 台 = commutator words** なので、
> $$\boxed{\ \mathrm{Im}(d_i\circ\rho_o)\ \text{が可換}\ \Longrightarrow\ d_i\rho_o(U_j)=1=d_i\rho_o(V_j)\ \Longrightarrow\ (\mathrm{C}\text{-}\beta)=0\ \Longrightarrow\ \textbf{EP-DEL PROVED}\ }$$
> **問うべきは「$E_4$ が可換か」ではなく「$d_i\circ\rho_o$ の像が可換か」** — **削除後**なので遥かに弱く、成立の見込みも高い。
> **1 行の機械検査**: 10 本の $\rho_o$ × 4 本の $d_i$ について $\mathrm{Im}(d_i\rho_o)=\langle d_i\rho_o(x),d_i\rho_o(y)\rangle$ を作り `IsAbelian` を問う。**40 回の 2 生成部分群の可換性判定**。⟹ **④(a) の正しい実行形はこれ。**

## 5.2 (b) ミニ evaluator 仕様(P block 限定・**工房単独で回る形**)

Sol の実 $M$ は存在しない(A5/A6 = 0/3)ので、**工房生成の charming 台 $M$** で回す。

### 入力(すべて在庫から取れる)
| 記号 | 内容 | 出所 |
|---|---|---|
| $\rho_o$ | P block の 5 本($p_1,p_2,p_3,p_5,p_4:F\to E_4$) | v189 l.27 |
| $\sigma_o,P_o,\xi_o$ | 符号・prefix・occurrence endpoint | v198 (2.2)・**printed order $b_1,b_2,b_3,b_5^{-1},b_4^{-1}$**(v194 (1.7)) |
| $\epsilon_P$ | corrected residual endpoint | v198 (1.3) |
| $d_i$ | 4 本の strand deletion $PB_4\to PB_3$ | 標準(生成元 ↦ 生成元 or 1) |

### 手順
```
E0  (前提検査) Im(d_i o rho_o) の可換性を 40 通り測る            # §5.1 — true なら E1..E3 は不要
E1  工房生成の charming 台 M を作る:
      U_j, V_j in [F(x,y),F(x,y)]  かつ  pi(U_j)=pi(V_j)         # roof-fibre 条件
      (pi が読めない場合は U_j V_j^{-1} in ker(rho_o) を満たす対で代用し、その旨を宣言)
E2  eta_P(M) := eps_P - sum_o sigma_o P_o sum_j a_j (rho_o(U_j)-rho_o(V_j)) xi_o     # v198 (2.2)
E3  for i in 1..4:  (d_i)_* eta_P(M)  を計算                     # 環準同型として係数と群元に適用
E4  判定:
      全 4 本が 0            -> その M で EP-DEL 成立(支持証拠を蓄積)
      1 本でも非零           -> ★ EP-DEL は一般に偽(反例) -> 即時報告
```

### 較正必達値(ゲート)
| # | 検査 | 期待 |
|---|---|---|
| **EP-G1** | $M=0$ で $\eta_P(0)=\epsilon_P$ | 一致 |
| **EP-G2** | **$(d_i)_*\epsilon_P=0$**(§(C-α) の実測確認) | **4 本とも 0**。非零なら BRUN-DEF の適用条件か $\epsilon_P$ の provenance が誤り |
| **EP-G3** | $U_j=V_j$(自明対)で補正和 $=0$ | 一致 |
| **EP-G4** | printed order を崩す mutant | 判定が変わる(prefix $P_o$ を見ている証拠) |
| **EP-G5** | $d_i$ を恒等に差し替える mutant | $(d_i)_*\eta_P=\eta_P$ に戻る |

### 出口の格
- **全零の蓄積** = `supporting evidence`。**一般命題の証明ではない**(実 $M$ が来るまで)。
- **非零 1 本** = **EP-DEL 一般偽の反例** ⟹ `REFUTED`(一級)。
- ⚠ **EP-G2 が落ちたら E3 以降は無意味** — (C-α) が成立しないことになり、BRUN-DEF の endpoint 適用そのものが崩れる。**最初に回すこと。**

---

# §6 UNKNOWN(推測で埋めていない)

1. **D-6**(census ラベル写像)— §4。**数値では閉じない。**
2. **$\mathrm{Im}(d_i\rho_o)$ の可換性** — 未実測(§5.1 の 40 通り)。**成立すれば EP-DEL は即 PROVED。**
3. **$E_4$ の可換性そのもの** — `candidate`(Jennings 次数 3 からの推定)。`IsAbelian` 未実行。
4. **$\ker\pi$ の明示**(v191 $\Delta_0$)— 未読。E1 の roof-fibre 条件を厳密に作るのに必要(代用手順は E1 に明記)。
5. **ds4 cert の同名異値(D-10)の修理** — cert 側の作業。
6. **$M_{\rm ord}=18$ 系の再計算**(4265 行分布)— `fib_ruling_and_fibre_checker_spec_v1.md` §1.5 の指示待ち。
