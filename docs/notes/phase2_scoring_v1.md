# 相 2 採点束 v1 — PL-LAB-1 初測定・T2-SPLIT・B′×Kellner(裁定 782)

**状態札: `採点 + 正札案 / candidate / Sol 未監査 / GAP 実走ゼロ・cert 発行ゼロ / 判定語の発効は司令塔専権 / 各設計ノートは不改変(versioned)`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-11 / 委嘱: 司令塔(**裁定 782**・編纂の最終データ)
- 生値: PL-LAB-1 初測定(対照 3 件 $\mathrm{def}=0$・$(5,5)$: $\mathrm{def}_5=-1$・$(7,7)$: $\mathrm{def}_7=-2$・$k<p$ は全て 0・P-PL-0 完全成立)/ T2-SPLIT(4/4 で Legendre $+1$)/ 算法 B′(Kellner 表の $s_1=k_0$・$s_2=j^*$ が全 9 一致)
- **自前検算**: §1.2 の isotypic 会計・§2.2 の付値は python(整数のみ・GAP 不使用・cert ではない)

---

## 0. 採点表(先に)

| 予言 | 生値 | 採点 |
|---|---|---|
| **P-PL-0**(層次元は $k<p$ で Witt・$k=p$ で落下) | 完全成立(落ち幅込み) | ★ **的中** |
| **P-PL-1′**(Lazard 域で $\mathrm{def}=0$) | 対照 3 件すべて $0$ | ★ **的中** |
| **P-PL-2′/3′**(class $=p$ が最初の分岐点) | $\mathrm{def}_5=-1$、$\mathrm{def}_7=-2$($k<p$ は 0) | ★ **分岐点は的中**($k=p$ でのみ非零)。**符号は負** ⟹ §1 の正規化判定へ |
| **P-CONE-6′ 系**($\left(\frac{d_K}p\right)$) | **4/4 で $+1$** | ★ **固有形式枝が確定側**(§2) |
| **算法 B′**(2 点から $j^*$) | Kellner 表と全 9 一致 | ★ **一致**(§3) |

---

# 1. PL-LAB-1 初測定の採点

## 1.1 ★★★ 正規化判定 — 負の $\mathrm{def}$ は**層次元の落ちで説明できるか**

P-PL-0 により $k=p$ で $\gamma_p/\gamma_{p+1}(P_{c,p})=\Lambda_p\otimes\mathbf F_p\big/R_p$($R_p$ = 指数 $p$ の法則が生む関係加群、$\delta_p:=\dim R_p$)。

> ### 命題 NORM-1(candidate・本束。**判定式**)
> $R_p$ は $\mathrm{Aut}(F_2)$-自然な構成($p$ 冪写像とその Hall–Petrescu 補正)から来るので **$S_3$-部分加群**である。定理 TOR-S3 により $H_k=\mathrm{mult}_{\rm std}(\Lambda_k)$(std のコピー 1 個につき 1 次元)だから
> $$\boxed{\ H_p^{\rm meas}\ =\ H_p\ -\ \mathrm{mult}_{\rm std}(R_p)\ }$$
> ゆえに **「Lazard 辞書補正のみ・異常なし」枝の判定式**は
> $$\boxed{\ \mathrm{def}_p\ =\ -\,\mathrm{mult}_{\rm std}(R_p)\ }$$
> であり、$\delta_p=\dim R_p=m_{\rm triv}+m_{\rm sgn}+2\,m_{\rm std}$ との整合を見ればよい。∎

> ### ★ 実測への当てはめ(**cert の落ち幅で 1 行検算できる**)
> | $p$ | $\mathrm{def}_p$ | 要求される $m_{\rm std}(R_p)$ | ゆえに $\delta_p$ が満たすべき式 | 最小値 |
> |---:|---:|---:|---|---:|
> | 5 | $-1$ | **1** | $\delta_5=m_{\rm triv}+m_{\rm sgn}+2$ | $\delta_5\ge\mathbf2$ |
> | 7 | $-2$ | **2** | $\delta_7=m_{\rm triv}+m_{\rm sgn}+4$ | $\delta_7\ge\mathbf4$ |
> $$\boxed{\ \textbf{発注 NORM-CHK(1 行)}: \text{cert の }\delta_p\ \text{を }S_3\text{-isotypic 分解し、}m_{\rm std}(R_p)=\lvert\mathrm{def}_p\rvert\ \text{を確認せよ。}\ }$$
> **一致 ⟹ 枝 L(Lazard 辞書補正のみ・異常なし)**。**不一致 ⟹ 残差**(§1.2)。

