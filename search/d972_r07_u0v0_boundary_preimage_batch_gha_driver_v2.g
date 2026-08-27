#############################################################################
## Task191 batched boundary-preimage driver v2. ASCII only; serial.
#############################################################################
if not IsBound(D972_R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_MODE) then Error("task191 driver: MODE must be SELFTEST or PRODUCTION"); fi;
D191Mode:=D972_R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_MODE;;
if not IsString(D191Mode) or (D191Mode<>"SELFTEST" and D191Mode<>"PRODUCTION") then Error("task191 driver: invalid MODE"); fi;
D191Resume:="";;
if not IsBound(D972_R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_RESUME) then
  D191Resume:="";
else
  D191Resume:=D972_R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_RESUME;
fi;
D191SafeResume:=function(path) local c;
  if not IsString(path) then Error("task191 driver: invalid RESUME type"); fi;
  if path="" then return true; fi;
  if Position("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_",path[1])=fail or
     PositionSublist(path,"..")<>fail then Error("task191 driver: unsafe RESUME path"); fi;
  for c in path do
    if Position("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_./-",c)=fail then
      Error("task191 driver: unsafe RESUME path");
    fi;
  od;
  return true;
end;;
D191SafeResume(D191Resume);;
if D191Mode="SELFTEST" and D191Resume<>"" then Error("task191 driver: SELFTEST cannot resume"); fi;
D191ResumeArg:="";; if D191Resume<>"" then D191ResumeArg:=Concatenation(" --resume ",D191Resume); fi;
D191Producer:="search/d972_r07_u0v0_boundary_preimage_batch_v2.py";;
D191Checker:="crosscheck/check_d972_r07_u0v0_boundary_preimage_batch_v2.py";;
D191Fixture:="search/certs/d972_r07_u0v0_boundary_preimage_batch_selftest_v2_20260827.json";;
D191Receipt:="ci/out/d972_r07_u0v0_boundary_preimage_batch_v2.json";;
D191ProducerLog:="ci/out/d972_r07_u0v0_boundary_preimage_batch_v2.producer.log";;
D191CheckerLog:="ci/out/d972_r07_u0v0_boundary_preimage_batch_v2.checker.log";;
D191Shell:="ci/out/d972_r07_u0v0_boundary_preimage_batch_v2.sh";;
D191OK:="ci/out/d972_r07_u0v0_boundary_preimage_batch_v2.ok";;
D191Checkpoint:="ci/out/d972_r07_u0v0_boundary_preimage_batch_v2.checkpoint.json";;
D191Common:="R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2";;
D191ResourceTerminal:="UNKNOWN_RESOURCE:(task175_reconstruction:(wall_seconds|rss_bytes)|fine_deletion:(wall_seconds|rss_bytes)|Q0_positive_shortlex_section:(wall_seconds|rss_bytes)|Q0_discovery:(wall_seconds|rss_bytes)|A_L_membership_scan:(wall_seconds|rss_bytes)|L_subgroup_closure:(wall_seconds|rss_bytes)|typed_singleton_equality:(wall_seconds|rss_bytes)|runtime_reconstruction:(wall_seconds|rss_bytes)|complete_boundary_correlation:(wall_seconds|rss_bytes|boundary_pairs|oracle_rounds)|boundary_echelon:(wall_seconds|rss_bytes|retained_columns)|checkpoint_serialization:(checkpoint_bytes)):[-+0-9.eE]+>[-+0-9.eE]+";;
D191InputTerminal:="UNKNOWN_INPUT:(pin:|v1 loader|task179:).*";;
D191Terminal:=Concatenation("(",D191Common,"|",D191ResourceTerminal,"|",D191InputTerminal,")");;
D191Current:=[
  [D191Producer,92528,"9e5a742e08c5c711dfb20bca9b3fa4f0d079c9b6fa588fbcd3f7d3a259ef9dc9"],
  [D191Checker,68823,"8dad4ca4fc0cb3e942c9ea3c7ea0a3da1339f2bbe683953c8518f511f5b85eac"],
  [D191Fixture,1396,"fe5e2adbb35d7594ea3ddebff654772a906236067623ac0d5f34bc5ad3e73b34"]
];;
D191Predecessor:=[
 ["search/d972_r07_u0v0_boundary_preimage_v1.py",35173,"18040f4f73fe963632bbd2200e730818a7354c5963143a5871e73b2d1284dbfe"],
 ["crosscheck/check_d972_r07_u0v0_boundary_preimage_v1.py",32825,"e94d19311d0afe23fde869045f959490528d18e0f3537209e57b7cbefb452b18"],
 ["search/d972_r07_u0v0_boundary_preimage_gha_driver_v1.g",7721,"16d354d387db53cfadd22a7442f9a7aa77580c8410664f9dd5b1a618fef026b8"],
 ["search/certs/d972_r07_u0v0_boundary_preimage_selftest_v1_20260827.json",699,"230de05643a94f775120ef7e62b2f2023b13fd12228f18ca860ef81b134babff"],
 ["search/d972_r07_positive_common_word_colgen_v1.py",123870,"47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"],
 ["crosscheck/check_d972_r07_positive_common_word_colgen_v1.py",73780,"de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"],
 ["search/d972_r07_positive_common_word_colgen_gha_driver_v1.g",12872,"48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"],
 ["search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json",407,"46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"],
 ["sol/proof_r07_task179_exact_exponent_lattice_v156.md",10409,"2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d"],
 ["sol/proof_r07_all_rung_exact_charming_lattice_selector_v157.md",8367,"08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8"]
];;
D191Read:=function(path) local raw; raw:=StringFile(path); if raw=fail or Length(raw)=0 then Error("task191 driver: missing ",path); fi; return raw; end;;
D191Pin:=function(row) local raw; raw:=D191Read(row[1]); if row[2]>0 and (Length(raw)<>row[2] or HexSHA256(raw)<>row[3]) then Error("task191 driver: pin drift ",row[1]); fi; end;;
D191Reject:=function(paths) local p; if Length(paths)<>Length(Set(paths)) then Error("task191 driver: duplicate output"); fi; for p in paths do if IsExistingFile(p) then Error("task191 driver: stale output ",p); fi; od; end;;
for D191Row in D191Predecessor do D191Pin(D191Row); od; for D191Row in D191Current do D191Pin(D191Row); od;
D191Reject([D191Receipt,D191ProducerLog,D191CheckerLog,D191Shell,D191OK,D191Checkpoint]);
if D191Resume<>"" then
  if not IsExistingFile(D191Resume) then Error("task191 driver: missing RESUME input ",D191Resume); fi;
  if D191Resume=D191Checkpoint then Error("task191 driver: RESUME must differ from output checkpoint"); fi;
