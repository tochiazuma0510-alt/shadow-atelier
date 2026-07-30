#############################################################################
## search/probe/wac_v1/sat_l1_probe13.g
##  判別窓 W-CENT-B (n=18, ell=9, r=2, t=0, p=s=0, w0=(9,9)) の全点検。
##  CENT 予測 |ker chi~| = |C_S18(w0)| = 162  vs  PRUNE 予測 18(9 倍差)。
##  p=s=0 ゆえ C(w0)=C(w0^2)=Stb(xbar) ==> 挟み撃ちが閉じ CENT は定理。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
NC := function(p, n) return n - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p))); end;;
n := 18;;
a1 := ( 1, 2)( 3, 4)( 5, 9)( 6,18)( 7,15)( 8,10)(11,14)(16,17);;
b1 := ( 2, 9, 4)( 5, 8,18)( 6,17,15)( 7,14,10)(11,13,12);;
Snn := SymmetricGroup(n);; Ann := AlternatingGroup(n);;
Print("=== W-CENT-B 窓 assert (n=18) ===\n");
Print("a1 = ", a1, "\nb1 = ", b1, "\n");
Print("  a1^2=1 ", a1^2=(), "  b1^3=1 ", b1^3=(), "  k=", NrMovedPoints(a1)/2,
      "  j=", NrMovedPoints(b1)/3, "  sign(a1)=", SignPerm(a1), " (eps=0)\n");
w := b1^-1*a1;; v := a1*b1^-1;;
Print("  w 型 ", CycleStructurePerm(w), " ord ", Order(w),
      "    xbar=w^2 型 ", CycleStructurePerm(w^2), " ord ", Order(w^2), "\n");
Print("  <a1,b1> = A_18 ? ", Group(a1,b1)=Ann, "\n");
Print("  Ree: ", NC(a1,n),"+",NC(b1,n),"+",NC(w,n)," = ", NC(a1,n)+NC(b1,n)+NC(w,n),
      "   n+2 = ", n+2, "   genus = ",
      ((3*n-(NC(a1,n)+NC(b1,n)+NC(w,n)))-2*n+2)/2, "\n");
aE := a1*(n+1,n+3);; bE := b1*(n+1,n+3,n+2);;
s1 := bE^-1*aE;; s2 := aE*bE^2;; cc := (s1*s2)^3;;
xb := s1^2;; yb := s2^2;; PN := Group(xb,yb);;
Print("  braid ", s1*s2*s1=s2*s1*s2, "   c=1 ", cc=(),
      "   P = A_18 ? ", PN = Ann, "   |E|=6|A_18| ? ",
      Size(Group(aE,bE))=6*Size(Ann), "\n");
Nord := Lcm(Order(xb),Order(yb),Order(cc));;
Print("  N_ord = ", Nord, "   c_m = ",
      Length(Filtered([0..Nord-1], z->GcdInt(2*z+1,Nord)=1)), "\n");
Stb := Centralizer(Snn, xb);; Cw := Centralizer(Snn, w);; Cv := Centralizer(Snn, v);;
Print("\n=== 挟み撃ち ===\n");
Print("  |C_S18(w)| = ", Size(Cw), " ", StructureDescription(Cw), "\n");
Print("  |Stb(xbar)| = |C_S18(w^2)| = ", Size(Stb), " ", StructureDescription(Stb), "\n");
Print("  C(w) = C(w^2) ? ", Cw = Stb, "   ==> CENT は本窓で定理\n");
Print("  PRUNE の予測(参考): O_2'(Stb)=", Size(SylowSubgroup(Stb,3)),
      " 系 ... 実測は下記 Xi 像で決まる\n");
Print("\n=== SURV による構成と全数検算 ===\n");
cnt := 0;; bad := 0;; badgen := 0;; alphas := [];;
for z in Elements(Cv) do
  f := (a1^z)*a1;
  if SignPerm(f) <> 1 then bad := bad+1; continue; fi;
  if not (s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f) then bad := bad+1; continue; fi;
  if Group(xb, yb^f) <> PN then badgen := badgen+1; continue; fi;
  cnt := cnt+1; Add(alphas, a1*z*a1);
od;
Print("  |C_S18(v)| = ", Size(Cv), "   全条件を通った f_z = ", cnt,
      "  (落ち: hexagon ", bad, " / 生成 ", badgen, ")\n");
XiIm := Group(alphas);;
Print("  Xi 像位数 = ", Size(XiIm), "   = Stb ? ", XiIm = Stb,
      "   構造 ", StructureDescription(XiIm), "\n");
Print("  ==> |Xi(ker chi~)| = ", Size(XiIm),
      "   (PRUNE 予測 18 = ", Size(XiIm) = 18, ")\n");
Print("\nSAT_L1_PROBE13_DONE\n");
QUIT;
