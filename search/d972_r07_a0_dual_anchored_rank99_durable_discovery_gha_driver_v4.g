#############################################################################
## R07 durable discovery v4 driver. ASCII only.
#############################################################################
if not IsBound(D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_RUN) or
   D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_RUN<>true then
 Error("task490 external run preamble required"); fi;
if not IsBound(D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_INPUT) then
 D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_INPUT:=
  "search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json";; fi;
D482Input:=D972_R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_INPUT;;
D482Producer:="search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.py";;
D482Checker:="crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.py";;
D482Base:="search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json";;
D482Rank51:="search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json";;
D482Task451P:="search/d972_r07_a0_dual_anchored_active_batch_v1.py";;
D482Task451C:="crosscheck/check_d972_r07_a0_dual_anchored_active_batch_recovered_v2.py";;
D482Paper:="sol/proof_r07_rank99_actual_owner_transform_v424.md";;
D482Paper426:="sol/proof_r07_rank99_cached_discovery_chain_v426.md";;
D482Paper427:="sol/proof_r07_deadline_flush_short_batch_v427.md";;
D482ProducerBytes:=98576;; D482ProducerSHA:="5b8f3ae76abb64768decb14be50fbd6d75b5e84aeaad2b1a63fcb544933cf36f";;
D482CheckerBytes:=66212;; D482CheckerSHA:="cd0acf346d4f133dfaa8e047db6593511a5423c6a166060a37fc313504e928e7";;
D482BaseBytes:=173082;; D482BaseSHA:="bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358";;
D482Rank51Bytes:=10934;; D482Rank51SHA:="a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4";;
D482Task451PBytes:=13834;; D482Task451PSHA:="ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b";;
D482Task451CBytes:=14442;; D482Task451CSHA:="1d1080cd3e130d987316feefd820215f495cd6320aa5eca764fd2f8997f0c424";;
D482PaperBytes:=7009;; D482PaperSHA:="f2e2103f214e6d7c15f5d1c2bc84cd100cd37a69634c381793a42a20e8bad2d9";;
D482Paper426Bytes:=9165;; D482Paper426SHA:="5c3176011ea64235196587ed19720ad5d5a5c542c2896e46fe33ef3df3a3977a";;
D482Paper427Bytes:=6602;; D482Paper427SHA:="b958a164dfc78c77596876227b31a39467e077c9666d4a7be9033a58ee4c0ec5";;
D482Receipt:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.json";;
D482Checkpoint:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.checkpoint";;
D482Verdict:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.checker.json";;
D482PLog:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.producer.log";;
D482CLog:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.checker.log";;
D482Script:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.sh";;
D482OK:="ci/out/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.ok";;
D482Safe:=function(path)
 local tail,allowed,i;
 if not IsString(path) or Length(path)<19 or path{[1..13]}<>"search/certs/" then return false; fi;
 if PositionSublist(path,"..")<>fail then return false; fi;
 tail:=path{[14..Length(path)]};
 if Length(tail)<6 or tail{[Length(tail)-4..Length(tail)]}<>".json" then return false; fi;
 allowed:="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-";
 if Position(tail,"/")<>fail or Position(tail,"\\")<>fail then return false; fi;
 for i in [1..Length(tail)] do
  if Position(allowed,tail[i])=fail then return false; fi;
 od;
 return true;
end;;
if not D482Safe(D482Input) then Error("task490 unsafe resume input"); fi;
if IsExistingFile(D482Receipt) or IsExistingFile(D482Checkpoint) or IsExistingFile(D482Verdict) or
   IsExistingFile(D482PLog) or IsExistingFile(D482CLog) or IsExistingFile(D482Script) or IsExistingFile(D482OK) then
 Error("task490 stale output"); fi;
