#############################################################################
# search/week4-k5-bridge-d1.g — K^(5) 橋 D1 の **第二系統**(GAP)
#
# ツール仕様ヘッダ
#  入力  : なし。D1 正典 (3.1)(3.6)(4.9)(4.12) だけを読んで、GAP の fp 群 →
#          IsomorphismPermGroup → DirectProduct で D_5^3 を組み、G_5 = <X,Y> を作る。
#          **node 側(search/week4-k5-bridge-d1.mjs)とヘルパーを一切共有しない**
#          (node は D_5 を整数 2a+e で自前符号化・GAP は fp 群と置換表現)。
#  モード: 群論のみ。u・Kummer 類・体には一切触れない(封印規律)。
#  出力  : 標準出力に [PASS]/[FAIL] 行と末尾の n/N。
#  検査する不変量: node 側 A/B/C/D/E/F/G 群の **load-bearing 項目**(便 29 ⑧)。
#  規約の差(既知罠): GAP の共役は H^g = g^-1 H g、coset 作用は右剰余類。
#          node は gHg^-1・左剰余類。⇒ tau の向きが互いに逆になるが、
#          <tau> と <tau^2> は同一、cycle type も同一なので判定は不変。
#############################################################################

k5PASSN := 0;; k5FAILN := 0;;
k5CK := function(k5name, k5ok, k5extra)
  if k5ok then k5PASSN := k5PASSN + 1; Print("[PASS] ", k5name);
  else k5FAILN := k5FAILN + 1; Print("[FAIL] ", k5name); fi;
  if k5extra <> "" then Print("  ", k5extra); fi;
  Print("\n");
end;;

# ---------------------------------------------------------------- D_5 と D_5^3
k5F := FreeGroup("r","s");;
k5D5f := k5F / [ k5F.1^5, k5F.2^2, k5F.2*k5F.1*k5F.2^-1*k5F.1 ];;   # D1 §3: k5r^n, k5s^2, srs^{-1}k5r
k5iso := IsomorphismPermGroup(k5D5f);;
k5D := Image(k5iso);;
k5r := Image(k5iso, k5D5f.1);;  k5s := Image(k5iso, k5D5f.2);;
k5CK("A0  D_5 は位数 10・s r s^-1 = r^-1", Size(k5D) = 10 and k5s*k5r*k5s^-1 = k5r^-1, "");

k5DP := DirectProduct(k5D,k5D,k5D);;
k5emb := List([1..3], k5i -> Embedding(k5DP, k5i));;
k5tri := function(a,b,k5c) return Image(k5emb[1],a)*Image(k5emb[2],b)*Image(k5emb[3],k5c); end;;

k5X := k5tri(k5r, k5s, k5s);;                    # (3.6) xbar
k5Y := k5tri(k5r*k5s, k5r, k5r*k5s);;                # (3.6) ybar
k5Z := k5tri(k5r^2*k5s, k5r^-1*k5s, k5r);;           # (3.6) zbar
k5G := Group(k5X, k5Y);;

k5CK("A1  xbar*ybar*zbar = 1", k5X*k5Y*k5Z = One(k5G), "");
k5CK("A2  ord = (10,10,10) = lcm(5,2)", Order(k5X)=10 and Order(k5Y)=10 and Order(k5Z)=10, "");
k5CK("A3  |G_5| = 500 = 4*5^3", Size(k5G) = 500, Concatenation("|G| = ", String(Size(k5G))));
k5Dg := DerivedSubgroup(k5G);;
k5CK("A5b [G_5,G_5] = C_5^3, |.| = 125", Size(k5Dg) = 125 and IsElementaryAbelian(k5Dg), "");
k5CK("A5c G_5/[G_5,G_5] ~= C_2 x C_2", Size(k5G)/Size(k5Dg) = 4 and IsElementaryAbelian(k5G/k5Dg), "");
k5CK("A6  Z(G_5) = 1", Size(Centre(k5G)) = 1, "");
k5e1 := k5X^2;; k5e2 := k5Y^2;; k5e3 := k5Z^2;;
k5CK("A7b 符号表 (1.4): h_i(e_j) = + (i=j) / - (i<>j)",
   k5e1^k5X = k5e1 and k5e2^k5X = k5e2^-1 and k5e3^k5X = k5e3^-1 and
   k5e1^k5Y = k5e1^-1 and k5e2^k5Y = k5e2 and k5e3^k5Y = k5e3^-1 and
   k5e1^k5Z = k5e1^-1 and k5e2^k5Z = k5e2^-1 and k5e3^k5Z = k5e3, "");
