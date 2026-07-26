#############################################################################
# search/kummer-decide-k3-driver.g -- exact Kummer 判定器・K3 較正用の薄い driver
# 委嘱: 便 34 blocker 2/3/4 (Sol 便 34 P6-E1/K1/C3)。
#
# 身分: 本ファイルは driver である。アルゴリズム本体(IsMthPower/OrdModM/
# KummerCovariance3Check 等)は search/kummer-decide.g(library・凍結対象)
# から Read するだけで、実行と QUIT はここに置く。将来の K5 driver は同じ
# 形の新しい driver ファイルを追加すればよい。
#
# 出力: certificates/k5pipeline/K3-regression-kummer-u.json,
#       certificates/k5pipeline/K3-regression-kummer-uinv.json,
#       certificates/k5pipeline/K3-regression-kummer-cov3.json
#############################################################################

Read("search/kummer-decide.g");

#################### K3 較正ケース ####################
# u = -4 (K3-regression の pathA/pathB 一致値), v := u^{-1} = -1/4.
# COV-2 (X -> X^{-1} / class 反転) 較正: ord(u) と ord(v)=ord(u^{-1}) が
# 一致すること (逆元は群の中で常に同じ位数を持つ -- 位数不変の直接検算)。

K12 := CyclotomicFieldForFactoring(12);;

RunK3Calibration := function()
  local u, v, ordU, ordV, out, cov3;
  u := -4;
  v := u^-1;   # -1/4
  Print("=== kummer-decide K3 calibration (K=Q(zeta_12), M=6) ===\n");
  ordU := OrdModM(K12, 6, u);
  Print("ord(u=-4)      = ", ordU.ord, "  witness = ", ordU.witness, "\n");
  Print("  minimality obstructions (u): ", ordU.minimalityObstructions, "\n");
  ordV := OrdModM(K12, 6, v);
  Print("ord(v=u^-1=-1/4) = ", ordV.ord, "  witness = ", ordV.witness, "\n");
  Print("  minimality obstructions (v): ", ordV.minimalityObstructions, "\n");
  Print("COV-2 class-reversal check: ord(u) = ord(v)? ", ordU.ord = ordV.ord, "\n");
  WriteFile("certificates/k5pipeline/K3-regression-kummer-u.json", KummerCertToJSON("K3-regression-u", K12, 12, 6, u, ordU));
  WriteFile("certificates/k5pipeline/K3-regression-kummer-uinv.json", KummerCertToJSON("K3-regression-uinv", K12, 12, 6, v, ordV));

  # 便 34 P6-C3: 第三 covariance (tau∘[d] + Kummer character 逆冪)。
  # u の witness (ord=3, e^6=u^3) について検査する。
  Print("=== KummerCovariance3Check (K3-regression, w=u=-4, ord=3) ===\n");
  cov3 := KummerCovariance3Check(12, 6, u, ordU.ord, ordU.witness);
  Print("  galoisUnits (Z/12)^x = ", cov3.galoisUnits, "\n");
  Print("  kappaTable (wrt zeta_6=E(6)) = ", cov3.kappaTable, "\n");
  Print("  unitsModM (Z/6)^x = ", cov3.unitsModM, "\n");
  Print("  allMatch (tau in [d] + kappa 逆冪の同時変換で不変)? ", cov3.allMatch, "\n");
  WriteFile("certificates/k5pipeline/K3-regression-kummer-cov3.json", KummerCovariance3ToJSON(cov3));
end;;

RunK3Calibration();

QUIT;