Exec("mkdir -p ci/out");;
D482S:=OutputTextFile(D482Script,false);; if D482S=fail then Error("task490 script open"); fi;
SetPrintFormattingStatus(D482S,false);;
PrintTo(D482S,"#!/usr/bin/env bash\nset -euo pipefail\numask 077\n");;
PrintTo(D482S,"test -f \"",D482Input,"\"\n");;
PrintTo(D482S,"test ! -L \"",D482Input,"\"\n");;
PrintTo(D482S,"test \"$(realpath -- \"",D482Input,"\")\" = \"$PWD/",D482Input,"\"\n");;
PrintTo(D482S,"test \"$(wc -c < ",D482Producer," | tr -d [:space:])\" = \"",String(D482ProducerBytes),"\"\n");;
PrintTo(D482S,"test \"$(sha256sum ",D482Producer," | cut -d \" \" -f1)\" = \"",D482ProducerSHA,"\"\n");;
PrintTo(D482S,"test \"$(wc -c < ",D482Checker," | tr -d [:space:])\" = \"",String(D482CheckerBytes),"\"\n");;
PrintTo(D482S,"test \"$(sha256sum ",D482Checker," | cut -d \" \" -f1)\" = \"",D482CheckerSHA,"\"\n");;
PrintTo(D482S,"test \"$(wc -c < ",D482Base," | tr -d [:space:])\" = \"",String(D482BaseBytes),"\"\n");;
PrintTo(D482S,"test \"$(sha256sum ",D482Base," | cut -d \" \" -f1)\" = \"",D482BaseSHA,"\"\n");;
PrintTo(D482S,"test \"$(wc -c < ",D482Rank51," | tr -d [:space:])\" = \"",String(D482Rank51Bytes),"\"\n");;
PrintTo(D482S,"test \"$(sha256sum ",D482Rank51," | cut -d \" \" -f1)\" = \"",D482Rank51SHA,"\"\n");;
PrintTo(D482S,"test \"$(wc -c < ",D482Task451P," | tr -d [:space:])\" = \"",String(D482Task451PBytes),"\"\n");;
PrintTo(D482S,"test \"$(sha256sum ",D482Task451P," | cut -d \" \" -f1)\" = \"",D482Task451PSHA,"\"\n");;
PrintTo(D482S,"test \"$(wc -c < ",D482Task451C," | tr -d [:space:])\" = \"",String(D482Task451CBytes),"\"\n");;
PrintTo(D482S,"test \"$(sha256sum ",D482Task451C," | cut -d \" \" -f1)\" = \"",D482Task451CSHA,"\"\n");;
PrintTo(D482S,"test \"$(wc -c < ",D482Paper," | tr -d [:space:])\" = \"",String(D482PaperBytes),"\"\n");;
PrintTo(D482S,"test \"$(sha256sum ",D482Paper," | cut -d \" \" -f1)\" = \"",D482PaperSHA,"\"\n");;
PrintTo(D482S,"test \"$(wc -c < ",D482Paper426," | tr -d [:space:])\" = \"",String(D482Paper426Bytes),"\"\n");;
PrintTo(D482S,"test \"$(sha256sum ",D482Paper426," | cut -d \" \" -f1)\" = \"",D482Paper426SHA,"\"\n");;
PrintTo(D482S,"test \"$(wc -c < ",D482Paper427," | tr -d [:space:])\" = \"",String(D482Paper427Bytes),"\"\n");;
PrintTo(D482S,"test \"$(sha256sum ",D482Paper427," | cut -d \" \" -f1)\" = \"",D482Paper427SHA,"\"\n");;
PrintTo(D482S,"test 14040 -lt 14220 && test 14220 -lt 14400\n");;
PrintTo(D482S,"test 4200000000 -lt 4500000000 && test 4500000000 -lt 5120000000\n");;
PrintTo(D482S,"ulimit -v 5000000\n");;
PrintTo(D482S,"timeout --foreground --kill-after=30s 14400s python3 -u -B ",D482Producer,
 " --resume ",D482Input," --output ",D482Receipt," --checkpoint ",D482Checkpoint,
 " --search-seconds 14040 --hard-seconds 14220 --external-seconds 14400",
 " --search-rss-bytes 4200000000 --hard-rss-bytes 4500000000 --hard-vm-bytes 5120000000",
 " --max-rises 64 --batch-cap 16 2>&1 | tee ",D482PLog,"\n");;
PrintTo(D482S,"test \"$(grep -Ec '^R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4 status=(COMMON_CANDIDATE|UNKNOWN_RESOURCE)$' ",D482PLog,")\" = 1\n");;
PrintTo(D482S,"if grep -Eq '^R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4 status=UNKNOWN_RESOURCE$' ",D482PLog,"; then\n");;
PrintTo(D482S," test -s ",D482Receipt," && test -s ",D482Checkpoint,"\n");;
PrintTo(D482S," grep -Eq '\"candidate_marker\":\"R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_RESOURCE_CANDIDATE\"' ",D482Receipt,"\n");;
PrintTo(D482S," grep -Eq '\"discovery_mode\":\"DISCOVERY_RESOURCE\"' ",D482Receipt,"\n");;
PrintTo(D482S," grep -Eq '\"state_sha256\":\"[0-9a-f]{64}\"' ",D482Checkpoint,"\n");;
PrintTo(D482S," printf '%s\\n' 'R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_RESOURCE_CANDIDATE' > ",D482OK,"\n");;
PrintTo(D482S," test \"$(wc -l < ",D482OK," | tr -d '[:space:]')\" = \"1\"\n");;
PrintTo(D482S," test \"$(cat ",D482OK,")\" = \"R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_RESOURCE_CANDIDATE\"\n");;
PrintTo(D482S," test \"$(grep -Ec 'R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_COMPLETE' ",D482OK,")\" = \"0\"\n");;
PrintTo(D482S," exit 0\nfi\n");;
PrintTo(D482S,"test \"$(grep -Ec '^R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4 status=COMMON_CANDIDATE$' ",D482PLog,")\" = 1\n");;
PrintTo(D482S,"timeout --foreground --kill-after=30s 5400s python3 -u -B ",D482Checker,
 " ",D482Receipt," --verdict ",D482Verdict," 2>&1 | tee ",D482CLog,"\n");;
PrintTo(D482S,"test \"$(grep -Ec '^R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_CHECKER_PASS terminal=COMMON_CANDIDATE$' ",D482CLog,")\" = 1\n");;
PrintTo(D482S,"test -s ",D482Verdict,"\n");;
PrintTo(D482S,"printf '%s\\n' 'R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_COMPLETE' > ",D482OK,"\n");;
PrintTo(D482S,"test \"$(wc -l < ",D482OK," | tr -d '[:space:]')\" = \"1\"\n");;
PrintTo(D482S,"test \"$(cat ",D482OK,")\" = \"R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_COMPLETE\"\n");;
CloseStream(D482S);; Exec(Concatenation("bash ",D482Script));
if not IsExistingFile(D482OK) then Error("task490 missing success marker"); fi;
Exec(Concatenation("test \"$(wc -l < ",D482OK," | tr -d '[:space:]')\" = 1"));
D482OKRaw:=StringFile(D482OK);;
if D482OKRaw="R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_RESOURCE_CANDIDATE\n" then
 Print("R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_RESOURCE_TERMINAL\n");
elif D482OKRaw="R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_COMPLETE\n" then
 Print("R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V4_COMPLETE\n");
else Error("task490 unexpected owned OK content"); fi;
