# [規約照合] 正典 (1.11)(1.12) の Ad の向きと alpha_i^2 の一致先
# 正典 照合_B3表示_T2土台 §1-§4:  Ad(g)(w) = g w g^-1  (左)・「逆向きなし」と明記
SizeScreen([4096,0]);;
F := FreeGroup("x","y");; x := F.1;; y := F.2;;

# 左規約 (sigma_i 共役) : (1.11) 第1形 / (1.12) 第1形  ※ c は K^(9) で消える
al1 := GroupHomomorphismByImages(F,F,[x,y],[x, y^-1*x^-1]);;
al2 := GroupHomomorphismByImages(F,F,[x,y],[x^-1*y^-1, y]);;
# 右規約 (sigma_i^-1 共役) : (1.11) 第2形 / (1.12) 第2形  ※ 語順が入れ替わる
be1 := GroupHomomorphismByImages(F,F,[x,y],[x, x^-1*y^-1]);;
be2 := GroupHomomorphismByImages(F,F,[x,y],[y^-1*x^-1, y]);;

Show := function(name,a1,a2,g)
  local sq, L, R;
  Print("=== ",name," ===\n");
  Print("  a1(y) = ", Image(a1,y), "   a2(x) = ", Image(a2,x), "\n");
  Print("  braid a1 a2 a1 = a2 a1 a2 : ", a1*a2*a1 = a2*a1*a2, "\n");
  sq := a1*a1;;
  L := Image(sq,y);;
  Print("  a1^2(y) = ", L, "\n");
  Print("     = x y x^-1 (LEFT  Ad(x))  : ", L = x*y*x^-1, "\n");
  Print("     = x^-1 y x (RIGHT y^x)    : ", L = x^-1*y*x, "\n");
  sq := a2*a2;;
  L := Image(sq,x);;
  Print("  a2^2(x) = ", L, "\n");
  Print("     = y x y^-1 (LEFT  Ad(y))  : ", L = y*x*y^-1, "\n");
  Print("     = y^-1 x y (RIGHT x^y)    : ", L = y^-1*x*y, "\n");
end;;
Show("LEFT  : alpha (sigma_i conj, canon (1.11)/(1.12) 1st form)", al1, al2, x);
Show("RIGHT : beta  (sigma_i^-1 conj, 2nd form)", be1, be2, x);
Print("=== 群としての一致 ===\n");
Print("  beta_i = alpha_i^-1 ? : ", be1 = al1^-1, " / ", be2 = al2^-1, "\n");
QUIT;
