##############################################################################
## m3_l2_probe_v3.g -- M3 (E[4] lane): matrices of the GT(N) action on P^ab,
##   Weil-pairing canary det(T_{m,f}) = 2m+1 mod 4, image/kernel of
##   GT(N) -> Aut(P^ab), and the normalizer-of-Cartan check.
## Author: shadow-atelier mathematician (Claude / Opus 5), 2026-08-23.
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
  local genElts, N, hm, Gimg, isoQ;
  genElts := List(words, w -> EvalString(w));;
  N := Subgroup(B3, genElts);;
  if Index(B3, N) <> indexExpected or not IsNormal(B3, N) then Error("window build failed"); fi;
  hm := NaturalHomomorphismByNormalSubgroup(B3, N);;
  Gimg := Image(hm);;
  isoQ := IsomorphismPermGroup(Gimg);;
  return rec(s1 := Image(isoQ, Image(hm, ga)), s2 := Image(isoQ, Image(hm, gb)));;
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

W1Assert := function(W)
  local f1, fbad, rhs;
  f1   := AbstractProd([W.y, W.x^-1]);
  fbad := AbstractProd([W.x^-1, W.y]);
  rhs  := AbstractProd([W.x, W.s2, W.x^-1]);
  return rec(positive := (AbstractProd([f1^-1, W.s2, f1]) = rhs),
             canary_fails := not (AbstractProd([fbad^-1, W.s2, fbad]) = rhs),
             f1_is_gap_xinv_y := (f1 = W.x^-1 * W.y),
             fixture_nonabelian := not IsAbelian(W.Bq));;
end;;

