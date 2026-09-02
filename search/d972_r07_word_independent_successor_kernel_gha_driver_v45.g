#############################################################################
## Task514 A4 checker fixture and dispatch-envelope repair. ASCII only.
## v43's reached transport is retained with v44/v35 pins and typed claims.
#############################################################################
if not IsBound(D972_R07_A4_TASK514_MODE) or D972_R07_A4_TASK514_MODE<>"ACTUAL_PRODUCTION" then Error("task514 mode"); fi;
D514V44:="search/d972_r07_word_independent_successor_kernel_gha_driver_v44.g";; D514V44Bytes:=8960;; D514V44SHA:="7f70546b51b934edcc6d64626af4d04c18f15642a10db8b40eaea3f9fcfb96f3";;
D514Producer:="search/d972_r07_word_independent_successor_kernel_v25.py";; D514ProducerBytes:=27075;; D514ProducerSHA:="8e5c16f28113218485f7196c6873dbbf3ce17a0e03bd7daafe71bc6e8da5015f";; D514ProducerGeneratedBytes:=286439;; D514ProducerGeneratedSHA:="e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098";;
D514Checker:="crosscheck/check_d972_r07_word_independent_successor_kernel_v35.py";; D514CheckerBytes:=10246;; D514CheckerSHA:="c8383a18169ec2da63e4e7a64de17f05d305c35e15393bcbb9e3c312ac6d5dd7";; D514CheckerGeneratedBytes:=312553;; D514CheckerGeneratedSHA:="2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75";;
D514Proof:="sol/proof_r07_a4_actual_production_shard_wiring_v430.md";; D514ProofBytes:=7137;; D514ProofSHA:="acea72aea1a8f62a3de1c84a7bf4cab95fc4da85162bbe226b1a5f158755a904";; D514V43:="search/d972_r07_word_independent_successor_kernel_gha_driver_v43.g";; D514V43Bytes:=15449;; D514V43SHA:="36be6a635fa7399c37048ef45debb5c25d5ede8cc1414fa153a7e8bb0dd7c8bb";;
D514Release:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9809473723_gap-run-out.a4-row26.zip";; D514ReleaseBytes:=56410;; D514ReleaseSHA:="5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3";;
D514Input:="ci/in/d972_r07_seven_context_roof_presentation_v1.json";; D514Zip:="ci/out/task514_row26_release.zip";; D514Extract:="ci/out/task514_row26_release_extract";; D514Root:="ci/out/task514_v25_physical";; D514Output:="ci/out/task514_v25_producer.json";; D514Checkpoint:="ci/out/d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json";; D514PLog:="ci/out/task514_v25.producer.log";;
D514COutput:="ci/out/task514_v35_checker.json";; D514Ckpt:="ci/out/d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json";; D514CLog:="ci/out/task514_v35.checker.log";; D514OK:="ci/out/task514_v45.success";; D514Script:="ci/out/task514_v45.sh";;
D514Authority:=["ci/in/d972_r07_seven_context_roof_presentation_v1.json","ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json","ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt","ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt","ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json"];;
D514Members:=[
 ["d972_r07_word_independent_successor_kernel_v40.json",9300,"7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.base.checkpoint.json",25581,"595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json",700,"910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000001.json",3551,"d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000002.json",3625,"acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523"],
 ["d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json",8991,"b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2"] ];;
