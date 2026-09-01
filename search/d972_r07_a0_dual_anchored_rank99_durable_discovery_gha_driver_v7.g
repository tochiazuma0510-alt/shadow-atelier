#############################################################################
## Task509 v7 checker/driver boundary repair. ASCII only.
#############################################################################
if not IsBound(D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_RUN) or
   D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_RUN<>true then
 Error("task509 external preamble required"); fi;
if not IsBound(D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_INPUT) then
 D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_INPUT:=
  "search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json";; fi;
D509Input:=D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_INPUT;;
D509Producer:="search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py";;
D509Checker:="crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py";;
D509Proof:="sol/proof_r07_rank99_tau_free_nonzero_constant_global_prefix_v431.md";;
D509Artifact:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.json";;
D509Checkpoint:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.checkpoint";;
D509Verdict:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.checker.json";;
D509PLog:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.producer.log";;
D509CLog:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.checker.log";;
D509Script:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.sh";;
D509OK:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.ok";;
D509ProducerBytes:=4911;; D509ProducerSHA:="a66526af4b4f86019b1a4a9283212b9782f5793a21c518a93f04b9925e6bee22";;
D509CheckerBytes:=9067;; D509CheckerSHA:="8de4f573a8a00da451c9518bbc87eb77c1c8cebfb2477ce38efb51e0e01c14f8";;
D509ProofBytes:=9592;; D509ProofSHA:="7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4";;
D509ResourceSentinel:="D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_RESOURCE\n";;
D509CompleteSentinel:="D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_COMPLETE\n";;
D509C99:="search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json";;
D509C99Bytes:=173082;; D509C99SHA:="bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358";;
D509R51:="search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json";;
D509R51Bytes:=10934;; D509R51SHA:="a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4";;
D509T451P:="search/d972_r07_a0_dual_anchored_active_batch_v1.py";;
D509T451PBytes:=13834;; D509T451PSHA:="ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b";;
D509T451C:="crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py";;
D509T451CBytes:=14442;; D509T451CSHA:="1d1080cd3e130d987316feefd820215f495cd6320aa5eca764fd2f8997f0c424";;
D509P424:="sol/proof_r07_rank99_actual_owner_transform_v424.md";;
D509P424Bytes:=7009;; D509P424SHA:="f2e2103f214e6d7c15f5d1c2bc84cd100cd37a69634c381793a42a20e8bad2d9";;
D509P426:="sol/proof_r07_rank99_cached_discovery_chain_v426.md";;
D509P426Bytes:=9165;; D509P426SHA:="5c3176011ea64235196587ed19720ad5d5a5c542c2896e46fe33ef3df3a3977a";;
D509P427:="sol/proof_r07_deadline_flush_short_batch_v427.md";;
D509P427Bytes:=6602;; D509P427SHA:="b958a164dfc78c77596876227b31a39467e077c9666d4a7be9033a58ee4c0ec5";;
D509Safe:=function(path)
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
if not D509Safe(D509Input) then Error("task509 unsafe resume input"); fi;
if IsExistingFile(D509Artifact) or IsExistingFile(D509Checkpoint) or
   IsExistingFile(D509Verdict) or IsExistingFile(D509PLog) or
   IsExistingFile(D509CLog) or IsExistingFile(D509Script) or IsExistingFile(D509OK) then
 Error("task509 stale output"); fi;
if not IsExistingFile(D509Input) then Error("task509 input missing"); fi;
if D509ProducerBytes<=0 or D509CheckerBytes<=0 or Length(D509ProducerSHA)<>64 or
   Length(D509CheckerSHA)<>64 or D509ProofBytes<>9592 or Length(D509ProofSHA)<>64 then
 Error("task509 source pins unset"); fi;
if not (14040<14220 and 14220<14400 and 4200000000<4500000000 and
        4500000000<5120000000) then Error("task509 envelope"); fi;
