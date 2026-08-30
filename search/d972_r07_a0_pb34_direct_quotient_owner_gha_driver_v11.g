#############################################################################
## Task430 v11 one-owner driver. Input/output checkpoints are immutable and distinct.
#############################################################################
D430Producer:="search/d972_r07_a0_pb34_direct_quotient_owner_v11.py";; D430ProducerBytes:=27430;; D430ProducerSHA:="b6ae32a89dfd0cd8afc540bc09089ef3722e489d4fdef574a8bd42540a1bfd63";;
D430Checker:="crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v11.py";; D430CheckerBytes:=7401;; D430CheckerSHA:="3dd65ccc71cf834674f2198458c4ecf4eea936a4e9cfca8c5e72e0dd10d9c8fd";;
D430Artifact:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v11.json";;
D430Input:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v11_input.checkpoint";; D430Output:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v11_output.checkpoint";;
D430PL:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v11_producer.log";; D430CL:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v11_checker.log";;
D430Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task430 missing ",p);fi;return x;end;;
D430Pin:=function(p,n,s)local x;x:=D430Read(p);if n<>Length(x) or Length(s)<>64 or HexSHA256(x)<>s then Error("task430 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_PB34_V11_RUN) or D972_R07_A0_PB34_V11_RUN<>true then Error("task430 external preamble required");fi;;
if D430ProducerSHA="PENDING" or D430CheckerSHA="PENDING" then Error("task430 pins pending");fi;;
D430Pin(D430Producer,D430ProducerBytes,D430ProducerSHA);;D430Pin(D430Checker,D430CheckerBytes,D430CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D430Output) then Error("task430 output checkpoint already exists; archive it and choose a fresh output path");fi;;
D430Resume:="";;D430InputArg:="";;if IsExistingFile(D430Input) then D430Resume:=Concatenation(" --resume ",D430Input);D430InputArg:=D430Input;fi;;
D430CheckInput:="";;if D430InputArg<>"" then D430CheckInput:=Concatenation(" --input-checkpoint ",D430InputArg);fi;;
Exec(Concatenation("python3 -u -B ",D430Producer," --mode PRODUCTION --seconds 9000 --rss-bytes 4800000000 --output ",D430Artifact," --checkpoint ",D430Output,D430Resume," 2>&1 | tee ",D430PL));;
if PositionSublist(D430Read(D430PL),"R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V11")=fail then Error("task430 producer marker");fi;;
D430A:=D430Read(D430Artifact);;if PositionSublist(D430A,"UNKNOWN_RESOURCE")<>fail and not IsExistingFile(D430Output) then Error("task430 output checkpoint missing");fi;;
Exec(Concatenation("python3 -u -B ",D430Checker," ",D430Artifact,D430CheckInput," --output-checkpoint ",D430Output," 2>&1 | tee ",D430CL));;
if PositionSublist(D430Read(D430CL),"R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V11_PASS")=fail then Error("task430 checker marker");fi;;
Print("R07_A0_PB34_DIRECT_QUOTIENT_GHA_DRIVER_V11_PASS artifact_sha256=",HexSHA256(D430A),"\n");;

