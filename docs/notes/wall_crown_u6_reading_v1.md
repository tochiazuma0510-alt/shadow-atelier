# 壁 crown census の U-6 読解 — crown 被覆 = 埋め込み問題(裁定 1106)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔
入力 = `sol/sol_reply_114_k13_wallcrown.md` §2(master merge 済)+ cert `wall_crown_census_v1_20260812` / `wall_crown_model_checker_v1_20260812` / `wall_crown_census_v1_check_20260812`(cross-checked)
生成 script(裁定 1103 規約)= `scratchpad/wall_crown_u6_decomp.g`(GAP 4.16.0・本書の全数値の出所)
⚠ $u$/$c$ 非接触・封印非接触・prereg 非抵触。**格: candidate**(Sol 未監査・verified ではない)。

---

## §0 結論(4 行)

1. ★ **Sol の census を独立に再現しました**(私の GAP・producer helper 非共有)。極大類数 8/8/9/11、可換 5/5/6/6、非可換 3/3/3/5、非可換 index 10,5,6 / 15,6,15,10,6 — **全欄一致**(§1)。
2. ★★ **非可換 crown は各窓で core が単一**(機械確認: `ALL CORES EQUAL = true`・$\lvert\mathrm{core}\rvert=\ell(\ell-1)$)⟹ **3 類(wall37 は 5 類)は同じ primitive quotient $S_t$ を与え、埋め込み問題としては 1 本に潰れます**(§3)。多重度 3/5 は極大部分群の数であって、算術条件の数ではありません。
3. ★★★ **8〜11 個の crown 被覆条件は、窓あたり 2 本の有料条件に分解します**(§5):
$$\boxed{\ \text{crown 被覆}\ =\ \underbrace{\omega(\ell-1)+2\ \text{類}}_{\textbf{円分で無料(見込み)}}\ +\ \underbrace{1\ \text{類}}_{\textbf{Kummer}(\ell)\ \textbf{有料}}\ +\ \underbrace{(3\ \text{or}\ 5)\ \text{類}=\mathbf 1\ \textbf{本の EP}}_{S_t\ \textbf{埋め込み問題・有料}}\ }$$
4. ⚠ **核が中心自由($Z(A_t)=1$・機械確認)なので、群拡大の側では何も問われません**(存在も一意性も自動)。問われるのは**体の側の持ち上げだけ**です(§4)。⟹ 発注の「可解性でなく一意性」の整理への答え: **どちらでもなく「群論は空・全部が算術」**。
★ **U-6 の実質的な収穫**: crown census は代金を下げませんが、**全射性を有限個の Frobenius 条件のチェックリストに変換します**(§6.3)。

---

## §1 材料の独立再構成

模型は $Q:=GT(N)/\Phi=GT(N)$(全窓 $\Phi=1$)、$Q\cong S_t\times\mathrm{AGL}(1,\ell)$:

| 窓 | $(t,\ell)$ | $\lvert Q\rvert$ | $\lvert[Q,Q]\rvert$ | $\lvert Q^{ab}\rvert$ | $\lvert\Phi\rvert$ | 極大類 | 可換 | 非可換 | 非可換 index |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| wall24 | (5,19) | 41,040 | 1,140 | 36 | 1 | 8 | 5 | **3** | 10, 5, 6 |
| wall28 | (5,23) | 60,720 | 1,380 | 44 | 1 | 8 | 5 | **3** | 10, 5, 6 |
| wall36 | (5,31) | 111,600 | 1,860 | 60 | 1 | 9 | 6 | **3** | 10, 5, 6 |
| wall37 | (6,31) | 669,600 | 11,160 | 60 | 1 | 11 | 6 | **5** | 15, 6, 15, 10, 6 |

★ **全欄が Sol §2.3 の生値と一致**。私は wall witness も `MakeWindow` も `CorrectedShadowsXi` も使わず、$\mathrm{AGL}(1,\ell)$ を $\ell$ 点上の置換群として直接構成しました(GAP の `AGL` にも依存せず)⟹ **第 3 の独立系統**です。
$\lvert Q^{ab}\rvert=2(\ell-1)$ も理論式と一致(36, 44, 60, 60)。

---

## §2 U-6 の枠 — crown 被覆の正確な言明

