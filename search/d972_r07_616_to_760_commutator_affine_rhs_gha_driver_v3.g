#############################################################################
## R07 616-to-760 commutator affine-RHS GHA driver v3.
## ASCII only.  Full mode uses one producer process followed by one
## independent checker process under one common 18000-second budget.
#############################################################################

D972R760V3Producer :=
  "search/d972_r07_616_to_760_commutator_affine_rhs_v3.py";;
D972R760V3Checker :=
  "search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py";;
D972R760V3Artifact :=
  "ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3.json";;
D972R760V3Q3Source :=
  "ci/b345_157dp_artifacts_32171982444/d972_b345_q3_chief_v1.json";;
D972R760V3Q3Runtime := "ci/out/d972_b345_q3_chief_v1.json";;
D972R760V3Preflight :=
  "search/certs/d972_r07_616_to_760_commutator_affine_rhs_preflight_v3_20260826.json";;

D972R760V3Pins := [
  [D972R760V3Producer,
   "db945914f2ed84329ca296e03732c6c4a16035f5181cecb683d12bdfca1f6377",39385],
  [D972R760V3Checker,
   "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f",33409],
  [D972R760V3Preflight,
   "55752b6c1a748fb0b25a86d6fc1a0381a82b203112568b0b1963c5665cef0408",184890],
  ["sol/luna_task_162_r07_760_commutator_affine_rhs_v3.md",
   "8ca38afc6f30e8e6074f191a17541f508f29ba1da58d3b286ba4fcf33406ae21",4053],
  ["sol/proof_r07_goursat_nakayama_onto_v88.md",
   "e0d8ff49963ef0cb98312e5ee288ed0744a42fd7d2dd6e0b8450439e28fe329b",4254],
  ["sol/audit_r07_616_e4_relation_onto_v89.md",
   "0b965baa8bade54c3e3784df64fdfe6f440824518f2c21174e26122f452d4244",4388],
  ["sol/proof_r07_joint_derived_commutator_rebase_v92.md",
   "cc56e2187fac08ffa70fe3753e200627e776b5fa591738dee5da908e4d217387",5969],
  ["sol/proof_r07_left_right_a18_basechange_v93.md",
   "5adc49196b7ac0c9d7472f5de0c77af9919b945304f6732e8ea182899308660e",4578],
  ["sol/proof_r07_frattini_invisible_onto_stability_v94.md",
   "fee0868727bc027d002d19200a73ac0292d76bb04d95e88553cbfa0e29942840",6506],
  [D972R760V3Q3Source,
   "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72",231570],
  ["search/d972_b345_target6_dual_colgen_v1.py",
   "8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc",410757],
  ["search/check_d972_b345_target6_dual_colgen_v1.py",
   "08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e",228980]
];;

D972R760V3SelfLog :=
  "ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_selftest.log";;
D972R760V3SelfOK :=
  "ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_selftest.ok";;
D972R760V3ProducerLog :=
  "ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_producer.log";;
D972R760V3CheckerLog :=
  "ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_checker.log";;
D972R760V3MathOK :=
  "ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_math.ok";;
D972R760V3Timing :=
  "ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_timing.txt";;

D972R760V3Read := function(path,label)
  local raw;
  raw:=StringFile(path);;
  if raw=fail or Length(raw)=0 then
    Error("R07 760 v3 driver: missing or empty ",label);
  fi;
  return raw;
end;;

D972R760V3Count := function(raw,needle)
  local i,n,m,count;
  if not IsString(raw) or not IsString(needle) or Length(needle)=0 then
    Error("R07 760 v3 driver: count input");
  fi;
  n:=Length(raw);; m:=Length(needle);; count:=0;;
  if n<m then return 0; fi;
  for i in [1..n-m+1] do
    if raw{[i..i+m-1]}=needle then count:=count+1;; fi;
  od;
  return count;
end;;

D972R760V3Pin := function(row)
  local raw,got;
  if not IsList(row) or Length(row)<>3 then
    Error("R07 760 v3 driver: malformed pin");
  fi;
  raw:=D972R760V3Read(row[1],row[1]);; got:=HexSHA256(raw);;
  if Length(raw)<>row[3] or got<>row[2] then
    Error("R07 760 v3 driver: pin drift ",row[1]," sha=",got,
          " bytes=",Length(raw));
  fi;
  return true;
end;;

D972R760V3CleanLog := function(raw,label)
  local token;
  for token in ["Traceback (most recent call last):", "SyntaxError",
                "Error,", " FAIL ", "failed"] do
    if D972R760V3Count(raw,token)<>0 then
      Error("R07 760 v3 driver: forbidden log token ",label," ",token);
    fi;
  od;
  return true;
end;;

for D972R760V3PinRow in D972R760V3Pins do
  D972R760V3Pin(D972R760V3PinRow);;
od;

D972R760V3Self :=
  IsBound(D972_R07_760_COMMUTATOR_AFFINE_RHS_V3_SELFTEST) and
  D972_R07_760_COMMUTATOR_AFFINE_RHS_V3_SELFTEST=true;;
D972R760V3Run :=
  IsBound(D972_R07_760_COMMUTATOR_AFFINE_RHS_V3_RUN) and
  D972_R07_760_COMMUTATOR_AFFINE_RHS_V3_RUN=true;;
if D972R760V3Self=D972R760V3Run then
  Error("R07 760 v3 driver: select exactly one mode");
fi;

