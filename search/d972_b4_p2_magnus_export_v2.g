#############################################################################
## Export the canonical-rho exact U_M input for bounded independent probes.
## Loaded only after the common P2 presentation, word/key, and rho gates pass.
#############################################################################

P2MagnusJson:=Concatenation(
  "{\"schema\":\"d972-b4-p2-magnus-input/v2\"",
  ",\"relator_count\":158,\"roof_count\":972",
  ",\"all_relators_sha256\":",P2Json(P2RelDigest),
  ",\"target_key_digest\":",P2Json(P2TargetDigest),
  ",\"roof_words_sha256\":",P2Json(P2RoofDigest),
  ",\"p2_input_file_sha256\":",P2Json(P2InputFileSha),
  ",\"rho_words_source\":\"universal_v2_canonical\"",
  ",\"rho_words\":",P2Json(P2RhoWords),
  ",\"all_relators\":",P2Json(P2RelWords),
  ",\"target_keys\":",P2Json(P2TargetKeys),
  ",\"roof_words\":",P2Json(P2RoofWords),"}");;
WriteFile("ci/out/d972_b4_p2_magnus_input_v2.json",
  Concatenation(P2MagnusJson,"\n"));;
Print("P2_MAGNUS_INPUT_WRITTEN ci/out/d972_b4_p2_magnus_input_v2.json\n");