$H:=a_N(G_{\mathbf Q})\le Q$。「crown 被覆」= **$H$ がどの極大部分群にも含まれないこと** $\iff H=Q$。
本窓の $Q$ は**直積**なので、Goursat で完全に分解できます:

> **【命題 WALL-SURJ】** $Q=S_t\times A$($A=\mathrm{AGL}(1,\ell)$)、$H\le Q$。このとき
> $$H=Q\iff \textbf{(E1)}\ \mathrm{pr}_1(H)=S_t\ \wedge\ \textbf{(E2)}\ \mathrm{pr}_2(H)=A\ \wedge\ \textbf{(E3)}\ H\ \text{が対角 }C_2\ \text{部分群に含まれない}$$

*証明*: (E1)(E2) の下で $H$ は subdirect product ⟹ Goursat により $S_t/N_1\cong A/N_2$ なる共通商が対応。**機械確認: $S_t$ と $A$ の非自明な共通商は $C_2$ **のみ**(4 窓とも)** ⟹ $H=Q$ または $H=$ 指数 2 の対角部分群 ∎

**crown 類との対応**(過不足なし):

| 条件 | 対応する極大類 | 個数 |
|---|---|---:|
| (E1) | 非可換 crown(全部)+ $A_t\times A$($C_2$ 商) | $\#\text{nonab}+1$ |
| (E2) | $S_t\times C_{\ell-1}$($C_\ell$ crown)+ $S_t\times(C_\ell{:}H_q)$($q\mid\ell-1$) | $1+\omega(\ell-1)$ |
| (E3) | 対角 $C_2$ | 1 |

合計 $=\#\text{nonab}+\omega(\ell-1)+3$ ⟹ wall24: $3+2+3=8$ ✔ wall28: $8$ ✔ wall36: $3+3+3=9$ ✔ wall37: $5+3+3=11$ ✔ **4 窓とも一致**。

---

## §3 ★★ 非可換 crown の潰れ(発注 1 の中核)

**機械確認**(`wall_crown_u6_decomp.g`):

| 窓 | 非可換 crown の core サイズ | 全 core が同一? | 共通 primitive quotient | socle | $\lvert Z(\mathrm{socle})\rvert$ | $\lvert\mathrm{Out}(\mathrm{socle})\rvert$ |
|---|---:|---|---|---|---:|---:|
| wall24 | **342** ($=19\cdot18$) | ★ **true** | $S_5$(位数 120) | $A_5$ | **1** | 2 |
| wall28 | **506** ($=23\cdot22$) | ★ **true** | $S_5$ | $A_5$ | **1** | 2 |
| wall36 | **930** ($=31\cdot30$) | ★ **true** | $S_5$ | $A_5$ | **1** | 2 |
| wall37 | **930** | ★ **true** | $S_6$(位数 720) | $A_6$ | **1** | **4** |

すなわち非可換 crown はすべて $M=M_1\times A$($M_1$ は $S_t$ の core-free 極大)の形で、
$$\mathrm{Core}_Q(M)=\mathrm{Core}_{S_t}(M_1)\times A=1\times A$$
は**$M_1$ に依らず同一**。⟹

$$\boxed{\ \textbf{非可換 crown 3 類(wall37 は 5 類)は}\textbf{同じ}\ \text{primitive quotient}\ Q/\mathrm{Core}=S_t\ \textbf{を与える}\ }$$
$$\boxed{\ \Longrightarrow\ \textbf{埋め込み問題としては}\ \mathbf 1\ \textbf{本}\textbf{。多重度 3/5 は「極大部分群の数」であって「算術条件の数」ではない}\ }$$

⚠ 生値 $[3,3,3,5]$ を「非可換な要求が 3 本/5 本ある」と読むと**過大評価**になります。正しくは「$S_t$ への全射性という 1 本の条件を、3 通り(5 通り)の primitive 作用で見ている」。

---

## §4 埋め込み問題の明示 — 中心自由核の整理(発注 1c)

### 4.1 埋め込み問題の形

(E1) の非可換部分は次の埋め込み問題です:

$$\boxed{\ \mathcal E_t:\quad 1\longrightarrow A_t\longrightarrow S_t\xrightarrow{\ \mathrm{sgn}\ }C_2\longrightarrow1,\qquad \text{与件: } G_{\mathbf Q}\twoheadrightarrow C_2\ (\text{= }\mathrm{sgn}\circ\mathrm{pr}_1\circ a_N)\ }$$
$$\text{解: } G_{\mathbf Q}\twoheadrightarrow S_t\ \text{で与件を持ち上げるもの — しかも }\mathrm{pr}_1\circ a_N\ \text{自身が解であること}$$

