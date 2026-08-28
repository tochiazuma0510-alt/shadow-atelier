#############################################################################
## math_f6false_admarking_v1.g -- mathematician (Opus 5), 2026-08-28
##
## PURPOSE: verify the closed-form generator formulas for Ad(sigma_i), Ad(Delta),
## Ad(delta) as automorphisms of A = PB3/K = <xbar,ybar,cbar>, so that the
## (F2) quotient rule can be run on F6=false windows WITHOUT ever building
## B3/K (which costs 6|Q| ~ 8.8M points on the roof M).
##
## Claimed identities in PB3 (x=s1^2, y=s2^2, c=(s1 s2 s1)^2 central):
##   (I1)  c = x * (s2 x s2^-1) * y                       [so z := s2 x s2^-1 = x^-1 y^-1 c]
##   (I2)  Ad(s2)(x) = x^-1 y^-1 c ,  Ad(s2)(y) = y
##   (I3)  Ad(s1)(y) = y^-1 x^-1 c ,  Ad(s1)(x) = x
##   (I4)  Ad(Delta)(x) = y , Ad(Delta)(y) = x           [Delta = s1 s2 s1]
##   (I5)  Ad(delta)(x) = y , Ad(delta)(y) = y^-1 x^-1 c [delta = s1 s2]
## All of these are c-EXACT: they hold whether or not c in K.
#############################################################################

Read("search/drophunt_checker_producer_v2.g");;
if LoadPackage("lins") <> true then Error("MF6: LINS load failed"); fi;

MF6T0 := GAPLIB_WallElapsedMs();;
MF6Search := LowIndexNormalSubgroupsSearch(DCP2B3, 100);;
MF6Nodes := ComputedNormalSubgroups(MF6Search);;
Print("MF6_LINS100 nodes=", Length(MF6Nodes),
  " elapsed_ms=", GAPLIB_WallElapsedMs()-MF6T0, "\n");;

## --------------------------------------------------------------------------
## (A) Verify I1-I5 in EVERY B3/L with [B3:L] <= 100 (these are honest images
##     of sigma1,sigma2, so Ad is directly computable there -- free calibration)
## --------------------------------------------------------------------------
MF6AllOk := true;; MF6Checked := 0;; MF6F6false := 0;; MF6F6true := 0;;
MF6COrders := [];;
for MF6Node in MF6Nodes do
  if Index(MF6Node) = 1 then continue; fi;   # trivial quotient: no sigma marking to test
  MF6L   := Grp(MF6Node);;
  MF6hom := NaturalHomomorphismByNormalSubgroup(DCP2B3, MF6L);;
  MF6Q   := Image(MF6hom);;
  MF6iso := IsomorphismPermGroup(MF6Q);;
  MF6S1  := Image(MF6iso, Image(MF6hom, DCP2s1));;
  MF6S2  := Image(MF6iso, Image(MF6hom, DCP2s2));;
  MF6X   := MF6S1^2;;  MF6Y := MF6S2^2;;
  MF6D   := MF6S1*MF6S2*MF6S1;;      # Delta
  MF6d   := MF6S1*MF6S2;;            # delta
  MF6C   := MF6D^2;;                 # c
  MF6Z   := MF6X^(MF6S2^-1);;        # s2 x s2^-1  (GAP: g^h = h^-1 g h, so use ^(h^-1))
  # I1
  if MF6X*MF6Z*MF6Y <> MF6C then MF6AllOk := false; Print("MF6_FAIL I1 idx=",Index(MF6Node),"\n"); fi;
  # I2
  if MF6X^(MF6S2^-1) <> MF6X^-1*MF6Y^-1*MF6C then MF6AllOk := false; Print("MF6_FAIL I2a idx=",Index(MF6Node),"\n"); fi;
  if MF6Y^(MF6S2^-1) <> MF6Y then MF6AllOk := false; Print("MF6_FAIL I2b idx=",Index(MF6Node),"\n"); fi;
  # I3
  if MF6Y^(MF6S1^-1) <> MF6Y^-1*MF6X^-1*MF6C then MF6AllOk := false; Print("MF6_FAIL I3a idx=",Index(MF6Node),"\n"); fi;
  if MF6X^(MF6S1^-1) <> MF6X then MF6AllOk := false; Print("MF6_FAIL I3b idx=",Index(MF6Node),"\n"); fi;
  # I4
  if MF6X^(MF6D^-1) <> MF6Y then MF6AllOk := false; Print("MF6_FAIL I4a idx=",Index(MF6Node),"\n"); fi;
  if MF6Y^(MF6D^-1) <> MF6X then MF6AllOk := false; Print("MF6_FAIL I4b idx=",Index(MF6Node),"\n"); fi;
  # I5
  if MF6X^(MF6d^-1) <> MF6Y then MF6AllOk := false; Print("MF6_FAIL I5a idx=",Index(MF6Node),"\n"); fi;
  if MF6Y^(MF6d^-1) <> MF6Y^-1*MF6X^-1*MF6C then MF6AllOk := false; Print("MF6_FAIL I5b idx=",Index(MF6Node),"\n"); fi;
  # c central in B3/L ?
  if MF6C^(MF6S1^-1) <> MF6C or MF6C^(MF6S2^-1) <> MF6C then
    MF6AllOk := false; Print("MF6_FAIL Ccentral idx=",Index(MF6Node),"\n"); fi;
  MF6Checked := MF6Checked + 1;;
  if MF6C = Identity(Image(MF6iso)) then MF6F6true := MF6F6true+1;;
  else MF6F6false := MF6F6false+1;; fi;
  Add(MF6COrders, Order(MF6C));;
