#############################################################################
## R07 task336 serial producer/checker driver. ASCII only.
#############################################################################
if not IsBound(D336Mode) then Error("task336 MODE required"); fi;
if D336Mode<>"SELFTEST" and D336Mode<>"PRODUCTION" then Error("task336 MODE"); fi;
D336Producer:="search/d972_r07_word_independent_successor_kernel_v4.py";;
D336Checker:="crosscheck/check_d972_r07_word_independent_successor_kernel_v4.py";;
D336Fixture:="search/certs/d972_r07_word_independent_successor_kernel_selftest_v4_20260829.json";;
D336Receipt:="ci/out/d972_r07_word_independent_successor_kernel_v4.json";;
D336Verdict:="ci/out/d972_r07_word_independent_successor_kernel_v4.verdict.json";;
D336PLog:="ci/out/d972_r07_word_independent_successor_kernel_v4.producer.log";;
D336CLog:="ci/out/d972_r07_word_independent_successor_kernel_v4.checker.log";;
D336Sh:="ci/out/d972_r07_word_independent_successor_kernel_v4.sh";;
D336OK:="ci/out/d972_r07_word_independent_successor_kernel_v4.ok";;
D336AuthReceipt:="d972_r07_seven_context_roof_presentation_v1.json";;
D336AuthManifest:="d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json";;
D336AuthProducer:="d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt";;
D336AuthChecker:="d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt";;
D336AuthVerdict:="d972_r07_seven_context_roof_presentation_v1.checker.verdict.json";;
D336Pins:=[[D336Producer,98454,"d895996da8c6014327028d5bd5c7076f27aa481f2d68511ac2cdbd55b1adaa6c"],[D336Checker,49223,"e006cfef8f6c650298f8ceaab0522c9459d5868d6d25939d575177eee60fc3eb"],[D336Fixture,593,"2cbf25f57c9b28c9b8b212b5ac6b56c10fc570ea33a75f1e3eb5adaa50c38c16"]];;
D336AuthorityPins:=[
 ["ci/in/d972_r07_seven_context_roof_presentation_v1.json",31017244,"82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"],
 ["ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",2722,"cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"],
 ["ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",81,"b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"],
 ["ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",95,"260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e"],
 ["ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",150,"ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"],
 ["search/d972_b345_seedspan_triple4_v1.py",535219,"fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"],
 ["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json",231570,"3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"],
 ["search/d972_r07_all_seven_extension_section_census_v1.py",66109,"878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"]];;
D336Read:=function(path) local value; value:=StringFile(path); if value=fail then Error("task336 missing ",path); fi; return value; end;;
D336Pin:=function(row) local value; if row[2]=0 then Error("task336 unresolved pin ",row[1]); fi; value:=D336Read(row[1]); if Length(value)<>row[2] or HexSHA256(value)<>row[3] then Error("task336 pin drift ",row[1]); fi; end;;
for D336Row in D336AuthorityPins do D336Pin(D336Row); od;
# The producer, checker and fixture pins are exact pre-dispatch identities.
for D336Row in D336Pins do D336Pin(D336Row); od;
D336Owned:=[
 "ci/out/d972_r07_word_independent_successor_kernel_v1.json",
 "ci/out/d972_r07_word_independent_successor_kernel_v1.verdict.json",
 "ci/out/d972_r07_word_independent_successor_kernel_v1.sh",
 "ci/out/d972_r07_word_independent_successor_kernel_v1.ok",
 "ci/out/d972_r07_word_independent_successor_kernel_v2.json",
 "ci/out/d972_r07_word_independent_successor_kernel_v2.verdict.json",
 "ci/out/d972_r07_word_independent_successor_kernel_v2.sh",
 "ci/out/d972_r07_word_independent_successor_kernel_v2.ok",
 "ci/out/d972_r07_word_independent_successor_kernel_v3.json",
 "ci/out/d972_r07_word_independent_successor_kernel_v3.verdict.json",
 "ci/out/d972_r07_word_independent_successor_kernel_v3.sh",
 "ci/out/d972_r07_word_independent_successor_kernel_v3.ok",
 D336Receipt,D336Verdict,D336PLog,D336CLog,D336Sh,D336OK];;
for D336Path in D336Owned do if IsExistingFile(D336Path) then Error("task336 stale output ",D336Path); fi; od;
D336S:=OutputTextFile(D336Sh,false);; SetPrintFormattingStatus(D336S,false);;
PrintTo(D336S,"#!/usr/bin/env bash\nset -eu\nset -o pipefail\nmkdir -p ci/out\n");
if D336Mode="SELFTEST" then
  PrintTo(D336S,"timeout 14400s python3 -u -B ",D336Producer," --selftest --fixture ",D336Fixture," --output ",D336Receipt," > ",D336PLog," 2>&1\n");
  PrintTo(D336S,"grep -Fxc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PRODUCER_SELFTEST_PASS' ",D336PLog," >/dev/null\n");
  PrintTo(D336S,"timeout 14400s python3 -u -B ",D336Checker," --selftest --fixture ",D336Fixture," --producer ",D336Receipt," --output ",D336Verdict," > ",D336CLog," 2>&1\n");
  PrintTo(D336S,"grep -Fxc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_CHECKER_SELFTEST_PASS' ",D336CLog," >/dev/null\n");
else
  PrintTo(D336S,"timeout 14400s python3 -u -B ",D336Producer," --output ",D336Receipt,
          " --task198-receipt ci/in/",D336AuthReceipt," --task198-manifest ci/in/",D336AuthManifest,
          " --task198-producer ci/in/",D336AuthProducer," --task198-checker ci/in/",D336AuthChecker,
          " --task198-verdict ci/in/",D336AuthVerdict," > ",D336PLog," 2>&1\n");
  PrintTo(D336S,"D336PLine=$(grep -E '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PRODUCER_TERMINAL (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PASS|UNKNOWN_INPUT|UNKNOWN_RESOURCE)$' ",D336PLog,")\n");
  PrintTo(D336S,"test \"$(grep -Ec '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PRODUCER_TERMINAL ' ",D336PLog,")\" = 1\n");
  PrintTo(D336S,"timeout 14400s python3 -u -B ",D336Checker," --producer ",D336Receipt," --output ",D336Verdict,
          " --task198-receipt ci/in/",D336AuthReceipt," --task198-manifest ci/in/",D336AuthManifest,
          " --task198-producer ci/in/",D336AuthProducer," --task198-checker ci/in/",D336AuthChecker,
          " --task198-verdict ci/in/",D336AuthVerdict," > ",D336CLog," 2>&1\n");
  PrintTo(D336S,"D336CLine=$(grep -E '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_CHECKER_TERMINAL (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_PASS|UNKNOWN_INPUT|UNKNOWN_RESOURCE)$' ",D336CLog,")\n");
  PrintTo(D336S,"test \"$(grep -Ec '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_CHECKER_TERMINAL ' ",D336CLog,")\" = 1\n");
  PrintTo(D336S,"test \"${D336PLine##* }\" = \"${D336CLine##* }\"\n");
fi;
PrintTo(D336S,"test -s ",D336Verdict,"\ngrep -F 'self_digest_sha256' ",D336Verdict," >/dev/null\nprintf 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_OK\\n' > ",D336OK,"\ntest -s ",D336OK,"\n"); CloseStream(D336S);;
Exec("bash ci/out/d972_r07_word_independent_successor_kernel_v4.sh");
if not IsExistingFile(D336OK) then Error("task336 missing completion sentinel"); fi;
Print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V4_DRIVER_PASS\n");
