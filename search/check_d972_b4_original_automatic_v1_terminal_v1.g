#############################################################################
## Versioned terminal replay wrapper for the frozen v1 direct receipt.
## The replay body is the independent v2 implementation; legacy mode accepts
## only the exact v1 defaults and still regenerates multipliers and GpAxioms.
#############################################################################

D972_B4_ORIGINAL_REPLAY_V2_RECEIPT:="ci/out/d972_b4_original_automatic_v1.json";;
D972_B4_ORIGINAL_REPLAY_V2_SOURCE:="search/certs/d972_b4_p2_magnus_input_v2_20260816.json";;
D972_B4_ORIGINAL_REPLAY_V2_WORDS:="search/certs/d972_b4_word_key_artifact_v1_20260816.json";;
D972_B4_ORIGINAL_REPLAY_V2_OUTPUT:="ci/out/d972_b4_original_automatic_v1_terminal_replay.json";;
D972_B4_ORIGINAL_REPLAY_V2_LARGE:=true;;
D972_B4_ORIGINAL_REPLAY_V2_FILESTORE:=true;;
D972_B4_ORIGINAL_REPLAY_V2_DIFF1:=false;;
D972_B4_ORIGINAL_REPLAY_V2_COMPUTE_SIZE:=true;;
D972_B4_ORIGINAL_REPLAY_V2_MAXEQNS:=250000;;
D972_B4_ORIGINAL_REPLAY_V2_MAXSTATES:=250000;;
D972_B4_ORIGINAL_REPLAY_V2_MAXWDIFFS:=250000;;
D972_B4_ORIGINAL_REPLAY_V2_MAXSTOREDLEN:=[4000,4000];;
D972_B4_ORIGINAL_REPLAY_V2_POST_REPLAY:=true;;
Read("search/check_d972_b4_original_automatic_replay_v2.g");;
if StringFile(D972_B4_ORIGINAL_REPLAY_V2_OUTPUT)=fail then
  Error("ORIGINAL v1 terminal wrapper: replay receipt missing");
fi;
Print("B4_ORIGINAL_AUTOMATIC_V1_TERMINAL_REPLAY_FINAL_MARKER output=",
  D972_B4_ORIGINAL_REPLAY_V2_OUTPUT,"\n");
