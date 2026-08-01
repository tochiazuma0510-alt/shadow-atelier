# 便 99 返信 — 数学便第 26 号・全項監査

## 総合判定

**条件付き PASS。**　最優先四件の裁定は次のとおりである。

| 対象 | 裁定 |
|---|---|
| §1 FAM-U (n=5) 対決・全奇数 domain 復帰 | **PASS**。4 公開予言の的中と versioned domain 復帰を受理する。ただし「二経路」は共有前件を持つので M2 の独立照合や Lean 検証へは昇格しない。復帰宣言は旧 P95-1.1 の改稿ではなく、新しい P99 宣言とする。seal 状態の旧記述 1 箇所には本返信で erratum を出す。 |
| §2.1 (972) | **PASS（整数 972 だけ）**。「二測定」ではなく **ROOF(4) による紙の予測 × 屋根の直接悉皆測定**という型を明記した cross-check 相当で受理する。shadow 集合/NF、U-11、P-IHN-1/2/3、抽象群型には伝播させない。 |
| §4.1 (K^{(5)}) Phase 1 | **GO**。K5-1〜K5-5 の較正だけを認可する。W-6、Phase 2、genuine 結論は解錠しない。K5-MOD には非半単純加群を落とした重大な穴があり、便 100 の定理ゲートでは現形を通せない。 |
| §6 W98-ALG | **PASS**。18 セルの (T_{\rm all},T_{\rm trans}) を照合済み有限計算として受理し、旧 UNKNOWN 12 セルを追記型で更新してよい。`verified` ではない。恒久 fixture の次版編入も条件つきで認可する。 |

分離裁定として、DIV-LAW、W2-arith、REFACT、GEN9-Λ、NO-CENTRAL、THM44-odd 系は後記の小修理/依存表示つきで通す。C2-Q の「(c_2) は検出器にならない」という個別結論は通るが、C2-QR2 と一般メタ主張は差戻す。EP の exact trio は仕様 freeze を通し、lane B の独立 per-point producer 実装を認可するが、W-6 閉鎖・EP 発効・正統性の陽性統制は認可しない。

### F99-0.1　入力・格の監査

便 99 が列挙した **26 artifact は 26/26 で記載 SHA-256 と一致**した。対話帳 T-25〜T-27、`provenance/LEDGER.md` の裁定 384〜410、および該当する CLAIMS/規約も突合した。`search/bundle-selfaudit-v11.py` は現 worktree で再実行し、**24/24 checks PASS**を再現した。ただし self-audit は bundle の構造・pin の検問であって数学の独立照合でも Lean 証明でもない。

本返信で用いる格は次のとおりである。

- `paper-proof candidate`: 紙上証明を監査して通したが Lean 未接続。
- `cross-checked`: 独立性の型と射程を併記した照合済み有限結果。
- `single lane`: 単一 GAP/単一実装の有限結果。
- `verified`: 本便では **0 件**。この語を使わない。

---

## 1. \(n=5\) 開封対決と domain 復帰

### F99-1.1　FAM-U 公開予言 4 項

**PASS。**　凍結後に観測された値は

\[
u_5(\widetilde\alpha=1)=-4,\qquad
u_5(\widetilde\alpha=2)=+4,\qquad
\operatorname{ord}([u_5]_{10})=5,\qquad
[u_5]_2=1
\]

であり、4 項とも公開予言と一致する。符号二値が (4(-1)^{\widetilde\alpha}) を保ち、mod (2) で自明、mod (5) で非自明だから mod (10) の類の位数が 5 になる、という内部整合も通る。`ALLOWED_N` の解除を script/cert の authority 欄に残した作法も versioned な domain 変更として正しい。

ただし二経路は TOWER/SPLIT/W3/W4 等の数学前件と同じ有限表現を共有する。従ってここで得たものは「**held-out \(n=5\) での予言的中と二実装一致**」であり、次の言い換えは禁止する。

- (n)-非依存性が Lean で検証された。
- M2 が独立二系統で照合された。
- 正典との向きが外部実装で照合された。
- NULL が一般に排除された。

FU-SYM の自主制限はそのまま維持する。陽性結果は、危険に曝した式族を支持するが、依存鎖の各札を個別に証明するものではない。

### F99-1.2　domain restore と B-1

**PASS。**　W95-1.2 の三段、f94 の 13 条項別効力表、NULL 11 本の risk 対応表、総組立の追記 B は、過去の記録を改変せず新 addendum で有効 domain を戻す、という正しい versioning になっている。新しい現行 domain は

\[
\boxed{\text{全奇数 }n\ge 3}
\]

でよい。偶数、\(\gcd(\alpha,n)>1\) の外側、未充足の枠組み前件まで同時に解錠したとは読まない。

旧 P95-1.1 は当時の裁定の逐語記録なので、一語を抜いたものを「P95-1.1 逐語」と呼ぶ作法は不可である。旧文は不改変で残し、復帰後の宣言を別 ID で置く今回の作法が正しい。

### P99-1.1　domain 復帰の現行宣言

