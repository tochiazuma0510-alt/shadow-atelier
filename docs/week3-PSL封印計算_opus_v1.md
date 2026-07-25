# 委嘱 06 回答 — PSL(2,7)/(2,8)/(2,11) の許容 (k,k,k) marking と n_m 封印予測(ブラインド起草)

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 06 の任務 1–4。**
**ブラインド規律**: 本稿は共有ツリー外(金庫 staging)。`sol/` は本委嘱中一切読んでいない(便 09 の内容は未見)。読んだのは `docs/`(狩場計画 v4・週3 20の正体 v1・定義ノート v2・manifest v1・文献配達 01–04)と `certificates/` のみ。

依存: `docs/week3-狩場計画_v4.md`(定理 T2・系 T2-A′・系 T2-B)・`docs/week3-20の正体_opus_v1.md`(補題 1–5・命題 S)・`docs/week1-定義ノート.md` v2・`docs/文献配達_02`(§3 MacBeath)・`docs/文献配達_03`(§1 第一段 scalar 化)・`docs/文献配達_04`(rigidity)。

---

## 0. 結論(先に 6 行)

1. **(k,k,k) 対称性は仮定ではなく定理**(定理 M1): c ∈ N なる許容対象では τ = Ad(δ̄) ∈ Aut(P) が X,Y,Z を巡回置換するので **ord(X) = ord(Y) = ord(Z) = k は自動**。θ,τ の Aut(G) への延長も定義から自動。よって任務 1 は「**G を PB₃/N にもつ c ∈ N 許容対象の N_ord = k の決定**」に等しい。
2. **許容 marking は 2 型に完全分類される**(定理 M2): **case A(split-inner)** Q ≅ G × S₃ と、**case B(outer)** Q ≅ Aut₂(G) ×_{C₂} S₃(2 | |Out(G)| のときのみ)。**それ以外は無い**。
3. **許容 k の完全決定**(定理 M3・(2,3,e)-生成に同値):
 **PSL(2,7)**: case A **k = 7** のみ / case B **k = 4** のみ。
 **PSL(2,8)**: case A **k = 7** と **k = 9**(3\|k・別記)のみ。**case B は存在しない**(Out = C₃ は S₃ の商でない)。
 **PSL(2,11)**: case A **k = 11** のみ / case B **k = 5** と **k = 6**(3\|k・別記)のみ。
4. **n_m は全窓で一定 = e := ord(w)**(w = σ̄₁ の P- resp. Aut₂(G)-成分)。これは **|C_Ã(v̂_m)| に等しい = 三つ組が rigid**(配達 04 の語彙)。
5. **|GT(N)| = ψ(k)·e**、ψ(k) := #{m ∈ ℤ/k : gcd(2m+1,k)=1} = 2^a·φ(k_odd)(k = 2^a k_odd)。
6. **命題 S(「\|GT\| = φ(k)·k」)の成否**: **case A では成立(4/4 の新窓で的中)**・**case B では破れる(3/3 で破れ)**。しかも **case B の対象は isolated でない**(shadow の半分だけが settled)— atlas 初の非 isolated 対象の予測。

---

## 1. 一般枠組み

記法は狩場計画 v4 §2 に従う。N を許容対象、**c ∈ N**、P := PB₃/N、A := [P,P]、Q := B₃/N、Δ̄, δ̄ ∈ Q、θ = Ad(Δ̄)\|_P、τ = Ad(δ̄)\|_P、σ̄₁ = δ̄⁻¹Δ̄、X̄ = σ̄₁²、k = N_ord = ord(X̄)、u = 2m+1。

### 定理 M1((k,k,k) 対称性と Aut 延長の自動性)【紙上証明・新規】

> **定理 M1.** c ∈ N なる任意の許容対象について、F₂ = ⟨x,y⟩, z = (xy)⁻¹ の像 X,Y,Z ∈ P は
> $$ Y = \tau(X),\quad Z = \tau(Y) = \tau^2(X),\quad XYZ = 1,\qquad \theta(X) = Y,\ \theta(Y) = X,\ \theta(Z) = Z^{X}. $$
> ゆえに **X, Y, Z は P 内で共役**であり、とくに
> $$ \mathrm{ord}(X) = \mathrm{ord}(Y) = \mathrm{ord}\bigl((XY)^{-1}\bigr) = k $$
> が**恒等的に成り立つ**。さらに θ, τ は定義から Aut(P) の元(Ad(Δ̄), Ad(δ̄) の制限)であり、**「Aut(G) に延びる」ことは追加条件ではない**。

**証明.** τ は F₂ 上 x ↦ y ↦ z ↦ x を誘導する自己同型で、定理 T2(ii) より P 上 τ = Ad(δ̄)。したがって Y = τ(X) = δ̄Xδ̄⁻¹、Z = τ(Y)。XYZ = 1 は F₂ の関係式 xyz = 1 の像。θ は x ↦ y, y ↦ x を誘導し θ(z) = θ((xy)⁻¹) = (yx)⁻¹ = x⁻¹(xy)⁻¹x = z^x。共役ゆえ位数一致 ∎

> ★ **意義**: 三角群文献((ℓ,m,n)-生成)では等位数は強い制約だが、**本工房の枠組み(hexagon の S₃ 対称性)では自動**。委嘱 06 の任務 1 は実質「N_ord = k を実現する許容対象の存在」に還元される。「(k,k,k) marking が存在しない k」は「その k を N_ord にもつ許容対象が存在しない k」と同義。

### 定理 M2(許容 marking の完全分類)【紙上証明・新規】

