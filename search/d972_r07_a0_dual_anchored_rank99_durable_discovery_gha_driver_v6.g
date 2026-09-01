#############################################################################
## Task506 rank99 nonzero-constant literal global-prefix v6 driver. ASCII.
#############################################################################
if not IsBound(D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6_RUN) or
   D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6_RUN<>true then
 Error("task506 external preamble required"); fi;
if not IsBound(D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6_INPUT) then
 D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6_INPUT:=
  "search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json";; fi;
D506Input:=D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6_INPUT;;
D506Producer:="search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.py";;
D506Checker:="crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.py";;
D506Proof:="sol/proof_r07_rank99_tau_free_nonzero_constant_global_prefix_v431.md";;
D506Artifact:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.json";;
D506Checkpoint:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.checkpoint";;
D506Verdict:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.checker.json";;
D506PLog:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.producer.log";;
D506CLog:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.checker.log";;
D506Script:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.sh";;
D506OK:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.ok";;
# Pins are filled by the bounded release freeze after the two source files are
# written; the frozen v5 arithmetic pins remain inside both Python owners.
D506ProducerBytes:=14329;; D506ProducerSHA:="3173c9d99fc5a94713d3dbed1b2c90d4ed3a5723b428838ec0bd50d8aee3d90c";;
D506CheckerBytes:=12191;; D506CheckerSHA:="2f579f818b7fff01a3af4764393ac2f2a3190767f0671e6d407c7fe2517e91da";;
D506ProofBytes:=9592;; D506ProofSHA:="7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4";;
D506Safe:=function(path)
 local tail,allowed,i;
 if not IsString(path) or Length(path)<19 or path{[1..13]}<>"search/certs/" then return false; fi;
 if PositionSublist(path,"..")<>fail then return false; fi;
 tail:=path{[14..Length(path)]};
 if Length(tail)<6 or tail{[Length(tail)-4..Length(tail)]}<>".json" then return false; fi;
 allowed:="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-";
 if Position(tail,"/")<>fail or Position(tail,"\\")<>fail then return false; fi;
 for i in [1..Length(tail)] do if Position(allowed,tail[i])=fail then return false; fi; od;
 return true;
end;;
if not D506Safe(D506Input) then Error("task506 unsafe resume input"); fi;
if IsExistingFile(D506Artifact) or IsExistingFile(D506Checkpoint) or
   IsExistingFile(D506Verdict) or IsExistingFile(D506PLog) or
   IsExistingFile(D506CLog) or IsExistingFile(D506Script) or IsExistingFile(D506OK) then
 Error("task506 stale output"); fi;
if not IsExistingFile(D506Input) then Error("task506 input missing"); fi;
if D506ProducerBytes<=0 or D506CheckerBytes<=0 or Length(D506ProducerSHA)<>64 or
   Length(D506CheckerSHA)<>64 then Error("task506 source pins unset"); fi;
if not (14040<14220 and 14220<14400 and 4200000000<4500000000 and
        4500000000<5120000000) then Error("task506 envelope"); fi;
if not IsDirectoryPath("ci/out") then if CreateDir("ci/out")=fail then Error("task506 ci/out"); fi; fi;
D506S:=OutputTextFile(D506Script,false);; if D506S=fail then Error("task506 script"); fi;
SetPrintFormattingStatus(D506S,false);
PrintTo(D506S,"#!/usr/bin/env bash\nset -euo pipefail\numask 077\n");
PrintTo(D506S,"test -f '",D506Input,"'\n");
PrintTo(D506S,"test ! -L '",D506Input,"'\n");
PrintTo(D506S,"test 14040 -lt 14220 && test 14220 -lt 14400\n");
PrintTo(D506S,"test 4200000000 -lt 4500000000 && test 4500000000 -lt 5120000000\n");
PrintTo(D506S,"ulimit -v 5000000\n");
PrintTo(D506S,"timeout --foreground --kill-after=30s 14400s python3 -u -B ",D506Producer,
 " --resume '",D506Input,"' --output '",D506Artifact,"' --checkpoint '",D506Checkpoint,
 "' --search-seconds 14040 --hard-seconds 14220 --external-seconds 14400",
 " --search-rss-bytes 4200000000 --hard-rss-bytes 4500000000 --hard-vm-bytes 5120000000",
 " --max-rises 64 --batch-cap 16 2>&1 | tee '",D506PLog,"'\n");
PrintTo(D506S,"if grep -Eq '^R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6 status=UNKNOWN_RESOURCE$' '",D506PLog,"'; then\n");
PrintTo(D506S," grep -Eq '\"candidate_marker\":\"R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6_RESOURCE_CANDIDATE\"' '",D506Artifact,"'\n");
PrintTo(D506S," exit 0\nfi\n");
PrintTo(D506S,"grep -Eq '^R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6 status=COMMON_CANDIDATE$' '",D506PLog,"'\n");
PrintTo(D506S,"timeout --foreground --kill-after=30s 14400s python3 -u -B ",D506Checker,
 " '",D506Artifact,"' --verdict '",D506Verdict,"' 2>&1 | tee '",D506CLog,"'\n");
PrintTo(D506S,"test -s '",D506Verdict,"'\n");
PrintTo(D506S,"printf '%s\\n' 'D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6_COMPLETE' > '",D506OK,"'\n");
CloseStream(D506S);
Exec(Concatenation("chmod 700 ",D506Script));
Exec(Concatenation("bash -n ",D506Script));
Print("TASK506 driver generated; production is intentionally not started.\n");