fi;
D191Stream:=OutputTextFile(D191Shell,false);; if D191Stream=fail then Error("task191 driver: shell open"); fi; SetPrintFormattingStatus(D191Stream,false);
PrintTo(D191Stream,"#!/usr/bin/env bash\nset -euo pipefail\nmkdir -p ci/out\n");
if D191Mode="SELFTEST" then
  PrintTo(D191Stream,"if ! python3 -u -B ",D191Producer," --selftest --output ",D191Receipt," > ",D191ProducerLog," 2>&1; then cat ",D191ProducerLog,"; exit 1; fi\ncat ",D191ProducerLog,"\nprintf 'R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_STAGE=producer_process\\n'\ngrep -Fxc 'R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_PRODUCER_SELFTEST_PASS' ",D191ProducerLog," | grep -qx 1\n");
  PrintTo(D191Stream,"if ! python3 -u -B ",D191Checker," ",D191Receipt," --selftest > ",D191CheckerLog," 2>&1; then cat ",D191CheckerLog,"; exit 1; fi\ncat ",D191CheckerLog,"\nprintf 'R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_STAGE=checker_process\\n'\nIFS= read -r checker_line < ",D191CheckerLog,"\ntest \"$checker_line\" = 'R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_CHECKER_PASS terminal=R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_SELFTEST_PASS'\ntest \"$(wc -l < ",D191CheckerLog,")\" -eq 1\n");
else
  PrintTo(D191Stream,"if ! python3 -u -B ",D191Producer," --mode PRODUCTION --output ",D191Receipt," --checkpoint ",D191Checkpoint," --seconds 19800 --boundary-pairs 8000000 --retained-columns 250000 --checkpoint-bytes 4000000000 --oracle-rounds 1000000 --rss-bytes 5700000000",D191ResumeArg," > ",D191ProducerLog," 2>&1; then cat ",D191ProducerLog,"; exit 1; fi\ncat ",D191ProducerLog,"\nprintf 'R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_STAGE=producer_process\\n'\ngrep -Ec '^R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_PRODUCER_TERMINAL ",D191Terminal,"$' ",D191ProducerLog," | grep -qx 1\n");
  PrintTo(D191Stream,"if ! python3 -u -B ",D191Checker," ",D191Receipt," > ",D191CheckerLog," 2>&1; then cat ",D191CheckerLog,"; exit 1; fi\ncat ",D191CheckerLog,"\nprintf 'R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_STAGE=checker_process\\n'\ngrep -Ec '^R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_CHECKER_PASS terminal=",D191Terminal,"$' ",D191CheckerLog," | grep -qx 1\nproducer_terminal=$(grep -E '^R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_PRODUCER_TERMINAL ' ",D191ProducerLog," | sed -E 's/^R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_PRODUCER_TERMINAL //'); test $(printf '%s\\n' \"$producer_terminal\" | wc -l) -eq 1\nchecker_terminal=$(grep -E '^R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_CHECKER_PASS terminal=' ",D191CheckerLog," | sed -E 's/^R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_CHECKER_PASS terminal=//'); test $(printf '%s\\n' \"$checker_terminal\" | wc -l) -eq 1\ntest \"$producer_terminal\" = \"$checker_terminal\"\n");
fi;
PrintTo(D191Stream,"printf 'R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_OK\\n' > ",D191OK,"\n"); PrintTo(D191Stream,"test \"$(wc -l < ",D191OK,")\" -eq 1\ntest \"$(cat ",D191OK,")\" = 'R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_OK'\n"); CloseStream(D191Stream);
Exec(Concatenation("bash ",D191Shell));
D191Sentinel:=D191Read(D191OK);;
if D191Sentinel<>"R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_OK\n" then Error("task191 driver: invalid completion sentinel"); fi;
if D191Mode="SELFTEST" then Print("R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_GHA_DRIVER_PASS mode=SELFTEST terminal=R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_SELFTEST_PASS\n");
else Print("R07_U0V0_BOUNDARY_PREIMAGE_BATCH_V2_GHA_DRIVER_PASS mode=PRODUCTION terminal=AUTHENTICATED_CHECKER_TERMINAL\n"); fi;
