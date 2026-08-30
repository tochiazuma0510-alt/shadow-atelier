
#############################################################################
## Task431 v12 one-owner driver. Input/output checkpoints are immutable and distinct.
#############################################################################
D431Producer:="search/d972_r07_a0_pb34_direct_quotient_owner_v12.py";; D431ProducerBytes:=50017;; D431ProducerSHA:="ff856827e462c9cd09fe6068fed7930b06bbf9de0d04b78e1f20bbf3965063a8";;
D431Checker:="crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v12.py";; D431CheckerBytes:=13334;; D431CheckerSHA:="e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891";;
D431Artifact:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v12.json";;
D431Input:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v12_input.checkpoint";; D431Output:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v12_output.checkpoint";;
D431PL:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v12_producer.log";; D431CL:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v12_checker.log";;
D431Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task431 missing ",p);fi;return x;end;;
D431Pin:=function(p,n,s)local x;x:=D431Read(p);if n<>Length(x) or Length(s)<>64 or HexSHA256(x)<>s then Error("task431 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_PB34_V12_RUN) or D972_R07_A0_PB34_V12_RUN<>true then Error("task431 external preamble required");fi;;
if D431ProducerSHA="PENDING" or D431CheckerSHA="PENDING" then Error("task431 pins pending");fi;;
D431Pin(D431Producer,D431ProducerBytes,D431ProducerSHA);;D431Pin(D431Checker,D431CheckerBytes,D431CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D431Output) then Error("task431 output checkpoint already exists; archive it and choose a fresh output path");fi;;
D431Resume:="";;D431InputArg:="";;D431MigrationArg:=Concatenation(" --resume-v11-url https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9735328330_gap-run-out.valid.zip");;if IsExistingFile(D431Input) then D431Resume:=Concatenation(" --resume ",D431Input);D431InputArg:=D431Input;D431MigrationArg:="";fi;;
D431CheckInput:="";;if D431InputArg<>"" then D431CheckInput:=Concatenation(" --input-checkpoint ",D431InputArg);fi;;
Exec(Concatenation("python3 -u -B ",D431Producer," --mode PRODUCTION --seconds 9000 --rss-bytes 4800000000",D431MigrationArg," --output ",D431Artifact," --checkpoint ",D431Output,D431Resume," 2>&1 | tee ",D431PL));;
if PositionSublist(D431Read(D431PL),"R07_A0_PHASE_SEPARATED_PACKED_OWNER_V12")=fail then Error("task431 producer marker");fi;;
D431A:=D431Read(D431Artifact);;if PositionSublist(D431A,"UNKNOWN_RESOURCE")<>fail and not IsExistingFile(D431Output) then Error("task431 output checkpoint missing");fi;;
Exec(Concatenation("python3 -u -B ",D431Checker," ",D431Artifact,D431CheckInput," --output-checkpoint ",D431Output," 2>&1 | tee ",D431CL));;
if PositionSublist(D431Read(D431CL),"R07_A0_PHASE_SEPARATED_PACKED_CHECKER_V12_PASS")=fail then Error("task431 checker marker");fi;;
Print("R07_A0_PB34_DIRECT_QUOTIENT_GHA_DRIVER_V12_PASS artifact_sha256=",HexSHA256(D431A),"\n");;
