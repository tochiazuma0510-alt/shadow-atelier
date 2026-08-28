#############################################################################
## pg1_pi_semantics_v1.g -- PG-1 decisive gate (mathematician, 2026-08-29)
## Claim under test: the census "pi" column is the degree-9 BLOCK COORDINATE
## of the shadow element f in the fixed roof window M, whose block group is
## the SPECIFIC PSL(2,8) = <X4,Y4> built by the producer -- hence every pi
## lies in PSL(2,8) BY CONSTRUCTION and no PGammaL/PSL coset can be carried.
## Verbatim source: search/d972_b4_word_key_artifact_v1.g L68-70
##   B4WKfirst :=D972BlockRestrict(B4WKf,0,27);
##   B4WKsecond:=D972BlockRestrict(B4WKf,27,9);
##   B4WKkey   :=[B4WKSh.m, D972Can9(B4WKfirst), D972Can4(B4WKsecond)];
## and search/d972_dovetail_core_v2.g L171-173
##   D972Can4 := function(perm9) return List([1..9],j->j^perm9); end;
#############################################################################
Read("search/drophunt_checker_producer_v2.g");;   ## builds DCP2X4, DCP2Y4, DCP2P4
Read("scratchpad/pi_values_export.g");;           ## PIV = the 27 distinct pi values

P4 := Group(DCP2X4, DCP2Y4);;
Print("PG1_BLOCK_GROUP_ORDER ", Size(P4), "  (producer asserts 504)\n");
Print("PG1_BLOCK_DEGREE ", LargestMovedPoint(P4), "\n");
Print("PG1_ALL_PI_IN_BLOCK_GROUP ", ForAll(PIV, p -> p in P4), "\n");
Print("PG1_PI_COUNT ", Length(PIV), "  generate_order ", Size(Group(PIV)),
      "  equals_block_group ", Group(PIV) = P4, "\n");
## roof factorisation 27 + 9
Print("PG1_G9_ORDER ", Size(DCP2G9Rec.G), "  x  PSL_ORDER ", Size(P4),
      "  =  ", Size(DCP2G9Rec.G)*Size(P4),
      "   |PB3/M| = ", Size(DCP2MBlock), "\n");
Print("PG1_ROOF_IS_DIRECT_PRODUCT_27x9 ",
      Size(DCP2G9Rec.G)*Size(P4) = Size(DCP2MBlock), "\n");
## is there ANY PGammaL(2,8) anywhere in the window?  The block group is the
## full degree-9 factor, and [PGammaL:PSL]=3 would need order 1512.
Print("PG1_BLOCK_INDEX_IN_PGammaL ", 1512/Size(P4), "\n");
Print("PG1_BLOCK_IS_NORMALISED_BY_ITS_OWN_NORMALISER_ONLY ",
      Size(Normalizer(SymmetricGroup(9), P4)), " (=1512 = PGammaL, NOT in the window)\n");
Print("PG1_VERDICT carrier_absent_by_construction ",
      ForAll(PIV, p -> p in P4) and Size(P4) = 504, "\n");
QUIT;
