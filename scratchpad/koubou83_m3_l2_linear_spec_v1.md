# 仕様書 — 押し出し線形則(83 線 M3/L2-LIFT 独立照合器用)v1

著者: 工房数学者(Opus 5・第二著者)/ 2026-08-23 / 実装者 = implementer。
**著者分離**: 本仕様は `c83_m3_e4_lane_v1.md` を未読で、shadow の作用の定義と P の生成系のみから導出。

## 0. 記号と規約 pin(必須)

G=F₂/N_{F₂}(192)、P=[G,G](64)、P^ab=P/[P,P]、u:=2m+1。
- **W-1**: paper 語 yx⁻¹ は GAP で `x^-1*y`。
- **ad_convention**: paper Ad(x̄)(v)=x̄vx̄⁻¹。GAP の `v^x` = x⁻¹vx = Ad(x̄⁻¹)(v) ⟹ **paper Ad は `v^(x^-1)`**。
- 座標 (a,b) ≡ a·v₁+b·v₂、ℤ/4={0,1,2,3}、行列は列ベクトルに左から作用、**列 = v₁,v₂ の像**。

## 1. 正準基底(GAP の任意生成元に依存させない)

v₁ := [ȳx̄⁻¹] ∈ P^ab、 v₂ := A v₁、 A := Ad(x̄)|_{P^ab}。

**補題 B1**(証明つき): C₃=G/P は x̄,ȳ の共通像で生成され、Ad は G/P 経由 ⟹ Ad(ȳ)=Ad(x̄)=A。A は位数 3 で P/Φ(P) 上自由(既測)⟹ P^ab は自明部分をもたない ℤ/4[C₃]-加群 ⟹ I+A+A²=0、ゆえに {v₁,v₂} は ℤ/4-基底で

**A = [[0,−1],[1,−1]]**(基底の定義から自動。GAP で A を求める必要はない)

Schreier 生成元との対応(検算用): b₀=yx⁻¹→v₁、b₁=xyx⁻²→v₂、b₂=x²y→A²v₁+[x³]。

## 2. 閉じた式(本体)

**定理 PUSH**(charming shadow f̄∈P に限る)。e:=u mod 3 ∈{1,2}、Σ₁:=I、Σ₂:=I+A(=−A⁻¹)とする。[f]∈P^ab の座標を (a,b) とすると

**θ̄_{m,f}(v₁) = (A^e − I)[f] + Σ_e v₁、 θ̄_{m,f}(v₂) = A^e θ̄_{m,f}(v₁)。**

(α,β) := 座標 of θ̄(v₁) とすると

e=1: θ̄ = [[α,−β],[β,α−β]]、 e=2: θ̄ = [[α,β−α],[β,−α]]。

**導出**(3 行): T(v₁)=T(ȳ)T(x̄)⁻¹=F⁻¹(ȳ^u F ȳ^{−u})(ȳ^u x̄^{−u})、3 因子とも P の元。P^ab で第 1・2 項が (A^u−I)[f]。w_k:=ȳ^k x̄^{−k} は [w_k]=A[w_{k−1}]+v₁ を満たすので [w_u]=Σ_u v₁、I+A+A²=0 より Σ は u mod 3 のみに依存(3∤u は charming の単元条件から)。半線型性 θ̄·Ad(g)=Ad(g^u)·θ̄ が第 2 式。∎

**⚠ 依頼文の一点訂正**: f̄∈P なので **Ad(f̄) は P^ab 上恒等**(内部自己同型は可換化に自明作用)。**しかし [f]∈P^ab 自体は消えず、(A^e−I)[f] として線型に効く。** det(A−I)=3、det(A²−I)=3 でともに mod 4 単元 ⟹ **u を固定すれば θ̄ が [f] を完全に決定する**(⑤ の含意)。

**自己検証(実装前に手で通ること)**: [0,1] ⟹ θ̄=I;[0,f₁](f₁=yx⁻¹、[f]=v₁)⟹ θ̄=A;[0,f₂]([f]=(I+A)v₁)⟹ θ̄=A² — 補題 U′(T_{0,f_ν}=Ad(x^ν))と一致。

## 3. 前計算レシピ(GAP・1 回・数百 ms 級)