### 4.2 ★ 「どの群拡大の可解性が問われるか」への答え: **何も問われません**

$Z(A_t)=1$(機械確認)。中心自由核 $A$ と coupling $\psi:\Gamma\to\mathrm{Out}(A)$ に対し、Eilenberg–MacLane の障害理論より
$$\text{拡大の存在障害}\in H^3(\Gamma,Z(A))=H^3(\Gamma,1)=0,\qquad \text{同値類の集合は }H^2(\Gamma,Z(A))=0\ \text{のトーサー}$$
$$\boxed{\ \Longrightarrow\ \textbf{拡大は}\textbf{存在し、かつ一意}\ \textbf{— 群拡大の側では可解性も一意性も}\textbf{自動}\ }$$

⟹ **整理**: 「可解性 vs 一意性」の二択ではなく、**群論の側は空**で、**残るのは体の側の持ち上げだけ**です。これは検分(集合手術)の結論「装置は分母を整理するが算術の代金は下がらない」と**同型**です。

### 4.3 ⚠ ただし wall37($A_6$)は coupling の固定が必須

$\lvert\mathrm{Out}(A_6)\rvert=\mathbf 4$(機械確認・$\mathrm{Out}(A_6)\cong C_2\times C_2$)⟹ 位数 2 の部分群が **3 つ**あり、$C_2$ への coupling は 3 通り。対応する拡大は
$$S_6,\qquad PGL(2,9),\qquad M_{10}$$
の 3 種で、**一意性は「coupling を $S_6$ のものに固定した後」で初めて成立**します。
⟹ ★ **wall37 の埋め込み問題を書くときは「$Q/\mathrm{Core}\cong S_6$」を明示的に固定すること**(census は $Q/\mathrm{core}$ の位数 720 と socle $A_6$ を出しており、これは $S_6$ を指しますが、$PGL(2,9)$ も $M_{10}$ も位数 720・socle $A_6$ なので**位数と socle だけでは区別できません**)。⟹ **【U6-GAP-1】**(§7 [U6-2] で決着)。
$A_5$ 側は $\lvert\mathrm{Out}(A_5)\rvert=2$ ⟹ 非自明 coupling は 1 通り ⟹ $S_5$ で一意 ✔

---

## §5 無料/有料の会計

$\chi_{\rm vir}:Q\to(\mathbf Z/N_{\rm ord})^\times$ は可換群への準同型 ⟹ $\ker\chi_{\rm vir}\supseteq[Q,Q]=A_t\times C_\ell$。$\chi_{\rm vir}\circ a_N=$ 円分指標で**全射**(Kronecker–Weber)⟹ $H$ は $Q/\ker\chi_{\rm vir}$ に全射。

$$H\ \not\subseteq\ M\quad\text{は}\quad M\supseteq\ker\chi_{\rm vir}\ \text{なる極大 }M\ \text{について}\textbf{自動}$$

**機械確認**($M\supseteq[Q,Q]$ の個数 = 最良の場合の無料 crown 数):

| 窓 | $\omega(\ell-1)$ | 無料候補($M\supseteq[Q,Q]$) | 有料候補 | 内訳(有料) |
|---|---:|---:|---:|---|
| wall24 | 2 | **4** | 4 | $C_{19}$ crown 1 + 非可換 3 |
| wall28 | 2 | **4** | 4 | $C_{23}$ crown 1 + 非可換 3 |
| wall36 | 3 | **5** | 4 | $C_{31}$ crown 1 + 非可換 3 |
| wall37 | 3 | **5** | 6 | $C_{31}$ crown 1 + 非可換 5 |

理論式 $\omega(\ell-1)+2$ と 4 窓とも一致 ✔

$$\boxed{\ \textbf{有料は 2 本}:\quad \textbf{(P1)}\ \ell\text{ 次 Kummer 型}(C_\ell\ \text{crown})\qquad \textbf{(P2)}\ S_t\ \textbf{埋め込み問題}(\text{非可換 crown 全部が 1 本に潰れる})\ }$$