> ### ★ 私の当初の見積りは $p=7$ で外れている(自己申告)
> 追補 A §2.2 では「$\gamma_1/\gamma_2\cong\mathrm{std}$ からの $p$ 冪像 ⟹ $R_p\cong\mathrm{std}$ ⟹ 落ち幅 $\ge2$」とし、暗に $m_{\rm std}=1$(すなわち $\mathrm{def}_p=-1$)を想定していた。**$p=7$ で $-2$ が出た** ⟹ $R_7$ は std を**2 コピー**含む ⟹ **$p$ 冪像だけでは説明できない**(Hall–Petrescu の高次補正が $\Lambda_7$ に std をもう 1 本落としている)。
> $$\boxed{\ \textbf{【PS-GAP-1】}\ R_p\ \textbf{の }S_3\text{-型の閉形式は未導出。}\ m_{\rm std}(R_p)\ \textbf{が }p\ \textbf{とともにどう増えるかは未知。}\ }$$
> ★ ただし**これは正規化判定を壊さない** — 判定は $R_p$ の**実測**を使うからである。

## 1.2 残差が出た場合の意味論(**事前固定**)

| 観測 | 読み | 次の一手 |
|---|---|---|
| $\mathrm{def}_p=-m_{\rm std}(R_p)$(**一致**) | ★ **枝 L**: 群と Lie のずれは「未知数空間が縮んだ分」で**完全に説明される** ⟹ Lazard の破綻は**辞書の付け替えだけ**で、hexagon の解の**質**には効いていない | 正札 §1.3 を発効請求 |
| $\mathrm{def}_p<-m_{\rm std}(R_p)$(**残差が負**) | **持ち上げ障害**: graded の解が群へ持ち上がらない ⟹ Lazard 破綻が**能動的に解を殺している** ⟹ 盾モデルの W 柱の新しい効き方 | 段別に残差の位置を特定 |
| $\mathrm{def}_p>-m_{\rm std}(R_p)$(**残差が正**) | ★★ **窓側の S 伸び** ⟹ Γ 縁の窓側双子が鳴った ⟹ **QUAR-TOR 型検疫**(pc 表示の別構成・独立再現)を経てから報告 | 検疫 |
> ★ **現時点の生値($-1,-2$)はいずれも負** ⟹ **正の残差(S 伸び)は出ていない**。これが §1.3 の正札の根拠。

## 1.3 ★ 正札案 **WILD-NOEXCESS**(いずれの枝でも成立)

> ## 正札 WILD-NOEXCESS(発効は司令塔専権・以下は案)
> ### 主張
> $$\boxed{\ \textbf{野生帯(post-Lazard)の初段 }c=p\ (p=5,7)\ \textbf{において、}\mathrm{def}(c,p)\le0\ \textbf{— すなわち窓側の「超過(S 伸び)」はゼロである。}\ }$$
> Lazard 域の対照 3 件は $\mathrm{def}=0$(P-PL-1′ 的中)、$k<p$ の全段で $\mathrm{def}_k=0$、非零は $k=p$ の 1 段のみでかつ**負**。
> ### ★ 限定(4 点・必ず併記)
> | # | 限定 |
> |---|---|
> | **(W1)** | **$\mathrm{def}\le0$ は「超過なし」であって「異常なし」ではない**。負の値が層次元の落ちで**ちょうど**説明されるかは NORM-CHK 待ち(§1.1) |
> | **(W2)** | $p=5,7$ の**初段($c=p$)のみ**。$c>p$ は未測 |
> | **(W3)** | hexagon-only($B_3$-gentle)の言明。pentagon($\mathcal S$)側は別(追補 A §1) |
> | **(W4)** | 単系統・Sol 未監査・格子(pc 表示)依存 |
> ### 言ってよい / いけない
> | ✔ | ✗ |
> |---|---|
> | 「野生帯初段に超過なし(candidate)」 | 「Lazard 破綻は無害」(NORM-CHK 前) |
> | 「$k=p$ でのみ差が出るという分岐点の予言が的中」 | 「窓側で共鳴を見た/見なかった」(共鳴は A×S の同番地一致・本測定は S 側のみ) |

---

# 2. T2-SPLIT の採点

## 2.1 生値と直接の帰結