od;
Print("MF6_IDENTITIES all_ok=", MF6AllOk, " windows_checked=", MF6Checked, "\n");
Print("MF6_F6DIST lins<=100 : F6true(c in L)=", MF6F6true,
      "  F6false(c notin L)=", MF6F6false, "\n");
Print("MF6_CORD_SET = ", Set(MF6COrders), "\n");

## --------------------------------------------------------------------------
## (B) b3_index = 96 (K_ord=18, F2=2) -- the named F6=false calibration window.
##     Build A = <JX,JY,JC> on the SAME 36+degL points; build theta~,tau~ as
##     automorphisms of A from the closed forms; no B3/K anywhere.
## --------------------------------------------------------------------------
MF6Tgt := fail;;
for MF6Node in MF6Nodes do
  if Index(MF6Node) = 96 then
    MF6q := DCP2BuildWindow(Grp(MF6Node));;
    if MF6q.K_ord = 18 and MF6q.F2 = 2 then MF6Tgt := MF6q;; break; fi;
  fi;
od;
if MF6Tgt = fail then Error("MF6: b3_index=96 target window not found"); fi;

Print("\nMF6_WIN96 c_in_K(F6)=", MF6Tgt.c_in_K, " K_ord=", MF6Tgt.K_ord,
      " F2=", MF6Tgt.F2, " F3=", MF6Tgt.F3, " degL=", MF6Tgt.degL,
      " |G=<x,y>|=", Size(MF6Tgt.G), "\n");

## joint c: M-block image is identity (K^(9)-type roof, documented);
## L-block image is Cp, already computed by the producer.
MF6JC := DCP2DirectSumPerm(Identity(DCP2MBlock), DCP2MDegree, MF6Tgt.Cp_on_L, MF6Tgt.degL);;
MF6A  := Group(MF6Tgt.JX, MF6Tgt.JY, MF6JC);;
Print("MF6_WIN96 ord(cbar)=", Order(MF6JC),
      "  |A=PB3/K|=", Size(MF6A),
      "  |A|/|G|=", Size(MF6A)/Size(MF6Tgt.G),
      "  perm_degree=", LargestMovedPoint(MF6A),
      "  cbar_central_in_A=", ForAll(GeneratorsOfGroup(MF6A), g -> g*MF6JC = MF6JC*g), "\n");

## theta~ : x->y, y->x, c->c        tau~ : x->y, y->y^-1 x^-1 c, c->c
MF6Th := GroupHomomorphismByImages(MF6A, MF6A,
           [MF6Tgt.JX, MF6Tgt.JY, MF6JC],
           [MF6Tgt.JY, MF6Tgt.JX, MF6JC]);;
MF6Ta := GroupHomomorphismByImages(MF6A, MF6A,
           [MF6Tgt.JX, MF6Tgt.JY, MF6JC],
           [MF6Tgt.JY, MF6Tgt.JY^-1*MF6Tgt.JX^-1*MF6JC, MF6JC]);;
Print("MF6_AUT theta_welldefined=", MF6Th <> fail,
      "  tau_welldefined=", MF6Ta <> fail, "\n");
