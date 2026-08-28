#############################################################################
## R07 task345 serial producer/checker driver. ASCII only.
#############################################################################
if not IsBound(D345Mode) then Error("task345 MODE required"); fi;
if D345Mode<>"SELFTEST" and D345Mode<>"PRODUCTION" and D345Mode<>"RESUME" then Error("task345 MODE"); fi;
D345Producer:="search/d972_r07_word_independent_successor_kernel_v5.py";;
D345Checker:="crosscheck/check_d972_r07_word_independent_successor_kernel_v5.py";;
D345Driver:="search/d972_r07_word_independent_successor_kernel_gha_driver_v5.g";;
D345Fixture:="search/certs/d972_r07_word_independent_successor_kernel_selftest_v5_20260829.json";;
D345Receipt:="ci/out/d972_r07_word_independent_successor_kernel_v5.json";;
D345Verdict:="ci/out/d972_r07_word_independent_successor_kernel_v5.verdict.json";;
D345PCheckpoint:="ci/out/d972_r07_word_independent_successor_kernel_v5.producer.checkpoint.json";;
D345CCheckpoint:="ci/out/d972_r07_word_independent_successor_kernel_v5.checker.checkpoint.json";;
D345PLog:="ci/out/d972_r07_word_independent_successor_kernel_v5.producer.log";;
D345CLog:="ci/out/d972_r07_word_independent_successor_kernel_v5.checker.log";;
D345Sh:="ci/out/d972_r07_word_independent_successor_kernel_v5.sh";;
D345OK:="ci/out/d972_r07_word_independent_successor_kernel_v5.ok";;
D345Input:="ci/in/d972_r07_seven_context_roof_presentation_v1.json";;
D345AuthReceipt:="d972_r07_seven_context_roof_presentation_v1.json";;
D345AuthManifest:="d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json";;
D345AuthProducer:="d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt";;
D345AuthChecker:="d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt";;
D345AuthVerdict:="d972_r07_seven_context_roof_presentation_v1.checker.verdict.json";;
# The driver is deliberately not self-pinned: hashing this file while it
# carries its own hash would create an in-file fixed-point cycle.  Its exact
# bytes/SHA are reported in the Luna reply and are bound by the immutable
# external commit/run owner; the executable inputs remain pinned below.
# The shell timeout has a fixed 120-second transport reserve over the
# program's 14400-second semantic deadline, so a typed terminal can still
# reach the checker instead of being killed at the same instant.
D345Pins:=[
 [D345Producer,218912,"e78537a5e5dcb7b897cf7398bea2f72d467d881c534d1118a9f0e93a99a0e0ac"],
 [D345Checker,258659,"49fead3263aba57a9058b9c0b2ed0f893cf45287ec18e772a0068a6ccd7ab3a5"],
 [D345Fixture,5026,"696386deb6b093abac2748ae6a7adc0c72aa9e9b8b2da8f065da6f75ac5d626f"]];;
D345AuthorityPins:=[
 ["ci/in/d972_r07_seven_context_roof_presentation_v1.json",31017244,"82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5"],
 ["ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json",2722,"cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4"],
 ["ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt",81,"b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090"],
 ["ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt",95,"260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e"],
 ["ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json",150,"ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de"],
 ["search/d972_r07_seven_context_roof_presentation_v1.py",137169,"6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c"],
 ["crosscheck/check_d972_r07_seven_context_roof_presentation_v1.py",157253,"001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1"],
 ["search/d972_r07_seven_context_roof_presentation_gha_driver_v1.g",20541,"6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068"],
 ["search/d972_b345_seedspan_triple4_v1.py",535219,"fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"],
 ["ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json",231570,"3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"],
 ["ci/in/d972_r07_all_seven_extension_section_census_v1.json",13649089,"715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41"],
 ["ci/in/d972_r07_all_seven_extension_section_census_v1.manifest.json",349,"de62e5e55a2e348a3cce297764f7ff4bfedc10ebe2545f22cbc1551f15e1adc1"],
 ["search/d972_r07_all_seven_extension_section_census_v1.py",66109,"878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"],
 ["crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py",84980,"4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"],
 ["search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g",15929,"1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995"],
 ["ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.json",757,"e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5"],
 ["ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.json",2035,"41d2cb72614ce7e2d5b2d7a9000e861414da1c749876b3d51f1ccf2ca63390a8"],
 ["ci/in/d972_r07_all_seven_extension_section_census_crosscheck_v1.recovery.manifest.v2.json",2690,"67dd555f6e0f943d0161ef2f2c8124b4cc31c9167846b45b43fd2001f5fbba3f"]];;