k5CK("A10  B4: C_{G_5}(X) = <X> ~= C_10 (巡回)",
   Size(Centralizer(k5G,k5X)) = 10 and Centralizer(k5G,k5X) = Group(k5X), "");
k5CK("A10c 教材: C_{G_5}(X^2) は位数 250 で非巡回 — B4 に代入禁止",
   Size(Centralizer(k5G, k5X^2)) = 250 and not IsCyclic(Centralizer(k5G, k5X^2)), "");

# ---------------------------------------------------------------- Aut と B1
k5A := AutomorphismGroup(k5G);;
k5CK("G2  |Aut(G_5)| = 48000 = 125 * 4^3 * 6  ⇒ marked triple 上で自由推移(B1)",
   Size(k5A) = 48000, Concatenation("|Aut| = ", String(Size(k5A))));

# ---------------------------------------------------------------- GT(K^(5)) と Phi
k5kap := function(k5m) if k5m mod 2 = 1 then return k5m+1; else return -k5m; fi; end;;
k5Xcal := Filtered([0..9], k5m -> GcdInt(2*k5m+1, 10) = 1);;
k5CK("B1  X_5 = {0,1,3,4,5,6,8,9} (|X_5| = 8)", k5Xcal = [0,1,3,4,5,6,8,9], "");
k5CK("B2  chi~: m -> 2m+1 は X_5 -> (Z/20)^x の全単射",
   Set(List(k5Xcal, k5m -> (2*k5m+1) mod 20)) = Set(Filtered([1..19], a -> GcdInt(a,20)=1)), "");
k5shad := [];;
for k5m in k5Xcal do for k5k in [0..4] do
  Add(k5shad, rec(k5m := k5m, k5k := k5k, u := 2*k5m+1,
                f := k5tri(k5r^(2*k5k), k5r^(-2*k5k), k5r^(k5kap(k5m)))));
od; od;
k5CK("B3  |GT(K^(5))| = 8 * 5 = 40  (Thm 4.3 (4.12), 4∤5)", Length(k5shad) = 40, "");
k5F0 := Filtered(k5shad, k5t -> k5t.u mod 20 = 1);;
k5CK("B5  F_0 = ker chi~ = {m=0} x {k mod 5}, e = |F_0| = 5", Length(k5F0) = 5 and ForAll(k5F0, k5t -> k5t.k5m = 0), "");
k5CK("B7  gcd(e, M/e) = gcd(5,2) = 1  (coprime regime)", GcdInt(5,2) = 1, "");

k5phis := [];;
for k5t in k5shad do
  k5t.aut := GroupHomomorphismByImages(k5G, k5G, [k5X, k5Y], [k5X^(k5t.u), k5t.f^-1 * k5Y^(k5t.u) * k5t.f]);
  Add(k5phis, k5t.aut);
od;
k5CK("C1  40 個の Phi_{m,k} はすべて G_5 の自己同型",
   ForAll(k5shad, k5t -> k5t.aut <> fail and IsBijective(k5t.aut)), "");
k5CK("C2  [別ゲート] Phi は単射(40 個が相異)", Length(Set(k5phis)) = 40, "");
k5CK("C5  Phi_{0,k}(X) = X", ForAll(k5F0, k5t -> Image(k5t.aut, k5X) = k5X), "");
k5CK("C6  ★★Phi_{0,k} = inn(X^{-2k})  (F_0 の像は <X^2> による内部自己同型)",
   ForAll(k5F0, k5t -> ForAll(GeneratorsOfGroup(k5G),
       k5g -> Image(k5t.aut, k5g) = (k5X^(-2*k5t.k5k))^-1 * k5g * (k5X^(-2*k5t.k5k)) or
            Image(k5t.aut, k5g) = (k5X^(-2*k5t.k5k)) * k5g * (k5X^(-2*k5t.k5k))^-1 )), "");
