# math_omega2_comm_cube_v1.g
# Purpose: decide whether [r_x,r_y]^3 lies in Omega = ker(Theta: F(x,y) -> Delta),
# i.e. whether the difference between the two readings comm^(-1) (v547 signed)
# and comm^(+2) (v548 section5 literal) is trivial in Delta.
# Inputs: scratchpad/a0_v2_prelude.g (DeltaJ, Gam, JointImg), scratchpad/a0_v2_qraw.g (19 raw Q0 relators).
# r_x = q1 * q6^-2 * q7^4 * q9 ; r_y = q8^-1 * q4^-1   (v459 (2.1) / v547 (1.2))
Read("scratchpad/a0_v2_prelude.g");;
SetPrintFormattingStatus("*stdout*", false);;
T0 := Runtime();;
qimg := List(A0V2_QRAW, JointImg);;
a := qimg[1]*qimg[6]^-2*qimg[7]^4*qimg[9];;
b := qimg[8]^-1*qimg[4]^-1;;
one := One(DeltaJ);;
c := a^-1*b^-1*a*b;;
Print("OM2 delta_order ", Size(DeltaJ), " gamma_order ", Size(Gam), "\n");
Print("OM2 a_in_Gamma0 ", a in Gam, " b_in_Gamma0 ", b in Gam, "\n");
Print("OM2 a_is_one ", a = one, " b_is_one ", b = one, " a_order ", Order(a), " b_order ", Order(b), "\n");
D := DerivedSubgroup(Gam);;
Print("OM2 Gamma0_derived_order ", Size(D), " comm_in_Gamma0_derived ", c in D, "\n");
Print("OM2 comm_is_one ", c = one, " comm_order ", Order(c), "\n");
Print("OM2 COMM_CUBE_IS_ONE ", c^3 = one, "   (TRUE <=> [r_x,r_y]^3 in Omega)\n");
Print("OM2 comm_inv_eq_comm_sq ", c^-1 = c^2, "   (the two readings have the SAME Delta-endpoint)\n");
# the two repaired roots differ only by comm^3; check on a generic left factor too
Print("OM2 Frattini_order ", Size(FrattiniSubgroup(Gam)), " ab_generate_Gamma0 ", Group([a,b]) = Gam, "\n");
Print("OM2 comm_central_in_Gamma0 ", ForAll(GeneratorsOfGroup(Gam), g -> g*c = c*g), "\n");
Print("OM2 runtime_ms ", Runtime()-T0, "\n");
QUIT;