if D972R760V3Self then
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_selftest.log' 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_selftest.ok' && python3 -u -B search/d972_r07_616_to_760_commutator_affine_rhs_v3.py --self-test > 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_selftest.log' 2>&1 && python3 -u -B search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py --self-test >> 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_selftest.log' 2>&1 && python3 -u -B search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py --receipt search/certs/d972_r07_616_to_760_commutator_affine_rhs_preflight_v3_20260826.json --mutations >> 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_selftest.log' 2>&1 && printf '%s' 'D972_R07_760_V3_SELFTEST_EXIT_ZERO' > 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_selftest.ok'");;
  if D972R760V3Read(D972R760V3SelfOK,"selftest sentinel")<>
       "D972_R07_760_V3_SELFTEST_EXIT_ZERO" then
    Error("R07 760 v3 driver: selftest process");
  fi;
  D972R760V3Raw:=D972R760V3Read(D972R760V3SelfLog,"selftest log");;
  D972R760V3CleanLog(D972R760V3Raw,"selftest");;
  if D972R760V3Count(D972R760V3Raw,
       "R07_760_COMMUTATOR_AFFINE_RHS_V3_PRODUCER_SELFTEST_PASS")<>1 or
     D972R760V3Count(D972R760V3Raw,
       "R07_760_COMMUTATOR_AFFINE_RHS_V3_CHECKER_SELFTEST_PASS")<>1 or
     D972R760V3Count(D972R760V3Raw,
       "R07_760_COMMUTATOR_AFFINE_RHS_V3_CHECKER_PASS")<>1 or
     D972R760V3Count(D972R760V3Raw,"mutations=7")<>2 then
    Error("R07 760 v3 driver: selftest marker count");
  fi;
  Print("R07_760_COMMUTATOR_AFFINE_RHS_V3_GHA_DRIVER_PASS ",
        "mode=selftest preflight_checker=1 mutations=7\n");;
else
  Exec("mkdir -p 'ci/out' && rm -f 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3.json' 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_producer.log' 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_checker.log' 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_math.ok' 'ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_timing.txt' && cp 'ci/b345_157dp_artifacts_32171982444/d972_b345_q3_chief_v1.json' 'ci/out/d972_b345_q3_chief_v1.json' && bash -o pipefail -c 'set -e; SECONDS=0; python3 -u -B search/d972_r07_616_to_760_commutator_affine_rhs_v3.py --full --seconds 18000 --output ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3.json 2>&1 | tee ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_producer.log; producer_elapsed=$SECONDS; remaining=$((18000-SECONDS)); if [ $remaining -le 0 ]; then exit 97; fi; python3 -u -B search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py --full --mutations --seconds $remaining --receipt ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3.json 2>&1 | tee ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_checker.log; final_elapsed=$SECONDS; final_margin=$((18000-final_elapsed)); if [ $final_margin -le 0 ]; then exit 98; fi; printf \"producer_elapsed=%s\nchecker_initial_remaining=%s\nfinal_elapsed=%s\nfinal_margin=%s\n\" $producer_elapsed $remaining $final_elapsed $final_margin > ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_timing.txt; printf %s D972_R07_760_V3_MATH_EXIT_ZERO > ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3_math.ok'");;
  if D972R760V3Read(D972R760V3MathOK,"math sentinel")<>
       "D972_R07_760_V3_MATH_EXIT_ZERO" then
    Error("R07 760 v3 driver: producer/checker process");
  fi;
  D972R760V3PRaw:=D972R760V3Read(D972R760V3ProducerLog,"producer log");;
  D972R760V3CRaw:=D972R760V3Read(D972R760V3CheckerLog,"checker log");;
  D972R760V3CleanLog(D972R760V3PRaw,"producer");;
  D972R760V3CleanLog(D972R760V3CRaw,"checker");;
  if D972R760V3Count(D972R760V3PRaw,
       "R07_760_COMMUTATOR_AFFINE_RHS_V3_PRODUCER_PASS")<>1 or
     D972R760V3Count(D972R760V3CRaw,
       "R07_760_COMMUTATOR_AFFINE_RHS_V3_CHECKER_PASS")<>1 then
    Error("R07 760 v3 driver: final marker count");
  fi;
  D972R760V3Receipt:=D972R760V3Read(D972R760V3Artifact,"artifact");;
  D972R760V3ReceiptSHA:=HexSHA256(D972R760V3Receipt);;
  if D972R760V3Count(D972R760V3PRaw,
       Concatenation("sha256=",D972R760V3ReceiptSHA))<>1 or
     D972R760V3Count(D972R760V3PRaw,
       Concatenation("bytes=",String(Length(D972R760V3Receipt))))<>1 or
     D972R760V3Count(D972R760V3CRaw,
       Concatenation("receipt_sha256=",D972R760V3ReceiptSHA))<>1 then
    Error("R07 760 v3 driver: artifact binding");
  fi;
  D972R760V3TerminalCount:=0;;
  for D972R760V3Token in ["R07_760_AFFINE_RHS_READY",
      "R07_760_AFFINE_UNKNOWN_RESOURCE", "R07_760_AFFINE_INPUT_STOP"] do
    D972R760V3TerminalCount:=D972R760V3TerminalCount+
      D972R760V3Count(D972R760V3PRaw,
        Concatenation("terminal=",D972R760V3Token));;
  od;
  if D972R760V3TerminalCount<>1 then
    Error("R07 760 v3 driver: exclusive terminal");
  fi;
  Print("R07_760_COMMUTATOR_AFFINE_RHS_V3_GHA_DRIVER_PASS mode=full ",
        "artifact_sha256=",D972R760V3ReceiptSHA,
        " bytes=",Length(D972R760V3Receipt),"\n");;
fi;
