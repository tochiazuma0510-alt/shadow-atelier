#############################################################################
## A4 v39 RESUME driver for the v21 producer and v27 checker.
## ASCII only.  Semantics and embedded seed ancestry are pinned to exact v38.
#############################################################################
if not IsBound(D386Mode) then Error("task443 MODE required"); fi;
if D386Mode<>"RESUME" then Error("task443 v39 requires RESUME"); fi;

D443V38:="search/d972_r07_word_independent_successor_kernel_gha_driver_v38.g";;
D443V38Bytes:=5283;;
D443V38SHA:="0aa69186576111e5931cd4428c56967432c148cef823d079cf1977ce588465ff";;
D443Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v30.g";;
D443BaseBytes:=76229;;
D443BaseSHA:="bacea39ac0615e0051d5cb59356f45f7fd8b8cd6867bad7b2bc2ec286949575c";;
D443Inner:="ci/out/a4_task443_inner.g";;
D443EmptyHeadBytes:=544;;
D443EmptyHeadSHA:="d324f9b7708802165c05b1581c3f75afedd6f7e43cdbe8a87dbfd270150ec1e5";;
D443OldHeadPathHex:="5f7633382e70726f64756365722e626173652e636865636b706f696e742e6a736f6e";;
D443NewHeadPathHex:="5f7633392e70726f64756365722e626173652e636865636b706f696e742e6a736f6e";;
D443OldHeadSealHex:="35393736643639623538643233373932396364313565376233326263646336633932346262383762303239316662373438623563616263363033343731653933";;
D443NewHeadSealHex:="31373062346465396434623363633130323432353033663961303633306461346465396663626434623439633438323366313063616536333866643463346561";;

D443Read:=function(path)
 local raw;
 raw:=StringFile(path);;
 if raw=fail or Length(raw)=0 then Error("task443 missing input ",path); fi;
 return raw;
end;;
D443Count:=function(raw,needle)
 local i,n,m,count;
 n:=Length(raw);; m:=Length(needle);; count:=0;;
 if m=0 then Error("task443 empty needle"); fi;
 if n<m then return 0; fi;
 for i in [1..n-m+1] do
  if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
 od;
 return count;
end;;
D443ReplaceOnce:=function(raw,old,new)
 if D443Count(raw,old)<>1 then Error("task443 replacement cardinality"); fi;
 return ReplacedString(raw,old,new);
end;;
D443ReplaceAll:=function(raw,old,new)
 if D443Count(raw,old)=0 then Error("task443 version marker absent"); fi;
 while D443Count(raw,old)>0 do raw:=ReplacedString(raw,old,new); od;
 return raw;
end;;

## Extract the exact v38 empty HEAD from its byte-pinned semantic owner, then
## change only its versioned base path and dependent self seal.
D443V38Raw:=D443Read(D443V38);;
if Length(D443V38Raw)<>D443V38Bytes or HexSHA256(D443V38Raw)<>D443V38SHA then
 Error("task443 frozen v38 driver drift");
fi;
D443HeadMarker:="D410EmptyHeadHex:=\"";;
D443HeadStart:=PositionSublist(D443V38Raw,D443HeadMarker);;
if D443HeadStart=fail then Error("task443 v38 HEAD marker"); fi;
D443HeadTail:=D443V38Raw{[D443HeadStart+Length(D443HeadMarker)..Length(D443V38Raw)]};;
D443HeadStop:=PositionSublist(D443HeadTail,"\";;");;
if D443HeadStop=fail then Error("task443 v38 HEAD terminator"); fi;
D443EmptyHeadHex:=D443HeadTail{[1..D443HeadStop-1]};;
D443EmptyHeadHex:=D443ReplaceOnce(D443EmptyHeadHex,D443OldHeadPathHex,D443NewHeadPathHex);;
D443EmptyHeadHex:=D443ReplaceOnce(D443EmptyHeadHex,D443OldHeadSealHex,D443NewHeadSealHex);;
if Length(D443EmptyHeadHex)<>2*D443EmptyHeadBytes then
 Error("task443 empty HEAD hex length");
