# Campaign 138 C5/C6 inventory in the complete installed PerfectGroups range.
# ASCII only.  This script opens no shadow, reduction, or survival outcome.

raw := "search/certs/campaign138_perfect_inventory_v1_raw.txt";
checkpoint := "search/certs/campaign138_perfect_inventory_v1_checkpoint.txt";
PrintTo(checkpoint, "stage=running\n");
PrintTo(raw, "SCHEMA|campaign138_perfect_inventory/v1\n");
AppendTo(raw, "DATABASE_LIMIT|2000000\n");

targetOrder := 504;
totalGroups := 0;
totalHits := 0;

for p in [2, 3] do
  d := 1;
  while targetOrder * p^d <= 2000000 do
    ord := targetOrder * p^d;
    nr := NrPerfectGroups(ord);
    if nr = fail then
      AppendTo(raw, "ORDER|", p, "|", d, "|", ord, "|FAIL\n");
    else
      AppendTo(raw, "ORDER|", p, "|", d, "|", ord, "|", nr, "\n");
      totalGroups := totalGroups + nr;
      for idx in [1..nr] do
        PrintTo(checkpoint, "stage=group\np=", p, "\nd=", d, "\nindex=", idx, "\n");
        g := PerfectGroup(ord, idx);
        rad := SolvableRadical(g);
        q := FactorGroup(g, rad);
        if Size(q) = targetOrder and IsSimpleGroup(q) then
          totalHits := totalHits + 1;
          AppendTo(raw, "HIT|", p, "|", d, "|", ord, "|", idx, "|",
            Size(rad), "|", IsElementaryAbelian(rad), "|", IsAbelian(rad), "|",
            Exponent(rad), "|", StructureDescription(rad), "|",
            StructureDescription(g), "\n");
        fi;
      od;
    fi;
    d := d + 1;
  od;
od;

AppendTo(raw, "TOTAL|", totalGroups, "|", totalHits, "\n");
AppendTo(raw, "DONE\n");
PrintTo(checkpoint, "stage=complete\ncomplete=true\ntotal_groups=", totalGroups,
  "\ntotal_hits=", totalHits, "\n");
QUIT_GAP(0);
