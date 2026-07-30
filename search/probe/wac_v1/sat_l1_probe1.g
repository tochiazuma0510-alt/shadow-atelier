#############################################################################
## search/probe/wac_v1/sat_l1_probe1.g
##  SAT-L1 委嘱: m=0 hexagon の (2,3)-分解への還元を機械検証する。
##  主張 A: {H1,H2}  <=>  (f*a)^2=1 かつ (f*b^-1)^3=1     (a=s1s2s1, b=s1s2)
##  主張 B: (eps=0 枝) 上は (f*a1)^2=1 かつ (f*b1^-1)^3=1 と同値(S3 部が消える)
##  主張 C: rho_a(c) := c*(u*c*u^-1)  (u=f0*a) は準同型でない(明示反例)
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
Analyse := function(nn, a1, b1, rr, label)
  local Snn, aE, bE, s1, s2, xb, yb, PN, Stab, CSy, al, cc, f, u, c, d,
        S1, S2, S3, S4, n1, n2, n3, n4, f0, rho, ctr, lst, i, j, ok;
  Snn := SymmetricGroup(nn);
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  s1 := bE^-1*aE; s2 := aE*bE^2;
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  Print("\n===== ", label, "  n=", nn, "  r=", rr, " =====\n");
  Print("  a=s1*s2*s1 ? ", s1*s2*s1 = aE, "   b=s1*s2 ? ", s1*s2 = bE,
        "   a^2=1 ", aE^2=(), "   b^3=1 ", bE^3=(), "\n");
  Print("  sign(a1)=", SignPerm(a1), "  (eps=0 なら +1)\n");
  Stab := Centralizer(Snn, xb);
  CSy  := Centralizer(Snn, yb);
  S1 := []; S2 := []; S3 := []; S4 := [];
  for al in Elements(Stab) do
    for cc in Elements(CSy) do
      f := cc*al;
      if SignPerm(f) = 1 then
        if s1*f^-1*s2*f = f^-1*s1*s2 and f^-1*s2*f*s1 = s2*s1*f then
          Add(S1, f); fi;
        if (f*aE)^2 = () and (f*bE^-1)^3 = () then Add(S2, f); fi;
        if (f*aE)^2 = () and (f*bE)^3 = ()   then Add(S3, f); fi;
        if (f*a1)^2 = () and (f*b1^-1)^3 = () then Add(S4, f); fi;
      fi;
    od;
  od;
  Print("  |{H1&H2}| = ", Length(S1),
        "   |{(fa)^2=(fb^-1)^3=1}| = ", Length(S2),
        "   |{(fa)^2=(fb)^3=1}| = ", Length(S3),
        "   |{a1,b1 版}| = ", Length(S4), "\n");
  Print("  一致 S1=S2 ? ", Set(S1)=Set(S2),
        "    S1=S3 ? ", Set(S1)=Set(S3),
        "    S1=S4 ? ", Set(S1)=Set(S4), "\n");
  ## 生成条件(surjectivity)を課したもの = ker chi~
  lst := Filtered(S1, f -> Group(xb, yb^f) = PN);
  Print("  うち生成条件も満たす(=|ker chi~|) : ", Length(lst), "\n");
  ## ---- 主張 C: rho_a の非準同型性(明示反例) ----
  f0 := lst[1]; u := f0*aE;
  Print("  f0 = ", f0, "   u=f0*a の位数 = ", Order(u), " (2 なら involution)\n");
  rho := c -> c*(u*c*u^-1);
  ctr := 0; c := (); d := ();
  for i in Elements(Centralizer(PN, yb)) do
    for j in Elements(Centralizer(PN, yb)) do
      if rho(i*j) <> rho(i)*rho(j) then
        ctr := ctr+1;
        if ctr = 1 then c := i; d := j; fi;
      fi;
    od;
  od;
  Print("  rho_a が準同型を破る (c,d) の個数 = ", ctr,
        " / ", Size(Centralizer(PN,yb))^2, "\n");
  if ctr > 0 then
    Print("    最小反例 c=", c, " d=", d, "\n",
          "      rho(cd) = ", rho(c*d), "\n      rho(c)rho(d) = ", rho(c)*rho(d), "\n");
  fi;
  ## 平行移動公式の確認: A(c*f0) = rho_a(c)*A(f0)
  ok := true;
  for i in Elements(Centralizer(PN, yb)) do
    if (i*f0*aE)^2 <> rho(i)*(f0*aE)^2 then ok := false; fi;
  od;
  Print("  平行移動公式 (c f0 a)^2 = rho_a(c)*(f0 a)^2 : 全 c で成立? ", ok, "\n");
  return true;
end;;

Analyse(10, ( 1, 2)( 3, 6)( 7,10), ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
        2, "W-E-A10-5x2t0");;
Analyse(15, ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11),
        ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11),
        3, "W-E-A15-5x3t0");;
Print("\nSAT_L1_PROBE1_DONE\n");
QUIT;
