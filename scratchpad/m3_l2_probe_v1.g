##############################################################################
## m3_l2_probe_v1.g -- M3 (E[4] lane): layer-2 structure of P and shadow visibility
## Author: shadow-atelier mathematician (Claude / Opus 5), 2026-08-23.
## Purpose: measure the second layer of P = [G,G] (|P| = 64) for windows
##   [1152,154161] / [1152,154163], and locate where each ker(chi_vir) shadow
##   first acts non-trivially.  Feeds the E[4] correspondence (task M3(i)-(iii)).
## Convention: W-1 (paper "AB" = GAP B*A) enforced everywhere via AbstractProd,
##   with a fail-closed positive assert + negative canary (Sol order A4-1).
##############################################################################
Read("search/probe/wac_v1/gap_output_prelude.g");
Read("search/gaplib_common.g");
Read("search/week3-battery-common.g");
Read("search/iso_census83_deep15_data.g");

BF3 := FreeGroup("a","b");;
brelD := BF3.1*BF3.2*BF3.1*BF3.2^-1*BF3.1^-1*BF3.2^-1;;
B3 := BF3 / [brelD];;
ga := B3.1;; gb := B3.2;; a := ga;; b := gb;;

BuildWindowFromWords := function(indexExpected, words)
  local genElts, N, hm, Gimg, isoQ, s1, s2;
  genElts := List(words, w -> EvalString(w));;
  N := Subgroup(B3, genElts);;
  if Index(B3, N) <> indexExpected or not IsNormal(B3, N) then
    Error("window build failed");
  fi;
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  Gimg := Image(hm);;
  isoQ := IsomorphismPermGroup(Gimg);;
  s1 := Image(isoQ, Image(hm, ga));;
  s2 := Image(isoQ, Image(hm, gb));;
  return rec(s1 := s1, s2 := s2);;
end;;

MakeWindow := function(s1, s2)
  local xx, yy, DD, dd, cc, zz;
  xx := s1^2;; yy := s2^2;;
  DD := AbstractProd([s1,s2,s1]);; dd := AbstractProd([s1,s2]);;
  cc := DD^2;; zz := AbstractProd([xx,yy])^-1;;
  return rec(s1 := s1, s2 := s2, x := xx, y := yy, Dlt := DD, dlt := dd, c := cc, z := zz,
             Bq := Group(s1,s2), PN := Group(xx,yy),
             Nord := Lcm(Order(xx),Order(yy),Order(cc)));;
end;;

TT := function(W,g) return AbstractProd([W.dlt, g, W.dlt^-1]); end;;
TH := function(W,g) return AbstractProd([W.Dlt, g, W.Dlt^-1]); end;;
RtOf := function(W,m,f)
  local Wd;
  Wd := AbstractProd([W.y^m, f]);
  return AbstractProd([TT(W,TT(W,Wd)), TT(W,Wd), Wd]);
end;;

CorrectedShadows := function(W, charmingSet)
  local out, f, m, u;
  out := [];;
  for f in Elements(DerivedSubgroup(W.PN)) do
    if AbstractProd([f, TH(W,f)]) <> Identity(W.Bq) then continue; fi;
    for m in charmingSet do
      u := 2*m+1;;
      if RtOf(W,m,f) <> W.c^m then continue; fi;
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN) then continue; fi;
      Add(out,[m,f]);
    od;
  od;
  return Set(out);;
end;;

## ---------- W-1 fail-closed assert (Sol A4-1) on a non-commutative fixture ----------
W1Assert := function(W)
  local f1, fbad, rhs, pos, neg;
  f1   := AbstractProd([W.y, W.x^-1]);      # paper  y x^{-1}
  fbad := AbstractProd([W.x^-1, W.y]);      # paper  x^{-1} y   (v1's raw-GAP mistake)
  rhs  := AbstractProd([W.x, W.s2, W.x^-1]);
  pos  := (AbstractProd([f1^-1, W.s2, f1]) = rhs);
  neg  := (AbstractProd([fbad^-1, W.s2, fbad]) = rhs);
  return rec(positive := pos, canary_fails := not neg,
             f1_is_gap_xinv_y := (f1 = W.x^-1 * W.y),
             fixture_nonabelian := not IsAbelian(W.Bq));;
end;;

## ---------- generic induced action on a quotient P/X ----------
ActOnQuot := function(P, X, actFn)
  local nat, Q, els, tab, ApplyQ, ord, allid, q, cq, i, wd;
  nat := NaturalHomomorphismByNormalSubgroup(P, X);;
  Q := Image(nat);;
  els := Elements(Q);;
  # well-definedness: actFn must preserve X
  wd := ForAll(Elements(X), u -> actFn(u) in X);;
  tab := List(els, q -> [q, Image(nat, actFn(PreImagesRepresentative(nat,q)))]);;
  ApplyQ := function(qq) return First(tab, t -> t[1] = qq)[2]; end;;
  ord := 1;;
  repeat
    allid := true;;
    for q in els do
      cq := q;;
      for i in [1..ord] do cq := ApplyQ(cq); od;;
      if cq <> q then allid := false; break; fi;
    od;;
    if allid then break; fi;
    ord := ord + 1;;
  until ord > 200;
  return rec(well_defined := wd, qsize := Size(Q), inv := AbelianInvariants(Q),
             order := ord, is_id := (ord = 1), apply := ApplyQ, elems := els, nat := nat);;
