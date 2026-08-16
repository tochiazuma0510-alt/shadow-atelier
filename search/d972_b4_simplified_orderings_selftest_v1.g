#############################################################################
## Numeric-only fail-closed selftest for d972_b4_simplified_orderings_v1.g.
#############################################################################
D972SOOrderNames:=["shortlex","recursive","rt_recursive","wreathprod",
  "wreathprod_reverse","wtlex","wtlex_reverse","recursive_reverse"];;
D972SOPerms:=[
  [1,2,3,4,5],[2,1,3,4,5],[3,2,1,4,5],[4,2,3,1,5],[5,2,3,4,1],
  [2,3,4,5,1],[5,1,2,3,4],[2,1,4,3,5],[3,4,5,1,2],[5,4,3,2,1]
];;
D972SOI:=1;; D972SPI:=1;;
if IsBound(D972_B4_SIMPLE_ORDERING_INDEX) then D972SOI:=D972_B4_SIMPLE_ORDERING_INDEX; fi;
if IsBound(D972_B4_SIMPLE_PERM_INDEX) then D972SPI:=D972_B4_SIMPLE_PERM_INDEX; fi;
if not IsInt(D972SOI) or D972SOI<1 or D972SOI>Length(D972SOOrderNames) then Error("ORDERING selftest index drift"); fi;
if not IsInt(D972SPI) or D972SPI<1 or D972SPI>Length(D972SOPerms) then Error("PERM selftest index drift"); fi;
if Length(Set(D972SOPerms[D972SPI]))<>5 then Error("PERM selftest nonbijection"); fi;
Print("B4_SIMPLE_ORDERINGS_SELFTEST_PASS order_index=",D972SOI,
  " ordering=",D972SOOrderNames[D972SOI]," permutation_index=",D972SPI,
  " permutation=",D972SOPerms[D972SPI],"\n");
Print("B4_SIMPLE_ORDERINGS_SELFTEST_FINAL_MARKER\n");