fi;

D443Raw:=D443Read(D443Base);;
if Length(D443Raw)<>D443BaseBytes or HexSHA256(D443Raw)<>D443BaseSHA then
 Error("task443 frozen v30 driver drift");
fi;
D443Raw:=D443ReplaceAll(D443Raw,"v30","v39");;
D443Pairs:=[
 ["D345Producer:=\\\\\\\"search/d972_r07_word_independent_successor_kernel_v16.py\\\\\\\";;",
  "D345Producer:=\\\\\\\"search/d972_r07_word_independent_successor_kernel_v21.py\\\\\\\";;"],
 ["D345Checker:=\\\\\\\"crosscheck/check_d972_r07_word_independent_successor_kernel_v22.py\\\\\\\";;",
  "D345Checker:=\\\\\\\"crosscheck/check_d972_r07_word_independent_successor_kernel_v27.py\\\\\\\";;"],
 ["[D345Producer,15991,\\\\\\\"bbd2c2093da3f18d2ea298c5d6955d987d4acbfc6eeb2dc9665abdad556bb2a7\\\\\\\"],",
  "[D345Producer,13268,\\\\\\\"23d90839025ae7dafdfef1a358666c640a32844544b4460aecec72644c6e0236\\\\\\\"],"],
 ["[D345Checker,6579,\\\\\\\"91ae327d9a983136cc5a1ac9188dc1ea11f9e553aef606e8bc4bf45cb9bd819a\\\\\\\"],",
  "[D345Checker,21489,\\\\\\\"79f42e751684f12814ac25dc7bd17ee5a6fa21b8ab9b8bdfc07c14bd37e4af2a\\\\\\\"],"],
 ["D345PCheckpoint:=\\\\\\\"ci/out/d972_r07_word_independent_successor_kernel_v39.producer.checkpoint.json\\\\\\\";;",
  "D345PCheckpoint:=\\\\\\\"ci/out/d972_r07_word_independent_successor_kernel_v39.producer.head.checkpoint.json\\\\\\\";;"],
 ["D386InstallSeed(\"ci/out/d972_r07_word_independent_successor_kernel_v39.producer.checkpoint.json\"",
  "D386InstallSeed(\"ci/out/d972_r07_word_independent_successor_kernel_v39.producer.base.checkpoint.json\""],
 [" D386InstallSeed(\"ci/out/d972_r07_word_independent_successor_kernel_v39.checker.checkpoint.json\"",
  Concatenation(" D386InstallSeed(\"ci/out/d972_r07_word_independent_successor_kernel_v39.producer.head.checkpoint.json\",\n",
                "                 D386HexDecode(D443EmptyHeadHex),",String(D443EmptyHeadBytes),",\"",
                D443EmptyHeadSHA,"\");;\n",
                "D386InstallSeed(\"ci/out/d972_r07_word_independent_successor_kernel_v39.checker.checkpoint.json\"")]
];;
for D443Pair in D443Pairs do
 D443Raw:=D443ReplaceOnce(D443Raw,D443Pair[1],D443Pair[2]);;
od;
for D443Pair in D443Pairs do
 if D443Count(D443Raw,D443Pair[1])<>0 or D443Count(D443Raw,D443Pair[2])<>1 then
  Error("task443 post-replacement gate");
 fi;
od;
## D386InstallSeed, inherited byte-for-byte from v38/v30, rejects an existing
## nonempty or corrupt HEAD instead of resetting it to the empty seed.
Exec("mkdir -p ci/out");;
D443Stream:=OutputTextFile(D443Inner,false);;
if D443Stream=fail then Error("task443 inner driver open"); fi;
SetPrintFormattingStatus(D443Stream,false);;
PrintTo(D443Stream,D443Raw);;
CloseStream(D443Stream);;
if D443Read(D443Inner)<>D443Raw then Error("task443 inner readback"); fi;
D386Mode:=D386Mode;;
Read(D443Inner);;
