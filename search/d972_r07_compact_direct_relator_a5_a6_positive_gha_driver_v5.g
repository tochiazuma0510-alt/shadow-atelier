#############################################################################
## R07 compact direct-relator actual positive owner v5. ASCII only.
#############################################################################
if not IsBound(D475Mode) then Error("task476 MODE required"); fi;
if D475Mode<>"PRODUCTION" then Error("task476 production-only mode"); fi;
if not IsBound(D475Task193Receipt) then Error("task476 task193 receipt required"); fi;
if not IsBound(D475Task193Verdict) then Error("task476 task193 verdict required"); fi;
D475InheritedDriver:="search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v3.g";;
D475InheritedDriverBytes:=4233;;
D475InheritedDriverSHA:="b1851ea2835ef752b64b8f04c6489bd9f9630178fadbe8acf38c7fb0aeb2a5d7";;
D475Producer:="search/d972_r07_compact_direct_relator_a5_a6_positive_v4.py";;
D475Checker:="crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v4.py";;
D475ProducerBytes:=1876;; D475ProducerSHA:="0e4f52e3af94d145121c70bf405219276984b73e14d19c3cf6b417480dfa09b9";;
D475CheckerBytes:=2552;; D475CheckerSHA:="a94e8180b0280fac92fbf749591c5985092188a62aab08cda2299e2c22d23eeb";;
D475Receipt:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v5.json";;
D475Verdict:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v5.checker.json";;
D475ProducerLog:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v5.producer.log";;
D475CheckerLog:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v5.checker.log";;
D475Script:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v5.sh";;
D475OK:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v5.ok";;
for D475Path in [D475Receipt,D475Verdict,D475ProducerLog,D475CheckerLog,D475Script,D475OK] do
  if IsExistingFile(D475Path) then Error("task476 stale output ",D475Path); fi;
od;
D475S:=OutputTextFile(D475Script,false);;
if D475S=fail then Error("task476 script open"); fi;
SetPrintFormattingStatus(D475S,false);;
PrintTo(D475S,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D475S,"test \"$(wc -c < ",D475InheritedDriver,")\" = \"",String(D475InheritedDriverBytes),"\"\n");
PrintTo(D475S,"test \"$(sha256sum ",D475InheritedDriver," | awk '{print $1}')\" = \"",D475InheritedDriverSHA,"\"\n");
PrintTo(D475S,"test \"$(wc -c < ",D475Producer,")\" = \"",String(D475ProducerBytes),"\"\n");
PrintTo(D475S,"test \"$(sha256sum ",D475Producer," | awk '{print $1}')\" = \"",D475ProducerSHA,"\"\n");
PrintTo(D475S,"test \"$(wc -c < ",D475Checker,")\" = \"",String(D475CheckerBytes),"\"\n");
PrintTo(D475S,"test \"$(sha256sum ",D475Checker," | awk '{print $1}')\" = \"",D475CheckerSHA,"\"\n");
PrintTo(D475S,"python3 -u -B ",D475Producer," --mode PRODUCTION --task193-receipt ",D475Task193Receipt," --task193-verdict ",D475Task193Verdict," --output ",D475Receipt," --seconds 14400 --rss-bytes 5700000000 > ",D475ProducerLog," 2>&1\n");
PrintTo(D475S,"cat ",D475ProducerLog,"\n");
PrintTo(D475S,"p=$(sed -n 's/^R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V4_PRODUCER_TERMINAL //p' ",D475ProducerLog,")\n");
PrintTo(D475S,"case \"$p\" in R07_ZERO_BASE_A5_A6_MEMBER|UNKNOWN_INCOMPLETE:compact_direct_span_exhausted|UNKNOWN_RESOURCE:*|UNKNOWN_INPUT:*) ;; *) exit 1;; esac\n");
PrintTo(D475S,"if case \"$p\" in R07_ZERO_BASE_A5_A6_MEMBER) true;; *) false;; esac; then\n");
PrintTo(D475S,"  python3 -u -B ",D475Checker," --mode PRODUCTION --task193-receipt ",D475Task193Receipt," --task193-verdict ",D475Task193Verdict," --receipt ",D475Receipt," --output ",D475Verdict," > ",D475CheckerLog," 2>&1\n");
PrintTo(D475S,"  cat ",D475CheckerLog,"\n");
PrintTo(D475S,"  test -s ",D475Verdict,"\n");
PrintTo(D475S,"else\n");
PrintTo(D475S,"  python3 -c \"import json; r=json.load(open('",D475Receipt,"')); assert r.get('resumable') is False and r.get('claims') == {'A5':'NONE','A6_M':False,'A7':'NONE','compatible_lift':'NONE','fake':'NONE','Ihara':'NONE'}\"\n");
PrintTo(D475S,"fi\n");
PrintTo(D475S,"test -s ",D475Receipt," && test -s ",D475ProducerLog,"\n");
PrintTo(D475S,"printf '%s\\n' 'R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V5_DRIVER_COMPLETE' > ",D475OK,"\n");
CloseStream(D475S);;
Print("R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V5_DRIVER_READY\n");
