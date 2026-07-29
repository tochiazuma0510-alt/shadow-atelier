#############################################################################
## search/probe/wac_v1/i11_ident.g
##  ideas_011 検分の付録: 「独占」の群を同定する。
##  N^conn((9)) の 36 解 (deg 9, |G| = 324/504/1512) と
##  N^conn((9,1^3)) の 18 解 (deg 12, |G| = 324) の群を名指しする。
##  併せて各成分の genus を Sigma c - n から出す。
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
WacCyc := function(l)
  local i, img, m;
  m := Maximum(l); img := [1..m];
  for i in [1..Length(l)-1] do img[l[i]] := l[i+1]; od;
  img[l[Length(l)]] := l[1];
  return PermList(img);
end;;
WacBlock := function(blocks, len)
  local p, i, base;
  p := (); base := 0;
  for i in [1..blocks] do
    p := p * WacCyc(List([1..len], j -> base+j)); base := base + len;
  od;
  return p;
end;;
NC := function(p, n)
  return n - NrMovedPoints(p) + Length(Cycles(p, MovedPoints(p)));
end;;

Ident := function(nn, sig, label)
  local Snn, k, a, b, G, seen, key, cls, sc, gg;
  Snn := SymmetricGroup(nn); seen := [];
  Print("== ", label, "  (degree ", nn, ") ==\n");
  for k in [0..Int(nn/2)] do
    if k = 0 then cls := [()]; else cls := AsList(ConjugacyClass(Snn, WacBlock(k,2))); fi;
    for a in cls do
      b := a * sig^-1;
      if b^3 = () then
        G := Group(a,b);
        if IsTransitive(G, [1..nn]) then
          key := [k, Size(G)];
          if not key in seen then
            Add(seen, key);
            sc := NC(a,nn) + NC(b,nn) + NC(sig,nn);
            gg := (2*1 - (sc - nn))/2;   ## 2 - 2g = Sigma c - n  =>  g = (2 - (Sc-n))/2
            Print("   a_k=", k, "  |G|=", Size(G));
            if Size(G) <= 2000 and Size(G) <> 1024 then
              Print("  IdGroup=", IdGroup(G));
            else
              Print("  IdGroup=out-of-range");
            fi;
            Print("  ", StructureDescription(G), "\n");
            Print("      primitive? ", IsPrimitive(G,[1..nn]),
                  "   TransId=", TransitiveIdentification(G),
                  "   Sigma c=", sc, " (n+2=", nn+2, ")  genus=", gg, "\n");
          fi;
        fi;
      fi;
    od;
  od;
  return;
end;;

Ident( 9, WacCyc([1..9]), "N^conn((9))");
Ident(12, WacCyc([1..9]), "N^conn((9,1^3))");
Ident(10, WacCyc([1..9]), "N^conn((9,1))");
Ident(11, WacCyc([1..9])*(10,11), "N^conn((9,2))");

Print("\n== (2,2) の消滅は Ree 境界内で起きる(非予算型)==\n");
Print("   n=4, sigma=(2,2): c(sigma)=2 ; sigma even => a even => k even <=2 => k=2, c(a)>=2\n");
Print("   j<=1 => c(b)>=2 ;  min Sigma c = 2+2+2 = 6 = n+2  => Ree は許す\n");
Print("   実際の解: ");
S4 := SymmetricGroup(4);; sig := (1,2)(3,4);; cnt := 0;;
for a in AsList(S4) do
  if a^2 = () then
    b := a*sig^-1;
    if b^3 = () and IsTransitive(Group(a,b),[1..4]) then cnt := cnt + 1; fi;
  fi;
od;
Print(cnt, " 個\n");
Print("   理由: sign(sigma)=+1 => a は偶対合 => a in V4 ; sigma in V4 ; V4 は正規\n");
Print("        => b = a*sigma^-1 in V4 => ord(b) | 2 => b^3=1 は b=1 を強制 => 非推移\n");

Print("\nI11_IDENT_DONE\n");
QUIT;
