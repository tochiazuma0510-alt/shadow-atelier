#############################################################################
## Task429 v10 one-owner driver. Input/output checkpoints are immutable and distinct.
#############################################################################
D429Producer:="search/d972_r07_a0_pb34_direct_quotient_owner_v10.py";; D429ProducerBytes:=26758;; D429ProducerSHA:="2a7ab84e8644579afa9137840eb0c018ba65065f0d07143ac9e46cfc7bbcdc15";;
D429Checker:="crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v10.py";; D429CheckerBytes:=7399;; D429CheckerSHA:="95b6348c75f1ea7316904b432f51e1a53caa84a4bdd5ac985bf1c6ec3c1c4acf";;
D429Artifact:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v10.json";;
D429Input:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v10_input.checkpoint";; D429Output:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v10_output.checkpoint";;
D429PL:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v10_producer.log";; D429CL:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v10_checker.log";;
D429Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task429 missing ",p);fi;return x;end;;
D429Pin:=function(p,n,s)local x;x:=D429Read(p);if n<>Length(x) or Length(s)<>64 or HexSHA256(x)<>s then Error("task429 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_PB34_V10_RUN) or D972_R07_A0_PB34_V10_RUN<>true then Error("task429 external preamble required");fi;;
if D429ProducerSHA="PENDING" or D429CheckerSHA="PENDING" then Error("task429 pins pending");fi;;
D429Pin(D429Producer,D429ProducerBytes,D429ProducerSHA);;D429Pin(D429Checker,D429CheckerBytes,D429CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D429Output) then Error("task429 output checkpoint already exists; archive it and choose a fresh output path");fi;;
D429Resume:="";;D429InputArg:="";;if IsExistingFile(D429Input) then D429Resume:=Concatenation(" --resume ",D429Input);D429InputArg:=D429Input;fi;;
D429CheckInput:="";;if D429InputArg<>"" then D429CheckInput:=Concatenation(" --input-checkpoint ",D429InputArg);fi;;
Exec(Concatenation("python3 -u -B ",D429Producer," --mode PRODUCTION --seconds 9000 --rss-bytes 4800000000 --output ",D429Artifact," --checkpoint ",D429Output,D429Resume," 2>&1 | tee ",D429PL));;
if PositionSublist(D429Read(D429PL),"R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V10")=fail then Error("task429 producer marker");fi;;
D429A:=D429Read(D429Artifact);;if PositionSublist(D429A,"UNKNOWN_RESOURCE")<>fail and not IsExistingFile(D429Output) then Error("task429 output checkpoint missing");fi;;
Exec(Concatenation("python3 -u -B ",D429Checker," ",D429Artifact,D429CheckInput," --output-checkpoint ",D429Output," 2>&1 | tee ",D429CL));;
if PositionSublist(D429Read(D429CL),"R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V10_PASS")=fail then Error("task429 checker marker");fi;;
Print("R07_A0_PB34_DIRECT_QUOTIENT_GHA_DRIVER_V10_PASS artifact_sha256=",HexSHA256(D429A),"\n");;


