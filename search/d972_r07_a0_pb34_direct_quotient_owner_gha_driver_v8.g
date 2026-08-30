#############################################################################
## Task426 v8 one-owner driver. Input/output checkpoints are immutable and distinct.
#############################################################################
D426Producer:="search/d972_r07_a0_pb34_direct_quotient_owner_v8.py";; D426ProducerBytes:=26006;; D426ProducerSHA:="777955b05c919a3b2c5f108e84e10e672f44ea259dd85ac4a343116aae08b5fc";;
D426Checker:="crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v8.py";; D426CheckerBytes:=7390;; D426CheckerSHA:="a3ad40ec2dc92ca8213905b858edca92cbdfacf1a700e6715624edec985d3976";;
D426Artifact:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v8.json";;
D426Input:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v8_input.checkpoint";; D426Output:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v8_output.checkpoint";;
D426PL:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v8_producer.log";; D426CL:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v8_checker.log";;
D426Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task426 missing ",p);fi;return x;end;;
D426Pin:=function(p,n,s)local x;x:=D426Read(p);if n<>Length(x) or Length(s)<>64 or HexSHA256(x)<>s then Error("task426 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_PB34_V8_RUN) or D972_R07_A0_PB34_V8_RUN<>true then Error("task426 set D972_R07_A0_PB34_V8_RUN=true");fi;;
if D426ProducerSHA="PENDING" or D426CheckerSHA="PENDING" then Error("task426 pins pending");fi;;
D426Pin(D426Producer,D426ProducerBytes,D426ProducerSHA);;D426Pin(D426Checker,D426CheckerBytes,D426CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D426Output) then Error("task426 output checkpoint already exists; archive it and choose a fresh output path");fi;;
D426Resume:="";;D426InputArg:="";;if IsExistingFile(D426Input) then D426Resume:=Concatenation(" --resume ",D426Input);D426InputArg:=D426Input;fi;;
D426CheckInput:="";;if D426InputArg<>"" then D426CheckInput:=Concatenation(" --input-checkpoint ",D426InputArg);fi;;
Exec(Concatenation("python3 -u -B ",D426Producer," --mode PRODUCTION --seconds 9000 --rss-bytes 4800000000 --output ",D426Artifact," --checkpoint ",D426Output,D426Resume," 2>&1 | tee ",D426PL));;
if PositionSublist(D426Read(D426PL),"R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V8")=fail then Error("task426 producer marker");fi;;
D426A:=D426Read(D426Artifact);;if PositionSublist(D426A,"UNKNOWN_RESOURCE")<>fail and not IsExistingFile(D426Output) then Error("task426 output checkpoint missing");fi;;
Exec(Concatenation("python3 -u -B ",D426Checker," ",D426Artifact,D426CheckInput," --output-checkpoint ",D426Output," 2>&1 | tee ",D426CL));;
if PositionSublist(D426Read(D426CL),"R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V8_PASS")=fail then Error("task426 checker marker");fi;;
Print("R07_A0_PB34_DIRECT_QUOTIENT_GHA_DRIVER_V8_PASS artifact_sha256=",HexSHA256(D426A),"\n");;