# GAP の共役規約に依らない形で厳密に(左右どちらの inn かは規約差なので両方許す)
k5CK("C6b k -> X^{-2k} は Z/5 -> <X^2> の同型(5 個相異)",
   Length(Set(List(k5F0, k5t -> k5X^(-2*k5t.k5k)))) = 5, "");

# ---------------------------------------------------------------- 部分群と Lambda
k5ccs := ConjugacyClassesSubgroups(k5G);;
k5idx10 := Filtered(k5ccs, k5c -> Index(k5G, Representative(k5c)) = 10);;
k5tot50 := Sum(k5idx10, k5c -> Size(k5c));;
k5CK("D2  位数 50 の部分群の総数(GAP 独立列挙)", k5tot50 > 0, Concatenation("|{H : |H|=50}| = ", String(k5tot50)));

k5qual := [];; k5good := [];; k5bad := [];;
for k5c in k5idx10 do
  k5H := Representative(k5c);
  k5act := FactorCosetAction(k5G, k5H);
  k5px := Image(k5act, k5X); k5py := Image(k5act, k5Y); k5pz := Image(k5act, k5Z);
  k5tx := Collected(CycleLengths(k5px, [1..10]));
  k5ty := Collected(CycleLengths(k5py, [1..10]));
  k5tz := Collected(CycleLengths(k5pz, [1..10]));
  k5Nh := Normalizer(k5G, k5H);
  k5rec0 := rec(k5H := k5H, cls := k5c, sz := Size(k5c), k5tx := k5tx, k5ty := k5ty, k5tz := k5tz,
              nrm := Size(k5Nh), lam := Index(k5G, k5Nh), k5act := k5act, k5px := k5px, k5py := k5py, k5pz := k5pz);
  if k5tx = [[10,1]] then
    Add(k5qual, k5rec0);
    if Size(k5Nh) = 50 then Add(k5good, k5rec0); else Add(k5bad, k5rec0); fi;
  fi;
od;
k5CK("D3  qualifying(X が 10-サイクル)の H は 50 個",
   Sum(k5qual, o -> o.sz) = 50, Concatenation("got ", String(Sum(k5qual, o -> o.sz))));
k5CK("D4  N_G(H) = H が 40 個 / それ以外が 10 個(|N| = 100, |Lambda| = 5)",
   Sum(k5good, o -> o.sz) = 40 and Sum(k5bad, o -> o.sz) = 10 and
   ForAll(k5bad, o -> o.nrm = 100 and o.lam = 5), "");
k5CK("D5-(3ab) good 側は N_P(H) = H かつ |Lambda| = 10 = M",
   ForAll(k5good, o -> o.nrm = 50 and o.lam = 10), "");
k5tgt := Filtered(k5good, o -> o.k5ty = [[1,2],[2,4]]);;
k5mir := Filtered(k5good, o -> o.k5tz = [[1,2],[2,4]]);;
k5CK("D6  good 40 は ordered passport で 20 + 20 に分裂((10,2^4 1^2,10) と (10,10,2^4 1^2))",
   Sum(k5tgt, o -> o.sz) = 20 and Sum(k5mir, o -> o.sz) = 20, "");
k5CK("D7  ★標的 20 個は G_5-共役類 **2 つ**(各 10)",
   Length(k5tgt) = 2 and ForAll(k5tgt, o -> o.sz = 10), Concatenation("classes = ", String(List(k5tgt, o -> o.sz))));
k5CK("D16b bad 側は |Lambda| = 5 = e だが Stab_{<X>}(H) の位数が 2 ⇒ tau 非単射(scope-out)",
   ForAll(k5bad, o -> o.lam = 5 and
      Size(Intersection(Group(k5X), Normalizer(k5G, o.k5H))) = 2), "");