⚠ **無料は「見込み」です**: $\ker\chi_{\rm vir}=[Q,Q]$(= $\chi_{\rm vir}$ が $Q^{ab}$ 上で単射)かどうかは未測定 ⟹ **【U6-GAP-2】**(§7 [U6-1])。もし $\ker\chi_{\rm vir}\supsetneq[Q,Q]$ なら無料枠は減り、有料が 3 本になります。

---

## §6 算術側との接続(発注 2)

### 6.1 具体形 — 2 つの体

$Q$ が直積なので、$a_N$ の 2 成分は**独立な 2 つのガロア拡大**を定めます。$L_1/\mathbf Q$ を $\mathrm{pr}_1\circ a_N$ の固定体、$L_2/\mathbf Q$ を $\mathrm{pr}_2\circ a_N$ の固定体とすると:

$$\boxed{\ a_N\ \text{全射}\iff \mathrm{Gal}(L_1/\mathbf Q)\cong S_t\ \wedge\ \mathrm{Gal}(L_2/\mathbf Q)\cong\mathrm{AGL}(1,\ell)\ \wedge\ L_1\cap L_2=\mathbf Q\ }$$
(第 3 条件 = (E3): 両者の二次部分体が相異なること。)

### 6.2 ⚠ 既知の実現は**移りません**(発注 2 への正面回答)

$A_5,A_6,S_5,S_6$ の $\mathbf Q$ 上の実現は古典的に既知です。さらに埋め込み問題 $\mathcal E_t$ も、抽象的には可解と期待されます(判別式体を指定した $S_t$ 拡大の構成)。しかし:

$$\boxed{\ \textbf{既知は「}\exists\ \textbf{全射 }G_{\mathbf Q}\twoheadrightarrow S_t\textbf{」。crown 条件は「}\textbf{与えられた写像 }\mathrm{pr}_1\circ a_N\ \textbf{が全射」}\ }$$

この 2 つは**別の問題**です。古典的実現は $\beta:G_{\mathbf Q}\twoheadrightarrow S_t$ を 1 本くれますが、$\beta=\mathrm{pr}_1\circ a_N$ である理由はどこにもありません。⟹ **正の方向には 1 ミリも移りません。**

**移るもの 2 つ(正直に)**:
- **(a) 障害の除去(消極的)**: $S_t$ が $\mathbf Q$ 上実現不可能なら crown 条件は即座に偽でした。実現可能なので、**大域的な逆ガロア障害は存在しない**ことが分かります。⟹ 「なぜ難しいか」の切り分けにはなります(難しさは 100% $a_N$ の特定性にある)。
- **(b) 通貨の同定(構造的)**: 何を調達すれば決着するかが決まります — $L_1$ を同定する receipt(SURG-A6 と同種)と、$L_2$ の $\ell$ 次 Kummer receipt。⟹ **U-6 は代金を下げず、品目を確定します。**

### 6.3 ★★ しかし crown census は**有限の証明書**を与えます(本読解の実質的収穫)

$H=Q$ を示すには「各極大類 $[M]$ について、$H$ が $M$ のどの共役にも含まれない」を示せばよく、それには **$H$ の元を 1 個ずつ**挙げれば十分です($\mathrm{cl}(h)\cap M=\emptyset$ なる $h\in H$)。Chebotarev で $H$ の元は Frobenius として供給されます ⟹

$$\boxed{\ \textbf{crown census}\ +\ \textbf{Chebotarev}\ =\ \textbf{全射性の}\textbf{有限証明書}\ }$$

本窓での具体的なチェックリスト($Q=S_t\times\mathrm{AGL}(1,\ell)$ の構造から):

| # | 要求する Frobenius | 効く条件 | 根拠 |
|---|---|---|---|
| **F1** | $\mathrm{pr}_2$ の位数が $\ell$ | (E2) の $C_\ell$ crown | $C_\ell$ は $A$ の最小正規部分群 |
| **F2** | $\mathrm{pr}_2$ が $C_{\ell-1}$ の生成元へ写る | (E2) の $q$-crown 群($\omega(\ell-1)$ 本) | ★ 円分で無料の見込み |
| **F3** | $\mathrm{pr}_1$ が $t$-cycle($t=5$)/ $(5,1)$ 型と $6$-cycle($t=6$) | $\mathrm{pr}_1(H)$ の可移性・原始性 | 素数次数 5 は可移 ⟹ 原始。$t=6$ は「可移 + 5-cycle ⟹ 原始」 |
| **F4** | $\mathrm{pr}_1$ が**互換** | 原始 + 互換 ⟹ $S_t$(Jordan) | ⟹ (E1) が閉じる |
| **F5** | 2 つの二次指標($\mathrm{sgn}\circ\mathrm{pr}_1$ と $A\to C_2$)が異なる | (E3) | 対角 $C_2$ crown |

