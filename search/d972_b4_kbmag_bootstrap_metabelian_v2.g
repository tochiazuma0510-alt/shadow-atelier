#############################################################################
## d972_b4_kbmag_bootstrap_metabelian_v2.g -- v2 target bootstrap shim.
##
## The generic bootstrap is pinned byte-for-byte.  Its temporary allow-list
## contains exactly the v2 wrapper; that wrapper reads the pinned v1 producer,
## forces POST_REPLAY=true, and emits the v2 receipt after the v1 replay.
## No workflow file or repository source is edited at runtime.
#############################################################################

D972MBV2BasePath:="search/d972_b4_kbmag_bootstrap_v1.g";;
D972MBV2BaseSha:="ea679047579065c03ac47680aaf97fe3b1ee7726fbc6f2eee273277307d6fb25";;
D972MBV2Target:="search/d972_b4_u_metabelian_kbmag_v3.g";;
D972MBV2TargetSha:="d57e8556076d1bc6ea684ae7ba5d9dd47fccf195e58bac172c92c252a9c0026e";;
if IsBound(D972_B4_KBMAG_BOOTSTRAP_TARGET) then
  if D972_B4_KBMAG_BOOTSTRAP_TARGET<>D972MBV2Target then
    Error("metabelian v2 bootstrap: target must be v2 wrapper");
  fi;
else
  Error("metabelian v2 bootstrap: target is required");
fi;
D972MBV2Raw:=StringFile(D972MBV2BasePath);;
if D972MBV2Raw=fail or HexSHA256(D972MBV2Raw)<>D972MBV2BaseSha then
  Error("metabelian v2 bootstrap: generic bootstrap SHA drift");
fi;
D972MBV2TargetRaw:=StringFile(D972MBV2Target);;
if D972MBV2TargetRaw=fail then
  Error("metabelian v2 bootstrap: v2 target missing");
fi;
D972MBV2TargetActualSha:=HexSHA256(D972MBV2TargetRaw);;
if D972MBV2TargetActualSha<>D972MBV2TargetSha then
  Error("metabelian v2 bootstrap: pinned target SHA drift");
fi;
D972MBV2Needle:="  \"search/d972_b4_simplified_orderings_v1.g\" ]";;
D972MBV2Replacement:="  \"search/d972_b4_u_metabelian_kbmag_v3.g\" ]";;
D972MBV2At:=PositionSublist(D972MBV2Raw,D972MBV2Needle);;
if D972MBV2At=fail or
   PositionSublist(
     D972MBV2Raw{[D972MBV2At+Length(D972MBV2Needle)..Length(D972MBV2Raw)]},
     D972MBV2Needle)<>fail then
  Error("metabelian v2 bootstrap: allow-list splice drift");
fi;
D972MBV2Patched:=Concatenation(
  D972MBV2Raw{[1..D972MBV2At-1]},D972MBV2Replacement,
  D972MBV2Raw{[D972MBV2At+Length(D972MBV2Needle)..Length(D972MBV2Raw)]});;
D972MBV2Temp:=Filename(DirectoryTemporary(),
  "d972_b4_kbmag_bootstrap_metabelian_v2_base.g");;
FileString(D972MBV2Temp,D972MBV2Patched);;
Read(D972MBV2Temp);;
if not IsBound(D972MCV3Reached) or D972MCV3Reached<>true then
  Error("metabelian v2 bootstrap: v3 completion marker missing");
fi;
Print("B4_KBMAG_METABELIAN_V2_BOOTSTRAP_SHIM_PASS target=",D972MBV2Target,
  " target_sha256=",D972MBV2TargetSha," base_sha256=",D972MBV2BaseSha,"\n");