if MF6Th <> fail and MF6Ta <> fail then
  Print("MF6_AUT theta_bijective=", IsBijective(MF6Th),
        "  tau_bijective=", IsBijective(MF6Ta),
        "  theta^2=id=", ForAll(GeneratorsOfGroup(MF6A), g->Image(MF6Th,Image(MF6Th,g))=g),
        "  tau^3=id=", ForAll(GeneratorsOfGroup(MF6A), g->Image(MF6Ta,Image(MF6Ta,Image(MF6Ta,g)))=g),
        "\n");
  Print("MF6_AUT theta_tau_theta = tau^-1 : ",
        ForAll(GeneratorsOfGroup(MF6A),
          g -> Image(MF6Th,Image(MF6Ta,Image(MF6Th,g))) = PreImagesRepresentative(MF6Ta,g)), "\n");
fi;

## --------------------------------------------------------------------------
## (C) The concrete row-level difference on b3_index=96:
##     naive word-level tau (v1) vs Ad(delta) quotient rule (F2), per row.
## --------------------------------------------------------------------------
MF6EvalW := function(letters, gx, gy, one)
  local z, l;
  z := one;;
  for l in letters do
    if l[1]="x" then z := z*gx^l[2]; else z := z*gy^l[2]; fi;
  od;
  return z;
end;;

## naive word-level theta/tau on a LETTER LIST (the rejected v1 prescription):
##   theta_naive : x<->y   ;   tau_naive : x->y, y->(xy)^-1   [c dropped]
MF6NaiveTau := function(letters)
  local out, l;
  out := [];;
  for l in letters do
    if l[1]="x" then Add(out, ["y", l[2]]);
    else
      if l[2] = 1 then Append(out, [["y",-1],["x",-1]]);
      else Append(out, [["x",1],["y",1]]); fi;
    fi;
  od;
  return out;
end;;

Print("\nMF6_ROWS b3_index=96  (seed, m, f-word) : naive-tau LHS vs Ad(delta) LHS vs RHS c^m\n");
MF6Hlist := Elements(MF6Tgt.H);;
for MF6Seed in DCP2Seeds do
  MF6JF := EvalWordInQ(MF6Seed.letters, MF6Tgt.JX, MF6Tgt.JY, Identity(MF6Tgt.G));;
  for MF6h in MF6Hlist do
    MF6p := MF6JF * MF6h;;
    MF6wp := DCP2FreeEltToLetters(PreImagesRepresentative(MF6Tgt.epi, MF6p));;
    for MF6m in List([0..(MF6Tgt.K_ord/MF6Tgt.M_ord)-1], t -> MF6Seed.m_seed + MF6Tgt.M_ord*t) do
      # y^m f  as an element of A
      MF6ymf := MF6Tgt.JY^MF6m * MF6p;;
      # (F2) quotient rule:  tau~^2(y^m f) tau~(y^m f) (y^m f) =? c^m
      MF6lhsF2 := Image(MF6Ta, Image(MF6Ta, MF6ymf)) * Image(MF6Ta, MF6ymf) * MF6ymf;;
      MF6rhs   := MF6JC^MF6m;;
      # naive word-level rule (v1): apply tau_naive to the LETTERS, then evaluate
      MF6ymfL  := Concatenation(List([1..MF6m], i->["y",1]), MF6wp);;
      MF6t1L   := MF6NaiveTau(MF6ymfL);;
      MF6t2L   := MF6NaiveTau(MF6t1L);;
      MF6lhsNv := MF6EvalW(MF6t2L, MF6Tgt.JX, MF6Tgt.JY, Identity(MF6Tgt.G))
                * MF6EvalW(MF6t1L, MF6Tgt.JX, MF6Tgt.JY, Identity(MF6Tgt.G))
                * MF6EvalW(MF6ymfL, MF6Tgt.JX, MF6Tgt.JY, Identity(MF6Tgt.G));;
      Print("  seed=", MF6Seed.name, " m=", MF6m,
            " | F2rule_holds=", MF6lhsF2 = MF6rhs,
            " | naive_holds=",  MF6lhsNv = Identity(MF6Tgt.G),
            " | naive_vs_F2_same_LHS=", MF6lhsNv = MF6lhsF2,
            " | c^m=1? ", MF6rhs = Identity(MF6A), "\n");
    od;
  od;
od;

Print("\nMF6_DONE\n");
QUIT;
