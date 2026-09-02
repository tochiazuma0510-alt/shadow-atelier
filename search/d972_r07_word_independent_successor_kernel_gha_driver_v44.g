#############################################################################
## Task512 A4 restore-order/live-dual/completion handoff driver. ASCII only.
## The reached shell keeps the v43 row-26 release transport and one producer.
#############################################################################
if not IsBound(D972_R07_A4_TASK512_MODE) or D972_R07_A4_TASK512_MODE<>"ACTUAL_PRODUCTION" then
 Error("task512 driver: ACTUAL_PRODUCTION mode required"); fi;
D512Release:="https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9809473723_gap-run-out.a4-row26.zip";;
D512ReleaseBytes:=56410;; D512ReleaseSHA:="5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3";;
D512Producer:="search/d972_r07_word_independent_successor_kernel_v25.py";; D512ProducerBytes:=27075;; D512ProducerSHA:="8e5c16f28113218485f7196c6873dbbf3ce17a0e03bd7daafe71bc6e8da5015f";;
D512ProducerGeneratedBytes:=286439;; D512ProducerGeneratedSHA:="e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098";;
D512Checker:="crosscheck/check_d972_r07_word_independent_successor_kernel_v34.py";; D512CheckerBytes:=5838;; D512CheckerSHA:="b00219523c2e5703b8c6c52c7bf24655c727ddc72c7da9fd06c746063875a9ba";;
D512CheckerGeneratedBytes:=312553;; D512CheckerGeneratedSHA:="2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75";;
D512Proof:="sol/proof_r07_a4_actual_production_shard_wiring_v430.md";; D512ProofBytes:=7137;; D512ProofSHA:="acea72aea1a8f62a3de1c84a7bf4cab95fc4da85162bbe226b1a5f158755a904";;
D512V43:="search/d972_r07_word_independent_successor_kernel_gha_driver_v43.g";; D512V43Bytes:=15449;; D512V43SHA:="36be6a635fa7399c37048ef45debb5c25d5ede8cc1414fa153a7e8bb0dd7c8bb";;
D512Input:="ci/in/d972_r07_seven_context_roof_presentation_v1.json";; D512Zip:="ci/out/task512_row26_release.zip";; D512Extract:="ci/out/task512_row26_release_extract";;
D512Root:="ci/out/task512_v25_physical";; D512Output:="ci/out/task512_v25_producer.json";; D512Checkpoint:="ci/out/d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json";; D512PLog:="ci/out/task512_v25.producer.log";;
D512COutput:="ci/out/task512_v34_checker.json";; D512Ckpt:="ci/out/d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json";; D512CLog:="ci/out/task512_v34.checker.log";; D512OK:="ci/out/task512_v44.success";; D512Script:="ci/out/task512_v44.sh";;
D512Members:=[
 ["d972_r07_word_independent_successor_kernel_v40.json",9300,"7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.base.checkpoint.json",25581,"595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json",700,"910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000001.json",3551,"d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19"],
 ["d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000002.json",3625,"acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523"],
 ["d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json",8991,"b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2"] ];;
if Length(D512Members)<>6 then Error("task512 release members"); fi;
if not IsExistingFile(D512Input) then Error("task512 input missing"); fi;
for D512Owned in [D512Zip,D512Extract,D512Root,D512Output,D512Checkpoint,D512PLog,D512COutput,D512Ckpt,D512CLog,D512OK,D512Script] do
 if IsExistingFile(D512Owned) or IsDirectoryPath(D512Owned) then Error("task512 stale output ",D512Owned); fi; od;
for D512Member in D512Members do
 D512Owned:=Concatenation("ci/out/",D512Member[1]);;
 if IsExistingFile(D512Owned) or IsDirectoryPath(D512Owned) then Error("task512 stale member ",D512Owned); fi;
