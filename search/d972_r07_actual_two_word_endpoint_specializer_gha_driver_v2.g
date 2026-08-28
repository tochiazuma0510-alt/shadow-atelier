#############################################################################
## Task226/229 serial fail-closed driver.  The parent invokes this through gap.ps1.
#############################################################################
D226ModeVariable:="D972_R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_MODE";;
if not IsBound(D972_R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_MODE) then Error("task226: supply quoted mode"); fi;
D226Mode:=D972_R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_MODE;;
if not IsString(D226Mode) or not D226Mode in ["SELFTEST","PRODUCTION"] then Error("task226: mode"); fi;
D226P:="search/d972_r07_actual_two_word_endpoint_specializer_v2.py";;
D226C:="crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py";;
D226F:="search/certs/d972_r07_actual_two_word_endpoint_specializer_selftest_v2_20260828.json";;
D226192:="ci/in/d972_r07_normalized_exact_common_word_cached_v3.json";;
D226198:="ci/in/d972_r07_seven_context_roof_presentation_v1.json";;
D226192A:="ci/in/d972_r07_normalized_exact_common_word_cached_v3.attestation";;
D226198A:="ci/in/d972_r07_seven_context_roof_presentation_v1.attestation";;
D226R:="ci/out/d972_r07_actual_two_word_endpoint_specializer_v2.json";;
D226V:="ci/out/d972_r07_actual_two_word_endpoint_specializer_v2.verdict";;
D226PL:="ci/out/d972_r07_actual_two_word_endpoint_specializer_v2.producer.log";;
D226CL:="ci/out/d972_r07_actual_two_word_endpoint_specializer_v2.checker.log";;
D226S:="ci/out/d972_r07_actual_two_word_endpoint_specializer_v2.sh";;
D226OK:="ci/out/d972_r07_actual_two_word_endpoint_specializer_v2.ok";;
D226InputBytes:=2100000000;;
D226PBytes:=40556;; D226PSha:="a1532740a7343bd8166c17947f6bd95203a4abdaaafd8e0d9607d3cdf202e6fb";;
D226CBytes:=35436;; D226CSha:="b81de8d7701995c5022dc2e97099599b18dafa6030233f29c37e60dfb70084eb";;
D226FBytes:=1187;; D226FSha:="91c62b70b3275e9e3bee9689bd677049adc172cb0519a2ccf2808d17d6cabef3";;
D226Selftest:="R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_SELFTEST_PASS";;
D226Complete:="R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_COMPLETE";;
D226UnknownInput:="UNKNOWN_INPUT";;
D226UnknownResource:="UNKNOWN_RESOURCE";;
for D226Path in [D226R,D226V,D226PL,D226CL,D226S,D226OK] do
 if IsExistingFile(D226Path) then Error("task226: stale output ",D226Path); fi;
od;
if not IsExistingFile(D226P) or not IsExistingFile(D226C) or not IsExistingFile(D226F) then Error("task226: missing source"); fi;
if not IsDirectoryPath("ci/out") then CreateDir("ci/out"); fi;
D226Stream:=OutputTextFile(D226S,false);; SetPrintFormattingStatus(D226Stream,false);
PrintTo(D226Stream,"set -eu\n");
PrintTo(D226Stream,"test \"$(wc -c < ",D226P,")\" = '",D226PBytes,"'\n");
PrintTo(D226Stream,"test \"$(sha256sum ",D226P," | cut -d' ' -f1)\" = '",D226PSha,"'\n");
PrintTo(D226Stream,"test \"$(wc -c < ",D226C,")\" = '",D226CBytes,"'\n");
PrintTo(D226Stream,"test \"$(sha256sum ",D226C," | cut -d' ' -f1)\" = '",D226CSha,"'\n");
PrintTo(D226Stream,"test \"$(wc -c < ",D226F,")\" = '",D226FBytes,"'\n");
PrintTo(D226Stream,"test \"$(sha256sum ",D226F," | cut -d' ' -f1)\" = '",D226FSha,"'\n");
PrintTo(D226Stream,"printf 'D226_GHA_ESTIMATE input_bytes=2100000000 wall_seconds=21600 rss_bytes=6442450944\\n'\n");
if D226Mode="SELFTEST" then
 PrintTo(D226Stream,"python3 -u -B ",D226P," --selftest --fixture ",D226F," --output ",D226R," > ",D226PL," 2>&1 || { cat ",D226PL,"; exit 1; }\n");
 PrintTo(D226Stream,"grep -Fxc 'D226_PRODUCER_TERMINAL ",D226Selftest,"' ",D226PL," | grep -qx 1\n");
 PrintTo(D226Stream,"python3 -u -B ",D226C," ",D226R," --selftest --fixture ",D226F," --verdict ",D226V," > ",D226CL," 2>&1 || { cat ",D226CL,"; exit 1; }\n");
 PrintTo(D226Stream,"grep -Fxc 'D226_CHECKER_PASS terminal=",D226Selftest,"' ",D226CL," | grep -qx 1\n");
else
 PrintTo(D226Stream,"python3 -u -B ",D226P," --task192 ",D226192," --task198 ",D226198," --task192-attestation ",D226192A," --task198-attestation ",D226198A," --output ",D226R," > ",D226PL," 2>&1 || { cat ",D226PL,"; exit 1; }\n");
 PrintTo(D226Stream,"grep -Ec '^D226_PRODUCER_TERMINAL (",D226UnknownInput,"|",D226UnknownResource,"|",D226Complete,")$' ",D226PL," | grep -qx 1\n");
 PrintTo(D226Stream,"python3 -u -B ",D226C," ",D226R," --task192 ",D226192," --task198 ",D226198," --task192-attestation ",D226192A," --task198-attestation ",D226198A," --verdict ",D226V," > ",D226CL," 2>&1 || { cat ",D226CL,"; exit 1; }\n");
 PrintTo(D226Stream,"grep -Ecx 'D226_CHECKER_PASS terminal=(",D226UnknownInput,"|",D226UnknownResource,"|",D226Complete,")' ",D226CL," | grep -qx 1\n");
 PrintTo(D226Stream,"p=$(sed -n 's/^D226_PRODUCER_TERMINAL //p' ",D226PL," | head -n 1)\n");
 PrintTo(D226Stream,"c=$(sed -n 's/^D226_CHECKER_PASS terminal=//p' ",D226CL," | head -n 1 | cut -d' ' -f1)\n");
 PrintTo(D226Stream,"test \"$p\" = \"$c\"\n");
fi;
PrintTo(D226Stream,"test -s ",D226R,"\n");
PrintTo(D226Stream,"printf '%s' 'R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_SENTINEL' > ",D226OK,"\n");
CloseStream(D226Stream);; Exec(Concatenation("bash ",D226S));
if StringFile(D226OK)<>"R07_ACTUAL_TWO_WORD_ENDPOINT_SPECIALIZER_V2_SENTINEL" then Error("task226: sentinel"); fi;
Print("D226_DRIVER_PASS mode=",D226Mode,"\n");