##############################################################################
Analyse := function(recWords, idExpected, label)
  local bw, W, w1, G, P, DP, nat, Pab, gensAb, u1, v1, MatOf, ActMat, i, j, k,
        charmingSet, corr, s, m, f, uu, psi, M, dets, mats, imgset, Adx, AdxM,
        cusp, ok, badDet, Cusps, autPab, homAdx, nrm, MatMul, MatEq, imgGrp,
        kerSize, seen, detOK, ccIdx, ccM, commAdx;
  bw := BuildWindowFromWords(idExpected, recWords);;
  W := MakeWindow(bw.s1, bw.s2);;
  w1 := W1Assert(W);;
  Print("\n########## ", label, " ##########\n");
  if not (w1.positive and w1.canary_fails and w1.f1_is_gap_xinv_y and w1.fixture_nonabelian) then
    Error("W-1 fail-closed assert FAILED");
  fi;
  Print("W-1 assert PASS (positive + negative canary)\n");

  G := W.PN;; P := DerivedSubgroup(G);; DP := DerivedSubgroup(P);;
  nat := NaturalHomomorphismByNormalSubgroup(P, DP);;
  Pab := Image(nat);;
  gensAb := IndependentGeneratorsOfAbelianGroup(Pab);;
  Print("|P^ab|=", Size(Pab), " inv=", AbelianInvariants(Pab),
        " indep gens orders=", List(gensAb, Order), "\n");
  if Length(gensAb) <> 2 or Set(List(gensAb, Order)) <> [4] then
    Error("P^ab is not (Z/4)^2 with 2 independent generators");
  fi;
  u1 := gensAb[1];; v1 := gensAb[2];;

  # coordinates: express w in P^ab as u1^i * v1^j
  MatOf := function(imgU, imgV)
    local ii, jj, aa, bb, cc, dd, r;
    aa := fail;; for ii in [0..3] do for jj in [0..3] do
      if u1^ii * v1^jj = imgU then aa := ii; bb := jj; fi; od; od;
    cc := fail;; for ii in [0..3] do for jj in [0..3] do
      if u1^ii * v1^jj = imgV then cc := ii; dd := jj; fi; od; od;
    if aa = fail or cc = fail then Error("coordinate lookup failed"); fi;
    return [[aa,bb],[cc,dd]];   # rows = images of u1, v1
  end;;

  ActMat := function(actFn)
    return MatOf(Image(nat, actFn(PreImagesRepresentative(nat, u1))),
                 Image(nat, actFn(PreImagesRepresentative(nat, v1))));
  end;;

  AdxM := ActMat(function(p) return AbstractProd([W.x, p, W.x^-1]); end);;
  Print("matrix of Ad(x) on P^ab (rows = images of indep gens) = ", AdxM,
        "  det=", (AdxM[1][1]*AdxM[2][2]-AdxM[1][2]*AdxM[2][1]) mod 4,
        "  trace=", (AdxM[1][1]+AdxM[2][2]) mod 4, "\n");
  Print("  [predicted: Ad(x) = mult by zeta_3 on O/4, so det=N(w)=1, trace=Tr(w)=-1=3]\n");

  ## cusps
  Print("x^3,y^3,z^3 in [P,P]? ", [W.x^3 in DP, W.y^3 in DP, W.z^3 in DP],
        "  |<cusps>^G|=", Size(NormalClosure(G, Subgroup(P,[W.x^3,W.y^3,W.z^3]))),
        "  |[P,P]|=", Size(DP), "\n");

  charmingSet := Filtered([0 .. W.Nord-1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
  corr := CorrectedShadows(W, charmingSet);;
  Print("|GT(N)|=", Length(corr), "\n");

  mats := [];; detOK := true;; ccIdx := fail;;
  for i in [1..Length(corr)] do
    s := corr[i];; m := s[1];; f := s[2];; uu := 2*m+1;;
    psi := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
             [W.x^uu, AbstractProd([f^-1, W.y^uu, f])]);;
    M := ActMat(function(p) return Image(psi, p); end);;
    Add(mats, rec(m := m, u := uu, M := M,
                  det := (M[1][1]*M[2][2]-M[1][2]*M[2][1]) mod 4));
    if mats[i].det <> uu mod 4 then detOK := false;
      Print("  !! det mismatch at m=", m, " det=", mats[i].det, " u mod 4=", uu mod 4, "\n"); fi;
    if m = 11 and f = Identity(G) then ccIdx := i; fi;
  od;
  Print("WEIL CANARY  det(T_{m,f} on P^ab) = (2m+1) mod 4 for all ", Length(corr),
        " shadows? ", detOK, "\n");

  ## image / kernel of GT(N) -> Aut(P^ab)
  imgset := Set(List(mats, r -> r.M));;
  Print("|image of GT(N) in Aut(P^ab)| = ", Length(imgset),
        "   |kernel| = ", Length(corr)/Length(imgset), "\n");
  autPab := AutomorphismGroup(Pab);;
  homAdx := GroupHomomorphismByImages(Pab, Pab, [u1,v1],
              [Image(nat, AbstractProd([W.x, PreImagesRepresentative(nat,u1), W.x^-1])),
               Image(nat, AbstractProd([W.x, PreImagesRepresentative(nat,v1), W.x^-1]))]);;
  Print("|Aut(P^ab)|=", Size(autPab),
        "  |C(Ad x)|=", Size(Centralizer(autPab, homAdx)),
        "  |N(<Ad x>)|=", Size(Normalizer(autPab, Group(homAdx))), "\n");

  ## complex conjugation shadow [11, 1]
  if ccIdx <> fail then
    ccM := mats[ccIdx].M;;
    commAdx := (ccM * AdxM) mod 4 = (AdxM * ccM) mod 4;;
    Print("cc shadow [11,1]: M=", ccM, " det=", mats[ccIdx].det,
          " (expect -1=3)  commutes with Ad(x)? ", commAdx, " (expect false: cc is in N \\ C)\n");
  else
    Print("cc shadow [11,1] NOT FOUND in GT(N) enumeration !!\n");
  fi;

  ## ker chi_vir detail with matrices
  Print("\n-- ker chi_vir: matrices on P^ab --\n");
  for i in [1..Length(corr)] do
    if (2*corr[i][1]+1) mod W.Nord = 1 mod W.Nord then
      Print("  m=", mats[i].m, " M=", mats[i].M, " det=", mats[i].det,
            "  is -I? ", mats[i].M = [[3,0],[0,3]],
            "  commutes Adx? ", (mats[i].M*AdxM) mod 4 = (AdxM*mats[i].M) mod 4, "\n");
    fi;
  od;
  return true;;
end;;

##############################################################################
R61 := First(DEEP15, r -> r.id = [1152,154161]);;
R63 := Filtered(DEEP15, r -> r.id = [1152,154163]);;
Analyse(R61.words, 1152, "[1152,154161]");;
Analyse(R63[1].words, 1152, "[1152,154163] rec A");;
Analyse(R63[2].words, 1152, "[1152,154163] rec B");;
Print("\nDONE\n");
QUIT_GAP(0);
