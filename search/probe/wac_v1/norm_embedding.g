#############################################################################
## search/probe/wac_v1/norm_embedding.g
##  P86-7-1: NORM の structural-embedding を測定で決める。
##  写像  Xi : GTSh(N,N) -> N_{S_n}(<xbar>) ,  [m,f] |-> alpha
##  ここで alpha は Aut(P)=S_n の一意の元で
##      xbar^alpha = xbar^(2m+1),      ybar^alpha = (ybar^(2m+1))^f
##  (= E_{m,f} を実現する共役元)。 charming ゆえ alpha in N_{S_n}(<xbar>)。
##  検査: (a) 全 shadow で alpha が存在・一意  (b) 準同型性(左右両規約を試す)
##        (c) 核 = 1  (d) 像が N_{S_n}(<xbar>) の部分群で位数 = |GTSh|
##  Single lane (GAP 4.16.0). NOT a ledger claim. No commit.
#############################################################################
OUT := "search/certs/norm_embedding_20260731.json";;
recs := [];;

DoWindow := function(nn, a1, b1, wid)
  local Snn, aE, bE, s1, s2, xb, yb, PN, Nord, charm, Stab, CPy, CSy, NX,
        gm, hm, m, q, al, cc, f, sh, alphas, i, j, s, t, m3, f3, a3L, a3R,
        okL, okR, img, t0, cnt, kersz, tot, CPyL, oddc, cset;
  Snn := SymmetricGroup(nn);
  aE := a1*(nn+1,nn+3); bE := b1*(nn+1,nn+3,nn+2);
  s1 := bE^-1*aE; s2 := aE*bE^2;
  xb := s1^2; yb := s2^2; PN := Group(xb,yb);
  Nord := Order(xb);
  charm := Filtered([0..Nord-1], z -> GcdInt(2*z+1, Nord) = 1);
  Stab := Centralizer(Snn, xb);
  CSy := Centralizer(Snn, yb);
  CPy := Intersection(CSy, AlternatingGroup(nn));
  CPyL := Elements(CPy);
  oddc := First(Elements(CSy), z -> SignPerm(z) = -1);
  NX := Normalizer(Snn, Group(xb));
  Print("== ", wid, "  n=", nn, " N_ord=", Nord, " |Stab|=", Size(Stab),
        " |C_P(y)|=", Size(CPy), " |N(<x>)|=", Size(NX), "\n");
  sh := [];
  for m in charm do
    q := 2*m+1;
    gm := RepresentativeAction(Snn, xb, xb^q);
    hm := RepresentativeAction(Snn, yb, yb^q);
    if gm = fail or hm = fail then Print("   m=",m," rep fail\n"); continue; fi;
    for al in Elements(Stab) do
      al := al*gm;
      ## sign(f) = sign(hm)*sign(c)*sign(al) = 1  =>  sign(c) = sign(hm)*sign(al)
      if SignPerm(hm)*SignPerm(al) = 1 then cset := CPyL;
      elif oddc <> fail then cset := List(CPyL, z -> oddc*z);
      else cset := []; fi;
        for cc in cset do
          f := hm^-1*cc*al;
          if s1^q*f^-1*s2^q*f = f^-1*s1*s2*xb^(-m) and
             f^-1*s2^q*f*s1^q = s2*s1*yb^(-m)*f then
            if Group(xb^q, (yb^q)^f) = PN then
              Add(sh, rec(m := m, f := f, al := al));
            fi;
          fi;
        od;
      fi;
    od;
  od;
  tot := Length(sh);
  kersz := Number(sh, z -> z.m = 0);
  alphas := Set(List(sh, z -> z.al));
  ## (a) alpha の定義的性質(再 assert)
  t0 := ForAll(sh, z -> xb^(z.al) = xb^(2*z.m+1) and
                        yb^(z.al) = (yb^(2*z.m+1))^(z.f));
  ## (b) 準同型性: (3.53) の合成と alpha の積を突合
  okL := true; okR := true;
  for i in [1..tot] do
    for j in [1..tot] do
      s := sh[i]; t := sh[j];
      m3 := (2*s.m*t.m + s.m + t.m) mod Nord;
      f3 := s.f * (t.f^(s.al));
      a3L := s.al * t.al;
      a3R := t.al * s.al;
      if not (xb^a3L = xb^(2*m3+1) and yb^a3L = (yb^(2*m3+1))^f3) then
        okL := false; fi;
      if not (xb^a3R = xb^(2*m3+1) and yb^a3R = (yb^(2*m3+1))^f3) then
        okR := false; fi;
      if not okL and not okR then break; fi;
    od;
    if not okL and not okR then break; fi;
  od;
  img := Group(alphas);
  Add(recs, rec(window_id := wid, n := nn, N_ord := Nord,
    stab_order := Size(Stab), cpy_order := Size(CPy),
    normalizer_order := Size(NX),
    shadow_total := tot, ker_size := kersz,
    alpha_well_defined := t0,
    distinct_alphas := Length(alphas),
    kernel_trivial := (Length(alphas) = tot),
    hom_left := okL, hom_right := okR,
    image_order := Size(img),
    image_is_subgroup_of_normalizer := IsSubgroup(NX, img),
    image_order_eq_gtsh := (Size(img) = tot),
    image_set_closed := (Size(img) = Length(alphas))));
  Print("   |GTSh|=", tot, " |ker|=", kersz, " distinct alpha=", Length(alphas),
        " ker(Xi)=1? ", Length(alphas)=tot, "\n");
  Print("   alpha well-defined ", t0, "   hom(left) ", okL, "   hom(right) ", okR,
        "\n");
  Print("   |image|=", Size(img), "  <= N(<x>)? ", IsSubgroup(NX, img),
        "  = |GTSh|? ", Size(img)=tot, "\n");
  return;