> **定理 M2.** G を有限非可換単純群、N を c ∈ N かつ PB₃/N ≅ G なる許容対象とし、Q = B₃/N と置く。C := C_Q(G) と置くと C ∩ G = Z(G) = 1、Q/GC ↪ Out(G)、かつ Q/G ≅ S₃ ゆえ **Q → Out(G) の像は S₃ の商かつ Out(G) の部分群 ∈ {1, C₂}**。それに応じて:
>
> **(A) 像 = 1(split-inner)**: Q = G × C、C ≅ S₃。marking 規約(§2.4)の下で
> $$ \bar\Delta = (s,(1\,2)),\quad \bar\delta = (t,(1\,2\,3)),\qquad s^2 = t^3 = 1 \text{ in } G. $$
> **(B) 像 = C₂**(2 \| \|Out(G)\| のときのみ): C ≅ C₃、Ã := Out(G) の位数 2 部分群の Aut(G) 内の逆像(\|Ã\| = 2\|G\|)と置くと
> $$ Q \;\cong\; \tilde A \times_{C_2} S_3 \;=\; \{(a,\sigma) \in \tilde A\times S_3 : \pi(a) = \mathrm{sgn}(\sigma)\},\qquad \bar\Delta = (\hat a,(1\,2)),\ \bar\delta = (\hat t,(1\,2\,3)) $$
> で â は Ã \ Inn(G) の対合、t̂ ∈ Inn(G) は位数 3。
>
> いずれの場合も **\|Q\| = 6\|G\|** であり、w := σ̄₁ の第一成分(= t⁻¹s resp. t̂⁻¹â)、X = w²、k = ord(X)、**e := ord(w)**。

**証明.** C = C_Q(G) は Q の正規部分群で C ∩ G = Z(G) = 1(G 単純非可換)。Q → Aut(G) の核は C、像は Inn(G) を含む。よって Q/C ↪ Aut(G) かつ Q/GC ↪ Out(G)。この写像は G を殺すので Q/G ≅ S₃ を経由し、像は S₃ の商 ∈ {1, C₂, S₃} であって同時に Out(G) の部分群。
- 像 = 1 なら Q = GC、C ≅ Q/G ≅ S₃、G ∩ C = 1 かつ双方正規 ⇒ **Q = G × S₃**。ε は G を殺すので ε\|_C は同型、marking 規約より Δ̄ の C-成分は転置、δ̄ の C-成分は 3-サイクル。Δ̄² = 1 ⇒ s² = 1、δ̄³ = 1 ⇒ t³ = 1。
- 像 = C₂ なら GC/G ⊴ Q/G ≅ S₃ で商 C₂ ⇒ GC/G ≅ A₃ ⇒ **C ≅ C₃**。\|Q/C\| = 6\|G\|/3 = 2\|G\| かつ Q/C ↪ Aut(G) ⇒ Q/C ≅ Ã。写像 Q → Ã × S₃ は核 C ∩ G = 1 で単射、像の位数 6\|G\| = \|Ã ×_{C₂} S₃\| かつ像は fiber product に含まれる(両方の C₂ は「外部性」を測る同じ写像)⇒ 同型。
- **像 = S₃ は不可能**(S₃ ↪ C₂ も S₃ ↪ C₃ も無い。一般に Out(G) が S₃ を含む場合は原理的に起こり得るが、本委嘱の 3 群では Out = C₂ or C₃ なので除外される)。∎

> **系 M2-a(PSL(2,8) には case B が無い)**: Out(PSL(2,8)) = C₃ で、C₂ も S₃ も C₃ の部分群でない ⇒ **像は 1 のみ**。したがって PSL(2,8) の許容対象はすべて split-inner。

### 定理 M3(許容性 ⟺ (2,3)-生成)【紙上証明・新規】

> **定理 M3.** 定理 M2 の記法で、Ĝ := G(case A)/ Ã(case B)を「周囲群」と呼ぶ。s(resp. â)を Ĝ の対合、t(resp. t̂)を位数 3 の元、w := t⁻¹s、X := w²、Y := τ(X) = tXt⁻¹ と置く。このとき
> **(i)** **XYZ = 1 は自動**(Z := t²Xt⁻²)。
> **(ii)** ⟨X,Y⟩ ⊴ ⟨s,t⟩。
> **(iii)** k := ord(X) > 1 のとき **⟨X,Y⟩ = G ⟺ ⟨s,t⟩ = Ĝ**。
> **(iv)** Q = ⟨Δ̄, δ̄⟩ は (iii) から**自動**。
> **(v)** e := ord(w) と置くと **k = e/gcd(2,e)**。case A では ⟨s,t⟩ = G が Δ(2,3,e) の商、case B では w は外部元ゆえ **e は偶数**で k = e/2。
> **(vi)** σ̄₁ の Q における位数は 2k(系 T2-A′ の exact order 条件)を**自動的に**満たす。

**証明.**
(i) s = tw より、s² = 1 と t³ = 1 を用いて
XYZ = (t⁻¹st⁻¹s)(st⁻¹st⁻¹)(tst²st) = t⁻¹st⁻¹·(s s)·t⁻¹st⁻¹·t·st²st = t⁻¹ s t s t⁻¹ · t s t² s t = t⁻¹ s t (s s) t² s t = t⁻¹ s t³ s t = t⁻¹ s s t = 1 ∎
(ii) θ = Ad(s) は {X,Y} を交換し Z ↦ Z^X、τ = Ad(t) は X→Y→Z→X を巡回。ゆえに ⟨X,Y⟩ = ⟨X,Y,Z⟩ は s,t の両方で正規化され、⟨s,t⟩ = ⟨w,t⟩ ⊇ ⟨X,Y⟩ の中で正規 ∎
(iii) (⇐) case A: ⟨X,Y⟩ ⊴ G 単純で X ≠ 1 ⇒ = G。case B: ⟨X,Y⟩ ⊴ Ã かつ ⟨X,Y⟩ ≤ Inn(G) ≅ G、M ⊴ Ã で M ≤ G なら M ⊴ G ⇒ M ∈ {1,G} ⇒ = G。(⇒) ⟨X,Y⟩ = G ≤ ⟨s,t⟩ ≤ Ĝ で、case B では â ∉ G ⇒ ⟨s,t⟩ = Ã ∎
(iv) R := ⟨Δ̄,δ̄⟩ ≤ Q は Ĝ 成分にも S₃ 成分にも全射(⟨σ,ρ⟩ = S₃)。Goursat より R は Ĝ と S₃ の共通商によるファイバー積。case A: G 単純非可換ゆえ S₃ との共通商は 1 のみ ⇒ R = G × S₃ = Q。case B: Ã = PGL 型の商は Ã, C₂, 1、S₃ との共通商は C₂ か 1。1 なら \|R\| = 12\|G\| > \|Q\| で矛盾 ⇒ C₂ ⇒ \|R\| = 6\|G\| = \|Q\| ⇒ R = Q ∎
(v) X = w² ゆえ k = ord(w²) = e/gcd(2,e)。case B: w = t̂⁻¹â は外部(内部×外部)、ord が奇なら w ∈ ⟨w²⟩ ≤ Inn(G) で矛盾 ⇒ e 偶 ∎
(vi) σ̄₁ = (w, ρ⁻¹σ) で ρ⁻¹σ は転置。ord(σ̄₁) = lcm(e,2)。case A(e = k 奇)で 2k、case B(e = 2k)で 2k ✔ ∎