```gap
G  := Group(x,y);;  P := DerivedSubgroup(G);;  D := DerivedSubgroup(P);;
q  := NaturalHomomorphismByNormalSubgroup(P, D);;  Pab := Image(q);;
# --- GATE 1 (item 1) ---
Assert(0, AbelianInvariants(Pab) = [4,4]);
# --- 正準基底 (W-1 / ad_convention pin) ---
s  := x^-1*y;;                    # paper word  y x^-1
v1 := Image(q, s);;
v2 := Image(q, s^(x^-1));;        # paper Ad(xbar) : v -> x v x^-1  =  GAP v^(x^-1)
Assert(0, Size(Subgroup(Pab,[v1,v2])) = 16 and Order(v1)=4 and Order(v2)=4);
# --- GATE: I+A+A^2 = 0  および Ad(ybar)=Ad(xbar) ---
Assert(0, v1 * v2 * Image(q, s^(x^-2)) = One(Pab));
Assert(0, Image(q, s^(y^-1)) = v2);
# --- 座標関数: (Z/4)^2 の離散対数 (16 通り総当たりでよい) ---
coord := w -> First(Cartesian([0..3],[0..3]), ab -> v1^ab[1]*v2^ab[2] = Image(q,w));
```
A は §1 の定数行列を**そのまま使う**(GAP から取らない — 上の 2 つの Assert が A の正しさの証明)。以後 shadow ごとの計算は `coord(f)` 1 回+2×2 行列演算のみ。**degree-1152 上の GroupHomomorphismByImages は一切不要。**

## 4. 5 項目の行列語訳

| # | 判定 | 行列演算だけの形 |
|---|---|---|
| ① P^ab≅(ℤ/4)² | AbelianInvariants(Pab)=[4,4]+§3 の基底 Assert 3 本 | 前計算 GATE 1 |
| ② cusp-death | [x³],[y³],[z³] ∈ 2P^ab、かつ **[y³]=[x³]**・**[z³]=−2[x³]**(§1 の b₂ 関係と I+A+A²=0 からの導出恒等式) | coord 3 回+ベクトル等式 3 本 |
| ③ θ_t(**−1 か否かが本題**) | **証明済み: θ(x↔y)は P^ab 上 −I**。∵θ(v₁)=[x̄ȳ⁻¹]=[s⁻¹]=−v₁、かつ θAθ⁻¹=Ad(θx̄)=Ad(ȳ)=A ⟹ 線型 ⟹ θ=−I | 実測は**確認**であって決定ではない。**どの θ_t か(x↔y の θ か・複素共役 [11,1] か)を cert に pin すること** — [11,1] の方は [[1,0],[1,−1]](位数 2・det=−1)で −I ではない |
| ④ Weil canary | **det θ̄_{m,f} ≡ u (mod 4) が 48/48**。内訳: det=ε_e·N(α+βA)、N(α+βA)=α²−αβ+β²、ε₁=+1, ε₂=−1 | 破壊対照: u を u+2 に差し替えると 48/48 FAIL になること |
| ⑤ GL₂(ℤ/4) 補助 | **半線型則 θ̄A=A^e θ̄**(定理 PUSH 第 2 式)⟹ 像は**非分裂 Cartan C=(ℤ/4[A])^×(位数 12)の正規化群 N(C)(位数 24)**に含まれる(|GL₂(ℤ/4)|=96)。e=1 ⟺ θ̄∈C、e=2 ⟺ θ̄∈N(C)∖C | 各 shadow で Theta·A = A^e·Theta を assert(48/48)。**これが C3-LIFT の CM 予測(Galois 像 = Cartan 正規化群)の独立確認**になる |

## 5. 独立性・射程の注意(cert に記載)

- 本仕様は **charming shadow 限定**(f̄∈P)。checker は 48/48 で `f in P` を assert すること(破れたら census 側の問題)。
- 依頼文の「Ad(f̄) が消える」は正しいが、**[f] は消えない**(§2 の訂正)。
- **副産物(設計判断に効く)**: (A^e−I) が可逆なので、u 固定なら θ̄ ↔ [f]∈P^ab は**全単射**。⟹ この計器の分解能は |P^ab|=16 で、P/Φ(P) の 4 の **4 倍**。**RES-1 が要求した L₂ 分解能をこれが供給する** — ker(Θ|_{H₀})(位数 2)の生成元が P^ab 水準で分離されるかを、この行列で直接見られる(§7.8 の「残問 1 ビット」に直結)。実装後、**ker χ_vir の 12 元の (α,β) 一覧を出力させることを推奨**。