k5o0 := k5tgt[1];;
k5CK("D12 標的 H の core は位数 5・monodromy 像は位数 100",
   Size(Core(k5G, k5o0.k5H)) = 5 and Size(Image(k5o0.k5act)) = 100, "");
k5CK("D13 B2: Aut(dessin) = N_G(H)/H = 1(標的 次数 10)", k5o0.nrm / 50 = 1, "");
# Riemann-Hurwitz: 2g-2 = -2d + sum (d - #cycles)
k5genus := function(k5d, k5cs) local k5c; k5c := Sum(k5cs); return (-2*k5d + 3*k5d - k5c)/2 + 1; end;;
k5CK("D14 Riemann-Hurwitz: 次数 10・(10, 2^4 1^2, 10) ⇒ 種数 2",
   k5genus(10, [ Length(Cycles(k5o0.k5px,[1..10])), Length(Cycles(k5o0.k5py,[1..10])), Length(Cycles(k5o0.k5pz,[1..10])) ]) = 2, "");
k5CK("D9-(5a) 次数 10 で (10,10,10) は符号により不可能(10-cycle は奇置換)",
   SignPerm(PermList(Concatenation([2..10],[1]))) = -1, "");
k5CK("D9-(5b) 観測 passport は符号整合(奇・偶・奇)",
   SignPerm(k5o0.k5px) = -1 and SignPerm(k5o0.k5py) = 1 and SignPerm(k5o0.k5pz) = -1, "");
# (3c) <k5X> は Lambda 上 regular: 全共役で k5H^k5g cap <k5X> = 1
k5CK("D9-(3c) 全 g で H^g cap <X> = 1(B3・全分岐)",
   ForAll(k5good, o -> ForAll(AsList(ConjugateSubgroups(k5G, o.k5H)),
       k5Hg -> Size(Intersection(k5Hg, Group(k5X))) = 1)), "");

# ---------------------------------------------------------------- (6') の判定
k5Lam := AsList(ConjugateSubgroups(k5G, k5o0.k5H));;
k5CK("E0  |Lambda| = 10", Length(k5Lam) = 10, "");
k5permOnLam := function(f)   # f: k5G の自己同型 or 元による共役 -> Lambda 上の置換
  local k5img, k5i, k5j, k5L;
  k5L := [];
  for k5i in [1..10] do
    k5img := Image(f, k5Lam[k5i]);
    k5j := Position(k5Lam, k5img);
    if k5j = fail then return fail; fi;
    Add(k5L, k5j);
  od;
  return PermList(k5L);
end;;
k5tauP := k5permOnLam(ConjugatorAutomorphism(k5G, k5X));;
k5CK("E1  tau は Lambda 上の 10-サイクル(regular)", k5tauP <> fail and Order(k5tauP) = 10, "");
k5r0 := List(k5F0, k5t -> k5permOnLam(k5t.aut));;
k5CK("E2a (6'-i) Lambda は Phi(F_0)-安定", ForAll(k5r0, k5p -> k5p <> fail), "");
k5CK("E2b (参考)Lambda は Phi(GT) 全 40 元で安定", ForAll(k5shad, k5t -> k5permOnLam(k5t.aut) <> fail), "");
k5CK("E3  (6'-ii) rho_0 は **忠実**(5 個の置換が相異)", Length(Set(k5r0)) = 5, "");
k5CK("E5  ★rho_0(F_0) = tau(mu_10[5]) = <tau^2>  ⇒ 前件 (6') PASS",
   Group(k5r0) = Group(k5tauP^2) and Size(Group(k5r0)) = 5, "");
k5CK("E6  rho_0(F_0) は tau と可換", ForAll(k5r0, k5p -> k5p*k5tauP = k5tauP*k5p), "");
k5CK("E7  非自明元は型 5.5(不動点なし)",
   ForAll(Filtered(k5r0, k5p -> k5p <> ()), k5p -> Collected(CycleLengths(k5p,[1..10])) = [[5,2]]), "");