if not IsDirectoryPath("ci/out") then if CreateDir("ci/out")=fail then Error("task509 ci/out"); fi; fi;
D509S:=OutputTextFile(D509Script,false);; if D509S=fail then Error("task509 script"); fi;
SetPrintFormattingStatus(D509S,false);
PrintTo(D509S,"#!/usr/bin/env bash\nset -euo pipefail\numask 077\n");
PrintTo(D509S,"test -f '",D509Input,"'\n");
PrintTo(D509S,"test ! -L '",D509Input,"'\n");
PrintTo(D509S,"test \"$(realpath -- '",D509Input,"')\" = \"$PWD/",D509Input,"\"\n");
PrintTo(D509S,"test \"$(wc -c < '",D509Producer,"' | tr -d '[:space:]')\" = '",String(D509ProducerBytes),"'\n");
PrintTo(D509S,"test \"$(sha256sum '",D509Producer,"' | cut -d ' ' -f1)\" = '",D509ProducerSHA,"'\n");
PrintTo(D509S,"test \"$(wc -c < '",D509Checker,"' | tr -d '[:space:]')\" = '",String(D509CheckerBytes),"'\n");
PrintTo(D509S,"test \"$(sha256sum '",D509Checker,"' | cut -d ' ' -f1)\" = '",D509CheckerSHA,"'\n");
PrintTo(D509S,"test \"$(wc -c < '",D509Proof,"' | tr -d '[:space:]')\" = '",String(D509ProofBytes),"'\n");
PrintTo(D509S,"test \"$(sha256sum '",D509Proof,"' | cut -d ' ' -f1)\" = '",D509ProofSHA,"'\n");
PrintTo(D509S,"test \"$(wc -c < '",D509C99,"' | tr -d '[:space:]')\" = '",String(D509C99Bytes),"'\n");
PrintTo(D509S,"test \"$(sha256sum '",D509C99,"' | cut -d ' ' -f1)\" = '",D509C99SHA,"'\n");
PrintTo(D509S,"test \"$(wc -c < '",D509R51,"' | tr -d '[:space:]')\" = '",String(D509R51Bytes),"'\n");
PrintTo(D509S,"test \"$(sha256sum '",D509R51,"' | cut -d ' ' -f1)\" = '",D509R51SHA,"'\n");
PrintTo(D509S,"test \"$(wc -c < '",D509T451P,"' | tr -d '[:space:]')\" = '",String(D509T451PBytes),"'\n");
PrintTo(D509S,"test \"$(sha256sum '",D509T451P,"' | cut -d ' ' -f1)\" = '",D509T451PSHA,"'\n");
PrintTo(D509S,"test \"$(wc -c < '",D509T451C,"' | tr -d '[:space:]')\" = '",String(D509T451CBytes),"'\n");
PrintTo(D509S,"test \"$(sha256sum '",D509T451C,"' | cut -d ' ' -f1)\" = '",D509T451CSHA,"'\n");
PrintTo(D509S,"test \"$(wc -c < '",D509P424,"' | tr -d '[:space:]')\" = '",String(D509P424Bytes),"'\n");
PrintTo(D509S,"test \"$(sha256sum '",D509P424,"' | cut -d ' ' -f1)\" = '",D509P424SHA,"'\n");
PrintTo(D509S,"test \"$(wc -c < '",D509P426,"' | tr -d '[:space:]')\" = '",String(D509P426Bytes),"'\n");
PrintTo(D509S,"test \"$(sha256sum '",D509P426,"' | cut -d ' ' -f1)\" = '",D509P426SHA,"'\n");
PrintTo(D509S,"test \"$(wc -c < '",D509P427,"' | tr -d '[:space:]')\" = '",String(D509P427Bytes),"'\n");
PrintTo(D509S,"test \"$(sha256sum '",D509P427,"' | cut -d ' ' -f1)\" = '",D509P427SHA,"'\n");
PrintTo(D509S,"test 14040 -lt 14220 && test 14220 -lt 14400\n");
PrintTo(D509S,"test 4200000000 -lt 4500000000 && test 4500000000 -lt 5120000000\n");
PrintTo(D509S,"ulimit -v 5000000\n");
PrintTo(D509S,"timeout --foreground --kill-after=30s 14400s python3 -u -B ",D509Producer,
 " --resume '",D509Input,"' --output '",D509Artifact,"' --checkpoint '",D509Checkpoint,
 "' --search-seconds 14040 --hard-seconds 14220 --external-seconds 14400",
 " --search-rss-bytes 4200000000 --hard-rss-bytes 4500000000 --hard-vm-bytes 5120000000",
 " --max-rises 64 --batch-cap 16 2>&1 | tee '",D509PLog,"'\n");
PrintTo(D509S,"test \"$(grep -Ec '^R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6 status=(COMMON_CANDIDATE|UNKNOWN_RESOURCE)$' '",D509PLog,"')\" = 1\n");
PrintTo(D509S,"if grep -Eq '^R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6 status=COMMON_CANDIDATE$' '",D509PLog,"'; then\n");
PrintTo(D509S," timeout --foreground --kill-after=30s 5400s python3 -u -B ",D509Checker,
 " '",D509Artifact,"' --verdict '",D509Verdict,"' 2>&1 | tee '",D509CLog,"'\n");
PrintTo(D509S," grep -Eq '^R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_CHECKER_PASS terminal=COMMON_CANDIDATE$' '",D509CLog,"'\n");
PrintTo(D509S," test -s '",D509Verdict,"'\n");
PrintTo(D509S," printf '%s\\n' 'D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_COMPLETE' > '",D509OK,"'\n");
PrintTo(D509S,"else\n");
PrintTo(D509S," test -s '",D509Artifact,"' && test -s '",D509Checkpoint,"'\n");
PrintTo(D509S," grep -Eq '\"candidate_marker\":\"R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V6_RESOURCE_CANDIDATE\"' '",D509Artifact,"'\n");
PrintTo(D509S," grep -Eq '\"discovery_mode\":\"DISCOVERY_RESOURCE\"' '",D509Artifact,"'\n");
PrintTo(D509S," grep -Eq '\"state_sha256\":\"[0-9a-f]{64}\"' '",D509Checkpoint,"'\n");
PrintTo(D509S," grep -Eq '\"A0\":false' '",D509Artifact,"' && grep -Eq '\"COMMON\":false' '",D509Artifact,"' && grep -Eq '\"NONMEMBER\":false' '",D509Artifact,"'\n");
PrintTo(D509S," grep -Eq '\"fake\":false' '",D509Artifact,"' && grep -Eq '\"Ihara\":false' '",D509Artifact,"'\n");
PrintTo(D509S," printf '%s\\n' 'D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V7_RESOURCE' > '",D509OK,"'\n");
PrintTo(D509S,"fi\n");
CloseStream(D509S);
Exec(Concatenation("chmod 700 ",D509Script));
Exec(Concatenation("bash -n ",D509Script));
Exec(Concatenation("bash ",D509Script));
if not IsExistingFile(D509OK) then Error("task509 missing owned ok"); fi;
D509OKRaw:=StringFile(D509OK);;
if D509OKRaw<>D509ResourceSentinel and D509OKRaw<>D509CompleteSentinel then
 Error("task509 invalid owned ok"); fi;
Print("TASK509 v7 driver executed and owned transport verified.\n");
