#############################################################################
## Task427 v9 one-owner driver. Input/output checkpoints are immutable and distinct.
#############################################################################
D427Producer:="search/d972_r07_a0_pb34_direct_quotient_owner_v9.py";; D427ProducerBytes:=26006;; D427ProducerSHA:="98efac926970a5c3aa23a43b100ae64c52ce60ab0313d151f88b4dc37e6bd611";;
D427Checker:="crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v9.py";; D427CheckerBytes:=7392;; D427CheckerSHA:="641a4af5523ff365d56ccd283d518263a00fc1a397f8b806f8da3698b9edc0de";;
D427Artifact:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v9.json";;
D427Input:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v9_input.checkpoint";; D427Output:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v9_output.checkpoint";;
D427PL:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v9_producer.log";; D427CL:="ci/out/d972_r07_a0_pb34_direct_quotient_owner_v9_checker.log";;
D427Read:=function(p)local x;x:=StringFile(p);if x=fail or Length(x)=0 then Error("task427 missing ",p);fi;return x;end;;
D427Pin:=function(p,n,s)local x;x:=D427Read(p);if n<>Length(x) or Length(s)<>64 or HexSHA256(x)<>s then Error("task427 pin drift ",p);fi;return true;end;;
if not IsBound(D972_R07_A0_PB34_V9_RUN) or D972_R07_A0_PB34_V9_RUN<>true then Error("task427 set D972_R07_A0_PB34_V9_RUN=true");fi;;
if D427ProducerSHA="PENDING" or D427CheckerSHA="PENDING" then Error("task427 pins pending");fi;;
D427Pin(D427Producer,D427ProducerBytes,D427ProducerSHA);;D427Pin(D427Checker,D427CheckerBytes,D427CheckerSHA);;
Exec("mkdir -p ci/out");;if IsExistingFile(D427Output) then Error("task427 output checkpoint already exists; archive it and choose a fresh output path");fi;;
D427Resume:="";;D427InputArg:="";;if IsExistingFile(D427Input) then D427Resume:=Concatenation(" --resume ",D427Input);D427InputArg:=D427Input;fi;;
D427CheckInput:="";;if D427InputArg<>"" then D427CheckInput:=Concatenation(" --input-checkpoint ",D427InputArg);fi;;
Exec(Concatenation("python3 -u -B ",D427Producer," --mode PRODUCTION --seconds 9000 --rss-bytes 4800000000 --output ",D427Artifact," --checkpoint ",D427Output,D427Resume," 2>&1 | tee ",D427PL));;
if PositionSublist(D427Read(D427PL),"R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V9")=fail then Error("task427 producer marker");fi;;
D427A:=D427Read(D427Artifact);;if PositionSublist(D427A,"UNKNOWN_RESOURCE")<>fail and not IsExistingFile(D427Output) then Error("task427 output checkpoint missing");fi;;
Exec(Concatenation("python3 -u -B ",D427Checker," ",D427Artifact,D427CheckInput," --output-checkpoint ",D427Output," 2>&1 | tee ",D427CL));;
if PositionSublist(D427Read(D427CL),"R07_A0_PB34_DIRECT_QUOTIENT_CHECKER_V9_PASS")=fail then Error("task427 checker marker");fi;;
Print("R07_A0_PB34_DIRECT_QUOTIENT_GHA_DRIVER_V9_PASS artifact_sha256=",HexSHA256(D427A),"\n");;


