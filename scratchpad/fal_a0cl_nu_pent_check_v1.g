# fal_a0cl_nu_pent_check_v1.g : falsifier check of two UNKNOWNs declared in a0_cofinal_lift_theorem_v2.md §6 (vi)/(viii):
#  (1) order of Theta(r_x), Theta(r_y) (v460 (1.1)) in the joint roof Delta -> is c_x = r_x^9 a cube of a joint-kernel word (r_x^3 in Omega)?
#      and the orders of their E4-coordinate images (P-block Fox visibility of c_x, c_y);
#  (2) pent(g760) = 1 in e4 under the four natural product conventions of the printed-order pentagon (convention caveat).
Read("scratchpad/a0_v2_prelude.g");;
q := A0V2_QRAW;;
rx := Concatenation(q[1], InvWord(q[6]), InvWord(q[6]), q[7], q[7], q[7], q[7], q[9]);;
ry := Concatenation(InvWord(q[8]), InvWord(q[4]));;
Rx := JointImg(rx);; Ry := JointImg(ry);;
Print("FAL2 Theta(r_x) in Gamma ", Rx in Gam, " order ", Order(Rx), "  Theta(r_y) in Gamma ", Ry in Gam, " order ", Order(Ry), "\n");
Print("FAL2 r_x^3 in Omega (cube trivial in Delta): ", IsOne(Rx^3), "  r_y^3 in Omega: ", IsOne(Ry^3), "\n");
for j in [1..10] do
  Print("FAL2 coord ", j, " image orders of r_x, r_y: ", Order(Image(proj[j], Rx)), " ", Order(Image(proj[j], Ry)), "\n");
od;
g := A0P_G760;;
f := List([1..5], j -> E4img(g, E4pairs[j]));;
# printed-order pentagon (DLL (2.20)): f(x12,x23x24) f(x13x23,x34) = f(x23,x34) f(x12x13,x24x34) f(x12,x23);
# prelude slot order: pair1=(x23,x34) pair2=(x13x12,x34x24) pair3=(x12,x23) pair4=(x23x13,x34) pair5=(x12,x24x23)
L1 := f[5]*f[4];; L2 := f[4]*f[5];; R1 := f[1]*f[2]*f[3];; R2 := f[3]*f[2]*f[1];;
Print("FAL2 pent(g760) in e4: f5f4=f1f2f3 ", L1 = R1, " ; f5f4=f3f2f1 ", L1 = R2, " ; f4f5=f1f2f3 ", L2 = R1, " ; f4f5=f3f2f1 ", L2 = R2, "\n");
Print("FAL2 each occurrence value order: ", List(f, Order), "\n");
QUIT;