> ★ **これで任務 1 は「Δ(2,3,e) の全射商としての Ĝ の分類」に完全に翻訳された**。**MacBeath の trace 三つ組**(配達 02 §3)はこの分類の古典的解答であり、下の §2 はその特殊値の読み取りに相当する(私は独立に列挙で確認した)。

### 補題 N(n_m の判定式 — case A/B 統一形)【紙上証明・新規】

> **補題 N.** 定理 M2/M3 の記法で A = [P,P] = G(G 単純非可換)。f ∈ G について
> $$ (\text{H-a})\ (\bar\Delta\bar f)^2 = 1 \iff (s f)^2 = 1 \text{ in } \hat G,\qquad
> (\text{H-b}')\ (\bar\delta^{-1}\bar Y^m\bar f)^3 = 1 \iff (t^{-1}Y^m f)^3 = 1 \text{ in } \hat G. $$
> ĝ := s f(f ↦ ĝ は G から剰余類 s·Inn(G) への全単射)、r̂ := w^u ĝ と置くと両条件は **r̂³ = ĝ² = 1 かつ r̂ĝ = w^u** に同値。ゆえに
> $$ \boxed{\ n_m \;=\; N_{\hat G}(w^{u}) \;:=\; \#\{(r,g)\in T_3(\hat G)\times T_2(\hat G)\ :\ rg = w^{u}\}\ } $$
> であり、**古典 Frobenius の scalar 類積公式**
> $$ n_m \;=\; \frac1{|\hat G|}\sum_{\chi\in\mathrm{Irr}(\hat G)}\frac{S_2(\chi)S_3(\chi)}{\chi(1)}\ \overline{\chi(w^{u})},\qquad S_j(\chi) = \sum_{x^j=1}\chi(x) $$
> **で指標表だけから計算できる**。

**証明.** case A は委嘱 05 補題 3 そのもの(Q = G × S₃ の S₃ 成分は σ² = ρ³ = 1 で消える)。case B: Δ̄f̄ = (â·Ad f, σ)、その平方の S₃ 成分は σ² = 1 ゆえ (H-a) ⟺ (â·Ad f)² = 1 in Ã。同様に (H-b′) ⟺ (t̂⁻¹Ad(Y^m f))³ = 1。委嘱 05 補題 2(v_m = σ̄₁^u)を Q に適用すると v̂_m = w^u。あとは ĝ := s f の置換で同じ計算 ∎
**scalar 化の正当性**: case A は委嘱 05 補題 3(z₂(G) は中心的)。**case B では剰余類 C = Δ̄A への制限が問題になるが、パリティが自動的に効く**: r ∈ T₃(Ã) は必ず Inn(G) に入り(位数 3 の元は Ã → C₂ で自明)、w^u は外部(u 奇)なので **g = r⁻¹w^u は自動的に外部剰余類に入る**。したがって「Δ̄A に制限した z_{2,C}」を使う必要がなく、**Ã 全体の中心元 z₂(Ã) がそのまま使える** ⇒ 行列値 F13 基準式ではなく古典 scalar 公式で足りる ∎

> ★ **【GAP-E2a】のさらなる部分閉鎖**: 配達 03 §1 第一段(「剰余類を共役類に分解すれば中心的」)の**もっと強い形が本設定では成立**する — **剰余類制限そのものがパリティで自動的に課される**ので分解すら不要。case A/B いずれも指標表のみで閉じる。**残る UNKNOWN は A ⊊ P(可解対象)の場合だけ**(委嘱 05 の絞り込みどおり)。

---

## 2. 任務 1 — 許容 k の決定(存在/非存在の証明つき)

**基本補題(三角群の低位数排除)**: 1/2 + 1/3 + 1/e ≥ 1 ⟺ e ≤ 6。e ≤ 5 で Δ(2,3,e) は有限(S₃, A₄, S₄, A₅)、e = 6 で Δ(2,3,6) ≅ ℤ²⋊C₆ は可解。ゆえに **e ≤ 6 の全射商は可解か A₅ の商**。PSL(2,7), PSL(2,8), PSL(2,11), PGL(2,7), PGL(2,11) はいずれも非可解かつ ≇ A₅ ⇒ **許容 marking は e ≥ 7 を要求する**。

| G | case | 周囲群 Ĝ | Ĝ\Inn の位数集合(case B のみ) | 排除される e | **許容 e** | **k = e/gcd(2,e)** | 3 \| k |
|---|---|---|---|---|---|---|---|
| PSL(2,7) | A | PSL(2,7)(位数 168) | — | 1,2,3,4(≤6 の基本補題+元位数 {1,2,3,4,7}) | **7** | **7** | no |
| PSL(2,7) | B | PGL(2,7)(336) | {2, 6, 8} | 2(k=1)・6(基本補題) | **8** | **4** | no |
| PSL(2,8) | A | PSL(2,8)(504) | — | 1,2,3(元位数 {1,2,3,7,9}) | **7**, **9** | **7**, **9** | no / **yes** |
| PSL(2,8) | B | — | **存在しない**(系 M2-a) | — | — | — | — |
| PSL(2,11) | A | PSL(2,11)(660) | — | 1,2,3,5,6(元位数 {1,2,3,5,6,11}・e=5 は A₅・e=6 は可解) | **11** | **11** | no |
| PSL(2,11) | B | PGL(2,11)(1320) | {2, 4, 10, 12} | 2(k=1)・4(Δ(2,3,4)=S₄) | **10**, **12** | **5**, **6** | no / **yes** |

**「なし」の証明**: 上表の「排除される e」欄はすべて (i) 周囲群の元位数表(計算で確認)+ (ii) 基本補題(≤6 は可解 or A₅)+ (iii) k = 1(X = 1 は ⟨X,Y⟩ = G に反する)の 3 つだけで閉じる。**それ以外の k は周囲群に該当位数の元が無いか、三角群が小さすぎて全射になれない**。したがって上表の k 以外は**存在しない(証明済み)**。

**「あり」の証明(構成的)**: 各許容 e について明示 marking を与えた(§5 の行列)。生成性・⟨X,Y⟩ = G・XYZ = 1・ord(σ̄₁) = 2k を全て機械確認した(§7)。

**対象の個数(marked 同型類 = 対象 N の個数)**:

| 窓 | 生成対 (s,t) の総数 | Inn(G)-軌道 | **Aut-軌道 = 対象 N の個数** | 個数の説明 |
|---|---:|---:|---:|---|
| PSL(2,7) A k=7 | 336 | 2 | **1** | 位数 7 の 2 類(7A/7B)を Out = C₂ が融合 |
| PSL(2,7) B k=4 | 672 | 2 | **2** | PGL の位数 8 の 2 類(8A/8B)。外部自己同型は既に Ã 内で使用済 ⇒ 融合しない |
| PSL(2,8) A k=7 | 1512 | 3 | **1** | 位数 7 の 3 類を Out = C₃(体自己同型)が融合 |
| PSL(2,8) A k=9 | 1512 | 3 | **1** | 位数 9 の 3 類を C₃ が融合 |
| PSL(2,11) A k=11 | 1320 | 2 | **1** | 位数 11 の 2 類を Out = C₂ が融合 |
| PSL(2,11) B k=5 | 2640 | 2 | **2** | PGL の位数 10 の 2 類(10A/10B) |
| PSL(2,11) B k=6 | 2640 | 2 | **2** | PGL の位数 12 の 2 類(12A/12B) |

> **case B の 2 対象は数値予測が完全に一致する**(§7 で両軌道を独立に計算し確認)。以下の封印値は両対象に共通。

---

## 3. 任務 2 — n_m の紙計算(scalar 類積公式)

### 3.1 使用した指標表(自前構成・直交性で自己検証済)

PSL(2,q)/PGL(2,q) の標準理論から**自分で組んだ**(文献値の丸写しではない)。次数と値の型:
- **PSL(2,7)**(168、6 類 1A/2A(21)/3A(56)/4A(42)/7A(24)/7B(24)): 次数 1,3,3,6,7,8。3 次元は 7A/7B 上で α = (−1+i√7)/2 とその共役。
- **PSL(2,8)**(504、9 類 1A/2A(63)/3A(56)/7A,7B,7C(72)/9A,9B,9C(56)): 次数 1, 8(Steinberg), 9×3(principal series・分裂トーラス C₇ の非自明指標)、7×4(discrete series・非分裂トーラス C₉)。
- **PSL(2,11)**(660、8 類 1A/2A(55)/3A(110)/5A,5B(132)/6A(110)/11A,11B(60)): 次数 1, 5,5(q≡3 mod 4 の例外対・11A/11B 上で (−1±i√11)/2), 10,10, 11(St), 12,12。
- **PGL(2,7)**(336、9 類 1A/2A(21)/2B(28,外部)/3A(56)/4A(42)/6A(56)/7A(48)/8A,8B(42)): 次数 1, 1(sgn), 7, 7(St·sgn), 8×2, 6×3。
- **PGL(2,11)**(1320、13 類): 次数 1, 1, 11, 11, 12×4, 10×5。

**自己検証**: Σχ(1)² = \|Ĝ\| と**行の直交関係を全ペアで数値検証**(§7 のスクリプトが 5 表すべてで `orthogonality OK`)。ゆえに以下の計算は「文献の権威」ではなく**自分で検証した表**に立つ。

### 3.2 手計算(1 例を全展開・残りはスクリプト)

**PSL(2,7)・case A・v ∈ 7A**: S₂(χ) = χ(1)+21χ(2A)、S₃(χ) = χ(1)+56χ(3A) より
| χ | 1 | 3a | 3b | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|
| S₂ | 22 | −18 | −18 | 48 | −14 | 8 |
| S₃ | 57 | 3 | 3 | 6 | 63 | −48 |
| S₂S₃/χ(1) | 1254 | −18 | −18 | 48 | −126 | −48 |
| χ̄(7A) | 1 | ᾱ | α | −1 | 0 | 1 |

Σ = 1254 + (−18)(ᾱ+α) + 48(−1) + 0 + (−48)(1) = 1254 + 18 − 48 − 48 = **1176**、÷168 = **7** ✔(α+ᾱ = −1)。
同様に **PSL(2,11)・11A**: Σ = 6216 + 1260 − 1440 + 1200 + 0 + 12 + 12 = 7260、÷660 = **11** ✔。
**PGL(2,7)・8A**: Σ = 2850 + 342 − 126 − 378 + 0 = 2688、÷336 = **8** ✔(σ₁ と σ₃ の ∓√2 項が相殺)。
**PSL(2,8)・7A**: (3648 − 48 + 72·Σ_{a=1}^{3}2cos(2πa/7))/504 = (3648 − 48 − 72)/504 = **7** ✔。

### 3.3 全窓の n_m(**二系統一致**: scalar 指標和 と 直接列挙)

| 窓 | Ĝ | v̂_m = w^u の類 | **n_m(指標和)** | **n_m(直接列挙)** | \|C_Ĝ(v̂_m)\| | rigid? |
|---|---|---|---:|---:|---:|:--:|
| PSL(2,7) A k=7 | PSL(2,7) | 7A/7B | **7** | **7** | 7 | ✔ |
| PSL(2,7) B k=4 | PGL(2,7) | 8A/8B | **8** | **8** | 8 | ✔ |
| PSL(2,8) A k=7 | PSL(2,8) | 7A/7B/7C | **7** | **7** | 7 | ✔ |
| PSL(2,8) A k=9 | PSL(2,8) | 9A/9B/9C | **9** | **9** | 9 | ✔ |
| PSL(2,11) A k=11 | PSL(2,11) | 11A/11B | **11** | **11** | 11 | ✔ |
| PSL(2,11) B k=5 | PGL(2,11) | 10A/10B | **10** | **10** | 10 | ✔ |
| PSL(2,11) B k=6 | PGL(2,11) | 12A/12B | **12** | **12** | 12 | ✔ |

**適用可能性(c ∈ N の確認)**: 全窓で **Δ̄² = 1**(定理 M2 の構成で Δ̄ の両成分が対合)ゆえ **c = Δ² ↦ 1、すなわち c ∈ N** ✔。したがって定理 T2・系 T2-B・委嘱 05 補題 2(v_m = σ̄₁^u)がそのまま使え、A2 段で問題になった「c ∉ M の罠(語レベル評価必須)」は**本委嘱の全窓で発生しない**(商内評価が正当)。

### 3.4 構造的な読み(rigidity)

> **命題 R(繊維の torsor 性・起案).** 各 charming m について m-繊維 𝔉_m は **C_Ĝ(v̂_m) の θ-捻れ共役作用 f ↦ θ(h)fh⁻¹ に関する自由推移的軌道**であり、
> $$ n_m \;=\; \bigl|C_{\hat G}(\hat v_m)\bigr| \;=\; e. $$

**根拠**: (i) 委嘱 05 補題 4 の作用は h ∈ Ĝ に拡張できる — case B で h が外部でも f^{(h)} = θ(h)fh⁻¹ は(外部)(内部)(外部) = 内部で **f ∈ G を保つ**(私の追加観察)。(ii) v̂_m は正則半単純でその中心化群は位数 e の極大トーラス、G/Ĝ の部分群の位数と互いに素な条件が満たされ作用は自由。(iii) 個数が一致するので推移的。
**状態札**: (i)(ii) は紙上、推移性は**計数からの帰結**(n_m = \|C\| を先に計算している)。**独立の推移性証明は書けていない**【GAP-06c】。
**文献位置(配達 04)**: これは逆ガロア理論の **rigidity(剛性三つ組)**そのもの。実際 (2A, 3A, 7A) in PSL(2,7)・(2A,3A,11A) in PSL(2,11) は古典的な rigid triple で、**私たちの n_m = \|C(v)\| は「その三つ組が rigid」という既知事実の再発見**である。⇒ **狩場設計への含意**: 非一様繊維(n_m が m で変わる)を探すなら **rigid でない三つ組の窓**を狙えばよい(例外軌道の分類は 2508.21671 にあると配達 04 が報告)。

---

## 4. 任務 3 の核心 — 命題 S の成否予測

**命題 S(委嘱 05 §3.5 の起案)**: 単純群の窓で \|GT(N)\| = φ(k)·k、GT(N) ≅ Hol(ℤ/k) = AGL(1,k)。

### 4.1 正しい一般式(私の予測)

> **命題 S′(改訂・起案).** 定理 M2/M3 の窓について
> $$ \boxed{\ |\mathrm{GT}(N)| \;=\; \psi(k)\cdot e \;=\; |\mathcal X_N|\cdot\bigl|C_{\hat G}(\hat v_m)\bigr|\ },\qquad
> \psi(k) := \#\{m\in\mathbb Z/k : \gcd(2m+1,k)=1\} = 2^{a}\varphi(k_{\mathrm{odd}}) $$
> (k = 2^a·k_odd)。**case A では e = k かつ k 奇 ⇒ ψ(k) = φ(k) ⇒ 命題 S に一致**。**case B では e = 2k ⇒ 命題 S は破れる**。

### 4.2 窓ごとの成否

| 窓 | \|𝒳\| = ψ(k) | e | **\|GT\| 予測** | φ(k)·k | **命題 S** | isolated 予測 |
|---|---:|---:|---:|---:|:--:|:--:|
| PSL(2,7) A k=7 | 6 | 7 | **42** | 42 | **○ 成立** | **true**(42/42 settled) |
| PSL(2,8) A k=7 | 6 | 7 | **42** | 42 | **○ 成立** | **true** |
| PSL(2,8) A k=9(3\|k) | 6 | 9 | **54** | 54 | **○ 成立** | **true** |
| PSL(2,11) A k=11 | 10 | 11 | **110** | 110 | **○ 成立** | **true** |
| PSL(2,7) B k=4 | 4 | 8 | **32** | 8 | **✕ 破れ(×4)** | **false**(16/32) |
| PSL(2,11) B k=5 | 4 | 10 | **40** | 20 | **✕ 破れ(×2)** | **false**(20/40) |
| PSL(2,11) B k=6(3\|k) | 4 | 12 | **48** | 12 | **✕ 破れ(×4)** | **false**(24/48) |
| (既知) A₅ k=5 | 4 | 5 | 20 | 20 | ○ | true(委嘱 05) |

> ★ **命題 S の正しい射程**: 「単純群の窓」ではなく「**split-inner 窓(= (2,3,k)-生成・k 奇)**」。この射程内では **4/4 の新窓で的中**(A₅ を入れて 5/5)。射程外(outer 窓)では**破れる**。
> ★ **3 \| k は命題 S の成否に無関係**(PSL(2,8) k=9 は 3\|k でも成立、PSL(2,11) B k=6 は 3\|k で破れるが破れの理由は outer 性)。**Q7 正面(3∤k)の条件は命題 S とは独立の軸**である。

### 4.3 群構造の予測(case A)

> **予測 G-S.** case A の 4 窓で **Φ: GT(N) → Aut(G)、[m,f] ↦ β(β(X) = X^u, β(Y) = f⁻¹Y^u f)は全単射で像は N_{Aut(G)}(⟨X⟩)** であり、
> $$ \mathrm{GT}(N)\ \cong\ N_{\mathrm{Aut}(G)}(\langle X\rangle)\ \cong\ \mathrm{Hol}(\mathbb Z/k) = \mathbb Z/k \rtimes (\mathbb Z/k)^\times. $$
> 各窓で \|N_{Aut(G)}(⟨X⟩)\| = k·φ(k)、C_{Aut(G)}(X) = ⟨X⟩(位数 k)、N/C ↠ (ℤ/k)^× 全射、位数 φ(k) の補群が存在することを確認した(§7)。具体的には
> **PSL(2,7) k=7** → Hol(ℤ/7) = AGL(1,7)(= PGL(2,7) の Borel、位数 42)
> **PSL(2,8) k=7** → Hol(ℤ/7)(PΓL(2,8) 内の分裂トーラス正規化群、位数 42)
> **PSL(2,8) k=9** → Hol(ℤ/9)(位数 54)
> **PSL(2,11) k=11** → Hol(ℤ/11) = AGL(1,11)(PGL(2,11) の Borel、位数 110)
> **A₅ k=5** → Hol(ℤ/5) = F₂₀(委嘱 05 と一致)

**状態札(W57 厳守)**: Φ が全単射であることは計算済み。**群同型であることは (3.53) の合成法則の確認を要する**(A₅ では委嘱 05 §3.2(vi) で確認済み、本 4 窓では未確認)⇒【GAP-06a】。isolated が二系統で確定するまでは「位数 \|GT\| の集合と N_{Aut(G)}(⟨X⟩) への全単射」までが言える上限。

### 4.4 case B の新現象(atlas 初の非 isolated 予測)

> **予測 B-S.** case B の 3 窓で **settled になるのは u ≡ ±1 (mod 2k) の m のみ**、すなわち **m ∈ {0, k−1} の 2 つの繊維だけ**。settled 総数 = 2e = \|N_{Aut(G)}(⟨X⟩)\|、非 settled 総数 = (ψ(k)−2)·e。ゆえに **isolated = false**。

| 窓 | settled な m | settled 数 | 非 settled 数 | \|N_{Aut(G)}(⟨X⟩)\| |
|---|---|---:|---:|---:|
| PSL(2,7) B k=4 | m ∈ {0,3}(u = 1,7 ≡ ±1 mod 8) | 16 | 16 | 16 |
| PSL(2,11) B k=5 | m ∈ {0,4}(u = 1,9 ≡ ±1 mod 10) | 20 | 20 | 20 |
| PSL(2,11) B k=6 | m ∈ {0,5}(u = 1,11 ≡ ±1 mod 12) | 24 | 24 | 24 |

**部分的な機構**: k=5 の窓では **N_{Aut(G)}(⟨X⟩) → (ℤ/5)^× の像が {±1} しかない**(\|N\|=20, \|C\|=10)ので u ≢ ±1 mod 5 の m は原理的に settled になれない — これは証明できる。**k=4, k=6 では exp 写像は全射**なので同じ議論は効かず、障害は「X の像」ではなく「(X,Y) 対の像」にある ⇒ 機構は未解明【GAP-06b】。
> ★ **意義**: これが的中すれば **atlas 初の「isolated でない対象」**であり、(i)「GT(N) を群と呼べない対象」の実例、(ii) 逆極限の塔で isolated cofinal 系(Prop 3.14)を取る操作の**必要性の実地例**、(iii) fake 判定の塔相対性(配達 01 §B-1)を論じる新しい足場になる。**外れた場合は私の settled 判定(∃β ∈ Aut(G))の解釈が誤り**であり、それも同じくらい重要な情報である。

---

## 5. 任務 3 — 封印 payload(P67 様式・canonical JSON 案)

**canonicalization**: `gtsh-canon/v1`(manifest §0: UTF-8・キー辞書順・空白なし・整数 10 進)。**私が定義するのは field と値だけ**。nonce(128-bit)生成・SHA-256 の**計算前 commit**・秘匿保管・byte 開封は司令塔(P67 六要件 ③④⑤⑥)。

**element_encoding**(全段共通・要件 ②):
```
"element_encoding":"pgl2q_matrix/v1"   // 2x2 行列 [[a,b],[c,d]] を GF(q) 上で、PGL(2,q)=GL/scalars の元として
"field_encoding_q8":"F_8 = F_2[x]/(x^3+x+1); 元 a0+a1*x+a2*x^2 を整数 a0+2*a1+4*a2 で表す"
```

### 5.1 段 S1 — PSL(2,7) case A(k=7)

```json
{"b3_points":1008,"case":"A_split_inner","charming_set":[0,1,2,4,5,6],"derived_order":168,
 "element_encoding":"pgl2q_matrix/v1","group":"PSL(2,7)","marking":{"S":[[2,1],[1,5]],"T":[[4,0],[2,2]],
 "det_S":2,"det_S_is_square":true,"det_T":1,"trace_triple":[0,-1,1],"w":"T^{-1}S","ord_w":7},
 "n_ord":7,"object_count":1,"pb3_index":168,"q":7,
 "s3_marking":{"convention":"delta_first","delta_image":"(1 2)","deltaB_image":"(1 2 3)",
   "simultaneous_conjugate_of_standard":true,"conjugator":"(1 2 3)"},
 "stage":"S1","triangle_marking":{"exact_order_binv_a":14,"k":7},"c_in_N":true,
 "sealed":{"candidate_total":1008,"generation_fail":0,"gt_count":42,"h10_fail":876,"h11_fail":90,
   "isolated":true,"n_m":{"0":7,"1":7,"2":7,"4":7,"5":7,"6":7},"n_m_uniform":7,
   "phi_image":"N_{PGL(2,7)}(<X>) = Hol(Z/7) = AGL(1,7)","phi_bijective":true,
   "prop_S_verdict":"holds","settled_count":42,"shadow_total":42}}
```

### 5.2 段 S2 — PSL(2,7) case B(k=4)

```json
{"b3_points":1008,"case":"B_outer","charming_set":[0,1,2,3],"derived_order":168,
 "element_encoding":"pgl2q_matrix/v1","group":"PSL(2,7)","Q_structure":"PGL(2,7) x_{C2} S3",
 "marking":{"S":[[1,0],[0,6]],"T":[[1,1],[4,5]],"det_S":6,"det_S_is_square":false,"det_T":1,
   "trace_triple":[0,-1,4],"w":"T^{-1}S","ord_w":8},
 "n_ord":4,"object_count":2,"pb3_index":168,"q":7,
 "stage":"S2","triangle_marking":{"exact_order_binv_a":8,"k":4},"c_in_N":true,
 "sealed":{"candidate_total":672,"generation_fail":0,"gt_count":32,"h10_fail":560,"h11_fail":80,
   "isolated":false,"n_m":{"0":8,"1":8,"2":8,"3":8},"n_m_uniform":8,
   "settled_m":[0,3],"settled_count":16,"shadow_total":32,
   "phi_image":"N_{PGL(2,7)}(<X>) (order 16) ; Phi は settled 部分でのみ定義",
   "prop_S_verdict":"fails","prop_S_ratio":4}}
```

### 5.3 段 S3 — PSL(2,8) case A(k=7)

```json
{"b3_points":3024,"case":"A_split_inner","charming_set":[0,1,2,4,5,6],"derived_order":504,
 "element_encoding":"pgl2q_matrix/v1","group":"PSL(2,8)","q":8,
 "marking":{"S":[[1,0],[1,1]],"T":[[4,2],[4,5]],"det_T":1,"trace_triple":[0,1,3],"w":"T^{-1}S","ord_w":7,
   "note":"GF(8) の元は整数符号: x=2, x+1=3, x^2=4, x^2+1=5"},
 "n_ord":7,"object_count":1,"pb3_index":504,
 "stage":"S3","triangle_marking":{"exact_order_binv_a":14,"k":7},"c_in_N":true,
 "sealed":{"candidate_total":3024,"generation_fail":0,"gt_count":42,"h10_fail":2640,"h11_fail":342,
   "isolated":true,"n_m_uniform":7,"phi_image":"N_{PGammaL(2,8)}(<X>) = Hol(Z/7)","phi_bijective":true,
   "prop_S_verdict":"holds","settled_count":42,"shadow_total":42}}
```

### 5.4 段 S4 — PSL(2,8) case A(k=9・**3 \| k**)

```json
{"b3_points":3024,"case":"A_split_inner","charming_set":[0,2,3,5,6,8],"derived_order":504,
 "element_encoding":"pgl2q_matrix/v1","group":"PSL(2,8)","q":8,
 "marking":{"S":[[1,0],[1,1]],"T":[[4,3],[1,5]],"det_T":1,"trace_triple":[0,1,2],"w":"T^{-1}S","ord_w":9},
 "n_ord":9,"object_count":1,"pb3_index":504,
 "stage":"S4","triangle_marking":{"exact_order_binv_a":18,"k":9},"c_in_N":true,"three_divides_k":true,
 "sealed":{"candidate_total":3024,"generation_fail":0,"gt_count":54,"h10_fail":2640,"h11_fail":330,
   "isolated":true,"n_m_uniform":9,"phi_image":"N_{PGammaL(2,8)}(<X>) = Hol(Z/9)","phi_bijective":true,
   "prop_S_verdict":"holds","settled_count":54,"shadow_total":54}}
```

### 5.5 段 S5 — PSL(2,11) case A(k=11)

```json
{"b3_points":3960,"case":"A_split_inner","charming_set":[0,1,2,3,4,6,7,8,9,10],"derived_order":660,
 "element_encoding":"pgl2q_matrix/v1","group":"PSL(2,11)","q":11,
 "marking":{"S":[[1,1],[1,10]],"T":[[9,1],[8,1]],"det_S":9,"det_S_is_square":true,"det_T":1,
   "trace_triple":[0,-1,5],"w":"T^{-1}S","ord_w":11},
 "n_ord":11,"object_count":1,"pb3_index":660,
 "stage":"S5","triangle_marking":{"exact_order_binv_a":22,"k":11},"c_in_N":true,
 "sealed":{"candidate_total":6600,"generation_fail":0,"gt_count":110,"h10_fail":6040,"h11_fail":450,
   "isolated":true,"n_m_uniform":11,"phi_image":"N_{PGL(2,11)}(<X>) = Hol(Z/11) = AGL(1,11)",
   "phi_bijective":true,"prop_S_verdict":"holds","settled_count":110,"shadow_total":110}}
```

### 5.6 段 S6 — PSL(2,11) case B(k=5)

```json
{"b3_points":3960,"case":"B_outer","charming_set":[0,1,3,4],"derived_order":660,
 "element_encoding":"pgl2q_matrix/v1","group":"PSL(2,11)","Q_structure":"PGL(2,11) x_{C2} S3","q":11,
 "marking":{"S":[[1,0],[0,10]],"T":[[3,1],[9,7]],"det_S":10,"det_S_is_square":false,"det_T":1,
   "trace_triple":[0,-1,4],"w":"T^{-1}S","ord_w":10},
 "n_ord":5,"object_count":2,"pb3_index":660,
 "stage":"S6","triangle_marking":{"exact_order_binv_a":10,"k":5},"c_in_N":true,
 "sealed":{"candidate_total":2640,"generation_fail":0,"gt_count":40,"h10_fail":2376,"h11_fail":224,
   "isolated":false,"n_m_uniform":10,"settled_m":[0,4],"settled_count":20,"shadow_total":40,
   "prop_S_verdict":"fails","prop_S_ratio":2}}
```

### 5.7 段 S7 — PSL(2,11) case B(k=6・**3 \| k**)

```json
{"b3_points":3960,"case":"B_outer","charming_set":[0,2,3,5],"derived_order":660,
 "element_encoding":"pgl2q_matrix/v1","group":"PSL(2,11)","Q_structure":"PGL(2,11) x_{C2} S3","q":11,
 "marking":{"S":[[1,0],[0,10]],"T":[[4,1],[1,6]],"det_S":10,"det_S_is_square":false,"det_T":1,
   "trace_triple":[0,-1,2],"w":"T^{-1}S","ord_w":12},
 "n_ord":6,"object_count":2,"pb3_index":660,
 "stage":"S7","triangle_marking":{"exact_order_binv_a":12,"k":6},"c_in_N":true,"three_divides_k":true,
 "sealed":{"candidate_total":2640,"generation_fail":0,"gt_count":48,"h10_fail":2376,"h11_fail":216,
   "isolated":false,"n_m_uniform":12,"settled_m":[0,5],"settled_count":24,"shadow_total":48,
   "prop_S_verdict":"fails","prop_S_ratio":4}}
```

### 5.8 宇宙数値のまとめ(spec 射影に渡してよい部分)

| 段 | 対象 | \|PB₃:N\| | **B₃ 点数 = 6\|G\|** | k | \|𝒳\| | candidate_total | 対象数 |
|---|---|---:|---:|---:|---:|---:|---:|
| S1 | PSL(2,7) A | 168 | **1008** | 7 | 6 | 1008 | 1 |
| S2 | PSL(2,7) B | 168 | **1008** | 4 | 4 | 672 | 2 |
| S3 | PSL(2,8) A | 504 | **3024** | 7 | 6 | 3024 | 1 |
| S4 | PSL(2,8) A | 504 | **3024** | 9 | 6 | 3024 | 1 |
| S5 | PSL(2,11) A | 660 | **3960** | 11 | 10 | 6600 | 1 |
| S6 | PSL(2,11) B | 660 | **3960** | 5 | 4 | 2640 | 2 |
| S7 | PSL(2,11) B | 660 | **3960** | 6 | 4 | 2640 | 2 |

**7 段合計 B₃ 点数 = 19944**(既存バッテリー 25200 の 0.79 倍・cap 内で十分実行可能)。
**排他的 staged count の整合**: 全段で `candidate_total = h10_fail + h11_fail + generation_fail + shadow_total` を確認 ✔(F16/W49 の要件)。
**per-m の (H-a) 通過数**(= \|T₂(Ĝ) ∩ 該当剰余類\|): S1: 22 / S2: 28 / S3,S4: 64 / S5: 56 / S6,S7: 66 — これも封印値にしてよい(較正力が高い安価な中間値)。

---

## 6. 【GAP】(隠さず明示)と提案

- **【GAP-06a】** case A 4 窓の **GT(N) ≅ Hol(ℤ/k)** は「Φ が全単射」までしか示していない。**(3.53) の合成法則が Φ と両立すること**は A₅ でしか確認していない。⇒ 実装で合成表を出させれば二系統化できる(P92 と同型の発注)。
- **【GAP-06b】** case B の「settled ⟺ u ≡ ±1 mod 2k」は **k=5 でのみ機構が説明できる**(N_{Aut}(⟨X⟩) → (ℤ/k)^× が非全射)。k=4, k=6 では exp 全射なのに settled が半分 — **機構は未解明**。trace 三つ組(MacBeath)の言葉で「(X^u, Y^u-共役) 三つ組が元の三つ組と Aut-同値か」を書けば見えるはずだが、**書けていない**。
- **【GAP-06c】** 命題 R の推移性は **n_m = \|C\| という計数結果からの逆算**であって、独立証明ではない。rigidity 文献(配達 04・Chen 2011.12940)の枠組で証明できる可能性が高い。⇒ **【文献要請 9】**: 「(2,3,e) 三つ組の rigidity 判定の**明示的十分条件**(trace 三つ組・トーラス正則性からの読み取り)」の原文。
- **【GAP-06d】** 定理 M2 で「像 = S₃」を除外したのは **本委嘱の 3 群で Out ∈ {C₂,C₃} だから**。Out(G) ⊇ S₃ の単純群(例: PSL(2,q) の一般 q、PSL(3,4) 等)では**第三の型 case C が存在し得る**。掃引を広げるときは M2 を拡張する必要がある。
- **【GAP-06e】** 対象数の勘定(case B が 2 対象)は **Aut(Ã) = Ã(PGL(2,q) が complete)**に依拠。q が素数でない場合(PGL(2,8) 等)は成り立たない。
- **【状態】** §3.3 の n_m は **私の中の二系統一致**(自前指標表の scalar 和 ⟷ 直接列挙)。**Sol 便 09 とのブラインド突合も、GAP 実装との突合も未了** ⇒ **cross-checked ではない**。**Lean 未接続 ⇒ verified でもない**。
- **【W28 厳守】** genuine / arithmetical は一切主張しない。Hol(ℤ/k) や rigid triple と逆ガロア理論の関係(配達 04 §5)についても、**形の一致の観察**以上のことは書いていない。
- **【W48 遵守】** Guillot の計算済み表(PSL(2,q) の GT₁)は**参照していない**(比較写像が未確立・対象が別物)。本稿の数値は完全に自前。

**司令塔への提案**
- **P-A(封印の粒度)**: 7 段を**一括封印しない**。命題 S の成否は **S1 単独(PSL(2,7) A・1008 点・最軽量)**で決まる。S1 → S2 の順で開封すれば、「成立側 1 点」と「破れ側 1 点」を最小コストで取れる。
- **P-B(最優先の実装)**: **S2(PSL(2,7) case B・672 候補)** — 非 isolated 予測の初検証。isolated の実装(∃β ∈ Aut(G) 探索)は Aut(G) が 336 元なので総当たりで足りる。
- **P-C(語彙)**: manifest に `case`(A_split_inner / B_outer)と `object_count` を欄として追加すべき。同じ (G,k) に複数の対象 N があり得ることは 2b 以前の段では起きていなかった。

---

## 7. 検算スクリプト(金庫内スクラッチパッド・node・整数/置換演算のみ・第三の独立実装)

| ファイル | 内容 |
|---|---|
| `scratchpad/psl_lib_v1.mjs` | GF(7)/GF(8)/GF(11)、P¹ 上の置換としての PGL(2,q)/PSL(2,q)、閉包・共役類 |
| `scratchpad/psl_markings_v1.mjs` | 任務 1: 全 (s,t) 対の列挙・許容 k の決定・共役軌道数 |
| `scratchpad/psl_nm_v1.mjs` | 任務 2: (H-a)/(H-b′) の定義どおりの直接列挙 + 類積計数 N(v) との突合 |
| `scratchpad/psl_struct_v1.mjs` | Aut(G)-軌道(対象数)・\|C(v)\|・settled/isolated・N_{Aut}(⟨X⟩) |
| `scratchpad/psl_detail_v1.mjs` | 段別 settled 内訳・Hol(ℤ/k) 判定・明示 marking(置換) |
| `scratchpad/psl_charsum_v1.mjs` | **scalar 類積(Frobenius 指標和)公式**による n_m・指標表の直交性自己検証 |
| `scratchpad/psl_matrix_v1.mjs` | marking の行列表示と trace 三つ組の確定 |
| `scratchpad/psl_final_v1.mjs` | **end-to-end**: §5 の行列だけから全封印数値を再生成(XYZ=1・ord(σ̄₁)=2k を含む) |

**再現の入口**: `node psl_final_v1.mjs` が §5 の 7 段すべての `candidate_total / h10_fail / h11_fail / generation_fail / gt_count / settled_count / isolated / ord(σ̄₁)` を出力する。`node psl_charsum_v1.mjs` が指標和による n_m を独立に出す(5 表すべてで直交性 OK)。

**開発中に自分で見つけて直したバグ(記録)**: `psl_charsum_v1.mjs` の初版で S_n(χ) の判定を「類の元の位数が n で**割り切れる**」と書いていた(正しくは「位数が n を**割る**」)。この誤りは n_m を 21/80/28/… と過大に出したため直接列挙との突合で即検出された。**二系統を走らせていなければ通過していた誤り**であり、規律の実効性の記録として残す。
