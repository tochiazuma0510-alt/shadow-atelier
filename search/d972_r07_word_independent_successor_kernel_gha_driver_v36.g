#############################################################################
## A4 v36 RESUME driver for the v19 producer and v25 checker.
## ASCII only.  Resume starts from the exact legacy base plus a sealed
## zero-segment delta HEAD; the first completed row appends segment one.
#############################################################################
if not IsBound(D386Mode) then Error("task410 MODE required"); fi;
if D386Mode<>"RESUME" then Error("task410 v36 requires RESUME"); fi;

D410Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v30.g";;
D410BaseBytes:=76229;;
D410BaseSHA:="bacea39ac0615e0051d5cb59356f45f7fd8b8cd6867bad7b2bc2ec286949575c";;
D410Inner:="ci/out/a4_task410_inner.g";;
D410EmptyHeadBytes:=544;;
D410EmptyHeadSHA:="c6fd5542a4c2d7d45a0f5db4e5443dc7f4beeb711950446e28fded6806b003ba";;
D410EmptyHeadHex:=Concatenation(
 "7b2262617365223a7b226279746573223a32353538312c2270617468223a22643937325f7230375f776f72645f696e646570656e64656e745f737563636573736f725f6b65726e656c5f7633362e70726f64756365722e626173652e636865636b706f696e742e6a736f6e222c22736861323536223a2235393532313362616238393336656631306539346365393063636635323663313035643032643837316334646335643032623663373663623531353933343435227d2c22636861696e223a2230303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030222c226c6173745f726f77223a32342c226c6173745f7365676d656e74223a6e756c6c2c226c6173745f7365676d656e745f736861323536223a6e756c6c2c",
 "226c6173745f73657175656e6365223a302c226e6578745f726f77223a32352c226f776e6572223a2270726f6475636572222c22736368656d61223a22643937322d7230372d776f72642d696e646570656e64656e742d737563636573736f722d6b65726e656c2f76362f686561642f7631222c227365676d656e745f636f756e74223a302c2273656c665f6469676573745f736861323536223a2231323163353264613862316366303439306165346261393261303463626133333963663034656435323061306266343832343831393864393437613131656430227d");;
D410Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task410 missing input ",path); fi;
 return raw;
end;;
D410Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);; m:=Length(needle);; count:=0;;
 if m=0 then Error("task410 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;
D410ReplaceOnce:=function(raw,old,new)
 if D410Count(raw,old)<>1 then Error("task410 replacement cardinality"); fi;
 return ReplacedString(raw,old,new);
end;;
D410ReplaceAll:=function(raw,old,new)
 local count;
 count:=D410Count(raw,old);;
 if count=0 then Error("task410 version marker absent"); fi;
 while D410Count(raw,old)>0 do raw:=ReplacedString(raw,old,new); od;
 return raw;
end;;

D410Raw:=D410Read(D410Base);;
if Length(D410Raw)<>D410BaseBytes or HexSHA256(D410Raw)<>D410BaseSHA then
 Error("task410 frozen v31 driver drift");
fi;
D410Raw:=D410ReplaceAll(D410Raw,"v30","v36");;
D410Pairs:=[
 ["D345Producer:=\\\\\\\"search/d972_r07_word_independent_successor_kernel_v16.py\\\\\\\";;",
  "D345Producer:=\\\\\\\"search/d972_r07_word_independent_successor_kernel_v19.py\\\\\\\";;"],
 ["D345Checker:=\\\\\\\"crosscheck/check_d972_r07_word_independent_successor_kernel_v22.py\\\\\\\";;",
  "D345Checker:=\\\\\\\"crosscheck/check_d972_r07_word_independent_successor_kernel_v25.py\\\\\\\";;"],
 ["[D345Producer,15991,\\\\\\\"bbd2c2093da3f18d2ea298c5d6955d987d4acbfc6eeb2dc9665abdad556bb2a7\\\\\\\"],",
  "[D345Producer,2388,\\\\\\\"c7add6648f53e4ec85eb40620e3469008349e5676ac7d9602a6699a52cb4c6c1\\\\\\\"],"],
 ["[D345Checker,6579,\\\\\\\"91ae327d9a983136cc5a1ac9188dc1ea11f9e553aef606e8bc4bf45cb9bd819a\\\\\\\"],",
  "[D345Checker,2540,\\\\\\\"4c04fd31fe4a27c96841ddc5931961cc6d2e4162f98f239df3577ee367a57317\\\\\\\"],"],
 ["D345PCheckpoint:=\\\\\\\"ci/out/d972_r07_word_independent_successor_kernel_v36.producer.checkpoint.json\\\\\\\";;",
  "D345PCheckpoint:=\\\\\\\"ci/out/d972_r07_word_independent_successor_kernel_v36.producer.head.checkpoint.json\\\\\\\";;"],
 ["D386InstallSeed(\"ci/out/d972_r07_word_independent_successor_kernel_v36.producer.checkpoint.json\"",
  "D386InstallSeed(\"ci/out/d972_r07_word_independent_successor_kernel_v36.producer.base.checkpoint.json\""],
 [" D386InstallSeed(\"ci/out/d972_r07_word_independent_successor_kernel_v36.checker.checkpoint.json\"",
  " D386InstallSeed(\"ci/out/d972_r07_word_independent_successor_kernel_v36.producer.head.checkpoint.json\",\n                 D386HexDecode(D410EmptyHeadHex),D410EmptyHeadBytes,D410EmptyHeadSHA);;\n D386InstallSeed(\"ci/out/d972_r07_word_independent_successor_kernel_v36.checker.checkpoint.json\""],
];;
for D410Pair in D410Pairs do
 D410Raw:=D410ReplaceOnce(D410Raw,D410Pair[1],D410Pair[2]);;
od;
for D410Pair in D410Pairs do
 if D410Count(D410Raw,D410Pair[1])<>0 or D410Count(D410Raw,D410Pair[2])<>1 then
  Error("task410 post-replacement gate");
 fi;
od;
Exec("mkdir -p ci/out");;
D410Stream:=OutputTextFile(D410Inner,false);;
if D410Stream=fail then Error("task410 inner driver open"); fi;
SetPrintFormattingStatus(D410Stream,false);;
PrintTo(D410Stream,D410Raw);;
CloseStream(D410Stream);;
if D410Read(D410Inner)<>D410Raw then Error("task410 inner readback"); fi;
D386Mode:=D386Mode;;
Read(D410Inner);;
