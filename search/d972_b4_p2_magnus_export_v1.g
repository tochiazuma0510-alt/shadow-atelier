#############################################################################
## Export exact U_M signed words for the independent class-2 Magnus probe.
## This file is loaded only by D972_P2_MAGNUS_ONLY after the common P2
## presentation and fullF2->compact roof-word gates have passed.
#############################################################################

P2MagnusJson:=Concatenation(
  "{\"schema\":\"d972-b4-p2-magnus-input/v1\"",
  ",\"relator_count\":158,\"roof_count\":972",
  ",\"all_relators_sha256\":",P2Json(P2RelDigest),
  ",\"target_key_digest\":",P2Json(P2TargetDigest),
  ",\"roof_words_sha256\":",P2Json(P2RoofDigest),
  ",\"p2_input_file_sha256\":",P2Json(P2InputFileSha),
  ",\"rho_words\":",P2Json(P2RhoWords),
  ",\"all_relators\":",P2Json(P2RelWords),
  ",\"target_keys\":",P2Json(P2TargetKeys),
  ",\"roof_words\":",P2Json(P2RoofWords),"}");;
WriteFile("ci/out/d972_b4_p2_magnus_input_v1.json",
  Concatenation(P2MagnusJson,"\n"));;
Print("P2_MAGNUS_INPUT_WRITTEN ci/out/d972_b4_p2_magnus_input_v1.json\n");
