# Lightweight S7 self-check (block system): use a single Blocks() call (not the expensive
# AllBlocks enumeration that timed out) to find ONE minimal nontrivial block system of
# Mperm on 2n points, and report its block size / number of blocks.
Read("search/probe/wac_v1/cbeta_model_indep.g");;
n := 7;;
m := BuildModel(n, 1, (-1) mod n, 1);;
bl := Blocks(m.Mperm, MovedPoints(m.Mperm));;
Print("n=", n, "  Mperm order=", Size(m.Mperm), "\n");
Print("block system (Blocks() minimal nontrivial): ", bl, "\n");
Print("num blocks=", Length(bl), " block size=", Length(bl[1]), "\n");
Print("DONE\n");
