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

  # 便 34 P6-C3 の第三 covariance はここでは走らせない(便 36・裁定 36):
  # KummerCovariance3Check は Sol 便 35 F3 により撤回された誤述語である
  # (Gal(K/Q) の K 内自己同型であって G_K 上の Kummer character ではない)。
  # 後継は search/kummer-cov3-actual.g(rho_0/tau/j の実値 covariance・
  # 射程限定を明記)。
end;;

RunK3Calibration();

QUIT;