D345Read:=function(path) local value; value:=StringFile(path); if value=fail then Error("task345 missing ",path); fi; return value; end;;
D345Pin:=function(row) local value; if row[2]=0 then Error("task345 unresolved pin ",row[1]); fi; value:=D345Read(row[1]); if Length(value)<>row[2] or HexSHA256(value)<>row[3] then Error("task345 pin drift ",row[1]); fi; end;;
for D345Row in D345AuthorityPins do D345Pin(D345Row); od;
for D345Row in D345Pins do D345Pin(D345Row); od;
D345Owned:=[
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
 "ci/out/d972_r07_word_independent_successor_kernel_v4.json",
 "ci/out/d972_r07_word_independent_successor_kernel_v4.verdict.json",
 "ci/out/d972_r07_word_independent_successor_kernel_v4.sh",
 "ci/out/d972_r07_word_independent_successor_kernel_v4.ok",
 D345Receipt,D345Verdict,D345PCheckpoint,D345CCheckpoint,D345PLog,D345CLog,D345Sh,D345OK];;
D345FreshOwned:=[D345Receipt,D345Verdict,D345PLog,D345CLog,D345Sh,D345OK];;
for D345Path in D345FreshOwned do if IsExistingFile(D345Path) then Error("task345 stale output ",D345Path); fi; od;
D345LegacyOwned:=[
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
 "ci/out/d972_r07_word_independent_successor_kernel_v4.json",
 "ci/out/d972_r07_word_independent_successor_kernel_v4.verdict.json",
 "ci/out/d972_r07_word_independent_successor_kernel_v4.sh",
 "ci/out/d972_r07_word_independent_successor_kernel_v4.ok"];;
for D345Path in D345LegacyOwned do if IsExistingFile(D345Path) then Error("task345 stale legacy output ",D345Path); fi; od;
if D345Mode<>"RESUME" then
 for D345Path in [D345PCheckpoint,D345CCheckpoint] do
  if IsExistingFile(D345Path) then Error("task345 stale checkpoint ",D345Path); fi;
 od;
fi;
D345S:=OutputTextFile(D345Sh,false);; SetPrintFormattingStatus(D345S,false);;
PrintTo(D345S,"#!/usr/bin/env bash\nset -eu\nset -o pipefail\nmkdir -p ci/out\n");
if D345Mode="SELFTEST" then
 PrintTo(D345S,"timeout 14520s python3 -u -B ",D345Producer," --selftest --fixture ",D345Fixture," --input ",D345Input," --output ",D345Receipt," --checkpoint ",D345PCheckpoint," --seconds 14400 --rss-bytes 8000000000 > ",D345PLog," 2>&1\n");
 PrintTo(D345S,"grep -Fxc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_SELFTEST_PASS' ",D345PLog," >/dev/null\n");
 PrintTo(D345S,"timeout 14520s python3 -u -B ",D345Checker," --selftest --fixture ",D345Fixture," --input ",D345Input," --producer ",D345Receipt," --output ",D345Verdict," --checkpoint ",D345CCheckpoint," --seconds 14400 --rss-bytes 8000000000 > ",D345CLog," 2>&1\n");
 PrintTo(D345S,"grep -Fxc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_CHECKER_SELFTEST_PASS' ",D345CLog," >/dev/null\n");
