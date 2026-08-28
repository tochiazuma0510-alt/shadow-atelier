#############################################################################
## math_kerpi_probe_v1.g -- mathematician (Opus 5), 2026-08-29
## v191 Lemma 1.1: M in J_0 <=> M = sum a_i (U_i - V_i) with pi(U_i)=pi(V_i),
## where pi : G ->> Delta_0 is the COMMON-SOURCE -> ROOF projection.
## v191 line 73: "V175's terms u_i - 1, with u_i in ker pi, are the special
## case in which every V_i = 1."
## ==> the implementer's (U,V) := (srcWord, []) is legitimate IFF
##     srcWord lies in ker(pi), i.e. dies in the roof group Q0.
## THIS SCRIPT DECIDES THAT, and nothing else.
#############################################################################
LoadPackage("json");;
q3 := JsonStringToGap(StringFile(
  "ci/b345_157eh_lexblock_artifacts_32401947156/d972_b345_q3_chief_v1.json"));;

Print("MK_MODELS ", RecNames(q3.coarse_models), "\n");
q0marks := List(q3.coarse_models.Q0.marked_permutations, r -> PermList(List(r, Int)));;
Q0 := Group(q0marks);;
Print("MK_Q0_ORDER ", Size(Q0), "  (expect 1469664)  ngens ", Length(q0marks),
      "  degree ", LargestMovedPoint(Q0), "\n");

srcWord := List(q3.selected_solution.typed_source_word, Int);;
Print("MK_SRCWORD ", srcWord, "\n");
Print("MK_CORRECTION_WORD ", q3.selected_solution.correction_word, "\n");

EvalW := function(w, gx, gy)
  local z, c;
  z := Identity(Q0);;
  for c in w do
    if   c =  1 then z := z*gx;
    elif c = -1 then z := z*gx^-1;
    elif c =  2 then z := z*gy;
    elif c = -2 then z := z*gy^-1;
    else Error("bad letter ", c); fi;
  od;
  return z;
end;;

v := EvalW(srcWord, q0marks[1], q0marks[2]);;
Print("MK_ROOF_VALUE_IS_IDENTITY ", v = Identity(Q0), "\n");
Print("MK_ROOF_VALUE_ORDER ", Order(v), "\n");
## reversed-word control (prepend vs append convention, per WDICT-5)
vr := EvalW(Reversed(srcWord), q0marks[1], q0marks[2]);;
Print("MK_ROOF_VALUE_REV_IS_IDENTITY ", vr = Identity(Q0),
      "  order ", Order(vr), "\n");
## inverse-letter reversal (true word inverse) control
vi := EvalW(Reversed(List(srcWord, c -> -c)), q0marks[1], q0marks[2]);;
Print("MK_ROOF_VALUE_INV_IS_IDENTITY ", vi = Identity(Q0), "\n");
Print("MK_VERDICT srcWord_in_ker_pi ", v = Identity(Q0), "\n");
QUIT;
