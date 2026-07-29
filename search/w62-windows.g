#############################################################################
## search/w62-windows.g -- W6-2 の窓仕様(strike-a{16,18,20}.g から逐語)
## 生成対 (a1,b1) と s1 = b^-1 a, s2 = a^-1 b^2 の構成は 3 本の strike script と
## 同一パターン。ここでは共有の窓表と組み立て関数だけを置く。
#############################################################################

W62_WINDOWS := [
 rec(id := "W-D-A16-11a", n := 16,
     a1 := ( 1, 2)( 3,14)( 4,10)( 5,12)( 6, 8)( 7,16)( 9,13)(11,15),
     b1 := ( 2,11,14)( 3,15,10)( 4, 9,12)( 5,13, 8)( 6, 7,16)),
 rec(id := "W-D-A18-13a", n := 18,
     a1 := ( 1,17)( 2, 6)( 3,14)( 5,15)( 7,16)( 8,13)(10,12)(11,18),
     b1 := ( 1,16, 6)( 2, 5,14)( 3,15, 4)( 7,17,13)( 8,12, 9)(10,11,18)),
 rec(id := "W-D-A20-15a", n := 20,
     a1 := ( 1, 7)( 2,16)( 3, 5)( 4,20)( 6,17)( 8, 9)(10,15)(11,19)(12,13)(14,18),
     b1 := ( 1, 6,16)( 2,17, 5)( 3, 4,20)( 7,15, 9)(10,14,19)(11,18,13))
];;

# 環境変数 W62_ONLY で 1 窓を選ぶ
W62_GetWindow := function()
  local id, sel;
  if IsBound(GAPInfo.SystemEnvironment) and IsBound(GAPInfo.SystemEnvironment.W62_ONLY) then
    id := GAPInfo.SystemEnvironment.W62_ONLY;
  else
    Error("w62-windows: 環境変数 W62_ONLY が未設定");
  fi;
  sel := Filtered(W62_WINDOWS, w -> w.id = id);
  if Length(sel) <> 1 then Error("w62-windows: 窓 ID 不一致: ", id); fi;
  return sel[1];
end;;

# 窓 spec -> kerchi-judge の W レコード
W62_MakeW := function(wspec)
  local An, S3, D, embA, embS, agen, bgen, s1, s2;
  An := AlternatingGroup(wspec.n);
  S3 := SymmetricGroup(3);
  D := DirectProduct(An, S3);
  embA := Embedding(D, 1);  embS := Embedding(D, 2);
  agen := Image(embA, wspec.a1) * Image(embS, (1,3));
  bgen := Image(embA, wspec.b1) * Image(embS, (1,3,2));
  s1 := bgen^-1 * agen;
  s2 := agen^-1 * bgen^2;
  return MakeWindow(s1, s2);
end;;