⟹ **F1–F5 を満たす素点が見つかれば $a_N$ の全射性が確定**します。⚠ $a_N(\mathrm{Frob}_p)$ の計算は算術入力(有料)ですが、**要求は有限個・具体的**になりました。
★ これが「crown 被覆 ⟺ 埋め込み問題」の**実効的な**形だと思います。

---

## §7 次の測定(prereg・発注 3)

### [U6-1] $\chi_{\rm vir}$ の核と無料 crown の確定(純群論・算術入力ゼロ)

```
目的: 【U6-GAP-2】= ker(chi_vir) = [Q,Q] か(⟹ 無料 crown の個数が確定)
[1] 各壁窓で N_ord と chi_vir: GT(N) -> (Z/N_ord)^* を producer 資産から取り、ker を計算
[2] ker ⊇ [Q,Q] を確認（自明・回帰）。|Q^ab / (ker/[Q,Q])| を出す
[3] 極大類のうち M ⊇ ker(chi_vir) なるものを数える = 無料 crown 数
出力: cert (schema u6_chivir/v1)。整数のみ。u_touched=false
```
**★ 凍結予言(整数)**: $\lvert[Q,Q]\rvert=1140,\ 1380,\ 1860,\ 11160$;$\lvert Q^{ab}\rvert=36,\ 44,\ 60,\ 60$。
$\ker\chi_{\rm vir}=[Q,Q]$ **なら** 無料 crown $=4,4,5,5$、有料 $=4,4,4,6$ 類($=$ 有料条件 2 本)。
⚠ $\ker\supsetneq[Q,Q]$ **なら** 有料が 3 本に増える ⟹ どちらでも結論が出ます。

### [U6-2] 非可換 crown の潰れと coupling の固定(純群論)

```
目的: §3 の潰れの機械確認 +【U6-GAP-1】(wall37 の Q/Core が S_6 か PGL(2,9) か M_10 か)
[1] 各窓で非可換 crown の core を全て計算し、集合として単一であることを確認
[2] Q/Core の同型型を *位数と socle ではなく* IdGroup / StructureDescription で確定
    ★ wall37 は位数 720・socle A_6 が 3 群(S_6, PGL(2,9), M_10)で共通 ⟹ 区別必須
[3] Out(socle) の位数と、coupling C_2 -> Out(A_t) の像を記録
出力: cert (schema u6_crowncore/v1)。u_touched=false
```
**★ 凍結予言(整数・機械生成)**: core 位数 $=342,\ 506,\ 930,\ 930$;単一性 `true`(4 窓);$\lvert Q/\mathrm{Core}\rvert=120,120,120,720$;$\lvert Z(\mathrm{socle})\rvert=1$(4 窓);$\lvert\mathrm{Out}(\mathrm{socle})\rvert=2,2,2,\mathbf 4$。**wall37 の $Q/\mathrm{Core}\cong S_6$**(私の模型からの予言 — 実物で確認せよ)。

### [U6-3] ★ 壁窓の isolated 性(TORSOR 線との接続・fail-closed)

```
目的: crown 枠の *前提* の検査。crown/極大部分群の議論は GT(N) が群であることを要する
      ⟺ N が isolated ⟺ #C(N) = 1（set_surgery_vetting_v1 系 C）
[1] 各壁窓で #C(N) = #{ker T_{m,f} : shadow} を marked factor map で数える
[2] 併せて |GT^settled(N)| を出し、|GT(N)| = |GT^settled(N)| · #C(N)（定理 TORSOR）を回帰
出力: cert (schema u6_isolated/v1)。u_touched=false
```
**★ 凍結予言**: $\#\mathcal C(N)=1$(4 窓とも)かつ $\lvert GT^{\rm settled}(N)\rvert=\lvert GT(N)\rvert=41040,\ 60720,\ 111600,\ 669600$。
⚠ **$\#\mathcal C>1$ が出たら**: $GT(N)$ は群でなく、Sol の $X$ は **settled 層のみ**の census です ⟹ 本読解は「$GT^{\rm settled}(N)$ の crown 被覆」に格下げされ、主戦場(非 settled 層)は**依然として枠外**になります。⟹ **この 1 本が本読解の適用範囲を決めます。先に走らせるべきです。**