od;
if not IsExistingFile("ci/out") and CreateDir("ci/out")=fail then Error("task512 ci/out"); fi;
D512ScriptText:=Concatenation("#!/usr/bin/env bash\nset -euo pipefail\numask 077\n",
 "command -v curl >/dev/null; command -v unzip >/dev/null; command -v sha256sum >/dev/null; command -v timeout >/dev/null; command -v python3 >/dev/null\n",
 "root=\"$(pwd -P)\"\ntest -f \"$root/",D512Input,"\"\ntest \"$(realpath -- \\"",D512Input,"\\")\" = \"$root/",D512Input,"\"\n",
 "test \"$(wc -c < ",D512Producer,")\" = ",String(D512ProducerBytes),"; test \"$(sha256sum ",D512Producer," | cut -d' ' -f1)\" = ",D512ProducerSHA,"\n",
 "test \"$(wc -c < ",D512Checker,")\" = ",String(D512CheckerBytes),"; test \"$(sha256sum ",D512Checker," | cut -d' ' -f1)\" = ",D512CheckerSHA,"\n",
 "test \"$(python3 -u -B ",D512Producer," --source-patch-info | python3 -c 'import json,sys; x=json.load(sys.stdin); print(str(x[\"generated\"][\"bytes\"])+\":\"+x[\"generated\"][\"sha256\"])')\" = ",String(D512ProducerGeneratedBytes),":",D512ProducerGeneratedSHA,"\n",
 "test \"$(python3 -u -B ",D512Checker," --source-patch-info | python3 -c 'import json,sys; x=json.load(sys.stdin); print(str(x[\"generated\"][\"bytes\"])+\":\"+x[\"generated\"][\"sha256\"])')\" = ",String(D512CheckerGeneratedBytes),":",D512CheckerGeneratedSHA,"\n",
 "test \"$(wc -c < ",D512Proof,")\" = ",String(D512ProofBytes),"; test \"$(sha256sum ",D512Proof," | cut -d' ' -f1)\" = ",D512ProofSHA,"\n",
 "test \"$(wc -c < ",D512V43,")\" = ",String(D512V43Bytes),"; test \"$(sha256sum ",D512V43," | cut -d' ' -f1)\" = ",D512V43SHA,"\n",
 "test 14400 -lt 15000; test 8000000000 -lt 8704000000; ulimit -v 8500000\n",
 "test ! -e ",D512Zip,"; test ! -e ",D512Extract,"; curl --fail --location --retry 3 --silent --show-error ",D512Release," -o ",D512Zip,"\n",
 "test \"$(wc -c < ",D512Zip,")\" = ",String(D512ReleaseBytes),"; test \"$(sha256sum ",D512Zip," | cut -d' ' -f1)\" = ",D512ReleaseSHA,"; mkdir ",D512Extract,"; unzip -q ",D512Zip," -d ",D512Extract,"\n",
 "mkdir -p ci/out\n",
 "test -d ",D512Extract,"\n");;
for D512Member in D512Members do
 D512ScriptText:=Concatenation(D512ScriptText,
  "test \"$(unzip -Z1 ",D512Zip," | grep -Fxc -- '",D512Member[1],"' || true)\" = 1\n",
  "test -f ",D512Extract,"/",D512Member[1],"; test ! -L ",D512Extract,"/",D512Member[1],"\n",
  "test \"$(wc -c < ",D512Extract,"/",D512Member[1],")\" = ",String(D512Member[2]),"\n",
  "test \"$(sha256sum ",D512Extract,"/",D512Member[1]," | cut -d' ' -f1)\" = ",D512Member[3],"\n",
  "cp ",D512Extract,"/",D512Member[1]," ci/out/",D512Member[1],"\n",
  "test \"$(wc -c < ci/out/",D512Member[1],")\" = ",String(D512Member[2]),"; test \"$(sha256sum ci/out/",D512Member[1]," | cut -d' ' -f1)\" = ",D512Member[3],"\n");;
od;
D512ScriptText:=Concatenation(D512ScriptText,
 "mkdir -p ",D512Root,"\n",
 "timeout --foreground --signal=TERM --kill-after=60s 15000s python3 -u -B ",D512Producer," --input ",D512Input," --output ",D512Output," --checkpoint ",D512Checkpoint," --resume ",D512Checkpoint," --physical-root ",D512Root," --seconds 14400 --rss-bytes 8000000000 > ",D512PLog," 2>&1\n",
 "grep -Ec '^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PRODUCER_TERMINAL (R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS|UNKNOWN_RESOURCE)$' ",D512PLog," | grep -qx 1\n",
 "if grep -Fqx 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PRODUCER_TERMINAL UNKNOWN_RESOURCE' ",D512PLog,"; then test -s ",D512Output,"; test -s ",D512Checkpoint,"; test \"$(grep -Fc 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL' ",D512PLog," || true)\" = 0; printf '%s\\n' 'TASK512_R07_A4_RESOURCE terminal=UNKNOWN_RESOURCE checker=0' > ",D512OK,"; else\n",
 " test -s ",D512Output,"; timeout --foreground --signal=TERM --kill-after=60s 5400s python3 -u -B ",D512Checker," --input ",D512Input," --producer ",D512Output," --output ",D512COutput," --checkpoint ",D512Ckpt," --resume ",D512Ckpt," --seconds 14400 --rss-bytes 8000000000 > ",D512CLog," 2>&1\n",
 " grep -Fqx 'R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_PASS' ",D512CLog,"; test -s ",D512COutput,"; printf '%s\\n' 'TASK512_R07_A4_PASS terminal=POSITIVE producer=1 checker=1' > ",D512OK,"; fi\n");;
D512S:=OutputTextFile(D512Script,false);; if D512S=fail then Error("task512 script open"); fi; SetPrintFormattingStatus(D512S,false); PrintTo(D512S,D512ScriptText); CloseStream(D512S);
Exec(Concatenation("chmod 700 ",D512Script));; Exec(Concatenation("bash -n ",D512Script));; Exec(Concatenation("bash ",D512Script));
if not IsExistingFile(D512OK) then Error("task512 owned marker missing"); fi;
D512Marker:=StringFile(D512OK);;
if D512Marker<>"TASK512_R07_A4_RESOURCE terminal=UNKNOWN_RESOURCE checker=0\n" and
   D512Marker<>"TASK512_R07_A4_PASS terminal=POSITIVE producer=1 checker=1\n" then
 Error("task512 owned marker drift");
fi;
Print("TASK512_R07_A4_RESTORE_ORDER_AND_LIVE_DUAL_REPAIR_TRANSPORT_PASS release=56410 producer_processes=1 resource_checker=0 positive_checker=1\\n");