if Length(D514Members)<>6 then Error("task514 six members"); fi;
if not IsExistingFile("ci/out") and CreateDir("ci/out")=fail then Error("task514 ci/out"); fi;
for D514Owned in [D514Zip,D514Extract,D514Root,D514Output,D514Checkpoint,D514PLog,D514COutput,D514Ckpt,D514CLog,D514OK,D514Script] do if IsExistingFile(D514Owned) or IsDirectoryPath(D514Owned) then Error("task514 stale output ",D514Owned); fi; od;
for D514Member in D514Members do D514Owned:=Concatenation("ci/out/",D514Member[1]);; if IsExistingFile(D514Owned) or IsDirectoryPath(D514Owned) then Error("task514 stale member ",D514Owned); fi; od;
D514S:=Concatenation("#!/usr/bin/env bash\nset -euo pipefail\numask 077\n",
 "command -v curl >/dev/null; command -v unzip >/dev/null; command -v sha256sum >/dev/null; command -v timeout >/dev/null; command -v python3 >/dev/null\n",
 "root=\"$(pwd -P)\"\ntest -f \"$root/",D514Input,"\"\ntest \"$(realpath -- \\\"",D514Input,"\\\")\" = \"$root/",D514Input,"\"\n",
 "test \"$(wc -c < ",D514Producer,")\" = ",String(D514ProducerBytes),"; test \"$(sha256sum ",D514Producer," | cut -d' ' -f1)\" = ",D514ProducerSHA,"\n",
 "test \"$(wc -c < ",D514Checker,")\" = ",String(D514CheckerBytes),"; test \"$(sha256sum ",D514Checker," | cut -d' ' -f1)\" = ",D514CheckerSHA,"\n",
 "test \"$(python3 -u -B ",D514Producer," --source-patch-info | python3 -c 'import json,sys; x=json.load(sys.stdin); print(str(x[\"generated\"][\"bytes\"])+\":\"+x[\"generated\"][\"sha256\"])')\" = ",String(D514ProducerGeneratedBytes),":",D514ProducerGeneratedSHA,"\n",
 "test \"$(python3 -u -B ",D514Checker," --source-patch-info | python3 -c 'import json,sys; x=json.load(sys.stdin); print(str(x[\"generated\"][\"bytes\"])+\":\"+x[\"generated\"][\"sha256\"])')\" = ",String(D514CheckerGeneratedBytes),":",D514CheckerGeneratedSHA,"\n",
 "test \"$(wc -c < ",D514V44,")\" = ",String(D514V44Bytes),"; test \"$(sha256sum ",D514V44," | cut -d' ' -f1)\" = ",D514V44SHA,"\n",
 "test \"$(wc -c < ",D514V43,")\" = ",String(D514V43Bytes),"; test \"$(sha256sum ",D514V43," | cut -d' ' -f1)\" = ",D514V43SHA,"\n",
 "test \"$(wc -c < ",D514Proof,")\" = ",String(D514ProofBytes),"; test \"$(sha256sum ",D514Proof," | cut -d' ' -f1)\" = ",D514ProofSHA,"\n",
 "for authority in ci/in/d972_r07_seven_context_roof_presentation_v1.json ci/in/d972_r07_seven_context_roof_presentation_v1.acceptance_v2.json ci/in/d972_r07_seven_context_roof_presentation_v1.producer.attestation.txt ci/in/d972_r07_seven_context_roof_presentation_v1.checker.attestation.txt ci/in/d972_r07_seven_context_roof_presentation_v1.checker.verdict.json; do test -f \"$root/$authority\"; test ! -L \"$root/$authority\"; done\n",
 "test 14400 -lt 15000; test 8000000000 -lt 8704000000; ulimit -v 8500000\n",
 "test ! -e ",D514Zip,"; test ! -e ",D514Extract,"; curl --fail --location --retry 3 --silent --show-error ",D514Release," -o ",D514Zip,"\n",
 "test \"$(wc -c < ",D514Zip,")\" = ",String(D514ReleaseBytes),"; test \"$(sha256sum ",D514Zip," | cut -d' ' -f1)\" = ",D514ReleaseSHA,"; mkdir ",D514Extract,"; unzip -q ",D514Zip," -d ",D514Extract,"\n",
 "mkdir -p ci/out\n");;
for D514Member in D514Members do D514S:=Concatenation(D514S,
 "test \"$(unzip -Z1 ",D514Zip," | grep -Fxc -- '",D514Member[1],"' || true)\" = 1\n",
 "test -f ",D514Extract,"/",D514Member[1],"; test ! -L ",D514Extract,"/",D514Member[1],"\n",
 "test \"$(wc -c < ",D514Extract,"/",D514Member[1],")\" = ",String(D514Member[2]),"; test \"$(sha256sum ",D514Extract,"/",D514Member[1]," | cut -d' ' -f1)\" = ",D514Member[3],"\n",
 "cp ",D514Extract,"/",D514Member[1]," ci/out/",D514Member[1],"\n",
 "test \"$(wc -c < ci/out/",D514Member[1],")\" = ",String(D514Member[2]),"; test \"$(sha256sum ci/out/",D514Member[1]," | cut -d' ' -f1)\" = ",D514Member[3],"\n"); od;
