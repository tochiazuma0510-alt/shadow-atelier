#############################################################################
## R07 compact direct-relator actual positive owner v6. ASCII only.
#############################################################################
if not IsBound(D479Mode) then Error("task479 MODE required"); fi;
if D479Mode<>"PRODUCTION" then Error("task479 production-only mode"); fi;
if not IsBound(D479Task193Receipt) then Error("task479 task193 receipt required"); fi;
if not IsBound(D479Task193Verdict) then Error("task479 task193 verdict required"); fi;
D479InheritedDriver:="search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v3.g";;
D479InheritedDriverBytes:=4233;;
D479InheritedDriverSHA:="b1851ea2835ef752b64b8f04c6489bd9f9630178fadbe8acf38c7fb0aeb2a5d7";;
D479Producer:="search/d972_r07_compact_direct_relator_a5_a6_positive_v4.py";;
D479Checker:="crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v4.py";;
D479ProducerBytes:=1876;; D479ProducerSHA:="0e4f52e3af94d145121c70bf405219276984b73e14d19c3cf6b417480dfa09b9";;
D479CheckerBytes:=2552;; D479CheckerSHA:="a94e8180b0280fac92fbf749591c5985092188a62aab08cda2299e2c22d23eeb";;
D479Receipt:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v6.json";;
D479Verdict:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v6.checker.json";;
D479ProducerLog:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v6.producer.log";;
D479CheckerLog:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v6.checker.log";;
D479Script:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v6.sh";;
D479OK:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v6.ok";;
for D479Path in [D479Receipt,D479Verdict,D479ProducerLog,D479CheckerLog,D479Script,D479OK] do
  if IsExistingFile(D479Path) then Error("task479 stale output ",D479Path); fi;
od;
D479S:=OutputTextFile(D479Script,false);;
if D479S=fail then Error("task479 script open"); fi;
SetPrintFormattingStatus(D479S,false);;
PrintTo(D479S,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D479S,"test \"$(wc -c < ",D479InheritedDriver,")\" = \"",String(D479InheritedDriverBytes),"\"\n");
PrintTo(D479S,"test \"$(sha256sum ",D479InheritedDriver," | awk '{print $1}')\" = \"",D479InheritedDriverSHA,"\"\n");
PrintTo(D479S,"test \"$(wc -c < ",D479Producer,")\" = \"",String(D479ProducerBytes),"\"\n");
PrintTo(D479S,"test \"$(sha256sum ",D479Producer," | awk '{print $1}')\" = \"",D479ProducerSHA,"\"\n");
PrintTo(D479S,"test \"$(wc -c < ",D479Checker,")\" = \"",String(D479CheckerBytes),"\"\n");
PrintTo(D479S,"test \"$(sha256sum ",D479Checker," | awk '{print $1}')\" = \"",D479CheckerSHA,"\"\n");
PrintTo(D479S,"python3 -u -B ",D479Producer," --mode PRODUCTION --task193-receipt ",D479Task193Receipt," --task193-verdict ",D479Task193Verdict," --output ",D479Receipt," --seconds 14400 --rss-bytes 5700000000 > ",D479ProducerLog," 2>&1\n");
PrintTo(D479S,"cat ",D479ProducerLog,"\n");
PrintTo(D479S,"p=$(sed -n 's/^R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V4_PRODUCER_TERMINAL //p' ",D479ProducerLog,")\n");
PrintTo(D479S,"case \"$p\" in R07_ZERO_BASE_A5_A6_MEMBER|UNKNOWN_INCOMPLETE:compact_direct_span_exhausted|UNKNOWN_RESOURCE:*|UNKNOWN_INPUT:*) ;; *) exit 1;; esac\n");
PrintTo(D479S,"if case \"$p\" in R07_ZERO_BASE_A5_A6_MEMBER) true;; *) false;; esac; then\n");
PrintTo(D479S,"  python3 -u -B ",D479Checker," --mode PRODUCTION --task193-receipt ",D479Task193Receipt," --task193-verdict ",D479Task193Verdict," --receipt ",D479Receipt," --output ",D479Verdict," > ",D479CheckerLog," 2>&1\n");
PrintTo(D479S,"  cat ",D479CheckerLog,"\n");
PrintTo(D479S,"  test -s ",D479Verdict,"\n");
PrintTo(D479S,"else\n");
PrintTo(D479S,"  python3 -c \"import json; r=json.load(open('",D479Receipt,"')); assert r.get('resumable') is False and r.get('claims') == {'A5':'NONE','A6_M':False,'A7':'NONE','compatible_lift':'NONE','fake':'NONE','Ihara':'NONE'}\"\n");
PrintTo(D479S,"fi\n");
PrintTo(D479S,"test -s ",D479Receipt," && test -s ",D479ProducerLog,"\n");
PrintTo(D479S,"printf '%s\\n' 'R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V6_DRIVER_COMPLETE' > ",D479OK,"\n");
CloseStream(D479S);;
Exec(Concatenation("bash ",D479Script));;
if not IsExistingFile(D479OK) then Error("task479 missing success marker"); fi;
if StringFile(D479OK) <> "R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V6_DRIVER_COMPLETE\n" then
  Error("task479 bad success marker");
fi;
Print("R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V6_DRIVER_COMPLETE\n");
