#############################################################################
## search/probe/wac_v1/sol87_fix.g
##  裁定 232: Sol 定理 SOL87-FIX の機械裏取り。
##  H = (C_ell^r : S_r) x S_t (t=0),  B = C_ell^r,  T in Syl_2(H).
##  主張: C_{O_{2'}(H)}(T) = B^{T_r} = C_ell^{s_2(r)}.
##  O_{2'}(H) = B : O_{2'}(S_r)(t=0)を preimage で安価に構成。
##  s_2(r)=2 進桁和。予測 5^{s_2(r)}: r=1..8 -> 5,5,25,5,25,25,125,5.
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
s2 := function(r)
  local s;
  s := 0;
  while r > 0 do s := s + (r mod 2); r := QuoInt(r,2); od;
  return s;
end;;

OddCore := function(G)   ## largest odd-order normal subgroup (small G のみ)
  local best, N;
  best := TrivialSubgroup(G);
  for N in NormalSubgroups(G) do
    if Size(N) mod 2 = 1 and Size(N) > Size(best) then best := N; fi;
  od;
  return best;
end;;

CheckR := function(ell, r)
  local W, proj, B, Sr, O2pSr, O2p, T, C, s2r, predicted, blockact, Tr, orbs;
  W := WreathProduct(CyclicGroup(IsPermGroup, ell), SymmetricGroup(r));
  proj := Projection(W);                          ## W -> S_r
  B := KernelOfMultiplicativeGeneralMapping(proj);## base C_ell^r
  Sr := SymmetricGroup(r);
  O2pSr := OddCore(Sr);                           ## O_{2'}(S_r): C_3 (r=3) else 1
  O2p := PreImage(proj, O2pSr);                   ## = B : O_{2'}(S_r) = O_{2'}(H) (t=0)
  T := SylowSubgroup(W, 2);
  C := Centralizer(O2p, T);
  s2r := s2(r);
  predicted := ell^s2r;
  Print("ell=", ell, " r=", r,
        "  |H|=", Size(W),
        "  |B|=", Size(B),
        "  |O_2'(S_r)|=", Size(O2pSr),
        "  |O_2'(H)|=", Size(O2p),
        "  |T|=", Size(T),
        "\n    s_2(", r, ")=", s2r,
        "  predicted 5^s2=", predicted,
        "  |C_{O2'(H)}(T)|=", Size(C),
        "  MATCH? ", Size(C) = predicted,
        "  C<=B? ", IsSubgroup(B, C),
        "  struct ", StructureDescription(C), "\n");
  return Size(C) = predicted;
end;;

Print("######## SOL87-FIX machine check (ell=5, t=0) ########\n");
ok := true;;
for r in [1,2,3,4,5,6,7,8] do
  ok := CheckR(5, r) and ok;
od;
Print("\nALL MATCH (r=1..8) ? ", ok, "\n");

## t=3 の tail C_3 も消えることの確認(r=2, t=3)
Print("\n######## tail C_3 消滅の確認 (r=2, t=3) ########\n");
Wt := DirectProduct(WreathProduct(CyclicGroup(IsPermGroup,5), SymmetricGroup(2)),
                    SymmetricGroup(3));;
O2pWt := OddCore(Wt);;
Tt := SylowSubgroup(Wt, 2);;
Ct := Centralizer(O2pWt, Tt);;
Print("r=2,t=3: |O_2'(H)|=", Size(O2pWt), " |C_{O2'}(T)|=", Size(Ct),
      " predicted 5^s2(2)=", 5^s2(2), " (tail C_3 が消えれば 5) MATCH? ",
      Size(Ct)=5^s2(2), "\n");

Print("\nSOL87_FIX_DONE\n");
QUIT;
