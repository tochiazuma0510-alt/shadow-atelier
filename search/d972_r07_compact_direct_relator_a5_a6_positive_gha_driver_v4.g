#############################################################################
## R07 compact direct-relator actual positive owner v4. ASCII only.
#############################################################################
if not IsBound(D474Mode) then Error("task473 MODE required"); fi;
if D474Mode<>"PRODUCTION" then Error("task473 production-only mode"); fi;
if not IsBound(D474Task193Receipt) then Error("task473 task193 receipt required"); fi;
if not IsBound(D474Task193Verdict) then Error("task473 task193 verdict required"); fi;
D474InheritedDriver:="search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v3.g";;
D474InheritedDriverBytes:=6920;;
D474InheritedDriverSHA:="05c438d045431948f4a487e0e264ed15e628cc7f22bc0cccf89fd9661b84431d";;
D474Producer:="search/d972_r07_compact_direct_relator_a5_a6_positive_v4.py";;
D474Checker:="crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v4.py";;
D474ProducerBytes:=1876;; D474ProducerSHA:="0e4f52e3af94d145121c70bf405219276984b73e14d19c3cf6b417480dfa09b9";;
D474CheckerBytes:=2552;; D474CheckerSHA:="a94e8180b0280fac92fbf749591c5985092188a62aab08cda2299e2c22d23eeb";;
D474Receipt:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v4.json";;
D474Verdict:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v4.checker.json";;
D474ProducerLog:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v4.producer.log";;
D474CheckerLog:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v4.checker.log";;
D474Script:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v4.sh";;
D474OK:="ci/out/d972_r07_compact_direct_relator_a5_a6_positive_v4.ok";;
for D474Path in [D474Receipt,D474Verdict,D474ProducerLog,D474CheckerLog,D474Script,D474OK] do
  if IsExistingFile(D474Path) then Error("task473 stale output ",D474Path); fi;
od;
D474S:=OutputTextFile(D474Script,false);;
if D474S=fail then Error("task473 script open"); fi;
SetPrintFormattingStatus(D474S,false);;
PrintTo(D474S,"#!/usr/bin/env bash\nset -euo pipefail\n");
PrintTo(D474S,"test \"$(wc -c < ",D474InheritedDriver,")\" = \"",String(D474InheritedDriverBytes),"\"\n");
PrintTo(D474S,"test \"$(sha256sum ",D474InheritedDriver," | awk '{print $1}')\" = \"",D474InheritedDriverSHA,"\"\n");
PrintTo(D474S,"test \"$(wc -c < ",D474Producer,")\" = \"",String(D474ProducerBytes),"\"\n");
PrintTo(D474S,"test \"$(sha256sum ",D474Producer," | awk '{print $1}')\" = \"",D474ProducerSHA,"\"\n");
PrintTo(D474S,"test \"$(wc -c < ",D474Checker,")\" = \"",String(D474CheckerBytes),"\"\n");
PrintTo(D474S,"test \"$(sha256sum ",D474Checker," | awk '{print $1}')\" = \"",D474CheckerSHA,"\"\n");
PrintTo(D474S,"python3 -u -B ",D474Producer," --mode PRODUCTION --task193-receipt ",D474Task193Receipt," --task193-verdict ",D474Task193Verdict," --output ",D474Receipt," --seconds 14400 --rss-bytes 5700000000 > ",D474ProducerLog," 2>&1\n");
PrintTo(D474S,"cat ",D474ProducerLog,"\n");
PrintTo(D474S,"p=$(sed -n 's/^R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V4_PRODUCER_TERMINAL //p' ",D474ProducerLog,")\n");
PrintTo(D474S,"case \"$p\" in R07_ZERO_BASE_A5_A6_MEMBER|UNKNOWN_INCOMPLETE:compact_direct_span_exhausted|UNKNOWN_RESOURCE:*|UNKNOWN_INPUT:*) ;; *) exit 1;; esac\n");
PrintTo(D474S,"if case \"$p\" in R07_ZERO_BASE_A5_A6_MEMBER) true;; *) false;; esac; then\n");
PrintTo(D474S,"  python3 -u -B ",D474Checker," --mode PRODUCTION --task193-receipt ",D474Task193Receipt," --task193-verdict ",D474Task193Verdict," --receipt ",D474Receipt," --output ",D474Verdict," > ",D474CheckerLog," 2>&1\n");
PrintTo(D474S,"  cat ",D474CheckerLog,"\n");
PrintTo(D474S,"  test -s ",D474Verdict,"\n");
PrintTo(D474S,"else\n");
PrintTo(D474S,"  python3 -c \"import json; r=json.load(open('",D474Receipt,"')); assert r.get('resumable') is False and r.get('claims') == {'A5':'NONE','A6_M':False,'A7':'NONE','compatible_lift':'NONE','fake':'NONE','Ihara':'NONE'}\"\n");
PrintTo(D474S,"fi\n");
PrintTo(D474S,"test -s ",D474Receipt," && test -s ",D474ProducerLog,"\n");
PrintTo(D474S,"printf '%s\\n' 'R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V4_DRIVER_COMPLETE' > ",D474OK,"\n");
CloseStream(D474S);;
Print("R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V4_DRIVER_READY\n");
