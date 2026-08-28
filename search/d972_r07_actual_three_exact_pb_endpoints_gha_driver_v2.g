#############################################################################
## R07 task292 serial GHA driver. ASCII only.
#############################################################################
if not IsBound(D292Mode) then Error("task292 MODE required"); fi;
if D292Mode<>"SELFTEST" and D292Mode<>"PRODUCTION" then Error("task292 MODE"); fi;

D292Producer:="search/d972_r07_actual_three_exact_pb_endpoints_v2.py";;
D292Checker:="crosscheck/check_d972_r07_actual_three_exact_pb_endpoints_v2.py";;
D292Driver:="search/d972_r07_actual_three_exact_pb_endpoints_gha_driver_v2.g";;
D292Fixture:="search/certs/d972_r07_actual_three_exact_pb_endpoints_selftest_v2_20260828.json";;
D292Schema:="d972-r07-actual-three-exact-pb-endpoints/v2";;
D292Receipt:="ci/out/d972_r07_actual_three_exact_pb_endpoints_v2.json";;
D292Verdict:="ci/out/d972_r07_actual_three_exact_pb_endpoints_v2.verdict.json";;
D292PLog:="ci/out/d972_r07_actual_three_exact_pb_endpoints_v2.producer.log";;
D292CLog:="ci/out/d972_r07_actual_three_exact_pb_endpoints_v2.checker.log";;
D292Sh:="ci/out/d972_r07_actual_three_exact_pb_endpoints_v2.sh";;
D292OK:="ci/out/d972_r07_actual_three_exact_pb_endpoints_v2.ok";;

D292Pins:=[
 [D292Producer,40044,"c44d2c8e7fdd7dcbf691600ba823445d1ac45695ef173043c723874a409f7208"],
 [D292Checker,46873,"8d7598f376715af16ccec7bae5550f2c5329922b1b36326643a2a4e9e7cf72d8"],
 [D292Fixture,1696,"5583205a500a878460de58e577daec0a2feff612b35742caf31ae0e4e902a9f7"],
 ["search/d972_r07_normalized_exact_common_word_cached_v3.py",193704,"f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37"],
 ["crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py",154009,"dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10"],
 ["search/d972_r07_second_frattini_affine_prefix_compiler_v1.py",37956,"7ec85fe5b359a371e7c7c6b701426c5521d2a9651f560cba0193fa9c34aa2530"],
 ["crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v1.py",33149,"278903c62c8f742cb985f44267f5f428c12dac9c514117f91eb6ae0daea17940"],
 ["search/d972_r07_actual_two_word_endpoint_specializer_v2.py",40556,"a1532740a7343bd8166c17947f6bd95203a4abdaaafd8e0d9607d3cdf202e6fb"],
 ["crosscheck/check_d972_r07_actual_two_word_endpoint_specializer_v2.py",35463,"e49e4ee24b56e35f8c8120bad7579865e497d94f57b2af51664d562f50ffaa44"],
 ["search/d972_r07_seven_context_roof_presentation_v1.py",137169,"6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"],
 ["crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py",157253,"001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"]
];;

D292Read:=function(path)
 local value;
 value:=StringFile(path);
 if value=fail or Length(value)=0 then Error("task292 missing ",path); fi;
 return value;
end;;

D292Pin:=function(row)
 local value;
 value:=D292Read(row[1]);
 if Length(value)<>row[2] or HexSHA256(value)<>row[3] then
  Error("task292 pin drift ",row[1]);
 fi;
end;;

for D292PinRow in D292Pins do D292Pin(D292PinRow); od;
if not IsExistingFile(D292Driver) or D292Schema<>"d972-r07-actual-three-exact-pb-endpoints/v2" then
 Error("task292 driver path/schema identity");
fi;
if IsExistingFile(D292Receipt) or IsExistingFile(D292Verdict) or
   IsExistingFile(D292PLog) or IsExistingFile(D292CLog) or
   IsExistingFile(D292Sh) or IsExistingFile(D292OK) then
 Error("task292 stale output");
fi;

D292S:=OutputTextFile(D292Sh,false);;
SetPrintFormattingStatus(D292S,false);;
PrintTo(D292S,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D292Mode="SELFTEST" then
 PrintTo(D292S,"python3 -u -B ",D292Producer," ",D292Receipt,
   " --selftest --fixture ",D292Fixture," > ",D292PLog," 2>&1\n");
 PrintTo(D292S,"python3 -u -B ",D292Checker," ",D292Receipt,
   " --selftest --fixture ",D292Fixture," --verdict ",D292Verdict,
   " > ",D292CLog," 2>&1\n");
else
 PrintTo(D292S,"python3 -u -B ",D292Producer," ",D292Receipt,
   " > ",D292PLog," 2>&1\n");
 PrintTo(D292S,"python3 -u -B ",D292Checker," ",D292Receipt,
   " --verdict ",D292Verdict," > ",D292CLog," 2>&1\n");
fi;
PrintTo(D292S,"cat ",D292PLog,"\ncat ",D292CLog,"\n");
PrintTo(D292S,"test \"$(grep -c '^D292_PRODUCER_PASS terminal=' ",D292PLog,
  ")\" -eq 1\n");
PrintTo(D292S,"test \"$(grep -c '^D292_CHECKER_PASS terminal=' ",D292CLog,
  ")\" -eq 1\n");
PrintTo(D292S,"pline=$(grep '^D292_PRODUCER_PASS terminal=' ",D292PLog,
  ")\ncline=$(grep '^D292_CHECKER_PASS terminal=' ",D292CLog,")\n");
PrintTo(D292S,"pt=${pline#D292_PRODUCER_PASS terminal=}\nct=${cline#D292_CHECKER_PASS terminal=}\n");
PrintTo(D292S,"test \"$pt\" = \"$ct\"\n");
PrintTo(D292S,"if [[ \"$pt\" == 'R07_THREE_EXACT_PB_ENDPOINTS_ZERO' ]]; then :; ");
PrintTo(D292S,"elif [[ \"$pt\" =~ ^R07_THREE_EXACT_PB_ENDPOINTS_NONZERO\\ block=(H1|H2|P)$ ]]; then :; ");
PrintTo(D292S,"elif [[ \"$pt\" =~ ^UNKNOWN_INPUT:.+$ ]]; then :; ");
PrintTo(D292S,"elif [[ \"$pt\" =~ ^UNKNOWN_RESOURCE:phase=[^:]+:cap=[^:]+:value=[0-9]+:limit=[0-9]+$ ]]; then :; ");
PrintTo(D292S,"else exit 1; fi\n");
if D292Mode="SELFTEST" then
 PrintTo(D292S,"test \"$pt\" = 'R07_THREE_EXACT_PB_ENDPOINTS_ZERO'\n");
fi;
PrintTo(D292S,"test -s ",D292Receipt," -a -s ",D292Verdict,"\n");
PrintTo(D292S,"sentinel='R07_THREE_EXACT_PB_ENDPOINTS_V2_DRIVER_PASS'\n");
PrintTo(D292S,"printf '%s\\n' \"$sentinel\" | tee ",D292OK,"\n");
PrintTo(D292S,"test \"$(grep -Fxc \"$sentinel\" ",D292OK,")\" -eq 1\n");
CloseStream(D292S);;
Exec("bash ci/out/d972_r07_actual_three_exact_pb_endpoints_v2.sh");
if not IsExistingFile(D292OK) then Error("task292 missing completion"); fi;
