#############################################################################
## Numeric, quote-free precheck selftest for direct AutomaticStructure v2.
## No AutomaticStructure call is made: canonical 158/972 gates and the
## complete typed configuration receipt are exercised only.
#############################################################################

D972_B4_ORIGINAL_AUTOMATIC_V2_LARGE:=true;;
D972_B4_ORIGINAL_AUTOMATIC_V2_FILESTORE:=true;;
D972_B4_ORIGINAL_AUTOMATIC_V2_DIFF1:=true;;
D972_B4_ORIGINAL_AUTOMATIC_V2_COMPUTE_SIZE:=false;;
D972_B4_ORIGINAL_AUTOMATIC_V2_MAXEQNS:=123;;
D972_B4_ORIGINAL_AUTOMATIC_V2_MAXSTATES:=234;;
D972_B4_ORIGINAL_AUTOMATIC_V2_MAXWDIFFS:=345;;
D972_B4_ORIGINAL_AUTOMATIC_V2_MAXSTOREDLEN:=[456,567];;
D972_B4_ORIGINAL_AUTOMATIC_V2_POST_REPLAY:=false;;
D972_B4_ORIGINAL_AUTOMATIC_PRECHECK:=1;;
D972_B4_ORIGINAL_AUTOMATIC_SELFTEST:=1;;
D972_B4_ORIGINAL_AUTOMATIC_OUTPUT:=Filename(DirectoryTemporary(),
  "d972_b4_original_automatic_v2_selftest.json");;
Read("search/d972_b4_original_automatic_v2.g");;
if not IsBound(D972OA2Settings) then Error("ORIGINAL v2 selftest: settings missing"); fi;
if not IsBound(D972OAOutput) or StringFile(D972OAOutput)=fail then
  Error("ORIGINAL v2 selftest: receipt missing");
fi;
## Parse both independent replay entry points without executing either heavy
## body.  This catches Read-context syntax regressions even in precheck mode.
D972OA2ReplaySyntax:=ReadAsFunction("search/check_d972_b4_original_automatic_replay_v2.g");;
D972OA2LegacySyntax:=ReadAsFunction("search/check_d972_b4_original_automatic_v1_terminal_v1.g");;
if D972OA2ReplaySyntax=fail or D972OA2LegacySyntax=fail then
  Error("ORIGINAL v2 selftest: replay syntax parse failed");
fi;
Print("B4_ORIGINAL_AUTOMATIC_V2_REPLAY_SYNTAX_PASS legacy=true\n");
Print("B4_ORIGINAL_AUTOMATIC_V2_SELFTEST_FINAL_MARKER diff1=true post_replay=false\n");