end;;

## ---------- GT composition law (3.53) ----------
CompShadow := function(W, s1, s2)
  local m1,f1,m2,f2,u1,psi1,m3,f3;
  m1 := s1[1];; f1 := s1[2];; m2 := s2[1];; f2 := s2[2];;
  u1 := 2*m1+1;;
  psi1 := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
            [W.x^u1, AbstractProd([f1^-1, W.y^u1, f1])]);;
  if psi1 = fail then return fail; fi;
  m3 := (2*m1*m2 + m1 + m2) mod W.Nord;;
  f3 := AbstractProd([f1, Image(psi1, f2)]);;
  return [m3, f3];;
end;;

ShadowOrder := function(W, s, idS)
  local cur, k;
  cur := s;; k := 1;;
  while cur <> idS and k < 100 do
    cur := CompShadow(W, cur, s);; k := k+1;;
  od;
  return k;;
end;;

##############################################################################
Report := function(recWords, idExpected, label)
  local bw, W, G, P, PhiP, DP, P2, P4, M4, L3, Cusp, x3,y3,z3, w1,
        charmingSet, corr, kerChi, s, m, f, u, psi, actFn, aPhi, aM4, aAb, aP,
        idS, H0, kerT, t, res, i, adx, sizes, e, natAb, Pab, cuspIm, ordS,
        H0orders, kerTheta, gg, innerMatch;
  bw := BuildWindowFromWords(idExpected, recWords);;
  W := MakeWindow(bw.s1, bw.s2);;
  w1 := W1Assert(W);;
  Print("\n########## ", label, " ##########\n");
  Print("W-1 assert: ", w1, "\n");
  if not (w1.positive and w1.canary_fails and w1.f1_is_gap_xinv_y and w1.fixture_nonabelian) then
    Error("W-1 fail-closed assert FAILED for ", label);
  fi;

  G := W.PN;;
  P := DerivedSubgroup(G);;
  PhiP := FrattiniSubgroup(P);;
  DP := DerivedSubgroup(P);;
  P2 := Agemo(P,2,1);;
  P4 := Agemo(P,2,2);;
  M4 := ClosureGroup(DP, P4);;
  L3 := ClosureGroup(CommutatorSubgroup(PhiP, P), Agemo(PhiP,2,1));;
  Print("|G|=",Size(G)," Nord=",W.Nord," |P|=",Size(P)," |Phi(P)|=",Size(PhiP),
        " |[P,P]|=",Size(DP)," |P^2|=",Size(P2)," |P^4|=",Size(P4),
        " |M4=[P,P]P^4|=",Size(M4)," |L3|=",Size(L3),"\n");
  Print("Phi(P) = [P,P]P^2 ? ", ClosureGroup(DP,P2) = PhiP, "\n");
  Print("IsAbelian(P)=",IsAbelian(P)," Exponent(P)=",Exponent(P),
        " IdGroup(P)=",IdGroup(P),"\n");
  Print("StructureDescription(P)=", StructureDescription(P), "\n");
  natAb := NaturalHomomorphismByNormalSubgroup(P, DP);;
  Pab := Image(natAb);;
  Print("P^ab invariants=", AbelianInvariants(Pab), "  |P^ab|=", Size(Pab), "\n");
  Print("P/M4 invariants=", AbelianInvariants(Image(NaturalHomomorphismByNormalSubgroup(P,M4))),
        "  |P/M4|=", Index(P,M4), "\n");
  Print("P/Phi(P) invariants=", AbelianInvariants(Image(NaturalHomomorphismByNormalSubgroup(P,PhiP))),
        "\n");

  ## cusp classes
  x3 := W.x^3;; y3 := W.y^3;; z3 := W.z^3;;
  Print("cusps in P? ", [x3 in P, y3 in P, z3 in P],
        "  orders ", [Order(x3),Order(y3),Order(z3)], "\n");
  Print("x3,y3,z3 in Phi(P)? ", [x3 in PhiP, y3 in PhiP, z3 in PhiP], "\n");
  Print("x3,y3,z3 in M4=[P,P]P^4? ", [x3 in M4, y3 in M4, z3 in M4], "\n");
  Print("x3,y3,z3 in [P,P]? ", [x3 in DP, y3 in DP, z3 in DP], "\n");
  Cusp := NormalClosure(G, Subgroup(P,[x3,y3,z3]));;
  Print("|<cusps>^G|=", Size(Cusp), "  image in P^ab has size ",
        Size(Image(natAb, Cusp)), "  invariants ", AbelianInvariants(Image(natAb,Cusp)), "\n");

  ## deck C3 action (Ad(x)) on the layers
  adx := rec();;
  adx.phi := ActOnQuot(P, PhiP, function(p) return AbstractProd([W.x, p, W.x^-1]); end);;
  adx.m4  := ActOnQuot(P, M4,   function(p) return AbstractProd([W.x, p, W.x^-1]); end);;
  adx.ab  := ActOnQuot(P, DP,   function(p) return AbstractProd([W.x, p, W.x^-1]); end);;
  Print("Ad(x) order on P/Phi(P)=", adx.phi.order, "  on P/M4=", adx.m4.order,
        "  on P^ab=", adx.ab.order, "\n");
  Print("Ad(x) nontrivial fixed pts: P/Phi=",
        Number(adx.phi.elems, q -> q <> Identity(Image(adx.phi.nat)) and adx.phi.apply(q)=q),
        "  P/M4=", Number(adx.m4.elems, q -> q <> Identity(Image(adx.m4.nat)) and adx.m4.apply(q)=q),
        "  P^ab=", Number(adx.ab.elems, q -> q <> Identity(Image(adx.ab.nat)) and adx.ab.apply(q)=q),
        "\n");

  ## shadows
  charmingSet := Filtered([0 .. W.Nord-1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
  corr := CorrectedShadows(W, charmingSet);;
  kerChi := Filtered(corr, ss -> (2*ss[1]+1) mod W.Nord = 1 mod W.Nord);;
  Print("|GT(N)|=", Length(corr), "  |ker chi_vir|=", Length(kerChi),
        "  m-distribution=", Collected(List(kerChi, ss -> ss[1])), "\n");
  idS := [0, Identity(G)];;

  res := [];;
  for s in kerChi do
    m := s[1];; f := s[2];; u := 2*m+1;;
    psi := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
             [W.x^u, AbstractProd([f^-1, W.y^u, f])]);;
    if psi = fail then Add(res, rec(m:=m, bad:=true)); continue; fi;
    actFn := function(p) return Image(psi, p); end;;
    aPhi := ActOnQuot(P, PhiP, actFn);;
    aM4  := ActOnQuot(P, M4,   actFn);;
    aAb  := ActOnQuot(P, DP,   actFn);;
    aP   := ActOnQuot(P, TrivialSubgroup(P), actFn);;
    innerMatch := Filtered(Elements(G), gg -> ForAll(Elements(P), p -> Image(psi,p) = AbstractProd([gg,p,gg^-1])));;
    ordS := ShadowOrder(W, s, idS);;
    Add(res, rec(m := m, f := f, ford := Order(f), sord := ordS,
                 oPhi := aPhi.order, oM4 := aM4.order, oAb := aAb.order, oP := aP.order,
                 inner_by := Length(innerMatch)));;
  od;

  Print("\n-- ker chi_vir table (m | ord(f) | ord(shadow) | act.order on P/Phi, P/M4, P^ab, P | #inner-reps) --\n");
  for i in [1..Length(res)] do
    Print("  ", i, ": m=", res[i].m, " ford=", res[i].ford, " sord=", res[i].sord,
          "  [", res[i].oPhi, ",", res[i].oM4, ",", res[i].oAb, ",", res[i].oP, "]",
          "  inner=", res[i].inner_by, "\n");
  od;

  H0 := Filtered([1..Length(res)], i -> res[i].m = 0);;
  Print("H0 (m=0) size=", Length(H0), " shadow orders=", List(H0, i->res[i].sord), "\n");
  kerTheta := Filtered(H0, i -> res[i].oPhi = 1);;
  Print("ker(Theta|H0) size=", Length(kerTheta), " entries=", kerTheta,
        " their [oPhi,oM4,oAb,oP]=", List(kerTheta, i -> [res[i].oPhi,res[i].oM4,res[i].oAb,res[i].oP]),
        " sord=", List(kerTheta, i -> res[i].sord), "\n");
  ## also whole ker Theta inside ker chi_vir
  Print("ker(Theta) in ker chi_vir: size=", Number([1..Length(res)], i -> res[i].oPhi = 1),
        " with m-values=", Collected(List(Filtered([1..Length(res)], i -> res[i].oPhi=1), i->res[i].m)), "\n");
  Print("m=6 slice: [oPhi,oM4,oAb,oP] = ",
        List(Filtered([1..Length(res)], i -> res[i].m <> 0), i -> [res[i].oPhi,res[i].oM4,res[i].oAb,res[i].oP]), "\n");
  return rec(W := W, res := res, P := P, PhiP := PhiP, M4 := M4, DP := DP);;
end;;

##############################################################################
if Length(DEEP15) <> 15 then Error("DEEP15 length != 15"); fi;
R61 := First(DEEP15, r -> r.id = [1152,154161]);;
R63 := Filtered(DEEP15, r -> r.id = [1152,154163]);;

out61  := Report(R61.words, 1152, "[1152,154161]");;
out63a := Report(R63[1].words, 1152, "[1152,154163] rec A");;
out63b := Report(R63[2].words, 1152, "[1152,154163] rec B");;

Print("\nDONE\n");
QUIT_GAP(0);
