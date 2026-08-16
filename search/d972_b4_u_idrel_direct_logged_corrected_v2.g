#############################################################################
## d972_b4_u_idrel_direct_logged_corrected_v2.g
##
## Bounded direct B4 IdRel lane using the repo-local corrected copy of
## LoggedOnePassKB.  The underlying stage/replay/checker contract is the
## versioned v1 lane; this wrapper changes only the OnePass type-1 formulas
## before v1 constructs U and runs its explicit bounded stages.
##
## No installed GAP package file is edited.  The helper's pinned source SHA
## is checked before it is read, and the helper installs its higher-rank
## method only in this GAP process.
#############################################################################

D972B4CorrectedHelper :=
  "search/d972_b4_idrel_logged_onepass_corrected_v2.g";;
D972B4CorrectedHelperSha :=
  "7c0190cd42dd8dbd63e9551b5934072073e36901feb42f657d5b81187c05bd83";;
D972B4CorrectedHelperText := StringFile(D972B4CorrectedHelper);;
if D972B4CorrectedHelperText=fail or
   HexSHA256(D972B4CorrectedHelperText)<>D972B4CorrectedHelperSha then
  Error("d972 corrected IdRel helper SHA drift");
fi;
Read(D972B4CorrectedHelper);;
D972B4CorrectedVariant := "repo-local-idrel-2.49-type1-f6-corrected-v2";;
Print("B4_IDREL_CORRECTED_V2_HELPER_READY sha=",
  D972B4CorrectedHelperSha,"\n");

## v1 owns the frozen-input gates, stage caps, rule filter, row F6 replay,
## duplicate map, and receipt.  Its LoggedOnePassKB call now dispatches to the
## higher-rank repo-local corrected method installed above.
Read("search/d972_b4_u_idrel_direct_logged_v1.g");;
