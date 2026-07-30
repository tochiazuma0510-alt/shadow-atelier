#############################################################################
## search/probe/wac_v1/sat_l1_probe11.g
##  P-WALL-2 witness (n=24) の窓としての全点検 + 非可解核の実証。
##  a1,b1 は probe10 の局所探索が返した実物。
##  鎖: 窓 assert -> C_S24(w)=C19 x S5 (非可解) -> 定理 SURV で 2280 個の
##      m=0 shadow を構成 -> hexagon + 全射(=settled)を全数検算
##      ==> ker chi~ は非可解部分群を含む ==> GTSh(N,N) 非可解。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
NC := function(p, n) return n - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p))); end;;
n := 24;;
a1 := ( 1,13)( 2, 9)( 3, 5)( 4,24)( 6, 8)( 7,21)(10,12)(11,20)(14,16)(15,22)(17,19)(18,23);;
b1 := ( 1,12, 9)( 2, 8, 5)( 3, 4,24)( 6, 7,21)(10,11,20)(13,19,16)(14,15,22)(17,18,23);;
Snn := SymmetricGroup(n);; Ann := AlternatingGroup(n);;
Print("=== P-WALL-2 窓 assert (n=24) ===\n");
Print("a1 = ", a1, "\nb1 = ", b1, "\n");
Print("  a1^2=1 ", a1^2=(), "  b1^3=1 ", b1^3=(),
      "  k=", NrMovedPoints(a1)/2, "  j=", NrMovedPoints(b1)/3,
      "  sign(a1)=", SignPerm(a1), "  (eps=0)\n");
w := b1^-1*a1;; v := a1*b1^-1;;
Print("  w=b1^-1*a1 型 ", CycleStructurePerm(w), " ord ", Order(w), "\n");
Print("  xbar = w^2 型 ", CycleStructurePerm(w^2), " ord ", Order(w^2),
      "   (ell=19, r=1, t=5 のはず)\n");
Print("  <a1,b1> = A_24 ? ", Group(a1,b1)=Ann, "\n");
Print("  Ree: c(a1)+c(b1)+c(w) = ", NC(a1,n),"+",NC(b1,n),"+",NC(w,n)," = ",
      NC(a1,n)+NC(b1,n)+NC(w,n), "   n+2 = ", n+2,
      "   genus = ", ((3*n-(NC(a1,n)+NC(b1,n)+NC(w,n)))-2*n+2)/2, "\n");
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);;
Print("  braid ? ", s1*s2*s1=s2*s1*s2, "   c=(s1s2)^3=1 ? ", cc=(), "\n");
Print("  P = <xbar,ybar> = A_24 ? ", PN = Ann, "\n");
Nord := Lcm(Order(xb), Order(yb), Order(cc));;
Print("  ord(x)=",Order(xb)," ord(y)=",Order(yb),"  N_ord = ", Nord,
      "   charming c_m = ", Length(Filtered([0..Nord-1], z->GcdInt(2*z+1,Nord)=1)), "\n");
Print("  |E| = 6|A_24| ? ", Size(Group(aE,bE)) = 6*Size(Ann), "\n");
Cw := Centralizer(Snn, w);; Cv := Centralizer(Snn, v);;
Print("\n=== 中心化群(壁の心臓)===\n");
Print("  |C_S24(w)| = ", Size(Cw), "   構造 ", StructureDescription(Cw),
      "   可解? ", IsSolvable(Cw), "\n");
Print("  Stab(xbar) = C_S24(xbar) 位数 ", Size(Centralizer(Snn,xb)),
      "   可解? ", IsSolvable(Centralizer(Snn,xb)), "\n");
Print("\n=== 定理 SURV による m=0 shadow の構成と全数検算 ===\n");
cnt := 0;; bad := 0;; badgen := 0;; alphas := [];;
for z in Elements(Cv) do
  f := (a1^z)*a1;
  if SignPerm(f) <> 1 then bad := bad + 1; continue; fi;
  if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then
    bad := bad + 1; continue; fi;
  if Group(xb, yb^f) <> PN then badgen := badgen + 1; continue; fi;
  cnt := cnt + 1;
  Add(alphas, a1*z*a1);
od;
Print("  |C_S24(v)| = ", Size(Cv), "\n");
Print("  hexagon(原形 (3.3)(3.4), m=0)+ sign を通った f_z の個数 = ", cnt+badgen, "\n");
Print("  さらに全射(<xbar, ybar^f> = P)も通った個数 = ", cnt,
      "   (落ちた: hexagon ", bad, " / 生成 ", badgen, ")\n");
XiIm := Group(alphas);;
Print("  Xi 像 <alpha_z> の位数 = ", Size(XiIm),
      "   = |C_S24(w)| ? ", Size(XiIm) = Size(Cw),
      "\n     構造 ", StructureDescription(XiIm),
      "   **可解? ", IsSolvable(XiIm), "**\n");
Print("  Xi 像 = C_S24(w) そのもの? ", XiIm = Cw, "\n");
Print("  Xi 像 <= Stab(xbar) ? ", IsSubgroup(Centralizer(Snn,xb), XiIm), "\n");
Print("\n  ==> ker chi~ は位数 ", Size(XiIm),
      " の非可解部分群を含む ==> GTSh(N,N) は非可解(下限のみで従う)\n");
Print("\nSAT_L1_PROBE11_DONE\n");
QUIT;
