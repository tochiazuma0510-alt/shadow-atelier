##############################################################################
## m3_l2_probe_v2.g -- M3 (E[4] lane): identify the ker(Theta|H0) involution
##   theta_t inside Aut(P^ab) (= Aut(E[4]) under the L2-LIFT identification).
## Decisive question: is theta_t equal to inversion (v |-> -v) on P^ab ?
##   (Bit 1 = YES  <=>  theta_t = -1, see c83_m3_e4_lane_v1.md)
## Author: shadow-atelier mathematician (Claude / Opus 5), 2026-08-23.
## Convention: W-1 (paper "AB" = GAP B*A) via AbstractProd; fail-closed assert.
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

CompShadow := function(W, s1, s2)
  local m1,f1,m2,f2,u1,psi1;
  m1 := s1[1];; f1 := s1[2];; m2 := s2[1];; f2 := s2[2];; u1 := 2*m1+1;;
  psi1 := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
            [W.x^u1, AbstractProd([f1^-1, W.y^u1, f1])]);;
  if psi1 = fail then return fail; fi;
  return [(2*m1*m2 + m1 + m2) mod W.Nord, AbstractProd([f1, Image(psi1, f2)])];;
end;;

ShadowOrder := function(W, s, idS)
  local cur, k;
  cur := s;; k := 1;;
  while cur <> idS and k < 100 do cur := CompShadow(W, cur, s);; k := k+1;; od;
  return k;;
end;;

##############################################################################
Analyse := function(recWords, idExpected, label)
  local bw, W, w1, G, P, DP, nat, Pab, els, idPab, AdxAb, ApplyAb, MkMap,
        inv, adPow, cand, candName, i, j, charmingSet, corr, kerChi, s, m, f, u,
        psi, mp, matched, res, H0, tIdx, tMap, autGrp, cent, normlz, nm,
        AdxOnP, k, autPab, gens, imgs, hom, cAd, ord3elts, invMap;
  bw := BuildWindowFromWords(idExpected, recWords);;
  W := MakeWindow(bw.s1, bw.s2);;
  w1 := W1Assert(W);;
  Print("\n########## ", label, " ##########\n");
  Print("W-1 assert: ", w1, "\n");
  if not (w1.positive and w1.canary_fails and w1.f1_is_gap_xinv_y and w1.fixture_nonabelian) then
    Error("W-1 fail-closed assert FAILED");
  fi;

  G := W.PN;; P := DerivedSubgroup(G);; DP := DerivedSubgroup(P);;
  nat := NaturalHomomorphismByNormalSubgroup(P, DP);;
  Pab := Image(nat);;
  els := Elements(Pab);;
  idPab := Identity(Pab);;
  Print("|P^ab|=", Size(Pab), " inv=", AbelianInvariants(Pab), "\n");

  # a map on P^ab is represented as the list of images of els (in order)
  MkMap := function(actFn)
    return List(els, q -> Image(nat, actFn(PreImagesRepresentative(nat, q))));
  end;;

  AdxAb := MkMap(function(p) return AbstractProd([W.x, p, W.x^-1]); end);;
  invMap := List(els, q -> q^-1);;
  # candidate maps: eps * Adx^j  (eps = +-1, j = 0,1,2), composed pointwise
  cand := [];; candName := [];;
  for j in [0,1,2] do
    for i in [1,-1] do
      # Adx^j then eps
      Add(cand, List([1..Length(els)], k -> (function(q0) local r,jj;
              r := q0; for jj in [1..j] do r := AdxAb[Position(els, r)]; od;
              if i = -1 then r := r^-1; fi; return r; end)(els[k])));
      Add(candName, Concatenation("(", String(i), ")*Adx^", String(j)));
    od;
  od;

  # sanity: order of Adx on P^ab, and that Adx^3 = id
  Print("Adx^3 = id on P^ab? ",
        List([1..Length(els)], k -> AdxAb[Position(els, AdxAb[Position(els, AdxAb[k])])]) = els, "\n");
  Print("Adx fixes only 0 on P^ab? ",
        Number([1..Length(els)], k -> AdxAb[k] = els[k]) = 1, "\n");
  # is Adx = -1 ?  (should be false: -1 has order 2)
  Print("Adx = inversion? ", AdxAb = invMap, "\n");

  charmingSet := Filtered([0 .. W.Nord-1], mm -> Gcd(2*mm+1, W.Nord) = 1);;
  corr := CorrectedShadows(W, charmingSet);;
  kerChi := Filtered(corr, ss -> (2*ss[1]+1) mod W.Nord = 1 mod W.Nord);;
  Print("|GT(N)|=", Length(corr), " |ker chi_vir|=", Length(kerChi), "\n");

  res := [];;
  for s in kerChi do
    m := s[1];; f := s[2];; u := 2*m+1;;
    psi := GroupHomomorphismByImages(W.PN, W.PN, [W.x, W.y],
             [W.x^u, AbstractProd([f^-1, W.y^u, f])]);;
    mp := MkMap(function(p) return Image(psi, p); end);;
    matched := Filtered([1..Length(cand)], i -> cand[i] = mp);;
    Add(res, rec(m := m, ford := Order(f),
                 sord := ShadowOrder(W, s, [0, Identity(G)]),
                 is_id := (mp = els), is_inv := (mp = invMap),
                 match := List(matched, i -> candName[i]),
                 nfix := Number([1..Length(els)], k -> mp[k] = els[k])));;
  od;

  Print("\n-- ker chi_vir on P^ab (m | ord f | ord shadow | #fixed | class) --\n");
  for i in [1..Length(res)] do
    Print("  ", i, ": m=", res[i].m, " ford=", res[i].ford, " sord=", res[i].sord,
          " nfix=", res[i].nfix, " class=", res[i].match,
          " is_inv=", res[i].is_inv, "\n");
  od;

  H0 := Filtered([1..Length(res)], i -> res[i].m = 0);;
  tIdx := Filtered(H0, i -> (not res[i].is_id) and res[i].sord = 2);;
  Print("H0 classes = ", List(H0, i -> res[i].match), "\n");
  Print("candidate t (m=0, shadow order 2, non-identity): idx=", tIdx,
        " class=", List(tIdx, i -> res[i].match),
        " IS_INVERSION=", List(tIdx, i -> res[i].is_inv), "\n");

  ## structural canaries in Aut(P^ab)
  autPab := AutomorphismGroup(Pab);;
  Print("|Aut(P^ab)|=", Size(autPab), " (GL_2(Z/4) has order 96)\n");
  hom := GroupHomomorphismByImages(Pab, Pab, els, AdxAb);;
  if hom <> fail then
    cAd := Centralizer(autPab, hom);;
    Print("|Centralizer_Aut(Adx)|=", Size(cAd),
          " (Cartan (O/4)^* has order 12)  |Normalizer<Adx>|=",
          Size(Normalizer(autPab, Group(hom))), " (expect 24)\n");
  fi;
  return true;;
end;;

##############################################################################
if Length(DEEP15) <> 15 then Error("DEEP15 length != 15"); fi;
R61 := First(DEEP15, r -> r.id = [1152,154161]);;
R63 := Filtered(DEEP15, r -> r.id = [1152,154163]);;
Analyse(R61.words, 1152, "[1152,154161]");;
Analyse(R63[1].words, 1152, "[1152,154163] rec A");;
Analyse(R63[2].words, 1152, "[1152,154163] rec B");;
Print("\nDONE\n");
QUIT_GAP(0);