elif D345Mode="PRODUCTION" then
 PrintTo(D345S,"timeout 14520s python3 -u -B ",D345Producer," --input ",D345Input," --output ",D345Receipt," --checkpoint ",D345PCheckpoint," --seconds 14400 --rss-bytes 8000000000",
         " --task198-receipt ci/in/",D345AuthReceipt," --task198-manifest ci/in/",D345AuthManifest,
         " --task198-producer ci/in/",D345AuthProducer," --task198-checker ci/in/",D345AuthChecker,
         " --task198-verdict ci/in/",D345AuthVerdict," > ",D345PLog," 2>&1\n");
 PrintTo(D345S,"D345PLine=$(grep -E '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_TERMINAL (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PASS|UNKNOWN_INPUT|UNKNOWN_RESOURCE)$' ",D345PLog,")\n");
 PrintTo(D345S,"test \"$(grep -Ec '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_TERMINAL ' ",D345PLog,")\" = 1\n");
 PrintTo(D345S,"timeout 14520s python3 -u -B ",D345Checker," --input ",D345Input," --producer ",D345Receipt," --output ",D345Verdict," --checkpoint ",D345CCheckpoint," --seconds 14400 --rss-bytes 8000000000",
         " --task198-receipt ci/in/",D345AuthReceipt," --task198-manifest ci/in/",D345AuthManifest,
         " --task198-producer ci/in/",D345AuthProducer," --task198-checker ci/in/",D345AuthChecker,
         " --task198-verdict ci/in/",D345AuthVerdict," > ",D345CLog," 2>&1\n");
 PrintTo(D345S,"D345CLine=$(grep -E '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_CHECKER_TERMINAL (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PASS|UNKNOWN_INPUT|UNKNOWN_RESOURCE)$' ",D345CLog,")\n");
 PrintTo(D345S,"test \"$(grep -Ec '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_CHECKER_TERMINAL ' ",D345CLog,")\" = 1\n");
 PrintTo(D345S,"D345PStatus=${D345PLine##* }\nD345CStatus=${D345CLine##* }\ntest \"$D345PStatus\" = \"$D345CStatus\"\n");
else
 PrintTo(D345S,"test -s ",D345PCheckpoint,"\ntest -s ",D345CCheckpoint,"\n");
 PrintTo(D345S,"timeout 14520s python3 -u -B ",D345Producer," --input ",D345Input," --output ",D345Receipt," --checkpoint ",D345PCheckpoint," --resume ",D345PCheckpoint," --seconds 14400 --rss-bytes 8000000000",
         " --task198-receipt ci/in/",D345AuthReceipt," --task198-manifest ci/in/",D345AuthManifest,
         " --task198-producer ci/in/",D345AuthProducer," --task198-checker ci/in/",D345AuthChecker,
         " --task198-verdict ci/in/",D345AuthVerdict," > ",D345PLog," 2>&1\n");
 PrintTo(D345S,"D345PLine=$(grep -E '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_TERMINAL (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PASS|UNKNOWN_INPUT|UNKNOWN_RESOURCE)$' ",D345PLog,")\n");
 PrintTo(D345S,"test \"$(grep -Ec '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PRODUCER_TERMINAL ' ",D345PLog,")\" = 1\n");
 PrintTo(D345S,"timeout 14520s python3 -u -B ",D345Checker," --input ",D345Input," --producer ",D345Receipt," --output ",D345Verdict," --checkpoint ",D345CCheckpoint," --resume ",D345CCheckpoint," --seconds 14400 --rss-bytes 8000000000",
         " --task198-receipt ci/in/",D345AuthReceipt," --task198-manifest ci/in/",D345AuthManifest,
         " --task198-producer ci/in/",D345AuthProducer," --task198-checker ci/in/",D345AuthChecker,
         " --task198-verdict ci/in/",D345AuthVerdict," > ",D345CLog," 2>&1\n");
 PrintTo(D345S,"D345CLine=$(grep -E '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_CHECKER_TERMINAL (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_PASS|UNKNOWN_INPUT|UNKNOWN_RESOURCE)$' ",D345CLog,")\n");
 PrintTo(D345S,"test \"$(grep -Ec '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_CHECKER_TERMINAL ' ",D345CLog,")\" = 1\n");
 PrintTo(D345S,"D345PStatus=${D345PLine##* }\nD345CStatus=${D345CLine##* }\ntest \"$D345PStatus\" = \"$D345CStatus\"\n");
fi;
PrintTo(D345S,"test -s ",D345Verdict,"\ngrep -F 'self_digest_sha256' ",D345Verdict," >/dev/null\nprintf 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_OK\\n' > ",D345OK,"\ntest -s ",D345OK,"\n"); CloseStream(D345S);;
Exec("bash ci/out/d972_r07_word_independent_successor_kernel_v5.sh");
if not IsExistingFile(D345OK) then Error("task345 missing completion sentinel"); fi;
Print("R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V5_DRIVER_PASS\n");
