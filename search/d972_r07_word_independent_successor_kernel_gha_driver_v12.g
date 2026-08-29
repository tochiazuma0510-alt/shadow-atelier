#############################################################################
## R07 task345 v12 checkpoint-accounting repair transport. ASCII only.
#############################################################################
if not IsBound(D345Mode) or D345Mode<>"PRODUCTION" then Error("task345 v12 PRODUCTION required"); fi;
D345V12Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v10.g";;
D345V12Generated:="ci/out/d972_r07_word_independent_successor_kernel_gha_driver_v12.generated.g";;
D345V12Raw:=StringFile(D345V12Base);;
if D345V12Raw=fail or Length(D345V12Raw)<>1900 or
   HexSHA256(D345V12Raw)<>"3f705d1786e0484f0eb56867eb28bdda63bd8b70bd98b243baea1808f5fb88d9" then
 Error("task345 v12 pinned v10 driver drift");
fi;
D345V12ReplaceOnce:=function(raw,old,new)
 local p;
 p:=PositionSublist(raw,old);
 if p=fail or PositionSublist(raw,old,p+1)<>fail then Error("task345 v12 replacement count"); fi;
 return Concatenation(raw{[1..p-1]},new,raw{[p+Length(old)..Length(raw)]});
end;;
D345V12Raw:=D345V12ReplaceOnce(D345V12Raw,
 "ci/out/d972_r07_word_independent_successor_kernel_gha_driver_v10.generated.g",
 "ci/out/d972_r07_word_independent_successor_kernel_gha_driver_v12.generated.g");;
D345V12Raw:=D345V12ReplaceOnce(D345V12Raw,
 "search/d972_r07_word_independent_successor_kernel_v9.py",
 "search/d972_r07_word_independent_successor_kernel_v10.py");;
D345V12Raw:=D345V12ReplaceOnce(D345V12Raw,
 "crosscheck/check_d972_r07_word_independent_successor_kernel_v9.py",
 "crosscheck/check_d972_r07_word_independent_successor_kernel_v10.py");;
D345V12Raw:=D345V12ReplaceOnce(D345V12Raw,
 "[D345Producer,1598,\\\"9982d1dc9c7bce4763fdd44ed12acc802a4c77440241e25bb98b1af4ed5d6ad9\\\"],",
 "[D345Producer,1877,\\\"b4143cb340a7feae4aa5f90a581e63ebd1b692200dbc15dfb0ae2bb4fde9abec\\\"],");;
D345V12Raw:=D345V12ReplaceOnce(D345V12Raw,
 "[D345Checker,1908,\\\"c092bd1b543b13304dba6f0765de143d5090f3cea4d48de69cbbf80e4d590003\\\"],",
 "[D345Checker,2199,\\\"62840c079fb6687a1c43fe13bf3655fbbf5e483ea149037a62f72133566faedc\\\"],");;
PrintTo(D345V12Generated,D345V12Raw);;
Read(D345V12Generated);;