end;;

## ---- 梯子 canonical 4 (N_ord=9) ----
DoWindow(10, ( 1, 2)( 3, 5)( 4,10)( 6, 9), ( 2, 9, 5)( 3, 4,10)( 6, 8, 7),
         "W-E-A10-9t1");
DoWindow(11, ( 2,11)( 3, 8)( 4, 5)( 6, 7)( 9,10), ( 1, 9,11)( 2,10, 8)( 3, 7, 5),
         "W-E-A11-9t2");
DoWindow(12, ( 3, 9)( 4,11)( 5, 7)( 6,12)( 8,10),
         ( 1, 9, 2)( 3, 8,11)( 4,10, 7)( 5, 6,12), "W-E-A12-9t3");
DoWindow(13, ( 2,10)( 3, 8)( 4,12)( 5, 6)( 7,13)( 9,11),
         ( 1, 9,10)( 2,11, 8)( 3, 7,12)( 4,13, 6), "W-E-A13-9t4");
## ---- I10-1 2 窓 (N_ord=5) ----
DoWindow(10, ( 1, 2)( 3, 6)( 7,10), ( 2,10, 6)( 3, 5, 4)( 7, 9, 8),
         "W-E-A10-5x2t0");
DoWindow(15, ( 1, 4)( 5, 9)( 6,15)( 7,13)( 8,11),
         ( 1, 3, 2)( 4,10, 9)( 5, 8,15)( 6,14,13)( 7,12,11), "W-E-A15-5x3t0");
## ---- D 族 3 窓 ----
DoWindow(16, ( 1, 2)( 3,14)( 4,10)( 5,12)( 6, 8)( 7,16)( 9,13)(11,15),
         ( 2,11,14)( 3,15,10)( 4, 9,12)( 5,13, 8)( 6, 7,16), "W-D-A16-11a");
DoWindow(18, ( 1,17)( 2, 6)( 3,14)( 5,15)( 7,16)( 8,13)(10,12)(11,18),
         ( 1,16, 6)( 2, 5,14)( 3,15, 4)( 7,17,13)( 8,12, 9)(10,11,18),
         "W-D-A18-13a");
DoWindow(20, ( 1, 7)( 2,16)( 3, 5)( 4,20)( 6,17)( 8, 9)(10,15)(11,19)(12,13)(14,18),
         ( 1, 6,16)( 2,17, 5)( 3, 4,20)( 7,15, 9)(10,14,19)(11,18,13),
         "W-D-A20-15a");

## ---- 証明書 ----
str := "";; out := OutputTextString(str, true);;
AppendTo(out, "{\"schema\":\"norm-embedding/v1\",\"generated_by\":\"search/probe/wac_v1/norm_embedding.g\",\"note\":\"Xi : GTSh -> N_{S_n}(<xbar>), [m,f] |-> alpha with xbar^alpha=xbar^(2m+1), ybar^alpha=(ybar^(2m+1))^f. Raw measurement, GAP single lane, NOT a ledger claim.\",\"windows\":[");
for i in [1..Length(recs)] do
  r := recs[i];
  if i > 1 then AppendTo(out, ","); fi;
  AppendTo(out, "{\"window_id\":\"", r.window_id, "\",\"n\":", r.n,
    ",\"N_ord\":", r.N_ord, ",\"stab_order\":", r.stab_order,
    ",\"cpy_order\":", r.cpy_order, ",\"normalizer_order\":", r.normalizer_order,
    ",\"shadow_total\":", r.shadow_total, ",\"ker_size\":", r.ker_size,
    ",\"alpha_well_defined\":", String(r.alpha_well_defined),
    ",\"distinct_alphas\":", r.distinct_alphas,
    ",\"kernel_trivial\":", String(r.kernel_trivial),
    ",\"hom_left\":", String(r.hom_left), ",\"hom_right\":", String(r.hom_right),
    ",\"image_order\":", r.image_order,
    ",\"image_is_subgroup_of_normalizer\":", String(r.image_is_subgroup_of_normalizer),
    ",\"image_order_eq_gtsh\":", String(r.image_order_eq_gtsh),
    ",\"image_set_closed\":", String(r.image_set_closed), "}");
od;
AppendTo(out, "]}\n");
CloseStream(out);
FileString(OUT, str);
Print("\nwrote ", OUT, "\n");
Print("NORM_EMBEDDING_DONE\n");
QUIT;
