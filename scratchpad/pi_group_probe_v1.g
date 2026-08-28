Read("scratchpad/pi_values_export.g");;
H := Group(PIV);;
Print("PI_COUNT ", Length(PIV), "\n");
Print("PI_GROUP_ORDER ", Size(H), "\n");
Print("PI_ORDER_IS_504 ", Size(H) = 504, "  IsSimple ", IsSimple(H),
      "  NrMovedPoints ", NrMovedPoints(H), "\n");
S := PSL(2,8);;
G := PGammaL(2,8);;
Print("PSL28_order ", Size(S), "  PGammaL28_order ", Size(G),
      "  index ", Size(G)/Size(S), "\n");
Print("PI_CONJ_TO_PSL28 ", RepresentativeAction(SymmetricGroup(9), H, S) <> fail, "\n");
Print("PI_ALL_27_INSIDE_H ", ForAll(PIV, p -> p in H), "\n");
Print("VERDICT Psi_pi_is_identically_zero ", Size(H) = 504, "\n");
QUIT;