D514S:=Concatenation(D514S,
 "mkdir -p ",D514Root,"\n",
 "producer_start=$SECONDS\n",
 "timeout --foreground --signal=TERM --kill-after=60s 15000s python3 -u -B ",D514Producer," --input ",D514Input," --output ",D514Output," --checkpoint ",D514Checkpoint," --resume ",D514Checkpoint," --physical-root ",D514Root," --seconds 14400 --rss-bytes 8000000000 > ",D514PLog," 2>&1\n",
 "producer_elapsed=$((SECONDS-producer_start)); test \"$producer_elapsed\" -lt 15000\n",
 "test \"$(grep -Ec '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PRODUCER_TERMINAL (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS|UNKNOWN_RESOURCE)$' ",D514PLog," || true)\" = 1\n",
 "test \"$(grep -Fc UNKNOWN_INPUT ",D514PLog," || true)\" = 0; test \"$(grep -Fc HARD_STOP ",D514PLog," || true)\" = 0; test \"$(grep -Fc ERROR ",D514PLog," || true)\" = 0; test \"$(grep -Fc Traceback ",D514PLog," || true)\" = 0\n",
 "if grep -Fqx 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PRODUCER_TERMINAL UNKNOWN_RESOURCE' ",D514PLog,"; then test -s ",D514Output,"; test -s ",D514Checkpoint,"; test \"$(grep -Fc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL' ",D514PLog," || true)\" = 0; python3 -c 'import json; x=json.load(open(\"",D514Output,"\")); assert x.get(\"status\")==\"UNKNOWN_RESOURCE\" and x.get(\"terminal\")==\"UNKNOWN_RESOURCE\" and x.get(\"complete\") is False; assert all(x.get(k) is False for k in (\"A0\",\"COMMON\",\"NONMEMBER\") if k in x); assert x.get(\"forbidden_downstream\")=={\"lift\":False,\"fake\":False,\"Ihara\":False}'\n",
 " printf '%s\\n' 'TASK514_R07_A4_RESOURCE terminal=UNKNOWN_RESOURCE checker=0' > ",D514OK,"; else\n",
 " test -s ",D514Output,"; test \"$(grep -Fxc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PRODUCER_TERMINAL R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS' ",D514PLog," || true)\" = 1; python3 -c 'import json; x=json.load(open(\"",D514Output,"\")); assert x.get(\"complete\") is True; assert all(x.get(k) is False for k in (\"A0\",\"COMMON\",\"NONMEMBER\") if k in x); assert x.get(\"forbidden_downstream\")=={\"lift\":False,\"fake\":False,\"Ihara\":False}'\n",
 " checker_start=$SECONDS; timeout --foreground --signal=TERM --kill-after=60s 15000s python3 -u -B ",D514Checker," --input ",D514Input," --producer ",D514Output," --output ",D514COutput," --checkpoint ",D514Ckpt," --resume ",D514Ckpt," --seconds 14400 --rss-bytes 8000000000 > ",D514CLog," 2>&1; checker_elapsed=$((SECONDS-checker_start)); test \"$checker_elapsed\" -lt 15000\n",
 " test -s ",D514COutput,"; test \"$(grep -Ec '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS|UNKNOWN_RESOURCE)$' ",D514CLog," || true)\" = 1; test \"$(grep -Fc UNKNOWN_INPUT ",D514CLog," || true)\" = 0; test \"$(grep -Fc HARD_STOP ",D514CLog," || true)\" = 0; test \"$(grep -Fc ERROR ",D514CLog," || true)\" = 0; test \"$(grep -Fc Traceback ",D514CLog," || true)\" = 0\n",
 " if grep -Fqx 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL UNKNOWN_RESOURCE' ",D514CLog,"; then python3 -c 'import json; x=json.load(open(\"",D514COutput,"\")); assert x.get(\"status\")==\"UNKNOWN_RESOURCE\" and x.get(\"terminal\")==\"UNKNOWN_RESOURCE\" and x.get(\"complete\") is False; assert all(x.get(k) is False for k in (\"A0\",\"COMMON\",\"NONMEMBER\") if k in x); assert x.get(\"forbidden_downstream\")=={\"lift\":False,\"fake\":False,\"Ihara\":False}'; printf '%s\\n' 'TASK514_R07_A4_RESOURCE terminal=UNKNOWN_RESOURCE checker=1' > ",D514OK,"; else test \"$(grep -Fxc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS' ",D514CLog," || true)\" = 1; python3 -c 'import json; x=json.load(open(\"",D514COutput,"\")); assert x.get(\"complete\") is True; assert all(x.get(k) is False for k in (\"A0\",\"COMMON\",\"NONMEMBER\") if k in x); assert x.get(\"forbidden_downstream\")=={\"lift\":False,\"fake\":False,\"Ihara\":False}'; printf '%s\\n' 'TASK514_R07_A4_PASS terminal=POSITIVE producer=1 checker=1' > ",D514OK,"; fi; fi\n");;
D514Out:=OutputTextFile("ci/out/task514_v45.sh",false);; if D514Out=fail then Error("task514 shell open"); fi; SetPrintFormattingStatus(D514Out,false); PrintTo(D514Out,D514S); CloseStream(D514Out);
Exec("chmod 700 ci/out/task514_v45.sh");; Exec("bash -n ci/out/task514_v45.sh");; Exec("bash ci/out/task514_v45.sh");;
if not IsExistingFile(D514OK) then Error("task514 marker missing"); fi;
D514Marker:=StringFile(D514OK);;
if D514Marker<>"TASK514_R07_A4_RESOURCE terminal=UNKNOWN_RESOURCE checker=0\n" and D514Marker<>"TASK514_R07_A4_RESOURCE terminal=UNKNOWN_RESOURCE checker=1\n" and D514Marker<>"TASK514_R07_A4_PASS terminal=POSITIVE producer=1 checker=1\n" then Error("task514 marker drift"); fi;
Print("TASK514_R07_A4_CHECKER_FIXTURE_AND_DRIVER_ENVELOPE_REPAIR_TRANSPORT_PASS\n");