> **P99-1.1 (FAM-U odd-domain restore).** 奇数 (n\ge3) について、FAM-U の他の明示前件の下で M2 と M4 の紙上鎖は閉じ、補題 LIFT により整数持上げの型も閉じた。従って
> \[
> \operatorname{ord}([u_n]_{2n})=n
> \]
> に至る candidate 鎖をこの domain で採用する。これは旧 P95-1.1 の改稿ではなく、domain 復帰後の新しい P99 宣言である。

「candidate 鎖」を落として無条件定理または `verified` と記帳してはならない。

### W99-1.1　seal 状態の erratum

`fam_u_v1_addendum_domain_restore.md` §9.3 の `seal_PSL_v1` を「維持」とする現況文は、後発の裁定 410 と両立しない。**現在の正本状態は 2026-07-26 開封済み**である。本返信を current erratum とし、過去 artifact 自体は編集しない。

これは FAM-U の非接触性を壊さない。言えるのは「その走査が PSL の開封値を入力しなかった」であって、「PSL seal が当時も現在も閉じている」ではない。

### F99-1.3　射程

`asm_n5restore_ordercheck.py` の宇宙 250・failures 0 は有限整合検査として受理する。ただし同じ式の再計算なので独立照合ではない。今回解除されたのは odd-domain restriction であり、他の framework/isolated/normality/surjectivity 前件は保存される。

---

## 2. 格付け 3 件

### F99-2.1　\(|\mathrm{GT}(K^{(9)}\cap N_{S_4})|=972\)

**整数 972 に限り格上げを受理する。**　正確な型は

\[
\underbrace{\text{ROOF(4) と既存因子 cert からの紙/整数予測 }972}_{\mathrm{R4a}}
\quad\times\quad
\underbrace{\text{屋根 }M\text{ 上 }4{,}408{,}992\text{ 候補の直接悉皆測定 }972}_{\mathrm{R4b}}
\]

の一致である。R4a は (M) を測定していない。従って台帳語は次のどちらかに固定する。

- `paper-predicted × machine-measured, cross-checked for the scalar cardinality 972`; または
- 日本語で「ROOF(4) による紙の予測と屋根の直接悉皆測定が、整数 972 で照合済み」。

「独立二測定」「972 元の集合等号を照合」「正規形まで照合」は不可である。R4b の `generation_fail=0` は、直積成分の hexagon が分かれるだけでは自動にならない Goursat/生成段を実測しており、比較は空虚ではない。

### P99-2.1　972 の CLAIMS 用確定文

> (M=K^{(9)}\cap N_{S_4}) について、命題 ROOF(4) と既存因子 certificate から得る紙の予測 (972) と、(M) 上の (4{,}408{,}992) 候補の直接悉皆列挙による測定 (972) が一致した。**cross-check の対象は基数 972 のみ**であり、二つの独立測定、shadow 集合/NF の同一性、正典向きの独立照合を主張しない。有限測定は Lean 未検証である。

108/54 は同じ受理式・marking の逐語複製を含むので、正典誤りに対する独立 anchor と数えない。とくに 54 は R4a の settled 数と R4b の shadow 数で述語が異なるが、当該 S4 cert では 54 行すべて settled なので、この run に限って集合差が空であることを副検問として使える。

### W99-2.1　格上げと同時に残す修文 queue

次の 6 点は値 972 を覆さないが、次の version で閉じる。

1. 54 を `R4a=settled`, `R4b=shadow`, cert 内では両集合一致、と正確に分離する。
2. R4a の独立 cert と `conventions_used` を作り、片側だけ artifact が無い状態を解消する。
3. 基数だけでなく、少なくとも canonical NF/source map を定義して各 (m)-fiber の 81 元を比較できるようにする。
4. R4b の `conventions_used` を CL-8 の正形 object に直し、欠落欄を明示 `n/a + reason` にする。
5. 落ちるべき dummy/negative fixture を事前登録する。期待値不一致で cert 自体が消える anchor だけでは足りない。
6. shard cert と digest を失効しない永続位置/LEDGER に束縛する。「二環境」は Windows/Linux の再現性であり、GAP 4.16.0 の実装独立性ではないことも記す。

CV-9 主検問が制度成立前で不在、R4a の走査→cert 消費という仕様変更があったことは消せない履歴である。事後 CV-9 は副検問として有用だが、過去に主検問があったことにはしない。

### F99-2.2　U-11 と P-IHN-1/2/3

**据え置きに同意する。**　U-11 の合成 11,664 対は R4a の単系統有限 exhaustive candidate のまま。R4b は積を一度も監査していないので cross-check を伝播させない。P-IHN-1/2/3 も R4b 単系統であり、972 の格上げとは分離する。P-IHN-7 後半の抽象群型にも伝播しない。

### F99-2.3　GTPI 二部作の総合格

**条件付き PASS。**　(A′) (c_3)-pentagon を含む source-map/定義式の紙上忠実性は閉じた。一方、CLOSURE の存在/全射 20 lifts と PB4-settled/NFI は有限計算に論理依存する。従って「紙証明が probe を単なる spot-check に降格した」とは書けない。

### P99-2.2　GTPI の CLAIMS 用確定文

> 固定した (K_\pi/N_0) に対し、source-map の定義式と (c_3)-pentagon の向きは paper-audited である。CLOSURE（20 lifts の存在・全射）および PB4-settled/NFI の有限結論は finite exhaustive artifact に本質的に依存する。総合格は **paper-proof + finite-exhaustive candidate**。settled 段は別の独立照合が付かない限り single lane であり、Lean verified ではない。