4/4 で $\left(\frac{d_K}p\right)=+1$ ⟹ **こだま素数はすべて Hecke 体で分裂**。とくに
$$\boxed{\ \left(\tfrac{d_{32}}{37}\right)=+1\ \Longrightarrow\ 37\ \text{は分裂}\ \Longrightarrow\ \mathcal O_K\otimes\mathbf Z_{37}\cong\mathbf Z_{37}\times\mathbf Z_{37}\ }$$
命題 IDX-2($p\ge5$ で極大)と合わせ、$C_{32}$ は $\bmod\,37$ で対 $(c_1,c_2)$ に分解し
$$\mathrm{rank}_{\mathbf F_{37}}\rho_{32}=2-\#\{i:37\mid c_i\}.$$

## 2.2 ★★★ $\rho$ 側検定に何が残るか — **紙で 1 に確定する**

$\#\{i:37\mid c_i\}=2$ なら $37^2\mid\det C_{32}$ ⟹ こだま分子の付値が $\ge2$。しかし自前計算(追補 B §1.3)より
$$\mathrm{num}(B_{32})=37\cdot683\cdot305065927\ \Longrightarrow\ v_{37}=\mathbf1,\qquad \mathrm{num}(B_{24})=103\cdot2294797\ \Longrightarrow\ v_{103}=\mathbf1 .$$

> ### 命題 RANK-1(candidate・本束)
> $\dim\mathsf P_k=2$、$p\ge5$、$\mathcal O_K$ が $p$ で極大、$p$ 分裂、$v_p\bigl(\mathrm{num}\,\zeta(k)\pi^{-k}\bigr)=1$ とする。$\det C_k$ の分子がこだま分子(命題 CONE-A′)なら
> $$\boxed{\ \mathrm{rank}_{\mathbf F_p}\rho_k\ =\ 1\ }$$
> **証明.** $\prod d_i=\lvert\det C_k\rvert$(命題 PS5-1)、$v_p(\det C_k)=1$ ⟹ $p$ はちょうど 1 つの単因子を割る ⟹ 階数落ちは 1。∎
> ⟹ **$(37,32)$ も $(103,24)$ も「固有形式枝」で確定**(P-CONE-6′ の答え)。
> ⚠ **依存**: 命題 CONE-A′ の「$\det C_k$ の分子 $=$ こだま分子」は $\dim\mathsf P\ge2$ で**仮定**【CB-GAP-5】⟹ **$\rho$ 側の実測($\tilde\sigma$ 律速)が残る唯一の未決点**。

$$\boxed{\ \textbf{P-CONE-6′ に残るのは「}\det C_k\ \textbf{の分子がこだま分子か」の 1 点だけ。分解型の問いは閉じた。}\ }$$

## 2.3 ★★ 「全 4 番地 $+1$」の構造的意味 — **偶然ではなく強制**

> ### 命題 SPLIT-FORCED(candidate・本束)
> $\dim\mathsf P_k=2$、Hecke 体 $K$、$p\ge5$ で $\mathcal O_K$ が $p$ で極大とする。Eisenstein 合同($\exists\mathfrak p\mid p$: $a_\ell\equiv1+\ell^{k-1}\ (\mathfrak p)$ が全ての素数 $\ell$ で)が存在するなら、**$p$ は $K$ で惰性ではありえない**。
> **証明.** 惰性なら $\mathfrak p=(p)$ で $\mathcal O_K/(p)\cong\mathbf F_{p^2}$。合同より全ての $\bar a_\ell=\overline{1+\ell^{k-1}}\in\mathbf F_p$。しかし $\{a_\ell\}$ は $\mathcal O_K$ を生成する(Hecke 体の定義)⟹ その還元は $\mathcal O_K/(p)=\mathbf F_{p^2}$ を生成せねばならない。$\mathbf F_p\subsetneq\mathbf F_{p^2}$ ゆえ矛盾。∎
> $$\Longrightarrow\ p\ \text{は分裂または分岐。}\ p\nmid d_K\ \text{なら}\ \boxed{\left(\tfrac{d_K}p\right)=+1\ \textbf{が強制される}}$$
> ★ **⟹ 4/4 の $+1$ は「$1/2^4=6\%$ の偶然」ではなく、Eisenstein 合同の存在から従う。** 測定は**予言の確認**であって新事実の発見ではない — が、**惰性が出ていたら合同の存在か極大性のどちらかが破れていた**ので、**強力な健全性検査**として機能した。
> ⚠ **【PS-GAP-2】**: 「$\{a_\ell\}$ が $\mathcal O_K$ を生成」は Hecke 体の定義から従うが、$\mathcal O_K$ でなく部分整環 $\mathbf T$ しか生成しない可能性 ⟹ 極大性(IDX-2)がそこを埋めている。**IDX-2 が命題 SPLIT-FORCED の前件**である。

---

# 3. B′ × Kellner の解釈

## 3.1 同定の正式化

