#############################################################################
## R07 compact direct-relator actual positive owner v3. ASCII only.
#############################################################################
if not IsBound(D464Mode) then Error("task464 MODE required"); fi;
if D464Mode<>"PRODUCTION" then Error("task464 production-only mode"); fi;
if not IsBound(D464Task193Receipt) then Error("task464 task193 receipt required"); fi;
if not IsBound(D464Task193Verdict) then Error("task464 task193 verdict required"); fi;
D464InheritedDriver:="search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v2.g";;
D464InheritedDriverBytes:=3763;;
D464InheritedDriverSHA:="1f6a5c51e382ffcb063bbb0b150073e6bc499662182a35f58b3b8f32f00e0d88";;
D464Producer:="search/d972_r07_compact_direct_relator_a5_a6_positive_v3.py";;
D464Checker:="crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v3.py";;
D464ProducerBytes:=2018;; D464ProducerSHA:="7a7272eb553d5256bdad2a123ad6cad87b171fb5d23c2e6d81b7702c5842f244";;
D464CheckerBytes:=2629;; D464CheckerSHA:="8b32643fe4169b7b42fc6d144438e26ceaa38ed2d2825e9c61f82a79d4f14a8b";;
D464Receipt:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v3.json";;
D464Verdict:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v3.checker.json";;
D464ProducerLog:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v3.producer.log";;
D464CheckerLog:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v3.checker.log";;
D464Script:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v3.sh";;
D464OK:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v3.ok";;
for D464Path in [D464Receipt,D464Verdict,D464ProducerLog,D464CheckerLog,D464Script,D464OK] do
  if IsExistingFile(D464Path) then Error("task464 stale output ",D464Path); fi;
od;
D464S:=OutputTextFile(D464Script,false);;
if D464S=fail then Error("task464 script open"); fi;
SetPrintFormattingStatus(D464S,false);;
PrintTo(D464S,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D464S,"test \"$(wc -c < ",D464InheritedDriver,")\" = \"",String(D464InheritedDriverBytes),"\"\n");
PrintTo(D464S,"test \"$(sha256sum ",D464InheritedDriver," | awk '{print $1}')\" = \"",D464InheritedDriverSHA,"\"\n");
PrintTo(D464S,"test \"$(wc -c < ",D464Producer,")\" = \"",String(D464ProducerBytes),"\"\n");
PrintTo(D464S,"test \"$(sha256sum ",D464Producer," | awk '{print $1}')\" = \"",D464ProducerSHA,"\"\n");
PrintTo(D464S,"test \"$(wc -c < ",D464Checker,")\" = \"",String(D464CheckerBytes),"\"\n");
PrintTo(D464S,"test \"$(sha256sum ",D464Checker," | awk '{print $1}')\" = \"",D464CheckerSHA,"\"\n");
PrintTo(D464S,"python3 -u -B ",D464Producer," --mode PRODUCTION --task193-receipt ",D464Task193Receipt," --task193-verdict ",D464Task193Verdict," --output ",D464Receipt," --seconds 14400 --rss-bytes 5700000000 > ",D464ProducerLog," 2>&1\n");
PrintTo(D464S,"cat ",D464ProducerLog,"\n");
PrintTo(D464S,"p=$(sed -n 's/^R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3_PRODUCER_TERMINAL //p' ",D464ProducerLog,")\n");
PrintTo(D464S,"case \"$p\" in R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3_MEMBER|UNKNOWN_INCOMPLETE:compact_direct_span_exhausted|UNKNOWN_RESOURCE:*|UNKNOWN_INPUT:*) ;; *) exit 1;; esac\n");
PrintTo(D464S,"if case \"$p\" in R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3_MEMBER) true;; *) false;; esac; then\n");
PrintTo(D464S,"  python3 -u -B ",D464Checker," --mode PRODUCTION --task193-receipt ",D464Task193Receipt," --task193-verdict ",D464Task193Verdict," --receipt ",D464Receipt," --output ",D464Verdict," > ",D464CheckerLog," 2>&1\n");
PrintTo(D464S,"  cat ",D464CheckerLog,"\n");
PrintTo(D464S,"  test -s ",D464Verdict,"\n");
PrintTo(D464S,"else\n");
PrintTo(D464S,"  python3 -c \"import json; r=json.load(open('",D464Receipt,"')); assert r.get('resumable') is False and r.get('claims') == {'A5':'NONE','A6_M':False,'A7':'NONE','compatible_lift':'NONE','fake':'NONE','Ihara':'NONE'}\"\n");
PrintTo(D464S,"fi\n");
PrintTo(D464S,"test -s ",D464Receipt," && test -s ",D464ProducerLog,"\n");
PrintTo(D464S,"printf '%s\\n' 'R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3_DRIVER_COMPLETE' > ",D464OK,"\n");
CloseStream(D464S);;
Print("R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V3_DRIVER_READY\n");