数値群構造の主張と canonical-fidelity の主張は CLAIMS で別行にするのが最も安全である。

---

## 3. 定理群 6 束（付随項を含む）

## 3.1 DIV-LAW

### F99-3.1　数学核

**paper-proof candidate として PASS。**　核は次の短いコホモロジー計算で閉じる。(A=C_{n/d})（奇数位数）上で、(Q) の中心元 (z=(-1,0)) が (-1) として作用する。1-cocycle (a) に対し (zq=qz) を二通り評価すると

\[
2a(q)=a(z)-q a(z).
\]

(2\in\operatorname{Aut}(A)) なので (a) は coboundary、従って (H^1(Q,A)=0)。このため kernel (F_0[d]) と全 (Q)-像をもつ補群は共役一意となる。さらに braid 由来の ι anchor が共役の自由度を殺し、安定像は約数 (d\mid n) ただ一つの標準 (H_d) に固定される。PIN-A の ((m,f)=(-1,1)) も二 reduced hexagon と生成条件を直接満たす。

従って、DIV-GEN の genuine 判定を (k\equiv0\pmod{n/d}) の一式へ落とすこと、素数窓が一ビットになること、降下回数が高々 Ω(n) であることは、列挙された前件の下で正しい。

P-DIV-1〜5 の prediction-first freeze は維持してよい。divlaw_check failures 0 は座標式と実装の有限整合検査であり、上の群論証明の代用品でも独立照合でもない。

### W99-3.1　左剰余類を群商と書いている

`div_law_v1.md` の DIV-COSET にある

\[
T/H_d\cong \mathbb Z/(n/d)
\]

は、\(H_d\) が一般に正規でない以上、**群同型としては誤り**である。正しくは「左剰余類集合 \(T/H_d\) は \(\mathbb Z/(n/d)\) で標識でき、その上の \(T\)-作用は affine」とする。剰余類 membership、fake の分割、DIV-GEN の合同判定はこの修正で保たれる。

### W99-3.2　IHNEC-GAP-1 の扱い

「停止深度問題が不要になった」は強すぎる。DIV-LAW は **目的を (d_{\rm gen}) の下界探索へ組み替える**が、元の有限計算上の stopping-depth 問題そのものを解決しない。従って

> ASM 鎖昇格に必要な下界だけを追えばよい場合には、元の stopping-depth 定理を迂回できる。

という conditional reprioritization に直す。`位置は UNKNOWN` の記帳は維持する。

DIV-LAW 自体は抽象有限群の紙上命題、DIV-GEN は E1/HOM/COR54/ARG/INT 等に相対、DIV-ARITH は BFC/RCYC を含む framework-conditional である。この三層を混ぜない。

## 3.2 W2-arith (S2)

### F99-3.2　格の裁定

**Route A を暫定正本として PASS。**　正典の式 \(m=(\widetilde\chi-1)/2\) と W2-fam の \(\widetilde\chi\) を合わせれば、必要な mod \(4n\) の主張は直接出る。TB/算術実現枠組みを必要としない。

- Route A: `paper-proof candidate / canonical-source-relative / framework-independent`。
- Route B: 同じ結論への framework-conditional な冗長経路。
- 補題 CHI とその DIV-SPLIT への投入では Route A を使う。
- Lean verified ではない。

\(\widetilde\chi\) の全射性に使う Kronecker–Weber 入力は標準外部定理として依存表に明記すればよい。

## 3.3 REFACT・GEN9-Λ・NO-CENTRAL・M2・ENT-1

### F99-3.3　REFACT / ENT-CRIT

**PASS。**　(d\mid n) なら

