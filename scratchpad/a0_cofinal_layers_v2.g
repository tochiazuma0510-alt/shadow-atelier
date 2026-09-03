# a0_cofinal_layers_v2.g : second structural check (needs the joint group; ~3 min).  Fable 2026-09-03.
# Frattini series of Gamma = ker(Delta -> Q0) (P-block coarse layer), of pc4, and the E4-coordinate images of Delta.
Read("scratchpad/a0_v2_prelude.g");;
FrattiniSeries := function(G)
  local L, H;
  L := [Size(G)]; H := G;
  while Size(H) > 1 do H := FrattiniSubgroup(H); Add(L, Size(H)); od;
  return L;
end;;
Print("LAYERS2 pc3 center ", Size(Center(pc3)), " derived ", Size(DerivedSubgroup(pc3)), " frattini ", FrattiniSeries(pc3), "\n");
Print("LAYERS2 pc4 center ", Size(Center(pc4)), " derived ", Size(DerivedSubgroup(pc4)), " frattini ", FrattiniSeries(pc4), " abinv ", AbelianInvariants(pc4), "\n");
Print("LAYERS2 Gamma order ", Size(Gam), " abinv ", AbelianInvariants(Gam), " exponent ", Exponent(Gam), " class ", NilpotencyClassOfGroup(Gam), " frattini ", FrattiniSeries(Gam), "\n");
for j in [1..10] do
  Print("LAYERS2 coord ", j, " image_order ", Size(Image(proj[j])), " kernel_order ", Size(Kernel(proj[j])), "\n");
od;
img6 := Image(proj[6]);;
Print("LAYERS2 E4coord6 image order ", Size(img6), " abinv ", AbelianInvariants(img6), "\n");
# coarse part of the E4 image: projection to Q4 (first factor of D4)
c4 := RestrictedMapping(Projection(D4,1), img6);;
Print("LAYERS2 E4coord6 coarse(Q4) image order ", Size(Image(c4)), " fine kernel order ", Size(Kernel(c4)), " fine kernel abinv ", AbelianInvariants(Kernel(c4)), " fine kernel frattini ", FrattiniSeries(Kernel(c4)), "\n");
QUIT;