k5CK("E10 Phi(GT) は 2 つの G_5-共役類を入れ替えない",
   ForAll(k5shad, k5t -> Image(k5t.aut, k5o0.k5H) in k5Lam), "");

# ------------------------------------------------- 便 30 F2.3/P4: 封印値 a = j_ns^{-1} j_sq
# GAP は共役を H^g = g^-1 H g、node は g H g^-1 を使う。**両クラスで同一規約**である限り
# a は不変(node I4 が逆向き規約でも同じ a を出すことを確認済み)。
k5jFor := function(H)
  local L, tau, rho, out, tt, kk;
  L := AsList(ConjugateSubgroups(k5G, H));
  tau := PermList(List([1..10], i -> Position(L, L[i]^k5X)));
  rho := List(k5F0, t -> PermList(List([1..10], i -> Position(L, Image(t.aut, L[i])))));
  out := [];
  for tt in [0..4] do
    kk := First([1..5], j -> rho[j] = tau^(2*tt));
    if kk = fail then return fail; fi;
    Add(out, k5F0[kk].k5k);
  od;
  return out;
end;;
k5j1 := k5jFor(k5tgt[1].k5H);;
k5j2 := k5jFor(k5tgt[2].k5H);;
k5CK("I1  j_i は標的二共役類の両方で定義される(rho_0 の像が tau_i(mu_10[5]) を尽くす)",
   k5j1 <> fail and k5j2 <> fail, "");
k5CK("I2  j_sq = j_ns(K5-1 の帰結 — j_i は i に依らない)", k5j1 = k5j2,
   Concatenation("j_1 = ", String(k5j1), "  j_2 = ", String(k5j2)));
k5aVals := Filtered([1..4], a -> ForAll([0..4], tt -> k5j2[(a*tt) mod 5 + 1] = k5j1[tt+1]));;
k5CK("I3  封印値 a = j_ns^{-1} j_sq in (Z/5)^x", Length(k5aVals) = 1 and k5aVals[1] = 1,
   Concatenation("a = ", String(k5aVals)));

# ---------------------------------------------------------------- 最小 faithful
k5cf := Filtered(k5ccs, k5c -> Size(Core(k5G, Representative(k5c))) = 1);;
k5mindeg := Minimum(List(k5cf, k5c -> Index(k5G, Representative(k5c))));;
k5CK("F4  最小 faithful transitive 次数 = 20", k5mindeg = 20, Concatenation("mindeg = ", String(k5mindeg)));
k5mc := Filtered(k5cf, k5c -> Index(k5G, Representative(k5c)) = 20);;
k5CK("F9  ★最小忠実側の core-free 部分群(位数 25)は G_5-共役類 **4 つ**(各 4 個・計 16)",
   Length(k5mc) = 4 and Sum(k5mc, k5c -> Size(k5c)) = 16,
   Concatenation("classes = ", String(List(k5mc, k5c -> Size(k5c)))));
k5Um := Representative(k5mc[1]);;
k5actm := FactorCosetAction(k5G, k5Um);;
k5CK("F5  最小忠実 dessin の passport = (10^2, 10^2, 10^2)",
   Collected(CycleLengths(Image(k5actm,k5X),[1..20])) = [[10,2]] and
   Collected(CycleLengths(Image(k5actm,k5Y),[1..20])) = [[10,2]] and
   Collected(CycleLengths(Image(k5actm,k5Z),[1..20])) = [[10,2]], "");
k5CK("F6  Riemann-Hurwitz: 次数 20・(10^2,10^2,10^2) ⇒ 種数 8", k5genus(20, [2,2,2]) = 8, "");
k5CK("F7  B2 FAIL: Aut(dessin) = N_G(U)/U ~= C_5",
   Size(Normalizer(k5G, k5Um)) / 25 = 5, "");
k5CK("F8  忠実 ⇒ monodromy = G_5 (位数 500)", Size(Image(k5actm)) = 500, "");

Print("\n=== ", k5PASSN, "/", k5PASSN + k5FAILN, " PASS (GAP second system) ===\n");
if k5FAILN > 0 then ForceQuitGap(1); fi;
QUIT;
