#############################################################################
## R07 task345 v15 bridge-index repair transport. ASCII only.
#############################################################################
if not IsBound(D345Mode) or D345Mode<>"PRODUCTION" then Error("task345 v15 PRODUCTION required"); fi;
D345V15Base:="search/d972_r07_word_independent_successor_kernel_gha_driver_v10.g";;
D345V15Generated:="ci/out/d972_r07_word_independent_successor_kernel_gha_driver_v15.generated.g";;
D345V15Raw:=StringFile(D345V15Base);;
if D345V15Raw=fail or Length(D345V15Raw)<>1900 or
   HexSHA256(D345V15Raw)<>"3f705d1786e0484f0eb56867eb28bdda63bd8b70bd98b243baea1808f5fb88d9" then
 Error("task345 v15 pinned v10 driver drift");
fi;
D345V15ReplaceOnce:=function(raw,old,new)
 local p;
 p:=PositionSublist(raw,old);
 if p=fail or PositionSublist(raw,old,p+1)<>fail then Error("task345 v15 replacement count"); fi;
 return Concatenation(raw{[1..p-1]},new,raw{[p+Length(old)..Length(raw)]});
end;;
D345V15Raw:=D345V15ReplaceOnce(D345V15Raw,
 "search/d972_r07_word_independent_successor_kernel_v9.py",
 "search/d972_r07_word_independent_successor_kernel_v11.py");;
D345V15Raw:=D345V15ReplaceOnce(D345V15Raw,
 "crosscheck/check_d972_r07_word_independent_successor_kernel_v9.py",
 "crosscheck/check_d972_r07_word_independent_successor_kernel_v11.py");;
D345V15Raw:=D345V15ReplaceOnce(D345V15Raw,"1598","2038");;
D345V15Raw:=D345V15ReplaceOnce(D345V15Raw,
 "9982d1dc9c7bce4763fdd44ed12acc802a4c77440241e25bb98b1af4ed5d6ad9",
 "f3cccb104402ee031baba59487a8e4f71dbe8fb244ff220db96f8814950f868e");;
D345V15Raw:=D345V15ReplaceOnce(D345V15Raw,"1908","2376");;
D345V15Raw:=D345V15ReplaceOnce(D345V15Raw,
 "c092bd1b543b13304dba6f0765de143d5090f3cea4d48de69cbbf80e4d590003",
 "552e7d866574fe6d92bf3586c63ff2640057d19b77b6e982078c52b9ae896026");;
PrintTo(D345V15Generated,D345V15Raw);;
Read(D345V15Generated);;
