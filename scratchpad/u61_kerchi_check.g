# [U6-1] 実装係の chi_vir 具体化のレビュー(数学者・独立確認)
#   主張: ker(chi_vir) = C_Q(Sylow_ell) = S_t x C_ell ,  [ker : [Q,Q]] = 2 ,
#         free crown = #{maximal M : M >= ker} = omega(ell-1)
SizeScreen([4096,0]);;
MakeAGL1 := function(ell)
  local z,a,b,i;
  z := PrimitiveRoot(GF(ell));;
  a := PermList(List([1..ell], i -> ((i-1+1) mod ell)+1));;
  b := PermList(List([1..ell], i -> (Int((i-1)*IntFFE(z)) mod ell)+1));;
  return Group(a,b);
end;;
OmegaN := function(n) return Length(Set(FactorsInt(n))); end;;
Chk := function(name,t,ell)
  local St,A,Q,der,syl,ker,mcl,nfree,c,M;
  St := SymmetricGroup(t);; A := MakeAGL1(ell);; Q := DirectProduct(St,A);;
  der := DerivedSubgroup(Q);;
  syl := SylowSubgroup(Q, ell);;
  ker := Centralizer(Q, syl);;
  mcl := ConjugacyClassesMaximalSubgroups(Q);;
  nfree := 0;;
  for c in mcl do M := Representative(c);; if IsSubset(M,ker) then nfree := nfree+1; fi; od;
  Print(name," (t=",t,",ell=",ell,")  |Q|=",Size(Q),
        "  |Syl_ell|=",Size(syl),
        "  |ker=C_Q(Syl)|=",Size(ker),
        "  |[Q,Q]|=",Size(der),
        "  [ker:[Q,Q]]=",Size(ker)/Size(der),
        "  Q/ker =",StructureDescription(Q/ker),
        "  (= C_{ell-1}? ",Size(Q)/Size(ker)=ell-1,")\n");
  Print("      ker = S_t x C_ell ? ",Size(ker)=Size(St)*ell,
        "   free crowns (M >= ker) = ",nfree,
        "   (theory omega(ell-1) = ",OmegaN(ell-1),")\n");
end;;
Chk("wall24",5,19); Chk("wall28",5,23); Chk("wall36",5,31); Chk("wall37",6,31);
QUIT;