---

## §8 【文献要請】(発注 4)

**【U6-L1】** 中心自由・非可換単純核をもつ埋め込み問題の $\mathbf Q$ 上の可解性。
- **困難**: §4 で群論側は空になったので、「抽象的な $\mathcal E_t$ は無条件に可解か」を知りたい。可解なら**難しさは 100% $a_N$ の特定性にある**と言い切れ、§6.2(a) の切り分けが確定する。
- **欲しい結果の型**: 「$\Gamma=C_2$、核 $=A_n$、coupling $=S_n$ の埋め込み問題は、任意の $G_{\mathbf Q}\twoheadrightarrow C_2$ に対し**真に可解**」型の定理(GAR/GAL 性・rigidity 系)と、$n=5,6$ での適用可否。

**【U6-L2】(本命)** **与えられた**副有限群からの射の**全射性**を有限個の Frobenius データで判定する手法。
- **困難**: §6.3 のチェックリストは私の手作りで、標準形かどうか分からない。極大部分群の census を使う "surjectivity criterion" の標準的な定式化(必要な素点の高さの評価・GRH 条件の有無)を知りたい。
- **欲しい結果の型**: 「$\rho:G_K\to G$ が全射 $\iff$ 各極大類を避ける Frobenius が存在」型の判定と、**必要な素点の explicit bound**(effective Chebotarev)。

**⚠ 在庫の $M_{23}$ 論文について**: `2608.08538` / `1311.2081` は「$M_{23}$ を**実現する**」= **存在問題**であり、本件の「**特定写像の全射性**」とは型が違います ⟹ **直接は効かない見込み**です。ただし L2 の技法(与えられた族の中で像を決める手続き)を含むなら価値があります — **降ろすかは司令塔判断**。私からは要請しません。

---

## §9 記帳

- ★ **本読解の新規部分**: ① Sol census の**第 3 独立系統での再現**(§1)② **命題 WALL-SURJ**(Goursat による (E1)(E2)(E3) への完全分解・crown 類との過不足なき対応)③ ★★ **非可換 crown の core が単一 ⟹ 3/5 類が 1 本の埋め込み問題に潰れる**(§3)④ **中心自由核ゆえ群論側は空**という整理(§4.2)⑤ **wall37 の coupling 曖昧性**($S_6$/$PGL(2,9)$/$M_{10}$ は位数と socle が同じ)(§4.3)⑥ **無料/有料の会計**(有料は 2 本)(§5)⑦ **既知実現は移らない**ことの明示と、移る 2 つ(障害除去・通貨同定)(§6.2)⑧ ★ **crown + Chebotarev = 全射性の有限証明書**(F1–F5)(§6.3)⑨ 測定 3 本(特に [U6-3] は crown 枠の適用可能性そのものを決める)。
- **【U6-GAP-1】(小・新)** wall37 の $Q/\mathrm{Core}$ が $S_6$ であることの確定(位数 720・socle $A_6$ は $PGL(2,9)$・$M_{10}$ とも共通)。⟹ [U6-2]。
- **【U6-GAP-2】(中・新)** $\ker\chi_{\rm vir}=[Q,Q]$ か(無料 crown の個数が懸かる)。⟹ [U6-1]。
- **【U6-GAP-3】(★大・新)** 壁窓が isolated か(= crown 枠の前提)。⟹ [U6-3]。**否なら本読解は settled 層限定に格下げ**。
- ⚠ **本読解の限界**: 検分(集合手術)と同じ結論に着きます — **crown census は分母(群論)を完全に整理するが、算術の代金は 1 円も下がりません**。下がらない代わりに、**品目が有限個に確定**しました(§6.3)。
- **申告**: GAP 4.16.0(`scratchpad/wall_crown_u6_decomp.g`・本書の全数値の出所)。$u$/$c$ 非接触・封印非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
