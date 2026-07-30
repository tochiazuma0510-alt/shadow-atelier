#############################################################################
## search/probe/wac_v1/pent_t2t3.g
##  (T2)(T3) の fine 水準実装。設計上の要点(紙で先に閉じたこと):
##   * pi: B4 -> B3 (s3|->s1) は全射で pi∘phi_123 = id_{B3}
##     ==> K_pi := pi^{-1}(N_A) ∩ PB4 は B4-正規・有限指数・<= PB4 (NFI 正真)
##         かつ **(K_pi)_{PB3} = N_A**(fine = coarse。fiber は 1 点)。
##   * さらに ker(pi) は S4 の V4 に全射 ==> pi(PB4) = PB3
##     ==> PB4/K_pi ≅ PB3/N_A = P。**pentagon は P の中の式**として書ける。
##   ==> fine hexagon = coarse hexagon(定理 REC)。追加の群構成は不要。
##  本 probe はこの構成で pentagon を (A.18) から直に組み、
##   (a) 語の取り替えに対する不変性(= 判定が類のみに依存するか)を自己診断し、
##   (b) 20 shadow の per-m 判定と |im(red)| を出す。
##  期待値は判定に使わない(接触遮断)。
##  Single lane (GAP 4.16.0). NOT a ledger claim.
#############################################################################
LoadPackage("io");;
n := 5;;
## --- A5 窓(定義ノート §1.5.4 の A1 marking)---
tt := (1,2,3);;  aa := (1,4,5);;
XX := aa*tt^-1;; YY := tt*XX*tt^-1;; ss := tt*XX^3;;
b1 := tt;;  a1 := ss;;
Print("a1 = ", a1, "  a1^2=1 ", a1^2=(), "\n");
Print("b1 = ", b1, "  b1^3=1 ", b1^3=(), "\n");
Print("<a1,b1> = A5 ? ", Group(a1,b1) = AlternatingGroup(5), "\n");
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);;
Print("braid ", s1*s2*s1=s2*s1*s2, "  c=1 ", cc=(), "  |P| = ", Size(PN),
      "  = A5 ? ", PN = AlternatingGroup(5), "\n");
Nord := Lcm(Order(xb), Order(yb), Order(cc));;
charm := Filtered([0..Nord-1], z -> GcdInt(2*z+1,Nord)=1);;
Print("N_ord = ", Nord, "  charming m = ", charm, "\n");

## --- GT(N_A): hexagon(原形 m 付き)+ 生成 ---
Hex := function(m, f)
  local u;
  u := 2*m+1;
  return s1^u*f^-1*s2^u*f = f^-1*s1*s2*xb^(-m)*cc^m and
         f^-1*s2^u*f*s1^u = s2*s1*yb^(-m)*cc^m*f;
end;;
shad := [];;
for m in charm do
  for f in Elements(PN) do
    if Hex(m,f) and Group(xb, yb^f) = PN then Add(shad, [m,f]); fi;
  od;
od;
Print("|GT(N_A)| = ", Length(shad), "   相異なる f = ",
      Length(Set(List(shad, z -> z[2]))), "\n");

## --- 余面(A.18)を pi で押した像。x13 は 2 通りの向きを両方作る ---
x13a := s2*xb*s2^-1;;   x13b := s2^-1*xb*s2;;
x24a := s1*yb*s1^-1;;   x24b := s1^-1*yb*s1;;
x14a := s1*x13a*s1^-1;; x14b := s1^-1*x13b*s1;;
## 余面 = (x12 の像, x23 の像) の対。x34 は pi で x12 = xb へ。
CofSet := function(x13, x24, x14, rev)
  local mul;
  mul := function(u,v) if rev then return v*u; else return u*v; fi; end;
  return [ [xb, yb],                      ## phi_123
           [yb, xb],                      ## phi_234  (x12->x23, x23->x34->x12)
           [mul(x13,yb), xb],             ## phi_12,3,4
           [mul(xb,x13), mul(x24,xb)],    ## phi_1,23,4
           [xb, mul(yb,x24)] ];           ## phi_1,2,34
end;;

epi := EpimorphismFromFreeGroup(PN : names := ["X","Y"]);;
F := Source(epi);;
WordOf := function(g) return PreImagesRepresentative(epi, g); end;;

Pent := function(cof, w, rev)
  local v, L, R;
  v := List(cof, p -> MappedWord(w, GeneratorsOfGroup(F), p));
  if rev then
    L := v[1]*v[4]*v[2];   ## paper phi234 phi1,23,4 phi123 -> GAP 反転
    R := v[3]*v[5];        ## paper phi1,2,34 phi12,3,4    -> GAP 反転
  else
    L := v[2]*v[4]*v[1];
    R := v[5]*v[3];
  fi;
  return L = R;
end;;

## --- 自己診断: 語の取り替えで判定が変わらないか ---
Diag := function(cof, rev, label)
  local g, w1, w2, bad, i, live, cnt;
  bad := 0; live := [];
  for g in Elements(PN) do
    w1 := WordOf(g);
    w2 := w1 * GeneratorsOfGroup(F)[1]^5;   ## 別語(x^5=1 in P)
    if Pent(cof, w1, rev) <> Pent(cof, w2, rev) then bad := bad + 1; fi;
    if Pent(cof, w1, rev) then Add(live, g); fi;
  od;
  Print("  [", label, "]  語不変性の破れ = ", bad, " / 60    live = ",
        Length(live), " / 60\n");
  return live;
end;;

Print("\n=== 4 通りの規約での census と自己診断 ===\n");
res := rec();;
L1 := Diag(CofSet(x13a,x24a,x14a,false), false, "x13a,rev=F");;
L2 := Diag(CofSet(x13a,x24a,x14a,true),  true,  "x13a,rev=T");;
L3 := Diag(CofSet(x13b,x24b,x14b,false), false, "x13b,rev=F");;
L4 := Diag(CofSet(x13b,x24b,x14b,true),  true,  "x13b,rev=T");;

## --- 20 shadow の per-m 判定(語不変な規約でのみ意味をもつ)---
Report := function(live, label)
  local m, cnt, tot, fs;
  Print("  [", label, "] per-m: ");
  tot := 0;
  for m in charm do
    cnt := Length(Filtered(shad, z -> z[1]=m and z[2] in live));
    Print("m=", m, ":", cnt, " ");
    tot := tot + cnt;
  od;
  fs := Filtered(Set(List(shad, z->z[2])), g -> g in live);
  Print("  計 ", tot, "/", Length(shad), "   f-成分 ", Length(fs), "/",
        Length(Set(List(shad, z->z[2]))), "\n");
  return tot;
end;;
Print("\n=== 20 shadow の持ち上げ可否 ===\n");
Report(L1,"x13a,rev=F");; Report(L2,"x13a,rev=T");;
Report(L3,"x13b,rev=F");; Report(L4,"x13b,rev=T");;
Print("\nPENT_T2T3_DONE\n");
QUIT;
