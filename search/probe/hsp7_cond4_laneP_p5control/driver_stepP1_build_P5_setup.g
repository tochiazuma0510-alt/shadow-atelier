## search/probe/hsp7_cond4_laneP_p5control/driver_stepP1_build_P5_setup.g
## NW-P7 (p=5 control), Sol限定認可 sol_reply_102_math29.md F102-1.4.
## P-side: P_p := F2/N_F2, N_F2 = gamma_5(F2) F2^p (定義NW(p), hs_prop7_translation_v1.md SS8.7.3).
## Built fresh for p=5 (P101-1/NW-1a/b理論は p>=7 前提のため p=5 で成立するかは
## この control run 自体が確認対象 -- paper-proof の借用はしない).
## h4 word は search/certs/hsp7_cond2_p7_20260804.json stage4_condition2_3_4.P_side.h4_word
## および search/probe/hsp7_cond4_laneP/driver_step1_build_K05_gen_setup.g の jh4 と
## 同一の DUM-FIN 定義(左正規化 group commutator, GAP native Comm, Exp/BCH/Lazard非経由).

Read("search/probe/wac_v1/gap_output_prelude.g");
LoadPackage("anupq");

Print("=== NW-P7 driver stepP1: build P5 = F2/(gamma_5(F2)F2^5) SetupFile ===\n");

F := FreeGroup("x","y");;
x := F.1;; y := F.2;;

## h4 (定義DUM-FIN): Comm(a,b):=a^-1 b^-1 a b (GAP native, left-normalized)
h4 := Comm(Comm(Comm(x,y),x),x) * Comm(Comm(Comm(x,y),x),y)^4
      * Comm(Comm(Comm(x,y),y),y);;
Print("h4 constructed in F2 as a word (same DUM-FIN definition as p=7 P-side/Q-side).\n");

setupFileP := "search/probe/hsp7_cond4_laneP_p5control/pq_setup_P5.txt";;
res := Pq(F : Prime := 5, ClassBound := 4, Exponent := 5, SetupFile := setupFileP);;
Print("Pq(F : Prime:=5, ClassBound:=4, Exponent:=5, SetupFile) returned: ", res, "\n");
Print("SetupFile written to: ", setupFileP, "\n");

Print("STAGEP1_DONE\n");
QUIT;
