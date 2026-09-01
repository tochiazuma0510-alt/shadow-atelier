#############################################################################
## R07 compact direct-relator actual positive owner. ASCII only.
#############################################################################
if not IsBound(D462Mode) then Error("task462 MODE required"); fi;
if D462Mode<>"PRODUCTION" then Error("task462 production-only mode"); fi;
if not IsBound(D462Task193Receipt) then Error("task462 task193 receipt required"); fi;
if not IsBound(D462Task193Verdict) then Error("task462 task193 verdict required"); fi;
D462Producer:="search/d972_r07_compact_direct_relator_a5_a6_positive_v2.py";;
D462Checker:="crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v2.py";;
D462ProducerBytes:=7707;; D462ProducerSHA:="47cc53c0b59cbca0981983373d30604cbffd874cfa01d2d2adef599e505a21d3";;
D462CheckerBytes:=7720;; D462CheckerSHA:="535c7b8aa0983748204d0e381d367d3398380ea3097cd48ef374dfc3daf38c67";;
D462Receipt:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v2.json";;
D462Verdict:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v2.checker.json";;
D462ProducerLog:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v2.producer.log";;
D462CheckerLog:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v2.checker.log";;
D462Script:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v2.sh";;
D462OK:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v2.ok";;
for D462Path in [D462Receipt,D462Verdict,D462ProducerLog,D462CheckerLog,D462Script,D462OK] do
  if IsExistingFile(D462Path) then Error("task462 stale output ",D462Path); fi;
od;
D462S:=OutputTextFile(D462Script,false);;
if D462S=fail then Error("task462 script open"); fi;
SetPrintFormattingStatus(D462S,false);;
PrintTo(D462S,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D462S,"test \"$(wc -c < ",D462Producer,")\" = \"",String(D462ProducerBytes),"\"\n");
PrintTo(D462S,"test \"$(sha256sum ",D462Producer," | awk '{print $1}')\" = \"",D462ProducerSHA,"\"\n");
PrintTo(D462S,"test \"$(wc -c < ",D462Checker,")\" = \"",String(D462CheckerBytes),"\"\n");
PrintTo(D462S,"test \"$(sha256sum ",D462Checker," | awk '{print $1}')\" = \"",D462CheckerSHA,"\"\n");
PrintTo(D462S,"python3 -u -B ",D462Producer," --mode PRODUCTION --task193-receipt ",D462Task193Receipt," --task193-verdict ",D462Task193Verdict," --output ",D462Receipt," --seconds 14400 --rss-bytes 5700000000 > ",D462ProducerLog," 2>&1\n");
PrintTo(D462S,"cat ",D462ProducerLog,"\n");
PrintTo(D462S,"p=$(sed -n 's/^R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V2_PRODUCER_TERMINAL //p' ",D462ProducerLog,")\n");
PrintTo(D462S,"case \"$p\" in R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V2_MEMBER|UNKNOWN_INCOMPLETE:compact_direct_span_exhausted|UNKNOWN_RESOURCE:*|UNKNOWN_INPUT:*) ;; *) exit 1;; esac\n");
PrintTo(D462S,"if case \"$p\" in R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V2_MEMBER) true;; *) false;; esac; then\n");
PrintTo(D462S,"  python3 -u -B ",D462Checker," --mode PRODUCTION --task193-receipt ",D462Task193Receipt," --task193-verdict ",D462Task193Verdict," --receipt ",D462Receipt," --output ",D462Verdict," > ",D462CheckerLog," 2>&1\n");
PrintTo(D462S,"  cat ",D462CheckerLog,"\n");
PrintTo(D462S,"  test -s ",D462Verdict,"\n");
PrintTo(D462S,"else\n");
PrintTo(D462S,"  grep -q '\"A5\":\"NONE\"' ",D462Receipt," || grep -q '\"A5\": \"NONE\"' ",D462Receipt,"\n");
PrintTo(D462S,"  grep -q '\"A6_M\":false' ",D462Receipt," || grep -q '\"A6_M\": false' ",D462Receipt,"\n");
PrintTo(D462S,"fi\n");
PrintTo(D462S,"test -s ",D462Receipt," && test -s ",D462ProducerLog,"\n");
PrintTo(D462S,"printf '%s\\n' 'R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V2_DRIVER_COMPLETE' > ",D462OK,"\n");
CloseStream(D462S);;
Print("R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V2_DRIVER_READY\n");