\[
K^{(n)}\cap(K^{(d)}\cap N'_0)=K^{(n)}\cap N'_0
\]

なので、屋根 (K^{(9)}\cap L) を「非分裂」と読む旧レシピは成立しない。共通商 (E_0\ne1) は検出力を含意せず、正しい条件は ENT-CRIT の **(B_3)-安定正規補群が存在しないこと**である。非分裂性は必要条件であって十分条件ではない、という T-27 の修正を採用する。

### F99-3.4　GEN9-Λ と M2 測定

GEN9-Λ は正しい。(K^{(9)}\to K^{(3)}) の reduction image が全 (G_3) なら、GEN(9) の破れは

\[
\Lambda=\ker\bigl(\mathrm{GT}(K^{(9)})\to\mathrm{GT}(K^{(3)})\bigr)\cong C_3^2
\]

にしか残らない。狩場を 9 元へ局在させる結論を受理する。

M2 の (324)、各 (m) 27、settled 324/324、三 reduction 像 108/36/12、(d=1)、R2-11 の 12/12 不発は互いに整合する。ただし **GAP 単系統**であり、有限 exhaustive candidate の格に留める。定理 K3 の既存 paper/cert 鎖と衝突しなかった、までが正確である。

### F99-3.5　NO-CENTRAL と NO-ENT(3)

NO-CENTRAL の (H^2(G_n,\mathbb F_3)=0)（奇数 (n)・自明係数）の計算は通る。さらに便 99 の NO-ENT(3) 候補は、次の形なら **bounded scan を越える紙上定理**にできる。

> **P99-NO-ENT(3).** (N'\triangleleft B_3), (N'\subset K^{(3)}), ([K^{(3)}:N']=3) とする。このとき拡大
> \[
> 1\to C_3=K^{(3)}/N'\to PB_3/N'\to G_3\to1
> \]
> は ENT-CRIT 型の障害をもたない。従ってこの class には (B_3)-安定な非分裂 χ_i-extension は存在しない。

証明は次の 3 段である。

1. \(G_3\) の \(C_3\) への作用は \(G_3\to\operatorname{Aut}(C_3)=C_2\) の指標であり、候補は自明指標と 3 個の非自明 χ_i。
2. (N'\triangleleft B_3) により外側 (S_3=B_3/PB_3) が拡大へ作用する。`Aut(C3)=C2` は可換なので作用指標は (S_3)-不変でなければならない。3 個の非自明 χ_i は (S_3) の一軌道だから、残るのは自明作用だけ。
3. 自明作用なら NO-CENTRAL により (H^2(G_3,C_3)=0)、従って拡大は split。さらに (H^1(G_3,C_3)=\operatorname{Hom}(G_3,C_3)=0)（(G_3^{ab}\cong C_2^2)）なので補群は一意であり、外側 (S_3) にも保存される。よって (B_3)-安定正規補群が得られる。

これで ENT-1 の指数 1944 scan は「その深さで 1 件・split」という校正へ降格し、非存在証明の役割を持たない。NO-ENT(3) の射程は上の **index 3・(B_3)-normal・(K^{(3)}) 内**に固定する。

## 3.4 TRUNC\(^{B_4}\)

### F99-3.6　TRUNC の監査

**外部定理への相対的 paper-proof として PASS。**　制限写像

\[
\operatorname{Aut}(\widehat{PaB})\longrightarrow
\operatorname{Aut}(\widehat{PaB}^{\le4})
\]

について、単射は arity 2 の braid と arity 3 の associator/braiding が全 operad を位相的に生成すること、全射は truncated automorphism の像が arity ≤4 で unit・pentagon・hexagon を満たすことから presentation を介して全 operad へ一意に延長すること、最後に profinite completion の普遍性を使うこと、という 6 段は正しい。

不足していた外部言明形は、Benoît Fresse の一次資料 [*Homotopy of Operads and Grothendieck–Teichmüller Groups, Part 2*](https://pro.univ-lille.fr/fileadmin/user_upload/pages_pros/benoit_fresse/Manuscripts/EnOperadHomotopy-II.pdf) の Theorem 1.1.5（PDF pp. 9–10）で pin できた。同定理は PaB から対象 operad への写像を unit/product/associator/braiding とその coherence relations で特徴づけ、参照元を Fresse I.6.2.4 と明記する。後続箇所には profinite analogue と連続延長も記されている。

従って Thm A.1 の「言明形が不明」という数学 blocker は閉じる。ただし repository 内に当該一次資料の local receipt/page image がまだ無いなら、IHNEC-L3 の取得・digest 記帳は provenance 上の後処理として残す。これは TRUNC の紙上依存を Lean verified に変えるものではない。

### W99-3.3　(OBJ) は無害な省略ではない

上の PASS は **対象を固定する automorphism**、または object-operad 上の作用を明示的に分離した定義に対するものとする。対象 operad 自身に非自明な \(S_2\)-automorphism がある以上、(OBJ) は無害とだけ書いて落とすことはできない。全 automorphism を採るなら、arity \(\le4\) 側にも同じ \(S_2\) が見え、object-fixed 部分の TRUNC と両立することを一段示す。Catalan 数列の一致は対象集合の有限 sanity check であって、この同型の証明ではない。

この object convention を明示すれば、TRUNC は Thm 3.8 の全射段だけでなく、同じ presentation 穴を使っていた単射段も同時に修理する。

FAKE-KILL\(^{B_4}\) の前件は引き続き (IH-S)/(GEN\(^{B_4}\))/(PR\(^{B_4}\))/(CHM\(^{B_4}\)) の 4 札である。TRUNC は full/truncated の橋を閉じるだけで、U-10 や四前件を証明しない。`TRUNC-PAIR = all invertible pairs` の強い版も別途 invertibility 条件を要する。

## 3.5 THM44 奇分岐と派生系

### F99-3.7　紙上補完

**PASS。**　PROP41-EVEN-odd の偶奇計算、THM44-odd の CRT 迂回は循環していない。(m\mapsto m+2nz) で (n) を割る素数に対する条件を保ち、(q) の新しい各素因数について避けるべき剰余類を一つずつ外し、CRT で同時に選べばよい。最後に対応する (k) を持ち上げる。

この補完により、奇 (q) の範囲で GEN-DESC、整除共終な (S) に対する GEN-COFINAL、K\(^{(5)}\) を名指す FIVE-BYPASS、fake の整除上方伝播 FAKE-LIFT を paper-proof candidate として受理する。探索の極小候補を奇素数へ落とす結論もこの射程で正しい。偶 (q) の未掲載分岐まで解いたとはしない。

ML-ODD の抽象 directedness は (COF) だけで足りる。(INT) は roof/intersection の同定に使うが directedness 自体の前件ではない、という依存修正を採用する。FIVE-BYPASS は seal 回避策ではなく、開封後も独立に有効な整合経路である。

## 3.6 C2-Q

### F99-3.8　有限定義・cocycle・D-ODD

**個別核は PASS。**　(Q_N=\gamma_2(P_N)/\gamma_3(P_N)=\langle c\rangle) を使う有限定義、自然性、真の法が (8d) であること、C2-FIN、C2-COC、D-ODD の証明は通る。特に「全 genuine shadow が hexagon+charming だけから C2-FIN を満たす」ので、**(c_2) というこの計器は pentagon 層 (b) の分離器にならない**という閉戦判断は正しい。

ただし D1 の表示

\[
c_2^{raw}:\gamma_2(F_2)\xrightarrow{\sim}\gamma_2(F_2)/\gamma_3(F_2)\cong\mathbb Z
\]

の最初の矢印は同型ではない。正しくは核 \(\gamma_3(F_2)\) をもつ全射であり、同型は quotient から \(\mathbb Z\) への矢印だけである。

### W99-3.4　C2-QR2 は現形で偽

「(3\nmid d) なら 3 が可逆なので任意の (c_2) が square-root 条件を満たす」という推論は成り立たない。例えば

\[
d=5,\qquad c_2=3,\qquad 1+24c_2=73\equiv33\pmod{40}
\]

だが 33 は mod 40 の平方剰余ではない。(3\mid d) の場合も mod 3 だけを調べて mod (8d) 全体の平方根を結論できない（例 (d=15,c_2=3) でも同じ失敗）。

C2-QR の正しい射程は「与えられた scalar congruence に解 (m) があること」と square-root 条件の同値までである。実際の GT-shadow の実現には、λ の (N_{ord}) での単元性、hexagon、surjectivity、(f) の存在が別に要る。既存の genuine shadow から得た (c_2) は C2-FIN により自動的に条件を満たすが、**任意 (c_2) の実現可能性**へ逆向きに使ってはならない。

### W99-3.5　一般メタ主張は差戻し

「gentle 圏で全要素が満たす恒等式は定義関係の帰結でなければならない」は一般には偽である。ある有限対象の全点が偶然満たす恒等式はあり得る。また「((m,\bar f)) の任意の関数は pentagon の破れを検出できない」も広すぎる。外部 source map/pentagon evaluator を組み込んだ関数なら、同じデータ表現から破れを評価し得る。

採用できるのは次の限定命題である。

> **P99-C2-BLIND.** gentle の定義 axioms（hexagon+charming）だけから全称的に導かれる invariant は、それら axioms を満たす候補同士を分離できない。とくに C2-FIN だけから得る (c_2) は pentagon の独立 detector ではない。

一般の ((m,\bar f))-invariant まで blind と言うには、その invariant が gentle-axiom quotient を経由するという factorization theorem が別途必要である。GTPI のような cross-frame 評価はこの限定の外にある。

## 3.7 MCOV と kerchi

### F99-3.9　付随二件

MCOV 119/119 は登録在庫内の bounded calibration として受理する。DIV-SPLIT が (AR) 等の前件下で odd-dihedral target の空性を紙上説明するので、同じ標的への追加 scan は取り下げてよい。「119 件で見つからなかった」自体を一般非存在証明にはしない。

`kerchi_equality_v2.md` 註 2 の CV-10 型 effective-source 注記は PASS。\(\widetilde\chi\) 全射の格は W2 Route A の裁定に従い、不変である。

---

## 4. \(K^{(5)}\) genuine 戦役

### F99-4.1　Phase 1 発火

**GO。**　認可範囲は §5.2 の **K5-1〜K5-5 だけ**である。

1. K5/K15 既存 cert の座標・reduction 突合。
2. 既存 K3 probes の (d=3) anchor。
3. K5 単体 40 元の集合 anchor。
4. K3 単体 12 元の anchor。
5. DF-1/2/3 の識別力 fixture。

K5-BIT の一元判定は、\(N\) の isolated 性から reduction map が homomorphism になる (HOM) を前提にすれば、(AR) や CHI を使わない、という意味で framework-independent である。「一切の前件なし」とは読まない。Phase 1 の較正は後記 K5-MOD の穴に依存しない。

namespace は `certificates/k5gen/` に分離し、既存算術飽和 namespace に書かない。K5-1〜5 のどれかが外れたら S-1/S-2 に従い即停止する。これらが全部当たっても買えるのは測定器の較正だけで、fake 非存在、(d_{gen}(5)) の値、W-6 の存在は買えない。

**非認可**は K5-6 以後、W-2/W-4/W-6 の本測定、Phase 2、PSL roof、封印/曲線データへの接触である。とくに targeted T1 の「見つからない」は非存在証明でないため、将来 T1 が (d=1) を示唆しても T2 悉皆完了前に発見宣言を出さない。

### F99-4.2　X-1 推論水準の干渉

干渉は実在する。測定設計が (u) を入力しなくても、T2 まで閉じた (d_{gen}(5)=1) は

\[
d_{arith}(5)\mid d_{gen}(5)
\]

を介して (d_{arith}(5)=1) を強制し、RCYC/BFC を通じて P1 の一側を決める。従って Phase 2 で (d=1) が確定した時点は **inference-contact event** として即停止・報告する。

ただし衝突選言には、有限測定、HOM/isolated、DIV-LAW/(AR)、DIV-ARITH/RCYC/BFC、FAM-U の (u_5) 測定という全段を残す。「(u) が誤り」または「BFC が誤り」と一足飛びに特定しない。

### F99-4.3　X-2 P1/P2 の実効状態

P1/P2 は、現在は **別の認可済み FAM-U \(n=5\) lane により外部解決・開封済み**と記帳するのが正しい。

- (u_{5,1}=-4, u_{5,2}=+4) から双方の mod 10 類の位数は 5。
- \([-4]_{10}=[4]_{10}\)。ここで商は \(K^\times/K^{\times10}\), \(K=\mathbb Q(\zeta_{20})\) であり、\(-1=\zeta_{20}^{10}\in K^{\times10}\) だからである。従って逆元の類も一致し、P2 も一致する。

ただしこれは `K5 Model-Builder / Freeze2 / BRIDGE-IN が実行された`という意味ではない。K5 genuine 戦役自身の status は **BRIDGE-UNKNOWN / 本測定未発火**のまま、prediction receipt に `resolved externally by authorized FAM-U n=5 lane; provenance u5_fire_20260801 + decision 398` を追記する。過去の封印記録を上書きしない。

### F99-4.4　X-3

裁定 410 を採用する。`seal_PSL_v1 = OPENED (2026-07-26)` が現行正本で、裁定 398 の「維持」は status 誤記。値判断そのものは無傷である。

### W99-4.1　便 100 へ持ち越す K5-MOD の重大穴

Phase 1 の GO には影響しないが、K5-MOD の現証明は定理候補として通せない。

正しいのは「\(\mathbb F_5[G_5]\) の**単純**加群は \(\mathbf 1,\chi_1,\chi_2,\chi_3\)」と各単純係数の \(H^1/H^2\) 計算までである。ところが \(\operatorname{char}\mathbb F_5\mid|G_5|\) なので \(\mathbb F_5[G_5]\) は半単純でない。一般の初等アーベル核 \(B_0\) は単純加群の直和とは限らず、正常 5-群 \(A\) が unipotent に作用する indecomposable module を持ち得る。

従って

\[
\text{「最小の }B_3\text{-安定非中心核は }
\chi_1\oplus\chi_2\oplus\chi_3\text{、次元 }3」
\]

は現前件から出ない。これに依存する「最小 index 125」「最小 frame (K^{(25)})」「標的は (H^2(G_5,A)^{S_3}\setminus\{[K^{(25)}]\})」「規模 62,500 以上」も一般には未確立である。

修理は次の二択である。

1. 定理の前件に `B0 is semisimple / A acts trivially / inflated from Q` を明記して限定版にする。
2. 非半単純 \(\mathbb F_5[G_5]\)-modules と \(S_3\)-equivariant extension を分類し直す。

また F-1 の Schur–Zassenhaus は補群の存在までで、**(B_3)-安定正規補群**を自動には与えない。現稿自身の K5-GAP-3 を維持し、F-1 は exclusion theorem でなく diagnostic にする。F-3 も plain (H^2(G_5,B_0)^{S_3}) だけでなく、外側作用を拡大へ持ち上げる equivariant obstruction を要する。

---

## 5. EP 二請求

### F99-5.1　lane B per-point producer

**実装認可。**　ただし「lane A の同型移植」ではなく、同じ出力契約を満たす **独立 lane B producer** とする。受入条件は次である。

- lane B 自身の curve/native data から各有理根ごとの exact witness を構成する。
- lane A の producer、canonicalizer、branch token 生成 helper、出力 token を import/参照しない。
- normative branch-key schema と literal は共有してよいが、producer code path と derivation は共有しない。
- finite points では (x)-root と (y)-root/rank を、infinity では専用 branch を保存し、全体 degree 12 の会計を per-point から再構成する。
- R1′ と R2′ の両方、mutation/negative fixture、source digest を fail-closed で残す。
- 当面 `diagnostic_construction=true`, `W6_CLOSED=false`。lane B 完成前は `AGGREGATE=ABSENT` を維持する。

lane B ができても閉じるのは AGGREGATE plane までである。`IMAGE-MU=UNKNOWN` が残るため W-6 は OPEN、EP は uncalibrated/UNKNOWN のまま。陽性統制や detector activation は別ゲートである。

### F99-5.2　spec v20 / contract v15 / manifest v15 freeze

凍結済み predecessor v19/v14/v14 は byte 不変のまま残り、新 trio は上書きでなく v20/v15/v15 の追加 plane であることも受理する。

commander receipt が下の exact digest 三つ組を束縛した時点で、新 era plane を PENDING_ADOPTION から ADOPTED へ遷移させ、lane B の実装 authorization を発効してよい。それ以前は PENDING_ADOPTION のまま fail-closed とする。

**exact trio の Sol freeze gate は PASS。**　相互 pin、W6KEY の 6 必須列、`IMAGE-MU UNKNOWN => overall PASS 不可`、AGGREGATE の不在状態、PENDING_ADOPTION の遷移条件はいずれも整合している。現 worktree で self-audit 24/24 を再現した。8 suite 892 PASS は裁定 392 の log provenance を受領するが、本便で 892 test 自体を再走したとは記帳しない。

```text
predicate_spec_freeze_id =
  "mb/ninfty-stage2-freeze/92025385-8f26416b-72623050"

sol_freeze_gate = PASS

predicate_spec_id = "mb/ninfty-stage2-predicate/v20"
predicate_spec_digest =
  92025385eed864ca036df3f59153597fd60dc5ca3a66a04fd21251a51563ec3a

verifier_contract_id = "mb/ninfty-verifier-contract/v15"
verifier_contract_digest =
  8f26416be35a34251efdbf24188826705fe7a8417243bd61cb5ecfbcda004fab

dependency_manifest_schema_id = "mb/dependency-manifest/v15"
dependency_manifest_schema_digest =
  72623050cca3fef45b09e458ef671a4d6bfc8d9038959b98b0ff586e121a66db

selfaudit_id = "bundle-selfaudit/v11"
selfaudit_digest =
  fd56c4f6457926ff4897de1e6924cad0a416891f5b1253f287b327b5ceec9e37
```

commander receipt の推奨 ID は

```text
mb/ninfty-stage2-freeze-receipt/sol99/92025385-8f26416b-72623050
```

である。発効対象は **W6KEY plane を含む仕様 bundle と、上記 lane B 実装 scope**。次は発効対象外である。

- `W6_CLOSED=true`
- `IMAGE-MU=PASS`
- EP detector の activation/mint
- positive-control event
- candidate 受理または Freeze 2 解錠

これらを同じ「freeze PASS」から暗黙に導出してはならない。

---

## 6. W98-ALG

### F99-6.1　18 セル正式検収

**PASS（cross-checked finite result、Lean 未検証）。**　route A/B は partition 生成、hook/character recurrence、determinant、rim-hook 方向を別実装にし、18/18 で整数値と contribution digest が一致した。さらに二項反転 18/18、(a=9) の RH 先行予言、指標を使わない小 (n) 総当たり 30 ケース、ALG-3 を使わない類乗積直撃が別角度を与える。Windows/Python 3.13 と Linux/Python 3.14 の 180/180 一致は環境再現性であり、独立数学 route とは数えない。

受理する exact table は次である。

| ℓ | \(a\) | \(T_{\rm all}\) | \(T_{\rm trans}\) |
|---:|---:|---:|---:|
| 37 | 0 | 2,011,535,710 | 2,011,535,710 |
| 37 | 1 | 4,679,183,836 | 2,667,648,126 |
| 37 | 2 | 10,643,405,866 | 3,296,573,904 |
| 37 | 3 | 24,056,578,600 | 4,152,376,800 |
| 37 | 4 | 52,751,075,158 | 3,679,996,320 |
| 37 | 5 | 111,545,928,340 | 3,306,663,360 |
| 37 | 6 | 228,753,490,786 | 3,199,996,800 |
| 37 | 7 | 456,206,091,616 | 319,999,680 |
| 37 | 8 | 883,762,688,590 | 639,999,360 |
| 41 | 0 | 33,331,783,448 | 33,331,783,448 |
| 41 | 1 | 77,994,118,780 | 44,662,335,332 |
| 41 | 2 | 185,344,366,464 | 62,687,912,352 |
| 41 | 3 | 428,742,375,920 | 73,359,849,420 |
| 41 | 4 | 955,559,694,328 | 74,011,697,760 |
| 41 | 5 | 2,070,568,312,068 | 83,388,745,440 |
| 41 | 6 | 4,379,610,428,960 | 60,281,020,800 |
| 41 | 7 | 9,029,008,665,304 | 35,459,424,000 |
| 41 | 8 | 18,097,451,796,120 | 21,275,654,400 |

RH 予算

\[
3f_2+4f_3=\ell+6-5t-12\gamma
\]

によりこの族では (t\ge9) の RHS が負になり、(T_{\rm trans}=0) が先に出る。(a=9) の (T_{\rm all}) がその二項変換予言へ厳密一致したことは強い境界試験である。「1/10 段差」は一般法則でなく、RH の 5 刻みと当該 smooth integer の組合せである。

route A/B は高水準の character formula ALG-1/2 を共有するため、それだけなら formula 自体の誤りを共倒れで見逃し得る。小 (n) brute と class-multiplication 直撃がその穴を部分的に塞いでいる、という依存表示を残す。

### P99-6.1　旧 UNKNOWN 12 セルの更新認可

**認可する。**　過去行を編集せず、次の provenance をもつ superseding entry を追記する。

```text
result_scope = corresponding 12 cells only
status = cross-checked finite computation
cert = search/certs/w98_alg_driver_cert_20260801.json
cert_sha256 = 6f030dacf9ae6c2ad388c240a72f6b61184618027e5a79693f58cfded9a398ea
report = mine/reports/w98-alg-18cells-20260801_report.md
report_sha256 = 3ede53671a590eefb2fe10045e49532dc625a43aafde1c6ab2fa26db792f882c
driver_sha256 = 991a8c1f0c233999c7d4aa8296fadad09170a8acece8c5f3e9ec92e0b2c4b052
lean_verified = false
```

旧 `UNKNOWN` は当時の正しい履歴として残す。

### P99-6.2　恒久 fixture

次版 driver への編入を **条件つきで認可**する。

- (n=10,11,12,13) の直接 brute 30 ケースを固定する。
- ℓ=9 の非単調消滅ケースを、落ち方を区別する negative/boundary fixture として固定する。
- 期待値、universe、式 ID、fixture source digest を versioned cert に保存し、失敗時も failure cert を残す。
- Windows 絶対 path を排除する。
- 「独立 fixture」と数える実装は main driver/helper を import せず、直接 permutation/class multiplication から計算する。

fixture の編入は既存 cert を改変せず、新 driver/cert version で行う。

---

## 7. 規約台帳 v1.4

### F99-7.1　総合ゲート

**条件付き PASS。**　CV-10（effective source chain）と CV-11（seal recoverability）の既存主項に対する §1.5/§1.6 の細則として置くなら番号衝突はない。動機となった 5 例も妥当である。ただし次の二つを条文上明確にしてから adopted とする。

### P99-7.1　CV-10 証明本文 status の正形

トップレベル三値は例えば次とする。

```text
proof_body_status = present | omitted | external_reference
```

`omitted` には追加で

```text
omission_kind = reader_exercise | silent_omission
source_wording = <exact page/line wording or null with reason>
```

を必須にする。「読者演習」と「証明本文が単に無い」を一値で潰してはならない。`external_reference` では cited theorem、版、ページ画像 pin、取得 digest を必須にする。今回の TRUNC は `external_reference`、THM44 奇分岐は `omitted + reader_exercise` に当たる。

### P99-7.2　CV-11 開封状態の二鍵

開封状態は

1. `provenance/seals/*.opened.json` の存在、かつ
2. LEDGER の opened event

の **AND** で決める方針を採用する。ただし mere existence では弱い。opened JSON は元 seal ID/digest、開封 blob digest、opening event/receipt ID を束縛し、LEDGER 側も opened artifact digest を pin しなければならない。二鍵が欠ける、または digest が食い違う場合は `OPENED`/`SEALED` を推測せず `INTEGRITY_STOP / UNKNOWN` とする。sealed vault の在庫が残っていることから status を推論しない。

この修文が入るまで v1.4 の数学的趣旨は PASS、schema adoption は conditional とする。

---

## 8. 情報共有項の受領と現物訂正

### F99-8.1　受領

裁定 384〜410、地図第 3 版、HS-1 の Prop. 7 所在、発案 6 札、二件の実装係自己申告を情報として受領した。監査対象外なので HS 移送案や発案 B/C の格は本便で上げない。自己申告は予言接触の除去と事故記録として正しい運用である。

### W99-8.1　PackageGT の「未収蔵」は現 worktree と不一致

便本文の「Dolgushev GT パッケージは未収蔵・`papers/` は PDF 4 本のみ」という全 repository 向けの記述は、現在の現物とは一致しない。次が存在する。

```text
thirdparty/packageGT/PackageGT.zip
sha256 = c3124483cb1464b9010c091011370db091a76561a2af923a38efb6900f645f95

thirdparty/packageGT/PackageGT_README.pdf
sha256 = 90545f5ea820b41c8bb16c5719c2540d39207f5247a4649fc4d784f1612468f1
```

ZIP の listing には `PackageGT/PaB.py`, `Aux.py`, `README.tex` 等の payload がある。従って正確な状態は少なくとも **「archive は収蔵済み、展開・較正・実行可能性/正典同定は未監査」**である。もし裁定 403 の「未収蔵」が `papers/` 棚だけ、または usable installation だけを意味したなら、その scope を明記する。IHNEC-L2 は再取得からではなく、まず archive の provenance、README、依存、既知例での較正を検分するのが先である。

---

## 最終アクション表

### P99-9.1　直ちに進めてよいもの

1. FAM-U odd-domain の P99-1.1 による現行宣言。
2. 972 の scalar-only 格上げと GTPI の分離 CLAIMS 記帳。
3. NO-ENT(3) の上記紙上定理化。
4. K5 Phase 1 の K5-1〜5。
5. lane B の独立 per-point producer 実装。
6. EP exact trio の freeze receipt 発行（W6/EP status は OPEN/UNKNOWN のまま）。
7. W98 18 セル受理、旧 12 UNKNOWN の追記型更新、fixture v-next。

### W99-9.1　同じ裁定から進めてはいけないもの

1. K5-MOD の一般形、最小 (K^{(25)}) frame、W-6/Phase 2。
2. C2-QR2 の任意 (c_2) 実現性と、全 ((m,\bar f))-invariant の blind 定理。
3. DIV-LAW による stopping-depth 問題そのものの解決宣言。
4. EP の W6 closure、IMAGE-MU PASS、detector activation、Freeze 2。
5. 972/W98/各 GAP cert への `verified` 表示。

★ 本便の構造的な教訓は二つある。第一に、**陽性予言の全的中は domain を戻す強い根拠だが、共有前件の個別証明にはならない**。第二に、**単純加群の分類は、標数が群位数を割るとき一般加群の分類ではない**。K5-MOD の穴は後者の典型であり、Phase 1 の良い較正設計と分離して扱えば戦役全体を止めずに修理できる。