算法 B′ の出力 $j^*$ と Kellner Table A.3 の $s_2$ 列が**全 9 一致**。

> ### 同定 KELL-ID(candidate・本束)
> $$\boxed{\ s_1=k_0\ (\text{order-1 の index}),\qquad s_2=j^*\ (\text{order-2 の index の offset}),\qquad l'=s_1+(p-1)s_2\ }$$
> すなわち Kellner の **order-2 不規則対の index $l'$** は我々の $k^*=k_0+(p-1)j^*$ に一致する。
> ⚠ **9/9 の数値一致は状況証拠であって定義の一致ではない** ⟹ 発効には §3.3 の pin が要る。

## 3.2 ★★★ 例外条件の完全形(**【P2-GAP-2】の残り方が整理された**)

CC-1★ の例外は $v_p(B_k)>v_p(k!)$。$k=k_0+(p-1)j$、$k<p^2$ の範囲で $v_p(k!)=\lfloor k/p\rfloor=j$(§P2 命題 P2-1 の一般化)。

> ### 命題 EXC-ALL(candidate・本束)
> $\Delta_{(p,k_0)}\ne0$(Kellner)とし、order-$n$ 不規則対の offset を $j^{(n)}$ とする($j^{(2)}=j^*$)。Kummer 合同 $\bmod p^n$ より $j^{(n)}\equiv j^{(2)}\pmod p$。ゆえに $n-1<p$ の範囲で
> $$j^{(n)}=n-1\ \Longrightarrow\ j^{(2)}=n-1 .$$
> $$\boxed{\ \textbf{CC-1★ の例外}\iff v_p\bigl(B_{k_0+(p-1)j^*}\bigr)\ \ge\ j^*+1\ \iff\ \textbf{order-}(j^*{+}1)\ \textbf{の対が order-2 の対と一致}\ }$$
> **証明の骨.** 例外は offset $j$ で $v_p(B_{k_j})\ge j+1$ を要する。$v_p\ge2$ は $j=j^*$ でのみ起こる(Kellner Thm 3.1 + $\Delta\ne0$)⟹ $j=j^*$ に限る。そこで $v_p(B_{k_{j^*}})\ge j^*+1$ が条件。∎
> ### ★ 帰結
> - $j^*=1$: 条件は $v_p\ge2$ ⟹ **$j^*=1$ そのものが例外**(本体 命題 P2-1 と一致 ✔)。
> - $j^*=j\ge2$: 条件は $v_p\ge j+1$ ⟹ **order-$(j{+}1)$ の対が order-2 の対と同じ index に来る**必要 ⟹ 生成的確率 $\approx p^{-(j-1)}$ ⟹ **急速に稀**。
> $$\Longrightarrow\ \boxed{\ \textbf{9/9 空振り($j^*\ne1$)は、}j^*\ge2\ \textbf{枝まで含めて「ほぼ確実に例外なし」へ強化される。厳密化には order-3 データが要る。}\ }$$
> ★ **【P2-GAP-2】は「未処理の穴」から「order-$(j^*{+}1)$ データで閉じる有限の課題」へ降格。**

## 3.3 ★ 主張仕様 — 発効に必要な pin

> ## 主張 **KELL-DECIDE**(発効前・**pin 待ち**)
> $$\boxed{\ \textbf{CC-1★ の例外の有無は、Kellner/BCEM の表により全非正則対 }p<1.2\times10^7\ \textbf{について決定可能である。}\ }$$
> ### 発効に必要な pin(4 点)
> | # | pin 対象 | 何を確かめるか |
> |---|---|---|
> | **K1** ★ | **Table A.3 の $s_1,s_2$ 列の定義の逐語** | $s_2$ が我々の $j^*$(order-2 対の offset)であることを**定義から**確認(9/9 の数値一致は状況証拠) |
> | **K2** | 表の**網羅性** | Table A.3 は 8 素数の抜粋の可能性 ⟹ **BCEM の完全データ**($p<1.2\times10^7$ の全非正則対の order-2 index)が公開されているか |
> | **K3** | **$\Delta\ne0$ の全域性** | 「$p<1.2\times10^7$ の全不規則対で $\Delta\ne0$」の逐語(scout §2 に既載・要 pin 格上げ) |
> | **K4** ★ | **order-3 以上のデータ** | 命題 EXC-ALL より $j^*\ge2$ の枝を閉じるには order-$(j^*{+}1)$ の index が要る。**無ければ主張は「$j^*=1$ 枝について決定可能」に限定** |
> ### 発効できる版(pin の程度に応じて)
> | pin | 発効できる主張 |
> |---|---|
> | K1+K2 のみ | 「**$j^*=1$ 枝**については全非正則対 $p<1.2\times10^7$ で決定可能」(= CC-1★ の例外の**主枝**が全域で決まる) |
> | K1+K2+K4 | 「CC-1★ の例外の有無が全域で決定可能」(**完全形**) |
> | K1 のみ | 「標的 9 番地について表と自前計算が一致」(現状) |
> ⚠ **文献裏書きの格**(追補 A §2 の規約を継承): これは**他人の計算の引用**であって二系統一致ではない。**cross-checked と書かない。**

---

# 4. 編纂への織り込み(§0〜§3 の要点)

**便 114 の相 2 章に載せるべき確定事項**(いずれも candidate・限定つき):

| # | 項目 | 格 |
|---|---|---|
| 1 | **④ の定義**(定義 CONE-2/CONE-4・命題 CONE-A′)と **等値化**(井原予想の $p$ 進の運命 ⟺ $e$ の $\mathbf Z$ 上飽和) | 紙・candidate |
| 2 | **$e$ は $k=16..32$ で飽和**(P-CONE-4 的中)・**$(37,32)$ は枝 E**(P-CONE-5)— 限定 (E1)〜(E4) | 実測+紙 |
| 3 | **こだま素数 = 非正則対**(定理 CC-1★ + 系 CC-1a)・例外は $p^2$ 事象のみ | 紙 |
| 4 | **$\Gamma$ 盾の縁は 9 番地で持つ**(GAMMA-EDGE-9)+ **KELL-DECIDE**(pin 待ち) | 実測+文献 |
| 5 | **$C_k$ の住む環 = 極大整環($p\ge5$)**(CONE-HECKE)+ **命題 SPLIT-FORCED**(分裂は強制)+ **命題 RANK-1**(固有形式枝が確定) | 実測+紙 |
| 6 | **野生帯初段に超過なし**(WILD-NOEXCESS)+ 境界一致の構造的読み(BOUND-ID・TWIN-EDGE) | 実測+紙 |
| 7 | **残る未決 3 点**: $\rho$ 側($\tilde\sigma$ 律速・【CC-GAP-4】)/ $\det C_k$ の分子【CB-GAP-5】/ NORM-CHK の残差 | — |

$$\boxed{\ \textbf{相 2 の骨格}:\ \textbf{④ を作り(1)、}e\ \textbf{側を測り切り(2)、こだまの正体を数論で閉じ(3,4)、小孔の環を同定し(5)、窓側の初段を叩いた(6)。}\ }$$

---

# 5. 【GAP】・帰属

| # | 内容 | 重さ |
|---|---|---|
| **【PS-GAP-1】** ★ | $R_p$ の $S_3$-型の閉形式が未導出($m_{\rm std}(R_7)=2$ の理由が不明)⟹ NORM-CHK は**実測依存** | 中 |
| **【PS-GAP-2】** | 命題 SPLIT-FORCED は「$\{a_\ell\}$ が $\mathcal O_K$ を生成」に依存 ⟹ IDX-2(極大性)が前件 | 小 |
| **【PS-GAP-3】** ★ | 命題 RANK-1 は【CB-GAP-5】($\det C_k$ の分子 $=$ こだま分子)に依存 ⟹ **$\rho$ 側の唯一の未決点** | ★ 大 |
| **【PS-GAP-4】** | KELL-DECIDE は K1〜K4 の pin 待ち。K4 が無ければ「$j^*=1$ 枝限定」 | 中 |
| **【PS-GAP-5】** | 本束の全命題は candidate(単系統・Sol 未監査)・判定語の発効は司令塔専権 | — |

**帰属**: 委嘱 = 司令塔(裁定 782)。生値 = 実装係(PL-LAB-1・T2-SPLIT・算法 B′)。文献 = paper-scout(Kellner 2007)。本束の新規部分 = **命題 NORM-1(正規化判定式 $\mathrm{def}_p=-m_{\rm std}(R_p)$)と発注 NORM-CHK** / §1.2 の残差 3 枝の意味論 / **正札 WILD-NOEXCESS** / **命題 RANK-1**($v_p=1$ + 分裂 + 極大 ⟹ 階数落ち 1) / ★ **命題 SPLIT-FORCED(4/4 の $+1$ は強制)** / **同定 KELL-ID** / ★ **命題 EXC-ALL(例外条件の完全形・【P2-GAP-2】の降格)** / **主張仕様 KELL-DECIDE と pin 4 点・段階発効表** / §4 の編纂骨格。
