#############################################################################
## R07 task345 v8 transport correction over the pinned v7 repair driver.
#############################################################################
if not IsBound(D345Mode) or D345Mode<>"PRODUCTION" then
 Error("task345 v8 PRODUCTION required");
fi;

D345V8Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v7.g";;
D345V8Generated:="ci/out/d972_r07_word_independent_successor_kernel_gha_driver_v8.generated.g";;
D345V8Raw:=StringFile(D345V8Base);;
if D345V8Raw=fail or Length(D345V8Raw)<>3899 or
   HexSHA256(D345V8Raw)<>"10bab698585077ac5965c3b54b0971b43c74a92829a14b2407f216d2f6b623ce" then
 Error("task345 v8 pinned v7 driver drift");
fi;

D345V8Needle:="PrintTo(D345V7Generated,D345V7Raw);;";;
D345V8Insertion:=Concatenation(
 "D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,\n",
 " \"D345Driver:=\\\"search/d972_r07_word_independent_successor_kernel_gha_driver_v7.g\\\";;\",\n",
 " \"D345Driver:=\\\"search/d972_r07_word_independent_successor_kernel_gha_driver_v8.g\\\";;\");;\n",
 "D345V7Raw:=D345V7ReplaceOnce(D345V7Raw,\n",
 " \"Exec(\\\"bash ci/out/d972_r07_word_independent_successor_kernel_v6.sh\\\");\",\n",
 " \"Exec(\\\"bash ci/out/d972_r07_word_independent_successor_kernel_v7.sh\\\");\");;\n",
 D345V8Needle);;
D345V8At:=PositionSublist(D345V8Raw,D345V8Needle);;
if D345V8At=fail or PositionSublist(D345V8Raw,D345V8Needle,D345V8At+1)<>fail then
 Error("task345 v8 insertion count");
fi;
D345V8Raw:=Concatenation(
 D345V8Raw{[1..D345V8At-1]},D345V8Insertion,
 D345V8Raw{[D345V8At+Length(D345V8Needle)..Length(D345V8Raw)]});;
PrintTo(D345V8Generated,D345V8Raw);;
Read(D345V8Generated);;
